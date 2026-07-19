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
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    linear_memory_relative_rms_radius,
    two_scale_local_curvature,
)


SOURCE_PATTERNS = (
    "dynamic_center_trace_q3_Aatt_20_N30M_seed1-5_eps1em4_rerun_2026-07-13",
    "dynamic_center_trace_q3_Aatt_35_N30M_seed1-5_eps1em4_rerun_2026-07-13",
    "ambient_dim_memory_shape_Aatt_35_N30M_d*_seed1-5_eps1em4_2026-07-13",
    "ambient_dim_memory_shape_Aatt_35_N300M_d10_seed1-5_eps1em4_foreground_2026-07-14",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Reconcile existing long-run dynamic-center radii with the finite-"
            "memory linear relative-mode prediction."
        )
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path("data/processed/long_run_metastability"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/long_runs/scalar_hardening/"
            "linear_long_run_reconciliation_2026-07-19.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/long_runs/scalar_hardening/"
            "linear_long_run_reconciliation_2026-07-19.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/scalar_hardening/linear_reconciliation_2026-07-19/"
            "linear_long_run_reconciliation.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _rel_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


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


def retained_memory_mass(
    *, lambda_value: float, memory_mass: float, horizon: int
) -> float:
    if not 0.0 < lambda_value <= 1.0:
        raise ValueError("lambda_value must satisfy 0 < value <= 1")
    if memory_mass < 0.0 or not math.isfinite(memory_mass):
        raise ValueError("memory_mass must be non-negative and finite")
    if horizon < 1:
        raise ValueError("horizon must be positive")
    return float(memory_mass * (1.0 - (1.0 - lambda_value) ** horizon))


def _discover(source_root: Path) -> list[Path]:
    directories: list[Path] = []
    for pattern in SOURCE_PATTERNS:
        directories.extend(path for path in source_root.glob(pattern) if path.is_dir())
    unique = sorted(set(directories), key=lambda path: path.name)
    if not unique:
        raise FileNotFoundError(f"no source directories found below {source_root}")
    return unique


def _stored_mass(directory: Path, config: dict[str, Any]) -> tuple[int, float, float]:
    case_path = next(iter(sorted(directory.glob("case_baseline_seed*.json"))), None)
    if case_path is None:
        raise FileNotFoundError(f"no baseline case in {directory}")
    case = json.loads(case_path.read_text(encoding="utf-8"))
    horizon = int(case["memory_horizon"])
    recorded = float(case["stored_weight_mass"])
    calculated = retained_memory_mass(
        lambda_value=float(config["alpha"]),
        memory_mass=float(config["memory_mass"]),
        horizon=horizon,
    )
    if not math.isclose(recorded, calculated, rel_tol=1.0e-12, abs_tol=1.0e-12):
        raise ValueError(f"stored memory mass mismatch in {case_path}")
    return horizon, recorded, calculated


def _prediction(
    *,
    config: dict[str, Any],
    condition: str,
    stored_mass: float,
) -> tuple[float, float, float]:
    curvature = two_scale_local_curvature(
        sigma_rep=float(config["sigma_rep"]),
        sigma_att=float(config["sigma_att"]),
        amplitude_rep=float(config["amplitude_rep"]),
        amplitude_att=float(config["amplitude_att"]),
    )
    eta = 0.0 if condition == "eta_zero" else float(config["eta"])
    nominal_g = eta * float(config["memory_mass"]) * curvature
    retained_g = eta * stored_mass * curvature
    nominal = linear_memory_relative_rms_radius(
        epsilon=float(config["epsilon"]),
        lambda_value=float(config["alpha"]),
        restoring_per_update=nominal_g,
        dim=int(config["dim"]),
    )
    retained = linear_memory_relative_rms_radius(
        epsilon=float(config["epsilon"]),
        lambda_value=float(config["alpha"]),
        restoring_per_update=retained_g,
        dim=int(config["dim"]),
    )
    return nominal_g, nominal, retained


def load_records(source_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    sources: list[str] = []
    seen_keys: set[tuple[int, int, float, str]] = set()
    for directory in _discover(source_root):
        summary_path = directory / "summary.json"
        if not summary_path.exists():
            raise FileNotFoundError(summary_path)
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        config = summary["base_config"]
        horizon, stored_mass, _ = _stored_mass(directory, config)
        sources.append(_rel(directory))
        for condition in ("baseline", "eta_zero"):
            rows = [
                case
                for case in summary["case_summaries"]
                if case["condition"] == condition
                and case.get("dynamic_center_rms_radius_median") is not None
            ]
            if not rows:
                continue
            key_amplitude = (
                float(config["amplitude_att"]) if condition == "baseline" else 0.0
            )
            key = (
                int(config["steps"]),
                int(config["dim"]),
                key_amplitude,
                condition,
            )
            if key in seen_keys:
                if condition == "eta_zero":
                    continue
                raise ValueError(f"duplicate reconciliation slice: {key}")
            seen_keys.add(key)
            measured = [float(row["dynamic_center_rms_radius_median"]) for row in rows]
            measured_median = float(statistics.median(measured))
            measured_q1, measured_q3 = _quartiles(measured)
            nominal_g, nominal_prediction, retained_prediction = _prediction(
                config=config,
                condition=condition,
                stored_mass=stored_mass,
            )
            retained_error = (
                abs(measured_median - retained_prediction) / retained_prediction
            )
            nominal_error = (
                abs(measured_median - nominal_prediction) / nominal_prediction
            )
            records.append(
                {
                    "source": _rel(directory),
                    "condition": condition,
                    "steps": int(config["steps"]),
                    "dim": int(config["dim"]),
                    "epsilon": float(config["epsilon"]),
                    "amplitude_att": float(config["amplitude_att"]),
                    "amplitude_rep": float(config["amplitude_rep"]),
                    "sigma_att": float(config["sigma_att"]),
                    "memory_horizon": horizon,
                    "stored_memory_mass": stored_mass,
                    "n_seeds": len(rows),
                    "restoring_per_update_nominal": nominal_g,
                    "measured_radius_median": measured_median,
                    "measured_radius_q1": measured_q1,
                    "measured_radius_q3": measured_q3,
                    "nominal_prediction": nominal_prediction,
                    "retained_mass_prediction": retained_prediction,
                    "measured_over_retained_prediction": measured_median
                    / retained_prediction,
                    "nominal_relative_error": nominal_error,
                    "retained_relative_error": retained_error,
                    "predicted_radius_over_sigma_att": retained_prediction
                    / float(config["sigma_att"]),
                }
            )
    return sorted(
        records,
        key=lambda row: (
            row["condition"],
            row["steps"],
            row["amplitude_att"],
            row["dim"],
        ),
    ), sources


def _plot(records: list[dict[str, Any]], output: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14.2, 4.4))
    styles = {
        "baseline": ("#176b87", "o"),
        "eta_zero": ("#777777", "s"),
    }
    for condition, (color, marker) in styles.items():
        rows = [row for row in records if row["condition"] == condition]
        axes[0].scatter(
            [row["retained_mass_prediction"] for row in rows],
            [row["measured_radius_median"] for row in rows],
            color=color,
            marker=marker,
            s=42,
            label=condition,
        )
        axes[1].scatter(
            [row["dim"] for row in rows],
            [row["measured_over_retained_prediction"] for row in rows],
            color=color,
            marker=marker,
            s=42,
            label=condition,
        )
        axes[2].scatter(
            [row["predicted_radius_over_sigma_att"] for row in rows],
            [row["retained_relative_error"] for row in rows],
            color=color,
            marker=marker,
            s=42,
            label=condition,
        )
    all_radii = [
        float(row[key])
        for row in records
        for key in ("retained_mass_prediction", "measured_radius_median")
    ]
    lower, upper = min(all_radii), max(all_radii)
    axes[0].plot([lower, upper], [lower, upper], color="#222222", linestyle="--")
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("linear prediction with retained mass")
    axes[0].set_ylabel("measured dynamic RMS radius")
    axes[1].axhline(1.0, color="#222222", linestyle="--")
    axes[1].set_xlabel("ambient dimension d")
    axes[1].set_ylabel("measured / predicted radius")
    axes[2].set_xscale("log")
    axes[2].set_yscale("log")
    axes[2].set_xlabel("predicted R / sigma_att")
    axes[2].set_ylabel("relative prediction error")
    for axis in axes:
        axis.grid(True, alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Long-run dynamic-center radius vs linear finite-memory mode")
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
    records: list[dict[str, Any]],
    sources: list[str],
) -> None:
    report = _resolve(args.report)
    summary_json = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    source_git_revision = _git_output(["rev-parse", "HEAD"])
    source_git_status = _git_output(["status", "--short"])
    _plot(records, figure)
    baseline_errors = [
        float(row["retained_relative_error"])
        for row in records
        if row["condition"] == "baseline"
    ]
    baseline_nominal_errors = [
        float(row["nominal_relative_error"])
        for row in records
        if row["condition"] == "baseline"
    ]
    control_errors = [
        float(row["retained_relative_error"])
        for row in records
        if row["condition"] == "eta_zero"
    ]
    generated = _utc_now()
    payload = {
        "description": "Long-run finite-memory linear radius reconciliation.",
        "generated_utc": generated,
        "git_revision": source_git_revision,
        "git_status": source_git_status,
        "sources": sources,
        "records": records,
        "baseline_error_summary": {
            "n_slices": len(baseline_errors),
            "median_retained_relative_error": _median(baseline_errors),
            "max_retained_relative_error": max(baseline_errors),
            "median_nominal_relative_error": _median(baseline_nominal_errors),
            "max_nominal_relative_error": max(baseline_nominal_errors),
        },
        "eta_zero_error_summary": {
            "n_slices": len(control_errors),
            "median_retained_relative_error": _median(control_errors),
            "max_retained_relative_error": max(control_errors),
        },
        "excluded_historical_slice": {
            "steps": 300_000_000,
            "dim": 3,
            "epsilon": 0.03,
            "reason": (
                "The committed report has no compatible dynamic-center RMS radius "
                "and its original raw source was external to the repository."
            ),
        },
    }
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )
    lines = [
        "# Linear Long-Run Reconciliation",
        "",
        f"Date: {generated}.",
        "",
        "## Scope",
        "",
        "Existing dynamic-center traces are compared with the scalar linear",
        "relative-mode radius. No new long simulation is used. The active-force",
        "prediction uses the actually retained finite memory mass",
        "`M_stored=M0(1-(1-lambda)^H)` rather than silently assuming an infinite",
        "memory buffer.",
        "",
        f"![Linear long-run reconciliation]({_rel_from(report, figure)})",
        "",
        "## Baseline slices",
        "",
        "| N | d | A_att | seeds | H | M_stored | measured R | predicted R | measured/predicted | rel error | R/sigma_att |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in records:
        if row["condition"] != "baseline":
            continue
        lines.append(
            f"| {row['steps']:,} | {row['dim']} | {_fmt(row['amplitude_att'])} | "
            f"{row['n_seeds']} | {row['memory_horizon']} | "
            f"{_fmt(row['stored_memory_mass'], 7)} | "
            f"{_fmt(row['measured_radius_median'])} | "
            f"{_fmt(row['retained_mass_prediction'])} | "
            f"{_fmt(row['measured_over_retained_prediction'])} | "
            f"{_fmt(row['retained_relative_error'])} | "
            f"{_fmt(row['predicted_radius_over_sigma_att'])} |"
        )
    lines.extend(
        [
            "",
            "## Eta-zero controls",
            "",
            "| N | d | seeds | measured R | predicted R | measured/predicted | rel error |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in records:
        if row["condition"] != "eta_zero":
            continue
        lines.append(
            f"| {row['steps']:,} | {row['dim']} | {row['n_seeds']} | "
            f"{_fmt(row['measured_radius_median'])} | "
            f"{_fmt(row['retained_mass_prediction'])} | "
            f"{_fmt(row['measured_over_retained_prediction'])} | "
            f"{_fmt(row['retained_relative_error'])} |"
        )
    summary = payload["baseline_error_summary"]
    control_summary = payload["eta_zero_error_summary"]
    lines.extend(
        [
            "",
            "## Reading",
            "",
            f"Across `{summary['n_slices']}` active long-run slices the median",
            f"relative radius error is `{_fmt(summary['median_retained_relative_error'])}`",
            f"and the maximum is `{_fmt(summary['max_retained_relative_error'])}`.",
            "The retained-mass correction is reported explicitly, although it is",
            "small for the stored horizons used here.",
            "",
            "The eta-zero controls have a median relative error of",
            f"`{_fmt(control_summary['median_retained_relative_error'])}` and a",
            f"maximum of `{_fmt(control_summary['max_retained_relative_error'])}`.",
            "The formula is therefore an accurate active-branch benchmark, not an",
            "exact implementation identity for every trace estimator and finite",
            "memory condition. The next gate must also test seed-paired scaling",
            "ratios rather than relying on absolute radius error alone.",
            "",
            "The old `N=300M`, `d=3`, `epsilon=0.03` campaign is not included in",
            "the numerical radius test: its committed report has no compatible",
            "dynamic-center RMS radius and the raw source paths were external.",
            "This is a provenance gap, not evidence for or against nonlinearity.",
            "",
            "## Decision",
            "",
            "- The available small-radius long runs remain consistent with the",
            "  linear finite-memory relative mode across N and ambient dimension.",
            "- Their duration does not by itself upgrade compactness to nonlinear",
            "  metastability.",
            "- Proceed to the pre-registered fixed-g, variable-R/sigma test. A",
            "  nonlinear claim requires systematic radius, shape, residence, or",
            "  mode deviations there.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{payload['git_revision']}`",
            f"- Git status: `{payload['git_status'] or 'clean'}`",
            f"- Source directories: `{len(sources)}`",
            "",
        ]
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    source_root = _resolve(args.source_root)
    records, sources = load_records(source_root)
    write_outputs(args=args, records=records, sources=sources)


if __name__ == "__main__":
    main()
