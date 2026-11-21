"""No target runs: compare spectra and lags of fixed finite FIFO linear controls."""

from math import pi

import numpy as np
import pytest
from scipy.linalg import solve_discrete_lyapunov


H_CROSS = np.array([0.25, 0.15])


def _matrices(horizon, retention, stay):
    age = np.array(retention)[:, None] ** np.arange(horizon)
    age /= age.sum(axis=1, keepdims=True)
    g = 1 - np.asarray(stay) - H_CROSS
    m = np.zeros((2 * horizon, 2 * horizon))
    b = np.zeros((2 * horizon, 2))
    c = np.zeros((2, 2 * horizon))
    for i in range(2):
        j = 1 - i
        start, end = i * horizon, (i + 1) * horizon
        own = slice(start, end)
        other = slice(j * horizon, (j + 1) * horizon)
        m[start, own] = g[i] * age[i]
        m[start, start] += stay[i]
        m[start, other] = H_CROSS[i] * age[j]
        m[start + 1 : end, start : end - 1] = np.eye(horizon - 1)
        b[start, i] = 1
        c[i, own] = age[i]
    return m, b, c, age, g


def _lags(m, b, c, variance, limit):
    # Quotient by subtracting the final coordinate from every other coordinate.
    dimension = m.shape[0] - 1
    eye = np.eye(dimension)
    embed = np.vstack([eye, np.zeros(dimension)])
    diff = np.column_stack([eye, -np.ones(dimension)])
    stable = diff @ m @ embed
    assert max(abs(np.linalg.eigvals(stable))) < 1
    noise = diff @ b
    output = c @ (m - np.eye(dimension + 1)) @ embed
    direct = c @ b
    sigma = np.asarray(variance)
    if sigma.ndim == 1:
        sigma = np.diag(sigma)
    cov = solve_discrete_lyapunov(stable, noise @ sigma @ noise.T)
    start = stable @ cov @ output.T + noise @ sigma @ direct.T
    return np.array(
        [output @ np.linalg.matrix_power(stable, j) @ start for j in range(limit)]
    )


@pytest.mark.parametrize(
    "horizon,retention,stay,variance,reversible",
    [
        (2, (0.5, 0.25), (0.55, 0.55), (5, 3), False),
        (3, (0.5, 0.25), (0.55, 0.55), (5, 3), False),
        (4, (0.5, 0.5), (0.55, 0.55), (5, 3), True),
        (2, (0.5, 0.5), (0.55, 0.45), (5, 3), False),
        (2, (0.5, 0.5), (0.55, 0.55), (1, 1), False),
        (1, (0.5, 0.25), (0.55, 0.45), (5, 3), True),
        (1, (0.5, 0.5), (0.55, 0.55), (1, 1), False),
    ],
)
def test_history_spectrum_and_lags_agree_on_time_direction(
    horizon, retention, stay, variance, reversible
):
    m, b, c, age, g = _matrices(horizon, retention, stay)
    lag = _lags(m, b, c, variance, 2 * horizon - 1)
    imbalance = lag[:, 0, 1] - lag[:, 1, 0]
    imag = []
    for z in np.exp(1j * np.array([0.31, 1.23, 2.74])):
        point_to_increment = (
            (1 - 1 / z) * c @ np.linalg.solve(z * np.eye(2 * horizon) - m, b)
        )
        spectrum = (point_to_increment * variance) @ point_to_increment.conj().T
        p = age @ z ** -np.arange(horizon)
        diagonal = (z - stay) / p - g
        det = np.prod(diagonal) - np.prod(H_CROSS)
        bracket = (
            variance[0] * H_CROSS[1] * diagonal[1].imag
            - variance[1] * H_CROSS[0] * diagonal[0].imag
        )
        expected = abs(1 - 1 / z) ** 2 * bracket / abs(det) ** 2
        assert spectrum[0, 1].imag == pytest.approx(expected, abs=2e-14)
        reciprocal_transfer = point_to_increment * (5, 3)
        np.testing.assert_allclose(
            reciprocal_transfer, reciprocal_transfer.T, atol=2e-14
        )
        imag.append(expected)
    if reversible:
        np.testing.assert_allclose(imbalance, 0, atol=5e-15)
        np.testing.assert_allclose(imag, 0, atol=5e-15)
    else:
        assert np.max(abs(imbalance)) > 1e-4
        assert np.max(np.abs(imag)) > 1e-4


def test_a_fixed_heterogeneous_pair_can_match_one_lag_but_not_the_next():
    m, b, c, _, _ = _matrices(2, (0.5, 0.25), (0.55, 0.55))
    # Exact linearity of the Lyapunov equation in the two noise variances.
    a, b_only = (_lags(m, b, c, variance, 3) for variance in [(1, 0), (0, 1)])
    a_antisym = a[:, 0, 1] - a[:, 1, 0]
    b_antisym = b_only[:, 0, 1] - b_only[:, 1, 0]
    ratio = -b_antisym[0] / a_antisym[0]
    assert ratio > 0
    lag = _lags(m, b, c, [ratio, 1], 3)
    imbalance = lag[:, 0, 1] - lag[:, 1, 0]
    assert imbalance[0] == pytest.approx(0, abs=2e-15)
    assert abs(imbalance[1]) > 1e-4


def test_reciprocal_transfer_can_have_an_exact_nonzero_spectral_bracket():
    m, b, c, _, _ = _matrices(2, (0.5, 0.25), (0.55, 0.55))
    z = np.exp(1j * pi / 2)
    transfer = (1 - 1 / z) * c @ np.linalg.solve(z * np.eye(4) - m, b)
    spectrum = (transfer * (5, 3)) @ transfer.conj().T
    # For this case Im(A_A)=87/100 and Im(A_B)=69/68.
    a_a = (z - 0.55) / ((1 + 0.5 / z) / 1.5) - 0.2
    a_b = (z - 0.55) / ((1 + 0.25 / z) / 1.25) - 0.3
    bracket = (
        spectrum[0, 1].imag * abs(a_a * a_b - 0.25 * 0.15) ** 2 / abs(1 - 1 / z) ** 2
    )
    assert bracket == pytest.approx(369 / 3400, abs=2e-15)


def test_two_slots_can_recover_reversibility_with_a_fixed_white_covariance():
    horizon = 2
    m, b, c, age, g = _matrices(horizon, (0.5, 0.6), (0.5, 1 / 6))
    sigma = np.array([[685 / 21, 1], [1, 789 / 35]])
    assert np.linalg.eigvalsh(sigma).min() > 20
    m_lags = _lags(m, b, c, sigma, 2 * horizon - 1)
    no_cross = _lags(m, b, c, np.diag(sigma), 2 * horizon - 1)
    np.testing.assert_allclose(m_lags, m_lags.transpose(0, 2, 1), atol=2e-14, rtol=0)
    assert np.max(abs(no_cross - no_cross.transpose(0, 2, 1))) > 0.01
    for z in np.exp(1j * np.array([0.33, 0.78, 1.4, 2.3])):
        transfer = (1 - 1 / z) * c @ np.linalg.solve(z * np.eye(4) - m, b)
        spectrum = transfer @ sigma @ transfer.conj().T
        assert spectrum[0, 1].imag == pytest.approx(0, abs=2e-14)
        diagonal = (z - (0.5, 1 / 6)) / (age @ z ** -np.arange(horizon)) - g
        imaginary_part = (
            sigma[0, 0] * H_CROSS[1] * diagonal[1].imag
            - sigma[1, 1] * H_CROSS[0] * diagonal[0].imag
            + sigma[0, 1] * (diagonal[1] * diagonal[0].conjugate()).imag
        )
        assert imaginary_part == pytest.approx(0, abs=2e-14)


@pytest.mark.parametrize(
    "horizon,stay,rank",
    [
        (2, (0.5, 1 / 6), 2),
        (2, (0.5, 0.2), 3),
        (3, (0.5, 1 / 6), 3),
        (4, (0.5, 1 / 6), 3),
    ],
)
def test_linear_map_from_symmetric_white_covariance_to_odd_lags(horizon, stay, rank):
    m, b, c, _, _ = _matrices(horizon, (0.5, 0.6), stay)
    # Use a symmetric basis, including its indefinite off-diagonal element.
    covariance_basis = (
        [[1, 0], [0, 0]],
        [[0, 0], [0, 1]],
        [[0, 1], [1, 0]],
    )
    observations = []
    for sigma in covariance_basis:
        lags = _lags(m, b, c, sigma, 2 * horizon - 1)
        observations.append(lags[:, 0, 1] - lags[:, 1, 0])
    singular_values = np.linalg.svd(np.column_stack(observations), compute_uv=False)
    assert singular_values[rank - 1] > 1e-5
    if rank < 3:
        assert singular_values[rank] < 1e-15
