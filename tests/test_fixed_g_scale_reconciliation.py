from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "current" / "kernels"))

import fixed_g_scale_reconciliation as reconciliation  # noqa: E402


def test_extract_dynamic_metrics_uses_scale_aware_trace_values() -> None:
    case = {
        "diagnostics": {
            "dynamic_center_trace": {
                "max_run_memory_times": 42.0,
                "comoving_inside_fraction_time_weighted": 0.75,
                "x_distance_to_rms_radius_median": 0.9,
            }
        }
    }

    assert reconciliation.extract_dynamic_metrics(case) == {
        "comoving_max_run_memory_times": 42.0,
        "comoving_inside_fraction": 0.75,
        "x_distance_to_rms_radius": 0.9,
    }


def test_scale_aware_reading_preserves_preregistered_classification() -> None:
    source = {
        "decision": {
            "classification": "inconclusive",
            "median_absolute_radius_departure": 0.062,
        },
        "endpoint_seed_pairs": [
            {"memory_dimension_change": -0.01, "memory_roundness_change": -0.02}
            for _ in range(5)
        ],
    }
    changes = [
        {
            "condition": "baseline",
            "comoving_log2_ratio": 0.01,
            "comoving_inside_fraction_change": 0.001,
        }
        for _ in range(5)
    ]

    reading = reconciliation.scale_aware_reading(source, changes)

    assert reading["pre_registered_classification"] == "inconclusive"
    assert (
        reading["post_hoc_reading"]
        == "weak_smooth_correction_without_metastable_transition"
    )
