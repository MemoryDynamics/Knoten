from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reconcile short and long scalar-memory AR closure gates."
    )
    parser.add_argument(
        "--short",
        type=Path,
        default=Path("reports/memory/low_mode_ar_feature_closure_2026-07-19.json"),
    )
    parser.add_argument(
        "--long",
        type=Path,
        default=Path(
            "reports/memory/low_mode_ar_feature_closure_long_N1M_2026-07-19.json"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/memory/low_mode_ar_long_run_reconciliation_2026-07-19.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/memory/low_mode_ar_long_run_reconciliation_2026-07-19.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/low_mode_ar_long_run_reconciliation_2026-07-19.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _load(path: Path) -> dict[str, Any]:
    return json.loads(_resolve(path).read_text(encoding="utf-8"))


def _dominant_mode(row: dict[str, Any]) -> dict[str, float] | None:
    for mode in row["top_modes"]:
        if 0.05 < mode["modulus"] < 1.0 and math.isfinite(mode["rate_per_update"]):
            return mode
    return None


def _rows(payload: dict[str, Any], ratio: float) -> list[dict[str, Any]]:
    return [
        row
        for row in payload["analyses"]
        if row["feature_group"] == "low_modes"
        and row["diffusion_length_ratio"] == ratio
    ]


def _key(row: dict[str, Any]) -> tuple[str, float]:
    return row["condition"], round(float(row["lag_memory_times"]), 12)


def _relative_change(new: float, old: float) -> float:
    if not math.isfinite(new) or not math.isfinite(old) or old == 0.0:
        return float("nan")
    return new / old - 1.0


def reconcile(short: dict[str, Any], long: dict[str, Any]) -> dict[str, Any]:
    short_ratio = float(short["gate"]["selected_ratio"])
    long_ratio = float(long["gate"]["selected_ratio"])
    if not math.isclose(short_ratio, long_ratio):
        raise ValueError("short and long gates selected different diffusion ratios")
    short_rows = {_key(row): row for row in _rows(short, short_ratio)}
    long_rows = {_key(row): row for row in _rows(long, long_ratio)}
    comparisons: list[dict[str, Any]] = []
    for key in sorted(short_rows.keys() & long_rows.keys()):
        short_row = short_rows[key]
        long_row = long_rows[key]
        short_mode = _dominant_mode(short_row)
        long_mode = _dominant_mode(long_row)
        if short_mode is None or long_mode is None:
            continue
        lambda_value = float(short["parameters"]["lambda_value"])
        short_rate = short_mode["rate_per_update"] / lambda_value
        long_rate = long_mode["rate_per_update"] / lambda_value
        comparisons.append(
            {
                "condition": key[0],
                "lag_memory_times": key[1],
                "short_closure_lift": short_row["closure_lift"],
                "long_closure_lift": long_row["closure_lift"],
                "short_rate_per_memory_time": short_rate,
                "long_rate_per_memory_time": long_rate,
                "rate_relative_change": long_rate / short_rate - 1.0,
                "interpretable": bool(
                    short_row["closure_lift"] > 0.02
                    and long_row["closure_lift"] > 0.02
                ),
            }
        )

    short_rate = float(short["gate"]["active_rate_per_memory_time"])
    long_rate = float(long["gate"]["active_rate_per_memory_time"])
    short_frequency = float(short["gate"]["complex_frequency_per_memory_time"])
    long_frequency = float(long["gate"]["complex_frequency_per_memory_time"])
    rate_relative_change = _relative_change(long_rate, short_rate)
    frequency_relative_change = _relative_change(long_frequency, short_frequency)
    active_common = [
        row
        for row in comparisons
        if row["condition"] == "active" and row["interpretable"]
    ]
    common_lag_required = 2
    common_lag_max_change = max(
        (abs(row["rate_relative_change"]) for row in active_common),
        default=float("inf"),
    )
    common_lag_stable = bool(
        len(active_common) >= common_lag_required and common_lag_max_change < 0.1
    )
    real_mode_stable = bool(
        common_lag_stable
        and long["gate"]["control_separation_pass"]
        and long["gate"]["closure_pass"]
    )
    complex_mode_stable = bool(
        math.isfinite(frequency_relative_change)
        and abs(frequency_relative_change) < 0.2
        and long["gate"]["complex_control_pass"]
        and long["gate"]["complex_stability_pass"]
    )
    return {
        "description": "N=100k versus N=1M low-mode AR reconciliation.",
        "created_utc": datetime.now(UTC).isoformat(),
        "selected_diffusion_length_ratio": short_ratio,
        "short_steps": int(short["parameters"]["steps"]),
        "long_steps": int(long["parameters"]["steps"]),
        "short_memory_times": (
            int(short["parameters"]["steps"])
            * float(short["parameters"]["lambda_value"])
        ),
        "long_memory_times": (
            int(long["parameters"]["steps"])
            * float(long["parameters"]["lambda_value"])
        ),
        "active_rate_short": short_rate,
        "active_rate_long": long_rate,
        "active_rate_relative_change": rate_relative_change,
        "common_active_lag_count": len(active_common),
        "common_active_lag_required": common_lag_required,
        "common_active_lag_max_abs_rate_change": common_lag_max_change,
        "common_active_lag_stability_pass": common_lag_stable,
        "eta_zero_rate_short": short["gate"]["eta_zero_rate_per_memory_time"],
        "eta_zero_rate_long": long["gate"]["eta_zero_rate_per_memory_time"],
        "complex_frequency_short": short_frequency,
        "complex_frequency_long": long_frequency,
        "complex_frequency_relative_change": frequency_relative_change,
        "complex_quality_short": short["gate"]["complex_quality_factor"],
        "complex_quality_long": long["gate"]["complex_quality_factor"],
        "short_eta_zero_complex_rows": short["gate"]["eta_zero_complex_rows"],
        "long_eta_zero_complex_rows": long["gate"]["eta_zero_complex_rows"],
        "real_mode_n_stability_pass": real_mode_stable,
        "complex_mode_n_stability_pass": complex_mode_stable,
        "common_lag_comparisons": comparisons,
        "verdict": (
            "The control-separated real relaxation rate is N-stable at all "
            "common interpretable active lags under the 10 percent criterion. "
            "The complex secondary mode fails N-stability and eta-zero specificity."
            if real_mode_stable and not complex_mode_stable
            else "The registered reconciliation criteria were not met."
        ),
    }


def _plot(
    short: dict[str, Any],
    long: dict[str, Any],
    result: dict[str, Any],
    output: Path,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    ratio = result["selected_diffusion_length_ratio"]
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.0))
    colors = {"active": "#0072B2", "eta_zero": "#D55E00"}
    for payload, marker, label_prefix in (
        (short, "o", "N=100k"),
        (long, "s", "N=1M"),
    ):
        for condition in ("active", "eta_zero"):
            rows = sorted(
                [
                    row
                    for row in _rows(payload, ratio)
                    if row["condition"] == condition
                ],
                key=lambda row: row["lag_memory_times"],
            )
            x = [row["lag_memory_times"] for row in rows]
            axes[0, 0].plot(
                x,
                [row["closure_lift"] for row in rows],
                marker=marker,
                color=colors[condition],
                linestyle="-" if payload is short else "--",
                label=f"{label_prefix}, {condition}",
            )
            rates = []
            for row in rows:
                mode = _dominant_mode(row)
                rates.append(
                    mode["rate_per_update"] / payload["parameters"]["lambda_value"]
                    if mode is not None
                    else np.nan
                )
            axes[0, 1].plot(
                x,
                rates,
                marker=marker,
                color=colors[condition],
                linestyle="-" if payload is short else "--",
            )
    axes[0, 0].axhline(0.02, color="#666666", linewidth=1)
    axes[0, 0].set_ylabel("closure lift")
    axes[0, 0].legend(fontsize=7)
    axes[0, 1].set_ylabel("dominant rate / memory time")
    for axis in axes[0]:
        axis.set_xscale("log")
        axis.set_xlabel("lag / memory time")
        axis.grid(alpha=0.25)

    labels = ["real rate", "complex frequency", "quality factor"]
    short_values = [
        result["active_rate_short"],
        result["complex_frequency_short"],
        result["complex_quality_short"],
    ]
    long_values = [
        result["active_rate_long"],
        result["complex_frequency_long"],
        result["complex_quality_long"],
    ]
    x = np.arange(len(labels))
    axes[1, 0].bar(x - 0.18, short_values, width=0.36, label="N=100k")
    axes[1, 0].bar(x + 0.18, long_values, width=0.36, label="N=1M")
    axes[1, 0].set_xticks(x, labels, rotation=20, ha="right")
    axes[1, 0].legend()
    axes[1, 0].grid(axis="y", alpha=0.25)

    comparisons = [
        row
        for row in result["common_lag_comparisons"]
        if row["condition"] == "active" and row["interpretable"]
    ]
    axes[1, 1].bar(
        [str(row["lag_memory_times"]) for row in comparisons],
        [100.0 * row["rate_relative_change"] for row in comparisons],
        color="#009E73",
    )
    axes[1, 1].axhline(10.0, color="#666666", linewidth=1)
    axes[1, 1].axhline(-10.0, color="#666666", linewidth=1)
    axes[1, 1].set_xlabel("common interpretable lag / memory time")
    axes[1, 1].set_ylabel("active rate change [%]")
    axes[1, 1].grid(axis="y", alpha=0.25)
    fig.suptitle("Low-mode AR short/long reconciliation")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _report(result: dict[str, Any], report_path: Path, figure_path: Path) -> str:
    lines = [
        "# Low-Mode AR Long-Run Reconciliation",
        "",
        f"Date: {result['created_utc']}.",
        "",
        "## Evidence",
        "",
        f"- The comparison spans {result['short_memory_times']:.0f} versus "
        f"{result['long_memory_times']:.0f} memory times.",
        f"- Descriptive aggregate active real rate: "
        f"{result['active_rate_short']:.4g} to "
        f"{result['active_rate_long']:.4g} "
        f"({100.0 * result['active_rate_relative_change']:+.2f} percent).",
        f"- Common interpretable active lags: "
        f"{result['common_active_lag_count']} "
        f"(maximum absolute rate change "
        f"{100.0 * result['common_active_lag_max_abs_rate_change']:.2f} percent).",
        f"- eta=0 real rate: {result['eta_zero_rate_short']:.4g} to "
        f"{result['eta_zero_rate_long']:.4g}.",
        f"- Complex frequency: {result['complex_frequency_short']:.4g} to "
        f"{result['complex_frequency_long']:.4g} "
        f"({100.0 * result['complex_frequency_relative_change']:+.2f} percent).",
        f"- Complex quality factor: {result['complex_quality_short']:.4g} to "
        f"{result['complex_quality_long']:.4g}.",
        f"- Stable eta=0 complex rows: "
        f"{result['short_eta_zero_complex_rows']} and "
        f"{result['long_eta_zero_complex_rows']}.",
        "",
        f"![Short/long reconciliation]({_relative(report_path, figure_path)})",
        "",
        "## Common-lag check",
        "",
        "| condition | lag / memory time | short closure | long closure | "
        "short rate | long rate | rate change | interpretable |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in result["common_lag_comparisons"]:
        lines.append(
            f"| {row['condition']} | {row['lag_memory_times']:.2f} | "
            f"{row['short_closure_lift']:.3f} | {row['long_closure_lift']:.3f} | "
            f"{row['short_rate_per_memory_time']:.4g} | "
            f"{row['long_rate_per_memory_time']:.4g} | "
            f"{100.0 * row['rate_relative_change']:+.2f}% | "
            f"{row['interpretable']} |"
        )
    lines.extend(
        [
            "",
            "## Inference",
            "",
            f"- Real-mode N-stability criterion: "
            f"{result['real_mode_n_stability_pass']}.",
            f"- Complex-mode N-stability and control criterion: "
            f"{result['complex_mode_n_stability_pass']}.",
            f"- {result['verdict']}",
            "",
            "The scalar spectral-memory model therefore supports a compact",
            "predictive relaxation description in this local one-dimensional",
            "regime. It does not yet support a feedback-specific oscillatory mode.",
            "",
            "## Limits",
            "",
            "- The 10 percent stability threshold is applied to every active",
            "  common lag with closure lift above 0.02 in both runs; at least",
            "  two such lags are required. The aggregate rate is descriptive",
            "  because the full short and long lag grids differ.",
            "- The positive diffusion ratio was selected exploratorily in the",
            "  short run and frozen before N=1M; it is not an optimized nu claim.",
            "- This is not evidence for a photon, spin, propagation, or physical",
            "  phase. The complex side modes are explicitly retained as a negative",
            "  result because they also occur for eta=0 and drift with N.",
            "",
            "## Reproduction",
            "",
            "    python experiments/current/memory/reconcile_low_mode_ar_runs.py",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    short = _load(args.short)
    long = _load(args.long)
    result = reconcile(short, long)
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    _plot(short, long, result, figure_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_report(result, report_path, figure_path), encoding="utf-8")
    summary_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
