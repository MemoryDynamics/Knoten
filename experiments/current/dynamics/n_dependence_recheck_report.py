"""Reconcile N-dependence diagnostics across scalar runs and snapshot pilots."""

from __future__ import annotations

import argparse
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


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an N-dependence reconciliation plot from existing reports."
    )
    parser.add_argument(
        "--scalar-summary",
        type=Path,
        default=Path("reports/long_runs/scalar_hardening/scalar_n_scaling_q3_summary_2026-07-10.json"),
    )
    parser.add_argument(
        "--long-summary",
        type=Path,
        default=Path("reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N30M_eps1em4_summary_2026-07-13.json"),
    )
    parser.add_argument(
        "--snapshot-summary",
        type=Path,
        default=Path("reports/dimensions/dspec_raw_snapshot_summary_2026-07-15.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/long_runs/scalar_hardening/n_dependence_recheck_2026-07-16.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/long_runs/scalar_hardening/n_dependence_recheck_summary_2026-07-16.json"),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/scalar_n/n_dependence_recheck_2026-07-16"),
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


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(_resolve(path).read_text(encoding="utf-8"))


def _finite(value: Any) -> float | None:
    if value is None:
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def _fmt(value: Any, digits: int = 3) -> str:
    number = _finite(value)
    if number is None:
        return "-"
    if abs(number) >= 1000.0 or (abs(number) < 0.001 and number != 0.0):
        return f"{number:.{digits}e}"
    return f"{number:.{digits}f}"


def _iqr(median: Any, q1: Any, q3: Any) -> str:
    if _finite(median) is None:
        return "-"
    return f"{_fmt(median)} [{_fmt(q1)}, {_fmt(q3)}]"


def load_scalar_rows(path: Path) -> list[dict[str, Any]]:
    payload = _read_json(path)
    rows: list[dict[str, Any]] = []
    for item in payload.get("summary", []):
        rows.append(
            {
                "family": "scalar_n_eps003",
                "a_att": _finite(item.get("a_att")),
                "steps": int(item.get("steps", 0)),
                "condition": "baseline",
                "n": int(item.get("n", 0)),
                "memory_shape_dimension_median": _finite(item.get("memory_shape_dimension_median")),
                "memory_shape_dimension_q1": _finite(item.get("memory_shape_dimension_q1")),
                "memory_shape_dimension_q3": _finite(item.get("memory_shape_dimension_q3")),
                "memory_roundness_median": _finite(item.get("memory_roundness_median")),
                "memory_roundness_q1": _finite(item.get("memory_roundness_q1")),
                "memory_roundness_q3": _finite(item.get("memory_roundness_q3")),
                "memory_radius_median": _finite(item.get("memory_radius_median")),
                "memory_radius_q1": _finite(item.get("memory_radius_q1")),
                "memory_radius_q3": _finite(item.get("memory_radius_q3")),
                "occupancy_window_dimension_median": _finite(item.get("occupancy_window_dimension_median")),
                "residence_gain_median": _finite(item.get("residence_gain_median")),
            }
        )
    return rows


def load_long_rows(path: Path) -> list[dict[str, Any]]:
    payload = _read_json(path)
    rows: list[dict[str, Any]] = []
    for item in payload.get("summary", []):
        rows.append(
            {
                "family": "long_reference_eps1e-4",
                "a_att": _finite(item.get("a_att")),
                "steps": int(item.get("steps", 0)),
                "condition": str(item.get("condition")),
                "n": int(item.get("n", 0)),
                "memory_shape_dimension_median": _finite(item.get("memory_shape_dimension_median")),
                "memory_shape_dimension_q1": _finite(item.get("memory_shape_dimension_q1")),
                "memory_shape_dimension_q3": _finite(item.get("memory_shape_dimension_q3")),
                "memory_roundness_median": _finite(item.get("memory_roundness_median")),
                "memory_roundness_q1": _finite(item.get("memory_roundness_q1")),
                "memory_roundness_q3": _finite(item.get("memory_roundness_q3")),
                "memory_radius_median": _finite(item.get("memory_radius_median")),
                "memory_radius_q1": _finite(item.get("memory_radius_q1")),
                "memory_radius_q3": _finite(item.get("memory_radius_q3")),
                "dynamic_radius_median": _finite(item.get("dynamic_rms_radius_median_median")),
                "drift_radius_fraction_median": _finite(item.get("dynamic_center_drift_radius_fraction_per_memory_time_median")),
                "best_residence_memory_times_median": _finite(item.get("best_residence_memory_times_median")),
            }
        )
    return rows


def load_snapshot_rows(path: Path) -> list[dict[str, Any]]:
    payload = _read_json(path)
    rows: list[dict[str, Any]] = []
    for item in payload.get("summary", []):
        rows.append(
            {
                "family": "raw_snapshot_pilot_eps1e-4",
                "dim": int(item.get("dim", 0)),
                "steps": int(item.get("steps", 0)),
                "condition": str(item.get("condition")),
                "n": int(item.get("n", 0)),
                "memory_shape_dimension_median": _finite(item.get("shape_effective_dimension_median")),
                "memory_shape_dimension_q1": _finite(item.get("shape_effective_dimension_q1")),
                "memory_shape_dimension_q3": _finite(item.get("shape_effective_dimension_q3")),
                "memory_roundness_median": _finite(item.get("shape_roundness_median")),
                "memory_roundness_q1": _finite(item.get("shape_roundness_q1")),
                "memory_roundness_q3": _finite(item.get("shape_roundness_q3")),
                "memory_radius_median": _finite(item.get("shape_radius_median")),
                "memory_radius_q1": _finite(item.get("shape_radius_q1")),
                "memory_radius_q3": _finite(item.get("shape_radius_q3")),
                "heat_trace_dimension_median": _finite(item.get("heat_median_median")),
                "heat_trace_dimension_q1": _finite(item.get("heat_median_q1")),
                "heat_trace_dimension_q3": _finite(item.get("heat_median_q3")),
                "heat_valid_count_median": _finite(item.get("heat_valid_count_median")),
            }
        )
    return rows


def _plot_iqr(
    ax: Any,
    rows: list[dict[str, Any]],
    *,
    metric: str,
    label: str,
    color: str,
    linestyle: str = "-",
    marker: str = "o",
) -> None:
    rows = sorted(rows, key=lambda row: int(row["steps"]))
    x = np.asarray([float(row["steps"]) for row in rows], dtype=float)
    y = np.asarray([_finite(row.get(f"{metric}_median")) or np.nan for row in rows], dtype=float)
    q1 = np.asarray([_finite(row.get(f"{metric}_q1")) or np.nan for row in rows], dtype=float)
    q3 = np.asarray([_finite(row.get(f"{metric}_q3")) or np.nan for row in rows], dtype=float)
    ax.plot(x, y, marker=marker, linestyle=linestyle, color=color, label=label)
    if np.isfinite(q1).any() and np.isfinite(q3).any():
        ax.fill_between(x, q1, q3, color=color, alpha=0.14)


def write_figure(rows: list[dict[str, Any]], figure_dir: Path) -> list[Path]:
    figure_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    scalar = [row for row in rows if row["family"] == "scalar_n_eps003"]
    long_ref = [row for row in rows if row["family"] == "long_reference_eps1e-4"]
    snapshot = [row for row in rows if row["family"] == "raw_snapshot_pilot_eps1e-4"]

    colors = {20.0: "#2563eb", 35.0: "#dc2626"}
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.5))
    panels = [
        (axes[0, 0], "memory_shape_dimension", "Memory shape dimension", False),
        (axes[0, 1], "memory_radius", "Memory radius / snapshot radius", True),
        (axes[1, 0], "memory_roundness", "Memory roundness", False),
        (axes[1, 1], "heat_trace_dimension", "Raw snapshot Heat-Trace D_spec", False),
    ]

    for ax, metric, title, log_y in panels:
        for a_att in [20.0, 35.0]:
            series = [row for row in scalar if row.get("a_att") == a_att]
            if metric != "heat_trace_dimension" and series:
                _plot_iqr(
                    ax,
                    series,
                    metric=metric,
                    label=f"A_att={a_att:g}, N-scaling eps=0.03",
                    color=colors[a_att],
                )
            ref = [
                row
                for row in long_ref
                if row.get("a_att") == a_att and row.get("condition") == "baseline"
            ]
            if metric != "heat_trace_dimension" and ref:
                _plot_iqr(
                    ax,
                    ref,
                    metric=metric,
                    label=f"A_att={a_att:g}, N30M eps=1e-4",
                    color=colors[a_att],
                    linestyle="",
                    marker="*",
                )
        if metric == "heat_trace_dimension":
            for dim, color in [(3, "#16a34a"), (10, "#7c3aed")]:
                series = [
                    row
                    for row in snapshot
                    if row.get("dim") == dim and row.get("condition") == "baseline"
                ]
                if series:
                    _plot_iqr(
                        ax,
                        series,
                        metric=metric,
                        label=f"raw snapshot d={dim}, baseline",
                        color=color,
                        linestyle="",
                        marker="D",
                    )
            ax.axhline(3.0, color="#666666", linewidth=1.0, linestyle=":")
        ax.set_xscale("log")
        if log_y:
            ax.set_yscale("log")
        ax.set_title(title)
        ax.set_xlabel("N updates")
        ax.grid(True, which="both", alpha=0.25)
        ax.legend(fontsize=7, frameon=False)

    fig.suptitle("N-dependence reconciliation: formation, reference, raw-snapshot pilot", y=1.01)
    fig.tight_layout()
    path = figure_dir / "n_dependence_recheck_overview_2026-07-16.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    outputs.append(path)
    return outputs


def build_report(
    *,
    report_path: Path,
    summary_json: Path,
    figures: list[Path],
    rows: list[dict[str, Any]],
) -> str:
    scalar = [row for row in rows if row["family"] == "scalar_n_eps003"]
    long_ref = [row for row in rows if row["family"] == "long_reference_eps1e-4"]
    snapshot = [row for row in rows if row["family"] == "raw_snapshot_pilot_eps1e-4"]
    lines = [
        "# N-Dependence Recheck",
        "",
        f"Date: {_utc_now()}.",
        "",
        "## Scope",
        "",
        "This is a reconciliation plot, not a new long run. It combines three already",
        "available evidence layers:",
        "",
        "- scalar formation scaling `N=100k..3M`, `epsilon=0.03`, `A_att in {20,35}`;",
        "- the `N=30M`, `epsilon=1e-4` scalar reference slice;",
        "- the short `N=200k` raw-memory-snapshot D_spec pilot.",
        "",
        "The parameter sets are not identical, so the figure should be read as a",
        "sanity check for qualitative N-behavior, not as a fitted scaling law.",
        "",
        "## Figures",
        "",
    ]
    for figure in figures:
        lines.append(f"- [{figure.stem}]({_rel_from(report_path, figure)})")

    lines.extend(
        [
            "",
            "## Scalar N-Scaling Summary",
            "",
            "| A_att | N | memory D | memory radius | roundness | D_win | residence gain |",
            "| ---: | ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for row in sorted(scalar, key=lambda item: (float(item["a_att"]), int(item["steps"]))):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['a_att']:g}`",
                    f"`{int(row['steps']):,}`",
                    _iqr(row.get("memory_shape_dimension_median"), row.get("memory_shape_dimension_q1"), row.get("memory_shape_dimension_q3")),
                    _iqr(row.get("memory_radius_median"), row.get("memory_radius_q1"), row.get("memory_radius_q3")),
                    _iqr(row.get("memory_roundness_median"), row.get("memory_roundness_q1"), row.get("memory_roundness_q3")),
                    _fmt(row.get("occupancy_window_dimension_median")),
                    _fmt(row.get("residence_gain_median")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## N30M Reference Summary",
            "",
            "| A_att | condition | N | memory D | memory radius | roundness | drift/r per tau_mem |",
            "| ---: | --- | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in sorted(long_ref, key=lambda item: (float(item["a_att"]), str(item["condition"]))):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['a_att']:g}`",
                    f"`{row['condition']}`",
                    f"`{int(row['steps']):,}`",
                    _iqr(row.get("memory_shape_dimension_median"), row.get("memory_shape_dimension_q1"), row.get("memory_shape_dimension_q3")),
                    _iqr(row.get("memory_radius_median"), row.get("memory_radius_q1"), row.get("memory_radius_q3")),
                    _iqr(row.get("memory_roundness_median"), row.get("memory_roundness_q1"), row.get("memory_roundness_q3")),
                    _fmt(row.get("drift_radius_fraction_median")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Raw Snapshot Pilot",
            "",
            "| dim | condition | N | shape D | heat D_spec | valid heat windows |",
            "| ---: | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in sorted(snapshot, key=lambda item: (int(item["dim"]), str(item["condition"]))):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['dim']}`",
                    f"`{row['condition']}`",
                    f"`{int(row['steps']):,}`",
                    _iqr(row.get("memory_shape_dimension_median"), row.get("memory_shape_dimension_q1"), row.get("memory_shape_dimension_q3")),
                    _iqr(row.get("heat_trace_dimension_median"), row.get("heat_trace_dimension_q1"), row.get("heat_trace_dimension_q3")),
                    _fmt(row.get("heat_valid_count_median")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Reading",
            "",
            "- Exact `3D` is not the right hard acceptance criterion. A physically",
            "  relevant sector may be flattened or effectively lower-dimensional under",
            "  angular-momentum-like constraints; the stronger criterion is stable",
            "  active dimension or response rank, contrasted against controls.",
            "- The old `N=100k..3M` scalar scaling behaves as before: compact memory",
            "  clouds form early, while residence is noisy and not monotone.",
            "- The `N=30M` reference slice is qualitatively consistent on memory shape",
            "  but uses a different epsilon scale, so it should not be used to fit the",
            "  older N-curve.",
            "- The `N=200k` raw snapshot point is a pipeline check. It is too short to",
            "  settle the D_spec question and does not reproduce a robust near-three",
            "  Heat-Trace signal.",
            "",
            "## Two-Knot Guardrail",
            "",
            "For a future response-rank test, start in a weak-probe regime rather than a",
            "free collision regime: separate memories, large initial separation,",
            "`eta_cross << eta_self`, and a small controlled displacement or field kick.",
            "The first observable should be a linear response matrix, not whether two",
            "free knots merge or become tangled.",
            "",
            f"Machine-readable summary: `{_rel(summary_json)}`.",
            f"Git revision while building: `{_git_output(['rev-parse', 'HEAD'])}`.",
            f"Git status while building: `{_git_status_inline()}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    scalar_rows = load_scalar_rows(args.scalar_summary)
    long_rows = load_long_rows(args.long_summary)
    snapshot_rows = load_snapshot_rows(args.snapshot_summary)
    rows = scalar_rows + long_rows + snapshot_rows

    figure_dir = _resolve(args.figure_dir)
    figures = write_figure(rows, figure_dir)

    summary_json = _resolve(args.summary_json)
    payload = {
        "generated_at": _utc_now(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_status_inline(),
        "source_files": {
            "scalar_summary": _rel(_resolve(args.scalar_summary)),
            "long_summary": _rel(_resolve(args.long_summary)),
            "snapshot_summary": _rel(_resolve(args.snapshot_summary)),
        },
        "figures": [_rel(path) for path in figures],
        "rows": rows,
    }
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    report_path = _resolve(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        build_report(
            report_path=report_path,
            summary_json=summary_json,
            figures=figures,
            rows=rows,
        ),
        encoding="utf-8",
    )
    print(f"wrote {_rel(report_path)}")
    print(f"wrote {_rel(summary_json)}")
    for figure in figures:
        print(f"wrote {_rel(figure)}")


if __name__ == "__main__":
    main()
