from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import statistics
import subprocess
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
DYNAMICS_DIR = ROOT / "experiments" / "current" / "dynamics"
sys.path.insert(0, str(DYNAMICS_DIR))
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    SimulationConfig,
    linear_memory_relative_rms_radius,
    memory_horizon,
)

import fixed_curvature_sigma_pilot as common  # noqa: E402
import long_run_metastability as metastability_run  # noqa: E402


METRICS = (
    "knot_score",
    "memory_radius_over_length",
    "memory_dimension",
    "memory_roundness",
    "dynamic_radius_over_length",
    "normalized_dynamic_radius",
    "dynamic_drift_ratio",
    "best_residence_memory_times",
)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


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


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(item < 0 for item in values):
        raise argparse.ArgumentTypeError(
            "expected non-negative comma-separated integers"
        )
    return values


def _parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(not math.isfinite(item) for item in values):
        raise argparse.ArgumentTypeError("expected finite comma-separated numbers")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Test the attractive-only scalar model at fixed restoring strength "
            "while increasing the predicted radius relative to the kernel scale."
        )
    )
    parser.add_argument("--steps", type=int, default=300_000)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument(
        "--seeds", type=_parse_int_list, default=_parse_int_list("1,2,3,4,5")
    )
    parser.add_argument(
        "--target-radius-ratios",
        type=_parse_float_list,
        default=_parse_float_list("0.03,0.1,0.3"),
    )
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-att", type=float, default=26.0)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--max-memory", type=int, default=600)
    parser.add_argument("--burn-in", type=int, default=0)
    parser.add_argument("--sample-every", type=int, default=1000)
    parser.add_argument("--trace-points", type=int, default=100)
    parser.add_argument(
        "--voxel-sizes",
        type=_parse_float_list,
        default=_parse_float_list("0.5,1.0,2.0"),
    )
    parser.add_argument("--max-ac-lag", type=int, default=50)
    parser.add_argument("--min-memory-times", type=float, default=10.0)
    parser.add_argument("--skip-run", action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "data/processed/kernel_core/fixed_g_RL_d3_N300k_seed1-5_A26_2026-07-19"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/kernels/nonlinearity/fixed_g_RL_d3_N300k_A26_2026-07-19.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/kernels/nonlinearity/fixed_g_RL_d3_N300k_A26_2026-07-19.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/kernels/nonlinearity_2026-07-19/fixed_g_RL_d3_N300k_A26.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _token(value: float) -> str:
    return f"RL{value:.8g}".replace(".", "p").replace("-", "m")


def retained_memory_mass(
    *, lambda_value: float, memory_mass: float, horizon: int
) -> float:
    if not 0.0 < lambda_value <= 1.0:
        raise ValueError("lambda_value must lie in (0,1]")
    if memory_mass < 0.0 or not math.isfinite(memory_mass):
        raise ValueError("memory_mass must be non-negative and finite")
    if horizon < 1:
        raise ValueError("horizon must be positive")
    return float(memory_mass * (1.0 - (1.0 - lambda_value) ** horizon))


def epsilon_for_target_radius_ratio(
    *,
    target_radius_ratio: float,
    length_scale: float,
    lambda_value: float,
    restoring_per_update: float,
    dim: int,
) -> float:
    """Invert the finite-memory linear relative-mode RMS radius."""

    if target_radius_ratio <= 0.0 or not math.isfinite(target_radius_ratio):
        raise ValueError("target_radius_ratio must be positive and finite")
    if length_scale <= 0.0 or not math.isfinite(length_scale):
        raise ValueError("length_scale must be positive and finite")
    if not 0.0 < lambda_value < 1.0:
        raise ValueError("lambda_value must lie in (0,1)")
    if dim < 1:
        raise ValueError("dim must be positive")
    q = 1.0 - lambda_value
    multiplier = q * (1.0 - restoring_per_update)
    if abs(multiplier) >= 1.0:
        raise ValueError("linear relative mode is unstable")
    return float(
        target_radius_ratio
        * length_scale
        * math.sqrt(1.0 - multiplier * multiplier)
        / (math.sqrt(dim) * q)
    )


def _validate_args(args: argparse.Namespace) -> None:
    if args.steps < 1 or args.dim < 1:
        raise SystemExit("--steps and --dim must be positive")
    if args.burn_in < 0 or args.burn_in >= args.steps:
        raise SystemExit("--burn-in must satisfy 0 <= burn_in < steps")
    if args.sample_every < 1 or args.trace_points < 2:
        raise SystemExit("sampling values must be positive and trace-points >= 2")
    if len(set(args.target_radius_ratios)) != len(args.target_radius_ratios):
        raise SystemExit("target radius ratios must not contain duplicates")
    if any(value <= 0.0 for value in args.target_radius_ratios):
        raise SystemExit("target radius ratios must be positive")
    if len(args.target_radius_ratios) < 2:
        raise SystemExit("at least two target radius ratios are required")
    for name in ("eta", "memory_mass", "sigma_att", "amplitude_att"):
        value = float(getattr(args, name))
        if value <= 0.0 or not math.isfinite(value):
            raise SystemExit(f"--{name.replace('_', '-')} must be positive and finite")
    if not 0.0 < args.alpha < 1.0:
        raise SystemExit("--alpha must lie in (0,1) for radius inversion")
    if args.sigma_rep <= 0.0 or not math.isfinite(args.sigma_rep):
        raise SystemExit("--sigma-rep must be positive and finite")


def _base_config(args: argparse.Namespace, *, epsilon: float) -> SimulationConfig:
    return SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=epsilon,
        eta=args.eta,
        alpha=args.alpha,
        memory_mass=args.memory_mass,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=0.0,
        amplitude_att=args.amplitude_att,
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )


def _finite(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _ratio(left: Any, right: Any) -> float | None:
    numerator = _finite(left)
    denominator = _finite(right)
    if numerator is None or denominator in (None, 0.0):
        return None
    return float(numerator / denominator)


def _difference(left: Any, right: Any) -> float | None:
    left_number = _finite(left)
    right_number = _finite(right)
    if left_number is None or right_number is None:
        return None
    return float(left_number - right_number)


def _case_row(
    case: dict[str, Any],
    *,
    control: dict[str, Any] | None,
    target: float,
    epsilon: float,
    prediction: float,
    length_scale: float,
    stored_mass: float,
    g_retained: float,
) -> dict[str, Any]:
    row = common._row_from_case(case, q=None, control=control)
    dynamic_radius = _finite(row.get("dynamic_radius"))
    memory_radius = _finite(row.get("memory_radius"))
    row.update(
        {
            "target_radius_ratio": target,
            "epsilon": epsilon,
            "linear_prediction": prediction,
            "stored_memory_mass": stored_mass,
            "retained_restoring_per_update": g_retained,
            "dynamic_radius_over_length": (
                dynamic_radius / length_scale if dynamic_radius is not None else None
            ),
            "memory_radius_over_length": (
                memory_radius / length_scale if memory_radius is not None else None
            ),
            "normalized_dynamic_radius": _ratio(dynamic_radius, prediction),
            "gaussian_curvature_loss_at_target": 1.0 - math.exp(-0.5 * target * target),
        }
    )
    return row


def run_or_load_cases(
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, float]]:
    output_dir = _resolve(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prototype = _base_config(args, epsilon=0.0)
    horizon = memory_horizon(prototype)
    stored_mass = retained_memory_mass(
        lambda_value=args.alpha,
        memory_mass=args.memory_mass,
        horizon=horizon,
    )
    curvature = args.amplitude_att / (args.sigma_att * args.sigma_att)
    g_retained = args.eta * stored_mass * curvature
    trace_targets = metastability_run._trace_targets(
        steps=args.steps,
        burn_in=args.burn_in,
        trace_every=0,
        trace_points=args.trace_points,
        trace_spacing="log",
    )
    active_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    for target in sorted(args.target_radius_ratios):
        epsilon = epsilon_for_target_radius_ratio(
            target_radius_ratio=target,
            length_scale=args.sigma_att,
            lambda_value=args.alpha,
            restoring_per_update=g_retained,
            dim=args.dim,
        )
        config = _base_config(args, epsilon=epsilon)
        active_prediction = linear_memory_relative_rms_radius(
            epsilon=epsilon,
            lambda_value=args.alpha,
            restoring_per_update=g_retained,
            dim=args.dim,
        )
        control_prediction = linear_memory_relative_rms_radius(
            epsilon=epsilon,
            lambda_value=args.alpha,
            restoring_per_update=0.0,
            dim=args.dim,
        )
        directory = output_dir / _token(target)
        for seed in args.seeds:
            control = common._run_or_load(
                config=config,
                condition="eta_zero",
                seed=seed,
                directory=directory,
                args=args,
                trace_targets=trace_targets,
            )
            active = common._run_or_load(
                config=config,
                condition="baseline",
                seed=seed,
                directory=directory,
                args=args,
                trace_targets=trace_targets,
            )
            active_rows.append(
                _case_row(
                    active,
                    control=control,
                    target=target,
                    epsilon=epsilon,
                    prediction=active_prediction,
                    length_scale=args.sigma_att,
                    stored_mass=stored_mass,
                    g_retained=g_retained,
                )
            )
            control_rows.append(
                _case_row(
                    control,
                    control=None,
                    target=target,
                    epsilon=epsilon,
                    prediction=control_prediction,
                    length_scale=args.sigma_att,
                    stored_mass=stored_mass,
                    g_retained=0.0,
                )
            )
    metadata = {
        "memory_horizon": float(horizon),
        "stored_memory_mass": stored_mass,
        "local_curvature": curvature,
        "retained_restoring_per_update": g_retained,
    }
    return active_rows, control_rows, metadata


def _median(values: Iterable[Any]) -> float | None:
    finite = [number for value in values if (number := _finite(value)) is not None]
    return statistics.median(finite) if finite else None


def _quartiles(values: Iterable[Any]) -> tuple[float | None, float | None]:
    finite = sorted(
        number for value in values if (number := _finite(value)) is not None
    )
    if not finite:
        return None, None
    if len(finite) == 1:
        return finite[0], finite[0]
    q1, _, q3 = statistics.quantiles(finite, n=4, method="inclusive")
    return q1, q3


def aggregate_rows(
    rows: list[dict[str, Any]], targets: list[float]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for target in sorted(targets):
        group = [row for row in rows if row["target_radius_ratio"] == target]
        record: dict[str, Any] = {
            "target_radius_ratio": target,
            "epsilon": _median(row["epsilon"] for row in group),
            "linear_prediction": _median(row["linear_prediction"] for row in group),
            "gaussian_curvature_loss_at_target": _median(
                row["gaussian_curvature_loss_at_target"] for row in group
            ),
            "n_seeds": len(group),
        }
        for metric in METRICS:
            record[f"{metric}_median"] = _median(row.get(metric) for row in group)
            low, high = _quartiles(row.get(metric) for row in group)
            record[f"{metric}_q1"] = low
            record[f"{metric}_q3"] = high
        output.append(record)
    return output


def endpoint_comparison(
    active_rows: list[dict[str, Any]],
    control_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    targets = sorted({float(row["target_radius_ratio"]) for row in active_rows})
    low_target, high_target = targets[0], targets[-1]
    records: list[dict[str, Any]] = []
    for seed in sorted({int(row["seed"]) for row in active_rows}):
        active_low = next(
            row
            for row in active_rows
            if row["seed"] == seed and row["target_radius_ratio"] == low_target
        )
        active_high = next(
            row
            for row in active_rows
            if row["seed"] == seed and row["target_radius_ratio"] == high_target
        )
        control_low = next(
            row
            for row in control_rows
            if row["seed"] == seed and row["target_radius_ratio"] == low_target
        )
        control_high = next(
            row
            for row in control_rows
            if row["seed"] == seed and row["target_radius_ratio"] == high_target
        )
        active_radius_ratio = _ratio(
            active_high["dynamic_radius"], active_low["dynamic_radius"]
        )
        control_radius_ratio = _ratio(
            control_high["dynamic_radius"], control_low["dynamic_radius"]
        )
        target_ratio = high_target / low_target
        active_departure = _ratio(
            active_high["normalized_dynamic_radius"],
            active_low["normalized_dynamic_radius"],
        )
        control_departure = _ratio(
            control_high["normalized_dynamic_radius"],
            control_low["normalized_dynamic_radius"],
        )
        low_residence = _finite(active_low.get("best_residence_memory_times"))
        high_residence = _finite(active_high.get("best_residence_memory_times"))
        residence_log2_ratio = (
            math.log2(high_residence / low_residence)
            if low_residence not in (None, 0.0) and high_residence not in (None, 0.0)
            else None
        )
        records.append(
            {
                "seed": seed,
                "low_target": low_target,
                "high_target": high_target,
                "active_normalized_radius_departure": (
                    active_departure - 1.0 if active_departure is not None else None
                ),
                "control_normalized_radius_departure": (
                    control_departure - 1.0 if control_departure is not None else None
                ),
                "active_scaling_exponent": (
                    math.log(active_radius_ratio) / math.log(target_ratio)
                    if active_radius_ratio is not None and active_radius_ratio > 0.0
                    else None
                ),
                "control_scaling_exponent": (
                    math.log(control_radius_ratio) / math.log(target_ratio)
                    if control_radius_ratio is not None and control_radius_ratio > 0.0
                    else None
                ),
                "knot_score_change": _difference(
                    active_high.get("knot_score"), active_low.get("knot_score")
                ),
                "memory_dimension_change": _difference(
                    active_high.get("memory_dimension"),
                    active_low.get("memory_dimension"),
                ),
                "memory_roundness_change": _difference(
                    active_high.get("memory_roundness"),
                    active_low.get("memory_roundness"),
                ),
                "residence_log2_ratio": residence_log2_ratio,
            }
        )
    return records


def classify_nonlinearity_gate(
    endpoint_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    departures = [
        value
        for row in endpoint_rows
        if (value := _finite(row.get("active_normalized_radius_departure"))) is not None
    ]
    if not departures:
        return {"classification": "insufficient_data"}
    signed_median = float(statistics.median(departures))
    median_absolute = float(statistics.median(abs(value) for value in departures))
    sign = 1.0 if signed_median >= 0.0 else -1.0
    consistent_sign = sum(value * sign > 0.0 for value in departures)
    within_twenty_percent = sum(abs(value) <= 0.20 for value in departures)
    supporting_medians = {
        "knot_score_change": _median(
            row.get("knot_score_change") for row in endpoint_rows
        ),
        "memory_dimension_change": _median(
            row.get("memory_dimension_change") for row in endpoint_rows
        ),
        "memory_roundness_change": _median(
            row.get("memory_roundness_change") for row in endpoint_rows
        ),
        "residence_log2_ratio": _median(
            row.get("residence_log2_ratio") for row in endpoint_rows
        ),
    }
    supporting_flags = {
        "knot_score": abs(supporting_medians["knot_score_change"] or 0.0) >= 0.10,
        "memory_dimension": abs(supporting_medians["memory_dimension_change"] or 0.0)
        >= 0.25,
        "memory_roundness": abs(supporting_medians["memory_roundness_change"] or 0.0)
        >= 0.10,
        "residence": abs(supporting_medians["residence_log2_ratio"] or 0.0) >= 1.0,
    }
    n_required = math.ceil(0.8 * len(departures))
    if (
        abs(signed_median) >= 0.20
        and consistent_sign >= n_required
        and any(supporting_flags.values())
    ):
        classification = "nonlinear_candidate"
    elif (
        median_absolute <= 0.10
        and within_twenty_percent >= n_required
        and not any(supporting_flags.values())
    ):
        classification = "linear_compatible"
    else:
        classification = "inconclusive"
    return {
        "classification": classification,
        "n_seeds": len(departures),
        "required_consistent_seeds": n_required,
        "median_signed_radius_departure": signed_median,
        "median_absolute_radius_departure": median_absolute,
        "same_sign_seed_count": consistent_sign,
        "within_twenty_percent_seed_count": within_twenty_percent,
        "supporting_metric_medians": supporting_medians,
        "supporting_metric_flags": supporting_flags,
    }


def _plot_series(
    axis: plt.Axes,
    rows: list[dict[str, Any]],
    metric: str,
    *,
    label: str,
    color: str,
    marker: str,
) -> None:
    valid = [row for row in rows if row.get(f"{metric}_median") is not None]
    if not valid:
        return
    x = np.asarray([float(row["target_radius_ratio"]) for row in valid])
    y = np.asarray([float(row[f"{metric}_median"]) for row in valid])
    low = np.asarray([float(row[f"{metric}_q1"]) for row in valid])
    high = np.asarray([float(row[f"{metric}_q3"]) for row in valid])
    axis.errorbar(
        x,
        y,
        yerr=np.vstack([y - low, high - y]),
        color=color,
        marker=marker,
        linewidth=1.8,
        capsize=3,
        label=label,
    )


def _plot(
    active: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    output: Path,
) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(13.4, 7.8))
    active_color = "#176b87"
    control_color = "#777777"
    _plot_series(
        axes[0, 0],
        active,
        "dynamic_radius_over_length",
        label="active",
        color=active_color,
        marker="o",
    )
    _plot_series(
        axes[0, 0],
        controls,
        "dynamic_radius_over_length",
        label="eta=0",
        color=control_color,
        marker="s",
    )
    targets = np.asarray([float(row["target_radius_ratio"]) for row in active])
    axes[0, 0].plot(targets, targets, "k--", linewidth=1.2, label="active target")
    axes[0, 0].set_xscale("log")
    axes[0, 0].set_yscale("log")
    axes[0, 0].set_ylabel("measured dynamic R / L")

    _plot_series(
        axes[0, 1],
        active,
        "normalized_dynamic_radius",
        label="active",
        color=active_color,
        marker="o",
    )
    _plot_series(
        axes[0, 1],
        controls,
        "normalized_dynamic_radius",
        label="eta=0",
        color=control_color,
        marker="s",
    )
    axes[0, 1].axhline(1.0, color="black", linestyle="--", linewidth=1.2)
    axes[0, 1].set_xscale("log")
    axes[0, 1].set_ylabel("measured / linear prediction")

    _plot_series(
        axes[0, 2],
        active,
        "knot_score",
        label="active vs eta=0",
        color=active_color,
        marker="o",
    )
    axes[0, 2].set_xscale("log")
    axes[0, 2].set_ylim(-0.03, 1.03)
    axes[0, 2].set_ylabel("KnotScore v0.5")

    for axis, metric, label in (
        (axes[1, 0], "memory_dimension", "D_mem"),
        (axes[1, 1], "memory_roundness", "memory roundness"),
        (axes[1, 2], "best_residence_memory_times", "best residence [memory times]"),
    ):
        _plot_series(
            axis,
            active,
            metric,
            label="active",
            color=active_color,
            marker="o",
        )
        _plot_series(
            axis,
            controls,
            metric,
            label="eta=0",
            color=control_color,
            marker="s",
        )
        axis.set_xscale("log")
        axis.set_ylabel(label)
    residence_values = [
        float(row["best_residence_memory_times_median"])
        for row in active + controls
        if row.get("best_residence_memory_times_median") is not None
    ]
    if residence_values and min(residence_values) > 0.0:
        axes[1, 2].set_yscale("log")
    for axis in axes.flat:
        axis.set_xlabel("target active R_linear / L")
        axis.grid(True, alpha=0.22)
        axis.legend(frameon=False, fontsize=7)
    fig.suptitle("Fixed-g scalar nonlinearity gate")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=190)
    plt.close(fig)


def _fmt(value: Any, digits: int = 4) -> str:
    number = _finite(value)
    if number is None:
        return "n/a"
    if number == 0.0:
        return "0"
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.{digits}e}"
    return f"{number:.{digits}f}"


def write_outputs(
    *,
    args: argparse.Namespace,
    active_rows: list[dict[str, Any]],
    control_rows: list[dict[str, Any]],
    metadata: dict[str, float],
    elapsed_seconds: float,
    source_git_revision: str,
    source_git_status: str,
) -> None:
    report = _resolve(args.report)
    summary_json = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    active_aggregate = aggregate_rows(active_rows, args.target_radius_ratios)
    control_aggregate = aggregate_rows(control_rows, args.target_radius_ratios)
    endpoints = endpoint_comparison(active_rows, control_rows)
    decision = classify_nonlinearity_gate(endpoints)
    _plot(active_aggregate, control_aggregate, figure)
    generated = _utc_now()
    payload = {
        "description": "Pre-registered fixed-g scalar nonlinearity gate.",
        "generated_utc": generated,
        "git_revision": source_git_revision,
        "git_status": source_git_status,
        "arguments": {
            key: str(value) if isinstance(value, Path) else value
            for key, value in vars(args).items()
        },
        "metadata": metadata,
        "active_rows": active_rows,
        "control_rows": control_rows,
        "active_aggregate": active_aggregate,
        "control_aggregate": control_aggregate,
        "endpoint_seed_pairs": endpoints,
        "decision": decision,
        "invocation_elapsed_seconds": elapsed_seconds,
    }
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )
    lines = [
        "# Fixed-g Scalar Nonlinearity Gate",
        "",
        f"Date: {generated}.",
        "",
        "## Scope",
        "",
        f"Attractive-only scalar kernel with `A_att={args.amplitude_att:g}`,",
        f"`L=sigma_att={args.sigma_att:g}`, `eta={args.eta:g}`,",
        f"`lambda={args.alpha:g}`, `M0={args.memory_mass:g}`, `d={args.dim}`,",
        f"`N={args.steps:,}`, delta deposition, and seeds",
        f"`{','.join(str(seed) for seed in args.seeds)}`. Only `epsilon` changes.",
        "It is chosen by inverting the finite-memory linear radius so that",
        "`R_linear/L` equals the pre-registered target.",
        "",
        f"Retained horizon `H={int(metadata['memory_horizon'])}`, retained mass",
        f"`M_stored={_fmt(metadata['stored_memory_mass'], 7)}`, and retained",
        f"restoring strength `g={_fmt(metadata['retained_restoring_per_update'], 7)}`.",
        "",
        f"![Fixed-g nonlinearity gate]({_rel_from(report, figure)})",
        "",
        "## Pre-registered decision rule",
        "",
        "A nonlinear candidate requires at least a 20% median endpoint change",
        "in the seed-paired normalized active radius, the same sign in at least",
        "80% of seeds, and one independent median change: KnotScore >=0.10,",
        "D_mem >=0.25, roundness >=0.10, or residence by a factor >=2.",
        "Linear-compatible requires median absolute radius departure <=10%,",
        "at least 80% of seeds within 20%, and no independent threshold crossing.",
        "Everything else is inconclusive.",
        "",
        "## Active results",
        "",
        "| target R/L | epsilon | force-curvature loss | measured R/L | measured/pred | score | D_mem | roundness | residence |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in active_aggregate:
        lines.append(
            f"| {_fmt(row['target_radius_ratio'])} | {_fmt(row['epsilon'])} | "
            f"{_fmt(row['gaussian_curvature_loss_at_target'])} | "
            f"{_fmt(row['dynamic_radius_over_length_median'])} | "
            f"{_fmt(row['normalized_dynamic_radius_median'])} | "
            f"{_fmt(row['knot_score_median'])} | "
            f"{_fmt(row['memory_dimension_median'])} | "
            f"{_fmt(row['memory_roundness_median'])} | "
            f"{_fmt(row['best_residence_memory_times_median'])} |"
        )
    lines.extend(
        [
            "",
            "## Eta-zero controls",
            "",
            "| target axis | epsilon | measured R/L | measured/pred | D_mem | roundness | residence |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in control_aggregate:
        lines.append(
            f"| {_fmt(row['target_radius_ratio'])} | {_fmt(row['epsilon'])} | "
            f"{_fmt(row['dynamic_radius_over_length_median'])} | "
            f"{_fmt(row['normalized_dynamic_radius_median'])} | "
            f"{_fmt(row['memory_dimension_median'])} | "
            f"{_fmt(row['memory_roundness_median'])} | "
            f"{_fmt(row['best_residence_memory_times_median'])} |"
        )
    lines.extend(
        [
            "",
            "## Seed-paired endpoint scaling",
            "",
            "| seed | active normalized departure | active exponent | control departure | control exponent | delta score | delta D_mem | delta roundness | log2 residence ratio |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in endpoints:
        lines.append(
            f"| {row['seed']} | {_fmt(row['active_normalized_radius_departure'])} | "
            f"{_fmt(row['active_scaling_exponent'])} | "
            f"{_fmt(row['control_normalized_radius_departure'])} | "
            f"{_fmt(row['control_scaling_exponent'])} | "
            f"{_fmt(row['knot_score_change'])} | "
            f"{_fmt(row['memory_dimension_change'])} | "
            f"{_fmt(row['memory_roundness_change'])} | "
            f"{_fmt(row['residence_log2_ratio'])} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"Classification: **{decision['classification']}**.",
            "",
            f"Median signed endpoint radius departure: `{_fmt(decision.get('median_signed_radius_departure'))}`.",
            f"Median absolute endpoint radius departure: `{_fmt(decision.get('median_absolute_radius_departure'))}`.",
            f"Same-sign seeds: `{decision.get('same_sign_seed_count', 'n/a')}`; seeds within 20%: `{decision.get('within_twenty_percent_seed_count', 'n/a')}`.",
            "",
            "This gate tests departure from the local scalar reduction. It does",
            "not by itself establish metastability, particle identity, or a",
            "physical length calibration.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{source_git_revision}`",
            f"- Git status: `{source_git_status or 'clean'}`",
            f"- Invocation elapsed: `{elapsed_seconds:.2f} s`",
            "",
        ]
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    _validate_args(args)
    source_git_revision = _git_output(["rev-parse", "HEAD"])
    source_git_status = _git_output(["status", "--short"])
    started = time.perf_counter()
    active_rows, control_rows, metadata = run_or_load_cases(args)
    write_outputs(
        args=args,
        active_rows=active_rows,
        control_rows=control_rows,
        metadata=metadata,
        elapsed_seconds=time.perf_counter() - started,
        source_git_revision=source_git_revision,
        source_git_status=source_git_status,
    )


if __name__ == "__main__":
    main()
