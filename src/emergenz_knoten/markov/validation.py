"""Validation diagnostics for finite transfer-operator estimates."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def vector_autocorrelation(
    values: Iterable[Iterable[float]] | Iterable[float],
    *,
    max_lag: int,
) -> np.ndarray:
    """Return normalized autocorrelation for scalar or vector observations."""

    arr = np.asarray(values, dtype=float)
    if arr.ndim == 1:
        arr = arr[:, None]
    if arr.ndim != 2:
        raise ValueError("values must be a 1D or 2D array")
    if max_lag < 0:
        raise ValueError("max_lag must be non-negative")
    if arr.shape[0] < 2:
        raise ValueError("at least two observations are required")

    centered = arr - arr.mean(axis=0, keepdims=True)
    denom = float(np.sum(centered * centered))
    out = np.empty(max_lag + 1, dtype=float)
    if denom <= 0.0:
        out.fill(np.nan)
        out[0] = 1.0
        return out
    for lag in range(max_lag + 1):
        if lag >= arr.shape[0]:
            out[lag] = np.nan
        elif lag == 0:
            out[lag] = 1.0
        else:
            out[lag] = float(np.sum(centered[:-lag] * centered[lag:]) / denom)
    return out


def implied_relaxation_rates(
    transition_matrix: Iterable[Iterable[float]],
    *,
    lag_time: float = 1.0,
    drop_stationary: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """Return eigenvalues and non-unit rates ``-log(|lambda|)/lag_time``.

    ``lag_time`` is a numeric lag denominator. In this package it is normally
    a sample lag or update-index lag, not a physical time variable.
    """

    if lag_time <= 0.0:
        raise ValueError("lag_time must be positive")
    matrix = np.asarray(transition_matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("transition_matrix must be square")
    if matrix.size == 0:
        return np.array([], dtype=complex), np.array([], dtype=float)

    eigenvalues = np.linalg.eigvals(matrix)
    order = np.argsort(-np.abs(eigenvalues))
    eigenvalues = eigenvalues[order]
    rates: list[float] = []
    for value in eigenvalues:
        modulus = float(abs(value))
        if drop_stationary and abs(modulus - 1.0) < 1e-8:
            continue
        if modulus <= 0.0:
            rates.append(float("inf"))
        else:
            rates.append(float(-np.log(min(modulus, 1.0)) / lag_time))
    return eigenvalues, np.asarray(rates, dtype=float)


def implied_timescales(
    eigenvalues: Iterable[complex],
    *,
    lag_time: float = 1.0,
    drop_stationary: bool = True,
) -> np.ndarray:
    """Return implied timescales ``-lag_time/log(|lambda|)`` for eigenvalues."""

    if lag_time <= 0.0:
        raise ValueError("lag_time must be positive")
    values = np.asarray(eigenvalues, dtype=complex)
    times: list[float] = []
    for value in values:
        modulus = float(abs(value))
        if drop_stationary and abs(modulus - 1.0) < 1e-8:
            continue
        if modulus <= 0.0:
            times.append(0.0)
        elif modulus >= 1.0:
            times.append(float("inf"))
        else:
            times.append(float(-lag_time / np.log(modulus)))
    return np.asarray(times, dtype=float)


def chapman_kolmogorov_error(
    transition_matrix: Iterable[Iterable[float]],
    multi_lag_matrix: Iterable[Iterable[float]],
    *,
    steps: int,
    ord: str | float = "fro",
) -> float:
    """Compare ``P^steps`` against an independently estimated multi-lag matrix."""

    if steps < 1:
        raise ValueError("steps must be positive")
    p = np.asarray(transition_matrix, dtype=float)
    q = np.asarray(multi_lag_matrix, dtype=float)
    if p.ndim != 2 or p.shape[0] != p.shape[1]:
        raise ValueError("transition_matrix must be square")
    if q.shape != p.shape:
        raise ValueError("multi_lag_matrix shape must match transition_matrix")
    predicted = np.linalg.matrix_power(p, steps)
    return float(np.linalg.norm(predicted - q, ord=ord))
