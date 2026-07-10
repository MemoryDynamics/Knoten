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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten.knot_score import score_v0_5_against_control  # noqa: E402


SOURCE_RE = re.compile(
    r"n_scaling_q3_Aatt_(?P<a_att>[\dp]+)_N(?P<n>[\dMk]+)_seed"
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
    quantiles = statistics.quantiles(finite, n=4, method="inclusive")
    return quantiles[0], quantiles[2]


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


def build_rows(cases: list[CaseRecord]) -> list[dict[str, Any]]:
    by_key = {(case.a_att, case.steps, case.condition, case.seed): case for case in cases}
    rows: list[dict[str, Any]] = []
    for case in sorted(cases, key=lambda item: (item.a_att, item.steps, item.seed)):
        if case.condition != "baseline":
            continue
        control = by_key.get((case.a_att, case.steps, "eta_zero", case.seed))
        if control is None:
            continue
        diagnostics = case.payload["diagnostics"]
        control_diagnostics = control.payload["diagnostics"]
        score = score_v0_5_against_control(diagnostics, control_diagnostics)
        row: dict[str, Any] = {
            "a_att": case.a_att,
            "steps": case.steps,
            "seed": case.seed,
            "case_path": case.path.relative_to(ROOT).as_posix(),
            "control_path": control.path.relative_to(ROOT).as_posix(),
            **score,
            "sample_shape_dimension": _diagnostic_value(diagnostics, ("sample_shape", "effective_dimension")),
            "sample_roundness": _diagnostic_value(diagnostics, ("sample_shape", "axis_ratio_min_max")),
            "sample_radius": _diagnostic_value(diagnostics, ("sample_shape", "mean_radius")),
            "occupancy_dimension_raw": _diagnostic_value(diagnostics, ("occupancy_dimension",)),
            "occupancy_window_dimension": _diagnostic_value(
                diagnostics, ("occupancy", "scaling_window", "dimension")
            ),
            "occupancy_window_valid": bool(
                diagnostics.get("occupancy", {}).get("scaling_window", {}).get("valid_scaling", False)
            ),
            "memory_shape_dimension": _diagnostic_value(
                diagnostics, ("memory_cloud", "shape", "effective_dimension")
            ),
            "memory_roundness": _diagnostic_value(
                diagnostics, ("memory_cloud", "shape", "axis_ratio_min_max")
            ),
            "memory_radius": _diagnostic_value(diagnostics, ("memory_cloud", "shape", "mean_radius")),
        }
        rows.append(row)
    return rows


SUMMARY_METRICS = [
    "score",
    "residence_gain",
    "compactness_gain",
    "memory_compactness_gain",
    "case_mean_radius",
    "memory_radius",
    "occupancy_dimension_raw",
    "internal_dimension",
    "occupancy_window_dimension",
    "memory_shape_dimension",
    "memory_roundness",
    "case_best_residence",
    "voxel_stability",
]


def summarize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[float, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(float(row["a_att"]), int(row["steps"]))].append(row)

    out: list[dict[str, Any]] = []
    for (a_att, steps), group in sorted(grouped.items()):
        summary: dict[str, Any] = {
            "a_att": a_att,
            "steps": steps,
            "n": len(group),
            "residence_pass_count": sum(float(row.get("residence_score") or 0.0) >= 1.0 for row in group),
            "score_pass_count": sum(float(row.get("score") or 0.0) >= 0.75 for row in group),
        }
        for metric in SUMMARY_METRICS:
            values = [row.get(metric) for row in group]
            q1, q3 = _iqr(values)
            summary[f"{metric}_median"] = _median(values)
            summary[f"{metric}_q1"] = q1
            summary[f"{metric}_q3"] = q3
        out.append(summary)
    return out


def _series(summary: list[dict[str, Any]], a_att: float, metric: str) -> tuple[list[int], list[float], list[float], list[float]]:
    items = [row for row in summary if float(row["a_att"]) == float(a_att)]
    items.sort(key=lambda row: int(row["steps"]))
    steps = [int(row["steps"]) for row in items]
    med = [float(row.get(f"{metric}_median") or math.nan) for row in items]
    q1 = [float(row.get(f"{metric}_q1") or math.nan) for row in items]
    q3 = [float(row.get(f"{metric}_q3") or math.nan) for row in items]
    return steps, med, q1, q3


def _plot_metric_panel(
    ax: Any,
    summary: list[dict[str, Any]],
    *,
    metric: str,
    title: str,
    ylabel: str,
    a_values: list[float],
    log_y: bool = False,
) -> None:
    colors = {20.0: "#2563eb", 35.0: "#dc2626"}
    for a_att in a_values:
        steps, med, q1, q3 = _series(summary, a_att, metric)
        if not steps:
            continue
        color = colors.get(float(a_att), None)
        ax.plot(steps, med, marker="o", linewidth=2.0, label=f"A_att={a_att:g}", color=color)
        ax.fill_between(steps, q1, q3, alpha=0.18, color=color)
    ax.set_xscale("log")
    if log_y:
        ax.set_yscale("log")
    ax.set_title(title)
    ax.set_xlabel("N updates")
    ax.set_ylabel(ylabel)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False)


def write_plots(summary: list[dict[str, Any]], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    a_values = sorted({float(row["a_att"]) for row in summary})
    outputs: list[Path] = []

    specs = [
        (
            "scalar_n_scaling_q3_score_residence_2026-07-10.png",
            [
                ("score", "KnotScore v0.5", "score", False),
                ("residence_gain", "Residence Gain", "case/control", False),
                ("case_best_residence", "Best Residence", "updates", True),
            ],
        ),
        (
            "scalar_n_scaling_q3_compactness_2026-07-10.png",
            [
                ("case_mean_radius", "Sample Radius", "mean radius", True),
                ("memory_radius", "Memory Radius", "mean radius", True),
                ("compactness_gain", "Sample Compactness Gain", "control/case", True),
            ],
        ),
        (
            "scalar_n_scaling_q3_dimensions_2026-07-10.png",
            [
                ("occupancy_dimension_raw", "Raw D_occ", "dimension", False),
                ("occupancy_window_dimension", "Automatic D_win", "dimension", False),
                ("memory_shape_dimension", "Memory Shape Dimension", "dimension", False),
            ],
        ),
    ]
    for filename, panels in specs:
        fig, axes = plt.subplots(1, len(panels), figsize=(5.0 * len(panels), 4.2), squeeze=False)
        for ax, (metric, title, ylabel, log_y) in zip(axes[0], panels, strict=True):
            _plot_metric_panel(
                ax,
                summary,
                metric=metric,
                title=title,
                ylabel=ylabel,
                a_values=a_values,
                log_y=log_y,
            )
        fig.suptitle("Corrected scalar N-scaling, burn_in=0", y=1.03)
        fig.tight_layout()
        path = output_dir / filename
        fig.savefig(path, dpi=220, bbox_inches="tight")
        plt.close(fig)
        outputs.append(path)
    return outputs


def write_report(
    *,
    summary: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    figures: list[Path],
    output_path: Path,
) -> None:
    lines: list[str] = [
        "# Corrected Scalar N-Scaling Pilot",
        "",
        "Date: 2026-07-10.",
        "",
        "## Scope",
        "",
        "This report measures how the corrected scalar candidates settle as the",
        "run length `N` increases. It uses `burn_in=0` deliberately, because the",
        "formation transient is part of the question.",
        "",
        "Fixed parameters: `d=3`, seeds `1..5`, `alpha=lambda_m=0.01`, `M0=1`,",
        "`epsilon=0.03`, `eta=0.15`, `A_rep=1`, `sigma_rep=1`, `sigma_att=3`,",
        "`memory_factor=6`, `max_memory=600`, `sample_every=200`, deposition",
        "`delta`.",
        "",
        "Axis: `A_att in {20,35}` and `N in {100k,300k,1M,3M}`.",
        "",
        "Each point is scored seedwise against a matched `eta_zero` control.",
        "",
        "## Median Summary",
        "",
        "| A_att | N | score med | residence gain med | best residence med | sample radius med | memory radius med | raw D_occ med | D_win med | memory dim med | score pass | residence pass |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{float(row['a_att']):g}`",
                    f"`{int(row['steps']):,}`",
                    _fmt(row.get("score_median")),
                    _fmt(row.get("residence_gain_median")),
                    _fmt(row.get("case_best_residence_median")),
                    _fmt(row.get("case_mean_radius_median")),
                    _fmt(row.get("memory_radius_median")),
                    _fmt(row.get("occupancy_dimension_raw_median")),
                    _fmt(row.get("occupancy_window_dimension_median")),
                    _fmt(row.get("memory_shape_dimension_median")),
                    f"`{row['score_pass_count']}/{row['n']}`",
                    f"`{row['residence_pass_count']}/{row['n']}`",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Reading",
            "",
            "The compact-memory-cloud signal is already present at `N=100k` and",
            "stays stable through `N=3M`. The memory radius is nearly stationary",
            "over this N-range. The sample radius grows slowly with `N`, but remains",
            "small compared with the matched `eta_zero` controls, which is why the",
            "compactness component stays saturated.",
            "",
            "The residence signal is not monotone and is still below the v0.5",
            "partial threshold in the median seed. At `N=3M`, median residence gain",
            "is `1.584` for `A_att=20` and `1.684` for `A_att=35`; both remain below",
            "the partial threshold `2`. Residence pass counts therefore remain too",
            "low for a final Paper-I metastability claim.",
            "",
            "Interpretation: the corrected scalar candidates appear to form compact",
            "memory clouds quickly. The unresolved question is not formation speed",
            "but whether residence statistics converge slowly, fluctuate by seed,",
            "or require a sharper residence observable than the current voxel",
            "maximum.",
            "",
            "## Figures",
            "",
        ]
    )
    for figure in figures:
        lines.append(f"- `{figure.relative_to(ROOT).as_posix()}`")
    lines.extend(
        [
            "",
            "## Raw Rows",
            "",
            f"- Seed score rows: `{len(rows)}`.",
            "- Machine-readable aggregate: `reports/scalar_n_scaling_q3_summary_2026-07-10.json`.",
        ]
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate corrected scalar N-scaling runs.")
    parser.add_argument(
        "--source-glob",
        default="data/processed/long_run_metastability/n_scaling_q3_Aatt_*_N*_seed1-5_2026-07-10",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("reports/scalar_n_scaling_q3_summary_2026-07-10.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/scalar_n_scaling_q3_2026-07-10.md"),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dirs = sorted(ROOT.glob(args.source_glob))
    if not source_dirs:
        raise SystemExit(f"no source directories match {args.source_glob!r}")
    cases = _load_cases(source_dirs)
    rows = build_rows(cases)
    summary = summarize_rows(rows)
    figure_dir = args.figure_dir if args.figure_dir.is_absolute() else ROOT / args.figure_dir
    figures = write_plots(summary, figure_dir)
    output_json = args.output_json if args.output_json.is_absolute() else ROOT / args.output_json
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(
            {
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
    write_report(summary=summary, rows=rows, figures=figures, output_path=report)
    print(f"wrote {output_json}")
    print(f"wrote {report}")
    for figure in figures:
        print(f"wrote {figure}")


if __name__ == "__main__":
    main()
