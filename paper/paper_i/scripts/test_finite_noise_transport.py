"""Algebraic controls of explicit remainder bounds, not target simulations."""

import numpy as np
from numpy.polynomial.hermite_e import hermegauss
import pytest

from finite_noise_transport import (
    audit_finite_noise_budget,
    estimator_error_coefficients,
    flat_start_error_coefficient,
    gaussian_norm,
    relative_error_budget,
    remainder_constants,
    sufficient_noise_interval,
    transport_error_coefficients,
)
from weak_nonlinearity import (
    covariance_response,
    exponential_weights,
    transport_response,
)


@pytest.mark.parametrize("dimension", [1, 3, 8])
@pytest.mark.parametrize("order", [2, 4, 12, 20])
def test_gaussian_even_moments_match_chi_square_product(dimension, order):
    exact = np.prod(dimension + 2.0 * np.arange(order // 2))
    assert gaussian_norm(dimension, order) ** order == pytest.approx(exact, rel=3e-14)


@pytest.mark.parametrize("horizon", [2, 7])
def test_zero_feedback_has_no_remainders_or_initialization_error(horizon):
    result = remainder_constants(0.3, horizon, 0.0, 1, 35, 1, 3, 2)
    assert result["D2"] == 0.5
    assert result["D4"] == 0
    assert all(result[key] == 0 for key in ("u4", "z4", "e4", "dU2", "dZ2", "dE2"))
    np.testing.assert_array_equal(transport_error_coefficients(result), np.zeros(3))
    np.testing.assert_array_equal(estimator_error_coefficients(result, 3), np.zeros(3))
    assert flat_start_error_coefficient(0.3, 0, 2, 3, 4, 0) == 0


@pytest.mark.parametrize("horizon", [2, 5, 12])
def test_explicit_transport_coefficients_match_independent_matrix_response(horizon):
    alpha, eta, dimension = 0.3, 0.02, 3
    weights = exponential_weights(alpha, horizon)
    mass = 1 - (1 - alpha) ** horizon
    gain = eta * mass * 26 / 9
    covariance, _, derivative = covariance_response(weights, gain, dimension)
    d2, response = transport_response(weights, gain, derivative)
    result = remainder_constants(
        alpha, horizon, eta, 1, 35, 1, 3, dimension, covariance
    )
    assert result["D2"] == pytest.approx(d2, rel=2e-13)
    assert result["D4"] == pytest.approx(eta * mass * 23 / 81 * response, rel=2e-13)


def test_h2_zero_curvature_cubic_moment_and_resampling_by_exact_quadrature():
    alpha, eta = 0.4, 0.1
    # Here kappa=0, W_n=xi_n and Z_n=-a*xi_(n-1)^3 exactly.
    result = remainder_constants(alpha, 2, eta, 1, 9, 1, 3, 1)
    a = eta * (4 / 9) * alpha * (1 - alpha)
    x, weights = hermegauss(8)
    weights /= np.sqrt(2 * np.pi)
    z = -a * x**3
    exact_l4 = (weights @ z**4) ** 0.25
    exact_dependence_l2 = np.sqrt(
        np.sum(np.outer(weights, weights) * (z[:, None] - z[None, :]) ** 2)
    )
    assert result["z4"] == pytest.approx(exact_l4, rel=2e-14)
    assert exact_dependence_l2 == pytest.approx(np.sqrt(30) * a)
    assert exact_dependence_l2 <= result["dZ2"]


@pytest.mark.parametrize("alpha,theta", [(0.2, 0.1), (0.3, 0.7), (0.01, 0.5)])
def test_positive_filter_and_full_past_initialization_recurrences(alpha, theta):
    q = 1 - alpha
    s = theta * alpha / q
    root = q + s * q
    impulse = [1.0]
    initial = []
    for n in range(1, 101):
        impulse.append(sum(s * q**k * impulse[n - k] for k in range(1, n + 1)))
        # Exact infinite prehistory contribution, all initial differences one.
        initial.append(
            sum(s * q**k * initial[n - k - 1] for k in range(1, n))
            + theta * q ** (n - 1)
        )
    np.testing.assert_allclose(impulse[1:], s * q * root ** np.arange(100), rtol=2e-13)
    np.testing.assert_allclose(initial, theta * root ** np.arange(100), rtol=2e-13)
    tail = s * q * root**100 / (1 - root)
    assert sum(impulse) + tail == pytest.approx(1 / (1 - theta), rel=2e-13)


@pytest.mark.parametrize("burn_in", [0, 3, 70])
def test_initialization_closed_sums_match_each_increment_and_block(burn_in):
    alpha, theta, dimension, length, pairs = 0.2, 0.4, 3, 4, 7
    root = 1 - alpha * (1 - theta)
    norm = (dimension * (dimension + 2)) ** 0.25 / (1 - theta)

    def raw(m, count):
        value = 0.0
        for block in range(count):
            delta = sum(
                norm * theta * root ** (n - 1)
                for n in range(burn_in + block * m + 1, burn_in + (block + 1) * m + 1)
            )
            stationary = norm * min(m, np.pi / 2 * np.sqrt(m))
            value += 2 * stationary * delta + delta**2
        return value / (2 * dimension * m * count)

    expected = 2 * raw(2 * length, pairs) + raw(length, 2 * pairs)
    assert flat_start_error_coefficient(
        alpha, theta, dimension, length, pairs, burn_in
    ) == pytest.approx(expected, rel=3e-14)


def test_raw_square_expansion_and_two_length_weights():
    constants = {"dimension": 3, "z4": 2.0, "e4": 7.0, "linear_filter_l1": 1.3}
    length, eps = 5, 0.03
    direct = 0.0
    for m, weight in ((length, 1), (2 * length, 2)):
        w = (3 * 5) ** 0.25 * 1.3 * np.sqrt(m)
        z, e = m * 2.0, m * 7.0
        # Evaluate products separately, without subtracting nearly equal squares.
        direct += (
            weight
            * (
                2 * eps**6 * w * e
                + eps**6 * z * z
                + 2 * eps**8 * z * e
                + eps**10 * e * e
            )
            / (6 * m)
        )
    coefficients = estimator_error_coefficients(constants, length)
    assert coefficients @ np.array([eps**6, eps**8, eps**10]) == pytest.approx(direct)


def test_covariance_product_remainder_has_correct_cross_factors():
    constants = {"dW2": 2.0, "dZ2": 3.0, "dE2": 5.0}
    np.testing.assert_array_equal(
        transport_error_coefficients(constants), [14.5, 15, 12.5]
    )


@pytest.mark.parametrize("initial", [0.0, 1e-8, 0.1])
def test_sufficient_interval_and_failure_without_claiming_impossibility(initial):
    coefficients = np.array([2.0, 3.0, 5.0])
    result = sufficient_noise_interval(coefficients, initial, 0.2)
    assert result["nonempty"] == (result["epsilon_lower"] <= result["epsilon_upper"])
    if result["nonempty"]:
        lower = max(result["epsilon_lower"] ** 2, 1e-15)
        for t in np.geomspace(lower, result["epsilon_upper"] ** 2, 31):
            assert coefficients @ [t, t * t, t * t * t] + initial / t <= 0.2 * (
                1 + 1e-14
            )
    else:
        assert initial == 0.1


def test_error_budget_places_transport_outside_probability_factor():
    result = relative_error_budget(0.1, 0.02, 0.03, [2, 3, 4], [5, 6, 7], 0.0001, 0.04)
    estimator = 2 * 0.01 + 3 * 0.0001 + 4 * 0.000001
    transport = 5 * 0.01 + 6 * 0.0001 + 7 * 0.000001
    assert result["radius_about_leading_prediction"] == pytest.approx(
        0.02 + (0.03 + estimator + 0.01) / 0.2
    )
    assert result["radius_about_finite_noise_transport"] == pytest.approx(
        result["radius_about_leading_prediction"] + transport
    )


@pytest.mark.parametrize(
    "change",
    [
        {"eta": 1.0},
        {"repulsive_scale": 0},
        {"alpha": 1e-20},
        {"dimension": True},
        {"covariance": np.eye(2)},
        {"attraction": float("nan")},
        {"attraction": 0},
    ],
)
def test_remainder_rejects_invalid_or_out_of_scope_inputs(change):
    args = dict(
        alpha=0.2,
        horizon=3,
        eta=0.01,
        repulsion=1,
        attraction=35,
        repulsive_scale=1,
        attractive_scale=3,
        dimension=3,
    )
    args.update(change)
    with pytest.raises(ValueError):
        remainder_constants(**args)


@pytest.mark.parametrize("burn_in", [-1, True, 2.3])
def test_initialization_rejects_invalid_burn_in(burn_in):
    with pytest.raises(ValueError):
        flat_start_error_coefficient(0.1, 0.5, 3, 2, 3, burn_in)


@pytest.mark.parametrize(
    "coefficients,initial,allowance",
    [
        ([0, 1, 2], 0, 1),
        ([1, -1, 2], 0, 1),
        ([1, 2], 0, 1),
        ([1, 2, 3], -1, 1),
        ([1, 2, 3], 0, 0),
    ],
)
def test_interval_rejects_invalid_inputs(coefficients, initial, allowance):
    with pytest.raises(ValueError):
        sufficient_noise_interval(coefficients, initial, allowance)


def test_fixed_comparison_is_only_a_small_noise_real_arithmetic_diagnostic():
    result = audit_finite_noise_budget()
    interval = result["sufficient_noise_interval"]
    assert interval["nonempty"]
    assert interval["epsilon_upper"] == pytest.approx(4.4578170028e-6, rel=2e-9)
    assert interval["epsilon_lower"] == pytest.approx(1.4589508500e-12, rel=2e-9)
    assert result["Delta_D4"] == pytest.approx(-14.4185159350, rel=2e-10)
    for endpoint in ("lower_endpoint_budget", "upper_endpoint_budget"):
        assert result[endpoint]["radius_about_finite_noise_transport"] < 0.10
    assert (
        result["previously_proposed_noise_budget"][
            "radius_about_finite_noise_transport"
        ]
        > 10000
    )
    assert result["upper_endpoint_leading_contrast_relative_to_linear_diffusion"] < 1e-9
    assert "not empty-memory" in result["initialization"]
