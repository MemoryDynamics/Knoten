from __future__ import annotations

import pytest

from emergenz_knoten.knot_score import (
    best_residence_memory_times,
    memory_mean_radius,
    memory_roundness_value,
    memory_shape_dimension_value,
    occupancy_dimension_value,
    score_against_control,
    score_v0_4_against_control,
    shape_roundness_value,
    threshold_score,
    voxel_stability_ratio,
)


def _diagnostics(
    *,
    radius: float,
    residences: list[float],
    d_occ: float = 1.8,
    roundness: float | None = None,
    memory_radius: float | None = None,
    memory_roundness: float | None = None,
    memory_dimension: float | None = None,
) -> dict[str, object]:
    diagnostics: dict[str, object] = {
        "mean_centered_radius": radius,
        "occupancy_dimension": d_occ,
        "residence_by_voxel_size": {
            str(i): {"max_residence_memory_times": value}
            for i, value in enumerate(residences)
        },
    }
    if roundness is not None:
        diagnostics["sample_shape"] = {"axis_ratio_min_max": roundness}
    if (
        memory_radius is not None
        or memory_roundness is not None
        or memory_dimension is not None
    ):
        diagnostics["memory_cloud"] = {
            "shape": {
                "mean_radius": memory_radius,
                "axis_ratio_min_max": memory_roundness,
                "effective_dimension": memory_dimension,
            }
        }
    return diagnostics


def test_best_residence_and_voxel_stability() -> None:
    diagnostics = _diagnostics(radius=2.0, residences=[10.0, 20.0, 40.0])

    assert best_residence_memory_times(diagnostics) == 40.0
    assert voxel_stability_ratio(diagnostics) == pytest.approx(0.25)


def test_threshold_score_uses_partial_and_pass_levels() -> None:
    assert threshold_score(None, partial_at=2.0, pass_at=3.0) == 0.0
    assert threshold_score(1.9, partial_at=2.0, pass_at=3.0) == 0.0
    assert threshold_score(2.0, partial_at=2.0, pass_at=3.0) == 0.5
    assert threshold_score(3.0, partial_at=2.0, pass_at=3.0) == 1.0


def test_occupancy_dimension_prefers_valid_scaling_window() -> None:
    diagnostics = {
        "occupancy_dimension": 1.2,
        "occupancy": {
            "dimension": 1.4,
            "scaling_window": {
                "dimension": 2.1,
                "valid_scaling": True,
            },
        },
    }

    assert occupancy_dimension_value(diagnostics) == pytest.approx(2.1)


def test_shape_roundness_reads_new_sample_shape_when_available() -> None:
    diagnostics = _diagnostics(
        radius=2.0,
        residences=[10.0, 20.0, 40.0],
        roundness=0.42,
    )

    assert shape_roundness_value(diagnostics) == pytest.approx(0.42)


def test_memory_shape_helpers_read_memory_cloud_shape() -> None:
    diagnostics = _diagnostics(
        radius=2.0,
        residences=[10.0, 20.0, 40.0],
        memory_radius=0.2,
        memory_roundness=0.64,
        memory_dimension=2.7,
    )

    assert memory_mean_radius(diagnostics) == pytest.approx(0.2)
    assert memory_roundness_value(diagnostics) == pytest.approx(0.64)
    assert memory_shape_dimension_value(diagnostics) == pytest.approx(2.7)


def test_score_against_control_combines_available_components() -> None:
    case = _diagnostics(radius=4.0, residences=[30.0, 60.0, 90.0], d_occ=1.8)
    control = _diagnostics(radius=40.0, residences=[10.0, 20.0, 30.0], d_occ=0.8)

    score = score_against_control(case, control)

    assert score["residence_gain"] == pytest.approx(3.0)
    assert score["compactness_gain"] == pytest.approx(10.0)
    assert score["voxel_stability"] == pytest.approx(1.0 / 3.0)
    assert score["internal_dimension"] == pytest.approx(1.8)
    assert score["dimension_score"] == pytest.approx(1.0)
    assert score["score"] == pytest.approx(1.0)


def test_score_v0_4_adds_memory_cloud_components() -> None:
    case = _diagnostics(
        radius=4.0,
        residences=[30.0, 60.0, 90.0],
        d_occ=1.8,
        memory_radius=2.0,
        memory_roundness=0.6,
        memory_dimension=2.4,
    )
    control = _diagnostics(
        radius=40.0,
        residences=[10.0, 20.0, 30.0],
        d_occ=0.8,
        memory_radius=10.0,
        memory_roundness=0.3,
        memory_dimension=1.5,
    )

    score = score_v0_4_against_control(case, control)

    assert score["score_v0_3"] == pytest.approx(1.0)
    assert score["memory_compactness_gain"] == pytest.approx(5.0)
    assert score["memory_roundness_gain"] == pytest.approx(2.0)
    assert score["memory_dimension_gain"] == pytest.approx(1.6)
    assert score["memory_compactness_score"] == pytest.approx(1.0)
    assert score["memory_roundness_score"] == pytest.approx(1.0)
    assert score["memory_dimension_score"] == pytest.approx(1.0)
    assert score["score"] == pytest.approx(1.0)
