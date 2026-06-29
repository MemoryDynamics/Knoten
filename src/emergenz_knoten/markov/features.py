"""Reduced feature maps for augmented finite-memory states ``z_n``."""

from __future__ import annotations

from typing import Iterable

import numpy as np


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
    """Compress an explicit memory state into finite augmented-state features.

    The feature vector contains the visible state, weighted memory centroid,
    offset between current state and centroid, memory spread, mean distance
    from the current state to retained memory deposits, and retained memory
    mass. It is a lossy representation of ``rho_n``, meant for diagnostics
    rather than for a mathematical equivalence claim.
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
