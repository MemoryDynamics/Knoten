from __future__ import annotations

import pytest

from emergenz_knoten.knot_score import (
    best_residence_memory_times,
    score_against_control,
    threshold_score,
    voxel_stability_ratio,
)


def _diagnostics(*, radius: float, residences: list[float]) -> dict[str, object]:
    return {
        "mean_centered_radius": radius,
        "residence_by_voxel_size": {
            str(i): {"max_residence_memory_times": value}
            for i, value in enumerate(residences)
        },
    }


def test_best_residence_and_voxel_stability() -> None:
    diagnostics = _diagnostics(radius=2.0, residences=[10.0, 20.0, 40.0])

    assert best_residence_memory_times(diagnostics) == 40.0
    assert voxel_stability_ratio(diagnostics) == pytest.approx(0.25)


def test_threshold_score_uses_partial_and_pass_levels() -> None:
    assert threshold_score(None, partial_at=2.0, pass_at=3.0) == 0.0
    assert threshold_score(1.9, partial_at=2.0, pass_at=3.0) == 0.0
    assert threshold_score(2.0, partial_at=2.0, pass_at=3.0) == 0.5
    assert threshold_score(3.0, partial_at=2.0, pass_at=3.0) == 1.0


def test_score_against_control_combines_available_components() -> None:
    case = _diagnostics(radius=4.0, residences=[30.0, 60.0, 90.0])
    control = _diagnostics(radius=40.0, residences=[10.0, 20.0, 30.0])

    score = score_against_control(case, control)

    assert score["residence_gain"] == pytest.approx(3.0)
    assert score["compactness_gain"] == pytest.approx(10.0)
    assert score["voxel_stability"] == pytest.approx(1.0 / 3.0)
    assert score["score"] == pytest.approx(1.0)