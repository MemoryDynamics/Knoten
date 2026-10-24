"""Synthetic algebraic controls, not new trajectory evidence."""

import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.linalg import solve_discrete_lyapunov
from scipy.special import gamma

from review_transport_audit import audit_review_cell, gaussian_block_floor
from weak_nonlinearity import (
    covariance_response,
    exponential_contraction_diagnostic,
    exponential_weights,
    lag_matrix,
    radius_energies,
    stationary_msd,
    stationary_msd_response,
    transport_response,
    untruncated_transport_response,
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


def _projected_gaussian_gain(variance, kernel, dimension):
    """Closed Gaussian regression formula, not a nonlinear simulator."""
    ar, aa, sr, sa = kernel
    power = -1 - dimension / 2
    return (
        aa / sa**2 * (1 + variance / sa**2) ** power
        - ar / sr**2 * (1 + variance / sr**2) ** power
    )


@pytest.mark.parametrize("dimension", [1, 3, 7])
@pytest.mark.parametrize("variance", [0.02, 0.7])
@pytest.mark.parametrize("kernel", [(0, 26, 1, 3), (1, 35, 1, 3)])
def test_gaussian_force_projection_against_radial_integral(dimension, variance, kernel):
    ar, aa, sr, sa = kernel
    normalization = dimension * 2 ** (dimension / 2 - 1) * gamma(dimension / 2)

    def integrand(radius):
        physical_r2 = variance * radius**2
        force_gain = aa / sa**2 * np.exp(
            -physical_r2 / (2 * sa**2)
        ) - ar / sr**2 * np.exp(-physical_r2 / (2 * sr**2))
        return radius ** (dimension + 1) * np.exp(-(radius**2) / 2) * force_gain

    integral, _ = quad(integrand, 0, np.inf, epsabs=1e-11, epsrel=1e-12)
    projected = integral / normalization
    assert projected == pytest.approx(
        _projected_gaussian_gain(variance, kernel, dimension), rel=2e-12
    )


@pytest.mark.parametrize("correlation", [-0.4, 0.6])
def test_gaussian_projection_keeps_correlated_lag_regression(correlation):
    covariance = np.array(
        [[0.4, correlation * np.sqrt(0.28)], [correlation * np.sqrt(0.28), 0.7]]
    )
    nodes, weights = np.polynomial.hermite.hermgauss(32)
    indices = np.array(np.meshgrid(np.arange(32), np.arange(32))).reshape(2, -1).T
    probability = np.prod((weights / np.sqrt(np.pi))[indices], axis=1)
    states = np.sqrt(2) * nodes[indices] @ np.linalg.cholesky(covariance).T
    kernel = (1, 35, 1, 3)
    force = states * (35 / 9 * np.exp(-(states**2) / 18) - np.exp(-(states**2) / 2))
    cross = np.einsum("n,ni,nj->ij", probability, force, states)
    regression = np.linalg.solve(covariance, cross.T).T
    expected = np.diag(_projected_gaussian_gain(np.diag(covariance), kernel, 1))
    np.testing.assert_allclose(regression, expected, atol=2e-11, rtol=2e-11)


@pytest.mark.parametrize("horizon", [2, 7, 21])
@pytest.mark.parametrize("dimension", [1, 3])
@pytest.mark.parametrize("kernel", [(0, 26, 1, 3), (1, 35, 1, 3)])
def test_statistical_linearization_reproduces_transport_correction(
    horizon, dimension, kernel
):
    alpha, eta = 0.3, 0.01
    ar, aa, sr, sa = kernel
    curvature, cubic = aa / sa**2 - ar / sr**2, ar / (2 * sr**4) - aa / (2 * sa**4)
    weights = exponential_weights(alpha, horizon)
    mass = 1 - (1 - alpha) ** horizon
    gain = eta * mass * curvature
    covariance, _, derivative_matrix = covariance_response(weights, gain, dimension)
    d2, response = transport_response(weights, gain, derivative_matrix)
    d4 = eta * mass * cubic * response
    source = np.ones(horizon - 1)
    shift = np.zeros((horizon - 1, horizon - 1))
    shift[1:, :-1] = np.eye(horizon - 2)

    def projected_transport(t):
        # An analytic complex-step derivative, never a physical negative variance.
        coefficients = (
            eta
            * mass
            * weights[1:]
            * _projected_gaussian_gain(t * np.diag(covariance), kernel, dimension)
        )
        operator = shift - np.outer(source, coefficients)
        transfer = np.linalg.solve(np.eye(horizon - 1) - operator, source)[0]
        return 0.5 * transfer**2

    assert projected_transport(0.0) == pytest.approx(d2, rel=1e-13)
    derivative = np.imag(projected_transport(1e-20j)) / 1e-20
    assert derivative == pytest.approx(d4, rel=2e-12)


@pytest.mark.parametrize("dimension", [1, 2, 3])
@pytest.mark.parametrize("variance", [0.25, 1.0])
def test_projection_does_not_erase_nonzero_cubic_residual(dimension, variance):
    nodes, weights = np.polynomial.hermite.hermgauss(4)
    indices = (
        np.array(np.meshgrid(*([np.arange(4)] * dimension))).reshape(dimension, -1).T
    )
    states = np.sqrt(2 * variance) * nodes[indices]
    probability = np.prod((weights / np.sqrt(np.pi))[indices], axis=1)
    cubic = np.sum(states**2, axis=1)[:, None] * states
    residual = cubic - (dimension + 2) * variance * states
    cross = np.einsum("n,ni,nj->ij", probability, residual, states)
    residual_energy = np.sum(probability * np.sum(residual**2, axis=1))
    np.testing.assert_allclose(cross, 0, atol=1e-13)
    assert residual_energy == pytest.approx(
        2 * dimension * (dimension + 2) * variance**3
    )
    assert residual_energy > 0


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


@pytest.mark.parametrize(
    "alpha,gain", [(0.1, 0.04), (0.35, 0.2), (0.8, 2.0), (0.2, -0.05)]
)
def test_infinite_transport_against_two_state_covariance_recursion(alpha, gain):
    q = 1 - alpha
    root = q * (1 - gain)
    covariance = np.diag([0.0, q**2 / (1 - root**2)])
    transition = np.array([[1.0, -gain], [0.0, root]])
    noise = np.array([1.0, q])
    age_covariance = 0.0
    for age in range(1, 1000):
        covariance = transition @ covariance @ transition.T + np.outer(noise, noise)
        age_covariance += alpha * q**age * age * covariance[0, 0]
    cubic_gain, dimension = 0.017, 3
    diffusion, correction = untruncated_transport_response(
        alpha, gain, cubic_gain, dimension
    )
    denominator = 1 + gain * q / alpha
    assert diffusion == pytest.approx(0.5 / denominator**2, rel=2e-13)
    assert correction == pytest.approx(
        -(dimension + 2) * cubic_gain * age_covariance / denominator**3,
        rel=2e-12,
    )


@pytest.mark.parametrize("cubic_gain", [-0.003, 0.002])
def test_infinite_coefficients_match_long_finite_linear_reference(cubic_gain):
    alpha, horizon, gain, dimension = 0.3, 100, 0.12, 3
    mass = 1 - (1 - alpha) ** horizon
    weights = exponential_weights(alpha, horizon)
    _, _, perturbation = covariance_response(weights, mass * gain, dimension)
    finite_diffusion, finite_derivative = transport_response(
        weights, mass * gain, perturbation
    )
    infinite = untruncated_transport_response(alpha, gain, cubic_gain, dimension)
    np.testing.assert_allclose(
        infinite,
        [finite_diffusion, cubic_gain * mass * finite_derivative],
        rtol=1e-9,
        atol=1e-13,
    )


def test_zero_curvature_uses_the_brownian_weighted_second_age():
    alpha, cubic_gain, dimension = 0.23, 0.017, 4
    q = 1 - alpha
    diffusion, correction = untruncated_transport_response(
        alpha, 0.0, cubic_gain, dimension
    )
    assert diffusion == pytest.approx(0.5)
    assert correction == pytest.approx(
        -(dimension + 2) * cubic_gain * q * (1 + q) / alpha**2
    )
    assert untruncated_transport_response(alpha, 0.0, 0.0, dimension) == (0.5, 0.0)


def test_matched_curvature_transport_split_has_predicted_sign_and_ratio():
    alpha, eta, dimension = 0.25, 0.01, 3
    results = []
    for repulsive, attractive in [(0.0, 26.0), (1.0, 35.0)]:
        curvature = attractive / 9 - repulsive
        cubic = repulsive / 2 - attractive / 162
        theta, _, rate = exponential_contraction_diagnostic(
            alpha, eta * (repulsive + attractive / 9)
        )
        assert theta < 1 and rate < 1
        results.append(
            untruncated_transport_response(
                alpha, eta * curvature, eta * cubic, dimension
            )
        )
    assert results[0][0] == pytest.approx(results[1][0])
    assert results[0][1] > 0 > results[1][1]
    assert results[1][1] / results[0][1] == pytest.approx(-23 / 13)


@pytest.mark.parametrize(
    "alpha,gain,cubic_gain,dimension",
    [
        (0.0, 0.1, 0.01, 3),
        (1.0, 0.1, 0.01, 3),
        (1e-30, 0.1, 0.01, 3),
        (0.5, -1.0, 0.01, 3),
        (0.5, 3.0, 0.01, 3),
        (0.2, np.nan, 0.01, 3),
        (0.2, 0.1, np.nan, 3),
        (0.2, 0.1, 0.01, 0),
        (0.2, 0.1, 0.01, 2.5),
        (0.2, 0.1, 0.01, True),
    ],
)
def test_invalid_infinite_transport_domains_fail_closed(
    alpha, gain, cubic_gain, dimension
):
    with pytest.raises(ValueError):
        untruncated_transport_response(alpha, gain, cubic_gain, dimension)


@pytest.mark.parametrize(
    "alpha,horizon,gain,dimension",
    [(0.2, 2, 0.3, 1), (0.15, 5, 0.2, 3), (0.4, 9, 0.0, 4)],
)
def test_fixed_lag_response_matches_independent_perturbed_matrix_covariances(
    alpha, horizon, gain, dimension
):
    weights = exponential_weights(alpha, horizon)
    matrix = lag_matrix(weights, gain)
    _, _, perturbation = covariance_response(weights, gain, dimension)
    lags = np.array([0, 1, 2, 7, 23, 101])
    actual, derivative = stationary_msd_response(weights, gain, lags, dimension)

    def direct_msd(operator):
        covariance = solve_discrete_lyapunov(operator, np.ones_like(operator))
        result = []
        for lag in lags:
            value = lag * covariance[0, 0]
            for index in range(1, lag):
                value += (
                    2
                    * (lag - index)
                    * (np.linalg.matrix_power(operator, index) @ covariance)[0, 0]
                )
            result.append(dimension * value)
        return np.array(result)

    step = 1e-4
    numerical = (
        -direct_msd(matrix + 2 * step * perturbation)
        + 8 * direct_msd(matrix + step * perturbation)
        - 8 * direct_msd(matrix - step * perturbation)
        + direct_msd(matrix - 2 * step * perturbation)
    ) / (12 * step)
    np.testing.assert_allclose(actual, direct_msd(matrix), rtol=2e-13, atol=2e-13)
    np.testing.assert_allclose(derivative, numerical, rtol=2e-7, atol=2e-8)


@pytest.mark.parametrize("dimension", [1, 3])
@pytest.mark.parametrize("seeds", [1, 5])
def test_gaussian_block_floor_reduces_to_independent_brownian_blocks(dimension, seeds):
    blocks = 7
    msd = 5.0 * np.arange(blocks + 1)
    floor = gaussian_block_floor(msd, blocks, seeds, dimension)
    assert floor["variance_inflation_lower"] == 1
    assert floor["variance_inflation_upper"] == 1
    assert floor["relative_se_upper"] == pytest.approx(
        np.sqrt(2 / (dimension * seeds * blocks))
    )


def test_gaussian_block_floor_matches_full_correlated_quadratic_form():
    blocks, length, dimension, seeds = 12, 3, 3, 5
    root = -0.4
    indices = np.arange(blocks * length)
    increments = root ** np.abs(indices[:, None] - indices[None, :]) / (1 - root**2)
    block_map = np.kron(np.eye(blocks), np.ones((1, length)))
    block_covariance = block_map @ increments @ block_map.T
    msd = np.array([increments[:n, :n].sum() for n in length * np.arange(blocks + 1)])
    floor = gaussian_block_floor(msd, blocks, seeds, dimension)
    variance = 2 * np.sum(block_covariance**2) / (dimension * seeds * blocks**2)
    assert floor["relative_se_upper"] == pytest.approx(
        np.sqrt(variance) / block_covariance[0, 0]
    )
    tail = np.sum(block_covariance[0, 3:] ** 2)
    partial = gaussian_block_floor(msd[:4], blocks, seeds, dimension, tail)
    assert partial["relative_se_lower"] <= floor["relative_se_upper"]
    assert floor["relative_se_upper"] <= partial["relative_se_upper"]
    assert partial["relative_se_upper"] > partial["relative_se_lower"]


def test_reviewed_cell_does_not_conflate_block_and_long_time_transport():
    result = audit_review_cell()
    assert result["finite_mean_age"] == pytest.approx(97.31889850537348)
    assert result["finite_D2"] == pytest.approx(0.30025902139879984)
    assert result["block_D2"] == pytest.approx(0.4118720005785257)
    assert result["relative_linear_block_bias"] == pytest.approx(0.3717223171505746)
    assert 0.35 < result["block_to_long_time_quartic_ratio"] < 0.36
    assert 2 < result["independent_kernel_gaussian_sizing_z"] < 3
    assert result["omitted_block_covariance_squares_bound"] < 1e-20
    first, second = result["kernels"]
    assert first["infinite_relative_correction"] == pytest.approx(0.0008933257688964004)
    assert second["infinite_relative_correction"] == pytest.approx(
        -0.0015804994372782472
    )
    assert second["block_D4"] / first["block_D4"] == pytest.approx(-23 / 13)


@pytest.mark.parametrize(
    "msd,blocks,seeds,dimension,tail",
    [
        ([0, 1, 2], 0, 1, 1, 0),
        ([0, 1, 2], 5, True, 1, 0),
        ([0, 1, 2], 5, 1, 1.5, 0),
        ([0, 1, 2], 5, 1, 1, None),
        ([0, 1, 2], 5, 1, 1, -1),
        ([0, 1, np.nan], 5, 1, 1, 0),
        ([1, 2, 3], 5, 1, 1, 0),
        ([0, 0, 1], 5, 1, 1, 0),
    ],
)
def test_invalid_gaussian_floor_inputs_fail_closed(msd, blocks, seeds, dimension, tail):
    with pytest.raises(ValueError):
        gaussian_block_floor(msd, blocks, seeds, dimension, tail)
