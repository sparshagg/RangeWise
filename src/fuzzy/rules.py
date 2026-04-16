from __future__ import annotations

from skfuzzy import control as ctrl


def build_rules(variables: dict[str, ctrl.Antecedent | ctrl.Consequent]) -> list[ctrl.Rule]:
    temperature = variables["temperature"]
    ac_intensity = variables["ac_intensity"]
    speed_kmh = variables["speed_kmh"]
    driving_mode = variables["driving_mode"]
    traffic_condition = variables["traffic_condition"]
    adjustment_factor = variables["adjustment_factor"]

    return [
        ctrl.Rule(
            temperature["hot"] & ac_intensity["high"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["highway"] & driving_mode["sport"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["highway"] & temperature["hot"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            driving_mode["sport"] & ac_intensity["high"],
            adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["highway"],
            adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            traffic_condition["heavy"] & ac_intensity["high"],
            adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["highway"] & traffic_condition["heavy"],
            adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            driving_mode["normal"] & speed_kmh["mixed"],
            adjustment_factor["mild_reduction"],
        ),
        ctrl.Rule(
            temperature["warm"] & ac_intensity["medium"],
            adjustment_factor["mild_reduction"],
        ),
        ctrl.Rule(
            traffic_condition["moderate"] & driving_mode["normal"],
            adjustment_factor["mild_reduction"],
        ),
        ctrl.Rule(
            temperature["mild"]
            & ac_intensity["low"]
            & driving_mode["eco"]
            & traffic_condition["light"],
            adjustment_factor["near_nominal"],
        ),
        ctrl.Rule(
            temperature["warm"]
            & ac_intensity["low"]
            & driving_mode["eco"]
            & traffic_condition["light"],
            adjustment_factor["near_nominal"],
        ),
    ]
