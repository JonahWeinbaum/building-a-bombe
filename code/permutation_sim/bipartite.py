# Generates and visualizes graphs of compositions of disjoint transpositions 
# and the corresponding cycles in each wire. Can include diagonal wirings. This can be used
# for emperical testing of cycle distributions on a number of enigmas connected in series. 

import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import math
import itertools
import sympy as sp
from itertools import chain, combinations
from tqdm import tqdm
from math import comb

def generate_disjoint_transpositions(n):
    # Initialize the list with numbers from 0 to n-1
    numbers = list(range(n))
    transpositions = []
    
    while len(numbers) > 1:
        # Randomly select two distinct indices for transposition
        i, j = random.sample(numbers, 2)
        
        # Add the transposition (i, j) to the list of transpositions
        transpositions.append((i, j))
        transpositions.append((j, i))
        
        # Remove the transposed elements from the list
        numbers.remove(i)
        numbers.remove(j)
    transpositions.sort(key=lambda x: x[0])
    
    return transpositions

def create_graph_with_transpositions(n, l, diag = False):
    G = nx.Graph()
    
    # Create l columns of n nodes

    for loop in range(len(l)):
        for col in range(l[loop]):
            for node in range(n):
                if col == 0 and loop == 0:
                    G.add_node((0, 0, node))
                elif col == 0 and loop != 0:
                    continue
                else:
                    G.add_node((loop, col, node))
    
    # Connect nodes within each column to the next via random transpositions
    for loop in range(len(l)):
        for col in range(l[loop] - 1):
            # if (col == 1):
            #     transpositions = generate_disjoint_transpositions(n)
            #     for i, j in transpositions:
            #         G.add_edge((col, i), (col + 1, j))
            transpositions = generate_disjoint_transpositions(n)
            for i, j in transpositions:
                if col == 0:
                    G.add_edge((0, 0, i), (loop, col + 1, j))
                else:
                    G.add_edge((loop, col, i), (loop, col + 1, j))
    
                
    for loop in range(len(l)):
        for node in range(n):
            G.add_edge((0, 0, node), (loop, l[loop] - 1, node), color='invis')  # Invisible edges
    
    if diag:
        for loop in range(len(l)):
            for i in range(l[loop]):
                for j in range(i+1, l[loop] - 1):
                    if i == 0:
                        G.add_edge((0, i, j), (loop, j, i), color='diag', connectionstyle = "arc3,rad=100")
                    else:
                        G.add_edge((loop, i, j), (loop, j, i), color='diag', connectionstyle = "arc3,rad=100")
    

    return G

def generate_random_bijection(n):
    # Generate a list of numbers from 1 to n
    numbers = list(range(1, n + 1))
    # Shuffle the list to create a random permutation
    permutation = random.sample(numbers, n)
    return permutation
    

def create_graph_from_bijection(n, permutation):
    # Create an empty graph
    G = nx.Graph()
    # Add nodes
    G.add_nodes_from(range(1, n + 1))
    # Add edges based on the permutation
    for i in range(n):
        G.add_edge(i + 1, permutation[i])
    return G

def generate_all_bijections(n):
    numbers = list(range(1, n + 1))
    return list(itertools.permutations(numbers))

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

# Parameters
n = 6

bij = generate_all_bijections(n)
bij_cycles = [permutation_to_cycles(b) for b in bij]

G = None
while True:
   chosen = random.sample(bij_cycles, 2)
   pos = {}
   row_nodes = [{}, {}]

   G = nx.Graph()

   for row_idx, row in enumerate(chosen):
       for col_idx, tup in enumerate(row):
           base_label = "".join(map(str, tup)) 
           node_label = f"{base_label}_{'top' if row_idx == 0 else 'bottom'}" 
           G.add_node(node_label)
           pos[node_label] = (col_idx, -row_idx)
           row_nodes[row_idx][node_label] = set(tup)

   for node1, numbers1 in row_nodes[0].items():
       for node2, numbers2 in row_nodes[1].items():
           if numbers1 & numbers2: 
               G.add_edge(node1, node2)
   if (not nx.is_connected(G)):
       break
# Draw the graph
plt.figure(figsize=(6, 4))
nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=12)
plt.show()

