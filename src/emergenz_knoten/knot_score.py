"""Scorecard helpers for metastable knot evidence."""

from __future__ import annotations

from collections.abc import Mapping
import math
from typing import Any
import numpy as np


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


def _residence_values(
    diagnostics: Mapping[str, Any],
    *,
    residence_field: str,
) -> list[float]:
    residence = diagnostics.get("residence_by_voxel_size")
    if not isinstance(residence, Mapping):
        return []
    values: list[float] = []
    for metrics in residence.values():
        if isinstance(metrics, Mapping):
            value = _as_finite(metrics.get(residence_field))
            if value is not None:
                values.append(value)
    return values


def best_residence_value(
    diagnostics: Mapping[str, Any],
    *,
    residence_field: str = "max_residence_memory_times",
) -> float | None:
    """Return the largest max-residence value for one residence field."""

    values = _residence_values(diagnostics, residence_field=residence_field)
    return max(values) if values else None


def best_residence_memory_times(diagnostics: Mapping[str, Any]) -> float | None:
    """Return the largest max-residence value measured in memory times."""

    return best_residence_value(
        diagnostics,
        residence_field="max_residence_memory_times",
    )


def best_residence_updates(diagnostics: Mapping[str, Any]) -> float | None:
    """Return the largest max-residence value measured in raw updates."""

    return best_residence_value(
        diagnostics,
        residence_field="max_residence_updates",
    )


def voxel_stability_ratio(
    diagnostics: Mapping[str, Any],
    *,
    residence_field: str = "max_residence_memory_times",
) -> float | None:
    """Return min/max residence across voxel sizes.

    Values near one mean that the residence signal is similar across the tested
    voxel sizes. Values near zero indicate that the signal is dominated by one
    coarse or fine voxel choice.
    """

    values = [
        value
        for value in _residence_values(diagnostics, residence_field=residence_field)
        if value > 0.0
    ]
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
    residence_field: str = "max_residence_memory_times",
) -> dict[str, float | None]:
    """Score one case against a matched negative control.

    The returned ``score`` averages four explicit components: residence gain
    over control, compactness gain over control, voxel stability, and internal
    occupancy dimension support. The dimension component deliberately does not
    target external three-dimensionality; it only penalizes collapsed or nearly
    one-dimensional internal support in single-knot diagnostics.
    """

    case_residence = best_residence_value(
        case_diagnostics, residence_field=residence_field
    )
    control_residence = best_residence_value(
        control_diagnostics, residence_field=residence_field
    )
    case_radius = mean_centered_radius(case_diagnostics)
    control_radius = mean_centered_radius(control_diagnostics)
    residence_gain = _ratio(case_residence, control_residence)
    compactness_gain = _ratio(control_radius, case_radius)
    voxel_stability = voxel_stability_ratio(
        case_diagnostics, residence_field=residence_field
    )
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
        "residence_field": residence_field,
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
    residence_field: str = "max_residence_memory_times",
) -> dict[str, float | None]:
    """Score v0.4 with memory-cloud shape support.

    This extends v0.3 by adding memory-cloud compactness, roundness gain, and
    shape-dimension gain against the matched ``eta_zero`` control. The raw
    sample path remains diagnostic output only; v0.4 treats the weighted memory
    cloud as the candidate knot shape observable.
    """

    score = score_against_control(
        case_diagnostics,
        control_diagnostics,
        residence_field=residence_field,
    )
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


def score_v0_5_against_control(
    case_diagnostics: Mapping[str, Any],
    control_diagnostics: Mapping[str, Any],
) -> dict[str, float | None]:
    """Score v0.5 with cross-alpha-safe residence and memory-shape gating.

    v0.5 is meant for comparison sets that include different memory decay
    rates. It compares residence in raw update counts rather than in
    ``alpha^{-1}`` units and only awards memory compactness when the case has a
    nondegenerate memory cloud with both roundness and dimension diagnostics.
    """

    score = score_v0_4_against_control(
        case_diagnostics,
        control_diagnostics,
        residence_field="max_residence_updates",
    )
    memory_shape_valid = (
        score["case_memory_roundness"] is not None
        and score["case_memory_dimension"] is not None
    )
    if not memory_shape_valid:
        score["memory_compactness_gain"] = None
        score["memory_compactness_score"] = 0.0

    components = [
        float(score["residence_score"] or 0.0),
        float(score["compactness_score"] or 0.0),
        float(score["voxel_score"] or 0.0),
        float(score["dimension_score"] or 0.0),
        float(score["memory_compactness_score"] or 0.0),
        float(score["memory_roundness_score"] or 0.0),
        float(score["memory_dimension_score"] or 0.0),
    ]
    score["score"] = sum(components) / 7.0
    score["memory_shape_valid"] = memory_shape_valid
    return score


def normalized_shape_spectra(shape_tensors: Any) -> np.ndarray:
    """Return rotation-invariant, trace-normalized shape eigenvalues."""

    tensors = np.asarray(shape_tensors, dtype=float)
    if (
        tensors.ndim != 3
        or tensors.shape[1] != tensors.shape[2]
        or tensors.shape[0] < 1
        or not np.isfinite(tensors).all()
    ):
        raise ValueError("shape_tensors must be finite with shape (samples, dim, dim)")
    eigenvalues = np.linalg.eigvalsh(tensors)
    eigenvalues = np.maximum(eigenvalues, 0.0)
    traces = np.sum(eigenvalues, axis=1, keepdims=True)
    if np.any(traces <= 0.0):
        raise ValueError("shape tensors must have positive trace")
    return eigenvalues / traces


def shape_stationarity_diagnostics(
    radii: Any,
    shape_tensors: Any,
    *,
    radius_drift_limit: float = 0.10,
    radius_cv_limit: float = 0.15,
    spectrum_drift_limit: float = 0.10,
) -> dict[str, float | bool]:
    """Assess whether a pre-interaction shape trace is statistically bounded.

    The first and second halves are compared. Eigenvalue spectra make the test
    invariant under rigid rotations, so coherent orientation dynamics are not
    mistaken for shape loss.
    """

    radius = np.asarray(radii, dtype=float)
    spectra = normalized_shape_spectra(shape_tensors)
    if (
        radius.ndim != 1
        or radius.shape[0] != spectra.shape[0]
        or radius.size < 4
        or not np.isfinite(radius).all()
        or np.any(radius <= 0.0)
    ):
        raise ValueError("radii must be positive and match at least four shape samples")
    if min(radius_drift_limit, radius_cv_limit, spectrum_drift_limit) <= 0.0:
        raise ValueError("stationarity limits must be positive")

    midpoint = radius.size // 2
    early_radius = float(np.median(radius[:midpoint]))
    late_radius = float(np.median(radius[midpoint:]))
    radius_relative_drift = abs(late_radius / early_radius - 1.0)
    radius_cv = float(np.std(radius) / np.mean(radius))
    early_spectrum = np.median(spectra[:midpoint], axis=0)
    late_spectrum = np.median(spectra[midpoint:], axis=0)
    spectrum_total_variation = float(
        0.5 * np.sum(np.abs(late_spectrum - early_spectrum))
    )
    stationarity_pass = bool(
        radius_relative_drift <= radius_drift_limit
        and radius_cv <= radius_cv_limit
        and spectrum_total_variation <= spectrum_drift_limit
    )
    return {
        "radius_relative_drift": radius_relative_drift,
        "radius_coefficient_of_variation": radius_cv,
        "shape_spectrum_total_variation": spectrum_total_variation,
        "radius_drift_limit": radius_drift_limit,
        "radius_cv_limit": radius_cv_limit,
        "spectrum_drift_limit": spectrum_drift_limit,
        "stationary_shape_pass": stationarity_pass,
    }


def paired_shape_coherence_diagnostics(
    case_radii: Any,
    control_radii: Any,
    case_shape_tensors: Any,
    control_shape_tensors: Any,
    *,
    radius_factor_limit: float = 2.0,
    spectrum_median_limit: float = 0.10,
    spectrum_q95_limit: float = 0.25,
) -> dict[str, float | bool]:
    """Compare driven and paired-control shapes without demanding rigidity."""

    case_radius = np.asarray(case_radii, dtype=float)
    control_radius = np.asarray(control_radii, dtype=float)
    case_spectra = normalized_shape_spectra(case_shape_tensors)
    control_spectra = normalized_shape_spectra(control_shape_tensors)
    if (
        case_radius.ndim != 1
        or case_radius.shape != control_radius.shape
        or case_radius.shape[0] != case_spectra.shape[0]
        or case_spectra.shape != control_spectra.shape
        or not np.isfinite(case_radius).all()
        or not np.isfinite(control_radius).all()
        or np.any(case_radius <= 0.0)
        or np.any(control_radius <= 0.0)
    ):
        raise ValueError("paired radii and shape tensors must be finite and compatible")
    if radius_factor_limit <= 1.0:
        raise ValueError("radius_factor_limit must exceed one")
    if min(spectrum_median_limit, spectrum_q95_limit) <= 0.0:
        raise ValueError("spectrum limits must be positive")

    radius_ratio = case_radius / control_radius
    max_radius_factor = float(
        np.max(np.maximum(radius_ratio, np.reciprocal(radius_ratio)))
    )
    spectrum_distance = 0.5 * np.sum(
        np.abs(case_spectra - control_spectra),
        axis=1,
    )
    spectrum_median = float(np.median(spectrum_distance))
    spectrum_q95 = float(np.quantile(spectrum_distance, 0.95))
    bounded_pass = bool(max_radius_factor <= radius_factor_limit)
    coherent_pass = bool(
        spectrum_median <= spectrum_median_limit and spectrum_q95 <= spectrum_q95_limit
    )
    return {
        "max_radius_factor": max_radius_factor,
        "shape_spectrum_distance_median": spectrum_median,
        "shape_spectrum_distance_q95": spectrum_q95,
        "radius_factor_limit": radius_factor_limit,
        "spectrum_median_limit": spectrum_median_limit,
        "spectrum_q95_limit": spectrum_q95_limit,
        "shape_bounded_pass": bounded_pass,
        "shape_coherent_pass": coherent_pass,
        "shape_bounded_coherent_pass": bounded_pass and coherent_pass,
    }


def score_v0_6_against_control(
    case_diagnostics: Mapping[str, Any],
    control_diagnostics: Mapping[str, Any],
    *,
    stationarity_diagnostics: Mapping[str, Any],
) -> dict[str, Any]:
    """KnotScore v0.6: v0.5 evidence plus checkpoint eligibility.

    Stationarity is an eligibility gate, not evidence of interaction response.
    The numerical score retains the seven v0.5 components and adds a binary
    stationarity component; consumers must also inspect eligible_knot_pass.
    """

    score: dict[str, Any] = score_v0_5_against_control(
        case_diagnostics,
        control_diagnostics,
    )
    score_v0_5 = float(score["score"])
    stationary = bool(stationarity_diagnostics.get("stationary_shape_pass", False))
    score["score_v0_5"] = score_v0_5
    score["stationarity_score"] = 1.0 if stationary else 0.0
    score["score"] = (7.0 * score_v0_5 + score["stationarity_score"]) / 8.0
    score["stationary_shape_pass"] = stationary
    score["eligible_knot_pass"] = bool(stationary and score["memory_shape_valid"])
    return score
