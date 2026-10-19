"""Synthetic algebraic controls, not new trajectory evidence."""

import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest
from scipy.linalg import solve_discrete_lyapunov

from weak_nonlinearity import (
    covariance_response,
    exponential_weights,
    lag_matrix,
    radius_energies,
    stationary_msd,
    transport_response,
)


@pytest.mark.parametrize("gain", [0.0, 0.17, 0.63])
def test_lag_covariance_matches_independent_impulse_reference(gain):
    spec = importlib.util.spec_from_file_location(
        "old_reference", Path(__file__).with_name("finalize_evidence.py")
    )
    reference = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reference)
    weights = exponential_weights(0.19, 9)
    covariance, _, _ = covariance_response(weights, gain, 1)
    np.testing.assert_allclose(
        radius_energies(weights, covariance, 1),
        reference.linear_energies(0.19, 9, gain, steps=3000),
        rtol=1e-10,
    )


def test_zero_gain_displacement_is_brownian_at_every_lag():
    weights = exponential_weights(0.23, 8)
    lags = np.array([0, 1, 2, 7, 21, 200])
    np.testing.assert_allclose(stationary_msd(weights, 0, lags, 3), 3 * lags)


@pytest.mark.parametrize("gain", [0.0, 0.31, 0.72])
def test_zero_frequency_transport_matches_mean_age_and_green_kubo(gain):
    weights = exponential_weights(0.21, 11)
    diffusion, _ = transport_response(weights, gain)
    expected = 0.5 / (1 + gain * (weights @ np.arange(len(weights)))) ** 2
    assert diffusion == pytest.approx(expected, rel=1e-12)
    lags = np.array([9999, 10000])
    msd = stationary_msd(weights, gain, lags)
    assert (msd[1] - msd[0]) / 2 == pytest.approx(diffusion, rel=1e-8)


def test_covariance_derivative_matches_perturbed_lyapunov_equations():
    weights = exponential_weights(0.27, 7)
    matrix = lag_matrix(weights, 0.41)
    covariance, derivative, perturbation = covariance_response(weights, 0.41, 3)
    step = 1e-6
    source = np.ones_like(matrix)
    plus = solve_discrete_lyapunov(matrix + step * perturbation, source)
    minus = solve_discrete_lyapunov(matrix - step * perturbation, source)
    np.testing.assert_allclose(derivative, (plus - minus) / (2 * step), rtol=1e-7)
    forcing = perturbation @ covariance @ matrix.T
    np.testing.assert_allclose(
        derivative - matrix @ derivative @ matrix.T,
        forcing + forcing.T,
        atol=2e-13,
    )


@pytest.mark.parametrize("dimension", [1, 3, 6])
def test_horizon_two_matches_scalar_cubic_moment_balance(dimension):
    weights = np.array([0.6, 0.4])
    gain = 0.5
    a = -gain * weights[1]
    covariance, derivative, _ = covariance_response(weights, gain, dimension)
    expected_c = 1 / (1 - a**2)
    expected_derivative = -2 * a * weights[1] * (dimension + 2) * expected_c**3
    assert covariance[0, 0] == pytest.approx(expected_c)
    assert derivative[0, 0] == pytest.approx(expected_derivative)


def test_wick_factor_from_exact_gaussian_quadrature():
    nodes, weights = np.polynomial.hermite.hermgauss(4)
    coordinates = np.sqrt(2) * nodes
    weights /= np.sqrt(np.pi)
    fourth = np.sum(weights * coordinates**4)
    second = np.sum(weights * coordinates**2)
    for dimension in (1, 3, 7):
        contraction = fourth + (dimension - 1) * second**2
        assert contraction == pytest.approx(dimension + 2)


def test_cross_lag_wick_forcing_from_correlated_gaussian_quadrature():
    covariance = np.array([[1.3, 0.4], [0.4, 0.8]])
    dimension = 3
    nodes, weights = np.polynomial.hermite.hermgauss(3)
    indices = (
        np.array(np.meshgrid(*([np.arange(3)] * (2 * dimension))))
        .reshape(2 * dimension, -1)
        .T
    )
    probability = np.prod((weights / np.sqrt(np.pi))[indices], axis=1)
    independent = np.sqrt(2) * nodes[indices].reshape(-1, dimension, 2)
    correlated = independent @ np.linalg.cholesky(covariance).T
    cubic = np.sum(correlated**2, axis=1) * correlated[:, 0, :]
    empirical = np.einsum("n,ni,nj->ij", probability, correlated[:, 0, :], cubic)
    expected = (dimension + 2) * covariance * np.diag(covariance)[None, :]
    np.testing.assert_allclose(empirical, expected, atol=1e-13)


@pytest.mark.parametrize(
    "repulsive,attractive,cubic", [(0, 26, -13 / 81), (1, 35, 23 / 81)]
)
def test_cubic_coefficients_and_remainder_against_production_kernel(
    repulsive, attractive, cubic
):
    path = Path(__file__).resolve().parents[3] / "src/emergenz_knoten/kernels.py"
    spec = importlib.util.spec_from_file_location("paper_i_kernel_control", path)
    kernels = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = kernels
    spec.loader.exec_module(kernels)
    curvature = kernels.two_scale_local_curvature(
        sigma_rep=1, sigma_att=3, amplitude_rep=repulsive, amplitude_att=attractive
    )
    assert curvature == pytest.approx(26 / 9)
    assert repulsive / 2 - attractive / (2 * 3**4) == pytest.approx(cubic)
    direction = np.array([1.0, -2.0, 1.0]) / np.sqrt(6)
    for radius in (0.005, 0.01, 0.4, 2.0):
        displacement = radius * direction
        gradient = kernels.double_gaussian_gradient(
            displacement,
            np.zeros((1, 3)),
            [1.0],
            sigma_rep=1,
            sigma_att=3,
            amplitude_rep=repulsive,
            amplitude_att=attractive,
        )
        approximation = (curvature + cubic * radius**2) * displacement
        bound = (abs(repulsive) / 8 + abs(attractive) / (8 * 3**6)) * radius**5
        assert np.linalg.norm(gradient - approximation) <= bound + 2e-14
        if radius == 0.01:
            measured_cubic = (
                np.dot(gradient - curvature * displacement, direction) / radius**3
            )
            assert measured_cubic == pytest.approx(cubic, rel=1e-4)


def test_transport_derivative_matches_first_moment_of_effective_gain():
    weights = exponential_weights(0.18, 12)
    gain, dimension = 0.37, 4
    covariance, _, perturbation = covariance_response(weights, gain, dimension)
    diffusion, derivative = transport_response(weights, gain, perturbation)
    ages = np.arange(1, len(weights))
    correction = (dimension + 2) * np.sum(ages * weights[1:] * np.diag(covariance))
    denominator = 1 + gain * np.sum(ages * weights[1:])
    assert derivative == pytest.approx(-2 * diffusion * correction / denominator)


@pytest.mark.parametrize(
    "weights,gain,dimension",
    [
        ([0.5, 0.4], 0.2, 3),
        ([1.1, -0.1], 0.2, 3),
        ([1.0], 0.2, 3),
        ([0.5, 0.5], 1.0, 3),
        ([0.5, 0.5], 0.2, 1.5),
    ],
)
def test_invalid_domains_fail_closed(weights, gain, dimension):
    with pytest.raises(ValueError):
        covariance_response(weights, gain, dimension)
