from itertools import combinations
from functools import cache, wraps
from collections import Counter
from typing_extensions import TypeVar, ParamSpec, Callable
from io import BufferedReader
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm
from rich.console import Console
from rich.progress import track
from rich.table import Table
from colorama import Fore, Style, init
import argparse
import math
import pickle
import glob
import logging
import warnings

N: int = 26
EPS: float = 1e-9
POP_CACHE_LOADED: bool = False
LAST_LOADED: int = 1
init(autoreset=True)

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


_T = TypeVar("_T")
_P = ParamSpec("_P")


def cached(func: Callable[_P, _T]):
    def load_pop_cache(func: Callable[_P, _T]):
        try:
            global POP_CACHE_LOADED
            log_info("Attempting to load POP cache...")
            pop_cache: BufferedReader = open("popCache.dat", "rb")
            func.cache = pickle.load(pop_cache)  # type: ignore
            pop_cache.close()
            POP_CACHE_LOADED = True
            log_success("POP Cache Loaded!")
        except:
            log_warning("Failed to load POP cache!")

    def load_prob_cache(func: Callable[_P, _T]):
        try:
            global LAST_LOADED
            log_info("Attempting to load probability cache...")
            prob_cache_files: list[str] = glob.glob("probCache*.dat")
            latest_file: str = max(
                prob_cache_files,
                key=lambda f: int(f.replace("probCache", "").replace(".dat", "")),
            )
            LAST_LOADED = (
                int(latest_file.replace("probCache", "").replace(".dat", "")) + 1
            )
            prob_cache: BufferedReader = open(latest_file, "rb")
            func.cache = pickle.load(prob_cache)  # type: ignore
            prob_cache.close()
            log_success(f"Probability Cache Loaded for i = {LAST_LOADED - 1}!")
        except:
            log_warning("Failed to load probability cache!")

    func.cache = {}  # type: ignore

    if func.__name__ == "get_transitive_prob":
        load_prob_cache(func)

    if func.__name__ == "partition_of_partition":
        load_pop_cache(func)

    @wraps(func)
    def wrapper(*args):
        try:
            return func.cache[args]
        except KeyError:
            func.cache[args] = result = func(*args)
            return result

    return wrapper


@cached
def tuple_remove_subset(t1: tuple[_T, ...], t2: tuple[_T, ...]) -> tuple[_T, ...]:
    result: list[_T] = list(t1)
    for thing in t2:
        result.remove(thing)
    return tuple(result)


@cached
def partition_of_partition(
    p: tuple[int, ...], target_p: tuple[int, ...]
) -> set[tuple[tuple[int, ...], ...]]:
    result: set[tuple[tuple[int, ...], ...]] = set()
    if len(target_p) == len(p) == 0:
        result.add(tuple())

    if len(target_p) == 0 or len(p) == 0:
        return result

    head: int = target_p[0]
    tail: tuple[int, ...] = target_p[1:]
    for partition in IPS[head]:
        if len(Counter(partition) - Counter(p)) == 0:
            suffixes: set[tuple[tuple[int, ...], ...]] = partition_of_partition(
                tuple_remove_subset(p, partition), tail
            )
            for suffix in suffixes:
                result.add((partition,) + suffix)
    return result


@cached
def generate_integer_partitions(n: int) -> list[tuple[int, ...]]:
    result: set[tuple[int, ...]] = set()
    result.add((n,))

    for i in range(1, n):
        for p in generate_integer_partitions(n - i):
            result.add(tuple((sorted((i,) + p))))

    return list(result)


@cached
def partition_to_multiplicity(p: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(Counter(p).items())


@cached
def num_of_partition(p: tuple, n: int) -> int:
    result: float = float(math.factorial(n))
    p_m: tuple[tuple[int, int], ...] = partition_to_multiplicity(p)
    for i, k_i in p_m:
        result /= math.pow(math.factorial(i), k_i) * math.factorial(k_i)
    return int(result)


@cached
def num_of_cycle_type(p: tuple[int, ...], n: int) -> int:
    result: float = float(math.factorial(n))
    p_m: tuple[tuple[int, int], ...] = partition_to_multiplicity(p)
    for i, k_i in p_m:
        result /= math.pow(i, k_i) * math.factorial(k_i)
    return int(result)


@cached
def cycle_type_prob(p: tuple[int, ...], n: int) -> float:
    result: float = 1.0
    p_m: tuple[tuple[int, int], ...] = partition_to_multiplicity(p)
    for i, k_i in p_m:
        result /= math.pow(i, k_i) * math.factorial(k_i)
    return result


@cached
def partitions_to_search_space(p1: tuple[int, ...], p2: tuple[int, ...], n: int) -> int:
    return num_of_cycle_type(p1, n) * num_of_cycle_type(p2, n)


@cached
def get_transitive_prob(
    p1: tuple[int, ...],
    p2: tuple[int, ...],
    n: int,
) -> float:
    if len(p1) == 1 or len(p2) == 1:
        return 1.0

    psearchsize: float = float(partitions_to_search_space(p1, p2, n))
    result: float = psearchsize

    for partition in IPS[n]:
        if len(partition) == 1:
            continue

        c1_pop: set[tuple[tuple[int, ...], ...]] = partition_of_partition(p1, partition)
        c2_pop: set[tuple[tuple[int, ...], ...]] = partition_of_partition(p2, partition)

        if len(c1_pop) == 0 or len(c2_pop) == 0:
            continue

        result -= sum(
            [
                math.prod(
                    [
                        partitions_to_search_space(s1, s2, i)
                        * get_transitive_prob(s1, s2, i)
                        for i, (s1, s2) in zip(partition, group)
                    ]
                )
                for group in [tuple(zip(c1, c2)) for c1 in c1_pop for c2 in c2_pop]
            ]
        ) * num_of_partition(partition, n)

    result /= psearchsize
    return result


@cached
def get_simple_transitive_prob(n: int) -> float:
    if n == 1:
        return 1.0

    psearchsize: float = math.pow(math.factorial(n), 2)
    result: float = psearchsize

    for partition in IPS[n]:
        if len(partition) == 1:
            continue

        result -= math.prod(
            [
                math.pow(math.factorial(val), 2) * get_simple_transitive_prob(val)
                for val in partition
            ]
        ) * num_of_partition(partition, n)

    result /= psearchsize

    return result


log_info("Generating all integer partitions...")
IPS: list[list[tuple[int, ...]]] = [
    generate_integer_partitions(i) for i in range(N + 1)
]
log_success("Generated!")


def main() -> None:
    if not POP_CACHE_LOADED:
        for i in range(1, N + 1):
            pop_pairs: list[tuple[tuple[int, ...], tuple[int, ...]]] = [
                (IPS[i][j1], IPS[i][j2])
                for j1 in range(len(IPS[i]))
                for j2 in range(j1, len(IPS[i]))
            ]

            with tqdm(total=len(pop_pairs), desc=f"Processing POPs {i}") as pbar:
                for p1, p2 in pop_pairs:
                    partition_of_partition(p1, p2)
                    pbar.update(1)

        pop_cache = open("popCache.dat", "wb")
        pickle.dump(partition_of_partition.cache, pop_cache)
        pop_cache.close()

        log_success("Saved POP cache!")

    for i in range(LAST_LOADED, N + 1):
        prob_pairs: list[tuple[tuple[int, ...], tuple[int, ...]]] = [
            (IPS[i][j1], IPS[i][j2])
            for j1 in range(len(IPS[i]))
            for j2 in range(j1, len(IPS[i]))
        ]
        with tqdm(total=len(prob_pairs), desc=f"Processing pairs {i}") as pbar:
            for p1, p2 in prob_pairs:
                get_transitive_prob(p1, p2, i)
                pbar.update(1)
        prob_cache = open(f"probCache{i}.dat", "wb")
        pickle.dump(get_transitive_prob.cache, prob_cache)
        prob_cache.close()
        log_success(f"Saved probability cache for i = {i}!")


def test() -> None:
    t_i = [get_simple_transitive_prob(i) for i in range(26)]
    total = 0
    for ip in IPS[26]:
        if sorted(ip) != sorted((26,)):
           pm = partition_to_multiplicity(ip)
           prod = 1
           for i, m_i in pm:
               prod *= (math.factorial(i)*t_i[i-1])**m_i/math.factorial(m_i)
           total += prod
    total /= math.factorial(26)
    print(1- total)

    
    # console = Console()

    # results = []

    # for i in track(range(1, N + 1), description="Running tests..."):
    #     simple_prob: int = get_simple_transitive_prob(i)

    #     calculated_prob: float = 0.0
    #     for j1 in range(len(IPS[i])):
    #         for j2 in range(j1, len(IPS[i])):
    #             if j1 != j2:
    #                 calculated_prob += 2 * (
    #                     cycle_type_prob(IPS[i][j1], i)
    #                     * cycle_type_prob(IPS[i][j2], i)
    #                     * get_transitive_prob(IPS[i][j1], IPS[i][j2], i)
    #                 )
    #             else:
    #                 calculated_prob += (
    #                     cycle_type_prob(IPS[i][j1], i)
    #                     * cycle_type_prob(IPS[i][j2], i)
    #                     * get_transitive_prob(IPS[i][j1], IPS[i][j2], i)
    #                 )
    #     passed = abs(calculated_prob - simple_prob) < EPS
    #     results.append((i, simple_prob, calculated_prob, passed))

    # table = Table(title="Test Results")
    # table.add_column("N", justify="right", style="cyan", no_wrap=True)
    # table.add_column("Simple Prob", justify="right", style="magenta")
    # table.add_column("Calculated Prob", justify="right", style="yellow")
    # table.add_column("Status", justify="center", style="green")

    # for i, simple_prob, calculated_prob, passed in results:
    #     status = (
    #         "[bold green]PASS[/bold green]" if passed else "[bold red]FAIL[/bold red]"
    #     )
    #     table.add_row(str(i), f"{simple_prob:.6f}", f"{calculated_prob:.6f}", status)

    # num_failures = sum(1 for _, _, _, passed in results if not passed)
    # console.print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["main", "test"],
        default="main",
        help="Specify the mode to run: 'main' (default) to execute the main function, "
        "or 'test' to run unit tests.",
    )
    parser.add_argument(
        "--N",
        type=int,
        default=26,
        help="Highest value of transitive probability to compute",
    )

    args = parser.parse_args()

    N = args.N

    if args.mode == "test":
        test()
    else:
        main()
