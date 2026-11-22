"""Fixed response integrals for a homogeneous comparison, not native runs."""

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import roots_legendre


EPSILON = 0.8
SIGMA = 0.7
B0 = -(EPSILON**2) / 2
AGES = np.array([2 / 3, 1 / 3])
MEAN_AGE = AGES[1]
L0 = 2 * np.sqrt(2 / np.pi) / 3


def _ratio(x):
    return (
        np.sqrt(2 / np.pi)
        * quad(lambda v: (1 - v**2) * np.exp(-(x**2) * v**2 / 2), 0, 1)[0]
    )


def _polar_speed(beta):
    return EPSILON * brentq(lambda x: beta * _ratio(x) / L0 - 1, 0, beta / L0)


def _shifted_gaussian_moments(speed, k):
    direction, angle_weights = roots_legendre(48)
    nodes, radial_weights = roots_legendre(72)
    r = 5 * (nodes[:, None] + 1)
    axial = EPSILON * r * direction
    measure = (
        5 * radial_weights[:, None] * angle_weights * np.sqrt(2 / np.pi) * r**2 / 2
    )
    tilt = np.exp(-(r**2 + (speed / EPSILON) ** 2) / 2 + speed * axial / EPSILON**2)
    score = (axial - speed) / EPSILON**2
    marked = measure * tilt * direction * np.exp(-1j * k * axial)
    return (
        marked.sum(),
        (marked * score).sum(),
        (marked * axial).sum(),
        (marked * score * axial).sum(),
    )


def _radial_map(beta, k):
    speed = _polar_speed(beta)
    gain0 = beta * EPSILON / L0
    gain = gain0 * np.exp(-(SIGMA**2) * k**2 / 2)
    p = np.exp(-1j * speed * k - EPSILON**2 * k**2 / 2)
    b = B0 * np.exp(-0.4 * k**2)
    moment, response, _, _ = _shifted_gaussian_moments(speed, k)
    matrix = np.zeros((3, 3), dtype=complex)
    matrix[0, 0] = p * (1 - k**2 * b)
    matrix[0, 1:] = -1j * p * k * gain * AGES
    matrix[1, 0] = moment - 1j * k * response * b
    matrix[1, 1:] = response * gain * AGES
    matrix[2, 1] = 1
    return matrix


def test_projected_gaussian_nonzero_fixed_point_and_radial_gain():
    beta = 1.04
    speed = _polar_speed(beta)
    gain = beta * EPSILON / L0
    marked, derivative, _, _ = _shifted_gaussian_moments(speed, 0)
    assert marked * gain == pytest.approx(speed, rel=2e-14)
    assert 0 < (derivative * gain).real < 1
    assert marked * gain / speed == pytest.approx(1, rel=2e-14)
    assert np.max(np.abs(np.linalg.eigvals(_radial_map(beta, 0)[1:, 1:]))) < 1


def test_polar_speed_vanishes_with_square_root_at_threshold():
    np.testing.assert_allclose(_ratio(0), L0, rtol=3e-16)
    assert _ratio(0.4) > _ratio(0.8) > _ratio(1.2)
    distance = 0.001
    assert (_polar_speed(1 + distance) / EPSILON) ** 2 == pytest.approx(
        10 * distance, rel=0.002
    )


@pytest.mark.parametrize("beta", [1.025, 1.04])
def test_longitudinal_density_mode_grows_although_uniform_magnitude_relaxes(beta):
    speed = _polar_speed(beta)
    gain = beta * EPSILON / L0
    _, derivative, first, derivative_first = _shifted_gaussian_moments(speed, 0)
    r = gain * derivative.real
    gap = 1 - r
    c = speed + speed / gap
    correction = (speed * MEAN_AGE * c - gain * first.real - B0) / gap + (
        speed * (c * (1 + r * MEAN_AGE) - gain * derivative_first.real) / gap**2
    )
    growth = correction + (speed / gap) ** 2 / 2 - EPSILON**2 / 2
    assert growth > 0
    assert growth * (beta - 1) ** 2 == pytest.approx(
        5 / 4 * EPSILON**2 * (1 + MEAN_AGE), rel=0.18
    )
    k = 2e-6
    roots = np.linalg.eigvals(_radial_map(beta, k))
    density = np.log(roots[np.argmin(np.abs(roots - 1))])
    assert density.real > 0
    assert density.real / k**2 == pytest.approx(growth, rel=0.002)
    assert density.imag / k == pytest.approx(-c, rel=1e-5)
