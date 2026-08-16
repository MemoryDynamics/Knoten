from __future__ import annotations

import numpy as np

from experiments.current.dynamics.scaling.scalar_memory_center_inertial_port_gate import (
    ALPHA_VALUES,
    GAMMA,
    PULSE_WIDTHS,
    _center_ledger,
    _center_work_from_odd_response,
    _mass_and_damping,
    _rectangular_profile,
    registered_cases,
)


def test_registered_center_port_profiles_are_resolved_and_unit_area() -> None:
    cases = registered_cases()
    assert [case.alpha for case in cases] == list(ALPHA_VALUES)
    for case in cases:
        profile = _rectangular_profile(
            alpha=case.alpha,
            pulse_width=0.2,
            free_response_time=1.2,
        )
        assert np.isclose(case.alpha * np.sum(profile), 1.0)
        assert np.count_nonzero(profile) == round(0.2 / case.alpha)
    holdout = cases[-1]
    for width in PULSE_WIDTHS:
        profile = _rectangular_profile(
            alpha=holdout.alpha,
            pulse_width=width,
            free_response_time=1.2,
        )
        assert np.isclose(holdout.alpha * np.sum(profile), 1.0)
        assert np.count_nonzero(profile) == round(width / holdout.alpha)


def test_registered_mass_estimator_recovers_unit_mass_and_gamma_five() -> None:
    for width in PULSE_WIDTHS:
        z = GAMMA * width
        pulse_end_velocity = (1.0 - np.exp(-z)) / z
        gain, mass, damping = _mass_and_damping(
            pulse_end_velocity=pulse_end_velocity,
            fitted_rate=GAMMA,
            pulse_width=width,
        )
        assert np.isclose(gain, 1.0)
        assert np.isclose(mass, 1.0)
        assert np.isclose(damping, GAMMA)


def test_center_work_and_positive_storage_ledger_close_for_smooth_trace() -> None:
    alpha = 0.001
    width = 0.2
    profile = _rectangular_profile(
        alpha=alpha,
        pulse_width=width,
        free_response_time=1.2,
    )
    times = alpha * np.arange(profile.size + 1)
    z = GAMMA * width
    relative = np.empty_like(times)
    inside = times <= width
    relative[inside] = (
        1.0 - np.exp(-GAMMA * times[inside])
    ) / z
    relative_end = (1.0 - np.exp(-z)) / z
    relative[~inside] = relative_end * np.exp(
        -GAMMA * (times[~inside] - width)
    )
    center = np.zeros_like(times)
    center[1:] = np.cumsum(
        alpha * 0.5 * (relative[:-1] + relative[1:])
    )
    work = _center_work_from_odd_response(center, profile)
    ledger = _center_ledger(
        relative[:, None], work, alpha=alpha
    )
    assert abs(ledger[-1]) / work[-1] < 1.0e-4
