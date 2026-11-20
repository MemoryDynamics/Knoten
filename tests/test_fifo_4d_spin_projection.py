"""Real-coordinate reference and static embedding identities, not target runs."""

import numpy as np
import pytest

from emergenz_knoten.kernels import double_gaussian_gradient
from emergenz_knoten.vector_memory import normalize_orientation, vector_gaussian_field
from experiments.current.reference.fifo_4d_spin_projection import (
    GENERATORS,
    INITIAL,
    INTERNAL_STEP,
    direction_readout,
    fifo_reference,
    real_orbit,
    real_rotation,
)


def test_real_generators_have_exact_quaternion_algebra():
    identity = np.eye(4, dtype=int)
    for index, generator in enumerate(GENERATORS):
        np.testing.assert_array_equal(generator.T, -generator)
        np.testing.assert_array_equal(generator @ generator, -identity)
        next_generator = GENERATORS[(index + 1) % 3]
        third = GENERATORS[(index + 2) % 3]
        np.testing.assert_array_equal(generator @ next_generator, third)
        np.testing.assert_array_equal(next_generator @ generator, -third)


@pytest.mark.parametrize("axis", [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 2, -3]])
def test_rotation_and_readout_are_covariant_about_multiple_axes(axis):
    axis = np.asarray(axis, dtype=float)
    axis /= np.linalg.norm(axis)
    angle = 0.73
    rotation = real_rotation(axis, angle)
    state = np.array([1, 2, 3, -4], dtype=float) / np.sqrt(30)
    direction = direction_readout(state)
    rodrigues = (
        direction * np.cos(angle)
        + np.cross(axis, direction) * np.sin(angle)
        + axis * np.dot(axis, direction) * (1 - np.cos(angle))
    )
    np.testing.assert_allclose(rotation.T @ rotation, np.eye(4), atol=4e-16)
    np.testing.assert_allclose(
        direction_readout(rotation @ state), rodrigues, atol=5e-16
    )
    np.testing.assert_allclose(real_rotation(axis, 2 * np.pi), -np.eye(4), atol=2e-16)
    np.testing.assert_allclose(real_rotation(axis, 4 * np.pi), np.eye(4), atol=3e-16)


@pytest.mark.parametrize("alpha", [0, 0.19, np.pi / 4, np.pi / 2, np.pi, 2 * np.pi])
def test_double_angle_follows_from_chosen_quadratic_readout(alpha):
    state = real_orbit(alpha)
    np.testing.assert_allclose(
        state, real_rotation([0, 0, 1], 2 * alpha) @ INITIAL, atol=4e-16
    )
    assert np.dot(state, state) == pytest.approx(1)
    np.testing.assert_allclose(
        direction_readout(state), [np.cos(2 * alpha), np.sin(2 * alpha), 0], atol=8e-16
    )


def test_entire_reference_fifo_negates_after_four_steps_and_returns_after_eight():
    initial = fifo_reference(0)
    np.testing.assert_allclose(fifo_reference(4), -initial, atol=5e-16)
    np.testing.assert_allclose(fifo_reference(8), initial, atol=9e-16)
    for step in range(8):
        state, next_state = fifo_reference(step), fifo_reference(step + 1)
        np.testing.assert_array_equal(next_state[1:], state[:-1])
        np.testing.assert_allclose(
            next_state[0],
            real_rotation([0, 0, 1], 2 * INTERNAL_STEP) @ state[0],
            atol=6e-16,
        )
    np.testing.assert_allclose(
        direction_readout(fifo_reference(4)), direction_readout(initial), atol=1e-15
    )
    assert np.linalg.norm(fifo_reference(4)[:, :3] - initial[:, :3]) > 1


def test_readout_has_whole_phase_fibers_not_only_two_preimages():
    state = np.array([1, 2, -3, 4], dtype=float)
    phase = 0.31
    c, s = np.cos(phase), np.sin(phase)
    common_phase = np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, c, -s], [0, 0, s, c]])
    np.testing.assert_allclose(
        direction_readout(common_phase @ state), direction_readout(state), atol=3e-16
    )
    np.testing.assert_array_equal(direction_readout(-state), direction_readout(state))
    with pytest.raises(ValueError):
        direction_readout(np.zeros(4))


@pytest.mark.parametrize("normal", [-1.3, 0, 0.8])
def test_embedded_native_gaussian_vector_field_factorizes(normal):
    # Fixed off-orbit history, with no assigned orbit gains or stability calculation.
    history = np.array(
        [
            [0.7, 0, 0.2],
            [0, -0.5, -0.1],
            [-0.6, 0, 0.3],
            [0, 0.8, -0.2],
            [0.2, 0.1, 0.4],
        ]
    )
    directions = np.array(
        [normalize_orientation(step) for step in history[:-1] - history[1:]]
    )
    weights, sigma = np.array([0.3, 0.2, 0.13, 0.07]), 1.1
    point = np.array([0.1, -0.3, 0.2])
    field = vector_gaussian_field(point, history[:-1], directions, weights, sigma=sigma)
    embedded = vector_gaussian_field(
        np.append(point, normal),
        np.column_stack([history[:-1], np.zeros(4)]),
        np.column_stack([directions, np.zeros(4)]),
        weights,
        sigma=sigma,
    )
    expected = np.append(np.exp(-(normal**2) / (2 * sigma**2)) * field, 0)
    np.testing.assert_allclose(embedded, expected, rtol=1e-14, atol=1e-17)


def test_native_delta_gradient_commutes_with_isometric_embedding():
    points = np.array([[0.2, 0.3, -0.4], [-0.1, 0.5, 0.7], [0.8, -0.2, 0.1]])
    point, weights = np.array([0.1, -0.2, 0.3]), np.array([0.4, 0.2, 0.1])
    kernel = dict(sigma_rep=0.7, sigma_att=1.2, amplitude_rep=0.8, amplitude_att=0.5)
    three = double_gaussian_gradient(point, points, weights, **kernel)
    four = double_gaussian_gradient(
        np.append(point, 0), np.column_stack([points, np.zeros(3)]), weights, **kernel
    )
    np.testing.assert_allclose(four, np.append(three, 0), atol=2e-17)


def test_four_distinct_points_have_at_most_three_affine_directions_even_in_4d():
    points = np.eye(4)
    assert np.linalg.matrix_rank(points) == 4
    assert np.linalg.matrix_rank(points - points[0]) == 3
    np.testing.assert_array_equal((points - points[0]) @ np.ones(4), 0)


def test_padding_a_four_cycle_does_not_change_its_exact_period():
    points = np.array([[1, 0, 1], [0, 1, -1], [-1, 0, 1], [0, -1, -1]])
    embedded = np.column_stack([points, np.zeros(4)])
    for shift in (1, 2, 3):
        assert not np.array_equal(np.roll(embedded, shift, axis=0), embedded)
    np.testing.assert_array_equal(np.roll(embedded, 4, axis=0), embedded)
