import numpy as np
import math

def sum_column(matrix, column_index):
    """Суммирует элементы указанного столбца матрицы."""
    return np.sum(matrix[:, column_index])

def main():
    types = 4
    age_groups = 5
    arr = np.array([[20, 15, 10, 5],
                     [30, 20, 15, 10],
                     [25, 25, 20, 15],
                     [20, 20, 25, 20],
                     [15, 15, 30, 25]])
    
    total_sum = np.sum(arr)

    probabilities = arr / total_sum

    res_ent_sov = -np.sum(probabilities * np.log2(probabilities + (probabilities == 0)))

    res_ent_ages = -np.sum(np.sum(probabilities, axis=1) * np.log2(np.sum(probabilities, axis=1) + (np.sum(probabilities, axis=1) == 0)))

    res_ent_types = -np.sum(sum_column(probabilities, k) * np.log2(sum_column(probabilities, k) + (sum_column(probabilities, k) == 0)) for k in range(types))

    res_ent_usl = 0
    for i in range(age_groups):
        temp_sum = np.sum(probabilities[i])
        if temp_sum > 0: 
            conditional_entropy = -np.sum((probabilities[i] / temp_sum) * np.log2((probabilities[i] / temp_sum) + (probabilities[i] == 0)))
            res_ent_usl += conditional_entropy * temp_sum

    result = np.zeros(5)
    
    result[0] = round(res_ent_sov, 2)
    result[1] = round(res_ent_ages, 2)
    result[2] = round(res_ent_types, 2)
    result[3] = round(res_ent_usl, 2)
    result[4] = result[1] - result[3]

    return result

if __name__ == "__main__":
    print(main())
