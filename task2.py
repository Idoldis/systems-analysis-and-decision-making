import json
import numpy as np

def main(file_path):
    with open(file_path, "r") as read_file:
        data = json.load(read_file)
    
    nodes = data["nodes"]
    num_nodes = len(nodes)
    adjacency_matrix = np.zeros((num_nodes, num_nodes))
    
    for i in range(1, num_nodes + 1):
        current_node = nodes[str(i)]
        for neighbor in current_node:
            t = int(neighbor)
            adjacency_matrix[i - 1][t - 1] = 1
            adjacency_matrix[t - 1][i - 1] = -1

    print(adjacency_matrix)
    
    result = np.zeros((5, num_nodes))
    print(result)

    def search_positive(strok, stolb):
        for u in range(num_nodes):
            if adjacency_matrix[stolb, u] == 1:
                result[2, strok] += 1
                search_positive(strok, u)

    def search_negative(strok, stolb):
        for u in range(num_nodes):
            if adjacency_matrix[stolb, u] == -1:
                result[3, strok] += 1
                search_negative(strok, u)

    def count_positive_edges(strok, stolb):
        for u in range(num_nodes):
            if adjacency_matrix[stolb, u] == 1 and u != strok:
                result[4, strok] += 1

    for i in range(num_nodes):
        for t in range(5):
            if t == 0:
                result[0][i] = np.sum(adjacency_matrix[i] == 1)
            elif t == 1:
                result[1][i] = np.sum(adjacency_matrix[i] == -1)
            elif t == 2:
                for j in range(num_nodes):
                    if adjacency_matrix[i][j] == 1:
                        search_positive(i, j)
            elif t == 3:
                for j in range(num_nodes):
                    if adjacency_matrix[i][j] == -1:
                        search_negative(i, j)
            elif t == 4:
                for j in range(num_nodes):
                    if adjacency_matrix[i][j] == -1:
                        count_positive_edges(i, j)

    return result
