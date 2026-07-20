"""One-way dynamic-source pilot with relational orbital controls."""

from __future__ import annotations

import argparse
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
    calibrate_frozen_source_cross_eta,
    load_finite_memory_checkpoint,
    memory_shape_tensor,
    one_way_coupled_response,
    relative_orbital_observables,
)


DEFAULT_CHECKPOINT = Path(
    "data/processed/reference_states/"
    "scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/"
    "scalar_Aatt35_d3_seed1_N100000000.npz"
)


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(item < 1 for item in values):
        raise argparse.ArgumentTypeError("expected positive comma-separated integers")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Continue one dynamic source and paired scalar target controls."
    )
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--steps", type=int, default=20_000)
    parser.add_argument("--sample-every", type=int, default=20)
    parser.add_argument("--continuation-seeds", type=_parse_int_list, default=[1, 2, 3, 4, 5])
    parser.add_argument("--separation-sigma-rep", type=float, default=1.0)
    parser.add_argument("--source-launch-sigma-rep", type=float, default=0.0)
    parser.add_argument("--source-launch-memory-times", type=float, default=10.0)
    parser.add_argument("--source-launch-axis", type=int, default=1)
    parser.add_argument("--response-fraction-per-memory", type=float, default=0.03)
    parser.add_argument("--max-ac-memory-times", type=float, default=50.0)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/one_way_dynamic_source_pilot_2026-07-20.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/one_way_dynamic_source_pilot_2026-07-20.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/one_way_dynamic_source_pilot_2026-07-20.png"
        ),
    )
    return parser.parse_args()


def _validate_args(args: argparse.Namespace) -> None:
    if args.steps < 100 or args.sample_every < 1:
        raise SystemExit("steps must be >=100 and sample-every positive")
    if args.steps % args.sample_every != 0:
        raise SystemExit("steps must be divisible by sample-every")
    if args.separation_sigma_rep <= 0.0:
        raise SystemExit("separation-sigma-rep must be positive")
    if args.source_launch_sigma_rep < 0.0:
        raise SystemExit("source-launch-sigma-rep must be non-negative")
    if args.source_launch_memory_times <= 0.0:
        raise SystemExit("source-launch-memory-times must be positive")
    if args.source_launch_axis < 0:
        raise SystemExit("source-launch-axis must be non-negative")
    if args.response_fraction_per_memory <= 0.0:
        raise SystemExit("response-fraction-per-memory must be positive")
    if args.max_ac_memory_times <= 0.0:
        raise SystemExit("max-ac-memory-times must be positive")


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


def _angular_components(tensors: np.ndarray) -> np.ndarray:
    dim = tensors.shape[1]
    return np.column_stack(
        [tensors[:, row, col] for row in range(dim) for col in range(row + 1, dim)]
    )


def _direction_autocorrelation(
    components: np.ndarray,
    *,
    max_lag: int,
) -> np.ndarray:
    values = np.asarray(components, dtype=float)
    correlations = np.empty(max_lag + 1, dtype=float)
    correlations[0] = 1.0
    for lag in range(1, max_lag + 1):
        left = values[:-lag]
        right = values[lag:]
        numerator = float(np.mean(np.sum(left * right, axis=1)))
        denominator = math.sqrt(
            float(np.mean(np.sum(left * left, axis=1)))
            * float(np.mean(np.sum(right * right, axis=1)))
        )
        correlations[lag] = numerator / denominator if denominator > 0.0 else 0.0
    return correlations


def _orbital_metrics(
    target_centers: np.ndarray,
    source_centers: np.ndarray,
    sample_steps: np.ndarray,
    *,
    alpha: float,
    max_ac_memory_times: float,
) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    orbital = relative_orbital_observables(
        target_centers,
        source_centers,
        sample_steps,
    )
    components = _angular_components(orbital.angular_momentum_tensors)
    norms = np.linalg.norm(components, axis=1)
    mean_norm = float(np.mean(norms))
    coherence = (
        float(np.linalg.norm(np.mean(components, axis=0)) / mean_norm)
        if mean_norm > 0.0
        else 0.0
    )
    speed = np.linalg.norm(orbital.relative_velocities, axis=1)
    tangential_fraction = np.divide(
        orbital.tangential_speeds,
        speed,
        out=np.zeros_like(speed),
        where=speed > 0.0,
    )
    midpoint = 0.5 * (
        orbital.relative_centers[1:] + orbital.relative_centers[:-1]
    )
    radius2 = np.sum(midpoint * midpoint, axis=1)
    angular_speed = np.divide(
        orbital.angular_momentum_norms,
        radius2,
        out=np.zeros_like(radius2),
        where=radius2 > 0.0,
    )
    memory_times_per_sample = float(np.median(np.diff(sample_steps))) * alpha
    max_lag = min(
        len(components) - 1,
        max(1, int(max_ac_memory_times / memory_times_per_sample)),
    )
    correlation = _direction_autocorrelation(components, max_lag=max_lag)
    crossings = np.flatnonzero(correlation <= math.exp(-1.0))
    if crossings.size:
        dephasing_memory_times = float(crossings[0] * memory_times_per_sample)
        censored = False
    else:
        dephasing_memory_times = float(max_lag * memory_times_per_sample)
        censored = True
    metrics = {
        "angular_momentum_norm_median": float(np.median(norms)),
        "angular_orientation_coherence": coherence,
        "tangential_fraction_median": float(np.median(tangential_fraction)),
        "angular_speed_median_per_memory_time": float(
            np.median(angular_speed) / alpha
        ),
        "dephasing_memory_times": dephasing_memory_times,
        "dephasing_censored": censored,
    }
    traces = {
        "angular_momentum_norm": norms,
        "angular_correlation": correlation,
        "tangential_fraction": tangential_fraction,
    }
    return metrics, traces


def _run_seed(
    *,
    checkpoint: Any,
    continuation_seed: int,
    source_launch_sigma_rep: float,
    source_launch_memory_times: float,
    source_launch_axis: int,
    steps: int,
    sample_every: int,
    source_offset: np.ndarray,
    cross_eta: float,
    max_ac_memory_times: float,
) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    config = checkpoint.config
    target_noise = np.random.default_rng(10_000 + continuation_seed).normal(
        size=(steps, config.dim)
    )
    source_noise = np.random.default_rng(20_000 + continuation_seed).normal(
        size=(steps, config.dim)
    )
    sample_steps = np.arange(0, steps + 1, sample_every, dtype=int)
    if source_launch_axis >= config.dim:
        raise ValueError("source launch axis must be smaller than dimension")
    launch_steps = min(
        steps,
        max(1, round(source_launch_memory_times / config.alpha)),
    )
    source_drive = np.zeros((steps, config.dim), dtype=float)
    if source_launch_sigma_rep > 0.0:
        source_drive[:launch_steps, source_launch_axis] = (
            source_launch_sigma_rep
            * config.sigma_rep
            / launch_steps
        )
    response = one_way_coupled_response(
        checkpoint.state,
        checkpoint.state,
        config,
        source_center_offset=source_offset,
        target_noise=target_noise,
        source_noise=source_noise,
        source_drive=source_drive,
        sample_steps=sample_steps,
        cross_eta=cross_eta,
    )
    if source_launch_sigma_rep > 0.0:
        launch_control = one_way_coupled_response(
            checkpoint.state,
            checkpoint.state,
            config,
            source_center_offset=source_offset,
            target_noise=target_noise,
            source_noise=source_noise,
            sample_steps=sample_steps,
            cross_eta=cross_eta,
        )
    else:
        launch_control = response
    condition_index = {
        name: index for index, name in enumerate(response.target_conditions)
    }
    frozen_source_centers = np.repeat(
        response.source_memory_centers[:1],
        len(response.sample_steps),
        axis=0,
    )
    orbital_metrics: dict[str, dict[str, Any]] = {}
    orbital_traces: dict[str, dict[str, np.ndarray]] = {}
    for condition in response.target_conditions:
        source_centers = (
            frozen_source_centers
            if condition == "frozen_source"
            else response.source_memory_centers
        )
        metrics, traces = _orbital_metrics(
            response.target_memory_centers[:, condition_index[condition]],
            source_centers,
            response.sample_steps,
            alpha=config.alpha,
            max_ac_memory_times=max_ac_memory_times,
        )
        orbital_metrics[condition] = metrics
        orbital_traces[condition] = traces

    initial_radius = float(np.sqrt(np.trace(memory_shape_tensor(checkpoint.state))))
    dynamic = condition_index["dynamic_source"]
    frozen = condition_index["frozen_source"]
    free = condition_index["free"]
    eta_zero = condition_index["eta_zero_dynamic"]
    source_displacement = float(
        np.linalg.norm(
            response.source_memory_centers[-1] - response.source_memory_centers[0]
        )
        / initial_radius
    )
    launch_source_displacement = float(
        np.linalg.norm(
            response.source_memory_centers[-1]
            - launch_control.source_memory_centers[-1]
        )
        / initial_radius
    )
    launch_target_response = float(
        np.linalg.norm(
            response.target_memory_centers[-1, dynamic]
            - launch_control.target_memory_centers[-1, dynamic]
        )
        / initial_radius
    )
    launch_source_radius_effect = float(
        np.max(
            np.abs(
                response.source_radius_ratios
                - launch_control.source_radius_ratios
            )
        )
    )
    dynamic_frozen = float(
        np.linalg.norm(
            response.target_memory_centers[-1, dynamic]
            - response.target_memory_centers[-1, frozen]
        )
        / initial_radius
    )
    dynamic_free = float(
        np.linalg.norm(
            response.target_memory_centers[-1, dynamic]
            - response.target_memory_centers[-1, free]
        )
        / initial_radius
    )
    dynamic_separation = np.linalg.norm(
        response.target_memory_centers[:, dynamic]
        - response.source_memory_centers,
        axis=1,
    )
    active_radius_disturbance = float(
        np.max(
            np.abs(
                response.target_radius_ratios[:, [dynamic, frozen]]
                - response.target_radius_ratios[:, free, None]
            )
        )
    )
    eta_zero_radius_disturbance = float(
        np.max(
            np.abs(
                response.target_radius_ratios[:, eta_zero]
                - response.target_radius_ratios[:, free]
            )
        )
    )
    row = {
        "continuation_seed": continuation_seed,
        "source_displacement_radii": source_displacement,
        "dynamic_minus_frozen_final_radii": dynamic_frozen,
        "dynamic_minus_free_final_radii": dynamic_free,
        "dynamic_separation_initial": float(dynamic_separation[0]),
        "dynamic_separation_final": float(dynamic_separation[-1]),
        "dynamic_separation_ratio": float(
            dynamic_separation[-1] / dynamic_separation[0]
        ),
        "source_launch_steps": launch_steps,
        "source_launch_axis": source_launch_axis,
        "source_launch_sigma_rep": source_launch_sigma_rep,
        "launch_specific_source_displacement_radii": launch_source_displacement,
        "launch_specific_target_response_radii": launch_target_response,
        "max_launch_specific_source_radius_effect": launch_source_radius_effect,
        "max_source_radius_disturbance": float(
            np.max(np.abs(response.source_radius_ratios - 1.0))
        ),
        "max_active_target_radius_disturbance": active_radius_disturbance,
        "max_eta_zero_radius_disturbance": eta_zero_radius_disturbance,
        "orbital_metrics": orbital_metrics,
    }
    trace = {
        "sample_steps": response.sample_steps,
        "source_centers": response.source_memory_centers,
        "target_centers": response.target_memory_centers,
        "target_radius_ratios": response.target_radius_ratios,
        "dynamic_separation": dynamic_separation,
        "dynamic_angular_momentum_norm": orbital_traces["dynamic_source"][
            "angular_momentum_norm"
        ],
        "free_angular_momentum_norm": orbital_traces["free"][
            "angular_momentum_norm"
        ],
    }
    return row, trace


def _null_error(
    checkpoint: Any,
    *,
    source_offset: np.ndarray,
    sample_every: int,
) -> float:
    steps = 2 * sample_every
    dim = checkpoint.config.dim
    noise = np.random.default_rng(991).normal(size=(steps, dim))
    response = one_way_coupled_response(
        checkpoint.state,
        checkpoint.state,
        checkpoint.config,
        source_center_offset=source_offset,
        target_noise=noise,
        source_noise=-noise,
        sample_steps=[0, sample_every, steps],
        cross_eta=0.0,
    )
    dynamic, frozen, free, _eta_zero = range(4)
    return float(
        max(
            np.max(
                np.abs(
                    response.target_positions[:, dynamic]
                    - response.target_positions[:, free]
                )
            ),
            np.max(
                np.abs(
                    response.target_positions[:, frozen]
                    - response.target_positions[:, free]
                )
            ),
        )
    )


def _median(rows: list[dict[str, Any]], key: str) -> float:
    return float(np.median([float(row[key]) for row in rows]))


def _gate(rows: list[dict[str, Any]], null_error: float) -> dict[str, Any]:
    dynamic_metrics = [row["orbital_metrics"]["dynamic_source"] for row in rows]
    free_metrics = [row["orbital_metrics"]["free"] for row in rows]
    coherence = float(
        np.median([row["angular_orientation_coherence"] for row in dynamic_metrics])
    )
    free_coherence = float(
        np.median([row["angular_orientation_coherence"] for row in free_metrics])
    )
    tangential = float(
        np.median([row["tangential_fraction_median"] for row in dynamic_metrics])
    )
    dephasing = float(
        np.median([row["dephasing_memory_times"] for row in dynamic_metrics])
    )
    dynamic_source_readout = bool(
        _median(rows, "dynamic_minus_frozen_final_radii") > 0.1
    )
    launch_source_displacement = _median(
        rows, "launch_specific_source_displacement_radii"
    )
    launch_target_response = _median(rows, "launch_specific_target_response_radii")
    launch_specific_readout = bool(launch_target_response > 0.1)
    launch_active = any(float(row["source_launch_sigma_rep"]) > 0.0 for row in rows)
    interaction_readout = (
        launch_specific_readout if launch_active else dynamic_source_readout
    )
    nondestructive = bool(
        max(float(row["max_active_target_radius_disturbance"]) for row in rows) < 0.1
    )
    source_nondestructive = bool(
        max(float(row["max_launch_specific_source_radius_effect"]) for row in rows) < 0.1
    )
    phase_candidate = bool(
        interaction_readout
        and nondestructive
        and source_nondestructive
        and coherence >= 0.5
        and coherence >= free_coherence + 0.2
        and tangential >= 0.5
        and dephasing >= 10.0
    )
    return {
        "zero_cross_identity_pass": null_error == 0.0,
        "zero_cross_max_abs_error": null_error,
        "dynamic_source_readout_pass": dynamic_source_readout,
        "launch_specific_target_readout_pass": launch_specific_readout,
        "launch_specific_target_response_radii_median": launch_target_response,
        "launch_specific_source_displacement_radii_median": launch_source_displacement,
        "interaction_readout_pass": interaction_readout,
        "nondestructive_target_pass": nondestructive,
        "dynamic_angular_orientation_coherence_median": coherence,
        "free_angular_orientation_coherence_median": free_coherence,
        "dynamic_tangential_fraction_median": tangential,
        "dynamic_dephasing_memory_times_median": dephasing,
        "relational_phase_candidate_pass": phase_candidate,
        "nondestructive_source_pass": source_nondestructive,
    }


def run_pilot(args: argparse.Namespace) -> tuple[dict[str, Any], list[dict[str, np.ndarray]]]:
    checkpoint = load_finite_memory_checkpoint(_resolve(args.checkpoint))
    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    config = checkpoint.config
    source_offset = np.zeros(config.dim, dtype=float)
    source_offset[0] = args.separation_sigma_rep * config.sigma_rep
    pulse_steps = max(1, round(1.0 / config.alpha))
    calibration = calibrate_frozen_source_cross_eta(
        checkpoint.state,
        checkpoint.state,
        config,
        source_center_offset=source_offset,
        response_fraction=args.response_fraction_per_memory,
        pulse_steps=pulse_steps,
    )
    rows = []
    traces = []
    for seed in args.continuation_seeds:
        row, trace = _run_seed(
            checkpoint=checkpoint,
            continuation_seed=seed,
            source_launch_sigma_rep=args.source_launch_sigma_rep,
            source_launch_memory_times=args.source_launch_memory_times,
            source_launch_axis=args.source_launch_axis,
            steps=args.steps,
            sample_every=args.sample_every,
            source_offset=source_offset,
            cross_eta=calibration.cross_eta,
            max_ac_memory_times=args.max_ac_memory_times,
        )
        rows.append(row)
        traces.append(trace)
    null_error = _null_error(
        checkpoint,
        source_offset=source_offset,
        sample_every=args.sample_every,
    )
    payload = {
        "description": "One-way dynamic scalar-source continuation with paired controls.",
        "created_utc": datetime.now(UTC).isoformat(),
        "git_revision": git_revision,
        "git_status": git_status,
        "checkpoint": str(args.checkpoint).replace("\\", "/"),
        "formation_seed": checkpoint.formation_seed,
        "model": {
            "dim": config.dim,
            "alpha": config.alpha,
            "epsilon": config.epsilon,
            "eta": config.eta,
        },
        "parameters": {
            key: value
            for key, value in vars(args).items()
            if key not in {"report", "summary_json", "figure", "checkpoint"}
        },
        "calibration": {
            "cross_eta": calibration.cross_eta,
            "pulse_steps_reference": pulse_steps,
            "response_fraction_per_memory": args.response_fraction_per_memory,
            "initial_target_radius": calibration.target_radius,
            "source_center_offset": source_offset.tolist(),
        },
        "launch": {
            "source_launch_sigma_rep": args.source_launch_sigma_rep,
            "source_launch_memory_times": args.source_launch_memory_times,
            "source_launch_axis": args.source_launch_axis,
        },
        "rows": rows,
        "gate": _gate(rows, null_error),
    }
    return payload, traces


def _plot(payload: dict[str, Any], traces: list[dict[str, np.ndarray]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    alpha = float(payload["model"]["alpha"])
    fig = plt.figure(figsize=(12.0, 8.4))
    axis_3d = fig.add_subplot(2, 2, 1, projection="3d")
    first = traces[0]
    times = first["sample_steps"] * alpha
    source = first["source_centers"]
    targets = first["target_centers"]
    axis_3d.plot(*source[:, :3].T, color="black", label="source")
    for index, (label, color) in enumerate(
        (
            ("dynamic", "#0072B2"),
            ("frozen", "#D55E00"),
            ("free", "#009E73"),
        )
    ):
        axis_3d.plot(*targets[:, index, :3].T, color=color, label=label)
    axis_3d.set_xlabel("x0")
    axis_3d.set_ylabel("x1")
    axis_3d.set_zlabel("x2")
    axis_3d.legend(fontsize=7)
    axis_3d.set_title("seed 1 memory-centre paths")

    axis_sep = fig.add_subplot(2, 2, 2)
    for trace, row in zip(traces, payload["rows"], strict=True):
        axis_sep.plot(
            trace["sample_steps"] * alpha,
            trace["dynamic_separation"],
            label=f"seed {row['continuation_seed']}",
        )
    axis_sep.set_xlabel("memory times")
    axis_sep.set_ylabel("dynamic target-source separation")
    axis_sep.legend(fontsize=7)
    axis_sep.grid(alpha=0.25)

    axis_l = fig.add_subplot(2, 2, 3)
    dynamic = np.vstack([trace["dynamic_angular_momentum_norm"] for trace in traces])
    free = np.vstack([trace["free_angular_momentum_norm"] for trace in traces])
    axis_l.plot(times[1:], np.median(dynamic, axis=0), label="dynamic source")
    axis_l.plot(times[1:], np.median(free, axis=0), label="free control")
    axis_l.set_yscale("log")
    axis_l.set_xlabel("memory times")
    axis_l.set_ylabel("median |relative angular momentum|")
    axis_l.legend()
    axis_l.grid(alpha=0.25)

    axis_kpi = fig.add_subplot(2, 2, 4)
    gate = payload["gate"]
    labels = ["coherence", "free coherence", "tangential", "dephase / 10"]
    values = [
        gate["dynamic_angular_orientation_coherence_median"],
        gate["free_angular_orientation_coherence_median"],
        gate["dynamic_tangential_fraction_median"],
        gate["dynamic_dephasing_memory_times_median"] / 10.0,
    ]
    axis_kpi.bar(np.arange(len(labels)), values, color=["#0072B2", "#009E73", "#CC79A7", "#E69F00"])
    axis_kpi.axhline(0.5, color="#666666", linewidth=1)
    axis_kpi.set_xticks(np.arange(len(labels)), labels, rotation=25, ha="right")
    axis_kpi.set_ylabel("registered KPI")
    axis_kpi.grid(axis="y", alpha=0.25)

    fig.suptitle("One-way dynamic scalar source with paired controls")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    gate = payload["gate"]
    lines = [
        "# One-Way Dynamic Scalar-Source Pilot",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Question",
        "",
        "Does an autonomously moving scalar-memory source produce a relational",
        "translation or coherent orbital mode in a second knot beyond frozen-source",
        "and no-cross controls?",
        "",
        "## Design",
        "",
        "- One N=100M d=3 checkpoint is cloned into target and source.",
        "- The source evolves under self-memory and independent future noise.",
        f"- External source launch: {payload['launch']['source_launch_sigma_rep']:.3g} "
        f"sigma_rep over {payload['launch']['source_launch_memory_times']:.3g} memory times.",
        "- The launch is an imposed probe, not emergent source propulsion.",
        "- The source does not read the target.",
        "- Dynamic-source, frozen-source, free, and eta=0 target paths share target noise.",
        "- cross_eta is calibrated once to 0.03 target radii per memory time initially.",
        "- Continuation seeds sample future noise, not independent formation basins.",
        "",
        "## Registered gate",
        "",
        f"- Exact cross=0 identity: {gate['zero_cross_identity_pass']} "
        f"(max error {gate['zero_cross_max_abs_error']:.3e}).",
        f"- Dynamic-versus-frozen source readout above 0.1 target radius: "
        f"{gate['dynamic_source_readout_pass']}.",
        f"- Launch-specific source displacement: "
        f"{gate['launch_specific_source_displacement_radii_median']:.3f} knot radii.",
        f"- Launch-specific target readout above 0.1 target radius: "
        f"{gate['launch_specific_target_readout_pass']} "
        f"({gate['launch_specific_target_response_radii_median']:.3e} radii).",
        f"- Target radius disturbance below 10 percent: "
        f"{gate['nondestructive_target_pass']}.",
        f"- Additional source-radius disturbance versus the paired unlaunched path "
        f"below 10 percent: {gate['nondestructive_source_pass']}.",
        f"- Median dynamic angular coherence: "
        f"{gate['dynamic_angular_orientation_coherence_median']:.3f} "
        f"(free {gate['free_angular_orientation_coherence_median']:.3f}).",
        f"- Median tangential fraction: "
        f"{gate['dynamic_tangential_fraction_median']:.3f}.",
        f"- Median dephasing time: "
        f"{gate['dynamic_dephasing_memory_times_median']:.3f} memory times.",
        f"- Relational phase candidate: {gate['relational_phase_candidate_pass']}.",
        "",
        f"![One-way dynamic source]({_relative(report, figure)})",
        "",
        "## Seed rows",
        "",
        "| continuation seed | source displacement / R | launch source / R | "
        "launch target / R | dynamic-frozen / R | max source radius effect | "
        "max target radius disturbance |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['continuation_seed']} | {row['source_displacement_radii']:.3f} | "
            f"{row['launch_specific_source_displacement_radii']:.3f} | "
            f"{row['launch_specific_target_response_radii']:.3e} | "
            f"{row['dynamic_minus_frozen_final_radii']:.3f} | "
            f"{row['max_launch_specific_source_radius_effect']:.3e} | "
            f"{row['max_active_target_radius_disturbance']:.3e} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- This is an instantaneous unsigned scalar cross-channel.",
            "- A moving-source response is not finite-speed propagation.",
            "- Continuation seeds from one checkpoint are not independent knot types.",
            "- Nonzero angular momentum amplitude without orientation coherence and",
            "  control separation is stochastic bending, not spin or orbit.",
            "- No charge, photon, synchronization, or Standard-Model claim follows.",
            "",
            "## Reproduction",
            "",
            "    python experiments/current/memory/synchronization/one_way_dynamic_source_pilot.py",
            "",
            f"Git revision: {payload['git_revision']}.",
            f"Git status at generation: {payload['git_status'] or 'clean'}.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    _validate_args(args)
    payload, traces = run_pilot(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    _plot(payload, traces, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")
    summary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload["gate"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

