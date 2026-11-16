"""Finite algebraic controls for defect recurrence; no trajectory search."""

from fractions import Fraction

import numpy as np
import pytest

from emergenz_knoten.core import SimulationConfig
from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights
from emergenz_knoten.vector_memory import (
    VectorMemoryConfig,
    _validate_vector_config,
    alignment_history_head_jacobian,
    normalize_orientation,
    vector_gaussian_field,
    vector_memory_force,
)


def _history():
    return (
        np.array(
            [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1], [1, 1, 1]],
            dtype=float,
        )
        / 2
    )


def _symmetry():
    return np.array([[0, 0, -1], [0, -1, 0], [1, 0, 0]])


def _config():
    # Algebra fixes q_v=1/2, g=1/2, q_s=1/6, B=-24, C=-108.
    return VectorMemoryConfig(
        scalar=SimulationConfig(
            steps=4,
            dim=3,
            epsilon=0,
            alpha=5 / 6,
            memory_mass=1,
            eta=108 / ((5 / 6) * 0.5 * np.exp(-0.5)),
            sigma_rep=np.sqrt(2),
            sigma_att=2,
            amplitude_rep=1,
            amplitude_att=0,
            max_memory=4,
            memory_factor=4,
        ),
        lambda_vector=0.5,
        vector_mass=1,
        eta_vector=-48 * np.sqrt(2),
        sigma_vector=1 / np.sqrt(np.log(2)),
        max_vector_memory=4,
        vector_memory_factor=4,
    )


def _map(history):
    config = _config()
    scalar = config.scalar
    positions = history[:4]
    directions = np.array(
        [normalize_orientation(step) for step in np.diff(history, axis=0) * -1]
    )
    gradient = double_gaussian_gradient(
        history[0],
        positions,
        exponential_memory_weights(scalar.alpha, 4),
        sigma_rep=scalar.sigma_rep,
        sigma_att=scalar.sigma_att,
        amplitude_rep=scalar.amplitude_rep,
        amplitude_att=scalar.amplitude_att,
    )
    field = vector_memory_force(
        history[0],
        positions,
        directions,
        exponential_memory_weights(0.5, 4),
        sigma=config.sigma_vector,
    )
    new_point = history[0] - scalar.eta * gradient + config.eta_vector * field
    return np.vstack([new_point, history[:-1]])


def _reduced_jacobian_parts():
    """Return exact rational M0,M1 with DG=M0+log(2) M1 at the cycle."""
    history = np.array((2 * _history()).astype(int), dtype=object) * Fraction(1, 2)
    chords = history[:-1] - history[1:]
    identity = np.eye(3, dtype=int).astype(object)
    constant = np.zeros((5, 3, 3), dtype=object)
    logarithmic = np.zeros_like(constant)
    constant[0] = identity
    q, s, g = Fraction(1, 2), Fraction(1, 6), Fraction(1, 2)
    b, c = Fraction(-24), Fraction(-108)
    for age in range(4):
        radial = history[0] - history[age]
        if age:
            scalar_hessian = (
                c * s**age * (identity - np.outer(radial, radial) / Fraction(2))
            )
            constant[0] -= scalar_hessian
            constant[age] += scalar_hessian
        gaussian = g if age else Fraction(1)
        orientation = (
            b
            * q**age
            * gaussian
            * (identity - np.outer(chords[age], chords[age]) / Fraction(2))
        )
        constant[age] += orientation
        constant[age + 1] -= orientation
        kernel = -b * q**age * gaussian * np.outer(chords[age], radial)
        logarithmic[0] += kernel
        logarithmic[age] -= kernel
    inverse = _symmetry().T.astype(object)
    m_zero = np.zeros((15, 15), dtype=object)
    m_log = np.zeros_like(m_zero)
    for age in range(5):
        m_zero[:3, 3 * age : 3 * age + 3] = inverse @ constant[age]
        m_log[:3, 3 * age : 3 * age + 3] = inverse @ logarithmic[age]
        if age:
            m_zero[3 * age : 3 * age + 3, 3 * (age - 1) : 3 * age] = inverse
    return m_zero, m_log


def test_signed_gain_control_is_an_exact_four_cycle_of_the_existing_rule():
    config = _config()
    _validate_vector_config(config)
    assert config.eta_vector < 0 < config.scalar.eta
    history = _history()
    rotation = _symmetry()
    np.testing.assert_array_equal(rotation.T @ rotation, np.eye(3))
    np.testing.assert_array_equal(np.linalg.matrix_power(rotation, 4), np.eye(3))
    assert np.linalg.det(rotation) == -1
    for phase in range(4):
        transform = np.linalg.matrix_power(rotation, phase)
        prescribed = history @ transform.T
        np.testing.assert_allclose(
            _map(prescribed), prescribed @ rotation.T, atol=2e-14, rtol=0
        )
        directions = np.array(
            [normalize_orientation(step) for step in -np.diff(prescribed, axis=0)]
        )
        root = transform @ np.array([-2.0, -1.0, 0.0])
        field = vector_gaussian_field(
            root,
            prescribed[:4],
            directions,
            exponential_memory_weights(0.5, 4),
            sigma=config.sigma_vector,
        )
        np.testing.assert_allclose(field, 0, atol=5e-17)
        assert np.linalg.norm(root) == pytest.approx(np.sqrt(5))


def test_full_reduced_derivative_matches_every_history_coordinate():
    m_zero, m_log = _reduced_jacobian_parts()
    matrix = np.asarray(m_zero, dtype=float) + np.log(2) * np.asarray(
        m_log, dtype=float
    )
    history = _history()
    rotation = _symmetry()
    redundant_length = np.zeros_like(history)
    redundant_length[-1] = history[-2] - history[-1]
    np.testing.assert_allclose(matrix @ redundant_length.ravel(), 0, atol=1e-15)
    step = 2e-6
    for column in range(15):
        perturbation = np.zeros(15)
        perturbation[column] = step
        perturbation = perturbation.reshape(5, 3)
        derivative = (
            (_map(history + perturbation) - _map(history - perturbation)) @ rotation
        ) / (2 * step)
        np.testing.assert_allclose(
            matrix[:, column], derivative.ravel(), rtol=2e-7, atol=2e-8
        )


def test_frame_reduction_preserves_translation_directions():
    m_zero, m_log = _reduced_jacobian_parts()
    matrix = np.asarray(m_zero, dtype=float) + np.log(2) * np.asarray(
        m_log, dtype=float
    )
    for axis in np.eye(3):
        translation = np.tile(axis, 5)
        expected = np.tile(_symmetry().T @ axis, 5)
        np.testing.assert_allclose(matrix @ translation, expected, rtol=0, atol=2e-14)


def test_rotations_remain_symmetry_directions_not_growing_form_modes():
    m_zero, m_log = _reduced_jacobian_parts()
    matrix = np.asarray(m_zero, dtype=float) + np.log(2) * np.asarray(
        m_log, dtype=float
    )
    history, symmetry = _history(), _symmetry()
    for first, second in [(0, 1), (0, 2), (1, 2)]:
        generator = np.zeros((3, 3))
        generator[first, second] = 1
        generator[second, first] = -1
        perturbation = history @ generator.T
        transported = symmetry.T @ generator @ symmetry
        expected = history @ transported.T
        np.testing.assert_allclose(
            matrix @ perturbation.ravel(), expected.ravel(), atol=2e-14, rtol=0
        )


def test_exact_trace_certificate_proves_instability_without_eigenvalue_rounding():
    m_zero, m_log = _reduced_jacobian_parts()
    assert all(
        isinstance(value, (int, np.integer, Fraction))
        for matrix in (m_zero, m_log)
        for value in matrix.flat
    )
    coefficients = (
        np.trace(m_zero @ m_zero),
        2 * np.trace(m_zero @ m_log),
        np.trace(m_log @ m_log),
    )
    assert coefficients == (Fraction(97, 16), Fraction(-63, 4), Fraction(261, 4))
    # log(2)=2*atanh(1/3); bound the positive tail by a geometric series.
    partial = Fraction(2, 3) + Fraction(2, 81)
    tail_bound = Fraction(2, 5) * Fraction(1, 3) ** 5 / (1 - Fraction(1, 3) ** 2)
    lower_log, upper_log = Fraction(69, 100), Fraction(7, 10)
    assert lower_log < partial < partial + tail_bound < upper_log
    lower_trace = (
        coefficients[0] + coefficients[1] * upper_log + coefficients[2] * lower_log**2
    )
    assert lower_trace > 26 > 15
    # |tr(M^2)| <= 15 rho(M)^2 and D(F^4)=M^4 at this orbit.
    assert Fraction(26, 15) ** 2 > 3


def test_general_head_blocks_reproduce_exact_orbit_matrix_and_two_step_return():
    history, config, rotation = _history(), _config(), _symmetry()

    def full_jacobian(state):
        blocks = alignment_history_head_jacobian(state, config)
        matrix = np.zeros((15, 15))
        matrix[:3] = np.concatenate(blocks, axis=1)
        matrix[3:, :-3] = np.eye(12)
        return matrix

    native = full_jacobian(history)
    frame = np.kron(np.eye(5), rotation.T)
    reduced = frame @ native
    m_zero, m_log = _reduced_jacobian_parts()
    expected = np.asarray(m_zero, dtype=float) + np.log(2) * np.asarray(
        m_log, dtype=float
    )
    np.testing.assert_allclose(reduced, expected, atol=2e-14)
    actual = _map(history)
    np.testing.assert_allclose(actual, history @ rotation.T, atol=2e-14)
    return_two = frame @ frame @ full_jacobian(actual) @ native
    np.testing.assert_allclose(return_two, reduced @ reduced, atol=2e-12)
    trace = 97 / 16 - 63 / 4 * np.log(2) + 261 / 4 * np.log(2) ** 2
    assert np.trace(return_two) == pytest.approx(trace, abs=3e-12)


def test_exact_gap_direction_is_not_closed_even_after_two_steps_and_translation():
    m_zero, m_log = _reduced_jacobian_parts()
    gap = np.zeros((5, 3), dtype=object)
    gap[:, 1] = np.array([1, -1, 1, -1, 1], dtype=object) * Fraction(1, 2)
    # R flips the y coordinate: the native head response is -M's head response.
    assert -(m_zero @ gap.ravel())[1] == 0
    assert -(m_log @ gap.ravel())[1] == Fraction(-15, 2)
    constant = (m_zero @ m_zero @ gap.ravel()).reshape(5, 3)
    linear = ((m_zero @ m_log + m_log @ m_zero) @ gap.ravel()).reshape(5, 3)
    quadratic = (m_log @ m_log @ gap.ravel()).reshape(5, 3)
    assert constant[1, 1] == 0
    assert linear[1, 1] == Fraction(-15, 2)
    assert quadratic[1, 1] == 0
    # Tail ages 2,3 force unit gap amplitude and zero common y translation.
    np.testing.assert_array_equal(constant[2:, 1], gap[2:, 1])
    np.testing.assert_array_equal(linear[2:, 1], 0)
    np.testing.assert_array_equal(quadratic[2:, 1], 0)
    # log(2)>69/100 was bounded independently in the trace-certificate test.
    assert Fraction(15, 2) * Fraction(69, 100) - Fraction(1, 2) > 4


def test_gap_slope_formula_matches_native_head_and_history_derivative():
    history, config = _history(), _config()
    tangent = np.zeros_like(history)
    tangent[:, 1] = history[:, 1]
    blocks = alignment_history_head_jacobian(history, config)
    head = np.einsum("aij,aj->i", blocks, tangent)
    scalar_slope = 37 / 4
    vector_slope = 39 / 4 - 15 / 2 * np.log(2)
    axial_slope = scalar_slope - vector_slope
    assert head[1] == pytest.approx(-0.5 - axial_slope, abs=2e-14)
    difference = (
        _map(history + 1e-6 * tangent) - _map(history - 1e-6 * tangent)
    ) / 2e-6
    np.testing.assert_allclose(head, difference[0], atol=5e-9)


@pytest.mark.parametrize("q", [Fraction(1, 3), Fraction(1, 2), Fraction(4, 5)])
@pytest.mark.parametrize("g", [Fraction(1, 3), Fraction(1, 2)])
def test_regular_cycle_equalities_force_outward_motion_for_positive_alignment(q, g):
    s = g * q * (1 - q) / (1 - g * q)
    assert 0 < s < q < 1
    b, c = Fraction(1), (1 - g * q) / s
    drift = [
        b * (1 - g * q**3) - c * (s + s**2 + s**3),
        b * g * (q - q**3) - c * (s**2 + s**3),
        b * g * (q**2 - q**3) - c * s**3,
    ]
    assert drift[0] == drift[1] == drift[2] == b * g * q * (1 - q) * (q - s)
    assert drift[2] > 0  # Required for the proposed cycle: all three equal -1.


@pytest.mark.parametrize("q", [0.5, 0.8])
@pytest.mark.parametrize("periods", [1, 2, 3])
def test_complete_fifo_periods_only_rescale_the_four_phase_weights(q, periods):
    weights = exponential_memory_weights(1 - q, 4 * periods, memory_mass=1.4)
    aggregated = weights.reshape(periods, 4).sum(axis=0)
    expected = weights[0] * (1 - q ** (4 * periods)) / (1 - q**4) * q ** np.arange(4)
    np.testing.assert_allclose(aggregated, expected, rtol=2e-15)


@pytest.mark.parametrize("dim", [2, 3, 5])
@pytest.mark.parametrize("mode", ["displacement", "unit"])
def test_every_full_rank_minimal_positive_relation_has_index_plus_one(dim, mode):
    basis = np.diag(np.linspace(0.8, 1.2, dim))
    relation = np.r_[np.linspace(0.6, 1.4, dim), 1.0]
    chords = np.vstack([basis.T, -(basis @ relation[:-1])])
    history = np.vstack([np.zeros(dim), -np.cumsum(chords, axis=0)])
    assert not np.allclose(history[-1], history[0])  # Not the old closed-simplex case.
    positions = history[:-1]
    divisors = np.linalg.norm(chords, axis=1) if mode == "unit" else np.ones(dim + 1)
    directions = chords / divisors[:, None]
    weights = exponential_memory_weights(0.15, dim + 1)
    effective = weights / divisors
    sigma = 0.9
    rhs = np.sum(positions[1:] ** 2, axis=1) / 2
    rhs -= sigma**2 * np.log(
        (effective[1:] / relation[1:]) / (effective[0] / relation[0])
    )
    root = np.linalg.solve(positions[1:] - positions[0], rhs)
    radial = positions - root
    coefficients = weights * np.exp(-np.sum(radial**2, axis=1) / (2 * sigma**2))
    field = vector_gaussian_field(root, positions, directions, weights, sigma=sigma)
    scale = np.sum(coefficients * np.linalg.norm(directions, axis=1))
    assert np.linalg.norm(field) / scale < 2e-13
    jacobian = np.einsum("n,ni,nj->ij", coefficients, directions, radial) / sigma**2
    common = coefficients[0] / divisors[0] / relation[0]
    triangular = np.triu(np.ones((dim, dim))) * relation[:-1, None]
    normalized = jacobian * sigma**2 / common
    np.testing.assert_allclose(
        normalized, basis @ triangular @ basis.T, rtol=2e-12, atol=2e-13
    )
    expected_det = np.linalg.det(basis) ** 2 * np.prod(relation[:-1])
    assert np.linalg.det(normalized) == pytest.approx(expected_det, rel=2e-12)
    assert np.linalg.slogdet(jacobian)[0] == 1
