from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from itertools import combinations
from collections import Counter
#from pymongo import MongoClient
#from pymongo.collection import Collection
#from pymongo.database import Database
from tqdm import tqdm # type: ignore
from functools import lru_cache
from typing import Dict
import math
import time

def partition_of_partition(p: tuple[int,...], target_p: tuple[int,...]) -> list[tuple[tuple[int,...],...]]:
    global ips
    @lru_cache(None)
    def backtrack(p: tuple[int,...], target_p: tuple[int,...], index: int, current_partition: tuple[tuple[int, ...], ...], result: tuple[tuple[tuple[int,...],...],...]) -> None:
        # We have gone through all targets
        if index == len(target_p):

            # No elements remain in p thus our partition is valid
            if not p:
                # Add partition to result only if not seen before
                current_partition = tuple(sorted(current_partition))
                if current_partition not in seen:
                    seen.add(current_partition)
                    result = result + (current_partition,)
            return

        # Next target value in target_p
        target: int = target_p[index]

        subsets: list[tuple[int,...]] = []
        for part in ips[target]:
            if not Counter(part) - Counter(p):
                subsets.append(part)
        #print(f"Subsets to sum: {subsets}")
        # Get unique subsets of p1 which add to target value
        for subset in subsets:
           remaining: list[int]= list(p)
           for elem in subset:
               remaining.remove(elem)
           new_current: tuple[tuple[int, ...],...] = current_partition + (subset,)
           backtrack(tuple(remaining), target_p, index + 1, new_current, result)

    result: tuple[tuple[tuple[int,...],...]] = tuple()
    seen: set[tuple[tuple[int,...],...]] = set()
    current_partition: tuple[tuple[int,...],...] = tuple()
    index: int = 0
    backtrack(p, target_p, index, current_partition, result)
    return [tuple(sorted(t, key=lambda x: sum(x))) for t in result]
 
def group_partitions(p1: tuple[tuple[int,...],...], p2: tuple[tuple[int,...],...]) -> tuple[tuple[tuple[int,...],tuple[int,...]],...]:
    return tuple((a, b) for a, b in zip(p1, p2))

def generate_integer_partitions(n: int) -> list[tuple]:
    result: set[tuple] = set()
    result.add((n,))
    
    for i in range(1, n):
        for p in generate_integer_partitions(n - i):
            result.add(tuple((sorted((i,) + p))))
    
    return list(result)

def number_of_partition(p: tuple, n: int) -> int:
    result: float = math.factorial(n)
    p_m: tuple = partition_to_multiplicity(p);
    for i, k_i in p_m:
        result /= math.pow(math.factorial(i), k_i)*math.factorial(k_i)
    return int(result)
        
def num_of_cycle_type(p: tuple, n: int) -> int:
    result: float = math.factorial(n)
    p_m: tuple = partition_to_multiplicity(p);
    for i, k_i in p_m:
        result /= math.pow(i, k_i)*math.factorial(k_i)
    return int(result)

def partition_to_multiplicity(p: tuple) -> tuple:
    return tuple(sorted(Counter(p).items()))

def partitions_to_search_space(p1: tuple[int,...], p2: tuple[int,...], n: int) -> int:
    n1: int = num_of_cycle_type(p1, n)
    n2: int = num_of_cycle_type(p2, n)

    return n1*n2

@lru_cache(None)
def get_transitive_prob(p1: tuple[int,...], p2: tuple[int,...], n: int, depth: int = 0):
    global probs
    global ips
    #print(" "*depth + f"n: {n} -> ips[{n}]: {ips[n]}")
    key: tuple[tuple[int,...],...] = tuple(sorted((p1, p2)))
    t: float | None = probs.get(key, None)

    if t is not None:
        return t

    psearchsize: float = float(partitions_to_search_space(p1, p2, n))
    total: float = psearchsize
   
    for gen in ips[n]:
        #print(" "*depth + f"On partition {gen}")
        if gen != (n,):

           c1_gen: list[tuple[tuple[int,...],...]] = partition_of_partition(p1, gen)
           c2_gen: list[tuple[tuple[int,...],...]] = partition_of_partition(p2, gen)
           #print(" "*depth + f"p1: {p1} -> c1_gen: {c1_gen}")
           #print(" "*depth + f"p2: {p2} -> c2_gen: {c2_gen}")
           grouped: list[tuple[tuple[tuple[int,...],tuple[int,...]],...]] = []

           # Both have valid subpartitions
           if c1_gen and c2_gen:
              for c1 in c1_gen:
                  for c2 in c2_gen:
                      grouped.append(group_partitions(c1, c2))
           else:
               continue

           #print(" "*depth + f"Grouped: {grouped}")
           num_partition: int = number_of_partition(gen, n)
           subtotal: float = 0.0
           for group in grouped:
               
               subsubtotal: float = 1.0
               for i, [s1, s2] in enumerate(group):
                  key = tuple(sorted((s1, s2)))
                  t = probs.get(key, None)

                  if t:
                      subsubtotal *= float(partitions_to_search_space(s1, s2, gen[i])*t)
                  else:
                      #Base casex
                      if len(s1) == 1 or len(s2) == 1:
                          key = tuple(sorted((s1, s2)))
                          probs[key] = 1.0
                          #print(" "*depth + "Length 1 case backtracking...")
                          subsubtotal *= partitions_to_search_space(s1, s2, gen[i])
                      else:
                          subsubtotal *= partitions_to_search_space(s1, s2, gen[i])*get_transitive_prob(s1, s2, gen[i], depth+1)
               subtotal += subsubtotal


           subtotal *= num_partition
           total -= subtotal

    total /= psearchsize

    key = tuple(sorted((p1, p2))) 
    probs[key] = total

    return total

#client: MongoClient  = MongoClient("mongodb://localhost:27017/")

#db: Database = client["transitive"]

#probabilities: Collection = db["probabilities"]
#partitions: Collection = db["partitions"]

ips: Dict[int, list[tuple]] = {}

print("Generating all integer partitions...")
for i in range(1,20):
    ips_i: list[tuple] | None = None
    #cached_p: Dict[str, list[tuple]] | None = partitions.find_one({"n": i}) 
    #if cached_p is None:
    ips_i = generate_integer_partitions(i)
        #partitions.insert_one({"n": i, "partitions": ips_i})
    # Found partitions we must convert to tuples
    #else:
    #    ips_i = [tuple(ip) for ip in cached_p["partitions"]]
    ips[i] = ips_i        
print("Generated!")

# # Extract all probabilities into local storage
# print("Loading probabilities from db...")
probs: Dict[tuple[tuple[int,...],...], float] = {}
# local_probabilities = {
#     tuple(sorted(map(tuple, [doc["p1"], doc["p2"]]))): doc["t"]
#     for doc in probabilities.find({}, {"p1": 1, "p2": 1, "t": 1, "_id": 0})
# }
# print("Loaded!")

# last_query = max(
#     sum(doc["p1"]) for doc in probabilities.find({}, {"p1": 1, "_id": 0})
# )


for k in range (1, 20):
    pairs: list[tuple[tuple[int,...], tuple[int,...]]] = [(i, j) for i in ips[k] for j in ips[k]]  # Generate all pairs

    with tqdm(total=len(pairs), desc="Processing pairs") as pbar:
        for p1, p2 in pairs:
            get_transitive_prob(p1, p2, k)
            pbar.update(1)


   # After completing this round insert missing probabilities
   # total = 0
   # for (p1, p2), t in .items():
   #   if sum(p1) == k:
   #      key = {"p1": list(p1), "p2": list(p2)}  

   #      if not probabilities.find_one(key):
   #          probabilities.insert_one({"p1": list(p1), "p2": list(p2), "t": t})
   #          total += 1
