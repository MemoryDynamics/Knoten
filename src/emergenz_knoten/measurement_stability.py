"""Convergence gates for cumulative, estimator-dependent observables."""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def occupancy_measurement_convergence_diagnostics(
    update_counts: Any,
    dimensions: Any,
    valid_scaling: Any,
    sampling_intervals: Any,
    estimator_labels: Any,
    *,
    training_checkpoints: int = 4,
    dimension_range_limit: float = 0.10,
    dimension_trend_per_decade_limit: float = 0.05,
    holdout_change_limit: float = 0.10,
    minimum_training_span_decades: float = 1.0,
    minimum_holdout_factor: float = 3.0,
) -> dict[str, Any]:
    """Test convergence of an occupancy-dimension measurement.

    This gate is deliberately separate from radius/shape stationarity.
    Occupancy dimensions are cumulative estimators and are only comparable
    when cadence and estimator implementation remain fixed. Invalid automatic
    scaling windows make the gate non-evaluable rather than silently passing.
    """

    if training_checkpoints < 3:
        raise ValueError("training_checkpoints must be at least three")
    required = training_checkpoints + 1
    updates = np.asarray(update_counts, dtype=float)
    values = np.asarray(dimensions, dtype=float)
    valid = np.asarray(valid_scaling, dtype=bool)
    intervals = np.asarray(sampling_intervals, dtype=float)
    labels = np.asarray(estimator_labels, dtype=str)
    arrays = (updates, values, valid, intervals, labels)
    if any(array.ndim != 1 or array.size < required for array in arrays):
        raise ValueError("all inputs must be aligned vectors with enough checkpoints")
    if any(array.shape != updates.shape for array in arrays[1:]):
        raise ValueError("all measurement-convergence inputs must align")
    if (
        not np.isfinite(updates).all()
        or np.any(updates <= 0.0)
        or np.any(np.diff(updates) <= 0.0)
    ):
        raise ValueError("update_counts must be positive and strictly increasing")
    if not np.isfinite(intervals).all() or np.any(intervals <= 0.0):
        raise ValueError("sampling_intervals must be positive and finite")
    limits = (
        dimension_range_limit,
        dimension_trend_per_decade_limit,
        holdout_change_limit,
        minimum_training_span_decades,
    )
    if any(not math.isfinite(value) or value <= 0.0 for value in limits):
        raise ValueError("convergence limits and training span must be positive")
    if not math.isfinite(minimum_holdout_factor) or minimum_holdout_factor <= 1.0:
        raise ValueError("minimum_holdout_factor must exceed one")

    selection = slice(updates.size - required, updates.size)
    selected_updates = updates[selection]
    selected_values = values[selection]
    selected_valid = valid[selection]
    selected_intervals = intervals[selection]
    selected_labels = labels[selection]
    finite_positive = np.isfinite(selected_values) & (selected_values > 0.0)
    fit_validity_pass = bool(np.all(selected_valid & finite_positive))
    sampling_cadence_pass = bool(np.all(selected_intervals == selected_intervals[0]))
    estimator_identity_pass = bool(np.all(selected_labels == selected_labels[0]))

    train_updates = selected_updates[:-1]
    training_span_decades = float(np.log10(train_updates[-1] / train_updates[0]))
    holdout_factor = float(selected_updates[-1] / train_updates[-1])
    training_span_pass = training_span_decades >= minimum_training_span_decades
    holdout_separation_pass = holdout_factor >= minimum_holdout_factor

    dimension_relative_range: float | None = None
    dimension_trend_per_decade: float | None = None
    holdout_relative_change: float | None = None
    if fit_validity_pass:
        train_values = selected_values[:-1]
        reference = float(np.median(train_values))
        dimension_relative_range = float(
            np.max(train_values) / np.min(train_values) - 1.0
        )
        log_slope = float(
            np.polyfit(np.log10(train_updates), np.log(train_values), 1)[0]
        )
        dimension_trend_per_decade = float(np.expm1(abs(log_slope)))
        holdout_relative_change = abs(float(selected_values[-1]) / reference - 1.0)

    range_pass = bool(
        dimension_relative_range is not None
        and dimension_relative_range <= dimension_range_limit
    )
    trend_pass = bool(
        dimension_trend_per_decade is not None
        and dimension_trend_per_decade <= dimension_trend_per_decade_limit
    )
    holdout_pass = bool(
        holdout_relative_change is not None
        and holdout_relative_change <= holdout_change_limit
    )
    protocol_flags = {
        "fit_validity_pass": fit_validity_pass,
        "sampling_cadence_pass": sampling_cadence_pass,
        "estimator_identity_pass": estimator_identity_pass,
        "training_span_pass": bool(training_span_pass),
        "holdout_separation_pass": bool(holdout_separation_pass),
    }
    convergence_flags = {
        "training_dimension_range_pass": range_pass,
        "training_dimension_trend_pass": trend_pass,
        "holdout_dimension_pass": holdout_pass,
    }
    evaluable = bool(all(protocol_flags.values()))
    return {
        "training_checkpoint_count": int(training_checkpoints),
        "candidate_update": int(train_updates[-1]),
        "holdout_update": int(selected_updates[-1]),
        "training_span_decades": training_span_decades,
        "holdout_factor": holdout_factor,
        "training_dimension_relative_range": dimension_relative_range,
        "training_dimension_trend_per_decade": dimension_trend_per_decade,
        "holdout_dimension_relative_change": holdout_relative_change,
        "dimension_range_limit": float(dimension_range_limit),
        "dimension_trend_per_decade_limit": float(dimension_trend_per_decade_limit),
        "holdout_change_limit": float(holdout_change_limit),
        "minimum_training_span_decades": float(minimum_training_span_decades),
        "minimum_holdout_factor": float(minimum_holdout_factor),
        "selected_sampling_intervals": selected_intervals.tolist(),
        "selected_estimator_labels": selected_labels.tolist(),
        "selected_valid_scaling": selected_valid.tolist(),
        **protocol_flags,
        **convergence_flags,
        "measurement_convergence_evaluable": evaluable,
        "occupancy_measurement_convergence_pass": bool(
            evaluable and all(convergence_flags.values())
        ),
    }
