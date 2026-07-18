from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "current" / "kernels"))
sys.path.insert(0, str(ROOT / "experiments" / "current" / "dynamics"))
sys.path.insert(0, str(ROOT / "src"))

import attractive_only_regime_scan as scan  # noqa: E402


def _record(amplitude: float, radius: float, dimension: float) -> dict[str, float]:
    return {
        "amplitude_att": amplitude,
        "memory_radius_median": radius,
        "dynamic_radius_median": radius,
        "dynamic_drift_ratio_median": radius,
        "memory_dimension_median": dimension,
        "memory_roundness_median": dimension / 3.0,
        "memory_compactness_gain_median": 1.0 / radius,
    }


def test_change_ranking_finds_inserted_kpi_jump() -> None:
    aggregate = [
        _record(0.0, 4.0, 1.0),
        _record(1.0, 3.9, 1.1),
        _record(2.0, 1.0, 2.8),
        _record(3.0, 0.95, 2.9),
    ]

    ranked = scan.rank_change_intervals(aggregate)

    assert ranked[0]["left"] == 1.0
    assert ranked[0]["right"] == 2.0


def test_default_scan_includes_null_and_matched_reference() -> None:
    amplitudes = scan._default_amplitudes()

    assert amplitudes[0] == 0.0
    assert amplitudes[-1] == 40.0
    assert 26.0 in amplitudes
