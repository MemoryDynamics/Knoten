"""Diagnostics for knot synchronization and external response modes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class LaggedCorrelationResult:
    lags: np.ndarray
    correlations: np.ndarray
    best_lag: int
    best_correlation: float


@dataclass(frozen=True)
class ResponseRankResult:
    rank: int
    singular_values: np.ndarray
    cumulative_energy: np.ndarray


def _as_series(values: Iterable[float] | Iterable[Iterable[float]]) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim == 1:
        arr = arr[:, None]
    if arr.ndim != 2:
        raise ValueError("series must be one- or two-dimensional")
    if arr.shape[0] < 2:
        raise ValueError("series must contain at least two samples")
    if not np.isfinite(arr).all():
        raise ValueError("series contains non-finite values")
    return arr


def _pearson_flat(a: np.ndarray, b: np.ndarray) -> float:
    av = a.reshape(-1)
    bv = b.reshape(-1)
    av = av - av.mean()
    bv = bv - bv.mean()
    denom = float(np.linalg.norm(av) * np.linalg.norm(bv))
    if denom == 0.0:
        return float("nan")
    return float(np.dot(av, bv) / denom)


def lagged_cross_correlation(
    driver: Iterable[float] | Iterable[Iterable[float]],
    responder: Iterable[float] | Iterable[Iterable[float]],
    *,
    max_lag: int,
) -> LaggedCorrelationResult:
    """Return lagged Pearson correlations between two observables.

    Positive lags mean the responder follows the driver by that many samples.
    """

    if max_lag < 0:
        raise ValueError("max_lag must be non-negative")
    a = _as_series(driver)
    b = _as_series(responder)
    if a.shape != b.shape:
        raise ValueError("driver and responder must have the same shape")
    if max_lag >= a.shape[0] - 1:
        raise ValueError("max_lag must be smaller than n_samples - 1")

    lags = np.arange(-max_lag, max_lag + 1, dtype=int)
    correlations = []
    for lag in lags:
        if lag < 0:
            aa = a[-lag:]
            bb = b[:lag]
        elif lag > 0:
            aa = a[:-lag]
            bb = b[lag:]
        else:
            aa = a
            bb = b
        correlations.append(_pearson_flat(aa, bb))

    corr_arr = np.asarray(correlations, dtype=float)
    finite = np.isfinite(corr_arr)
    if not finite.any():
        best_lag = 0
        best_corr = float("nan")
    else:
        best_idx = int(np.nanargmax(np.abs(corr_arr)))
        best_lag = int(lags[best_idx])
        best_corr = float(corr_arr[best_idx])
    return LaggedCorrelationResult(lags, corr_arr, best_lag, best_corr)


def phase_locking_value(
    phase_a: Iterable[float],
    phase_b: Iterable[float],
) -> float:
    """Return the phase-locking value for two phase series."""

    a = np.asarray(list(phase_a), dtype=float)
    b = np.asarray(list(phase_b), dtype=float)
    if a.shape != b.shape:
        raise ValueError("phase series must have the same shape")
    if a.ndim != 1 or a.size < 2:
        raise ValueError("phase series must be one-dimensional with at least two samples")
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("phase series contain non-finite values")
    return float(abs(np.mean(np.exp(1j * (a - b)))))


def response_rank(
    response_matrix: Iterable[Iterable[float]],
    *,
    energy_threshold: float = 0.95,
    rtol: float = 1e-12,
) -> ResponseRankResult:
    """Estimate effective rank from singular-value energy."""

    if not 0.0 < energy_threshold <= 1.0:
        raise ValueError("energy_threshold must satisfy 0 < value <= 1")
    matrix = np.asarray(response_matrix, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("response_matrix must be two-dimensional")
    if not np.isfinite(matrix).all():
        raise ValueError("response_matrix contains non-finite values")

    singular_values = np.linalg.svd(matrix, compute_uv=False)
    if singular_values.size == 0:
        return ResponseRankResult(0, singular_values, np.array([], dtype=float))
    cutoff = max(float(singular_values.max(initial=0.0)) * rtol, rtol)
    singular_values = singular_values[singular_values > cutoff]
    if singular_values.size == 0:
        return ResponseRankResult(0, singular_values, np.array([], dtype=float))
    energy = singular_values * singular_values
    cumulative = np.cumsum(energy) / float(np.sum(energy))
    rank = int(np.searchsorted(cumulative, energy_threshold, side="left") + 1)
    return ResponseRankResult(rank, singular_values, cumulative)


def shape_tensor(points: Iterable[Iterable[float]]) -> np.ndarray:
    """Return covariance-like shape tensor for a trajectory window."""

    pts = _as_series(points)
    centered = pts - pts.mean(axis=0, keepdims=True)
    return centered.T @ centered / max(len(centered), 1)


def radius_from_shape(tensor: Iterable[Iterable[float]]) -> float:
    """Return scalar radius proxy from a shape tensor."""

    arr = np.asarray(tensor, dtype=float)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError("tensor must be a square matrix")
    if not np.isfinite(arr).all():
        raise ValueError("tensor contains non-finite values")
    trace = float(np.trace(arr))
    if trace < 0.0:
        return float("nan")
    return float(np.sqrt(trace))
