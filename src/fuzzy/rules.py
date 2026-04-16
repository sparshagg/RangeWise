from __future__ import annotations

from skfuzzy import control as ctrl


def build_rules(variables: dict[str, ctrl.Antecedent | ctrl.Consequent]) -> list[ctrl.Rule]:
    temperature = variables["temperature"]
    ac_intensity = variables["ac_intensity"]
    speed_kmh = variables["speed_kmh"]
    driving_mode = variables["driving_mode"]
    traffic_level = variables["traffic_level"]
    adjustment_factor = variables["adjustment_factor"]

    return [
        ctrl.Rule(temperature["pleasant"], adjustment_factor["near_nominal"]),
        ctrl.Rule(temperature["hot"], adjustment_factor["mild_reduction"]),
        ctrl.Rule(temperature["very_hot"], adjustment_factor["moderate_reduction"]),
        ctrl.Rule(temperature["extremely_hot"], adjustment_factor["high_reduction"]),
        ctrl.Rule(ac_intensity["low"], adjustment_factor["near_nominal"]),
        ctrl.Rule(ac_intensity["medium"], adjustment_factor["mild_reduction"]),
        ctrl.Rule(ac_intensity["high"], adjustment_factor["moderate_reduction"]),
        ctrl.Rule(speed_kmh["local"], adjustment_factor["near_nominal"]),
        ctrl.Rule(speed_kmh["city"], adjustment_factor["mild_reduction"]),
        ctrl.Rule(speed_kmh["highway"], adjustment_factor["moderate_reduction"]),
        ctrl.Rule(speed_kmh["fast_highway"], adjustment_factor["high_reduction"]),
        ctrl.Rule(speed_kmh["extreme_highway"], adjustment_factor["severe_reduction"]),
        ctrl.Rule(driving_mode["eco"], adjustment_factor["near_nominal"]),
        ctrl.Rule(driving_mode["comfort"], adjustment_factor["mild_reduction"]),
        ctrl.Rule(driving_mode["sport"], adjustment_factor["high_reduction"]),
        ctrl.Rule(traffic_level["no_traffic"], adjustment_factor["near_nominal"]),
        ctrl.Rule(traffic_level["moderate"], adjustment_factor["mild_reduction"]),
        ctrl.Rule(traffic_level["high"], adjustment_factor["high_reduction"]),
        ctrl.Rule(
            temperature["extremely_hot"] & ac_intensity["high"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            temperature["very_hot"] & ac_intensity["high"],
            adjustment_factor["high_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["extreme_highway"] & driving_mode["sport"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["fast_highway"] & driving_mode["sport"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["highway"] & driving_mode["sport"],
            adjustment_factor["high_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["highway"] & driving_mode["comfort"],
            adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["highway"] & driving_mode["eco"],
            adjustment_factor["mild_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["extreme_highway"] & temperature["extremely_hot"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["fast_highway"] & temperature["very_hot"],
            adjustment_factor["high_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["highway"] & temperature["very_hot"],
            adjustment_factor["high_reduction"],
        ),
        ctrl.Rule(
            driving_mode["sport"] & ac_intensity["high"],
            adjustment_factor["high_reduction"],
        ),
        ctrl.Rule(
            traffic_level["high"] & ac_intensity["high"],
            adjustment_factor["high_reduction"],
        ),
        ctrl.Rule(
            traffic_level["high"] & driving_mode["sport"],
            adjustment_factor["high_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["fast_highway"] & ac_intensity["high"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["highway"] & ac_intensity["high"],
            adjustment_factor["high_reduction"],
        ),
        ctrl.Rule(
            traffic_level["high"] & speed_kmh["fast_highway"],
            adjustment_factor["severe_reduction"],
        ),
        ctrl.Rule(
            traffic_level["high"] & speed_kmh["highway"],
            adjustment_factor["high_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["city"] & traffic_level["moderate"],
            adjustment_factor["mild_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["city"] & traffic_level["high"],
            adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            temperature["pleasant"]
            & ac_intensity["low"]
            & driving_mode["eco"]
            & speed_kmh["local"]
            & traffic_level["no_traffic"],
            adjustment_factor["near_nominal"],
        ),
        ctrl.Rule(
            temperature["hot"]
            & ac_intensity["low"]
            & speed_kmh["city"]
            & driving_mode["eco"]
            & traffic_level["no_traffic"],
            adjustment_factor["near_nominal"],
        ),
        ctrl.Rule(
            temperature["pleasant"] & driving_mode["eco"] & traffic_level["no_traffic"],
            adjustment_factor["near_nominal"],
        ),
        ctrl.Rule(
            temperature["hot"] & driving_mode["comfort"] & traffic_level["moderate"],
            adjustment_factor["mild_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["city"] & driving_mode["comfort"],
            adjustment_factor["mild_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["local"] & traffic_level["high"],
            adjustment_factor["mild_reduction"],
        ),
    ]
