import random
import networkx as nx
import matplotlib.pyplot as plt
import string



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
    
    for i in range(l):
        for j in range(i+1, l):
            G.add_edge((i, j), (j, i), color='diag', connectionstyle = "arc3,rad=100")
    

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

def add_random_edges(G, l):
    # List of all possible edges including self-loops
    possible_edges = [(i, j) for i in range(len(G.nodes)) for j in range(len(G.nodes))]
    
    # Add l random edges (with repetition)
    additional_edges = random.choices(possible_edges, k=l)
    G.add_edges_from(additional_edges)

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

def is_connected(G):
    return nx.is_connected(G)

def monte_carlo_simulation(n, l, num_simulations):
    connected_count = 0
    for _ in range(num_simulations):
        permutation = generate_random_bijection(n)
        G = create_graph_from_bijection(n, permutation)
        add_random_edges(G, l)
        if is_connected(G):
            connected_count += 1
    return connected_count / num_simulations

# Parameters
n = 26
l = 4

visualize_graph(create_graph_with_transpositions(n, l), n, l, 10)

# for l in range(1, 13):
#     # print(k)
#     num_simulations = 10000


#     s = 0
#     monte_total = 10000
#     for i in range(monte_total):
#         s += int(is_connected(create_graph_with_transpositions(n, l)))

#     score = (s / monte_total)
#     print(f"l = {l} -> " + "{:.1%}".format(score))