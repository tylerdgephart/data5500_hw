# Prompt to ChatGPT: "Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph that have a degree greater than 5 using edges = [] and edges.append(). Then print the output to the console."
# Now repeat the code for hard.py but print the output to the console

import networkx as nx

def count_high_degree_nodes(graph):
    """Returns the number of nodes in the input graph with a degree greater than 5 by appending high-degree nodes to a list and counting the list length."""
    high_degree_nodes = []
    for node in graph.nodes:
        if graph.degree(node) > 5:
            high_degree_nodes.append(node)
    return len(high_degree_nodes)

# Sample graph to test the function
G = nx.Graph()
# Adding nodes and edges to create nodes with a degree greater than 5
edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (1, 3), (1, 4), (1, 5), (1, 6)]
G.add_edges_from(edges)

# Print the output
print("Number of nodes with degree greater than 5:", count_high_degree_nodes(G))
