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
