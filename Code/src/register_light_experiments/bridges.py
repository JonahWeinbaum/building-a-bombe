import itertools
import math
from collections import defaultdict, Counter
import math
import itertools

from itertools import chain, combinations
from tqdm import tqdm
from math import comb

def bridges_cycles(a, b):
    if(len(a) == 1):
        return True

    bridges = list(itertools.combinations(a, 2))
    for comp in b:
        for bridge in bridges:
            b1 = [value for value in comp if value in bridge[0]]
            b2 = [value for value in comp if value in bridge[1]]
            # Bridge found
            if len(b1) > 0 and len(b2) > 0:
                a.remove(bridge[0])
                a.remove(bridge[1])
                t = []
                for c in bridge[0]:
                    t.append(c)
                for c in bridge[1]:
                    t.append(c)
                a.append(t)
                return bridges_cycles(a, b)
    return False
                
def integer_partitions(n):
    """
    Generate all partitions of the integer n.
    """
    result = set()
    result.add((n,))
    
    for i in range(1, n):
        for p in integer_partitions(n - i):
            result.add(tuple(sorted((i,) + p)))
    
    return result

def partition_to_instance(part, n):
    # Create a list of integers from 1 to n
    elements = list(range(1, n + 1))
    bijection = [0] * n  # Initialize the bijection list
    
    index = 0
    for cycle_length in part:
        cycle = elements[index:index + cycle_length]
        for i in range(len(cycle)):
            bijection[cycle[i] - 1] = cycle[(i + 1) % cycle_length]  # Create the cycle
        index += cycle_length

    return bijection

def permutation_to_cycles(permutation):
    standard_order = sorted(permutation)
    visited = [False] * len(standard_order)
    cycles = []

    if len(standard_order) == 0:
        return tuple(cycles) 
    
    elem = standard_order[0]
    while visited != [True]*len(standard_order):
        if not visited[standard_order.index(elem)]:
            cycle = []
            while not visited[standard_order.index(elem)]:
                visited[standard_order.index(elem)] = True
                cycle.append(elem)
                #Get next iter
                elem = permutation[standard_order.index(elem)]
            cycles.append(tuple(cycle))
            if visited != [True]*len(standard_order):
                elem = standard_order[visited.index(False)]
    return tuple(cycles)

def cycle_type(cycles):
    return tuple(sorted(tuple(len(cycle) for cycle in cycles)))

def generate_sets(list_of_lists):
    # Use itertools.product to generate all combinations
    return list(itertools.product(*list_of_lists))

def remaining_elements(full_tuple, elements_to_exclude):
    return tuple(x for x in full_tuple if x not in elements_to_exclude)

def powerset(input_tuple):
    # Generate the powerset by getting all combinations of all possible lengths
    return list(itertools.chain.from_iterable(itertools.combinations(input_tuple, r) for r in range(len(input_tuple) + 1)))

def is_subset(tuple1, tuple2):
    return set(tuple1).issubset(set(tuple2))

def get_necc(necc_sets, to_test):
    necc = []
    for s in necc_sets:
        if is_subset(s, to_test):
            necc.append(s)
    return necc

def get_unique_cycles(tup):
    # Generate all permutations of the elements in the tuple
    permutations = set(itertools.permutations(tup))
    unique_cycles = set()

    for perm in permutations:
        # Normalize each cycle by rotating it to start with the smallest element
        min_index = perm.index(min(perm))
        normalized_cycle = perm[min_index:] + perm[:min_index]
        unique_cycles.add(normalized_cycle)

    return list(unique_cycles)

def partition_to_multiplicity(partition):
    """
    Convert a partition to a multiplicity representation.
    """
    return tuple(sorted(Counter(partition).items()))

def cycles_satisfy(necc_sets, b):
    #Convert list to tuples of cycles
    t_of_c = list(tuple(p) for p in permutation_to_cycles(b))

    satifies = False
    #For each cycle check if satisfies necc
    for c in t_of_c:
        if get_necc(necc_sets, c) != []:
            satifies = True
    return satifies
    
n = 26

#Get all cycle types in
ip = integer_partitions(n)
total = 0
#Initialize query dictionary
query = dict()
for part in (tqdm(ip, desc="Processing Partitions")):
    query[part] = dict()
    for part2 in ip:
        #CHECK IF THIS IS REALLY SYMEMTRIC
        if not (part2 in list(query.keys())):
            longer = [p2 >= len(part) for p2 in part2]
            # More cycle bridges (No longer mutually exclusive)
            if (True in longer and dict(Counter(longer).items())[True] > 1):
                query[part][part2] = 0
                instance = partition_to_instance(part, n)
                necc_sets = generate_sets(permutation_to_cycles(instance))

                for s in necc_sets:
                    #         remain_after_s = remaining_elements(tuple(range(1, n + 1)), s)
#         power_remain = powerset(remain_after_s)
#         for p in power_remain:

            # One cycle bridges
            elif True in longer:
                length_k = part2[(longer.index(True))]
                prob = 0
                for c in (chain.from_iterable(combinations(list(part), r) for r in range(len(part)+1))):
                    if c != ():
                        prob += math.pow(-1, len(c)+1)*comb(n-sum(c), length_k)
                total_outcomes = comb(n, length_k)
                prob = (total_outcomes - prob) / total_outcomes
                query[part][part2] = prob

            # No Bridges
            else:
                query[part][part2] = 0

def overcount_solver():
    return

def query_solver(query, p1, n):
    mutually = 0
    #Create an instance of cycle_type
    ip1 = partition_to_instance(p1, n)
    all_bridges = []

    #Generate all bridges of ip1
    necc_sets = generate_sets(permutation_to_cycles(ip1))
    for s in necc_sets: 
        remain_after_s = remaining_elements(tuple(range(1, n + 1)), s)
        power_remain = powerset(remain_after_s)
        for p in power_remain:
            necc_cycle = tuple(set(s).union(set(p)))
            remain = remaining_elements(tuple(range(1, n + 1)), necc_cycle)
            if len(remain) < len(p1):
                continue
            for q in get_unique_cycles(necc_cycle):
                for r in itertools.permutations(remain):
                    cycles_r = list(permutation_to_cycles(r))
                    longer_than_necc = [len(c)>=len(p1) for c in cycles_r]
                    if (not (True in longer_than_necc)):
                        continue
                    remain_permutes = []
                    for cycle in cycles_r:
                        remain_permutes.append(cycle)
                    remain_permutes.append(tuple(q))
                    all_bridges.append(tuple(sorted(remain_permutes)))

    cycle_types = dict()
    for bridge in list(set(all_bridges)):
        ct = cycle_type(bridge)
        if ct in list(cycle_types.keys()):
            cycle_types[ct] += 1
        else:
            cycle_types[ct] = 1
    for ct in list(cycle_types.keys()):
        mult = partition_to_multiplicity(ct)  
        inner_product = math.factorial(n)
        for (c_i, i) in mult:
            inner_product /= math.factorial(i)*(c_i**i)
        cycle_types[ct] /= inner_product
        longer = list(c >= len(p1) for c in ct)
        mutually += (int(dict(Counter(longer).items())[True] > 1))
        query[p1][ct] = cycle_types[ct]
    return mutually

