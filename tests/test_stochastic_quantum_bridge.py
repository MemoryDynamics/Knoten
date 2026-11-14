"""Constructed reference identities, not quantum emergence or target runs."""

import numpy as np
import pytest

from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    exponential_memory_weights,
)


def test_same_visible_position_can_have_different_native_conditional_drifts():
    x = np.array([0.0])
    left = np.array([[0.0], [-1.0], [-0.5]])
    right = -left
    weights = exponential_memory_weights(0.2, 3, memory_mass=1.0)
    kernel = dict(sigma_rep=1.0, sigma_att=2.0, amplitude_rep=0.0, amplitude_att=1.0)
    drift_left = -double_gaussian_gradient(x, left, weights, **kernel)
    drift_right = -double_gaussian_gradient(x, right, weights, **kernel)
    np.testing.assert_allclose(drift_left, -drift_right, atol=0)
    assert drift_left[0] < -0.01
    assert drift_right[0] > 0.01


@pytest.mark.parametrize("order", [0, 1, 2])
def test_ou_ground_state_transform_has_real_decay_eigenvalues(order):
    diffusion, gamma = 0.7, 1.3
    x = np.linspace(-2.0, 2.0, 17)
    a = gamma / (2 * diffusion)
    h = np.exp(-a * x**2 / 2)
    coefficients = [[1.0], [0.0, 1.0], [-diffusion / gamma, 0.0, 1.0]][order]
    polynomial = np.polynomial.Polynomial(coefficients)
    p, dp, ddp = polynomial(x), polynomial.deriv()(x), polynomial.deriv(2)(x)

    # Apply the forward generator to h*phi, then compare in phi coordinates.
    density = h**2 * p
    density_prime = h**2 * (dp - 2 * a * x * p)
    density_second = h**2 * (ddp - 4 * a * x * dp + (4 * a**2 * x**2 - 2 * a) * p)
    transformed = (
        diffusion * density_second + gamma * (density + x * density_prime)
    ) / h
    phi = h * p
    phi_second = h * (ddp - 2 * a * x * dp + (a**2 * x**2 - a) * p)
    shifted_hamiltonian = (
        -diffusion * phi_second + (gamma**2 * x**2 / (4 * diffusion) - gamma / 2) * phi
    )
    np.testing.assert_allclose(transformed, -shifted_hamiltonian, atol=2e-15)
    np.testing.assert_allclose(transformed, -order * gamma * phi, atol=2e-15)


def test_stationary_density_match_uses_an_explicit_action_mass_calibration():
    diffusion, gamma, mass = 0.7, 1.3, 1.9
    hbar = 2 * mass * diffusion
    x = np.linspace(-3.0, 3.0, 19)
    ou_density = np.sqrt(gamma / (2 * np.pi * diffusion)) * np.exp(
        -gamma * x**2 / (2 * diffusion)
    )
    oscillator_density = np.sqrt(mass * gamma / (np.pi * hbar)) * np.exp(
        -mass * gamma * x**2 / hbar
    )
    np.testing.assert_allclose(ou_density, oscillator_density, rtol=2e-15)
    assert diffusion / gamma == pytest.approx(hbar / (2 * mass * gamma))


def test_imaginary_time_and_real_time_mode_amplitudes_are_not_interchangeable():
    coefficients = np.array([1.0, 0.3, -0.4])
    coefficients /= np.linalg.norm(coefficients)
    rates = 1.3 * np.arange(3)
    time = 0.7
    relaxed = coefficients * np.exp(-rates * time)
    unitary = coefficients * np.exp(-1j * rates * time)
    assert np.linalg.norm(relaxed) < 0.94
    assert np.linalg.norm(unitary) == pytest.approx(1.0)
    assert abs(relaxed[1] / relaxed[0]) < abs(unitary[1] / unitary[0])
    renormalized = relaxed / np.linalg.norm(relaxed)
    assert abs(renormalized[1] / renormalized[0]) == pytest.approx(
        abs(relaxed[1] / relaxed[0])
    )


@pytest.mark.parametrize("width_factor", [0.5, 1.0, 2.0])
def test_ou_gaussian_transient_does_not_keep_the_nelson_oscillator_force(width_factor):
    diffusion, gamma = 0.7, 1.3
    variance = width_factor * diffusion / gamma
    variance_rate = 2 * diffusion - 2 * gamma * variance
    x = np.array([-1.2, 0.0, 0.8])
    current_slope = diffusion / variance - gamma
    current_slope_rate = -diffusion * variance_rate / variance**2
    osmotic_slope = -diffusion / variance
    acceleration = (current_slope_rate + current_slope**2 - osmotic_slope**2) * x
    np.testing.assert_allclose(
        acceleration, (gamma**2 - 2 * diffusion**2 / variance**2) * x, atol=3e-15
    )
    oscillator_acceleration = -(gamma**2) * x
    if width_factor == 1.0:
        np.testing.assert_allclose(acceleration, oscillator_acceleration, atol=3e-15)
    else:
        assert np.linalg.norm(acceleration - oscillator_acceleration) > 1.0


@pytest.mark.parametrize("circulation", [-2.0, 0.0, 1.0, 0.25, 1.5])
def test_local_ring_schrodinger_solution_need_not_obey_periodic_boundary(circulation):
    length, mass, hbar = 4.7, 1.3, 0.8
    velocity = 2 * np.pi * hbar * circulation / (mass * length)
    energy = mass * velocity**2 / 2

    def local_wave(position, time):
        return np.exp(
            1j * (mass * velocity * position - energy * time) / hbar
        ) / np.sqrt(length)

    x, time = np.linspace(0.1, length - 0.1, 11), 0.3
    dx, dt = 1e-4, 1e-5
    wave = local_wave(x, time)
    time_derivative = (local_wave(x, time + dt) - local_wave(x, time - dt)) / (2 * dt)
    second_derivative = (
        local_wave(x + dx, time) - 2 * wave + local_wave(x - dx, time)
    ) / dx**2
    residual = 1j * hbar * time_derivative + hbar**2 * second_derivative / (2 * mass)
    np.testing.assert_allclose(residual, 0, atol=5e-7)
    np.testing.assert_allclose(abs(wave) ** 2, 1 / length, atol=2e-16)
    boundary_ratio = local_wave(length, time) / local_wave(0.0, time)
    np.testing.assert_allclose(
        boundary_ratio, np.exp(2j * np.pi * circulation), atol=2e-15
    )
    assert bool(np.isclose(boundary_ratio, 1.0)) == circulation.is_integer()


def test_one_fixed_twisted_boundary_allows_one_shifted_integer_lattice():
    twist = 0.25
    allowed = twist + np.array([-2, 0, 1])
    boundary_phase = np.exp(2j * np.pi * twist)
    np.testing.assert_allclose(np.exp(2j * np.pi * allowed), boundary_phase, atol=2e-15)
    assert not np.isclose(np.exp(2j * np.pi * 0.5), boundary_phase)


def test_memory_step_scale_inversion_and_physical_diffusion_units_are_separate():
    alpha, epsilon, calibration = 0.2, 0.3, 1.7
    memory_steps = 1 / alpha
    proposed_action = calibration * epsilon**2 / alpha
    assert proposed_action / (calibration * memory_steps) == pytest.approx(epsilon**2)
    assert proposed_action * memory_steps / calibration != pytest.approx(epsilon**2)

    physical_step, mass = 0.07, 1.9
    diffusion = epsilon**2 / (2 * physical_step)
    hbar = 2 * mass * diffusion
    assert hbar * physical_step / mass == pytest.approx(epsilon**2)
    # Exponents are ordered as mass, length, time; alpha is dimensionless.
    length_squared = np.array([0, 2, 0])
    action_units = np.array([1, 2, -1])
    np.testing.assert_array_equal(
        np.array([1, 0, 0]) + length_squared - np.array([0, 0, 1]), action_units
    )
    assert not np.array_equal(length_squared, action_units)
