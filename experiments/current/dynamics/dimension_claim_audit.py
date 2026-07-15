from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import statistics
import subprocess
from typing import Any, Iterable

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from emergenz_knoten import covariance_dimension, spectral_dimension
from emergenz_knoten.diagnostics import fit_occupancy_scaling_window, occupancy_dimension


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()


DEFAULT_SOURCE_DIRS = [
    Path(
        "data/processed/long_run_metastability/"
        "dynamic_center_trace_q3_Aatt_35_N30M_seed1-5_eps1em4_rerun_2026-07-13"
    ),
    Path(
        "data/processed/long_run_metastability/"
        "ambient_dim_memory_shape_Aatt_35_N30M_d4_seed1-5_eps1em4_2026-07-13"
    ),
    Path(
        "data/processed/long_run_metastability/"
        "ambient_dim_memory_shape_Aatt_35_N30M_d5_seed1-5_eps1em4_2026-07-13"
    ),
    Path(
        "data/processed/long_run_metastability/"
        "ambient_dim_memory_shape_Aatt_35_N30M_d7_seed1-5_eps1em4_2026-07-13"
    ),
    Path(
        "data/processed/long_run_metastability/"
        "ambient_dim_memory_shape_Aatt_35_N30M_d10_seed1-5_eps1em4_2026-07-13"
    ),
    Path(
        "data/processed/long_run_metastability/"
        "ambient_dim_memory_shape_Aatt_35_N30M_d13_seed1-5_eps1em4_2026-07-13"
    ),
    Path(
        "data/processed/long_run_metastability/"
        "ambient_dim_memory_shape_Aatt_35_N30M_d20_seed1-5_eps1em4_2026-07-13"
    ),
]


SUMMARY_METRICS = [
    "dynamic_radius",
    "dynamic_drift_radius",
    "sample_covariance_dimension",
    "sample_occupancy_window_dimension",
    "sample_spectral_dimension",
    "memory_shape_dimension",
    "memory_d90",
    "memory_d95",
    "memory_spectral_dimension",
    "memory_roundness",
    "center_trace_covariance_dimension",
    "center_trace_occupancy_window_dimension",
    "center_trace_spectral_dimension",
    "center_trace_point_count",
]


@dataclass(frozen=True)
class CaseRecord:
    dim: int
    condition: str
    seed: int
    steps: int
    path: Path
    payload: dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit the current 3D-dimension claim ladder from existing case JSON outputs."
    )
    parser.add_argument(
        "--source-dir",
        action="append",
        type=Path,
        help="Directory containing case_*.json files. Defaults to the current d3 and ambient-d N30M slices.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/dimensions/dimension_claim_audit_2026-07-15.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/dimensions/dimension_claim_audit_summary_2026-07-15.json"),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/dimensions/dimension_claim_audit_2026-07-15"),
    )
    parser.add_argument(
        "--center-trace-min-gap-memory-times",
        type=float,
        default=1.0,
        help="Minimum memory-time spacing for low-pass center-trace diagnostics.",
    )
    parser.add_argument(
        "--center-trace-spectral-points",
        type=int,
        default=300,
        help="Maximum center-trace points used for spectral dimension.",
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _rel_from(source_file: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source_file.resolve().parent)).as_posix()


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


def _git_status_inline() -> str:
    return (_git_output(["status", "--short"]) or "clean").replace("\n", "; ")


def _finite_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _diagnostic_value(payload: dict[str, Any], path: tuple[str, ...]) -> float | None:
    value: Any = payload
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return _finite_float(value)


def _median(values: Iterable[Any]) -> float | None:
    finite = [float(value) for value in values if _finite_float(value) is not None]
    return statistics.median(finite) if finite else None


def _iqr(values: Iterable[Any]) -> tuple[float | None, float | None]:
    finite = sorted(float(value) for value in values if _finite_float(value) is not None)
    if not finite:
        return None, None
    if len(finite) == 1:
        return finite[0], finite[0]
    q1, _, q3 = statistics.quantiles(finite, n=4, method="inclusive")
    return q1, q3


def _fmt(value: Any, digits: int = 3) -> str:
    number = _finite_float(value)
    if number is None:
        return "`n/a`"
    if number == 0.0:
        text = "0"
    elif abs(number) < 1e-3 or abs(number) >= 1e4:
        text = f"{number:.{digits}e}"
    else:
        text = f"{number:.{digits}f}"
    return f"`{text}`"


def _fmt_iqr(median: Any, q1: Any, q3: Any) -> str:
    return f"{_fmt(median)} [{_fmt(q1)}, {_fmt(q3)}]"


def variance_axis_count(eigenvalues: Iterable[Any], fraction: float) -> float | None:
    values = np.asarray([float(v) for v in eigenvalues if _finite_float(v) is not None], dtype=float)
    values = values[values > 0.0]
    if values.size == 0:
        return None
    if not 0.0 < fraction <= 1.0:
        raise ValueError("fraction must be in (0, 1]")
    values = np.sort(values)[::-1]
    total = float(values.sum())
    if total <= 0.0:
        return None
    return float(int(np.searchsorted(np.cumsum(values) / total, fraction, side="left") + 1))


def _downsample_evenly(points: np.ndarray, max_points: int) -> np.ndarray:
    if max_points <= 0 or len(points) <= max_points:
        return points
    indices = np.linspace(0, len(points) - 1, max_points, dtype=int)
    return points[indices]


def _thin_trace_by_memory_time(
    *,
    steps: np.ndarray,
    points: np.ndarray,
    alpha: float,
    min_gap_memory_times: float,
) -> np.ndarray:
    if len(steps) == 0 or len(points) == 0:
        return np.empty((0, points.shape[1] if points.ndim == 2 else 0), dtype=float)
    if len(steps) != len(points):
        return np.empty((0, points.shape[1] if points.ndim == 2 else 0), dtype=float)
    if min_gap_memory_times <= 0.0:
        return points

    keep = [0]
    last_step = float(steps[0])
    for index, step in enumerate(steps[1:], start=1):
        if (float(step) - last_step) * alpha >= min_gap_memory_times:
            keep.append(index)
            last_step = float(step)
    if keep[-1] != len(steps) - 1:
        keep.append(len(steps) - 1)
    return points[np.asarray(keep, dtype=int)]


def _points_dimension_payload(
    points: np.ndarray,
    *,
    spectral_points: int,
) -> dict[str, float | int | bool | None]:
    if points.ndim != 2 or len(points) < 2:
        return {
            "point_count": int(len(points)) if points.ndim == 2 else 0,
            "covariance_dimension": None,
            "occupancy_window_dimension": None,
            "occupancy_window_valid": False,
            "spectral_dimension": None,
        }
    out: dict[str, float | int | bool | None] = {"point_count": int(len(points))}
    try:
        out["covariance_dimension"] = _finite_float(covariance_dimension(points))
    except ValueError:
        out["covariance_dimension"] = None
    try:
        occupancy = occupancy_dimension(points, return_details=True)
        window = fit_occupancy_scaling_window(
            occupancy.scales,
            occupancy.counts,
            n_samples=len(points),
        )
        out["occupancy_window_dimension"] = _finite_float(window.dimension)
        out["occupancy_window_valid"] = bool(window.valid_scaling)
    except (ValueError, FloatingPointError):
        out["occupancy_window_dimension"] = None
        out["occupancy_window_valid"] = False
    try:
        spectral_points_arr = _downsample_evenly(points, spectral_points)
        out["spectral_dimension"] = _finite_float(spectral_dimension(spectral_points_arr))
    except ValueError:
        out["spectral_dimension"] = None
    return out


def _load_case(path: Path) -> CaseRecord:
    payload = json.loads(path.read_text(encoding="utf-8"))
    config = payload.get("config")
    if not isinstance(config, dict):
        raise ValueError(f"missing config in {path}")
    return CaseRecord(
        dim=int(config["dim"]),
        condition=str(payload["condition"]),
        seed=int(payload["seed"]),
        steps=int(config["steps"]),
        path=path,
        payload=payload,
    )


def load_cases(source_dirs: Iterable[Path]) -> list[CaseRecord]:
    cases: list[CaseRecord] = []
    for source_dir in source_dirs:
        directory = _resolve(source_dir)
        for path in sorted(directory.glob("case_*.json")):
            cases.append(_load_case(path))
    return sorted(cases, key=lambda item: (item.steps, item.dim, item.condition, item.seed))


def case_row(
    case: CaseRecord,
    *,
    center_trace_min_gap_memory_times: float,
    center_trace_spectral_points: int,
) -> dict[str, Any]:
    diagnostics = case.payload.get("diagnostics", {})
    if not isinstance(diagnostics, dict):
        diagnostics = {}
    config = case.payload.get("config", {})
    if not isinstance(config, dict):
        config = {}
    alpha = float(config.get("alpha", 1.0))

    dynamic = diagnostics.get("dynamic_center_trace", {})
    if not isinstance(dynamic, dict):
        dynamic = {}
    trend = dynamic.get("trend", dynamic)
    if not isinstance(trend, dict):
        trend = dynamic
    trace = dynamic.get("trace", {})
    center_payload = {
        "point_count": 0,
        "covariance_dimension": None,
        "occupancy_window_dimension": None,
        "occupancy_window_valid": False,
        "spectral_dimension": None,
    }
    if isinstance(trace, dict):
        centers = np.asarray(trace.get("centers", []), dtype=float)
        steps = np.asarray(trace.get("steps", []), dtype=float)
        if centers.ndim == 2 and steps.ndim == 1:
            centers = _thin_trace_by_memory_time(
                steps=steps,
                points=centers,
                alpha=alpha,
                min_gap_memory_times=center_trace_min_gap_memory_times,
            )
            center_payload = _points_dimension_payload(
                centers,
                spectral_points=center_trace_spectral_points,
            )

    memory_cloud = diagnostics.get("memory_cloud", {})
    memory_shape = memory_cloud.get("shape", {}) if isinstance(memory_cloud, dict) else {}
    if not isinstance(memory_shape, dict):
        memory_shape = {}
    memory_eigenvalues = memory_shape.get("covariance_eigenvalues", [])
    sample_shape = diagnostics.get("sample_shape", {})
    if not isinstance(sample_shape, dict):
        sample_shape = {}
    occupancy = diagnostics.get("occupancy", {})
    scaling = occupancy.get("scaling_window", {}) if isinstance(occupancy, dict) else {}
    if not isinstance(scaling, dict):
        scaling = {}

    return {
        "steps": case.steps,
        "dim": case.dim,
        "condition": case.condition,
        "seed": case.seed,
        "path": _rel(case.path),
        "dynamic_radius": _diagnostic_value(trend, ("rms_radius_median",)),
        "dynamic_drift_radius": _diagnostic_value(
            trend, ("center_drift_radius_fraction_per_memory_time_median",)
        ),
        "sample_covariance_dimension": _diagnostic_value(sample_shape, ("effective_dimension",))
        or _diagnostic_value(diagnostics, ("covariance_dimension",)),
        "sample_occupancy_window_dimension": _diagnostic_value(scaling, ("dimension",)),
        "sample_spectral_dimension": _diagnostic_value(diagnostics, ("sample_spectral", "dimension")),
        "memory_shape_dimension": _diagnostic_value(memory_shape, ("effective_dimension",)),
        "memory_d90": variance_axis_count(memory_eigenvalues, 0.90),
        "memory_d95": variance_axis_count(memory_eigenvalues, 0.95),
        "memory_spectral_dimension": _diagnostic_value(memory_cloud, ("spectral", "dimension"))
        if isinstance(memory_cloud, dict)
        else None,
        "memory_roundness": _diagnostic_value(memory_shape, ("axis_ratio_min_max",)),
        "memory_axis_ratio_second_first": _diagnostic_value(memory_shape, ("axis_ratio_second_first",)),
        "memory_axis_ratio_third_first": _diagnostic_value(memory_shape, ("axis_ratio_third_first",)),
        "center_trace_covariance_dimension": center_payload["covariance_dimension"],
        "center_trace_occupancy_window_dimension": center_payload["occupancy_window_dimension"],
        "center_trace_occupancy_window_valid": center_payload["occupancy_window_valid"],
        "center_trace_spectral_dimension": center_payload["spectral_dimension"],
        "center_trace_point_count": center_payload["point_count"],
    }


def build_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(int(row["steps"]), int(row["dim"]), str(row["condition"]))].append(row)

    summary: list[dict[str, Any]] = []
    for (steps, dim, condition), group in sorted(grouped.items()):
        item: dict[str, Any] = {
            "steps": steps,
            "dim": dim,
            "condition": condition,
            "n": len(group),
        }
        for metric in SUMMARY_METRICS:
            values = [row.get(metric) for row in group]
            q1, q3 = _iqr(values)
            item[f"{metric}_median"] = _median(values)
            item[f"{metric}_q1"] = q1
            item[f"{metric}_q3"] = q3
        valid = [row.get("center_trace_occupancy_window_valid") for row in group]
        item["center_trace_occupancy_window_valid_fraction"] = (
            sum(1 for value in valid if bool(value)) / len(valid) if valid else None
        )
        summary.append(item)
    return summary


def _summary_by_key(summary: list[dict[str, Any]]) -> dict[tuple[int, int, str], dict[str, Any]]:
    return {(int(item["steps"]), int(item["dim"]), str(item["condition"])): item for item in summary}


def _ratio(numerator: Any, denominator: Any) -> float | None:
    num = _finite_float(numerator)
    den = _finite_float(denominator)
    if num is None or den in (None, 0.0):
        return None
    return num / den


def _delta(a: Any, b: Any) -> float | None:
    first = _finite_float(a)
    second = _finite_float(b)
    if first is None or second is None:
        return None
    return first - second


def _plot_audit(summary: list[dict[str, Any]], figure_dir: Path) -> list[Path]:
    figure_dir.mkdir(parents=True, exist_ok=True)
    baseline = [row for row in summary if row["condition"] == "baseline" and row["steps"] == 30_000_000]
    baseline.sort(key=lambda row: row["dim"])
    controls = [row for row in summary if row["condition"] == "eta_zero" and row["steps"] == 30_000_000]
    controls.sort(key=lambda row: row["dim"])
    paths: list[Path] = []

    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    series = [
        ("memory_shape_dimension", "D_mem", "#1f77b4"),
        ("memory_d90", "D_p90", "#9467bd"),
        ("memory_d95", "D_p95", "#8c564b"),
        ("memory_spectral_dimension", "D_spec memory", "#2ca02c"),
        ("center_trace_covariance_dimension", "D_cov center", "#d62728"),
    ]
    dims = [row["dim"] for row in baseline]
    for key, label, color in series:
        values = [row.get(f"{key}_median") for row in baseline]
        ax.plot(dims, values, marker="o", linewidth=1.8, label=label, color=color)
    ax.axhline(3.0, color="#444444", linestyle="--", linewidth=1.0, alpha=0.7)
    ax.set_xlabel("ambient dimension d")
    ax.set_ylabel("dimension diagnostic")
    ax.set_title("Baseline dimension diagnostics")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, ncol=2)
    fig.tight_layout()
    path = figure_dir / "dimension_claim_audit_baseline_dimensions.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    paths.append(path)

    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    dims = [row["dim"] for row in baseline]
    by_control = {row["dim"]: row for row in controls}
    radius_gain = [
        _ratio(by_control.get(row["dim"], {}).get("dynamic_radius_median"), row.get("dynamic_radius_median"))
        for row in baseline
    ]
    drift_gain = [
        _ratio(
            by_control.get(row["dim"], {}).get("dynamic_drift_radius_median"),
            row.get("dynamic_drift_radius_median"),
        )
        for row in baseline
    ]
    roundness_delta = [
        _delta(row.get("memory_roundness_median"), by_control.get(row["dim"], {}).get("memory_roundness_median"))
        for row in baseline
    ]
    ax.plot(dims, radius_gain, marker="o", label="radius gain eta0/baseline", color="#1f77b4")
    ax.plot(dims, drift_gain, marker="o", label="drift/r gain eta0/baseline", color="#d62728")
    ax.plot(dims, roundness_delta, marker="o", label="roundness delta", color="#2ca02c")
    ax.set_xlabel("ambient dimension d")
    ax.set_ylabel("control separation")
    ax.set_title("Baseline vs eta_zero separation")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    path = figure_dir / "dimension_claim_audit_control_separation.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    paths.append(path)
    return paths


def _build_report(
    *,
    rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    source_dirs: list[Path],
    summary_json: Path,
    figure_paths: list[Path],
    report_path: Path,
) -> str:
    by_key = _summary_by_key(summary)
    baseline_rows = [row for row in summary if row["condition"] == "baseline" and row["steps"] == 30_000_000]
    dims = sorted({int(row["dim"]) for row in baseline_rows})

    lines = [
        "# 3D Dimension Claim Audit",
        "",
        f"Date: {_utc_now()}.",
        "",
        "## Scope",
        "",
        "This audit turns the current 3D evidence into an explicit claim ladder.",
        "It reuses existing `A_att=35`, `epsilon=1e-4`, corrected q=3 scalar",
        "case JSONs and does not introduce a new long run.",
        "",
        "The audit separates four diagnostics:",
        "",
        "- `D_mem`: covariance participation dimension of the weighted memory cloud.",
        "- `D_p90`/`D_p95`: number of covariance axes needed for 90%/95% memory variance.",
        "- `D_spec memory`: unweighted point-cloud spectral geometry of the memory cloud.",
        "- `D_center`: low-pass dynamic-center trace geometry, thinned to one memory time.",
        "",
        "## Provenance",
        "",
        f"- Source dirs: `{', '.join(_rel(_resolve(path)) for path in source_dirs)}`",
        f"- Machine-readable summary: `{_rel(summary_json)}`",
        f"- Git revision while building this report: `{_git_output(['rev-parse', 'HEAD'])}`",
        f"- Git status while building this report: `{_git_status_inline()}`",
        "",
        "## Figures",
        "",
    ]
    for path in figure_paths:
        title = path.stem.replace("dimension_claim_audit_", "")
        lines.append(f"- [{title}]({_rel_from(report_path, path)})")

    lines.extend(
        [
            "",
            "## Claim Ladder",
            "",
            "| level | statement | current status |",
            "| --- | --- | --- |",
            "| Paper I | Co-moving compact memory clouds exist in the corrected scalar reference slice. | Supported by radius, drift/radius, roundness and control separation. |",
            "| Paper I teaser | In a chosen 3D embedding, the scalar reference cloud has near-3 local memory-shape geometry. | Supported for `d=3`: `D_mem ~=2.95` at `A_att=35`; still a chosen-embedding statement. |",
            "| Paper II hypothesis | A coarse/external sector may be near three-dimensional. | Plausible but unresolved: `D_spec memory` approaches 3 at high ambient `d`, while center-trace geometry remains a separate observable. |",
            "| strong dimension claim | The model selects macroscopic 3D independent of ambient dimension. | Not supported by this audit: `D_mem` rises with ambient dimension. |",
            "",
            "## Ambient-Dimension Summary",
            "",
            "| N | dim | condition | seeds | radius | drift/r | D_mem | D_p90 | D_p95 | D_spec memory | D_center cov | D_center spec | roundness |",
            "| ---: | ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in summary:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{int(item['steps']):,}`",
                    f"`{int(item['dim'])}`",
                    f"`{item['condition']}`",
                    f"`{int(item['n'])}`",
                    _fmt_iqr(item.get("dynamic_radius_median"), item.get("dynamic_radius_q1"), item.get("dynamic_radius_q3")),
                    _fmt_iqr(
                        item.get("dynamic_drift_radius_median"),
                        item.get("dynamic_drift_radius_q1"),
                        item.get("dynamic_drift_radius_q3"),
                    ),
                    _fmt_iqr(
                        item.get("memory_shape_dimension_median"),
                        item.get("memory_shape_dimension_q1"),
                        item.get("memory_shape_dimension_q3"),
                    ),
                    _fmt_iqr(item.get("memory_d90_median"), item.get("memory_d90_q1"), item.get("memory_d90_q3")),
                    _fmt_iqr(item.get("memory_d95_median"), item.get("memory_d95_q1"), item.get("memory_d95_q3")),
                    _fmt_iqr(
                        item.get("memory_spectral_dimension_median"),
                        item.get("memory_spectral_dimension_q1"),
                        item.get("memory_spectral_dimension_q3"),
                    ),
                    _fmt_iqr(
                        item.get("center_trace_covariance_dimension_median"),
                        item.get("center_trace_covariance_dimension_q1"),
                        item.get("center_trace_covariance_dimension_q3"),
                    ),
                    _fmt_iqr(
                        item.get("center_trace_spectral_dimension_median"),
                        item.get("center_trace_spectral_dimension_q1"),
                        item.get("center_trace_spectral_dimension_q3"),
                    ),
                    _fmt_iqr(item.get("memory_roundness_median"), item.get("memory_roundness_q1"), item.get("memory_roundness_q3")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Baseline/Control Separation",
            "",
            "| dim | radius gain eta0/baseline | drift/r gain eta0/baseline | D_mem delta | D_spec memory delta | roundness delta |",
            "| ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for dim in dims:
        base = by_key.get((30_000_000, dim, "baseline"), {})
        ctrl = by_key.get((30_000_000, dim, "eta_zero"), {})
        lines.append(
            f"| `{dim}` | "
            f"{_fmt(_ratio(ctrl.get('dynamic_radius_median'), base.get('dynamic_radius_median')))} | "
            f"{_fmt(_ratio(ctrl.get('dynamic_drift_radius_median'), base.get('dynamic_drift_radius_median')))} | "
            f"{_fmt(_delta(base.get('memory_shape_dimension_median'), ctrl.get('memory_shape_dimension_median')))} | "
            f"{_fmt(_delta(base.get('memory_spectral_dimension_median'), ctrl.get('memory_spectral_dimension_median')))} | "
            f"{_fmt(_delta(base.get('memory_roundness_median'), ctrl.get('memory_roundness_median')))} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Paper I can use this as a stronger teaser: the scalar reference is not",
            "  just compact, it has a clear local memory-geometry signal in the",
            "  chosen 3D slice.",
            "- The strong ambient-independent 3D claim fails in the strict `D_mem`",
            "  sense: `D_mem`, `D_p90`, and `D_p95` grow with supplied dimension.",
            "- The interesting Paper-II opening is spectral/coarse geometry:",
            "  `D_spec memory` moves toward about three while `D_mem` keeps rising.",
            "- `D_center` is an external/coarse trace observable, but a single drifting",
            "  knot still need not sample the full external interaction sector.",
            "- The next decisive test is relational: a weak second knot or external",
            "  field should see an effective response rank near three if the",
            "  external-sector interpretation is correct.",
            "",
            "## Next Checks",
            "",
            "1. Add D_spec bandwidth/kNN sensitivity before treating `D_spec ~=3` as robust.",
            "2. Run the same audit on any completed higher-N d10/d13 cases once case JSONs exist.",
            "3. Add a response-rank experiment with a second knot or weak external probe.",
            "4. Keep Paper I wording at `local memory-shape evidence in a chosen 3D embedding`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    source_dirs = [Path(path) for path in args.source_dir] if args.source_dir else DEFAULT_SOURCE_DIRS
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_dir = _resolve(args.figure_dir)

    cases = load_cases(source_dirs)
    if not cases:
        raise SystemExit("no case_*.json files found for dimension audit")
    rows = [
        case_row(
            case,
            center_trace_min_gap_memory_times=args.center_trace_min_gap_memory_times,
            center_trace_spectral_points=args.center_trace_spectral_points,
        )
        for case in cases
    ]
    summary = build_summary(rows)
    figure_paths = _plot_audit(summary, figure_dir)

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "source_dirs": [_rel(_resolve(path)) for path in source_dirs],
        "rows": rows,
        "summary": summary,
        "center_trace_min_gap_memory_times": args.center_trace_min_gap_memory_times,
        "center_trace_spectral_points": args.center_trace_spectral_points,
    }
    summary_path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")
    report_path.write_text(
        _build_report(
            rows=rows,
            summary=summary,
            source_dirs=source_dirs,
            summary_json=summary_path,
            figure_paths=figure_paths,
            report_path=report_path,
        ),
        encoding="utf-8",
    )
    print(f"wrote {report_path}")
    print(f"wrote {summary_path}")
    for path in figure_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
