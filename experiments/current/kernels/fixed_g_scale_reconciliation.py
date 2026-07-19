from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import statistics
import subprocess
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
METRICS = (
    "fixed_voxel_residence",
    "comoving_max_run_memory_times",
    "comoving_inside_fraction",
    "x_distance_to_rms_radius",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Reconcile fixed-voxel and co-moving residence diagnostics for "
            "the pre-registered fixed-g scalar radius gate."
        )
    )
    parser.add_argument(
        "--source-summary",
        type=Path,
        default=Path(
            "reports/kernels/nonlinearity/fixed_g_RL_d3_N300k_A26_2026-07-19.json"
        ),
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path(
            "data/processed/kernel_core/fixed_g_RL_d3_N300k_seed1-5_A26_2026-07-19"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/kernels/nonlinearity/"
            "fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/kernels/nonlinearity/"
            "fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/kernels/nonlinearity_2026-07-19/"
            "fixed_g_scale_reconciliation_d3_N300k_A26.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _token(value: float) -> str:
    return f"RL{value:.8g}".replace(".", "p").replace("-", "m")


def _finite(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


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


def extract_dynamic_metrics(case: dict[str, Any]) -> dict[str, float]:
    diagnostics = case.get("diagnostics")
    if not isinstance(diagnostics, dict):
        raise ValueError("case has no diagnostics")
    dynamic = diagnostics.get("dynamic_center_trace")
    if not isinstance(dynamic, dict):
        raise ValueError("case has no dynamic_center_trace")
    keys = {
        "comoving_max_run_memory_times": "max_run_memory_times",
        "comoving_inside_fraction": "comoving_inside_fraction_time_weighted",
        "x_distance_to_rms_radius": "x_distance_to_rms_radius_median",
    }
    output: dict[str, float] = {}
    for output_key, source_key in keys.items():
        value = _finite(dynamic.get(source_key))
        if value is None:
            raise ValueError(f"dynamic_center_trace lacks {source_key}")
        output[output_key] = value
    return output


def _case_path(
    source_dir: Path,
    *,
    target: float,
    condition: str,
    seed: int,
    steps: int,
) -> Path:
    return (
        source_dir / _token(target) / f"case_{condition}_seed{seed}_steps{steps}.json"
    )


def load_records(summary: dict[str, Any], source_dir: Path) -> list[dict[str, Any]]:
    arguments = summary["arguments"]
    steps = int(arguments["steps"])
    records: list[dict[str, Any]] = []
    for condition, source_key in (
        ("baseline", "active_rows"),
        ("eta_zero", "control_rows"),
    ):
        for source_row in summary[source_key]:
            target = float(source_row["target_radius_ratio"])
            seed = int(source_row["seed"])
            path = _case_path(
                source_dir,
                target=target,
                condition=condition,
                seed=seed,
                steps=steps,
            )
            if not path.exists():
                raise FileNotFoundError(path)
            case = json.loads(path.read_text(encoding="utf-8"))
            records.append(
                {
                    "condition": condition,
                    "target_radius_ratio": target,
                    "seed": seed,
                    "fixed_voxel_residence": source_row["best_residence_memory_times"],
                    **extract_dynamic_metrics(case),
                }
            )
    return records


def aggregate_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    conditions = sorted({str(row["condition"]) for row in records})
    targets = sorted({float(row["target_radius_ratio"]) for row in records})
    for condition in conditions:
        for target in targets:
            group = [
                row
                for row in records
                if row["condition"] == condition
                and row["target_radius_ratio"] == target
            ]
            result: dict[str, Any] = {
                "condition": condition,
                "target_radius_ratio": target,
                "n_seeds": len(group),
            }
            for metric in METRICS:
                result[f"{metric}_median"] = _median(row.get(metric) for row in group)
                low, high = _quartiles(row.get(metric) for row in group)
                result[f"{metric}_q1"] = low
                result[f"{metric}_q3"] = high
            output.append(result)
    return output


def endpoint_changes(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    targets = sorted({float(row["target_radius_ratio"]) for row in records})
    low, high = targets[0], targets[-1]
    output: list[dict[str, Any]] = []
    for condition in sorted({str(row["condition"]) for row in records}):
        for seed in sorted({int(row["seed"]) for row in records}):
            low_row = next(
                row
                for row in records
                if row["condition"] == condition
                and row["seed"] == seed
                and row["target_radius_ratio"] == low
            )
            high_row = next(
                row
                for row in records
                if row["condition"] == condition
                and row["seed"] == seed
                and row["target_radius_ratio"] == high
            )
            fixed_low = _finite(low_row["fixed_voxel_residence"])
            fixed_high = _finite(high_row["fixed_voxel_residence"])
            moving_low = float(low_row["comoving_max_run_memory_times"])
            moving_high = float(high_row["comoving_max_run_memory_times"])
            output.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "fixed_voxel_log2_ratio": (
                        math.log2(fixed_high / fixed_low)
                        if fixed_low not in (None, 0.0)
                        and fixed_high not in (None, 0.0)
                        else None
                    ),
                    "comoving_log2_ratio": math.log2(moving_high / moving_low),
                    "comoving_inside_fraction_change": float(
                        high_row["comoving_inside_fraction"]
                        - low_row["comoving_inside_fraction"]
                    ),
                    "x_distance_to_rms_radius_change": float(
                        high_row["x_distance_to_rms_radius"]
                        - low_row["x_distance_to_rms_radius"]
                    ),
                }
            )
    return output


def scale_aware_reading(
    source_summary: dict[str, Any], changes: list[dict[str, Any]]
) -> dict[str, Any]:
    active_changes = [row for row in changes if row["condition"] == "baseline"]
    source_decision = source_summary["decision"]
    endpoint_rows = source_summary["endpoint_seed_pairs"]
    radius_departure = float(source_decision["median_absolute_radius_departure"])
    dimension_change = abs(
        float(_median(row["memory_dimension_change"] for row in endpoint_rows) or 0.0)
    )
    roundness_change = abs(
        float(_median(row["memory_roundness_change"] for row in endpoint_rows) or 0.0)
    )
    moving_log_change = abs(
        float(_median(row["comoving_log2_ratio"] for row in active_changes) or 0.0)
    )
    inside_change = abs(
        float(
            _median(row["comoving_inside_fraction_change"] for row in active_changes)
            or 0.0
        )
    )
    stable_shape = dimension_change < 0.25 and roundness_change < 0.10
    stable_comoving = moving_log_change < 0.25 and inside_change < 0.01
    if radius_departure <= 0.10 and stable_shape and stable_comoving:
        reading = "weak_smooth_correction_without_metastable_transition"
    else:
        reading = "unresolved_after_scale_reconciliation"
    return {
        "pre_registered_classification": source_decision["classification"],
        "post_hoc_reading": reading,
        "median_absolute_radius_departure": radius_departure,
        "median_absolute_memory_dimension_change": dimension_change,
        "median_absolute_memory_roundness_change": roundness_change,
        "median_absolute_comoving_log2_change": moving_log_change,
        "median_absolute_comoving_inside_fraction_change": inside_change,
        "stable_shape": stable_shape,
        "stable_comoving_residence": stable_comoving,
    }


def _plot_series(
    axis: plt.Axes,
    rows: list[dict[str, Any]],
    metric: str,
    *,
    condition: str,
    label: str,
    color: str,
    marker: str,
) -> None:
    selected = [row for row in rows if row["condition"] == condition]
    x = np.asarray([float(row["target_radius_ratio"]) for row in selected])
    y = np.asarray([float(row[f"{metric}_median"]) for row in selected])
    low = np.asarray([float(row[f"{metric}_q1"]) for row in selected])
    high = np.asarray([float(row[f"{metric}_q3"]) for row in selected])
    axis.errorbar(
        x,
        y,
        yerr=np.vstack([y - low, high - y]),
        label=label,
        color=color,
        marker=marker,
        linewidth=1.8,
        capsize=3,
    )


def _plot(rows: list[dict[str, Any]], output: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))
    for condition, label, color, marker in (
        ("baseline", "active", "#176b87", "o"),
        ("eta_zero", "eta=0", "#777777", "s"),
    ):
        _plot_series(
            axes[0],
            rows,
            "fixed_voxel_residence",
            condition=condition,
            label=label,
            color=color,
            marker=marker,
        )
        _plot_series(
            axes[1],
            rows,
            "comoving_max_run_memory_times",
            condition=condition,
            label=label,
            color=color,
            marker=marker,
        )
        _plot_series(
            axes[2],
            rows,
            "x_distance_to_rms_radius",
            condition=condition,
            label=label,
            color=color,
            marker=marker,
        )
    axes[0].set_title("Fixed-voxel residence")
    axes[0].set_ylabel("best residence [memory times]")
    axes[1].set_title("Co-moving residence")
    axes[1].set_ylabel("max run [memory times]")
    axes[1].set_yscale("log")
    axes[2].set_title("Relative center distance")
    axes[2].set_ylabel("median |x-center| / RMS radius")
    for axis in axes:
        axis.set_xscale("log")
        axis.set_xlabel("target active R_linear / L")
        axis.grid(True, alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Residence scale reconciliation")
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


def write_outputs(args: argparse.Namespace) -> None:
    source_summary_path = _resolve(args.source_summary)
    source_dir = _resolve(args.source_dir)
    report = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    source_revision = _git_output(["rev-parse", "HEAD"])
    source_status = _git_output(["status", "--short"])
    source_summary = json.loads(source_summary_path.read_text(encoding="utf-8"))
    records = load_records(source_summary, source_dir)
    aggregate = aggregate_records(records)
    changes = endpoint_changes(records)
    reading = scale_aware_reading(source_summary, changes)
    arguments = source_summary["arguments"]
    length = float(arguments["sigma_att"])
    voxel_sizes = [float(value) for value in arguments["voxel_sizes"]]
    targets = sorted({float(row["target_radius_ratio"]) for row in records})
    voxel_audit = [
        {
            "target_radius_ratio": target,
            "predicted_radius": target * length,
            "voxel_over_predicted_radius": [
                voxel / (target * length) for voxel in voxel_sizes
            ],
        }
        for target in targets
    ]
    _plot(aggregate, figure)
    generated = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    payload = {
        "description": "Post-hoc residence scale reconciliation.",
        "generated_utc": generated,
        "git_revision": source_revision,
        "git_status": source_status,
        "source_summary": str(args.source_summary),
        "source_summary_revision": source_summary["git_revision"],
        "records": records,
        "aggregate": aggregate,
        "endpoint_changes": changes,
        "voxel_scale_audit": voxel_audit,
        "reading": reading,
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )
    lines = [
        "# Fixed-g Residence Scale Reconciliation",
        "",
        f"Date: {generated}.",
        "",
        "## Scope",
        "",
        "This is a post-hoc measurement audit of the pre-registered fixed-g",
        "run. It does not replace its `inconclusive` classification. It asks",
        "whether the supporting KnotScore/residence changes are independent",
        "of the deliberately changed trajectory radius.",
        "",
        f"![Residence scale reconciliation]({_rel_from(report, figure)})",
        "",
        "## Voxel scale audit",
        "",
        "| target R/L | predicted R | fixed voxel sizes / predicted R |",
        "| ---: | ---: | --- |",
    ]
    for row in voxel_audit:
        ratios = ", ".join(_fmt(value) for value in row["voxel_over_predicted_radius"])
        lines.append(
            f"| {_fmt(row['target_radius_ratio'])} | "
            f"{_fmt(row['predicted_radius'])} | {ratios} |"
        )
    lines.extend(
        [
            "",
            "## Scale-aware observables",
            "",
            "| condition | target R/L | fixed-voxel residence | co-moving max run | co-moving inside fraction | median distance/RMS radius |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in aggregate:
        lines.append(
            f"| {row['condition']} | {_fmt(row['target_radius_ratio'])} | "
            f"{_fmt(row['fixed_voxel_residence_median'])} | "
            f"{_fmt(row['comoving_max_run_memory_times_median'])} | "
            f"{_fmt(row['comoving_inside_fraction_median'])} | "
            f"{_fmt(row['x_distance_to_rms_radius_median'])} |"
        )
    lines.extend(
        [
            "",
            "## Reading",
            "",
            f"Pre-registered classification: **{reading['pre_registered_classification']}**.",
            f"Post-hoc reading: **{reading['post_hoc_reading']}**.",
            "",
            f"The endpoint radius departure is `{_fmt(reading['median_absolute_radius_departure'])}`.",
            f"Median absolute D_mem and roundness changes are `{_fmt(reading['median_absolute_memory_dimension_change'])}` and `{_fmt(reading['median_absolute_memory_roundness_change'])}`.",
            f"The active co-moving max-run log2 change is `{_fmt(reading['median_absolute_comoving_log2_change'])}`.",
            "",
            "Fixed-voxel residence is strongly radius-dependent here. The",
            "co-moving residence is stable, but it is equally saturated for",
            "the eta=0 controls and is therefore not discriminating. KnotScore",
            "v0.5 includes fixed-voxel residence and voxel-stability components;",
            "its endpoint drop is not independent evidence for a new regime.",
            "The seed-stable 6% superlinear radius growth is consistent with a",
            "weak smooth finite-Gaussian correction; no shape transition or",
            "metastable branch is isolated by this gate.",
            "",
            "## Decision",
            "",
            "Do not launch another scalar amplitude or epsilon sweep from this",
            "result. Keep the attractive-only scalar model as a controlled",
            "relaxation baseline and advance the separately defined dynamic-field",
            "pilot. Future variable-scale scores must normalize spatial bins or",
            "report their scale dependence explicitly.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{source_revision}`",
            f"- Git status: `{source_status or 'clean'}`",
            f"- Source summary: `{args.source_summary.as_posix()}`",
            "",
        ]
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_outputs(parse_args())


if __name__ == "__main__":
    main()
