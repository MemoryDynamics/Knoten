"""Exact bounded-feedback controls, not a sampled transport or trajectory test."""

import math

import pytest
from scipy.integrate import quad
from scipy.special import ndtr


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
