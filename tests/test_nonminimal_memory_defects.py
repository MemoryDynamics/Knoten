"""Fixed history/readout controls, not trajectories or a root/parameter search."""

from fractions import Fraction as F
from math import factorial

import numpy as np
import pytest

from emergenz_knoten.kernels import exponential_memory_weights
from emergenz_knoten.state import FiniteMemoryState
from emergenz_knoten.vector_memory import (
    oriented_history_from_state,
    vector_gaussian_field,
)


Q = 0.99
RADIUS = 1 / 6


def _vertices():
    return np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)


def _history(kind):
    vertices = _vertices()
    if kind == "negative":
        history = np.empty((9, 3))
        history[:8:2] = vertices
        history[1:8:2] = 5 * vertices
        history[8] = vertices[0]
        return history
    if kind == "positive":
        return vertices[np.arange(9) % 4]
    raise ValueError("unknown constructed history")


def _readout(history):
    state = FiniteMemoryState(
        x=history[0],
        memory=history,
        weights=exponential_memory_weights(1 - Q, len(history), memory_mass=1),
    )
    return oriented_history_from_state(state, mode="unit")


def _field(point, positions, directions, weights):
    return vector_gaussian_field(point, positions, directions, weights, sigma=1)


def _jacobian(point, positions, directions, weights):
    radial = positions - point
    factors = weights * np.exp(-np.sum(radial**2, axis=1) / 2)
    return np.einsum("n,ni,nj->ij", factors, directions, radial)


def _exp_lower(value, order):
    return sum(value**k / factorial(k) for k in range(order + 1))


def test_tetrahedron_identities_have_integer_certificates():
    vertices = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
    np.testing.assert_array_equal(vertices.sum(axis=0), 0)
    np.testing.assert_array_equal(vertices.T @ vertices, 4 * np.eye(3, dtype=int))
    np.testing.assert_array_equal(vertices @ vertices.T, 4 * np.eye(4, dtype=int) - 1)
    assert F(88, 3) < 6**2


@pytest.mark.parametrize("kind", ["negative", "positive"])
def test_histories_are_closed_and_use_native_unnormalized_age_weights(kind):
    history = _history(kind)
    positions, directions, weights = _readout(history)
    np.testing.assert_array_equal(history[0], history[-1])
    np.testing.assert_array_equal(positions, history[:-1])
    chords = history[:-1] - history[1:]
    assert np.all(np.linalg.norm(chords, axis=1) > 0)
    np.testing.assert_allclose(
        directions, chords / np.linalg.norm(chords, axis=1)[:, None], atol=1e-15
    )
    np.testing.assert_allclose(weights, (1 - Q) * Q ** np.arange(8), rtol=2e-15)
    assert weights.sum() == pytest.approx(1 - Q**8)
    assert weights.sum() < 0.08


def _scaled_radial(history, weights, direction, distance):
    sites = history[:-1]
    chord_norm = np.linalg.norm(sites - history[1:], axis=1)
    projection = sites @ direction
    deficits = distance * (projection.max() - projection)
    coefficients = weights * np.exp(-np.sum(sites**2, axis=1) / 2) / chord_norm
    return np.sum(coefficients * np.exp(-deficits) * (np.roll(deficits, -1) - deficits))


def test_scaled_radial_identity_matches_native_field_without_losing_its_sign():
    history = _history("negative")
    points, directions, weights = _readout(history)
    direction = np.array([1, 0.1, -0.2]) / np.sqrt(1.05)
    distance = 7.0
    direct = direction @ _field(distance * direction, points, directions, weights)
    factor = distance * np.exp(distance**2 / 2 - distance * (points @ direction).max())
    assert _scaled_radial(history, weights, direction, distance) == pytest.approx(
        factor * direct, rel=1e-13
    )


def test_positive_weights_do_not_force_outward_field_at_every_finite_radius():
    history = np.array([[2, 0, 0], [1, 1, 0], [-1, 0, 1], [0, 0, 0], [2, 0, 0]])
    sites = history[:-1]
    chord_norm = np.linalg.norm(sites - history[1:], axis=1)
    weights = (
        np.array([1, 0.2, 2, 8]) * chord_norm * np.exp(np.sum(sites**2, axis=1) / 2)
    )
    assert _scaled_radial(history, weights, [1, 0, 0], 0.1) < 0
    assert _scaled_radial(history, weights, [1, 0, 0], 4) > 0


def test_closed_opposite_cores_keep_their_margins_under_a_fixed_separation():
    separation = 20
    maximum_source_radius = 5
    negative_history = _history("negative")
    positive_history = _history("positive")
    _, _, weights = _readout(negative_history)
    source_bound = len(weights) * weights[0]
    cross_bound = source_bound * np.exp(
        -((separation - RADIUS - maximum_source_radius) ** 2) / 2
    )
    negative_margin = weights[0] * (41 / 6000)
    positive_margin = weights[0] / 20
    assert cross_bound < min(negative_margin, positive_margin)

    direction = np.array([0, 0, 1])
    for history, margin, sign in (
        (negative_history, negative_margin, -1),
        (positive_history, positive_margin, 1),
    ):
        native = _field(RADIUS * direction, *_readout(history))
        assert np.linalg.norm(native) > margin
        assert sign * (native @ direction) > cross_bound


def test_full_dimensional_open_chain_can_have_no_defect():
    history = np.array([[3, 0, 0], [2, 1, 0], [1, 0, 1], [0, 0, 0], [-1, 0, 0]])
    points, directions, weights = _readout(history)
    assert np.linalg.matrix_rank(points[1:] - points[0]) == 3
    assert np.all(directions[:, 0] > 0)
    assert np.all(weights > 0)


def test_negative_history_directions_are_not_independent_inputs():
    positions, directions, _ = _readout(_history("negative"))
    vertices = _vertices()
    np.testing.assert_allclose(directions[::2], -vertices, atol=2e-16)
    expected_far = (5 * vertices - np.roll(vertices, -1, axis=0)) / np.sqrt(88 / 3)
    np.testing.assert_allclose(directions[1::2], expected_far, atol=2e-16)
    np.testing.assert_allclose(np.linalg.norm(positions[::2], axis=1), 1)
    np.testing.assert_allclose(np.linalg.norm(positions[1::2], axis=1), 5)


@pytest.mark.parametrize("point", [[0, 0, 0], [1 / 6, 0, 0], [0.1, -0.05, 0.02]])
def test_reference_plus_forgetting_and_far_terms_matches_native_readout(point):
    point = np.array(point)
    positions, directions, weights = _readout(_history("negative"))
    vertices = _vertices()
    near_gaussians = np.exp(-np.sum((vertices - point) ** 2, axis=1) / 2)
    reference = -near_gaussians @ vertices
    forgetting = ((1 - Q ** (2 * np.arange(4))) * near_gaussians) @ vertices
    far = _field(point, positions[1::2], directions[1::2], Q ** (2 * np.arange(4) + 1))
    np.testing.assert_allclose(
        _field(point, positions, directions, weights) / weights[0],
        reference + forgetting + far,
        rtol=2e-14,
        atol=3e-16,
    )


def test_reference_jacobian_is_negative_isotropic():
    vertices = _vertices()
    np.testing.assert_allclose(_field(np.zeros(3), vertices, -vertices, np.ones(4)), 0)
    kappa = 4 * np.exp(-0.5) / 3
    np.testing.assert_allclose(
        _jacobian(np.zeros(3), vertices, -vertices, np.ones(4)),
        -kappa * np.eye(3),
        atol=2e-16,
    )


def test_exponential_bounds_are_certified_by_rational_series():
    # Upper tail at 1/2 uses k! >= 2*3**(k-2) for k >= 2.
    assert 1 + F(1, 2) + F(1, 8) / (1 - F(1, 6)) == F(33, 20) < F(5, 3)
    assert _exp_lower(F(1), 2) > F(9, 4)
    assert _exp_lower(F(25, 72), 2) > F(25, 18)
    assert F(841, 72) > 11
    assert _exp_lower(F(11), 16) > 40000
    assert _exp_lower(F(4), 7) > 50
    assert F(3, 50**4) < F(1, 10000)


def test_inner_boundary_and_jacobian_margins_are_strict_rationals():
    radius, kappa_lower, gaussian_hessian_upper = F(1, 6), F(4, 5), F(18, 25)
    near_t_min, near_t_max = (1 - radius) ** 2, (1 + radius) ** 2
    assert max(abs(near_t_min - 1), abs(near_t_max - 1)) < 1
    lipschitz = 4 * gaussian_hessian_upper
    reference_lower = kappa_lower * radius - lipschitz * radius**2 / 2
    assert reference_lower == F(7, 75)
    q = F(99, 100)
    forgetting_sum = sum(1 - q ** (2 * i) for i in range(4))
    bernoulli_upper = sum(2 * i * (1 - q) for i in range(4))
    assert forgetting_sum < bernoulli_upper == F(3, 25)
    perturbation_upper = bernoulli_upper * gaussian_hessian_upper + F(1, 10000)
    assert reference_lower - perturbation_upper == F(41, 6000) > 0
    far_derivative_upper = F(29, 6) / 10000
    assert far_derivative_upper < F(1, 2000)
    derivative_error = lipschitz * radius + bernoulli_upper * F(2, 3) + F(1, 2000)
    assert kappa_lower - derivative_error == F(479, 2000) > 0
    assert radius < F(1, 3)  # Inradius of the near tetrahedron.


@pytest.mark.parametrize("direction", [[1, 0, 0], [-1, -1, -1], [1, 2, -3]])
def test_inner_fixed_samples_check_formulas_not_the_continuous_certificate(direction):
    direction = np.array(direction, dtype=float)
    point = RADIUS * direction / np.linalg.norm(direction)
    positions, directions, weights = _readout(_history("negative"))
    vertices = _vertices()
    native_scaled = _field(point, positions, directions, weights) / weights[0]
    reference = _field(point, vertices, -vertices, np.ones(4))
    assert np.linalg.norm(reference) > 7 / 75
    assert np.linalg.norm(native_scaled - reference) < 54 / 625 + 1 / 10000
    assert np.linalg.norm(native_scaled) > 41 / 6000
    jac = _jacobian(point, positions, directions, weights) / weights[0]
    kappa = 4 * np.exp(-0.5) / 3
    assert np.linalg.norm(jac + kappa * np.eye(3), ord=2) < 12 / 25 + 2 / 25 + 1 / 2000
    assert np.linalg.slogdet(jac)[0] == -1
    step = 1e-5
    finite_difference = np.column_stack(
        [
            (
                _field(point + step * axis, positions, directions, weights)
                - _field(point - step * axis, positions, directions, weights)
            )
            / (2 * step * weights[0])
            for axis in np.eye(3)
        ]
    )
    np.testing.assert_allclose(jac, finite_difference, rtol=2e-8, atol=2e-11)
    barycentric = (1 + 3 * vertices @ point) / 4
    assert np.all(barycentric > 0)
    np.testing.assert_allclose(barycentric @ vertices, point, atol=1e-16)


def test_positive_control_has_same_horizon_weights_and_a_local_regular_zero():
    positions, directions, weights = _readout(_history("positive"))
    negative_weights = _readout(_history("negative"))[2]
    np.testing.assert_array_equal(weights, negative_weights)
    root = np.sqrt(3) * np.log(Q) * np.array([1, 0.5, 0])
    assert np.linalg.norm(root) < RADIUS
    amplitude = np.sum(weights * np.exp(-np.sum((positions - root) ** 2, axis=1) / 2))
    assert (
        np.linalg.norm(_field(root, positions, directions, weights)) / amplitude < 1e-15
    )
    jac = _jacobian(root, positions, directions, weights)
    assert np.linalg.slogdet(jac)[0] == 1
    assert np.linalg.eigvalsh((jac + jac.T) / 2).min() > 0
    np.testing.assert_allclose(weights[:4] + weights[4:], weights[:4] * (1 + Q**4))
    # -log(q) <= (1-q)/q; square to keep the localization certificate rational.
    assert F(15, 4) * F(1, 99) ** 2 < F(1, 6) ** 2


def test_outer_degree_margin_is_strict_rational():
    q = F(99, 100)
    assert q**7 > 1 - 7 * (1 - q) == F(93, 100)
    leading_lower = F(93, 100) * 4 * F(1, 3) / 6
    assert leading_lower == F(31, 150)
    assert 12 - 4 * 12 * F(1, 3) == -4
    assert leading_lower - F(2, 25) - F(1, 10000) == F(3797, 30000) > 0


@pytest.mark.parametrize("direction", [[1, 0, 0], [1, 1, 1], [-1, -1, -1], [1, 2, 3]])
def test_outer_fixed_samples_check_scaled_radial_formula(direction):
    n = np.array(direction, dtype=float)
    n /= np.linalg.norm(n)
    positions, directions, weights = _readout(_history("negative"))
    projections = _vertices() @ n
    maximum = projections.max()
    assert maximum >= 1 / 3 - 1e-15
    radii_squared = np.sum(positions**2, axis=1)
    log_common = -(12**2) / 2 - 25 / 2 + 5 * 12 * maximum
    # Factor out a positive common exponential; do not change the native force.
    exponents = (25 - radii_squared) / 2 + 12 * (positions @ n - 5 * maximum)
    scaled = np.sum((weights / weights[0]) * (directions @ n) * np.exp(exponents))
    raw = n @ _field(12 * n, positions, directions, weights)
    assert raw / (weights[0] * np.exp(log_common)) == pytest.approx(scaled, rel=1e-13)
    bound = (
        Q**7 * 4 * maximum / np.sqrt(88 / 3)
        - 3 * np.exp(-4 * 12 * maximum)
        - 4 * np.exp(12 - 4 * 12 * maximum)
    )
    assert scaled >= bound > 3797 / 30000


@pytest.mark.parametrize("kind", ["negative", "positive"])
@pytest.mark.parametrize("parity", [-1, 1])
def test_rigid_space_transform_is_covariant_not_a_charge_sign_switch(kind, parity):
    transform = np.array([[0, 0, parity], [1, 0, 0], [0, 1, 0]])
    shift = np.array([0.2, -0.3, 0.4])
    history = _history(kind)
    point = np.array([0.02, -0.01, 0.03])
    positions, directions, weights = _readout(history)
    mapped_positions, mapped_directions, mapped_weights = _readout(
        history @ transform.T + shift
    )
    mapped_point = transform @ point + shift
    np.testing.assert_allclose(
        _field(mapped_point, mapped_positions, mapped_directions, mapped_weights),
        transform @ _field(point, positions, directions, weights),
        atol=2e-17,
    )
    jac = _jacobian(point, positions, directions, weights)
    mapped_jac = _jacobian(
        mapped_point, mapped_positions, mapped_directions, mapped_weights
    )
    np.testing.assert_allclose(mapped_jac, transform @ jac @ transform.T, atol=2e-17)
    assert np.linalg.slogdet(mapped_jac)[0] == np.linalg.slogdet(jac)[0]
