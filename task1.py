import json
import numpy as np

def main(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    
    nodes = data["nodes"]
    num_nodes = len(nodes)
    adjacency_matrix = np.zeros((num_nodes, num_nodes))
    
    for index in range(1, num_nodes + 1):
        current_node = nodes[str(index)]
        for neighbor in current_node:
            neighbor_index = int(neighbor)
            adjacency_matrix[index - 1][neighbor_index - 1] = 1
            
    return adjacency_matrix
