"""
UAE severity-weighted hybrid combiner.

Merges the Mamdani fuzzy adjustment factor with the ANFIS adjustment factor
using weights that shift toward ANFIS under extreme UAE conditions.
"""

from __future__ import annotations

from src.config import (
    FINAL_RANGE_CLAIM_CAP,
    FUZZY_FACTOR_MAX,
    FUZZY_FACTOR_MIN,
    SEVERITY_SPEED_MAX,
    SEVERITY_SPEED_THRESHOLD,
    SEVERITY_TEMP_MAX,
    SEVERITY_TEMP_THRESHOLD,
    SEVERITY_W_ANFIS_MAX,
    SEVERITY_W_ANFIS_MIN,
)


def compute_uae_severity(
    temperature: float,
    ac_intensity: float,
    speed_kmh: float,
) -> float:
    """
    Return a UAE severity score in [0, 1].

    Three components, weighted to reflect UAE physics:
      0.45 × thermal load (dominant range killer in UAE)
      0.30 × AC draw
      0.25 × aerodynamic drag at speed

    High severity → ANFIS (data-driven) gets more weight.
    Low severity  → Mamdani (expert rules) gets more weight.
    """
    # Temperature component: ramp from 0 at 35°C to 1 at 52°C
    temp_s = max(0.0, min(1.0, (temperature - SEVERITY_TEMP_THRESHOLD) / (SEVERITY_TEMP_MAX - SEVERITY_TEMP_THRESHOLD)))

    # AC component: quadratic to emphasise max-AC demand
    ac_norm = max(0.0, min(1.0, ac_intensity / 10.0))
    ac_s = ac_norm ** 1.5

    # Speed component: ramp from 0 at 110 km/h to 1 at 160 km/h
    speed_s = max(0.0, min(1.0, (speed_kmh - SEVERITY_SPEED_THRESHOLD) / (SEVERITY_SPEED_MAX - SEVERITY_SPEED_THRESHOLD)))

    return round(0.45 * temp_s + 0.30 * ac_s + 0.25 * speed_s, 4)


def compute_hybrid_weights(severity: float) -> tuple[float, float]:
    """
    Map severity [0, 1] to (w_anfis, w_fuzzy) that sum to 1.

    At severity=0: w_anfis=SEVERITY_W_ANFIS_MIN (expert rules dominate)
    At severity=1: w_anfis=SEVERITY_W_ANFIS_MAX (data-driven dominates for extremes)
    """
    w_anfis = SEVERITY_W_ANFIS_MIN + severity * (SEVERITY_W_ANFIS_MAX - SEVERITY_W_ANFIS_MIN)
    w_fuzzy = 1.0 - w_anfis
    return round(w_anfis, 4), round(w_fuzzy, 4)


def _clip(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def compute_hybrid_factor(
    anfis_factor: float,
    fuzzy_factor: float,
    severity: float,
) -> float:
    """Return the weighted hybrid adjustment factor, clipped to valid range."""
    w_anfis, w_fuzzy = compute_hybrid_weights(severity)
    hybrid = w_anfis * anfis_factor + w_fuzzy * fuzzy_factor
    return round(_clip(hybrid, FUZZY_FACTOR_MIN, FUZZY_FACTOR_MAX), 4)


def predict_hybrid_range(
    *,
    shown_range_km: float,
    claimed_remaining_km: float,
    anfis_factor: float,
    fuzzy_factor: float,
    temperature: float,
    ac_intensity: float,
    speed_kmh: float,
) -> dict[str, float]:
    """
    Compute the hybrid range estimate and associated metadata.

    Returns a dict with keys ready to merge into the main payload:
      hybrid_factor, w_anfis, w_fuzzy, severity_score,
      hybrid_range_km, range_delta_hybrid_vs_fuzzy_km
    """
    severity = compute_uae_severity(temperature, ac_intensity, speed_kmh)
    w_anfis, w_fuzzy = compute_hybrid_weights(severity)
    hybrid_factor = _clip(
        w_anfis * anfis_factor + w_fuzzy * fuzzy_factor,
        FUZZY_FACTOR_MIN,
        FUZZY_FACTOR_MAX,
    )

    hybrid_range_km = shown_range_km * hybrid_factor
    hybrid_range_km = max(0.0, hybrid_range_km)
    if claimed_remaining_km > 0:
        hybrid_range_km = min(hybrid_range_km, claimed_remaining_km * FINAL_RANGE_CLAIM_CAP)

    fuzzy_range_km = shown_range_km * fuzzy_factor

    return {
        "hybrid_factor": round(hybrid_factor, 4),
        "w_anfis": round(w_anfis, 4),
        "w_fuzzy": round(w_fuzzy, 4),
        "severity_score": round(severity, 4),
        "anfis_factor": round(anfis_factor, 4),
        "hybrid_range_km": round(hybrid_range_km, 2),
        "range_delta_hybrid_vs_fuzzy_km": round(hybrid_range_km - fuzzy_range_km, 2),
    }
