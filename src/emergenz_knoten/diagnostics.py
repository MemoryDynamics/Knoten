"""Numerical diagnostics for memory-driven trajectory data.

The functions here are intentionally dependency-light. They use only NumPy so
they can serve as smoke-testable reference implementations before the faster
Numba/GPU scripts are refactored.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


def _as_points(points: Iterable[Iterable[float]]) -> np.ndarray:
    arr = np.asarray(points, dtype=float)
    if arr.ndim != 2:
        raise ValueError("points must be a 2D array with shape (n_points, dim)")
    if arr.shape[0] < 2:
        raise ValueError("at least two points are required")
    return arr


def covariance_dimension(
    points: Iterable[Iterable[float]], *, rtol: float = 1e-12
) -> float:
    """Estimate effective dimension by covariance participation ratio.

    For covariance eigenvalues lambda_i, the diagnostic is

        (sum_i lambda_i)^2 / sum_i lambda_i^2.

    It is robust, cheap, and useful for quick checks, but it is not a
    substitute for fractal or spectral diagnostics.
    """

    pts = _as_points(points)
    centered = pts - pts.mean(axis=0, keepdims=True)
    cov = centered.T @ centered / max(len(centered), 1)
    eig = np.linalg.eigvalsh(cov)
    eig = eig[eig > max(float(eig.max(initial=0.0)) * rtol, rtol)]
    if eig.size == 0:
        return float("nan")
    s1 = float(eig.sum())
    s2 = float(np.dot(eig, eig))
    if s2 == 0.0:
        return float("nan")
    return s1 * s1 / s2


@dataclass(frozen=True)
class OccupancyDimensionResult:
    dimension: float
    scales: np.ndarray
    counts: np.ndarray


@dataclass(frozen=True)
class OccupancyScalingWindow:
    dimension: float
    start_index: int
    stop_index: int
    r_squared: float
    local_slope_mean: float
    local_slope_std: float
    log_width: float
    n_points: int
    valid_scaling: bool


def occupancy_local_slopes(
    scales: Iterable[float],
    counts: Iterable[float],
) -> np.ndarray:
    """Return adjacent log-log occupancy slopes."""

    scales_arr = np.asarray(list(scales), dtype=float)
    counts_arr = np.asarray(list(counts), dtype=float)
    if scales_arr.size != counts_arr.size:
        raise ValueError("scales and counts must have the same length")
    if scales_arr.size < 2:
        return np.array([], dtype=float)

    x = np.log(1.0 / scales_arr)
    y = np.log(counts_arr)
    with np.errstate(divide="ignore", invalid="ignore"):
        slopes = np.diff(y) / np.diff(x)
    return slopes[np.isfinite(slopes)]


def fit_occupancy_scaling_window(
    scales: Iterable[float],
    counts: Iterable[float],
    *,
    n_samples: int | None = None,
    min_points: int = 4,
    min_boxes: int = 20,
    max_count_fraction: float = 0.8,
    min_r_squared: float = 0.98,
    max_local_slope_std: float = 0.35,
) -> OccupancyScalingWindow:
    """Choose a stable log-log box-counting fit window.

    The historical occupancy estimator fits every box scale. This helper is
    stricter: it excludes undersampled large boxes and, when ``n_samples`` is
    known, the small-scale regime where occupied boxes saturate near the number
    of sampled points. Among contiguous windows it prefers valid, wide, locally
    stable scaling ranges.
    """

    scales_arr = np.asarray(list(scales), dtype=float)
    counts_arr = np.asarray(list(counts), dtype=float)
    if scales_arr.size != counts_arr.size:
        raise ValueError("scales and counts must have the same length")
    if min_points < 3:
        raise ValueError("min_points must be at least 3")
    if not 0.0 < max_count_fraction <= 1.0:
        raise ValueError("max_count_fraction must satisfy 0 < value <= 1")

    finite = (
        np.isfinite(scales_arr)
        & np.isfinite(counts_arr)
        & (scales_arr > 0.0)
        & (counts_arr > 0.0)
    )
    finite_indices = np.flatnonzero(finite)
    if finite_indices.size < min_points:
        return OccupancyScalingWindow(
            float("nan"), -1, -1, float("nan"), float("nan"),
            float("nan"), 0.0, 0, False
        )

    valid = finite & (counts_arr >= min_boxes)
    if n_samples is not None and n_samples > 0:
        valid &= counts_arr <= max_count_fraction * float(n_samples)

    candidates: list[tuple[bool, float, OccupancyScalingWindow]] = []
    n_scales = len(scales_arr)
    for start in range(n_scales):
        for stop in range(start + min_points, n_scales + 1):
            window_indices = np.arange(start, stop)
            if not bool(np.all(valid[window_indices])):
                continue

            x = np.log(1.0 / scales_arr[start:stop])
            y = np.log(counts_arr[start:stop])
            if np.unique(x).size < 2 or np.unique(y).size < 2:
                continue

            coeff = np.polyfit(x, y, 1)
            fit = coeff[0] * x + coeff[1]
            ss_res = float(np.sum((y - fit) ** 2))
            ss_tot = float(np.sum((y - y.mean()) ** 2))
            r_squared = float(1.0 - ss_res / ss_tot) if ss_tot > 0.0 else float("nan")
            slopes = np.diff(y) / np.diff(x)
            slopes = slopes[np.isfinite(slopes)]
            if slopes.size == 0:
                continue
            local_std = float(np.std(slopes, ddof=1)) if slopes.size > 1 else 0.0
            local_mean = float(np.mean(slopes))
            log_width = float(abs(x[-1] - x[0]))
            dimension = float(coeff[0])
            valid_scaling = (
                np.isfinite(dimension)
                and dimension > 0.0
                and np.isfinite(r_squared)
                and r_squared >= min_r_squared
                and local_std <= max_local_slope_std
            )
            result = OccupancyScalingWindow(
                dimension=dimension,
                start_index=start,
                stop_index=stop,
                r_squared=r_squared,
                local_slope_mean=local_mean,
                local_slope_std=local_std,
                log_width=log_width,
                n_points=stop - start,
                valid_scaling=valid_scaling,
            )
            score = log_width + 0.25 * r_squared - 0.25 * local_std
            candidates.append((valid_scaling, score, result))

    if not candidates:
        return OccupancyScalingWindow(
            float("nan"), -1, -1, float("nan"), float("nan"),
            float("nan"), 0.0, 0, False
        )

    valid_candidates = [item for item in candidates if item[0]]
    pool = valid_candidates if valid_candidates else candidates
    return max(pool, key=lambda item: item[1])[2]


def occupancy_dimension(
    points: Iterable[Iterable[float]],
    *,
    scales: Iterable[float] | None = None,
    n_scales: int = 10,
    min_count: int = 2,
    return_details: bool = False,
) -> float | OccupancyDimensionResult:
    """Estimate box-counting/occupancy dimension from visited boxes.

    The fit is log(N_boxes) versus log(1/scale). This reference
    implementation is deliberately conservative and returns NaN if there are
    too few valid scales for a meaningful line fit.
    """

    pts = _as_points(points)
    shifted = pts - pts.min(axis=0, keepdims=True)
    span = float(np.max(shifted.max(axis=0)))
    if not np.isfinite(span) or span <= 0.0:
        value = float("nan")
        empty = np.array([], dtype=float)
        result = OccupancyDimensionResult(value, empty, empty)
        return result if return_details else value

    if scales is None:
        lo = span / 64.0
        hi = span / 4.0
        scales_arr = np.geomspace(lo, hi, n_scales)
    else:
        scales_arr = np.asarray(list(scales), dtype=float)

    counts = []
    used_scales = []
    for scale in scales_arr:
        if not np.isfinite(scale) or scale <= 0.0:
            continue
        boxes = np.floor(shifted / scale).astype(np.int64)
        count = len({tuple(row) for row in boxes})
        if count >= min_count:
            used_scales.append(scale)
            counts.append(count)

    used = np.asarray(used_scales, dtype=float)
    counts_arr = np.asarray(counts, dtype=float)
    if used.size < 3 or np.unique(counts_arr).size < 2:
        value = float("nan")
    else:
        coeff = np.polyfit(np.log(1.0 / used), np.log(counts_arr), 1)
        value = float(coeff[0])

    result = OccupancyDimensionResult(value, used, counts_arr)
    return result if return_details else value


def residence_statistics(
    points: Iterable[Iterable[float]],
    *,
    voxel_size: float,
    min_visits: int = 2,
) -> dict[str, float]:
    """Compute simple voxel residence statistics for knot-like regions."""

    pts = _as_points(points)
    if voxel_size <= 0.0:
        raise ValueError("voxel_size must be positive")

    voxels: dict[tuple[int, ...], list[int]] = {}
    for idx, point in enumerate(pts):
        key = tuple(np.floor(point / voxel_size).astype(int))
        voxels.setdefault(key, []).append(idx)

    residences = []
    for visits in voxels.values():
        if len(visits) < min_visits:
            continue
        visit_arr = np.asarray(visits, dtype=int)
        gaps = np.diff(visit_arr)
        transitions = int(np.sum(gaps > 1))
        residences.append(len(visit_arr) / (transitions + 1))

    if not residences:
        return {
            "knot_count": 0.0,
            "mean_residence": 0.0,
            "max_residence": 0.0,
            "visited_voxels": float(len(voxels)),
        }

    res = np.asarray(residences, dtype=float)
    return {
        "knot_count": float(len(residences)),
        "mean_residence": float(res.mean()),
        "max_residence": float(res.max()),
        "visited_voxels": float(len(voxels)),
    }


def spectral_dimension(points: Iterable[Iterable[float]]) -> float:
    """Estimate spectral dimension from heat kernel eigenvalue distribution.

    Uses normalized Laplacian spectrum: eigenvalues measure scale-dependence
    of local connectivity. Returns NaN if computation is unreliable.
    """
    pts = _as_points(points)
    if len(pts) < 100:
        return float("nan")

    D2 = ((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1)
    eps = float(np.median(D2[D2 > 1e-10]))
    if not np.isfinite(eps) or eps <= 0.0:
        return float("nan")

    K = np.exp(-D2 / eps)

    # Normalize K to be more stable
    rowsums = K.sum(axis=1, keepdims=True)
    K_norm = K / (rowsums + 1e-12)

    w = np.linalg.eigvalsh(K_norm)

    # Filter out spurious eigenvalues
    w = w[(w > 1e-10) & (w < 1.0 - 1e-10)]

    if len(w) < 2:
        return float("nan")

    # Use only the largest eigenvalues that represent significant structure
    w = np.sort(w)[-min(50, len(w)) :]

    w_mean = float(np.mean(w))
    if not np.isfinite(w_mean) or w_mean <= 0.0:
        return float("nan")

    log_ratio = float(np.log(w.max() / w_mean))
    if not np.isfinite(log_ratio) or log_ratio <= 0.0:
        return float("nan")

    result = float(np.log(len(w)) / log_ratio)
    if not np.isfinite(result) or result < 0.5 or result > 10.0:
        return float("nan")

    return result


def bootstrap_mean_ci(
    values: Iterable[float],
    *,
    level: float = 0.95,
    n_boot: int = 2000,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Return mean and percentile bootstrap confidence interval."""

    arr = np.asarray(list(values), dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan"), float("nan"), float("nan")
    if not 0.0 < level < 1.0:
        raise ValueError("level must lie between 0 and 1")
    rng = np.random.default_rng(seed)
    samples = rng.choice(arr, size=(n_boot, arr.size), replace=True).mean(axis=1)
    alpha = (1.0 - level) / 2.0
    lo, hi = np.quantile(samples, [alpha, 1.0 - alpha])
    return float(arr.mean()), float(lo), float(hi)
