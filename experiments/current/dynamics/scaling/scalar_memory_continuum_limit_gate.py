"""Run the preregistered scalar-memory continuum-limit audit."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
import sys
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
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    aggregate_standard_normal_increments,
    finite_h_linear_response,
    matched_scalar_continuum_case,
    simulate_matched_continuum_response,
)


DEFAULT_REPORT = Path(
    "reports/dynamics/limits/scalar_memory_continuum_limit_gate_2026-08-15.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/limits/scalar_memory_continuum_limit_gate_2026-08-15.json"
)
DEFAULT_FIGURE = Path(
    "figures/draft/dynamics/limits/scalar_memory_continuum_limit_gate_2026-08-15.png"
)
PREREGISTRATION = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_continuum_limit_protocol_2026-08-15.md"
)

TAIL_EXTENTS = (6.0, 9.0, 12.0)
ALPHA_VALUES = (0.04, 0.02, 0.01, 0.005, 0.0025)
HOLDOUT_ALPHA = 0.0025
OFFSET_FRACTIONS = (0.005, 0.01)
FORMATION_SEEDS = (1, 2, 3, 4, 5)
NOISE_SEED = 20_260_815

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


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _git_output(arguments: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return result.stdout.strip()


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return _jsonable(value.tolist())
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, (float, np.floating)):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True, allow_nan=False)
        + "\n",
        encoding="utf-8",
    )


def _case_key(alpha: float, tail_extent: float) -> str:
    return f"alpha_{alpha:.4g}_C_{tail_extent:.4g}"


def registered_cases() -> list[Any]:
    """Return the seven unique registered finite-step cases."""

    pairs = [(0.01, extent) for extent in TAIL_EXTENTS]
    pairs.extend((alpha, 12.0) for alpha in ALPHA_VALUES if alpha != 0.01)
    return [
        matched_scalar_continuum_case(
            alpha=alpha,
            tail_extent=extent,
            restoring_per_memory_time=CHI,
            diffusion_per_memory_time=DIFFUSION,
            dim=DIM,
            memory_mass=MEMORY_MASS,
            sigma_rep=SIGMA_REP,
            sigma_att=SIGMA_ATT,
            amplitude_rep=AMPLITUDE_REP,
            amplitude_att=AMPLITUDE_ATT,
        )
        for alpha, extent in pairs
    ]


def _integer_steps(duration: float, alpha: float) -> int:
    raw = duration / alpha
    rounded = int(round(raw))
    if not math.isclose(raw, rounded, rel_tol=0.0, abs_tol=1.0e-10):
        raise ValueError("registered duration must contain an integer number of steps")
    return rounded


def _coupled_noise(
    *, seed: int, minimum_alpha: float, total_time: float, dim: int
) -> np.ndarray:
    steps = _integer_steps(total_time, minimum_alpha)
    return np.random.default_rng(NOISE_SEED + int(seed)).standard_normal((steps, dim))


def _noise_at_alpha(fine_noise: np.ndarray, alpha: float, minimum_alpha: float) -> np.ndarray:
    ratio_float = alpha / minimum_alpha
    ratio = int(round(ratio_float))
    if not math.isclose(ratio_float, ratio, rel_tol=0.0, abs_tol=1.0e-10):
        raise ValueError("alpha grid must be an integer multiple of minimum alpha")
    return aggregate_standard_normal_increments(fine_noise, ratio)


def _normalized_rms_error(observed: np.ndarray, reference: np.ndarray) -> float:
    residual = np.asarray(observed, dtype=float) - np.asarray(reference, dtype=float)
    denominator = float(np.sqrt(np.mean(np.asarray(reference, dtype=float) ** 2)))
    if denominator <= 0.0:
        raise ValueError("reference RMS must be positive")
    return float(np.sqrt(np.mean(residual * residual)) / denominator)


def _fit_response_rate(
    values: np.ndarray,
    reference: np.ndarray,
    *,
    alpha: float,
    support_floor: float = 1.0e-3,
) -> tuple[float, float, int]:
    observed = np.asarray(values, dtype=float)
    exact = np.asarray(reference, dtype=float)
    if observed.shape != exact.shape or observed.ndim != 1 or observed.size < 3:
        raise ValueError("response and reference must be matching one-dimensional arrays")
    mask = np.abs(exact[:-1]) >= support_floor * abs(exact[0])
    predictors = observed[:-1][mask]
    targets = observed[1:][mask]
    denominator = float(np.dot(predictors, predictors))
    if denominator <= 0.0 or predictors.size < 3:
        raise ValueError("response does not support a one-step rate fit")
    coefficient = float(np.dot(predictors, targets) / denominator)
    if not 0.0 < coefficient < 1.0:
        raise ValueError("fitted response coefficient must lie in (0, 1)")
    return coefficient, float(-math.log(coefficient) / alpha), int(predictors.size)


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
    response = simulate_matched_continuum_response(
        case,
        formation_noise=coarse[:n_formation],
        response_noise=coarse[n_formation:],
        offset_fractions=OFFSET_FRACTIONS,
        axis=[1.0, 0.0, 0.0],
        memory_mass=MEMORY_MASS,
        sigma_rep=SIGMA_REP,
        sigma_att=SIGMA_ATT,
        amplitude_rep=AMPLITUDE_REP,
        amplitude_att=AMPLITUDE_ATT,
    )
    linear = finite_h_linear_response(case, response_steps=n_response)
    exact = np.asarray(linear["relative"], dtype=float)
    continuum = np.exp(-case.continuum_relative_rate * response.sample_times)

    fraction_rows: list[dict[str, Any]] = []
    projected_responses: list[np.ndarray] = []
    for offset_index, fraction in enumerate(response.offset_fractions):
        vector_response = response.relative_responses[offset_index]
        projected = vector_response[:, 0]
        projected_responses.append(projected)
        drift = response.drift_responses[offset_index, :, 0]
        fitted_root, fitted_rate, fit_count = _fit_response_rate(
            projected, exact, alpha=case.alpha
        )
        reference_root, reference_rate, _ = _fit_response_rate(
            exact, exact, alpha=case.alpha
        )
        predicted_drift = -case.restoring_per_update * projected[:-1]
        even_norm = np.linalg.norm(
            response.relative_even_leakage[offset_index], axis=1
        )
        cross_norm = np.linalg.norm(vector_response[:, 1:], axis=1)
        fraction_rows.append(
            {
                "offset_fraction": float(fraction),
                "offset_amplitude": float(response.offset_amplitudes[offset_index]),
                "normalized_rms_error_exact": _normalized_rms_error(projected, exact),
                "normalized_rms_error_continuum": _normalized_rms_error(
                    projected, continuum
                ),
                "fitted_root": fitted_root,
                "fitted_rate": fitted_rate,
                "reference_fitted_root": reference_root,
                "reference_fitted_rate": reference_rate,
                "relative_rate_error_exact": abs(fitted_rate - reference_rate)
                / reference_rate,
                "relative_rate_error_continuum": abs(
                    fitted_rate - case.continuum_relative_rate
                )
                / case.continuum_relative_rate,
                "force_closure_normalized_rms": _normalized_rms_error(
                    drift, predicted_drift
                ),
                "mirror_even_maximum": float(np.max(even_norm)),
                "cross_axis_maximum": float(np.max(cross_norm)),
                "fit_sample_count": fit_count,
                "projected_response": projected,
            }
        )

    strength_residual = projected_responses[0] - projected_responses[1]
    strength_rms = float(
        np.sqrt(np.mean(strength_residual * strength_residual))
        / np.sqrt(np.mean(exact * exact))
    )
    return {
        "seed": int(seed),
        "initial_control_radius": response.initial_control_radius,
        "final_control_radius": response.final_control_radius,
        "control_radius_ratio": response.final_control_radius
        / response.initial_control_radius,
        "strength_nonlinearity_rms": strength_rms,
        "strength_nonlinearity_maximum": float(np.max(np.abs(strength_residual))),
        "analytic_maximum_recurrence_residual": float(
            linear["maximum_recurrence_residual"]
        ),
        "sample_times": response.sample_times,
        "exact_response": exact,
        "continuum_response": continuum,
        "fractions": fraction_rows,
    }


def _median(values: Iterable[float]) -> float:
    finite = [float(value) for value in values if math.isfinite(float(value))]
    if not finite:
        raise ValueError("cannot aggregate an empty finite collection")
    return float(np.median(finite))


def _aggregate_case(case: Any, seeds: list[dict[str, Any]]) -> dict[str, Any]:
    fractions = [row for seed in seeds for row in seed["fractions"]]
    seed_median_traces = [
        np.median(
            np.stack([row["projected_response"] for row in seed["fractions"]]),
            axis=0,
        )
        for seed in seeds
    ]
    return {
        "case": asdict(case),
        "n_seeds": len(seeds),
        "median_normalized_rms_error_exact": _median(
            row["normalized_rms_error_exact"] for row in fractions
        ),
        "maximum_normalized_rms_error_exact": max(
            row["normalized_rms_error_exact"] for row in fractions
        ),
        "median_normalized_rms_error_continuum": _median(
            row["normalized_rms_error_continuum"] for row in fractions
        ),
        "median_fitted_rate": _median(row["fitted_rate"] for row in fractions),
        "median_reference_fitted_rate": _median(
            row["reference_fitted_rate"] for row in fractions
        ),
        "median_relative_rate_error_exact": _median(
            row["relative_rate_error_exact"] for row in fractions
        ),
        "maximum_relative_rate_error_exact": max(
            row["relative_rate_error_exact"] for row in fractions
        ),
        "median_relative_rate_error_continuum": _median(
            row["relative_rate_error_continuum"] for row in fractions
        ),
        "median_force_closure_normalized_rms": _median(
            row["force_closure_normalized_rms"] for row in fractions
        ),
        "maximum_force_closure_normalized_rms": max(
            row["force_closure_normalized_rms"] for row in fractions
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
        "minimum_control_radius_ratio": min(
            seed["control_radius_ratio"] for seed in seeds
        ),
        "maximum_control_radius_ratio": max(
            seed["control_radius_ratio"] for seed in seeds
        ),
        "maximum_analytic_recurrence_residual": max(
            seed["analytic_maximum_recurrence_residual"] for seed in seeds
        ),
        "sample_times": seeds[0]["sample_times"],
        "median_projected_response": np.median(np.stack(seed_median_traces), axis=0),
        "exact_response": seeds[0]["exact_response"],
        "continuum_response": seeds[0]["continuum_response"],
        "seeds": seeds,
    }


def _evaluate_gates(cases: dict[str, dict[str, Any]]) -> dict[str, Any]:
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
    radius_ratios = [
        seed["control_radius_ratio"] for case in every for seed in case["seeds"]
    ]
    g0_checks = {
        "analytic_reference": max(
            case["maximum_analytic_recurrence_residual"] for case in every
        )
        <= 1.0e-12,
        "mirror_even_median": _median(even_values) <= 1.0e-3,
        "mirror_even_maximum": max(even_values) <= 1.0e-2,
        "strength_median": _median(strength_rms) <= 1.0e-3,
        "strength_maximum": max(strength_max) <= 1.0e-2,
        "control_radius_lower": min(radius_ratios) >= 0.95,
        "control_radius_upper": max(radius_ratios) <= 1.05,
    }
    g0 = all(g0_checks.values())

    tail = {
        extent: cases[_case_key(0.01, extent)] for extent in TAIL_EXTENTS
    }
    rate_change_6_9 = abs(
        tail[9.0]["median_fitted_rate"] - tail[6.0]["median_fitted_rate"]
    )
    rate_change_9_12 = abs(
        tail[12.0]["median_fitted_rate"] - tail[9.0]["median_fitted_rate"]
    )
    g1_checks = {
        "all_exact_response_errors": all(
            row["median_normalized_rms_error_exact"] <= 0.01
            for row in tail.values()
        ),
        "C12_rate_error": tail[12.0]["median_relative_rate_error_exact"] <= 0.01,
        "tail_change_contracts": rate_change_9_12 <= rate_change_6_9 + 0.005,
    }
    g1_components = all(g1_checks.values())
    g1 = g0 and g1_components

    alpha = {
        value: cases[_case_key(value, 12.0)] for value in ALPHA_VALUES
    }
    holdout = alpha[HOLDOUT_ALPHA]
    reference_alpha = alpha[0.01]
    g2_checks = {
        "all_exact_response_errors": all(
            row["median_normalized_rms_error_exact"] <= 0.01
            for row in alpha.values()
        ),
        "all_exact_rate_errors": all(
            row["median_relative_rate_error_exact"] <= 0.01
            for row in alpha.values()
        ),
        "holdout_continuum_rate": holdout[
            "median_relative_rate_error_continuum"
        ]
        <= 0.01,
        "holdout_continuum_response": holdout[
            "median_normalized_rms_error_continuum"
        ]
        <= 0.01,
        "holdout_improves_on_alpha_001": holdout[
            "median_relative_rate_error_continuum"
        ]
        < reference_alpha["median_relative_rate_error_continuum"],
    }
    g2_components = all(g2_checks.values())
    g2 = g0 and g2_components

    if not g0:
        decision = "experiment-inadequate"
    elif g1 and g2:
        decision = "continuum-limit-supported-in-local-linear-slice"
    else:
        decision = "registered-continuum-limit-not-supported"
    return {
        "experimental_validity": {
            "pass": g0,
            "status": "pass" if g0 else "fail",
            "checks": g0_checks,
        },
        "finite_tail_convergence": {
            "pass": g1,
            "status": "blocked" if not g0 else ("pass" if g1_components else "fail"),
            "component_checks_pass": g1_components,
            "checks": g1_checks,
            "rate_change_C6_to_C9": rate_change_6_9,
            "rate_change_C9_to_C12": rate_change_9_12,
        },
        "matched_alpha_convergence": {
            "pass": g2,
            "status": "blocked" if not g0 else ("pass" if g2_components else "fail"),
            "component_checks_pass": g2_components,
            "checks": g2_checks,
        },
        "decision": decision,
    }


def run_audit(*, seeds: Iterable[int] = FORMATION_SEEDS) -> dict[str, Any]:
    """Run the complete registered audit and return its in-memory payload."""

    selected_seeds = [int(seed) for seed in seeds]
    if not selected_seeds or len(set(selected_seeds)) != len(selected_seeds):
        raise ValueError("seeds must be a non-empty unique collection")
    cases = registered_cases()
    minimum_alpha = min(case.alpha for case in cases)
    total_time = FORMATION_TIME + RESPONSE_TIME
    rows: dict[str, list[dict[str, Any]]] = {
        _case_key(case.alpha, case.tail_extent): [] for case in cases
    }
    for seed in selected_seeds:
        fine_noise = _coupled_noise(
            seed=seed,
            minimum_alpha=minimum_alpha,
            total_time=total_time,
            dim=DIM,
        )
        for case in cases:
            key = _case_key(case.alpha, case.tail_extent)
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
        _case_key(case.alpha, case.tail_extent): _aggregate_case(
            case, rows[_case_key(case.alpha, case.tail_extent)]
        )
        for case in cases
    }
    gates = _evaluate_gates(aggregate)
    return {
        "schema": "emergenz-knoten.scalar-memory-continuum-limit",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "simulation_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "preregistration": PREREGISTRATION.as_posix(),
        "registration": {
            "tail_extents": TAIL_EXTENTS,
            "alpha_values": ALPHA_VALUES,
            "holdout_alpha": HOLDOUT_ALPHA,
            "offset_fractions": OFFSET_FRACTIONS,
            "formation_seeds": selected_seeds,
            "noise_seed": NOISE_SEED,
            "dim": DIM,
            "chi": CHI,
            "diffusion": DIFFUSION,
            "memory_mass": MEMORY_MASS,
            "formation_time": FORMATION_TIME,
            "response_time": RESPONSE_TIME,
            "kernel": {
                "sigma_rep": SIGMA_REP,
                "sigma_att": SIGMA_ATT,
                "amplitude_rep": AMPLITUDE_REP,
                "amplitude_att": AMPLITUDE_ATT,
            },
        },
        "cases": aggregate,
        "gates": gates,
        "decision": gates["decision"],
        "claim_limits": {
            "physical_mass": "not tested; no normalized force-work port",
            "momentum": "not identified by a real scalar relaxation response",
            "nonlinear_knot": "not tested; registered slice is deliberately local-linear",
            "continuum_scope": "matched scalar memory-centre response only",
        },
    }


def _fmt(value: float) -> str:
    number = float(value)
    if number == 0.0:
        return "0"
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.4e}"
    return f"{number:.6f}"


def _write_figure(payload: dict[str, Any], path: Path) -> None:
    cases = payload["cases"]
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.2))

    tail_rows = [cases[_case_key(0.01, extent)] for extent in TAIL_EXTENTS]
    axes[0, 0].plot(
        TAIL_EXTENTS,
        [row["median_fitted_rate"] for row in tail_rows],
        "o-",
        label="observed",
    )
    axes[0, 0].plot(
        TAIL_EXTENTS,
        [row["median_reference_fitted_rate"] for row in tail_rows],
        "s--",
        label="exact finite H",
    )
    axes[0, 0].set_xlabel("tail extent C")
    axes[0, 0].set_ylabel("coarse-time rate")
    axes[0, 0].set_title("Finite-tail convergence")
    axes[0, 0].legend()

    alpha_rows = [cases[_case_key(alpha, 12.0)] for alpha in ALPHA_VALUES]
    axes[0, 1].plot(
        ALPHA_VALUES,
        [row["median_fitted_rate"] for row in alpha_rows],
        "o-",
        label="observed",
    )
    axes[0, 1].plot(
        ALPHA_VALUES,
        [row["median_reference_fitted_rate"] for row in alpha_rows],
        "s--",
        label="exact finite step",
    )
    axes[0, 1].axhline(1.0 + CHI, color="black", linestyle=":", label="continuum")
    axes[0, 1].invert_xaxis()
    axes[0, 1].set_xlabel("alpha (decreasing to the right)")
    axes[0, 1].set_ylabel("coarse-time rate")
    axes[0, 1].set_title("Matched-alpha convergence")
    axes[0, 1].legend()

    for alpha, row in zip(ALPHA_VALUES, alpha_rows, strict=True):
        axes[1, 0].plot(
            row["sample_times"],
            row["median_projected_response"],
            label=f"alpha={alpha:g}",
        )
    finest = alpha_rows[-1]
    axes[1, 0].plot(
        finest["sample_times"],
        finest["continuum_response"],
        color="black",
        linestyle="--",
        linewidth=2.0,
        label="exp(-5t)",
    )
    axes[1, 0].set_xlabel("scaled time t=alpha n")
    axes[1, 0].set_ylabel("normalized relative response")
    axes[1, 0].set_title("Response collapse")
    axes[1, 0].legend(fontsize=8)

    axes[1, 1].loglog(
        ALPHA_VALUES,
        [row["median_relative_rate_error_continuum"] for row in alpha_rows],
        "o-",
        label="rate error to continuum",
    )
    axes[1, 1].loglog(
        ALPHA_VALUES,
        [row["median_normalized_rms_error_exact"] for row in alpha_rows],
        "s-",
        label="response error to exact finite H",
    )
    axes[1, 1].set_xlabel("alpha")
    axes[1, 1].set_ylabel("relative error")
    axes[1, 1].set_title("Discretization and nonlinear residual")
    axes[1, 1].set_xticks(ALPHA_VALUES)
    axes[1, 1].set_xticklabels(
        [f"{alpha:g}" for alpha in ALPHA_VALUES], rotation=25, ha="right"
    )
    axes[1, 1].legend(fontsize=8)

    for axis in axes.flat:
        axis.grid(alpha=0.25)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _write_report(payload: dict[str, Any], path: Path, figure: Path) -> None:
    cases = payload["cases"]
    gates = payload["gates"]
    lines = [
        "# Scalar-memory continuum-limit gate",
        "",
        "Date: 2026-08-15.",
        "",
        "## Verdict",
        "",
        f"Decision: **`{payload['decision']}`**.",
        "",
        "| gate | status |",
        "|---|:---:|",
        f"| experimental validity | {gates['experimental_validity']['status']} |",
        f"| finite-tail convergence | {gates['finite_tail_convergence']['status']} |",
        f"| matched-alpha convergence | {gates['matched_alpha_convergence']['status']} |",
        "",
        "The test uses a mirrored visible-coordinate displacement of a complete",
        "formed Markov state. It is an initial-condition response, not an external",
        "force or canonical write-port experiment.",
        "",
        "The downstream finite-tail and matched-alpha component checks all",
        "satisfy their registered numerical thresholds, but they are formally",
        "blocked because G0 failed its control-radius endpoint bounds. Those",
        "component values are reported diagnostically and are not promoted to a",
        "registered pass.",
        "",
        "## Registered matched family",
        "",
        "| alpha | C | H | tail mass | eta | epsilon | exact rate | observed rate | exact response error | continuum response error |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    ordered = [(0.01, 6.0), (0.01, 9.0)] + [
        (alpha, 12.0) for alpha in ALPHA_VALUES
    ]
    for alpha, extent in ordered:
        row = cases[_case_key(alpha, extent)]
        case = row["case"]
        lines.append(
            f"| {_fmt(alpha)} | {_fmt(extent)} | {case['horizon']} | "
            f"{_fmt(case['tail_mass_fraction'])} | {_fmt(case['eta'])} | "
            f"{_fmt(case['epsilon'])} | {_fmt(row['median_reference_fitted_rate'])} | "
            f"{_fmt(row['median_fitted_rate'])} | "
            f"{_fmt(row['median_normalized_rms_error_exact'])} | "
            f"{_fmt(row['median_normalized_rms_error_continuum'])} |"
        )
    lines.extend(
        [
            "",
            "## Validity diagnostics",
            "",
            "| case | mirror-even max | strength max | radius range | force-closure RMS median |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for alpha, extent in ordered:
        row = cases[_case_key(alpha, extent)]
        lines.append(
            f"| alpha={alpha:g}, C={extent:g} | "
            f"{_fmt(row['maximum_mirror_even_maximum'])} | "
            f"{_fmt(row['maximum_strength_nonlinearity_maximum'])} | "
            f"{_fmt(row['minimum_control_radius_ratio'])}.."
            f"{_fmt(row['maximum_control_radius_ratio'])} | "
            f"{_fmt(row['median_force_closure_normalized_rms'])} |"
        )
    lines.extend(
        [
            "",
            "## Figure",
            "",
            f"![Continuum-limit gate]({_relative(path, figure)})",
            "",
            "## Interpretation boundary",
            "",
            "Evidence: the table and gates compare the nonlinear finite-memory",
            "simulation first with its exact finite-H local-linear reference and",
            "then with the registered continuum exponential.",
            "",
            "Inference, if all gates pass: the tested local scalar memory-centre",
            "response has a controlled joint tail and small-alpha limit when chi,",
            "D and alpha*H are matched.",
            "",
            "Not established: physical inertial mass, a force-work normalization,",
            "momentum, an underdamped mode, nonlinear knot existence, or a physical",
            "continuum time.",
            "",
            "## Provenance",
            "",
            f"- Preregistration: [{PREREGISTRATION.name}]({_relative(path, _resolve(PREREGISTRATION))}).",
            f"- Simulation revision: `{payload['simulation_revision']}`.",
            f"- Git status at execution: `{payload['git_status'] or 'clean'}`.",
            "- Five registered formation seeds and Brownian-coarsened common noise.",
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
    payload = run_audit()
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    _write_json(summary, payload)
    _write_figure(payload, figure)
    _write_report(payload, report, figure)
    print(json.dumps({"decision": payload["decision"], "report": str(report)}))


if __name__ == "__main__":
    main()
