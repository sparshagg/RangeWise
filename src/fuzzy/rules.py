from __future__ import annotations

from skfuzzy import control as ctrl


def build_rules(variables: dict[str, ctrl.Antecedent | ctrl.Consequent]) -> list[ctrl.Rule]:
    temperature = variables["temperature"]
    ac_intensity = variables["ac_intensity"]
    speed_kmh = variables["speed_kmh"]
    driving_mode = variables["driving_mode"]
    traffic_level = variables["traffic_level"]
    fuzzy_adjustment_factor = variables["fuzzy_adjustment_factor"]

    return [
        ctrl.Rule(temperature["pleasant"], fuzzy_adjustment_factor["mild_uplift"]),
        ctrl.Rule(temperature["hot"], fuzzy_adjustment_factor["neutral"]),
        ctrl.Rule(temperature["very_hot"], fuzzy_adjustment_factor["moderate_reduction"]),
        ctrl.Rule(temperature["extremely_hot"], fuzzy_adjustment_factor["strong_reduction"]),

        ctrl.Rule(ac_intensity["low"], fuzzy_adjustment_factor["mild_uplift"]),
        ctrl.Rule(ac_intensity["medium"], fuzzy_adjustment_factor["neutral"]),
        ctrl.Rule(ac_intensity["high"], fuzzy_adjustment_factor["moderate_reduction"]),

        ctrl.Rule(speed_kmh["local"], fuzzy_adjustment_factor["mild_uplift"]),
        ctrl.Rule(speed_kmh["city"], fuzzy_adjustment_factor["neutral"]),
        ctrl.Rule(speed_kmh["highway"], fuzzy_adjustment_factor["light_reduction"]),
        ctrl.Rule(speed_kmh["fast_highway"], fuzzy_adjustment_factor["moderate_reduction"]),
        ctrl.Rule(speed_kmh["extreme_highway"], fuzzy_adjustment_factor["strong_reduction"]),

        ctrl.Rule(driving_mode["eco"], fuzzy_adjustment_factor["mild_uplift"]),
        ctrl.Rule(driving_mode["comfort"], fuzzy_adjustment_factor["neutral"]),
        ctrl.Rule(driving_mode["sport"], fuzzy_adjustment_factor["moderate_reduction"]),

        ctrl.Rule(traffic_level["no_traffic"], fuzzy_adjustment_factor["mild_uplift"]),
        ctrl.Rule(traffic_level["moderate"], fuzzy_adjustment_factor["neutral"]),
        ctrl.Rule(traffic_level["high"], fuzzy_adjustment_factor["light_reduction"]),

        ctrl.Rule(
            temperature["pleasant"] & ac_intensity["low"] & driving_mode["eco"] & traffic_level["no_traffic"],
            fuzzy_adjustment_factor["best_case_uplift"],
        ),
        ctrl.Rule(
            temperature["pleasant"] & ac_intensity["low"] & speed_kmh["highway"] & driving_mode["eco"],
            fuzzy_adjustment_factor["mild_uplift"],
        ),
        ctrl.Rule(
            temperature["pleasant"] & ac_intensity["medium"] & speed_kmh["city"] & traffic_level["moderate"],
            fuzzy_adjustment_factor["neutral"],
        ),
        ctrl.Rule(
            temperature["hot"] & ac_intensity["low"] & speed_kmh["city"] & driving_mode["eco"],
            fuzzy_adjustment_factor["neutral"],
        ),
        ctrl.Rule(
            temperature["hot"] & ac_intensity["high"],
            fuzzy_adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            temperature["very_hot"] & ac_intensity["high"],
            fuzzy_adjustment_factor["strong_reduction"],
        ),
        ctrl.Rule(
            temperature["extremely_hot"] & ac_intensity["medium"],
            fuzzy_adjustment_factor["strong_reduction"],
        ),
        ctrl.Rule(
            temperature["extremely_hot"] & ac_intensity["high"],
            fuzzy_adjustment_factor["strong_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["highway"] & driving_mode["eco"] & traffic_level["no_traffic"],
            fuzzy_adjustment_factor["neutral"],
        ),
        ctrl.Rule(
            speed_kmh["highway"] & driving_mode["sport"],
            fuzzy_adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["fast_highway"] & driving_mode["sport"],
            fuzzy_adjustment_factor["strong_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["extreme_highway"] & driving_mode["sport"],
            fuzzy_adjustment_factor["strong_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["fast_highway"] & traffic_level["high"],
            fuzzy_adjustment_factor["strong_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["extreme_highway"] & traffic_level["high"],
            fuzzy_adjustment_factor["strong_reduction"],
        ),
        ctrl.Rule(
            traffic_level["high"] & driving_mode["sport"],
            fuzzy_adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            traffic_level["high"] & ac_intensity["high"],
            fuzzy_adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            traffic_level["high"] & temperature["very_hot"],
            fuzzy_adjustment_factor["moderate_reduction"],
        ),
        ctrl.Rule(
            traffic_level["high"] & temperature["extremely_hot"],
            fuzzy_adjustment_factor["strong_reduction"],
        ),
        ctrl.Rule(
            speed_kmh["local"] & traffic_level["no_traffic"] & driving_mode["eco"],
            fuzzy_adjustment_factor["mild_uplift"],
        ),
        ctrl.Rule(
            speed_kmh["city"] & traffic_level["no_traffic"] & driving_mode["eco"],
            fuzzy_adjustment_factor["mild_uplift"],
        ),
    ]
