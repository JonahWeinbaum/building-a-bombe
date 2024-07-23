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


def bridges_cycles(a, b):

    if(len(a) == 1):
        return True

    bridges = list(itertools.combinations(a, 2))
    bridged = list()
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

n = 6  # You can change this value to generate bijections for a different n
bijections = generate_bijections(n)

cycle_type_map = dict()
s = 0
for (b1, b2) in list(itertools.combinations(bijections, 2)):
        if bridges_cycles(permutation_to_cycles(b1), permutation_to_cycles(b2)):
            if not ((tuple(b1)) in cycle_type_map):
                cycle_type_map[tuple(b1)] = 1
            else:
                cycle_type_map[tuple(b1)] += 1
        else:
            if not ((tuple(b1)) in cycle_type_map):
                cycle_type_map[tuple(b1)] = 0

print(cycle_type_map)