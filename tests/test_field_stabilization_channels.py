"""Constructed reference controls, not a native knot or field simulation."""

from fractions import Fraction
import math

import numpy as np
import pytest
from scipy.integrate import quad


@pytest.mark.parametrize("coupling", [Fraction(0), Fraction(1, 2), Fraction(2)])
def test_relaxed_curvature_and_square_completion(coupling):
    core, field = Fraction(3, 5), Fraction(-7, 4)
    original = (core**2 + field**2) / 2 - coupling * core * field
    relaxed_curvature = 1 - coupling**2
    completed = (field - coupling * core) ** 2 / 2 + relaxed_curvature * core**2 / 2
    assert completed == original
    assert relaxed_curvature <= 1
    assert (relaxed_curvature > 0) == (abs(coupling) < 1)


def test_frozen_field_minimum_has_a_negative_joint_direction():
    hessian = np.array([[1, -2], [-2, 1]])
    assert hessian[0, 0] > 0
    variation = np.array([1, 1])
    assert variation @ hessian @ variation == -2
    np.testing.assert_allclose(np.linalg.eigvalsh(hessian), [-1, 3])


def test_block_square_completion_in_more_than_one_dimension():
    core = np.array([0.3, -0.7])
    field = np.array([0.4, 0.1, -0.9])
    k = np.diag([2.0, 3.0])
    b = np.array([[0.1, -0.2, 0.3], [0.5, 0.0, -0.1]])
    field_stiffness = np.diag([1.0, 2.0, 4.0])
    relaxation = np.linalg.solve(field_stiffness, b.T)
    effective = k - b @ relaxation
    shifted = field - relaxation @ core
    original = core @ k @ core / 2 - core @ b @ field + field @ field_stiffness @ field / 2
    completed = shifted @ field_stiffness @ shifted / 2 + core @ effective @ core / 2
    assert completed == pytest.approx(original, rel=2e-15)
    assert np.linalg.eigvalsh(k - effective).min() >= 0
    assert np.linalg.eigvalsh(effective).min() > 0


@pytest.mark.parametrize("mass,radius", [(0.0, 3.0), (0.2, 0.7), (2.0, 4.0)])
def test_screened_gauss_flux_includes_induced_charge(mass, radius):
    charge = 1.7
    x = mass * radius
    electric_field = charge * math.exp(-x) * (1 / radius**2 + mass / radius) / (4 * math.pi)
    flux = 4 * math.pi * radius**2 * electric_field
    # Integral of -m^2 A0 over the ball, including the point source separately.
    induced = -charge * (1 - (1 + x) * math.exp(-x))
    assert flux == pytest.approx(charge + induced, abs=2e-15)
    if mass == 0:
        assert flux == pytest.approx(charge)
    else:
        assert 0 < flux < charge


def test_near_core_flux_is_not_asymptotic_charge():
    flux_ratios = [(1 + x) * math.exp(-x) for x in (0.01, 1.0, 30.0)]
    assert flux_ratios[0] > 0.9999
    assert flux_ratios[2] < 3e-12
    assert flux_ratios[0] > flux_ratios[1] > flux_ratios[2]


def test_condensate_gram_form_matches_covariant_derivative_expansion():
    charges = np.array([[1, 2, 0], [0, 1, -1]])
    amplitudes = np.array([2, 3])
    gauge = np.array([3, -1, 2])
    mass_squared = charges.T @ np.diag(amplitudes**2) @ charges
    kinetic_expansion = np.sum(amplitudes**2 * (charges @ gauge) ** 2) / 2
    assert kinetic_expansion == gauge @ mass_squared @ gauge / 2
    null_vector = np.array([-2, 1, 1])
    np.testing.assert_array_equal(charges @ null_vector, [0, 0])
    np.testing.assert_array_equal(mass_squared @ null_vector, [0, 0, 0])


def test_two_channel_null_projector_is_exact():
    half = Fraction(1, 2)
    p_zero = np.array([[half, -half], [-half, half]], dtype=object)
    mass_squared = np.array([[1, 1], [1, 1]], dtype=object)
    np.testing.assert_array_equal(p_zero @ p_zero, p_zero)
    np.testing.assert_array_equal(p_zero.T, p_zero)
    np.testing.assert_array_equal(mass_squared @ p_zero, np.zeros((2, 2), dtype=int))
    massive_source = np.array([1, 1], dtype=object)
    charged_source = np.array([1, 0], dtype=object)
    np.testing.assert_array_equal(p_zero @ massive_source, [0, 0])
    assert charged_source @ p_zero @ charged_source == half
    assert charged_source @ p_zero @ (-charged_source) == -half


@pytest.mark.parametrize("wavenumber", [0.25, 1.0, 3.0])
def test_projector_response_matches_direct_positive_wavenumber_solve(wavenumber):
    mass_squared = np.ones((2, 2))
    p_zero = np.array([[0.5, -0.5], [-0.5, 0.5]])
    p_massive = np.eye(2) - p_zero
    k_squared = wavenumber**2
    response = p_zero / k_squared + p_massive / (k_squared + 2)
    direct = np.linalg.solve(k_squared * np.eye(2) + mass_squared, np.eye(2))
    np.testing.assert_allclose(response, direct, rtol=2e-14, atol=2e-15)
    screened = np.array([1, 1])
    assert screened @ response @ screened == pytest.approx(2 / (k_squared + 2))
    charged = np.array([1, 0])
    residue = k_squared * (charged @ response @ charged)
    assert residue == pytest.approx(0.5 + k_squared / (2 * (k_squared + 2)))


def test_monopole_pair_signs_and_screened_orthogonal_channel():
    p_zero = np.array([[0.5, -0.5], [-0.5, 0.5]])
    p_massive = np.eye(2) - p_zero
    radius = 4.0
    green = (p_zero + math.exp(-math.sqrt(2) * radius) * p_massive) / (4 * math.pi * radius)
    charged, screened = np.array([1, 0]), np.array([1, 1])
    assert charged @ green @ charged > 0
    assert charged @ green @ (-charged) < 0
    assert screened @ p_zero @ screened == 0
    assert screened @ green @ screened == pytest.approx(
        2 * math.exp(-math.sqrt(2) * radius) / (4 * math.pi * radius)
    )


def test_independent_second_condensate_removes_unbroken_channel():
    charges = np.array([[1, 1], [1, -1]])
    mass_squared = charges.T @ charges
    np.testing.assert_array_equal(mass_squared, 2 * np.eye(2))
    assert np.linalg.det(mass_squared) == pytest.approx(4)


@pytest.mark.parametrize("coefficients", [[2, 3], [-4, 1], [0, -2]])
def test_minimal_condensate_currents_have_no_unbroken_charge(coefficients):
    charges = np.array([[1, 2, 0], [0, 1, -1]])
    null_vector = np.array([-2, 1, 1])
    current = charges.T @ np.asarray(coefficients)
    assert null_vector @ current == 0
    assert np.dot(current, current) > 0


def test_uncondensed_charged_species_does_not_higgs_the_remaining_channel():
    charges = np.array([[1, 1], [1, 0]])
    amplitudes = np.array([1, 0])
    mass_squared = charges.T @ np.diag(amplitudes**2) @ charges
    np.testing.assert_array_equal(mass_squared, np.ones((2, 2)))
    null_vector = np.array([1, -1])
    assert null_vector @ charges[0] == 0
    assert null_vector @ charges[1] == 1


def test_charge_residue_is_invariant_under_common_orthogonal_basis_change():
    rotation = np.array([[0.6, -0.8], [0.8, 0.6]])
    mass_squared = np.ones((2, 2))
    p_zero = np.array([[0.5, -0.5], [-0.5, 0.5]])
    j_a, j_b = np.array([1.0, 0.0]), np.array([-1.0, 0.0])
    rotated_mass = rotation @ mass_squared @ rotation.T
    rotated_projector = rotation @ p_zero @ rotation.T
    np.testing.assert_allclose(rotated_mass @ rotated_projector, 0, atol=3e-16)
    residue = (rotation @ j_a) @ rotated_projector @ (rotation @ j_b)
    assert residue == pytest.approx(j_a @ p_zero @ j_b, abs=3e-16)


def test_nonsingular_kinetic_normalization_does_not_create_a_nullspace():
    mass_squared = np.diag([2.0, 3.0])
    kinetic = np.array([[2.0, 0.5], [0.5, 1.0]])
    transform = np.linalg.solve(np.linalg.cholesky(kinetic).T, np.eye(2))
    np.testing.assert_allclose(transform.T @ kinetic @ transform, np.eye(2), atol=3e-16)
    canonical_mass = transform.T @ mass_squared @ transform
    assert np.linalg.eigvalsh(canonical_mass).min() > 0
    assert np.linalg.det(canonical_mass) == pytest.approx(
        np.linalg.det(transform) ** 2 * np.linalg.det(mass_squared)
    )


@pytest.mark.parametrize("size", [12, 20])
def test_single_valued_phase_can_have_local_charge_but_zero_periodic_monopole(size):
    grid = np.arange(size) * (2 * math.pi / size)
    x, y, z = np.meshgrid(grid, grid, grid, indexing="ij")
    # theta=sin(x), B=curl(sin(z), sin(x), sin(y)) has zero divergence.
    gradient = np.stack([np.cos(x), np.zeros_like(x), np.zeros_like(x)])
    magnetic = np.stack([np.cos(y), np.cos(z), np.cos(x)])
    density = np.sum(gradient * magnetic, axis=0)
    assert np.max(np.abs(density)) > 0.9
    assert abs(float(np.mean(density))) < 2e-16


@pytest.mark.parametrize("width", [0.25, 1.0, 3.0])
def test_smoothed_vortex_source_has_nonzero_transverse_continuity_residual(width):
    winding, coupling, tangent_field = 2, 0.3, 0.7

    def transverse_density(radius):
        return 2 * winding * width**2 / (radius**2 + width**2) ** 2

    integral, error = quad(
        lambda radius: 2 * math.pi * radius * transverse_density(radius),
        0,
        np.inf,
        epsabs=1e-10,
        epsrel=1e-10,
    )
    assert error < 1e-8
    assert integral == pytest.approx(2 * math.pi * winding, rel=1e-12)
    assert coupling * tangent_field * integral > 0
    radius = 2.0
    finite_integral, _ = quad(
        lambda r: 2 * math.pi * r * transverse_density(r), 0, radius
    )
    circulation = 2 * math.pi * winding * radius**2 / (radius**2 + width**2)
    assert finite_integral == pytest.approx(circulation, rel=1e-12)


@pytest.mark.parametrize("x,y,width", [(0, 0, 1), (1, 2, 3), (-2, 3, 2)])
def test_regularized_bulk_divergence_and_core_charge_rate_cancel_exactly(x, y, width):
    denominator = Fraction(x * x + y * y + width * width)
    coupling, winding, tangent_field = Fraction(2, 5), 2, Fraction(3, 7)
    radial_gain = coupling * winding * tangent_field
    bulk_divergence = radial_gain * (
        2 / denominator - 2 * (x * x + y * y) / denominator**2
    )
    source = 2 * radial_gain * width**2 / denominator**2
    assert bulk_divergence == source > 0
    core_charge_rate = -source
    assert bulk_divergence + core_charge_rate == 0


def test_worldsheet_completion_is_invariant_under_regular_gauge_change():
    coefficient = Fraction(3, 5)
    connection = np.array([Fraction(0), Fraction(7, 4)], dtype=object)
    phase_derivative = np.array([Fraction(2), Fraction(-1, 3)], dtype=object)
    gauge_derivative = np.array([Fraction(-5, 3), Fraction(4, 7)], dtype=object)
    current = -coefficient * connection + phase_derivative
    transformed = (
        -coefficient * (connection + gauge_derivative)
        + phase_derivative
        + coefficient * gauge_derivative
    )
    np.testing.assert_array_equal(transformed, current)


@pytest.mark.parametrize("linking", [-2, 0, 1, 3])
def test_link_charge_is_not_total_charge_in_completed_current(linking):
    coefficient, tube_flux = Fraction(3, 7), Fraction(5, 2)
    bulk_charge = coefficient * tube_flux * linking
    for phase_period in (Fraction(0), Fraction(2, 3)):
        core_charge = -bulk_charge + phase_period
        assert bulk_charge + core_charge == phase_period
    if linking:
        assert bulk_charge != 0


def test_core_winding_requires_periodic_field_not_a_single_valued_real_phase():
    period, winding = 1.7, 2
    angles = np.arange(24) * (2 * math.pi / 24)
    derivative = period * winding / (2 * math.pi) + 0.2 * np.cos(angles)
    assert (2 * math.pi * np.mean(derivative)) == pytest.approx(period * winding)
    assert abs(float(2 * math.pi * np.mean(0.2 * np.cos(angles)))) < 2e-15


def test_nonminimal_bulk_source_can_project_onto_unbroken_channel():
    p_zero = np.diag([0, 1])
    minimal_source = np.array([3, 0])
    phase_gradient = np.array([1, 2, -1])
    massive_magnetic = np.array([2, 0, 1])
    mixed_source = np.array([0, phase_gradient @ massive_magnetic])
    np.testing.assert_array_equal(p_zero @ minimal_source, [0, 0])
    np.testing.assert_array_equal(p_zero @ mixed_source, [0, 1])
    # A pointwise source projection says nothing about its spatial integral.
