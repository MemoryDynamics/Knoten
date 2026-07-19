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
from types import SimpleNamespace
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

from emergenz_knoten import SimulationConfig, two_scale_local_curvature  # noqa: E402

import attractive_only_regime_scan as single_scan  # noqa: E402
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
            "Compare attractive-only and curvature-matched two-scale scalar "
            "kernels on raw-amplitude and effective-curvature axes."
        )
    )
    parser.add_argument("--steps", type=int, default=300_000)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument(
        "--seeds", type=_parse_int_list, default=_parse_int_list("1,2,3,4,5")
    )
    parser.add_argument(
        "--effective-amplitudes",
        type=_parse_float_list,
        default=_parse_float_list("0,1,3,5,6,8,11,16,26,31"),
    )
    parser.add_argument("--epsilon", type=float, default=1.0e-4)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
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
    parser.add_argument("--score-threshold", type=float, default=0.75)
    parser.add_argument("--skip-run", action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument(
        "--single-source-dir",
        type=Path,
        default=Path(
            "data/processed/kernel_core/"
            "attractive_only_A0-40_d3_N300k_seed1-5_eps1em4_2026-07-18"
        ),
    )
    parser.add_argument(
        "--single-summary",
        type=Path,
        default=Path(
            "reports/kernels/core/attractive_only_regime_scan_d3_N300k_2026-07-18.json"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "data/processed/kernel_core/"
            "kernel_family_comparison_d3_N300k_seed1-5_eps1em4_2026-07-19"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.json"
        ),
    )
    parser.add_argument(
        "--figure-raw",
        type=Path,
        default=Path(
            "figures/draft/kernels/core_2026-07-19/kernel_family_comparison_raw.png"
        ),
    )
    parser.add_argument(
        "--figure-effective",
        type=Path,
        default=Path(
            "figures/draft/kernels/core_2026-07-19/"
            "kernel_family_comparison_effective.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _token(value: float) -> str:
    return f"Aeff{value:.8g}".replace(".", "p").replace("-", "m")


def effective_attractive_amplitude(
    *,
    amplitude_att: float,
    amplitude_rep: float,
    sigma_rep: float,
    sigma_att: float,
) -> float:
    """Return the attractive-only amplitude with the same local curvature."""

    curvature = two_scale_local_curvature(
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )
    return float(curvature * sigma_att**2)


def two_scale_amplitude_for_effective(
    *,
    effective_amplitude: float,
    amplitude_rep: float,
    sigma_rep: float,
    sigma_att: float,
) -> float:
    return float(effective_amplitude + amplitude_rep * (sigma_att / sigma_rep) ** 2)


def _validate_args(args: argparse.Namespace) -> None:
    if args.steps < 1 or args.dim < 1:
        raise SystemExit("--steps and --dim must be positive")
    if args.burn_in < 0 or args.burn_in >= args.steps:
        raise SystemExit("--burn-in must satisfy 0 <= burn_in < steps")
    if args.sample_every < 1 or args.trace_points < 2:
        raise SystemExit("sampling values must be positive and trace-points >= 2")
    if any(value < 0.0 for value in args.effective_amplitudes):
        raise SystemExit("effective amplitudes must be non-negative")
    if len(set(args.effective_amplitudes)) != len(args.effective_amplitudes):
        raise SystemExit("effective amplitudes must not contain duplicates")
    for name in ("sigma_rep", "sigma_att", "eta", "alpha", "memory_mass"):
        value = float(getattr(args, name))
        if value <= 0.0 or not math.isfinite(value):
            raise SystemExit(f"--{name.replace('_', '-')} must be positive and finite")
    if args.alpha > 1.0:
        raise SystemExit("--alpha must not exceed one")
    if args.amplitude_rep < 0.0 or not math.isfinite(args.amplitude_rep):
        raise SystemExit("--amplitude-rep must be non-negative and finite")
    if not 0.0 <= args.score_threshold <= 1.0:
        raise SystemExit("--score-threshold must lie in [0,1]")


def _config(
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


def _load_args(args: argparse.Namespace) -> SimpleNamespace:
    values = vars(args).copy()
    values["skip_run"] = True
    values["no_resume"] = False
    return SimpleNamespace(**values)


def run_or_load_rows(
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    single_source = _resolve(args.single_source_dir)
    output_dir = _resolve(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    trace_targets = metastability_run._trace_targets(
        steps=args.steps,
        burn_in=args.burn_in,
        trace_every=0,
        trace_points=args.trace_points,
        trace_spacing="log",
    )
    load_args = _load_args(args)
    controls: dict[int, dict[str, Any]] = {}
    null_config = _config(args, amplitude_rep=0.0, amplitude_att=0.0)
    for seed in args.seeds:
        controls[seed] = common._run_or_load(
            config=null_config,
            condition="eta_zero",
            seed=seed,
            directory=single_source / "shared_eta_zero",
            args=load_args,
            trace_targets=trace_targets,
        )

    single_rows: list[dict[str, Any]] = []
    two_scale_rows: list[dict[str, Any]] = []
    for effective in sorted(args.effective_amplitudes):
        single_config = _config(
            args,
            amplitude_rep=0.0,
            amplitude_att=effective,
        )
        two_amplitude = two_scale_amplitude_for_effective(
            effective_amplitude=effective,
            amplitude_rep=args.amplitude_rep,
            sigma_rep=args.sigma_rep,
            sigma_att=args.sigma_att,
        )
        two_config = _config(
            args,
            amplitude_rep=args.amplitude_rep,
            amplitude_att=two_amplitude,
        )
        for seed in args.seeds:
            single_case = common._run_or_load(
                config=single_config,
                condition="baseline",
                seed=seed,
                directory=single_source / single_scan._token(effective),
                args=load_args,
                trace_targets=trace_targets,
            )
            single_row = single_scan._row(
                single_case,
                amplitude_att=effective,
                control=controls[seed],
                args=args,
                family="attractive_only",
            )
            single_row["effective_amplitude"] = effective
            single_rows.append(single_row)

            two_case = common._run_or_load(
                config=two_config,
                condition="baseline",
                seed=seed,
                directory=output_dir / _token(effective),
                args=args,
                trace_targets=trace_targets,
            )
            two_row = single_scan._row(
                two_case,
                amplitude_att=two_amplitude,
                control=controls[seed],
                args=args,
                family="two_scale",
            )
            two_row["effective_amplitude"] = effective
            two_scale_rows.append(two_row)
    return single_rows, two_scale_rows


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
    effective_amplitudes: list[float],
) -> list[dict[str, Any]]:
    aggregate: list[dict[str, Any]] = []
    for effective in sorted(effective_amplitudes):
        group = [row for row in rows if row["effective_amplitude"] == effective]
        if not group:
            continue
        record: dict[str, Any] = {
            "family": group[0]["family"],
            "effective_amplitude": effective,
            "amplitude_att": _median(row["amplitude_att"] for row in group),
            "local_curvature": _median(row["local_curvature"] for row in group),
            "n_seeds": len(group),
        }
        for metric in METRICS:
            record[f"{metric}_median"] = _median(row.get(metric) for row in group)
            low, high = _quartiles(row.get(metric) for row in group)
            record[f"{metric}_q1"] = low
            record[f"{metric}_q3"] = high
        aggregate.append(record)
    return aggregate


def paired_family_differences(
    single_rows: list[dict[str, Any]],
    two_scale_rows: list[dict[str, Any]],
    *,
    minimum_effective_amplitude: float = 1.0,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for metric, label in METRICS.items():
        differences: list[float] = []
        for single in single_rows:
            effective = float(single["effective_amplitude"])
            if effective < minimum_effective_amplitude or single.get(metric) is None:
                continue
            match = next(
                (
                    row
                    for row in two_scale_rows
                    if row["effective_amplitude"] == effective
                    and row["seed"] == single["seed"]
                ),
                None,
            )
            if match is None or match.get(metric) is None:
                continue
            left = float(single[metric])
            right = float(match[metric])
            scale = max(abs(left), abs(right), 1.0e-300)
            differences.append(abs(left - right) / scale)
        output.append(
            {
                "metric": metric,
                "label": label,
                "n_pairs": len(differences),
                "median_relative_difference": _median(differences),
                "max_relative_difference": max(differences) if differences else None,
            }
        )
    return output


def first_threshold_crossing(
    aggregate: list[dict[str, Any]],
    *,
    threshold: float,
) -> dict[str, float] | None:
    for row in sorted(aggregate, key=lambda item: float(item["amplitude_att"])):
        score = row.get("knot_score_median")
        if score is not None and float(score) >= threshold:
            return {
                "amplitude_att": float(row["amplitude_att"]),
                "effective_amplitude": float(row["effective_amplitude"]),
                "score": float(score),
            }
    return None


def _plot(
    *,
    single_full: list[dict[str, Any]],
    two_scale: list[dict[str, Any]],
    x_mode: str,
    output: Path,
    raw_boundary: float,
) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(13.2, 7.8))
    x_key = "amplitude_att" if x_mode == "raw" else "effective_amplitude"
    xlabel = "raw A_att" if x_mode == "raw" else "A_eff = sigma_att^2 kappa"
    families = [
        (single_full, "attractive-only", "#176b87", "-", "o"),
        (two_scale, "two-scale", "#c74b36", "--", "s"),
    ]
    for axis, (metric, label) in zip(axes.flat, METRICS.items(), strict=True):
        for rows, family, color, linestyle, marker in families:
            valid = [
                row
                for row in rows
                if row.get(f"{metric}_median") is not None
                and (x_mode != "effective" or float(row[x_key]) >= 0.0)
            ]
            valid.sort(key=lambda row: float(row[x_key]))
            if not valid:
                continue
            x = np.asarray([float(row[x_key]) for row in valid])
            y = np.asarray([float(row[f"{metric}_median"]) for row in valid])
            axis.plot(
                x,
                y,
                color=color,
                linestyle=linestyle,
                marker=marker,
                markersize=4.0,
                linewidth=2.0,
                label=family,
            )
        if x_mode == "raw":
            axis.axvline(
                raw_boundary,
                color="#777777",
                linestyle=":",
                linewidth=1.2,
                label="two-scale local boundary",
            )
        else:
            axis.axvline(0.0, color="#777777", linestyle=":", linewidth=1.2)
        if metric in {"memory_radius", "dynamic_radius", "dynamic_drift_ratio"}:
            axis.set_yscale("log")
        axis.set_xlabel(xlabel)
        axis.set_ylabel(label)
        axis.grid(True, alpha=0.22)
        axis.legend(frameon=False, fontsize=7)
    title_axis = "raw amplitude" if x_mode == "raw" else "matched local curvature"
    fig.suptitle(f"Attractive-only vs two-scale scalar kernels: {title_axis}")
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
    single_rows: list[dict[str, Any]],
    two_scale_rows: list[dict[str, Any]],
    invocation_elapsed_seconds: float,
) -> None:
    report = _resolve(args.report)
    summary_json = _resolve(args.summary_json)
    figure_raw = _resolve(args.figure_raw)
    figure_effective = _resolve(args.figure_effective)
    source = json.loads(_resolve(args.single_summary).read_text(encoding="utf-8"))
    single_full = source["aggregate"]
    for row in single_full:
        row["effective_amplitude"] = float(row["amplitude_att"])
    single_aggregate = aggregate_rows(single_rows, args.effective_amplitudes)
    two_aggregate = aggregate_rows(two_scale_rows, args.effective_amplitudes)
    paired = paired_family_differences(single_rows, two_scale_rows)
    raw_boundary = args.amplitude_rep * (args.sigma_att / args.sigma_rep) ** 2
    _plot(
        single_full=single_full,
        two_scale=two_aggregate,
        x_mode="raw",
        output=figure_raw,
        raw_boundary=raw_boundary,
    )
    _plot(
        single_full=single_full,
        two_scale=two_aggregate,
        x_mode="effective",
        output=figure_effective,
        raw_boundary=raw_boundary,
    )
    single_crossing = first_threshold_crossing(
        single_full,
        threshold=args.score_threshold,
    )
    two_crossing = first_threshold_crossing(
        two_aggregate,
        threshold=args.score_threshold,
    )
    all_case_rows = [*single_rows, *two_scale_rows]
    generated = _utc_now()
    payload = {
        "description": "Matched attractive-only and two-scale kernel comparison.",
        "generated_utc": generated,
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "arguments": {
            key: str(value) if isinstance(value, Path) else value
            for key, value in vars(args).items()
        },
        "raw_two_scale_local_boundary": raw_boundary,
        "single_support": single_aggregate,
        "two_scale_support": two_aggregate,
        "paired_differences_effective_amplitude_ge_1": paired,
        "descriptive_score_crossings": {
            "threshold": args.score_threshold,
            "attractive_only": single_crossing,
            "two_scale": two_crossing,
        },
        "source_single_summary_revision": source.get("git_revision"),
        "active_family_case_count": len(all_case_rows),
        "shared_control_case_count": len(args.seeds),
        "summed_case_compute_seconds": sum(
            float(row.get("case_elapsed_seconds", 0.0)) for row in all_case_rows
        ),
        "invocation_elapsed_seconds": invocation_elapsed_seconds,
    }
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )

    lines = [
        "# Scalar Kernel Family Comparison",
        "",
        f"Date: {generated}.",
        "",
        "## Scope",
        "",
        f"Seed-matched comparison at `N={args.steps:,}`, `d={args.dim}`,",
        f"`epsilon={args.epsilon:g}`, `eta={args.eta:g}`, `lambda={args.alpha:g}`,",
        f"`M0={args.memory_mass:g}`, delta deposition, and seeds",
        f"`{','.join(str(seed) for seed in args.seeds)}`.",
        "",
        "The attractive-only family uses `A_rep=0`. The two-scale family uses",
        f"`A_rep={args.amplitude_rep:g}`, `sigma_rep={args.sigma_rep:g}`, and",
        f"`sigma_att={args.sigma_att:g}`. Local-curvature matching gives",
        "",
        "```text",
        "A_eff = sigma_att^2 kappa",
        f"      = A_att - {raw_boundary:g}",
        "```",
        "",
        "for the two-scale branch. The raw-amplitude plot shows the horizontal",
        "offset; the effective-amplitude plot tests curve collapse at equal local",
        "restoring curvature.",
        "",
        f"![Raw amplitude comparison]({_rel_from(report, figure_raw)})",
        "",
        f"![Effective amplitude comparison]({_rel_from(report, figure_effective)})",
        "",
        "## Matched support points",
        "",
        "| A_eff | A_att one-scale | A_att two-scale | score one | score two | dyn R one | dyn R two | D_mem one | D_mem two |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    by_single = {float(row["effective_amplitude"]): row for row in single_aggregate}
    by_two = {float(row["effective_amplitude"]): row for row in two_aggregate}
    for effective in sorted(set(by_single) & set(by_two)):
        one = by_single[effective]
        two = by_two[effective]
        lines.append(
            f"| {_fmt(effective)} | {_fmt(one['amplitude_att'])} | {_fmt(two['amplitude_att'])} | "
            f"{_fmt(one['knot_score_median'])} | {_fmt(two['knot_score_median'])} | "
            f"{_fmt(one['dynamic_radius_median'])} | {_fmt(two['dynamic_radius_median'])} | "
            f"{_fmt(one['memory_dimension_median'])} | {_fmt(two['memory_dimension_median'])} |"
        )
    lines.extend(
        [
            "",
            "## Seed-paired collapse for A_eff >= 1",
            "",
            "| KPI | pairs | median relative difference | max relative difference |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for row in paired:
        lines.append(
            f"| {row['label']} | {row['n_pairs']} | "
            f"{_fmt(row['median_relative_difference'])} | "
            f"{_fmt(row['max_relative_difference'])} |"
        )
    lines.extend(
        [
            "",
            "## Threshold reading",
            "",
            f"The first sampled `KnotScore >= {args.score_threshold:g}` crossing is",
            f"`{single_crossing}` for the attractive-only curve and",
            f"`{two_crossing}` for the two-scale support points. This is a",
            "descriptive score crossing, not a phase transition or force-sign",
            "boundary.",
            "",
            "The analytic local restoring boundary is `A_att=0` for the",
            f"attractive-only family and `A_att={raw_boundary:g}` for the two-scale",
            "family. The historical `A_att~=7.9` drift flip was measured at",
            "`epsilon=0.03` with force-direction observables. It must not be",
            "translated into an attractive-only threshold near six.",
            "",
            "## Decision",
            "",
            "- Compare scalar families on `A_eff` or `kappa`, not raw `A_att`.",
            "- Keep `A_rep` available as an ablation, but do not treat it as",
            "  identified by the current compact branch.",
            "- Do not launch another raw-amplitude threshold search from this",
            "  comparison. Continue with the fixed-`g`, variable-`R/L` gate.",
            "",
            "## Provenance",
            "",
            f"- Active family cases represented: `{payload['active_family_case_count']}`",
            f"- Summed active per-case compute time: `{payload['summed_case_compute_seconds']:.2f} s`",
            f"- Current invocation: `{invocation_elapsed_seconds:.2f} s`",
            f"- Git revision: `{payload['git_revision']}`",
            f"- Git status: `{payload['git_status'] or 'clean'}`",
            f"- Single-family source revision: `{payload['source_single_summary_revision']}`",
            "",
        ]
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    _validate_args(args)
    started = time.perf_counter()
    single_rows, two_scale_rows = run_or_load_rows(args)
    write_outputs(
        args=args,
        single_rows=single_rows,
        two_scale_rows=two_scale_rows,
        invocation_elapsed_seconds=time.perf_counter() - started,
    )


if __name__ == "__main__":
    main()
