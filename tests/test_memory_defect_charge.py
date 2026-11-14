"""Constructed native readouts and one-step controls, not target trajectories."""

import numpy as np
import pytest

from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights
from emergenz_knoten.state import FiniteMemoryState
from emergenz_knoten.vector_memory import (
    normalize_orientation,
    oriented_history_from_state,
    update_vector_history,
    vector_gaussian_field,
    vector_memory_force,
)


def _simplex_history(dim):
    vertices = np.vstack([np.zeros(dim), np.diag(np.linspace(0.8, 1.3, dim))])
    vertices += np.linspace(-0.2, 0.3, dim)
    return np.vstack([vertices, vertices[0]])


def _regular_history():
    vertices = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
    return np.vstack([vertices, vertices[0]]).astype(float) / 2


def _readout(history, q, mode):
    state = FiniteMemoryState(
        x=history[0],
        memory=history,
        weights=exponential_memory_weights(1 - q, len(history), memory_mass=1.7),
    )
    return oriented_history_from_state(state, mode=mode)


def _simplex_zero(history, weights, sigma, mode):
    vertices = history[:-1]
    divisors = np.ones(len(vertices))
    if mode == "unit":
        divisors = np.linalg.norm(history[:-1] - history[1:], axis=1)
    effective = weights / divisors
    rhs = (np.sum(vertices[1:] ** 2, axis=1) - np.sum(vertices[0] ** 2)) / 2
    rhs -= sigma**2 * np.log(effective[1:] / effective[0])
    return np.linalg.solve(vertices[1:] - vertices[0], rhs)


def _jacobian(point, positions, currents, weights, sigma):
    radial = positions - point
    coefficients = weights * np.exp(-np.sum(radial**2, axis=1) / (2 * sigma**2))
    return np.einsum("n,ni,nj->ij", coefficients, currents, radial) / sigma**2


@pytest.mark.parametrize("dim", [2, 3, 5])
@pytest.mark.parametrize("mode", ["displacement", "unit"])
@pytest.mark.parametrize("q", [0.4, 0.85])
def test_simplex_zero_has_native_weights_and_positive_nondegenerate_index(dim, mode, q):
    history = _simplex_history(dim)
    positions, currents, weights = _readout(history, q, mode)
    sigma = 0.9
    root = _simplex_zero(history, weights, sigma, mode)
    value = vector_gaussian_field(root, positions, currents, weights, sigma=sigma)
    amplitude = np.sum(
        weights
        * np.linalg.norm(currents, axis=1)
        * np.exp(-np.sum((root - positions) ** 2, axis=1) / (2 * sigma**2))
    )
    assert np.linalg.norm(value) / amplitude < 64 * dim * np.finfo(float).eps
    jac = _jacobian(root, positions, currents, weights, sigma)
    chords = history[:-1] - history[1:]
    divisor = np.linalg.norm(chords[0]) if mode == "unit" else 1
    common = weights[0] * np.exp(-np.sum((root - positions[0]) ** 2) / (2 * sigma**2))
    common /= divisor
    expected = common * chords.T @ positions / sigma**2
    roundoff = 64 * dim * np.finfo(float).eps * np.linalg.norm(expected, ord=np.inf)
    np.testing.assert_allclose(jac, expected, rtol=2e-14, atol=roundoff)
    np.testing.assert_allclose(
        (jac + jac.T) / 2,
        common * chords.T @ chords / (2 * sigma**2),
        rtol=2e-14,
        atol=roundoff,
    )
    assert np.linalg.eigvalsh((jac + jac.T) / 2).min() > 0
    assert np.linalg.slogdet(jac)[0] == 1
    step = 1e-5
    finite_difference = np.column_stack(
        [
            (
                vector_gaussian_field(
                    root + step * axis, positions, currents, weights, sigma=sigma
                )
                - vector_gaussian_field(
                    root - step * axis, positions, currents, weights, sigma=sigma
                )
            )
            / (2 * step)
            for axis in np.eye(dim)
        ]
    )
    np.testing.assert_allclose(jac, finite_difference, rtol=2e-8, atol=2e-11)


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("reflect", [False, True])
def test_reversing_path_or_reflecting_space_does_not_reverse_this_index(
    reverse, reflect
):
    history = _regular_history()
    if reverse:
        history = history[::-1].copy()
    if reflect:
        history[:, 0] *= -1
    history += [0.2, -0.1, 0.4]
    positions, currents, weights = _readout(history, 0.7, "unit")
    root = _simplex_zero(history, weights, 1.1, "unit")
    np.testing.assert_allclose(
        vector_gaussian_field(root, positions, currents, weights, sigma=1.1),
        0,
        atol=2e-16,
    )
    assert np.linalg.det(_jacobian(root, positions, currents, weights, 1.1)) > 0


@pytest.mark.parametrize("q", [0.3, 0.8])
@pytest.mark.parametrize("gain", [0.1, 0.7])
def test_active_alignment_step_removes_all_zeros_by_an_exact_halfspace_witness(q, gain):
    history = _regular_history()
    positions, currents, weights = _readout(history, q, "unit")
    sigma = 1.2
    root = _simplex_zero(history, weights, sigma, "unit")
    assert np.linalg.det(_jacobian(root, positions, currents, weights, sigma)) > 0
    chords = history[:-1] - history[1:]
    witness = np.linalg.solve(chords[:3], np.ones(3))
    np.testing.assert_allclose(chords @ witness, [1, 1, 1, -3], atol=1e-15)
    # Native epsilon=eta_scalar=0, eta_vector=gain>0, with filled H_vector=4.
    force = vector_memory_force(history[0], positions, currents, weights, sigma=sigma)
    new_point = history[0] + gain * force
    ell = np.linalg.norm(chords[0])
    g = np.exp(-(ell**2) / (2 * sigma**2))
    margin = weights[0] / ell * ((1 - g) + g * (1 - q) * (3 * q**2 + 2 * q + 1))
    assert witness @ force == pytest.approx(margin, rel=2e-14)
    assert margin > 0
    new_direction = normalize_orientation(new_point - history[0])
    after_positions, after_currents, filled = update_vector_history(
        positions.copy(),
        currents.copy(),
        new_point,
        new_direction,
        4,
    )
    assert filled == 4
    # Positive Gaussian coefficients then exclude a zero at EVERY finite point.
    assert np.all(after_currents @ witness > 0)
    shifted = np.vstack([new_point, history[:-1]])
    expected_positions, expected_currents, expected_weights = _readout(
        shifted, q, "unit"
    )
    np.testing.assert_array_equal(after_positions, expected_positions)
    np.testing.assert_allclose(after_currents, expected_currents, atol=2e-15)
    np.testing.assert_array_equal(weights, expected_weights)


@pytest.mark.parametrize("mode", ["displacement", "unit"])
@pytest.mark.parametrize("q", [0.4, 0.8])
def test_source_tail_identity_matches_native_history_push(mode, q):
    history = _simplex_history(3)
    positions, currents, weights = _readout(history, q, mode)
    new_point = history[0] + [0.2, -0.1, 0.3]
    shifted = np.vstack([new_point, history[:-1]])
    after_positions, after_currents, after_weights = _readout(shifted, q, mode)
    for point in (np.zeros(3), np.array([0.4, -0.2, 0.3])):
        before = vector_gaussian_field(point, positions, currents, weights, sigma=1.3)
        after = vector_gaussian_field(
            point, after_positions, after_currents, after_weights, sigma=1.3
        )
        source = (
            weights[0]
            * after_currents[0]
            * np.exp(-np.sum((point - new_point) ** 2) / (2 * 1.3**2))
        )
        tail = (
            weights[0]
            * q**4
            * currents[-1]
            * np.exp(-np.sum((point - positions[-1]) ** 2) / (2 * 1.3**2))
        )
        np.testing.assert_allclose(
            after, q * before + source - tail, rtol=2e-14, atol=2e-16
        )


@pytest.mark.parametrize("side", ["below", "above"])
def test_existing_scalar_channel_can_restore_direction_enclosure_in_one_step(side):
    history = _regular_history()
    q, sigma, vector_gain = 0.7, 1.2, 0.2
    positions, currents, weights = _readout(history, q, "unit")
    chords = history[:-1] - history[1:]
    basis = chords[:3].T
    ell = np.linalg.norm(chords[0])
    scalar_weights = exponential_memory_weights(0.25, 4, memory_mass=1.3)
    kernel = dict(sigma_rep=0.5, sigma_att=1.5, amplitude_rep=1, amplitude_att=2)
    radial = 2 / 1.5**2 * np.exp(-(ell**2) / (2 * 1.5**2))
    radial -= 1 / 0.5**2 * np.exp(-(ell**2) / (2 * 0.5**2))
    assert radial > 0
    tails = np.cumsum(scalar_weights[:0:-1])[::-1]
    gradient = double_gaussian_gradient(history[0], positions, scalar_weights, **kernel)
    np.testing.assert_allclose(gradient, radial * basis @ tails, atol=1e-16)
    g = np.exp(-(ell**2) / (2 * sigma**2))
    b = weights[0] / ell * np.array([1 - g * q**3, g * (q - q**3), g * (q**2 - q**3)])
    thresholds = vector_gain * b / (radial * tails)
    # Two constructed sides of the derived inequality, not fitted particle gains.
    scalar_gain = 0.5 * thresholds.min() if side == "below" else 2 * thresholds.max()
    force = vector_memory_force(history[0], positions, currents, weights, sigma=sigma)
    displacement = vector_gain * force - scalar_gain * gradient
    coefficients = np.linalg.solve(basis, displacement)
    np.testing.assert_allclose(
        coefficients, vector_gain * b - scalar_gain * radial * tails, atol=1e-16
    )
    after = np.vstack([history[0] + displacement, history[:-1]])
    new_positions, new_currents, new_weights = _readout(after, q, "unit")
    if side == "below":
        assert np.all(coefficients > 0)
        witness = np.linalg.solve(chords[:3], np.ones(3))
        assert np.all(new_currents @ witness > 0)
    else:
        assert np.all(coefficients < 0)
        null_coefficients = np.r_[1.0, -coefficients]
        lengths = np.linalg.norm(after[:-1] - after[1:], axis=1)
        np.testing.assert_allclose(
            (null_coefficients * lengths) @ new_currents, 0, atol=2e-16
        )
        effective = new_weights / lengths
        rhs = (
            np.sum(new_positions[1:] ** 2, axis=1) - np.sum(new_positions[0] ** 2)
        ) / 2
        rhs -= sigma**2 * np.log(effective[1:] / effective[0] / null_coefficients[1:])
        root = np.linalg.solve(new_positions[1:] - new_positions[0], rhs)
        field = vector_gaussian_field(
            root, new_positions, new_currents, new_weights, sigma=sigma
        )
        kernel_weights = new_weights * np.exp(
            -np.sum((new_positions - root) ** 2, axis=1) / (2 * sigma**2)
        )
        assert np.linalg.norm(field) / kernel_weights.sum() < 2e-12
        jac = _jacobian(root, new_positions, new_currents, new_weights, sigma)
        common = kernel_weights[0] / lengths[0]
        normalized_jac = jac * sigma**2 / common
        expected_det = (
            np.linalg.det(basis) ** 2
            * coefficients[0]
            * coefficients[1]
            * coefficients[2] ** 2
        )
        assert np.linalg.det(normalized_jac) == pytest.approx(expected_det, rel=2e-10)
        assert np.linalg.slogdet(jac)[0] == 1  # The raw determinant underflows.
        assert np.linalg.norm(root) > 25
        assert np.linalg.norm(new_positions, axis=1).max() < 1


def test_embedding_a_three_dimensional_history_does_not_make_a_four_dimensional_point_defect():
    history = _regular_history()
    _, _, weights = _readout(history, 0.7, "unit")
    root = _simplex_zero(history, weights, 1.0, "unit")
    embedded = np.column_stack([history, np.zeros(len(history))])
    positions, currents, weights = _readout(embedded, 0.7, "unit")
    for transverse in (-0.5, 0.0, 0.8):
        point = np.append(root, transverse)
        np.testing.assert_allclose(
            vector_gaussian_field(point, positions, currents, weights, sigma=1),
            0,
            atol=2e-16,
        )
        assert np.linalg.det(_jacobian(point, positions, currents, weights, 1)) == 0


def test_analytic_boundary_margin_bound_at_a_constructed_simplex_zero():
    history = _regular_history()
    positions, currents, weights = _readout(history, 0.7, "unit")
    sigma = 1.1
    root = _simplex_zero(history, weights, sigma, "unit")
    jac = _jacobian(root, positions, currents, weights, sigma)
    singular_lower = np.linalg.eigvalsh((jac + jac.T) / 2).min()
    hessian_bound = np.sum(weights * np.linalg.norm(currents, axis=1)) / sigma**2
    radius = singular_lower / hessian_bound
    lower = singular_lower * radius - hessian_bound * radius**2 / 2
    assert lower > 0
    directions = np.vstack([np.eye(3), -np.eye(3), np.ones(3) / np.sqrt(3)])
    for axis in directions:
        field = vector_gaussian_field(
            root + radius * axis, positions, currents, weights, sigma=sigma
        )
        assert np.linalg.norm(field) >= lower


def test_regular_zero_velocity_formula_has_the_continuity_sign():
    jac = np.array([[2.0, 0.2, 0], [0, 1, -0.1], [0.3, 0, 1.5]])
    translation = np.array([0.4, -0.2, 0.1])
    time_derivative = -jac @ translation
    velocity = -np.linalg.solve(jac, time_derivative)
    np.testing.assert_allclose(velocity, translation, rtol=1e-14, atol=1e-16)
