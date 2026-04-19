"""Tests for UAE severity score and hybrid combiner."""

from __future__ import annotations

import pytest

from src.config import FUZZY_FACTOR_MAX, FUZZY_FACTOR_MIN, SEVERITY_W_ANFIS_MAX, SEVERITY_W_ANFIS_MIN
from src.neuro_fuzzy.hybrid import (
    compute_hybrid_factor,
    compute_hybrid_weights,
    compute_uae_severity,
    predict_hybrid_range,
)


# ---------------------------------------------------------------------------
# Severity score
# ---------------------------------------------------------------------------

def test_severity_mild_conditions_is_zero():
    """Pleasant temp, low AC, city speed → no severity contribution."""
    s = compute_uae_severity(temperature=20.0, ac_intensity=2.0, speed_kmh=80.0)
    assert s == 0.0


def test_severity_extreme_conditions_near_one():
    s = compute_uae_severity(temperature=52.0, ac_intensity=10.0, speed_kmh=160.0)
    assert s > 0.9


def test_severity_monotone_in_temperature():
    s_low = compute_uae_severity(30.0, 5.0, 100.0)
    s_high = compute_uae_severity(50.0, 5.0, 100.0)
    assert s_high > s_low


def test_severity_monotone_in_ac():
    s_low = compute_uae_severity(40.0, 2.0, 100.0)
    s_high = compute_uae_severity(40.0, 9.0, 100.0)
    assert s_high > s_low


def test_severity_monotone_in_speed():
    s_slow = compute_uae_severity(40.0, 5.0, 80.0)
    s_fast = compute_uae_severity(40.0, 5.0, 155.0)
    assert s_fast > s_slow


def test_severity_clipped_to_unit_interval():
    s = compute_uae_severity(100.0, 100.0, 500.0)  # way out of range
    assert 0.0 <= s <= 1.0


# ---------------------------------------------------------------------------
# Hybrid weights
# ---------------------------------------------------------------------------

def test_hybrid_weights_sum_to_one():
    for sev in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
        wa, wf = compute_hybrid_weights(sev)
        assert abs(wa + wf - 1.0) < 1e-9, f"Weights don't sum to 1 at severity={sev}"


def test_hybrid_weights_mild_favours_fuzzy():
    wa, wf = compute_hybrid_weights(0.0)
    assert wf > wa, "Mild conditions should give more weight to fuzzy (expert rules)"


def test_hybrid_weights_severe_favours_anfis():
    wa, wf = compute_hybrid_weights(1.0)
    assert wa > wf, "Extreme UAE should give more weight to ANFIS (data-driven)"


def test_hybrid_weights_at_zero_match_config():
    wa, _ = compute_hybrid_weights(0.0)
    assert abs(wa - SEVERITY_W_ANFIS_MIN) < 1e-6


def test_hybrid_weights_at_one_match_config():
    wa, _ = compute_hybrid_weights(1.0)
    assert abs(wa - SEVERITY_W_ANFIS_MAX) < 1e-6


def test_hybrid_weights_monotone_in_severity():
    wa_low, _ = compute_hybrid_weights(0.2)
    wa_high, _ = compute_hybrid_weights(0.8)
    assert wa_high > wa_low


# ---------------------------------------------------------------------------
# Hybrid factor
# ---------------------------------------------------------------------------

def test_hybrid_factor_clips_to_valid_range():
    # Use factors at the boundary
    hf = compute_hybrid_factor(FUZZY_FACTOR_MIN, FUZZY_FACTOR_MIN, 1.0)
    assert hf >= FUZZY_FACTOR_MIN

    hf = compute_hybrid_factor(FUZZY_FACTOR_MAX, FUZZY_FACTOR_MAX, 0.0)
    assert hf <= FUZZY_FACTOR_MAX


def test_hybrid_factor_between_inputs():
    """Hybrid factor should be a convex combination (between the two inputs)."""
    anfis_f, fuzzy_f, sev = 0.85, 1.05, 0.5
    hf = compute_hybrid_factor(anfis_f, fuzzy_f, sev)
    assert min(anfis_f, fuzzy_f) <= hf <= max(anfis_f, fuzzy_f)


# ---------------------------------------------------------------------------
# predict_hybrid_range
# ---------------------------------------------------------------------------

def test_predict_hybrid_range_returns_required_keys():
    result = predict_hybrid_range(
        shown_range_km=300.0,
        claimed_remaining_km=360.0,
        anfis_factor=0.90,
        fuzzy_factor=0.95,
        temperature=45.0,
        ac_intensity=8.0,
        speed_kmh=120.0,
    )
    required_keys = {
        "hybrid_factor", "w_anfis", "w_fuzzy", "severity_score",
        "anfis_factor", "hybrid_range_km", "range_delta_hybrid_vs_fuzzy_km",
    }
    assert required_keys.issubset(result.keys())


def test_predict_hybrid_range_never_negative():
    result = predict_hybrid_range(
        shown_range_km=0.0,
        claimed_remaining_km=0.0,
        anfis_factor=0.90,
        fuzzy_factor=0.95,
        temperature=30.0,
        ac_intensity=5.0,
        speed_kmh=80.0,
    )
    assert result["hybrid_range_km"] == 0.0


def test_predict_hybrid_range_respects_cap():
    """hybrid_range_km must not exceed claimed_remaining_km × 1.15."""
    from src.config import FINAL_RANGE_CLAIM_CAP
    claimed = 360.0
    result = predict_hybrid_range(
        shown_range_km=500.0,
        claimed_remaining_km=claimed,
        anfis_factor=1.08,
        fuzzy_factor=1.08,
        temperature=20.0,
        ac_intensity=2.0,
        speed_kmh=60.0,
    )
    assert result["hybrid_range_km"] <= claimed * FINAL_RANGE_CLAIM_CAP + 1e-6


def test_predict_hybrid_range_severe_lower_than_mild():
    """Severe UAE conditions should produce a lower hybrid range than mild ones."""
    common = dict(
        shown_range_km=300.0,
        claimed_remaining_km=360.0,
        anfis_factor=0.85,
        fuzzy_factor=0.92,
    )
    mild = predict_hybrid_range(**common, temperature=20.0, ac_intensity=2.0, speed_kmh=60.0)
    severe = predict_hybrid_range(**common, temperature=52.0, ac_intensity=10.0, speed_kmh=155.0)

    # When ANFIS factor < fuzzy factor, higher ANFIS weight → lower hybrid range
    assert severe["hybrid_range_km"] <= mild["hybrid_range_km"]


def test_predict_hybrid_range_w_anfis_plus_w_fuzzy_equals_one():
    result = predict_hybrid_range(
        shown_range_km=300.0,
        claimed_remaining_km=360.0,
        anfis_factor=0.90,
        fuzzy_factor=0.95,
        temperature=40.0,
        ac_intensity=7.0,
        speed_kmh=130.0,
    )
    assert abs(result["w_anfis"] + result["w_fuzzy"] - 1.0) < 1e-6
