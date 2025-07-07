from itertools import combinations_with_replacement, combinations
from collections import defaultdict, Counter
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from colorama import Fore, Style, init
from pyenigma import *
import networkx as nx
import numpy as np
import io
import os.path
import math
import time
import random
import warnings
import logging
import pickle
import argparse
import string

EPS: float = 1e-3
PATIENCE: int = 30

ROTORS = [
    rotor.ROTOR_I,
    rotor.ROTOR_II,
    rotor.ROTOR_III,
    rotor.ROTOR_IV,
    rotor.ROTOR_V,
]

init(autoreset=True)

warnings.simplefilter("ignore", Warning)
warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

LOG_FORMAT = "[%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

logger = logging.getLogger("PartitionLogger")


def log_success(message: str):
    logger.info(Fore.GREEN + message)


def log_warning(message: str):
    logger.warning(Fore.YELLOW + message)


def log_error(message: str):
    logger.error(Fore.RED + message)


def log_info(message: str):
    logger.info(Fore.CYAN + message)


def generate_integer_partitions(n: int) -> list[tuple[int, ...]]:
    result: set[tuple[int, ...]] = set()
    result.add((n,))

    for i in range(1, n):
        for p in generate_integer_partitions(n - i):
            result.add(tuple((sorted((i,) + p))))

    return list(result)


def partition_to_multiplicity(p: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(Counter(p).items())


def generate_disjoint_transpositions(n: int) -> list[tuple[int, int]]:
    # Initialize the list with numbers from 0 to n-1
    numbers: list[int] = list(range(n))
    transpositions: list[tuple[int, int]] = []

    while len(numbers) > 1:
        # Randomly select two distinct indices for transposition
        i, j = random.sample(numbers, 2)

        # Add the transposition (i, j) to the list of transpositions
        transpositions.append((i, j))
        transpositions.append((j, i))

        # Remove the transposed elements from the list
        numbers.remove(i)
        numbers.remove(j)
    transpositions.sort(key=lambda x: x[0])

    return transpositions


def generate_engima_transpositions(
    n: int, offset: int, reflector: rotor.Reflector, rotors: list[rotor.Rotor], key: str
) -> list[tuple[int, int]]:
    transpositions: list[tuple[int, int]] = []

    for i in range(int(n)):
        i_as_chr = chr(0x41 + i)

        # Initialize new Enigma
        e = enigma.Enigma(reflector, rotors[0], rotors[1], rotors[2], key, plugs="")
        e.encipher("a" * offset)

        sig_i_as_char = e.encipher(i_as_chr)
        sig_i = ord(sig_i_as_char) - 0x41

        transpositions.append((i, sig_i))
        transpositions.append((sig_i, i))
    transpositions.sort(key=lambda x: x[0])
    return list(set(transpositions))


def create_enigma_graph(n: int, l: int) -> nx.Graph:
    G: nx.Graph = nx.Graph()

    # Create l columns of n nodes
    for col in range(l):
        for node in range(n):
            G.add_node((col, node))

    # Choose l random offsets
    offsets = random.sample(range(17), k=l)
    rotor_choice = random.sample(ROTORS, k=3)
    key_choice = "".join(random.choices(string.ascii_uppercase, k=3))

    # Connect nodes within each column to the next via random transpositions
    for col in range(l - 1):
        transpositions: list[tuple[int, int]] = generate_engima_transpositions(
            n,
            offsets[col],
            rotor.ROTOR_Reflector_B,
            rotor_choice,
            key_choice,
        )

        for i, j in transpositions:
            G.add_edge((col, i), (col + 1, j))

    for node in range(n):
        G.add_edge((0, node), (l - 1, node), color="invis")  # Invisible edges

    return G


def create_graph_with_transpositions(n: int, l: int) -> nx.Graph:
    G: nx.Graph = nx.Graph()

    # Create l columns of n nodes
    for col in range(l):
        for node in range(n):
            G.add_node((col, node))

    # Connect nodes within each column to the next via random transpositions
    for col in range(l - 1):
        transpositions: list[tuple[int, int]] = generate_disjoint_transpositions(n)
        for i, j in transpositions:
            G.add_edge((col, i), (col + 1, j))

    for node in range(n):
        G.add_edge((0, node), (l - 1, node), color="invis")  # Invisible edges

    return G


def get_cycle_type(G: nx.Graph) -> tuple[int, ...]:
    components: list[set[tuple[int, ...]]] = list(nx.connected_components(G))
    cycle_type: list[int] = []
    for component in components:
        s = 0
        for node in component:
            if node[0] == 0:
                s += 1
        cycle_type.append(s)
    return tuple(sorted(cycle_type))


def total_variation_distance(d1, d2) -> float:
    keys = set(d1.keys()).union(set(d2.keys()))
    return sum(abs(d1.get(k, 0) - d2.get(k, 0)) for k in keys) / 2


def collect_cycle_types(n: int, l: int, num_sims: int, enigma: bool = False):
    # Collect cycle types and their counts
    cycles_seen = {}
    prev_d = {}
    iters = 0
    change_count = 0
    steady_state = False

    tvd_history = []
    time_history = []
    start_time = time.time()

    with Progress(
        TextColumn("[progress.description]{task.description}", style="bold blue"),
        BarColumn(bar_width=50),
        TextColumn("[TVD] {task.fields[tvd]:.6e}", style="bold magenta"),
    ) as progress:
        task = progress.add_task(f"Collecting cycles l={l}", total=None, tvd=0.00)
        for i in range(1, num_sims + 1):
            if enigma:
                G = create_enigma_graph(n, l+1)
            else:
                G = create_graph_with_transpositions(n, l + 1)
            cycle_type = get_cycle_type(G)
            try:
                cycles_seen[cycle_type] += 1
            except KeyError:
                cycles_seen[cycle_type] = 1

            if i % 1000 == 0:
                current_d = {cycle: count / i for cycle, count in cycles_seen.items()}

                dist_change = total_variation_distance(prev_d, current_d)

                progress.update(task, tvd=dist_change)

                if dist_change < EPS:
                    change_count += 1
                else:
                    change_count = 0

                prev_d = current_d

                if change_count >= PATIENCE:
                    iters = i
                    steady_state = True
                    break

    if steady_state:
        log_success(f"Reached steady state after {i} iterations")
    else:
        log_warning(f"Failed to reach steady state in {num_sims} iterations")

    total_sims = sum(cycles_seen.values())
    return {cycle: count / total_sims for cycle, count in cycles_seen.items()}


def main(n: int, num_sims: int) -> None:
    for i in range(2, 17):
        # Check if file was previously cached
        if os.path.isfile(f"collectedCycles{i}.dat"):
            log_info(f"Cycles for l={i} were previously cached, skipping...")
        else:
            log_info(f"Collecting cycles for l={i}")
            got_cycles = collect_cycle_types(n, i, num_sims)
            collected_cycles = open(f"collectedCycles{i}.dat", "wb")
            pickle.dump(got_cycles, collected_cycles)
            collected_cycles.close()
            log_success(f"Saved cycle collection cache for l={i}")


# Computes distribution from real Enigma machines rather than randomized permutations
# This gives much better results in the case when l = 2
def enigma_distribution(n: int, num_sims: int) -> None:
    for i in range(2, 17):
        # Check if file was previously cached
        if os.path.isfile(f"enigmaCycles{i}.dat"):
            log_info(f"Cycles for l={i} were previously cached, skipping...")
        else:
            log_info(f"Collecting cycles for l={i}")
            got_cycles = collect_cycle_types(n, i, num_sims, enigma=True)
            collected_cycles = open(f"enigmaCycles{i}.dat", "wb")
            pickle.dump(got_cycles, collected_cycles)
            collected_cycles.close()
            log_success(f"Saved cycle collection cache for l={i}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--N",
        type=int,
        default=26,
        help="Size of S_n to compute",
    )

    parser.add_argument(
        "--SIMS",
        type=int,
        default=1e12,
        help="Maximum number of simulations to run in collecting cycle types",
    )

    args = parser.parse_args()

    n = args.N
    num_sims = int(args.SIMS)

    main(n, num_sums)
