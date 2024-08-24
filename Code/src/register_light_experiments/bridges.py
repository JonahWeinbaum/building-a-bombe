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
        for t in to_test:
            if is_subset(s, t):
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
    
#Brute Force Query Solver
def bf_query_solver(query, p1, n):
    #Create an instance of cycle_type
    ip1 = partition_to_instance(p1, n)
    all_bridges = set()

    overcounts = dict()

    #Generate all bridges of ip1
    necc_sets = generate_sets(permutation_to_cycles(ip1))
    for s in necc_sets: 
        remain_after_s = remaining_elements(tuple(range(1, n + 1)), s)
        power_remain = powerset(remain_after_s)
        for p in power_remain:
            necc_cycle = tuple(set(s).union(set(p)))
            remain = remaining_elements(tuple(range(1, n + 1)), necc_cycle)
            for q in get_unique_cycles(necc_cycle):
                for r in itertools.permutations(remain):
                    cycles_r = list(permutation_to_cycles(r))
                    len_cycles_r = [len(c) for c in cycles_r]
                    longer_than_q =[len(q) <  length for length in len_cycles_r]
                    if True in longer_than_q:
                        continue
                    remain_permutes = []
                    for cycle in cycles_r:
                        remain_permutes.append(cycle)
                    remain_permutes.append(tuple(q))
                    all_bridges.add(tuple(sorted(remain_permutes)))
    cycle_types = dict()
    for bridge in all_bridges:
        ct = cycle_type(bridge)
        if ct in list(cycle_types.keys()):
            cycle_types[ct] += 1
        else:
            cycle_types[ct] = 1
    
    for ct in list(cycle_types.keys()):
        # mult = partition_to_multiplicity(ct)  
        # inner_product = math.factorial(n)
        # for (c_i, i) in mult:
        #     inner_product /= math.factorial(i)*(c_i**i)
        # cycle_types[ct] /= inner_product
        # longer = list(c >= len(p1) for c in ct)
        # mutually += (int(dict(Counter(longer).items())[True] > 1))
        query[p1][ct] = cycle_types[ct]
    # return mutually

#Brute Force Equalities Solver
def bf_equalities_solver(query, p1, n):
    #Create an instance of cycle_type
    ip1 = partition_to_instance(p1, n)
    all_bridges = set()
    equalities = dict()

    #Generate all bridges of ip1
    necc_sets = generate_sets(permutation_to_cycles(ip1))
    for s in necc_sets: 
        remain_after_s = remaining_elements(tuple(range(1, n + 1)), s)
        power_remain = powerset(remain_after_s)
        for p in power_remain:
            necc_cycle = tuple(set(s).union(set(p)))
            remain = remaining_elements(tuple(range(1, n + 1)), necc_cycle)
            for q in get_unique_cycles(necc_cycle):
                for r in itertools.permutations(remain):
                    cycles_r = list(permutation_to_cycles(r))
                    len_cycles_r = [len(c) for c in cycles_r]
                    longer_than_q =[len(q) <  length for length in len_cycles_r]
                    if True in longer_than_q:
                        continue
                    remain_permutes = []
                    for cycle in cycles_r:
                        remain_permutes.append(cycle)
                    remain_permutes.append(tuple(q))
                    if tuple(sorted(remain_permutes)) in all_bridges:
                        if cycle_type(remain_permutes) in list(equalities.keys()):
                            equalities[cycle_type(remain_permutes)] += 1
                        else:
                            perms = 1
                            for c in remain_permutes:
                                perms *= math.factorial(len(c)-1)
                            equalities[cycle_type(remain_permutes)] = 1
                    all_bridges.add(tuple(sorted(remain_permutes)))
    for ct in list(equalities.keys()):
        l = max(ct)
        list_ct = list(ct)
        list_ct.remove(l)
        ct_remain = tuple(list_ct) 
        mult_remain = partition_to_multiplicity(ct_remain)
        N = len(necc_sets)
        k = len(necc_sets[0])
        perms = 1
        for c in ct:
            perms *= math.factorial(c-1)
        if l != 1:
            t1 = N*comb(n-k, l-k)*math.factorial(l-1)*math.factorial(n-l)
            divisor = 1
            for (c_i, i) in mult_remain:
                divisor *= math.factorial(i)*math.pow(c_i, i)
            t1 /= divisor
        else:
            t1 = N*comb(n-k, l-k)*math.factorial(n-l)
            divisor = 1
            for (c_i, i) in mult_remain:
                divisor *= math.factorial(i)*math.pow(c_i, i)
            t1 /= divisor
        equalities[ct] = (t1-query[part][ct]) / perms
    print(equalities)
n = 7

#Get all cycle types in
ip = integer_partitions(n)
total = 0
#Initialize query dictionary
query = dict()
query2 = dict()
equalities = dict()
for part in ip:
    query[part] = dict()
    query2[part] = dict()
    for part2 in ip:
        query[part][part2] = 0
        query2[part][part2] = 0
    if part == (2, 2, 3):
        bf_query_solver(query, part, n)
        bf_equalities_solver(query, part, n)
# print(query[(2,2,3)])
# print(query2[(2,2,3)])
