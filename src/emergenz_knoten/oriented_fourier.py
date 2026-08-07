"""Exact Fourier observables of the retained oriented-memory fibre."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .oriented_source import OrientedMemoryState


@dataclass(frozen=True)
class OrientedFourierTransition:
    """Source-conditioned homogeneous target for one vector-memory update."""

    previous_modes: np.ndarray
    next_modes: np.ndarray
    source_modes: np.ndarray
    dropped_tail_modes: np.ndarray
    homogeneous_target_modes: np.ndarray


def _wavevectors(values: np.ndarray, dim: int) -> np.ndarray:
    wavevectors = np.asarray(values, dtype=float)
    if (
        wavevectors.ndim != 2
        or wavevectors.shape[1] != dim
        or wavevectors.shape[0] < 1
        or not np.isfinite(wavevectors).all()
    ):
        raise ValueError("wavevectors must be finite with shape (n_modes, dim)")
    return wavevectors


def oriented_memory_fourier_modes(
    state: OrientedMemoryState,
    wavevectors: np.ndarray,
) -> np.ndarray:
    """Evaluate every retained directed deposit in Fourier space."""

    k = _wavevectors(wavevectors, state.dim)
    phases = np.exp(-1j * (k @ state.scalar_state.memory.T))
    return np.asarray(
        np.einsum(
            "kn,n,nd->kd",
            phases,
            state.weights,
            state.orientations,
        ),
        dtype=np.complex128,
    )


def source_conditioned_fourier_transition(
    previous: OrientedMemoryState,
    following: OrientedMemoryState,
    wavevectors: np.ndarray,
    *,
    forgetting_factor: float,
) -> OrientedFourierTransition:
    """Remove the new deposit and finite-horizon tail from one transition."""

    if previous.dim != following.dim:
        raise ValueError("states must have the same dimension")
    if previous.scalar_state.n_memory != following.scalar_state.n_memory:
        raise ValueError("states must have the same retained horizon")
    if not np.array_equal(previous.weights, following.weights):
        raise ValueError("states must have identical vector weights")
    q = float(forgetting_factor)
    if not np.isfinite(q) or not 0.0 <= q < 1.0:
        raise ValueError("forgetting_factor must lie in [0, 1)")
    k = _wavevectors(wavevectors, previous.dim)
    old_modes = oriented_memory_fourier_modes(previous, k)
    new_modes = oriented_memory_fourier_modes(following, k)
    new_phase = np.exp(-1j * (k @ following.scalar_state.x))
    source_modes = (
        previous.weights[0]
        * new_phase[:, None]
        * following.carrier_orientation[None, :]
    )
    old_position = previous.scalar_state.memory[-1]
    old_orientation = previous.orientations[-1]
    old_phase = np.exp(-1j * (k @ old_position))
    dropped_tail = (
        q
        * previous.weights[-1]
        * old_phase[:, None]
        * old_orientation[None, :]
    )
    homogeneous_target = new_modes - source_modes + dropped_tail
    return OrientedFourierTransition(
        previous_modes=old_modes,
        next_modes=new_modes,
        source_modes=source_modes,
        dropped_tail_modes=dropped_tail,
        homogeneous_target_modes=homogeneous_target,
    )


def helmholtz_mode_components(
    modes: np.ndarray,
    wavevectors: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Split vector Fourier modes into longitudinal and transverse parts."""

    values = np.asarray(modes, dtype=np.complex128)
    if values.ndim != 2:
        raise ValueError("modes must have shape (n_modes, dim)")
    k = _wavevectors(wavevectors, values.shape[1])
    if k.shape[0] != values.shape[0]:
        raise ValueError("modes and wavevectors must have equal mode counts")
    norms = np.linalg.norm(k, axis=1)
    if np.any(norms <= 0.0):
        raise ValueError("Helmholtz split requires non-zero wavevectors")
    directions = k / norms[:, None]
    scalar = np.einsum("kd,kd->k", values, directions)
    longitudinal = scalar[:, None] * directions
    transverse = values - longitudinal
    return longitudinal, transverse