from __future__ import annotations

from functools import lru_cache

import pandas as pd
from skfuzzy import control as ctrl

from src.analysis.dataset_range_model import DatasetRangeEstimate, build_dataset_multiplier
from src.config import (
    AC_LEVEL_VALUES,
    FINAL_RANGE_CLAIM_CAP,
    FUZZY_FACTOR_MAX,
    FUZZY_FACTOR_MIN,
    TEMPERATURE_LEVEL_VALUES,
)
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
    temperature_level: str,
    ac_level: str,
) -> float:
    simulation = ctrl.ControlSystemSimulation(build_control_system())
    simulation.input["temperature"] = TEMPERATURE_LEVEL_VALUES[temperature_level]
    simulation.input["ac_intensity"] = AC_LEVEL_VALUES[ac_level]
    simulation.compute()
    adjustment_factor = simulation.output.get("fuzzy_adjustment_factor", 1.0)
    return max(min(float(adjustment_factor), FUZZY_FACTOR_MAX), FUZZY_FACTOR_MIN)


def predict_adjusted_range(
    *,
    manufacturer_range_km: float,
    battery_pct: float,
    temperature_level: str,
    ac_level: str,
    speed_level: str,
    driving_mode: str,
    traffic_level: str,
    dataset: pd.DataFrame | None = None,
) -> dict[str, float | str | list[str]]:
    claimed_remaining_km = max(manufacturer_range_km, 0) * max(min(battery_pct, 100), 0) / 100

    if dataset is None:
        dataset_estimate = DatasetRangeEstimate(
            multiplier=1.0,
            selected_efficiency=1.0,
            reference_efficiency=1.0,
            fallback_level="unavailable",
            proxy_speed_level=speed_level,
            sample_count=0,
        )
    else:
        dataset_estimate = build_dataset_multiplier(
            dataset,
            speed_level=speed_level,
            driving_mode=driving_mode,
            traffic_level=traffic_level,
        )
    shown_range_km = max(claimed_remaining_km * dataset_estimate.multiplier, 0.0)

    fuzzy_adjustment_factor = _compute_adjustment_factor(
        temperature_level=temperature_level,
        ac_level=ac_level,
    )
    adjusted_range_km = max(shown_range_km * fuzzy_adjustment_factor, 0.0)
    adjusted_range_cap = claimed_remaining_km * FINAL_RANGE_CLAIM_CAP
    adjusted_range_km = min(adjusted_range_km, adjusted_range_cap) if claimed_remaining_km else 0.0
    range_delta_vs_shown_km = adjusted_range_km - shown_range_km
    range_delta_vs_claimed_km = adjusted_range_km - claimed_remaining_km

    explanation = build_explanation(
        battery_pct=battery_pct,
        temperature_level=temperature_level,
        ac_level=ac_level,
        speed_level=speed_level,
        driving_mode=driving_mode,
        traffic_level=traffic_level,
        dataset_multiplier=dataset_estimate.multiplier,
        fuzzy_adjustment_factor=fuzzy_adjustment_factor,
        dataset_fallback_level=dataset_estimate.fallback_level,
        proxy_speed_level=dataset_estimate.proxy_speed_level,
        sample_count=dataset_estimate.sample_count,
    )

    return {
        "claimed_remaining_km": round(claimed_remaining_km, 2),
        "dataset_multiplier": round(dataset_estimate.multiplier, 3),
        "shown_range_km": round(shown_range_km, 2),
        "fuzzy_adjustment_factor": round(fuzzy_adjustment_factor, 3),
        "adjusted_range_km": round(adjusted_range_km, 2),
        "range_delta_vs_shown_km": round(range_delta_vs_shown_km, 2),
        "range_delta_vs_claimed_km": round(range_delta_vs_claimed_km, 2),
        "dataset_fallback_level": dataset_estimate.fallback_level,
        "dataset_bucket_used": f"{speed_level} / {driving_mode} / {traffic_level}",
        "dataset_proxy_speed_level": dataset_estimate.proxy_speed_level,
        "dataset_sample_count": dataset_estimate.sample_count,
        "dataset_selected_efficiency": round(dataset_estimate.selected_efficiency, 3),
        "dataset_reference_efficiency": round(dataset_estimate.reference_efficiency, 3),
        "summary": explanation["summary"],
        "dataset_summary_driver": explanation["dataset_summary_driver"],
        "fuzzy_summary_driver": explanation["fuzzy_summary_driver"],
        "drivers": explanation["drivers"],
    }
