# Examining the probability that a diagonal wire connects any cycles in
# a loop of a certain number of enigmas. Can use hard coded probability distribution of 
# cycle types or assume a random distribution

from itertools import combinations_with_replacement
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import math
import random
import networkx as nx
import string

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

def cycle_even(cycle_type):
    # Count the number of even-length cycles
    even_count = sum(1 for length in cycle_type if length % 2 == 0)
    
    # Check if the number of even-length cycles is even or odd
    return even_count % 2 == 0

def partition_to_multiplicity(partition):
    """
    Convert a partition to a multiplicity representation.
    """
    return tuple(sorted(Counter(partition).items()))

def all_multiplicities(partitions, n):
    """
    Generate all distinct multiplicities for partitions in S_n.
    """

    multiplicities = {partition_to_multiplicity(part) for part in partitions}
    return sorted(multiplicities)

def probability_diag_connects_one(cycle_types, n, dist=None):
    total = 0
    for cycle_type in cycle_types: 
        inner_sum = 0
        inner_product = 1
        for (i, c_i) in cycle_type:
            inner_sum += c_i*(i/n*(1-(i/n)))
            if dist is None:
                inner_product *= math.factorial(c_i)*math.pow(i, c_i)
        if dist is None:
            total += inner_sum/inner_product
        else: 
            if cycle_type in dist:
                prob = dist[cycle_type]
                total += inner_sum*prob
    return total

def probability_diag_connects_any(cycle_types, n, l, dist=None):
    p = probability_diag_connects_one(cycle_types, n, dist)
    return 1 - math.pow(1-p, l*(l-1)/2)

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

def subscript_letter(index):
    # Return the corresponding lowercase letter for the given index
    return string.ascii_lowercase[index]

def visualize_graph(G, n, l, col_distance=2):
    pos = {}
    labels = {}

    # Assign positions to nodes with specified column distance
    for col in range(l):
        col_label = string.ascii_uppercase[col]
        for node in range(n):
            pos[(col, node)] = (col * col_distance, -node)
            labels[(col, node)] = f"{col_label}{subscript_letter(node)}"
    
    components = list(nx.connected_components(G))
    colors = plt.cm.get_cmap('tab20', len(components))  # Use a colormap with enough colors
    
    # Assign colors to nodes based on their component
    # Assign colors to nodes and edges based on their component
    node_color_map = {}
    for i, component in enumerate(components):
        color = colors(i)
        for node in component:
            node_color_map[node] = color
    
    # Assign edge colors based on the color of the first node it's connected to
    edge_colors = []
    for edge in G.edges():
        if G.edges[edge].get('color') == 'invis':
            edge_colors.append('none')  # Invisible edges
        elif G.edges[edge].get('color') == 'diag':
            edge_colors.append('tab:green')  # Invisible edges
        else:
            edge_colors.append(node_color_map.get(edge[0], 'black'))
    # Draw the graph with colored components
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=200, node_color=[node_color_map[node] for node in G.nodes()],
            edge_color=edge_colors, width=2, font_weight="bold", font_size=10)
    
    # Set background color to black
    plt.gca().set_facecolor('black')
    plt.show()

def create_graph_with_transpositions(n, l):
    G = nx.Graph()
    
    # Create l columns of n nodes
    for col in range(l):
        for node in range(n):
            G.add_node((col, node))
    
    # Connect nodes within each column to the next via random transpositions
    for col in range(l - 1):
        transpositions = generate_disjoint_transpositions(n)
        for i, j in transpositions:
            G.add_edge((col, i), (col + 1, j))
    
    for node in range(n):
        G.add_edge((0, node), (l - 1, node), color='invis')  # Invisible edges
    
    return G

def get_cycle_type(G):
    components = list(nx.connected_components(G))
    type = []
    for component in components:
        s = 0
        for node in component:
                if node[0] == 0:
                    s+=1 
        type.append(s)
    return type

# Calculate emperical distribution of cycle types and probabilities
def collect_cycle_types(n, l, num_simulations):
    cycles_seen = dict()
    for i in range(num_simulations):
        G = create_graph_with_transpositions(n, l+1)
        cycle_type = get_cycle_type(G)
        cycle_type = tuple(sorted(cycle_type))
        cycle_type = partition_to_multiplicity(cycle_type)
        if not cycle_type in cycles_seen:
            cycles_seen.update({cycle_type: 1})
        else: 
            s = cycles_seen[cycle_type]
            cycles_seen.update({cycle_type: s + 1})
    for cycle in cycles_seen:
        cycles_seen[cycle] /= num_simulations

    return cycles_seen


def monte_carlo_simulation(n, l, num_simulations):
    connected_count = 0
    for _ in range(num_simulations):
        G = create_graph_with_transpositions(n, l+1)
        num_before = len(list(nx.connected_components(G)))
        # Add in Diagonal Edge
        # G.add_edge((0, 1), (1, 0))
        # G.add_edge((2, 1), (1, 2))
        # G.add_edge((3, 1), (1, 2))
        # for i in range(l):
        #     for j in range(i+1, l):
        #         G.add_edge((i, j), (j, i), color='diag', connectionstyle = "arc3,rad=100")

        # IF EDGES ARE SAMPLED RANDOMLY THEN THIS ALIGNS WITH THE COLLECTED DISTRIBUTION
        # HOWEVER THE DIAGONAL NATURE SEEMS TO SKEW THESE PROBABILITIES QUITE A LOT
        possible_edges = []
        for col in range(l - 1):
            for i in range(n):
                for j in range(n):
                    possible_edges.append(((col, i), (col + 1, j)))

        # Sample k edges randomly from the possible edges
        sampled_edges = random.sample(possible_edges, int(l*(l-1)/2))
        G.add_edges_from(sampled_edges)

        num_after = len(list(nx.connected_components(G)))
        if (num_before != num_after):
            connected_count += 1

    return connected_count / num_simulations


n = 26
l = 3
print(f"Monte Carlo -> {monte_carlo_simulation(n, l, 10000)}")

cycle_types = all_multiplicities(integer_partitions(n), n)

print(f"Uniform Dist -> {probability_diag_connects_any(cycle_types, n, l)}")
print(f"Collected Dist -> {probability_diag_connects_any(cycle_types, n, l, collect_cycle_types(n, l, 10000))}")
