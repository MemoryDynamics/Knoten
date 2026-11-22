"""Fixed one-write checks, not native FIFO trajectories."""

import numpy as np
import pytest

from emergenz_knoten.kernels import gaussian_gradient
from experiments.current.reference.fifo_4d_delayed_spin import (
    coherent_history,
    delayed_step,
)
from experiments.current.reference.fifo_balanced_volume import balanced_gaussian_write


WEIGHTS = np.array([1, 0.5, 0.25, 0.125])
E1, E2, E3, E4 = np.eye(4)
A = np.stack((E1, E2, E3, E1))
B = np.stack((E1, E4, E2, E1))


def _raw_heads(first, second, coupling):
    proposed = []
    for own, other in ((first, second), (second, first)):
        free = -own[-1]
        head = free - gaussian_gradient(
            free, other, WEIGHTS, sigma=1.0, amplitude=coupling
        )
        proposed.append(head / np.linalg.norm(head))
    return np.stack(proposed)


@pytest.mark.parametrize("coupling", [-0.02, 0.02])
def test_balanced_exchange_matches_closed_optimum_and_not_the_raw_drift(coupling):
    raw = _raw_heads(A, B, coupling)
    normal = np.stack((-E4, -E3))
    axial = np.sum(raw * normal, axis=1)
    assert np.all(coupling * axial > 0)

    transverse = np.sqrt(1 - axial**2).sum()
    delta = axial[0] - axial[1]
    expected_q = delta / np.hypot(delta, transverse)
    result = balanced_gaussian_write(A, B, WEIGHTS, coupling=coupling)
    volumes = np.linalg.det(result)
    np.testing.assert_allclose(volumes, (expected_q, -expected_q), atol=2e-15)
    assert coupling * volumes[0] > 0
    np.testing.assert_allclose(np.linalg.norm(result, axis=2), 1, atol=2e-15)
    np.testing.assert_array_equal(result[:, 1:], (A[:3], B[:3]))


def test_weak_exchange_has_the_predicted_coefficient():
    coupling = 1e-6
    pos, neg = (
        np.linalg.det(balanced_gaussian_write(A, B, WEIGHTS, coupling=sign * coupling))
        for sign in (1, -1)
    )
    slope = (WEIGHTS[1] - WEIGHTS[2]) / (2 * np.e)
    np.testing.assert_allclose((pos - neg) / (2 * coupling), (slope, -slope), rtol=1e-7)


def test_nonzero_net_volume_is_conserved_and_reflection_covariant():
    first = A.copy()
    first[3] = 0.8 * E1 + 0.6 * E4
    coupling = -0.03
    result = balanced_gaussian_write(first, B, WEIGHTS, coupling=coupling)
    volumes = np.linalg.det(result)
    np.testing.assert_allclose(volumes.sum(), 0.6, atol=2e-15)
    assert abs(volumes[1]) > 1e-5

    # A reflection not aligned with any of the basis vectors in the fixture.
    direction = np.array([1, 2, -1, 0]) / np.sqrt(6)
    reflection = np.eye(4) - 2 * np.outer(direction, direction)
    mirrored = balanced_gaussian_write(
        first @ reflection, B @ reflection, WEIGHTS, coupling=coupling
    )
    swapped = balanced_gaussian_write(B, first, WEIGHTS, coupling=coupling)
    np.testing.assert_allclose(mirrored, result @ reflection, atol=2e-15)
    np.testing.assert_allclose(swapped, result[::-1], atol=2e-15)


def test_a_rank_deficient_peer_cannot_absorb_unbalanced_volume():
    repeated = np.tile(0.6 * E1 + 0.8 * E4, (4, 1))
    raw = _raw_heads(A, repeated, 0.1)
    assert raw[0, 3] < 0
    result = balanced_gaussian_write(A, repeated, WEIGHTS, coupling=0.1)
    np.testing.assert_array_equal(np.linalg.det(result), (0, 0))
    np.testing.assert_array_equal(result[1, 0], raw[1])


def test_planar_rule_is_unconstrained_and_zero_coupling_is_free():
    first = coherent_history([0, 0, 1])
    second = delayed_step(first)
    result = balanced_gaussian_write(first, second, WEIGHTS, coupling=0.1)
    np.testing.assert_allclose(result[:, 0], _raw_heads(first, second, 0.1), atol=2e-15)
    neutral = balanced_gaussian_write(A, B, WEIGHTS, coupling=0)
    np.testing.assert_array_equal(neutral, (delayed_step(A), delayed_step(B)))


def test_saturated_total_forces_both_heads_to_their_axes():
    first = np.eye(4)
    coupled = balanced_gaussian_write(first, first, WEIGHTS, coupling=0.1)
    np.testing.assert_array_equal(coupled, (delayed_step(first), delayed_step(first)))


def test_exact_rank_collapse_has_a_discontinuous_head_limit():
    second = np.tile(E4, (4, 1))
    first = A.copy()
    first[2] = E1
    collapsed = balanced_gaussian_write(first, second, WEIGHTS, coupling=0.1)
    assert collapsed[0, 0, 3] < -0.05

    for epsilon in (0.125, 1e-4, 1e-8):
        first[2] = np.sqrt(1 - epsilon**2) * E1 + epsilon * E3
        resolved = balanced_gaussian_write(first, second, WEIGHTS, coupling=0.1)
        np.testing.assert_allclose(resolved[0, 0], -E1, atol=2e-15)
        np.testing.assert_array_equal(np.linalg.det(resolved), (0, 0))
