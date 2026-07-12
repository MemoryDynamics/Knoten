from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
import json
import math
from pathlib import Path
import statistics
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
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import SimulationConfig  # noqa: E402
from emergenz_knoten.knot_score import score_v0_5_against_control  # noqa: E402

import dynamic_center_trace_report as trace_report  # noqa: E402
import long_run_metastability as metastability_run  # noqa: E402


DEFAULT_EPSILONS = [0.0, *np.geomspace(1.0e-12, 1.0e1, 24).tolist()]


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def _parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one float")
    return values


def _epsilon_token(value: float) -> str:
    if value == 0.0:
        return "0"
    mantissa, exponent = f"{value:.6e}".split("e")
    mantissa = mantissa.rstrip("0").rstrip(".").replace(".", "p")
    sign = "m" if exponent.startswith("-") else "p"
    return f"{mantissa}e{sign}{abs(int(exponent)):02d}"


def _fmt(value: object, digits: int = 3) -> str:
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return "`n/a`"
    if not math.isfinite(number):
        return "`n/a`"
    if number == 0.0:
        text = "0"
    elif abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        text = f"{number:.{digits}e}"
    else:
        text = f"{number:.{digits}f}"
    return f"`{text}`"


def _median(values: Iterable[object]) -> float | None:
    finite: list[float] = []
    for value in values:
        try:
            number = float(value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            continue
        if math.isfinite(number):
            finite.append(number)
    return statistics.median(finite) if finite else None


def _iqr(values: Iterable[object]) -> tuple[float | None, float | None]:
    finite: list[float] = []
    for value in values:
        try:
            number = float(value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            continue
        if math.isfinite(number):
            finite.append(number)
    finite.sort()
    if not finite:
        return None, None
    if len(finite) == 1:
        return finite[0], finite[0]
    q1, _, q3 = statistics.quantiles(finite, n=4, method="inclusive")
    return q1, q3


def _diagnostic_value(payload: dict[str, Any], path: tuple[str, ...]) -> float | None:
    value: Any = payload
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _best_voxel_residence(diagnostics: dict[str, Any]) -> float | None:
    residence = diagnostics.get("residence_by_voxel_size")
    if not isinstance(residence, dict):
        return None
    values: list[float] = []
    for item in residence.values():
        if not isinstance(item, dict):
            continue
        value = item.get("max_residence_memory_times")
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(number):
            values.append(number)
    return max(values) if values else None


def _dynamic_sources(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    diagnostics = payload.get("diagnostics", {})
    dynamic = diagnostics.get("dynamic_center_trace", {}) if isinstance(diagnostics, dict) else {}
    if not isinstance(dynamic, dict):
        dynamic = {}
    trend = dynamic.get("trend", dynamic)
    if not isinstance(trend, dict):
        trend = dynamic
    spin = dynamic.get("spin_proxy", {})
    if not isinstance(spin, dict):
        spin = {}
    return diagnostics if isinstance(diagnostics, dict) else {}, trend, spin


def _case_row(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    config = payload.get("config", {})
    diagnostics, trend, spin = _dynamic_sources(payload)
    memory_cloud = diagnostics.get("memory_cloud", {})
    memory_shape = memory_cloud.get("shape", {}) if isinstance(memory_cloud, dict) else {}
    if not isinstance(memory_shape, dict):
        memory_shape = {}
    return {
        "epsilon": float(config.get("epsilon", float("nan"))) if isinstance(config, dict) else float("nan"),
        "a_att": float(config.get("amplitude_att", float("nan"))) if isinstance(config, dict) else float("nan"),
        "steps": int(config.get("steps", 0)) if isinstance(config, dict) else 0,
        "condition": str(payload.get("condition")),
        "seed": int(payload.get("seed", 0)),
        "path": path.relative_to(ROOT).as_posix(),
        "best_residence_memory_times": _best_voxel_residence(diagnostics),
        "memory_center_residence_memory_times": _diagnostic_value(
            diagnostics,
            ("center_residence", "memory_center", "primary_max_run_memory_times"),
        ),
        "dynamic_rms_radius_median": _diagnostic_value(trend, ("rms_radius_median",)),
        "dynamic_center_drift_radius_fraction_per_memory_time": _diagnostic_value(
            trend, ("center_drift_radius_fraction_per_memory_time_median",)
        ),
        "dynamic_x_distance_to_radius_median": _diagnostic_value(
            trend, ("x_distance_to_rms_radius_median",)
        ),
        "dynamic_inside_fraction_time_weighted": _diagnostic_value(
            trend, ("comoving_inside_fraction_time_weighted",)
        ),
        "dynamic_max_run_memory_times": _diagnostic_value(trend, ("max_run_memory_times",)),
        "spin_amplitude_median": _diagnostic_value(spin, ("amplitude_median",)),
        "spin_lab_frame_amplitude_median": _diagnostic_value(spin, ("lab_frame_amplitude_median",)),
        "spin_angular_speed_median": _diagnostic_value(spin, ("angular_speed_median",)),
        "spin_comoving_speed_median": _diagnostic_value(spin, ("comoving_speed_median",)),
        "spin_center_speed_median": _diagnostic_value(spin, ("center_speed_median",)),
        "spin_axis_polarization": _diagnostic_value(spin, ("axis_polarization",)),
        "spin_direction_dephasing_memory_times": _diagnostic_value(
            spin, ("direction_dephasing_memory_times",)
        ),
        "spin_sample_interval_memory_times": _diagnostic_value(
            spin, ("sample_interval_memory_times",)
        ),
        "memory_shape_dimension": _diagnostic_value(memory_shape, ("effective_dimension",)),
        "memory_roundness": _diagnostic_value(memory_shape, ("axis_ratio_min_max",)),
        "memory_radius": _diagnostic_value(memory_shape, ("mean_radius",)),
    }


def _refresh_dynamic_center_payload(payload: dict[str, Any]) -> None:
    """Recompute frame-sensitive diagnostics from persisted center/position traces."""
    diagnostics = payload.get("diagnostics")
    config_payload = payload.get("config")
    if not isinstance(diagnostics, dict) or not isinstance(config_payload, dict):
        return
    dynamic = diagnostics.get("dynamic_center_trace")
    trace = dynamic.get("trace") if isinstance(dynamic, dict) else None
    if not isinstance(trace, dict):
        return
    try:
        config = SimulationConfig(**config_payload)
        steps = np.asarray(trace.get("steps", []), dtype=np.int64)
        centers = np.asarray(trace.get("centers", []), dtype=float)
        positions = np.asarray(trace.get("positions", []), dtype=float)
        mean_radii = np.asarray(trace.get("mean_radii", []), dtype=float)
        rms_radii = np.asarray(trace.get("rms_radii", []), dtype=float)
        x_distances = np.asarray(trace.get("x_distances", []), dtype=float)
        if len(steps) < 3:
            return
        tail_gap = int(steps[-1] - steps[-2])
        if tail_gap <= 0:
            return
        result = {
            "trace_steps": steps,
            "trace_centers": centers,
            "trace_positions": positions,
            "trace_mean_radii": mean_radii,
            "trace_rms_radii": rms_radii,
            "trace_x_distances": x_distances,
        }
    except (TypeError, ValueError) as error:
        raise ValueError("cannot reconstruct dynamic-center diagnostics from persisted trace") from error
    refreshed = metastability_run._dynamic_center_trace_diagnostics(
        result,
        config=config,
        trace_every=tail_gap,
    )
    if not isinstance(refreshed, dict):
        raise ValueError("persisted trace did not yield dynamic-center diagnostics")
    if "spin_proxy" not in refreshed:
        raise ValueError("persisted trace did not yield a regular spin window")
    diagnostics["dynamic_center_trace"] = refreshed


def _load_payloads(output_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    items: list[tuple[Path, dict[str, Any]]]
    items = []
    for path in sorted(output_dir.glob("eps_*/case_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        _refresh_dynamic_center_payload(payload)
        trace_report._ensure_trend_payload(payload)
        items.append((path, payload))
    return items


def build_rows(output_dir: Path) -> list[dict[str, Any]]:
    payloads = _load_payloads(output_dir)
    controls: dict[tuple[float, int], dict[str, Any]] = {}
    for _, payload in payloads:
        config = payload.get("config", {})
        if payload.get("condition") != "eta_zero" or not isinstance(config, dict):
            continue
        controls[(float(config.get("epsilon", float("nan"))), int(payload.get("seed", 0)))] = payload

    rows: list[dict[str, Any]] = []
    for path, payload in payloads:
        row = _case_row(path, payload)
        row["score"] = None
        row["residence_gain"] = None
        row["memory_compactness_gain"] = None
        row["memory_roundness_gain"] = None
        row["memory_dimension_gain"] = None
        if row["condition"] == "baseline":
            control = controls.get((float(row["epsilon"]), int(row["seed"])))
            if control is not None:
                score = score_v0_5_against_control(
                    payload.get("diagnostics", {}),
                    control.get("diagnostics", {}),
                )
                for key in (
                    "score",
                    "residence_gain",
                    "memory_compactness_gain",
                    "memory_roundness_gain",
                    "memory_dimension_gain",
                ):
                    row[key] = score.get(key)
        rows.append(row)
    return rows


SUMMARY_METRICS = [
    "score",
    "residence_gain",
    "memory_compactness_gain",
    "memory_roundness_gain",
    "memory_dimension_gain",
    "best_residence_memory_times",
    "memory_center_residence_memory_times",
    "dynamic_rms_radius_median",
    "dynamic_center_drift_radius_fraction_per_memory_time",
    "dynamic_x_distance_to_radius_median",
    "dynamic_inside_fraction_time_weighted",
    "dynamic_max_run_memory_times",
    "spin_amplitude_median",
    "spin_lab_frame_amplitude_median",
    "spin_angular_speed_median",
    "spin_comoving_speed_median",
    "spin_center_speed_median",
    "spin_axis_polarization",
    "spin_direction_dephasing_memory_times",
    "spin_sample_interval_memory_times",
    "memory_shape_dimension",
    "memory_roundness",
    "memory_radius",
]


def build_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[float, str], list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault((float(row["epsilon"]), str(row["condition"])), []).append(row)
    summary: list[dict[str, Any]] = []
    for (epsilon, condition), group in sorted(grouped.items()):
        item: dict[str, Any] = {
            "epsilon": epsilon,
            "condition": condition,
            "n": len(group),
            "steps": int(group[0]["steps"]) if group else None,
            "a_att": float(group[0]["a_att"]) if group else None,
        }
        for metric in SUMMARY_METRICS:
            values = [row.get(metric) for row in group]
            q1, q3 = _iqr(values)
            item[f"{metric}_median"] = _median(values)
            item[f"{metric}_q1"] = q1
            item[f"{metric}_q3"] = q3
        summary.append(item)
    return summary


def _epsilon_positions(epsilons: Iterable[float]) -> tuple[dict[float, float], list[float], list[str]]:
    values = sorted({float(value) for value in epsilons})
    positives = [value for value in values if value > 0.0]
    min_log = math.floor(math.log10(min(positives))) if positives else -1
    max_log = math.ceil(math.log10(max(positives))) if positives else 1
    positions: dict[float, float] = {}
    for value in values:
        positions[value] = min_log - 1.0 if value == 0.0 else math.log10(value)
    ticks = [min_log - 1.0, *range(min_log, max_log + 1)]
    labels = ["0", *[f"1e{power}" for power in range(min_log, max_log + 1)]]
    return positions, [float(tick) for tick in ticks], labels


def _plot_metric(
    ax: Any,
    rows: list[dict[str, Any]],
    *,
    metric: str,
    title: str,
    ylabel: str,
    positions: dict[float, float],
    log_y: bool = False,
    baseline_only: bool = False,
) -> None:
    colors = {"baseline": "#2563eb", "eta_zero": "#64748b"}
    offsets = {"baseline": -0.06, "eta_zero": 0.06}
    labels_seen: set[str] = set()
    for condition in ["baseline", "eta_zero"]:
        if baseline_only and condition != "baseline":
            continue
        by_eps: dict[float, list[float]] = {}
        for row in rows:
            if row["condition"] != condition:
                continue
            value = row.get(metric)
            if value is None:
                continue
            number = float(value)
            if not math.isfinite(number) or (log_y and number <= 0.0):
                continue
            by_eps.setdefault(float(row["epsilon"]), []).append(number)
        for epsilon, values in sorted(by_eps.items()):
            x = positions[epsilon] + offsets.get(condition, 0.0)
            label = condition if condition not in labels_seen else None
            labels_seen.add(condition)
            color = colors.get(condition, "#0f172a")
            ax.scatter([x] * len(values), values, color=color, alpha=0.72, s=35, edgecolor="white", linewidth=0.4, label=label)
            median = statistics.median(values)
            q1, q3 = _iqr(values)
            ax.plot([x - 0.035, x + 0.035], [median, median], color=color, linewidth=2.0)
            if q1 is not None and q3 is not None:
                ax.vlines(x, q1, q3, color=color, alpha=0.65, linewidth=1.6)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    if log_y:
        ax.set_yscale("log")
    ax.grid(True, which="both", alpha=0.25)


def _nearest_epsilons(epsilons: list[float], targets: list[float]) -> list[float]:
    selected: list[float] = []
    positives = [value for value in epsilons if value > 0.0]
    for target in targets:
        if target == 0.0:
            if 0.0 in epsilons:
                selected.append(0.0)
            continue
        if positives:
            selected.append(min(positives, key=lambda value: abs(math.log10(value) - math.log10(target))))
    out: list[float] = []
    for value in selected:
        if value not in out:
            out.append(value)
    return out


def _trace_from_payload(payload: dict[str, Any]) -> dict[str, list[Any]]:
    diagnostics = payload.get("diagnostics", {})
    dynamic = diagnostics.get("dynamic_center_trace", {}) if isinstance(diagnostics, dict) else {}
    trace = dynamic.get("trace", {}) if isinstance(dynamic, dict) else {}
    return trace if isinstance(trace, dict) else {}


def write_plots(output_dir: Path, rows: list[dict[str, Any]], figure_dir: Path) -> list[Path]:
    figure_dir.mkdir(parents=True, exist_ok=True)
    positions, ticks, labels = _epsilon_positions(row["epsilon"] for row in rows)
    outputs: list[Path] = []

    specs = [
        (
            "epsilon_dynamic_center_knot_score_2026-07-12.png",
            [
                ("score", "KnotScore v0.5", "score", False, True),
                ("dynamic_rms_radius_median", "Dynamic Radius", "median RMS radius", True, False),
                (
                    "dynamic_center_drift_radius_fraction_per_memory_time",
                    "Center Drift / Radius",
                    "radius fractions per memory time",
                    True,
                    False,
                ),
                ("memory_shape_dimension", "Memory Dimension", "dimension", False, False),
            ],
        ),
        (
            "epsilon_dynamic_center_spin_proxy_2026-07-12.png",
            [
                ("spin_amplitude_median", "Spin-Proxy Amplitude", "median |r wedge v|", True, False),
                ("spin_angular_speed_median", "Angular Speed Proxy", "median |L| / R^2", True, False),
                ("spin_axis_polarization", "Axis Polarization", "|mean unit axis|", False, False),
                ("spin_direction_dephasing_memory_times", "Axis Dephasing", "memory times", True, False),
            ],
        ),
    ]
    for filename, panels in specs:
        fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.0), squeeze=False)
        for ax, (metric, title, ylabel, log_y, baseline_only) in zip(axes.ravel(), panels, strict=True):
            _plot_metric(
                ax,
                rows,
                metric=metric,
                title=title,
                ylabel=ylabel,
                positions=positions,
                log_y=log_y,
                baseline_only=baseline_only,
            )
            ax.set_xticks(ticks, labels, rotation=45, ha="right")
            ax.set_xlabel("epsilon")
        handles, legend_labels = axes[0, 0].get_legend_handles_labels()
        if handles:
            fig.legend(handles, legend_labels, loc="upper center", ncol=len(handles), frameon=False)
        fig.suptitle("Epsilon sensitivity at fixed corrected-sign compact candidate", y=1.02)
        fig.tight_layout()
        path = figure_dir / filename
        fig.savefig(path, dpi=220, bbox_inches="tight")
        plt.close(fig)
        outputs.append(path)

    payloads = _load_payloads(output_dir)
    epsilons = sorted({float(payload.get("config", {}).get("epsilon", float("nan"))) for _, payload in payloads})
    selected = _nearest_epsilons(epsilons, [0.0, 1.0e-12, 1.0e-8, 1.0e-4, 3.0e-2, 1.0, 1.0e1])
    if selected:
        fig, axes = plt.subplots(2, len(selected), figsize=(4.2 * len(selected), 6.4), squeeze=False)
        colors = {"baseline": "#2563eb", "eta_zero": "#64748b"}
        for col, epsilon in enumerate(selected):
            matching = [
                payload
                for _, payload in payloads
                if float(payload.get("config", {}).get("epsilon", float("nan"))) == epsilon
            ]
            for payload in matching:
                trace = _trace_from_payload(payload)
                steps = np.asarray(trace.get("steps", []), dtype=float)
                radii = np.asarray(trace.get("rms_radii", []), dtype=float)
                xdist = np.asarray(trace.get("x_distances", []), dtype=float)
                valid = np.isfinite(steps) & (steps > 0.0) & np.isfinite(radii) & (radii > 0.0)
                if not np.any(valid):
                    continue
                condition = str(payload.get("condition"))
                seed = int(payload.get("seed", 0))
                color = colors.get(condition, "#0f172a")
                alpha = 0.9 if condition == "baseline" else 0.55
                label = f"{condition} s{seed}"
                axes[0, col].plot(steps[valid], radii[valid], color=color, alpha=alpha, linewidth=1.1, label=label)
                ratio = np.full(radii.shape, np.nan, dtype=float)
                ratio[valid] = xdist[valid] / radii[valid]
                ratio_valid = valid & np.isfinite(ratio)
                axes[1, col].plot(steps[ratio_valid], ratio[ratio_valid], color=color, alpha=alpha, linewidth=1.1)
            axes[0, col].set_title(f"epsilon={epsilon:.2e}" if epsilon else "epsilon=0")
            axes[0, col].set_yscale("log")
            axes[0, col].set_ylabel("RMS radius")
            axes[1, col].axhline(2.0, color="#dc2626", linestyle="--", linewidth=0.9)
            axes[1, col].set_ylabel("x distance / RMS radius")
            axes[1, col].set_xlabel("updates N")
            for row in range(2):
                axes[row, col].set_xscale("log")
                axes[row, col].grid(True, which="both", alpha=0.25)
        handles, legend_labels = axes[0, 0].get_legend_handles_labels()
        if handles:
            fig.legend(handles[:6], legend_labels[:6], loc="upper center", ncol=min(6, len(handles)), frameon=False)
        fig.suptitle("Seedwise epsilon sweep traces on logarithmic update time", y=1.02)
        fig.tight_layout()
        path = figure_dir / "epsilon_dynamic_center_seedwise_timeseries_2026-07-12.png"
        fig.savefig(path, dpi=220, bbox_inches="tight")
        plt.close(fig)
        outputs.append(path)
    return outputs


def write_report(
    *,
    rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    figures: list[Path],
    output_dir: Path,
    output_json: Path,
    report_path: Path,
) -> None:
    baseline = [row for row in summary if row["condition"] == "baseline"]
    best = max(
        (row for row in baseline if row.get("score_median") is not None),
        key=lambda row: float(row["score_median"]),
        default=None,
    )
    score_plateau = [
        row
        for row in baseline
        if row.get("score_median") is not None and float(row["score_median"]) >= 0.75
    ]
    failure_band = [
        row
        for row in baseline
        if row.get("score_median") is not None
        and float(row["epsilon"]) > 0.0
        and float(row["score_median"]) <= 0.2
    ]
    lines = [
        "# Epsilon Sensitivity for Dynamic-Center Knot Benchmarks",
        "",
        "Date: 2026-07-12.",
        "",
        "## Scope",
        "",
        "This sweep varies only `epsilon` around the corrected-sign compact scalar-memory",
        "candidate. It is a short diagnostic run to estimate the stochastic-noise scale",
        "at which co-moving knot observables and spin proxies separate from matched",
        "`eta_zero` controls.",
        "",
        f"Raw data root: `{output_dir.relative_to(ROOT).as_posix()}`.",
        f"Case rows: `{len(rows)}`.",
        "",
        "## Median Summary",
        "",
        "| epsilon | condition | score | dyn radius | drift/radius/memtime | memory dim | memory roundness | internal spin amp | lab spin amp | spin omega | axis pol | dephase |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary:
        lines.append(
            "| "
            + " | ".join(
                [
                    _fmt(row["epsilon"]),
                    f"`{row['condition']}`",
                    _fmt(row.get("score_median")),
                    _fmt(row.get("dynamic_rms_radius_median_median")),
                    _fmt(row.get("dynamic_center_drift_radius_fraction_per_memory_time_median")),
                    _fmt(row.get("memory_shape_dimension_median")),
                    _fmt(row.get("memory_roundness_median")),
                    _fmt(row.get("spin_amplitude_median_median")),
                    _fmt(row.get("spin_lab_frame_amplitude_median_median")),
                    _fmt(row.get("spin_angular_speed_median_median")),
                    _fmt(row.get("spin_axis_polarization_median")),
                    _fmt(row.get("spin_direction_dephasing_memory_times_median")),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Reading", ""])
    if best is None:
        lines.append("No finite baseline KnotScore was available; inspect raw diagnostics before extending N.")
    else:
        lines.append(
            "The strongest short-run baseline score in this sweep occurs near "
            f"`epsilon={float(best['epsilon']):.3e}` with median score {_fmt(best.get('score_median'))}."
        )
    if score_plateau:
        lines.append(
            "The `score >= 0.75` band spans approximately "
            f"`epsilon={min(float(row['epsilon']) for row in score_plateau):.3e}` to "
            f"`{max(float(row['epsilon']) for row in score_plateau):.3e}` in this 100k pilot."
        )
    if failure_band:
        lines.append(
            "The first high-noise collapse back toward the `eta_zero`-like score occurs by "
            f"`epsilon={min(float(row['epsilon']) for row in failure_band):.3e}`."
        )
    lines.extend(
        [
            "",
            "Use this sweep as a threshold finder, not as final evidence. The relevant",
            "signal is a band where radius and radius-normalized center drift improve",
            "against `eta_zero` without creating only a deterministic zero-start artifact.",
            "Spin quantities use `r = x - c_memory` and the co-moving velocity",
            "`d(x - c_memory)/dt`; the adjacent laboratory-frame amplitude reports the",
            "translation removed by that correction. Persistent internal circulation would",
            "require amplitude, axis polarization, and dephasing to separate from controls.",
            "A large angular-speed proxy alone is insufficient.",
            "",
            "## Figures",
            "",
        ]
    )
    for figure in figures:
        lines.append(f"- `{figure.relative_to(ROOT).as_posix()}`")
    lines.extend(["", "## Machine Output", "", f"- `{output_json.relative_to(ROOT).as_posix()}`"])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_sweep(args: argparse.Namespace, epsilons: list[float], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    trace_window_updates = int(math.ceil(args.trace_window_memory_times / args.alpha))
    started = time.perf_counter()
    cases: list[dict[str, Any]] = []
    for epsilon in epsilons:
        config = SimulationConfig(
            steps=args.steps,
            dim=args.dim,
            epsilon=float(epsilon),
            eta=args.eta,
            alpha=args.alpha,
            memory_mass=args.memory_mass,
            deposition_kernel=args.deposition_kernel,
            deposition_sigma=args.deposition_sigma,
            sigma_rep=args.sigma_rep,
            sigma_att=args.sigma_att,
            amplitude_rep=args.amplitude_rep,
            amplitude_att=args.amplitude_att,
            memory_factor=args.memory_factor,
            max_memory=args.max_memory,
            burn_in=args.burn_in,
            sample_every=args.sample_every,
        )
        trace_targets = metastability_run._trace_targets(
            steps=config.steps,
            burn_in=config.burn_in,
            trace_every=args.trace_every,
            trace_points=args.trace_points,
            trace_spacing=args.trace_spacing,
            trace_window_updates=trace_window_updates,
        )
        epsilon_dir = output_dir / f"eps_{_epsilon_token(float(epsilon))}"
        for condition in args.conditions:
            for seed in args.seeds:
                print(
                    f"running epsilon={epsilon:.6e} condition={condition} seed={seed} steps={args.steps}",
                    flush=True,
                )
                payload = metastability_run.run_case(
                    base_config=config,
                    condition=condition,
                    seed=seed,
                    voxel_sizes=args.voxel_sizes,
                    max_ac_lag=args.max_ac_lag,
                    min_memory_times=args.min_memory_times,
                    output_dir=epsilon_dir,
                    force_components=False,
                    trace_every=args.trace_every,
                    trace_targets=trace_targets,
                )
                cases.append(payload)
    run_summary = {
        "description": "Short epsilon sensitivity sweep for dynamic-center knot benchmarks.",
        "started_utc": _utc_now(),
        "total_elapsed_seconds": time.perf_counter() - started,
        "epsilons": epsilons,
        "conditions": args.conditions,
        "seeds": args.seeds,
        "base_config": asdict(
            SimulationConfig(
                steps=args.steps,
                dim=args.dim,
                epsilon=0.0,
                eta=args.eta,
                alpha=args.alpha,
                memory_mass=args.memory_mass,
                deposition_kernel=args.deposition_kernel,
                deposition_sigma=args.deposition_sigma,
                sigma_rep=args.sigma_rep,
                sigma_att=args.sigma_att,
                amplitude_rep=args.amplitude_rep,
                amplitude_att=args.amplitude_att,
                memory_factor=args.memory_factor,
                max_memory=args.max_memory,
                burn_in=args.burn_in,
                sample_every=args.sample_every,
            )
        )
        | {"epsilon": "sweep_axis"},
        "case_count": len(cases),
    }
    (output_dir / "sweep_summary.json").write_text(
        json.dumps(run_summary, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run and report epsilon sensitivity for dynamic-center knot traces.")
    parser.add_argument("--skip-run", action="store_true", help="only aggregate existing raw JSON outputs")
    parser.add_argument("--steps", type=int, default=100_000)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument("--seeds", type=_parse_int_list, default=_parse_int_list("1,2,3"))
    parser.add_argument("--conditions", type=metastability_run._parse_conditions, default=metastability_run._parse_conditions("baseline,eta_zero"))
    parser.add_argument("--epsilons", type=_parse_float_list, default=DEFAULT_EPSILONS)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--deposition-kernel", choices=sorted(metastability_run.DEPOSITION_KERNELS), default="delta")
    parser.add_argument("--deposition-sigma", type=float, default=0.0)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=35.0)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--max-memory", type=int, default=600)
    parser.add_argument("--burn-in", type=int, default=0)
    parser.add_argument("--sample-every", type=int, default=100)
    parser.add_argument("--trace-every", type=int, default=1)
    parser.add_argument("--trace-points", type=int, default=80)
    parser.add_argument("--trace-spacing", choices=("linear", "log"), default="log")
    parser.add_argument("--trace-window-memory-times", type=float, default=50.0)
    parser.add_argument("--voxel-sizes", type=_parse_float_list, default=_parse_float_list("0.5,1.0,2.0"))
    parser.add_argument("--max-ac-lag", type=int, default=50)
    parser.add_argument("--min-memory-times", type=float, default=10.0)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed/long_run_metastability/epsilon_dynamic_center_q3_Aatt_35_N100k_seed1-3_2026-07-12"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/long_runs/epsilon/epsilon_dynamic_center_q3_Aatt35_N100k_2026-07-12.md"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("reports/long_runs/epsilon/epsilon_dynamic_center_q3_Aatt35_N100k_summary_2026-07-12.json"),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/epsilon_dynamic_center"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    epsilons = [float(value) for value in args.epsilons]
    if not args.skip_run:
        run_sweep(args, epsilons, output_dir)
    rows = build_rows(output_dir)
    if not rows:
        raise SystemExit(f"no case rows found under {output_dir}")
    summary = build_summary(rows)
    figure_dir = args.figure_dir if args.figure_dir.is_absolute() else ROOT / args.figure_dir
    figures = write_plots(output_dir, rows, figure_dir)
    output_json = args.output_json if args.output_json.is_absolute() else ROOT / args.output_json
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps({"rows": rows, "summary": summary}, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )
    report_path = args.report if args.report.is_absolute() else ROOT / args.report
    write_report(
        rows=rows,
        summary=summary,
        figures=figures,
        output_dir=output_dir,
        output_json=output_json,
        report_path=report_path,
    )
    print(f"wrote report to {report_path}", flush=True)


if __name__ == "__main__":
    main()



