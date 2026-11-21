"""Fixed annulus-residual checks of the nonlinear density reference."""

from math import pi, sqrt

import numpy as np
import pytest
from scipy.special import roots_hermite, roots_legendre


D0, WIDTH = 0.5, 0.6
D4 = D0 * WIDTH + D0**2 / 2
_HERMITE, _GAUSSIAN_WEIGHTS = roots_hermite(40)
_GAUSSIAN_WEIGHTS /= sqrt(pi)
_LEGENDRE, _LEGENDRE_WEIGHTS = roots_legendre(512)


def _probe(radius):
    return np.maximum(1 - (2 * radius - 3) ** 2, 0) ** 10


def _radial_heat(test, r, time):
    # Radial 3D heat flow equals 1D heat flow on the odd extension r*f(r), divided by r.
    shifted = r[:, None] + 2 * sqrt(time) * _HERMITE
    return (shifted * test(abs(shifted))) @ _GAUSSIAN_WEIGHTS / r


def _drift(r, power, amplitude):
    shifted = r[:, None] + 2 * sqrt(WIDTH) * _HERMITE
    values = amplitude * (4 + shifted**2) ** (-power / 2)
    # Differentiate the radial heat integral, not the tail limit for the drift.
    numerator_prime = values * (1 - power * shifted**2 / (4 + shifted**2))
    return (
        D0 * (numerator_prime - shifted * values / r[:, None]) @ _GAUSSIAN_WEIGHTS / r
    )


def _weak_residual(scale, power, amplitude):
    # Test the full bounded push and Gaussian kick, not a gradient expansion.
    length = 2.5 * scale
    r = scale / 2 + length * (_LEGENDRE + 1) / 2
    density_delta = amplitude * (4 + r**2) ** (-power / 2)

    def test(radius):
        return _probe(radius / scale)

    smoothed = _radial_heat(test, r, D0)
    pushed = _radial_heat(test, r + _drift(r, power, amplitude), D0)
    difference = density_delta * (smoothed - test(r)) + (1 + density_delta) * (
        pushed - smoothed
    )
    return 2 * pi * length * ((r**2 * difference) @ _LEGENDRE_WEIGHTS)


def _shell_integral(power):
    r = 1 + (_LEGENDRE + 1) / 2
    return 2 * pi * ((r ** (2 - power) * _probe(r)) @ _LEGENDRE_WEIGHTS)


@pytest.mark.parametrize("amplitude", [-0.8, 0.8])
def test_both_signs_of_inverse_radius_leave_the_same_leading_shell_deficit(amplitude):
    scale = 64
    residual = scale * _weak_residual(scale, 1, amplitude) / _shell_integral(4)
    assert residual == pytest.approx(-D0 * amplitude**2, rel=0.012)


@pytest.mark.parametrize("amplitude", [0.7, -1.1, -4 * D4 / D0])
def test_inverse_square_requires_a_negative_balance_coefficient(amplitude):
    scale = 64
    residual = scale**3 * _weak_residual(scale, 2, amplitude) / _shell_integral(6)
    expected = -24 * D4 * amplitude - 6 * D0 * amplitude**2
    assert residual == pytest.approx(expected, abs=0.16)


def test_inverse_square_balance_is_asymptotic_not_an_exact_prepared_equilibrium():
    amplitude = -4 * D4 / D0
    normalized = [
        scale**3 * _weak_residual(scale, 2, amplitude) for scale in (12, 24, 48)
    ]
    assert abs(normalized[0]) > abs(normalized[1]) > abs(normalized[2]) > 1e-4
