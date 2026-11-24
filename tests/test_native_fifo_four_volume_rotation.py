"""Fixed substitutions for a native 4D relative equilibrium, not a trajectory."""

from fractions import Fraction as F

import numpy as np
import pytest

from emergenz_knoten.core import SimulationConfig
from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights
from emergenz_knoten.vector_memory import (
    VectorMemoryConfig,
    alignment_history_head_jacobian,
    vector_gaussian_field,
)


def _rotation(theta):
    c, s = np.cos(theta), np.sin(theta)
    return [[c, -s], [s, c]]


def _pentagon(length_squared, diagonal_squared):
    r = np.zeros((4, 4))
    r[:2, :2], r[2:, 2:] = _rotation(2 * np.pi / 5), _rotation(4 * np.pi / 5)
    a, b = (5 - np.sqrt(5)) / 2, (5 + np.sqrt(5)) / 2
    radius = np.sqrt(
        np.linalg.solve([[a, b], [b, a]], [length_squared, diagonal_squared])
    )
    head = np.array([radius[0], 0.0, radius[1], 0.0])
    points = np.stack([np.linalg.matrix_power(r.T, j) @ head for j in range(5)])
    return points, r, radius**2


def _five_cycle():
    length_squared, diagonal_squared = 2 * np.log([5, 10])
    history, r, _ = _pentagon(length_squared, diagonal_squared)
    config = VectorMemoryConfig(
        scalar=SimulationConfig(
            dim=4,
            epsilon=0.0,
            alpha=5 / 6,
            max_memory=4,
            memory_factor=4,
            eta=2592.0,
            memory_mass=1.0,
            sigma_rep=1.0,
            amplitude_rep=1.0,
            amplitude_att=0.0,
        ),
        lambda_vector=0.5,
        vector_memory_factor=4,
        max_vector_memory=4,
        vector_mass=1.0,
        eta_vector=-160 * np.sqrt(length_squared),
        sigma_vector=1.0,
    )
    return history, r, config


def _native_head(history, config):
    scalar = config.scalar
    vector_count = len(history) - 1
    steps = history[:-1] - history[1:]
    gradient = double_gaussian_gradient(
        history[0],
        history[:4],
        exponential_memory_weights(scalar.alpha, 4),
        sigma_rep=scalar.sigma_rep,
        sigma_att=scalar.sigma_att,
        amplitude_rep=scalar.amplitude_rep,
        amplitude_att=scalar.amplitude_att,
    )
    vector = vector_gaussian_field(
        history[0],
        history[:vector_count],
        steps / np.linalg.norm(steps, axis=1, keepdims=True),
        exponential_memory_weights(config.lambda_vector, vector_count),
        sigma=config.sigma_vector,
    )
    return history[0] - scalar.eta * gradient + config.eta_vector * vector


def test_five_cycle_exact_coefficients_and_regular_simplex_mismatch():
    vector = (F(80), F(8), F(2), F(1))
    scalar = [b - a for a, b in zip(vector[:-1], vector[1:], strict=True)]
    assert scalar == [-72, -6, -1]
    expected = [
        -2160 * F(1, 6) ** j * g for j, g in enumerate((F(1, 5), F(1, 10), F(1, 10)), 1)
    ]
    assert expected == scalar

    # Equal chords give unequal successive ratios of the required age differences.
    g, q = F(3, 5), F(1, 2)
    r = (1 / (g * q**3), q**-2, q**-1, F(1))
    differences = [a - b for a, b in zip(r[:-1], r[1:], strict=True)]
    assert differences[1] / differences[0] < q == differences[2] / differences[1]


@pytest.mark.parametrize("phase", range(5))
def test_five_cycle_closes_at_all_prescribed_phases_with_full_rank(phase):
    history, r, config = _five_cycle()
    phase_history = history @ np.linalg.matrix_power(r, phase).T
    head = _native_head(phase_history, config)
    np.testing.assert_allclose(head, r @ phase_history[0], atol=2e-13)
    assert np.linalg.matrix_rank(phase_history[:-1] - phase_history[1:]) == 4
    np.testing.assert_allclose(np.linalg.matrix_power(r, 5), np.eye(4), atol=1e-15)


def test_co_rotating_trace_matches_analytic_instability_bound():
    history, r, config = _five_cycle()
    blocks = alignment_history_head_jacobian(history, config)
    expected = (71 - 40 / np.log(5)) * np.log(2.5) - 21 * np.log(2)
    np.testing.assert_allclose(np.trace(r.T @ blocks[0]), expected, atol=2e-12)
    # Rational lower and upper bounds for the three logarithms in the trace.
    assert 2 * sum(F(2, 3) ** j / j for j in (1, 3, 5, 7)) > F(8, 5)
    assert 2 * sum(F(3, 7) ** j / j for j in (1, 3)) > F(9, 10)
    assert 2 * (F(1, 3) + F(1, 27) / (3 * (1 - F(1, 9)))) < F(7, 10)
    assert (71 - 40 / F(8, 5)) * F(9, 10) - 21 * F(7, 10) == F(267, 10)


def _five_deposit_cycle(t):
    denominator = 2 * t * t - 2 * t + 1
    g1, g2 = 1 / denominator, 1 / (denominator * t)
    d1, d2 = -2 * np.log([g1, g2])
    points, rotation, radii_squared = _pentagon(d1, d2)
    b0 = 16 * t * denominator / (t - 2)
    s = 1 / (4 * t - 2)
    scalar_gain = (2 / (t - 2)) / (g2 * s**3 * (1 - s))
    config = VectorMemoryConfig(
        scalar=SimulationConfig(
            dim=4,
            epsilon=0.0,
            alpha=1 - s,
            max_memory=4,
            memory_factor=4,
            eta=scalar_gain,
            memory_mass=1.0,
            sigma_att=1.0,
            amplitude_att=1.0,
            amplitude_rep=0.0,
        ),
        lambda_vector=0.5,
        vector_memory_factor=4,
        max_vector_memory=5,
        vector_mass=1.0,
        eta_vector=2 * b0 * np.sqrt(d1),
        sigma_vector=1.0,
    )
    return np.vstack((points, points[:1])), rotation, radii_squared, config


@pytest.mark.parametrize("t", [3, 32, 64])
def test_five_deposit_rational_coefficients_close_exactly(t):
    t = F(t)
    denominator = 2 * t * t - 2 * t + 1
    g1, g2 = 1 / denominator, 1 / (denominator * t)
    s = 1 / (4 * t - 2)
    b = [
        16 * t * denominator / (t - 2) * g / 2**j
        for j, g in enumerate([F(1), g1, g2, g2, g1])
    ]
    gamma = [
        2 / (t - 2) / (g2 * s**3) * s**j * g for j, g in enumerate([g1, g2, g2], 1)
    ]
    assert all(value > 0 for value in gamma)
    assert [b[j] - b[4] - sum(gamma[j:]) for j in range(4)] == [-1] * 4


@pytest.mark.parametrize("phase", range(5))
def test_native_interior_defect_regenerates_at_five_prescribed_phases(phase):
    history, r, r_sq, config = _five_deposit_cycle(32)
    phase_history = history @ np.linalg.matrix_power(r, phase).T
    head = _native_head(phase_history, config)
    np.testing.assert_allclose(head, r @ phase_history[0], atol=3e-9)
    points = phase_history[:5]
    z = np.linalg.solve(points[1:] - points[0], np.arange(1, 5) * np.log(2))
    steps = phase_history[:-1] - phase_history[1:]
    directions = steps / np.linalg.norm(steps, axis=1, keepdims=True)
    weights = exponential_memory_weights(0.5, 5)
    field = vector_gaussian_field(z, points, directions, weights, sigma=1.0)
    np.testing.assert_allclose(field, 0, atol=1e-17)

    lam = np.linalg.solve(np.vstack((points.T, np.ones(5))), np.r_[z, 1])
    assert lam.min() == pytest.approx(1 / 5 - 2 * np.log(2) / 5 * np.sum(1 / r_sq))
    assert np.all(lam > 0.02)
    coefficient = weights * np.exp(-0.5 * np.sum((points - z) ** 2, axis=1))
    np.testing.assert_allclose(coefficient, np.exp(-0.5 * (z @ z + r_sq.sum())) / 8)
    jacobian = (directions.T * coefficient) @ (points - z)
    np.linalg.cholesky((jacobian + jacobian.T) / 2)
    assert np.linalg.det(jacobian) > 0


@pytest.mark.parametrize("t", [3, 32, 64])
def test_five_deposit_full_trace_matches_the_family_obstruction(t):
    history, r, r_sq, config = _five_deposit_cycle(t)
    blocks = alignment_history_head_jacobian(history, config)
    denominator = 2 * t * t - 2 * t + 1
    a, d = np.log([denominator, t])
    b0 = 16 * t * denominator / (t - 2)
    b1, b2, b3, b4 = np.array([8 * t, 4, 2, t]) / (t - 2)
    expected = -b4 + (b0 - b1 + 1 - b0 / (2 * a)) * (d - a)
    expected += (2 * b1 + 2 * b2 + b3) * d
    np.testing.assert_allclose(np.trace(r.T @ blocks[0]), expected, rtol=1e-12)
    assert expected < -32
    if t == 3:
        assert 1 / 5 - 2 * np.log(2) / 5 * np.sum(1 / r_sq) < 0
