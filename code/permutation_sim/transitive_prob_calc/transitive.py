from itertools import combinations
from functools import cache
from collections import Counter
from typing import TypeVar
from tqdm import tqdm
import math


_T = TypeVar("_T")


@cache
def tuple_remove_subset(t1: tuple[_T, ...], t2: tuple[_T, ...]) -> tuple[_T, ...]:
    result: list[_T] = list(t1)
    for thing in t2:
        result.remove(thing)
    return tuple(result)


@cache
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


@cache
def generate_integer_partitions(n: int) -> list[tuple[int, ...]]:
    result: set[tuple[int, ...]] = set()
    result.add((n,))

    for i in range(1, n):
        for p in generate_integer_partitions(n - i):
            result.add(tuple((sorted((i,) + p))))

    return list(result)


@cache
def partition_to_multiplicity(p: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(Counter(p).items())


@cache
def num_of_partition(p: tuple, n: int) -> int:
    result: float = float(math.factorial(n))
    p_m: tuple[tuple[int, int], ...] = partition_to_multiplicity(p)
    for i, k_i in p_m:
        result /= math.pow(math.factorial(i), k_i) * math.factorial(k_i)
    return int(result)


@cache
def num_of_cycle_type(p: tuple[int, ...], n: int) -> int:
    result: float = float(math.factorial(n))
    p_m: tuple[tuple[int, int], ...] = partition_to_multiplicity(p)
    for i, k_i in p_m:
        result /= math.pow(i, k_i) * math.factorial(k_i)
    return int(result)


@cache
def partitions_to_search_space(p1: tuple[int, ...], p2: tuple[int, ...], n: int) -> int:
    return num_of_cycle_type(p1, n) * num_of_cycle_type(p2, n)


@cache
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


N: int = 26

# This thing never changes
print("Generating all integer partitions...")
IPS: list[list[tuple[int, ...]]] = [generate_integer_partitions(i) for i in range(N + 1)]
print("Generated!")


def main() -> None:
    for i in range(1, N + 1):
        pairs: list[tuple[tuple[int, ...], tuple[int, ...]]] = [
            (IPS[i][j1], IPS[i][j2])
            for j1 in range(len(IPS[i]))
            for j2 in range(j1, len(IPS[i]))
        ]
        with tqdm(total=len(pairs), desc=f"Processing pairs {i}") as pbar:
           for p1, p2 in pairs:
               get_transitive_prob(p1, p2, i)
               pbar.update(1)


if __name__ == "__main__":
    main()
