import itertools
import numpy as np
import matplotlib.pyplot as plt

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

# def order_cycles(c1, c2, sort_part):
#     ind_c1 = sort_part.index(cycle_type(permutation_to_cycles(c1)))
#     ind_c2 = sort_part.index(cycle_type(permutation_to_cycles(c2)))
#     return ind_c1 < ind_c2

n = 4 # You can change this value to generate bijections for a different n
partitions = sorted(integer_partitions(n))
bijections = generate_bijections(n)
# order_cycles(bijections[0], bijections[1], partitions)
bijections.sort(key=lambda x: partitions.index(cycle_type(permutation_to_cycles(x))))

# Initialize a 2D list to store bridge information
size = len(bijections)
bridge_info = [[False] * size for _ in range(size)]
# Fill the bridge_info list with boolean values
for i, b1 in enumerate(bijections):
    for j, b2 in enumerate(bijections):
        b1_cycles = permutation_to_cycles(b1)
        b2_cycles = permutation_to_cycles(b2)
        # Here you can set the condition for True or False
        # For demonstration, let's assume we set True if they have any common element
        if bridges_cycles(b1_cycles, b2_cycles):  # Modify as per your condition
            bridge_info[i][j] = True
        else:
            bridge_info[i][j] = False

# Create a heatmap
plt.figure(figsize=(5, 5))  # Adjust the figure size to zoom out

# Prepare the data for visualization
data = np.array(bridge_info, dtype=int)  # Convert to numpy array for visualization

plt.imshow(data, cmap='RdYlGn', interpolation='nearest')
plt.xticks(ticks=np.arange(size), labels=[str(permutation_to_cycles(b)) for b in bijections], rotation=90)
plt.yticks(ticks=np.arange(size), labels=[str(permutation_to_cycles(b)) for b in bijections])
plt.title(f'Bridges in S{n}')
plt.xlabel('')
plt.ylabel('')
plt.tight_layout()
plt.show()