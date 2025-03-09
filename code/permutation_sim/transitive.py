from pprint import pprint
from itertools import combinations
from collections import Counter
def partition_of_partition(p1, p2):
        
    def backtrack(p1, p2, index, current_partition, result, seen):
        # We have gone through all targets
        if index == len(p2):

            # No elements remain in p1 thus our partition is valid
            if not p1:

                # Add partition to result only if not seen before
                partition_tuple = tuple(tuple(sorted(sub)) for sub in current_partition)
                if partition_tuple not in seen:
                    seen.add(partition_tuple)
                    result.append(current_partition[:])
            return

        # Next target value in P2
        target = p2[index]

        # TODO: Cache integer partitions
        global ips

        subsets = []
        for part in ips[target]:
            if not Counter(part) - Counter(p1):
                subsets.append(part)
                
        # Get unique subsets of p1 which add to target value
        for subset in subsets:
           remaining = list(p1)
           for elem in subset:
               remaining.remove(elem)            
           backtrack(remaining, p2, index + 1, current_partition + [list(subset)], result, seen)

    result = []
    seen = set()
    
    backtrack(p1, p2, 0, [], result, seen)
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

n = 26
ips = {}
print("Generating all integer partitions")
for i in range(1, 27):
    ips[i] = generate_integer_partitions(i)
print("Generated...")
c1 = [1 for i in range(26)]
c2 = [2 for i in range(13)]

for gen in ips[26]:
    print(gen)
    c1_gen = (partition_of_partition(c1, gen))
    c2_gen = (partition_of_partition(c2, gen))
    grouped = []
    for p1 in c1_gen:
        for p2 in c2_gen:
            grouped.append(group_partitions(p1, p2))
    print(*grouped, sep='\n')
    print("...")
