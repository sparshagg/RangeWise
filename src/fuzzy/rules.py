from __future__ import annotations

from skfuzzy import control as ctrl


def build_rules(variables: dict[str, ctrl.Antecedent | ctrl.Consequent]) -> list[ctrl.Rule]:
    temperature = variables["temperature"]
    ac_intensity = variables["ac_intensity"]
    fuzzy_adjustment_factor = variables["fuzzy_adjustment_factor"]

    return [
        ctrl.Rule(temperature["pleasant"] & ac_intensity["low"], fuzzy_adjustment_factor["best_case_uplift"]),
        ctrl.Rule(temperature["pleasant"] & ac_intensity["medium"], fuzzy_adjustment_factor["mild_uplift"]),
        ctrl.Rule(temperature["pleasant"] & ac_intensity["high"], fuzzy_adjustment_factor["light_reduction"]),
        ctrl.Rule(temperature["hot"] & ac_intensity["low"], fuzzy_adjustment_factor["neutral"]),
        ctrl.Rule(temperature["hot"] & ac_intensity["medium"], fuzzy_adjustment_factor["light_reduction"]),
        ctrl.Rule(temperature["hot"] & ac_intensity["high"], fuzzy_adjustment_factor["moderate_reduction"]),
        ctrl.Rule(temperature["very_hot"] & ac_intensity["low"], fuzzy_adjustment_factor["light_reduction"]),
        ctrl.Rule(temperature["very_hot"] & ac_intensity["medium"], fuzzy_adjustment_factor["moderate_reduction"]),
        ctrl.Rule(temperature["very_hot"] & ac_intensity["high"], fuzzy_adjustment_factor["strong_reduction"]),
        ctrl.Rule(temperature["extremely_hot"] & ac_intensity["low"], fuzzy_adjustment_factor["moderate_reduction"]),
        ctrl.Rule(temperature["extremely_hot"] & ac_intensity["medium"], fuzzy_adjustment_factor["strong_reduction"]),
        ctrl.Rule(temperature["extremely_hot"] & ac_intensity["high"], fuzzy_adjustment_factor["strong_reduction"]),
        ctrl.Rule(temperature["pleasant"], fuzzy_adjustment_factor["neutral"]),
        ctrl.Rule(temperature["hot"], fuzzy_adjustment_factor["light_reduction"]),
        ctrl.Rule(temperature["very_hot"], fuzzy_adjustment_factor["moderate_reduction"]),
        ctrl.Rule(temperature["extremely_hot"], fuzzy_adjustment_factor["strong_reduction"]),
        ctrl.Rule(ac_intensity["low"], fuzzy_adjustment_factor["mild_uplift"]),
        ctrl.Rule(ac_intensity["medium"], fuzzy_adjustment_factor["neutral"]),
        ctrl.Rule(ac_intensity["high"], fuzzy_adjustment_factor["moderate_reduction"]),
    ]
