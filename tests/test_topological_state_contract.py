"""Constructed failures of an automatic sphere-valued memory field; no targets."""

import numpy as np
import pytest

from emergenz_knoten.kernels import exponential_memory_weights
from emergenz_knoten.oriented_source import update_persistent_orientation
from emergenz_knoten.state import FiniteMemoryState
from emergenz_knoten.vector_memory import (
    normalize_orientation,
    oriented_history_from_state,
    vector_gaussian_field,
)


def _backtracking_history(alpha, a):
    history = np.array([[a, 0.0, 0.0], [-a, 0.0, 0.0], [a, 0.0, 0.0]])
    state = FiniteMemoryState(
        x=history[0], memory=history, weights=exponential_memory_weights(alpha, 3)
    )
    return oriented_history_from_state(state, mode="unit")


@pytest.mark.parametrize(
    "alpha,a,sigma", [(0.2, 1.0, 1.0), (0.4, 0.5, 0.7), (0.1, 2.0, 1.3)]
)
def test_unit_history_directions_allow_an_exact_nodal_plane(alpha, a, sigma):
    positions, currents, weights = _backtracking_history(alpha, a)
    np.testing.assert_array_equal(currents, [[1, 0, 0], [-1, 0, 0]])
    root = sigma**2 * np.log1p(-alpha) / (2 * a)
    for transverse in ([0, 0], [0.3, -0.4]):
        point = np.array([root, *transverse])
        field = vector_gaussian_field(point, positions, currents, weights, sigma=sigma)
        np.testing.assert_allclose(field, 0, atol=5e-17)
        signs = []
        for offset in (-0.1 * a, 0.1 * a):
            point[0] = root + offset
            value = vector_gaussian_field(
                point, positions, currents, weights, sigma=sigma
            )
            signs.append(np.sign(value[0]))
        assert signs == [-1, 1]


def test_direction_readout_has_opposite_ray_directions_without_underflow():
    positions, currents, weights = _backtracking_history(0.2, 1.0)
    directions = []
    for x in (-4.0, 4.0):
        value = vector_gaussian_field(
            np.array([x, 0.0, 0.0]), positions, currents, weights, sigma=1.0
        )
        assert np.linalg.norm(value) > 1e-4
        directions.append(value / np.linalg.norm(value))
    np.testing.assert_array_equal(directions, [[-1, 0, 0], [1, 0, 0]])


def test_stationary_native_orientation_is_zero_not_a_point_on_the_sphere():
    np.testing.assert_array_equal(normalize_orientation(np.zeros(3)), np.zeros(3))


def test_persistent_orientation_can_cancel_at_regular_parameter_value():
    value = update_persistent_orientation(
        np.array([1.0, 0.0, 0.0]), np.array([-0.2, 0.0, 0.0]), relaxation=0.5
    )
    np.testing.assert_array_equal(value, np.zeros(3))
