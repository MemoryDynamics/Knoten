"""Cross-seed linear feature-closure and lag-normalized mode diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class ClosureScores:
    """Leave-one-series-out prediction scores for one lag."""

    lag: int
    n_series: int
    n_pairs: int
    ar_r2_median: float
    persistence_r2_median: float
    shuffled_r2_median: float
    ar_minus_persistence: float
    ar_minus_shuffled: float
    closure_lift: float
    ar_r2_by_series: tuple[float, ...]


@dataclass(frozen=True)
class ARSpectrum:
    """Linear AR map and its lag-normalized eigenmodes."""

    lag: int
    lag_updates: int
    matrix: np.ndarray
    eigenvalues: np.ndarray
    rates_per_update: np.ndarray
    angular_frequencies_per_update: np.ndarray
    residual_rms: float
    n_pairs: int


def _lagged_xy(series: Sequence[np.ndarray], lag: int) -> tuple[np.ndarray, np.ndarray]:
    x_parts = [np.asarray(values, dtype=float)[:-lag] for values in series]
    y_parts = [np.asarray(values, dtype=float)[lag:] for values in series]
    return np.concatenate(x_parts, axis=0), np.concatenate(y_parts, axis=0)


def _fit_ridge(x: np.ndarray, y: np.ndarray, ridge: float) -> np.ndarray:
    if ridge == 0.0:
        return np.linalg.lstsq(x, y, rcond=None)[0]
    gram = x.T @ x
    return np.linalg.solve(gram + ridge * np.eye(gram.shape[0]), x.T @ y)


def _r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    residual = y_true - y_pred
    centered = y_true - y_true.mean(axis=0, keepdims=True)
    sst = float(np.sum(centered * centered))
    if sst <= 0.0:
        return float("nan")
    return float(1.0 - np.sum(residual * residual) / sst)


def _training_standardization(
    train: Sequence[np.ndarray],
    test: np.ndarray,
) -> tuple[list[np.ndarray], np.ndarray]:
    pooled = np.concatenate([np.asarray(values, dtype=float) for values in train])
    mean = pooled.mean(axis=0)
    scale = pooled.std(axis=0)
    scale = np.where(scale > 1e-12, scale, 1.0)
    return (
        [(np.asarray(values, dtype=float) - mean) / scale for values in train],
        (np.asarray(test, dtype=float) - mean) / scale,
    )


def leave_one_series_out_closure(
    series: Sequence[np.ndarray],
    *,
    lag: int,
    ridge: float = 1e-6,
    shuffle_repeats: int = 3,
    random_seed: int = 20260719,
) -> ClosureScores:
    """Compare cross-series AR prediction with persistence and shuffled futures."""

    values = [np.asarray(item, dtype=float) for item in series]
    if len(values) < 2:
        raise ValueError("at least two series are required")
    if lag < 1 or not math.isfinite(ridge) or ridge < 0.0 or shuffle_repeats < 1:
        raise ValueError("lag and shuffle_repeats must be positive; ridge non-negative")
    feature_dim = values[0].shape[1] if values[0].ndim == 2 else -1
    if (
        feature_dim < 1
        or any(item.ndim != 2 or item.shape[1] != feature_dim for item in values)
        or any(item.shape[0] <= lag + 1 for item in values)
        or any(not np.isfinite(item).all() for item in values)
    ):
        raise ValueError("series must be compatible finite 2D arrays longer than lag")

    rng = np.random.default_rng(random_seed)
    ar_scores: list[float] = []
    persistence_scores: list[float] = []
    shuffle_scores: list[float] = []
    n_pairs = 0
    for holdout_index, raw_test in enumerate(values):
        raw_train = [
            item for index, item in enumerate(values) if index != holdout_index
        ]
        train, test = _training_standardization(raw_train, raw_test)
        x_train, y_train = _lagged_xy(train, lag)
        x_test, y_test = test[:-lag], test[lag:]
        coefficient = _fit_ridge(x_train, y_train, ridge)
        ar_scores.append(_r2(y_test, x_test @ coefficient))
        persistence_scores.append(_r2(y_test, x_test))
        n_pairs += int(x_test.shape[0])
        for _ in range(shuffle_repeats):
            shuffled = y_train[rng.permutation(y_train.shape[0])]
            shuffled_coefficient = _fit_ridge(x_train, shuffled, ridge)
            shuffle_scores.append(_r2(y_test, x_test @ shuffled_coefficient))

    ar_median = float(np.nanmedian(ar_scores))
    persistence_median = float(np.nanmedian(persistence_scores))
    shuffled_median = float(np.nanmedian(shuffle_scores))
    ar_minus_persistence = ar_median - persistence_median
    ar_minus_shuffled = ar_median - shuffled_median
    return ClosureScores(
        lag=int(lag),
        n_series=len(values),
        n_pairs=n_pairs,
        ar_r2_median=ar_median,
        persistence_r2_median=persistence_median,
        shuffled_r2_median=shuffled_median,
        ar_minus_persistence=ar_minus_persistence,
        ar_minus_shuffled=ar_minus_shuffled,
        closure_lift=min(ar_median, ar_minus_persistence, ar_minus_shuffled),
        ar_r2_by_series=tuple(float(value) for value in ar_scores),
    )


def fit_ar_spectrum(
    series: Sequence[np.ndarray],
    *,
    lag: int,
    lag_updates: int,
    ridge: float = 1e-6,
) -> ARSpectrum:
    """Fit one standardized AR map and normalize its modes by update lag."""

    values = [np.asarray(item, dtype=float) for item in series]
    if (
        not values
        or lag < 1
        or lag_updates < 1
        or not math.isfinite(ridge)
        or ridge < 0.0
    ):
        raise ValueError("series, lag, and lag_updates are required")
    feature_dim = values[0].shape[1] if values[0].ndim == 2 else -1
    if (
        feature_dim < 1
        or any(item.ndim != 2 or item.shape[1] != feature_dim for item in values)
        or any(item.shape[0] <= lag + 1 for item in values)
        or any(not np.isfinite(item).all() for item in values)
    ):
        raise ValueError("series must be compatible finite 2D arrays longer than lag")
    pooled = np.concatenate(values, axis=0)
    mean = pooled.mean(axis=0)
    scale = pooled.std(axis=0)
    scale = np.where(scale > 1e-12, scale, 1.0)
    standardized = [(item - mean) / scale for item in values]
    x, y = _lagged_xy(standardized, lag)
    coefficient = _fit_ridge(x, y, ridge)
    residual = y - x @ coefficient
    eigenvalues = np.linalg.eigvals(coefficient)
    modulus = np.abs(eigenvalues)
    rates = np.full(modulus.shape, np.inf, dtype=float)
    positive = modulus > 0.0
    rates[positive] = -np.log(modulus[positive]) / float(lag_updates)
    frequencies = np.angle(eigenvalues) / float(lag_updates)
    order = np.argsort(modulus)[::-1]
    return ARSpectrum(
        lag=int(lag),
        lag_updates=int(lag_updates),
        matrix=np.asarray(coefficient, dtype=float),
        eigenvalues=np.asarray(eigenvalues[order], dtype=np.complex128),
        rates_per_update=np.asarray(rates[order], dtype=float),
        angular_frequencies_per_update=np.asarray(
            frequencies[order],
            dtype=float,
        ),
        residual_rms=float(np.sqrt(np.mean(residual * residual))),
        n_pairs=int(x.shape[0]),
    )


def analytic_field_mode_multiplier(
    config_lambda: float,
    diffusion_per_update: float,
    wavenumber: float,
    lag_updates: int,
) -> float:
    """Field-only multiplier expected from forgetting plus heat diffusion."""

    if (
        not 0.0 < config_lambda <= 1.0
        or not math.isfinite(config_lambda)
        or diffusion_per_update < 0.0
        or not math.isfinite(diffusion_per_update)
        or lag_updates < 1
        or not math.isfinite(wavenumber)
    ):
        raise ValueError("invalid field-mode parameters")
    one_step = (1.0 - config_lambda) * math.exp(
        -diffusion_per_update * wavenumber**2
    )
    return float(one_step**lag_updates)
