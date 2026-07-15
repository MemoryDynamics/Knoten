from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "dynamics"
    / "dimension_claim_audit.py"
)
SPEC = importlib.util.spec_from_file_location("dimension_claim_audit", SCRIPT_PATH)
assert SPEC is not None
dimension_claim_audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = dimension_claim_audit
SPEC.loader.exec_module(dimension_claim_audit)


def test_variance_axis_count_counts_cumulative_axes() -> None:
    eig = [4.0, 1.0, 1.0, 0.1]

    assert dimension_claim_audit.variance_axis_count(eig, 0.90) == 3.0
    assert dimension_claim_audit.variance_axis_count(eig, 0.95) == 3.0
    assert dimension_claim_audit.variance_axis_count([0.0, -1.0], 0.90) is None


def test_case_row_derives_memory_tail_and_center_trace(tmp_path: Path) -> None:
    centers = [[float(i), float(i % 3), 0.0] for i in range(120)]
    payload = {
        "condition": "baseline",
        "seed": 1,
        "config": {"dim": 3, "steps": 1000, "alpha": 0.1},
        "diagnostics": {
            "dynamic_center_trace": {
                "trend": {
                    "rms_radius_median": 0.2,
                    "center_drift_radius_fraction_per_memory_time_median": 0.05,
                },
                "trace": {
                    "steps": list(range(120)),
                    "centers": centers,
                },
            },
            "memory_cloud": {
                "shape": {
                    "effective_dimension": 2.8,
                    "axis_ratio_min_max": 0.7,
                    "covariance_eigenvalues": [4.0, 1.0, 0.5],
                },
                "spectral": {"dimension": 2.2},
            },
            "sample_shape": {"effective_dimension": 1.5},
            "occupancy": {"scaling_window": {"dimension": 1.4}},
            "sample_spectral": {"dimension": 1.2},
        },
    }
    path = tmp_path / "case_baseline_seed1_steps1000.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    [case] = dimension_claim_audit.load_cases([tmp_path])
    row = dimension_claim_audit.case_row(
        case,
        center_trace_min_gap_memory_times=1.0,
        center_trace_spectral_points=50,
    )

    assert row["memory_d90"] == 2.0
    assert row["memory_d95"] == 3.0
    assert row["center_trace_point_count"] < len(centers)
    assert row["center_trace_covariance_dimension"] is not None
    assert row["sample_covariance_dimension"] == 1.5
