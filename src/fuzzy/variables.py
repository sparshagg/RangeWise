from __future__ import annotations

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def build_variables() -> dict[str, ctrl.Antecedent | ctrl.Consequent]:
    temperature = ctrl.Antecedent(np.arange(0, 56, 1), "temperature")
    ac_intensity = ctrl.Antecedent(np.arange(0, 11, 1), "ac_intensity")
    speed_kmh = ctrl.Antecedent(np.arange(0, 121, 1), "speed_kmh")
    driving_mode = ctrl.Antecedent(np.arange(1.0, 3.1, 0.1), "driving_mode")
    traffic_condition = ctrl.Antecedent(np.arange(1.0, 3.1, 0.1), "traffic_condition")
    adjustment_factor = ctrl.Consequent(np.arange(0.45, 1.051, 0.01), "adjustment_factor")

    temperature["mild"] = fuzz.trapmf(temperature.universe, [0, 0, 20, 28])
    temperature["warm"] = fuzz.trimf(temperature.universe, [24, 32, 40])
    temperature["hot"] = fuzz.trapmf(temperature.universe, [36, 42, 55, 55])

    ac_intensity["low"] = fuzz.trapmf(ac_intensity.universe, [0, 0, 2, 4])
    ac_intensity["medium"] = fuzz.trimf(ac_intensity.universe, [3, 5, 7])
    ac_intensity["high"] = fuzz.trapmf(ac_intensity.universe, [6, 8, 10, 10])

    speed_kmh["urban"] = fuzz.trapmf(speed_kmh.universe, [0, 0, 30, 50])
    speed_kmh["mixed"] = fuzz.trimf(speed_kmh.universe, [40, 58, 85])
    speed_kmh["highway"] = fuzz.trapmf(speed_kmh.universe, [75, 95, 120, 120])

    driving_mode["eco"] = fuzz.trimf(driving_mode.universe, [1, 1, 2])
    driving_mode["normal"] = fuzz.trimf(driving_mode.universe, [1, 2, 3])
    driving_mode["sport"] = fuzz.trimf(driving_mode.universe, [2, 3, 3])

    traffic_condition["light"] = fuzz.trimf(traffic_condition.universe, [1, 1, 2])
    traffic_condition["moderate"] = fuzz.trimf(traffic_condition.universe, [1, 2, 3])
    traffic_condition["heavy"] = fuzz.trimf(traffic_condition.universe, [2, 3, 3])

    adjustment_factor["severe_reduction"] = fuzz.trapmf(
        adjustment_factor.universe, [0.45, 0.45, 0.55, 0.68]
    )
    adjustment_factor["moderate_reduction"] = fuzz.trimf(
        adjustment_factor.universe, [0.62, 0.74, 0.84]
    )
    adjustment_factor["mild_reduction"] = fuzz.trimf(
        adjustment_factor.universe, [0.80, 0.89, 0.97]
    )
    adjustment_factor["near_nominal"] = fuzz.trapmf(
        adjustment_factor.universe, [0.93, 0.98, 1.05, 1.05]
    )

    return {
        "temperature": temperature,
        "ac_intensity": ac_intensity,
        "speed_kmh": speed_kmh,
        "driving_mode": driving_mode,
        "traffic_condition": traffic_condition,
        "adjustment_factor": adjustment_factor,
    }
