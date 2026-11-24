"""Fixed Gaussian context controls, not proposed native parameter choices."""

import numpy as np
import pytest

from experiments.current.reference.fifo_gaussian_influence import (
    influence_matrix,
    vacuum_displacement_matrix,
)


def _causal_window(size, lags):
    result = -sum(lags) * np.eye(size)
    for lag, strength in enumerate(lags, start=1):
        if lag < size:
            result += strength * np.eye(size, k=-lag)
    return result


def test_three_paths_detect_inadmissibility_even_though_pairwise_moduli_are_bounded():
    response = _causal_window(2, [1.0])
    paths = 0.2 * np.vstack((np.zeros(2), np.eye(2)))
    noise = 0.4 * np.eye(2)
    matrix = influence_matrix(paths, response, noise)
    assert np.max(np.abs(matrix)) <= 1 + 2e-16
    assert np.linalg.eigvalsh(matrix)[0] < -1e-3
    with pytest.raises(ValueError, match="positivity"):
        vacuum_displacement_matrix(paths, response, noise)


@pytest.mark.parametrize("white_noise", [0.5, 0.9])
def test_time_ordered_vacuum_protocol_matches_given_phase_at_and_above_bound(
    white_noise,
):
    response = _causal_window(2, [1.0])
    noise = white_noise * np.eye(2)
    paths = np.array([[0, 0], [0.3, 0], [0, 0.8], [-0.1, 1.1]])
    expected = influence_matrix(paths, response, noise)
    actual = vacuum_displacement_matrix(paths, response, noise)
    np.testing.assert_allclose(actual, expected, atol=3e-16)
    assert np.linalg.eigvalsh(actual)[0] >= -1e-15
    cyclic = actual[0, 1] * actual[1, 2] * actual[2, 0]
    assert np.angle(cyclic) == pytest.approx(-0.3 * 0.8 / 2, abs=1e-15)


def test_multi_lag_spectral_couplings_recover_the_same_noise_and_response_on_every_window():
    times = np.arange(15)
    theta = np.linspace(-np.pi, np.pi, 128, endpoint=False)
    lags = [0.8, -0.3, 0.2]
    symbol = 1.4 + sum(gain * np.sin(lag * theta) for lag, gain in enumerate(lags, 1))
    wave = np.sqrt(symbol) * np.exp(-1j * times[:, None] * theta)
    covariance = wave.conj() @ wave.T / len(theta)
    for size in (2, 7, 15):
        response = _causal_window(size, lags)
        expected = 1.4 * np.eye(size) + 0.5j * (response - response.T)
        np.testing.assert_allclose(covariance[:size, :size], expected, atol=2e-15)


def test_one_lag_exact_white_floor_changes_with_window_size():
    for width in (2, 4, 16, 64):
        response = _causal_window(width, [1.7])
        antisymmetric = 0.5j * (response - response.T)
        floor = -np.linalg.eigvalsh(antisymmetric)[0]
        assert floor == pytest.approx(1.7 * np.cos(np.pi / (width + 1)), abs=2e-15)


def test_two_time_admissibility_alone_does_not_extend_to_four_times():
    vacuum_displacement_matrix(np.eye(2), _causal_window(2, [1.0]), 0.6 * np.eye(2))
    with pytest.raises(ValueError, match="positivity"):
        vacuum_displacement_matrix(np.eye(4), _causal_window(4, [1.0]), 0.6 * np.eye(4))


def test_conservative_phase_can_have_unit_modulus_but_causal_memory_cannot():
    paths = np.array([[0, 0], [0.4, 0], [0, 0.6]])
    diagonal = np.diag([0.3, -0.2])
    phase_only = vacuum_displacement_matrix(paths, diagonal, np.zeros((2, 2)))
    np.testing.assert_allclose(np.linalg.eigvalsh(phase_only), [0, 0, 3], atol=1e-15)
    response = _causal_window(2, [1.0])
    coarse = influence_matrix(paths, response, np.zeros((2, 2)))
    np.testing.assert_allclose(np.abs(coarse), 1, atol=3e-16)
    assert np.linalg.eigvalsh(coarse)[0] < 0
