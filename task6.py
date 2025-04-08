import json
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import trapezoid

def main(temperature_sets_json, heating_sets_json, rules_json, current_temperature):
    """
    Реализует алгоритм нечеткого управления.

    Args:
        temperature_sets_json: JSON-строка с описанием функций принадлежности для температуры.
        heating_sets_json: JSON-строка с описанием функций принадлежности для уровня нагрева.
        rules_json: JSON-строка с описанием правил нечеткого управления.
        current_temperature: Текущее значение температуры (вещественное число).

    Returns:
        Вещественное число значения оптимального управления (уровень нагрева).
    """
    try:
        temperature_sets = json.loads(temperature_sets_json)
        heating_sets = json.loads(heating_sets_json)
        rules = json.loads(rules_json)
    except json.JSONDecodeError:
        return "Ошибка: Неверный формат JSON-строки."

    def create_interp_function(points):
        """Создает интерполяционную функцию на основе заданных точек."""
        x = np.array([point[0] for point in points])
        y = np.array([point[1] for point in points])

        unique_x, index, counts = np.unique(x, return_index=True, return_counts=True)
        averaged_y = np.array([np.mean(y[i:i+c]) for i,c in zip(index, counts)])

        return interp1d(unique_x, averaged_y, kind='linear', fill_value="extrapolate")

    temp_functions = {term["id"]: create_interp_function(term["points"]) for term in temperature_sets["температура"]}

    heating_functions = {term["id"]: create_interp_function(term["points"]) for term in heating_sets["температура"]}

    membership_degrees = {term_id: temp_functions[term_id](current_temperature) for term_id in temp_functions}

    heating_membership = {}
    for temp_term, heating_term in rules:
        degree = min(membership_degrees[temp_term], 1) 
        if heating_term in heating_membership:
            heating_membership[heating_term] = max(heating_membership[heating_term], degree)
        else:
            heating_membership[heating_term] = degree

    numerator = 0
    denominator = 0

    for term_id, degree in heating_membership.items():
        x = np.linspace(0, 26, 100) 
        y = heating_functions[term_id](x)
        
        if np.sum(y) > 0: 
            centroid = trapezoid(x * y, x) / trapezoid(y, x)
            numerator += centroid * degree
            denominator += degree

    if denominator == 0:
        return 0  

    optimal_heating = numerator / denominator

    return round(optimal_heating, 2)

temperature_sets_json = """
{
  "температура": [
      {
      "id": "холодно",
      "points": [
          [0,1],
          [18,1],
          [22,0],
          [50,0]
      ]
      },
      {
      "id": "комфортно",
      "points": [
          [18,0],
          [22,1],
          [24,1],
          [26,0]
      ]
      },
      {
      "id": "жарко",
      "points": [
          [24,0],
          [26,1],
          [50,1]
      ]
      }
  ]
}
"""

heating_sets_json = """
{
  "температура": [
      {
        "id": "слабый",
        "points": [
            [0,0],
            [0,1],
            [5,1],
            [8,0]
        ]
      },
      {
        "id": "умеренный",
        "points": [
            [5,0],
            [8,1],
            [13,1],
            [16,0]
        ]
      },
      {
        "id": "интенсивный",
        "points": [
            [13,0],
            [18,1],
            [23,1],
            [26,0]
        ]
      }
  ]
}
"""

rules_json = """
[
    ["холодно", "интенсивный"],
    ["комфортно", "умеренный"],
    ["жарко", "слабый"]
]
"""

current_temp_values = [-24.00, 23]

for current_temp in current_temp_values:
    optimal_heating = main(temperature_sets_json, heating_sets_json, rules_json, current_temp)
    print(f"Оптимальный уровень нагрева при температуре {current_temp}°C: {optimal_heating}")
