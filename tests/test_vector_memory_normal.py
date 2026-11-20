"""Small derivative and recurrence controls; no target orbit or parameter search."""

from dataclasses import replace
from fractions import Fraction

import numpy as np
import pytest

from emergenz_knoten.core import SimulationConfig, memory_horizon
from emergenz_knoten.fifo_normal_stability import (
    normal_translation_slope,
    rotation_symmetry_division,
)
from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights
from emergenz_knoten.vector_memory import (
    VectorMemoryConfig,
    _vector_horizon,
    normalize_orientation,
    planar_alignment_normal_row,
    vector_memory_force,
)


def _config(dim=3, deposition="delta"):
    return VectorMemoryConfig(
        scalar=SimulationConfig(
            steps=4,
            dim=dim,
            epsilon=0,
            alpha=0.2,
            max_memory=4,
            deposition_kernel=deposition,
            deposition_sigma=0.4 if deposition == "gaussian" else 0,
            eta=0.3,
            amplitude_att=1.2,
            sigma_att=1.7,
        ),
        lambda_vector=0.3,
        max_vector_memory=5,
        eta_vector=0.4,
        vector_mass=0.8,
        sigma_vector=1.4,
    )


def _planar_history(count):
    ages = np.arange(count)
    return np.column_stack([np.cos(0.6 * ages) + 0.1 * ages, np.sin(0.6 * ages)])


def _next_position(history, config, frozen_orientations=None):
    scalar = config.scalar
    scalar_count = memory_horizon(scalar)
    vector_count = _vector_horizon(config)
    scalar_weights = exponential_memory_weights(
        scalar.alpha, scalar_count, memory_mass=scalar.memory_mass
    )
    vector_weights = exponential_memory_weights(
        config.lambda_vector, vector_count, memory_mass=config.vector_mass
    )
    directions = frozen_orientations
    if directions is None:
        directions = np.array(
            [
                normalize_orientation(history[j] - history[j + 1])
                for j in range(vector_count)
            ]
        )
    gradient = double_gaussian_gradient(
        history[0],
        history[:scalar_count],
        scalar_weights,
        sigma_rep=scalar.sigma_rep,
        sigma_att=scalar.sigma_att,
        amplitude_rep=scalar.amplitude_rep,
        amplitude_att=scalar.amplitude_att,
        deposition_kernel=scalar.deposition_kernel,
        deposition_sigma=scalar.deposition_sigma,
    )
    vector = vector_memory_force(
        history[0],
        history[:vector_count],
        directions,
        vector_weights,
        sigma=config.sigma_vector,
    )
    return history[0] - scalar.eta * gradient + config.eta_vector * vector


@pytest.mark.parametrize("dim", [3, 5, 7])
@pytest.mark.parametrize("deposition", ["delta", "gaussian", "matched_gaussian"])
def test_normal_row_matches_all_history_derivatives_and_rigid_tilts(dim, deposition):
    config = _config(dim, deposition)
    planar = _planar_history(6)
    before = np.zeros((6, dim))
    before[:, :2] = planar
    original = before.copy()
    row = planar_alignment_normal_row(planar, config)
    normal_axis = dim - 1
    step = 1e-6
    for age in range(6):
        offset = np.zeros_like(before)
        offset[age, normal_axis] = step
        derivative = (
            _next_position(before + offset, config)[normal_axis]
            - _next_position(before - offset, config)[normal_axis]
        ) / (2 * step)
        assert derivative == pytest.approx(row[age], abs=2e-11, rel=2e-9)
    assert row.sum() == pytest.approx(1, abs=3e-15)
    next_point = _next_position(before, config)
    np.testing.assert_allclose(row @ planar, next_point[:2], rtol=2e-14, atol=3e-15)
    np.testing.assert_array_equal(before, original)


def test_scalar_horizon_can_exceed_vector_horizon():
    config = _config()
    config = replace(
        config, scalar=replace(config.scalar, max_memory=7), max_vector_memory=2
    )
    planar = _planar_history(7)
    history = np.column_stack([planar, np.zeros(7)])
    direction = np.linspace(-0.4, 0.7, 7)
    offset = np.zeros_like(history)
    offset[:, 2] = 1e-6 * direction
    derivative = (
        _next_position(history + offset, config)[2]
        - _next_position(history - offset, config)[2]
    ) / 2e-6
    row = planar_alignment_normal_row(planar, config)
    assert row.shape == (7,)
    assert derivative == pytest.approx(row @ direction, abs=2e-11)


def test_freezing_orientations_loses_the_actual_normal_response():
    config = _config()
    planar = _planar_history(6)
    history = np.column_stack([planar, np.zeros(6)])
    orientations = np.array(
        [normalize_orientation(d) for d in history[:-1] - history[1:]]
    )
    perturbation = np.zeros_like(history)
    perturbation[0, 2] = 1e-6
    frozen = (
        _next_position(history + perturbation, config, orientations)[2]
        - _next_position(history - perturbation, config, orientations)[2]
    ) / 2e-6
    full = planar_alignment_normal_row(planar, config)[0]
    assert full - frozen > 0.1


@pytest.mark.parametrize("change", [{"eta_vector": 0.0}, {"vector_mass": 0.0}])
def test_passive_channel_requires_no_extra_predecessor_or_nonzero_steps(change):
    config = replace(_config(), **change)
    row = planar_alignment_normal_row(np.zeros((4, 2)), config)
    assert row.shape == (4,)
    assert row.sum() == pytest.approx(1)


def test_noncontributing_zero_weight_orientations_do_not_create_singular_derivative():
    config = replace(_config(), lambda_vector=1.0)
    history = np.array(
        [[1.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
    )
    row = planar_alignment_normal_row(history, config)
    assert np.isfinite(row).all()


def test_large_self_curvature_does_not_destroy_exact_translation_of_one_point():
    config = _config()
    config = replace(
        config,
        scalar=replace(config.scalar, max_memory=1, sigma_rep=1e-9),
        eta_vector=0.0,
    )
    row = planar_alignment_normal_row(np.zeros((1, 2)), config)
    np.testing.assert_array_equal(row, [1.0])


@pytest.mark.parametrize(
    "case", ["short", "nonfinite", "zero_step", "noise", "dimension", "transverse"]
)
def test_out_of_scope_or_singular_inputs_are_rejected(case):
    config = _config()
    history = _planar_history(6)
    if case == "short":
        history = history[:-1]
    elif case == "nonfinite":
        history[2, 0] = np.nan
    elif case == "zero_step":
        history[2] = history[3]
    elif case == "noise":
        config = replace(config, scalar=replace(config.scalar, epsilon=0.01))
    elif case == "dimension":
        config = replace(config, scalar=replace(config.scalar, dim=2))
    else:
        config = replace(
            config, force_mode="transverse_2d", scalar=replace(config.scalar, dim=2)
        )
    with pytest.raises(ValueError):
        planar_alignment_normal_row(history, config)


@pytest.mark.parametrize("extra_root", [Fraction(1, 2), Fraction(2), Fraction(-2)])
def test_symmetry_quotient_and_slope_distinguish_formal_recurrences(extra_root):
    factor = np.array([1, -1, 1, -1], dtype=object)  # theta=pi/2
    polynomial = list(np.convolve(factor, [1, -extra_root]))
    row = [-value for value in polynomial[1:]]
    assert sum(row) == 1
    quotient, remainder = rotation_symmetry_division(polynomial, Fraction(0))
    assert quotient == [1, -extra_root]
    assert remainder == [0, 0, 0]
    slope = normal_translation_slope(row[1:])
    assert slope == 2 * (1 - extra_root)
    if extra_root == -2:
        assert slope > 0 and abs(extra_root) > 1  # Positive slope is not stability.


def test_circular_trial_residual_is_not_silently_removed_as_symmetry():
    config = _config()
    theta = 0.6
    angles = -theta * np.arange(6)
    history = np.column_stack([np.cos(angles), np.sin(angles)])
    row = planar_alignment_normal_row(history, config)
    _, remainder = rotation_symmetry_division([1.0, *(-row)], np.cos(theta))
    actual_next = row @ history
    required_next = np.array([np.cos(theta), np.sin(theta)])
    assert np.linalg.norm(actual_next - required_next) > 0.1
    assert np.linalg.norm(remainder) > 0.01


def test_exact_active_update_changes_displacement_mode_intensity():
    config = VectorMemoryConfig(
        scalar=SimulationConfig(
            steps=2,
            dim=3,
            epsilon=0,
            eta=0,
            alpha=0.5,
            memory_mass=2,
            max_memory=3,
        ),
        lambda_vector=1,
        vector_mass=1,
        eta_vector=0.5,
        max_vector_memory=1,
    )
    history = np.array([[0, 0, 0], [-1, 0, 0], [-1, 0, 0]], dtype=float)
    np.testing.assert_array_equal(_next_position(history, config), [0.5, 0, 0])
    # omega=pi/2: Z=e1, Z'=(1/2+i/2)e1, with no rounded trigonometry.
    before_intensity = Fraction(1)
    after_intensity = Fraction(1, 2) ** 2 + Fraction(1, 2) ** 2
    assert after_intensity - before_intensity == Fraction(-1, 2)


@pytest.mark.parametrize("q,omega", [(0.5, 0.7), (0.9, 1.2)])
def test_mode_intensity_budget_contains_memory_source_terms(q, omega):
    config = _config()
    config = replace(config, scalar=replace(config.scalar, alpha=1 - q))
    history = np.column_stack([_planar_history(6), np.zeros(6)])
    next_point = _next_position(history, config)
    updated_history = np.vstack([next_point, history[:-1]])
    length = memory_horizon(config.scalar) - 1
    w_zero = config.scalar.alpha * config.scalar.memory_mass
    coefficients = w_zero * (q * np.exp(1j * omega)) ** np.arange(length)
    deposits = history[:length] - history[1 : length + 1]
    updated_deposits = updated_history[:length] - updated_history[1 : length + 1]
    z = coefficients @ deposits
    updated_z = coefficients @ updated_deposits
    source = (
        w_zero * (next_point - history[0])
        - w_zero * q**length * np.exp(1j * length * omega) * deposits[-1]
    )
    drift = q * np.exp(1j * omega) * z
    np.testing.assert_allclose(updated_z, drift + source, atol=2e-16)
    intensity_change = np.vdot(updated_z, updated_z).real - np.vdot(z, z).real
    budget = (
        (q**2 - 1) * np.vdot(z, z).real
        + 2 * np.vdot(drift, source).real
        + np.vdot(source, source).real
    )
    assert intensity_change == pytest.approx(budget, abs=3e-15)
    assert abs(intensity_change) > 1e-6
