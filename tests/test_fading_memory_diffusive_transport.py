"""Exact bounded-feedback controls, not a sampled transport or trajectory test."""

import math

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.special import ndtr

from emergenz_knoten.kernels import double_gaussian_gradient


def _normal_density(z):
    return math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)


def _positive_variance_bound(epsilon, corrector):
    ratio = 2 * corrector / epsilon
    return (
        2
        * epsilon**2
        * ((1 + ratio**2) * ndtr(-ratio) - ratio * _normal_density(ratio))
    )


@pytest.mark.parametrize("corrector", [0, 0.35, 1.8])
def test_gaussian_tail_variance_bound_agrees_with_direct_quadrature(corrector):
    epsilon = 0.73
    threshold = 2 * corrector / epsilon
    value, _ = quad(
        lambda z: 2 * (epsilon * z - 2 * corrector) ** 2 * _normal_density(z),
        threshold,
        math.inf,
        epsabs=1e-15,
    )
    assert value > 0
    assert _positive_variance_bound(epsilon, corrector) == pytest.approx(
        value, rel=4e-10, abs=0
    )
    assert value <= epsilon**2 + 1e-15


@pytest.mark.parametrize("amplitude", [-0.75, 0, 0.75])
def test_correlation_sum_and_martingale_agree_for_bounded_sign_feedback(amplitude):
    # v_next = amplitude * sign(v_now) + epsilon * Z, not a native Gaussian force.
    epsilon = 0.8
    sign_eigenvalue = 2 * ndtr(amplitude / epsilon) - 1
    corrector = amplitude / (1 - sign_eigenvalue)
    absolute_increment = 2 * epsilon * _normal_density(amplitude / epsilon)
    absolute_increment += amplitude * sign_eigenvalue
    covariance = amplitude**2 + epsilon**2 + 2 * corrector * absolute_increment

    def moment(order):
        # The previous sign can be held positive by reflection invariance.
        threshold = -amplitude / epsilon
        return sum(
            quad(
                lambda z: (
                    (amplitude + epsilon * z + corrector * (sign - 1)) ** order
                    * _normal_density(z)
                ),
                lower,
                upper,
                epsabs=1e-13,
            )[0]
            for sign, lower, upper in (
                (-1, -math.inf, threshold),
                (1, threshold, math.inf),
            )
        )

    assert moment(1) == pytest.approx(0, abs=4e-15)
    assert moment(2) == pytest.approx(covariance, abs=5e-15)
    assert covariance >= _positive_variance_bound(epsilon, abs(corrector)) - 1e-15
    if amplitude < 0:
        assert 0 < covariance < epsilon**2
    elif amplitude > 0:
        assert covariance > epsilon**2
    else:
        assert covariance == epsilon**2


@pytest.mark.parametrize("amplitude", [-0.75, 0, 0.75])
def test_constant_input_response_matches_gaussian_innovation_weight(amplitude):
    epsilon = 0.8
    eigenvalue = 2 * ndtr(amplitude / epsilon) - 1
    corrector = amplitude / (1 - eigenvalue)

    def average_increment(bias):
        plus, minus = (
            ndtr((bias + amplitude) / epsilon),
            ndtr((bias - amplitude) / epsilon),
        )
        positive_sign = minus / (1 - plus + minus)
        return bias + amplitude * (2 * positive_sign - 1)

    expected = 1 + 2 * corrector * _normal_density(amplitude / epsilon) / epsilon
    delta = 1e-5
    slope = (average_increment(delta) - average_increment(-delta)) / (2 * delta)
    assert slope == pytest.approx(expected, abs=3e-10)

    threshold = -amplitude / epsilon
    cross = sum(
        quad(
            lambda z: (
                (amplitude + epsilon * z + corrector * (sign - 1))
                * (epsilon * z)
                * _normal_density(z)
            ),
            lower,
            upper,
            epsabs=1e-13,
        )[0]
        for sign, lower, upper in (
            (-1, -math.inf, threshold),
            (1, threshold, math.inf),
        )
    )
    assert cross / epsilon**2 == pytest.approx(expected, abs=2e-14)
    abs_step = (
        2 * epsilon * _normal_density(amplitude / epsilon) + amplitude * eigenvalue
    )
    covariance = amplitude**2 + epsilon**2 + 2 * corrector * abs_step
    assert covariance >= epsilon**2 * expected**2 - 1e-15


@pytest.mark.parametrize("dimension", [1, 3, 4])
def test_native_weak_response_uses_the_exact_radial_gaussian_moment(dimension):
    epsilon, sigma = 0.62, 1.16
    probe = np.linspace(0.25, 0.6, dimension)
    gradient = double_gaussian_gradient(
        np.zeros(dimension),
        np.vstack([np.zeros(dimension), -probe]),
        np.array([0.7, 0.3]),
        amplitude_rep=0,
        amplitude_att=1,
        sigma_rep=sigma,
        sigma_att=sigma,
    )
    np.testing.assert_allclose(
        -(sigma**2) * gradient / 0.3,
        -probe * np.exp(-(probe @ probe) / (2 * sigma**2)),
        atol=2e-16,
    )

    def moment(power):
        return quad(
            lambda z: (
                (epsilon * z) ** power
                * math.exp(-((epsilon * z / sigma) ** 2) / 2)
                * _normal_density(z)
            ),
            -math.inf,
            math.inf,
            epsabs=1e-13,
        )[0]

    coefficient = -moment(2) * moment(0) ** (dimension - 1)
    assert coefficient < 0
    assert coefficient == pytest.approx(
        -(epsilon**2) * (1 + (epsilon / sigma) ** 2) ** (-dimension / 2 - 1),
        rel=2e-14,
    )


def test_scalar_gaussian_two_place_cycle_is_not_reversible():
    amplitude, sigma, epsilon = 0.1, 1.16, 0.62
    y, z = 0.4, 0.9

    def log_kernel(new, old):
        drift = -amplitude * old * math.exp(-((old / sigma) ** 2) / 2)
        return -(((new - drift) / epsilon) ** 2) / 2

    change = (
        log_kernel(y, 0)
        + log_kernel(z, y)
        + log_kernel(0, z)
        - log_kernel(z, 0)
        - log_kernel(y, z)
        - log_kernel(0, y)
    )
    expected = (
        amplitude
        * y
        * z
        / epsilon**2
        * (math.exp(-((z / sigma) ** 2) / 2) - math.exp(-((y / sigma) ** 2) / 2))
    )
    assert change == pytest.approx(expected, abs=1e-15)
    assert expected < 0
