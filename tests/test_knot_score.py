from __future__ import annotations

import pytest
import numpy as np


from emergenz_knoten.knot_score import (
    best_residence_memory_times,
    best_residence_updates,
    memory_mean_radius,
    memory_roundness_value,
    memory_shape_dimension_value,
    paired_shape_coherence_diagnostics,
    shape_stationarity_diagnostics,
    occupancy_dimension_value,
    score_against_control,
    score_v0_4_against_control,
    score_v0_5_against_control,
    score_v0_6_against_control,
    shape_roundness_value,
    threshold_score,
    voxel_stability_ratio,
)


def _diagnostics(
    *,
    radius: float,
    residences: list[float],
    residence_updates: list[float] | None = None,
    d_occ: float = 1.8,
    roundness: float | None = None,
    memory_radius: float | None = None,
    memory_roundness: float | None = None,
    memory_dimension: float | None = None,
) -> dict[str, object]:
    if residence_updates is None:
        residence_updates = residences
    diagnostics: dict[str, object] = {
        "mean_centered_radius": radius,
        "occupancy_dimension": d_occ,
        "residence_by_voxel_size": {
            str(i): {
                "max_residence_memory_times": value,
                "max_residence_updates": residence_updates[i],
            }
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
    assert best_residence_updates(diagnostics) == 40.0
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


def test_score_v0_5_uses_update_residence_and_gates_degenerate_memory() -> None:
    case = _diagnostics(
        radius=10.0,
        residences=[8000.0],
        residence_updates=[8000.0],
        d_occ=1.8,
        memory_radius=0.1,
    )
    control = _diagnostics(
        radius=10.0,
        residences=[80.0],
        residence_updates=[8000.0],
        d_occ=1.8,
        memory_radius=0.5,
        memory_roundness=0.3,
        memory_dimension=1.8,
    )

    old_score = score_v0_4_against_control(case, control)
    new_score = score_v0_5_against_control(case, control)

    assert old_score["residence_gain"] == pytest.approx(100.0)
    assert new_score["residence_gain"] == pytest.approx(1.0)
    assert new_score["memory_shape_valid"] is False
    assert new_score["memory_compactness_gain"] is None
    assert new_score["score"] == pytest.approx(2.0 / 7.0)


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


def test_shape_stationarity_allows_rotation_but_rejects_shape_drift() -> None:
    angles = np.linspace(0.0, np.pi / 2.0, 12)
    base = np.diag([0.8, 0.15, 0.05])
    tensors = []
    for angle in angles:
        rotation = np.array(
            [
                [np.cos(angle), -np.sin(angle), 0.0],
                [np.sin(angle), np.cos(angle), 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        tensors.append(rotation @ base @ rotation.T)
    radii = np.ones(len(tensors))

    stationary = shape_stationarity_diagnostics(radii, np.asarray(tensors))
    drifting = shape_stationarity_diagnostics(
        np.linspace(1.0, 2.0, len(tensors)),
        np.asarray(tensors),
    )

    assert stationary["stationary_shape_pass"]
    assert stationary["shape_spectrum_total_variation"] == pytest.approx(0.0)
    assert not drifting["stationary_shape_pass"]


def test_paired_shape_coherence_allows_rotation_and_bounded_breathing() -> None:
    control = np.repeat(np.diag([0.7, 0.2, 0.1])[None, :, :], 10, axis=0)
    rotation = np.array(
        [
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    case = np.asarray([1.2 * rotation @ tensor @ rotation.T for tensor in control])
    coherent = paired_shape_coherence_diagnostics(
        np.full(10, np.sqrt(1.2)),
        np.ones(10),
        case,
        control,
    )
    deformed = case.copy()
    deformed[:, :, :] = np.diag([0.98, 0.01, 0.01])
    incoherent = paired_shape_coherence_diagnostics(
        np.full(10, np.sqrt(1.2)),
        np.ones(10),
        deformed,
        control,
    )

    assert coherent["shape_bounded_coherent_pass"]
    assert coherent["shape_spectrum_distance_median"] == pytest.approx(0.0)
    assert not incoherent["shape_coherent_pass"]


def test_score_v0_6_requires_stationary_shape_eligibility() -> None:
    case = _diagnostics(
        radius=4.0,
        residences=[30.0, 60.0, 90.0],
        residence_updates=[30.0, 60.0, 90.0],
        memory_radius=2.0,
        memory_roundness=0.6,
        memory_dimension=2.4,
    )
    control = _diagnostics(
        radius=40.0,
        residences=[10.0, 20.0, 30.0],
        residence_updates=[10.0, 20.0, 30.0],
        memory_radius=10.0,
        memory_roundness=0.3,
        memory_dimension=1.5,
    )

    eligible = score_v0_6_against_control(
        case,
        control,
        stationarity_diagnostics={"stationary_shape_pass": True},
    )
    ineligible = score_v0_6_against_control(
        case,
        control,
        stationarity_diagnostics={"stationary_shape_pass": False},
    )

    assert eligible["eligible_knot_pass"]
    assert eligible["score"] == pytest.approx(1.0)
    assert not ineligible["eligible_knot_pass"]
    assert ineligible["score"] == pytest.approx(7.0 / 8.0)
