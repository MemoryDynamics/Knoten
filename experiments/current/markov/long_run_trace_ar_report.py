from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable

import numpy as np


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()

sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ar_mode_probe import (  # noqa: E402
    _fit_to_row,
    _fmt_complex,
    fit_ar_map,
    pca_project_series,
    standardize_feature_series,
)


DEFAULT_SOURCE_DIRS = [
    Path(
        "data/processed/long_run_metastability/"
        "dynamic_center_trace_q3_Aatt_20_N30M_seed1-5_eps1em4_rerun_2026-07-13"
    ),
    Path(
        "data/processed/long_run_metastability/"
        "dynamic_center_trace_q3_Aatt_35_N30M_seed1-5_eps1em4_rerun_2026-07-13"
    ),
]
DEFAULT_OUTPUT_JSON = Path(
    "data/processed/long_run_trace_ar_modes/"
    "N30M_eps1em4_2026-07-13/summary.json"
)
DEFAULT_REPORT = Path(
    "reports/long_runs/long_3e8/"
    "long_run_trace_ar_modes_N30M_eps1em4_2026-07-13.md"
)


@dataclass(frozen=True)
class CaseRecord:
    a_att: float
    condition: str
    seed: int
    path: Path
    payload: dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fit coarse-grained AR maps on stored dynamic-center long-run "
            "traces. This reuses completed simulations and is a mode diagnostic, "
            "not a closed-dynamics proof."
        )
    )
    parser.add_argument("--source-dirs", type=str, nargs="+", default=[str(p) for p in DEFAULT_SOURCE_DIRS])
    parser.add_argument("--conditions", type=str, nargs="+", default=["baseline", "eta_zero"])
    parser.add_argument("--a-att", type=float, nargs="*", default=None)
    parser.add_argument("--block-memory-times", type=float, nargs="+", default=[0.1, 1.0, 5.0])
    parser.add_argument("--lags", type=int, nargs="+", default=[1, 2, 5])
    parser.add_argument("--pca-components", type=int, default=6)
    parser.add_argument("--ridge", type=float, default=1e-6)
    parser.add_argument("--imag-tol", type=float, default=1e-3)
    parser.add_argument("--unstable-tol", type=float, default=1.05)
    parser.add_argument("--slow-abs-min", type=float, default=0.2)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
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


def _parse_path_list(values: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if item:
                paths.append(Path(item))
    return paths


def _load_cases(
    source_dirs: Iterable[Path],
    *,
    conditions: set[str],
    a_att_filter: set[float] | None,
) -> list[CaseRecord]:
    cases: list[CaseRecord] = []
    for source_dir in source_dirs:
        directory = _resolve(source_dir)
        if not directory.exists():
            continue
        for path in sorted(directory.glob("case_*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            condition = str(payload.get("condition"))
            if condition not in conditions:
                continue
            config = payload.get("config", {})
            if not isinstance(config, dict):
                continue
            try:
                a_att = float(config["amplitude_att"])
                seed = int(payload["seed"])
            except (KeyError, TypeError, ValueError):
                continue
            if a_att_filter is not None and a_att not in a_att_filter:
                continue
            cases.append(CaseRecord(a_att, condition, seed, path, payload))
    return sorted(cases, key=lambda case: (case.a_att, case.condition, case.seed))


def _dynamic_trace(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    diagnostics = payload.get("diagnostics", {})
    dynamic = diagnostics.get("dynamic_center_trace", {}) if isinstance(diagnostics, dict) else {}
    trace = dynamic.get("trace", {}) if isinstance(dynamic, dict) else {}
    spin = dynamic.get("spin_proxy", {}) if isinstance(dynamic, dict) else {}
    return (
        dynamic if isinstance(dynamic, dict) else {},
        trace if isinstance(trace, dict) else {},
        spin if isinstance(spin, dict) else {},
    )


def _uniform_tail_arrays(case: CaseRecord) -> dict[str, np.ndarray] | None:
    _, trace, spin = _dynamic_trace(case.payload)
    sample_count_value = spin.get("sample_count")
    try:
        sample_count = int(sample_count_value)
    except (TypeError, ValueError):
        sample_count = 0
    if sample_count < 4:
        return None
    config = case.payload.get("config", {})
    if not isinstance(config, dict):
        return None
    try:
        alpha = float(config["alpha"])
    except (KeyError, TypeError, ValueError):
        return None
    steps = np.asarray(trace.get("steps", []), dtype=float)
    centers = np.asarray(trace.get("centers", []), dtype=float)
    positions = np.asarray(trace.get("positions", []), dtype=float)
    radii = np.asarray(trace.get("rms_radii", []), dtype=float)
    x_distances = np.asarray(trace.get("x_distances", []), dtype=float)
    if (
        steps.size < sample_count
        or centers.shape != positions.shape
        or centers.ndim != 2
        or centers.shape[0] != steps.size
        or radii.shape[0] != steps.size
        or x_distances.shape[0] != steps.size
    ):
        return None
    steps = steps[-sample_count:]
    centers = centers[-sample_count:]
    positions = positions[-sample_count:]
    radii = radii[-sample_count:]
    x_distances = x_distances[-sample_count:]
    gaps = np.diff(steps) * alpha
    if gaps.size == 0 or np.any(~np.isfinite(gaps)) or np.any(gaps <= 0.0):
        return None
    if not np.allclose(gaps, np.median(gaps), rtol=1e-6, atol=1e-12):
        return None
    return {
        "times": steps * alpha,
        "centers": centers,
        "positions": positions,
        "radii": radii,
        "x_distances": x_distances,
        "dt_memory": np.asarray([float(np.median(gaps))]),
        "alpha": np.asarray([alpha]),
    }


def _bivector_components(rel: np.ndarray, velocity: np.ndarray) -> np.ndarray:
    dim = rel.shape[1]
    if dim < 2:
        return np.empty((rel.shape[0], 0), dtype=float)
    pieces: list[np.ndarray] = []
    for i in range(dim):
        for j in range(i + 1, dim):
            pieces.append(rel[:, i] * velocity[:, j] - rel[:, j] * velocity[:, i])
    return np.stack(pieces, axis=1) if pieces else np.empty((rel.shape[0], 0), dtype=float)


def trace_block_features(case: CaseRecord, *, block_memory_time: float) -> np.ndarray:
    arrays = _uniform_tail_arrays(case)
    if arrays is None:
        return np.empty((0, 0), dtype=float)
    centers = arrays["centers"]
    positions = arrays["positions"]
    radii = arrays["radii"]
    x_distances = arrays["x_distances"]
    dt_memory = float(arrays["dt_memory"][0])
    rel = positions - centers
    rel_mid = 0.5 * (rel[:-1] + rel[1:])
    radius_mid = 0.5 * (radii[:-1] + radii[1:])
    x_distance_mid = 0.5 * (x_distances[:-1] + x_distances[1:])
    rel_velocity = np.diff(rel, axis=0) / dt_memory
    center_velocity = np.diff(centers, axis=0) / dt_memory
    positive_radius = radius_mid[np.isfinite(radius_mid) & (radius_mid > 0.0)]
    if positive_radius.size == 0:
        return np.empty((0, 0), dtype=float)
    radius_scale = float(np.median(positive_radius))
    if not math.isfinite(radius_scale) or radius_scale <= 0.0:
        return np.empty((0, 0), dtype=float)
    safe_radius = np.where(radius_mid > 0.0, radius_mid, radius_scale)
    center_speed = np.linalg.norm(center_velocity, axis=1) / radius_scale
    rel_speed = np.linalg.norm(rel_velocity, axis=1) / radius_scale
    bivectors = _bivector_components(rel_mid, rel_velocity)
    spin_amplitude = (
        np.linalg.norm(bivectors, axis=1) / (radius_scale * radius_scale)
        if bivectors.shape[1]
        else np.zeros(rel_mid.shape[0], dtype=float)
    )
    raw_features = np.column_stack(
        [
            rel_mid / radius_scale,
            rel_velocity / radius_scale,
            np.log(safe_radius / radius_scale),
            x_distance_mid / safe_radius,
            center_speed,
            rel_speed,
            spin_amplitude,
        ]
    )
    raw_features = raw_features[np.all(np.isfinite(raw_features), axis=1)]
    if raw_features.shape[0] == 0:
        return np.empty((0, 0), dtype=float)
    block_size = max(1, int(round(float(block_memory_time) / dt_memory)))
    n_blocks = raw_features.shape[0] // block_size
    if n_blocks < 4:
        return np.empty((0, raw_features.shape[1]), dtype=float)
    trimmed = raw_features[: n_blocks * block_size]
    return trimmed.reshape(n_blocks, block_size, raw_features.shape[1]).mean(axis=1)


def _fit_group(
    cases: list[CaseRecord],
    *,
    block_memory_time: float,
    lags: list[int],
    pca_components: int,
    ridge: float,
    imag_tol: float,
    unstable_tol: float,
    slow_abs_min: float,
) -> dict[str, Any] | None:
    raw_series: list[np.ndarray] = []
    seed_counts: dict[int, int] = {}
    for case in cases:
        features = trace_block_features(case, block_memory_time=block_memory_time)
        if features.shape[0] > max(lags, default=0) + 2 and features.shape[1] > 0:
            raw_series.append(features)
            seed_counts[case.seed] = int(features.shape[0])
    if not raw_series:
        return None
    standardized, _, _ = standardize_feature_series(raw_series)
    projected, _, explained_ratio = pca_project_series(standardized, pca_components)
    alpha = float(cases[0].payload["config"]["alpha"])
    rows: list[dict[str, Any]] = []
    for lag in lags:
        fit = fit_ar_map(
            projected,
            lag=int(lag),
            lag_updates=int(round(lag * block_memory_time / alpha)),
            ridge=float(ridge),
        )
        row = _fit_to_row(
            fit,
            imag_tol=imag_tol,
            unstable_tol=unstable_tol,
            slow_abs_min=slow_abs_min,
        )
        row["lag_memory_times"] = float(lag * block_memory_time)
        rows.append(row)
    return {
        "a_att": float(cases[0].a_att),
        "condition": cases[0].condition,
        "block_memory_time": float(block_memory_time),
        "feature_dim_raw": int(raw_series[0].shape[1]),
        "feature_dim_projected": int(projected[0].shape[1]),
        "pca_explained_ratio": [float(value) for value in explained_ratio],
        "seed_block_counts": {str(seed): count for seed, count in sorted(seed_counts.items())},
        "rows": rows,
    }


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    a_att_filter = set(args.a_att) if args.a_att else None
    cases = _load_cases(
        _parse_path_list(args.source_dirs),
        conditions=set(args.conditions),
        a_att_filter=a_att_filter,
    )
    grouped: dict[tuple[float, str], list[CaseRecord]] = defaultdict(list)
    for case in cases:
        grouped[(case.a_att, case.condition)].append(case)

    results: list[dict[str, Any]] = []
    for key in sorted(grouped):
        for block_memory_time in args.block_memory_times:
            result = _fit_group(
                grouped[key],
                block_memory_time=float(block_memory_time),
                lags=[int(lag) for lag in args.lags],
                pca_components=int(args.pca_components),
                ridge=float(args.ridge),
                imag_tol=float(args.imag_tol),
                unstable_tol=float(args.unstable_tol),
                slow_abs_min=float(args.slow_abs_min),
            )
            if result is not None:
                results.append(result)
    return {
        "description": "AR mode probe on stored N=30M dynamic-center trace windows.",
        "created_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "source_dirs": [str(path) for path in _parse_path_list(args.source_dirs)],
        "parameters": {
            "conditions": args.conditions,
            "a_att": args.a_att,
            "block_memory_times": args.block_memory_times,
            "lags": args.lags,
            "pca_components": args.pca_components,
            "ridge": args.ridge,
            "imag_tol": args.imag_tol,
            "unstable_tol": args.unstable_tol,
            "slow_abs_min": args.slow_abs_min,
        },
        "case_count": len(cases),
        "results": results,
    }


def _fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return "`n/a`"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return f"`{value}`"
    if not math.isfinite(number):
        return "`n/a`"
    if number == 0.0:
        text = "0"
    elif abs(number) < 1e-3 or abs(number) >= 1e4:
        text = f"{number:.{digits}e}"
    else:
        text = f"{number:.{digits}f}"
    return f"`{text}`"


def _classification_counts(payload: dict[str, Any]) -> Counter[tuple[str, str]]:
    counts: Counter[tuple[str, str]] = Counter()
    for result in payload["results"]:
        role = "active" if result["condition"] == "baseline" else result["condition"]
        for row in result["rows"]:
            counts[(role, row["classification"])] += 1
    return counts


def build_report(payload: dict[str, Any]) -> str:
    counts = _classification_counts(payload)
    lines = [
        "# Long-Run Trace AR Mode Probe: N=30M",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Scope",
        "",
        "This report fits linear AR maps on coarse-grained features extracted from",
        "the uniform tail windows of the completed `N=30M` dynamic-center traces.",
        "It is a mode diagnostic on reduced observables, not a proof that these",
        "variables form a closed Markov state.",
        "",
        "The relevant question is narrow: do the scalar long-run candidates show a",
        "lag- and block-stable complex slow mode that is absent from `eta_zero`?",
        "",
        "## Feature Construction",
        "",
        "- Use only the uniform end window used by the spin proxy.",
        "- Work in the co-moving memory-center frame with `x-c_mem`.",
        "- Normalize relative positions, relative velocities, center speed, radius,",
        "  and bivector amplitude by each case's median local radius.",
        "- Average sample-level features into non-overlapping blocks measured in",
        "  memory times, then fit `Y_{m+lag}=A Y_m + noise` after standardization",
        "  and PCA.",
        "",
        "## Parameters",
        "",
    ]
    params = payload["parameters"]
    for key in [
        "conditions",
        "a_att",
        "block_memory_times",
        "lags",
        "pca_components",
        "ridge",
        "slow_abs_min",
    ]:
        lines.append(f"- `{key}`: `{params[key]}`")
    lines.extend(
        [
            f"- `case_count`: `{payload['case_count']}`",
            f"- `git_revision`: `{payload['git_revision']}`",
            f"- `git_status`: `{payload['git_status'] or 'clean'}`",
            "",
            "## Mode Table",
            "",
            "| A_att | condition | block mem-time | lag blocks | lag mem-time | class | leading | |leading| | residual rms | n pairs | top eigenvalues |",
            "| ---: | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for result in payload["results"]:
        for row in result["rows"]:
            leading = complex(row["leading_real"] or 0.0, row["leading_imag"] or 0.0)
            lines.append(
                f"| `{result['a_att']:.6g}` | `{result['condition']}` | "
                f"`{result['block_memory_time']:.6g}` | `{row['lag']}` | "
                f"{_fmt(row['lag_memory_times'])} | `{row['classification']}` | "
                f"`{_fmt_complex(leading)}` | {_fmt(row['leading_abs'])} | "
                f"{_fmt(row['residual_rms'])} | `{row['n_pairs']}` | "
                f"`{' ; '.join(row['top_eigenvalues'])}` |"
            )

    lines.extend(["", "## PCA Coverage", ""])
    lines.append("| A_att | condition | block mem-time | raw dim | projected dim | explained ratio first components | seed block counts |")
    lines.append("| ---: | --- | ---: | ---: | ---: | --- | --- |")
    for result in payload["results"]:
        ratios = ", ".join(f"{value:.3f}" for value in result["pca_explained_ratio"])
        seed_counts = ", ".join(
            f"{seed}:{count}" for seed, count in result["seed_block_counts"].items()
        )
        lines.append(
            f"| `{result['a_att']:.6g}` | `{result['condition']}` | "
            f"`{result['block_memory_time']:.6g}` | `{result['feature_dim_raw']}` | "
            f"`{result['feature_dim_projected']}` | `{ratios}` | `{seed_counts}` |"
        )

    lines.extend(["", "## Classification Counts", ""])
    if counts:
        for (role, classification), count in sorted(counts.items()):
            lines.append(f"- `{role}` / `{classification}`: `{count}`")
    else:
        lines.append("- No fitted rows.")

    active_complex = counts.get(("active", "complex"), 0)
    control_complex = sum(
        count for (role, classification), count in counts.items()
        if role != "active" and classification == "complex"
    )
    lines.extend(["", "## Reading", ""])
    if active_complex == 0:
        lines.extend(
            [
                "No scalar active row is classified as a complex slow mode under this",
                "feature/block/lag grid. This is consistent with the prior short AR",
                "probe: the scalar model supports relaxation and compactness more",
                "directly than a persistent oscillatory mode.",
            ]
        )
    elif control_complex >= active_complex:
        lines.extend(
            [
                "Complex classifications are not isolated to the active scalar cases.",
                "That would not support a scalar photon/phase claim without stronger",
                "feature closure and control separation.",
            ]
        )
    else:
        lines.extend(
            [
                "Some active scalar rows are classified as complex while controls are",
                "less complex. Treat this only as a candidate signal until it is stable",
                "across block sizes, lags, features, and controls.",
            ]
        )
    lines.extend(
        [
            "",
            "Paper-I implication: this AR layer can be cited as a negative or neutral",
            "mode check. It does not weaken the co-moving memory-cloud evidence, but",
            "it also does not justify photon-, spin-, or phase-mode language.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    payload = run_probe(args)
    output_json = _resolve(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    report = _resolve(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(build_report(payload), encoding="utf-8")
    print(f"wrote {output_json}")
    print(f"wrote {report}")


if __name__ == "__main__":
    main()
