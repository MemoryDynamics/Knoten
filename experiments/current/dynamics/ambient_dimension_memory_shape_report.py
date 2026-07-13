from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
import json
import math
from pathlib import Path
import statistics
import subprocess
from typing import Any, Iterable


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()


@dataclass(frozen=True)
class CaseRecord:
    dim: int
    condition: str
    seed: int
    steps: int
    path: Path
    payload: dict[str, Any]


SUMMARY_METRICS = [
    "dynamic_rms_radius_median",
    "dynamic_center_drift_radius_fraction_per_memory_time",
    "memory_shape_dimension",
    "memory_roundness",
    "memory_radius",
    "memory_center_residence_memory_times",
    "best_residence_memory_times",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Aggregate ambient-dimension memory-shape checks from "
            "long_run_metastability.py case JSON outputs."
        )
    )
    parser.add_argument(
        "--source-dir",
        action="append",
        type=Path,
        required=True,
        help="Directory containing case_*.json files. May be supplied multiple times.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/dimensions/ambient_memory_shape_2026-07-13.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/dimensions/ambient_memory_shape_summary_2026-07-13.json"),
    )
    return parser.parse_args()


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


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


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


def _best_voxel_residence(diagnostics: dict[str, Any]) -> float | None:
    payload = diagnostics.get("residence_by_voxel_size")
    if not isinstance(payload, dict):
        return None
    values: list[float] = []
    for item in payload.values():
        if not isinstance(item, dict):
            continue
        value = _finite_float(item.get("max_residence_memory_times"))
        if value is not None:
            values.append(value)
    return max(values) if values else None


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
    return sorted(cases, key=lambda item: (item.dim, item.condition, item.seed))


def case_row(case: CaseRecord) -> dict[str, Any]:
    diagnostics = case.payload.get("diagnostics", {})
    if not isinstance(diagnostics, dict):
        diagnostics = {}
    dynamic = diagnostics.get("dynamic_center_trace", {})
    if not isinstance(dynamic, dict):
        dynamic = {}
    trend = dynamic.get("trend", dynamic)
    if not isinstance(trend, dict):
        trend = dynamic
    memory_cloud = diagnostics.get("memory_cloud", {})
    memory_shape = memory_cloud.get("shape", {}) if isinstance(memory_cloud, dict) else {}
    if not isinstance(memory_shape, dict):
        memory_shape = {}
    return {
        "dim": case.dim,
        "condition": case.condition,
        "seed": case.seed,
        "steps": case.steps,
        "path": _rel(case.path),
        "dynamic_rms_radius_median": _diagnostic_value(trend, ("rms_radius_median",)),
        "dynamic_center_drift_radius_fraction_per_memory_time": _diagnostic_value(
            trend, ("center_drift_radius_fraction_per_memory_time_median",)
        ),
        "memory_shape_dimension": _diagnostic_value(memory_shape, ("effective_dimension",)),
        "memory_roundness": _diagnostic_value(memory_shape, ("axis_ratio_min_max",)),
        "memory_radius": _diagnostic_value(memory_shape, ("mean_radius",)),
        "memory_center_residence_memory_times": _diagnostic_value(
            diagnostics,
            ("center_residence", "memory_center", "primary_max_run_memory_times"),
        ),
        "best_residence_memory_times": _best_voxel_residence(diagnostics),
    }


def build_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(int(row["dim"]), str(row["condition"]))].append(row)

    summary: list[dict[str, Any]] = []
    for (dim, condition), group in sorted(grouped.items()):
        item: dict[str, Any] = {
            "dim": dim,
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


def _summary_by_key(summary: list[dict[str, Any]]) -> dict[tuple[int, str], dict[str, Any]]:
    return {(int(item["dim"]), str(item["condition"])): item for item in summary}


def _ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0.0):
        return None
    return numerator / denominator


def build_report(
    *,
    rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    source_dirs: Iterable[Path],
    summary_json: Path,
) -> str:
    by_key = _summary_by_key(summary)
    dims = sorted({int(row["dim"]) for row in rows})
    lines = [
        "# Ambient-Dimension Memory-Shape Check",
        "",
        f"Date: {_utc_now()}.",
        "",
        "## Scope",
        "",
        "This report tests whether the current `D_mem ~= 3` scalar reference",
        "candidate remains a local memory-shape feature beyond the originally",
        "chosen 3D embedding. It is not a dimension-selection theorem and not a",
        "macroscopic spacetime claim.",
        "",
        "Fixed target slice: `A_att=35`, `epsilon=1e-4`, corrected q=3 scalar",
        "kernel, `baseline` versus matched `eta_zero`, same co-moving dynamic",
        "center observables as the Paper-I N30M reference.",
        "",
        "## Provenance",
        "",
        f"- Source dirs: `{', '.join(_rel(_resolve(path)) for path in source_dirs)}`",
        f"- Machine-readable summary: `{_rel(summary_json)}`",
        f"- Git revision while building this report: `{_git_output(['rev-parse', 'HEAD'])}`",
        f"- Git status while building this report: `{_git_output(['status', '--short']) or 'clean'}`",
        "",
        "## Dimension Summary",
        "",
        "| dim | condition | seeds | N | radius median [q1,q3] | drift/r median [q1,q3] | D_mem median [q1,q3] | roundness median [q1,q3] |",
        "| ---: | --- | ---: | ---: | --- | --- | --- | --- |",
    ]
    for item in summary:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{int(item['dim'])}`",
                    f"`{item['condition']}`",
                    f"`{int(item['n'])}`",
                    f"`{int(item['steps']):,}`" if item.get("steps") is not None else "`n/a`",
                    _fmt_iqr(
                        item.get("dynamic_rms_radius_median_median"),
                        item.get("dynamic_rms_radius_median_q1"),
                        item.get("dynamic_rms_radius_median_q3"),
                    ),
                    _fmt_iqr(
                        item.get("dynamic_center_drift_radius_fraction_per_memory_time_median"),
                        item.get("dynamic_center_drift_radius_fraction_per_memory_time_q1"),
                        item.get("dynamic_center_drift_radius_fraction_per_memory_time_q3"),
                    ),
                    _fmt_iqr(
                        item.get("memory_shape_dimension_median"),
                        item.get("memory_shape_dimension_q1"),
                        item.get("memory_shape_dimension_q3"),
                    ),
                    _fmt_iqr(
                        item.get("memory_roundness_median"),
                        item.get("memory_roundness_q1"),
                        item.get("memory_roundness_q3"),
                    ),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Baseline/Control Separation",
            "",
            "| dim | radius gain eta0/baseline | drift separation eta0/baseline | D_mem delta | roundness delta |",
            "| ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for dim in dims:
        baseline = by_key.get((dim, "baseline"), {})
        eta_zero = by_key.get((dim, "eta_zero"), {})
        base_radius = _finite_float(baseline.get("dynamic_rms_radius_median_median"))
        ctrl_radius = _finite_float(eta_zero.get("dynamic_rms_radius_median_median"))
        base_drift = _finite_float(
            baseline.get("dynamic_center_drift_radius_fraction_per_memory_time_median")
        )
        ctrl_drift = _finite_float(
            eta_zero.get("dynamic_center_drift_radius_fraction_per_memory_time_median")
        )
        base_dim = _finite_float(baseline.get("memory_shape_dimension_median"))
        ctrl_dim = _finite_float(eta_zero.get("memory_shape_dimension_median"))
        base_round = _finite_float(baseline.get("memory_roundness_median"))
        ctrl_round = _finite_float(eta_zero.get("memory_roundness_median"))
        lines.append(
            f"| `{dim}` | {_fmt(_ratio(ctrl_radius, base_radius))} | "
            f"{_fmt(_ratio(ctrl_drift, base_drift))} | "
            f"{_fmt(base_dim - ctrl_dim if base_dim is not None and ctrl_dim is not None else None)} | "
            f"{_fmt(base_round - ctrl_round if base_round is not None and ctrl_round is not None else None)} |"
        )

    lines.extend(
        [
            "",
            "## Reading Rules",
            "",
            "- A robust extension of the current 3D finding requires compact active",
            "  memory clouds, low radius-normalized drift, and `D_mem` near three",
            "  with roundness separated from `eta_zero` across ambient dimensions.",
            "- If `D_mem` rises with ambient dimension, the old phrase `chosen 3D",
            "  embedding` remains necessary and Paper II must treat 3D as open.",
            "- If `D_mem` stays near three while roundness and compactness remain",
            "  controlled, the phrase can be upgraded to a local 3D memory-shape",
            "  phenomenon that is not tied to the original embedding.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    source_dirs = [Path(path) for path in args.source_dir]
    rows = [case_row(case) for case in load_cases(source_dirs)]
    summary = build_summary(rows)

    summary_path = _resolve(args.summary_json)
    report_path = _resolve(args.report)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_dirs": [_rel(_resolve(path)) for path in source_dirs],
        "rows": rows,
        "summary": summary,
    }
    summary_path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")
    report_path.write_text(
        build_report(
            rows=rows,
            summary=summary,
            source_dirs=source_dirs,
            summary_json=summary_path,
        ),
        encoding="utf-8",
    )
    print(f"wrote {report_path}", flush=True)
    print(f"wrote {summary_path}", flush=True)


if __name__ == "__main__":
    main()
