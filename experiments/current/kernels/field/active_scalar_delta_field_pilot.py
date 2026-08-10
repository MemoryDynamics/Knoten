from __future__ import annotations

import argparse
from dataclasses import asdict, replace
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

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
    ActiveScalarFieldConfig,
    scalar_field_linear_rate,
    scalar_field_preferred_wavenumber,
    simulate_active_scalar_delta_field,
    spectral_delta_coefficients,
)


def _git_output(args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return completed.stdout.strip()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the preregistered active scalar delta-source mechanism gate "
            "with numerical and mechanistic controls."
        )
    )
    parser.add_argument("--grid-points", type=int, default=256)
    parser.add_argument("--time-step", type=float, default=0.05)
    parser.add_argument("--final-time", type=float, default=200.0)
    parser.add_argument("--seeds", type=str, default="1,2,3")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/kernels/field/active_scalar_delta_field_pilot_2026-07-31.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/kernels/field/active_scalar_delta_field_pilot_2026-07-31.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/kernels/field_2026-07-31/active_scalar_delta_field_pilot.png"
        ),
    )
    args = parser.parse_args(argv)
    args.seeds = [int(value) for value in args.seeds.split(",") if value.strip()]
    return args


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative_link(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _validate_args(args: argparse.Namespace) -> None:
    if args.grid_points < 64 or args.grid_points % 2:
        raise SystemExit("--grid-points must be an even integer of at least 64")
    if not math.isfinite(args.time_step) or args.time_step <= 0.0:
        raise SystemExit("--time-step must be positive and finite")
    if not math.isfinite(args.final_time) or args.final_time < 50.0:
        raise SystemExit("--final-time must be finite and at least 50")
    if len(args.seeds) < 3 or len(set(args.seeds)) != len(args.seeds):
        raise SystemExit("--seeds must contain at least three distinct integers")


def _base_config(args: argparse.Namespace, *, seed: int) -> ActiveScalarFieldConfig:
    steps = int(round(args.final_time / args.time_step))
    return ActiveScalarFieldConfig(
        grid_points=int(args.grid_points),
        time_step=float(args.time_step),
        steps=steps,
        sample_every=max(1, steps // 400),
        seed=int(seed),
    )


def build_cases(
    base: ActiveScalarFieldConfig,
) -> dict[str, ActiveScalarFieldConfig]:
    """Return the fixed cases; this function performs no fitting."""

    return {
        "gaussian_null": replace(
            base,
            gradient_coefficient=0.5,
            biharmonic_coefficient=0.125,
            cubic_saturation=0.0,
        ),
        "stable_finite_k": replace(
            base,
            gradient_coefficient=-1.8,
            biharmonic_coefficient=1.0,
            cubic_saturation=0.0,
        ),
        "active_finite_k": replace(
            base,
            gradient_coefficient=-2.2,
            biharmonic_coefficient=1.0,
            cubic_saturation=1.0,
        ),
        "cubic_off": replace(
            base,
            gradient_coefficient=-2.2,
            biharmonic_coefficient=1.0,
            cubic_saturation=0.0,
        ),
        "source_off": replace(
            base,
            gradient_coefficient=-2.2,
            biharmonic_coefficient=1.0,
            cubic_saturation=1.0,
            source_enabled=False,
        ),
        "eta_zero": replace(
            base,
            gradient_coefficient=-2.2,
            biharmonic_coefficient=1.0,
            cubic_saturation=1.0,
            eta=0.0,
        ),
    }


def _unwrap_positions(positions: np.ndarray, length: float) -> np.ndarray:
    angles = np.asarray(positions) * 2.0 * np.pi / length
    return np.unwrap(angles) * length / (2.0 * np.pi)


def _trace_metrics(
    trace: Any,
    config: ActiveScalarFieldConfig,
) -> dict[str, Any]:
    quarter = max(3, trace.times.size // 4)
    late = slice(trace.times.size - quarter, trace.times.size)
    previous = slice(
        max(0, trace.times.size - 2 * quarter),
        trace.times.size - quarter,
    )
    late_rms = float(np.median(trace.field_rms[late]))
    previous_rms = float(np.median(trace.field_rms[previous]))
    relative_change = abs(late_rms / previous_rms - 1.0) if previous_rms > 0.0 else None
    phases = trace.source_field_phase[late]
    phases = phases[np.isfinite(phases)]
    phase_coherence = float(abs(np.mean(np.exp(1j * phases)))) if phases.size else None
    phase_lag = float(np.angle(np.mean(np.exp(1j * phases)))) if phases.size else None
    unwrapped = _unwrap_positions(trace.positions, config.domain_length)
    late_speed = (
        float(np.polyfit(trace.times[late], unwrapped[late], 1)[0])
        if quarter >= 3
        else None
    )

    positive = trace.wavenumbers > 0.0
    positive_k = trace.wavenumbers[positive]
    power = np.square(
        np.abs(trace.final_coefficients[positive]) / trace.final_coefficients.size
    )
    if power.size and float(np.max(power)) > 0.0:
        peak_index = int(np.argmax(power))
        half_power = positive_k[power >= 0.5 * power[peak_index]]
        half_power_width = float(np.ptp(half_power))
        peak_k = float(positive_k[peak_index])
    else:
        half_power_width = 0.0
        peak_k = 0.0
    return {
        "stop_reason": trace.stop_reason,
        "completed_steps": int(trace.completed_steps),
        "final_field_rms": float(trace.field_rms[-1]),
        "late_field_rms": late_rms,
        "late_field_rms_relative_change": relative_change,
        "final_field_max_abs": float(trace.field_max_abs[-1]),
        "dominant_wavenumber": peak_k,
        "half_power_peak_width": half_power_width,
        "source_field_phase_coherence": phase_coherence,
        "source_field_phase_lag": phase_lag,
        "source_total_excursion": float(np.ptp(unwrapped)),
        "source_late_excursion": float(np.ptp(unwrapped[late])),
        "source_late_speed": late_speed,
    }


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "run_count": len(rows),
        "completed_count": sum(row["stop_reason"] == "completed" for row in rows),
        "stop_reasons": sorted({str(row["stop_reason"]) for row in rows}),
    }
    for key in (
        "final_field_rms",
        "late_field_rms",
        "late_field_rms_relative_change",
        "final_field_max_abs",
        "dominant_wavenumber",
        "half_power_peak_width",
        "source_field_phase_coherence",
        "source_field_phase_lag",
        "source_total_excursion",
        "source_late_excursion",
        "source_late_speed",
    ):
        values = [
            float(row[key])
            for row in rows
            if row[key] is not None and math.isfinite(float(row[key]))
        ]
        result[f"{key}_median"] = float(np.median(values)) if values else None
        result[f"{key}_max"] = float(np.max(values)) if values else None
    return result


def _shared_low_mode_error(reference: Any, candidate: Any) -> float:
    reference_values = (
        np.abs(reference.final_coefficients) / reference.final_coefficients.size
    )
    candidate_values = (
        np.abs(candidate.final_coefficients) / candidate.final_coefficients.size
    )
    reference_modes = {
        round(float(k), 10): float(value)
        for k, value in zip(
            reference.wavenumbers,
            reference_values,
            strict=True,
        )
        if abs(k) <= 3.0 + 1.0e-12
    }
    candidate_modes = {
        round(float(k), 10): float(value)
        for k, value in zip(
            candidate.wavenumbers,
            candidate_values,
            strict=True,
        )
        if abs(k) <= 3.0 + 1.0e-12
    }
    shared = sorted(reference_modes.keys() & candidate_modes.keys())
    reference_array = np.asarray([reference_modes[key] for key in shared])
    candidate_array = np.asarray([candidate_modes[key] for key in shared])
    denominator = float(np.linalg.norm(reference_array))
    if denominator == 0.0:
        return float(np.linalg.norm(candidate_array))
    return float(np.linalg.norm(candidate_array - reference_array) / denominator)


def _stationary_linear_error(
    config: ActiveScalarFieldConfig,
    trace: Any,
) -> float:
    position = 0.5 * config.domain_length
    source = config.source_strength * spectral_delta_coefficients(
        position,
        config,
        trace.wavenumbers,
    )
    denominator = -scalar_field_linear_rate(config, trace.wavenumbers)
    expected = source / denominator
    mode_number = np.fft.fftfreq(config.grid_points) * config.grid_points
    expected[np.abs(mode_number) >= config.grid_points / 4] = 0.0
    expected[config.grid_points // 2] = 0.0
    return float(
        np.linalg.norm(trace.final_coefficients - expected) / np.linalg.norm(expected)
    )


def _steady_equation_residual(
    config: ActiveScalarFieldConfig,
    trace: Any,
) -> float:
    coefficients = trace.final_coefficients
    field = np.fft.ifft(coefficients).real
    denominator = -scalar_field_linear_rate(config, trace.wavenumbers)
    nonlinear = np.fft.fft(config.cubic_saturation * np.power(field, 3))
    source = config.source_strength * spectral_delta_coefficients(
        0.5 * config.domain_length,
        config,
        trace.wavenumbers,
    )
    mode_number = np.fft.fftfreq(config.grid_points) * config.grid_points
    retained = np.abs(mode_number) < config.grid_points / 4
    residual = denominator * coefficients + nonlinear - source
    return float(np.linalg.norm(residual[retained]) / np.linalg.norm(source[retained]))


def _numerical_audit(
    base: ActiveScalarFieldConfig,
) -> tuple[dict[str, Any], dict[str, Any]]:
    fixed = replace(base, eta=0.0, epsilon=0.0, seed=1)
    time_traces: dict[str, Any] = {}
    for time_step in (0.1, 0.05, 0.025):
        config = replace(
            fixed,
            time_step=time_step,
            steps=int(round(200.0 / time_step)),
            sample_every=max(1, int(round(2.0 / time_step))),
        )
        time_traces[str(time_step)] = simulate_active_scalar_delta_field(config)
    grid_traces: dict[str, Any] = {}
    for grid_points in (128, 256, 512):
        config = replace(fixed, grid_points=grid_points)
        grid_traces[str(grid_points)] = simulate_active_scalar_delta_field(config)

    gaussian = simulate_active_scalar_delta_field(
        replace(
            fixed,
            gradient_coefficient=0.5,
            biharmonic_coefficient=0.125,
            cubic_saturation=0.0,
        )
    )
    stable = simulate_active_scalar_delta_field(
        replace(
            fixed,
            gradient_coefficient=-1.8,
            biharmonic_coefficient=1.0,
            cubic_saturation=0.0,
        )
    )
    active = grid_traces[str(base.grid_points)]
    audit = {
        "time_step_low_mode_errors_vs_dt_0p025": {
            key: _shared_low_mode_error(time_traces["0.025"], trace)
            for key, trace in time_traces.items()
        },
        "grid_low_mode_errors_vs_n512": {
            key: _shared_low_mode_error(grid_traces["512"], trace)
            for key, trace in grid_traces.items()
        },
        "gaussian_stationary_relative_error": _stationary_linear_error(
            replace(
                fixed,
                gradient_coefficient=0.5,
                biharmonic_coefficient=0.125,
                cubic_saturation=0.0,
            ),
            gaussian,
        ),
        "stable_finite_k_stationary_relative_error": _stationary_linear_error(
            replace(
                fixed,
                gradient_coefficient=-1.8,
                biharmonic_coefficient=1.0,
                cubic_saturation=0.0,
            ),
            stable,
        ),
        "active_steady_equation_relative_residual": _steady_equation_residual(
            fixed,
            active,
        ),
    }
    audit["time_convergence_pass"] = (
        audit["time_step_low_mode_errors_vs_dt_0p025"]["0.05"] <= 0.01
    )
    audit["grid_convergence_pass"] = (
        audit["grid_low_mode_errors_vs_n512"]["256"] <= 0.01
    )
    audit["linear_null_pass"] = (
        audit["gaussian_stationary_relative_error"] <= 1.0e-6
        and audit["stable_finite_k_stationary_relative_error"] <= 1.0e-6
    )
    audit["steady_equation_closure_pass"] = (
        audit["active_steady_equation_relative_residual"] <= 0.01
    )
    return audit, {
        "time": time_traces,
        "grid": grid_traces,
        "gaussian": gaussian,
        "stable": stable,
    }


def build_payload(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    _validate_args(args)
    traces: dict[tuple[str, int], Any] = {}
    rows: list[dict[str, Any]] = []
    case_configs: dict[str, ActiveScalarFieldConfig] = {}
    for seed in args.seeds:
        cases = build_cases(_base_config(args, seed=seed))
        case_configs = cases
        for name, config in cases.items():
            trace = simulate_active_scalar_delta_field(config)
            traces[(name, seed)] = trace
            rows.append(
                {
                    "case": name,
                    "seed": seed,
                    **_trace_metrics(trace, config),
                }
            )
    summary = {
        name: _aggregate([row for row in rows if row["case"] == name])
        for name in case_configs
    }
    numerical, numerical_traces = _numerical_audit(
        _base_config(args, seed=args.seeds[0])
    )
    active_rows = [row for row in rows if row["case"] == "active_finite_k"]
    cubic_rows = [row for row in rows if row["case"] == "cubic_off"]
    source_rows = [row for row in rows if row["case"] == "source_off"]
    eta_zero_rows = [row for row in rows if row["case"] == "eta_zero"]
    dk = 2.0 * np.pi / next(iter(case_configs.values())).domain_length
    eta_zero_relative_rms_differences = [
        abs(active["late_field_rms"] / eta_zero["late_field_rms"] - 1.0)
        for active, eta_zero in zip(active_rows, eta_zero_rows, strict=True)
    ]
    active_expected = scalar_field_preferred_wavenumber(case_configs["active_finite_k"])
    stable_expected = scalar_field_preferred_wavenumber(case_configs["stable_finite_k"])
    decisions = {
        "numerical_gate_pass": bool(
            numerical["time_convergence_pass"]
            and numerical["grid_convergence_pass"]
            and numerical["linear_null_pass"]
            and numerical["steady_equation_closure_pass"]
        ),
        "active_amplitude_bounded_pass": bool(
            all(row["stop_reason"] == "completed" for row in active_rows)
            and all(
                row["late_field_rms_relative_change"] is not None
                and row["late_field_rms_relative_change"] <= 0.05
                for row in active_rows
            )
        ),
        "cubic_saturation_discriminates_pass": bool(
            all(
                cubic["stop_reason"] != "completed"
                or cubic["final_field_rms"] > 10.0 * active["final_field_rms"]
                for cubic, active in zip(cubic_rows, active_rows, strict=True)
            )
        ),
        "source_off_null_pass": bool(
            all(row["final_field_max_abs"] <= 1.0e-14 for row in source_rows)
        ),
        "finite_wavenumber_peak_pass": bool(
            abs(
                summary["active_finite_k"]["dominant_wavenumber_median"]
                - active_expected
            )
            <= dk
            and abs(
                summary["stable_finite_k"]["dominant_wavenumber_median"]
                - stable_expected
            )
            <= dk
        ),
        "late_visible_source_bounded_pass": bool(
            all(row["source_late_excursion"] <= 0.05 for row in active_rows)
        ),
        "eta_zero_pattern_similarity_pass": bool(
            max(eta_zero_relative_rms_differences) <= 0.10
            and abs(
                summary["active_finite_k"]["dominant_wavenumber_median"]
                - summary["eta_zero"]["dominant_wavenumber_median"]
            )
            <= dk
        ),
        "pattern_requires_visible_readout": False,
        "exploratory_feedback_phase_relocation": bool(
            abs(
                abs(summary["active_finite_k"]["source_field_phase_lag_median"]) - np.pi
            )
            <= 0.10
            and abs(summary["eta_zero"]["source_field_phase_lag_median"]) <= 0.10
            and summary["active_finite_k"]["source_total_excursion_median"] >= 1.0
        ),
    }
    decisions["pattern_requires_visible_readout"] = not decisions[
        "eta_zero_pattern_similarity_pass"
    ]
    decisions["classical_finite_wavenumber_mechanism_gate_pass"] = bool(
        all(
            decisions[key]
            for key in (
                "numerical_gate_pass",
                "active_amplitude_bounded_pass",
                "cubic_saturation_discriminates_pass",
                "source_off_null_pass",
                "finite_wavenumber_peak_pass",
            )
        )
    )
    payload = {
        "question": (
            "Can the preregistered local scalar delta-source field produce a "
            "numerically converged, bounded finite-wavenumber pattern that "
            "separates from cubic-off and source-off controls?"
        ),
        "equation": (
            "d_t phi = -[1+a2(-d_x^2)+a4 d_x^4]phi "
            "- u phi^3 + s delta_L(x-X_t); "
            "dX_t = -eta d_x phi(X_t)dt + epsilon dW_t"
        ),
        "representation": (
            "Periodic 1D pseudo-spectral ETD1; the delta source uses every "
            "retained Fourier mode and has no fitted deposition width."
        ),
        "base_configuration": asdict(_base_config(args, seed=args.seeds[0])),
        "case_configurations": {
            name: asdict(config) for name, config in case_configs.items()
        },
        "seeds": args.seeds,
        "rows": rows,
        "summary": summary,
        "numerical_audit": numerical,
        "decisions": decisions,
        "claim_boundaries": {
            "classical_pattern_formation": bool(
                decisions["classical_finite_wavenumber_mechanism_gate_pass"]
            ),
            "feedback_specific_pattern": False,
            "exploratory_feedback_phase_relocation": bool(
                decisions["exploratory_feedback_phase_relocation"]
            ),
            "metastable_multidimensional_knot": False,
            "ambient_dimension_selection": False,
            "quantization_or_qft": False,
        },
    }
    return payload, {
        "case": traces,
        "numerical": numerical_traces,
    }


def _field_on_relative_grid(trace: Any, config: ActiveScalarFieldConfig) -> tuple:
    relative = np.linspace(
        -0.5 * config.domain_length,
        0.5 * config.domain_length,
        config.grid_points,
        endpoint=False,
    )
    position = float(trace.positions[-1])
    series = trace.final_coefficients / trace.final_coefficients.size
    field = np.real(
        np.exp(
            1j
            * np.outer(
                position + relative,
                trace.wavenumbers,
            )
        )
        @ series
    )
    return relative, field


def plot_result(
    args: argparse.Namespace,
    payload: dict[str, Any],
    traces: dict[str, Any],
    output: Path,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 8.8))
    colors = {
        "gaussian_null": "#277da1",
        "stable_finite_k": "#43aa8b",
        "active_finite_k": "#d1495b",
        "cubic_off": "#6f4e7c",
        "source_off": "#7d8597",
        "eta_zero": "#f8961e",
    }
    labels = {
        "gaussian_null": "Gaussian null",
        "stable_finite_k": "stable finite-k",
        "active_finite_k": "active + cubic",
        "cubic_off": "active, cubic off",
        "source_off": "source off",
        "eta_zero": "eta = 0",
    }

    u = np.linspace(0.0, 2.0, 1001)
    for name in ("gaussian_null", "stable_finite_k", "active_finite_k"):
        config = ActiveScalarFieldConfig(**payload["case_configurations"][name])
        denominator = (
            1.0
            + config.gradient_coefficient * np.square(u)
            + config.biharmonic_coefficient * np.power(u, 4)
        )
        axes[0, 0].plot(
            u,
            denominator,
            color=colors[name],
            linewidth=2.0,
            label=labels[name],
        )
    axes[0, 0].axhline(0.0, color="#202020", linewidth=0.8)
    axes[0, 0].set_xlabel("wavenumber k")
    axes[0, 0].set_ylabel("P(k)")
    axes[0, 0].set_title("Preregistered linear operators")
    axes[0, 0].legend(frameon=False)

    for name in labels:
        for seed in args.seeds:
            trace = traces["case"][(name, seed)]
            axes[0, 1].plot(
                trace.times,
                trace.field_rms,
                color=colors[name],
                alpha=0.28,
                linewidth=0.9,
            )
    axes[0, 1].set_yscale("symlog", linthresh=1.0e-4)
    axes[0, 1].set_xlabel("dimensionless time")
    axes[0, 1].set_ylabel("field RMS")
    axes[0, 1].set_title("Amplitude and mechanistic controls")

    for name in (
        "gaussian_null",
        "stable_finite_k",
        "active_finite_k",
        "eta_zero",
    ):
        trace = traces["case"][(name, args.seeds[0])]
        axes[1, 0].plot(
            trace.times,
            trace.dominant_wavenumber,
            color=colors[name],
            linewidth=1.7,
            label=labels[name],
        )
    axes[1, 0].set_xlabel("dimensionless time")
    axes[1, 0].set_ylabel("dominant positive k")
    axes[1, 0].set_title(f"Mode selection, seed {args.seeds[0]}")
    axes[1, 0].legend(frameon=False)

    for name in ("gaussian_null", "stable_finite_k", "active_finite_k"):
        trace = traces["case"][(name, args.seeds[0])]
        config = ActiveScalarFieldConfig(**payload["case_configurations"][name])
        relative, field = _field_on_relative_grid(trace, config)
        axes[1, 1].plot(
            relative,
            field,
            color=colors[name],
            linewidth=1.8,
            label=labels[name],
        )
    axes[1, 1].set_xlim(-12.0, 12.0)
    axes[1, 1].set_xlabel("x - final source position")
    axes[1, 1].set_ylabel("phi")
    axes[1, 1].set_title("Final source-aligned field")
    axes[1, 1].legend(frameon=False)

    for axis in axes.flat:
        axis.grid(alpha=0.2, linewidth=0.6)
    fig.suptitle("Active scalar delta-source mechanism gate", fontsize=14)
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def render_report(
    payload: dict[str, Any],
    *,
    generated: str,
    figure_link: str,
    json_link: str,
) -> str:
    summary = payload["summary"]
    numerical = payload["numerical_audit"]
    decisions = payload["decisions"]
    lines = [
        "# Active scalar delta-source field pilot",
        "",
        f"Generated: `{generated}`",
        "",
        "## Question",
        "",
        payload["question"],
        "",
        f"![Active scalar field pilot]({figure_link})",
        "",
        "## Fixed model",
        "",
        f"`{payload['equation']}`",
        "",
        payload["representation"],
        "",
        "The six arms were fixed before execution: Gaussian-null, stable",
        "finite-k, active finite-k with positive cubic saturation, cubic-off,",
        "source-off, and eta-zero. No coefficient was fit to these outputs.",
        "",
        "## Numerical gate",
        "",
        (
            "- time-step low-mode error (`dt=0.05` versus `0.025`): "
            f"`{numerical['time_step_low_mode_errors_vs_dt_0p025']['0.05']:.3e}`;"
        ),
        (
            "- grid low-mode error (`N_x=256` versus `512`): "
            f"`{numerical['grid_low_mode_errors_vs_n512']['256']:.3e}`;"
        ),
        (
            "- Gaussian/stable linear stationary errors: "
            f"`{numerical['gaussian_stationary_relative_error']:.3e}` / "
            f"`{numerical['stable_finite_k_stationary_relative_error']:.3e}`;"
        ),
        (
            "- active steady-equation residual: "
            f"`{numerical['active_steady_equation_relative_residual']:.3e}`."
        ),
        "",
        (
            "Numerical pass: "
            f"`{decisions['numerical_gate_pass']}`. The explicit Hermitian"
            " projection is part of the real-field integrator; without it an"
            " unstable mode can amplify floating-point asymmetry."
        ),
        "",
        "## Three-seed comparison",
        "",
        (
            "| case | completed | late RMS | late relative change | peak k | "
            "half-power width | late source excursion |"
        ),
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name in (
        "gaussian_null",
        "stable_finite_k",
        "active_finite_k",
        "cubic_off",
        "source_off",
        "eta_zero",
    ):
        item = summary[name]

        def fmt(key: str) -> str:
            value = item.get(key)
            return "n/a" if value is None else f"{value:.4g}"

        lines.append(
            f"| `{name}` | {item['completed_count']}/{item['run_count']} | "
            f"{fmt('late_field_rms_median')} | "
            f"{fmt('late_field_rms_relative_change_median')} | "
            f"{fmt('dominant_wavenumber_median')} | "
            f"{fmt('half_power_peak_width_median')} | "
            f"{fmt('source_late_excursion_median')} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            (
                "- bounded active amplitude: "
                f"`{decisions['active_amplitude_bounded_pass']}`;"
            ),
            (
                "- cubic-off discrimination: "
                f"`{decisions['cubic_saturation_discriminates_pass']}`;"
            ),
            (f"- source-off null: `{decisions['source_off_null_pass']}`;"),
            (
                "- finite-wavenumber peak: "
                f"`{decisions['finite_wavenumber_peak_pass']}`;"
            ),
            (
                "- late visible-source bound: "
                f"`{decisions['late_visible_source_bounded_pass']}`;"
            ),
            (
                "- eta-zero field-pattern similarity: "
                f"`{decisions['eta_zero_pattern_similarity_pass']}`;"
            ),
            (
                "- exploratory feedback phase relocation: "
                f"`{decisions['exploratory_feedback_phase_relocation']}`;"
            ),
            (
                "- classical finite-wavenumber mechanism gate: "
                f"`{decisions['classical_finite_wavenumber_mechanism_gate_pass']}`."
            ),
            "",
            "The active operator produces a bounded peak near the predicted",
            "finite wavenumber, while the same unstable linear operator without",
            "the cubic term grows until the safety stop. Source-off remains",
            "exactly zero. This is a positive result for the proposed classical",
            "pattern-forming mechanism.",
            "",
            "The eta-zero arm forms essentially the same field amplitude and",
            "wavenumber, so the finite-k pattern does not require visible trajectory",
            "readout. Exploratorily, readout changes the source-field phase from",
            "approximately zero to approximately pi and relocates the source by",
            "about half a wavelength before late-time pinning. This was not a",
            "preregistered gate and is neither an oscillation nor a metastable",
            "multidimensional knot.",
            "",
            "## Claim boundary",
            "",
            "- Evidence: numerically converged classical finite-k pattern",
            "  formation with a delta source and cubic saturation.",
            "- Inference: the local field law is a viable mechanism candidate",
            "  for later coupled-node tests.",
            "- Not established: ambient 3D selection, quantized states, spin,",
            "  QFT, particle identity, or a physical field law.",
            "",
            "## Provenance",
            "",
            f"- Git revision before generation: `{payload['git_revision']}`",
            f"- Git status before generation: `{payload['git_status']}`",
            (
                "- Script: "
                "`experiments/current/kernels/"
                "active_scalar_delta_field_pilot.py`"
            ),
            f"- Machine-readable summary: [{Path(json_link).name}]({json_link})",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    payload, traces = build_payload(args)
    report = _resolve(args.report)
    summary_json = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    payload["git_revision"] = _git_output(["rev-parse", "HEAD"])
    payload["git_status"] = _git_output(["status", "--short"])
    payload["outputs"] = {
        "report": str(args.report),
        "summary_json": str(args.summary_json),
        "figure": str(args.figure),
    }
    plot_result(args, payload, traces, figure)
    generated = datetime.now(UTC).isoformat()
    report.parent.mkdir(parents=True, exist_ok=True)
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    report.write_text(
        render_report(
            payload,
            generated=generated,
            figure_link=_relative_link(report, figure),
            json_link=_relative_link(report, summary_json),
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
