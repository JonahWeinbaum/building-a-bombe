# Generates and visualizes graphs of compositions of disjoint transpositions
# and the corresponding cycles in each wire. Can include diagonal wirings. This can be used
# for emperical testing of cycle distributions on a number of enigmas connected in series.

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


def create_graph_with_transpositions(n, l, diag=False):
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
            G.add_edge(
                (0, 0, node), (loop, l[loop] - 1, node), color="invis"
            )  # Invisible edges

    if diag:
        for loop in range(len(l)):
            for i in range(l[loop]):
                for j in range(i + 1, l[loop] - 1):
                    if i == 0:
                        G.add_edge(
                            (0, i, j),
                            (loop, j, i),
                            color="diag",
                            connectionstyle="arc3,rad=100",
                        )
                    else:
                        G.add_edge(
                            (loop, i, j),
                            (loop, j, i),
                            color="diag",
                            connectionstyle="arc3,rad=100",
                        )

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


def visualize_graph(G, n, l, col_distance=2, row_distance=40):
    pos = {}
    labels = {}

    # Assign positions to nodes with specified column distance
    for loop in range(len(l)):
        for col in range(l[loop]):
            col_label = string.ascii_uppercase[col]
            if col == l[loop] - 1:
                col_label = string.ascii_uppercase[0]
            for node in range(n):
                if loop != 0 and col == 0:
                    continue
                if loop == 0 and col == 0:
                    pos[(loop, col, node)] = (col * col_distance, -node)
                    labels[(loop, col, node)] = f"{col_label}{subscript_letter(node)}"
                else:
                    if len(l) % 2 == 0:
                        if loop % 2 == 0:
                            pos[(loop, col, node)] = (
                                col * col_distance,
                                -node
                                + (row_distance / 2)
                                + row_distance * (int(loop / 2)),
                            )
                            labels[(loop, col, node)] = (
                                f"{col_label}{subscript_letter(node)}"
                            )
                        else:
                            pos[(loop, col, node)] = (
                                col * col_distance,
                                -node
                                - (row_distance / 2)
                                - row_distance * (int(loop / 2)),
                            )
                            labels[(loop, col, node)] = (
                                f"{col_label}{subscript_letter(node)}"
                            )
                    else:
                        if loop % 2 == 0:
                            pos[(loop, col, node)] = (
                                col * col_distance,
                                -node + row_distance * (int(loop / 2)),
                            )
                            labels[(loop, col, node)] = (
                                f"{col_label}{subscript_letter(node)}"
                            )
                        else:
                            pos[(loop, col, node)] = (
                                col * col_distance,
                                -node - row_distance * (int(loop / 2) + 1),
                            )
                            labels[(loop, col, node)] = (
                                f"{col_label}{subscript_letter(node)}"
                            )

    components = list(nx.connected_components(G))
    colors = plt.cm.get_cmap(
        "tab20", len(components)
    )  # Use a colormap with enough colors

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
        if G.edges[edge].get("color") == "invis":
            edge_colors.append("none")  # Invisible edges
        elif G.edges[edge].get("color") == "diag":
            edge_colors.append("tab:green")  # Invisible edges
        else:
            edge_colors.append(node_color_map.get(edge[0], "black"))
    # Draw the graph with colored components
    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        labels=labels,
        with_labels=True,
        node_size=200,
        node_color=[node_color_map[node] for node in G.nodes()],
        edge_color=edge_colors,
        width=2,
        font_weight="bold",
        font_size=10,
    )

    # Set background color to black
    plt.gca().set_facecolor("black")
    plt.show()


def is_connected(G):
    return nx.is_connected(G)


def get_cycle_type(G):
    components = list(nx.connected_components(G))
    type = []
    for component in components:
        s = 0
        for node in component:
            if node[0] == 0:
                s += 1
        type.append(s)
    return type


def is_stop(G):
    components = list(nx.connected_components(G))
    type = []
    for component in components:
        s = 0
        for node in component:
            if node[1] == 0:
                s += 1
        type.append(s)
    if 25 in type:
        return True
    return False


def monte_carlo_simulation(n, l, num_simulations):
    connected_count = 0
    for _ in range(num_simulations):
        G = create_graph_with_transpositions(n, l, diag=False)

        # visualize_graph(G, n, l)
        if is_connected(G):
            connected_count += 1
    return (num_simulations - connected_count) / num_simulations


# Parameters
n = 26
l = [2, 2]
k = [l + 1 for l in l]

# p = monte_carlo_simulation(n, [3], 1000000)
# print(f"[l=2, c=1] -> {p}")
# p = monte_carlo_simulation(n, [3, 3], 1000000)
# print(f"[l=2, c=2] -> {p}")
# p = monte_carlo_simulation(n, [4], 1000000)
# print(f"[l=3, c=1] -> {p}")
# p = monte_carlo_simulation(n, k, 1000000)
# print(f"[l=2-4, c=2] -> {p}")
visualize_graph(create_graph_with_transpositions(n, l, diag=False), n, l)
