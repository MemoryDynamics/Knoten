from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import statistics
import sys
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

sys.path.insert(0, str(ROOT / "src"))


SOURCE_RE = re.compile(
    r"dynamic_center_trace_q3_Aatt_(?P<a_att>[\dp]+)_N(?P<n>[\dMk]+)_seed"
)


@dataclass(frozen=True)
class CaseRecord:
    a_att: float
    steps: int
    condition: str
    seed: int
    path: Path
    payload: dict[str, Any]


def _parse_steps(value: str) -> int:
    if value.endswith("k"):
        return int(value[:-1]) * 1_000
    if value.endswith("M"):
        return int(value[:-1]) * 1_000_000
    return int(value)


def _parse_float_token(value: str) -> float:
    return float(value.replace("p", "."))


def _format_count(value: int | None) -> str:
    if value is None:
        return "n/a"
    if value >= 1_000_000 and value % 1_000_000 == 0:
        return f"{value // 1_000_000}M"
    if value >= 1_000 and value % 1_000 == 0:
        return f"{value // 1_000}k"
    return f"{value:,}"


def _fmt(value: float | int | None, digits: int = 3) -> str:
    if value is None:
        return "`n/a`"
    number = float(value)
    if not math.isfinite(number):
        return "`n/a`"
    if number == 0.0:
        text = "0"
    elif abs(number) < 1e-3 or abs(number) >= 1e4:
        text = f"{number:.{digits}e}"
    else:
        text = f"{number:.{digits}f}"
    return f"`{text}`"


def _median(values: Iterable[float | None]) -> float | None:
    finite = [float(value) for value in values if value is not None and math.isfinite(float(value))]
    return statistics.median(finite) if finite else None


def _iqr(values: Iterable[float | None]) -> tuple[float | None, float | None]:
    finite = sorted(float(value) for value in values if value is not None and math.isfinite(float(value)))
    if not finite:
        return None, None
    if len(finite) == 1:
        return finite[0], finite[0]
    q1, _, q3 = statistics.quantiles(finite, n=4, method="inclusive")
    return q1, q3


def _diagnostic_value(diagnostics: dict[str, Any], path: tuple[str, ...]) -> float | None:
    value: Any = diagnostics
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    if value is None:
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def _best_voxel_residence(diagnostics: dict[str, Any]) -> float | None:
    payload = diagnostics.get("residence_by_voxel_size")
    if not isinstance(payload, dict):
        return None
    values: list[float] = []
    for item in payload.values():
        if not isinstance(item, dict):
            continue
        value = item.get("max_residence_memory_times")
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(number):
            values.append(number)
    return max(values) if values else None


def _steps_label(rows: list[dict[str, Any]]) -> str:
    values = sorted({int(row["steps"]) for row in rows if row.get("steps") is not None})
    if not values:
        return "N=n/a"
    if len(values) == 1:
        return f"N={_format_count(values[0])}"
    return "N in {" + ", ".join(_format_count(value) for value in values) + "}"


def _seed_label(rows: list[dict[str, Any]]) -> str:
    values = sorted({int(row["seed"]) for row in rows if row.get("seed") is not None})
    if not values:
        return "n/a"
    if values == list(range(values[0], values[-1] + 1)):
        return f"{values[0]}..{values[-1]}"
    return ",".join(str(value) for value in values)


def _a_label(rows: list[dict[str, Any]]) -> str:
    values = sorted({float(row["a_att"]) for row in rows if row.get("a_att") is not None})
    return "{" + ",".join(f"{value:g}" for value in values) + "}" if values else "n/a"


def _condition_label(rows: list[dict[str, Any]]) -> str:
    values = sorted({str(row["condition"]) for row in rows if row.get("condition") is not None})
    return "{" + ",".join(values) + "}" if values else "n/a"


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _load_cases(source_dirs: list[Path]) -> list[CaseRecord]:
    cases: list[CaseRecord] = []
    for source_dir in source_dirs:
        directory = source_dir if source_dir.is_absolute() else ROOT / source_dir
        match = SOURCE_RE.search(directory.name)
        if match is None:
            continue
        a_att = _parse_float_token(match.group("a_att"))
        steps = _parse_steps(match.group("n"))
        for path in sorted(directory.glob("case_*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            cases.append(
                CaseRecord(
                    a_att=a_att,
                    steps=steps,
                    condition=str(payload.get("condition")),
                    seed=int(payload.get("seed")),
                    path=path,
                    payload=payload,
                )
            )
    return cases


def _case_row(case: CaseRecord) -> dict[str, Any]:
    diagnostics = case.payload["diagnostics"]
    dynamic = diagnostics.get("dynamic_center_trace", {})
    if not isinstance(dynamic, dict):
        dynamic = {}
    spin = dynamic.get("spin_proxy", {})
    if not isinstance(spin, dict):
        spin = {}
    memory_cloud = diagnostics.get("memory_cloud", {})
    memory_shape = memory_cloud.get("shape", {}) if isinstance(memory_cloud, dict) else {}
    if not isinstance(memory_shape, dict):
        memory_shape = {}
    return {
        "a_att": case.a_att,
        "steps": case.steps,
        "condition": case.condition,
        "seed": case.seed,
        "path": _rel(case.path),
        "best_residence_memory_times": _best_voxel_residence(diagnostics),
        "memory_center_residence_memory_times": _diagnostic_value(
            diagnostics,
            ("center_residence", "memory_center", "primary_max_run_memory_times"),
        ),
        "dynamic_trace_count": _diagnostic_value(dynamic, ("n_traces",)),
        "dynamic_inside_fraction": _diagnostic_value(dynamic, ("comoving_inside_fraction",)),
        "dynamic_inside_fraction_time_weighted": (
            _diagnostic_value(dynamic, ("comoving_inside_fraction_time_weighted",))
            or _diagnostic_value(dynamic, ("comoving_inside_fraction",))
        ),
        "dynamic_max_run_memory_times": _diagnostic_value(dynamic, ("max_run_memory_times",)),
        "dynamic_rms_radius_median": _diagnostic_value(dynamic, ("rms_radius_median",)),
        "dynamic_x_distance_to_radius_median": _diagnostic_value(
            dynamic, ("x_distance_to_rms_radius_median",)
        ),
        "dynamic_center_drift_per_memory_time": _diagnostic_value(
            dynamic, ("center_drift_per_memory_time_median",)
        ),
        "dynamic_center_drift_radius_fraction_per_memory_time": _diagnostic_value(
            dynamic, ("center_drift_radius_fraction_per_memory_time_median",)
        ),
        "spin_valid_fraction": _diagnostic_value(spin, ("valid_fraction",)),
        "spin_amplitude_median": _diagnostic_value(spin, ("amplitude_median",)),
        "spin_amplitude_cv": _diagnostic_value(spin, ("amplitude_cv",)),
        "spin_angular_speed_median": _diagnostic_value(spin, ("angular_speed_median",)),
        "spin_axis_polarization": _diagnostic_value(spin, ("axis_polarization",)),
        "spin_direction_dephasing_memory_times": _diagnostic_value(
            spin, ("direction_dephasing_memory_times",)
        ),
        "spin_signed_component_median": _diagnostic_value(spin, ("signed_component_median",)),
        "memory_shape_dimension": _diagnostic_value(memory_shape, ("effective_dimension",)),
        "memory_roundness": _diagnostic_value(memory_shape, ("axis_ratio_min_max",)),
        "memory_radius": _diagnostic_value(memory_shape, ("mean_radius",)),
    }


SUMMARY_METRICS = [
    "best_residence_memory_times",
    "memory_center_residence_memory_times",
    "dynamic_trace_count",
    "dynamic_inside_fraction",
    "dynamic_inside_fraction_time_weighted",
    "dynamic_max_run_memory_times",
    "dynamic_rms_radius_median",
    "dynamic_x_distance_to_radius_median",
    "dynamic_center_drift_per_memory_time",
    "dynamic_center_drift_radius_fraction_per_memory_time",
    "spin_valid_fraction",
    "spin_amplitude_median",
    "spin_amplitude_cv",
    "spin_angular_speed_median",
    "spin_axis_polarization",
    "spin_direction_dephasing_memory_times",
    "spin_signed_component_median",
    "memory_shape_dimension",
    "memory_roundness",
    "memory_radius",
]


def build_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[float, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(float(row["a_att"]), str(row["condition"]))].append(row)

    summary: list[dict[str, Any]] = []
    for (a_att, condition), group in sorted(grouped.items()):
        item: dict[str, Any] = {
            "a_att": a_att,
            "condition": condition,
            "n": len(group),
            "steps": int(group[0]["steps"]) if group else None,
        }
        for metric in SUMMARY_METRICS:
            values = [row.get(metric) for row in group]
            q1, q3 = _iqr(values)
            item[f"{metric}_median"] = _median(values)
            item[f"{metric}_q1"] = q1
            item[f"{metric}_q3"] = q3
        summary.append(item)
    return summary


def _row_values(rows: list[dict[str, Any]], a_att: float, condition: str, metric: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        if float(row["a_att"]) != float(a_att) or row["condition"] != condition:
            continue
        value = row.get(metric)
        if value is None:
            continue
        number = float(value)
        if math.isfinite(number):
            values.append(number)
    return values


def _scatter_metric(
    ax: Any,
    rows: list[dict[str, Any]],
    *,
    metric: str,
    title: str,
    ylabel: str,
    a_values: list[float],
    log_y: bool = False,
) -> None:
    colors = {"baseline": "#2563eb", "eta_zero": "#64748b"}
    offsets = {"baseline": -0.13, "eta_zero": 0.13}
    labels_seen: set[str] = set()
    x_positions: list[float] = []
    x_labels: list[str] = []
    for index, a_att in enumerate(a_values):
        x_positions.append(float(index))
        x_labels.append(f"{a_att:g}")
        for condition in ["baseline", "eta_zero"]:
            values = _row_values(rows, a_att, condition, metric)
            if log_y:
                values = [value for value in values if value > 0.0]
            if not values:
                continue
            x = index + offsets.get(condition, 0.0)
            label = condition if condition not in labels_seen else None
            labels_seen.add(condition)
            ax.scatter(
                [x] * len(values),
                values,
                s=42,
                alpha=0.75,
                color=colors.get(condition, "#0f172a"),
                edgecolor="white",
                linewidth=0.5,
                label=label,
            )
            median = statistics.median(values)
            q1, q3 = _iqr(values)
            ax.plot([x - 0.08, x + 0.08], [median, median], color=colors.get(condition, "#0f172a"), linewidth=2.4)
            if q1 is not None and q3 is not None:
                ax.vlines(x, q1, q3, color=colors.get(condition, "#0f172a"), linewidth=2.0, alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel("A_att")
    ax.set_ylabel(ylabel)
    ax.set_xticks(x_positions, x_labels)
    if log_y:
        ax.set_yscale("log")
    ax.grid(True, which="both", alpha=0.25)
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(handles, labels, frameon=False)


def _trace(case: CaseRecord) -> dict[str, list[Any]]:
    diagnostics = case.payload["diagnostics"]
    dynamic = diagnostics.get("dynamic_center_trace", {})
    trace = dynamic.get("trace", {}) if isinstance(dynamic, dict) else {}
    return trace if isinstance(trace, dict) else {}


def _case_alpha(case: CaseRecord) -> float:
    config = case.payload.get("config", {})
    if not isinstance(config, dict):
        return 1.0
    try:
        value = float(config.get("alpha", 1.0))
    except (TypeError, ValueError):
        return 1.0
    return value if math.isfinite(value) and value > 0.0 else 1.0


def _spin_trace_from_case(case: CaseRecord) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    trace = _trace(case)
    steps = np.asarray(trace.get("steps", []), dtype=float)
    centers = np.asarray(trace.get("centers", []), dtype=float)
    positions = np.asarray(trace.get("positions", []), dtype=float)
    radii = np.asarray(trace.get("rms_radii", []), dtype=float)
    if steps.size < 2 or centers.shape != positions.shape or centers.ndim != 2:
        empty = np.empty(0, dtype=float)
        return empty, empty, empty
    alpha = _case_alpha(case)
    gaps = np.diff(steps) * alpha
    valid_gap = np.isfinite(gaps) & (gaps > 0.0)
    if not np.any(valid_gap):
        empty = np.empty(0, dtype=float)
        return empty, empty, empty
    rel = positions - centers
    velocity = np.diff(positions, axis=0)[valid_gap] / gaps[valid_gap, None]
    rel_mid = 0.5 * (rel[:-1] + rel[1:])[valid_gap]
    radius_mid = 0.5 * (radii[:-1] + radii[1:])[valid_gap]
    times = 0.5 * (steps[:-1] + steps[1:])[valid_gap] * alpha
    dim = rel_mid.shape[1]
    if dim == 3:
        components = np.cross(rel_mid, velocity)
    elif dim >= 2:
        pieces = []
        for i in range(dim):
            for j in range(i + 1, dim):
                pieces.append(rel_mid[:, i] * velocity[:, j] - rel_mid[:, j] * velocity[:, i])
        components = np.stack(pieces, axis=1) if pieces else np.empty((len(times), 0), dtype=float)
    else:
        components = np.empty((len(times), 0), dtype=float)
    if components.shape[1] == 0:
        empty = np.empty(0, dtype=float)
        return empty, empty, empty
    amplitude = np.linalg.norm(components, axis=1)
    angular_speed = np.full(amplitude.shape, np.nan, dtype=float)
    valid_radius = np.isfinite(radius_mid) & (radius_mid > 0.0) & np.isfinite(amplitude)
    angular_speed[valid_radius] = amplitude[valid_radius] / (radius_mid[valid_radius] ** 2)
    return times, amplitude, angular_speed

def _representative_cases(cases: list[CaseRecord]) -> list[CaseRecord]:
    selected: list[CaseRecord] = []
    for a_att in sorted({case.a_att for case in cases}):
        for condition in ["baseline", "eta_zero"]:
            options = [
                case
                for case in cases
                if float(case.a_att) == float(a_att)
                and case.condition == condition
                and case.seed == 1
                and _trace(case)
            ]
            if options:
                selected.append(options[0])
    return selected


def write_plots(cases: list[CaseRecord], rows: list[dict[str, Any]], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    a_values = sorted({float(row["a_att"]) for row in rows})
    run_label = _steps_label(rows)
    outputs: list[Path] = []

    specs = [
        (
            "dynamic_center_trace_q3_compactness_drift_2026-07-12.png",
            [
                ("dynamic_rms_radius_median", "Dynamic Memory Radius", "median RMS radius", True),
                (
                    "dynamic_center_drift_radius_fraction_per_memory_time",
                    "Center Drift / Radius",
                    "radius fractions per memory time",
                    True,
                ),
                ("memory_shape_dimension", "Memory Shape Dimension", "dimension", False),
            ],
        ),
        (
            "dynamic_center_trace_q3_residence_observables_2026-07-12.png",
            [
                ("best_residence_memory_times", "Voxel Residence", "memory times", True),
                ("memory_center_residence_memory_times", "Final Memory-Center Residence", "memory times", True),
                ("dynamic_max_run_memory_times", "Dynamic Center Max Run", "memory times", True),
                ("dynamic_inside_fraction_time_weighted", "Dynamic Inside Fraction", "time-weighted fraction", False),
            ],
        ),
        (
            "dynamic_center_trace_q3_spin_proxy_2026-07-12.png",
            [
                ("spin_amplitude_median", "Spin-Proxy Amplitude", "median |r wedge v|", True),
                ("spin_angular_speed_median", "Angular Speed Proxy", "median |L| / R^2", True),
                ("spin_axis_polarization", "Axis Polarization", "|mean unit axis|", False),
                (
                    "spin_direction_dephasing_memory_times",
                    "Axis Dephasing",
                    "memory times to 1/e",
                    True,
                ),
            ],
        ),
    ]
    for filename, panels in specs:
        fig, axes = plt.subplots(1, len(panels), figsize=(5.0 * len(panels), 4.2), squeeze=False)
        for ax, (metric, title, ylabel, log_y) in zip(axes[0], panels, strict=True):
            _scatter_metric(
                ax,
                rows,
                metric=metric,
                title=title,
                ylabel=ylabel,
                a_values=a_values,
                log_y=log_y,
            )
        fig.suptitle(f"Dynamic center trace validation, {run_label}", y=1.03)
        fig.tight_layout()
        path = output_dir / filename
        fig.savefig(path, dpi=220, bbox_inches="tight")
        plt.close(fig)
        outputs.append(path)

    representatives = _representative_cases(cases)
    if representatives:
        fig, axes = plt.subplots(3, len(representatives), figsize=(4.2 * len(representatives), 8.4), squeeze=False)
        for col, case in enumerate(representatives):
            trace = _trace(case)
            alpha = _case_alpha(case)
            steps = [float(value) * alpha for value in trace.get("steps", [])]
            radii = [float(value) for value in trace.get("rms_radii", [])]
            xdist = [float(value) for value in trace.get("x_distances", [])]
            ratio = [
                (dist / radius) if radius > 0.0 else math.nan
                for dist, radius in zip(xdist, radii, strict=False)
            ]
            axes[0, col].plot(steps, radii, color="#2563eb" if case.condition == "baseline" else "#64748b")
            axes[0, col].set_title(f"A_att={case.a_att:g}, {case.condition}, seed {case.seed}")
            axes[0, col].set_ylabel("RMS radius")
            axes[0, col].grid(True, alpha=0.25)
            axes[1, col].plot(steps, ratio, color="#0f766e")
            axes[1, col].axhline(2.0, color="#dc2626", linestyle="--", linewidth=1.0)
            axes[1, col].set_ylabel("x distance / RMS radius")
            axes[1, col].grid(True, alpha=0.25)
            spin_times, _, spin_omega = _spin_trace_from_case(case)
            finite_spin = np.isfinite(spin_times) & np.isfinite(spin_omega) & (spin_omega > 0.0)
            if np.any(finite_spin):
                axes[2, col].plot(spin_times[finite_spin], spin_omega[finite_spin], color="#7c3aed")
                axes[2, col].set_yscale("log")
            else:
                axes[2, col].text(0.5, 0.5, "n/a", ha="center", va="center", transform=axes[2, col].transAxes)
            axes[2, col].set_xlabel("memory times")
            axes[2, col].set_ylabel("spin |L| / R^2")
            axes[2, col].grid(True, which="both", alpha=0.25)
        fig.suptitle("Representative dynamic trace, seed 1", y=1.02)
        fig.tight_layout()
        path = output_dir / "dynamic_center_trace_q3_seed1_timeseries_2026-07-12.png"
        fig.savefig(path, dpi=220, bbox_inches="tight")
        plt.close(fig)
        outputs.append(path)
    return outputs


def write_report(
    *,
    summary: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    figures: list[Path],
    output_json: Path,
    output_path: Path,
) -> None:
    lines: list[str] = [
        "# Dynamic Center and Spin-Proxy Trace Validation",
        "",
        "Date: 2026-07-12.",
        "",
        "## Scope",
        "",
        "This report aggregates dynamic memory-center traces and the new",
        "seedwise spin-proxy observables. It is a pre-long-run methodology check,",
        "not a replacement for the `N=300M` evidence set.",
        "",
        f"Run label: `{_steps_label(rows)}`.",
        f"Seeds: `{_seed_label(rows)}`.",
        f"A_att values: `{_a_label(rows)}`.",
        f"Conditions: `{_condition_label(rows)}`.",
        "",
        "The spin proxy is the co-moving angular-momentum bivector",
        "`L = (x - c_mem) wedge dx/dt_mem`, where `c_mem` is the contemporaneous",
        "memory center and `t_mem = alpha n`. It is a continuous diagnostic of",
        "amplitude, angular speed, axis polarization, and dephasing. It is not a",
        "claim of quantized spin.",
        "",
        "## Dynamic-Center Median Summary",
        "",
        "| A_att | condition | dyn radius | dyn drift/radius/memtime | dyn inside weighted | dyn max run | final-center residence | voxel residence | memory dim | memory roundness |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{float(row['a_att']):g}`",
                    f"`{row['condition']}`",
                    _fmt(row.get("dynamic_rms_radius_median_median")),
                    _fmt(row.get("dynamic_center_drift_radius_fraction_per_memory_time_median")),
                    _fmt(row.get("dynamic_inside_fraction_time_weighted_median")),
                    _fmt(row.get("dynamic_max_run_memory_times_median")),
                    _fmt(row.get("memory_center_residence_memory_times_median")),
                    _fmt(row.get("best_residence_memory_times_median")),
                    _fmt(row.get("memory_shape_dimension_median")),
                    _fmt(row.get("memory_roundness_median")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Spin-Proxy Median Summary",
            "",
            "| A_att | condition | valid frac | amplitude | angular speed | axis polarization | dephase time | signed comp | amplitude CV |",
            "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{float(row['a_att']):g}`",
                    f"`{row['condition']}`",
                    _fmt(row.get("spin_valid_fraction_median")),
                    _fmt(row.get("spin_amplitude_median_median")),
                    _fmt(row.get("spin_angular_speed_median_median")),
                    _fmt(row.get("spin_axis_polarization_median")),
                    _fmt(row.get("spin_direction_dephasing_memory_times_median")),
                    _fmt(row.get("spin_signed_component_median_median")),
                    _fmt(row.get("spin_amplitude_cv_median")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Reading",
            "",
            "The dynamic-center diagnostics remain the primary knot observables:",
            "compact co-moving radius, slow normalized center drift, memory-shape",
            "dimension/roundness, and residence controls. The spin proxy adds a",
            "seedwise test for persistent oriented circulation around the moving",
            "memory center.",
            "",
            "Interpretation rules for this stage:",
            "",
            "- `spin_amplitude_median` measures the typical co-moving angular momentum scale.",
            "- `spin_angular_speed_median` divides that amplitude by the squared memory radius.",
            "- `spin_axis_polarization` near `1` means a stable oriented axis; near `0` means",
            "  strong axis dephasing or axis wandering across the trace.",
            "- `spin_direction_dephasing_memory_times` is the first autocorrelation lag below",
            "  `1/e`, if that crossing occurs within the stored trace lags.",
            "- `eta_zero` can still generate incidental angular momentum from random walks, so",
            "  active conditions only become interesting if amplitude, axis stability, or",
            "  dephasing separate seedwise from matched controls and remain stable with N.",
            "",
            "For the current pre-long-run scale, these values should be read as observable",
            "calibration, not as particle-spin evidence.",
            "",
            "## Decision",
            "",
            "Use this trace layer to decide whether the next expensive run has stable",
            "co-moving compactness and stable or dephasing spin proxies. If the spin",
            "metrics are noisy but the compactness/drift metrics remain separated from",
            "`eta_zero`, continue the scalar-knot track. If spin-axis persistence appears",
            "only in active cases and survives longer N, it becomes a candidate input for",
            "a separate ModeScore or vector-memory test, not a KnotScore replacement.",
            "",
            "## Figures",
            "",
        ]
    )
    for figure in figures:
        lines.append(f"- `{_rel(figure)}`")
    lines.extend(
        [
            "",
            "## Raw Rows",
            "",
            f"- Case rows: `{len(rows)}`.",
            f"- Machine-readable aggregate: `{_rel(output_json)}`.",
            "- Raw JSON outputs remain under ignored `data/processed/long_run_metastability/`.",
        ]
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate dynamic center trace validation runs.")
    parser.add_argument(
        "--source-glob",
        default="data/processed/long_run_metastability/dynamic_center_trace_q3_Aatt_*_N3M_seed1-5_2026-07-12",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("reports/long_runs/long_3e8/dynamic_center_trace_q3_N3M_summary_2026-07-12.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/long_runs/long_3e8/dynamic_center_trace_q3_N3M_2026-07-12.md"),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/dynamic_center"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dirs = sorted(ROOT.glob(args.source_glob))
    if not source_dirs:
        raise SystemExit(f"no source directories match {args.source_glob!r}")
    cases = _load_cases(source_dirs)
    if not cases:
        raise SystemExit("no case JSON files found")
    rows = [_case_row(case) for case in cases]
    summary = build_summary(rows)
    figure_dir = args.figure_dir if args.figure_dir.is_absolute() else ROOT / args.figure_dir
    figures = write_plots(cases, rows, figure_dir)
    output_json = args.output_json if args.output_json.is_absolute() else ROOT / args.output_json
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(
            {
                "run_label": _steps_label(rows),
                "source_dirs": [path.relative_to(ROOT).as_posix() for path in source_dirs],
                "rows": rows,
                "summary": summary,
                "figures": [path.relative_to(ROOT).as_posix() for path in figures],
            },
            indent=2,
            sort_keys=True,
            allow_nan=False,
        ),
        encoding="utf-8",
    )
    report = args.report if args.report.is_absolute() else ROOT / args.report
    write_report(summary=summary, rows=rows, figures=figures, output_json=output_json, output_path=report)
    print(f"wrote {output_json}")
    print(f"wrote {report}")
    for figure in figures:
        print(f"wrote {figure}")


if __name__ == "__main__":
    main()
