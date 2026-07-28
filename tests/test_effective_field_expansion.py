from __future__ import annotations

from dataclasses import asdict
import json

import numpy as np
import pytest

from emergenz_knoten import (
    LocalScalarFieldExpansion,
    RelaxationDiffusionField,
    gaussian_matched_local_expansion,
    gaussian_transfer,
    isotropic_ambient_transfer_matrix,
    local_scalar_frequency_response,
    local_scalar_stationary_transfer,
    propagate_isotropic_ambient_covariance,
    relaxation_diffusion_local_expansion,
)


def test_gaussian_matched_operator_matches_through_fourth_order() -> None:
    length = 3.0
    field = gaussian_matched_local_expansion(gaussian_length=length)

    assert field.gradient_coefficient == pytest.approx(length**2 / 2.0)
    assert field.biharmonic_coefficient == pytest.approx(length**4 / 8.0)

    coarse = 0.1 / length
    fine = coarse / 2.0
    errors = []
    for wavenumber in (coarse, fine):
        exact = gaussian_transfer(np.array([wavenumber]), length=length)[0]
        matched = local_scalar_stationary_transfer(
            wavenumber,
            field,
            normalize_zero_mode=True,
        )
        errors.append(abs(float(matched) - float(exact)))

    assert errors[0] / errors[1] == pytest.approx(2.0**6, rel=0.03)


def test_relaxation_diffusion_embeds_exactly_in_operator_family() -> None:
    original = RelaxationDiffusionField(
        diffusivity=2.0,
        decay_rate=0.5,
        coupling=-3.0,
        relaxation_time=4.0,
    )
    expansion = relaxation_diffusion_local_expansion(original)

    assert expansion.mass_coefficient == 0.5
    assert expansion.gradient_coefficient == 2.0
    assert expansion.biharmonic_coefficient == 0.0
    assert expansion.source_coefficient == -3.0
    assert expansion.relaxation_time == 4.0


def test_stability_classifies_finite_wavenumber_threshold() -> None:
    stable = LocalScalarFieldExpansion(
        mass_coefficient=1.0,
        gradient_coefficient=-1.8,
        biharmonic_coefficient=1.0,
    ).linear_stability()
    critical = LocalScalarFieldExpansion(
        mass_coefficient=1.0,
        gradient_coefficient=-2.0,
        biharmonic_coefficient=1.0,
    ).linear_stability()
    unstable = LocalScalarFieldExpansion(
        mass_coefficient=1.0,
        gradient_coefficient=-2.2,
        biharmonic_coefficient=1.0,
        cubic_saturation=1.0,
    ).linear_stability()

    assert stable.classification == "stable_finite_wavenumber_minimum"
    assert stable.minimum_denominator == pytest.approx(0.19)
    assert stable.preferred_wavenumber == pytest.approx(np.sqrt(0.9))
    assert critical.classification == "critical_finite_wavenumber"
    assert critical.minimum_denominator == pytest.approx(0.0)
    assert unstable.classification == "finite_wavenumber_instability"
    assert unstable.minimum_denominator == pytest.approx(-0.21)


def test_stability_treats_roundoff_at_threshold_as_critical() -> None:
    critical = LocalScalarFieldExpansion(
        mass_coefficient=1.0,
        gradient_coefficient=-2.0 - 1e-15,
        biharmonic_coefficient=1.0,
    ).linear_stability()

    assert critical.classification == "critical_finite_wavenumber"
    assert not critical.stable
    json.dumps(asdict(critical))


def test_quadratic_field_term_is_allowed_without_internal_sign_symmetry() -> None:
    field = LocalScalarFieldExpansion(
        mass_coefficient=1.0,
        gradient_coefficient=0.5,
        quadratic_nonlinearity=-0.75,
        cubic_saturation=1.0,
    )

    assert field.quadratic_nonlinearity == -0.75
    assert field.linear_stability().stable


def test_negative_gradient_without_biharmonic_term_is_uv_unstable() -> None:
    stability = LocalScalarFieldExpansion(
        mass_coefficient=1.0,
        gradient_coefficient=-0.1,
    ).linear_stability()

    assert stability.classification == "ultraviolet_unstable"
    assert not stability.high_wavenumber_stable
    assert np.isneginf(stability.minimum_denominator)


def test_derivative_source_has_exact_zero_mode_null() -> None:
    field = LocalScalarFieldExpansion(
        mass_coefficient=1.0,
        gradient_coefficient=0.5,
        biharmonic_coefficient=0.125,
        source_coefficient=0.0,
        source_laplacian_coefficient=1.0,
    )
    response = local_scalar_stationary_transfer(np.array([0.0, 0.5]), field)

    assert field.zero_mean_linear_response
    assert response[0] == 0.0
    assert response[1] > 0.0
    with pytest.raises(ValueError, match="zero-mean"):
        local_scalar_stationary_transfer(0.0, field, normalize_zero_mode=True)


def test_frequency_response_reduces_to_stationary_response_at_zero_frequency() -> None:
    field = gaussian_matched_local_expansion(gaussian_length=2.0)
    k = np.array([0.0, 0.5, 1.0])

    stationary = local_scalar_stationary_transfer(k, field)
    dynamic = local_scalar_frequency_response(k, 0.0, field)

    np.testing.assert_allclose(dynamic.real, stationary)
    np.testing.assert_array_equal(dynamic.imag, 0.0)


def test_componentwise_isotropic_transfer_preserves_full_rank() -> None:
    response = 0.4 - 0.2j
    transfer = isotropic_ambient_transfer_matrix(response, dimension=10)
    source_covariance = np.diag(np.linspace(1.0, 0.1, 10))
    propagated = propagate_isotropic_ambient_covariance(
        source_covariance,
        response,
    )

    np.testing.assert_allclose(transfer, response * np.eye(10))
    assert np.linalg.matrix_rank(source_covariance) == 10
    assert np.linalg.matrix_rank(propagated) == 10
    np.testing.assert_allclose(propagated, abs(response) ** 2 * source_covariance)


def test_zero_isotropic_response_collapses_covariance_rank() -> None:
    source_covariance = np.eye(4)

    propagated = propagate_isotropic_ambient_covariance(source_covariance, 0.0)

    assert np.linalg.matrix_rank(propagated) == 0
