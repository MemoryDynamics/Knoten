"""Deterministic checks of paired-reference algebra, not production evidence."""

from itertools import product

import numpy as np
from numpy.polynomial.hermite_e import hermegauss
import pytest

from paired_transport import (
    audit_paired_reference,
    cubic_force_covariance_sum,
    exponential_cubic_tail_bound,
    exponential_two_length_bias_bounds,
    paired_long_block_reference,
)
from weak_nonlinearity import (
    covariance_response,
    exponential_weights,
    lag_matrix,
    stationary_msd_response,
    transport_response,
)


@pytest.mark.parametrize("dimension", [1, 2, 3])
@pytest.mark.parametrize("correlation", [-0.6, 0.0, 0.7])
def test_wick_cubic_covariance_by_exact_gauss_hermite_quadrature(
    dimension, correlation
):
    nodes, weights = hermegauss(4)
    weights /= np.sqrt(2 * np.pi)
    indices = np.array(list(product(range(4), repeat=2 * dimension)))
    probability = weights[indices].prod(axis=1)
    x = np.sqrt(1.7) * nodes[indices[:, :dimension]]
    y = np.sqrt(0.8) * (
        correlation * nodes[indices[:, :dimension]]
        + np.sqrt(1 - correlation**2) * nodes[indices[:, dimension:]]
    )
    tx = x * (np.sum(x**2, axis=1) - (dimension + 2) * 1.7)[:, None]
    ty = y * (np.sum(y**2, axis=1) - (dimension + 2) * 0.8)[:, None]
    actual = tx.T @ (probability[:, None] * ty)
    cross = correlation * np.sqrt(1.7 * 0.8)
    np.testing.assert_allclose(
        actual, 2 * (dimension + 2) * cross**3 * np.eye(dimension), atol=1e-12
    )
    np.testing.assert_allclose(x.T @ (probability[:, None] * ty), 0, atol=1e-13)


@pytest.mark.parametrize("gain", [0.0, 0.2, 0.7])
@pytest.mark.parametrize("dimension", [1, 3])
def test_h2_cubic_spectrum_matches_signed_geometric_series(gain, dimension):
    weights = exponential_weights(0.4, 2)
    covariance, _, _ = covariance_response(weights, gain, dimension)
    root = -gain * weights[1]
    variance = 1 / (1 - root**2)
    exact = 2 * (dimension + 2) * weights[1] ** 2 * variance**3
    exact *= (1 + root**3) / (1 - root**3)
    actual = cubic_force_covariance_sum(weights, gain, covariance, dimension, 40)
    assert actual == pytest.approx(exact, rel=2e-13)


def test_cubic_covariance_recursion_matches_direct_matrix_powers():
    weights, gain, dimension, maximum = exponential_weights(0.25, 6), 0.17, 3, 9
    covariance, _, _ = covariance_response(weights, gain, dimension)
    matrix = lag_matrix(weights, gain)
    pair_weights = np.outer(weights[1:], weights[1:])
    expected = np.sum(pair_weights * covariance**3)
    for time in range(1, maximum + 1):
        cross = np.linalg.matrix_power(matrix, time) @ covariance
        expected += 2 * np.sum(pair_weights * cross**3)
    expected *= 2 * (dimension + 2)
    assert cubic_force_covariance_sum(
        weights, gain, covariance, dimension, maximum
    ) == pytest.approx(expected)


@pytest.mark.parametrize("bare_gain", [0.0, 0.08, 0.2])
def test_canonical_cubic_tail_encloses_a_longer_sum(bare_gain):
    alpha, horizon, dimension = 0.3, 7, 3
    weights = exponential_weights(alpha, horizon)
    gain = (1 - (1 - alpha) ** horizon) * bare_gain
    covariance, _, _ = covariance_response(weights, gain, dimension)
    short = cubic_force_covariance_sum(weights, gain, covariance, dimension, horizon)
    long = cubic_force_covariance_sum(weights, gain, covariance, dimension, 150)
    bound = exponential_cubic_tail_bound(alpha, bare_gain, horizon, dimension, horizon)
    assert abs(long - short) <= bound + 1e-12


@pytest.mark.parametrize("length", [1, 10, 100])
@pytest.mark.parametrize("bare_gain", [0.0, 0.08, 0.2])
def test_two_length_coefficient_bounds_enclose_exact_bias(length, bare_gain):
    alpha, horizon, dimension = 0.3, 7, 3
    weights = exponential_weights(alpha, horizon)
    gain = (1 - (1 - alpha) ** horizon) * bare_gain
    covariance, _, perturbation = covariance_response(weights, gain, dimension)
    limits = np.array(transport_response(weights, gain, perturbation))
    msd, response = stationary_msd_response(
        weights, gain, np.array([length, 2 * length]), dimension
    )
    actual = np.array([np.diff(msd)[0], np.diff(response)[0]]) / (
        2 * dimension * length
    )
    bounds = exponential_two_length_bias_bounds(
        alpha, bare_gain, horizon, dimension, length, covariance
    )
    assert abs(actual[0] - limits[0]) <= bounds["linear_absolute_bias_bound"] + 1e-12
    assert (
        abs(actual[1] - limits[1])
        <= bounds["quartic_per_beta_absolute_bias_bound"] + 1e-11
    )


@pytest.mark.parametrize("dimension", [1, 3])
def test_long_block_cross_covariance_matches_independent_transport_response(dimension):
    weights, gain = exponential_weights(0.2, 9), 0.17
    covariance, _, perturbation = covariance_response(weights, gain, dimension)
    linear, derivative = transport_response(weights, gain, perturbation)
    spectrum = cubic_force_covariance_sum(weights, gain, covariance, dimension, 100)
    result = paired_long_block_reference(weights, gain, covariance, dimension, spectrum)
    assert result["linear_zero_frequency_variance"] == pytest.approx(2 * linear)
    assert result["linear_cubic_zero_frequency_covariance"] == pytest.approx(derivative)
    assert result["raw_relative_variance_times_d_S_M"] > 2


@pytest.mark.parametrize("dimension", [1, 3])
def test_nested_two_length_variance_factor_by_gaussian_quadratic_form(dimension):
    # Independent limiting blocks with a nontrivial W--Z correlation.
    v_w, v_z, cross = 0.7, 1.8, -0.6
    single_covariance = np.array([[v_w, cross], [cross, v_z]])
    covariance = np.kron(np.eye(2 * dimension), single_covariance)
    raw = np.zeros_like(covariance)
    corrected = np.zeros_like(covariance)
    for coordinate in range(dimension):
        w1, z1 = 2 * coordinate, 2 * coordinate + 1
        w2, z2 = 2 * (coordinate + dimension), 2 * (coordinate + dimension) + 1
        for w, z in [(w1, z1), (w2, z2)]:
            raw[w, z] = raw[z, w] = 1 / (4 * dimension)
            corrected[w, z] = corrected[z, w] = 1 / (4 * dimension)
        for w, z in [(w1, z2), (w2, z1)]:
            corrected[w, z] = corrected[z, w] = 1 / (2 * dimension)
    assert np.trace(raw @ covariance) == pytest.approx(cross)
    assert np.trace(corrected @ covariance) == pytest.approx(cross)
    raw_variance = 2 * np.trace(raw @ covariance @ raw @ covariance)
    corrected_variance = 2 * np.trace(corrected @ covariance @ corrected @ covariance)
    assert raw_variance == pytest.approx((v_w * v_z + cross**2) / (2 * dimension))
    assert corrected_variance == pytest.approx(5 * raw_variance)


@pytest.mark.parametrize("root", [-0.5, 0.4])
@pytest.mark.parametrize("length", [1, 7])
def test_two_length_bias_identity_retains_signed_covariances(root, length):
    covariances = root ** np.arange(400) / (1 - root**2)

    def block_mean(size):
        ages = np.arange(1, size)
        return covariances[0] / 2 + (1 - ages / size) @ covariances[1:size]

    limit = 0.5 / (1 - root) ** 2
    ages = np.arange(1, len(covariances))
    exact_bias = -np.clip((ages - length) / length, 0, 1) @ covariances[1:]
    assert 2 * block_mean(2 * length) - block_mean(length) - limit == pytest.approx(
        exact_bias, abs=1e-14
    )


def test_finite_gaussian_cubic_products_do_not_have_independent_coordinates():
    nodes, weights = hermegauss(5)
    weights /= np.sqrt(2 * np.pi)
    x, y = np.meshgrid(nodes, nodes)
    probability = np.outer(weights, weights)
    first, second = x**2 * (x**2 + y**2), y**2 * (x**2 + y**2)
    covariance = np.sum(probability * first * second)
    covariance -= np.sum(probability * first) * np.sum(probability * second)
    assert covariance == pytest.approx(32.0)


def test_fixed_review_cell_has_separate_bias_and_long_block_precision_records():
    result = audit_paired_reference()
    old, longer = result["lag_diagnostics"]
    assert old["raw_quartic_relative_bias"] == pytest.approx(-0.6466784436)
    assert old["two_length_quartic_relative_bias"] == pytest.approx(-0.2149456454)
    assert abs(longer["two_length_quartic_relative_bias"]) < 1e-6
    assert abs(longer["two_length_linear_relative_bias"]) < 1e-6
    assert result["cubic_force_spectrum_partial_sum"] == pytest.approx(
        402678296.5606201, rel=1e-9
    )
    assert result["cubic_force_spectrum_omitted_absolute_bound"] < 3e-12
    reference = result["long_block_reference"]
    assert reference["extra_relative_variance_from_third_chaos"] == pytest.approx(
        0.1465419576071239
    )
    assert reference["linear_cubic_zero_frequency_covariance"] == pytest.approx(
        result["finite_D4_per_unit_beta"]
    )


@pytest.mark.parametrize(
    "dimension,maximum", [(True, 8), (1.5, 8), (0, 8), (3, -1), (3, 1.2)]
)
def test_invalid_cubic_counts_fail_closed(dimension, maximum):
    weights = exponential_weights(0.3, 5)
    covariance, _, _ = covariance_response(weights, 0.1, 3)
    with pytest.raises(ValueError):
        cubic_force_covariance_sum(weights, 0.1, covariance, dimension, maximum)


def test_wrong_covariance_and_uncontrolled_tail_fail_closed():
    weights = exponential_weights(0.3, 5)
    covariance, _, _ = covariance_response(weights, 0.1, 3)
    with pytest.raises(ValueError, match="Lyapunov"):
        cubic_force_covariance_sum(weights, 0.1, 2 * covariance, 3, 10)
    with pytest.raises(ValueError, match="maximum_lag"):
        exponential_cubic_tail_bound(0.3, 0.1, 5, 3, 2)
    with pytest.raises(ValueError, match="summable"):
        exponential_cubic_tail_bound(0.3, 0.8, 5, 3, 10)
    with pytest.raises(ValueError, match="nonnegative"):
        paired_long_block_reference(weights, 0.1, covariance, 3, -1)
