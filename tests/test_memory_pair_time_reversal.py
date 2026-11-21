"""No target runs: compare spectra and lags of fixed finite FIFO linear controls."""

from fractions import Fraction
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


def _port_impedance(z, age, stay, g):
    gain = np.diag(H_CROSS)
    p = age @ z ** -np.arange(age.shape[1])
    coefficient = np.diag((z - np.asarray(stay)) / p - g)
    coefficient[0, 1], coefficient[1, 0] = -H_CROSS
    return np.linalg.solve(gain, coefficient) / (z - 1)


@pytest.mark.parametrize(
    "horizon,retention,stay",
    [
        (2, (0.45, 0.8), (0.71, 0.3)),
        (3, (0.05, 0.08), (0.64, 0.4)),
        (6, (0.05, 0.08), (0.64, 0.4)),
    ],
)
def test_colored_port_spectrum_matches_full_history_response(horizon, retention, stay):
    m, b, c, age, g = _matrices(horizon, retention, stay)
    scale = 1.3
    gain = np.diag(H_CROSS)
    for z in np.exp(1j * np.array([0.07, 0.7, 1.5, 2.7, pi])):
        impedance = _port_impedance(z, age, stay, g)
        transfer = (z - 1) * c @ np.linalg.solve(z * np.eye(2 * horizon) - m, b)
        response = transfer @ gain
        np.testing.assert_allclose(impedance @ response, np.eye(2), atol=3e-14)
        input_spectrum = scale * gain @ (impedance + impedance.conj().T) @ gain
        assert np.linalg.eigvalsh(input_spectrum).min() > 0.1
        assert input_spectrum[0, 1] == pytest.approx(scale * np.prod(H_CROSS))
        output = transfer @ input_spectrum @ transfer.conj().T
        np.testing.assert_allclose(
            output, scale * (response + response.conj().T), atol=2e-14
        )


def test_two_slot_colored_lags_match_the_impedance_fourier_coefficients():
    q = np.array([0.45, 0.65])
    stay = np.array([0.6, 0.35])
    _, _, _, age, g = _matrices(2, q, stay)
    z = np.exp(2j * pi * (np.arange(256) + 0.5) / 256)
    gain = np.diag(H_CROSS)
    spectral = []
    for point in z:
        impedance = _port_impedance(point, age, stay, g)
        spectral.append(gain @ (impedance + impedance.conj().T) @ gain)
    spectral = np.array(spectral)
    for lag in range(5):
        actual = np.mean(z[:, None, None] ** lag * spectral, axis=0)
        if lag == 0:
            expected = np.diag(H_CROSS * (2 * (1 + q) - H_CROSS))
            expected[0, 1] = expected[1, 0] = np.prod(H_CROSS)
        else:
            expected = np.diag(-H_CROSS * q * (stay + q) * (-q) ** (lag - 1))
        np.testing.assert_allclose(actual, expected, atol=1e-14)


def test_stable_long_retention_control_is_active_at_a_rational_frequency():
    horizon = 4
    stay = (0.7, 0.45)
    m, b, c, age, g = _matrices(horizon, (0.99, 0.5), stay)
    _lags(
        m, b, c, (1, 1), 1
    )  # Also checks the full translation quotient is Schur-stable.
    # Exact sign check at z=(7+24i)/25 using only rational arithmetic.
    cosine, sine, q = Fraction(7, 25), Fraction(24, 25), Fraction(99, 100)
    real, imag = Fraction(1), Fraction(0)
    p_re, p_im = real, imag
    for age_index in range(1, horizon):
        real, imag = real * cosine + imag * sine, imag * cosine - real * sine
        p_re += q**age_index * real
        p_im += q**age_index * imag
    normalizer = sum(q**j for j in range(horizon))
    d_re = (p_re * (cosine - 1) - p_im * sine) / normalizer
    d_im = (p_re * sine + p_im * (cosine - 1)) / normalizer
    exact = ((cosine - Fraction(7, 10)) * d_re + sine * d_im) / (d_re**2 + d_im**2)
    exact += Fraction(1, 40)  # Self coefficient divided by two, from -g/(z-1).
    assert exact < 0
    z = complex(cosine, sine)
    impedance = _port_impedance(z, age, stay, g)
    assert H_CROSS[0] * impedance[0, 0].real == pytest.approx(float(exact), abs=3e-14)
    velocity = np.array([1, 0])
    force = impedance @ velocity
    assert np.vdot(force, velocity).real < 0


def test_two_slot_causal_factors_and_shared_white_input_realize_the_spectrum():
    q = np.array([0.35, 0.81])
    stay = np.array([0.64, 0.5])
    _, _, _, age, g = _matrices(2, q, stay)
    gain = np.diag(H_CROSS)
    base = 1 + q - H_CROSS
    n0 = base * (1 + q**2) - q**2 * (stay + q)
    n1 = 2 * base * q - q * (stay + q)
    alpha = np.sqrt((n0 + np.sqrt(n0**2 - n1**2)) / 2)
    beta = n1 / (2 * alpha)
    for z in np.exp(1j * np.array([0.17, 0.95, 1.5, 2.3, pi])):
        independent = np.sqrt(2 * H_CROSS) * (alpha + beta / z) / (1 + q / z)
        source = np.column_stack([H_CROSS, np.diag(independent)])
        realized = source @ source.conj().T
        impedance = _port_impedance(z, age, stay, g)
        target = gain @ (impedance + impedance.conj().T) @ gain
        np.testing.assert_allclose(realized, target, atol=1e-14)
