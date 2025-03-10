from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from itertools import combinations
from collections import Counter
from pymongo import MongoClient
from tqdm import tqdm
from functools import lru_cache
import math
import time

def partition_of_partition(p, target_p):
    def backtrack(p, target_p, index, current_partition, result, seen):
        # We have gone through all targets
        if index == len(target_p):

            # No elements remain in p thus our partition is valid
            if not p:

                # Add partition to result only if not seen before
                partition_tuple = tuple(tuple(sorted(sub)) for sub in current_partition)
                if partition_tuple not in seen:
                    seen.add(partition_tuple)
                    result.append(current_partition[:])
            return

        # Next target value in target_p
        target = target_p[index]

        # Cache integer partitions
        global ips

        subsets = []
        for part in ips[target]:
            if not Counter(part) - Counter(p):
                subsets.append(part)
                
        # Get unique subsets of p1 which add to target value
        for subset in subsets:
           remaining = list(p)
           for elem in subset:
               remaining.remove(elem)            
           backtrack(remaining, target_p, index + 1, current_partition + [list(subset)], result, seen)

    result = []
    seen = set()
    
    backtrack(p, target_p, 0, [], result, seen)
    return result
 
def group_partitions(part1, part2):
    return [[list(a), list(b)] for a, b in zip(part1, part2)]

def generate_integer_partitions(n):
    result = list()
    result.append([n,])
    
    for i in range(1, n):
        for p in generate_integer_partitions(n - i):
            result.append(list(sorted([i,] + p)))
    
    return [list(i) for i in set(tuple(i) for i in result)]

def number_of_partition(p, n):
    result = math.factorial(n)
    p_m = partition_to_multiplicity(p);
    for i, k_i in p_m:
        result /= math.pow(math.factorial(i), k_i)*math.factorial(k_i)
    return int(result)
        
def num_of_cycle_type(p, n):
    result = math.factorial(n)
    p_m = partition_to_multiplicity(p);
    for i, k_i in p_m:
        result /= math.pow(i, k_i)*math.factorial(k_i)
    return int(result)

def partition_to_multiplicity(partition):
    return tuple(sorted(Counter(partition).items()))

def partitions_to_search_space(p1, p2, n):
    n1 = num_of_cycle_type(p1, n)
    n2 = num_of_cycle_type(p2, n)
    return n1*n2

def get_transitive_prob(p1, p2, n, depth = 0):
    global local_probabilities

    key = tuple(sorted(map(tuple, [p1, p2])))  
    t = local_probabilities.get(key, None)

    if t is not None:
        return t
    global ips

    psearchsize = partitions_to_search_space(p1, p2, n)
    total = psearchsize
   
    for gen in ips[n]:
        if gen != [n]:
           c1_gen = (partition_of_partition(p1, gen))
           c2_gen = (partition_of_partition(p2, gen))

           grouped = []

           # Both have valid subpartitions
           if c1_gen and c2_gen:
              for c1 in c1_gen:
                  for c2 in c2_gen:
                      grouped.append(group_partitions(c1, c2))
           else:
               continue

           num_partition = number_of_partition(gen, n)
           subtotal = 0
           for group in grouped:
               subsubtotal = 1
               for i, [s1, s2] in enumerate(group):
                  key = tuple(sorted(map(tuple, [s1, s2])))  
                  t = local_probabilities.get(key, None)

                  if t:
                      subsubtotal *= partitions_to_search_space(s1, s2, gen[i])*t
                  else:
                      #Base case
                      if len(s1) == 1 or len(s2) == 1:
                          print(len(local_probabilities))
                          key = tuple(sorted(map(tuple, [s1, s2]))) 
                          local_probabilities[key] = 1.0
                          print(len(local_probabilities))
                          #print(" "*depth + "Length 1 case backtracking...")
                          subsubtotal *= partitions_to_search_space(s1, s2, gen[i])
                      else:
                          subsubtotal *= partitions_to_search_space(s1, s2, gen[i])*get_transitive_prob(s1, s2, gen[i], depth+1)
               subtotal += subsubtotal


           subtotal *= num_partition
           total -= subtotal

    total /= psearchsize

    key = tuple(sorted(map(tuple, [p1, p2]))) 
    local_probabilities[key] = total

    return total

client = MongoClient("mongodb://localhost:27017/")

db = client["transitive"]

probabilities = db["probabilities"]
partitions = db["partitions"]

# Extract all probabilities into local storage
print("Loading probabilities from db...")
local_probabilities = {
    tuple(sorted(map(tuple, [doc["p1"], doc["p2"]]))): doc["t"]
    for doc in probabilities.find({}, {"p1": 1, "p2": 1, "t": 1, "_id": 0})
}
print("Loaded!")

last_query = max(
    sum(doc["p1"]) for doc in probabilities.find({}, {"p1": 1, "_id": 0})
)
ips = {}
print("Generating all integer partitions...")
for i in range(1,27):
    ips_i = partitions.find_one({"n": i})["partitions"]
    if ips_i is None:
        ips_i = generate_integer_partitions(i)
        partitions.insert_one({"n": i, "partitions": ips_i})
    ips[i] = ips_i        
print("Generated!")


for k in range (last_query, 27):
   pairs = [(i, j) for i in ips[k] for j in ips[k]]  # Generate all pairs

   with tqdm(total=len(pairs), desc="Processing pairs") as pbar:
       for (i,j) in pairs:
           get_transitive_prob(i, j, k)
           pbar.update(1)

   # After completing this round insert missing probabilities
   total = 0
   for (p1, p2), t in local_probabilities.items():
     if sum(p1) == k:
        key = {"p1": list(p1), "p2": list(p2)}  

        if not probabilities.find_one(key):
            probabilities.insert_one({"p1": list(p1), "p2": list(p2), "t": t})
            total += 1
