"""Rigid-history compatibility controls, not new candidate or stability runs."""

from math import sqrt

import numpy as np
import pytest

from emergenz_knoten.kernels import exponential_memory_weights
from emergenz_knoten.vector_memory import (
    normalize_orientation,
    update_vector_history,
    vector_gaussian_field,
)


def _rotation(theta, axis=2):
    matrix = np.eye(3)
    plane = [j for j in range(3) if j != axis]
    c, s = np.cos(theta), np.sin(theta)
    matrix[np.ix_(plane, plane)] = [[c, -s], [s, c]]
    return matrix


def _directions(matrix, head, count):
    return np.array([np.linalg.matrix_power(matrix.T, j) @ head for j in range(count)])


def _jacobian(z, positions, directions, weights, ell):
    radial = positions - z
    factors = weights * np.exp(-np.sum(radial**2, axis=1) / (2 * ell**2))
    return np.einsum("n,ni,nj->ij", factors, directions, radial) / ell**2


def _tetrahedron():
    points = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / 2
    directions = np.array(
        [
            normalize_orientation(p - old)
            for p, old in zip(points, np.roll(points, -1, axis=0))
        ]
    )
    return points, directions


def _simplex_root(points, weights, ell):
    rhs = (np.sum(points[1:] ** 2, axis=1) - np.sum(points[0] ** 2)) / 2
    rhs -= ell**2 * np.log(weights[1:] / weights[0])
    return np.linalg.solve(points[1:] - points[0], rhs)


@pytest.mark.parametrize("axial", [0.0, 0.4, -0.4])
@pytest.mark.parametrize("theta", [0.4, 1.1])
def test_single_rotation_obeys_fifo_shift_but_has_fixed_axial_projection(axial, theta):
    matrix = _rotation(theta)
    head = np.array([sqrt(1 - axial**2), 0, axial])
    directions = _directions(matrix, head, 6)
    # Direction-only control: no claim that arbitrary positions solve a native orbit.
    positions = np.column_stack([np.arange(6), np.zeros((6, 2))])
    _, after, _ = update_vector_history(
        positions.copy(), directions.copy(), np.array([2, 1, 0]), matrix @ head, 6
    )
    np.testing.assert_allclose(after, directions @ matrix.T, atol=3e-16)
    np.testing.assert_allclose(directions[:, 2], axial, atol=1e-16)
    weights = exponential_memory_weights(0.2, 6, memory_mass=1.3)
    z, ell = np.array([0.3, -0.2, 0.4]), 1.2
    value = vector_gaussian_field(z, positions, directions, weights, sigma=ell)
    total = np.sum(
        weights * np.exp(-np.sum((z - positions) ** 2, axis=1) / (2 * ell**2))
    )
    assert value[2] == pytest.approx(axial * total, abs=2e-16)
    jacobian = _jacobian(z, positions, directions, weights, ell)
    if axial:
        assert value[2] * axial > 0
    else:
        np.testing.assert_array_equal(jacobian[2], 0)
        assert np.linalg.matrix_rank(jacobian) <= 2


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_projected_shift_identity_holds_for_arbitrary_native_directions(axis):
    _, directions = _tetrahedron()
    matrix = _rotation(0.7, axis)
    residual = directions[:-1] - directions[1:] @ matrix.T
    np.testing.assert_allclose(
        residual[:, axis], np.diff(-directions[:, axis]), atol=2e-16
    )


def test_known_improper_four_cycle_is_not_excluded_by_proper_rotation_theorem():
    points, directions = _tetrahedron()
    matrix = np.array([[0, 0, -1], [0, -1, 0], [1, 0, 0]])
    assert np.linalg.det(matrix) == -1
    assert np.linalg.matrix_rank(np.eye(3) - matrix) == 3
    np.testing.assert_array_equal(np.linalg.matrix_power(matrix, 4), np.eye(3))
    np.testing.assert_allclose(directions[1:] @ matrix.T, directions[:-1], atol=1e-16)
    np.testing.assert_array_equal(points[1:] @ matrix.T, points[:-1])
    assert np.linalg.matrix_rank(directions) == 3
    proper = matrix @ matrix
    assert np.linalg.det(proper) == 1
    assert np.linalg.matrix_rank(np.eye(3) - proper) == 2
    np.testing.assert_allclose(directions[2:] @ proper.T, directions[:-2], atol=1e-16)
    np.testing.assert_allclose(
        directions[:, 1], [1, -1, 1, -1] / np.sqrt(2), atol=1e-16
    )


@pytest.mark.parametrize("q", [0.4, 0.5, 0.8])
def test_two_temporal_classes_balance_at_known_native_readout_zero(q):
    points, directions = _tetrahedron()
    ell = 1.1
    weights = exponential_memory_weights(1 - q, 4, memory_mass=1.7)
    root = _simplex_root(points, weights, ell)
    coefficients = weights * np.exp(
        -np.sum((root - points) ** 2, axis=1) / (2 * ell**2)
    )
    np.testing.assert_allclose(coefficients @ directions, 0, atol=3e-16)
    even, odd = coefficients[::2].sum(), coefficients[1::2].sum()
    assert even / odd == pytest.approx(-directions[1, 1] / directions[0, 1], rel=2e-14)
    assert np.linalg.det(_jacobian(root, points, directions, weights, ell)) > 0


@pytest.mark.parametrize("q", [0.4, 0.8])
@pytest.mark.parametrize("axis", [0, 1, 2])
def test_near_rotation_reserve_bound_at_known_regular_zero(q, axis):
    points, directions = _tetrahedron()
    ell, matrix = 1.1, _rotation(0.7, axis)
    weights = exponential_memory_weights(1 - q, 4, memory_mass=1.7)
    root = _simplex_root(points, weights, ell)
    coefficients = weights * np.exp(
        -np.sum((root - points) ** 2, axis=1) / (2 * ell**2)
    )
    beta = coefficients / coefficients.sum()
    assert beta @ directions[:, axis] == pytest.approx(0, abs=3e-15)
    residual = directions[:-1] - directions[1:] @ matrix.T
    axial_error = np.sum(np.abs(residual[:, axis]))
    assert np.max(np.abs(directions[:, axis])) <= axial_error
    jacobian = _jacobian(root, points, directions, weights, ell)
    reserve = np.linalg.svd(jacobian, compute_uv=False)[-1]
    bound = weights.sum() * axial_error / (ell * np.sqrt(np.e))
    assert reserve > 0
    assert reserve <= np.linalg.norm(jacobian[axis]) + 3e-16
    assert np.linalg.norm(jacobian[axis]) <= bound
    assert np.linalg.norm(residual, axis=1).max() >= reserve * ell * np.sqrt(np.e) / (
        weights.sum() * 3
    )
    # Scaling the field cannot evade a reserve expressed relative to total weight.
    scaled = _jacobian(root, points, directions, 0.01 * weights, ell)
    assert np.linalg.svd(scaled, compute_uv=False)[-1] / (
        0.01 * weights.sum()
    ) == pytest.approx(reserve / weights.sum(), rel=2e-14)


@pytest.mark.parametrize(
    "ordering", [np.arange(6), np.arange(6)[::-1], [0, 2, 4, 1, 3, 5]]
)
def test_distinct_axis_levels_cannot_be_one_rigid_fifo_chain(ordering):
    # Generic geometric control, not a reproduction of literature coupling weights.
    r, h = sqrt(3) / 2, 0.5
    directions = np.array(
        [[r, 0, h], [-r, 0, h], [0, r, -h], [0, -r, -h], [0, 0, 1], [0, 0, -1]]
    )[ordering]
    matrix = _rotation(0.4)
    residual = directions[:-1] - directions[1:] @ matrix.T
    assert np.linalg.matrix_rank(directions) == 3
    # Any ordering must traverse the full range along its finite chain.
    assert np.abs(residual[:, 2]).sum() >= np.ptp(directions[:, 2])
    assert np.max(np.abs(residual[:, 2])) >= np.ptp(directions[:, 2]) / 5


def test_even_dimension_has_no_automatic_fixed_axis():
    # Algebraic boundary of the theorem, not a new native orbit candidate.
    matrix = np.zeros((4, 4))
    for offset, angle in ((0, 2 * np.pi / 5), (2, 4 * np.pi / 5)):
        c, s = np.cos(angle), np.sin(angle)
        matrix[offset : offset + 2, offset : offset + 2] = [[c, -s], [s, c]]
    assert np.linalg.det(matrix) == pytest.approx(1)
    assert np.linalg.matrix_rank(np.eye(4) - matrix) == 4
    directions = _directions(matrix, np.array([1, 0, 1, 0]) / sqrt(2), 5)
    assert np.linalg.matrix_rank(directions) == 4
    np.testing.assert_allclose(directions.sum(axis=0), 0, atol=2e-15)


def test_projection_dimension_requires_enough_temporal_classes():
    # Affine rank, not merely linear rank, controls interior of the convex hull.
    three_classes = np.eye(3)
    assert np.linalg.matrix_rank(three_classes) == 3
    assert np.linalg.matrix_rank(three_classes[1:] - three_classes[0]) == 2
    assert np.all(three_classes @ np.ones(3) > 0)
    _, four_classes = _tetrahedron()
    assert np.linalg.matrix_rank(four_classes[1:] - four_classes[0]) == 3
    np.testing.assert_allclose(four_classes.sum(axis=0), 0, atol=1e-16)


@pytest.mark.parametrize("pitch", [0.0, 0.3, 0.8])
def test_two_phase_affine_history_has_predicted_axial_direction_classes(pitch):
    # Kinematic identity only: no native force, gain, root solve, or target run.
    rotation = _rotation(0.7)
    affine = np.eye(4)
    affine[:3, :3] = rotation
    affine[:3, 3] = [0.2, -0.1, pitch]
    first = np.array([1.0, 0.0, 0.2, 1.0])
    second = np.array([0.1, 0.8, 0.6, 1.0])
    points = np.array(
        [
            (np.linalg.matrix_power(affine, k) @ seed)[:3]
            for k in range(-2, 3)
            for seed in (first, second)
        ]
    )
    increments = np.diff(points, axis=0)
    directions = increments / np.linalg.norm(increments, axis=1)[:, None]
    delta = second[2] - first[2]
    odd_length = np.linalg.norm(second[:3] - first[:3])
    even_length = np.linalg.norm((affine @ first - second)[:3])
    np.testing.assert_allclose(directions[::2, 2], delta / odd_length, atol=4e-16)
    np.testing.assert_allclose(
        directions[1::2, 2], (pitch - delta) / even_length, atol=4e-16
    )
    np.testing.assert_allclose(
        points[2:], points[:-2] @ rotation.T + affine[:3, 3], atol=6e-16
    )
    assert (directions[0, 2] * directions[1, 2] < 0) == (delta * (pitch - delta) < 0)
