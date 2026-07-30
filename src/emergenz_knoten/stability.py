"""Conservative stationarity gates for long-running knot simulations.

The gates distinguish convergence across simulation age from short-time
stationarity near the end of one run. Passing either gate is a measurement
eligibility result, not evidence for a physical particle or attractor.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def _positive_vector(name: str, values: Any, *, minimum_size: int) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if (
        array.ndim != 1
        or array.size < minimum_size
        or not np.isfinite(array).all()
        or np.any(array <= 0.0)
    ):
        raise ValueError(
            f"{name} must be a positive finite vector with at least "
            f"{minimum_size} entries"
        )
    return array


def _nonnegative_vector(name: str, values: Any, *, minimum_size: int) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if (
        array.ndim != 1
        or array.size < minimum_size
        or not np.isfinite(array).all()
        or np.any(array < 0.0)
    ):
        raise ValueError(
            f"{name} must be a non-negative finite vector with at least "
            f"{minimum_size} entries"
        )
    return array


def normalized_shape_eigenvalues(eigenvalues: Any) -> np.ndarray:
    """Normalize non-negative covariance eigenvalues checkpoint by checkpoint."""

    values = np.asarray(eigenvalues, dtype=float)
    if (
        values.ndim != 2
        or values.shape[0] < 1
        or values.shape[1] < 1
        or not np.isfinite(values).all()
        or np.any(values < 0.0)
    ):
        raise ValueError("eigenvalues must be a finite non-negative matrix")
    totals = np.sum(values, axis=1, keepdims=True)
    if np.any(totals <= 0.0):
        raise ValueError("each eigenvalue spectrum must have positive mass")
    return values / totals


def _total_variation_rows(values: np.ndarray, reference: np.ndarray) -> np.ndarray:
    return 0.5 * np.sum(np.abs(values - reference[None, :]), axis=1)


def checkpoint_stability_diagnostics(
    update_counts: Any,
    radii: Any,
    covariance_eigenvalues: Any,
    *,
    training_checkpoints: int = 4,
    radius_range_limit: float = 0.10,
    radius_cv_limit: float = 0.15,
    radius_trend_per_decade_limit: float = 0.05,
    spectrum_tv_limit: float = 0.10,
    minimum_training_span_decades: float = 1.0,
    minimum_holdout_factor: float = 3.0,
) -> dict[str, float | int | bool]:
    """Test age convergence on training checkpoints plus one later holdout.

    Only the last ``training_checkpoints + 1`` observations are used. The final
    observation is reserved as a holdout. Shape comparison uses normalized
    covariance spectra and is therefore invariant under rigid rotation.
    """

    if training_checkpoints < 3:
        raise ValueError("training_checkpoints must be at least three")
    required = training_checkpoints + 1
    updates = _positive_vector("update_counts", update_counts, minimum_size=required)
    radius = _positive_vector("radii", radii, minimum_size=required)
    spectra = normalized_shape_eigenvalues(covariance_eigenvalues)
    if radius.shape != updates.shape or spectra.shape[0] != updates.size:
        raise ValueError("updates, radii, and eigenvalue rows must align")
    if np.any(np.diff(updates) <= 0.0):
        raise ValueError("update_counts must be strictly increasing")
    limits = (
        radius_range_limit,
        radius_cv_limit,
        radius_trend_per_decade_limit,
        spectrum_tv_limit,
        minimum_training_span_decades,
    )
    if any(not math.isfinite(value) or value <= 0.0 for value in limits):
        raise ValueError("stability limits and training span must be positive")
    if not math.isfinite(minimum_holdout_factor) or minimum_holdout_factor <= 1.0:
        raise ValueError("minimum_holdout_factor must exceed one")

    selection = slice(updates.size - required, updates.size)
    selected_updates = updates[selection]
    selected_radius = radius[selection]
    selected_spectra = spectra[selection]
    train_updates = selected_updates[:-1]
    train_radius = selected_radius[:-1]
    train_spectra = selected_spectra[:-1]
    holdout_radius = float(selected_radius[-1])
    holdout_spectrum = selected_spectra[-1]

    radius_reference = float(np.median(train_radius))
    radius_relative_range = float(np.max(train_radius) / np.min(train_radius) - 1.0)
    radius_cv = float(np.std(train_radius) / np.mean(train_radius))
    log_slope = float(np.polyfit(np.log10(train_updates), np.log(train_radius), 1)[0])
    radius_trend_per_decade = float(np.expm1(abs(log_slope)))
    holdout_radius_change = abs(holdout_radius / radius_reference - 1.0)

    spectrum_reference = np.median(train_spectra, axis=0)
    spectrum_reference /= np.sum(spectrum_reference)
    training_spectrum_tv = _total_variation_rows(
        train_spectra,
        spectrum_reference,
    )
    training_spectrum_tv_max = float(np.max(training_spectrum_tv))
    holdout_spectrum_tv = float(
        0.5 * np.sum(np.abs(holdout_spectrum - spectrum_reference))
    )

    training_span_decades = float(np.log10(train_updates[-1] / train_updates[0]))
    holdout_factor = float(selected_updates[-1] / train_updates[-1])
    pass_flags = {
        "training_radius_range_pass": (radius_relative_range <= radius_range_limit),
        "training_radius_cv_pass": radius_cv <= radius_cv_limit,
        "training_radius_trend_pass": (
            radius_trend_per_decade <= radius_trend_per_decade_limit
        ),
        "training_shape_pass": training_spectrum_tv_max <= spectrum_tv_limit,
        "holdout_radius_pass": holdout_radius_change <= radius_range_limit,
        "holdout_shape_pass": holdout_spectrum_tv <= spectrum_tv_limit,
        "training_span_pass": (training_span_decades >= minimum_training_span_decades),
        "holdout_separation_pass": holdout_factor >= minimum_holdout_factor,
    }
    return {
        "training_checkpoint_count": int(training_checkpoints),
        "candidate_update": int(train_updates[-1]),
        "holdout_update": int(selected_updates[-1]),
        "training_span_decades": training_span_decades,
        "holdout_factor": holdout_factor,
        "training_radius_relative_range": radius_relative_range,
        "training_radius_cv": radius_cv,
        "training_radius_trend_per_decade": radius_trend_per_decade,
        "holdout_radius_relative_change": holdout_radius_change,
        "training_shape_spectrum_tv_max": training_spectrum_tv_max,
        "holdout_shape_spectrum_tv": holdout_spectrum_tv,
        "radius_range_limit": float(radius_range_limit),
        "radius_cv_limit": float(radius_cv_limit),
        "radius_trend_per_decade_limit": float(radius_trend_per_decade_limit),
        "spectrum_tv_limit": float(spectrum_tv_limit),
        "minimum_training_span_decades": float(minimum_training_span_decades),
        "minimum_holdout_factor": float(minimum_holdout_factor),
        **pass_flags,
        "checkpoint_stability_pass": bool(all(pass_flags.values())),
    }


def local_radius_stationarity_diagnostics(
    update_counts: Any,
    radii: Any,
    *,
    window_updates: int,
    training_windows: int = 4,
    minimum_samples_per_window: int = 20,
    radius_range_limit: float = 0.10,
    radius_cv_limit: float = 0.15,
) -> dict[str, float | int | bool | list[float]]:
    """Test trailing local radius stationarity in fixed-duration windows."""

    if window_updates < 1:
        raise ValueError("window_updates must be positive")
    if training_windows < 3:
        raise ValueError("training_windows must be at least three")
    if minimum_samples_per_window < 2:
        raise ValueError("minimum_samples_per_window must be at least two")
    if min(radius_range_limit, radius_cv_limit) <= 0.0:
        raise ValueError("radius limits must be positive")

    required_windows = training_windows + 1
    updates = _positive_vector(
        "update_counts",
        update_counts,
        minimum_size=required_windows * minimum_samples_per_window,
    )
    radius = _nonnegative_vector(
        "radii",
        radii,
        minimum_size=required_windows * minimum_samples_per_window,
    )
    if updates.shape != radius.shape or np.any(np.diff(updates) <= 0.0):
        raise ValueError("updates and radii must align with increasing updates")

    end = int(updates[-1])
    medians: list[float] = []
    cvs: list[float] = []
    sample_counts: list[int] = []
    for index in range(required_windows):
        lower = end - (required_windows - index) * window_updates
        upper = lower + window_updates
        mask = (updates > lower) & (updates <= upper)
        values = radius[mask]
        sample_counts.append(int(values.size))
        if values.size < minimum_samples_per_window:
            raise ValueError("each trailing window needs enough radius samples")
        if np.any(values <= 0.0):
            raise ValueError("radii in each trailing window must be positive")
        medians.append(float(np.median(values)))
        cvs.append(float(np.std(values) / np.mean(values)))

    training_medians = np.asarray(medians[:-1], dtype=float)
    training_reference = float(np.median(training_medians))
    training_range = float(np.max(training_medians) / np.min(training_medians) - 1.0)
    training_cv_max = float(np.max(cvs[:-1]))
    holdout_change = abs(medians[-1] / training_reference - 1.0)
    pass_flags = {
        "training_radius_range_pass": training_range <= radius_range_limit,
        "training_radius_cv_pass": training_cv_max <= radius_cv_limit,
        "holdout_radius_pass": holdout_change <= radius_range_limit,
    }
    return {
        "window_updates": int(window_updates),
        "training_window_count": int(training_windows),
        "holdout_window_count": 1,
        "window_median_radii": medians,
        "window_radius_cvs": cvs,
        "window_sample_counts": sample_counts,
        "training_radius_relative_range": training_range,
        "training_radius_cv_max": training_cv_max,
        "holdout_radius_relative_change": holdout_change,
        "radius_range_limit": float(radius_range_limit),
        "radius_cv_limit": float(radius_cv_limit),
        **pass_flags,
        "local_radius_stationarity_pass": bool(all(pass_flags.values())),
    }


def local_shape_stationarity_diagnostics(
    update_counts: Any,
    covariance_eigenvalues: Any,
    *,
    window_updates: int,
    training_windows: int = 4,
    minimum_samples_per_window: int = 20,
    spectrum_tv_limit: float = 0.10,
) -> dict[str, Any]:
    """Test trailing rotation-invariant shape stationarity in fixed windows."""

    if window_updates < 1:
        raise ValueError("window_updates must be positive")
    if training_windows < 3:
        raise ValueError("training_windows must be at least three")
    if minimum_samples_per_window < 2:
        raise ValueError("minimum_samples_per_window must be at least two")
    if not math.isfinite(spectrum_tv_limit) or spectrum_tv_limit <= 0.0:
        raise ValueError("spectrum_tv_limit must be positive")

    required_windows = training_windows + 1
    minimum_size = required_windows * minimum_samples_per_window
    updates = _positive_vector(
        "update_counts",
        update_counts,
        minimum_size=minimum_size,
    )
    spectra = normalized_shape_eigenvalues(covariance_eigenvalues)
    if (
        spectra.shape[0] != updates.size
        or updates.size < minimum_size
        or np.any(np.diff(updates) <= 0.0)
    ):
        raise ValueError(
            "updates and covariance eigenvalue rows must align with increasing updates"
        )

    end = int(updates[-1])
    medians: list[np.ndarray] = []
    within_window_q95: list[float] = []
    sample_counts: list[int] = []
    for index in range(required_windows):
        lower = end - (required_windows - index) * window_updates
        upper = lower + window_updates
        mask = (updates > lower) & (updates <= upper)
        values = spectra[mask]
        sample_counts.append(int(values.shape[0]))
        if values.shape[0] < minimum_samples_per_window:
            raise ValueError("each trailing window needs enough shape samples")
        median = np.median(values, axis=0)
        median /= np.sum(median)
        medians.append(median)
        within_window_q95.append(
            float(np.quantile(_total_variation_rows(values, median), 0.95))
        )

    training_medians = np.asarray(medians[:-1], dtype=float)
    training_reference = np.median(training_medians, axis=0)
    training_reference /= np.sum(training_reference)
    training_reference_tv_max = float(
        np.max(_total_variation_rows(training_medians, training_reference))
    )
    training_within_window_tv_q95_max = float(np.max(within_window_q95[:-1]))
    holdout_reference_tv = float(0.5 * np.sum(np.abs(medians[-1] - training_reference)))
    pass_flags = {
        "training_shape_reference_pass": (
            training_reference_tv_max <= spectrum_tv_limit
        ),
        "training_shape_within_window_pass": (
            training_within_window_tv_q95_max <= spectrum_tv_limit
        ),
        "holdout_shape_pass": holdout_reference_tv <= spectrum_tv_limit,
    }
    return {
        "window_updates": int(window_updates),
        "training_window_count": int(training_windows),
        "holdout_window_count": 1,
        "window_median_shape_spectra": [row.tolist() for row in medians],
        "window_shape_tv_q95": within_window_q95,
        "window_sample_counts": sample_counts,
        "training_shape_reference_tv_max": training_reference_tv_max,
        "training_shape_within_window_tv_q95_max": (training_within_window_tv_q95_max),
        "holdout_shape_reference_tv": holdout_reference_tv,
        "spectrum_tv_limit": float(spectrum_tv_limit),
        **pass_flags,
        "local_shape_stationarity_pass": bool(all(pass_flags.values())),
    }
