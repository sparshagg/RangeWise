from __future__ import annotations

from functools import lru_cache

from skfuzzy import control as ctrl

from src.fuzzy.explain import build_explanation
from src.fuzzy.rules import build_rules
from src.fuzzy.variables import build_variables


@lru_cache(maxsize=1)
def build_control_system() -> ctrl.ControlSystem:
    variables = build_variables()
    rules = build_rules(variables)
    return ctrl.ControlSystem(rules)


def _compute_adjustment_factor(
    *,
    temperature_c: float,
    ac_intensity: float,
    driving_style: float,
    traffic_level: float,
) -> float:
    simulation = ctrl.ControlSystemSimulation(build_control_system())
    simulation.input["temperature"] = temperature_c
    simulation.input["ac_intensity"] = ac_intensity
    simulation.input["driving_style"] = driving_style
    simulation.input["traffic_level"] = traffic_level
    simulation.compute()
    return float(simulation.output["adjustment_factor"])


def predict_adjusted_range(
    *,
    manufacturer_range_km: float,
    battery_pct: float,
    temperature_c: float,
    ac_intensity: float,
    driving_style: float,
    traffic_level: float,
) -> dict[str, float | str | list[str]]:
    baseline_remaining_km = max(manufacturer_range_km, 0) * max(min(battery_pct, 100), 0) / 100
    adjustment_factor = _compute_adjustment_factor(
        temperature_c=temperature_c,
        ac_intensity=ac_intensity,
        driving_style=driving_style,
        traffic_level=traffic_level,
    )
    adjusted_range_km = max(baseline_remaining_km * adjustment_factor, 0.0)
    range_delta_km = adjusted_range_km - baseline_remaining_km

    explanation = build_explanation(
        battery_pct=battery_pct,
        temperature_c=temperature_c,
        ac_intensity=ac_intensity,
        driving_style=driving_style,
        traffic_level=traffic_level,
        adjustment_factor=adjustment_factor,
    )

    return {
        "baseline_remaining_km": round(baseline_remaining_km, 2),
        "adjustment_factor": round(adjustment_factor, 3),
        "adjusted_range_km": round(adjusted_range_km, 2),
        "range_delta_km": round(range_delta_km, 2),
        "summary": explanation["summary"],
        "drivers": explanation["drivers"],
    }

