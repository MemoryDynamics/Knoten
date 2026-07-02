from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "experiments" / "knot_score_report.py"
SPEC = importlib.util.spec_from_file_location("knot_score_report", SCRIPT_PATH)
assert SPEC is not None
knot_score_report = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = knot_score_report
SPEC.loader.exec_module(knot_score_report)


def _payload(condition: str, seed: int, *, radius: float, memory_roundness: float) -> dict[str, object]:
    return {
        "condition": condition,
        "seed": seed,
        "diagnostics": {
            "mean_centered_radius": radius,
            "occupancy_dimension": 1.8,
            "sample_shape": {
                "effective_dimension": 2.0,
                "axis_ratio_min_max": 0.3,
                "mean_radius": radius,
            },
            "memory_cloud": {
                "shape": {
                    "effective_dimension": 2.6,
                    "axis_ratio_min_max": memory_roundness,
                    "mean_radius": radius / 10.0,
                }
            },
            "residence_by_voxel_size": {
                "1.0": {"max_residence_memory_times": 30.0},
                "2.0": {"max_residence_memory_times": 60.0},
            },
        },
    }


def _cases() -> dict[tuple[str, int], object]:
    return {
        ("baseline", 1): knot_score_report.CaseRecord(
            "baseline",
            1,
            Path("baseline.json"),
            _payload("baseline", 1, radius=1.0, memory_roundness=0.6),
        ),
        ("eta_zero", 1): knot_score_report.CaseRecord(
            "eta_zero",
            1,
            Path("eta_zero.json"),
            _payload("eta_zero", 1, radius=10.0, memory_roundness=0.3),
        ),
    }


def test_shape_rows_include_eta_zero_controls() -> None:
    cases = _cases()

    rows = knot_score_report.build_rows(cases, score_version="v0.3")
    shape_rows = knot_score_report.build_shape_rows(cases)
    report = knot_score_report.build_report(
        {
            "finished_utc": "2026-07-02T00:00:00Z",
            "score_version": "v0.3",
            "rows": rows,
            "shape_rows": shape_rows,
        }
    )

    assert "| `baseline` |" in report
    assert "| `eta_zero` |" in report
    assert "## Shape Summary" in report
    assert "memory roundness med" in report


def test_v0_4_report_includes_memory_cloud_components() -> None:
    cases = _cases()

    rows = knot_score_report.build_rows(cases, score_version="v0.4")
    shape_rows = knot_score_report.build_shape_rows(cases)
    report = knot_score_report.build_report(
        {
            "finished_utc": "2026-07-02T00:00:00Z",
            "score_version": "v0.4",
            "rows": rows,
            "shape_rows": shape_rows,
        }
    )

    assert "# Knot Score v0.4 Report" in report
    assert "memory-cloud compactness gain" in report
    assert "memory roundness gain" in report
    assert "components R/C/V/D/MC/MR/MD" in report
    assert rows[0]["memory_compactness_score"] == 1.0
