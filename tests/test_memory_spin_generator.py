"""Fixed algebraic controls for the generator ambiguity; no native target runs."""

import numpy as np
import pytest
from scipy.linalg import expm

from emergenz_knoten.state import FiniteMemoryState
from emergenz_knoten.vector_memory import (
    antisymmetric_current_tensor,
    oriented_history_from_state,
)
from experiments.current.reference.fifo_4d_spin_projection import (
    GENERATORS,
    INITIAL,
    INTERNAL_STEP,
    direction_readout,
    real_orbit,
)


def _hodge(matrix):
    """Euclidean 4D dual with epsilon_1234=+1, preserving exact test dtypes."""
    dual = np.zeros_like(matrix)
    dual[0, 1], dual[0, 2], dual[0, 3] = matrix[2, 3], -matrix[1, 3], matrix[1, 2]
    dual[1, 2], dual[1, 3], dual[2, 3] = matrix[0, 3], -matrix[0, 2], matrix[0, 1]
    return dual - dual.T


def _plane_data():
    p = INITIAL
    v = GENERATORS[2] @ p
    plane = np.outer(p, p) + np.outer(v, v)
    simple = np.outer(v, p) - np.outer(p, v)
    return p, v, plane, simple


def test_hodge_involution_and_reference_sector_exactly():
    upper = np.triu(np.arange(16).reshape(4, 4), 1)
    matrix = upper - upper.T
    np.testing.assert_array_equal(_hodge(_hodge(matrix)), matrix)
    for generator in GENERATORS:
        np.testing.assert_array_equal(_hodge(generator), -generator)


def test_exact_complementary_planes_and_quaternion_completion():
    p, v, plane, simple = _plane_data()
    dual = _hodge(simple)
    np.testing.assert_array_equal(simple @ p, v)
    np.testing.assert_array_equal(simple @ v, -p)
    np.testing.assert_array_equal(simple @ simple, -plane)
    np.testing.assert_array_equal(dual @ dual, -(np.eye(4) - plane))
    np.testing.assert_array_equal(simple @ dual, np.zeros((4, 4)))
    np.testing.assert_array_equal(dual @ simple, np.zeros((4, 4)))
    np.testing.assert_array_equal(simple - dual, GENERATORS[2])
    for sign in (-1, 1):
        completed = simple + sign * dual
        np.testing.assert_array_equal(completed @ completed, -np.eye(4))


@pytest.mark.parametrize("kappa", [-1, 0, 1, 2])
def test_same_entire_fifo_for_distinct_complementary_generators(kappa):
    p, v, plane, simple = _plane_data()
    generator = simple + kappa * _hodge(simple)
    np.testing.assert_array_equal(generator @ p, v)
    np.testing.assert_array_equal(generator @ v, -p)
    np.testing.assert_array_equal(
        generator @ generator, -plane - kappa**2 * (np.eye(4) - plane)
    )
    angles = 0.73 - INTERNAL_STEP * np.arange(5)
    history = np.array([expm(alpha * generator) @ p for alpha in angles])
    np.testing.assert_allclose(history, real_orbit(angles), atol=2e-15)
    np.testing.assert_allclose(
        direction_readout(history), direction_readout(real_orbit(angles)), atol=2e-15
    )


def test_fixed_off_plane_probe_distinguishes_the_completions_exactly():
    _, _, plane, simple = _plane_data()
    probe = np.array([1, 1, -1, -1]) / 2
    np.testing.assert_array_equal(plane @ probe, np.zeros(4))
    np.testing.assert_array_equal(simple @ probe, np.zeros(4))
    response = _hodge(simple) @ probe
    assert np.dot(response, response) == 1
    for kappa in (-1, 0, 1, 2):
        generator = simple + kappa * _hodge(simple)
        np.testing.assert_array_equal(generator @ probe, kappa * response)


def test_reflection_fixes_the_history_but_exchanges_quaternion_completions():
    p, v, _, simple = _plane_data()
    normal = np.array([1, 1, -1, -1]) / 2
    reflection = np.eye(4) - 2 * np.outer(normal, normal)
    np.testing.assert_array_equal(reflection @ reflection.T, np.eye(4))
    np.testing.assert_array_equal(reflection @ p, p)
    np.testing.assert_array_equal(reflection @ v, v)
    np.testing.assert_array_equal(reflection @ simple @ reflection.T, simple)
    np.testing.assert_array_equal(
        reflection @ _hodge(simple) @ reflection.T, -_hodge(simple)
    )
    np.testing.assert_array_equal(
        reflection @ GENERATORS[2] @ reflection.T, simple + _hodge(simple)
    )
    assert not np.array_equal(
        reflection @ GENERATORS[2] @ reflection.T, GENERATORS[2]
    )


@pytest.mark.parametrize("phase", [0, 0.37, 1.91])
def test_native_current_of_reference_history_is_a_simple_bivector(phase):
    history = real_orbit(phase - INTERNAL_STEP * np.arange(5))
    state = FiniteMemoryState(history[0], history, 0.3 * 0.7 ** np.arange(5))
    positions, directions, weights = oriented_history_from_state(state, mode="unit")
    current = antisymmetric_current_tensor(
        positions, directions, weights, origin=np.zeros(4)
    )
    _, _, plane, simple = _plane_data()
    scale = np.cos(INTERNAL_STEP / 2) * np.sum(weights)
    np.testing.assert_allclose(current, -scale * simple, atol=2e-16)
    np.testing.assert_allclose(current @ current, -(scale**2) * plane, atol=3e-16)
    np.testing.assert_allclose(
        (current - _hodge(current)) / (-scale), GENERATORS[2], atol=5e-16
    )
    assert np.linalg.matrix_rank(current) == 2
    assert np.linalg.norm(current + _hodge(current)) > 0.1


def test_centered_four_cycle_current_has_a_null_direction_in_4d():
    positions = np.eye(4)
    directions = (positions - np.roll(positions, -1, axis=0)) / np.sqrt(2)
    weights = np.array([0.4, 0.3, 0.2, 0.1])
    origin = np.average(positions, axis=0, weights=weights)
    current = antisymmetric_current_tensor(positions, directions, weights, origin=origin)
    np.testing.assert_allclose(current @ np.ones(4), np.zeros(4), atol=6e-17)
    assert np.linalg.matrix_rank(current) == 2
