from itertools import combinations
from functools import cache, wraps
from collections import Counter
from typing import TypeVar
from tqdm import tqdm
import math
import pickle

_T = TypeVar("_T")

def cached(func):
    func.cache = {}
    @wraps(func)
    def wrapper(*args):
        key = tuple(sorted(args, key=lambda x: repr(x)))
        try:
            return func.cache[key]
        except KeyError:
            func.cache[key] = result = func(*args)
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
        p: tuple[int,...],
        target_p: tuple[int,...]
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

def load_pop_cache():
    try:
        print("Attempting to load POP cache...")
        pop_cache = open("popTestCache.dat", 'rb')
        partition_of_partition.cache = pickle.load(pop_cache)
        pop_cache.close()
        print("POP Cache Loaded!")
        return True
    except:
        print("Failed to load POP cache!")
        return False

def load_prob_cache():
    try:
        print("Attempting to load probability cache...")
        pop_cache = open("probTestCache.dat", 'rb')
        get_transitive_prob.cache = pickle.load(pop_cache)
        pop_cache.close()
        print("Probability Cache Loaded!")
        return True
    except:
        print("Failed to load probability cache!")
        return False

N: int = 26

# This thing never changes
print("Generating all integer partitions...")
IPS: list[list[tuple[int, ...]]] = [generate_integer_partitions(i) for i in range(N + 1)]
print("Generated!")

def main() -> None:
    precached_pop = load_pop_cache()
    if not precached_pop:
        print("Creating POP cache from scratch...")
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
                    
        pop_cache = open("popCacheTest.dat", 'ab')
        pickle.dump(partition_of_partition.cache, pop_cache)
        pop_cache.close()
        print("Saved POP cache!")


    precached_prob = load_prob_cache()
    if not precached_prob:
        print("Creating probability cache from scratch...")
        for i in range(1, N + 1):
             prob_pairs: list[tuple[tuple[int, ...], tuple[int, ...]]] = [
                 (IPS[i][j1], IPS[i][j2])
                 for j1 in range(len(IPS[i]))
                 for j2 in range(j1, len(IPS[i]))
             ]
             with tqdm(total=len(prob_pairs), desc=f"Processing pairs {i}") as pbar:
                for p1, p2 in prob_pairs:
                    
                    get_transitive_prob(p1, p2, i)
                    pbar.update(1)
        prob_cache = open("probCacheTest.dat", 'ab')
        pickle.dump(get_transitive_prob.cache, prob_cache)
        prob_cache.close()
        print("Saved probability cache!")
    
        
def test() -> None:
    precached = load_prob_cache()
    for i in range(1, 26):
    
        if not precached:
            print("Precache computation first!")
            return
        
        simple_prob: int = (get_simple_transitive_prob(i))

        calculated_prob: float = 0.0
        for j1 in range(len(IPS[i])):
            for j2 in range(j1, len(IPS[i])):
                if (j1 != j2):
                    calculated_prob += 2*(cycle_type_prob(IPS[i][j1], N)*cycle_type_prob(IPS[i][j2], N)*get_transitive_prob(IPS[i][j1], IPS[i][j2], N))
                else:
                    calculated_prob += (cycle_type_prob(IPS[i][j1], N)*cycle_type_prob(IPS[i][j2], N)*get_transitive_prob(IPS[i][j1], IPS[i][j2], N))
                    
        print(f"Probability is {simple_prob}, calculated probability is {calculated_prob}")
            
    
if __name__ == "__main__":
    main()
    #test()
