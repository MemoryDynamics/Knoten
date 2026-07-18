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
    scalar_dimensionless_groups,
    two_scale_local_curvature,
)

import fixed_curvature_sigma_pilot as common  # noqa: E402
import long_run_metastability as metastability_run  # noqa: E402


METRICS = {
    "knot_score": "KnotScore v0.5",
    "memory_radius": "memory radius",
    "memory_dimension": "D_mem",
    "memory_roundness": "memory roundness",
    "dynamic_radius": "dynamic RMS radius",
    "dynamic_drift_ratio": "center drift / radius / memory time",
}

CHANGE_METRICS = {
    "memory_radius_median": "log",
    "dynamic_radius_median": "log",
    "dynamic_drift_ratio_median": "log",
    "memory_dimension_median": "linear",
    "memory_roundness_median": "linear",
    "memory_compactness_gain_median": "log",
}

PAIR_METRICS = {
    "memory_radius": "memory radius",
    "memory_dimension": "D_mem",
    "memory_roundness": "roundness",
    "dynamic_radius": "dynamic radius",
    "dynamic_drift_ratio": "drift/r",
    "covariance_dimension": "D_cov",
    "occupancy_window_dimension": "D_occ window",
}


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


def _default_amplitudes() -> list[float]:
    return [float(value) for value in range(0, 41)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scan an attractive-only scalar kernel over A_att=0..40, compare "
            "A_att=26 with the curvature-matched two-scale (1,35) reference, "
            "and rank observed KPI change intervals without presupposing a "
            "phase transition."
        )
    )
    parser.add_argument("--steps", type=int, default=300_000)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument(
        "--seeds", type=_parse_int_list, default=_parse_int_list("1,2,3,4,5")
    )
    parser.add_argument(
        "--amplitudes",
        type=_parse_float_list,
        default=_default_amplitudes(),
    )
    parser.add_argument("--epsilon", type=float, default=1.0e-4)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--reference-amplitude-rep", type=float, default=1.0)
    parser.add_argument("--reference-amplitude-att", type=float, default=35.0)
    parser.add_argument("--matched-amplitude-att", type=float, default=26.0)
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
            "data/processed/kernel_core/"
            "attractive_only_A0-40_d3_N300k_seed1-5_eps1em4_2026-07-18"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/kernels/core/attractive_only_regime_scan_d3_N300k_2026-07-18.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/kernels/core/attractive_only_regime_scan_d3_N300k_2026-07-18.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/kernels/core_2026-07-18/attractive_only_regime_scan.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _token(value: float) -> str:
    return f"A{value:.8g}".replace(".", "p").replace("-", "m")


def _validate_args(args: argparse.Namespace) -> None:
    if args.steps < 1 or args.dim < 1:
        raise SystemExit("--steps and --dim must be positive")
    if args.burn_in < 0 or args.burn_in >= args.steps:
        raise SystemExit("--burn-in must satisfy 0 <= burn_in < steps")
    if args.sample_every < 1 or args.trace_points < 2:
        raise SystemExit("sampling values must be positive and trace-points >= 2")
    if any(value < 0.0 for value in args.amplitudes):
        raise SystemExit("attractive-only amplitudes must be non-negative")
    if len(set(args.amplitudes)) != len(args.amplitudes):
        raise SystemExit("--amplitudes must not contain duplicates")
    if 0.0 not in args.amplitudes:
        raise SystemExit(
            "--amplitudes must include A_att=0 as null implementation control"
        )
    if args.matched_amplitude_att not in args.amplitudes:
        raise SystemExit("--amplitudes must include --matched-amplitude-att")
    if args.sigma_rep <= 0.0 or args.sigma_att <= 0.0:
        raise SystemExit("kernel lengths must be positive")
    if not math.isfinite(args.epsilon) or args.epsilon < 0.0:
        raise SystemExit("--epsilon must be non-negative")
    if not math.isfinite(args.eta) or args.eta <= 0.0:
        raise SystemExit("--eta must be positive for the dimensionless scan axis")
    if not math.isfinite(args.alpha) or not 0.0 < args.alpha <= 1.0:
        raise SystemExit("--alpha must satisfy 0 < value <= 1")
    if not math.isfinite(args.memory_mass) or args.memory_mass <= 0.0:
        raise SystemExit("--memory-mass must be positive")
    target = two_scale_local_curvature(
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=args.reference_amplitude_rep,
        amplitude_att=args.reference_amplitude_att,
    )
    matched = two_scale_local_curvature(
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=0.0,
        amplitude_att=args.matched_amplitude_att,
    )
    if not math.isclose(target, matched, rel_tol=1e-12, abs_tol=1e-12):
        raise SystemExit(
            "matched attractive-only amplitude does not preserve reference curvature"
        )


def _base_config(
    args: argparse.Namespace,
    *,
    amplitude_rep: float,
    amplitude_att: float,
) -> SimulationConfig:
    return SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=args.epsilon,
        eta=args.eta,
        alpha=args.alpha,
        memory_mass=args.memory_mass,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )


def _row(
    case: dict[str, Any],
    *,
    amplitude_att: float,
    control: dict[str, Any] | None,
    args: argparse.Namespace,
    family: str,
) -> dict[str, Any]:
    row = common._row_from_case(case, q=None, control=control)
    curvature = two_scale_local_curvature(
        sigma_rep=float(case["base_config"]["sigma_rep"]),
        sigma_att=float(case["base_config"]["sigma_att"]),
        amplitude_rep=float(case["base_config"]["amplitude_rep"]),
        amplitude_att=float(case["base_config"]["amplitude_att"]),
    )
    groups = scalar_dimensionless_groups(
        epsilon=args.epsilon,
        eta=args.eta,
        lambda_value=args.alpha,
        memory_mass=args.memory_mass,
        local_curvature=curvature,
        length_scale=args.sigma_att,
    )
    row.update(
        {
            "family": family,
            "amplitude_att": float(amplitude_att),
            "local_curvature": curvature,
            "restoring_per_update": groups.restoring_per_update,
            "restoring_per_memory_time": groups.restoring_per_memory_time,
            "memory_radius_over_length_unit": (
                float(row["memory_radius"]) / args.sigma_att
                if row.get("memory_radius") is not None
                else None
            ),
        }
    )
    return row


def run_or_load_cases(
    args: argparse.Namespace,
    output_dir: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], bool]:
    output_dir.mkdir(parents=True, exist_ok=True)
    trace_targets = metastability_run._trace_targets(
        steps=args.steps,
        burn_in=args.burn_in,
        trace_every=0,
        trace_points=args.trace_points,
        trace_spacing="log",
    )
    null_config = _base_config(args, amplitude_rep=0.0, amplitude_att=0.0)
    controls: dict[int, dict[str, Any]] = {}
    for seed in args.seeds:
        controls[seed] = common._run_or_load(
            config=null_config,
            condition="eta_zero",
            seed=seed,
            directory=output_dir / "shared_eta_zero",
            args=args,
            trace_targets=trace_targets,
        )

    rows: list[dict[str, Any]] = []
    null_exact = True
    for amplitude in sorted(args.amplitudes):
        config = _base_config(args, amplitude_rep=0.0, amplitude_att=amplitude)
        for seed in args.seeds:
            case = common._run_or_load(
                config=config,
                condition="baseline",
                seed=seed,
                directory=output_dir / _token(amplitude),
                args=args,
                trace_targets=trace_targets,
            )
            rows.append(
                _row(
                    case,
                    amplitude_att=amplitude,
                    control=controls[seed],
                    args=args,
                    family="attractive_only",
                )
            )
            if amplitude == 0.0:
                null_exact = null_exact and case.get("diagnostics") == controls[
                    seed
                ].get("diagnostics")

    reference_config = _base_config(
        args,
        amplitude_rep=args.reference_amplitude_rep,
        amplitude_att=args.reference_amplitude_att,
    )
    reference_rows: list[dict[str, Any]] = []
    for seed in args.seeds:
        case = common._run_or_load(
            config=reference_config,
            condition="baseline",
            seed=seed,
            directory=output_dir / "two_scale_reference",
            args=args,
            trace_targets=trace_targets,
        )
        reference_rows.append(
            _row(
                case,
                amplitude_att=args.reference_amplitude_att,
                control=controls[seed],
                args=args,
                family="two_scale_reference",
            )
        )
    control_rows = [
        _row(
            case,
            amplitude_att=0.0,
            control=None,
            args=args,
            family="eta_zero",
        )
        for case in controls.values()
    ]
    return rows, reference_rows, control_rows, null_exact


def _median(values: Iterable[Any]) -> float | None:
    finite: list[float] = []
    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(number):
            finite.append(number)
    return statistics.median(finite) if finite else None


def _quartiles(values: Iterable[Any]) -> tuple[float | None, float | None]:
    finite = sorted(
        float(value)
        for value in values
        if value is not None and math.isfinite(float(value))
    )
    if not finite:
        return None, None
    if len(finite) == 1:
        return finite[0], finite[0]
    q1, _, q3 = statistics.quantiles(finite, n=4, method="inclusive")
    return q1, q3


def aggregate_rows(
    rows: list[dict[str, Any]],
    amplitudes: list[float],
) -> list[dict[str, Any]]:
    metrics = [
        "knot_score",
        "memory_compactness_gain",
        "memory_radius",
        "memory_radius_over_length_unit",
        "memory_dimension",
        "memory_roundness",
        "dynamic_radius",
        "dynamic_drift_ratio",
        "covariance_dimension",
        "occupancy_window_dimension",
        "best_residence_memory_times",
    ]
    aggregate: list[dict[str, Any]] = []
    for amplitude in sorted(amplitudes):
        group = [row for row in rows if row["amplitude_att"] == amplitude]
        record: dict[str, Any] = {
            "amplitude_att": amplitude,
            "n_seeds": len(group),
            "local_curvature": _median(row.get("local_curvature") for row in group),
            "restoring_per_update": _median(
                row.get("restoring_per_update") for row in group
            ),
            "restoring_per_memory_time": _median(
                row.get("restoring_per_memory_time") for row in group
            ),
        }
        for metric in metrics:
            values = [row.get(metric) for row in group]
            record[f"{metric}_median"] = _median(values)
            q1, q3 = _quartiles(values)
            record[f"{metric}_q1"] = q1
            record[f"{metric}_q3"] = q3
        aggregate.append(record)
    return aggregate


def rank_change_intervals(aggregate: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(aggregate, key=lambda row: float(row["amplitude_att"]))
    transformed: dict[str, np.ndarray] = {}
    scales: dict[str, float] = {}
    for metric, mode in CHANGE_METRICS.items():
        values = np.asarray([float(row[metric]) for row in ordered], dtype=float)
        if mode == "log":
            values = np.log(np.maximum(values, 1.0e-300))
        transformed[metric] = values
        scale = float(np.quantile(values, 0.9) - np.quantile(values, 0.1))
        scales[metric] = scale if scale > 1.0e-15 else 1.0

    intervals: list[dict[str, Any]] = []
    for index in range(len(ordered) - 1):
        left = float(ordered[index]["amplitude_att"])
        right = float(ordered[index + 1]["amplitude_att"])
        width = right - left
        contributions = {
            metric: abs(values[index + 1] - values[index]) / scales[metric] / width
            for metric, values in transformed.items()
        }
        intervals.append(
            {
                "left": left,
                "right": right,
                "score": float(
                    np.sqrt(np.mean(np.square(list(contributions.values()))))
                ),
                "contributions": contributions,
            }
        )
    return sorted(intervals, key=lambda row: float(row["score"]), reverse=True)


def paired_reference_differences(
    rows: list[dict[str, Any]],
    reference_rows: list[dict[str, Any]],
    matched_amplitude: float,
) -> list[dict[str, Any]]:
    matched = {
        int(row["seed"]): row
        for row in rows
        if row["amplitude_att"] == matched_amplitude
    }
    reference = {int(row["seed"]): row for row in reference_rows}
    output: list[dict[str, Any]] = []
    for metric, label in PAIR_METRICS.items():
        relative: list[float] = []
        for seed, base in reference.items():
            candidate = matched.get(seed)
            if (
                candidate is None
                or base.get(metric) is None
                or candidate.get(metric) is None
            ):
                continue
            base_value = float(base[metric])
            candidate_value = float(candidate[metric])
            scale = abs(base_value)
            relative.append(
                abs(candidate_value - base_value) / scale
                if scale > 0.0
                else abs(candidate_value)
            )
        output.append(
            {
                "metric": metric,
                "label": label,
                "n_seeds": len(relative),
                "median_relative_difference": _median(relative),
                "max_relative_difference": max(relative) if relative else None,
            }
        )
    return output


def _plot(
    *,
    args: argparse.Namespace,
    rows: list[dict[str, Any]],
    reference_rows: list[dict[str, Any]],
    control_rows: list[dict[str, Any]],
    aggregate: list[dict[str, Any]],
    output: Path,
) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(13.2, 7.8))
    seeds = sorted({int(row["seed"]) for row in rows})
    colors = plt.get_cmap("tab10")
    factor = args.eta * args.memory_mass / (args.alpha * args.sigma_att**2)

    for axis, (metric, label) in zip(axes.flat, METRICS.items(), strict=True):
        for index, seed in enumerate(seeds):
            seed_rows = sorted(
                (row for row in rows if int(row["seed"]) == seed),
                key=lambda row: float(row["amplitude_att"]),
            )
            axis.plot(
                [factor * float(row["amplitude_att"]) for row in seed_rows],
                [float(row[metric]) for row in seed_rows],
                color=colors(index % 10),
                alpha=0.28,
                linewidth=0.9,
            )
        valid = [row for row in aggregate if row.get(f"{metric}_median") is not None]
        axis.plot(
            [float(row["restoring_per_memory_time"]) for row in valid],
            [float(row[f"{metric}_median"]) for row in valid],
            color="#202020",
            linewidth=2.2,
            label="attractive-only median",
        )
        control = _median(row.get(metric) for row in control_rows)
        if control is not None:
            axis.axhline(
                control,
                color="#777777",
                linestyle="--",
                linewidth=1.2,
                label="eta=0 median",
            )
        reference = _median(row.get(metric) for row in reference_rows)
        if reference is not None:
            axis.scatter(
                factor * args.matched_amplitude_att,
                reference,
                marker="*",
                s=90,
                color="#c23b22",
                zorder=5,
                label="two-scale (1,35)",
            )
        axis.axvline(
            factor * args.matched_amplitude_att,
            color="#147d64",
            linestyle=":",
            linewidth=1.0,
        )
        axis.set_xlabel("g_tau = eta M0 kappa / lambda")
        axis.set_ylabel(label)
        axis.grid(True, alpha=0.22)
        if metric in {"memory_radius", "dynamic_radius", "dynamic_drift_ratio"}:
            axis.set_yscale("log")
        secondary = axis.secondary_xaxis(
            "top",
            functions=(
                lambda value, factor=factor: value / factor,
                lambda value, factor=factor: value * factor,
            ),
        )
        secondary.set_xlabel("A_att")
        axis.legend(frameon=False, fontsize=7)
    fig.suptitle(
        "Attractive-only scalar screening scan: seed paths, medians, and matched reference"
    )
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=190)
    plt.close(fig)


def _fmt(value: Any, digits: int = 4) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if not math.isfinite(number):
        return "n/a"
    if number == 0.0:
        return "0"
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.{digits}e}"
    return f"{number:.{digits}f}"


def write_outputs(
    *,
    args: argparse.Namespace,
    rows: list[dict[str, Any]],
    reference_rows: list[dict[str, Any]],
    control_rows: list[dict[str, Any]],
    null_exact: bool,
    elapsed_seconds: float,
) -> None:
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    source_git_revision = _git_output(["rev-parse", "HEAD"])
    source_git_status = _git_output(["status", "--short"])
    aggregate = aggregate_rows(rows, args.amplitudes)
    changes = rank_change_intervals(aggregate)
    paired = paired_reference_differences(
        rows,
        reference_rows,
        args.matched_amplitude_att,
    )
    _plot(
        args=args,
        rows=rows,
        reference_rows=reference_rows,
        control_rows=control_rows,
        aggregate=aggregate,
        output=figure,
    )
    generated = _utc_now()
    payload = {
        "description": "Attractive-only scalar A_att screening and matched ablation.",
        "generated_utc": generated,
        "git_revision": source_git_revision,
        "git_status": source_git_status,
        "elapsed_seconds": elapsed_seconds,
        "arguments": {
            key: str(value) if isinstance(value, Path) else value
            for key, value in vars(args).items()
        },
        "aggregate": aggregate,
        "change_intervals": changes,
        "matched_reference_differences": paired,
        "acceptance": {
            "A_att_zero_matches_eta_zero_bitwise": null_exact,
            "old_local_sign_boundary_removed": True,
        },
    }
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Attractive-Only Scalar Regime Scan",
        "",
        f"Date: {generated}.",
        "",
        "## Scope",
        "",
        f"Screening run with `N={args.steps:,}`, seeds `{','.join(str(seed) for seed in args.seeds)}`,",
        f"`d={args.dim}`, `epsilon={args.epsilon:g}`, `eta={args.eta:g}`,",
        f"`lambda={args.alpha:g}`, `M0={args.memory_mass:g}`, delta deposition,",
        f"`A_rep=0`, `sigma_att={args.sigma_att:g}`, and `A_att=0..40`.",
        "`A_att=0` is an implementation null; the requested physical scan is",
        "`1..40`. This is a screening run, not long-run phase evidence.",
        "",
        "Without `A_rep`, every `A_att>0` has positive local restoring curvature.",
        "The former sign boundary near `A_att=9` is therefore absent analytically.",
        "Intervals below are ranked empirical KPI changes, not pre-labelled phase",
        "transitions.",
        "",
        f"![Attractive-only regime scan]({_rel_from(report, figure)})",
        "",
        "## Aggregate",
        "",
        "| A_att | kappa | g/update | g/tau_mem | score | compact gain | R_mem/L_att | D_mem | roundness | dyn R | drift/R |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in aggregate:
        lines.append(
            f"| {_fmt(row['amplitude_att'])} | {_fmt(row['local_curvature'])} | "
            f"{_fmt(row['restoring_per_update'])} | {_fmt(row['restoring_per_memory_time'])} | "
            f"{_fmt(row['knot_score_median'])} | {_fmt(row['memory_compactness_gain_median'])} | "
            f"{_fmt(row['memory_radius_over_length_unit_median'])} | "
            f"{_fmt(row['memory_dimension_median'])} | {_fmt(row['memory_roundness_median'])} | "
            f"{_fmt(row['dynamic_radius_median'])} | {_fmt(row['dynamic_drift_ratio_median'])} |"
        )
    lines.extend(
        [
            "",
            "## Matched ablation",
            "",
            f"The attractive-only `A_att={args.matched_amplitude_att:g}` branch and",
            f"the two-scale `(A_rep,A_att)=({args.reference_amplitude_rep:g},{args.reference_amplitude_att:g})`",
            "reference have equal point-deposit curvature and share seed-matched",
            "noise and controls.",
            "",
            "| KPI | seeds | median relative difference | max relative difference |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for row in paired:
        lines.append(
            f"| {row['label']} | {row['n_seeds']} | "
            f"{_fmt(row['median_relative_difference'])} | {_fmt(row['max_relative_difference'])} |"
        )
    lines.extend(
        [
            "",
            "## Highest empirical change intervals",
            "",
            "| rank | A_att interval | normalized change score | dominant KPI | contribution |",
            "| ---: | --- | ---: | --- | ---: |",
        ]
    )
    for rank, row in enumerate(changes[:8], start=1):
        dominant, contribution = max(
            row["contributions"].items(),
            key=lambda item: float(item[1]),
        )
        lines.append(
            f"| {rank} | [{_fmt(row['left'])}, {_fmt(row['right'])}] | "
            f"{_fmt(row['score'])} | {dominant} | {_fmt(contribution)} |"
        )
    lines.extend(
        [
            "",
            "## Decision gate",
            "",
            f"- `A_att=0` baseline is bitwise equal to shared `eta=0`: `{null_exact}`.",
            "- Only an interval with a seed-consistent raw-KPI change, not merely a",
            "  KnotScore threshold crossing, qualifies for a denser `N=1M` retest.",
            "- If the curves are smooth, the correct conclusion is a continuous",
            "  stiffness/noise response and no detected finite-A phase transition.",
            "- The matched `A_att=26` comparison decides whether `A_rep` is",
            "  dynamically identifiable in the currently sampled Taylor regime.",
            "",
            "## Provenance",
            "",
            f"- Runtime: `{elapsed_seconds:.2f} s`",
            f"- Git revision: `{payload['git_revision']}`",
            f"- Git status: `{payload['git_status'] or 'clean'}`",
            "- Raw cases: `data/processed/kernel_core/` (ignored bulk data)",
            "- Script: `experiments/current/kernels/attractive_only_regime_scan.py`",
            "",
        ]
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    _validate_args(args)
    output_dir = _resolve(args.output_dir)
    started = time.perf_counter()
    rows, reference_rows, control_rows, null_exact = run_or_load_cases(
        args,
        output_dir,
    )
    write_outputs(
        args=args,
        rows=rows,
        reference_rows=reference_rows,
        control_rows=control_rows,
        null_exact=null_exact,
        elapsed_seconds=time.perf_counter() - started,
    )


if __name__ == "__main__":
    main()
