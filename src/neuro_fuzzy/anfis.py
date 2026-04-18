"""
Sugeno first-order ANFIS (Jang 1993) implemented in numpy.

Architecture for n_inputs=5, n_mfs=2:
  Layer 1  Fuzzification     Gaussian MFs, shape (n_samples, n_inputs, n_mfs)
  Layer 2  Rule strengths    product T-norm,  shape (n_samples, n_rules)   n_rules = n_mfs^n_inputs
  Layer 3  Normalization     sum-normalize,   shape (n_samples, n_rules)
  Layer 4  Consequents       linear Sugeno,   shape (n_samples, n_rules)
  Layer 5  Defuzzification   weighted sum,    shape (n_samples,)
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

from src.config import ANFIS_INPUT_BOUNDS, ANFIS_INIT_CENTERS, ANFIS_N_MFS, FUZZY_FACTOR_MAX, FUZZY_FACTOR_MIN


class ANFIS:
    def __init__(self, n_inputs: int = 5, n_mfs: int = ANFIS_N_MFS) -> None:
        self.n_inputs = n_inputs
        self.n_mfs = n_mfs
        self.n_rules = n_mfs ** n_inputs

        # Gaussian MF parameters: centers and sigmas, shape (n_inputs, n_mfs)
        bounds = ANFIS_INPUT_BOUNDS[:n_inputs]
        init_c = ANFIS_INIT_CENTERS[:n_inputs]

        self.centers = np.array(init_c, dtype=float)  # (n_inputs, n_mfs)

        # Initial sigma = universe_range / (2 * n_mfs) — ensures MFs overlap well
        self.sigmas = np.array(
            [[(hi - lo) / (2.0 * n_mfs) for _ in range(n_mfs)] for lo, hi in bounds],
            dtype=float,
        )  # (n_inputs, n_mfs)

        # Sugeno consequent matrix: (n_rules, n_inputs + 1) — bias + linear coefficients
        self.P = np.zeros((self.n_rules, n_inputs + 1), dtype=float)

        # Pre-compute rule index → MF assignment for each input
        # rule_map[k] = (mf_i0, mf_i1, ..., mf_i{n_inputs-1})
        self._rule_map: list[tuple[int, ...]] = list(
            itertools.product(range(n_mfs), repeat=n_inputs)
        )

    # ------------------------------------------------------------------
    # Forward pass
    # ------------------------------------------------------------------

    def _gaussian_mf(self, X: np.ndarray) -> np.ndarray:
        """
        Compute Gaussian membership values.

        X: (n_samples, n_inputs)
        Returns: (n_samples, n_inputs, n_mfs)
        """
        # X[:, :, None] broadcasts to (n_samples, n_inputs, 1)
        diff = X[:, :, None] - self.centers[None, :, :]          # (n, n_inputs, n_mfs)
        return np.exp(-0.5 * (diff / (self.sigmas[None, :, :] + 1e-12)) ** 2)

    def _rule_strengths(self, mu: np.ndarray) -> np.ndarray:
        """
        Compute firing strength for each rule via product T-norm.

        mu: (n_samples, n_inputs, n_mfs)
        Returns: (n_samples, n_rules)
        """
        n_samples = mu.shape[0]
        W = np.ones((n_samples, self.n_rules), dtype=float)
        for k, mf_idx in enumerate(self._rule_map):
            for i, j in enumerate(mf_idx):
                W[:, k] *= mu[:, i, j]
        return W

    def _normalize(self, W: np.ndarray) -> np.ndarray:
        """Sum-normalize rule strengths. (n_samples, n_rules) → (n_samples, n_rules)"""
        total = W.sum(axis=1, keepdims=True) + 1e-12
        return W / total

    def _consequents(self, X: np.ndarray, W_bar: np.ndarray) -> np.ndarray:
        """
        Compute weighted rule outputs (Sugeno first-order).

        X:     (n_samples, n_inputs)
        W_bar: (n_samples, n_rules)
        Returns: (n_samples,)
        """
        # Augment X with bias column → (n_samples, n_inputs+1)
        X_aug = np.hstack([np.ones((X.shape[0], 1)), X])  # (n, n_inputs+1)
        # F[s, k] = P[k] · X_aug[s]
        F = X_aug @ self.P.T  # (n_samples, n_rules)
        return (W_bar * F).sum(axis=1)  # (n_samples,)

    def forward(self, X: np.ndarray) -> np.ndarray:
        """
        Full forward pass.

        X: (n_samples, n_inputs) — normalized to [0,1]
        Returns: (n_samples,) clipped to [FUZZY_FACTOR_MIN, FUZZY_FACTOR_MAX]
        """
        mu = self._gaussian_mf(X)
        W = self._rule_strengths(mu)
        W_bar = self._normalize(W)
        out = self._consequents(X, W_bar)
        return np.clip(out, FUZZY_FACTOR_MIN, FUZZY_FACTOR_MAX)

    # ------------------------------------------------------------------
    # MF parameter accessors (used by scipy optimizer)
    # ------------------------------------------------------------------

    def get_mf_params(self) -> np.ndarray:
        """Return flat vector [centers..., sigmas...] shape (2 * n_inputs * n_mfs,)."""
        return np.concatenate([self.centers.ravel(), self.sigmas.ravel()])

    def set_mf_params(self, params: np.ndarray) -> None:
        """Restore centers and sigmas from flat vector."""
        split = self.n_inputs * self.n_mfs
        self.centers = params[:split].reshape(self.n_inputs, self.n_mfs)
        # Enforce σ > 0 via abs to avoid divide-by-zero
        self.sigmas = np.abs(params[split:]).reshape(self.n_inputs, self.n_mfs) + 1e-6

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": 1,
            "n_inputs": self.n_inputs,
            "n_mfs": self.n_mfs,
            "n_rules": self.n_rules,
            "input_names": ["temperature_c", "ac_intensity", "speed_kmh", "driving_mode", "traffic_level"],
            "centers": self.centers.tolist(),
            "sigmas": self.sigmas.tolist(),
            "consequents": self.P.tolist(),
        }
        path.write_text(json.dumps(payload, indent=2))

    @classmethod
    def load(cls, path: Path) -> "ANFIS":
        path = Path(path)
        data = json.loads(path.read_text())
        model = cls(n_inputs=data["n_inputs"], n_mfs=data["n_mfs"])
        model.centers = np.array(data["centers"], dtype=float)
        model.sigmas = np.array(data["sigmas"], dtype=float)
        model.P = np.array(data["consequents"], dtype=float)
        return model
