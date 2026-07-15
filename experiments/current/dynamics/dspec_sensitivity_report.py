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

from emergenz_knoten import covariance_dimension


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

BANDWIDTH_FACTORS = [0.25, 0.5, 1.0, 2.0, 4.0]
KNN_VALUES = [8, 16, 32, 64, 128]


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
        description="Audit D_spec bandwidth/kNN sensitivity using existing case summaries and covariance surrogates."
    )
    parser.add_argument("--source-dir", action="append", type=Path)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/dimensions/dspec_sensitivity_2026-07-15.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/dimensions/dspec_sensitivity_summary_2026-07-15.json"),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/dimensions/dspec_sensitivity_2026-07-15"),
    )
    parser.add_argument("--surrogate-points", type=int, default=600)
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


def _diagnostic_value(payload: dict[str, Any], path: tuple[str, ...]) -> float | None:
    value: Any = payload
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return _finite_float(value)


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


def _memory_shape(case: CaseRecord) -> dict[str, Any]:
    diagnostics = case.payload.get("diagnostics", {})
    memory_cloud = diagnostics.get("memory_cloud", {}) if isinstance(diagnostics, dict) else {}
    shape = memory_cloud.get("shape", {}) if isinstance(memory_cloud, dict) else {}
    return shape if isinstance(shape, dict) else {}


def _memory_spectral(case: CaseRecord) -> dict[str, Any]:
    diagnostics = case.payload.get("diagnostics", {})
    memory_cloud = diagnostics.get("memory_cloud", {}) if isinstance(diagnostics, dict) else {}
    spectral = memory_cloud.get("spectral", {}) if isinstance(memory_cloud, dict) else {}
    return spectral if isinstance(spectral, dict) else {}


def _case_eigenvalues(case: CaseRecord) -> np.ndarray:
    eig = np.asarray(_memory_shape(case).get("covariance_eigenvalues", []), dtype=float)
    eig = eig[np.isfinite(eig) & (eig > 0.0)]
    return eig


def _case_point_count(case: CaseRecord, default: int) -> int:
    spectral = _memory_spectral(case)
    for key in ("source_n_points", "n_points"):
        value = spectral.get(key)
        if isinstance(value, int) and value >= 100:
            return int(value)
    return int(default)


def _surrogate_seed(case: CaseRecord) -> int:
    condition_bit = 17 if case.condition == "baseline" else 53
    return int(case.dim * 1009 + case.seed * 9176 + condition_bit)


def covariance_surrogate(eigenvalues: Iterable[float], *, n_points: int, seed: int) -> np.ndarray:
    eig = np.asarray(list(eigenvalues), dtype=float)
    eig = eig[np.isfinite(eig) & (eig > 0.0)]
    if eig.size == 0:
        raise ValueError("at least one positive eigenvalue is required")
    rng = np.random.default_rng(seed)
    points = rng.normal(size=(int(n_points), eig.size)) * np.sqrt(eig)[None, :]
    return points.astype(float)


def _dimension_from_eigenvalues(values: np.ndarray, *, eigen_count: int = 50) -> float | None:
    w = np.asarray(values, dtype=float)
    w = w[np.isfinite(w) & (w > 1e-10) & (w < 1.0 - 1e-10)]
    if w.size < 2:
        return None
    w = np.sort(w)[-min(int(eigen_count), len(w)) :]
    w_mean = float(np.mean(w))
    if not np.isfinite(w_mean) or w_mean <= 0.0:
        return None
    log_ratio = float(np.log(float(w.max()) / w_mean))
    if not np.isfinite(log_ratio) or log_ratio <= 0.0:
        return None
    out = float(np.log(len(w)) / log_ratio)
    return out if np.isfinite(out) and 0.5 <= out <= 20.0 else None




def _heat_trace_dimension_from_transition_eigenvalues(
    values: np.ndarray,
    *,
    eigen_count: int = 50,
) -> float | None:
    transition = np.asarray(values, dtype=float)
    transition = transition[np.isfinite(transition)]
    if transition.size < 3:
        return None
    laplacian = np.maximum(1.0 - transition, 0.0)
    laplacian.sort()
    zero_modes = laplacian[laplacian <= 1e-10]
    positive_modes = laplacian[laplacian > 1e-10]
    if positive_modes.size < 2:
        return None
    positive_modes = positive_modes[: min(int(eigen_count), positive_modes.size)]
    modes = np.concatenate((zero_modes, positive_modes))
    times = np.geomspace(
        0.1 / float(positive_modes[-1]),
        10.0 / float(positive_modes[0]),
        256,
    )
    heat_trace = np.exp(-np.outer(times, modes)).sum(axis=1)
    log_times = np.log(times)
    local_dimensions = -2.0 * np.gradient(
        np.log(heat_trace), log_times, edge_order=2
    )
    local_change = np.gradient(local_dimensions, log_times, edge_order=2)
    eligible = (
        np.isfinite(local_dimensions)
        & np.isfinite(local_change)
        & (heat_trace > max(float(zero_modes.size) + 1.0, 2.5))
        & (heat_trace < 0.5 * float(modes.size))
        & (local_dimensions >= 0.25)
        & (local_dimensions <= 20.0)
        & (np.abs(local_change) <= 0.25)
    )
    windows: list[tuple[float, int, int]] = []
    start: int | None = None
    for index, is_eligible in enumerate(eligible):
        if bool(is_eligible) and start is None:
            start = index
        if start is not None and (
            not bool(is_eligible) or index == len(eligible) - 1
        ):
            stop = index if bool(is_eligible) else index - 1
            width = float(log_times[stop] - log_times[start])
            if width >= float(np.log(2.0)):
                windows.append((width, start, stop))
            start = None
    if not windows:
        return None
    _, start, stop = max(windows, key=lambda item: item[0])
    dimension = float(np.median(local_dimensions[start : stop + 1]))
    return dimension if np.isfinite(dimension) else None

def _pairwise_squared(points: np.ndarray) -> np.ndarray:
    return ((points[:, None, :] - points[None, :, :]) ** 2).sum(-1)


def heat_spectral_from_d2(
    d2: np.ndarray,
    *,
    bandwidth_factor: float,
    normalization: str = "symmetric",
    eigen_count: int = 50,
) -> float | None:
    distances = np.asarray(d2, dtype=float)
    if (
        distances.ndim != 2
        or distances.shape[0] != distances.shape[1]
        or distances.shape[0] < 100
    ):
        return None
    if not np.isfinite(bandwidth_factor) or bandwidth_factor <= 0.0:
        raise ValueError("bandwidth_factor must be positive and finite")
    if normalization == "legacy_row":
        positive = distances[distances > 1e-10]
        if positive.size == 0:
            return None
        bandwidth = float(np.median(positive)) * float(bandwidth_factor)
        kernel = np.exp(-distances / bandwidth)
        matrix = kernel / (kernel.sum(axis=1)[:, None] + 1e-12)
        return _dimension_from_eigenvalues(
            np.linalg.eigvalsh(matrix), eigen_count=eigen_count
        )
    if normalization != "symmetric":
        raise ValueError("unknown normalization")

    neighbor_distances = distances.copy()
    np.fill_diagonal(neighbor_distances, np.inf)
    neighbor_index = min(7, distances.shape[0] - 2)
    local_scales = np.partition(
        neighbor_distances, neighbor_index, axis=1
    )[:, neighbor_index]
    local_scales = local_scales[
        np.isfinite(local_scales) & (local_scales > 1e-14)
    ]
    if local_scales.size == 0:
        return None
    bandwidth = float(np.median(local_scales)) * float(bandwidth_factor)
    kernel = np.exp(-distances / bandwidth)
    density = kernel.sum(axis=1)
    corrected = kernel / (np.outer(density, density) + 1e-24)
    degree = corrected.sum(axis=1)
    matrix = corrected / np.sqrt(np.outer(degree, degree) + 1e-24)
    return _heat_trace_dimension_from_transition_eigenvalues(
        np.linalg.eigvalsh(matrix), eigen_count=eigen_count
    )


def knn_spectral_from_d2(d2: np.ndarray, *, k: int, eigen_count: int = 50) -> float | None:
    n = int(d2.shape[0])
    if n < 100:
        return None
    kk = int(min(max(k, 2), n - 1))
    work = d2.copy()
    np.fill_diagonal(work, np.inf)
    idx = np.argpartition(work, kk, axis=1)[:, :kk]
    adjacency = np.zeros((n, n), dtype=float)
    rows = np.arange(n)[:, None]
    adjacency[rows, idx] = 1.0
    adjacency = np.maximum(adjacency, adjacency.T)
    adjacency += np.eye(n)
    degree = adjacency.sum(axis=1)
    matrix = adjacency / np.sqrt(np.outer(degree, degree) + 1e-24)
    return _heat_trace_dimension_from_transition_eigenvalues(
        np.linalg.eigvalsh(matrix), eigen_count=eigen_count
    )


def case_row(case: CaseRecord, *, surrogate_points: int) -> dict[str, Any] | None:
    eig = _case_eigenvalues(case)
    if eig.size == 0:
        return None
    n_points = _case_point_count(case, surrogate_points)
    points = covariance_surrogate(eig, n_points=n_points, seed=_surrogate_seed(case))
    d2 = _pairwise_squared(points)
    shape = _memory_shape(case)
    spectral = _memory_spectral(case)

    row: dict[str, Any] = {
        "steps": case.steps,
        "dim": case.dim,
        "condition": case.condition,
        "seed": case.seed,
        "path": _rel(case.path),
        "point_count": int(n_points),
        "memory_shape_dimension": _diagnostic_value(shape, ("effective_dimension",)),
        "memory_roundness": _diagnostic_value(shape, ("axis_ratio_min_max",)),
        "stored_legacy_dspec": _diagnostic_value(spectral, ("dimension",)),
        "surrogate_covariance_dimension": covariance_dimension(points),
    }
    heat_values: list[float] = []
    legacy_values: list[float] = []
    for factor in BANDWIDTH_FACTORS:
        heat = heat_spectral_from_d2(d2, bandwidth_factor=factor, normalization="symmetric")
        legacy = heat_spectral_from_d2(d2, bandwidth_factor=factor, normalization="legacy_row")
        row[f"heat_sym_{factor:g}"] = heat
        row[f"heat_legacy_{factor:g}"] = legacy
        if heat is not None:
            heat_values.append(float(heat))
        if legacy is not None:
            legacy_values.append(float(legacy))
    knn_values: list[float] = []
    for k in KNN_VALUES:
        value = knn_spectral_from_d2(d2, k=k)
        row[f"knn_{k}"] = value
        if value is not None:
            knn_values.append(float(value))
    row["heat_sym_range"] = (max(heat_values) - min(heat_values)) if heat_values else None
    row["legacy_range"] = (max(legacy_values) - min(legacy_values)) if legacy_values else None
    row["knn_range"] = (max(knn_values) - min(knn_values)) if knn_values else None
    row["heat_sym_near3_fraction"] = (
        sum(1 for value in heat_values if 2.75 <= value <= 3.25) / len(heat_values)
        if heat_values
        else None
    )
    return row


def build_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metrics = [
        "memory_shape_dimension",
        "memory_roundness",
        "stored_legacy_dspec",
        "surrogate_covariance_dimension",
        "heat_sym_0.25",
        "heat_sym_0.5",
        "heat_sym_1",
        "heat_sym_2",
        "heat_sym_4",
        "heat_legacy_1",
        "knn_16",
        "knn_32",
        "knn_64",
        "heat_sym_range",
        "legacy_range",
        "knn_range",
        "heat_sym_near3_fraction",
    ]
    grouped: dict[tuple[int, int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(int(row["steps"]), int(row["dim"]), str(row["condition"]))].append(row)
    summary: list[dict[str, Any]] = []
    for (steps, dim, condition), group in sorted(grouped.items()):
        item: dict[str, Any] = {"steps": steps, "dim": dim, "condition": condition, "n": len(group)}
        for metric in metrics:
            values = [row.get(metric) for row in group]
            q1, q3 = _iqr(values)
            item[f"{metric}_median"] = _median(values)
            item[f"{metric}_q1"] = q1
            item[f"{metric}_q3"] = q3
        summary.append(item)
    return summary


def synthetic_rank_controls(*, n_points: int = 600, ambient_dim: int = 20) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rank in [1, 2, 3, 5, 10, 15]:
        if rank > ambient_dim:
            continue
        points = np.zeros((n_points, ambient_dim), dtype=float)
        rng = np.random.default_rng(10_000 + rank)
        points[:, :rank] = rng.normal(size=(n_points, rank))
        d2 = _pairwise_squared(points)
        row: dict[str, Any] = {
            "rank": rank,
            "ambient_dim": ambient_dim,
            "covariance_dimension": covariance_dimension(points),
        }
        for factor in BANDWIDTH_FACTORS:
            row[f"heat_sym_{factor:g}"] = heat_spectral_from_d2(
                d2, bandwidth_factor=factor, normalization="symmetric"
            )
        for k in KNN_VALUES:
            row[f"knn_{k}"] = knn_spectral_from_d2(d2, k=k)
        rows.append(row)
    return rows


def _summary_by_key(summary: list[dict[str, Any]]) -> dict[tuple[int, int, str], dict[str, Any]]:
    return {(int(item["steps"]), int(item["dim"]), str(item["condition"])): item for item in summary}


def _plot(summary: list[dict[str, Any]], figure_dir: Path) -> list[Path]:
    figure_dir.mkdir(parents=True, exist_ok=True)
    baseline = [item for item in summary if item["condition"] == "baseline" and item["steps"] == 30_000_000]
    baseline.sort(key=lambda item: item["dim"])
    paths: list[Path] = []

    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    dims = [item["dim"] for item in baseline]
    series = [
        ("stored_legacy_dspec_median", "stored legacy D_spec", "#444444"),
        ("heat_sym_0.5_median", "sym heat f=0.5", "#1f77b4"),
        ("heat_sym_1_median", "sym heat f=1", "#2ca02c"),
        ("heat_sym_2_median", "sym heat f=2", "#ff7f0e"),
        ("knn_32_median", "kNN k=32", "#9467bd"),
    ]
    for key, label, color in series:
        ax.plot(dims, [item.get(key) for item in baseline], marker="o", label=label, color=color)
    ax.axhline(3.0, color="#222222", linestyle="--", linewidth=1.0, alpha=0.7)
    ax.set_xlabel("ambient dimension d")
    ax.set_ylabel("D_spec diagnostic")
    ax.set_title("D_spec sensitivity on covariance-matched memory surrogates")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, ncol=2)
    fig.tight_layout()
    path = figure_dir / "dspec_sensitivity_by_dimension.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    paths.append(path)

    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    ax.plot(dims, [item.get("heat_sym_range_median") for item in baseline], marker="o", label="heat bandwidth range")
    ax.plot(dims, [item.get("knn_range_median") for item in baseline], marker="o", label="kNN range")
    ax.plot(dims, [item.get("heat_sym_near3_fraction_median") for item in baseline], marker="o", label="near-3 heat fraction")
    ax.set_xlabel("ambient dimension d")
    ax.set_ylabel("sensitivity diagnostic")
    ax.set_title("Scale sensitivity of D_spec surrogates")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    path = figure_dir / "dspec_sensitivity_ranges.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    paths.append(path)
    return paths


def _build_report(
    *,
    rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    synthetic: list[dict[str, Any]],
    source_dirs: list[Path],
    summary_json: Path,
    figure_paths: list[Path],
    report_path: Path,
) -> str:
    lines = [
        "# D_spec Sensitivity Audit",
        "",
        f"Date: {_utc_now()}.",
        "",
        "## Scope",
        "",
        "This audit is the next Paper-II guardrail after the 3D dimension claim audit.",
        "The existing case JSONs do not store raw memory-cloud coordinates, so this",
        "report does not remeasure the original clouds. Instead it separates:",
        "",
        "- stored historical `D_spec memory` values from the case summaries;",
        "- covariance-matched Gaussian surrogates using the saved memory covariance eigenvalues;",
        "- symmetric heat-kernel bandwidth sensitivity;",
        "- kNN graph-scale sensitivity.",
        "",
        "The result is a methodological stress test, not a new dimension-selection claim.",
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
        lines.append(f"- [{path.stem}]({_rel_from(report_path, path)})")

    lines.extend(
        [
            "",
            "## Main Summary",
            "",
            "| N | dim | condition | seeds | D_mem | stored D_spec | sym heat f=0.5 | sym heat f=1 | sym heat f=2 | kNN 32 | heat range | kNN range | near-3 heat fraction |",
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
                    _fmt_iqr(item.get("memory_shape_dimension_median"), item.get("memory_shape_dimension_q1"), item.get("memory_shape_dimension_q3")),
                    _fmt_iqr(item.get("stored_legacy_dspec_median"), item.get("stored_legacy_dspec_q1"), item.get("stored_legacy_dspec_q3")),
                    _fmt_iqr(item.get("heat_sym_0.5_median"), item.get("heat_sym_0.5_q1"), item.get("heat_sym_0.5_q3")),
                    _fmt_iqr(item.get("heat_sym_1_median"), item.get("heat_sym_1_q1"), item.get("heat_sym_1_q3")),
                    _fmt_iqr(item.get("heat_sym_2_median"), item.get("heat_sym_2_q1"), item.get("heat_sym_2_q3")),
                    _fmt_iqr(item.get("knn_32_median"), item.get("knn_32_q1"), item.get("knn_32_q3")),
                    _fmt_iqr(item.get("heat_sym_range_median"), item.get("heat_sym_range_q1"), item.get("heat_sym_range_q3")),
                    _fmt_iqr(item.get("knn_range_median"), item.get("knn_range_q1"), item.get("knn_range_q3")),
                    _fmt_iqr(item.get("heat_sym_near3_fraction_median"), item.get("heat_sym_near3_fraction_q1"), item.get("heat_sym_near3_fraction_q3")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Synthetic Rank Controls",
            "",
            "These controls use known-rank Gaussian clouds embedded in 20 dimensions.",
            "They show how strongly the current lightweight D_spec proxy depends on scale.",
            "",
            "| true rank | D_cov | heat f=0.25 | heat f=0.5 | heat f=1 | heat f=2 | heat f=4 | kNN 32 |",
            "| ---: | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in synthetic:
        lines.append(
            f"| `{row['rank']}` | {_fmt(row.get('covariance_dimension'))} | "
            f"{_fmt(row.get('heat_sym_0.25'))} | {_fmt(row.get('heat_sym_0.5'))} | "
            f"{_fmt(row.get('heat_sym_1'))} | {_fmt(row.get('heat_sym_2'))} | "
            f"{_fmt(row.get('heat_sym_4'))} | {_fmt(row.get('knn_32'))} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The previous `D_spec memory ~=3` signal should be treated as legacy and exploratory.",
            "  The old implementation used a row-normalized kernel with a symmetric eigenvalue solver;",
            "  future runs should use the symmetric normalized heat kernel or an explicitly non-symmetric solver.",
            "- The covariance-surrogate stress test is scale-sensitive: changing bandwidth or kNN scale",
            "  moves the diagnostic by order-one amounts in several dimensions.",
            "- Therefore `D_spec memory` remains a useful Paper-II lead, but it is not yet a robust",
            "  external-dimension observable.",
            "- The next data-format change should persist a small raw final memory-cloud snapshot",
            "  so D_spec sensitivity can be run on actual clouds instead of covariance surrogates.",
            "- The next physics-facing test remains relational response rank: if an external sector is",
            "  effectively three-dimensional, a weak second knot or probe should see a rank-near-3 response.",
            "",
            "## Decision",
            "",
            "Do not use `D_spec ~=3` as a Paper-I or Paper-II claim yet. Use it only as a",
            "hypothesis-generating diagnostic that now requires raw-cloud persistence and response-rank validation.",
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
        raise SystemExit("no case_*.json files found")
    rows = [row for case in cases if (row := case_row(case, surrogate_points=args.surrogate_points)) is not None]
    summary = build_summary(rows)
    synthetic = synthetic_rank_controls(n_points=args.surrogate_points, ambient_dim=20)
    figures = _plot(summary, figure_dir)

    payload = {
        "generated_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "source_dirs": [_rel(_resolve(path)) for path in source_dirs],
        "bandwidth_factors": BANDWIDTH_FACTORS,
        "knn_values": KNN_VALUES,
        "rows": rows,
        "summary": summary,
        "synthetic_rank_controls": synthetic,
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")
    report_path.write_text(
        _build_report(
            rows=rows,
            summary=summary,
            synthetic=synthetic,
            source_dirs=source_dirs,
            summary_json=summary_path,
            figure_paths=figures,
            report_path=report_path,
        ),
        encoding="utf-8",
    )
    print(f"wrote {report_path}")
    print(f"wrote {summary_path}")
    for path in figures:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()