from __future__ import annotations

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def build_variables() -> dict[str, ctrl.Antecedent | ctrl.Consequent]:
    temperature = ctrl.Antecedent(np.arange(0, 56, 1), "temperature")
    ac_intensity = ctrl.Antecedent(np.arange(0, 11, 1), "ac_intensity")
    driving_style = ctrl.Antecedent(np.arange(0, 11, 1), "driving_style")
    traffic_level = ctrl.Antecedent(np.arange(0, 11, 1), "traffic_level")
    adjustment_factor = ctrl.Consequent(np.arange(0.45, 1.051, 0.01), "adjustment_factor")

    temperature["mild"] = fuzz.trapmf(temperature.universe, [0, 0, 18, 28])
    temperature["warm"] = fuzz.trimf(temperature.universe, [24, 32, 40])
    temperature["hot"] = fuzz.trapmf(temperature.universe, [36, 42, 55, 55])

    ac_intensity["low"] = fuzz.trapmf(ac_intensity.universe, [0, 0, 2, 4])
    ac_intensity["medium"] = fuzz.trimf(ac_intensity.universe, [3, 5, 7])
    ac_intensity["high"] = fuzz.trapmf(ac_intensity.universe, [6, 8, 10, 10])

    driving_style["efficient"] = fuzz.trapmf(driving_style.universe, [0, 0, 2, 4])
    driving_style["balanced"] = fuzz.trimf(driving_style.universe, [3, 5, 7])
    driving_style["aggressive"] = fuzz.trapmf(driving_style.universe, [6, 8, 10, 10])

    traffic_level["light"] = fuzz.trapmf(traffic_level.universe, [0, 0, 2, 4])
    traffic_level["moderate"] = fuzz.trimf(traffic_level.universe, [3, 5, 7])
    traffic_level["heavy"] = fuzz.trapmf(traffic_level.universe, [6, 8, 10, 10])

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
        "driving_style": driving_style,
        "traffic_level": traffic_level,
        "adjustment_factor": adjustment_factor,
    }

