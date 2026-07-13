from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "dynamics"
    / "paper_i_evidence_table.py"
)
SPEC = importlib.util.spec_from_file_location("paper_i_evidence_table", SCRIPT_PATH)
assert SPEC is not None
paper_i_evidence_table = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = paper_i_evidence_table
SPEC.loader.exec_module(paper_i_evidence_table)


def test_evidence_rows_compute_control_separation() -> None:
    payload = {
        "summary": [
            {
                "a_att": 35.0,
                "condition": "baseline",
                "n": 5,
                "steps": 30_000_000,
                "dynamic_rms_radius_median": 0.2,
                "dynamic_center_drift_radius_fraction_per_memory_time_median": 0.05,
                "memory_shape_dimension_median": 2.9,
                "memory_roundness_median": 0.8,
            },
            {
                "a_att": 35.0,
                "condition": "eta_zero",
                "n": 5,
                "steps": 30_000_000,
                "dynamic_rms_radius_median": 1.0,
                "dynamic_center_drift_radius_fraction_per_memory_time_median": 0.3,
                "memory_shape_dimension_median": 1.9,
                "memory_roundness_median": 0.4,
            },
        ]
    }

    rows = paper_i_evidence_table.evidence_rows(payload)

    assert len(rows) == 1
    assert rows[0]["radius_control_over_active"] == 5.0
    assert rows[0]["drift_control_over_active"] == pytest.approx(6.0)
    assert rows[0]["memory_dimension_delta"] == 1.0
    assert rows[0]["roundness_delta"] == 0.4


def test_report_states_claim_boundary() -> None:
    payload = {
        "summary": [
            {
                "a_att": 35.0,
                "condition": "baseline",
                "n": 5,
                "steps": 30_000_000,
                "dynamic_rms_radius_median": 0.2,
                "dynamic_center_drift_radius_fraction_per_memory_time_median": 0.05,
            },
            {
                "a_att": 35.0,
                "condition": "eta_zero",
                "n": 5,
                "steps": 30_000_000,
                "dynamic_rms_radius_median": 1.0,
                "dynamic_center_drift_radius_fraction_per_memory_time_median": 0.3,
            },
        ]
    }

    report = paper_i_evidence_table.build_report(
        payload,
        source_path=Path("summary.json"),
        reference_a_att=35.0,
    )

    assert "# Paper I Evidence Table" in report
    assert "co-moving compact memory-cloud" in report
    assert "Not supported here" in report
