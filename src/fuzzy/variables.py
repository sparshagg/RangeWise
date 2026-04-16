from __future__ import annotations

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from src.config import FUZZY_FACTOR_MAX, FUZZY_FACTOR_MIN


def build_variables() -> dict[str, ctrl.Antecedent | ctrl.Consequent]:
    temperature = ctrl.Antecedent(np.arange(15, 57, 1), "temperature")
    ac_intensity = ctrl.Antecedent(np.arange(0, 11, 1), "ac_intensity")
    fuzzy_adjustment_factor = ctrl.Consequent(
        np.arange(FUZZY_FACTOR_MIN, FUZZY_FACTOR_MAX + 0.001, 0.001),
        "fuzzy_adjustment_factor",
    )

    temperature["pleasant"] = fuzz.trapmf(temperature.universe, [15, 15, 22, 30])
    temperature["hot"] = fuzz.trimf(temperature.universe, [28, 34, 40])
    temperature["very_hot"] = fuzz.trimf(temperature.universe, [38, 43, 49])
    temperature["extremely_hot"] = fuzz.trapmf(temperature.universe, [47, 51, 56, 56])

    ac_intensity["low"] = fuzz.trapmf(ac_intensity.universe, [0, 0, 2, 4])
    ac_intensity["medium"] = fuzz.trimf(ac_intensity.universe, [3, 5, 7])
    ac_intensity["high"] = fuzz.trapmf(ac_intensity.universe, [6, 8, 10, 10])

    fuzzy_adjustment_factor["strong_reduction"] = fuzz.trapmf(
        fuzzy_adjustment_factor.universe, [FUZZY_FACTOR_MIN, FUZZY_FACTOR_MIN, 0.86, 0.90]
    )
    fuzzy_adjustment_factor["moderate_reduction"] = fuzz.trimf(
        fuzzy_adjustment_factor.universe, [0.88, 0.92, 0.97]
    )
    fuzzy_adjustment_factor["light_reduction"] = fuzz.trimf(
        fuzzy_adjustment_factor.universe, [0.95, 0.985, 1.0]
    )
    fuzzy_adjustment_factor["neutral"] = fuzz.trimf(
        fuzzy_adjustment_factor.universe, [0.99, 1.0, 1.02]
    )
    fuzzy_adjustment_factor["mild_uplift"] = fuzz.trimf(
        fuzzy_adjustment_factor.universe, [1.01, 1.04, 1.06]
    )
    fuzzy_adjustment_factor["best_case_uplift"] = fuzz.trapmf(
        fuzzy_adjustment_factor.universe, [1.04, 1.06, FUZZY_FACTOR_MAX, FUZZY_FACTOR_MAX]
    )

    return {
        "temperature": temperature,
        "ac_intensity": ac_intensity,
        "fuzzy_adjustment_factor": fuzzy_adjustment_factor,
    }
