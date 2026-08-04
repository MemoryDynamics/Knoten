"""Reduced-mode diagnostics for paired reciprocal knot continuations."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


@dataclass(frozen=True)
class IsotropicRelativeModeFit:
    """Affine two-state fit shared across all ambient coordinates."""

    transition: np.ndarray
    intercept: np.ndarray
    eigenvalues: np.ndarray
    design_condition: float
    residual_ratio: float

    @property
    def is_complex(self) -> bool:
        return bool(np.max(np.abs(self.eigenvalues.imag)) > 1e-8)

    @property
    def is_stable(self) -> bool:
        return bool(np.max(np.abs(self.eigenvalues)) < 1.0)

    @property
    def angular_frequency(self) -> float:
        """Positive phase advance per sampled update, or zero for real modes."""

        if not self.is_complex:
            return 0.0
        return float(np.max(np.abs(np.angle(self.eigenvalues))))

    @property
    def damping_rate(self) -> float:
        """Return ``-log(max |mu|)``; negative values denote growth."""

        radius = float(np.max(np.abs(self.eigenvalues)))
        if radius == 0.0:
            return math.inf
        return float(-math.log(radius))


def fit_isotropic_relative_mode(
    relative_positions: np.ndarray,
    relative_memory_centers: np.ndarray,
    *,
    lag: int = 1,
) -> IsotropicRelativeModeFit:
    r"""Fit one real 2x2 map to the relative visible/memory coordinates.

    Each ambient coordinate supplies another realization of
    ``(x_-, m_-)``. The fit includes an affine intercept but constrains the
    same transition matrix across coordinates, as required by an isotropic
    local reduction.
    """

    positions = np.asarray(relative_positions, dtype=float)
    centers = np.asarray(relative_memory_centers, dtype=float)
    if (
        positions.ndim != 2
        or positions.shape != centers.shape
        or positions.shape[0] < 4
        or positions.shape[1] < 1
        or not np.isfinite(positions).all()
        or not np.isfinite(centers).all()
    ):
        raise ValueError("relative traces must be finite arrays of shape (time, dim)")
    if isinstance(lag, bool) or not isinstance(lag, (int, np.integer)) or lag < 1:
        raise ValueError("lag must be a positive integer")
    if positions.shape[0] <= lag + 2:
        raise ValueError("relative traces are too short for the requested lag")

    state = np.stack((positions, centers), axis=-1)
    predictors = state[:-lag].reshape(-1, 2)
    responses = state[lag:].reshape(-1, 2)
    predictor_mean = np.mean(predictors, axis=0)
    response_mean = np.mean(responses, axis=0)
    centered_predictors = predictors - predictor_mean
    centered_responses = responses - response_mean
    coefficients, _, _, _ = np.linalg.lstsq(
        centered_predictors,
        centered_responses,
        rcond=None,
    )
    transition = coefficients.T
    intercept = response_mean - transition @ predictor_mean
    residual = responses - (predictors @ transition.T + intercept)
    response_scale = float(np.sqrt(np.mean(centered_responses * centered_responses)))
    residual_scale = float(np.sqrt(np.mean(residual * residual)))
    residual_ratio = residual_scale / max(response_scale, np.finfo(float).tiny)
    design_condition = float(np.linalg.cond(centered_predictors))
    eigenvalues = np.linalg.eigvals(transition)
    return IsotropicRelativeModeFit(
        transition=np.asarray(transition, dtype=float),
        intercept=np.asarray(intercept, dtype=float),
        eigenvalues=np.asarray(eigenvalues, dtype=np.complex128),
        design_condition=design_condition,
        residual_ratio=float(residual_ratio),
    )


def relative_mode_phase_coherence(
    relative_positions: np.ndarray,
    relative_memory_centers: np.ndarray,
    fit: IsotropicRelativeModeFit,
    *,
    lag: int = 1,
) -> float:
    """Return phase-increment coherence of a fitted complex relative mode.

    A left eigenvector turns each ambient-coordinate trace into one complex
    modal coordinate. The circular resultant compares observed phase
    increments with the fitted eigenvalue phase and lies in ``[0, 1]``.
    """

    if not fit.is_complex:
        return 0.0
    positions = np.asarray(relative_positions, dtype=float)
    centers = np.asarray(relative_memory_centers, dtype=float)
    if positions.ndim != 2 or positions.shape != centers.shape:
        raise ValueError("relative traces must share shape (time, dim)")
    if isinstance(lag, bool) or not isinstance(lag, (int, np.integer)) or lag < 1:
        raise ValueError("lag must be a positive integer")
    if positions.shape[0] <= lag:
        raise ValueError("relative traces are too short for the requested lag")

    eigenvalues, left_vectors = np.linalg.eig(fit.transition.T)
    candidates = np.flatnonzero(eigenvalues.imag > 1e-8)
    if candidates.size != 1:
        return 0.0
    index = int(candidates[0])
    state = np.stack((positions, centers), axis=-1)
    equilibrium, _, _, _ = np.linalg.lstsq(
        np.eye(2) - fit.transition, fit.intercept, rcond=None
    )
    state = state - equilibrium[None, None, :]
    modal = np.einsum("tds,s->td", state, left_vectors[:, index])
    earlier = modal[:-lag]
    later = modal[lag:]
    amplitude = np.abs(earlier) * np.abs(later)
    positive = amplitude > 0.0
    if not np.any(positive):
        return 0.0
    threshold = float(np.quantile(amplitude[positive], 0.25))
    selected = positive & (amplitude >= threshold)
    increments = np.angle(later[selected] * np.conjugate(earlier[selected]))
    expected = float(np.angle(eigenvalues[index]))
    return float(abs(np.mean(np.exp(1j * (increments - expected)))))
