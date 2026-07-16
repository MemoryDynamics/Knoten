import numpy as np
import pytest

from emergenz_knoten import (
    FiniteMemoryState,
    double_gaussian_gradient,
    memory_centroid,
    memory_shape_tensor,
    place_finite_memory_state,
    translate_finite_memory_state,
)


def _state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.array([0.4, -0.2, 0.7]),
        memory=np.array(
            [
                [0.4, -0.2, 0.7],
                [0.1, 0.3, 0.5],
                [-0.2, 0.4, -0.1],
                [0.6, -0.5, 0.2],
            ]
        ),
        weights=np.array([0.4, 0.3, 0.2, 0.1]),
    )


def _gradient(state: FiniteMemoryState) -> np.ndarray:
    return double_gaussian_gradient(
        state.x,
        state.memory,
        state.weights,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=2.5,
    )


def test_state_arrays_are_copied_and_read_only() -> None:
    x = np.array([0.0, 1.0])
    memory = np.array([[0.0, 1.0], [1.0, 0.0]])
    weights = np.array([0.7, 0.3])
    state = FiniteMemoryState(x=x, memory=memory, weights=weights)

    x[0] = 99.0
    memory[0, 0] = 99.0
    weights[0] = 0.0

    assert state.x[0] == 0.0
    assert state.memory[0, 0] == 0.0
    assert state.weights[0] == pytest.approx(0.7)
    with pytest.raises(ValueError):
        state.x[0] = 1.0


def test_translation_preserves_shape_and_self_gradient() -> None:
    state = _state()
    shifted = translate_finite_memory_state(state, [10.0, -4.0, 2.5])

    np.testing.assert_allclose(memory_centroid(shifted), memory_centroid(state) + [10.0, -4.0, 2.5])
    np.testing.assert_allclose(memory_shape_tensor(shifted), memory_shape_tensor(state), atol=1e-14)
    np.testing.assert_allclose(_gradient(shifted), _gradient(state), atol=1e-14)


def test_rigid_placement_rotates_shape_and_gradient_equivariantly() -> None:
    state = _state()
    rotation = np.array(
        [
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    target = np.array([3.0, 4.0, -2.0])
    placed = place_finite_memory_state(state, target, rotation=rotation)

    np.testing.assert_allclose(memory_centroid(placed), target, atol=1e-14)
    np.testing.assert_allclose(
        memory_shape_tensor(placed),
        rotation @ memory_shape_tensor(state) @ rotation.T,
        atol=1e-14,
    )
    np.testing.assert_allclose(_gradient(placed), rotation @ _gradient(state), atol=1e-14)


def test_rigid_placement_rejects_nonorthogonal_matrix() -> None:
    with pytest.raises(ValueError, match="orthogonal"):
        place_finite_memory_state(_state(), [0.0, 0.0, 0.0], rotation=np.diag([1.0, 1.0, 2.0]))
