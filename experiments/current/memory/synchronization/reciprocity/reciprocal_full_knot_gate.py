"""P3.1: compare off, one-way, and synchronous reciprocal full-knot modes."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
import time
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from emergenz_knoten import (
    load_finite_memory_checkpoint,
    memory_shape_tensor,
    paired_shape_coherence_diagnostics,
)
from emergenz_knoten.kernels import (
    effective_double_gaussian_parameters,
    two_scale_local_curvature,
)
from emergenz_knoten.reciprocal_diagnostics import (
    fit_isotropic_relative_mode,
    relative_mode_phase_coherence,
)
from emergenz_knoten.reciprocal_modes import reciprocal_scalar_memory_modes
from emergenz_knoten.reciprocal_nodes import reciprocal_pair_response


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_CHECKPOINT = Path(
    "data/processed/reference_states/"
    "scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/"
    "scalar_Aatt35_d3_seed1_N100000000.npz"
)
CONDITION_COLORS = {
    "channel_off": "#666666",
    "one_way": "#0072B2",
    "reciprocal": "#D55E00",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="P3.1 synchronous reciprocal full-knot reconciliation gate."
    )
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--future-seeds", default="1,2,3,4,5")
    parser.add_argument("--updates", type=int, default=50_000)
    parser.add_argument("--sample-every", type=int, default=1)
    parser.add_argument("--distance-ratio", type=float, default=2.5)
    parser.add_argument("--cross-gain", type=float, default=0.02)
    parser.add_argument("--analysis-burn-memory-times", type=float, default=100.0)
    parser.add_argument("--segments", type=int, default=4)
    parser.add_argument("--min-complex-segments", type=int, default=3)
    parser.add_argument("--min-complex-seeds", type=int, default=4)
    parser.add_argument("--max-control-complex-seeds", type=int, default=1)
    parser.add_argument("--frequency-min-per-memory-time", type=float, default=0.05)
    parser.add_argument("--mode-relative-range-max", type=float, default=0.25)
    parser.add_argument("--phase-coherence-min", type=float, default=0.5)
    parser.add_argument("--fit-residual-ratio-max", type=float, default=0.8)
    parser.add_argument("--fit-condition-max", type=float, default=1e8)
    parser.add_argument("--response-min-r", type=float, default=1e-3)
    parser.add_argument("--radius-factor-limit", type=float, default=1.10)
    parser.add_argument("--shape-spectrum-median-limit", type=float, default=0.05)
    parser.add_argument("--shape-spectrum-q95-limit", type=float, default=0.10)
    parser.add_argument("--noise-seed-offset", type=int, default=20_260_804)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/reciprocal/reciprocal_full_knot_gate_2026-08-04.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/reciprocal/reciprocal_full_knot_gate_2026-08-04.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path("figures/draft/response/reciprocal_full_knot_gate_2026-08-04.png"),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _relative_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _git(arguments: list[str]) -> str:
    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return _jsonable(value.tolist())
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if np.isfinite(number) else None
    if isinstance(value, np.complexfloating):
        value = complex(value)
    if isinstance(value, complex):
        return {"real": float(value.real), "imag": float(value.imag)}
    if isinstance(value, Path):
        return _relative(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def parse_seeds(text: str) -> list[int]:
    values = [int(part.strip()) for part in text.split(",") if part.strip()]
    if (
        not values
        or len(values) != len(set(values))
        or any(value < 0 for value in values)
    ):
        raise ValueError("future seeds must be unique non-negative integers")
    return values


def _proper_cyclic_rotation(dim: int) -> np.ndarray:
    rotation = np.eye(dim)
    if dim > 1:
        rotation = np.roll(rotation, shift=1, axis=0)
        if np.linalg.det(rotation) < 0.0:
            rotation[[0, 1]] = rotation[[1, 0]]
    return rotation


def _relative_range(values: list[float]) -> float:
    if not values:
        return math.inf
    median = float(np.median(values))
    return float((max(values) - min(values)) / max(abs(median), np.finfo(float).tiny))


def _mode_row(
    relative_positions: np.ndarray,
    relative_centers: np.ndarray,
    *,
    alpha: float,
    sample_every: int,
    thresholds: dict[str, float],
) -> dict[str, Any]:
    fitted = fit_isotropic_relative_mode(relative_positions, relative_centers)
    frequency = fitted.angular_frequency / (alpha * sample_every)
    damping = fitted.damping_rate / (alpha * sample_every)
    coherence = relative_mode_phase_coherence(
        relative_positions,
        relative_centers,
        fitted,
    )
    meaningful = bool(
        fitted.is_complex
        and fitted.is_stable
        and frequency >= thresholds["frequency_min_per_memory_time"]
        and fitted.residual_ratio <= thresholds["fit_residual_ratio_max"]
        and fitted.design_condition <= thresholds["fit_condition_max"]
        and coherence >= thresholds["phase_coherence_min"]
    )
    return {
        "transition": fitted.transition,
        "intercept": fitted.intercept,
        "eigenvalues": fitted.eigenvalues,
        "is_complex": fitted.is_complex,
        "is_stable": fitted.is_stable,
        "frequency_per_memory_time": frequency,
        "damping_per_memory_time": damping,
        "phase_coherence": coherence,
        "residual_ratio": fitted.residual_ratio,
        "design_condition": fitted.design_condition,
        "meaningful_complex": meaningful,
    }


def _segment_modes(
    relative_positions: np.ndarray,
    relative_centers: np.ndarray,
    *,
    start_index: int,
    segments: int,
    alpha: float,
    sample_every: int,
    thresholds: dict[str, float],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    boundaries = np.rint(
        np.linspace(start_index, relative_positions.shape[0] - 1, segments + 1)
    ).astype(int)
    rows: list[dict[str, Any]] = []
    for index in range(segments):
        begin = int(boundaries[index])
        end = int(boundaries[index + 1])
        row = _mode_row(
            relative_positions[begin : end + 1],
            relative_centers[begin : end + 1],
            alpha=alpha,
            sample_every=sample_every,
            thresholds=thresholds,
        )
        row["segment"] = index + 1
        row["sample_start"] = begin
        row["sample_end"] = end
        rows.append(row)

    selected = [row for row in rows if row["meaningful_complex"]]
    frequencies = [float(row["frequency_per_memory_time"]) for row in selected]
    dampings = [float(row["damping_per_memory_time"]) for row in selected]
    frequency_range = _relative_range(frequencies)
    damping_range = _relative_range(dampings)
    identity_pass = bool(
        len(selected) >= int(thresholds["min_complex_segments"])
        and frequency_range <= thresholds["mode_relative_range_max"]
        and damping_range <= thresholds["mode_relative_range_max"]
    )
    return rows, {
        "meaningful_complex_segments": len(selected),
        "frequency_relative_range": frequency_range,
        "damping_relative_range": damping_range,
        "median_frequency_per_memory_time": float(np.median(frequencies))
        if frequencies
        else 0.0,
        "median_damping_per_memory_time": float(np.median(dampings))
        if dampings
        else 0.0,
        "median_phase_coherence": float(
            np.median([row["phase_coherence"] for row in selected])
        )
        if selected
        else 0.0,
        "segment_identity_pass": identity_pass,
    }


def _shape_metrics(
    response: Any,
    condition_index: int,
    node: int,
    thresholds: dict[str, float],
) -> dict[str, Any]:
    return paired_shape_coherence_diagnostics(
        response.radius_ratios[:, condition_index, node],
        response.radius_ratios[:, 0, node],
        response.shape_tensors[:, condition_index, node],
        response.shape_tensors[:, 0, node],
        radius_factor_limit=thresholds["radius_factor_limit"],
        spectrum_median_limit=thresholds["shape_spectrum_median_limit"],
        spectrum_q95_limit=thresholds["shape_spectrum_q95_limit"],
    )


def _zero_cross_identity(
    checkpoint: Any,
    *,
    separation: np.ndarray,
    second_rotation: np.ndarray,
) -> float:
    steps = 100
    noise = np.zeros((steps, checkpoint.config.dim))
    response = reciprocal_pair_response(
        checkpoint.state,
        checkpoint.state,
        checkpoint.config,
        initial_center_separation=separation,
        first_noise=noise,
        second_noise=noise,
        sample_steps=[0, steps],
        cross_eta=0.0,
        second_rotation=second_rotation,
    )
    return float(
        max(
            np.max(np.abs(response.positions[:, index] - response.positions[:, 0]))
            for index in (1, 2)
        )
    )


def run_gate(args: argparse.Namespace) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    checkpoint_path = _resolve(args.checkpoint)
    checkpoint = load_finite_memory_checkpoint(checkpoint_path)
    config = checkpoint.config
    seeds = parse_seeds(args.future_seeds)
    if args.updates < 100 or args.sample_every < 1 or args.segments < 2:
        raise SystemExit("updates, sample cadence, or segments are invalid")
    if args.updates % args.sample_every:
        raise SystemExit("updates must be divisible by sample-every")
    if args.distance_ratio <= 0.0 or args.cross_gain <= 0.0:
        raise SystemExit("distance ratio and cross gain must be positive")
    if not args.allow_dirty and _git(["status", "--porcelain"]):
        raise SystemExit("working tree is dirty; commit first or pass --allow-dirty")

    started_at = time.perf_counter()
    initial_radius = float(np.sqrt(np.trace(memory_shape_tensor(checkpoint.state))))
    separation = np.zeros(config.dim)
    separation[0] = args.distance_ratio * initial_radius
    rotation = _proper_cyclic_rotation(config.dim)
    effective = effective_double_gaussian_parameters(
        dim=config.dim,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )
    curvature = two_scale_local_curvature(**effective)
    retained_mass = float(np.sum(checkpoint.state.weights))
    if curvature <= 0.0:
        raise SystemExit(
            "registered positive cross gain requires positive local curvature"
        )
    cross_eta = args.cross_gain / (retained_mass * curvature)
    self_gain = config.eta * retained_mass * curvature
    analytic = reciprocal_scalar_memory_modes(
        config.alpha,
        self_gain=self_gain,
        cross_gain=args.cross_gain,
    )

    sample_steps = np.arange(0, args.updates + 1, args.sample_every, dtype=int)
    analysis_start_updates = int(round(args.analysis_burn_memory_times / config.alpha))
    if analysis_start_updates >= args.updates:
        raise SystemExit("analysis burn leaves no post-burn samples")
    start_index = int(np.searchsorted(sample_steps, analysis_start_updates))
    if (sample_steps.size - 1 - start_index) // args.segments < 100:
        raise SystemExit("post-burn segments need at least 100 transitions each")

    thresholds = {
        "min_complex_segments": args.min_complex_segments,
        "frequency_min_per_memory_time": args.frequency_min_per_memory_time,
        "mode_relative_range_max": args.mode_relative_range_max,
        "phase_coherence_min": args.phase_coherence_min,
        "fit_residual_ratio_max": args.fit_residual_ratio_max,
        "fit_condition_max": args.fit_condition_max,
        "response_min_r": args.response_min_r,
        "radius_factor_limit": args.radius_factor_limit,
        "shape_spectrum_median_limit": args.shape_spectrum_median_limit,
        "shape_spectrum_q95_limit": args.shape_spectrum_q95_limit,
    }
    zero_cross_error = _zero_cross_identity(
        checkpoint,
        separation=separation,
        second_rotation=rotation,
    )
    rows: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    for future_seed in seeds:
        rng = np.random.default_rng(args.noise_seed_offset + future_seed)
        first_noise = rng.standard_normal((args.updates, config.dim))
        second_noise = rng.standard_normal((args.updates, config.dim))
        response = reciprocal_pair_response(
            checkpoint.state,
            checkpoint.state,
            config,
            initial_center_separation=separation,
            first_noise=first_noise,
            second_noise=second_noise,
            sample_steps=sample_steps,
            cross_eta=cross_eta,
            second_rotation=rotation,
        )
        condition_rows: dict[str, Any] = {}
        for condition_index, condition in enumerate(response.conditions):
            relative_positions = 0.5 * (
                response.positions[:, condition_index, 1]
                - response.positions[:, condition_index, 0]
            )
            relative_centers = 0.5 * (
                response.memory_centers[:, condition_index, 1]
                - response.memory_centers[:, condition_index, 0]
            )
            segment_rows, mode_summary = _segment_modes(
                relative_positions,
                relative_centers,
                start_index=start_index,
                segments=args.segments,
                alpha=config.alpha,
                sample_every=args.sample_every,
                thresholds=thresholds,
            )
            center_delta = (
                response.memory_centers[:, condition_index]
                - response.memory_centers[:, 0]
            )
            response_rms_r = float(
                np.sqrt(np.mean(np.sum(center_delta * center_delta, axis=-1)))
                / initial_radius
            )
            shapes = []
            if condition_index > 0:
                shapes = [
                    _shape_metrics(response, condition_index, node, thresholds)
                    for node in range(2)
                ]
            shape_pass = bool(
                condition_index == 0
                or all(item["shape_bounded_coherent_pass"] for item in shapes)
            )
            channel_detected = bool(
                condition_index == 0 or response_rms_r >= args.response_min_r
            )
            condition_rows[condition] = {
                "mode_segments": segment_rows,
                "mode_summary": mode_summary,
                "response_rms_r": response_rms_r,
                "node_shape_metrics": shapes,
                "shape_bounded_coherent_pass": shape_pass,
                "channel_detected": channel_detected,
                "candidate_pass": bool(
                    mode_summary["segment_identity_pass"]
                    and shape_pass
                    and channel_detected
                ),
                "final_pair_distance_r": float(
                    np.linalg.norm(
                        response.memory_centers[-1, condition_index, 1]
                        - response.memory_centers[-1, condition_index, 0]
                    )
                    / initial_radius
                ),
            }
        rows.append({"future_seed": future_seed, "conditions": condition_rows})

        plot_stride = max(1, sample_steps.size // 1200)
        traces.append(
            {
                "future_seed": future_seed,
                "sample_steps": sample_steps[::plot_stride],
                "pair_distances_r": np.linalg.norm(
                    response.memory_centers[::plot_stride, :, 1]
                    - response.memory_centers[::plot_stride, :, 0],
                    axis=-1,
                )
                / initial_radius,
                "relative_positions_axis_r": 0.5
                * (
                    response.positions[::plot_stride, :, 1, 0]
                    - response.positions[::plot_stride, :, 0, 0]
                )
                / initial_radius,
                "relative_centers_axis_r": 0.5
                * (
                    response.memory_centers[::plot_stride, :, 1, 0]
                    - response.memory_centers[::plot_stride, :, 0, 0]
                )
                / initial_radius,
            }
        )

    candidate_counts = {
        condition: sum(
            bool(row["conditions"][condition]["candidate_pass"]) for row in rows
        )
        for condition in ("channel_off", "one_way", "reciprocal")
    }
    shape_counts = {
        condition: sum(
            bool(row["conditions"][condition]["shape_bounded_coherent_pass"])
            for row in rows
        )
        for condition in ("one_way", "reciprocal")
    }
    response_counts = {
        condition: sum(
            bool(row["conditions"][condition]["channel_detected"]) for row in rows
        )
        for condition in ("one_way", "reciprocal")
    }
    controls_bounded = bool(
        candidate_counts["channel_off"] <= args.max_control_complex_seeds
        and candidate_counts["one_way"] <= args.max_control_complex_seeds
    )
    reciprocal_candidate = bool(
        candidate_counts["reciprocal"] >= args.min_complex_seeds and controls_bounded
    )
    operational = bool(
        zero_cross_error == 0.0
        and shape_counts["reciprocal"] >= args.min_complex_seeds
        and response_counts["reciprocal"] >= args.min_complex_seeds
    )
    if reciprocal_candidate:
        classification = "unexpected nonlinear complex-mode candidate"
    elif operational:
        classification = "registered real-mode null confirmed"
    else:
        classification = "inconclusive: channel or shape gate failed"

    runtime_seconds = time.perf_counter() - started_at
    payload = {
        "schema": "emergenz-knoten.reciprocal-full-knot-gate",
        "schema_version": 1,
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": _git(["rev-parse", "HEAD"]),
        "git_status": _git(["status", "--porcelain"]),
        "checkpoint": _relative(checkpoint_path),
        "checkpoint_update_index": checkpoint.update_index,
        "formation_seed": checkpoint.formation_seed,
        "config": asdict(config),
        "parameters": vars(args),
        "runtime_seconds": runtime_seconds,
        "continuation_updates_per_second": len(seeds) * args.updates / runtime_seconds,
        "derived": {
            "initial_radius": initial_radius,
            "initial_center_separation": separation,
            "retained_memory_mass": retained_mass,
            "effective_local_curvature": curvature,
            "finite_horizon_self_gain": self_gain,
            "registered_cross_gain": args.cross_gain,
            "cross_eta": cross_eta,
            "analysis_start_updates": analysis_start_updates,
            "analysis_start_memory_times": analysis_start_updates * config.alpha,
            "continuation_memory_times": args.updates * config.alpha,
            "second_state_rotation": rotation,
        },
        "analytic_relative_mode": {
            "multipliers": analytic.relative_multipliers,
            "trace": analytic.relative_trace,
            "determinant": analytic.relative_determinant,
            "discriminant": analytic.relative_discriminant,
            "is_complex": analytic.relative_is_complex,
            "is_stable": analytic.relative_is_stable,
        },
        "thresholds": thresholds,
        "rows": rows,
        "gate": {
            "zero_cross_max_abs_error": zero_cross_error,
            "zero_cross_identity_pass": zero_cross_error == 0.0,
            "candidate_seed_counts": candidate_counts,
            "shape_seed_counts": shape_counts,
            "response_seed_counts": response_counts,
            "controls_bounded_pass": controls_bounded,
            "reciprocal_complex_candidate_pass": reciprocal_candidate,
            "operational_reconciliation_pass": operational,
            "classification": classification,
        },
    }
    return _jsonable(payload), traces


def _plot(payload: dict[str, Any], traces: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    alpha = float(payload["config"]["alpha"])
    conditions = ("channel_off", "one_way", "reciprocal")
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.6))

    for condition_index, condition in enumerate(conditions):
        for trace in traces:
            axes[0, 0].plot(
                trace["sample_steps"] * alpha,
                trace["pair_distances_r"][:, condition_index],
                color=CONDITION_COLORS[condition],
                alpha=0.25,
                linewidth=0.8,
            )
        stacked = np.vstack(
            [trace["pair_distances_r"][:, condition_index] for trace in traces]
        )
        axes[0, 0].plot(
            traces[0]["sample_steps"] * alpha,
            np.median(stacked, axis=0),
            color=CONDITION_COLORS[condition],
            linewidth=2.0,
            label=condition,
        )
    axes[0, 0].set_xlabel("continuation / memory times")
    axes[0, 0].set_ylabel("memory-centre separation / R")
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.25)

    representative = traces[0]
    reciprocal_index = 2
    time = representative["sample_steps"] * alpha
    axes[0, 1].plot(
        time,
        representative["relative_positions_axis_r"][:, reciprocal_index],
        label="visible relative coordinate",
        color="#D55E00",
    )
    axes[0, 1].plot(
        time,
        representative["relative_centers_axis_r"][:, reciprocal_index],
        label="memory relative coordinate",
        color="#009E73",
    )
    axes[0, 1].set_xlabel("continuation / memory times")
    axes[0, 1].set_ylabel("initial-axis coordinate / R")
    axes[0, 1].set_title(f"reciprocal arm, future seed {representative['future_seed']}")
    axes[0, 1].legend(fontsize=8)
    axes[0, 1].grid(alpha=0.25)

    angle = np.linspace(0.0, 2.0 * np.pi, 300)
    axes[1, 0].plot(np.cos(angle), np.sin(angle), color="#999999", linewidth=1)
    for condition in conditions:
        eigenvalues = []
        for row in payload["rows"]:
            for segment in row["conditions"][condition]["mode_segments"]:
                eigenvalues.extend(
                    complex(value["real"], value["imag"])
                    for value in segment["eigenvalues"]
                )
        axes[1, 0].scatter(
            [value.real for value in eigenvalues],
            [value.imag for value in eigenvalues],
            s=18,
            alpha=0.65,
            color=CONDITION_COLORS[condition],
            label=condition,
        )
    axes[1, 0].axhline(0.0, color="#bbbbbb", linewidth=0.8)
    axes[1, 0].set_aspect("equal", adjustable="box")
    axes[1, 0].set_xlabel("Re multiplier")
    axes[1, 0].set_ylabel("Im multiplier")
    axes[1, 0].set_title("segmentwise isotropic relative-mode fits")
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].grid(alpha=0.2)

    x = np.arange(len(payload["rows"]))
    width = 0.24
    for condition_index, condition in enumerate(conditions):
        counts = [
            row["conditions"][condition]["mode_summary"]["meaningful_complex_segments"]
            for row in payload["rows"]
        ]
        axes[1, 1].bar(
            x + (condition_index - 1) * width,
            counts,
            width,
            color=CONDITION_COLORS[condition],
            label=condition,
        )
    axes[1, 1].axhline(
        payload["thresholds"]["min_complex_segments"],
        color="#222222",
        linestyle="--",
        linewidth=1,
        label="segment gate",
    )
    axes[1, 1].set_xticks(
        x,
        [str(row["future_seed"]) for row in payload["rows"]],
    )
    axes[1, 1].set_xlabel("future-noise seed")
    axes[1, 1].set_ylabel("meaningful complex segments")
    axes[1, 1].set_ylim(0, payload["parameters"]["segments"] + 0.5)
    axes[1, 1].legend(fontsize=8)
    axes[1, 1].grid(axis="y", alpha=0.25)

    fig.suptitle("P3.1 synchronous reciprocal full-knot reconciliation")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    gate = payload["gate"]
    analytic = payload["analytic_relative_mode"]
    derived = payload["derived"]
    parameters = payload["parameters"]
    lines = [
        "# P3.1 reciprocal full-knot reconciliation gate",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Question",
        "",
        "Does synchronous instantaneous reciprocal scalar readout create a stable,",
        "control-separated complex relative mode in the complete finite-memory knot,",
        "despite the registered local reduction predicting a real mode?",
        "",
        "## Meaning of complex",
        "",
        "A coordinate-fixed-effects real 2 x 2 relative-state matrix has a complex mode when its",
        "eigenvalues are a non-real conjugate pair. Such a matrix is real-similar",
        "to `a E + b J`, with `J=[[0,-1],[1,0]]`; it need not have that literal",
        "entry pattern in the measured `(x_-, m_-)` coordinates. This rotation is",
        "in relative state space, not evidence for spatial rotation or d=3.",
        "",
        "## Fixed design",
        "",
        f"- complete d={payload['config']['dim']} checkpoint at "
        f"N={payload['checkpoint_update_index']:,}, formation seed "
        f"{payload['formation_seed']};",
        "- two copies are rigidly placed and the second is cyclically rotated;",
        f"- initial centre distance `{parameters['distance_ratio']:.3g} R_pair`;",
        f"- lambda={payload['config']['alpha']:.4g}, eta={payload['config']['eta']:.4g}, "
        f"epsilon={payload['config']['epsilon']:.4g};",
        f"- registered finite-horizon cross gain c={parameters['cross_gain']:.4g}, "
        f"giving cross_eta={derived['cross_eta']:.7g};",
        f"- {len(payload['rows'])} node-specific future-noise seed pairs, each "
        "shared across channel-off, one-way, and reciprocal conditions;",
        f"- {parameters['updates']:,} updates = "
        f"{derived['continuation_memory_times']:.1f} memory times; the first "
        f"{derived['analysis_start_memory_times']:.1f} memory times are excluded from "
        f"four segment fits.",
        "",
        f"- runtime {payload['runtime_seconds']:.2f} s, or "
        f"{payload['continuation_updates_per_second']:.1f} continuation updates/s.",
        "",
        "The future-noise seeds are repeated continuations of one formation basin.",
        "They test pathwise robustness but are not independent knot formations.",
        "",
        "## Analytic preregistration",
        "",
        f"The retained-memory self gain is `{derived['finite_horizon_self_gain']:.6g}`.",
        f"At c={parameters['cross_gain']:.4g}, the local relative discriminant is "
        f"`{analytic['discriminant']:.6g}` and the multipliers are "
        f"`{analytic['multipliers']}`. The local mode is therefore "
        f"complex={analytic['is_complex']}, stable={analytic['is_stable']}.",
        "",
        "A segment counts only if the fitted pair is stable and non-real, its",
        f"frequency is at least {parameters['frequency_min_per_memory_time']:.3g} per "
        "memory time, phase coherence is at least "
        f"{parameters['phase_coherence_min']:.3g}, normalized residual at most "
        f"{parameters['fit_residual_ratio_max']:.3g}, and design condition at most "
        f"{parameters['fit_condition_max']:.3g}. A seed needs "
        f"{parameters['min_complex_segments']}/{parameters['segments']} segments with "
        f"frequency and damping ranges each at most "
        f"{parameters['mode_relative_range_max']:.3g}. The reciprocal candidate needs "
        f"{parameters['min_complex_seeds']}/{len(payload['rows'])} seeds and at most "
        f"{parameters['max_control_complex_seeds']} candidate seed in either control.",
        "",
        "## Result",
        "",
        f"Classification: **{gate['classification']}**.",
        "",
        f"- exact cross-zero identity: {gate['zero_cross_identity_pass']} "
        f"(max error {gate['zero_cross_max_abs_error']:.3e});",
        f"- candidate seeds off / one-way / reciprocal: "
        f"{gate['candidate_seed_counts']['channel_off']} / "
        f"{gate['candidate_seed_counts']['one_way']} / "
        f"{gate['candidate_seed_counts']['reciprocal']};",
        f"- reciprocal response detected: "
        f"{gate['response_seed_counts']['reciprocal']}/{len(payload['rows'])};",
        f"- reciprocal shape bounded/coherent: "
        f"{gate['shape_seed_counts']['reciprocal']}/{len(payload['rows'])};",
        f"- nonlinear complex candidate: {gate['reciprocal_complex_candidate_pass']}.",
        "",
        f"![P3.1 reciprocal full-knot gate]({_relative_from(report, figure)})",
        "",
        "## Seed rows",
        "",
        "| future seed | off complex seg | one-way complex seg | reciprocal complex seg | "
        "reciprocal response/R | reciprocal shape | final separation/R | candidate |",
        "| ---: | ---: | ---: | ---: | ---: | :---: | ---: | :---: |",
    ]
    for row in payload["rows"]:
        off = row["conditions"]["channel_off"]
        one_way = row["conditions"]["one_way"]
        reciprocal = row["conditions"]["reciprocal"]
        lines.append(
            f"| {row['future_seed']} | "
            f"{off['mode_summary']['meaningful_complex_segments']} | "
            f"{one_way['mode_summary']['meaningful_complex_segments']} | "
            f"{reciprocal['mode_summary']['meaningful_complex_segments']} | "
            f"{reciprocal['response_rms_r']:.4g} | "
            f"{reciprocal['shape_bounded_coherent_pass']} | "
            f"{reciprocal['final_pair_distance_r']:.4g} | "
            f"{reciprocal['candidate_pass']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "- A null confirms only the registered direct instantaneous scalar arm at",
            "  this fixed gain and mature checkpoint. It is not a no-oscillator theorem",
            "  for nonlinear fields, delayed mediators, or oriented memory.",
            "- A positive result would remain a candidate until reproduced across",
            "  independently formed mature states without retuning.",
            "- Shape-bounded/coherent permits bounded breathing and rigid rotation; it",
            "  does not require pointwise shape preservation.",
            "- No charge, spin, particle, QFT, or dimensional-selection claim follows.",
            "",
            "## Reproduction",
            "",
            "    python experiments/current/memory/synchronization/reciprocity/reciprocal_full_knot_gate.py",
            "",
            f"Checkpoint: `{payload['checkpoint']}`.",
            f"Git revision: `{payload['git_revision']}`.",
            f"Machine-readable summary: "
            f"[{Path(parameters['summary_json']).name}]"
            f"({_relative_from(report, _resolve(Path(parameters['summary_json'])))})",
            f"Git status at generation: `{payload['git_status'] or 'clean'}`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    payload, traces = run_gate(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _plot(payload, traces, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")
    print(json.dumps(payload["gate"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
