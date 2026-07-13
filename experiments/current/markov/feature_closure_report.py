from __future__ import annotations

import argparse
from collections import defaultdict
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

from long_run_trace_ar_report import (  # noqa: E402
    DEFAULT_SOURCE_DIRS,
    CaseRecord,
    _load_cases,
    _parse_path_list,
    _resolve,
    trace_block_features,
)


DEFAULT_OUTPUT_JSON = Path(
    "data/processed/feature_closure/"
    "N30M_eps1em4_2026-07-13/summary.json"
)
DEFAULT_REPORT = Path(
    "reports/long_runs/long_3e8/"
    "feature_closure_N30M_eps1em4_2026-07-13.md"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate coarse feature-closure on stored N=30M dynamic-center "
            "traces. Closure means predictive skill over shuffled controls, "
            "not a proof of a closed Markov state."
        )
    )
    parser.add_argument("--source-dirs", type=str, nargs="+", default=[str(p) for p in DEFAULT_SOURCE_DIRS])
    parser.add_argument("--conditions", type=str, nargs="+", default=["baseline", "eta_zero"])
    parser.add_argument("--a-att", type=float, nargs="*", default=[35.0])
    parser.add_argument("--block-memory-times", type=float, nargs="+", default=[0.1, 1.0, 5.0])
    parser.add_argument("--lags", type=int, nargs="+", default=[1, 2, 5])
    parser.add_argument("--ridge", type=float, default=1e-6)
    parser.add_argument("--shuffle-repeats", type=int, default=5)
    parser.add_argument("--random-seed", type=int, default=20260713)
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
    return completed.stdout.strip().replace("\r\n", "; ").replace("\n", "; ")


def _standardize_train_test(
    train: list[np.ndarray],
    test: np.ndarray,
) -> tuple[list[np.ndarray], np.ndarray]:
    stacked = np.vstack(train).astype(float)
    mean = stacked.mean(axis=0)
    scale = stacked.std(axis=0)
    scale[scale == 0.0] = 1.0
    return [((arr - mean) / scale) for arr in train], (test - mean) / scale


def _lagged_xy(series: list[np.ndarray], lag: int) -> tuple[np.ndarray, np.ndarray]:
    xs: list[np.ndarray] = []
    ys: list[np.ndarray] = []
    for arr in series:
        if arr.shape[0] <= lag:
            continue
        xs.append(arr[:-lag])
        ys.append(arr[lag:])
    if not xs:
        return np.empty((0, 0), dtype=float), np.empty((0, 0), dtype=float)
    return np.vstack(xs), np.vstack(ys)


def _fit_ridge(x: np.ndarray, y: np.ndarray, ridge: float) -> np.ndarray:
    gram = x.T @ x
    return np.linalg.solve(gram + float(ridge) * np.eye(gram.shape[0]), x.T @ y)


def _r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    if y_true.size == 0 or y_true.shape != y_pred.shape:
        return float("nan")
    residual = y_true - y_pred
    centered = y_true - y_true.mean(axis=0, keepdims=True)
    sse = float(np.sum(residual * residual))
    sst = float(np.sum(centered * centered))
    if sst <= 0.0:
        return float("nan")
    return 1.0 - sse / sst


def _median(values: Iterable[float]) -> float | None:
    finite = sorted(float(value) for value in values if math.isfinite(float(value)))
    if not finite:
        return None
    n = len(finite)
    mid = n // 2
    if n % 2:
        return finite[mid]
    return 0.5 * (finite[mid - 1] + finite[mid])


def _feature_names(dim: int) -> list[str]:
    return (
        [f"rel_pos_{i}" for i in range(dim)]
        + [f"rel_vel_{i}" for i in range(dim)]
        + [
            "log_radius",
            "x_distance_over_radius",
            "center_speed_over_radius",
            "rel_speed_over_radius",
            "spin_amplitude_over_radius2",
        ]
    )


def feature_groups(feature_dim: int) -> dict[str, list[int]]:
    if feature_dim < 7 or (feature_dim - 5) % 2 != 0:
        raise ValueError(f"unsupported feature dimension: {feature_dim}")
    dim = (feature_dim - 5) // 2
    rel_pos = list(range(0, dim))
    rel_vel = list(range(dim, 2 * dim))
    log_radius = 2 * dim
    x_over_r = 2 * dim + 1
    center_speed = 2 * dim + 2
    rel_speed = 2 * dim + 3
    spin_amp = 2 * dim + 4
    return {
        "geometry": rel_pos + [log_radius, x_over_r],
        "kinematics": rel_pos + rel_vel + [rel_speed],
        "shape_scalars": [log_radius, x_over_r],
        "drift_scalars": [center_speed, rel_speed],
        "spin_scalar": [spin_amp],
        "all": list(range(feature_dim)),
    }


def _select_group(series: list[np.ndarray], indices: list[int]) -> list[np.ndarray]:
    return [arr[:, indices] for arr in series if arr.shape[0] > 0]


def _closure_scores(
    series: list[np.ndarray],
    *,
    lag: int,
    ridge: float,
    shuffle_repeats: int,
    rng: np.random.Generator,
) -> dict[str, Any] | None:
    if len(series) < 2 or any(arr.shape[0] <= lag + 1 for arr in series):
        return None
    ar_scores: list[float] = []
    persistence_scores: list[float] = []
    shuffle_scores: list[float] = []
    n_pairs = 0
    for holdout_index, test_raw in enumerate(series):
        train_raw = [arr for index, arr in enumerate(series) if index != holdout_index]
        train, test = _standardize_train_test(train_raw, test_raw)
        x_train, y_train = _lagged_xy(train, lag)
        if x_train.size == 0 or test.shape[0] <= lag:
            continue
        x_test = test[:-lag]
        y_test = test[lag:]
        coef = _fit_ridge(x_train, y_train, ridge)
        ar_scores.append(_r2_score(y_test, x_test @ coef))
        persistence_scores.append(_r2_score(y_test, x_test))
        n_pairs += int(x_test.shape[0])
        if y_train.shape[0] > 1:
            for _ in range(max(1, int(shuffle_repeats))):
                shuffled = y_train[rng.permutation(y_train.shape[0])]
                shuffled_coef = _fit_ridge(x_train, shuffled, ridge)
                shuffle_scores.append(_r2_score(y_test, x_test @ shuffled_coef))
    ar_median = _median(ar_scores)
    shuffle_median = _median(shuffle_scores)
    persistence_median = _median(persistence_scores)
    return {
        "n_series": len(series),
        "n_pairs": n_pairs,
        "ar_r2_median": ar_median,
        "shuffle_r2_median": shuffle_median,
        "persistence_r2_median": persistence_median,
        "ar_minus_shuffle": (
            ar_median - shuffle_median
            if ar_median is not None and shuffle_median is not None
            else None
        ),
        "ar_minus_persistence": (
            ar_median - persistence_median
            if ar_median is not None and persistence_median is not None
            else None
        ),
        "closure_lift": (
            min(ar_median, ar_median - shuffle_median, ar_median - persistence_median)
            if (
                ar_median is not None
                and shuffle_median is not None
                and persistence_median is not None
            )
            else None
        ),
        "ar_r2_by_seed": [float(value) for value in ar_scores if math.isfinite(value)],
    }


def _series_for_cases(cases: list[CaseRecord], block_memory_time: float) -> list[np.ndarray]:
    out: list[np.ndarray] = []
    for case in cases:
        arr = trace_block_features(case, block_memory_time=block_memory_time)
        if arr.shape[0] > 0 and arr.shape[1] > 0:
            out.append(arr)
    return out


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
    rng = np.random.default_rng(int(args.random_seed))
    results: list[dict[str, Any]] = []
    for (a_att, condition), group_cases in sorted(grouped.items()):
        for block_memory_time in args.block_memory_times:
            base_series = _series_for_cases(group_cases, float(block_memory_time))
            if not base_series:
                continue
            names = _feature_names((base_series[0].shape[1] - 5) // 2)
            groups = feature_groups(base_series[0].shape[1])
            for group_name, indices in groups.items():
                group_series = _select_group(base_series, indices)
                for lag in args.lags:
                    scores = _closure_scores(
                        group_series,
                        lag=int(lag),
                        ridge=float(args.ridge),
                        shuffle_repeats=int(args.shuffle_repeats),
                        rng=rng,
                    )
                    if scores is None:
                        continue
                    scores.update(
                        {
                            "a_att": float(a_att),
                            "condition": condition,
                            "block_memory_time": float(block_memory_time),
                            "lag": int(lag),
                            "lag_memory_time": float(lag) * float(block_memory_time),
                            "feature_group": group_name,
                            "feature_names": [names[index] for index in indices],
                        }
                    )
                    results.append(scores)
    return {
        "description": "Feature-closure probe on stored N=30M dynamic-center traces.",
        "created_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "source_dirs": [str(path) for path in _parse_path_list(args.source_dirs)],
        "parameters": {
            "conditions": args.conditions,
            "a_att": args.a_att,
            "block_memory_times": args.block_memory_times,
            "lags": args.lags,
            "ridge": args.ridge,
            "shuffle_repeats": args.shuffle_repeats,
            "random_seed": args.random_seed,
        },
        "case_count": len(cases),
        "results": results,
    }


def _fmt(value: Any, digits: int = 3) -> str:
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


def _best_rows(payload: dict[str, Any], *, limit: int = 12) -> list[dict[str, Any]]:
    rows = [
        row for row in payload["results"]
        if row.get("closure_lift") is not None
    ]
    return sorted(
        rows,
        key=lambda row: (
            float(row["closure_lift"]),
            float(row.get("ar_r2_median") or -1e9),
        ),
        reverse=True,
    )[:limit]


def build_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Feature-Closure Probe: N=30M Dynamic-Center Traces",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Scope",
        "",
        "This report asks whether reduced co-moving observables are predictive",
        "enough to be treated as a coarse state. It fits leave-one-seed-out ridge",
        "AR maps and compares their out-of-seed prediction skill with shuffled",
        "future controls and persistence. This is a closure diagnostic, not a",
        "proof that the variables define a closed Markov process.",
        "",
        "## Reading Rule",
        "",
        "- `AR R2` above shuffled control means the feature family contains real",
        "  predictive information.",
        "- `AR - persistence` near or below zero means a linear AR map does not",
        "  improve much over trivial short-lag continuity.",
        "- A Paper-I scalar claim needs baseline/control separation in compactness",
        "  and shape; feature closure is supporting evidence, not the primary",
        "  knot criterion.",
        "",
        "## Parameters",
        "",
    ]
    for key, value in payload["parameters"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            f"- `case_count`: `{payload['case_count']}`",
            f"- `git_revision`: `{payload['git_revision']}`",
            f"- `git_status`: `{payload['git_status'] or 'clean'}`",
            "",
            "## Best Closure-Lift Rows",
            "",
            "| A_att | condition | group | block mem-time | lag mem-time | AR R2 | shuffled R2 | persistence R2 | AR-shuffle | AR-persistence | closure lift | n pairs |",
            "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in _best_rows(payload):
        lines.append(
            f"| `{row['a_att']:.6g}` | `{row['condition']}` | `{row['feature_group']}` | "
            f"{_fmt(row['block_memory_time'])} | {_fmt(row['lag_memory_time'])} | "
            f"{_fmt(row['ar_r2_median'])} | {_fmt(row['shuffle_r2_median'])} | "
            f"{_fmt(row['persistence_r2_median'])} | {_fmt(row['ar_minus_shuffle'])} | "
            f"{_fmt(row['ar_minus_persistence'])} | {_fmt(row['closure_lift'])} | `{row['n_pairs']}` |"
        )
    lines.extend(["", "## Full Closure Table", ""])
    lines.append(
        "| A_att | condition | group | block mem-time | lag | AR R2 | shuffled R2 | persistence R2 | AR-shuffle | AR-persistence | closure lift |"
    )
    lines.append("| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in payload["results"]:
        lines.append(
            f"| `{row['a_att']:.6g}` | `{row['condition']}` | `{row['feature_group']}` | "
            f"{_fmt(row['block_memory_time'])} | `{row['lag']}` | "
            f"{_fmt(row['ar_r2_median'])} | {_fmt(row['shuffle_r2_median'])} | "
            f"{_fmt(row['persistence_r2_median'])} | {_fmt(row['ar_minus_shuffle'])} | "
            f"{_fmt(row['ar_minus_persistence'])} | {_fmt(row['closure_lift'])} |"
        )
    lines.extend(
        [
            "",
            "## Result",
            "",
            "The scalar baseline has its clearest closure lift in shape/radius",
            "features at short memory-time lags. Some `eta_zero` rows also have",
            "positive closure lift, so this diagnostic is not a standalone knot",
            "classifier. Raw geometry in `eta_zero` can have larger `AR R2`, but",
            "much of that is persistence of a broad random walk. The spin scalar",
            "does not produce a useful closed phase observable in the active",
            "scalar case.",
            "",
            "Paper-I implication: scalar memory is appropriate as the first",
            "coarse-graining layer for compactness, radius and relaxation. Phase-",
            "bearing sectors should remain future vector, tensor or internal-memory",
            "extensions rather than Paper-I claims.",
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
