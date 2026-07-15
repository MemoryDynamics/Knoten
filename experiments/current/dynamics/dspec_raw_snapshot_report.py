"""D_spec sensitivity on persisted raw memory-cloud snapshots.

This report is the direct follow-up to ``dspec_sensitivity_report.py``.  The
older report used covariance-matched surrogates because the long-run case JSONs
did not contain raw memory-cloud coordinates.  This script consumes the new
``memory_cloud.snapshot`` payload from ``long_run_metastability.py`` and reruns
the scale audit on actual stored memory points.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
from typing import Any, Iterable

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from emergenz_knoten import (
    covariance_dimension,
    heat_trace_spectral_dimension,
    shape_statistics,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
BANDWIDTH_FACTORS = [0.5, 1.0, 2.0]
NEIGHBOR_COUNTS = [8, 16, 32, 64]


@dataclass(frozen=True)
class SnapshotRecord:
    dim: int
    condition: str
    seed: int
    steps: int
    path: Path
    points: np.ndarray
    weights: np.ndarray
    stored_dspec: float | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit D_spec sensitivity on persisted raw memory-cloud snapshots."
    )
    parser.add_argument(
        "--source-dir",
        action="append",
        type=Path,
        help="Directory searched recursively for case_*.json files. Defaults to data/processed/long_run_metastability.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/dimensions/dspec_raw_snapshot_2026-07-15.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/dimensions/dspec_raw_snapshot_summary_2026-07-15.json"),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/dimensions/dspec_raw_snapshot_2026-07-15"),
    )
    parser.add_argument(
        "--max-points",
        type=int,
        default=500,
        help=(
            "uniformly downsample each stored snapshot to at most this many "
            "points for spectral diagnostics; 0 keeps all points"
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


def _rel_from(source_file: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source_file.resolve().parent)).as_posix()


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _git_output(args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def _git_status_inline() -> str:
    status = _git_output(["status", "--short"])
    return status.replace("\n", "; ") if status else "clean"


def _finite_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if np.isfinite(out) else None


def _quantiles(values: Iterable[float | None]) -> dict[str, float | None]:
    arr = np.asarray([float(v) for v in values if v is not None and np.isfinite(v)], dtype=float)
    if arr.size == 0:
        return {"median": None, "q1": None, "q3": None}
    return {
        "median": float(np.median(arr)),
        "q1": float(np.quantile(arr, 0.25)),
        "q3": float(np.quantile(arr, 0.75)),
    }


def _weighted_covariance_dimension(points: np.ndarray, weights: np.ndarray) -> float | None:
    w = np.asarray(weights, dtype=float)
    pts = np.asarray(points, dtype=float)
    if w.ndim != 1 or pts.ndim != 2 or len(w) != len(pts):
        return None
    if np.any(~np.isfinite(w)) or np.any(w < 0.0) or float(w.sum()) <= 0.0:
        return None
    w = w / float(w.sum())
    center = np.sum(pts * w[:, None], axis=0)
    centered = pts - center
    cov = centered.T @ (centered * w[:, None])
    eig = np.linalg.eigvalsh(cov)
    eig = eig[eig > max(float(eig.max(initial=0.0)) * 1e-12, 1e-12)]
    if eig.size == 0:
        return None
    s1 = float(eig.sum())
    s2 = float(np.dot(eig, eig))
    if s2 <= 0.0:
        return None
    out = s1 * s1 / s2
    return out if np.isfinite(out) else None


def _case_files(source_dirs: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for source_dir in source_dirs:
        root = _resolve(source_dir)
        if root.is_file():
            files.append(root)
        elif root.exists():
            files.extend(root.rglob("case_*.json"))
    return sorted(set(files))


def _load_snapshot(path: Path) -> SnapshotRecord | None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    diagnostics = payload.get("diagnostics", {})
    memory_cloud = diagnostics.get("memory_cloud", {})
    snapshot = memory_cloud.get("snapshot")
    if not isinstance(snapshot, dict):
        return None

    points = np.asarray(snapshot.get("points"), dtype=float)
    weights = np.asarray(snapshot.get("weights"), dtype=float)
    if points.ndim != 2 or len(points) < 100:
        return None
    if weights.ndim != 1 or len(weights) != len(points):
        weights = np.ones(len(points), dtype=float)
    if np.any(~np.isfinite(points)) or np.any(~np.isfinite(weights)):
        return None
    if np.any(weights < 0.0) or float(weights.sum()) <= 0.0:
        weights = np.ones(len(points), dtype=float)

    config = payload.get("config", {})
    spectral = memory_cloud.get("spectral", {})
    return SnapshotRecord(
        dim=int(config.get("dim", points.shape[1])),
        condition=str(payload.get("condition", "unknown")),
        seed=int(payload.get("seed", -1)),
        steps=int(config.get("steps", payload.get("steps", 0))),
        path=path,
        points=points,
        weights=weights,
        stored_dspec=_finite_float(spectral.get("dimension")),
    )


def load_snapshots(source_dirs: Iterable[Path]) -> list[SnapshotRecord]:
    records = []
    for path in _case_files(source_dirs):
        record = _load_snapshot(path)
        if record is not None:
            records.append(record)
    return records


def _limited_points(
    points: np.ndarray,
    weights: np.ndarray,
    *,
    max_points: int,
) -> tuple[np.ndarray, np.ndarray, int]:
    source_points = int(len(points))
    if max_points <= 0 or len(points) <= max_points:
        return points, weights, source_points
    indices = np.linspace(0, len(points) - 1, int(max_points), dtype=int)
    return points[indices], weights[indices], source_points


def measure_snapshot(record: SnapshotRecord, *, max_points: int = 0) -> dict[str, Any]:
    points, weights, source_points = _limited_points(
        record.points,
        record.weights,
        max_points=max_points,
    )
    shape = shape_statistics(points, weights=weights)
    row: dict[str, Any] = {
        "path": _rel(record.path),
        "dim": record.dim,
        "condition": record.condition,
        "seed": record.seed,
        "steps": record.steps,
        "n_points": int(len(points)),
        "source_n_points": source_points,
        "max_points": int(max_points),
        "stored_dspec": record.stored_dspec,
        "covariance_dimension": _finite_float(covariance_dimension(points)),
        "weighted_covariance_dimension": _weighted_covariance_dimension(points, weights),
        "shape_effective_dimension": _finite_float(shape.get("effective_dimension")),
        "shape_radius": _finite_float(shape.get("mean_radius")),
        "shape_roundness": _finite_float(shape.get("axis_ratio_intrinsic_min_max")),
    }

    heat_values: list[float] = []
    valid_count = 0
    for factor in BANDWIDTH_FACTORS:
        for neighbor_count in NEIGHBOR_COUNTS:
            if neighbor_count >= len(points):
                continue
            result = heat_trace_spectral_dimension(
                points,
                bandwidth_factor=factor,
                neighbor_count=neighbor_count,
                eigen_count=min(80, max(8, len(points) - 2)),
            )
            key = f"heat_f{factor:g}_k{neighbor_count}"
            row[key] = _finite_float(result.dimension)
            row[f"{key}_valid"] = bool(result.valid_scaling)
            row[f"{key}_log_width"] = _finite_float(result.log_width)
            if result.valid_scaling and np.isfinite(result.dimension):
                valid_count += 1
                heat_values.append(float(result.dimension))

    if heat_values:
        arr = np.asarray(heat_values, dtype=float)
        row["heat_valid_count"] = valid_count
        row["heat_median"] = float(np.median(arr))
        row["heat_min"] = float(arr.min())
        row["heat_max"] = float(arr.max())
        row["heat_range"] = float(arr.max() - arr.min())
        row["heat_near3_fraction"] = float(np.mean((arr >= 2.5) & (arr <= 3.5)))
    else:
        row["heat_valid_count"] = 0
        row["heat_median"] = None
        row["heat_min"] = None
        row["heat_max"] = None
        row["heat_range"] = None
        row["heat_near3_fraction"] = None
    return row


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[int, int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(int(row["steps"]), int(row["dim"]), str(row["condition"]))].append(row)

    out: list[dict[str, Any]] = []
    metrics = [
        "n_points",
        "stored_dspec",
        "covariance_dimension",
        "weighted_covariance_dimension",
        "shape_effective_dimension",
        "shape_radius",
        "shape_roundness",
        "heat_median",
        "heat_min",
        "heat_max",
        "heat_range",
        "heat_near3_fraction",
        "heat_valid_count",
    ]
    for (steps, dim, condition), group in sorted(groups.items()):
        item: dict[str, Any] = {
            "steps": steps,
            "dim": dim,
            "condition": condition,
            "n": len(group),
            "seeds": sorted(int(row["seed"]) for row in group),
        }
        for metric in metrics:
            q = _quantiles(row.get(metric) for row in group)
            item[f"{metric}_median"] = q["median"]
            item[f"{metric}_q1"] = q["q1"]
            item[f"{metric}_q3"] = q["q3"]
        out.append(item)
    return out


def _fmt(value: Any, digits: int = 3) -> str:
    val = _finite_float(value)
    if val is None:
        return "-"
    if abs(val) >= 1000.0 or (abs(val) < 0.001 and val != 0.0):
        return f"{val:.{digits}e}"
    return f"{val:.{digits}f}"


def _fmt_iqr(median: Any, q1: Any, q3: Any) -> str:
    if _finite_float(median) is None:
        return "-"
    return f"{_fmt(median)} [{_fmt(q1)}, {_fmt(q3)}]"


def _plot_summary(summary: list[dict[str, Any]], figure_dir: Path) -> list[Path]:
    figure_dir.mkdir(parents=True, exist_ok=True)
    if not summary:
        return []

    figures: list[Path] = []
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in summary:
        by_condition[str(item["condition"])].append(item)

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    for condition, rows in sorted(by_condition.items()):
        rows = sorted(rows, key=lambda row: (int(row["dim"]), int(row["steps"])))
        xs = [int(row["dim"]) for row in rows]
        ax.plot(xs, [row.get("heat_median_median", math.nan) for row in rows], marker="o", label=f"{condition} heat")
        ax.plot(xs, [row.get("weighted_covariance_dimension_median", math.nan) for row in rows], marker="s", linestyle="--", label=f"{condition} weighted D_cov")
    ax.axhline(3.0, color="#666666", linewidth=1.0, linestyle=":")
    ax.set_xlabel("ambient dimension")
    ax.set_ylabel("dimension diagnostic")
    ax.set_title("Raw memory snapshot dimension diagnostics")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    path = figure_dir / "raw_snapshot_dspec_by_dimension.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    figures.append(path)

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    width = 0.35
    rows = sorted(summary, key=lambda row: (int(row["dim"]), str(row["condition"])))
    labels = [f"d{row['dim']} {row['condition']}" for row in rows]
    x = np.arange(len(rows), dtype=float)
    ax.bar(x - width / 2, [row.get("heat_valid_count_median") or 0.0 for row in rows], width, label="valid heat windows")
    ax.bar(x + width / 2, [row.get("heat_range_median") or 0.0 for row in rows], width, label="heat range")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_title("Raw snapshot D_spec validity and scale spread")
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    path = figure_dir / "raw_snapshot_dspec_validity.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    figures.append(path)
    return figures


def _build_report(
    *,
    report_path: Path,
    summary_json: Path,
    source_dirs: list[Path],
    rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    figure_paths: list[Path],
) -> str:
    lines = [
        "# Raw Memory Snapshot D_spec Audit",
        "",
        f"Date: {_utc_now()}.",
        "",
        "## Scope",
        "",
        "This report reruns spectral-geometry diagnostics on persisted raw",
        "`memory_cloud.snapshot` coordinates from long-run case JSONs. It is the",
        "direct replacement for covariance-surrogate checks when snapshots are available.",
        "The first 2026-07-15 run is a short `N=200k` pipeline pilot, not a",
        "long-run dimension-selection result.",
        "",
        "## Provenance",
        "",
        f"- Source dirs: `{', '.join(_rel(_resolve(path)) for path in source_dirs)}`",
        f"- Machine-readable summary: `{_rel(summary_json)}`",
        f"- Git revision while building this report: `{_git_output(['rev-parse', 'HEAD'])}`",
        f"- Git status while building this report: `{_git_status_inline()}`",
        f"- Snapshot cases found: `{len(rows)}`",
        "",
    ]
    if figure_paths:
        lines.extend(["## Figures", ""])
        for path in figure_paths:
            lines.append(f"- [{path.stem}]({_rel_from(report_path, path)})")
        lines.append("")

    if not rows:
        lines.extend(
            [
                "## Result",
                "",
                "No case JSON with `diagnostics.memory_cloud.snapshot` was found.",
                "Run `long_run_metastability.py` with `--memory-snapshot-points`",
                "and then rerun this report.",
                "",
                "## Decision",
                "",
                "`D_spec` cannot yet be reclassified from hypothesis lead to evidence.",
            ]
        )
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            "## Main Summary",
            "",
            "| N | dim | condition | seeds | points | stored D_spec | weighted D_cov | shape D | heat median | heat range | near-3 heat fraction | valid heat windows |",
            "| ---: | ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
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
                    _fmt_iqr(item.get("n_points_median"), item.get("n_points_q1"), item.get("n_points_q3")),
                    _fmt_iqr(item.get("stored_dspec_median"), item.get("stored_dspec_q1"), item.get("stored_dspec_q3")),
                    _fmt_iqr(item.get("weighted_covariance_dimension_median"), item.get("weighted_covariance_dimension_q1"), item.get("weighted_covariance_dimension_q3")),
                    _fmt_iqr(item.get("shape_effective_dimension_median"), item.get("shape_effective_dimension_q1"), item.get("shape_effective_dimension_q3")),
                    _fmt_iqr(item.get("heat_median_median"), item.get("heat_median_q1"), item.get("heat_median_q3")),
                    _fmt_iqr(item.get("heat_range_median"), item.get("heat_range_q1"), item.get("heat_range_q3")),
                    _fmt_iqr(item.get("heat_near3_fraction_median"), item.get("heat_near3_fraction_q1"), item.get("heat_near3_fraction_q3")),
                    _fmt_iqr(item.get("heat_valid_count_median"), item.get("heat_valid_count_q1"), item.get("heat_valid_count_q3")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `weighted D_cov` and `shape D` use the stored memory weights; `heat median`",
            "  is still unweighted point-cloud spectral geometry on the raw snapshot.",
            "- `heat range` is the spread across bandwidth factors and neighbor counts;",
            "  large values mean the diagnostic is not yet scale-robust.",
            "- A near-three heat median is only meaningful when valid heat windows are",
            "  common and the range is small across seeds and conditions.",
            "- In the first `N=200k` pilot, raw Heat-Trace `D_spec` does not reproduce",
            "  a robust near-three signal; the `d=10` baseline has no accepted",
            "  scaling window under the conservative estimator.",
            "",
            "## Decision",
            "",
            "Treat the raw-snapshot path as validated, but treat the short pilot as",
            "non-evidential for dimension selection. The next gate is a longer",
            "raw-snapshot retest on the established long-run slice. If raw snapshot",
            "`D_spec` remains scale-sensitive there, Paper II should prioritize",
            "relational response rank rather than an isolated geometry claim.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    source_dirs = args.source_dir or [Path("data/processed/long_run_metastability")]
    report_path = _resolve(args.report)
    summary_json = _resolve(args.summary_json)
    figure_dir = _resolve(args.figure_dir)

    records = load_snapshots(source_dirs)
    rows = [measure_snapshot(record, max_points=args.max_points) for record in records]
    summary = summarize(rows)
    figure_paths = _plot_summary(summary, figure_dir)

    payload = {
        "generated_at": _utc_now(),
        "source_dirs": [_rel(_resolve(path)) for path in source_dirs],
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_status_inline(),
        "bandwidth_factors": BANDWIDTH_FACTORS,
        "neighbor_counts": NEIGHBOR_COUNTS,
        "max_points": args.max_points,
        "cases": rows,
        "summary": summary,
    }
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        _build_report(
            report_path=report_path,
            summary_json=summary_json,
            source_dirs=source_dirs,
            rows=rows,
            summary=summary,
            figure_paths=figure_paths,
        ),
        encoding="utf-8",
    )
    print(f"wrote {_rel(report_path)}")
    print(f"wrote {_rel(summary_json)}")
    for path in figure_paths:
        print(f"wrote {_rel(path)}")


if __name__ == "__main__":
    main()
