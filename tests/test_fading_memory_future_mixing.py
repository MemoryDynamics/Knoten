"""Fixed algebra and native drift readouts, never a simulated noisy path."""

from fractions import Fraction as F
import math

import numpy as np
import pytest

from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights
from emergenz_knoten.vector_memory import normalize_orientation, vector_gaussian_field


SCALAR_RETENTION, VECTOR_RETENTION = 0.64, 0.72
SCALAR_GAIN, VECTOR_GAIN = 0.23, 0.81
GRADIENT_BOUND = math.exp(-0.5) * (0.4 / 0.7 + 1.2 / 1.1)
INCREMENTS = np.array(
    [
        [0.2, -0.6, 0.4],
        [0.8, 0.2, -0.3],
        [-0.5, 0.4, 0.2],
        [0.1, -0.3, -0.7],
        [1.2, 0.4, -0.9],
        [0.4, -0.6, 1.2],
    ]
)


def _weights(h_s, h_v):
    return (
        exponential_memory_weights(1 - SCALAR_RETENTION, h_s),
        exponential_memory_weights(1 - VECTOR_RETENTION, h_v),
    )


def _drifts(increments, h_s, h_v):
    positions = np.vstack([np.zeros(3), -np.cumsum(increments, axis=0)])
    directions = np.array([normalize_orientation(step) for step in increments[:h_v]])
    ws, wv = _weights(h_s, h_v)
    scalar = -SCALAR_GAIN * double_gaussian_gradient(
        positions[0],
        positions[:h_s],
        ws,
        amplitude_rep=0.4,
        amplitude_att=1.2,
        sigma_rep=0.7,
        sigma_att=1.1,
    )
    vector = VECTOR_GAIN * vector_gaussian_field(
        positions[0], positions[:h_v], directions, wv, sigma=0.94
    )
    return scalar, vector


@pytest.mark.parametrize(("h_s", "h_v"), [(5, 3), (3, 5)])
def test_common_suffix_leaves_distinct_scalar_and_vector_age_bounds(h_s, h_v):
    unchanged_s, unchanged_v = _drifts(INCREMENTS, h_s, h_v)
    ws, wv = _weights(h_s, h_v)
    length = max(h_s - 1, h_v)
    for common in range(length + 1):
        altered = INCREMENTS.copy()
        altered[common:] *= -1
        scalar, vector = _drifts(altered, h_s, h_v)
        assert np.linalg.norm(scalar - unchanged_s) <= (
            2 * SCALAR_GAIN * GRADIENT_BOUND * ws[common + 1 :].sum() + 2e-16
        )
        assert np.linalg.norm(vector - unchanged_v) <= (
            2 * VECTOR_GAIN * wv[common:].sum() + 2e-16
        )
        if common == length:
            np.testing.assert_array_equal(scalar, unchanged_s)
            np.testing.assert_array_equal(vector, unchanged_v)


def test_same_oldest_position_can_still_have_a_different_alignment_direction():
    altered = INCREMENTS.copy()
    altered[2] *= -1
    scalar, vector = _drifts(INCREMENTS, 3, 3)
    other_s, other_v = _drifts(altered, 3, 3)
    np.testing.assert_array_equal(scalar, other_s)
    assert np.linalg.norm(vector - other_v) > 0.03


def test_truncation_uses_only_the_omitted_mass_and_geometric_square_budget():
    full = np.sum(_drifts(INCREMENTS, 6, 6), axis=0)
    cut = np.sum(_drifts(INCREMENTS, 3, 4), axis=0)
    c_s, c_v = SCALAR_GAIN * GRADIENT_BOUND, VECTOR_GAIN
    s, q = SCALAR_RETENTION, VECTOR_RETENTION
    assert np.linalg.norm(full - cut) <= c_s * s**3 + c_v * q**4
    ages = np.arange(128)
    budget = c_s**2 * s**2 / (1 - s**2) + 2 * c_s * c_v * s / (1 - s * q)
    budget += c_v**2 / (1 - q**2)
    assert np.sum((c_s * s ** (ages + 1) + c_v * q**ages) ** 2) == pytest.approx(
        budget, rel=2e-15
    )


@pytest.mark.parametrize("direction", [[0, 0, 0], [0.3, 0.4, 0.1], [0, 1, 0]])
def test_shared_gaussian_postprocessing_restores_both_means_and_covariance(direction):
    direction = np.asarray(direction)
    midpoint = np.array([0.31, -0.22, 0.13])
    bound, epsilon = 0.83, 0.74
    outer = np.outer(direction, direction)
    residual = np.eye(3) - outer / (1 + math.sqrt(1 - direction @ direction))
    np.testing.assert_allclose(residual @ residual.T + outer, np.eye(3), atol=2e-16)
    for sign in (-1, 1):
        expected = midpoint + sign * bound * direction
        actual = midpoint + epsilon * direction * (sign * bound / epsilon)
        np.testing.assert_allclose(actual, expected, atol=2e-16)


def test_defective_renewal_law_matches_the_exact_matching_counter():
    a = [F(1, 3), F(1, 4), F(0)]
    renewals = [F(1)]
    distribution = [F(1), F(0), F(0)]
    for n in range(1, 15):
        reset = sum(state * fail for state, fail in zip(distribution, a, strict=True))
        assert reset == F(1, 3) * renewals[n - 1] + (
            F(1, 6) * renewals[n - 2] if n >= 2 else 0
        )
        renewals.append(reset)
        distribution = [
            reset,
            distribution[0] * (1 - a[0]),
            distribution[1] * (1 - a[1]) + distribution[2],
        ]
        assert sum(distribution) == 1
    t = F(5, 4)
    moment = F(1, 2) / (1 - t / 3 - t**2 / 6)
    assert moment == F(48, 31)
    truncated = sum(F(1, 2) * u * t**n for n, u in enumerate(renewals))
    assert truncated < moment
