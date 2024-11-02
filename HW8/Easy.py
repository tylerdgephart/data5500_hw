#Problem 1

# Prompt to ChatGPT: "Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph using edges = [] and edges.append(). Then print the output to the console."

import networkx as nx

def count_nodes(graph):
    """Returns the number of nodes in the input graph by appending each node to a list and counting the list length."""
    nodes = []
    for node in graph.nodes:
        nodes.append(node)
    return len(nodes)

# Sample graph to test the function
G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])

# Print the output
print("Number of nodes in the graph:", count_nodes(G))