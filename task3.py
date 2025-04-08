import json
import numpy as np

def main(file_path):
    with open(file_path, "r") as read_file:
        data = json.load(read_file)
    
    nodes = data["nodes"]
    num_nodes = len(nodes)
    adjacency_matrix = np.zeros((num_nodes, num_nodes))
    
    for i in range(1, num_nodes + 1):
        neighbors = nodes[str(i)]
        for neighbor in neighbors:
            t = int(neighbor)
            adjacency_matrix[i - 1][t - 1] = 1

    result_matrix = adjacency_matrix.copy()

    def search(i, j):
        nonlocal result_matrix
        for t in range(num_nodes):
            if result_matrix[j, t] != 0:
                if result_matrix[i, t] == 0:
                    result_matrix[i, t] += 2
                else:
                    result_matrix[i, t] += 1
                search(i, t)

    edge_count = 0
    for i in range(num_nodes):
        for j in range(num_nodes):
            if result_matrix[i][j] != 0:
                search(i, j)
            if adjacency_matrix[i][j] == 1:
                edge_count += 1

    total_sum = 0
    for j in range(num_nodes):
        for i in range(edge_count):
            if result_matrix[j][i] != 0:
                total_sum += (result_matrix[j][i] / (num_nodes - 1)) * np.log2(result_matrix[j][i] / (num_nodes - 1))
    
    total_sum = round(-total_sum, 1)

    return total_sum
