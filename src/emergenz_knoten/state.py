"""Finite-memory state objects and rigid state transformations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class FiniteMemoryState:
    """Immutable visible position plus retained memory fibre.

    ``memory[0]`` is the youngest retained point and ``weights[0]`` its
    corresponding exponential weight.
    """

    x: np.ndarray
    memory: np.ndarray
    weights: np.ndarray

    def __post_init__(self) -> None:
        x = np.asarray(self.x, dtype=float)
        memory = np.asarray(self.memory, dtype=float)
        weights = np.asarray(self.weights, dtype=float)
        if x.ndim != 1 or x.size < 1:
            raise ValueError("x must be a non-empty one-dimensional vector")
        if memory.ndim != 2 or memory.shape[1] != x.size:
            raise ValueError("memory must have shape (n_memory, dim)")
        if memory.shape[0] < 1:
            raise ValueError("memory must contain at least one retained point")
        if weights.ndim != 1 or weights.shape[0] != memory.shape[0]:
            raise ValueError("weights must match the retained memory length")
        if not np.isfinite(x).all() or not np.isfinite(memory).all():
            raise ValueError("state coordinates must be finite")
        if not np.isfinite(weights).all() or np.any(weights < 0.0):
            raise ValueError("memory weights must be finite and non-negative")
        if float(np.sum(weights)) <= 0.0:
            raise ValueError("memory weight mass must be positive")

        x = x.copy()
        memory = memory.copy()
        weights = weights.copy()
        x.setflags(write=False)
        memory.setflags(write=False)
        weights.setflags(write=False)
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "memory", memory)
        object.__setattr__(self, "weights", weights)

    @property
    def dim(self) -> int:
        return int(self.x.size)

    @property
    def n_memory(self) -> int:
        return int(self.memory.shape[0])


def memory_centroid(state: FiniteMemoryState) -> np.ndarray:
    """Return the weighted centre of the retained memory cloud."""

    return np.average(state.memory, axis=0, weights=state.weights)


def memory_shape_tensor(state: FiniteMemoryState) -> np.ndarray:
    """Return the weighted covariance tensor around the memory centroid."""

    center = memory_centroid(state)
    centered = state.memory - center
    mass = float(np.sum(state.weights))
    return (centered * state.weights[:, None]).T @ centered / mass


def translate_finite_memory_state(
    state: FiniteMemoryState,
    offset: Iterable[float],
) -> FiniteMemoryState:
    """Translate the visible point and every retained memory point together."""

    shift = np.asarray(offset, dtype=float)
    if shift.shape != (state.dim,) or not np.isfinite(shift).all():
        raise ValueError("offset must be a finite vector matching state dimension")
    return FiniteMemoryState(
        x=state.x + shift,
        memory=state.memory + shift,
        weights=state.weights,
    )


def place_finite_memory_state(
    state: FiniteMemoryState,
    target_center: Iterable[float],
    *,
    rotation: Iterable[Iterable[float]] | None = None,
    source_center: Iterable[float] | None = None,
    atol: float = 1e-10,
) -> FiniteMemoryState:
    """Rigidly place a complete memory state around ``target_center``.

    The default source centre is the weighted memory centroid. ``rotation``
    may be any orthogonal matrix, including a reflection used as a diagnostic.
    """

    target = np.asarray(target_center, dtype=float)
    if target.shape != (state.dim,) or not np.isfinite(target).all():
        raise ValueError("target_center must match state dimension")
    if source_center is None:
        source = memory_centroid(state)
    else:
        source = np.asarray(source_center, dtype=float)
        if source.shape != (state.dim,) or not np.isfinite(source).all():
            raise ValueError("source_center must match state dimension")

    if rotation is None:
        transform = np.eye(state.dim, dtype=float)
    else:
        transform = np.asarray(rotation, dtype=float)
        if transform.shape != (state.dim, state.dim) or not np.isfinite(transform).all():
            raise ValueError("rotation must be a finite square matrix matching state dimension")
        if not np.allclose(transform.T @ transform, np.eye(state.dim), atol=atol, rtol=0.0):
            raise ValueError("rotation must be orthogonal")

    return FiniteMemoryState(
        x=target + transform @ (state.x - source),
        memory=target[None, :] + (state.memory - source[None, :]) @ transform.T,
        weights=state.weights,
    )
