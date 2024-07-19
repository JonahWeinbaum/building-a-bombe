import random

n = 4
loop_size = 7  
steps = 100


# Add diagonal
def d(transposition, i, j):
    transposition.add((j, i))


def o(a, b):
    for i in range(n):
        a[i] = a[i] or b[i]
        b[i] = a[i] or b[i]
    return a


def random_disjoint_transpositions():
    elements = list(range(n))
    transpositions = set()
    random.shuffle(elements)

    for i in range(0, n - 1, 2):
        if i + 1 < n:
            transpositions.add((elements[i], elements[i + 1]))
            transpositions.add((elements[i+1], elements[i]))

    # If n is odd, add the last element as a self-loop
    if n % 2 == 1:
        transpositions.add((elements[-1], elements[-1]))

    return transpositions

# Map set to set through transposition
def t(transposition, cable_set):
    out_set = set()
    for wire in cable_set:
        for swap in transposition:
            if swap[0] == wire:
                out_set.add(swap[1])
    return out_set





def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, rank, x, y):
    rootX = find(parent, x)
    rootY = find(parent, y)
    
    if rootX != rootY:
        if rank[rootX] > rank[rootY]:
            parent[rootY] = rootX
        elif rank[rootX] < rank[rootY]:
            parent[rootX] = rootY
        else:
            parent[rootY] = rootX
            rank[rootX] += 1

def collapse_sets(list_of_sets):
    # Create a mapping from element to its set representative
    elements = set(elem for s in list_of_sets for elem in s)
    parent = {elem: elem for elem in elements}
    rank = {elem: 0 for elem in elements}
    
    for s in list_of_sets:
        it = iter(s)
        first = next(it)
        for elem in it:
            union(parent, rank, first, elem)
    
    # Group elements by their set representative
    from collections import defaultdict
    collapsed_sets = defaultdict(set)
    for elem in elements:
        root = find(parent, elem)
        collapsed_sets[root].add(elem)
    
    return list(collapsed_sets.values())

s = 0

iters = 10000

tran = {(0, 1), (1,0), (3, 2), (2, 3)}
tran2 = {(1, 2), (2, 1), (0, 3), (3, 0)}
tran3 = {(3, 2), (2, 3), (1, 0), (0, 1)}
# tran4 =  {(3, 2), (2, 3), (1, 0), (0, 1)}
#tran4 = random_disjoint_transpositions()
# tran5 = random_disjoint_transpositions()
# d(tran, 0, 1)
# d(tran, 0, 2)
# d(tran, 0, 3)
# d(tran, 0, 5)
# d(tran2, 1, 2)
# d(tran2, 1, 3)
# d(tran2, 1, 5)
# d(tran3, 2, 3)
# d(tran3, 2, 5)
# d(tran4, 3, 5)
# d(tran5, 4, 5)


circuits = []
for i in range(n):
    cable_set = t(tran3, t(tran2, t(tran, {i})))
    circuits.append(cable_set)
circuits = collapse_sets(circuits)

print(circuits)