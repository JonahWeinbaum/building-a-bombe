import itertools
import math

def generate_bijections(n):
    numbers = list(range(1, n+1))
    bijections = list(itertools.permutations(numbers))
    return bijections

def permutation_to_cycles(permutation):
    visited = [False] * len(permutation)
    cycles = []

    for i in range(len(permutation)):
        if not visited[i]:
            cycle = []
            x = i
            while not visited[x]:
                visited[x] = True
                cycle.append(x + 1)
                x = permutation[x] - 1
            if len(cycle) > 1:
                cycles.append(cycle)
            else:
                cycles.append(cycle)
    
    return cycles

def cycle_type(cycles):
    return tuple(sorted([len(cycle) for cycle in cycles]))

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

def cycles_satisfy(necc_sets, b):
    #Convert list to tuples of cycles
    t_of_c = list(tuple(p) for p in permutation_to_cycles(b))

    satifies = False
    #For each cycle check if satisfies necc
    for c in t_of_c:
        if get_necc(necc_sets, c) != []:
            satifies = True
    return satifies

n = 6 # You can change this value to generate bijections for a different n
bijections = generate_bijections(n)

full_tuple =  tuple(range(1, n + 1))
for b in bijections:
    necc_sets = generate_sets(permutation_to_cycles(b))

    overcounts = dict()
    for s in necc_sets:
        overcounts[s] = 0
    for s in necc_sets: 
        remain_after_s = remaining_elements(full_tuple, s)
        power_remain = powerset(remain_after_s)
        for p in power_remain:
            for s2 in necc_sets:
                if s2 in get_necc(necc_sets, tuple(set(s) | set(p))) and s != s2:
                    overcounts[s2] += 1
            # print(tuple(set(s).union(set(p))), get_necc(necc_sets, tuple(set(s) | set(p))))
    print(str(cycle_type(permutation_to_cycles(b))) + " -> " + str(overcounts[list(overcounts.keys())[0]]))
    
# avg = 0
# for b1 in bijections:
#     necc_sets = generate_sets(permutation_to_cycles(b1))

#     total = 0
#     for b2 in bijections:
#         total += cycles_satisfy(necc_sets, b2)
#         # print(permutation_to_cycles(b), cycles_satisfy(necc_sets, b))
#     print(permutation_to_cycles(b1), total/len(bijections))
#     avg += total/len(bijections)
# print("Average -> " + str(avg/len(bijections)))