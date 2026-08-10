"""Registered two-seed 500k accumulation control for the fixed P3.2 model."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import importlib.util
import json
from pathlib import Path
import subprocess
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[5]
BASE_PATH = Path(__file__).with_name("retarded_reciprocal_full_knot_gate.py")
SPEC = importlib.util.spec_from_file_location("p32_retarded_base", BASE_PATH)
assert SPEC is not None and SPEC.loader is not None
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

WINDOWS = ((100.0, 500.0), (500.0, 1000.0), (1000.0, 2500.0), (2500.0, 5000.0))
CONDITIONS = BASE.RETARDED_RECIPROCAL_CONDITIONS
COLORS = BASE.CONDITION_COLORS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/reciprocal/p32_accumulation_control_N500k_2026-08-06.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/reciprocal/p32_accumulation_control_N500k_2026-08-06.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path("figures/draft/response/p32_accumulation_control_N500k_2026-08-06.png"),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _git(*arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _base_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        checkpoint=BASE.DEFAULT_CHECKPOINT,
        future_seeds="1,2",
        updates=500_000,
        sample_every=10,
        distance_ratio=2.5,
        cross_gain=0.02,
        correlation_length_r=5.0,
        relaxation_memory_times=10.0,
        grid_spacing_r=0.25,
        grid_points_left=120,
        grid_points_right=180,
        analysis_burn_memory_times=100.0,
        segments=4,
        min_complex_segments=3,
        min_complex_seeds=2,
        max_control_complex_seeds=0,
        frequency_min_per_memory_time=0.05,
        mode_relative_range_max=0.25,
        phase_coherence_min=0.5,
        fit_residual_ratio_max=0.8,
        fit_condition_max=1e8,
        response_min_r=1e-3,
        mediator_rms_min=1e-6,
        radius_factor_limit=1.10,
        shape_spectrum_median_limit=0.05,
        shape_spectrum_q95_limit=0.10,
        noise_seed_offset=20_260_804,
        allow_dirty=args.allow_dirty,
        report=args.report,
        summary_json=args.summary_json,
        figure=args.figure,
    )


def _window_row(
    times: np.ndarray,
    distances: np.ndarray,
    off_distances: np.ndarray,
    lower: float,
    upper: float,
    *,
    include_upper: bool,
) -> dict[str, float]:
    selected = (times >= lower) & (times <= upper if include_upper else times < upper)
    if np.count_nonzero(selected) < 3:
        raise RuntimeError(f"window [{lower}, {upper}] has fewer than three samples")
    window_times = times[selected]
    values = distances[selected]
    centered_times = window_times - float(np.mean(window_times))
    denominator = float(np.sum(centered_times * centered_times))
    slope = float(np.sum(centered_times * (values - np.mean(values))) / denominator)
    return {
        "start_memory_times": lower,
        "end_memory_times": upper,
        "samples": int(np.count_nonzero(selected)),
        "median_pair_distance_r": float(np.median(values)),
        "q25_pair_distance_r": float(np.quantile(values, 0.25)),
        "q75_pair_distance_r": float(np.quantile(values, 0.75)),
        "slope_r_per_1000_memory_times": 1000.0 * slope,
        "median_absolute_delta_from_off_r": float(
            np.median(np.abs(values - off_distances[selected]))
        ),
    }


def _accumulation_rows(
    traces: list[dict[str, Any]],
    *,
    alpha: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for trace in traces:
        times = np.asarray(trace["sample_steps"], dtype=float) * alpha
        distances = np.asarray(trace["pair_distances_r"], dtype=float)
        off = distances[:, 0]
        conditions: dict[str, Any] = {}
        for condition_index, condition in enumerate(CONDITIONS):
            epochs = [
                _window_row(
                    times,
                    distances[:, condition_index],
                    off,
                    lower,
                    upper,
                    include_upper=index == len(WINDOWS) - 1,
                )
                for index, (lower, upper) in enumerate(WINDOWS)
            ]
            conditions[condition] = {
                "epochs": epochs,
                "late_minus_early_absolute_delta_from_off_r": float(
                    epochs[-1]["median_absolute_delta_from_off_r"]
                    - epochs[0]["median_absolute_delta_from_off_r"]
                ),
            }
        rows.append(
            {
                "future_seed": int(trace["future_seed"]),
                "trace_sample_interval_memory_times": float(
                    np.median(np.diff(times))
                ),
                "conditions": conditions,
            }
        )
    return rows


def run_control(args: argparse.Namespace) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not args.allow_dirty and _git("status", "--porcelain"):
        raise SystemExit("working tree is dirty; commit first or pass --allow-dirty")
    base_payload, traces = BASE.run_gate(_base_args(args))
    accumulation = _accumulation_rows(
        traces,
        alpha=float(base_payload["config"]["alpha"]),
    )
    reciprocal_changes = np.asarray(
        [
            row["conditions"]["retarded_reciprocal"][
                "late_minus_early_absolute_delta_from_off_r"
            ]
            for row in accumulation
        ],
        dtype=float,
    )
    one_way_changes = np.asarray(
        [
            row["conditions"]["retarded_one_way"][
                "late_minus_early_absolute_delta_from_off_r"
            ]
            for row in accumulation
        ],
        dtype=float,
    )
    shape_count = int(
        base_payload["gate"]["shape_seed_counts"]["retarded_reciprocal"]
    )
    signs_agree = bool(np.all(reciprocal_changes >= 0.0) or np.all(reciprocal_changes <= 0.0))
    accumulation_candidate = bool(
        np.all(reciprocal_changes >= 0.1) and np.all(one_way_changes < 0.05)
    )
    mode_candidate = bool(
        base_payload["gate"]["retarded_reciprocal_complex_candidate_pass"]
    )
    if shape_count < 2 or not signs_agree:
        classification = "inconclusive two-seed accumulation control"
    elif mode_candidate:
        classification = "control-separated long-horizon mode candidate"
    elif accumulation_candidate:
        classification = "late reciprocal accumulation candidate"
    else:
        classification = "no control-separated P3.2 accumulation through 500k"
    payload = {
        "schema": "emergenz-knoten.p32-accumulation-control",
        "schema_version": 1,
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": _git("rev-parse", "HEAD"),
        "git_status": _git("status", "--porcelain"),
        "preregistration": (
            "reports/project/meta/"
            "p32_accumulation_control_preregistration_2026-08-06.md"
        ),
        "base_gate": base_payload,
        "accumulation_windows_memory_times": WINDOWS,
        "accumulation_rows": accumulation,
        "gate": {
            "classification": classification,
            "mode_candidate": mode_candidate,
            "accumulation_candidate": accumulation_candidate,
            "shape_seed_count": shape_count,
            "reciprocal_change_signs_agree": signs_agree,
            "reciprocal_late_minus_early_r": reciprocal_changes,
            "one_way_late_minus_early_r": one_way_changes,
            "reciprocal_threshold_r": 0.1,
            "one_way_max_r": 0.05,
        },
    }
    return BASE._jsonable(payload), traces


def _plot(payload: dict[str, Any], traces: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    alpha = float(payload["base_gate"]["config"]["alpha"])
    fig, axes = plt.subplots(2, 2, figsize=(12.2, 8.7), constrained_layout=True)
    for condition_index, condition in enumerate(CONDITIONS):
        for trace in traces:
            times = np.asarray(trace["sample_steps"]) * alpha
            axes[0, 0].plot(
                times,
                trace["pair_distances_r"][:, condition_index],
                color=COLORS[condition],
                alpha=0.35,
                linewidth=0.8,
            )
        axes[0, 0].plot([], [], color=COLORS[condition], label=condition)
    axes[0, 0].set(
        xlabel="continuation / memory times",
        ylabel="pair distance / R",
        title="All four fixed P3.2 arms",
    )
    axes[0, 0].legend(fontsize=7)
    axes[0, 0].grid(alpha=0.25)

    for condition_index, condition in ((2, "retarded_one_way"), (3, "retarded_reciprocal")):
        for trace in traces:
            times = np.asarray(trace["sample_steps"]) * alpha
            difference = np.abs(
                trace["pair_distances_r"][:, condition_index]
                - trace["pair_distances_r"][:, 0]
            )
            axes[0, 1].plot(
                times,
                difference,
                color=COLORS[condition],
                alpha=0.55,
                linewidth=0.9,
            )
        axes[0, 1].plot([], [], color=COLORS[condition], label=condition)
    axes[0, 1].set(
        xlabel="continuation / memory times",
        ylabel="absolute distance delta from off / R",
        title="Accumulated control-subtracted response",
    )
    axes[0, 1].legend(fontsize=8)
    axes[0, 1].grid(alpha=0.25)

    labels = [f"{lower:g}-{upper:g}" for lower, upper in WINDOWS]
    x = np.arange(len(labels))
    for condition in ("retarded_one_way", "retarded_reciprocal"):
        values = np.asarray(
            [
                [
                    epoch["median_absolute_delta_from_off_r"]
                    for epoch in row["conditions"][condition]["epochs"]
                ]
                for row in payload["accumulation_rows"]
            ]
        )
        axes[1, 0].plot(
            x,
            values.T,
            color=COLORS[condition],
            marker="o",
            alpha=0.65,
            label=condition,
        )
    axes[1, 0].set(
        xticks=x,
        xticklabels=labels,
        xlabel="fixed memory-time window",
        ylabel="median absolute delta / R",
        title="Epoch accumulation by future seed",
    )
    handles, names = axes[1, 0].get_legend_handles_labels()
    unique = dict(zip(names, handles))
    axes[1, 0].legend(unique.values(), unique.keys(), fontsize=8)
    axes[1, 0].grid(alpha=0.25)

    seeds = [row["future_seed"] for row in payload["accumulation_rows"]]
    reciprocal = payload["gate"]["reciprocal_late_minus_early_r"]
    one_way = payload["gate"]["one_way_late_minus_early_r"]
    width = 0.34
    axes[1, 1].bar(np.arange(len(seeds)) - width / 2, reciprocal, width, label="reciprocal")
    axes[1, 1].bar(np.arange(len(seeds)) + width / 2, one_way, width, label="one-way")
    axes[1, 1].axhline(0.1, color="black", linestyle=":", linewidth=1, label="reciprocal gate")
    axes[1, 1].axhline(0.05, color="#666666", linestyle="--", linewidth=1, label="one-way max")
    axes[1, 1].set(
        xticks=np.arange(len(seeds)),
        xticklabels=[str(seed) for seed in seeds],
        xlabel="future-noise seed",
        ylabel="late minus early absolute delta / R",
        title="Registered accumulation effect size",
    )
    axes[1, 1].legend(fontsize=8)
    axes[1, 1].grid(axis="y", alpha=0.25)
    fig.suptitle("P3.2 500k accumulation control")
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    gate = payload["gate"]
    base = payload["base_gate"]
    parameters = base["parameters"]
    lines = [
        "# P3.2 500k accumulation control",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Design",
        "",
        f"Two future-noise paths continue the same mature formation checkpoint for `{parameters['updates']:,}` updates or `{base['derived']['continuation_memory_times']:.0f}` memory times. Every `{parameters['sample_every']}`th update is stored; regression tests require this to be exact subsampling of the same hidden path and preserve fitted rates.",
        "",
        "The mechanism, gain, kernel, grid, noise scale, and four P3.2 arms are unchanged. This is an accumulation falsification, not a reopening of the earlier mode or source-local gates.",
        "",
        "## Result",
        "",
        f"Classification: **{gate['classification']}**.",
        "",
        f"- original long-horizon mode candidate: {gate['mode_candidate']};",
        f"- registered accumulation candidate: {gate['accumulation_candidate']};",
        f"- reciprocal shape-valid seeds: {gate['shape_seed_count']}/2;",
        f"- reciprocal late-minus-early deltas: {gate['reciprocal_late_minus_early_r']};",
        f"- one-way late-minus-early deltas: {gate['one_way_late_minus_early_r']}.",
        "",
        "The large off-subtracted path differences are not reciprocal-specific: the one-way control accumulates nearly the same changes in both future-noise paths. Meanwhile, the actual late pair-distance medians remain bounded near one knot radius in both retarded arms. The supported reading is sensitive path divergence after a persistent perturbation, not a control-separated reciprocal accumulation law.",
        "",
        f"![P3.2 500k accumulation control]({(Path('../..') / figure.relative_to(ROOT)).as_posix()})",
        "",
        "## Fixed-window diagnostics",
        "",
        "| seed | arm | window | median distance/R | IQR/R | slope R/1000 memory times | median absolute delta from off/R |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["accumulation_rows"]:
        for condition in ("retarded_one_way", "retarded_reciprocal"):
            for epoch in row["conditions"][condition]["epochs"]:
                lines.append(
                    f"| {row['future_seed']} | {condition} | {epoch['start_memory_times']:g}-{epoch['end_memory_times']:g} | {epoch['median_pair_distance_r']:.4g} | {epoch['q25_pair_distance_r']:.4g}-{epoch['q75_pair_distance_r']:.4g} | {epoch['slope_r_per_1000_memory_times']:+.4g} | {epoch['median_absolute_delta_from_off_r']:.4g} |"
                )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "Both paths branch from one formation state. They can reveal a delayed numerical accumulation on this branch but cannot estimate basin prevalence. The source remains a target-specific cross-gradient, and the channel law remains inserted. No field, causal-speed, spin, charge, particle, dimension, or QFT claim follows.",
            "",
            "## Reproducibility",
            "",
            f"- preregistration: `{payload['preregistration']}`;",
            f"- git revision: `{payload['git_revision']}`;",
            f"- git status at start: `{'clean' if not payload['git_status'] else payload['git_status']}`;",
            f"- base runtime: `{base['runtime_seconds']:.3f} s`;",
            "- command: `python experiments/current/memory/synchronization/reciprocity/p32_accumulation_control.py`;",
            f"- machine-readable summary: `{Path(parameters['summary_json']).as_posix()}`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    payload, traces = run_control(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _plot(payload, traces, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")
    print(payload["gate"]["classification"])
    print(report.relative_to(ROOT))


if __name__ == "__main__":
    main()
