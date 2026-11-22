"""Fixed linear homogeneous-block controls, not a native many-node run."""

import numpy as np
import pytest
from scipy.special import roots_legendre


EPSILON = 0.8
SIGMA = 0.7
SCALAR_WIDTH = 0.4
CHI = 2 * np.sqrt(2 / np.pi) / (3 * EPSILON)
VECTOR_AGES = np.array([2 / 3, 1 / 3])


def _moments(k):
    mu, mu_weights = roots_legendre(32)
    radial_nodes, radial_weights = roots_legendre(64)
    r = 5 * (radial_nodes + 1)
    weights = 5 * radial_weights * np.sqrt(2 / np.pi) * r**2 * np.exp(-(r**2) / 2)
    phase = k * EPSILON * r[:, None] * mu
    odd = np.sum(weights * (np.sin(phase) @ (mu_weights * mu))) / 2
    response = np.sum(weights * r * (np.cos(phase) @ (mu_weights * mu**2)))
    return odd, response / (2 * EPSILON)


def _mode(k, scalar_gain, alignment=1.0):
    p = np.exp(-(EPSILON**2) * k**2 / 2)
    gain = alignment * np.exp(-(SIGMA**2) * k**2 / 2) / CHI
    b = scalar_gain * np.exp(-SCALAR_WIDTH * k**2)
    odd, response = _moments(k)
    matrix = np.zeros((3, 3), dtype=complex)
    matrix[0, 0] = p * (1 - k**2 * b)
    matrix[0, 1:] = -1j * p * k * gain * VECTOR_AGES
    matrix[1, 0] = -1j * (odd + k * response * b)
    matrix[1, 1:] = response * gain * VECTOR_AGES
    matrix[2, 1] = 1
    source = np.array([-p * k**2 * b, -1j * k * response * b, 0])
    return matrix, source


def test_gaussian_endpoint_write_supplies_the_zero_mode_susceptibility():
    odd0, response0 = _moments(0)
    assert odd0 == 0
    assert response0 == pytest.approx(CHI, rel=3e-15)
    k = 0.004
    odd, response = _moments(k)
    assert odd / k == pytest.approx(EPSILON**2 * CHI, rel=1e-5)
    assert (1 - response / CHI) / k**2 == pytest.approx(6 / 5 * EPSILON**2, rel=1e-5)


@pytest.mark.parametrize(("strength", "conclusion"), [(0.8, -1), (1.0, 0), (1.2, 1)])
def test_uniform_direction_is_critical_only_at_unit_loop_gain(strength, conclusion):
    block, _ = _mode(0, -(EPSILON**2) / 2, alignment=strength)
    roots = np.linalg.eigvals(block[1:, 1:])
    dominant = roots.real.max()
    if conclusion == 0:
        assert dominant == pytest.approx(1, abs=1e-14)
    else:
        assert (dominant - 1) * conclusion > 0


def test_two_age_current_gives_damped_longitudinal_waves_at_vector_threshold():
    k = 0.014
    block, _ = _mode(k, -(EPSILON**2) / 2)
    roots = np.linalg.eigvals(block)
    waves = roots[np.argsort(np.abs(roots - 1))[:2]]
    assert np.all(np.abs(waves) < 1)
    logs = np.log(waves)
    np.testing.assert_allclose(
        np.sort(logs.imag) / k, EPSILON * np.sqrt(3 / 8) * np.array([-1, 1]), rtol=4e-4
    )
    vector_width = SIGMA**2 / 2 + 6 / 5 * EPSILON**2
    damping = (13 / 24 * EPSILON**2 - vector_width) / (8 / 3)
    np.testing.assert_allclose(logs.real / k**2, damping, rtol=8e-4)


def test_at_old_scalar_criticality_static_pole_disappears_when_current_is_critical():
    b = -(EPSILON**2) / 2
    errors = []
    for k in (0.02, 0.01):
        gains = []
        for alignment in (0, 1):
            block, source = _mode(k, b, alignment)
            state = np.linalg.solve(np.eye(3) - block, source)
            gains.append(state[0].real)
        scalar, coupled = gains
        assert scalar > 1000
        assert coupled == pytest.approx(1, rel=4e-4)
        errors.append(1 - coupled)
    assert errors[0] / errors[1] == pytest.approx(4, rel=1e-3)


def test_cancelling_the_static_denominator_removes_nonzero_sound_speed():
    k = 0.012
    block, source = _mode(k, -(EPSILON**2))
    state = np.linalg.solve(np.eye(3) - block, source)
    assert abs(state[0]) > 1000  # static response restored in this fixed case
    roots = np.linalg.eigvals(block)
    close = roots[np.argsort(np.abs(roots - 1))[:2]]
    assert max(abs(close - 1)) / k < 0.03
