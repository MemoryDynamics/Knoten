import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "dynamics"
    / "n_dependence_recheck_report.py"
)
SPEC = importlib.util.spec_from_file_location("n_dependence_recheck_report", SCRIPT_PATH)
assert SPEC is not None
n_dependence_recheck_report = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = n_dependence_recheck_report
SPEC.loader.exec_module(n_dependence_recheck_report)


def test_load_scalar_rows_preserves_n_axis(tmp_path: Path) -> None:
    path = tmp_path / "scalar.json"
    path.write_text(
        json.dumps(
            {
                "summary": [
                    {
                        "a_att": 35.0,
                        "steps": 100000,
                        "n": 5,
                        "memory_shape_dimension_median": 2.9,
                        "memory_radius_median": 0.06,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    rows = n_dependence_recheck_report.load_scalar_rows(path)

    assert rows == [
        {
            "family": "scalar_n_eps003",
            "a_att": 35.0,
            "steps": 100000,
            "condition": "baseline",
            "n": 5,
            "memory_shape_dimension_median": 2.9,
            "memory_shape_dimension_q1": None,
            "memory_shape_dimension_q3": None,
            "memory_roundness_median": None,
            "memory_roundness_q1": None,
            "memory_roundness_q3": None,
            "memory_radius_median": 0.06,
            "memory_radius_q1": None,
            "memory_radius_q3": None,
            "occupancy_window_dimension_median": None,
            "residence_gain_median": None,
        }
    ]


def test_load_snapshot_rows_marks_dim_and_heat_metric(tmp_path: Path) -> None:
    path = tmp_path / "snapshot.json"
    path.write_text(
        json.dumps(
            {
                "summary": [
                    {
                        "dim": 10,
                        "steps": 200000,
                        "condition": "baseline",
                        "n": 3,
                        "shape_effective_dimension_median": 9.1,
                        "heat_median_median": None,
                        "heat_valid_count_median": 0,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    [row] = n_dependence_recheck_report.load_snapshot_rows(path)

    assert row["family"] == "raw_snapshot_pilot_eps1e-4"
    assert row["dim"] == 10
    assert row["memory_shape_dimension_median"] == 9.1
    assert row["heat_trace_dimension_median"] is None
    assert row["heat_valid_count_median"] == 0.0


def test_build_report_contains_guardrails(tmp_path: Path) -> None:
    report = n_dependence_recheck_report.build_report(
        report_path=tmp_path / "report.md",
        summary_json=tmp_path / "summary.json",
        figures=[],
        rows=[
            {
                "family": "raw_snapshot_pilot_eps1e-4",
                "dim": 3,
                "steps": 200000,
                "condition": "baseline",
                "n": 3,
                "memory_shape_dimension_median": 2.9,
                "heat_trace_dimension_median": 1.5,
                "heat_valid_count_median": 7,
            }
        ],
    )

    assert "Exact `3D` is not the right hard acceptance criterion" in report
    assert "weak-probe regime" in report
