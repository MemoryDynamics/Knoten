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


def _radial_map(beta, k, b0=B0):
    speed = _polar_speed(beta)
    gain0 = beta * EPSILON / L0
    gain = gain0 * np.exp(-(SIGMA**2) * k**2 / 2)
    p = np.exp(-1j * speed * k - EPSILON**2 * k**2 / 2)
    b = b0 * np.exp(-0.4 * k**2)
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


def _ordered_coefficients(x):
    gain = EPSILON / _ratio(x)
    prefactor = 2 * np.sqrt(2 / np.pi)
    second = quad(lambda v: v**2 * np.exp(-((x * v) ** 2) / 2), 0, 1)[0]
    fourth = quad(lambda v: v**4 * np.exp(-((x * v) ** 2) / 2), 0, 1)[0]
    r = gain * prefactor * second / EPSILON
    gap = 1 - r
    curvature = -x * prefactor * fourth / EPSILON**2
    a = EPSILON * x
    positive = (
        (1 + r) * (a**2 - EPSILON**2 * gap**2) / (2 * gap**3)
        + MEAN_AGE * (1 + gap) * a**2 / gap**3
        - a * EPSILON**2 * gain * curvature / gap**2
    )
    assert 0 < gap < min(1, x)
    assert curvature < 0 and positive > 0
    return gap, positive


@pytest.mark.parametrize("x", [0.7, 1.8, 4.0])
@pytest.mark.parametrize("repulsive", [False, True])
def test_longitudinal_full_branch_and_repulsive_threshold(x, repulsive):
    gap, positive = _ordered_coefficients(x)
    b = gap * positive + 0.5 if repulsive else B0
    k = 1e-5
    roots = np.linalg.eigvals(_radial_map(L0 / _ratio(x), k, b))
    density = np.log(roots[np.argmin(np.abs(roots - 1))])
    expected = positive - b / gap
    assert (density.real < 0) == repulsive
    assert density.real / k**2 == pytest.approx(expected, rel=1e-4)


def _full_write_response(a, wave):
    direction, angle_weights = roots_legendre(48)
    nodes, radial_weights = roots_legendre(72)
    r = 5 * (nodes[:, None, None] + 1)
    mu = direction[:, None]
    phi = 2 * np.pi * np.arange(24) / 24
    sine = np.sqrt(1 - mu**2)
    unit = np.stack(
        (mu + np.zeros(24), sine * np.cos(phi), sine * np.sin(phi)), axis=-1
    )
    displacement = EPSILON * r[..., None] * unit
    mean = np.array([a, 0, 0])
    score = (displacement - mean) / EPSILON**2
    measure = (
        5
        * radial_weights[:, None, None]
        * angle_weights[None, :, None]
        * np.sqrt(2 / np.pi)
        * r**2
        / 48
    )
    tilt = np.exp(
        -(r**2 + (a / EPSILON) ** 2) / 2 + a * displacement[..., 0] / EPSILON**2
    )
    weight = measure * tilt * np.exp(-1j * (displacement @ wave))
    b = np.einsum("ijk,jkm->m", weight, unit)
    t = np.einsum("ijk,jkm,ijkn->mn", weight, unit, score)
    return b, t


def _plane_map(x, wave, scalar, scalar_delay=0):
    a, gain = EPSILON * x, EPSILON / _ratio(x)
    length2 = wave @ wave
    wave3 = np.r_[wave, 0]
    b, t = _full_write_response(a, wave3)
    g = gain * np.exp(-(SIGMA**2) * length2 / 2)
    p = np.exp(-1j * a * wave[0] - EPSILON**2 * length2 / 2)
    size = 5 + scalar_delay
    d = np.zeros((2, size), dtype=complex)
    d[:, 1:3] = g * AGES[0] * np.eye(2)
    d[:, 3:5] = g * AGES[1] * np.eye(2)
    scalar_index = 0 if scalar_delay == 0 else size - 1
    d[:, scalar_index] = -1j * wave * scalar * np.exp(-0.4 * length2)
    matrix = np.zeros((size, size), dtype=complex)
    matrix[0] = -1j * p * (wave @ d)
    matrix[0, 0] += p
    matrix[1:3] = t[:2, :2] @ d
    matrix[1:3, 0] += b[:2]
    matrix[3:5, 1:3] = np.eye(2)
    if scalar_delay:
        matrix[5, 0] = 1
        for row in range(6, size):
            matrix[row, row - 1] = 1
    return matrix


def _slow_logs(matrix):
    roots = np.linalg.eigvals(matrix)
    return np.log(roots[np.argsort(np.abs(roots - 1))[:2]])


@pytest.mark.parametrize(
    "scalar,cosine,growing",
    [(B0, 0, True), (B0, 0.06, True), (B0, 0.7, False), (1.2, 0.3, False)],
)
def test_oblique_sound_discriminant_matches_the_discrete_write(scalar, cosine, growing):
    x = 1.8
    gap, _ = _ordered_coefficients(x)
    a = EPSILON * x
    p = 1 + MEAN_AGE
    c = a + a / gap
    v = (a - EPSILON**2 * gap / a) / p
    sine = np.sqrt(1 - cosine**2)
    velocities = np.linalg.eigvals(
        [[c * cosine, sine], [scalar * sine / p, v * cosine]]
    )
    k = 1e-5
    logs = _slow_logs(_plane_map(x, k * np.array([cosine, sine]), scalar))
    assert bool(np.any(velocities.imag)) == growing
    if growing:
        np.testing.assert_allclose(
            np.sort_complex(logs / k), np.sort_complex(-1j * velocities), atol=0.001
        )
        assert logs.real.max() > 0
    else:
        np.testing.assert_allclose(
            np.sort(logs.imag / k), np.sort(-velocities.real), atol=1e-6
        )


@pytest.mark.parametrize("scalar,delay", [(1.2, 0), (10, 1)])
def test_repulsive_transverse_waves_gain_damping_or_antidamping_from_delay(
    scalar, delay
):
    x = 1.8
    gap, _ = _ordered_coefficients(x)
    p = 1 + MEAN_AGE
    m2 = 2 * AGES[1]
    diffusion = SIGMA**2 / 2 + EPSILON**2 / 2 * (1 - gap / x**2)
    damping = -(diffusion + EPSILON**2 * p / 2 + EPSILON**2 * p / gap) / (2 * p)
    damping += scalar * (delay - m2 / (2 * p)) / (2 * p)
    k = 1e-4
    logs = _slow_logs(_plane_map(x, np.array([0, k]), scalar, delay))
    np.testing.assert_allclose(logs.real / k**2, damping, rtol=3e-5)
    np.testing.assert_allclose(np.abs(logs.imag) / k, np.sqrt(scalar / p), rtol=1e-7)
    assert (damping > 0) == bool(delay)


def test_delayed_repulsion_cannot_damp_both_axes_near_threshold():
    x = 0.06
    gap, positive = _ordered_coefficients(x)
    p = 1 + MEAN_AGE
    diffusion = SIGMA**2 / 2 + EPSILON**2 / 2 * (1 - gap / x**2)
    delay_offset = 1 - AGES[1] / p
    longitudinal_min = gap * positive
    transverse_max = (
        diffusion + EPSILON**2 * p / 2 + EPSILON**2 * p / gap
    ) / delay_offset
    assert longitudinal_min > transverse_max
    assert longitudinal_min / transverse_max == pytest.approx(
        5 * delay_offset, rel=0.003
    )


def test_out_of_plane_orientation_response_decouples_and_contracts():
    x = 1.8
    gain = EPSILON / _ratio(x)
    wave = np.array([0.31, 0.72, 0])
    b, t = _full_write_response(EPSILON * x, wave)
    np.testing.assert_allclose(b[2], 0, atol=5e-16)
    np.testing.assert_allclose(t[2, :2], 0, atol=5e-16)
    np.testing.assert_allclose(t[:2, 2], 0, atol=5e-16)
    assert abs(t[2, 2]) < 1 / gain
