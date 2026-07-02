"""Scorecard helpers for metastable knot evidence."""

from __future__ import annotations

from collections.abc import Mapping
import math
from typing import Any


def _as_finite(value: Any) -> float | None:
    if value is None:
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def best_residence_memory_times(diagnostics: Mapping[str, Any]) -> float | None:
    """Return the largest max-residence value measured in memory times."""

    residence = diagnostics.get("residence_by_voxel_size")
    if not isinstance(residence, Mapping):
        return None
    values: list[float] = []
    for metrics in residence.values():
        if isinstance(metrics, Mapping):
            value = _as_finite(metrics.get("max_residence_memory_times"))
            if value is not None:
                values.append(value)
    return max(values) if values else None


def voxel_stability_ratio(diagnostics: Mapping[str, Any]) -> float | None:
    """Return min/max residence across voxel sizes.

    Values near one mean that the residence signal is similar across the tested
    voxel sizes. Values near zero indicate that the signal is dominated by one
    coarse or fine voxel choice.
    """

    residence = diagnostics.get("residence_by_voxel_size")
    if not isinstance(residence, Mapping):
        return None
    values: list[float] = []
    for metrics in residence.values():
        if isinstance(metrics, Mapping):
            value = _as_finite(metrics.get("max_residence_memory_times"))
            if value is not None and value > 0.0:
                values.append(value)
    if not values:
        return None
    high = max(values)
    return min(values) / high if high > 0.0 else None


def mean_centered_radius(diagnostics: Mapping[str, Any]) -> float | None:
    """Return the mean centered radius diagnostic when available."""

    value = _as_finite(diagnostics.get("mean_centered_radius"))
    return value if value is not None and value > 0.0 else None


def occupancy_dimension_value(diagnostics: Mapping[str, Any]) -> float | None:
    """Return the preferred internal occupancy dimension diagnostic.

    Newer long-run outputs contain an automatic scaling-window fit under
    ``occupancy.scaling_window``. When that window is marked valid, it is used.
    Older outputs only contain the historical top-level ``occupancy_dimension``;
    those remain valid fallback inputs for retrospective scorecards.
    """

    occupancy = _mapping(diagnostics.get("occupancy"))
    if occupancy is not None:
        window = _mapping(occupancy.get("scaling_window"))
        if window is not None and bool(window.get("valid_scaling")):
            value = _as_finite(window.get("dimension"))
            if value is not None and value > 0.0:
                return value
        value = _as_finite(occupancy.get("dimension"))
        if value is not None and value > 0.0:
            return value

    value = _as_finite(diagnostics.get("occupancy_dimension"))
    return value if value is not None and value > 0.0 else None


def shape_roundness_value(diagnostics: Mapping[str, Any]) -> float | None:
    """Return a sample-cloud axis ratio when newer diagnostics contain it."""

    sample_shape = _mapping(diagnostics.get("sample_shape"))
    if sample_shape is None:
        return None
    value = _as_finite(sample_shape.get("axis_ratio_min_max"))
    if value is None:
        return None
    return max(0.0, min(1.0, value))


def memory_shape_value(diagnostics: Mapping[str, Any], key: str) -> float | None:
    """Return one scalar from ``diagnostics.memory_cloud.shape``."""

    memory_cloud = _mapping(diagnostics.get("memory_cloud"))
    if memory_cloud is None:
        return None
    shape = _mapping(memory_cloud.get("shape"))
    if shape is None:
        return None
    value = _as_finite(shape.get(key))
    if value is None:
        return None
    if key == "axis_ratio_min_max":
        return max(0.0, min(1.0, value))
    return value if value > 0.0 else None


def memory_mean_radius(diagnostics: Mapping[str, Any]) -> float | None:
    """Return the mean radius of the weighted memory cloud."""

    return memory_shape_value(diagnostics, "mean_radius")


def memory_roundness_value(diagnostics: Mapping[str, Any]) -> float | None:
    """Return the min/max axis ratio of the weighted memory cloud."""

    return memory_shape_value(diagnostics, "axis_ratio_min_max")


def memory_shape_dimension_value(diagnostics: Mapping[str, Any]) -> float | None:
    """Return the covariance participation dimension of the memory cloud."""

    return memory_shape_value(diagnostics, "effective_dimension")


def _ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator <= 0.0:
        return None
    return numerator / denominator


def threshold_score(
    value: float | None,
    *,
    partial_at: float,
    pass_at: float,
) -> float:
    """Map a metric to 0, 0.5, or 1 with explicit thresholds."""

    if value is None or not math.isfinite(value):
        return 0.0
    if value >= pass_at:
        return 1.0
    if value >= partial_at:
        return 0.5
    return 0.0


def score_against_control(
    case_diagnostics: Mapping[str, Any],
    control_diagnostics: Mapping[str, Any],
    *,
    residence_partial_at: float = 2.0,
    residence_pass_at: float = 3.0,
    compactness_partial_at: float = 3.0,
    compactness_pass_at: float = 5.0,
    voxel_partial_at: float = 0.15,
    voxel_pass_at: float = 0.25,
    dimension_partial_at: float = 1.25,
    dimension_pass_at: float = 1.5,
) -> dict[str, float | None]:
    """Score one case against a matched negative control.

    The returned ``score`` averages four explicit components: residence gain
    over control, compactness gain over control, voxel stability, and internal
    occupancy dimension support. The dimension component deliberately does not
    target external three-dimensionality; it only penalizes collapsed or nearly
    one-dimensional internal support in single-knot diagnostics.
    """

    case_residence = best_residence_memory_times(case_diagnostics)
    control_residence = best_residence_memory_times(control_diagnostics)
    case_radius = mean_centered_radius(case_diagnostics)
    control_radius = mean_centered_radius(control_diagnostics)
    residence_gain = _ratio(case_residence, control_residence)
    compactness_gain = _ratio(control_radius, case_radius)
    voxel_stability = voxel_stability_ratio(case_diagnostics)
    internal_dimension = occupancy_dimension_value(case_diagnostics)
    shape_roundness = shape_roundness_value(case_diagnostics)

    residence_score = threshold_score(
        residence_gain,
        partial_at=residence_partial_at,
        pass_at=residence_pass_at,
    )
    compactness_score = threshold_score(
        compactness_gain,
        partial_at=compactness_partial_at,
        pass_at=compactness_pass_at,
    )
    voxel_score = threshold_score(
        voxel_stability,
        partial_at=voxel_partial_at,
        pass_at=voxel_pass_at,
    )
    dimension_score = threshold_score(
        internal_dimension,
        partial_at=dimension_partial_at,
        pass_at=dimension_pass_at,
    )
    score = (residence_score + compactness_score + voxel_score + dimension_score) / 4.0
    return {
        "score": score,
        "residence_score": residence_score,
        "compactness_score": compactness_score,
        "voxel_score": voxel_score,
        "dimension_score": dimension_score,
        "case_best_residence": case_residence,
        "control_best_residence": control_residence,
        "residence_gain": residence_gain,
        "case_mean_radius": case_radius,
        "control_mean_radius": control_radius,
        "compactness_gain": compactness_gain,
        "voxel_stability": voxel_stability,
        "internal_dimension": internal_dimension,
        "shape_roundness": shape_roundness,
    }


def score_v0_4_against_control(
    case_diagnostics: Mapping[str, Any],
    control_diagnostics: Mapping[str, Any],
    *,
    memory_compactness_partial_at: float = 2.0,
    memory_compactness_pass_at: float = 3.0,
    memory_roundness_partial_at: float = 1.2,
    memory_roundness_pass_at: float = 1.5,
    memory_dimension_partial_at: float = 1.15,
    memory_dimension_pass_at: float = 1.35,
) -> dict[str, float | None]:
    """Score v0.4 with memory-cloud shape support.

    This extends v0.3 by adding memory-cloud compactness, roundness gain, and
    shape-dimension gain against the matched ``eta_zero`` control. The raw
    sample path remains diagnostic output only; v0.4 treats the weighted memory
    cloud as the candidate knot shape observable.
    """

    score = score_against_control(case_diagnostics, control_diagnostics)
    case_memory_radius = memory_mean_radius(case_diagnostics)
    control_memory_radius = memory_mean_radius(control_diagnostics)
    case_memory_roundness = memory_roundness_value(case_diagnostics)
    control_memory_roundness = memory_roundness_value(control_diagnostics)
    case_memory_dimension = memory_shape_dimension_value(case_diagnostics)
    control_memory_dimension = memory_shape_dimension_value(control_diagnostics)

    memory_compactness_gain = _ratio(control_memory_radius, case_memory_radius)
    memory_roundness_gain = _ratio(case_memory_roundness, control_memory_roundness)
    memory_dimension_gain = _ratio(case_memory_dimension, control_memory_dimension)

    memory_compactness_score = threshold_score(
        memory_compactness_gain,
        partial_at=memory_compactness_partial_at,
        pass_at=memory_compactness_pass_at,
    )
    memory_roundness_score = threshold_score(
        memory_roundness_gain,
        partial_at=memory_roundness_partial_at,
        pass_at=memory_roundness_pass_at,
    )
    memory_dimension_score = threshold_score(
        memory_dimension_gain,
        partial_at=memory_dimension_partial_at,
        pass_at=memory_dimension_pass_at,
    )
    base_scores = [
        float(score["residence_score"] or 0.0),
        float(score["compactness_score"] or 0.0),
        float(score["voxel_score"] or 0.0),
        float(score["dimension_score"] or 0.0),
    ]
    memory_scores = [
        memory_compactness_score,
        memory_roundness_score,
        memory_dimension_score,
    ]
    score.update(
        {
            "score": sum(base_scores + memory_scores) / 7.0,
            "score_v0_3": score["score"],
            "memory_compactness_score": memory_compactness_score,
            "memory_roundness_score": memory_roundness_score,
            "memory_dimension_score": memory_dimension_score,
            "case_memory_radius": case_memory_radius,
            "control_memory_radius": control_memory_radius,
            "memory_compactness_gain": memory_compactness_gain,
            "case_memory_roundness": case_memory_roundness,
            "control_memory_roundness": control_memory_roundness,
            "memory_roundness_gain": memory_roundness_gain,
            "case_memory_dimension": case_memory_dimension,
            "control_memory_dimension": control_memory_dimension,
            "memory_dimension_gain": memory_dimension_gain,
        }
    )
    return score
