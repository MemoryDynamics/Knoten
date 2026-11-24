"""Constructed flux algebra, not a new spin-ice or Memory target simulation."""

import numpy as np
import pytest

from emergenz_knoten.kernels import exponential_memory_weights
from emergenz_knoten.memory_current import path_current_fourier
from emergenz_knoten.state import FiniteMemoryState
from emergenz_knoten.vector_memory import (
    oriented_history_from_state,
    vector_gaussian_field,
)


def _incidence(vertices, edges):
    """Discrete outgoing divergence: +1 at tail, -1 at head."""
    matrix = np.zeros((vertices, len(edges)))
    for j, (tail, head) in enumerate(edges):
        matrix[tail, j] += 1
        matrix[head, j] -= 1
    return matrix


def _cycle(vertices):
    return _incidence(vertices, [(j, (j + 1) % vertices) for j in range(vertices)])


def test_local_edge_change_creates_opposite_defects_and_cycle_preserves_them():
    divergence = _cycle(4)
    flux = np.array([1.0, 0.0, 0.0, 0.0])
    charge = divergence @ flux
    np.testing.assert_array_equal(charge, [1, -1, 0, 0])
    np.testing.assert_array_equal(divergence @ (flux + 3), charge)
    np.testing.assert_array_equal(np.ones(4) @ divergence, np.zeros(4))


def test_integer_charges_do_not_follow_without_a_discrete_flux_alphabet():
    charge = _cycle(4) @ np.array([0.25, 0, 0, 0])
    np.testing.assert_array_equal(charge, [0.25, -0.25, 0, 0])
    assert charge.sum() == 0


@pytest.mark.parametrize("stiffness", [0.7, 2.0])
def test_constrained_minimum_matches_independent_kkt_and_loop_energy(stiffness):
    divergence = _incidence(4, [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)])
    charge = np.array([1.0, 0.0, -1.0, 0.0])
    green = np.linalg.pinv(divergence @ divergence.T, hermitian=True)
    flux = divergence.T @ green @ charge
    np.testing.assert_allclose(divergence @ flux, charge, atol=2e-15)
    kkt = np.block(
        [
            [stiffness * np.eye(5), divergence.T],
            [divergence, np.zeros((4, 4))],
        ]
    )
    independent = np.linalg.lstsq(kkt, np.r_[np.zeros(5), charge], rcond=None)[0]
    np.testing.assert_allclose(independent[:5], flux, atol=2e-15)
    energy = 0.5 * stiffness * (flux @ flux)
    assert energy == pytest.approx(0.5 * stiffness * (charge @ green @ charge))
    loop = np.array([1.0, 1.0, 1.0, 1.0, 0.0])
    np.testing.assert_array_equal(divergence @ loop, np.zeros(4))
    assert flux @ loop == pytest.approx(0, abs=2e-15)
    assert 0.5 * stiffness * ((flux + loop) @ (flux + loop)) == pytest.approx(
        energy + 0.5 * stiffness * (loop @ loop)
    )


def test_reversing_edge_conventions_changes_neither_charge_nor_energy():
    divergence = _cycle(4)
    flux = np.array([1.0, -0.25, 0.5, 0.0])
    signs = np.array([-1, 1, -1, 1])
    np.testing.assert_array_equal(
        (divergence * signs) @ (signs * flux), divergence @ flux
    )
    assert (signs * flux) @ (signs * flux) == flux @ flux


def test_pseudoinverse_does_not_solve_a_nonneutral_closed_graph_source():
    divergence = _cycle(4)
    charge = np.array([1.0, 0, 0, 0])
    green = np.linalg.pinv(divergence @ divergence.T, hermitian=True)
    residual = charge - divergence @ divergence.T @ green @ charge
    np.testing.assert_allclose(residual, np.full(4, charge.mean()), atol=2e-15)
    assert np.linalg.norm(residual) > 0.4


@pytest.mark.parametrize("distance", [1, 2, 4])
def test_cycle_green_energy_has_resistance_scaling_not_three_dimensional_coulomb(
    distance,
):
    size = 8
    divergence = _cycle(size)
    charge = np.zeros(size)
    charge[0], charge[distance] = 1, -1
    green = np.linalg.pinv(divergence @ divergence.T, hermitian=True)
    assert charge @ green @ charge == pytest.approx(distance * (size - distance) / size)


@pytest.mark.parametrize("sigma", [0.0, 0.65])
def test_native_age_weights_leave_internal_sources_in_a_line_flux_readout(sigma):
    history = np.array([[1, 0, 0], [0, 1, 0], [-1, 0, 0.5], [0, -1, 0]])
    alpha = 0.2
    state = FiniteMemoryState(
        x=history[0], memory=history, weights=exponential_memory_weights(alpha, 4)
    )
    positions, displacements, weights = oriented_history_from_state(state)
    np.testing.assert_array_equal(positions, history[:-1])
    np.testing.assert_array_equal(displacements, history[:-1] - history[1:])
    k = np.array([[0, 0, 0], [0.4, -0.7, 0.3], [1.2, 0.3, -0.5]])
    flux = sum(
        weight
        * path_current_fourier(np.array([history[j + 1], history[j]]), k, sigma=sigma)
        for j, weight in enumerate(weights)
    )
    source = np.r_[-weights[0], weights[:-1] - weights[1:], weights[-1]]
    smoothing = np.exp(-0.5 * sigma**2 * np.sum(k**2, axis=1))
    expected = smoothing * (np.exp(-1j * k @ history.T) @ source)
    np.testing.assert_allclose(1j * np.sum(k * flux, axis=1), expected, atol=2e-16)
    np.testing.assert_allclose(source[1:-1], alpha * weights[:-1], atol=1e-17)
    assert np.all(source[1:-1] > 0)
    assert source.sum() == pytest.approx(0, abs=2e-17)


def test_geometrically_closed_loop_is_not_divergence_free_with_age_weights():
    # Newest-first history runs opposite to the edge orientation used above.
    divergence = _incidence(4, [((j + 1) % 4, j) for j in range(4)])
    weights = exponential_memory_weights(0.2, 5)[:-1]
    np.testing.assert_array_equal(divergence @ np.full(4, weights[0]), np.zeros(4))
    source = divergence @ weights
    assert source[0] == pytest.approx(weights[-1] - weights[0])
    np.testing.assert_allclose(source[1:], weights[:-1] - weights[1:])
    assert np.count_nonzero(source) == 4
    assert np.sum(np.abs(source)) == pytest.approx(2 * (weights[0] - weights[-1]))


def test_native_point_deposits_are_not_an_exact_line_integral_even_without_aging():
    history = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 0]])
    state = FiniteMemoryState(x=history[0], memory=history, weights=np.ones(5))
    positions, displacements, weights = oriented_history_from_state(state)
    point = np.array([0.2, 0.3, 0.0])
    sigma = 0.7
    difference = point - positions
    kernel = np.exp(-np.sum(difference**2, axis=1) / (2 * sigma**2))
    analytic = (
        -np.sum(weights * kernel * np.sum(displacements * difference, axis=1))
        / sigma**2
    )
    step = 1e-5
    numeric = 0.0
    for axis in np.eye(3):
        plus = vector_gaussian_field(
            point + step * axis, positions, displacements, weights, sigma=sigma
        )
        minus = vector_gaussian_field(
            point - step * axis, positions, displacements, weights, sigma=sigma
        )
        numeric += (plus - minus) @ axis / (2 * step)
    assert numeric == pytest.approx(analytic, abs=2e-9)
    assert abs(analytic) > 0.01
    k = np.array([[0.3, -0.7, 0.1], [1.2, 0.4, -0.5]])
    line = path_current_fourier(history[::-1], k, sigma=sigma)
    np.testing.assert_allclose(np.sum(k * line, axis=1), 0, atol=2e-16)
