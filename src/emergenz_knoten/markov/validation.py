"""Validation diagnostics for finite transfer-operator estimates."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def critical_gamma(lambda_value: float) -> float:
    """Return the analytic critical coupling gamma_c(lambda)."""

    if not 0.0 < lambda_value < 1.0:
        raise ValueError("lambda_value must satisfy 0 < value < 1")
    return float(lambda_value * lambda_value / (1.0 - lambda_value))


def self_consistency_residual(
    velocity: float,
    *,
    gamma: float,
    lambda_value: float,
    k_max: int = 200,
) -> float:
    """Return the residual of the analytic ballistic self-consistency equation."""

    if not 0.0 < lambda_value < 1.0:
        raise ValueError("lambda_value must satisfy 0 < value < 1")
    if k_max < 1:
        raise ValueError("k_max must be positive")
    if velocity < 0.0:
        raise ValueError("velocity must be non-negative")

    k = np.arange(1, k_max + 1, dtype=float)
    weights = k * np.power(1.0 - lambda_value, k) * np.exp(-0.5 * (k * velocity) ** 2)
    return float(1.0 - gamma * np.sum(weights))


def mean_squared_displacement(
    positions: Iterable[Iterable[float]] | Iterable[float],
    *,
    max_lag: int,
) -> np.ndarray:
    """Return the mean squared displacement for a trajectory over lags."""

    arr = np.asarray(positions, dtype=float)
    if arr.ndim == 1:
        arr = arr[:, None]
    if arr.ndim != 2:
        raise ValueError("positions must be a 1D or 2D array")
    if max_lag < 0:
        raise ValueError("max_lag must be non-negative")
    if arr.shape[0] < 2:
        raise ValueError("at least two positions are required")

    n_points = arr.shape[0]
    out = np.empty(max_lag + 1, dtype=float)
    for lag in range(max_lag + 1):
        if lag >= n_points:
            out[lag] = np.nan
        elif lag == 0:
            out[lag] = 0.0
        else:
            deltas = arr[lag:] - arr[:-lag]
            out[lag] = float(np.mean(np.sum(deltas * deltas, axis=1)))
    return out


def ballistic_scaling_slope(
    positions: Iterable[Iterable[float]] | Iterable[float],
    *,
    fit_window: tuple[int, int],
) -> float:
    """Estimate the log-log scaling slope for MSD over a lag window."""

    if len(fit_window) != 2:
        raise ValueError("fit_window must contain start and stop indices")
    start, stop = fit_window
    if start < 1 or stop <= start:
        raise ValueError("fit_window must satisfy 1 <= start < stop")

    msd = mean_squared_displacement(positions, max_lag=stop)
    lags = np.arange(1, stop + 1, dtype=float)
    valid = np.isfinite(msd[1 : stop + 1]) & (msd[1 : stop + 1] > 0.0)
    valid &= (lags >= start) & (lags <= stop)
    if np.count_nonzero(valid) < 2:
        return float("nan")

    x = np.log(lags[valid])
    y = np.log(msd[1 : stop + 1][valid])
    coeff = np.polyfit(x, y, 1)
    return float(coeff[0])


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
