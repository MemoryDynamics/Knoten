"""Anchor-paper utilities for augmented-state metastability analysis.

The functions in this module are intentionally small, explicit, and
dependency-light. They provide a reproducible bridge from finite-memory
simulations to reduced augmented-state features and simple Ulam/MSM-style
transfer-operator estimates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .core import SimulationConfig
from .kernels import double_gaussian_gradient, exponential_weights


def augmented_feature_names(dim: int) -> list[str]:
    """Return names for the reduced augmented-state feature vector."""

    if dim < 1:
        raise ValueError("dim must be positive")
    return (
        [f"x_{i}" for i in range(dim)]
        + [f"memory_centroid_{i}" for i in range(dim)]
        + [f"x_minus_memory_centroid_{i}" for i in range(dim)]
        + ["memory_spread", "memory_mean_distance_to_x", "memory_mass"]
    )


def memory_summary_features(
    x: Iterable[float],
    memory: Iterable[Iterable[float]],
    weights: Iterable[float],
) -> np.ndarray:
    """Compress an explicit memory trace into finite augmented-state features.

    The feature vector contains the visible state, weighted memory centroid,
    offset between current state and centroid, memory spread, mean distance
    from the current state to retained memory deposits, and retained memory
    mass. It is a lossy representation of rho_n, meant for diagnostics rather
    than for a mathematical equivalence claim.
    """

    x_arr = np.asarray(x, dtype=float)
    if x_arr.ndim != 1:
        raise ValueError("x must be a 1D vector")

    mem = np.asarray(memory, dtype=float)
    w = np.asarray(weights, dtype=float)
    if mem.size == 0 or w.size == 0:
        centroid = x_arr.copy()
        offset = np.zeros_like(x_arr)
        tail = np.array([0.0, 0.0, 0.0], dtype=float)
        return np.concatenate([x_arr, centroid, offset, tail])
    if mem.ndim != 2:
        raise ValueError("memory must have shape (n_memory, dim)")
    if mem.shape[1] != x_arr.shape[0]:
        raise ValueError("memory dimension must match x")
    if mem.shape[0] != w.shape[0]:
        raise ValueError("weights must match memory length")
    if np.any(w < 0.0):
        raise ValueError("weights must be non-negative")

    mass = float(w.sum())
    if mass <= 0.0:
        centroid = x_arr.copy()
        offset = np.zeros_like(x_arr)
        tail = np.array([0.0, 0.0, 0.0], dtype=float)
        return np.concatenate([x_arr, centroid, offset, tail])

    normalized = w / mass
    centroid = np.sum(normalized[:, None] * mem, axis=0)
    offset = x_arr - centroid
    centered = mem - centroid[None, :]
    spread2 = float(np.sum(normalized * np.einsum("ij,ij->i", centered, centered)))
    to_x = mem - x_arr[None, :]
    dist_to_x = np.sqrt(np.einsum("ij,ij->i", to_x, to_x))
    mean_distance = float(np.sum(normalized * dist_to_x))
    tail = np.array([np.sqrt(max(spread2, 0.0)), mean_distance, mass], dtype=float)
    return np.concatenate([x_arr, centroid, offset, tail])


def memory_weight_in_ball(
    memory: Iterable[Iterable[float]],
    weights: Iterable[float],
    center: Iterable[float],
    *,
    radius: float,
) -> float:
    """Return retained memory weight inside a ball around ``center``."""

    if radius < 0.0:
        raise ValueError("radius must be non-negative")
    mem = np.asarray(memory, dtype=float)
    w = np.asarray(weights, dtype=float)
    c = np.asarray(center, dtype=float)
    if mem.size == 0 or w.size == 0:
        return 0.0
    if mem.ndim != 2:
        raise ValueError("memory must have shape (n_memory, dim)")
    if mem.shape[1] != c.shape[0]:
        raise ValueError("memory dimension must match center")
    if mem.shape[0] != w.shape[0]:
        raise ValueError("weights must match memory length")
    dist2 = np.einsum("ij,ij->i", mem - c[None, :], mem - c[None, :])
    return float(w[dist2 <= radius * radius].sum())


def vector_autocorrelation(
    values: Iterable[Iterable[float]] | Iterable[float],
    *,
    max_lag: int,
) -> np.ndarray:
    """Return normalized autocorrelation for scalar or vector observations."""

    arr = np.asarray(values, dtype=float)
    if arr.ndim == 1:
        arr = arr[:, None]
    if arr.ndim != 2:
        raise ValueError("values must be a 1D or 2D array")
    if max_lag < 0:
        raise ValueError("max_lag must be non-negative")
    if arr.shape[0] < 2:
        raise ValueError("at least two observations are required")

    centered = arr - arr.mean(axis=0, keepdims=True)
    denom = float(np.sum(centered * centered))
    out = np.empty(max_lag + 1, dtype=float)
    if denom <= 0.0:
        out.fill(np.nan)
        out[0] = 1.0
        return out
    for lag in range(max_lag + 1):
        if lag >= arr.shape[0]:
            out[lag] = np.nan
        elif lag == 0:
            out[lag] = 1.0
        else:
            out[lag] = float(np.sum(centered[:-lag] * centered[lag:]) / denom)
    return out


def _validate_config(config: SimulationConfig) -> None:
    if config.steps < 1:
        raise ValueError("steps must be positive")
    if config.dim < 1:
        raise ValueError("dim must be positive")
    if config.sample_every < 1:
        raise ValueError("sample_every must be positive")
    if config.max_memory < 1:
        raise ValueError("max_memory must be positive")
    if not 0.0 < config.alpha <= 1.0:
        raise ValueError("alpha must satisfy 0 < alpha <= 1")


def _horizon(config: SimulationConfig) -> int:
    return min(config.max_memory, max(1, int(config.memory_factor / config.alpha)))


def simulate_augmented_features(
    config: SimulationConfig,
    *,
    seed: int = 0,
) -> dict[str, np.ndarray]:
    """Run the finite-memory model and record reduced augmented-state features."""

    _validate_config(config)
    rng = np.random.default_rng(seed)
    horizon = _horizon(config)
    weights = exponential_weights(config.alpha, horizon)
    history = np.zeros((horizon, config.dim), dtype=float)
    filled = 0
    x = np.zeros(config.dim, dtype=float)
    samples: list[np.ndarray] = []
    sample_steps: list[int] = []
    features: list[np.ndarray] = []

    for step in range(1, config.steps + 1):
        if filled:
            grad = double_gaussian_gradient(
                x,
                history[:filled],
                weights[:filled],
                sigma_rep=config.sigma_rep,
                sigma_att=config.sigma_att,
                amplitude_rep=config.amplitude_rep,
                amplitude_att=config.amplitude_att,
            )
        else:
            grad = np.zeros(config.dim, dtype=float)

        x = x + config.epsilon * rng.normal(size=config.dim) - config.eta * grad

        if filled < horizon:
            if filled > 0:
                history[1 : filled + 1] = history[:filled]
            filled += 1
        else:
            history[1:] = history[:-1]
        history[0] = x

        if step >= config.burn_in and step % config.sample_every == 0:
            current_memory = history[:filled].copy()
            current_weights = weights[:filled].copy()
            samples.append(x.copy())
            sample_steps.append(step)
            features.append(memory_summary_features(x, current_memory, current_weights))

    return {
        "samples": np.asarray(samples, dtype=float),
        "sample_steps": np.asarray(sample_steps, dtype=int),
        "augmented_features": np.asarray(features, dtype=float),
        "feature_names": np.asarray(augmented_feature_names(config.dim), dtype=str),
        "final_x": x.copy(),
        "memory": history[:filled].copy(),
        "weights": weights[:filled].copy(),
    }


def voxel_labels(points: Iterable[Iterable[float]], *, voxel_size: float) -> np.ndarray:
    """Assign each point to an integer voxel label."""

    pts = np.asarray(points, dtype=float)
    if pts.ndim != 2:
        raise ValueError("points must be a 2D array")
    if voxel_size <= 0.0:
        raise ValueError("voxel_size must be positive")

    boxes = np.floor(pts / voxel_size).astype(np.int64)
    label_by_box: dict[tuple[int, ...], int] = {}
    labels = np.empty(pts.shape[0], dtype=np.int64)
    for i, box in enumerate(boxes):
        key = tuple(int(v) for v in box)
        labels[i] = label_by_box.setdefault(key, len(label_by_box))
    return labels


def transition_count_matrix(
    labels: Iterable[int],
    *,
    lag: int = 1,
    n_states: int | None = None,
) -> np.ndarray:
    """Count lagged transitions between integer state labels."""

    arr = np.asarray(labels, dtype=np.int64)
    if arr.ndim != 1:
        raise ValueError("labels must be a 1D array")
    if lag < 1:
        raise ValueError("lag must be positive")
    if arr.size <= lag:
        raise ValueError("need more labels than lag")
    if np.any(arr < 0):
        raise ValueError("labels must be non-negative")
    if n_states is None:
        n_states = int(arr.max()) + 1
    if n_states < 1:
        raise ValueError("n_states must be positive")

    counts = np.zeros((n_states, n_states), dtype=float)
    for i in range(arr.size - lag):
        counts[arr[i], arr[i + lag]] += 1.0
    return counts


def row_stochastic_matrix(
    counts: Iterable[Iterable[float]],
    *,
    empty_row: str = "self",
) -> np.ndarray:
    """Normalize transition counts row-wise.

    Finite trajectories can produce states that are observed only as terminal
    targets for the chosen lag and therefore have no outgoing transition
    counts. By default these rows are made absorbing. Use ``empty_row="zero"``
    to keep a substochastic matrix with explicit zero rows.
    """

    mat = np.asarray(counts, dtype=float)
    if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
        raise ValueError("counts must be a square matrix")
    if empty_row not in {"self", "zero"}:
        raise ValueError("empty_row must be 'self' or 'zero'")
    row_sum = mat.sum(axis=1, keepdims=True)
    out = np.zeros_like(mat, dtype=float)
    np.divide(mat, row_sum, out=out, where=row_sum > 0.0)
    if empty_row == "self":
        empty = np.flatnonzero(row_sum[:, 0] == 0.0)
        out[empty, empty] = 1.0
    return out


def implied_relaxation_rates(
    transition_matrix: Iterable[Iterable[float]],
    *,
    lag_time: float = 1.0,
    drop_stationary: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """Return eigenvalues and rates ``-log(|lambda|)/lag_time``."""

    if lag_time <= 0.0:
        raise ValueError("lag_time must be positive")
    matrix = np.asarray(transition_matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("transition_matrix must be square")
    if matrix.size == 0:
        return np.array([], dtype=complex), np.array([], dtype=float)

    eigenvalues = np.linalg.eigvals(matrix)
    order = np.argsort(-np.abs(eigenvalues))
    eigenvalues = eigenvalues[order]
    rates: list[float] = []
    for value in eigenvalues:
        modulus = float(abs(value))
        if drop_stationary and abs(modulus - 1.0) < 1e-8:
            continue
        if modulus <= 0.0:
            rates.append(float("inf"))
        else:
            rates.append(float(-np.log(min(modulus, 1.0)) / lag_time))
    return eigenvalues, np.asarray(rates, dtype=float)


@dataclass(frozen=True)
class TransferOperatorEstimate:
    labels: np.ndarray
    counts: np.ndarray
    transition_matrix: np.ndarray
    eigenvalues: np.ndarray
    relaxation_rates: np.ndarray
    empty_rows: np.ndarray


def estimate_transfer_operator(
    features: Iterable[Iterable[float]],
    *,
    voxel_size: float,
    lag: int = 1,
    lag_time: float | None = None,
    empty_row: str = "self",
) -> TransferOperatorEstimate:
    """Estimate a finite-state transfer operator from augmented features."""

    labels = voxel_labels(features, voxel_size=voxel_size)
    counts = transition_count_matrix(labels, lag=lag)
    empty_rows = np.flatnonzero(counts.sum(axis=1) == 0.0)
    transition = row_stochastic_matrix(counts, empty_row=empty_row)
    eigenvalues, rates = implied_relaxation_rates(
        transition,
        lag_time=float(lag if lag_time is None else lag_time),
        drop_stationary=True,
    )
    return TransferOperatorEstimate(
        labels=labels,
        counts=counts,
        transition_matrix=transition,
        eigenvalues=eigenvalues,
        relaxation_rates=rates,
        empty_rows=empty_rows,
    )
