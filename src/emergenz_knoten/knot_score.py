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
) -> dict[str, float | None]:
    """Score one case against a matched negative control.

    The returned ``score`` is a transparent scorecard average of three available
    components: residence gain over control, compactness gain over control, and
    voxel stability. Center/shape stability is intentionally not included here
    because the current archived long-run JSON files do not contain trajectory
    samples.
    """

    case_residence = best_residence_memory_times(case_diagnostics)
    control_residence = best_residence_memory_times(control_diagnostics)
    case_radius = mean_centered_radius(case_diagnostics)
    control_radius = mean_centered_radius(control_diagnostics)
    residence_gain = _ratio(case_residence, control_residence)
    compactness_gain = _ratio(control_radius, case_radius)
    voxel_stability = voxel_stability_ratio(case_diagnostics)

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
    score = (residence_score + compactness_score + voxel_score) / 3.0
    return {
        "score": score,
        "residence_score": residence_score,
        "compactness_score": compactness_score,
        "voxel_score": voxel_score,
        "case_best_residence": case_residence,
        "control_best_residence": control_residence,
        "residence_gain": residence_gain,
        "case_mean_radius": case_radius,
        "control_mean_radius": control_radius,
        "compactness_gain": compactness_gain,
        "voxel_stability": voxel_stability,
    }