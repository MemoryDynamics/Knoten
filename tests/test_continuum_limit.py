from __future__ import annotations

import numpy as np

from emergenz_knoten import (
    aggregate_standard_normal_increments,
    finite_h_linear_response,
    matched_scalar_continuum_case,
    simulate_matched_continuum_response,
)
from experiments.current.dynamics.scaling.scalar_memory_continuum_limit_gate import (
    ALPHA_VALUES,
    TAIL_EXTENTS,
    _fit_response_rate,
    registered_cases,
)


def test_matched_case_keeps_registered_coarse_groups() -> None:
    case = matched_scalar_continuum_case(
        alpha=0.01,
        tail_extent=12.0,
        restoring_per_memory_time=4.0,
        diffusion_per_memory_time=1.0e-4,
        dim=3,
    )

    assert case.horizon == 1200
    assert case.tail_mass_fraction == np.float64(0.99**1200)
    assert np.isclose(case.restoring_per_update / case.alpha, 4.0)
    assert np.isclose(case.epsilon**2 / (2.0 * case.alpha), 1.0e-4)
    assert np.isclose(case.continuum_relative_rate, 5.0)
    assert np.isclose(case.continuum_rms_radius, np.sqrt(3.0e-4 / 5.0))
    assert np.isclose(case.untruncated_relative_root, 0.9504)


def test_finite_h_linear_response_closes_delayed_recurrence() -> None:
    case = matched_scalar_continuum_case(
        alpha=0.05,
        tail_extent=1.0,
        restoring_per_memory_time=2.0,
        diffusion_per_memory_time=1.0e-5,
        dim=1,
    )
    response = finite_h_linear_response(case, response_steps=3 * case.horizon)

    assert response["maximum_recurrence_residual"] < 1.0e-14
    relative = np.asarray(response["relative"])
    assert relative[0] == 1.0
    assert np.isfinite(relative).all()


def test_brownian_aggregation_preserves_coarse_increment() -> None:
    fine = np.arange(24, dtype=float).reshape(12, 2)
    coarse = aggregate_standard_normal_increments(fine, 3)

    expected = fine.reshape(4, 3, 2).sum(axis=1) / np.sqrt(3.0)
    np.testing.assert_allclose(coarse, expected)


def test_mirrored_local_response_matches_linear_reference() -> None:
    case = matched_scalar_continuum_case(
        alpha=0.1,
        tail_extent=2.0,
        restoring_per_memory_time=1.0,
        diffusion_per_memory_time=1.0e-6,
        dim=1,
    )
    formation = np.zeros((case.horizon + 5, 1), dtype=float)
    continuation = np.zeros((10, 1), dtype=float)
    response = simulate_matched_continuum_response(
        case,
        formation_noise=formation,
        response_noise=continuation,
        offset_fractions=[0.01, 0.02],
        axis=[1.0],
    )
    reference = np.asarray(
        finite_h_linear_response(case, response_steps=10)["relative"]
    )

    np.testing.assert_allclose(
        response.relative_responses[:, :, 0],
        np.repeat(reference[None, :], 2, axis=0),
        rtol=2.0e-9,
        atol=2.0e-12,
    )
    np.testing.assert_allclose(response.relative_even_leakage, 0.0, atol=2.0e-12)
    assert response.memory_radii.shape == (11, 5)
    np.testing.assert_allclose(response.memory_radii[0], 0.0, atol=0.0)
    assert response.initial_control_radius == response.memory_radii[0, 0]
    assert response.final_control_radius == response.memory_radii[-1, 0]

    deposition = case.centroid_deposition_fraction
    delta = response.offset_amplitudes[0]
    normalized_relative = response.relative_responses[0, 1, 0]
    first_displaced_x = delta * normalized_relative / (1.0 - deposition)
    expected_first_radius = abs(first_displaced_x) * np.sqrt(
        deposition * (1.0 - deposition)
    )
    np.testing.assert_allclose(
        response.memory_radii[1, 1], expected_first_radius, rtol=1.0e-12
    )


def test_registered_gate_cases_are_unique_and_rate_fit_is_predictive() -> None:
    cases = registered_cases()
    keys = {(case.alpha, case.tail_extent) for case in cases}

    assert len(cases) == len(TAIL_EXTENTS) + len(ALPHA_VALUES) - 1
    assert len(keys) == len(cases)
    case = next(
        item for item in cases if item.alpha == 0.01 and item.tail_extent == 12.0
    )
    reference = np.asarray(
        finite_h_linear_response(case, response_steps=120)["relative"]
    )
    _, fitted_rate, supported = _fit_response_rate(
        reference, reference, alpha=case.alpha
    )

    assert supported > 10
    assert abs(fitted_rate - case.finite_relative_rate) / case.finite_relative_rate < 1e-5
