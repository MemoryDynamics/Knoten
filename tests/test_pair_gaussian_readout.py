"""Quadrature and finite Gaussian moment controls; no sampled target paths."""

from decimal import Decimal, localcontext
from itertools import product

import numpy as np
import pytest
from scipy.special import roots_hermitenorm

from emergenz_knoten.kernels import ScalarReadoutKernel
from emergenz_knoten.pair_gaussian_readout import (
    isotropic_gaussian_contrast,
    linear_gaussian_moments,
    linear_gaussian_pair_readout,
)


KERNEL = ScalarReadoutKernel(
    sigma_rep=1, sigma_att=3, amplitude_rep=1, amplitude_att=35
)


def _quadrature(mean, variance):
    nodes, weights = roots_hermitenorm(24)
    indices = np.array(list(product(range(len(nodes)), repeat=len(mean))))
    z = mean + np.sqrt(variance) * nodes[indices]
    w = np.prod(weights[indices] / np.sqrt(2 * np.pi), axis=1)
    r2 = np.sum(z**2, axis=1)
    gradient = (-np.exp(-r2 / 2) + 35 / 9 * np.exp(-r2 / 18))[:, None] * z
    return w @ gradient


@pytest.mark.parametrize(
    "mean,joint,independent",
    [([0.4], 0.2, 0.4), ([0.1, -0.2], 0.04, 0.07), ([0.2, -0.1, 0.03], 0.02, 0.01)],
)
def test_full_gaussian_integral_and_cubic_bound_against_quadrature(
    mean, joint, independent
):
    mean = np.array(mean)
    result = isotropic_gaussian_contrast(mean, joint, independent, KERNEL)
    explicit = _quadrature(mean, joint) - _quadrature(mean, independent)
    np.testing.assert_allclose(result["exact"], explicit, rtol=1e-10, atol=3e-14)
    assert (
        np.linalg.norm(result["exact"] - result["cubic"]) <= result["cubic_error_bound"]
    )


def test_tiny_covariance_contrast_agrees_with_80_digit_direct_difference():
    mean, joint, independent = np.array([0.000529, 0.0, 0.0]), 2.774e-8, 2.776e-8
    result = isotropic_gaussian_contrast(mean, joint, independent, KERNEL)
    with localcontext() as context:
        context.prec = 80
        m = Decimal.from_float(float(mean[0]))
        values = []
        for value in (joint, independent):
            variance = Decimal.from_float(value)
            total = Decimal(0)
            for amplitude, sigma in ((1, 1), (-35, 3)):
                width = Decimal(sigma) ** 2
                log_factor = -Decimal("2.5") * (1 + variance / width).ln() - m * m / (
                    2 * (width + variance)
                )
                total -= Decimal(amplitude) / width * log_factor.exp() * m
            values.append(total)
        exact = float(values[0] - values[1])
    assert result["exact"][0] == pytest.approx(exact, rel=2e-13, abs=1e-28)
    assert (
        np.linalg.norm(result["exact"] - result["cubic"]) < result["cubic_error_bound"]
    )


def test_zero_mean_blindness_does_not_imply_equal_variances_or_independence():
    # Two equal-variance correlated normals have unequal joint/product
    # difference variances, but any centered Gaussian has zero odd readout.
    result = isotropic_gaussian_contrast(np.zeros(3), 0.02, 0.08, KERNEL)
    np.testing.assert_array_equal(result["exact"], np.zeros(3))
    np.testing.assert_array_equal(result["cubic"], np.zeros(3))
    same = isotropic_gaussian_contrast([0.2, 0.1], 0.08, 0.08, KERNEL)
    np.testing.assert_array_equal(same["exact"], np.zeros(2))


def test_covariance_exchange_and_reflection_reverse_contrast():
    mean = np.array([[0.01, 0.02], [-0.1, 0.3]])
    result = isotropic_gaussian_contrast(mean, [0.01, 0.02], [0.02, 0.01], KERNEL)
    swapped = isotropic_gaussian_contrast(mean, [0.02, 0.01], [0.01, 0.02], KERNEL)
    reflected = isotropic_gaussian_contrast(-mean, [0.01, 0.02], [0.02, 0.01], KERNEL)
    np.testing.assert_allclose(swapped["exact"], -result["exact"], rtol=1e-14)
    np.testing.assert_allclose(reflected["exact"], -result["exact"], rtol=1e-14)


def _parameters():
    return dict(
        alpha=0.2,
        self_gain=0.2,
        cross_gain=0.04,
        epsilon=0.01,
        points=np.array([[0.02, -0.01], [-0.03, 0.04]]),
        centers=np.array([[0.01, 0.0], [-0.01, 0.02]]),
    )


def _three_state(parameters, length):
    alpha, g, h, epsilon = [
        parameters[key] for key in ("alpha", "self_gain", "cross_gain", "epsilon")
    ]
    q, s = 1 - alpha, 1 - g - h
    transition = np.array(
        [[q * s, 0, 0], [0, s, g - h], [0, alpha * s, q + alpha * (g - h)]]
    )
    # Node noise enters common V and relative (D,E) with opposite signs.
    drive = epsilon * np.array([[q / 2, q / 2], [1, -1], [alpha, -alpha]])
    points, centers = parameters["points"], parameters["centers"]
    mean = np.array(
        [
            points.mean(axis=0) - centers.mean(axis=0),
            points[0] - points[1],
            centers[0] - centers[1],
        ]
    )
    means, covariances = [mean], [np.zeros((3, 3))]
    for _ in range(length - 1):
        means.append(transition @ means[-1])
        covariances.append(
            transition @ covariances[-1] @ transition.T + drive @ drive.T
        )
    return transition, np.array(means), np.array(covariances)


def test_finite_start_moments_against_full_three_state_covariance_recursion():
    parameters = _parameters()
    result = linear_gaussian_moments(**parameters, length=10)
    transition, means, covariance = _three_state(parameters, 10)
    output = np.array([[1, 0.5, -0.5], [1, -0.5, 0.5]])
    np.testing.assert_allclose(
        result["inner_means"], output @ means, rtol=1e-13, atol=1e-17
    )
    np.testing.assert_allclose(
        result["inner_variance"],
        np.einsum("i,nij,j->n", output[0], covariance, output[0]),
        rtol=1e-12,
        atol=1e-19,
    )
    e = np.array([1, -1])
    for n in range(3, 10):
        for lag in range(3):
            cross = (
                result["common_powers"][lag] * result["common_variance"][n - lag]
                - e
                @ result["powers"][lag]
                @ result["relative_covariance"][n - lag]
                @ e
                / 4
            )
            explicit = (
                output[0]
                @ np.linalg.matrix_power(transition, lag)
                @ covariance[n - lag]
                @ output[1]
            )
            assert cross == pytest.approx(explicit, rel=1e-11, abs=1e-19)


def test_complete_small_window_against_three_state_moments_and_quadrature():
    parameters, length = _parameters(), 7
    r, weights = np.array([0.04, -0.01]), np.array([0.5, 0.3, 0.2])
    result = linear_gaussian_pair_readout(
        **parameters, separation=r, weights=weights, start=3, stop=length, kernel=KERNEL
    )
    transition, means, covariance = _three_state(parameters, length)
    output = np.array([[1, 0.5, -0.5], [1, -0.5, 0.5]])
    explicit = np.zeros((2, 2))
    for n in range(3, length):
        for lag, weight in enumerate(weights):
            k = n - lag
            for target, source, sign in ((0, 1, 1), (1, 0, -1)):
                mean = sign * r + output[target] @ means[n] - output[source] @ means[k]
                product_var = (
                    output[target] @ covariance[n] @ output[target]
                    + output[source] @ covariance[k] @ output[source]
                )
                cross = (
                    output[target]
                    @ np.linalg.matrix_power(transition, lag)
                    @ covariance[k]
                    @ output[source]
                )
                explicit[target] += (
                    weight
                    * (
                        _quadrature(mean, product_var - 2 * cross)
                        - _quadrature(mean, product_var)
                    )
                    / (length - 3)
                )
    np.testing.assert_allclose(
        result["exact_gradient_contrast"], explicit, rtol=2e-8, atol=3e-16
    )
    difference = np.linalg.norm(
        np.array(result["exact_gradient_contrast"]) - result["cubic_gradient_contrast"],
        axis=1,
    )
    assert np.all(difference <= result["cubic_error_bound"])


def test_deterministic_common_trend_has_no_replica_contrast():
    result = linear_gaussian_pair_readout(
        **(_parameters() | {"epsilon": 0}),
        separation=[0.1, 0.2],
        weights=[0.5, 0.3, 0.2],
        start=3,
        stop=7,
        kernel=KERNEL,
    )
    np.testing.assert_array_equal(result["exact_gradient_contrast"], np.zeros((2, 2)))


@pytest.mark.parametrize("joint,product", [(-1, 1), (0, np.nan), (np.inf, 0)])
def test_invalid_variance_rejected(joint, product):
    with pytest.raises(ValueError):
        isotropic_gaussian_contrast([0.1], joint, product, KERNEL)


@pytest.mark.parametrize(
    "change",
    [
        {"alpha": 0},
        {"cross_gain": 0},
        {"self_gain": 2},
        {"epsilon": -1},
        {"length": True},
    ],
)
def test_invalid_comparison_rejected(change):
    with pytest.raises(ValueError):
        linear_gaussian_moments(**(_parameters() | {"length": 10} | change))
