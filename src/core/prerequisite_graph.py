import json
import networkx as nx


def process_prerequisites(input_file):
    with open(input_file, 'r') as file:
        prerequisites_data = json.load(file)
    return create_prerequisite_graph(prerequisites_data)


def create_prerequisite_graph(prerequisites_data):
    graph = nx.DiGraph()  # Create a directed graph

    for course, prerequisites in prerequisites_data.items():
        for prerequisite in prerequisites:
            graph.add_edge(course, prerequisite)  # Add edges representing prerequisites

    return graph
