"""Run the preregistered scalar-memory center inertial-port gate."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
import json
import math
from pathlib import Path
import sys
import time
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    aggregate_standard_normal_increments,
    continuum_rectangular_force_response,
    finite_h_force_work_response,
    matched_scalar_continuum_case,
    simulate_matched_force_work_response,
    stationary_center_msd,
)
from experiments.current.dynamics.scaling import (  # noqa: E402
    scalar_memory_continuum_limit_gate as continuum_gate,
)


DEFAULT_REPORT = Path(
    "reports/dynamics/limits/"
    "scalar_memory_center_inertial_port_gate_2026-08-16.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/limits/"
    "scalar_memory_center_inertial_port_gate_2026-08-16.json"
)
DEFAULT_FIGURE = Path(
    "figures/draft/dynamics/limits/"
    "scalar_memory_center_inertial_port_gate_2026-08-16.png"
)
PREREGISTRATION = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_center_inertial_port_protocol_2026-08-16.md"
)
PRECEDING_VISIBLE_PORT_REPORT = Path(
    "reports/dynamics/limits/"
    "scalar_memory_force_work_port_gate_2026-08-16.md"
)

ALPHA_VALUES = (0.04, 0.02, 0.01, 0.005, 0.0025)
HOLDOUT_ALPHA = 0.0025
TAIL_EXTENT = 12.0
IMPULSE_FRACTIONS = (0.005, 0.01)
FORMATION_SEEDS = (16, 17, 18, 19, 20)
NOISE_SEED = 20_260_817
MSD_SEED = 20_260_817
MSD_PATHS = 65_536
MSD_STEPS = 16
MSD_FIT_START = 2

DIM = 3
CHI = 4.0
GAMMA = 1.0 + CHI
DIFFUSION = 1.0e-4
MEMORY_MASS = 1.0
SIGMA_REP = 1.0
SIGMA_ATT = 3.0
AMPLITUDE_REP = 1.0
AMPLITUDE_ATT = 35.0
FORMATION_TIME = 20.0
FREE_RESPONSE_TIME = 1.2
MAIN_PULSE_WIDTH = 0.2
PULSE_WIDTHS = (0.4, 0.2, 0.1, 0.05)


def _case_key(alpha: float) -> str:
    return f"alpha_{alpha:.4g}_C_{TAIL_EXTENT:g}"


def _width_key(width: float) -> str:
    return f"delta_{width:.4g}"


def registered_cases() -> list[Any]:
    """Return the five registered matched center-port cases."""

    return [
        matched_scalar_continuum_case(
            alpha=alpha,
            tail_extent=TAIL_EXTENT,
            restoring_per_memory_time=CHI,
            diffusion_per_memory_time=DIFFUSION,
            dim=DIM,
            memory_mass=MEMORY_MASS,
            sigma_rep=SIGMA_REP,
            sigma_att=SIGMA_ATT,
            amplitude_rep=AMPLITUDE_REP,
            amplitude_att=AMPLITUDE_ATT,
        )
        for alpha in ALPHA_VALUES
    ]


def _integer_steps(duration: float, alpha: float) -> int:
    return continuum_gate._integer_steps(duration, alpha)


def _rectangular_profile(
    *, alpha: float, pulse_width: float, free_response_time: float
) -> np.ndarray:
    pulse_steps = _integer_steps(pulse_width, alpha)
    total_steps = _integer_steps(pulse_width + free_response_time, alpha)
    profile = np.zeros(total_steps, dtype=float)
    profile[:pulse_steps] = 1.0 / pulse_width
    if not math.isclose(
        alpha * float(np.sum(profile)), 1.0, rel_tol=0.0, abs_tol=1.0e-14
    ):
        raise RuntimeError("rectangular force profile does not have unit area")
    return profile


def _coupled_noise(
    *, seed: int, minimum_alpha: float, total_time: float, dim: int
) -> np.ndarray:
    steps = _integer_steps(total_time, minimum_alpha)
    return np.random.default_rng(NOISE_SEED + int(seed)).standard_normal(
        (steps, dim)
    )


def _noise_at_alpha(
    fine_noise: np.ndarray, alpha: float, minimum_alpha: float
) -> np.ndarray:
    ratio_float = alpha / minimum_alpha
    ratio = int(round(ratio_float))
    if not math.isclose(ratio_float, ratio, rel_tol=0.0, abs_tol=1.0e-10):
        raise ValueError("alpha grid must be an integer multiple of minimum alpha")
    return aggregate_standard_normal_increments(fine_noise, ratio)


def _normalized_rms_error(observed: np.ndarray, reference: np.ndarray) -> float:
    return continuum_gate._normalized_rms_error(observed, reference)


def _median(values: Iterable[float]) -> float:
    finite = [float(value) for value in values if math.isfinite(float(value))]
    if not finite:
        raise ValueError("cannot aggregate an empty finite collection")
    return float(np.median(finite))


def _fit_postpulse_rate(
    values: np.ndarray,
    reference: np.ndarray,
    *,
    alpha: float,
    pulse_steps: int,
) -> tuple[float, float, int]:
    observed = np.asarray(values, dtype=float)
    exact = np.asarray(reference, dtype=float)
    if observed.shape != exact.shape or pulse_steps >= observed.size - 3:
        raise ValueError("post-pulse response must match its reference")
    return continuum_gate._fit_response_rate(
        observed[pulse_steps:],
        exact[pulse_steps:],
        alpha=alpha,
    )


def _mass_and_damping(
    *, pulse_end_velocity: float, fitted_rate: float, pulse_width: float
) -> tuple[float, float, float]:
    z = fitted_rate * pulse_width
    denominator = -math.expm1(-z)
    gain = pulse_end_velocity * z / denominator
    if not math.isfinite(gain) or gain <= 0.0:
        return float("nan"), float("nan"), float("nan")
    mass = 1.0 / gain
    damping = fitted_rate / gain
    return gain, mass, damping


def _center_work_from_odd_response(
    center_response: np.ndarray, force_profile: np.ndarray
) -> np.ndarray:
    projected = np.asarray(center_response, dtype=float)
    profile = np.asarray(force_profile, dtype=float)
    if projected.ndim != 1 or projected.size != profile.size + 1:
        raise ValueError("center response and force profile must align")
    return np.concatenate(
        ([0.0], np.cumsum(profile * np.diff(projected)))
    )


def _center_ledger(
    relative_response: np.ndarray,
    center_work_coefficient: np.ndarray,
    *,
    alpha: float,
) -> np.ndarray:
    relative = np.asarray(relative_response, dtype=float)
    work = np.asarray(center_work_coefficient, dtype=float)
    if relative.ndim != 2 or work.shape != (relative.shape[0],):
        raise ValueError("relative response and center work must align")
    norm2 = np.sum(relative * relative, axis=1)
    kinetic = 0.5 * norm2
    dissipation = np.concatenate(
        (
            [0.0],
            np.cumsum(GAMMA * alpha * 0.5 * (norm2[:-1] + norm2[1:])),
        )
    )
    return kinetic - kinetic[0] - work + dissipation


def _run_response(
    case: Any,
    *,
    seed: int,
    fine_noise: np.ndarray,
    minimum_alpha: float,
    pulse_width: float,
) -> dict[str, Any]:
    coarse = _noise_at_alpha(fine_noise, case.alpha, minimum_alpha)
    n_formation = _integer_steps(FORMATION_TIME, case.alpha)
    profile = _rectangular_profile(
        alpha=case.alpha,
        pulse_width=pulse_width,
        free_response_time=FREE_RESPONSE_TIME,
    )
    n_response = profile.size
    required = n_formation + n_response
    if coarse.shape[0] < required:
        raise ValueError("coupled noise is shorter than the registered response")
    response = simulate_matched_force_work_response(
        case,
        formation_noise=coarse[:n_formation],
        response_noise=coarse[n_formation:required],
        impulse_fractions=IMPULSE_FRACTIONS,
        normalized_force_profile=profile,
        axis=[1.0, 0.0, 0.0],
        memory_mass=MEMORY_MASS,
        sigma_rep=SIGMA_REP,
        sigma_att=SIGMA_ATT,
        amplitude_rep=AMPLITUDE_REP,
        amplitude_att=AMPLITUDE_ATT,
    )
    exact = finite_h_force_work_response(
        case, normalized_force_profile=profile
    )
    continuum = continuum_rectangular_force_response(
        case,
        sample_times=response.sample_times,
        pulse_width=pulse_width,
    )
    pulse_steps = _integer_steps(pulse_width, case.alpha)

    exact_center = np.asarray(exact["centers"], dtype=float)
    exact_relative = np.asarray(exact["relative"], dtype=float)
    exact_position = np.asarray(exact["positions"], dtype=float)
    exact_center_work = np.asarray(
        exact["center_port_cumulative_work"], dtype=float
    )
    continuum_center = np.asarray(continuum["centers"], dtype=float)
    continuum_relative = np.asarray(continuum["relative"], dtype=float)
    continuum_position = np.asarray(continuum["positions"], dtype=float)
    continuum_center_work = np.asarray(
        continuum["center_cumulative_work"], dtype=float
    )

    control_radii = np.asarray(response.memory_radii[:, 0], dtype=float)
    all_radii = np.asarray(response.memory_radii, dtype=float)
    radii_valid = bool(
        np.isfinite(all_radii).all()
        and np.all(all_radii > 0.0)
        and np.all(control_radii > 0.0)
    )
    if radii_valid:
        branch_ratios = all_radii[:, 2:] / control_radii[:, None]
        minimum_radius_ratio = float(np.min(branch_ratios))
        maximum_radius_ratio = float(np.max(branch_ratios))
    else:
        minimum_radius_ratio = None
        maximum_radius_ratio = None

    fractions: list[dict[str, Any]] = []
    center_traces: list[np.ndarray] = []
    relative_traces: list[np.ndarray] = []
    for impulse_index, fraction in enumerate(response.impulse_fractions):
        impulse = float(response.impulse_amplitudes[impulse_index])
        center_vector = np.asarray(
            response.center_responses[impulse_index], dtype=float
        )
        relative_vector = np.asarray(
            response.relative_responses[impulse_index], dtype=float
        )
        position_vector = np.asarray(
            response.position_responses[impulse_index], dtype=float
        )
        center_projected = center_vector[:, 0]
        relative_projected = relative_vector[:, 0]
        position_projected = position_vector[:, 0]
        center_traces.append(center_projected)
        relative_traces.append(relative_projected)

        _, fitted_rate, fit_count = _fit_postpulse_rate(
            relative_projected,
            exact_relative,
            alpha=case.alpha,
            pulse_steps=pulse_steps,
        )
        _, reference_rate, _ = _fit_postpulse_rate(
            exact_relative,
            exact_relative,
            alpha=case.alpha,
            pulse_steps=pulse_steps,
        )
        gain, inferred_mass, inferred_damping = _mass_and_damping(
            pulse_end_velocity=float(relative_projected[pulse_steps]),
            fitted_rate=fitted_rate,
            pulse_width=pulse_width,
        )

        raw_center_work = np.asarray(
            response.paired_even_center_cumulative_work[impulse_index],
            dtype=float,
        ) / (impulse * impulse)
        derived_center_work = _center_work_from_odd_response(
            center_projected, profile
        )
        work_scale = max(abs(float(raw_center_work[-1])), 1.0e-30)
        work_identity_error = float(
            np.max(np.abs(raw_center_work - derived_center_work)) / work_scale
        )
        ledger = _center_ledger(
            relative_vector,
            raw_center_work,
            alpha=case.alpha,
        )
        ledger_relative_residual = (
            abs(float(ledger[-1])) / abs(float(raw_center_work[-1]))
        )

        position_even = np.asarray(
            response.position_even_leakage[impulse_index], dtype=float
        )
        relative_even = np.asarray(
            response.relative_even_leakage[impulse_index], dtype=float
        )
        center_even = position_even - relative_even
        mirror_even = max(
            float(np.max(np.linalg.norm(position_even, axis=1))),
            float(np.max(np.linalg.norm(relative_even, axis=1))),
            float(np.max(np.linalg.norm(center_even, axis=1))),
        )
        cross_axis = max(
            float(np.max(np.linalg.norm(center_vector[:, 1:], axis=1))),
            float(np.max(np.linalg.norm(relative_vector[:, 1:], axis=1))),
            float(np.max(np.linalg.norm(position_vector[:, 1:], axis=1))),
        )
        first_force_off_center_velocity = float(
            (
                center_projected[pulse_steps + 1]
                - center_projected[pulse_steps]
            )
            / case.alpha
        )
        fractions.append(
            {
                "impulse_fraction": float(fraction),
                "impulse_amplitude": impulse,
                "integrated_input_relative_error": abs(
                    float(response.integrated_impulses[impulse_index]) / impulse
                    - 1.0
                ),
                "normalized_rms_center_error_exact": _normalized_rms_error(
                    center_projected, exact_center
                ),
                "normalized_rms_relative_error_exact": _normalized_rms_error(
                    relative_projected, exact_relative
                ),
                "normalized_rms_position_error_exact": _normalized_rms_error(
                    position_projected, exact_position
                ),
                "normalized_rms_center_error_continuum": _normalized_rms_error(
                    center_projected, continuum_center
                ),
                "normalized_rms_relative_error_continuum": _normalized_rms_error(
                    relative_projected, continuum_relative
                ),
                "normalized_rms_position_error_continuum": _normalized_rms_error(
                    position_projected, continuum_position
                ),
                "center_work_coefficient": float(raw_center_work[-1]),
                "center_work_error_exact": abs(
                    float(raw_center_work[-1]) - float(exact_center_work[-1])
                )
                / abs(float(exact_center_work[-1])),
                "center_work_error_continuum": abs(
                    float(raw_center_work[-1])
                    - float(continuum_center_work[-1])
                )
                / abs(float(continuum_center_work[-1])),
                "center_work_identity_relative_error": work_identity_error,
                "nonlinear_center_ledger_relative_residual": (
                    ledger_relative_residual
                ),
                "fitted_rate": fitted_rate,
                "reference_fitted_rate": reference_rate,
                "relative_rate_error_exact": abs(fitted_rate - reference_rate)
                / reference_rate,
                "input_gain": gain,
                "inferred_mass": inferred_mass,
                "inferred_damping": inferred_damping,
                "pulse_end_center_displacement_per_impulse": float(
                    center_projected[pulse_steps]
                ),
                "pulse_end_relative_velocity_per_impulse": float(
                    relative_projected[pulse_steps]
                ),
                "first_force_off_center_velocity_per_impulse": (
                    first_force_off_center_velocity
                ),
                "mirror_even_maximum": mirror_even,
                "cross_axis_maximum": cross_axis,
                "fit_sample_count": fit_count,
                "projected_center_response": center_projected,
                "projected_relative_response": relative_projected,
                "projected_position_response": position_projected,
                "center_work_coefficient_trace": raw_center_work,
                "center_ledger_trace": ledger,
            }
        )

    center_strength_difference = center_traces[0] - center_traces[1]
    relative_strength_difference = relative_traces[0] - relative_traces[1]
    strength_rms = max(
        _normalized_rms_error(center_traces[0], center_traces[1]),
        _normalized_rms_error(relative_traces[0], relative_traces[1]),
    )
    strength_maximum = max(
        float(np.max(np.abs(center_strength_difference))),
        float(np.max(np.abs(relative_strength_difference))),
    )
    exact_final_work = float(exact_center_work[-1])
    exact_ledger_relative_residual = (
        abs(float(exact["center_port_ledger_residual"][-1]))
        / abs(exact_final_work)
    )
    return {
        "seed": int(seed),
        "pulse_width": float(pulse_width),
        "pulse_steps": int(pulse_steps),
        "integer_pulse_steps": math.isclose(
            pulse_steps * case.alpha,
            pulse_width,
            rel_tol=0.0,
            abs_tol=1.0e-14,
        ),
        "force_off_maximum_residual": response.force_off_maximum_residual,
        "all_memory_radii_positive_finite": radii_valid,
        "minimum_memory_radius": float(np.nanmin(all_radii)),
        "maximum_memory_radius": float(np.nanmax(all_radii)),
        "minimum_simultaneous_forced_control_radius_ratio": (
            minimum_radius_ratio
        ),
        "maximum_simultaneous_forced_control_radius_ratio": (
            maximum_radius_ratio
        ),
        "strength_nonlinearity_rms": strength_rms,
        "strength_nonlinearity_maximum": strength_maximum,
        "analytic_maximum_recurrence_residual": float(
            exact["maximum_recurrence_residual"]
        ),
        "exact_center_ledger_relative_residual": (
            exact_ledger_relative_residual
        ),
        "sample_times": response.sample_times,
        "force_profile": profile,
        "exact_center_response": exact_center,
        "exact_relative_response": exact_relative,
        "exact_position_response": exact_position,
        "exact_center_work_coefficient_trace": exact_center_work,
        "continuum_center_response": continuum_center,
        "continuum_relative_response": continuum_relative,
        "continuum_position_response": continuum_position,
        "continuum_center_work_coefficient_trace": continuum_center_work,
        "fractions": fractions,
    }


def _aggregate_response(
    case: Any, seeds: list[dict[str, Any]]
) -> dict[str, Any]:
    fractions = [row for seed in seeds for row in seed["fractions"]]
    ratio_minima = [
        seed["minimum_simultaneous_forced_control_radius_ratio"]
        for seed in seeds
        if seed["minimum_simultaneous_forced_control_radius_ratio"] is not None
    ]
    ratio_maxima = [
        seed["maximum_simultaneous_forced_control_radius_ratio"]
        for seed in seeds
        if seed["maximum_simultaneous_forced_control_radius_ratio"] is not None
    ]
    return {
        "case": asdict(case),
        "pulse_width": seeds[0]["pulse_width"],
        "pulse_steps": seeds[0]["pulse_steps"],
        "integer_pulse_steps": all(
            seed["integer_pulse_steps"] for seed in seeds
        ),
        "maximum_integrated_input_relative_error": max(
            row["integrated_input_relative_error"] for row in fractions
        ),
        "maximum_force_off_residual": max(
            seed["force_off_maximum_residual"] for seed in seeds
        ),
        "maximum_analytic_recurrence_residual": max(
            seed["analytic_maximum_recurrence_residual"] for seed in seeds
        ),
        "maximum_center_work_identity_relative_error": max(
            row["center_work_identity_relative_error"] for row in fractions
        ),
        "median_mirror_even_maximum": _median(
            row["mirror_even_maximum"] for row in fractions
        ),
        "maximum_mirror_even_maximum": max(
            row["mirror_even_maximum"] for row in fractions
        ),
        "maximum_cross_axis_response": max(
            row["cross_axis_maximum"] for row in fractions
        ),
        "median_strength_nonlinearity_rms": _median(
            seed["strength_nonlinearity_rms"] for seed in seeds
        ),
        "maximum_strength_nonlinearity_maximum": max(
            seed["strength_nonlinearity_maximum"] for seed in seeds
        ),
        "all_memory_radii_positive_finite": all(
            seed["all_memory_radii_positive_finite"] for seed in seeds
        ),
        "minimum_memory_radius": min(
            seed["minimum_memory_radius"] for seed in seeds
        ),
        "maximum_memory_radius": max(
            seed["maximum_memory_radius"] for seed in seeds
        ),
        "minimum_simultaneous_forced_control_radius_ratio": (
            min(ratio_minima) if ratio_minima else None
        ),
        "maximum_simultaneous_forced_control_radius_ratio": (
            max(ratio_maxima) if ratio_maxima else None
        ),
        "median_center_error_exact": _median(
            row["normalized_rms_center_error_exact"] for row in fractions
        ),
        "median_relative_error_exact": _median(
            row["normalized_rms_relative_error_exact"] for row in fractions
        ),
        "median_center_error_continuum": _median(
            row["normalized_rms_center_error_continuum"] for row in fractions
        ),
        "median_relative_error_continuum": _median(
            row["normalized_rms_relative_error_continuum"] for row in fractions
        ),
        "median_relative_rate_error_exact": _median(
            row["relative_rate_error_exact"] for row in fractions
        ),
        "median_fitted_rate": _median(
            row["fitted_rate"] for row in fractions
        ),
        "median_reference_fitted_rate": _median(
            row["reference_fitted_rate"] for row in fractions
        ),
        "median_input_gain": _median(row["input_gain"] for row in fractions),
        "median_inferred_mass": _median(
            row["inferred_mass"] for row in fractions
        ),
        "median_inferred_damping": _median(
            row["inferred_damping"] for row in fractions
        ),
        "median_center_work_coefficient": _median(
            row["center_work_coefficient"] for row in fractions
        ),
        "median_center_work_error_exact": _median(
            row["center_work_error_exact"] for row in fractions
        ),
        "median_center_work_error_continuum": _median(
            row["center_work_error_continuum"] for row in fractions
        ),
        "exact_center_ledger_relative_residual": seeds[0][
            "exact_center_ledger_relative_residual"
        ],
        "median_nonlinear_center_ledger_relative_residual": _median(
            row["nonlinear_center_ledger_relative_residual"]
            for row in fractions
        ),
        "median_pulse_end_center_displacement_per_impulse": _median(
            row["pulse_end_center_displacement_per_impulse"]
            for row in fractions
        ),
        "median_pulse_end_relative_velocity_per_impulse": _median(
            row["pulse_end_relative_velocity_per_impulse"]
            for row in fractions
        ),
        "median_first_force_off_center_velocity_per_impulse": _median(
            row["first_force_off_center_velocity_per_impulse"]
            for row in fractions
        ),
        "sample_times": seeds[0]["sample_times"],
        "force_profile": seeds[0]["force_profile"],
        "median_center_response": np.median(
            np.stack(
                [
                    row["projected_center_response"]
                    for row in fractions
                ]
            ),
            axis=0,
        ),
        "median_relative_response": np.median(
            np.stack(
                [
                    row["projected_relative_response"]
                    for row in fractions
                ]
            ),
            axis=0,
        ),
        "median_center_work_coefficient_trace": np.median(
            np.stack(
                [
                    row["center_work_coefficient_trace"]
                    for row in fractions
                ]
            ),
            axis=0,
        ),
        "exact_center_response": seeds[0]["exact_center_response"],
        "exact_relative_response": seeds[0]["exact_relative_response"],
        "exact_center_work_coefficient_trace": seeds[0][
            "exact_center_work_coefficient_trace"
        ],
        "continuum_center_response": seeds[0]["continuum_center_response"],
        "continuum_relative_response": seeds[0][
            "continuum_relative_response"
        ],
        "continuum_center_work_coefficient_trace": seeds[0][
            "continuum_center_work_coefficient_trace"
        ],
        "seeds": seeds,
    }


def _msd_diagnostics(holdout_case: Any) -> dict[str, Any]:
    result = stationary_center_msd(
        holdout_case,
        dim=DIM,
        n_paths=MSD_PATHS,
        n_steps=MSD_STEPS,
        seed=MSD_SEED,
    )
    fit = slice(MSD_FIT_START, MSD_STEPS + 1)
    simulated = np.asarray(result.simulated_msd[fit], dtype=float)
    exact = np.asarray(result.exact_discrete_msd[fit], dtype=float)
    continuum = np.asarray(result.continuum_msd[fit], dtype=float)
    times = np.asarray(result.sample_times[fit], dtype=float)
    return {
        "sample_times": result.sample_times,
        "simulated_msd": result.simulated_msd,
        "exact_discrete_msd": result.exact_discrete_msd,
        "continuum_msd": result.continuum_msd,
        "fit_start_step": MSD_FIT_START,
        "fit_stop_step": MSD_STEPS,
        "n_paths": MSD_PATHS,
        "seed": MSD_SEED,
        "normalized_rms_error_exact_discrete": _normalized_rms_error(
            simulated, exact
        ),
        "normalized_rms_error_exact_to_continuum": _normalized_rms_error(
            exact, continuum
        ),
        "simulated_slope": float(
            np.polyfit(np.log(times), np.log(simulated), 1)[0]
        ),
        "exact_discrete_slope": float(
            np.polyfit(np.log(times), np.log(exact), 1)[0]
        ),
        "continuum_slope": float(
            np.polyfit(np.log(times), np.log(continuum), 1)[0]
        ),
    }


def _evaluate_gates(
    main_cases: dict[str, dict[str, Any]],
    width_ladder: dict[str, dict[str, Any]],
    msd: dict[str, Any],
) -> dict[str, Any]:
    main = list(main_cases.values())
    ladder = [width_ladder[_width_key(width)] for width in PULSE_WIDTHS]
    every = main + ladder
    even_values = [
        row["mirror_even_maximum"]
        for cell in every
        for seed in cell["seeds"]
        for row in seed["fractions"]
    ]
    strength_rms = [
        seed["strength_nonlinearity_rms"]
        for cell in every
        for seed in cell["seeds"]
    ]
    strength_max = [
        seed["strength_nonlinearity_maximum"]
        for cell in every
        for seed in cell["seeds"]
    ]
    minima = [
        cell["minimum_simultaneous_forced_control_radius_ratio"]
        for cell in every
    ]
    maxima = [
        cell["maximum_simultaneous_forced_control_radius_ratio"]
        for cell in every
    ]
    ratios_available = all(value is not None for value in minima + maxima)
    g0_checks = {
        "integrated_input": max(
            cell["maximum_integrated_input_relative_error"] for cell in every
        )
        <= 1.0e-14,
        "force_off_clone": max(
            cell["maximum_force_off_residual"] for cell in every
        )
        <= 1.0e-14,
        "analytic_reference": max(
            cell["maximum_analytic_recurrence_residual"] for cell in every
        )
        <= 1.0e-12,
        "center_work_identity": max(
            cell["maximum_center_work_identity_relative_error"]
            for cell in every
        )
        <= 1.0e-12,
        "mirror_even_median": _median(even_values) <= 1.0e-3,
        "mirror_even_maximum": max(even_values) <= 1.0e-2,
        "strength_median": _median(strength_rms) <= 1.0e-3,
        "strength_maximum": max(strength_max) <= 1.0e-2,
        "all_memory_radii_positive_finite": all(
            cell["all_memory_radii_positive_finite"] for cell in every
        ),
        "local_radius_maximum": max(
            cell["maximum_memory_radius"] / SIGMA_REP for cell in every
        )
        <= 0.02,
        "forced_control_radius_lower": bool(
            ratios_available and min(minima) >= 0.95
        ),
        "forced_control_radius_upper": bool(
            ratios_available and max(maxima) <= 1.05
        ),
        "integer_pulse_steps": all(
            cell["integer_pulse_steps"] for cell in every
        ),
    }
    g0 = all(g0_checks.values())

    holdout = main_cases[_case_key(HOLDOUT_ALPHA)]
    alpha_001 = main_cases[_case_key(0.01)]
    g1_checks = {
        "all_exact_center_errors": all(
            cell["median_center_error_exact"] <= 0.01 for cell in main
        ),
        "all_exact_relative_errors": all(
            cell["median_relative_error_exact"] <= 0.01 for cell in main
        ),
        "all_exact_rate_errors": all(
            cell["median_relative_rate_error_exact"] <= 0.01 for cell in main
        ),
        "all_exact_work_errors": all(
            cell["median_center_work_error_exact"] <= 0.01 for cell in main
        ),
        "holdout_continuum_center": (
            holdout["median_center_error_continuum"] <= 0.01
        ),
        "holdout_continuum_relative": (
            holdout["median_relative_error_continuum"] <= 0.01
        ),
        "holdout_continuum_work": (
            holdout["median_center_work_error_continuum"] <= 0.03
        ),
        "holdout_exact_ledger": (
            holdout["exact_center_ledger_relative_residual"] <= 0.02
        ),
        "exact_ledger_improves": (
            holdout["exact_center_ledger_relative_residual"]
            < alpha_001["exact_center_ledger_relative_residual"]
        ),
        "holdout_nonlinear_ledger": (
            holdout["median_nonlinear_center_ledger_relative_residual"] <= 0.03
        ),
        "nonlinear_ledger_improves": (
            holdout["median_nonlinear_center_ledger_relative_residual"]
            < alpha_001["median_nonlinear_center_ledger_relative_residual"]
        ),
        "msd_monte_carlo_reference": (
            msd["normalized_rms_error_exact_discrete"] <= 0.01
        ),
        "msd_discrete_continuum": (
            msd["normalized_rms_error_exact_to_continuum"] <= 0.02
        ),
    }
    g1_components = all(g1_checks.values())
    g1 = g0 and g1_components

    displacements = [
        cell["median_pulse_end_center_displacement_per_impulse"]
        for cell in ladder
    ]
    pulse_velocities = [
        cell["median_pulse_end_relative_velocity_per_impulse"]
        for cell in ladder
    ]
    force_off_velocities = [
        cell["median_first_force_off_center_velocity_per_impulse"]
        for cell in ladder
    ]
    work_coefficients = [
        cell["median_center_work_coefficient"] for cell in ladder
    ]
    smallest = ladder[-1]
    inertial_checks = {
        "positive_mass": 0.95
        <= holdout["median_inferred_mass"]
        <= 1.05,
        "positive_damping": 4.8
        <= holdout["median_inferred_damping"]
        <= 5.2,
        "positive_pulse_end_velocity": all(
            value > 0.0 for value in pulse_velocities
        ),
        "positive_force_off_velocity": all(
            value > 0.0 for value in force_off_velocities
        ),
        "displacement_decreases_with_width": all(
            left > right
            for left, right in zip(
                displacements[:-1], displacements[1:], strict=True
            )
        ),
        "velocity_increases_with_narrowing": all(
            left < right
            for left, right in zip(
                pulse_velocities[:-1],
                pulse_velocities[1:],
                strict=True,
            )
        ),
        "work_increases_with_narrowing": all(
            left < right
            for left, right in zip(
                work_coefficients[:-1],
                work_coefficients[1:],
                strict=True,
            )
        ),
        "small_width_no_position_feedthrough": (
            smallest["median_pulse_end_center_displacement_per_impulse"]
            <= 0.03
        ),
        "small_width_persistent_velocity": 0.84
        <= smallest["median_first_force_off_center_velocity_per_impulse"]
        <= 0.93,
        "finite_impulse_work": 0.44
        <= smallest["median_center_work_coefficient"]
        <= 0.52,
        "ballistic_center_msd": 1.9 <= msd["simulated_slope"] <= 2.1,
    }
    overdamped_checks = {
        "direct_center_feedthrough": 0.15
        <= smallest["median_pulse_end_center_displacement_per_impulse"]
        <= 0.25,
        "no_persistent_velocity": abs(
            smallest["median_first_force_off_center_velocity_per_impulse"]
        )
        <= 0.05,
        "divergent_rectangular_work": 0.15
        <= PULSE_WIDTHS[-1] * smallest["median_center_work_coefficient"]
        <= 0.25,
        "diffusive_center_msd": 0.9 <= msd["simulated_slope"] <= 1.1,
    }
    inertial_components = all(inertial_checks.values())
    overdamped_components = all(overdamped_checks.values())
    inertial = g1 and inertial_components
    overdamped = g1 and overdamped_components

    if not g0:
        decision = "center-port-experiment-inadequate"
    elif not g1_components:
        decision = "center-port-reference-closure-failed"
    elif inertial and not overdamped:
        decision = "center-port-supports-positive-effective-inertia"
    elif overdamped and not inertial:
        decision = "center-port-supports-overdamped-position"
    else:
        decision = "center-port-discrimination-inconclusive"
    return {
        "port_and_experimental_validity": {
            "pass": g0,
            "status": "pass" if g0 else "fail",
            "checks": g0_checks,
        },
        "center_response_work_and_reference_closure": {
            "pass": g1,
            "status": "blocked"
            if not g0
            else ("pass" if g1_components else "fail"),
            "component_checks_pass": g1_components,
            "checks": g1_checks,
        },
        "positive_center_inertial_signature": {
            "pass": inertial,
            "status": "blocked"
            if not g1
            else ("pass" if inertial_components else "fail"),
            "component_checks_pass": inertial_components,
            "checks": inertial_checks,
        },
        "overdamped_center_signature": {
            "pass": overdamped,
            "status": "blocked"
            if not g1
            else ("pass" if overdamped_components else "fail"),
            "component_checks_pass": overdamped_components,
            "checks": overdamped_checks,
        },
        "decision": decision,
    }


def run_gate(*, seeds: Iterable[int] = FORMATION_SEEDS) -> dict[str, Any]:
    """Run the complete preregistered center inertial-port audit."""

    started = time.perf_counter()
    selected_seeds = [int(seed) for seed in seeds]
    if not selected_seeds or len(set(selected_seeds)) != len(selected_seeds):
        raise ValueError("seeds must be a non-empty unique collection")
    cases = registered_cases()
    minimum_alpha = min(case.alpha for case in cases)
    maximum_total_time = (
        FORMATION_TIME + max(PULSE_WIDTHS) + FREE_RESPONSE_TIME
    )
    main_rows: dict[str, list[dict[str, Any]]] = {
        _case_key(case.alpha): [] for case in cases
    }
    ladder_rows: dict[str, list[dict[str, Any]]] = {
        _width_key(width): [] for width in PULSE_WIDTHS
    }
    holdout_case = next(case for case in cases if case.alpha == HOLDOUT_ALPHA)

    for seed in selected_seeds:
        fine_noise = _coupled_noise(
            seed=seed,
            minimum_alpha=minimum_alpha,
            total_time=maximum_total_time,
            dim=DIM,
        )
        holdout_main: dict[str, Any] | None = None
        for case in cases:
            key = _case_key(case.alpha)
            print(
                f"running main {key} delta={MAIN_PULSE_WIDTH:g} seed={seed}",
                flush=True,
            )
            row = _run_response(
                case,
                seed=seed,
                fine_noise=fine_noise,
                minimum_alpha=minimum_alpha,
                pulse_width=MAIN_PULSE_WIDTH,
            )
            main_rows[key].append(row)
            if case.alpha == HOLDOUT_ALPHA:
                holdout_main = row
        if holdout_main is None:
            raise RuntimeError("holdout main response was not generated")
        for width in PULSE_WIDTHS:
            key = _width_key(width)
            if width == MAIN_PULSE_WIDTH:
                ladder_rows[key].append(holdout_main)
                continue
            print(
                f"running ladder alpha={HOLDOUT_ALPHA:g} "
                f"delta={width:g} seed={seed}",
                flush=True,
            )
            ladder_rows[key].append(
                _run_response(
                    holdout_case,
                    seed=seed,
                    fine_noise=fine_noise,
                    minimum_alpha=minimum_alpha,
                    pulse_width=width,
                )
            )

    main_aggregate = {
        _case_key(case.alpha): _aggregate_response(
            case, main_rows[_case_key(case.alpha)]
        )
        for case in cases
    }
    width_aggregate = {
        _width_key(width): _aggregate_response(
            holdout_case, ladder_rows[_width_key(width)]
        )
        for width in PULSE_WIDTHS
    }
    msd = _msd_diagnostics(holdout_case)
    gates = _evaluate_gates(main_aggregate, width_aggregate, msd)
    elapsed = time.perf_counter() - started

    response_paths = 2 + 2 * len(IMPULSE_FRACTIONS)
    main_updates_per_seed = sum(
        _integer_steps(FORMATION_TIME, case.alpha)
        + response_paths
        * _integer_steps(
            MAIN_PULSE_WIDTH + FREE_RESPONSE_TIME, case.alpha
        )
        for case in cases
    )
    ladder_updates_per_seed = sum(
        _integer_steps(FORMATION_TIME, HOLDOUT_ALPHA)
        + response_paths
        * _integer_steps(width + FREE_RESPONSE_TIME, HOLDOUT_ALPHA)
        for width in PULSE_WIDTHS
        if width != MAIN_PULSE_WIDTH
    )
    total_updates = len(selected_seeds) * (
        main_updates_per_seed + ladder_updates_per_seed
    )
    return {
        "schema": "emergenz-knoten.scalar-memory-center-inertial-port",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "simulation_revision": continuum_gate._git_output(["rev-parse", "HEAD"]),
        "git_status": continuum_gate._git_output(["status", "--short"]),
        "preregistration": PREREGISTRATION.as_posix(),
        "registration": {
            "alpha_values": ALPHA_VALUES,
            "holdout_alpha": HOLDOUT_ALPHA,
            "tail_extent": TAIL_EXTENT,
            "main_pulse_width": MAIN_PULSE_WIDTH,
            "pulse_widths": PULSE_WIDTHS,
            "impulse_fractions": IMPULSE_FRACTIONS,
            "formation_seeds": selected_seeds,
            "noise_seed": NOISE_SEED,
            "msd_seed": MSD_SEED,
            "msd_paths": MSD_PATHS,
            "msd_steps": MSD_STEPS,
            "msd_fit_steps": [MSD_FIT_START, MSD_STEPS],
            "dim": DIM,
            "chi": CHI,
            "gamma": GAMMA,
            "diffusion": DIFFUSION,
            "memory_mass": MEMORY_MASS,
            "formation_time": FORMATION_TIME,
            "free_response_time": FREE_RESPONSE_TIME,
            "port": {
                "input_update": "x_next += alpha * force",
                "output": "normalized finite-H memory center c",
                "work": "sum force dot (c_next-c)",
                "force_profile": "resolved unit-area rectangle",
            },
            "kernel": {
                "sigma_rep": SIGMA_REP,
                "sigma_att": SIGMA_ATT,
                "amplitude_rep": AMPLITUDE_REP,
                "amplitude_att": AMPLITUDE_ATT,
            },
        },
        "main_cases": main_aggregate,
        "width_ladder": width_aggregate,
        "msd": msd,
        "gates": gates,
        "decision": gates["decision"],
        "runtime": {
            "simulation_and_aggregation_seconds": elapsed,
            "dynamic_path_updates": total_updates,
            "dynamic_path_updates_per_second": total_updates / elapsed,
        },
        "analytic_identity": {
            "center_equation": "c_ddot + 5 c_dot = f + sqrt(2D) white_noise",
            "center_velocity_transfer": "1 / (s + 5)",
            "registered_mass": 1.0,
            "registered_damping": 5.0,
            "positive_storage": "0.5 * norm(r)^2",
            "visible_readout": "x = c + c_dot",
            "visible_velocity_transfer": "(s + 1) / (s + 5)",
        },
        "claim_limits": {
            "force_units": "dimensionless generalized force; no SI map",
            "mass_scope": "effective inertia of the normalized center output only",
            "work_conjugacy": "f dc is a prospective mathematical port pairing",
            "locality": "small-radius Taylor slice with matched alpha scaling",
            "double_limit": "finite width ladder, not a uniform proof",
            "physical_coordinate": "not established",
        },
    }


def _fmt(value: float | None) -> str:
    if value is None:
        return "unavailable"
    return continuum_gate._fmt(value)


def _write_figure(payload: dict[str, Any], path: Path) -> None:
    cases = payload["main_cases"]
    rows = [cases[_case_key(alpha)] for alpha in ALPHA_VALUES]
    ladder = [
        payload["width_ladder"][_width_key(width)] for width in PULSE_WIDTHS
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11.4, 8.3))

    for alpha, row in zip(ALPHA_VALUES, rows, strict=True):
        axes[0, 0].plot(
            row["sample_times"],
            row["median_center_response"],
            label=f"alpha={alpha:g}",
        )
    holdout = rows[-1]
    axes[0, 0].plot(
        holdout["sample_times"],
        holdout["continuum_center_response"],
        "k--",
        linewidth=2.0,
        label="positive-inertial continuum",
    )
    axes[0, 0].axvspan(0.0, MAIN_PULSE_WIDTH, color="gray", alpha=0.12)
    axes[0, 0].set_title("Center position response")
    axes[0, 0].set_xlabel("time")
    axes[0, 0].set_ylabel("center displacement / impulse")
    axes[0, 0].legend(fontsize=8)

    for alpha, row in zip(ALPHA_VALUES, rows, strict=True):
        axes[0, 1].plot(
            row["sample_times"],
            row["median_relative_response"],
            label=f"alpha={alpha:g}",
        )
    axes[0, 1].plot(
        holdout["sample_times"],
        holdout["continuum_relative_response"],
        "k--",
        linewidth=2.0,
        label="center velocity continuum",
    )
    axes[0, 1].axvspan(0.0, MAIN_PULSE_WIDTH, color="gray", alpha=0.12)
    axes[0, 1].set_title("Center velocity candidate r")
    axes[0, 1].set_xlabel("time")
    axes[0, 1].set_ylabel("r / impulse")
    axes[0, 1].legend(fontsize=8)

    widths = np.asarray(PULSE_WIDTHS)
    displacement = np.asarray(
        [
            row["median_pulse_end_center_displacement_per_impulse"]
            for row in ladder
        ]
    )
    velocity = np.asarray(
        [
            row["median_first_force_off_center_velocity_per_impulse"]
            for row in ladder
        ]
    )
    work = np.asarray(
        [row["median_center_work_coefficient"] for row in ladder]
    )
    axes[1, 0].semilogx(widths, displacement, "o-", label="Delta c / J")
    axes[1, 0].semilogx(widths, velocity, "^-", label="first force-off velocity / J")
    axes[1, 0].semilogx(widths, work, "s-", label="Wc / J^2")
    z = GAMMA * widths
    axes[1, 0].semilogx(
        widths,
        widths * (z - 1.0 + np.exp(-z)) / np.square(z),
        "k:",
        linewidth=1.2,
        label="continuum references",
    )
    axes[1, 0].semilogx(
        widths,
        (1.0 - np.exp(-z)) / z,
        "k:",
        linewidth=1.2,
    )
    axes[1, 0].semilogx(
        widths,
        (z - 1.0 + np.exp(-z)) / np.square(z),
        "k:",
        linewidth=1.2,
    )
    axes[1, 0].invert_xaxis()
    axes[1, 0].set_xticks(PULSE_WIDTHS)
    axes[1, 0].set_xticklabels([f"{width:g}" for width in PULSE_WIDTHS])
    axes[1, 0].tick_params(axis="x", which="minor", labelbottom=False)
    axes[1, 0].set_title("Resolved approach to the impulse limit")
    axes[1, 0].set_xlabel("pulse width (decreasing to the right)")
    axes[1, 0].set_ylabel("normalized response")
    axes[1, 0].legend(fontsize=8)

    msd = payload["msd"]
    times = np.asarray(msd["sample_times"])[MSD_FIT_START:]
    simulated = np.asarray(msd["simulated_msd"])[MSD_FIT_START:]
    exact = np.asarray(msd["exact_discrete_msd"])[MSD_FIT_START:]
    continuum = np.asarray(msd["continuum_msd"])[MSD_FIT_START:]
    axes[1, 1].loglog(times, simulated, "o", label="Monte Carlo")
    axes[1, 1].loglog(times, exact, "-", label="exact discrete")
    axes[1, 1].loglog(times, continuum, "--", label="continuum")
    anchor = simulated[0]
    axes[1, 1].loglog(
        times,
        anchor * times / times[0],
        ":",
        color="gray",
        label="slope 1",
    )
    axes[1, 1].loglog(
        times,
        anchor * np.square(times / times[0]),
        "-.",
        color="black",
        label="slope 2",
    )
    axes[1, 1].set_xticks((0.005, 0.01, 0.02, 0.04))
    axes[1, 1].set_xticklabels(("0.005", "0.01", "0.02", "0.04"))
    axes[1, 1].tick_params(axis="x", which="minor", labelbottom=False)
    axes[1, 1].set_title(
        f"Center MSD: slope={msd['simulated_slope']:.3f}"
    )
    axes[1, 1].set_xlabel("time")
    axes[1, 1].set_ylabel("MSD")
    axes[1, 1].legend(fontsize=8)

    for axis in axes.flat:
        axis.grid(alpha=0.25)
    fig.suptitle(payload["decision"], fontsize=12)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _write_report(
    payload: dict[str, Any], path: Path, figure: Path, summary: Path
) -> None:
    gates = payload["gates"]
    cases = payload["main_cases"]
    ladder = payload["width_ladder"]
    holdout = cases[_case_key(HOLDOUT_ALPHA)]
    msd = payload["msd"]
    radius_minima = [
        row["minimum_simultaneous_forced_control_radius_ratio"]
        for row in list(cases.values()) + list(ladder.values())
        if row["minimum_simultaneous_forced_control_radius_ratio"] is not None
    ]
    radius_maxima = [
        row["maximum_simultaneous_forced_control_radius_ratio"]
        for row in list(cases.values()) + list(ladder.values())
        if row["maximum_simultaneous_forced_control_radius_ratio"] is not None
    ]
    lines = [
        "# Scalar-memory center inertial-port gate",
        "",
        "Date: 2026-08-16.",
        "",
        "## Verdict",
        "",
        f"Decision: **{payload['decision']}**.",
        "",
        "| gate | status |",
        "|---|:---:|",
        f"| port and experimental validity | {gates['port_and_experimental_validity']['status']} |",
        f"| center response, work and reference closure | {gates['center_response_work_and_reference_closure']['status']} |",
        f"| positive center-inertial signature | {gates['positive_center_inertial_signature']['status']} |",
        f"| competing overdamped-center signature | {gates['overdamped_center_signature']['status']} |",
        "",
        "The microscopic input remains x_next += alpha f. The new output is",
        "the normalized finite-H memory center c, and supplied center work is",
        "the mirrored even average of sum f dot (c_next-c). No response-fitted",
        "coefficient rescales the force.",
        "",
        "## Fixed-width alpha family",
        "",
        "| alpha | H | exact center error | exact velocity error | continuum center error | continuum velocity error | inferred m | inferred gamma | Wc/J^2 | nonlinear ledger/work |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for alpha in ALPHA_VALUES:
        row = cases[_case_key(alpha)]
        lines.append(
            "| "
            f"{alpha:.6f} | {row['case']['horizon']} | "
            f"{_fmt(row['median_center_error_exact'])} | "
            f"{_fmt(row['median_relative_error_exact'])} | "
            f"{_fmt(row['median_center_error_continuum'])} | "
            f"{_fmt(row['median_relative_error_continuum'])} | "
            f"{_fmt(row['median_inferred_mass'])} | "
            f"{_fmt(row['median_inferred_damping'])} | "
            f"{_fmt(row['median_center_work_coefficient'])} | "
            f"{_fmt(row['median_nonlinear_center_ledger_relative_residual'])} |"
        )

    lines.extend(
        [
            "",
            "## Holdout pulse-width ladder",
            "",
            "| delta | native steps | Delta c/J | pulse-end velocity/J | first force-off velocity/J | Wc/J^2 | inferred m | inferred gamma |",
            "|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for width in PULSE_WIDTHS:
        row = ladder[_width_key(width)]
        lines.append(
            "| "
            f"{width:.6f} | {row['pulse_steps']} | "
            f"{_fmt(row['median_pulse_end_center_displacement_per_impulse'])} | "
            f"{_fmt(row['median_pulse_end_relative_velocity_per_impulse'])} | "
            f"{_fmt(row['median_first_force_off_center_velocity_per_impulse'])} | "
            f"{_fmt(row['median_center_work_coefficient'])} | "
            f"{_fmt(row['median_inferred_mass'])} | "
            f"{_fmt(row['median_inferred_damping'])} |"
        )

    radius_range = "unavailable"
    if radius_minima and radius_maxima:
        radius_range = (
            f"{_fmt(min(radius_minima))}..{_fmt(max(radius_maxima))}"
        )
    lines.extend(
        [
            "",
            "## Validity and discrimination diagnostics",
            "",
            f"- Maximum force-off clone residual: {_fmt(max(row['maximum_force_off_residual'] for row in cases.values()))}.",
            f"- Maximum analytic forced-recurrence residual: {_fmt(max(row['maximum_analytic_recurrence_residual'] for row in cases.values()))}.",
            f"- Maximum raw/odd center-work identity error: {_fmt(max(row['maximum_center_work_identity_relative_error'] for row in list(cases.values()) + list(ladder.values())))}.",
            f"- Maximum local radius R/sigma_rep: {_fmt(max(row['maximum_memory_radius'] / SIGMA_REP for row in list(cases.values()) + list(ladder.values())))}.",
            f"- Simultaneous forced/control radius range: {radius_range}.",
            f"- Holdout inferred mass and damping: {_fmt(holdout['median_inferred_mass'])}, {_fmt(holdout['median_inferred_damping'])}.",
            f"- Center-MSD slope: {msd['simulated_slope']:.6f} (exact discrete {msd['exact_discrete_slope']:.6f}, continuum {msd['continuum_slope']:.6f}).",
            f"- Monte Carlo center-MSD error to exact discrete reference: {_fmt(msd['normalized_rms_error_exact_discrete'])}.",
            "",
            "## Figure",
            "",
            f"![Center inertial-port gate]({continuum_gate._relative(path, figure)})",
            "",
            "## Interpretation boundary",
            "",
            "Evidence: the nonlinear finite-H center and relative responses close",
            "against their exact discrete references; resolved center work closes",
            "against the positive kinetic-storage ledger; the fixed-width alpha",
            "family and the independent pulse-width ladder select one registered",
            "input/output signature.",
            "",
            "Inference if the positive-inertial signature is selected: the",
            "normalized memory center is a dimensionless effective inertial",
            "coordinate with r as its velocity under this mathematical port.",
            "This does not reverse the preceding visible-x result because",
            "x=c+r mixes center position and center velocity.",
            "",
            "Not established: SI mass, uniqueness or physical observability of c,",
            "uniformity of the double limit, nonlinear long-run transfer, or a",
            "microscopic principle selecting f dc as physical work.",
            "",
            "## Provenance",
            "",
            f"- Protocol: [{PREREGISTRATION.name}]({continuum_gate._relative(path, continuum_gate._resolve(PREREGISTRATION))}).",
            f"- Preceding visible-port result: [{PRECEDING_VISIBLE_PORT_REPORT.name}]({continuum_gate._relative(path, continuum_gate._resolve(PRECEDING_VISIBLE_PORT_REPORT))}).",
            f"- Simulation revision: {payload['simulation_revision']}.",
            f"- Git status at execution: {payload['git_status'] or 'clean'}.",
            f"- Formation seeds: {','.join(str(seed) for seed in FORMATION_SEEDS)}; Brownian-coarsened common noise.",
            f"- Main pulse width: {MAIN_PULSE_WIDTH:g}; free response: {FREE_RESPONSE_TIME:g} memory times.",
            f"- Runtime: {payload['runtime']['simulation_and_aggregation_seconds']:.3f} s for {payload['runtime']['dynamic_path_updates']} dynamic path updates ({payload['runtime']['dynamic_path_updates_per_second']:.1f}/s).",
            f"- Machine-readable summary: [{summary.name}]({continuum_gate._relative(path, summary)}).",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--figure", type=Path, default=DEFAULT_FIGURE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = run_gate()
    report = continuum_gate._resolve(args.report)
    summary = continuum_gate._resolve(args.summary_json)
    figure = continuum_gate._resolve(args.figure)
    continuum_gate._write_json(summary, payload)
    _write_figure(payload, figure)
    _write_report(payload, report, figure, summary)
    print(json.dumps({"decision": payload["decision"], "report": str(report)}))


if __name__ == "__main__":
    main()
