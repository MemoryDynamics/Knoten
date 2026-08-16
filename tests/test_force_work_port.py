from __future__ import annotations

import numpy as np

from emergenz_knoten import (
    continuum_rectangular_force_response,
    continuum_unit_impulse_response,
    finite_h_force_work_response,
    matched_scalar_continuum_case,
    simulate_matched_force_work_response,
    stationary_center_msd,
    stationary_visible_msd,
)
from experiments.current.dynamics.scaling.scalar_memory_force_work_port_gate import (
    ALPHA_VALUES,
    _fit_postpulse_rate,
    _unit_impulse_profile,
    registered_cases,
)


def _unit_native_impulse(alpha: float, steps: int) -> np.ndarray:
    profile = np.zeros(steps, dtype=float)
    profile[0] = 1.0 / alpha
    return profile


def test_finite_h_force_port_closes_recurrence_and_normalizes_work() -> None:
    case = matched_scalar_continuum_case(
        alpha=0.05,
        tail_extent=1.0,
        restoring_per_memory_time=2.0,
        diffusion_per_memory_time=1.0e-4,
        dim=1,
    )
    force = _unit_native_impulse(case.alpha, 3 * case.horizon)
    response = finite_h_force_work_response(
        case, normalized_force_profile=force
    )
    positions = np.asarray(response["positions"])

    assert response["maximum_recurrence_residual"] < 1.0e-14
    assert positions[1] == 1.0
    assert np.isclose(case.alpha * response["cumulative_work"][-1], 1.0)
    expected_post_velocity = -case.restoring_per_memory_time * (
        1.0 - case.centroid_deposition_fraction
    )
    assert np.isclose(
        (positions[2] - positions[1]) / case.alpha,
        expected_post_velocity,
    )

    continuum = continuum_unit_impulse_response(
        case, sample_times=response["sample_times"]
    )
    assert continuum["positions"][0] == 0.0
    assert continuum["positions"][1] == 1.0
    assert continuum["relative"][1] == 1.0


def test_nonlinear_force_port_matches_local_reference_and_has_exact_off_clone() -> None:
    case = matched_scalar_continuum_case(
        alpha=0.1,
        tail_extent=2.0,
        restoring_per_memory_time=1.0,
        diffusion_per_memory_time=1.0e-6,
        dim=1,
    )
    formation = np.zeros((case.horizon + 5, 1), dtype=float)
    continuation = np.zeros((10, 1), dtype=float)
    force = _unit_native_impulse(case.alpha, len(continuation))
    response = simulate_matched_force_work_response(
        case,
        formation_noise=formation,
        response_noise=continuation,
        impulse_fractions=[0.01, 0.02],
        normalized_force_profile=force,
        axis=[1.0],
    )
    reference = finite_h_force_work_response(
        case, normalized_force_profile=force
    )

    np.testing.assert_allclose(
        response.position_responses[:, :, 0],
        np.repeat(np.asarray(reference["positions"])[None, :], 2, axis=0),
        rtol=2.0e-9,
        atol=2.0e-12,
    )
    np.testing.assert_allclose(response.position_even_leakage, 0.0, atol=2.0e-12)
    assert response.force_off_maximum_residual == 0.0
    np.testing.assert_allclose(
        response.integrated_impulses, response.impulse_amplitudes
    )
    normalized_work = (
        case.alpha
        * response.paired_even_cumulative_work[:, -1]
        / np.square(response.impulse_amplitudes)
    )
    np.testing.assert_allclose(normalized_work, 1.0, rtol=1.0e-12)
    for impulse_index, impulse in enumerate(response.impulse_amplitudes):
        derived = np.concatenate(
            (
                [0.0],
                impulse
                * impulse
                * np.cumsum(
                    force
                    * np.diff(
                        response.center_responses[impulse_index, :, 0]
                    )
                ),
            )
        )
        np.testing.assert_allclose(
            response.paired_even_center_cumulative_work[impulse_index],
            derived,
            rtol=1.0e-12,
            atol=1.0e-18,
        )


def test_resolved_center_port_matches_positive_inertial_reference() -> None:
    case = matched_scalar_continuum_case(
        alpha=0.0025,
        tail_extent=12.0,
        restoring_per_memory_time=4.0,
        diffusion_per_memory_time=1.0e-4,
        dim=1,
    )
    pulse_width = 0.2
    force = np.zeros(round(1.4 / case.alpha), dtype=float)
    pulse_steps = round(pulse_width / case.alpha)
    force[:pulse_steps] = 1.0 / pulse_width
    exact = finite_h_force_work_response(
        case, normalized_force_profile=force
    )
    continuum = continuum_rectangular_force_response(
        case,
        sample_times=exact["sample_times"],
        pulse_width=pulse_width,
    )

    center = np.asarray(exact["centers"])
    relative = np.asarray(exact["relative"])
    center_work = np.asarray(exact["center_port_cumulative_work"])
    assert np.isclose(center_work[-1], np.sum(force * np.diff(center)))
    assert np.isclose(case.alpha * np.sum(force), 1.0)
    assert 0.0 < center[pulse_steps] < 0.1
    assert 0.6 < relative[pulse_steps] < 0.7
    assert 0.35 < center_work[-1] < 0.4
    assert (
        abs(float(exact["center_port_ledger_residual"][-1]))
        / center_work[-1]
        < 0.02
    )
    np.testing.assert_allclose(
        center,
        continuum["centers"],
        rtol=0.0,
        atol=1.3e-3,
    )


def test_stationary_center_msd_is_ballistic_and_matches_covariance() -> None:
    case = matched_scalar_continuum_case(
        alpha=0.0025,
        tail_extent=12.0,
        restoring_per_memory_time=4.0,
        diffusion_per_memory_time=1.0e-4,
        dim=3,
    )
    result = stationary_center_msd(
        case, dim=3, n_paths=32768, n_steps=16, seed=20260817
    )
    fit = slice(2, 17)
    discrete_error = np.sqrt(
        np.mean(
            np.square(
                result.simulated_msd[fit] - result.exact_discrete_msd[fit]
            )
        )
        / np.mean(np.square(result.exact_discrete_msd[fit]))
    )
    continuum_error = np.sqrt(
        np.mean(
            np.square(
                result.exact_discrete_msd[fit] - result.continuum_msd[fit]
            )
        )
        / np.mean(np.square(result.continuum_msd[fit]))
    )
    slope = np.polyfit(
        np.log(result.sample_times[fit]),
        np.log(result.simulated_msd[fit]),
        1,
    )[0]
    assert discrete_error < 0.03
    assert continuum_error < 0.02
    assert 1.9 <= slope <= 2.1


def test_stationary_visible_msd_is_diffusive_and_matches_discrete_covariance() -> None:
    case = matched_scalar_continuum_case(
        alpha=0.0025,
        tail_extent=12.0,
        restoring_per_memory_time=4.0,
        diffusion_per_memory_time=1.0e-4,
        dim=3,
    )
    result = stationary_visible_msd(
        case, dim=3, n_paths=32768, n_steps=16, seed=20260816
    )
    relative_variance = (
        (case.q * case.epsilon) ** 2
        / (1.0 - case.untruncated_relative_root**2)
    )
    expected_first = 3.0 * (
        case.restoring_per_update**2 * relative_variance + case.epsilon**2
    )
    assert np.isclose(result.exact_discrete_msd[1], expected_first)

    fit = slice(2, 17)
    discrete_error = np.sqrt(
        np.mean(
            np.square(
                result.simulated_msd[fit] - result.exact_discrete_msd[fit]
            )
        )
        / np.mean(np.square(result.exact_discrete_msd[fit]))
    )
    continuum_error = np.sqrt(
        np.mean(
            np.square(result.exact_discrete_msd[fit] - result.continuum_msd[fit])
        )
        / np.mean(np.square(result.continuum_msd[fit]))
    )
    slope = np.polyfit(
        np.log(result.sample_times[fit]),
        np.log(result.simulated_msd[fit]),
        1,
    )[0]
    assert discrete_error < 0.03
    assert continuum_error < 0.01
    assert 0.9 <= slope <= 1.1


def test_registered_force_port_cases_have_unit_area_and_predictive_rate_fit() -> None:
    cases = registered_cases()
    assert [case.alpha for case in cases] == list(ALPHA_VALUES)
    assert len({(case.alpha, case.horizon) for case in cases}) == len(cases)

    case = cases[-1]
    profile = _unit_impulse_profile(case.alpha, 32)
    assert np.isclose(case.alpha * np.sum(profile), 1.0)
    exact = finite_h_force_work_response(
        case, normalized_force_profile=profile
    )
    _, fitted_rate, supported = _fit_postpulse_rate(
        np.asarray(exact["relative"]),
        np.asarray(exact["relative"]),
        alpha=case.alpha,
    )
    assert supported > 10
    assert fitted_rate > 0.0
