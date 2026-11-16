"""Static charts and analytic bounds only; no native orbit or target evaluation."""

from fractions import Fraction
from math import exp, log, sqrt

import numpy as np
import pytest

from emergenz_knoten.vector_memory import normalize_orientation, vector_gaussian_field


def _history():
    # The existing off-orbit geometry, with no gains or force-balance assignment.
    return np.array(
        [[0.8, 0, 0.3], [0, -0.8, -0.3], [-0.8, 0, 0.3], [0, 0.8, -0.3], [0.8, 0, 0.3]]
    )


def _split(history):
    centered = history - history[0]
    first = normalize_orientation(centered[1])
    second = normalize_orientation(centered[2] - (centered[2] @ first) * first)
    frame = np.column_stack([first, second, np.cross(first, second)])
    local = centered @ frame
    shape = np.concatenate([local[1, :1], local[2, :2], local[3:].ravel()])
    return history[0], frame, shape


def _join(center, frame, shape):
    local = np.zeros((5, 3))
    local[1, 0] = shape[0]
    local[2, :2] = shape[1:3]
    local[3:] = shape[3:].reshape(2, 3)
    return center + local @ frame.T


@pytest.mark.parametrize("phase", range(4))
def test_proper_frame_chart_retains_all_nine_shape_coordinates(phase):
    symmetry = np.array([[0, -1, 0], [1, 0, 0], [0, 0, -1]])
    history = _history() @ np.linalg.matrix_power(symmetry, phase).T
    history[-1] += [0.02, -0.03, 0.01]
    center, frame, shape = _split(history)
    assert shape.shape == (9,)
    assert np.linalg.det(frame) == pytest.approx(1)
    np.testing.assert_allclose(_join(center, frame, shape), history, atol=5e-16)


def test_chart_is_invariant_under_proper_rigid_motion_not_reflection():
    history = _history()
    history[-1] += [0.02, -0.03, 0.01]
    _, frame, shape = _split(history)
    rotation = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    moved = history @ rotation.T + [2, -3, 1]
    _, moved_frame, moved_shape = _split(moved)
    np.testing.assert_allclose(moved_frame, rotation @ frame, atol=6e-16)
    np.testing.assert_allclose(moved_shape, shape, atol=6e-16)
    reflection = np.diag([1, 1, -1])
    _, _, reflected_shape = _split(history @ reflection)
    expected = shape.copy()
    expected[[5, 8]] *= -1
    np.testing.assert_allclose(reflected_shape, expected, atol=5e-16)
    assert abs(shape[5]) > 0.1


def test_chart_rank_removes_exactly_six_rigid_directions():
    history = _history()
    machine_epsilon = np.finfo(float).eps
    step = np.cbrt(machine_epsilon)
    # Diagnostic balance of central truncation O(h^2) and roundoff O(eps/h).
    tolerance = 32 * (step**2 + machine_epsilon / step)
    derivative = np.column_stack(
        [
            (
                _split(history + step * basis.reshape(5, 3))[2]
                - _split(history - step * basis.reshape(5, 3))[2]
            )
            / (2 * step)
            for basis in np.eye(15)
        ]
    )
    assert np.linalg.matrix_rank(derivative, tol=1e-7) == 9
    for axis in np.eye(3):
        np.testing.assert_allclose(derivative @ np.tile(axis, 5), 0, atol=tolerance)
    for axis in np.eye(3):
        tangent = np.cross(axis, history)
        np.testing.assert_allclose(derivative @ tangent.ravel(), 0, atol=tolerance)


def test_oldest_length_is_a_shape_coordinate_even_when_readout_forgets_it():
    history = _history()
    changed = history.copy()
    changed[-1] = history[-2] + 1.2 * (history[-1] - history[-2])
    assert np.linalg.norm(_split(changed)[2] - _split(history)[2]) > 0.1
    before = np.array([normalize_orientation(s) for s in np.diff(-history, axis=0)])
    after = np.array([normalize_orientation(s) for s in np.diff(-changed, axis=0)])
    np.testing.assert_allclose(after, before, atol=3e-16)
    np.testing.assert_array_equal(changed[:4], history[:4])


@pytest.mark.parametrize("retention", [Fraction(0), Fraction(1, 2)])
def test_singular_nonnormal_matrix_has_exact_lyapunov_metric(retention):
    # Pure algebra: A=[[0,2],[0,t]], P=diag(1,5/(1-t^2)).
    diagonal = Fraction(5) / (1 - retention**2)
    assert 4 + retention**2 * diagonal - diagonal == -1
    assert Fraction(1) - 1 / diagonal < 1
    matrix = np.array([[0, 2], [0, float(retention)]])
    metric = np.diag([1, float(diagonal)])
    np.testing.assert_allclose(matrix.T @ metric @ matrix - metric, -np.eye(2))
    assert np.linalg.norm(matrix, 2) > 1
    assert np.linalg.det(matrix) == 0
    direction = np.array([0, 1])
    moved = matrix @ direction
    assert moved @ metric @ moved < direction @ metric @ direction


def test_small_spectrum_is_not_a_finite_radius_certificate():
    # A stable derivative does not fix a usable radius for the nonlinear map.
    x = Fraction(1, 100)
    assert Fraction(1, 2) < 1
    assert x / 2 + 100 * x**2 > x


def _field_data(history):
    directions = np.array([normalize_orientation(s) for s in np.diff(-history, axis=0)])
    weights = 0.1 * 0.9 ** np.arange(4)
    return directions, weights


def _jacobian(z, history):
    directions, weights = _field_data(history)
    radial = history[:4] - z
    coefficients = weights * np.exp(-np.sum(radial**2, axis=1) / 2)
    return np.einsum("n,ni,nj->ij", coefficients, directions, radial)


@pytest.mark.parametrize("sign", [-1, 1])
def test_static_history_perturbations_obey_field_and_derivative_bounds(sign):
    history = _history()
    perturbation = (
        sign
        * 1e-4
        * np.array([[1, 0, 1], [0, -1, 0], [1, 1, 0], [-1, 0, 1], [0, 1, -1]])
    )
    changed = history + perturbation
    delta = np.max(np.linalg.norm(perturbation, axis=1))
    length = np.linalg.norm(history[0] - history[1])
    assert delta < length / 4
    directions, weights = _field_data(history)
    new_directions, _ = _field_data(changed)
    c_zero = weights.sum() * (4 / length + 1 / sqrt(exp(1)))
    c_one = weights.sum() * (4 / (length * sqrt(exp(1))) + 1)
    for z in [np.zeros(3), history[0], np.array([2, -1, 0.5])]:
        before = vector_gaussian_field(z, history[:4], directions, weights, sigma=1)
        after = vector_gaussian_field(z, changed[:4], new_directions, weights, sigma=1)
        assert np.linalg.norm(after - before) <= c_zero * delta
        assert (
            np.linalg.norm(_jacobian(z, changed) - _jacobian(z, history), 2)
            <= c_one * delta
        )


@pytest.mark.parametrize("log_q", [-0.05, -0.1])
def test_static_defect_clearance_equals_barycentric_distance_to_faces(log_q):
    radius, height = 0.8, 0.3
    points = _history()[:4]
    root = np.array([log_q / radius, -log_q / radius, log_q / (2 * height)])
    homogeneous = np.vstack([points.T, np.ones(4)])
    barycentric = np.linalg.solve(homogeneous, np.append(root, 1))
    gradients = np.linalg.inv(homogeneous)[:, :3]
    distances = barycentric / np.linalg.norm(gradients, axis=1)
    smallest = 0.25 + log_q / (8 * height**2) + log_q / (2 * radius**2)
    predicted = smallest * 4 * radius * height / sqrt(radius**2 + 4 * height**2)
    assert predicted > 0
    assert distances.min() == pytest.approx(predicted)


def test_static_inner_defect_has_nonzero_joint_reserve_without_any_gains():
    history = _history()
    radius, height = 0.8, 0.3
    u = log(0.9)
    root = np.array([u / radius, -u / radius, u / (2 * height)])
    directions, weights = _field_data(history)
    np.testing.assert_allclose(
        vector_gaussian_field(root, history[:4], directions, weights, sigma=1),
        0,
        atol=5e-17,
    )
    length = np.linalg.norm(history[0] - history[1])
    c = weights[0] * exp(-(np.linalg.norm(root - history[0]) ** 2) / 2)
    reserve = 8 * c * height**2 / length
    assert np.linalg.svd(_jacobian(root, history), compute_uv=False)[
        -1
    ] == pytest.approx(reserve)
    clearance = (
        (0.25 + u / (8 * height**2) + u / (2 * radius**2))
        * 4
        * radius
        * height
        / sqrt(radius**2 + 4 * height**2)
    )
    ball, delta = clearance / 4, 1e-6
    c_zero = weights.sum() * (4 / length + 1 / sqrt(exp(1)))
    c_one = weights.sum() * (4 / (length * sqrt(exp(1))) + 1)
    kappa = (c_one * delta + weights.sum() * ball) / reserve
    residual_bound = c_zero * delta / reserve
    assert delta < length / 4
    assert kappa < 1 and residual_bound + kappa * ball < ball
    assert ball + delta < clearance


def test_bounded_reduced_error_requires_a_margin_and_not_just_kappa_below_one():
    kappa, radius = Fraction(3, 4), Fraction(1, 10)
    admissible = Fraction(1, 100)
    excessive = Fraction(3, 100)
    assert kappa * radius + admissible < radius
    assert kappa * radius + excessive > radius
