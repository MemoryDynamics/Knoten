"""Run the preregistered scalar-memory force/work-port discrimination gate."""

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
    continuum_unit_impulse_response,
    finite_h_force_work_response,
    matched_scalar_continuum_case,
    simulate_matched_force_work_response,
    stationary_visible_msd,
)
from experiments.current.dynamics.scaling import (  # noqa: E402
    scalar_memory_continuum_limit_gate as continuum_gate,
)


DEFAULT_REPORT = Path(
    "reports/dynamics/limits/scalar_memory_force_work_port_gate_2026-08-16.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/limits/scalar_memory_force_work_port_gate_2026-08-16.json"
)
DEFAULT_FIGURE = Path(
    "figures/draft/dynamics/limits/"
    "scalar_memory_force_work_port_gate_2026-08-16.png"
)
PREREGISTRATION = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_force_work_port_protocol_2026-08-16.md"
)
CONTINUUM_REVIEW = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_continuum_limit_review_2026-08-15.md"
)

ALPHA_VALUES = (0.04, 0.02, 0.01, 0.005, 0.0025)
HOLDOUT_ALPHA = 0.0025
TAIL_EXTENT = 12.0
IMPULSE_FRACTIONS = (0.005, 0.01)
FORMATION_SEEDS = (11, 12, 13, 14, 15)
NOISE_SEED = 20_260_816
MSD_SEED = 20_260_816
MSD_PATHS = 65_536
MSD_STEPS = 16
MSD_FIT_START = 2
FIRST_PROSPECTIVE_EXECUTION_REVISION = (
    "e6a034b5ad08b862b041e60311c2cb92501178a2"
)

DIM = 3
CHI = 4.0
DIFFUSION = 1.0e-4
MEMORY_MASS = 1.0
SIGMA_REP = 1.0
SIGMA_ATT = 3.0
AMPLITUDE_REP = 1.0
AMPLITUDE_ATT = 35.0
FORMATION_TIME = 20.0
RESPONSE_TIME = 1.2


def _case_key(alpha: float) -> str:
    return f"alpha_{alpha:.4g}_C_{TAIL_EXTENT:g}"


def registered_cases() -> list[Any]:
    """Return the five registered matched force-port cases."""

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


def _unit_impulse_profile(alpha: float, n_steps: int) -> np.ndarray:
    profile = np.zeros(n_steps, dtype=float)
    profile[0] = 1.0 / alpha
    return profile


def _normalized_rms_error(observed: np.ndarray, reference: np.ndarray) -> float:
    return continuum_gate._normalized_rms_error(observed, reference)


def _fit_postpulse_rate(
    values: np.ndarray, reference: np.ndarray, *, alpha: float
) -> tuple[float, float, int]:
    observed = np.asarray(values, dtype=float)
    exact = np.asarray(reference, dtype=float)
    if observed.shape != exact.shape or observed.size < 4:
        raise ValueError("post-pulse response must match its reference")
    return continuum_gate._fit_response_rate(
        observed[1:], exact[1:], alpha=alpha
    )


def _run_case_seed(
    case: Any,
    *,
    seed: int,
    fine_noise: np.ndarray,
    minimum_alpha: float,
) -> dict[str, Any]:
    coarse = _noise_at_alpha(fine_noise, case.alpha, minimum_alpha)
    n_formation = _integer_steps(FORMATION_TIME, case.alpha)
    n_response = _integer_steps(RESPONSE_TIME, case.alpha)
    if coarse.shape[0] != n_formation + n_response:
        raise ValueError("coupled noise has the wrong registered duration")
    profile = _unit_impulse_profile(case.alpha, n_response)
    response = simulate_matched_force_work_response(
        case,
        formation_noise=coarse[:n_formation],
        response_noise=coarse[n_formation:],
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
    continuum = continuum_unit_impulse_response(
        case, sample_times=response.sample_times
    )
    exact_position = np.asarray(exact["positions"], dtype=float)
    exact_relative = np.asarray(exact["relative"], dtype=float)
    continuum_position = np.asarray(continuum["positions"], dtype=float)
    continuum_relative = np.asarray(continuum["relative"], dtype=float)

    fraction_rows: list[dict[str, Any]] = []
    projected_positions: list[np.ndarray] = []
    projected_relative: list[np.ndarray] = []
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

    for impulse_index, fraction in enumerate(response.impulse_fractions):
        position_vector = response.position_responses[impulse_index]
        relative_vector = response.relative_responses[impulse_index]
        projected_position = position_vector[:, 0]
        projected_r = relative_vector[:, 0]
        projected_positions.append(projected_position)
        projected_relative.append(projected_r)
        _, fitted_rate, fit_count = _fit_postpulse_rate(
            projected_r, exact_relative, alpha=case.alpha
        )
        _, reference_rate, _ = _fit_postpulse_rate(
            exact_relative, exact_relative, alpha=case.alpha
        )
        position_even = np.linalg.norm(
            response.position_even_leakage[impulse_index], axis=1
        )
        relative_even = np.linalg.norm(
            response.relative_even_leakage[impulse_index], axis=1
        )
        cross_axis = max(
            float(np.max(np.linalg.norm(position_vector[:, 1:], axis=1))),
            float(np.max(np.linalg.norm(relative_vector[:, 1:], axis=1))),
        )
        impulse = float(response.impulse_amplitudes[impulse_index])
        work_coefficient = float(
            case.alpha
            * response.paired_even_cumulative_work[impulse_index, -1]
            / (impulse * impulse)
        )
        fraction_rows.append(
            {
                "impulse_fraction": float(fraction),
                "impulse_amplitude": impulse,
                "integrated_input_relative_error": abs(
                    float(response.integrated_impulses[impulse_index]) / impulse
                    - 1.0
                ),
                "normalized_rms_position_error_exact": _normalized_rms_error(
                    projected_position, exact_position
                ),
                "normalized_rms_relative_error_exact": _normalized_rms_error(
                    projected_r, exact_relative
                ),
                "normalized_rms_position_error_continuum": _normalized_rms_error(
                    projected_position, continuum_position
                ),
                "normalized_rms_relative_error_continuum": _normalized_rms_error(
                    projected_r, continuum_relative
                ),
                "fitted_rate": fitted_rate,
                "reference_fitted_rate": reference_rate,
                "relative_rate_error_exact": abs(fitted_rate - reference_rate)
                / reference_rate,
                "mirror_even_maximum": max(
                    float(np.max(position_even)), float(np.max(relative_even))
                ),
                "cross_axis_maximum": cross_axis,
                "normalized_work_coefficient": work_coefficient,
                "pulse_end_feedthrough": float(projected_position[1]),
                "first_postpulse_velocity_per_impulse": float(
                    (projected_position[2] - projected_position[1]) / case.alpha
                ),
                "fit_sample_count": fit_count,
                "projected_position_response": projected_position,
                "projected_relative_response": projected_r,
            }
        )

    position_strength_difference = projected_positions[0] - projected_positions[1]
    relative_strength_difference = projected_relative[0] - projected_relative[1]
    position_strength_rms = _normalized_rms_error(
        projected_positions[0], projected_positions[1]
    )
    relative_strength_rms = _normalized_rms_error(
        projected_relative[0], projected_relative[1]
    )
    strength_rms = max(position_strength_rms, relative_strength_rms)
    strength_max = max(
        float(np.max(np.abs(position_strength_difference))),
        float(np.max(np.abs(relative_strength_difference))),
    )
    final_work = float(exact["cumulative_work"][-1])
    ledger_residual = abs(float(exact["ledger_residual"][-1])) / abs(final_work)
    return {
        "seed": int(seed),
        "force_off_maximum_residual": response.force_off_maximum_residual,
        "all_memory_radii_positive_finite": radii_valid,
        "minimum_memory_radius": float(np.nanmin(all_radii)),
        "maximum_memory_radius": float(np.nanmax(all_radii)),
        "minimum_simultaneous_forced_control_radius_ratio": minimum_radius_ratio,
        "maximum_simultaneous_forced_control_radius_ratio": maximum_radius_ratio,
        "strength_nonlinearity_rms": strength_rms,
        "strength_nonlinearity_maximum": strength_max,
        "analytic_maximum_recurrence_residual": float(
            exact["maximum_recurrence_residual"]
        ),
        "native_ledger_relative_residual": ledger_residual,
        "sample_times": response.sample_times,
        "exact_position_response": exact_position,
        "exact_relative_response": exact_relative,
        "continuum_position_response": continuum_position,
        "continuum_relative_response": continuum_relative,
        "fractions": fraction_rows,
    }


def _median(values: Iterable[float]) -> float:
    finite = [float(value) for value in values if math.isfinite(float(value))]
    if not finite:
        raise ValueError("cannot aggregate an empty finite collection")
    return float(np.median(finite))


def _aggregate_case(case: Any, seeds: list[dict[str, Any]]) -> dict[str, Any]:
    fractions = [row for seed in seeds for row in seed["fractions"]]
    seed_position_traces = [
        np.median(
            np.stack(
                [row["projected_position_response"] for row in seed["fractions"]]
            ),
            axis=0,
        )
        for seed in seeds
    ]
    seed_relative_traces = [
        np.median(
            np.stack(
                [row["projected_relative_response"] for row in seed["fractions"]]
            ),
            axis=0,
        )
        for seed in seeds
    ]
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
        "n_seeds": len(seeds),
        "maximum_integrated_input_relative_error": max(
            row["integrated_input_relative_error"] for row in fractions
        ),
        "maximum_force_off_residual": max(
            seed["force_off_maximum_residual"] for seed in seeds
        ),
        "maximum_analytic_recurrence_residual": max(
            seed["analytic_maximum_recurrence_residual"] for seed in seeds
        ),
        "maximum_work_coefficient_error": max(
            abs(row["normalized_work_coefficient"] - 1.0) for row in fractions
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
            min(ratio_minima) if len(ratio_minima) == len(seeds) else None
        ),
        "maximum_simultaneous_forced_control_radius_ratio": (
            max(ratio_maxima) if len(ratio_maxima) == len(seeds) else None
        ),
        "median_position_error_exact": _median(
            row["normalized_rms_position_error_exact"] for row in fractions
        ),
        "median_relative_error_exact": _median(
            row["normalized_rms_relative_error_exact"] for row in fractions
        ),
        "median_position_error_continuum": _median(
            row["normalized_rms_position_error_continuum"] for row in fractions
        ),
        "median_relative_error_continuum": _median(
            row["normalized_rms_relative_error_continuum"] for row in fractions
        ),
        "median_relative_rate_error_exact": _median(
            row["relative_rate_error_exact"] for row in fractions
        ),
        "median_fitted_rate": _median(row["fitted_rate"] for row in fractions),
        "median_reference_fitted_rate": _median(
            row["reference_fitted_rate"] for row in fractions
        ),
        "median_work_coefficient": _median(
            row["normalized_work_coefficient"] for row in fractions
        ),
        "median_pulse_end_feedthrough": _median(
            row["pulse_end_feedthrough"] for row in fractions
        ),
        "median_first_postpulse_velocity_per_impulse": _median(
            row["first_postpulse_velocity_per_impulse"] for row in fractions
        ),
        "native_ledger_relative_residual": seeds[0][
            "native_ledger_relative_residual"
        ],
        "sample_times": seeds[0]["sample_times"],
        "median_position_response": np.median(
            np.stack(seed_position_traces), axis=0
        ),
        "median_relative_response": np.median(
            np.stack(seed_relative_traces), axis=0
        ),
        "exact_position_response": seeds[0]["exact_position_response"],
        "exact_relative_response": seeds[0]["exact_relative_response"],
        "continuum_position_response": seeds[0]["continuum_position_response"],
        "continuum_relative_response": seeds[0]["continuum_relative_response"],
        "seeds": seeds,
    }


def _msd_diagnostics(holdout_case: Any) -> dict[str, Any]:
    result = stationary_visible_msd(
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
    simulated_slope = float(np.polyfit(np.log(times), np.log(simulated), 1)[0])
    exact_slope = float(np.polyfit(np.log(times), np.log(exact), 1)[0])
    continuum_slope = float(np.polyfit(np.log(times), np.log(continuum), 1)[0])
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
        "normalized_rms_error_continuum": _normalized_rms_error(
            simulated, continuum
        ),
        "simulated_slope": simulated_slope,
        "exact_discrete_slope": exact_slope,
        "continuum_slope": continuum_slope,
    }


def _evaluate_gates(
    cases: dict[str, dict[str, Any]], msd: dict[str, Any]
) -> dict[str, Any]:
    every = list(cases.values())
    even_values = [
        row["mirror_even_maximum"]
        for case in every
        for seed in case["seeds"]
        for row in seed["fractions"]
    ]
    strength_rms = [
        seed["strength_nonlinearity_rms"]
        for case in every
        for seed in case["seeds"]
    ]
    strength_max = [
        seed["strength_nonlinearity_maximum"]
        for case in every
        for seed in case["seeds"]
    ]
    minimum_ratios = [
        case["minimum_simultaneous_forced_control_radius_ratio"] for case in every
    ]
    maximum_ratios = [
        case["maximum_simultaneous_forced_control_radius_ratio"] for case in every
    ]
    ratios_available = all(value is not None for value in minimum_ratios + maximum_ratios)
    g0_checks = {
        "integrated_input": max(
            case["maximum_integrated_input_relative_error"] for case in every
        )
        <= 1.0e-14,
        "force_off_clone": max(
            case["maximum_force_off_residual"] for case in every
        )
        <= 1.0e-14,
        "analytic_reference": max(
            case["maximum_analytic_recurrence_residual"] for case in every
        )
        <= 1.0e-12,
        "work_normalization": max(
            case["maximum_work_coefficient_error"] for case in every
        )
        <= 1.0e-10,
        "mirror_even_median": _median(even_values) <= 1.0e-3,
        "mirror_even_maximum": max(even_values) <= 1.0e-2,
        "strength_median": _median(strength_rms) <= 1.0e-3,
        "strength_maximum": max(strength_max) <= 1.0e-2,
        "all_memory_radii_positive_finite": all(
            case["all_memory_radii_positive_finite"] for case in every
        ),
        "local_radius_maximum": max(
            case["maximum_memory_radius"] / SIGMA_REP for case in every
        )
        <= 0.02,
        "forced_control_radius_lower": bool(
            ratios_available and min(minimum_ratios) >= 0.95
        ),
        "forced_control_radius_upper": bool(
            ratios_available and max(maximum_ratios) <= 1.05
        ),
    }
    g0 = all(g0_checks.values())

    holdout = cases[_case_key(HOLDOUT_ALPHA)]
    alpha_001 = cases[_case_key(0.01)]
    g1_checks = {
        "all_exact_position_errors": all(
            case["median_position_error_exact"] <= 0.01 for case in every
        ),
        "all_exact_relative_errors": all(
            case["median_relative_error_exact"] <= 0.01 for case in every
        ),
        "all_exact_rate_errors": all(
            case["median_relative_rate_error_exact"] <= 0.01 for case in every
        ),
        "holdout_continuum_position": holdout[
            "median_position_error_continuum"
        ]
        <= 0.01,
        "holdout_continuum_relative": holdout[
            "median_relative_error_continuum"
        ]
        <= 0.01,
        "holdout_ledger": holdout["native_ledger_relative_residual"] <= 0.01,
        "ledger_improves": holdout["native_ledger_relative_residual"]
        < alpha_001["native_ledger_relative_residual"],
        "msd_reference": msd["normalized_rms_error_exact_discrete"] <= 0.01,
    }
    g1_components = all(g1_checks.values())
    g1 = g0 and g1_components

    overdamped_checks = {
        "direct_feedthrough": 0.95
        <= holdout["median_pulse_end_feedthrough"]
        <= 1.05,
        "restoring_postpulse_velocity": -4.1
        <= holdout["median_first_postpulse_velocity_per_impulse"]
        <= -3.5,
        "divergent_impulse_work_coefficient": 0.99
        <= holdout["median_work_coefficient"]
        <= 1.01,
        "diffusive_visible_msd": 0.9 <= msd["simulated_slope"] <= 1.1,
    }
    inertial_checks = {
        "no_direct_feedthrough": holdout["median_pulse_end_feedthrough"] <= 0.05,
        "positive_postpulse_velocity": holdout[
            "median_first_postpulse_velocity_per_impulse"
        ]
        > 0.0,
        "finite_impulse_work": holdout["median_work_coefficient"] <= 0.05,
        "ballistic_visible_msd": 1.8 <= msd["simulated_slope"] <= 2.2,
    }
    overdamped_components = all(overdamped_checks.values())
    inertial_components = all(inertial_checks.values())
    overdamped = g1 and overdamped_components
    inertial = g1 and inertial_components

    if not g0:
        decision = "force-port-experiment-inadequate"
    elif not g1_components:
        decision = "force-port-reference-closure-failed"
    elif overdamped and not inertial:
        decision = "force-port-supports-overdamped-memory-not-finite-inertial-mass"
    elif inertial and not overdamped:
        decision = "finite-inertial-port-signature-candidate"
    else:
        decision = "force-port-discrimination-inconclusive"
    return {
        "port_and_experimental_validity": {
            "pass": g0,
            "status": "pass" if g0 else "fail",
            "checks": g0_checks,
        },
        "force_response_and_ledger_closure": {
            "pass": g1,
            "status": "blocked" if not g0 else ("pass" if g1_components else "fail"),
            "component_checks_pass": g1_components,
            "checks": g1_checks,
        },
        "overdamped_memory_signature": {
            "pass": overdamped,
            "status": "blocked"
            if not g1
            else ("pass" if overdamped_components else "fail"),
            "component_checks_pass": overdamped_components,
            "checks": overdamped_checks,
        },
        "finite_inertial_signature": {
            "pass": inertial,
            "status": "blocked"
            if not g1
            else ("pass" if inertial_components else "fail"),
            "component_checks_pass": inertial_components,
            "checks": inertial_checks,
        },
        "decision": decision,
    }


def run_gate(*, seeds: Iterable[int] = FORMATION_SEEDS) -> dict[str, Any]:
    """Run the complete preregistered force/work-port audit."""

    started = time.perf_counter()
    selected_seeds = [int(seed) for seed in seeds]
    if not selected_seeds or len(set(selected_seeds)) != len(selected_seeds):
        raise ValueError("seeds must be a non-empty unique collection")
    cases = registered_cases()
    minimum_alpha = min(case.alpha for case in cases)
    total_time = FORMATION_TIME + RESPONSE_TIME
    rows: dict[str, list[dict[str, Any]]] = {
        _case_key(case.alpha): [] for case in cases
    }
    for seed in selected_seeds:
        fine_noise = _coupled_noise(
            seed=seed,
            minimum_alpha=minimum_alpha,
            total_time=total_time,
            dim=DIM,
        )
        for case in cases:
            key = _case_key(case.alpha)
            print(f"running {key} seed={seed}", flush=True)
            rows[key].append(
                _run_case_seed(
                    case,
                    seed=seed,
                    fine_noise=fine_noise,
                    minimum_alpha=minimum_alpha,
                )
            )
    aggregate = {
        _case_key(case.alpha): _aggregate_case(case, rows[_case_key(case.alpha)])
        for case in cases
    }
    holdout_case = next(case for case in cases if case.alpha == HOLDOUT_ALPHA)
    msd = _msd_diagnostics(holdout_case)
    gates = _evaluate_gates(aggregate, msd)
    elapsed = time.perf_counter() - started
    response_paths = 2 + 2 * len(IMPULSE_FRACTIONS)
    updates_per_seed = sum(
        _integer_steps(FORMATION_TIME, case.alpha)
        + response_paths * _integer_steps(RESPONSE_TIME, case.alpha)
        for case in cases
    )
    total_updates = len(selected_seeds) * updates_per_seed
    return {
        "schema": "emergenz-knoten.scalar-memory-force-work-port",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "simulation_revision": continuum_gate._git_output(["rev-parse", "HEAD"]),
        "git_status": continuum_gate._git_output(["status", "--short"]),
        "preregistration": PREREGISTRATION.as_posix(),
        "registration": {
            "alpha_values": ALPHA_VALUES,
            "holdout_alpha": HOLDOUT_ALPHA,
            "tail_extent": TAIL_EXTENT,
            "impulse_fractions": IMPULSE_FRACTIONS,
            "formation_seeds": selected_seeds,
            "noise_seed": NOISE_SEED,
            "msd_seed": MSD_SEED,
            "msd_paths": MSD_PATHS,
            "msd_steps": MSD_STEPS,
            "msd_fit_steps": [MSD_FIT_START, MSD_STEPS],
            "dim": DIM,
            "chi": CHI,
            "diffusion": DIFFUSION,
            "memory_mass": MEMORY_MASS,
            "formation_time": FORMATION_TIME,
            "response_time": RESPONSE_TIME,
            "port": {
                "update": "x_next += alpha * force",
                "work": "sum force dot (x_next-x)",
                "pulse_steps": 1,
            },
            "kernel": {
                "sigma_rep": SIGMA_REP,
                "sigma_att": SIGMA_ATT,
                "amplitude_rep": AMPLITUDE_REP,
                "amplitude_att": AMPLITUDE_ATT,
            },
        },
        "cases": aggregate,
        "msd": msd,
        "gates": gates,
        "decision": gates["decision"],
        "runtime": {
            "simulation_and_aggregation_seconds": elapsed,
            "dynamic_path_updates": total_updates,
            "dynamic_path_updates_per_second": total_updates / elapsed,
        },
        "posthoc_transfer_expansion": {
            "velocity_over_force_dc_mobility": 1.0 / (1.0 + CHI),
            "linear_laplace_coefficient": CHI / (1.0 + CHI) ** 2,
            "matched_free_inertial_damping": 1.0 + CHI,
            "matched_free_inertial_mass": -CHI,
            "gate_role": "none; analytic interpretation only",
        },
        "claim_limits": {
            "force_units": "dimensionless generalized force; no SI map",
            "mass_scope": "finite inertial reading of this canonical port only",
            "extended_states": "not ruled out",
            "port_dependence": "force placement is part of the tested architecture",
        },
        "first_prospective_execution_revision": (
            FIRST_PROSPECTIVE_EXECUTION_REVISION
        ),
    }


def _fmt(value: float | None) -> str:
    if value is None:
        return "unavailable"
    return continuum_gate._fmt(value)


def _write_figure(payload: dict[str, Any], path: Path) -> None:
    cases = payload["cases"]
    rows = [cases[_case_key(alpha)] for alpha in ALPHA_VALUES]
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.2))

    for alpha, row in zip(ALPHA_VALUES, rows, strict=True):
        shifted = np.maximum(np.asarray(row["sample_times"]) - alpha, 0.0)
        axes[0, 0].plot(
            shifted[1:], row["median_position_response"][1:], label=f"alpha={alpha:g}"
        )
    holdout = rows[-1]
    holdout_shifted = np.maximum(
        np.asarray(holdout["sample_times"]) - HOLDOUT_ALPHA, 0.0
    )
    axes[0, 0].plot(
        holdout_shifted[1:],
        holdout["continuum_position_response"][1:],
        "k--",
        linewidth=2.0,
        label="overdamped continuum",
    )
    axes[0, 0].set_title("Force-impulse position response")
    axes[0, 0].set_xlabel("time after pulse")
    axes[0, 0].set_ylabel("position / impulse")
    axes[0, 0].legend(fontsize=8)

    for alpha, row in zip(ALPHA_VALUES, rows, strict=True):
        shifted = np.maximum(np.asarray(row["sample_times"]) - alpha, 0.0)
        axes[0, 1].plot(
            shifted[1:], row["median_relative_response"][1:], label=f"alpha={alpha:g}"
        )
    axes[0, 1].plot(
        holdout_shifted[1:],
        holdout["continuum_relative_response"][1:],
        "k--",
        linewidth=2.0,
        label="exp(-5t)",
    )
    axes[0, 1].set_title("Relative response")
    axes[0, 1].set_xlabel("time after pulse")
    axes[0, 1].set_ylabel("relative coordinate / impulse")
    axes[0, 1].legend(fontsize=8)

    axes[1, 0].semilogx(
        ALPHA_VALUES,
        [row["median_pulse_end_feedthrough"] for row in rows],
        "o-",
        label="direct feedthrough",
    )
    axes[1, 0].semilogx(
        ALPHA_VALUES,
        [row["median_work_coefficient"] for row in rows],
        "s-",
        label="alpha W / J^2",
    )
    axes[1, 0].semilogx(
        ALPHA_VALUES,
        [
            -row["median_first_postpulse_velocity_per_impulse"] / CHI
            for row in rows
        ],
        "^-",
        label="-post-pulse velocity / chi",
    )
    axes[1, 0].axhline(1.0, color="black", linestyle=":")
    axes[1, 0].invert_xaxis()
    axes[1, 0].set_xticks(ALPHA_VALUES)
    axes[1, 0].set_xticklabels(
        [f"{alpha:g}" for alpha in ALPHA_VALUES], rotation=25, ha="right"
    )
    axes[1, 0].tick_params(axis="x", which="minor", labelbottom=False)
    axes[1, 0].set_title("High-frequency overdamped signatures")
    axes[1, 0].set_xlabel("alpha (decreasing to the right)")
    axes[1, 0].set_ylabel("normalized coefficient")
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
        times, anchor * times / times[0], ":", color="black", label="slope 1"
    )
    axes[1, 1].loglog(
        times,
        anchor * np.square(times / times[0]),
        "-.",
        color="gray",
        label="slope 2",
    )
    axes[1, 1].set_title(f"Visible MSD: slope={msd['simulated_slope']:.3f}")
    msd_ticks = (0.005, 0.01, 0.02, 0.04)
    axes[1, 1].set_xticks(msd_ticks)
    axes[1, 1].set_xticklabels([f"{value:g}" for value in msd_ticks])
    axes[1, 1].tick_params(axis="x", which="minor", labelbottom=False)
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
    cases = payload["cases"]
    radius_minima = [
        row["minimum_simultaneous_forced_control_radius_ratio"]
        for row in cases.values()
        if row["minimum_simultaneous_forced_control_radius_ratio"] is not None
    ]
    radius_maxima = [
        row["maximum_simultaneous_forced_control_radius_ratio"]
        for row in cases.values()
        if row["maximum_simultaneous_forced_control_radius_ratio"] is not None
    ]
    radius_range = "unavailable"
    if len(radius_minima) == len(cases) == len(radius_maxima):
        radius_range = f"{_fmt(min(radius_minima))}..{_fmt(max(radius_maxima))}"
    lines = [
        "# Scalar-memory force/work-port gate",
        "",
        "Date: 2026-08-16.",
        "",
        "## Verdict",
        "",
        f"Decision: **`{payload['decision']}`**.",
        "",
        "| gate | status |",
        "|---|:---:|",
        f"| port and experimental validity | {gates['port_and_experimental_validity']['status']} |",
        f"| force-response and ledger closure | {gates['force_response_and_ledger_closure']['status']} |",
        f"| overdamped-memory signature | {gates['overdamped_memory_signature']['status']} |",
        f"| regular finite-inertial signature | {gates['finite_inertial_signature']['status']} |",
        "",
        "The generalized force normalization is fixed by `x_next += alpha*f`;",
        "the supplied work is `sum f dot (x_next-x)`. No fitted response",
        "coefficient or mass rescales the input.",
        "",
        "## Registered alpha family",
        "",
        "| alpha | H | exact position error | exact relative error | continuum position error | continuum relative error | feedthrough | post-pulse velocity/J | alpha W/J^2 | ledger residual/work |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for alpha in ALPHA_VALUES:
        row = cases[_case_key(alpha)]
        lines.append(
            "| "
            f"{alpha:.6f} | {row['case']['horizon']} | "
            f"{_fmt(row['median_position_error_exact'])} | "
            f"{_fmt(row['median_relative_error_exact'])} | "
            f"{_fmt(row['median_position_error_continuum'])} | "
            f"{_fmt(row['median_relative_error_continuum'])} | "
            f"{_fmt(row['median_pulse_end_feedthrough'])} | "
            f"{_fmt(row['median_first_postpulse_velocity_per_impulse'])} | "
            f"{_fmt(row['median_work_coefficient'])} | "
            f"{_fmt(row['native_ledger_relative_residual'])} |"
        )

    holdout = cases[_case_key(HOLDOUT_ALPHA)]
    msd = payload["msd"]
    lines.extend(
        [
            "",
            "## Validity and discrimination diagnostics",
            "",
            f"- Maximum force-off clone residual: `{_fmt(max(row['maximum_force_off_residual'] for row in cases.values()))}`.",
            f"- Maximum analytic forced-recurrence residual: `{_fmt(max(row['maximum_analytic_recurrence_residual'] for row in cases.values()))}`.",
            f"- Maximum work-normalization error: `{_fmt(max(row['maximum_work_coefficient_error'] for row in cases.values()))}`.",
            f"- Maximum local radius `R/sigma_rep`: `{_fmt(max(row['maximum_memory_radius'] / SIGMA_REP for row in cases.values()))}`.",
            f"- Simultaneous forced/control radius range: `{radius_range}`.",
            f"- Holdout direct feedthrough: `{_fmt(holdout['median_pulse_end_feedthrough'])}`.",
            f"- Holdout first post-pulse velocity per impulse: `{_fmt(holdout['median_first_postpulse_velocity_per_impulse'])}`.",
            f"- Visible-MSD slope on the fixed window: `{msd['simulated_slope']:.6f}` (exact discrete `{msd['exact_discrete_slope']:.6f}`, continuum `{msd['continuum_slope']:.6f}`).",
            f"- Monte Carlo MSD error to exact discrete reference: `{_fmt(msd['normalized_rms_error_exact_discrete'])}`.",
            "",
            "## Figure",
            "",
            f"![Force/work-port gate]({continuum_gate._relative(path, figure)})",
            "",
            "## Interpretation boundary",
            "",
            "Evidence: the native nonlinear force response closes against its",
            "exact finite-H reference, the work ledger approaches its continuum",
            "balance, and the fixed high-frequency diagnostics select one of the",
            "two registered port signatures.",
            "",
            "Inference if the overdamped signature is selected: this canonical",
            "additive-force port exposes finite mobility rather than a regular",
            "finite inertial mass. Its impulse displacement is direct and its",
            "short-time visible MSD is diffusive.",
            "",
            "Not established: an SI force or energy scale, a no-go for every",
            "coarse graining, or the absence of an explicitly added or separately",
            "derived momentum field. Force placement is part of the tested model.",
            "",
            "Post-hoc analytic check (not a gate): expanding the measured",
            "overdamped transfer gives `(s+1)/(s+5)=1/5+(4/25)s+...`.",
            "Matching a free inertial mobility `1/(gamma+m s)` at low frequency",
            "would require `gamma=5` and `m=-4`, not a positive passive mass.",
            "",
            "## Provenance",
            "",
            f"- Protocol: [{PREREGISTRATION.name}]({continuum_gate._relative(path, continuum_gate._resolve(PREREGISTRATION))}).",
            f"- Preceding continuum review: [{CONTINUUM_REVIEW.name}]({continuum_gate._relative(path, continuum_gate._resolve(CONTINUUM_REVIEW))}).",
            f"- Simulation revision: `{payload['simulation_revision']}`.",
            f"- First prospective seed-11--15 execution revision: `{FIRST_PROSPECTIVE_EXECUTION_REVISION}`.",
            f"- Git status at execution: `{payload['git_status'] or 'clean'}`.",
            f"- Formation seeds: `{','.join(str(seed) for seed in FORMATION_SEEDS)}`; Brownian-coarsened common noise.",
            f"- Formation: `{FORMATION_TIME:g}` memory times; response: `{RESPONSE_TIME:g}` memory times at native cadence.",
            f"- Runtime: `{payload['runtime']['simulation_and_aggregation_seconds']:.3f} s` for `{payload['runtime']['dynamic_path_updates']}` dynamic path updates (`{payload['runtime']['dynamic_path_updates_per_second']:.1f}/s`).",
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
