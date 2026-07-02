from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
import statistics
import subprocess
import sys
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten.knot_score import score_against_control  # noqa: E402


DEFAULT_SOURCE_DIRS = [
    Path("data/processed/long_run_metastability/2026-06-29_initial"),
    Path("data/processed/long_run_metastability/2026-06-30_baseline_seeds"),
    Path("data/processed/long_run_metastability/2026-06-30_controls"),
    Path("data/processed/long_run_metastability/2026-06-30_eta_zero_seeds"),
    Path("data/processed/long_run_metastability/2026-06-30_single_scale_seeds"),
]


@dataclass(frozen=True)
class CaseRecord:
    condition: str
    seed: int
    path: Path
    payload: dict[str, Any]


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


def _parse_path_list(values: Iterable[str]) -> list[Path]:
    out: list[Path] = []
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if item:
                out.append(Path(item))
    return out


def _case_sort_key(case: CaseRecord) -> tuple[int, int, str]:
    steps = int(case.payload.get("config", {}).get("steps", 0))
    return (case.seed, steps, str(case.path))


def load_cases(source_dirs: Iterable[Path]) -> dict[tuple[str, int], CaseRecord]:
    by_key: dict[tuple[str, int], CaseRecord] = {}
    for source_dir in source_dirs:
        directory = source_dir if source_dir.is_absolute() else ROOT / source_dir
        if not directory.exists():
            continue
        for path in sorted(directory.glob("case_*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            condition = str(payload.get("condition"))
            seed = int(payload.get("seed"))
            case = CaseRecord(condition, seed, path, payload)
            key = (condition, seed)
            previous = by_key.get(key)
            if previous is None or _case_sort_key(previous) < _case_sort_key(case):
                by_key[key] = case
    return by_key


def _fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "`n/a`"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return f"`{value}`"
    if not (number == number and abs(number) != float("inf")):
        return "`n/a`"
    if number == 0.0:
        text = "0"
    elif abs(number) < 1e-3 or abs(number) >= 1e4:
        text = f"{number:.{digits}e}"
    else:
        text = f"{number:.{digits}f}"
    return f"`{text}`"


def _summary(values: list[float]) -> dict[str, float | int | None]:
    finite = [float(value) for value in values if value == value]
    if not finite:
        return {"n": 0, "mean": None, "median": None, "min": None, "max": None, "sd": None}
    return {
        "n": len(finite),
        "mean": statistics.fmean(finite),
        "median": statistics.median(finite),
        "min": min(finite),
        "max": max(finite),
        "sd": statistics.stdev(finite) if len(finite) > 1 else 0.0,
    }


def build_rows(cases: dict[tuple[str, int], CaseRecord]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    control_by_seed = {
        seed: case for (condition, seed), case in cases.items() if condition == "eta_zero"
    }
    for (condition, seed), case in sorted(cases.items()):
        if condition == "eta_zero":
            continue
        control = control_by_seed.get(seed)
        if control is None:
            continue
        score = score_against_control(
            case.payload["diagnostics"],
            control.payload["diagnostics"],
        )
        rows.append(
            {
                "condition": condition,
                "seed": seed,
                "case_path": case.path,
                "control_path": control.path,
                **score,
            }
        )
    return rows


def build_report(payload: dict[str, Any]) -> str:
    rows = payload["rows"]
    lines = [
        "# Knot Score v0.3 Report",
        "",
        f"Date: {payload['finished_utc']}.",
        "",
        "## Scope",
        "",
        "This report applies a scorecard-style knot criterion to the existing",
        "matched long-run JSON files. It does not rerun simulations and it does not",
        "claim a final scalar knot definition.",
        "",
        "The current score averages four available components against the matched",
        "`eta_zero` seed control:",
        "",
        "- residence gain over control, pass at `>=3`, partial at `>=2`;",
        "- compactness gain, defined as `eta_zero radius / case radius`, pass at `>=5`, partial at `>=3`;",
        "- voxel stability, defined as min/max residence across voxel sizes, pass at `>=0.25`, partial at `>=0.15`;",
        "- internal occupancy dimension `D_occ`, pass at `>=1.5`, partial at `>=1.25`.",
        "",
        "The `D_occ` component is an internal-dimensional-support signal, not an",
        "external three-dimensionality criterion. Shape roundness is reported where",
        "available, but it is not yet included in the scalar score because the",
        "archived 10M JSON files predate the new center/shape diagnostics.",
        "",
        "## Seed Scorecard",
        "",
        "| condition | seed | score | residence gain | compactness gain | voxel stability | D_occ | roundness | best residence | radius | components R/C/V/D |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        components = (
            f"{row['residence_score']:.1f}/{row['compactness_score']:.1f}/"
            f"{row['voxel_score']:.1f}/{row['dimension_score']:.1f}"
        )
        lines.append(
            f"| `{row['condition']}` | `{row['seed']}` | {_fmt(row['score'])} | "
            f"{_fmt(row['residence_gain'])} | {_fmt(row['compactness_gain'])} | "
            f"{_fmt(row['voxel_stability'])} | {_fmt(row['internal_dimension'])} | "
            f"{_fmt(row['shape_roundness'])} | {_fmt(row['case_best_residence'])} | "
            f"{_fmt(row['case_mean_radius'])} | `{components}` |"
        )

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["condition"]].append(row)
    lines.extend([
        "",
        "## Condition Summary",
        "",
        "| condition | n | score mean | score median | residence gain median | compactness gain median | voxel stability median | D_occ median |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for condition, condition_rows in sorted(grouped.items()):
        score_summary = _summary([row["score"] for row in condition_rows])
        residence_summary = _summary([
            row["residence_gain"] for row in condition_rows if row["residence_gain"] is not None
        ])
        compact_summary = _summary([
            row["compactness_gain"] for row in condition_rows if row["compactness_gain"] is not None
        ])
        voxel_summary = _summary([
            row["voxel_stability"] for row in condition_rows if row["voxel_stability"] is not None
        ])
        dimension_summary = _summary([
            row["internal_dimension"] for row in condition_rows if row["internal_dimension"] is not None
        ])
        lines.append(
            f"| `{condition}` | `{score_summary['n']}` | {_fmt(score_summary['mean'])} | "
            f"{_fmt(score_summary['median'])} | {_fmt(residence_summary['median'])} | "
            f"{_fmt(compact_summary['median'])} | {_fmt(voxel_summary['median'])} | "
            f"{_fmt(dimension_summary['median'])} |"
        )

    baseline = grouped.get("baseline", [])
    single = grouped.get("single_scale", [])
    paired = []
    single_by_seed = {row["seed"]: row for row in single}
    for row in baseline:
        other = single_by_seed.get(row["seed"])
        if other is None:
            continue
        paired.append(float(row["score"]) - float(other["score"]))
    paired_summary = _summary(paired)
    lines.extend(
        [
            "",
            "## Reading",
            "",
            "- High score means the condition separates from the no-feedback",
            "  `eta_zero` control for that seed in residence, compactness, voxel",
            "  stability, and non-collapsed internal occupancy dimension.",
            "- This is a feedback-confinement plus internal-dimensional-support score,",
            "  not yet a proof of a specific two-scale knot mechanism.",
            f"- Baseline minus `single_scale` score difference has median {_fmt(paired_summary['median'])};",
            "  therefore the current score still does not isolate the baseline two-scale",
            "  kernel as necessary.",
            "- New long-run outputs now include center/shape diagnostics, but the archived",
            "  10M JSON files do not; the next evidence step is to rerun selected cases",
            "  and compare sample-shape versus memory-cloud shape.",
            "",
        ]
    )
    return "\n".join(lines)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score existing long-run knot evidence JSON files.")
    parser.add_argument("--source-dir", action="append", default=[], help="Source directory or comma-separated directories with case_*.json files.")
    parser.add_argument("--report", type=Path, default=Path("reports/knot_score_v0_3_2026-07-02.md"))
    parser.add_argument("--output-json", type=Path, default=Path("data/processed/knot_score/2026-07-02_v0_3/summary.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dirs = _parse_path_list(args.source_dir) if args.source_dir else DEFAULT_SOURCE_DIRS
    cases = load_cases(source_dirs)
    rows = build_rows(cases)
    payload = {
        "description": "Knot score v0.3 scorecard on existing long-run JSON files.",
        "finished_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "--short", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "source_dirs": [str(path) for path in source_dirs],
        "rows": [
            {
                **row,
                "case_path": str(row["case_path"]),
                "control_path": str(row["control_path"]),
            }
            for row in rows
        ],
    }
    report = args.report if args.report.is_absolute() else ROOT / args.report
    output_json = args.output_json if args.output_json.is_absolute() else ROOT / args.output_json
    report.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")
    report.write_text(build_report(payload), encoding="utf-8")
    print(f"wrote {report}")
    print(f"wrote {output_json}")


if __name__ == "__main__":
    main()
