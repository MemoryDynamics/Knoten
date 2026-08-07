from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten import (
    FiniteMemoryState,
    OrientedMemoryState,
    helmholtz_mode_components,
    oriented_memory_fourier_modes,
    source_conditioned_fourier_transition,
)


def _state() -> OrientedMemoryState:
    return OrientedMemoryState(
        scalar_state=FiniteMemoryState(
            x=np.array([1.0, 0.0]),
            memory=np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]]),
            weights=np.array([0.5, 0.25, 0.125]),
        ),
        orientations=np.array([[1.0, 0.0], [0.0, 0.5], [-0.25, 0.0]]),
        weights=np.array([0.5, 0.25, 0.125]),
        carrier_orientation=np.array([1.0, 0.0]),
        orientation_relaxation=0.5,
    )


def test_zero_mode_is_weighted_vector_sum() -> None:
    state = _state()
    modes = oriented_memory_fourier_modes(state, np.zeros((1, 2)))

    expected = np.sum(state.weights[:, None] * state.orientations, axis=0)
    np.testing.assert_allclose(modes[0], expected)


def test_source_conditioned_transition_recovers_exact_forgetting_factor() -> None:
    previous = _state()
    q = 0.5
    following = OrientedMemoryState(
        scalar_state=FiniteMemoryState(
            x=np.array([2.0, 0.0]),
            memory=np.array([[2.0, 0.0], [1.0, 0.0], [0.0, 1.0]]),
            weights=previous.scalar_state.weights,
        ),
        orientations=np.array([[0.5, 0.5], [1.0, 0.0], [0.0, 0.5]]),
        weights=previous.weights,
        carrier_orientation=np.array([0.5, 0.5]),
        orientation_relaxation=0.5,
    )
    wavevectors = np.array([[0.3, 0.0], [0.0, 0.8], [0.4, -0.2]])

    transition = source_conditioned_fourier_transition(
        previous,
        following,
        wavevectors,
        forgetting_factor=q,
    )

    np.testing.assert_allclose(
        transition.homogeneous_target_modes,
        q * transition.previous_modes,
        atol=2e-16,
    )


def test_helmholtz_split_reconstructs_modes_and_is_orthogonal() -> None:
    wavevectors = np.array([[1.0, 0.0], [1.0, 1.0]])
    modes = np.array([[2.0 + 1j, 3.0], [0.5, -0.2j]])

    longitudinal, transverse = helmholtz_mode_components(modes, wavevectors)

    np.testing.assert_allclose(longitudinal + transverse, modes)
    directions = wavevectors / np.linalg.norm(wavevectors, axis=1)[:, None]
    np.testing.assert_allclose(
        np.einsum("kd,kd->k", transverse, directions),
        0.0,
        atol=1e-15,
    )


def test_fourier_observables_validate_shapes_and_forgetting() -> None:
    state = _state()

    with pytest.raises(ValueError, match="wavevectors"):
        oriented_memory_fourier_modes(state, np.ones((2, 3)))
    with pytest.raises(ValueError, match="non-zero"):
        helmholtz_mode_components(np.ones((1, 2)), np.zeros((1, 2)))
    with pytest.raises(ValueError, match="forgetting_factor"):
        source_conditioned_fourier_transition(
            state,
            state,
            np.ones((1, 2)),
            forgetting_factor=1.0,
        )