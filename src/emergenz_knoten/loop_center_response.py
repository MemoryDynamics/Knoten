"""Local Loop--Center response utilities for prepared rotating waves."""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from .rotating_wave_stability import (
    co_rotating_fifo_step,
    finite_memory_weights,
    native_fifo_step,
    rotation_matrix,
)


def normalized_memory_weights(
    *, alpha: float, horizon: int, memory_mass: float = 1.0
) -> np.ndarray:
    """Return normalized finite-memory weights for the exact center readout."""

    weights = finite_memory_weights(
        alpha=alpha,
        horizon=horizon,
        memory_mass=memory_mass,
    )
    return weights / np.sum(weights)


def memory_center(
    history: np.ndarray,
    *,
    alpha: float,
    memory_mass: float = 1.0,
) -> np.ndarray:
    """Return the exact normalized finite-history center."""

    state = np.asarray(history, dtype=float)
    if (
        state.ndim != 2
        or state.shape[0] < 1
        or state.shape[1] != 2
        or not np.isfinite(state).all()
    ):
        raise ValueError("history must be a finite array with shape (H,2)")
    weights = normalized_memory_weights(
        alpha=alpha,
        horizon=state.shape[0],
        memory_mass=memory_mass,
    )
    return np.sum(weights[:, None] * state, axis=0)


def finite_h_center_recurrence(
    center: np.ndarray,
    *,
    new_visible: np.ndarray,
    retiring_visible: np.ndarray,
    alpha: float,
    horizon: int,
) -> np.ndarray:
    """Advance the normalized center with the exact retiring-sample term."""

    forgetting = float(alpha)
    if not math.isfinite(forgetting) or not 0.0 < forgetting < 1.0:
        raise ValueError("alpha must lie strictly between zero and one")
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    current = np.asarray(center, dtype=float)
    incoming = np.asarray(new_visible, dtype=float)
    retiring = np.asarray(retiring_visible, dtype=float)
    if current.shape != (2,) or incoming.shape != (2,) or retiring.shape != (2,):
        raise ValueError("center and visible samples must have shape (2,)")
    if not all(np.isfinite(value).all() for value in (current, incoming, retiring)):
        raise ValueError("center and visible samples must be finite")
    q = 1.0 - forgetting
    normalization = forgetting / (1.0 - q**horizon)
    return (
        q * current
        + normalization * incoming
        - normalization * q**horizon * retiring
    )


def native_fifo_forced_step(
    history: np.ndarray,
    *,
    force: np.ndarray,
    alpha: float,
    **parameters: float,
) -> np.ndarray:
    """Advance the native FIFO map with the declared additive visible input."""

    forcing = np.asarray(force, dtype=float)
    if forcing.shape != (2,) or not np.isfinite(forcing).all():
        raise ValueError("force must be a finite vector with shape (2,)")
    advanced = native_fifo_step(history, alpha=alpha, **parameters)
    advanced[0] += float(alpha) * forcing
    return advanced


def laboratory_force_in_next_corotating_frame(
    force: np.ndarray,
    *,
    theta: float,
    step_index: int,
) -> np.ndarray:
    """Express a laboratory force in the next co-rotating frame."""

    forcing = np.asarray(force, dtype=float)
    if forcing.shape != (2,) or not np.isfinite(forcing).all():
        raise ValueError("force must be a finite vector with shape (2,)")
    if isinstance(step_index, bool) or not isinstance(step_index, int) or step_index < 0:
        raise ValueError("step_index must be a non-negative integer")
    return rotation_matrix(-(step_index + 1) * float(theta)) @ forcing


def co_rotating_fifo_forced_step(
    history: np.ndarray,
    *,
    force_lab: np.ndarray,
    step_index: int,
    theta: float,
    alpha: float,
    **parameters: float,
) -> np.ndarray:
    """Advance the co-rotating FIFO map under a laboratory-frame force."""

    advanced = co_rotating_fifo_step(
        history,
        theta=theta,
        alpha=alpha,
        **parameters,
    )
    advanced[0] += float(alpha) * laboratory_force_in_next_corotating_frame(
        force_lab,
        theta=theta,
        step_index=step_index,
    )
    return advanced


def tangent_fifo_forced_step(
    perturbation: np.ndarray,
    *,
    jacobian: Any,
    force_lab: np.ndarray,
    step_index: int,
    theta: float,
    alpha: float,
) -> np.ndarray:
    """Advance the frozen full-FIFO tangent recurrence with the same input."""

    delta = np.asarray(perturbation, dtype=float)
    if (
        delta.ndim != 2
        or delta.shape[0] < 1
        or delta.shape[1] != 2
        or not np.isfinite(delta).all()
    ):
        raise ValueError("perturbation must be a finite array with shape (H,2)")
    advanced = np.asarray(jacobian @ delta.ravel(), dtype=float).reshape(delta.shape)
    advanced[0] += float(alpha) * laboratory_force_in_next_corotating_frame(
        force_lab,
        theta=theta,
        step_index=step_index,
    )
    return advanced


def laboratory_center_displacement(
    perturbation: np.ndarray,
    *,
    alpha: float,
    memory_mass: float,
    theta: float,
    step: int,
    initial_phase: float = 0.0,
) -> np.ndarray:
    """Return a co-rotating center perturbation in laboratory coordinates."""

    if isinstance(step, bool) or not isinstance(step, int) or step < 0:
        raise ValueError("step must be a non-negative integer")
    center = memory_center(
        perturbation,
        alpha=alpha,
        memory_mass=memory_mass,
    )
    return rotation_matrix(float(initial_phase) + step * float(theta)) @ center


def weighted_state_norm(
    perturbation: np.ndarray,
    *,
    weights: np.ndarray,
) -> float:
    """Return the RMS norm induced by normalized finite-memory weights."""

    delta = np.asarray(perturbation, dtype=float)
    metric = np.asarray(weights, dtype=float)
    if delta.ndim != 2 or delta.shape[1] != 2:
        raise ValueError("perturbation must have shape (H,2)")
    if metric.shape != (delta.shape[0],):
        raise ValueError("weights must have shape (H,)")
    if not np.isfinite(delta).all() or not np.isfinite(metric).all():
        raise ValueError("perturbation and weights must be finite")
    if np.any(metric < 0.0) or not math.isclose(
        float(np.sum(metric)), 1.0, rel_tol=0.0, abs_tol=5.0e-14
    ):
        raise ValueError("weights must be non-negative and normalized")
    return float(math.sqrt(np.sum(metric[:, None] * delta * delta)))


def registered_zero_sum_waveforms(length: int = 400) -> dict[str, np.ndarray]:
    """Return the frozen primary and holdout zero-sum probe profiles."""

    if length != 400:
        raise ValueError("the frozen P2 waveform length is 400")
    indices = np.arange(length, dtype=float)
    primary = np.sin(2.0 * math.pi * (indices + 0.5) / length)
    half_indices = np.arange(length // 2, dtype=float)
    lobe = np.sin(math.pi * (half_indices + 0.5) / (length // 2)) ** 2
    holdout = np.concatenate((lobe, -lobe))
    return {
        "sine_cycle": primary,
        "hann_doublet": holdout,
    }
