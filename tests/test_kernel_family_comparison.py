from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "current" / "kernels"))
sys.path.insert(0, str(ROOT / "experiments" / "current" / "dynamics"))
sys.path.insert(0, str(ROOT / "src"))

import kernel_family_comparison as comparison  # noqa: E402


def test_q3_effective_amplitude_mapping() -> None:
    effective = comparison.effective_attractive_amplitude(
        amplitude_att=35.0,
        amplitude_rep=1.0,
        sigma_rep=1.0,
        sigma_att=3.0,
    )
    restored = comparison.two_scale_amplitude_for_effective(
        effective_amplitude=effective,
        amplitude_rep=1.0,
        sigma_rep=1.0,
        sigma_att=3.0,
    )

    assert effective == pytest.approx(26.0)
    assert restored == pytest.approx(35.0)


def test_first_threshold_crossing_is_descriptive_grid_point() -> None:
    rows = [
        {"amplitude_att": 1.0, "effective_amplitude": 1.0, "knot_score_median": 0.5},
        {"amplitude_att": 3.0, "effective_amplitude": 3.0, "knot_score_median": 0.8},
    ]

    crossing = comparison.first_threshold_crossing(rows, threshold=0.75)

    assert crossing == {
        "amplitude_att": 3.0,
        "effective_amplitude": 3.0,
        "score": 0.8,
    }
