"""Fixed algebra/integral controls; no target trajectories or fitted gains."""

from itertools import product
from math import erf, exp, pi, sqrt

import numpy as np
import pytest
from scipy.integrate import quad

from emergenz_knoten.kernels import exponential_memory_weights
from emergenz_knoten.vector_memory import (
    normalize_orientation,
    update_vector_history,
    vector_gaussian_field,
)


def _history(q):
    points = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / 2
    directions = np.array(
        [
            normalize_orientation(p - old)
            for p, old in zip(points, np.roll(points, -1, axis=0))
        ]
    )
    weights = exponential_memory_weights(1 - q, 4, memory_mass=1.7)
    return points, directions, weights


def _jacobian(z, points, directions, weights, ell):
    radial = points - z
    coefficients = weights * np.exp(-np.sum(radial**2, axis=1) / (2 * ell**2))
    return np.einsum("n,ni,nj->ij", coefficients, directions, radial) / ell**2


@pytest.mark.parametrize("q", [0.4, 0.9])
@pytest.mark.parametrize("offset", [0.0, 0.2])
def test_native_source_tail_cancellation_bounds(q, offset):
    points, directions, weights = _history(q)
    ell = 1.3
    new_point = points[-1] + offset * np.array([1, -2, 1])
    new_direction = normalize_orientation(new_point - points[0])
    after_points, after_directions, _ = update_vector_history(
        points.copy(), directions.copy(), new_point, new_direction, 4
    )
    e_p = np.linalg.norm(new_direction - q**4 * directions[-1])
    d_y = np.linalg.norm(new_point - points[-1])
    l1, l2 = 1 / (ell * sqrt(exp(1))), 1 / ell**2
    bound = weights[0] * (e_p + q**4 * l1 * d_y)
    derivative_bound = weights[0] * (e_p * l1 + q**4 * l2 * d_y)
    for z in (np.zeros(3), points[-1], np.array([2, -1, 0.2])):
        before = vector_gaussian_field(z, points, directions, weights, sigma=ell)
        after = vector_gaussian_field(
            z, after_points, after_directions, weights, sigma=ell
        )
        source_tail = weights[0] * (
            new_direction * np.exp(-np.sum((z - new_point) ** 2) / (2 * ell**2))
            - q**4
            * directions[-1]
            * np.exp(-np.sum((z - points[-1]) ** 2) / (2 * ell**2))
        )
        np.testing.assert_allclose(after - q * before, source_tail, atol=3e-16)
        assert np.linalg.norm(source_tail) <= bound + 3e-16
        jac_delta = _jacobian(z, after_points, after_directions, weights, ell)
        jac_delta -= q * _jacobian(z, points, directions, weights, ell)
        assert np.linalg.norm(jac_delta, 2) <= derivative_bound + 3e-16


@pytest.mark.parametrize("q", [0.4, 0.9])
def test_geometric_center_update_uses_tail_and_finite_mass(q):
    points, directions, weights = _history(q)
    new_point = points[0] + [0.2, -0.3, 0.1]
    after_points, _, _ = update_vector_history(
        points.copy(),
        directions.copy(),
        new_point,
        normalize_orientation(new_point - points[0]),
        4,
    )
    center = weights @ points / weights.sum()
    actual = weights @ after_points / weights.sum()
    predicted = q * center + weights[0] / weights.sum() * (
        new_point - q**4 * points[-1]
    )
    np.testing.assert_allclose(actual, predicted, atol=3e-16)
    assert weights.sum() == pytest.approx(1.7 * (1 - q**4))


@pytest.mark.parametrize("delta", [1e-3, 1e-6])
def test_small_native_alignment_gain_does_not_make_deposition_small(delta):
    points, directions, weights = _history(0.7)
    ell = 1.2
    force = vector_gaussian_field(points[0], points, directions, weights, sigma=ell)
    new_point = points[0] + delta * force
    new_direction = normalize_orientation(new_point - points[0])
    positive_points, positive_directions, _ = update_vector_history(
        points.copy(), directions.copy(), new_point, new_direction, 4
    )
    zero_points, zero_directions, _ = update_vector_history(
        points.copy(),
        directions.copy(),
        points[0],
        normalize_orientation(np.zeros(3)),
        4,
    )
    z = np.zeros(3)
    difference = vector_gaussian_field(
        z, positive_points, positive_directions, weights, sigma=ell
    )
    difference -= vector_gaussian_field(
        z, zero_points, zero_directions, weights, sigma=ell
    )
    predicted_limit = (
        weights[0]
        * normalize_orientation(force)
        * np.exp(-np.sum((z - points[0]) ** 2) / (2 * ell**2))
    )
    error_bound = weights[0] / (ell * sqrt(exp(1))) * delta * np.linalg.norm(force)
    assert np.linalg.norm(difference - predicted_limit) <= error_bound + 2e-10
    assert np.linalg.norm(difference) > 0.3
    np.testing.assert_array_equal(zero_directions[0], 0)


@pytest.mark.parametrize("curvature", [0.0, 0.3])
@pytest.mark.parametrize("index", [-1, 1])
def test_local_certificate_bounds_known_synthetic_root_and_index(curvature, index):
    # This analytic polynomial control is not a native memory orbit.
    q, a, radius = 0.8, 2.0, 0.2
    old_jac = np.diag([3.0, 2.0, index * 2.0])
    matrix = q * old_jac
    root = np.array([0.01, -0.02, 0.03])
    center = np.array([0.005, 0, 0])
    displacement = center - root
    field_at_center = (
        matrix @ displacement + curvature * (displacement @ displacement) * np.eye(3)[0]
    )
    error = 2 * curvature * np.linalg.norm(displacement)
    hessian = 2 * curvature
    kappa = (error + hessian * radius) / (q * a)
    b = np.linalg.norm(field_at_center) / (q * a)
    assert kappa < 1 and b + kappa * radius < radius
    assert np.linalg.norm(root - center) <= b / (1 - kappa)
    assert np.linalg.slogdet(matrix)[0] == np.linalg.slogdet(old_jac)[0] == index


@pytest.mark.parametrize(
    "b,kappa,radius", [(0.2, 0.0, 0.2), (0.0, 1.0, 0.2), (0.1, 0.6, 0.2)]
)
def test_strict_local_certificate_rejects_boundary_and_excess(b, kappa, radius):
    assert not (kappa < 1 and b + kappa * radius < radius)


@pytest.mark.parametrize("q", [0.4, 0.9])
def test_iid_unit_filter_second_moment_by_exact_sign_enumeration(q):
    # Signs of independent one-dimensional centered Gaussians are iid fair signs.
    weights = exponential_memory_weights(1 - q, 4, memory_mass=1.7)
    sums = np.array([weights @ signs for signs in product([-1, 1], repeat=4)])
    assert np.mean(sums) == pytest.approx(0, abs=1e-16)
    finite_variance = weights @ weights
    assert np.mean(sums**2) == pytest.approx(finite_variance, rel=2e-15)
    assert finite_variance == pytest.approx(1.7**2 * (1 - q) / (1 + q) * (1 - q**8))
    assert sqrt(finite_variance) <= 1.7 * sqrt((1 - q) / (1 + q))


@pytest.mark.parametrize("a", [0.0, 0.2, -0.7])
def test_gaussian_unit_direction_mean_bound_in_one_dimension(a):
    exact_mean = erf(a / sqrt(2))
    assert abs(exact_mean) <= abs(a)


@pytest.mark.parametrize("z", [0.0, 0.8, -0.8])
@pytest.mark.parametrize("epsilon", [0.05, 0.2])
def test_correlated_direction_and_new_position_gaussian_integral(z, epsilon):
    ell = 1.3
    scale = sqrt(ell**2 + epsilon**2)
    prefactor = ell / scale * exp(-(z**2) / (2 * scale**2))
    argument = z * epsilon / (sqrt(2) * ell * scale)
    exact = prefactor * erf(argument)
    exact_derivative = -z / scale**2 * exact
    exact_derivative += (
        prefactor * sqrt(2 / pi) * epsilon / (ell * scale) * exp(-(argument**2))
    )

    def integrand(xi, derivative=False):
        delta = z - epsilon * xi
        value = exp(-(xi**2) / 2 - delta**2 / (2 * ell**2)) / sqrt(2 * pi)
        value *= 1 if xi > 0 else -1
        return value * (-delta / ell**2 if derivative else 1)

    for derivative, expected in ((False, exact), (True, exact_derivative)):
        numerical = sum(
            quad(integrand, lower, upper, args=(derivative,), epsabs=1e-12)[0]
            for lower, upper in ((-np.inf, 0), (0, np.inf))
        )
        assert numerical == pytest.approx(expected, abs=2e-13)
    assert abs(exact) <= epsilon / (ell * sqrt(exp(1)))
    assert abs(exact_derivative) <= epsilon / ell**2
    if z != 0:
        assert exact * z > 0  # Zero drift does not make E[p G] vanish.


def test_initial_memory_remnant_is_not_part_of_generated_martingale_sum():
    q, ell = 0.8, 1.2
    points, directions, weights = _history(q)
    pushed_points, pushed_directions, _ = update_vector_history(
        points.copy(), directions.copy(), points[0], np.zeros(3), 4
    )
    z = points[1]
    remainder = q * vector_gaussian_field(
        z, points[:-1], directions[:-1], weights[:-1], sigma=ell
    )
    actual = vector_gaussian_field(
        z, pushed_points, pushed_directions, weights, sigma=ell
    )
    np.testing.assert_allclose(actual, remainder, atol=3e-16)
    assert np.linalg.norm(actual) > 0.1
