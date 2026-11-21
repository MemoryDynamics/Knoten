"""Fixed checks of the analytic density reference, not a particle target run."""

import numpy as np
import pytest


DIFFUSION = 0.6  # Gaussian noise variance divided by two, per update.
WIDTH = 0.4  # Kernel variance divided by two.


def _mode(k, strength, ages):
    p = np.exp(-DIFFUSION * k**2)
    kernel = -np.exp(-WIDTH * k**2)
    # Units in this control: rho0 = W = K0 = 1, eta = strength.
    matrix = np.zeros((len(ages), len(ages)))
    matrix[0] = -p * strength * k**2 * kernel * np.asarray(ages)
    matrix[0, 0] += p
    matrix[1:, :-1] = np.eye(len(ages) - 1)
    drive = np.zeros(len(ages))
    drive[0] = -p * strength * k**2 * kernel
    return matrix, drive, p, kernel


@pytest.mark.parametrize("ages", [(1.0,), (0.4, 0.3, 0.2, 0.1), (0.7, 0.2, 0.1)])
def test_critical_static_residue_and_real_quartic_relaxation_are_age_independent(ages):
    k = 0.03
    matrix, drive, _, kernel = _mode(k, DIFFUSION, ages)
    roots = np.linalg.eigvals(matrix)
    index = np.argmax(abs(roots))
    slow = roots[index]
    assert slow.imag == pytest.approx(0, abs=1e-14)
    assert 0 < slow.real < 1
    assert np.all(abs(np.delete(roots, index)) < 0.1)
    d4 = DIFFUSION * WIDTH + DIFFUSION**2 / 2
    assert (1 - slow.real) / k**4 == pytest.approx(d4, rel=0.002)
    state = np.linalg.solve(np.eye(len(ages)) - matrix, drive)
    dressed = kernel * (1 + np.dot(ages, state))
    assert k**2 * dressed == pytest.approx(-DIFFUSION / d4, rel=0.002)


@pytest.mark.parametrize(
    "strength,stable", [(0.0, True), (0.4, True), (0.6, True), (0.8, False)]
)
def test_fixed_long_wave_modes_on_both_sides_of_the_threshold(strength, stable):
    matrix, _, _, _ = _mode(0.2, strength, (0.4, 0.3, 0.2, 0.1))
    assert bool(max(abs(np.linalg.eigvals(matrix))) < 1) == stable


def test_static_dressing_matches_the_full_history_resolvent():
    ages = (0.45, 0.35, 0.2)
    k = 0.7
    strength = 0.6
    matrix, drive, p, kernel = _mode(k, strength, ages)
    for z in (1, 1.4, np.exp(0.21j)):
        history = np.linalg.solve(z * np.eye(3) - matrix, drive)
        potential = kernel * (1 + np.dot(ages, history))
        age_filter = sum(weight * z**-age for age, weight in enumerate(ages))
        reduced = kernel * (z - p) / (z - p + p * strength * k**2 * kernel * age_filter)
        assert potential == pytest.approx(reduced, rel=2e-14)


@pytest.mark.parametrize("ages", [(0.4, 0.3, 0.2, 0.1), (0.7, 0.2, 0.1)])
def test_first_fifo_only_slow_mode_correction_is_sixth_order(ages):
    k = 0.08
    matrix, _, _, _ = _mode(k, DIFFUSION, ages)
    memoryless, _, _, _ = _mode(k, DIFFUSION, (1.0,))
    roots = np.linalg.eigvals(matrix)
    slow = roots[np.argmax(abs(roots))]
    correction = (slow - memoryless[0, 0]) / k**6
    mean_age = np.dot(np.arange(len(ages)), ages)
    d4 = DIFFUSION * WIDTH + DIFFUSION**2 / 2
    assert correction == pytest.approx(DIFFUSION * mean_age * d4, rel=0.03)


@pytest.mark.parametrize("k", [0.02, 0.04])
def test_fixed_time_critical_potential_has_no_static_pole(k):
    ages = (0.6, 0.3, 0.1)
    matrix, drive, _, kernel = _mode(k, DIFFUSION, ages)
    state = np.zeros(len(ages))
    for count in range(1, 8):
        state = matrix @ state + drive
        response = kernel * (1 + np.dot(ages, state))
        assert 0 < response / kernel - 1 <= count * drive[0]


def test_pushforward_derivative_matches_the_mode_rule_on_a_fixed_torus():
    # Direct Fourier quadrature of one nonlinear push and an exact Gaussian convolution.
    x = np.arange(8192) * (2 * np.pi / 8192)
    k, rho0, eta = 2, 0.8, 0.35
    history, weights, source = (
        np.array([0.2, -0.4, 0.5]),
        np.array([0.6, 0.3, 0.1]),
        0.25,
    )
    p = np.exp(-DIFFUSION * k**2)
    kernel = -np.exp(-WIDTH * k**2)
    source_amplitude = np.dot(weights, history) + source

    def cosine_after_update(amplitude):
        density = rho0 + amplitude * history[0] * np.cos(k * x)
        drift = amplitude * eta * k * kernel * source_amplitude * np.sin(k * x)
        return 2 * p * np.mean(density * np.cos(k * (x + drift)))

    step = 1e-4
    actual = (cosine_after_update(step) - cosine_after_update(-step)) / (2 * step)
    expected = p * (history[0] - eta * rho0 * k**2 * kernel * source_amplitude)
    assert actual == pytest.approx(expected, abs=3e-12)
