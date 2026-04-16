from __future__ import annotations

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def build_variables() -> dict[str, ctrl.Antecedent | ctrl.Consequent]:
    temperature = ctrl.Antecedent(np.arange(15, 57, 1), "temperature")
    ac_intensity = ctrl.Antecedent(np.arange(0, 11, 1), "ac_intensity")
    speed_kmh = ctrl.Antecedent(np.arange(40, 161, 1), "speed_kmh")
    driving_mode = ctrl.Antecedent(np.arange(1.0, 3.1, 0.1), "driving_mode")
    traffic_level = ctrl.Antecedent(np.arange(1.0, 3.1, 0.1), "traffic_level")
    adjustment_factor = ctrl.Consequent(np.arange(0.40, 1.011, 0.01), "adjustment_factor")

    temperature["pleasant"] = fuzz.trapmf(temperature.universe, [15, 15, 22, 30])
    temperature["hot"] = fuzz.trimf(temperature.universe, [28, 34, 40])
    temperature["very_hot"] = fuzz.trimf(temperature.universe, [38, 43, 49])
    temperature["extremely_hot"] = fuzz.trapmf(temperature.universe, [47, 51, 56, 56])

    ac_intensity["low"] = fuzz.trapmf(ac_intensity.universe, [0, 0, 2, 4])
    ac_intensity["medium"] = fuzz.trimf(ac_intensity.universe, [3, 5, 7])
    ac_intensity["high"] = fuzz.trapmf(ac_intensity.universe, [6, 8, 10, 10])

    speed_kmh["local"] = fuzz.trapmf(speed_kmh.universe, [40, 40, 45, 52])
    speed_kmh["city"] = fuzz.trimf(speed_kmh.universe, [50, 60, 72])
    speed_kmh["highway"] = fuzz.trimf(speed_kmh.universe, [95, 110, 125])
    speed_kmh["fast_highway"] = fuzz.trimf(speed_kmh.universe, [120, 135, 145])
    speed_kmh["extreme_highway"] = fuzz.trapmf(speed_kmh.universe, [140, 150, 160, 160])

    driving_mode["eco"] = fuzz.trapmf(driving_mode.universe, [1, 1, 1.3, 2.0])
    driving_mode["comfort"] = fuzz.trimf(driving_mode.universe, [1, 2, 3])
    driving_mode["sport"] = fuzz.trapmf(driving_mode.universe, [2.0, 2.7, 3.0, 3.0])

    traffic_level["no_traffic"] = fuzz.trapmf(traffic_level.universe, [1, 1, 1.3, 2.0])
    traffic_level["moderate"] = fuzz.trimf(traffic_level.universe, [1, 2, 3])
    traffic_level["high"] = fuzz.trapmf(traffic_level.universe, [2.0, 2.7, 3.0, 3.0])

    adjustment_factor["severe_reduction"] = fuzz.trapmf(
        adjustment_factor.universe, [0.40, 0.40, 0.50, 0.60]
    )
    adjustment_factor["high_reduction"] = fuzz.trimf(
        adjustment_factor.universe, [0.52, 0.62, 0.72]
    )
    adjustment_factor["moderate_reduction"] = fuzz.trimf(
        adjustment_factor.universe, [0.68, 0.77, 0.86]
    )
    adjustment_factor["mild_reduction"] = fuzz.trimf(
        adjustment_factor.universe, [0.84, 0.90, 0.96]
    )
    adjustment_factor["near_nominal"] = fuzz.trapmf(
        adjustment_factor.universe, [0.94, 0.98, 1.01, 1.01]
    )

    return {
        "temperature": temperature,
        "ac_intensity": ac_intensity,
        "speed_kmh": speed_kmh,
        "driving_mode": driving_mode,
        "traffic_level": traffic_level,
        "adjustment_factor": adjustment_factor,
    }
