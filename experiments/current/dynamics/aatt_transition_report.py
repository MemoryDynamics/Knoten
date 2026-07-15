from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import statistics
import subprocess
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


@dataclass(frozen=True)
class CaseRow:
    dim: int
    a_att: float
    seed: int
    metrics: dict[str, float]


METRICS = {
    "covariance_dimension": "D_cov",
    "occupancy_window_dimension": "D_occ_window",
    "memory_shape_dimension": "D_mem",
    "memory_spectral_dimension": "D_spec_mem",
    "memory_axis_ratio_min_max": "roundness",
    "dynamic_center_rms_radius_median": "radius",
    "dynamic_center_drift_radius_fraction_per_memory_time_median": "drift/r",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate d=3/d=10 A_att transition summaries and plot KPI curves."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path("data/processed/long_run_metastability"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/long_runs/scalar_hardening/aatt_transition_d3_d10_2026-07-15.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/long_runs/scalar_hardening/aatt_transition_d3_d10_summary_2026-07-15.json"),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/scalar_hardening/aatt_transition_2026-07-15"),
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


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _finite(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if number == number and abs(number) != float("inf") else None


def _mean(values: Iterable[float]) -> float:
    data = list(values)
    return statistics.fmean(data) if data else float("nan")


def _sd(values: Iterable[float]) -> float:
    data = list(values)
    return statistics.stdev(data) if len(data) > 1 else 0.0


def _fmt(value: float, digits: int = 3) -> str:
    if value != value:
        return "`n/a`"
    if value == 0.0:
        text = "0"
    elif abs(value) < 1e-3 or abs(value) >= 1e4:
        text = f"{value:.{digits}e}"
    else:
        text = f"{value:.{digits}f}"
    return f"`{text}`"


def _load_summary(path: Path) -> tuple[dict[str, Any], list[CaseRow]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    config = payload["base_config"]
    dim = int(config["dim"])
    a_att = float(config["amplitude_att"])
    rows: list[CaseRow] = []
    for case in payload["case_summaries"]:
        if case["condition"] != "baseline":
            continue
        metrics: dict[str, float] = {}
        for key in METRICS:
            value = _finite(case.get(key))
            if value is not None:
                metrics[key] = value
        rows.append(CaseRow(dim=dim, a_att=a_att, seed=int(case["seed"]), metrics=metrics))
    return payload, rows


def load_rows(source_dir: Path) -> tuple[list[CaseRow], list[str]]:
    patterns = [
        "Aatt_sweep_d10_N10M_Aatt_*_seed1-5_eps1em4_2026-07-14",
        "Aatt_transition_d10_N10M_Aatt_*_seed1-5_eps1em4_2026-07-15",
        "Aatt_transition_d3_N10M_Aatt_*_seed1-5_eps1em4_2026-07-15",
    ]
    rows: list[CaseRow] = []
    sources: list[str] = []
    for pattern in patterns:
        for directory in sorted(source_dir.glob(pattern)):
            summary_path = directory / "summary.json"
            if not summary_path.exists():
                continue
            _, loaded = _load_summary(summary_path)
            rows.extend(loaded)
            sources.append(_rel(directory))
    return rows, sources


def summarize(rows: list[CaseRow]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, float], list[CaseRow]] = {}
    for row in rows:
        grouped.setdefault((row.dim, row.a_att), []).append(row)

    out: list[dict[str, Any]] = []
    for (dim, a_att), group in sorted(grouped.items()):
        record: dict[str, Any] = {"dim": dim, "A_att": a_att, "n": len(group)}
        for key in METRICS:
            values = [row.metrics[key] for row in group if key in row.metrics]
            record[f"{key}_mean"] = _mean(values)
            record[f"{key}_sd"] = _sd(values)
        out.append(record)
    return out


def _plot_metric(summary: list[dict[str, Any]], key: str, label: str, figure_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for dim, color in [(3, "#1f77b4"), (10, "#d62728")]:
        points = [row for row in summary if row["dim"] == dim and row.get(f"{key}_mean") == row.get(f"{key}_mean")]
        points.sort(key=lambda item: item["A_att"])
        if not points:
            continue
        x = [row["A_att"] for row in points]
        y = [row[f"{key}_mean"] for row in points]
        yerr = [row[f"{key}_sd"] for row in points]
        ax.errorbar(x, y, yerr=yerr, marker="o", linewidth=1.8, capsize=3, label=f"d={dim}", color=color)
    ax.set_xlabel("A_att")
    ax.set_ylabel(label)
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    path = figure_dir / f"aatt_transition_{key}.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def write_report(
    *,
    report_path: Path,
    summary_json: Path,
    figure_paths: list[Path],
    summary: list[dict[str, Any]],
    sources: list[str],
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_json.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "sources": sources,
        "rows": summary,
    }
    summary_json.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")

    lines: list[str] = [
        "# A_att Transition: d=3 vs d=10",
        "",
        f"Date: {payload['generated_utc']}.",
        "",
        "## Scope",
        "",
        "This report compares matched `N=10M`, seeds `1..5`, q=3 scalar",
        "finite-memory runs across `d=3` and `d=10`. The goal is to separate",
        "sample/outer geometry diagnostics from internal memory-shape diagnostics.",
        "",
        "It also closes the report-level reference gap for the `beta=0` control:",
        "`beta=0` is represented in the current code by `M0=0` / condition",
        "`m0_zero`; see `reports/long_runs/scalar_hardening/d10_memory_controls_2026-07-14.md`.",
        "",
        "## Figures",
        "",
    ]
    for path in figure_paths:
        title = path.stem.replace("aatt_transition_", "")
        lines.append(f"- [{title}]({_rel_from(report_path, path)})")
    lines.extend(
        [
            "",
            "## Aggregated Metrics",
            "",
            "| dim | A_att | seeds | D_cov | D_occ win | D_mem | D_spec mem | roundness | radius | drift/r |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary:
        lines.append(
            "| "
            f"{int(row['dim'])} | {_fmt(row['A_att'])} | {int(row['n'])} | "
            f"{_fmt(row['covariance_dimension_mean'])} | "
            f"{_fmt(row['occupancy_window_dimension_mean'])} | "
            f"{_fmt(row['memory_shape_dimension_mean'])} | "
            f"{_fmt(row['memory_spectral_dimension_mean'])} | "
            f"{_fmt(row['memory_axis_ratio_min_max_mean'])} | "
            f"{_fmt(row['dynamic_center_rms_radius_median_mean'])} | "
            f"{_fmt(row['dynamic_center_drift_radius_fraction_per_memory_time_median_mean'])} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `D_cov` and `D_occ_window` are sample/trajectory diagnostics. They",
            "  describe the visible point cloud, not the full memory state.",
            "- `D_mem` is a covariance participation-ratio dimension of the weighted",
            "  memory cloud. It is an internal state-space shape diagnostic.",
            "- `D_spec_mem` is a point-cloud diffusion/spectral-geometry diagnostic,",
            "  not an FFT window and not a transfer-operator spectrum.",
            "- In d10, the compact regime has `D_cov` near 2.5 while `D_mem` keeps",
            "  increasing from the transition region to `A_att=35`. This supports",
            "  an inside/outside split rather than a single dimension number.",
            "- In d3, `D_mem` approaches the embedding limit while `D_cov` remains",
            "  below 2 for the single-knot trajectory. A single knot does not",
            "  necessarily sample all external directions isotropically.",
            "",
            "## Missing Checks",
            "",
            "- Add center-trace versions of `D_cov`, `D_occ`, and `D_spec` for a",
            "  cleaner coarse-grained external observable.",
            "- Add cumulative-variance memory dimensions such as `D_p90`/`D_p95`",
            "  to distinguish real internal dimensionality from small-eigenvalue tails.",
            "- Add D_spec bandwidth or kNN-scale sensitivity.",
            "- Add response-based tests with a second knot or weak external field;",
            "  external dimension should ultimately be relational, not inferred",
            "  from a single raw trajectory alone.",
            "- Re-express A_att through a dimensionless stiffness/Hessian scale",
            "  before making cross-dimension universality claims.",
            "",
            "## Sources",
            "",
        ]
    )
    lines.extend(f"- `{source}`" for source in sources)
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    source_dir = _resolve(args.source_dir)
    report_path = _resolve(args.report)
    summary_json = _resolve(args.summary_json)
    figure_dir = _resolve(args.figure_dir)
    figure_dir.mkdir(parents=True, exist_ok=True)

    rows, sources = load_rows(source_dir)
    if not rows:
        raise SystemExit("no matching A_att transition summaries found")
    summary = summarize(rows)
    figure_paths = [
        _plot_metric(summary, key, label, figure_dir)
        for key, label in METRICS.items()
    ]
    write_report(
        report_path=report_path,
        summary_json=summary_json,
        figure_paths=figure_paths,
        summary=summary,
        sources=sources,
    )
    print(f"wrote {report_path}")
    print(f"wrote {summary_json}")
    for path in figure_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
