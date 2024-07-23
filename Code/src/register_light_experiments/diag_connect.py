# Examining the probability that a diagonal wire connects any cycles in
# a loop of a certain number of enigmas. Can use hard coded probability distribution of 
# cycle types or assume a random distribution

from itertools import combinations_with_replacement
from collections import defaultdict, Counter
import math
import random
import networkx as nx

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

def probability_diag_connects_any(cycle_types, n, l):
    p = probability_diag_connects_one(cycle_types, n)
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
            cycles_seen.update({cycle_type: 0})
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
        G.add_edge((0, 1), (1, 0))

        num_after = len(list(nx.connected_components(G)))
        if (num_before != num_after):
            connected_count += 1

    return connected_count / num_simulations


n = 26
l = 2
cycle_types = all_multiplicities(integer_partitions(n), n)

print(f"Uniform Dist -> {probability_diag_connects_one(cycle_types, n)}")
print(f"Collected Dist -> {probability_diag_connects_one(cycle_types, n, collect_cycle_types(n, l, 100000))}")
print(f"Monte Carlo -> {monte_carlo_simulation(n, l, 100000)}")