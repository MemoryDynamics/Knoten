"""P3.2: reciprocal full-knot modes through one fixed Telegraph mediator."""

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
    LocalMediatorGrid,
    TelegraphMediator,
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
from emergenz_knoten.retarded_reciprocal import (
    RETARDED_RECIPROCAL_CONDITIONS,
    retarded_reciprocal_pair_response,
)


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
    "instantaneous_reciprocal": "#D55E00",
    "retarded_one_way": "#0072B2",
    "retarded_reciprocal": "#009E73",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="P3.2 fixed-Telegraph reciprocal full-knot mode gate."
    )
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--future-seeds", default="1,2,3,4,5")
    parser.add_argument("--updates", type=int, default=50_000)
    parser.add_argument("--sample-every", type=int, default=1)
    parser.add_argument("--distance-ratio", type=float, default=2.5)
    parser.add_argument("--cross-gain", type=float, default=0.02)
    parser.add_argument("--correlation-length-r", type=float, default=5.0)
    parser.add_argument("--relaxation-memory-times", type=float, default=10.0)
    parser.add_argument("--grid-spacing-r", type=float, default=0.25)
    parser.add_argument("--grid-points-left", type=int, default=120)
    parser.add_argument("--grid-points-right", type=int, default=180)
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
    parser.add_argument("--mediator-rms-min", type=float, default=1e-6)
    parser.add_argument("--radius-factor-limit", type=float, default=1.10)
    parser.add_argument("--shape-spectrum-median-limit", type=float, default=0.05)
    parser.add_argument("--shape-spectrum-q95-limit", type=float, default=0.10)
    parser.add_argument("--noise-seed-offset", type=int, default=20_260_804)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/retarded_reciprocal_full_knot_gate_2026-08-04.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/retarded_reciprocal_full_knot_gate_2026-08-04.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/retarded_reciprocal_full_knot_gate_2026-08-04.png"
        ),
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
        relative_positions, relative_centers, fitted
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
        row.update(segment=index + 1, sample_start=begin, sample_end=end)
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
    response: Any, condition_index: int, node: int, thresholds: dict[str, float]
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


def run_gate(args: argparse.Namespace) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    checkpoint_path = _resolve(args.checkpoint)
    checkpoint = load_finite_memory_checkpoint(checkpoint_path)
    config = checkpoint.config
    seeds = parse_seeds(args.future_seeds)
    if args.updates < 100 or args.sample_every < 1 or args.segments < 2:
        raise SystemExit("updates, sample cadence, or segments are invalid")
    if args.updates % args.sample_every:
        raise SystemExit("updates must be divisible by sample-every")
    if (
        min(
            args.distance_ratio,
            args.cross_gain,
            args.correlation_length_r,
            args.relaxation_memory_times,
            args.grid_spacing_r,
        )
        <= 0.0
    ):
        raise SystemExit("registered scales and gains must be positive")
    if min(args.grid_points_left, args.grid_points_right) < 2:
        raise SystemExit("mediator grid requires at least two points on each side")
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
    direct_analytic = reciprocal_scalar_memory_modes(
        config.alpha,
        self_gain=self_gain,
        cross_gain=args.cross_gain,
    )

    correlation_length = args.correlation_length_r * initial_radius
    relaxation_time = args.relaxation_memory_times
    grid = LocalMediatorGrid(
        spacing=args.grid_spacing_r * initial_radius,
        time_step=config.alpha,
        points_left=args.grid_points_left,
        points_right=args.grid_points_right,
    )
    mediator = TelegraphMediator(
        wave_speed=correlation_length / relaxation_time,
        damping_rate=1.0 / relaxation_time,
        natural_frequency=1.0 / relaxation_time,
    )
    readout_position = float(np.linalg.norm(separation))

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
        "mediator_rms_min": args.mediator_rms_min,
        "radius_factor_limit": args.radius_factor_limit,
        "shape_spectrum_median_limit": args.shape_spectrum_median_limit,
        "shape_spectrum_q95_limit": args.shape_spectrum_q95_limit,
    }
    rows: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    static_gain = 0.0
    source_normalization = 0.0
    for future_seed in seeds:
        rng = np.random.default_rng(args.noise_seed_offset + future_seed)
        first_noise = rng.standard_normal((args.updates, config.dim))
        second_noise = rng.standard_normal((args.updates, config.dim))
        response = retarded_reciprocal_pair_response(
            checkpoint.state,
            checkpoint.state,
            config,
            initial_center_separation=separation,
            first_noise=first_noise,
            second_noise=second_noise,
            sample_steps=sample_steps,
            cross_eta=cross_eta,
            mediator_grid=grid,
            mediator=mediator,
            mediator_readout_position=readout_position,
            second_rotation=rotation,
        )
        static_gain = response.static_readout_gain
        source_normalization = response.source_normalization
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
            mediator_rms = float(
                np.sqrt(
                    np.mean(
                        np.square(
                            response.mediator_readouts[start_index:, condition_index]
                        )
                    )
                )
            )
            input_rms = float(
                np.sqrt(
                    np.mean(
                        np.square(
                            response.mediator_inputs[start_index:, condition_index]
                        )
                    )
                )
            )
            shapes = (
                []
                if condition_index == 0
                else [
                    _shape_metrics(response, condition_index, node, thresholds)
                    for node in range(2)
                ]
            )
            shape_pass = bool(
                condition_index == 0
                or all(item["shape_bounded_coherent_pass"] for item in shapes)
            )
            channel_detected = bool(
                condition_index == 0 or response_rms_r >= args.response_min_r
            )
            mediator_detected = bool(
                condition not in ("retarded_one_way", "retarded_reciprocal")
                or mediator_rms >= args.mediator_rms_min
            )
            condition_rows[condition] = {
                "mode_segments": segment_rows,
                "mode_summary": mode_summary,
                "response_rms_r": response_rms_r,
                "mediator_readout_rms": mediator_rms,
                "mediator_input_rms": input_rms,
                "mediator_detected": mediator_detected,
                "node_shape_metrics": shapes,
                "shape_bounded_coherent_pass": shape_pass,
                "channel_detected": channel_detected,
                "candidate_pass": bool(
                    mode_summary["segment_identity_pass"]
                    and shape_pass
                    and channel_detected
                    and mediator_detected
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
                "mediator_input_axis": response.mediator_inputs[::plot_stride, 3, 0, 0],
                "mediator_readout_axis": response.mediator_readouts[
                    ::plot_stride, 3, 0, 0
                ],
            }
        )

    candidate_counts = {
        condition: sum(
            bool(row["conditions"][condition]["candidate_pass"]) for row in rows
        )
        for condition in RETARDED_RECIPROCAL_CONDITIONS
    }
    shape_counts = {
        condition: sum(
            bool(row["conditions"][condition]["shape_bounded_coherent_pass"])
            for row in rows
        )
        for condition in RETARDED_RECIPROCAL_CONDITIONS[1:]
    }
    response_counts = {
        condition: sum(
            bool(row["conditions"][condition]["channel_detected"]) for row in rows
        )
        for condition in RETARDED_RECIPROCAL_CONDITIONS[1:]
    }
    mediator_counts = {
        condition: sum(
            bool(row["conditions"][condition]["mediator_detected"]) for row in rows
        )
        for condition in ("retarded_one_way", "retarded_reciprocal")
    }
    controls_bounded = bool(
        all(
            candidate_counts[condition] <= args.max_control_complex_seeds
            for condition in RETARDED_RECIPROCAL_CONDITIONS[:-1]
        )
    )
    retarded_candidate = bool(
        candidate_counts["retarded_reciprocal"] >= args.min_complex_seeds
        and controls_bounded
    )
    operational = bool(
        shape_counts["retarded_reciprocal"] >= args.min_complex_seeds
        and response_counts["retarded_reciprocal"] >= args.min_complex_seeds
        and mediator_counts["retarded_reciprocal"] >= args.min_complex_seeds
    )
    if retarded_candidate:
        classification = "retarded reciprocal complex-mode candidate"
    elif operational:
        classification = "retarded channel operational; complex-mode null"
    else:
        classification = "inconclusive: mediator, response, or shape gate failed"

    runtime_seconds = time.perf_counter() - started_at
    payload = {
        "schema": "emergenz-knoten.retarded-reciprocal-full-knot-gate",
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
            "correlation_length": correlation_length,
            "mediator_readout_position": readout_position,
            "nominal_front_time_memory_times": readout_position / mediator.wave_speed,
            "courant_number": mediator.wave_speed * grid.time_step / grid.spacing,
            "static_readout_gain": static_gain,
            "source_normalization": source_normalization,
            "second_state_rotation": rotation,
        },
        "mediator_grid": asdict(grid),
        "mediator": asdict(mediator),
        "direct_analytic_relative_mode": {
            "multipliers": direct_analytic.relative_multipliers,
            "discriminant": direct_analytic.relative_discriminant,
            "is_complex": direct_analytic.relative_is_complex,
            "is_stable": direct_analytic.relative_is_stable,
        },
        "thresholds": thresholds,
        "rows": rows,
        "gate": {
            "candidate_seed_counts": candidate_counts,
            "shape_seed_counts": shape_counts,
            "response_seed_counts": response_counts,
            "mediator_seed_counts": mediator_counts,
            "controls_bounded_pass": controls_bounded,
            "retarded_reciprocal_complex_candidate_pass": retarded_candidate,
            "operational_reconciliation_pass": operational,
            "classification": classification,
        },
    }
    return _jsonable(payload), traces


def _plot(payload: dict[str, Any], traces: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    alpha = float(payload["config"]["alpha"])
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.6))
    for condition_index, condition in enumerate(RETARDED_RECIPROCAL_CONDITIONS):
        for trace in traces:
            axes[0, 0].plot(
                trace["sample_steps"] * alpha,
                trace["pair_distances_r"][:, condition_index],
                color=CONDITION_COLORS[condition],
                alpha=0.22,
                linewidth=0.7,
            )
        stacked = np.vstack(
            [trace["pair_distances_r"][:, condition_index] for trace in traces]
        )
        axes[0, 0].plot(
            traces[0]["sample_steps"] * alpha,
            np.median(stacked, axis=0),
            color=CONDITION_COLORS[condition],
            linewidth=1.8,
            label=condition,
        )
    axes[0, 0].set(
        xlabel="continuation / memory times", ylabel="memory-centre separation / R"
    )
    axes[0, 0].legend(fontsize=7)
    axes[0, 0].grid(alpha=0.25)

    representative = traces[0]
    retarded_index = 3
    times = representative["sample_steps"] * alpha
    axes[0, 1].plot(
        times,
        representative["relative_positions_axis_r"][:, retarded_index],
        label="visible relative",
        color="#009E73",
    )
    axes[0, 1].plot(
        times,
        representative["relative_centers_axis_r"][:, retarded_index],
        label="memory relative",
        color="#CC79A7",
    )
    axes[0, 1].set(
        xlabel="continuation / memory times",
        ylabel="initial-axis coordinate / R",
        title=f"retarded reciprocal, future seed {representative['future_seed']}",
    )
    axes[0, 1].legend(fontsize=8)
    axes[0, 1].grid(alpha=0.25)

    angle = np.linspace(0.0, 2.0 * np.pi, 300)
    axes[1, 0].plot(np.cos(angle), np.sin(angle), color="#999999", linewidth=1)
    for condition in RETARDED_RECIPROCAL_CONDITIONS:
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
            s=16,
            alpha=0.6,
            color=CONDITION_COLORS[condition],
            label=condition,
        )
    axes[1, 0].axhline(0.0, color="#bbbbbb", linewidth=0.8)
    axes[1, 0].set_aspect("equal", adjustable="box")
    axes[1, 0].set(
        xlabel="Re multiplier",
        ylabel="Im multiplier",
        title="observable segmentwise mode fits",
    )
    axes[1, 0].legend(fontsize=7)
    axes[1, 0].grid(alpha=0.2)

    input_trace = representative["mediator_input_axis"]
    output_trace = representative["mediator_readout_axis"]
    input_scale = max(float(np.std(input_trace)), np.finfo(float).tiny)
    output_scale = max(float(np.std(output_trace)), np.finfo(float).tiny)
    axes[1, 1].plot(
        times,
        input_trace / input_scale,
        label="input / std",
        color="#0072B2",
        alpha=0.75,
    )
    axes[1, 1].plot(
        times,
        output_trace / output_scale,
        label="readout / std",
        color="#009E73",
        alpha=0.75,
    )
    axes[1, 1].set(
        xlabel="continuation / memory times",
        ylabel="standardized channel signal",
        title="fixed-axis Telegraph channel",
    )
    axes[1, 1].legend(fontsize=8)
    axes[1, 1].grid(alpha=0.25)

    fig.suptitle("P3.2 fixed-Telegraph reciprocal full-knot gate")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    gate = payload["gate"]
    raw_complex_total = sum(
        bool(segment["is_complex"])
        for row in payload["rows"]
        for condition in RETARDED_RECIPROCAL_CONDITIONS
        for segment in row["conditions"][condition]["mode_segments"]
    )
    segment_total = (
        len(payload["rows"])
        * len(RETARDED_RECIPROCAL_CONDITIONS)
        * int(payload["parameters"]["segments"])
    )
    final_ranges = {
        condition: (
            min(
                row["conditions"][condition]["final_pair_distance_r"]
                for row in payload["rows"]
            ),
            max(
                row["conditions"][condition]["final_pair_distance_r"]
                for row in payload["rows"]
            ),
        )
        for condition in ("instantaneous_reciprocal", "retarded_reciprocal")
    }
    derived = payload["derived"]
    parameters = payload["parameters"]
    direct = payload["direct_analytic_relative_mode"]
    lines = [
        "# P3.2 retarded reciprocal full-knot gate",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Question",
        "",
        "Does the already fixed scalar reciprocal readout acquire a stable,",
        "control-separated complex observable relative mode when it is passed",
        "through one preregistered local Telegraph channel?",
        "",
        "## Fixed mechanism",
        "",
        f"- mature d={payload['config']['dim']} checkpoint at N={payload['checkpoint_update_index']:,}, formation seed {payload['formation_seed']};",
        f"- lambda={payload['config']['alpha']:.4g}, direct P3.1 gain c={parameters['cross_gain']:.4g}, cross_eta={derived['cross_eta']:.7g};",
        f"- initial pair distance {parameters['distance_ratio']:.3g} R; fixed channel correlation length {parameters['correlation_length_r']:.3g} R and relaxation time {parameters['relaxation_memory_times']:.3g} memory times;",
        f"- grid spacing {parameters['grid_spacing_r']:.3g} R, Courant number {derived['courant_number']:.4g}, nominal r/v time {derived['nominal_front_time_memory_times']:.3g} memory times;",
        "- the finite grid axis and target readout position remain fixed during each continuation; no moving-grid phase is introduced;",
        "- the mediator input is still the target-specific instantaneous cross-gradient; only its transport/filter state is local, so this is not a fully local source-field theory;",
        f"- the discrete DC readout is solved exactly and normalized to unity (raw gain {derived['static_readout_gain']:.7g}); no knot-response calibration or cross-gain retuning is performed;",
        f"- {len(payload['rows'])} common-noise future seeds, {parameters['updates']:,} updates = {derived['continuation_memory_times']:.1f} memory times, first {derived['analysis_start_memory_times']:.1f} excluded.",
        "",
        "The arms are channel-off, the exact instantaneous reciprocal P3.1 control,",
        "retarded one-way, and retarded reciprocal. Unit tests require the direct",
        "control to be bitwise identical to the existing P3.1 implementation.",
        "",
        "## Preregistered gate",
        "",
        "The primary observable remains the fitted 2 x 2 `(x_-, m_-)` map. Complex",
        "internal Telegraph poles are inserted by construction and cannot establish",
        "a knot mode. A seed needs stable non-real fits in at least",
        f"{parameters['min_complex_segments']}/{parameters['segments']} segments, frequency at least {parameters['frequency_min_per_memory_time']:.3g} per memory time, phase coherence at least {parameters['phase_coherence_min']:.3g}, and registered fit/identity/shape bounds. The candidate needs {parameters['min_complex_seeds']}/{len(payload['rows'])} reciprocal seeds and at most {parameters['max_control_complex_seeds']} in every control.",
        "",
        f"The direct local prediction remains real: discriminant {direct['discriminant']:.6g}, multipliers {direct['multipliers']}.",
        "",
        "## Result",
        "",
        f"Classification: **{gate['classification']}**.",
        "",
        "- candidate seeds off / direct / retarded one-way / retarded reciprocal: "
        + " / ".join(
            str(gate["candidate_seed_counts"][name])
            for name in RETARDED_RECIPROCAL_CONDITIONS
        )
        + ";",
        f"- retarded reciprocal mediator detected: {gate['mediator_seed_counts']['retarded_reciprocal']}/{len(payload['rows'])};",
        f"- retarded reciprocal response detected: {gate['response_seed_counts']['retarded_reciprocal']}/{len(payload['rows'])};",
        f"- retarded reciprocal shape bounded/coherent: {gate['shape_seed_counts']['retarded_reciprocal']}/{len(payload['rows'])};",
        f"- control-separated complex candidate: {gate['retarded_reciprocal_complex_candidate_pass']}.",
        f"- raw non-real segment fits: {raw_complex_total}/{segment_total};",
        f"- final distance/R, direct: {final_ranges['instantaneous_reciprocal'][0]:.4g}..{final_ranges['instantaneous_reciprocal'][1]:.4g};",
        f"- final distance/R, retarded reciprocal: {final_ranges['retarded_reciprocal'][0]:.4g}..{final_ranges['retarded_reciprocal'][1]:.4g};",
        "  the delay weakens or postpones binding but does not create an observable rotation.",
        "",
        f"![P3.2 retarded reciprocal gate]({_relative_from(report, figure)})",
        "",
        "## Seed rows",
        "",
        "| future seed | off | direct | retarded one-way | retarded reciprocal | mediator RMS | final distance/R | candidate |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |",
    ]
    for row in payload["rows"]:
        conditions = row["conditions"]
        primary = conditions["retarded_reciprocal"]
        lines.append(
            f"| {row['future_seed']} | "
            f"{conditions['channel_off']['mode_summary']['meaningful_complex_segments']} | "
            f"{conditions['instantaneous_reciprocal']['mode_summary']['meaningful_complex_segments']} | "
            f"{conditions['retarded_one_way']['mode_summary']['meaningful_complex_segments']} | "
            f"{primary['mode_summary']['meaningful_complex_segments']} | "
            f"{primary['mediator_readout_rms']:.3e} | "
            f"{primary['final_pair_distance_r']:.4g} | "
            f"{primary['candidate_pass']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This is a mechanism test of one inserted retarded channel, not discovery",
            "of a field law. Its input remains a target-specific cross-gradient from",
            "the current source memory. Only the transport/filter update is local; a",
            "source-local emission field has not been derived.",
            "",
            "The fixed one-dimensional relation axis carries vectors in a supplied",
            "d=3 ambient state. Its finite-difference stencil has a numerical grid",
            "cone; this proves no continuum causal speed. No spatial rotation, d=3",
            "selection, spin, charge, photon, particle, Lorentz, QFT, or Standard-Model claim follows.",
            "",
            f"The {len(payload['rows'])} future-noise paths all continue one formation checkpoint. They",
            "test pathwise robustness, not basin-to-basin reproducibility.",
            "",
            "## Reproducibility",
            "",
            f"- checkpoint: `{payload['checkpoint']}`;",
            f"- git revision: `{payload['git_revision']}`;",
            f"- git status at start: `{'clean' if not payload['git_status'] else payload['git_status']}`;",
            f"- runtime: `{payload['runtime_seconds']:.3f} s`;",
            "- command: `python experiments/current/memory/synchronization/retarded_reciprocal_full_knot_gate.py`;",
            "- machine-readable summary: "
            f"[{Path(payload['parameters']['summary_json']).name}]"
            f"({_relative_from(report, _resolve(Path(payload['parameters']['summary_json'])))}).",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    payload, traces = run_gate(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    _plot(payload, traces, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")
    summary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload["gate"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
