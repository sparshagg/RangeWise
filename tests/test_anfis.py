"""Unit tests for the ANFIS model class — no dataset required."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from src.config import ANFIS_WEIGHTS_PATH, FUZZY_FACTOR_MAX, FUZZY_FACTOR_MIN
from src.neuro_fuzzy.anfis import ANFIS


def _random_input(n: int = 10) -> np.ndarray:
    """Return n samples of normalized inputs in [0, 1]."""
    rng = np.random.default_rng(0)
    return rng.random((n, 5))


# ---------------------------------------------------------------------------
# Structure and shape tests
# ---------------------------------------------------------------------------

def test_anfis_default_has_32_rules():
    anfis = ANFIS()
    assert anfis.n_rules == 32


def test_anfis_forward_shape():
    anfis = ANFIS()
    X = _random_input(20)
    out = anfis.forward(X)
    assert out.shape == (20,)


def test_anfis_forward_single_sample():
    anfis = ANFIS()
    X = _random_input(1)
    out = anfis.forward(X)
    assert out.shape == (1,)


def test_anfis_output_clipped_to_valid_range():
    """Untrained ANFIS (zero consequents) should still return clipped output."""
    anfis = ANFIS()
    X = _random_input(100)
    out = anfis.forward(X)
    assert np.all(out >= FUZZY_FACTOR_MIN - 1e-9)
    assert np.all(out <= FUZZY_FACTOR_MAX + 1e-9)


# ---------------------------------------------------------------------------
# MF parameter round-trip
# ---------------------------------------------------------------------------

def test_anfis_mf_params_roundtrip():
    anfis = ANFIS()
    original = anfis.get_mf_params().copy()
    anfis.set_mf_params(original)
    recovered = anfis.get_mf_params()
    np.testing.assert_allclose(recovered, original, rtol=1e-10)


def test_anfis_mf_params_length():
    anfis = ANFIS(n_inputs=5, n_mfs=2)
    params = anfis.get_mf_params()
    # centers (5*2) + sigmas (5*2) = 20
    assert len(params) == 20


def test_anfis_set_params_enforces_positive_sigma():
    anfis = ANFIS()
    params = anfis.get_mf_params()
    # Set sigmas to negative values
    params[10:] = -0.5
    anfis.set_mf_params(params)
    assert np.all(anfis.sigmas > 0)


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def test_anfis_save_load_roundtrip(tmp_path: Path):
    anfis = ANFIS()
    rng = np.random.default_rng(42)
    anfis.P = rng.standard_normal(anfis.P.shape)

    save_path = tmp_path / "test_weights.json"
    anfis.save(save_path)
    loaded = ANFIS.load(save_path)

    np.testing.assert_allclose(loaded.centers, anfis.centers, rtol=1e-10)
    np.testing.assert_allclose(loaded.sigmas, anfis.sigmas, rtol=1e-10)
    np.testing.assert_allclose(loaded.P, anfis.P, rtol=1e-10)
    assert loaded.n_rules == anfis.n_rules


def test_anfis_save_creates_parent_dirs(tmp_path: Path):
    anfis = ANFIS()
    deep_path = tmp_path / "nested" / "dir" / "weights.json"
    anfis.save(deep_path)
    assert deep_path.exists()


def test_anfis_forward_consistent_after_save_load(tmp_path: Path):
    anfis = ANFIS()
    X = _random_input(5)
    out_before = anfis.forward(X)

    save_path = tmp_path / "weights.json"
    anfis.save(save_path)
    loaded = ANFIS.load(save_path)
    out_after = loaded.forward(X)

    np.testing.assert_allclose(out_after, out_before, rtol=1e-8)


# ---------------------------------------------------------------------------
# Training-dependent test (skipped if weights not present)
# ---------------------------------------------------------------------------

def test_trained_severe_inputs_reduce_factor():
    """After training, extreme UAE inputs should yield a lower factor than mild inputs."""
    if not ANFIS_WEIGHTS_PATH.exists():
        pytest.skip("Trained weights not found — run scripts/train_anfis.py first")

    anfis = ANFIS.load(ANFIS_WEIGHTS_PATH)

    # Mild: pleasant temp, low AC, city speed, eco mode, no traffic
    # Normalized from: [22, 2.5, 60, 1.1, 1.1] using INPUT_BOUNDS
    from src.config import ANFIS_INPUT_BOUNDS
    mild_raw = np.array([[22.0, 2.5, 60.0, 1.1, 1.1]])
    severe_raw = np.array([[52.0, 9.0, 155.0, 2.9, 2.9]])

    def norm(x_raw):
        x_n = np.empty_like(x_raw, dtype=float)
        for i, (lo, hi) in enumerate(ANFIS_INPUT_BOUNDS):
            x_n[0, i] = (x_raw[0, i] - lo) / (hi - lo + 1e-12)
        return np.clip(x_n, 0.0, 1.0)

    mild_factor = anfis.forward(norm(mild_raw))[0]
    severe_factor = anfis.forward(norm(severe_raw))[0]

    assert severe_factor < mild_factor, (
        f"Expected severe ({severe_factor:.4f}) < mild ({mild_factor:.4f})"
    )
