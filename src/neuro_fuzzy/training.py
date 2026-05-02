"""
ANFIS training pipeline.

Hybrid learning algorithm (Jang 1993):
  - Least squares  → optimise Sugeno consequent parameters P
  - L-BFGS-B       → optimise Gaussian MF parameters (centers, sigmas)
  Alternated for ANFIS_N_EPOCHS epochs.

AC intensity is not directly measured in the dataset.
It is derived from temperature_c using the same piecewise thresholds as config.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from src.config import (
    ANFIS_INPUT_BOUNDS,
    ANFIS_N_EPOCHS,
    ANFIS_RANDOM_SEED,
    ANFIS_TRAIN_SPLIT,
    ANFIS_WEIGHTS_PATH,
    FUZZY_FACTOR_MAX,
    FUZZY_FACTOR_MIN,
)
from src.neuro_fuzzy.anfis import ANFIS


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------

def _derive_ac_proxy(temp_c: np.ndarray) -> np.ndarray:
    """
    Estimate AC intensity (0–10 scale) from ambient temperature.

    Mirrors the three-level config mapping:
      temp < 28°C  → AC ≈ 2.0  (Low)
      28–40°C      → AC ≈ 5.0  (Medium), linear interpolation
      > 40°C       → AC ≈ 8.0  (High), linear interpolation up to 52°C
    """
    ac = np.where(
        temp_c < 28.0,
        2.0,
        np.where(
            temp_c <= 40.0,
            2.0 + (temp_c - 28.0) / 12.0 * 3.0,          # 2.0 → 5.0
            np.minimum(5.0 + (temp_c - 40.0) / 12.0 * 3.0, 10.0),  # 5.0 → 8.0+
        ),
    )
    return ac.astype(float)


def extract_features(df: pd.DataFrame) -> np.ndarray:
    """
    Extract the 5 ANFIS input features from a processed DataFrame.

    Column order: [temperature_c, ac_intensity, speed_kmh, driving_mode, traffic_level]

    Expects canonical column names (as produced by loader.normalize_columns).
    """
    temp = df["temperature_c"].to_numpy(dtype=float)
    speed = df["speed"].to_numpy(dtype=float)
    driving_mode = df["driving_mode"].to_numpy(dtype=float)
    traffic = df["traffic_level"].to_numpy(dtype=float)
    ac_proxy = _derive_ac_proxy(temp)

    return np.column_stack([temp, ac_proxy, speed, driving_mode, traffic])


def compute_training_target(df: pd.DataFrame) -> np.ndarray:
    """
    Compute per-row adjustment factors relative to the reference bucket.

    Reference bucket = City / Comfort (mode=2) / Moderate (traffic=2).
    Target = efficiency factor x UAE thermal penalty, clipped to
    [FUZZY_FACTOR_MIN, FUZZY_FACTOR_MAX].
    """
    dist = df["distance_travelled_km"].to_numpy(dtype=float)
    energy = df["energy_consumption_kwh"].to_numpy(dtype=float)
    temp = df["temperature_c"].to_numpy(dtype=float)
    ac_proxy = _derive_ac_proxy(temp)

    # Filter valid rows inline
    valid = (energy > 0) & (dist > 0)
    km_per_kwh = np.where(valid, dist / energy, np.nan)

    # Reference efficiency: median of City/Comfort/Moderate rows
    speed_bins = [0, 50, 80, 120, 140, float("inf")]
    speed_labels_num = [0, 1, 2, 3, 4]  # Local=0, City=1, Highway=2, ...
    speed_level_num = pd.cut(
        df["speed"], bins=speed_bins, labels=speed_labels_num, right=True
    ).astype(float)

    ref_mask = (
        (speed_level_num == 1) &   # City
        (df["driving_mode"] == 2) &  # Comfort
        (df["traffic_level"] == 2) &  # Moderate
        valid
    )
    ref_vals = km_per_kwh[ref_mask.to_numpy()]
    if len(ref_vals) == 0 or np.nanmedian(ref_vals) == 0:
        ref_efficiency = float(np.nanmedian(km_per_kwh[~np.isnan(km_per_kwh)]))
    else:
        ref_efficiency = float(np.nanmedian(ref_vals))

    target = km_per_kwh / ref_efficiency

    # Add a bounded UAE thermal penalty so extreme heat and heavy cooling learn
    # lower factors even though the dataset is not UAE-native and has no direct
    # AC telemetry column.
    temp_s = np.clip((temp - 35.0) / (52.0 - 35.0 + 1e-12), 0.0, 1.0)
    ac_s = np.clip((ac_proxy - 3.0) / 7.0, 0.0, 1.0) ** 1.5
    thermal_penalty = 1.0 - 0.25 * (0.7 * temp_s + 0.3 * ac_s)

    target = target * thermal_penalty
    target = np.clip(target, FUZZY_FACTOR_MIN, FUZZY_FACTOR_MAX)
    return target.astype(float)


def normalize_inputs(X: np.ndarray) -> np.ndarray:
    """
    Min-max normalize each input column using fixed universe bounds from config.
    Does NOT use dataset statistics — ensures inference normalization matches training.
    """
    X_norm = np.empty_like(X, dtype=float)
    for i, (lo, hi) in enumerate(ANFIS_INPUT_BOUNDS):
        X_norm[:, i] = (X[:, i] - lo) / (hi - lo + 1e-12)
    return np.clip(X_norm, 0.0, 1.0)


def prepare_training_data(
    df: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Extract, normalize, and split data into train/test sets.

    Returns: X_train, X_test, y_train, y_test
    """
    X_raw = extract_features(df)
    y = compute_training_target(df)

    # Drop rows with NaN in features or target
    valid = ~(np.isnan(X_raw).any(axis=1) | np.isnan(y))
    X_raw, y = X_raw[valid], y[valid]

    X_norm = normalize_inputs(X_raw)

    rng = np.random.default_rng(ANFIS_RANDOM_SEED)
    n = len(y)
    idx = rng.permutation(n)
    split = int(n * ANFIS_TRAIN_SPLIT)
    train_idx, test_idx = idx[:split], idx[split:]

    return X_norm[train_idx], X_norm[test_idx], y[train_idx], y[test_idx]


# ---------------------------------------------------------------------------
# Hybrid learning steps
# ---------------------------------------------------------------------------

def lstsq_consequents(anfis: ANFIS, X_norm: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Compute optimal Sugeno consequent matrix P via least squares.

    With MF parameters fixed, the output is linear in P:
      Phi[s, k*(n+1) + j] = W_bar[s,k] * X_aug[s,j]
    Solve Phi @ p_flat = y via numpy lstsq.

    Returns P of shape (n_rules, n_inputs+1).
    """
    mu = anfis._gaussian_mf(X_norm)
    W = anfis._rule_strengths(mu)
    W_bar = anfis._normalize(W)                       # (n_samples, n_rules)

    n_samples = X_norm.shape[0]
    n_cols = anfis.n_inputs + 1
    X_aug = np.hstack([np.ones((n_samples, 1)), X_norm])  # (n, n_inputs+1)

    # Build expanded regressor matrix Phi: (n_samples, n_rules * n_cols)
    Phi = (W_bar[:, :, None] * X_aug[:, None, :]).reshape(n_samples, anfis.n_rules * n_cols)

    # Mild ridge regularization keeps the consequent weights from exploding and
    # saturating the clipped ANFIS output.
    ridge_lambda = 1e-2
    gram = Phi.T @ Phi
    regularized = gram + ridge_lambda * np.eye(gram.shape[0])
    rhs = Phi.T @ y
    p_flat = np.linalg.solve(regularized, rhs)
    return p_flat.reshape(anfis.n_rules, n_cols)


def _mse_loss(params: np.ndarray, anfis: ANFIS, X_norm: np.ndarray, y: np.ndarray) -> float:
    """MSE loss as a function of flat MF params, for scipy.optimize.minimize."""
    anfis.set_mf_params(params)
    pred = anfis.forward(X_norm)
    return float(np.mean((pred - y) ** 2))


def gradient_step_mf_params(
    anfis: ANFIS,
    X_norm: np.ndarray,
    y: np.ndarray,
) -> None:
    """
    One L-BFGS-B step optimising MF parameters (centers, sigmas) with P fixed.
    Sigma values are kept > 0 via bounds.
    """
    n_mf_params = anfis.n_inputs * anfis.n_mfs
    x0 = anfis.get_mf_params()

    # Bounds: centers unconstrained, sigmas > 1e-3
    bounds = [(None, None)] * n_mf_params + [(1e-3, None)] * n_mf_params

    result = minimize(
        _mse_loss,
        x0,
        args=(anfis, X_norm, y),
        method="L-BFGS-B",
        bounds=bounds,
        options={"maxiter": 50, "ftol": 1e-9},
    )
    anfis.set_mf_params(result.x)


# ---------------------------------------------------------------------------
# Full training loop
# ---------------------------------------------------------------------------

def train_anfis(
    df: pd.DataFrame,
    n_epochs: int = ANFIS_N_EPOCHS,
) -> tuple[ANFIS, dict[str, list[float]]]:
    """
    Train an ANFIS model on the EV dataset using hybrid learning.

    Returns:
      anfis    — trained ANFIS instance
      metrics  — dict with "train_mse" and "test_mse" lists (one entry per epoch)
    """
    X_train, X_test, y_train, y_test = prepare_training_data(df)

    anfis = ANFIS()
    metrics: dict[str, list[float]] = {"train_mse": [], "test_mse": []}

    for epoch in range(1, n_epochs + 1):
        # Step A: least-squares consequents
        anfis.P = lstsq_consequents(anfis, X_train, y_train)

        # Step B: L-BFGS-B on MF parameters
        gradient_step_mf_params(anfis, X_train, y_train)

        train_mse = float(np.mean((anfis.forward(X_train) - y_train) ** 2))
        test_mse = float(np.mean((anfis.forward(X_test) - y_test) ** 2))
        metrics["train_mse"].append(round(train_mse, 6))
        metrics["test_mse"].append(round(test_mse, 6))

        print(f"  Epoch {epoch:>3}/{n_epochs}  train_MSE={train_mse:.6f}  test_MSE={test_mse:.6f}")

    return anfis, metrics


def save_weights(anfis: ANFIS, metrics: dict, path: Path = ANFIS_WEIGHTS_PATH) -> None:
    """Save trained weights plus training metadata to JSON."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing JSON to preserve any extra fields, or start fresh
    try:
        existing = json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        existing = {}

    from datetime import date
    payload = {
        "version": 1,
        "n_inputs": anfis.n_inputs,
        "n_mfs": anfis.n_mfs,
        "n_rules": anfis.n_rules,
        "input_names": ["temperature_c", "ac_intensity", "speed_kmh", "driving_mode", "traffic_level"],
        "centers": anfis.centers.tolist(),
        "sigmas": anfis.sigmas.tolist(),
        "consequents": anfis.P.tolist(),
        "training_mse_train": metrics["train_mse"][-1] if metrics["train_mse"] else None,
        "training_mse_test": metrics["test_mse"][-1] if metrics["test_mse"] else None,
        "training_epochs": len(metrics["train_mse"]),
        "training_date": str(date.today()),
        "epoch_history": metrics,
    }
    path.write_text(json.dumps(payload, indent=2))
    print(f"\nWeights saved → {path}")
