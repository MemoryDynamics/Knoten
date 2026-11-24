"""Deterministic controls for the finite-population fluctuation diagnostic."""

from math import pi, sqrt

import numpy as np
import pytest
from scipy.linalg import solve_discrete_lyapunov


D0, WIDTH = 0.6, 0.4
D4 = D0 * WIDTH + D0**2 / 2


def _mode(k, ages):
    p = np.exp(-D0 * k**2)
    attractive = D0 * k**2 * np.exp(-WIDTH * k**2)
    matrix = np.zeros((len(ages), len(ages)))
    matrix[0] = p * attractive * np.asarray(ages)
    matrix[0, 0] += p
    matrix[1:, :-1] = np.eye(len(ages) - 1)
    return matrix


def _slow_mode(k, ages):
    roots = np.linalg.eigvals(_mode(k, ages))
    slow = roots[np.argmax(abs(roots))]
    assert abs(slow.imag) < 1e-14
    return slow.real


@pytest.mark.parametrize("k,other_k", [(1, 1), (1, 2), (-1, 2), (0, 1)])
def test_conditional_covariance_by_independent_gaussian_quadrature(k, other_k):
    predicted_heads = np.array([0.31, -0.25, 1.15, 2.0])
    nodes, weights = np.polynomial.hermite.hermgauss(40)
    probabilities = weights / sqrt(pi)
    positions = predicted_heads[:, None] + 2 * sqrt(D0) * nodes[None, :]
    values_k = np.exp(-1j * k * positions)
    values_l = np.exp(-1j * other_k * positions)
    centered_k = values_k - (values_k @ probabilities)[:, None]
    centered_l = values_l - (values_l @ probabilities)[:, None]
    # Different particles contribute no cross terms after conditioning.
    actual = (centered_k * centered_l.conj()) @ probabilities
    actual = actual.sum() / len(predicted_heads) ** 2
    difference = k - other_k
    expected = (
        (np.exp(-D0 * difference**2) - np.exp(-D0 * (k**2 + other_k**2)))
        * np.mean(np.exp(-1j * difference * predicted_heads))
        / len(predicted_heads)
    )
    assert actual == pytest.approx(expected, abs=3e-15)


@pytest.mark.parametrize("ages", [(1.0,), (0.5, 0.3, 0.2), (0.4, 0.3, 0.2, 0.1)])
def test_full_history_lyapunov_covariance_has_the_same_critical_residue(ages):
    k, population = 0.03, 320
    matrix = _mode(k, ages)
    noise = np.zeros_like(matrix)
    noise[0, 0] = -np.expm1(-2 * D0 * k**2) / population
    covariance = solve_discrete_lyapunov(matrix, noise)
    np.testing.assert_allclose(
        covariance, matrix @ covariance @ matrix.T + noise, atol=1e-12
    )
    assert population * k**2 * covariance[0, 0] == pytest.approx(D0 / D4, rel=0.003)


@pytest.mark.parametrize("c", [0.07, 0.22])
def test_quadratic_second_harmonic_from_direct_pushforward(c):
    theta = np.arange(4096) * (2 * pi / 4096)
    p2 = np.exp(-4 * D0 * 0.35**2)

    def second(amplitude):
        kicked = theta - c * amplitude * np.sin(theta)
        return 2 * p2 * np.mean((1 + amplitude * np.cos(theta)) * np.cos(2 * kicked))

    step = 1e-3
    quadratic = (second(step) + second(-step) - 2 * second(0)) / (2 * step**2)
    assert quadratic == pytest.approx(p2 * (c + c**2), abs=7e-9)


@pytest.mark.parametrize("ages", [(1.0,), (0.5, 0.3, 0.2)])
def test_forced_second_harmonic_uses_product_rate_not_static_denominator(ages):
    k = 0.04
    r = _slow_mode(k, ages)
    matrix = _mode(2 * k, ages)
    assert r**2 > _slow_mode(2 * k, ages)
    c = r / np.exp(-D0 * k**2) - 1
    drive = np.zeros(len(ages))
    drive[0] = np.exp(-4 * D0 * k**2) * (c + c**2)
    history = np.linalg.solve(r**2 * np.eye(len(ages)) - matrix, drive)
    np.testing.assert_allclose(r**2 * history, matrix @ history + drive, atol=1e-12)
    assert k**2 * history[0] == pytest.approx(D0 / (14 * D4), rel=0.02)
    static = np.linalg.solve(np.eye(len(ages)) - matrix, drive)
    assert k**2 * static[0] == pytest.approx(D0 / (16 * D4), rel=0.02)
    assert history[0] > static[0]


@pytest.mark.parametrize("k", [0.2, 0.035])
def test_gaussian_phase_reference_covariance_and_infrared_scale(k):
    population = 8_000_000
    r, s = _slow_mode(k, (1.0,)), _slow_mode(2 * k, (1.0,))
    variance = -np.expm1(-2 * D0 * k**2) / (population * (1 - r**2))
    c = D0 * k**2 * np.exp(-WIDTH * k**2)
    coupling = 2 * np.exp(-4 * D0 * k**2) * (c + c**2)
    expected = (
        2 * coupling**2 * variance**2 * (1 + s * r**2) / ((1 - s**2) * (1 - s * r**2))
    )
    if k == 0.2:
        # Compare the identity away from the ill-conditioned unit eigenvalues.
        matrix = np.array([[r**2, 0], [coupling, s]])
        noise = np.diag([2 * variance**2 * (1 - r**4), 0])
        direct = solve_discrete_lyapunov(matrix, noise)[1, 1]
        assert direct == pytest.approx(expected, abs=0, rel=3e-11)
    else:
        scaled_ratio = sqrt(expected / variance) * sqrt(population) * k**3
        assert scaled_ratio == pytest.approx(D0 / (6 * D4) * sqrt(D0 / D4), rel=0.02)
