"""Fixed controls for exact active-state projection and FIFO pose overlap."""

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights
from emergenz_knoten.vector_memory import (
    normalize_orientation,
    update_vector_history,
    vector_gaussian_field,
)


def _orbit(times, radius=0.8, height=0.2):
    phase = np.asarray(times) % 4
    ring = np.array(
        [
            [radius, 0, height],
            [0, radius, -height],
            [-radius, 0, height],
            [0, -radius, -height],
        ]
    )
    return ring[phase]


def _directions(history):
    return np.array(
        [normalize_orientation(step) for step in history[:-1] - history[1:]]
    )


def _head(positions, directions, kick):
    scalar = double_gaussian_gradient(
        positions[0],
        positions,
        exponential_memory_weights(0.38, 4),
        amplitude_rep=0.4,
        amplitude_att=1.1,
        sigma_rep=0.9,
        sigma_att=1.5,
    )
    field = _field(positions, directions, positions[0])
    return positions[0] - 0.34 * scalar + 0.72 * field + kick


def _field(positions, directions, at):
    return vector_gaussian_field(
        at, positions, directions, exponential_memory_weights(0.21, 4), sigma=0.83
    )


@pytest.mark.parametrize("length", [0.25, 2.0, 8.0])
@pytest.mark.parametrize("kick", [(0, 0, 0), (0.13, -0.19, 0.04)])
def test_native_readouts_and_fifo_shift_factor_through_four_points_and_one_direction(
    length, kick
):
    # Fixed dyadic non-orbit points; no gains assigned to the pending candidate.
    positions = np.array(
        [[0.75, 0, 0.25], [0, -0.5, -0.125], [-1, 0.125, 0.25], [0.25, 0.75, -0.125]]
    )
    old_direction = np.array([0.5, -0.5, 0.5])
    old_direction /= np.linalg.norm(old_direction)
    lifted = np.vstack([positions, positions[-1] - length * old_direction])
    original_directions = _directions(lifted)
    active_directions = np.vstack([_directions(positions), old_direction])
    kick = np.asarray(kick)
    head = _head(positions, original_directions, kick)
    active_head = _head(positions, active_directions, kick)
    np.testing.assert_allclose(head, active_head, atol=2e-16)
    np.testing.assert_allclose(
        _field(positions, original_directions, np.array([0.3, -0.4, 0.9])),
        _field(positions, active_directions, np.array([0.3, -0.4, 0.9])),
        atol=2e-16,
    )
    moved = np.vstack([head, lifted[:-1]])
    native_positions, native_directions, filled = update_vector_history(
        positions.copy(),
        original_directions.copy(),
        head,
        normalize_orientation(head - positions[0]),
        4,
    )
    assert filled == 4
    np.testing.assert_array_equal(native_positions, moved[:4])
    np.testing.assert_allclose(native_directions, _directions(moved), atol=2e-16)
    np.testing.assert_allclose(native_directions[-1], active_directions[2], atol=2e-16)
    flipped = active_directions.copy()
    flipped[-1] *= -1
    assert np.linalg.norm(_head(positions, flipped, kick) - active_head) > 0.01


@pytest.mark.parametrize("phase", range(4))
def test_shared_active_triangle_bounds_pose_change_with_exact_reference_eigenvalues(
    phase,
):
    r, h = 0.8, 0.2
    times = phase - np.arange(4)
    old_ref = _orbit(times, r, h)
    next_ref = _orbit(times + 1, r, h)
    shared = old_ref[:3]
    centroid = shared.mean(axis=0)
    centered = shared - centroid
    eigenvalues = np.linalg.eigvalsh(centered.T @ centered)
    np.testing.assert_allclose(
        eigenvalues, [0, 2 * (r**2 + 4 * h**2) / 3, 2 * r**2], atol=2e-16
    )
    q_old = Rotation.from_rotvec([0.21, -0.13, 0.34]).as_matrix()
    q_new = Rotation.from_rotvec([-0.09, 0.04, 0.26]).as_matrix()
    t_old = np.array([0.1, -0.2, 0.3])
    t_new = np.array([0.27, -0.14, 0.19])
    # Exactly shared points, approached by two distinct poses.
    real_shared = 0.5 * (shared @ (q_old + q_new).T + t_old + t_new)
    old = np.vstack([real_shared, old_ref[3] @ q_old.T + t_old])
    new = np.vstack([next_ref[0] @ q_new.T + t_new, real_shared])
    residual_old = np.linalg.norm(old - (old_ref @ q_old.T + t_old), axis=1).max()
    residual_new = np.linalg.norm(new - (next_ref @ q_new.T + t_new), axis=1).max()
    delta_q, delta_t = q_new - q_old, t_new - t_old
    d = residual_old + residual_new
    budget = 3 * np.linalg.norm(delta_t + delta_q @ centroid) ** 2
    budget += np.linalg.norm(centered @ delta_q.T, "fro") ** 2
    assert budget <= 3 * d**2 + 1e-16
    bound = np.sqrt(3 / eigenvalues[1]) * d
    assert np.linalg.norm(delta_q, 2) <= bound
    assert np.linalg.norm(delta_t) <= d + np.linalg.norm(centroid) * bound


@pytest.mark.parametrize("phase", range(4))
@pytest.mark.parametrize("offset", [0.0, 0.075])
def test_active_old_direction_detects_four_dimensional_hinge_and_bounds_pose(
    phase, offset
):
    r, h = 0.8, 0.2
    old_ref = np.column_stack([_orbit(phase - np.arange(4), r, h), np.zeros(4)])
    next_ref = np.roll(old_ref, 1, axis=0)
    triangle = old_ref[:3]
    _, _, frame = np.linalg.svd(triangle[1:] - triangle[0])
    u, v = frame[2:]
    c, s = np.cos(0.31), np.sin(0.31)
    delta_q = (c - 1) * (np.outer(u, u) + np.outer(v, v))
    delta_q += s * (np.outer(v, u) - np.outer(u, v))
    q = np.eye(4) + delta_q
    t = -delta_q @ triangle[0] + offset * np.array([0.1, -0.2, 0.3, 0.4])
    assert np.linalg.det(q) == pytest.approx(1)
    np.testing.assert_allclose(q @ q.T, np.eye(4), atol=3e-16)

    next_fit = next_ref @ q.T + t
    shared = (triangle + next_fit[1:]) / 2
    old = np.vstack([shared, old_ref[3] + offset * np.array([0.4, 0.3, 0.2, 0.1])])
    new = np.vstack([next_fit[0], shared])
    delta_old = np.linalg.norm(old - old_ref, axis=1).max()
    delta_new = np.linalg.norm(new - next_fit, axis=1).max()
    reference_step = old_ref[2] - old_ref[3]
    length = np.linalg.norm(reference_step)
    # The direction entering the new FIFO's oldest slot is fixed by old sites.
    actual_direction = normalize_orientation(old[2] - old[3])
    fitted_direction = q @ (reference_step / length)
    direction_error = np.linalg.norm(actual_direction - fitted_direction)
    if offset == 0:
        assert delta_old + delta_new < 2e-15
        assert direction_error > 0.01

    fourth_error = delta_new + 3 * delta_old + length * direction_error
    fourth_delta = delta_q @ old_ref[3] + t
    assert np.linalg.norm(fourth_delta) <= fourth_error + 2e-15
    budget = 3 * (delta_old + delta_new) ** 2 + fourth_error**2
    scatter = np.diag([2 * r * r, 2 * r * r, 4 * h * h, 0])
    np.testing.assert_allclose(old_ref.T @ old_ref, scatter, atol=1e-16)
    spread = np.trace(delta_q @ scatter @ delta_q.T)
    assert 4 * np.dot(t, t) + spread <= budget + 2e-15
    assert min(2 * r * r, 4 * h * h) * np.linalg.norm(delta_q, 2) ** 2 <= spread


@pytest.mark.parametrize("trace", ["kick", "drift"])
def test_full_five_point_closure_lower_bound_has_an_explicit_optimal_pose(trace):
    time = 7
    reference = _orbit(time - np.arange(5))
    v = np.array([0.1, -0.2, 0.09])
    locations = reference.copy()
    if trace == "kick":
        locations[0] += v
        fit = reference + v / 2
        expected = np.linalg.norm(v) / 2
    else:
        locations += (time - np.arange(5))[:, None] * v
        fit = reference + (time - 2) * v
        expected = 2 * np.linalg.norm(v)
    lower = np.linalg.norm(locations[0] - locations[4]) / 2
    upper = np.linalg.norm(locations - fit, axis=1).max()
    assert lower == pytest.approx(expected, abs=2e-16)
    assert upper == pytest.approx(lower, abs=2e-16)


def test_five_point_closure_is_not_inherited_by_the_active_state():
    history = _orbit(-np.arange(5))
    changed = history.copy()
    changed[4] = 2 * history[4] - history[3]
    np.testing.assert_array_equal(changed[:4], history[:4])
    np.testing.assert_allclose(_directions(changed), _directions(history), atol=1e-16)
    np.testing.assert_array_equal(history[0], history[4])
    assert np.linalg.norm(changed[0] - changed[4]) > 0.5
