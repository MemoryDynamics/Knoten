"""Fixed two-phase force identities, not orbit runs or parameter fitting."""

from fractions import Fraction as F
from math import factorial

import numpy as np
import pytest

from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights
from emergenz_knoten.state import FiniteMemoryState
from emergenz_knoten.vector_memory import (
    oriented_history_from_state,
    vector_memory_force,
)


Q = 0.99


def _vertices():
    return np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)


def _history(phase, inner=1.0, outer=5.0, periods=1):
    vertices = _vertices()
    base = np.empty((8, 3))
    base[::2], base[1::2] = inner * vertices, outer * vertices
    if phase == "far":
        base = np.roll(base, -1, axis=0)
    elif phase != "near":
        raise ValueError("unknown phase")
    return np.vstack([np.tile(base, (periods, 1)), base[0]])


def _witness(q):
    t = q**2
    return np.sqrt(3) / 2 * np.array([1, -(1 + t) / t, 1 / t])


def _factors(inner, outer, sigma, q):
    ell = np.sqrt(inner**2 + outer**2 + 2 * inner * outer / 3)
    radial = np.exp(-((outer - inner) ** 2) / (2 * sigma**2))
    cross = np.exp(-(ell**2) / (2 * sigma**2))
    far = np.exp(-4 * outer**2 / (3 * sigma**2))
    beta_near = q * inner * (radial - cross) / ell
    beta_far = inner * (1 - far) / ell
    return beta_near, beta_far, radial, cross, far, ell


def _scalar_force(history, retention, deposition="delta"):
    weights = exponential_memory_weights(
        1 - retention, len(history) - 1, memory_mass=1.3
    )
    return -double_gaussian_gradient(
        history[0],
        history[:-1],
        weights,
        sigma_rep=0.9,
        sigma_att=2.3,
        amplitude_rep=1.7,
        amplitude_att=0.6,
        deposition_kernel=deposition,
        deposition_sigma=0.0 if deposition == "delta" else 0.4,
    )


def _vector_force(history, q, sigma):
    state = FiniteMemoryState(
        x=history[0],
        memory=history,
        weights=exponential_memory_weights(1 - q, len(history), memory_mass=1),
    )
    positions, orientations, weights = oriented_history_from_state(state, mode="unit")
    return vector_memory_force(
        history[0], positions, orientations, weights, sigma=sigma
    )


@pytest.mark.parametrize("phase", ["near", "far"])
def test_phase_histories_have_the_required_predecessor_and_successor(phase):
    vertices = _vertices()
    history = _history(phase)
    np.testing.assert_array_equal(history[0], history[-1])
    target = 5 * vertices[3] if phase == "near" else vertices[0]
    np.testing.assert_array_equal(history[-2], target)
    shifted = np.vstack([target, history[:-1]])
    chords = shifted[:-1] - shifted[1:]
    assert np.all(np.linalg.norm(chords, axis=1) > 0)


@pytest.mark.parametrize("q", [0.6, Q])
def test_witness_annihilates_the_shared_scalar_tangent_direction(q):
    vertices = _vertices()
    h = _witness(q)
    t = q**2
    expected = np.array([0, 1, -(1 + t) / t, 1 / t])
    np.testing.assert_allclose(vertices @ h, expected, atol=2e-16)
    tangent_sum = sum(q ** (2 * i) * vertices[i] for i in range(1, 4))
    assert abs(h @ tangent_sum) < 1e-15
    assert np.dot(h, h) == pytest.approx(3 * (1 + t + t**2) / (2 * t**2))


@pytest.mark.parametrize("phase", ["near", "far"])
@pytest.mark.parametrize("periods", [1, 3])
@pytest.mark.parametrize("deposition", ["delta", "gaussian"])
def test_native_radial_scalar_channel_has_zero_witness_projection(
    phase, periods, deposition
):
    history = _history(phase, periods=periods)
    force = _scalar_force(history, Q, deposition)
    assert abs(_witness(Q) @ force) < 3e-15


@pytest.mark.parametrize("phase", ["near", "far"])
@pytest.mark.parametrize("periods", [1, 2])
@pytest.mark.parametrize("geometry", [(1.0, 5.0, 1.0), (0.8, 1.7, 1.2)])
def test_native_vector_projection_matches_the_two_phase_formula(
    phase, periods, geometry
):
    inner, outer, sigma = geometry
    history = _history(phase, inner, outer, periods)
    beta_near, beta_far, *_ = _factors(inner, outer, sigma, Q)
    aggregate_w0 = (1 - Q) * sum(Q ** (8 * k) for k in range(periods))
    beta = beta_near if phase == "near" else beta_far
    projected = _witness(Q) @ _vector_force(history, Q, sigma)
    assert projected == pytest.approx(-aggregate_w0 * beta, rel=2e-12, abs=2e-17)
    assert 0 < beta_near < Q * beta_far


@pytest.mark.parametrize("gain", [-1.3, 0.0, 0.7])
def test_two_phase_native_residual_identity_eliminates_any_shared_vector_gain(gain):
    vertices = _vertices()
    h = _witness(Q)
    beta_near, beta_far, *_ = _factors(1, 5, 1, Q)
    residuals = []
    for phase in ("near", "far"):
        scalar_history = _history(phase, periods=3)
        vector_history = _history(phase, periods=2)
        target = 5 * vertices[3] if phase == "near" else vertices[0]
        required = target - vector_history[0]
        proposed = 0.7 * _scalar_force(scalar_history, Q)
        proposed += gain * _vector_force(vector_history, Q, 1)
        residuals.append(proposed - required)
    projected = beta_far * (h @ residuals[0]) - beta_near * (h @ residuals[1])
    assert projected == pytest.approx(-5 * beta_far / Q**2, rel=2e-15)
    bound = 5 * beta_far / (Q**2 * np.linalg.norm(h) * (beta_far + beta_near))
    assert max(np.linalg.norm(residual) for residual in residuals) >= bound > 7 / 3


def test_fixed_residual_and_retention_bounds_have_rational_certificates():
    assert sum(F(4) ** k / factorial(k) for k in range(8)) > 50
    assert F(100, 3) > 8
    assert 50 * 2499**2 > 49 * 2500**2  # (5*sqrt(2)/3)*(2499/2500) > 7/3.
    assert sum(F(44, 3) ** k / factorial(k) for k in range(25)) > 2000000
    assert 1 - F(99, 100) ** 2 < F(1, 50)
    assert F(6) * F(1, 2000000) * F(1, 50) * F(2500, 2499) < F(1, 4000) ** 2


def test_unequal_aging_necessary_condition_is_only_a_tangent_collinearity():
    _, beta_far, _, cross, far, ell = _factors(1, 5, 1, Q)
    coefficient = far * (5 - Q**-2) / ell - cross / Q
    assert coefficient < 0
    magnitude, t = -coefficient, Q**2
    u = magnitude * t**2 * (1 - t) / (beta_far + magnitude * t * (1 - t))
    assert 0 < u < (1 / 4000) ** 2 < t
    vector_coordinates = np.array(
        [coefficient * t * (1 - t) * (1 + t) - beta_far, coefficient * t**2 * (1 - t)]
    )
    scalar_coordinates = np.array([1 + u, u])
    determinant = scalar_coordinates[0] * vector_coordinates[1]
    determinant -= scalar_coordinates[1] * vector_coordinates[0]
    assert abs(determinant) < 1e-23
    # No force-balance solution, gain or trajectory is constructed here.
    unequal_witness = _witness(0.5)
    near_target = 5 * _vertices()[3] - _vertices()[0]
    assert unequal_witness @ near_target == pytest.approx(5 / 0.5**2)
    assert abs(unequal_witness @ _scalar_force(_history("near"), 0.5)) < 2e-15


@pytest.mark.parametrize("exception", ["different_aging", "incomplete_period"])
def test_scalar_cancellation_is_not_claimed_outside_its_hypotheses(exception):
    history = _history("near")
    retention = Q
    if exception == "different_aging":
        retention = 0.5
    else:
        history = history[:6]  # Five scalar deposits, not a complete eight-period.
    assert abs(_witness(Q) @ _scalar_force(history, retention)) > 1e-6
