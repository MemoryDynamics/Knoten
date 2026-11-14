"""Independent finite-block covariance and bound checks; no target sampling."""

from itertools import product

import numpy as np
from numpy.polynomial.hermite_e import hermegauss
import pytest
from scipy.linalg import solve_discrete_lyapunov, toeplitz

from finite_block_transport import (
    audit_finite_block_reference,
    filtered_block_variance_bounds,
    finite_block_reference_bound,
    stationary_average_variance_bound,
)
from paired_transport import cubic_force_covariances
from weak_nonlinearity import covariance_response, exponential_weights


def _state_block_variance(matrix, covariance, component, length):
    value = length * covariance[component, component]
    for age in range(1, length):
        value += (
            2
            * (length - age)
            * (np.linalg.matrix_power(matrix, age) @ covariance)[component, component]
        )
    return value


@pytest.mark.parametrize("root", [-0.4, 0.0, 0.6])
@pytest.mark.parametrize("length", [1, 4])
def test_filtered_variance_matches_full_toeplitz_quadratic_form(root, length):
    impulse = np.array([1.0, -0.3, 0.1])
    block_filter = np.convolve(np.ones(length), impulse)
    forcing = root ** np.arange(len(block_filter)) / (1 - root**2)
    total = forcing[0] * (1 + abs(root)) / (1 - abs(root))
    result = filtered_block_variance_bounds(forcing, impulse, length, 0.0, total)
    exact = block_filter @ toeplitz(forcing) @ block_filter
    assert result["variance_lower"] == pytest.approx(exact)
    assert result["variance_upper"] == pytest.approx(exact)


@pytest.mark.parametrize("gain", [0.0, 0.2, 0.7])
def test_h2_first_and_third_force_covariances_have_distinct_ar_rates(gain):
    weights, dimension = exponential_weights(0.4, 2), 3
    covariance, _, _ = covariance_response(weights, gain, dimension)
    root = -gain * weights[1]
    first, third = cubic_force_covariances(weights, gain, covariance, dimension, 20)
    times = np.arange(21)
    variance = 1 / (1 - root**2)
    np.testing.assert_allclose(
        first,
        (dimension + 2) ** 2 * weights[1] ** 2 * variance**3 * root**times,
        atol=1e-14,
    )
    np.testing.assert_allclose(
        third,
        2 * (dimension + 2) * weights[1] ** 2 * variance**3 * root ** (3 * times),
        atol=1e-14,
    )


@pytest.mark.parametrize("bare_gain", [0.0, 0.1, 0.25])
@pytest.mark.parametrize("length", [1, 4, 11])
def test_h2_filtered_chaos_bounds_enclose_independent_two_state_solution(
    bare_gain, length
):
    alpha, dimension, horizon = 0.4, 3, 2
    weights = exponential_weights(alpha, horizon)
    mass = 1 - (1 - alpha) ** horizon
    root = -mass * bare_gain * weights[1]
    variance = 1 / (1 - root**2)
    first_matrix = np.array(
        [[root, 0], [-(dimension + 2) * weights[1] * variance, root]]
    )
    first_covariance = solve_discrete_lyapunov(first_matrix, np.diag([1.0, 0.0]))
    force_variance = 2 * (dimension + 2) * weights[1] ** 2 * variance**3
    third_matrix = np.array([[root**3, 0], [1.0, root]])
    third_covariance = solve_discrete_lyapunov(
        third_matrix, np.diag([force_variance * (1 - root**6), 0.0])
    )
    result = finite_block_reference_bound(
        alpha, horizon, bare_gain, dimension, length, 5, 10, 2
    )
    for label, matrix, cov in [
        ("first_chaos_block_variance", first_matrix, first_covariance),
        ("third_chaos_block_variance", third_matrix, third_covariance),
    ]:
        exact = _state_block_variance(matrix, cov, 1, length)
        assert result[label]["variance_lower"] <= exact + 1e-12
        assert result[label]["variance_upper"] >= exact - 1e-12
    tighter = finite_block_reference_bound(
        alpha, horizon, bare_gain, dimension, length, 100, 10, 2
    )
    assert (
        tighter["first_chaos_block_variance"]["variance_upper"]
        <= result["first_chaos_block_variance"]["variance_upper"] + 1e-12
    )
    assert (
        tighter["third_chaos_block_variance"]["variance_upper"]
        <= result["third_chaos_block_variance"]["variance_upper"] + 1e-12
    )


def test_finite_superblock_gaussian_polynomial_differs_from_long_block_variance():
    nodes, weights = hermegauss(5)
    weights /= np.sqrt(2 * np.pi)
    indices = np.array(list(product(range(5), repeat=5)))
    probability = weights[indices].prod(axis=1)
    x = nodes[indices]

    def statistic(offset):
        past, first, second = x[:, offset : offset + 3].T
        return (
            -(first * past**3 + second * first**3 + 2 * first**4 + 2 * second * past**3)
            / 2
        )

    first, second = statistic(0), statistic(2)
    mean = probability @ first
    variance = probability @ (first - mean) ** 2
    adjacent_covariance = probability @ ((first - mean) * (second - mean))
    assert mean == pytest.approx(-3)
    assert variance == pytest.approx(118.5)
    assert adjacent_covariance == pytest.approx(0, abs=1e-12)
    # The long-block variance for this unit-weight response would be only 60.
    assert variance > 1.9 * 60
    alpha, horizon = 0.4, 2
    weight = exponential_weights(alpha, horizon)[1]
    result = finite_block_reference_bound(alpha, horizon, 0.0, 1, 1, 5, 7, 2)
    exact_average_variance = 118.5 * weight**2 / (7 * 2)
    assert result["sample_mean_variance_bound"] >= exact_average_variance
    assert result["remote_superblock_coupling_sum_bound"] == 0


@pytest.mark.parametrize("blocks", [1, 2, 5, 100])
def test_covariance_assembly_matches_finite_sample_weights(blocks):
    second_moment, mean, tail, near, seeds = 10.0, 2.0, 3.0, 2, 5
    variance = second_moment - mean**2
    expected = variance
    for lag in range(1, min(near, blocks - 1) + 1):
        expected += 2 * (1 - lag / blocks) * variance
    if blocks > near + 1:
        expected += 2 * np.sqrt(variance) * tail
    expected /= seeds * blocks
    assert stationary_average_variance_bound(
        second_moment, mean, tail, near, blocks, seeds
    ) == pytest.approx(expected)


def test_fixed_cell_finite_bound_is_not_the_long_block_power_formula():
    result = audit_finite_block_reference()
    assert result["nearby_covariances_bounded_without_decay"] == 1
    assert result["implied_steps_per_seed"] == 400_000_000
    assert result["remote_superblock_coupling_sum_bound"] == pytest.approx(
        3.78373751534, rel=1e-9
    )
    assert result[
        "relative_sampling_sd_bound_against_long_time_coefficient"
    ] == pytest.approx(0.01820303909786, rel=1e-9)
    assert result["relative_chebyshev_95_radius_about_finite_mean"] < 0.082
    assert result["omitted_filter_l1_bound"] < 1.8e-8
    bias = result["coefficient_bias_bounds"][
        "quartic_per_beta_absolute_bias_bound"
    ] / abs(result["long_time_mean_per_beta"])
    assert result["relative_chebyshev_95_radius_about_finite_mean"] + bias < 0.088


@pytest.mark.parametrize("horizon,length", [(2, 1), (2, 5), (7, 1), (7, 5)])
def test_remote_coupling_closed_sum_matches_explicit_history_and_block_sums(
    horizon, length
):
    alpha, bare_gain, dimension = 0.4, 0.2, 2
    q, k = 1 - alpha, horizon - 1
    b = q * bare_gain
    root = q + b
    weights = exponential_weights(alpha, horizon)
    covariance, _, _ = covariance_response(
        weights, (1 - q**horizon) * bare_gain, dimension
    )
    variances = np.diag(covariance)
    ages = np.arange(1, horizon)
    m4 = (dimension * (dimension + 2)) ** 0.25
    m12_cubed = np.prod(dimension + 2.0 * np.arange(6)) ** 0.25
    old_force = 2 * m12_cubed * (weights[1:] @ variances**1.5)

    def impulse(age):
        return 1.0 if age == 0 else b * root ** (age - 1)

    def force_difference(time):
        lag_differences = (
            b
            * np.sqrt(2 / (1 - root**2))
            * root ** (time - ages)
            * (1 - root**ages)
            / (1 - root)
        )
        return 3 * m12_cubed * (weights[1:] @ (variances * lag_differences))

    result = finite_block_reference_bound(
        alpha, horizon, bare_gain, dimension, length, 30, 20, 2
    )
    w4 = m4 * np.sqrt(result["linear_block_variance"])
    z4 = m4 * np.sqrt(result["first_chaos_block_variance"]["variance_upper"])
    z4 += (
        np.sqrt(dimension)
        * 3**1.5
        * np.sqrt(result["third_chaos_block_variance"]["variance_upper"])
    )
    near = result["nearby_covariances_bounded_without_decay"]
    total = 0.0
    for lag in range(near + 1, near + 30):
        w_difference = z_difference = 0.0
        for time in range(2 * (lag - 1) * length + 1, 2 * lag * length + 1):
            w_difference += m4 * b * np.sqrt(2 / (1 - root**2)) * root ** (time - 1)
            newest = time - 1 - k
            z_difference += sum(
                impulse(age) * force_difference(time - 1 - age)
                for age in range(newest + 1)
            )
            z_difference += old_force * b * root**newest / (1 - root)
        total += 3 * (z4 * w_difference + w4 * z_difference) / (2 * dimension * length)
    assert result["remote_superblock_coupling_sum_bound"] == pytest.approx(
        total, rel=2e-7
    )


@pytest.mark.parametrize(
    "forcing,impulse,length,tail,total",
    [
        ([1.0], [1, 0.2], 3, 0, 1),
        ([1, 0], [1], 1.5, 0, 1),
        ([1, 0], [1], 1, -1, 1),
        ([1, 0.5], [1], 1, 0, 1),
        ([1, np.nan], [1], 1, 0, 2),
    ],
)
def test_invalid_filtered_bounds_fail_closed(forcing, impulse, length, tail, total):
    with pytest.raises(ValueError):
        filtered_block_variance_bounds(forcing, impulse, length, tail, total)


def test_invalid_sampling_and_canonical_domains_fail_closed():
    with pytest.raises(ValueError):
        stationary_average_variance_bound(1, 2, 0, 1, 5, 2)
    with pytest.raises(ValueError):
        stationary_average_variance_bound(10, 2, -1, 1, 5, 2)
    with pytest.raises(ValueError):
        finite_block_reference_bound(0.3, 10, 0.1, 3, 1, 1, 5, 2)
    with pytest.raises(ValueError):
        finite_block_reference_bound(0.3, 5, 0.8, 3, 10, 10, 5, 2)
