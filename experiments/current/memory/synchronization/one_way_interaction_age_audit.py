"""Long interaction-age audit for a mature target under one dynamic source."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
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
    normalized_shape_spectra,
    one_way_coupled_response,
    shape_stationarity_diagnostics,
)


DEFAULT_CHECKPOINT = Path(
    "data/processed/reference_states/"
    "scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/"
    "scalar_Aatt35_d3_seed1_N100000000.npz"
)
DEFAULT_EVALUATIONS = [20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(item < 1 for item in values):
        raise argparse.ArgumentTypeError("expected positive comma-separated integers")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit target adaptation up to one million continuation updates."
    )
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--steps", type=int, default=1_000_000)
    parser.add_argument("--sample-every", type=int, default=200)
    parser.add_argument(
        "--continuation-seeds", type=_parse_int_list, default=[1, 2, 3, 4, 5]
    )
    parser.add_argument(
        "--evaluation-updates", type=_parse_int_list, default=DEFAULT_EVALUATIONS
    )
    parser.add_argument("--window-memory-times", type=float, default=50.0)
    parser.add_argument("--separation-sigma-rep", type=float, default=1.0)
    parser.add_argument("--response-fraction-per-memory", type=float, default=0.03)
    parser.add_argument("--min-seed-fraction", type=float, default=0.8)
    parser.add_argument("--plateau-radius-log-limit", type=float, default=0.05)
    parser.add_argument("--plateau-dimension-limit", type=float, default=0.05)
    parser.add_argument("--plateau-spectrum-limit", type=float, default=0.02)
    parser.add_argument("--modified-radius-log-min", type=float, default=0.10)
    parser.add_argument("--modified-dimension-min", type=float, default=0.10)
    parser.add_argument("--modified-spectrum-min", type=float, default=0.05)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/one_way_interaction_age_N1M_2026-07-21.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/one_way_interaction_age_N1M_2026-07-21.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/one_way_interaction_age_N1M_2026-07-21.png"
        ),
    )
    return parser.parse_args()


def _validate_args(args: argparse.Namespace) -> None:
    evaluations = sorted(set(args.evaluation_updates))
    if args.steps < 1 or args.sample_every < 1 or args.steps % args.sample_every:
        raise SystemExit("steps must be positive and divisible by sample-every")
    if evaluations[-1] != args.steps:
        raise SystemExit("evaluation-updates must include steps as the final value")
    if any(value % args.sample_every for value in evaluations):
        raise SystemExit("all evaluation updates must be divisible by sample-every")
    if args.window_memory_times <= 0.0 or args.separation_sigma_rep <= 0.0:
        raise SystemExit("window and separation must be positive")
    if not 0.0 < args.min_seed_fraction <= 1.0:
        raise SystemExit("min-seed-fraction must be in (0, 1]")
    threshold_values = (
        args.plateau_radius_log_limit,
        args.plateau_dimension_limit,
        args.plateau_spectrum_limit,
        args.modified_radius_log_min,
        args.modified_dimension_min,
        args.modified_spectrum_min,
    )
    if min(threshold_values) <= 0.0:
        raise SystemExit("gate thresholds must be positive")
    args.evaluation_updates = evaluations


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


def _shape_features(shape_tensors: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    spectra = normalized_shape_spectra(shape_tensors)
    effective_dimension = np.reciprocal(np.sum(spectra * spectra, axis=1))
    roundness = np.sqrt(
        np.divide(
            spectra[:, 0],
            spectra[:, -1],
            out=np.zeros(len(spectra), dtype=float),
            where=spectra[:, -1] > 0.0,
        )
    )
    return effective_dimension, roundness


def _window_metrics(
    response: Any,
    *,
    evaluation_update: int,
    window_updates: int,
    initial_radius: float,
) -> dict[str, float]:
    steps = response.sample_steps
    mask = (steps > max(0, evaluation_update - window_updates)) & (
        steps <= evaluation_update
    )
    if np.count_nonzero(mask) < 4:
        raise ValueError("each evaluation window must contain at least four samples")
    dynamic, frozen, free, eta_zero = range(4)
    target_centers = response.target_memory_centers[mask]
    target_radii = response.target_radius_ratios[mask]
    target_tensors = response.target_shape_tensors[mask]
    dynamic_spectra = normalized_shape_spectra(target_tensors[:, dynamic])
    free_spectra = normalized_shape_spectra(target_tensors[:, free])
    spectrum_distance = 0.5 * np.sum(np.abs(dynamic_spectra - free_spectra), axis=1)
    dynamic_dimension, dynamic_roundness = _shape_features(target_tensors[:, dynamic])
    free_dimension, free_roundness = _shape_features(target_tensors[:, free])
    radius_ratio = target_radii[:, dynamic] / target_radii[:, free]
    radius_factor = np.maximum(radius_ratio, np.reciprocal(radius_ratio))
    source_centers = response.source_memory_centers[mask]
    separation = np.linalg.norm(target_centers[:, dynamic] - source_centers, axis=1)
    return {
        "dynamic_minus_free_center_radii": float(
            np.median(
                np.linalg.norm(
                    target_centers[:, dynamic] - target_centers[:, free], axis=1
                )
                / initial_radius
            )
        ),
        "dynamic_minus_frozen_center_radii": float(
            np.median(
                np.linalg.norm(
                    target_centers[:, dynamic] - target_centers[:, frozen], axis=1
                )
                / initial_radius
            )
        ),
        "dynamic_minus_eta_zero_center_radii": float(
            np.median(
                np.linalg.norm(
                    target_centers[:, dynamic] - target_centers[:, eta_zero], axis=1
                )
                / initial_radius
            )
        ),
        "dynamic_free_radius_ratio": float(np.median(radius_ratio)),
        "dynamic_free_max_radius_factor": float(np.max(radius_factor)),
        "dynamic_free_shape_spectrum_median": float(np.median(spectrum_distance)),
        "dynamic_free_shape_spectrum_q95": float(np.quantile(spectrum_distance, 0.95)),
        "dynamic_shape_dimension": float(np.median(dynamic_dimension)),
        "free_shape_dimension": float(np.median(free_dimension)),
        "dynamic_minus_free_shape_dimension": float(
            np.median(dynamic_dimension - free_dimension)
        ),
        "dynamic_roundness": float(np.median(dynamic_roundness)),
        "free_roundness": float(np.median(free_roundness)),
        "target_source_separation_sigma_rep": float(np.median(separation)),
    }


def _run_seed(
    checkpoint: Any,
    *,
    continuation_seed: int,
    steps: int,
    sample_every: int,
    evaluations: list[int],
    window_updates: int,
    source_offset: np.ndarray,
    cross_eta: float,
) -> dict[str, Any]:
    config = checkpoint.config
    target_noise = np.random.default_rng(10_000 + continuation_seed).normal(
        size=(steps, config.dim)
    )
    source_noise = np.random.default_rng(20_000 + continuation_seed).normal(
        size=(steps, config.dim)
    )
    sample_steps = np.arange(0, steps + 1, sample_every, dtype=int)
    started = time.perf_counter()
    response = one_way_coupled_response(
        checkpoint.state,
        checkpoint.state,
        config,
        source_center_offset=source_offset,
        target_noise=target_noise,
        source_noise=source_noise,
        sample_steps=sample_steps,
        cross_eta=cross_eta,
    )
    runtime_seconds = time.perf_counter() - started
    initial_radius = float(np.sqrt(np.trace(memory_shape_tensor(checkpoint.state))))
    stationarity_mask = sample_steps <= window_updates
    source_stationarity = shape_stationarity_diagnostics(
        response.source_radius_ratios[stationarity_mask],
        response.source_shape_tensors[stationarity_mask],
    )
    checkpoints = [
        {
            "evaluation_update": evaluation,
            **_window_metrics(
                response,
                evaluation_update=evaluation,
                window_updates=window_updates,
                initial_radius=initial_radius,
            ),
        }
        for evaluation in evaluations
    ]
    return {
        "continuation_seed": continuation_seed,
        "runtime_seconds": runtime_seconds,
        "source_stationarity": source_stationarity,
        "checkpoints": checkpoints,
    }


def _checkpoint_by_update(row: dict[str, Any], update: int) -> dict[str, Any]:
    return next(
        checkpoint
        for checkpoint in row["checkpoints"]
        if checkpoint["evaluation_update"] == update
    )


def _gate(rows: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    previous_update, final_update = args.evaluation_updates[-2:]
    plateau_by_seed = []
    modified_by_seed = []
    deltas = []
    for row in rows:
        previous = _checkpoint_by_update(row, previous_update)
        final = _checkpoint_by_update(row, final_update)
        radius_log_delta = abs(
            math.log(
                final["dynamic_free_radius_ratio"]
                / previous["dynamic_free_radius_ratio"]
            )
        )
        dimension_delta = abs(
            final["dynamic_shape_dimension"] - previous["dynamic_shape_dimension"]
        )
        spectrum_delta = abs(
            final["dynamic_free_shape_spectrum_median"]
            - previous["dynamic_free_shape_spectrum_median"]
        )
        plateau = bool(
            radius_log_delta <= args.plateau_radius_log_limit
            and dimension_delta <= args.plateau_dimension_limit
            and spectrum_delta <= args.plateau_spectrum_limit
        )
        modified = bool(
            abs(math.log(final["dynamic_free_radius_ratio"]))
            >= args.modified_radius_log_min
            or abs(final["dynamic_minus_free_shape_dimension"])
            >= args.modified_dimension_min
            or final["dynamic_free_shape_spectrum_median"] >= args.modified_spectrum_min
        )
        plateau_by_seed.append(plateau)
        modified_by_seed.append(modified)
        deltas.append(
            {
                "continuation_seed": row["continuation_seed"],
                "radius_log_delta": radius_log_delta,
                "dimension_delta": dimension_delta,
                "spectrum_delta": spectrum_delta,
                "plateau_pass": plateau,
                "modified_shape_pass": modified,
            }
        )
    required = math.ceil(args.min_seed_fraction * len(rows))
    plateau_count = sum(plateau_by_seed)
    modified_count = sum(modified_by_seed)
    stationary_count = sum(
        bool(row["source_stationarity"]["stationary_shape_pass"]) for row in rows
    )
    final_rows = [_checkpoint_by_update(row, final_update) for row in rows]
    return {
        "required_seed_count": required,
        "stationary_source_count": stationary_count,
        "stationary_source_pass": stationary_count >= required,
        "late_shape_plateau_count": plateau_count,
        "late_shape_plateau_pass": plateau_count >= required,
        "interaction_modified_shape_count": modified_count,
        "interaction_modified_shape_pass": modified_count >= required,
        "stable_interaction_modified_shape_candidate": bool(
            stationary_count >= required
            and plateau_count >= required
            and modified_count >= required
        ),
        "final_dynamic_minus_free_center_radii_median": float(
            np.median([row["dynamic_minus_free_center_radii"] for row in final_rows])
        ),
        "final_dynamic_free_radius_ratio_median": float(
            np.median([row["dynamic_free_radius_ratio"] for row in final_rows])
        ),
        "final_dynamic_minus_free_shape_dimension_median": float(
            np.median([row["dynamic_minus_free_shape_dimension"] for row in final_rows])
        ),
        "final_dynamic_free_shape_spectrum_median": float(
            np.median([row["dynamic_free_shape_spectrum_median"] for row in final_rows])
        ),
        "per_seed_late_deltas": deltas,
    }


def _aggregate(
    rows: list[dict[str, Any]], evaluations: list[int]
) -> list[dict[str, Any]]:
    metrics = [key for key in rows[0]["checkpoints"][0] if key != "evaluation_update"]
    aggregated = []
    for evaluation in evaluations:
        item: dict[str, Any] = {"evaluation_update": evaluation}
        checkpoints = [_checkpoint_by_update(row, evaluation) for row in rows]
        for metric in metrics:
            values = np.asarray([checkpoint[metric] for checkpoint in checkpoints])
            item[metric] = {
                "median": float(np.median(values)),
                "q25": float(np.quantile(values, 0.25)),
                "q75": float(np.quantile(values, 0.75)),
            }
        aggregated.append(item)
    return aggregated


def run_audit(args: argparse.Namespace) -> dict[str, Any]:
    checkpoint = load_finite_memory_checkpoint(_resolve(args.checkpoint))
    config = checkpoint.config
    window_updates = round(args.window_memory_times / config.alpha)
    if window_updates < 3 * args.sample_every:
        raise SystemExit("window must contain at least four samples")
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
    started = time.perf_counter()
    rows = [
        _run_seed(
            checkpoint,
            continuation_seed=seed,
            steps=args.steps,
            sample_every=args.sample_every,
            evaluations=args.evaluation_updates,
            window_updates=window_updates,
            source_offset=source_offset,
            cross_eta=calibration.cross_eta,
        )
        for seed in args.continuation_seeds
    ]
    payload = {
        "description": "One-way sustained-field interaction-age audit.",
        "created_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "checkpoint": str(args.checkpoint).replace("\\", "/"),
        "checkpoint_update_index": checkpoint.update_index,
        "final_update_index": checkpoint.update_index + args.steps,
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
            if key not in {"checkpoint", "report", "summary_json", "figure"}
        },
        "window_updates": window_updates,
        "calibration": {
            "cross_eta": calibration.cross_eta,
            "response_fraction_per_memory": args.response_fraction_per_memory,
            "initial_target_radius": calibration.target_radius,
            "source_center_offset": source_offset.tolist(),
        },
        "runtime_seconds": time.perf_counter() - started,
        "rows": rows,
        "aggregate": _aggregate(rows, args.evaluation_updates),
        "gate": _gate(rows, args),
    }
    return payload


def _series(payload: dict[str, Any], metric: str) -> tuple[np.ndarray, ...]:
    x = np.asarray([row["evaluation_update"] for row in payload["aggregate"]])
    median = np.asarray([row[metric]["median"] for row in payload["aggregate"]])
    q25 = np.asarray([row[metric]["q25"] for row in payload["aggregate"]])
    q75 = np.asarray([row[metric]["q75"] for row in payload["aggregate"]])
    return x, median, q25, q75


def _plot(payload: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.0), sharex=True)
    panels = (
        (
            axes[0, 0],
            "dynamic_minus_free_center_radii",
            "dynamic - free centre / R",
            None,
        ),
        (
            axes[0, 1],
            "dynamic_free_radius_ratio",
            "dynamic/free radius",
            1.0,
        ),
        (
            axes[1, 0],
            "dynamic_shape_dimension",
            "dynamic shape dimension",
            None,
        ),
        (
            axes[1, 1],
            "dynamic_free_shape_spectrum_median",
            "dynamic/free spectral distance",
            0.05,
        ),
    )
    for axis, metric, ylabel, reference in panels:
        x, median, q25, q75 = _series(payload, metric)
        axis.plot(x, median, marker="o", color="#0072B2")
        axis.fill_between(x, q25, q75, color="#56B4E9", alpha=0.3)
        if reference is not None:
            axis.axhline(reference, color="#666666", linestyle="--", linewidth=1)
        axis.set_xscale("log")
        axis.set_ylabel(ylabel)
        axis.grid(alpha=0.25)
    axes[1, 0].set_xlabel("continuation updates")
    axes[1, 1].set_xlabel("continuation updates")
    fig.suptitle("Sustained one-way interaction age: median and seed IQR")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    gate = payload["gate"]
    lines = [
        "# One-Way Interaction-Age Audit",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Question",
        "",
        "Does a mature target develop a slowly emerging, control-separated shape",
        "under the sustained field of a second autonomously evolving scalar knot?",
        "",
        "## Design",
        "",
        f"- Start checkpoint: N={payload['checkpoint_update_index']:,}.",
        f"- Final state age: N={payload['final_update_index']:,}.",
        f"- Evaluations: {payload['parameters']['evaluation_updates']} updates.",
        f"- Trailing window: {payload['window_updates']:,} updates.",
        "- Every N point comes from one common-prefix continuation per seed.",
        "- Dynamic-source, frozen-source, free and eta-zero targets share noise.",
        "- This is one-way sustained-field adaptation, not reciprocal formation.",
        "",
        "## Registered decision gate",
        "",
        f"- Mature source stationary: {gate['stationary_source_pass']} "
        f"({gate['stationary_source_count']}/{len(payload['rows'])}).",
        f"- Shape plateau from the penultimate to final age: "
        f"{gate['late_shape_plateau_pass']} "
        f"({gate['late_shape_plateau_count']}/{len(payload['rows'])}).",
        f"- Interaction-modified shape at final age: "
        f"{gate['interaction_modified_shape_pass']} "
        f"({gate['interaction_modified_shape_count']}/{len(payload['rows'])}).",
        f"- Stable interaction-modified shape candidate: "
        f"{gate['stable_interaction_modified_shape_candidate']}.",
        f"- Final dynamic-free centre response: "
        f"{gate['final_dynamic_minus_free_center_radii_median']:.4g} R.",
        f"- Final dynamic/free radius ratio: "
        f"{gate['final_dynamic_free_radius_ratio_median']:.5f}.",
        f"- Final shape-dimension difference: "
        f"{gate['final_dynamic_minus_free_shape_dimension_median']:.5f}.",
        f"- Final spectral-shape distance: "
        f"{gate['final_dynamic_free_shape_spectrum_median']:.5f}.",
        "",
        f"![Interaction-age audit]({_relative(report, figure)})",
        "",
        "## N dependence",
        "",
        "| continuation N | centre / R | radius ratio | dynamic D_shape | "
        "D_shape difference | spectral distance |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload["aggregate"]:
        lines.append(
            f"| {row['evaluation_update']:,} | "
            f"{row['dynamic_minus_free_center_radii']['median']:.4g} | "
            f"{row['dynamic_free_radius_ratio']['median']:.5f} | "
            f"{row['dynamic_shape_dimension']['median']:.4f} | "
            f"{row['dynamic_minus_free_shape_dimension']['median']:.4f} | "
            f"{row['dynamic_free_shape_spectrum_median']['median']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- A stable shape difference is an effective-state candidate, not a new",
            "  particle type, quantum number or reciprocal bound state.",
            "- Five continuation seeds share one formation checkpoint and therefore",
            "  sample future noise, not independent formation basins.",
            "- If the last two ages do not plateau, extend N before changing parameters.",
            "- If they plateau without a control-separated shape, longer waiting under",
            "  this same channel is not the next priority.",
            "",
            f"Runtime: {payload['runtime_seconds']:.1f} seconds.",
            f"Git revision: {payload['git_revision']}.",
            f"Git status at generation: {payload['git_status'] or 'clean'}.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    _validate_args(args)
    payload = run_audit(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")
    summary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    _plot(payload, figure)
    print(json.dumps(payload["gate"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
