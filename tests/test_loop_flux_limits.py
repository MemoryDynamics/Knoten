"""Prescribed polygons and analytic ensembles, not native target trajectories."""

import numpy as np
import pytest

from emergenz_knoten.kernels import exponential_memory_weights
from emergenz_knoten.memory_current import path_current_fourier
from emergenz_knoten.state import FiniteMemoryState
from emergenz_knoten.vector_memory import oriented_history_from_state


SQUARE = np.array(
    [[-0.5, -0.5, 0], [0.5, -0.5, 0], [0.5, 0.5, 0], [-0.5, 0.5, 0], [-0.5, -0.5, 0]]
)


def _phase_weights(alpha, period):
    values = np.exp(np.arange(period) * np.log1p(-alpha))
    return values / values.sum()


@pytest.mark.parametrize("alpha", [0.2, 0.02, 0.0002])
def test_native_periodic_history_groups_exactly_and_obeys_uniform_limit_bound(alpha):
    period, repeats = 4, 3
    segments = period * repeats
    history = np.vstack([np.tile(SQUARE[:-1], (repeats, 1)), SQUARE[0]])
    weights = exponential_memory_weights(alpha, segments + 1, memory_mass=1.7)
    state = FiniteMemoryState(x=history[0], memory=history, weights=weights)
    _, _, native_weights = oriented_history_from_state(state)
    k = np.array([[0, 0, 0], [0.3, -0.5, 0.2], [1.2, 0.4, -0.1]])
    per_edge = np.array(
        [path_current_fourier(SQUARE[j : j + 2][::-1], k) for j in range(period)]
    )
    direct = np.einsum(
        "j,jki->ki", native_weights, per_edge[np.arange(segments) % period]
    )
    phase = _phase_weights(alpha, period)
    infinite = 1.7 * np.einsum("j,jki->ki", phase, per_edge)
    retained = -np.expm1(segments * np.log1p(-alpha))
    np.testing.assert_allclose(direct, retained * infinite, atol=4e-16)
    assert native_weights.sum() == pytest.approx(1.7 * retained)
    uniform = 1.7 * per_edge.mean(axis=0)
    bound = min(2.0, np.expm1(-(period - 1) * np.log1p(-alpha)))
    assert np.sum(np.abs(phase - 1 / period)) <= bound
    assert np.linalg.norm(infinite - uniform, axis=1).max() <= (
        1.7 * bound * np.linalg.norm(per_edge, axis=2).max() + 1e-15
    )


def test_positive_forgetting_can_leave_a_zero_wavevector_flux_on_a_closed_polygon():
    phase = _phase_weights(0.2, 4)
    displacements = SQUARE[:-1] - SQUARE[1:]
    assert np.linalg.norm(phase @ displacements) > 0.1
    np.testing.assert_array_equal(displacements.mean(axis=0), np.zeros(3))
    source = np.roll(phase, 1) - phase
    assert np.sum(np.abs(source)) == pytest.approx(2 * (phase[0] - phase[-1]))


def _refine(path, subdivisions):
    points = [
        start + fraction * (end - start)
        for start, end in zip(path[:-1], path[1:], strict=True)
        for fraction in np.arange(subdivisions) / subdivisions
    ]
    return np.vstack([points, path[-1]])


@pytest.mark.parametrize("subdivisions", [1, 4, 16])
def test_displacement_point_readout_has_a_controlled_line_quadrature_error(
    subdivisions,
):
    path = _refine(SQUARE, subdivisions)
    state = FiniteMemoryState(x=path[-1], memory=path[::-1], weights=np.ones(len(path)))
    positions, displacements, weights = oriented_history_from_state(state)
    k = np.array([[0, 0, 0], [0.3, -0.7, 0.2], [1.1, 0.2, -0.3]])
    sigma = 0.4
    gaussian = np.exp(-0.5 * sigma**2 * np.sum(k**2, axis=1))
    point = gaussian[:, None] * (
        (np.exp(-1j * k @ positions.T) * weights) @ displacements
    )
    line = path_current_fourier(path, k, sigma=sigma)
    lengths = np.linalg.norm(np.diff(path, axis=0), axis=1)
    bound = 0.5 * np.linalg.norm(k, axis=1) * np.sum(lengths**2) * gaussian
    assert np.all(np.linalg.norm(point - line, axis=1) <= bound + 4e-16)
    assert np.sum(lengths**2) == pytest.approx(4 / subdivisions)
    np.testing.assert_allclose(np.sum(k * line, axis=1), 0, atol=4e-16)


@pytest.mark.parametrize(
    "path",
    [SQUARE, np.array([[0, 0, 0], [1, 0.2, 0.3], [-0.1, 0.8, -0.2], [0, 0, 0]])],
)
def test_closed_loop_has_zero_mode_and_area_expansion_with_explicit_remainder(path):
    k = np.array([[0, 0, 0], [0.02, -0.01, 0.03], [0.7, -0.4, 0.2]])
    flux = path_current_fourier(path, k)
    length = np.linalg.norm(np.diff(path, axis=0), axis=1).sum()
    radius = np.linalg.norm(path, axis=1).max()
    area = 0.5 * np.cross(path[:-1], path[1:]).sum(axis=0)
    leading = 1j * np.cross(k, area)
    wave_norm = np.linalg.norm(k, axis=1)
    np.testing.assert_allclose(flux[0], 0, atol=2e-16)
    assert np.all(np.linalg.norm(flux, axis=1) <= wave_norm * length * radius + 2e-16)
    assert np.all(
        np.linalg.norm(flux - leading, axis=1)
        <= 0.5 * wave_norm**2 * length * radius**2 + 2e-16
    )
    np.testing.assert_allclose(np.sum(k * flux, axis=1), 0, atol=2e-16)


def _orthogonal_loop_spectrum(k, sigma=0.0):
    currents = np.array(
        [
            path_current_fourier(SQUARE[:, axes], k, sigma=sigma)
            for axes in ([0, 1, 2], [2, 0, 1], [1, 2, 0])
        ]
    )
    return np.einsum("aki,akj->kij", currents, currents.conj()) / 3


def test_normalized_transverse_shape_hides_vanishing_spectral_amplitude():
    direction = np.array([1, 2, 3]) / np.sqrt(14)
    magnitudes = np.array([0.005, 0.01])
    spectrum = _orthogonal_loop_spectrum(magnitudes[:, None] * direction)
    projector = np.eye(3) - np.outer(direction, direction)
    trace = np.trace(spectrum, axis1=1, axis2=2).real
    for j, magnitude in enumerate(magnitudes):
        np.testing.assert_allclose(spectrum[j] / trace[j], projector / 2, atol=2e-6)
        np.testing.assert_allclose(spectrum[j] / magnitude**2, projector / 3, atol=3e-6)
    assert trace[1] / trace[0] == pytest.approx(4, rel=2e-5)
    assert trace[1] < 0.0001


def test_fixed_gaussian_smoothing_cannot_remove_the_small_wavevector_suppression():
    k = np.array([[0.02, -0.03, 0.01], [0.4, 0.2, -0.1]])
    raw = _orthogonal_loop_spectrum(k)
    smoothed = _orthogonal_loop_spectrum(k, sigma=0.7)
    np.testing.assert_allclose(
        smoothed, np.exp(-(0.7**2) * np.sum(k**2, axis=1))[:, None, None] * raw
    )


def test_periodic_winding_path_is_not_a_closed_loop_in_its_euclidean_lift():
    size = 3.0
    path = np.array([[0, 0, 0], [size, 0, 0]])
    k = np.array([[0, 0, 0], [0, 2 * np.pi / size, 0]])
    np.testing.assert_array_equal(
        np.remainder(path[0], size), np.remainder(path[-1], size)
    )
    current = path_current_fourier(path, k)
    np.testing.assert_allclose(current, [[size, 0, 0], [size, 0, 0]])
    np.testing.assert_array_equal(np.sum(k * current, axis=1), np.zeros(2))
    assert np.linalg.norm(current[0]) == size
