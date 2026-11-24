"""Finite matrix identities for the existing linear memory reference.

No target trajectories, parameter search, or changes to native dynamics.
"""

import numpy as np
import pytest
from scipy.integrate import quad_vec
from scipy.linalg import expm

from emergenz_knoten.analytic import local_scalar_memory_modes


def _drift(restoring, memory_rate):
    return np.array([[-restoring, restoring], [memory_rate, -memory_rate]])


def _transition(time, restoring, memory_rate):
    rate = restoring + memory_rate
    return np.eye(2) - np.expm1(-rate * time) / rate * _drift(restoring, memory_rate)


def _moment_generator(restoring, memory_rate, diffusion):
    return np.array(
        [
            [-2 * restoring, 2 * restoring, 0, 2 * diffusion],
            [memory_rate, -(restoring + memory_rate), restoring, 0],
            [0, 2 * memory_rate, -2 * memory_rate, 0],
            [0, 0, 0, 0],
        ]
    )


def _variance(time, covariance, readout, restoring, memory_rate, diffusion):
    rate = restoring + memory_rate
    constant = memory_rate * sum(readout) / rate
    transient = (restoring * readout[0] - memory_rate * readout[1]) / rate
    row = readout @ _transition(time, restoring, memory_rate)
    noise = (
        2
        * diffusion
        * (
            constant**2 * time
            - 2 * constant * transient * np.expm1(-rate * time) / rate
            - transient**2 * np.expm1(-2 * rate * time) / (2 * rate)
        )
    )
    return row @ covariance @ row + noise


@pytest.mark.parametrize("restoring", [-0.2, 0.0, 0.7])
def test_continuous_reference_keeps_the_discrete_postwrite_order(restoring):
    memory_rate, diffusion = 1.3, 0.4
    drift = _drift(restoring, memory_rate)
    errors = []
    for step in [0.1, 0.01, 0.001]:
        alpha, gain = memory_rate * step, restoring * step
        transition = np.array(
            [[1 - gain, gain], [alpha * (1 - gain), 1 - alpha + alpha * gain]]
        )
        expected_remainder = np.array([[0, 0], [-alpha * gain, alpha * gain]])
        np.testing.assert_allclose(
            transition - np.eye(2) - step * drift, expected_remainder, atol=1e-16
        )
        np.testing.assert_allclose(
            np.sort(np.linalg.eigvals(transition)),
            np.sort(local_scalar_memory_modes(alpha, gain)),
            atol=2e-15,
        )
        noise_vector = np.array([1.0, alpha])
        noise_covariance_per_time = 2 * diffusion * np.outer(noise_vector, noise_vector)
        limiting_noise = np.diag([2 * diffusion, 0.0])
        errors.append(np.linalg.norm(noise_covariance_per_time - limiting_noise))
    assert errors[1] < errors[0] / 9
    assert errors[2] < errors[1] / 9


@pytest.mark.parametrize("restoring", [-0.2, 0.0, 0.7])
def test_closed_transition_and_covariance_match_independent_matrix_calculation(
    restoring,
):
    memory_rate, diffusion = 1.3, 0.4
    drift = _drift(restoring, memory_rate)
    initial = np.array([[1.2, 0.3], [0.3, 0.8]])
    moments = np.array([initial[0, 0], initial[0, 1], initial[1, 1], 1.0])
    generator = _moment_generator(restoring, memory_rate, diffusion)
    for time in [0.0, 0.3, 1.1]:
        transition = expm(drift * time)
        np.testing.assert_allclose(
            _transition(time, restoring, memory_rate), transition, atol=5e-16
        )

        def noise_covariance(age):
            response = expm(drift * age)[:, 0]
            return 2 * diffusion * np.outer(response, response)

        covariance = (
            transition @ initial @ transition.T + quad_vec(noise_covariance, 0, time)[0]
        )
        evolved = expm(generator * time) @ moments
        np.testing.assert_allclose(
            covariance, [[evolved[0], evolved[1]], [evolved[1], evolved[2]]], atol=2e-15
        )
        for readout in [np.array([1.0, 0.0]), np.array([0.2, 0.8])]:
            assert _variance(
                time, initial, readout, restoring, memory_rate, diffusion
            ) == pytest.approx(readout @ covariance @ readout, rel=3e-15)


def test_identical_gaussian_density_and_current_do_not_close_hidden_memory_variance():
    generator = _moment_generator(1.0, 0.5, 0.5)
    first, second = np.array([1.0, 0.5, 0.5, 1.0]), np.array([1.0, 0.5, 1.0, 1.0])
    for moments in [first, second]:
        covariance = np.array([[moments[0], moments[1]], [moments[1], moments[2]]])
        assert np.linalg.eigvalsh(covariance).min() > 0
        assert (generator @ moments)[0] == 0
        # Centered Gaussian current slope is s'/(2*s), hence both have S_x=0.
        assert (generator @ moments)[0] / (2 * moments[0]) == 0
    assert (generator @ generator @ first)[0] == pytest.approx(0.5)
    assert (generator @ generator @ second)[0] == pytest.approx(1.5)


@pytest.mark.parametrize("time", [0.001, 0.2, 2.0])
def test_hidden_variance_difference_has_an_exact_finite_time_position_signature(time):
    generator = _moment_generator(1.0, 0.5, 0.5)
    first, second = np.array([1.0, 0.5, 0.5, 1.0]), np.array([1.0, 0.5, 1.0, 1.0])
    observed = (expm(generator * time) @ (second - first))[0]
    expected = 0.5 * (-np.expm1(-1.5 * time) / 1.5) ** 2
    assert observed == pytest.approx(expected, rel=3e-13)
    assert observed > 0


def test_instantaneous_free_quantum_width_match_is_not_dynamically_invariant():
    generator = _moment_generator(1.0, 0.5, 0.5)
    initial = np.array([1.0, 0.5, 0.5, 1.0])
    s = initial[0]
    first = (generator @ initial)[0]
    second = (generator @ generator @ initial)[0]
    third = (generator @ generator @ generator @ initial)[0]
    action_over_twice_mass = 0.5
    residual = s * second / 2 - first**2 / 4 - action_over_twice_mass**2
    assert residual == pytest.approx(0.0)
    assert third == pytest.approx(-1.75)
    residual_derivative = s * third / 2
    assert residual_derivative == pytest.approx(-0.875)


@pytest.mark.parametrize("readout", [[1, 0], [0, 1], [0.3, 0.7], [2, -1]])
def test_translation_covariant_linear_positions_share_diffusive_large_time_variance(
    readout,
):
    readout = np.asarray(readout, dtype=float)
    restoring, memory_rate, diffusion = 0.7, 1.3, 0.4
    rate = restoring + memory_rate
    covariance = np.array([[1.2, 0.3], [0.3, 0.8]])
    constant = memory_rate / rate
    transient = (restoring * readout[0] - memory_rate * readout[1]) / rate
    diffusion_effective = diffusion * constant**2
    bounded_initial = (
        np.linalg.norm(readout) ** 2
        * np.linalg.norm(covariance, 2)
        * (1 + np.linalg.norm(_drift(restoring, memory_rate), 2) / rate) ** 2
    )
    bound = bounded_initial + 2 * diffusion * (
        2 * abs(constant * transient) / rate + transient**2 / (2 * rate)
    )
    for time in [0.1, 1.0, 10.0, 1000.0]:
        variance = _variance(
            time, covariance, readout, restoring, memory_rate, diffusion
        )
        assert abs(variance - 2 * diffusion_effective * time) <= bound
        assert abs(variance / (2 * time) - diffusion_effective) <= bound / (2 * time)


@pytest.mark.parametrize("initial_current_slope", [-0.4, 0.0, 0.7])
def test_free_quantum_gaussian_width_identity_also_has_a_classical_shear_control(
    initial_current_slope,
):
    mass, hbar, width = 1.3, 0.8, 1.1
    dq = hbar / (2 * mass)
    cross = mass * initial_current_slope * width
    momentum_variance = mass**2 * initial_current_slope**2 * width + hbar**2 / (
        4 * width
    )
    covariance = np.array([[width, cross], [cross, momentum_variance]])
    assert np.linalg.det(covariance) == pytest.approx(hbar**2 / 4)
    for time in [0.0, 0.2, 1.7]:
        shear = np.array([[1.0, time / mass], [0.0, 1.0]])
        s = (shear @ covariance @ shear.T)[0, 0]
        coefficient = width * initial_current_slope**2 + dq**2 / width
        first = 2 * width * initial_current_slope + 2 * coefficient * time
        second = 2 * coefficient
        assert s == pytest.approx(
            width + 2 * width * initial_current_slope * time + coefficient * time**2
        )
        assert s * second / 2 - first**2 / 4 - dq**2 == pytest.approx(0, abs=5e-16)
