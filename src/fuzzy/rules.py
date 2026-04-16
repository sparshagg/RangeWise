from __future__ import annotations

from skfuzzy import control as ctrl


def build_rules(variables: dict[str, ctrl.Antecedent | ctrl.Consequent]) -> list[ctrl.Rule]:
    temperature = variables["temperature"]
    ac_intensity = variables["ac_intensity"]
    driving_style = variables["driving_style"]
    traffic_level = variables["traffic_level"]
    adjustment_factor = variables["adjustment_factor"]

    return [
        ctrl.Rule(
            temperature["hot"] & ac_intensity["high"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            temperature["hot"] & driving_style["aggressive"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            traffic_level["heavy"] & driving_style["aggressive"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            temperature["hot"] & traffic_level["heavy"],
            adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            temperature["warm"] & ac_intensity["medium"],
            adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            traffic_level["heavy"] & ac_intensity["high"],
            adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            temperature["mild"]
            & ac_intensity["low"]
            & driving_style["efficient"]
            & traffic_level["light"],
            adjustment_factor["near_nominal"],
        ),
        ctrl.Rule(
            temperature["mild"] & driving_style["balanced"],
            adjustment_factor["mild_reduction"],
        ),
        ctrl.Rule(
            temperature["warm"] & driving_style["efficient"] & ac_intensity["low"],
            adjustment_factor["mild_reduction"],
        ),
        ctrl.Rule(
            traffic_level["moderate"] & driving_style["balanced"],
            adjustment_factor["mild_reduction"],
        ),
    ]

