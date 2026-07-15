import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "dynamics"
    / "dspec_raw_snapshot_report.py"
)
SPEC = importlib.util.spec_from_file_location("dspec_raw_snapshot_report", SCRIPT_PATH)
assert SPEC is not None
dspec_raw_snapshot_report = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = dspec_raw_snapshot_report
SPEC.loader.exec_module(dspec_raw_snapshot_report)


def _write_case(path: Path, *, dim: int = 3) -> None:
    rng = np.random.default_rng(123)
    points = rng.normal(size=(180, dim))
    weights = np.linspace(0.1, 1.0, len(points))
    payload = {
        "condition": "baseline",
        "seed": 7,
        "config": {"dim": dim, "steps": 1000},
        "diagnostics": {
            "memory_cloud": {
                "spectral": {"dimension": 2.75},
                "snapshot": {
                    "points": points.tolist(),
                    "weights": weights.tolist(),
                    "n_points": len(points),
                },
            }
        },
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_load_snapshots_finds_case_payload(tmp_path: Path) -> None:
    case_path = tmp_path / "case_baseline_seed7_steps1000.json"
    _write_case(case_path, dim=4)

    records = dspec_raw_snapshot_report.load_snapshots([tmp_path])

    assert len(records) == 1
    assert records[0].dim == 4
    assert records[0].seed == 7
    assert records[0].points.shape == (180, 4)


def test_measure_snapshot_reports_weighted_and_heat_metrics(tmp_path: Path) -> None:
    case_path = tmp_path / "case_baseline_seed7_steps1000.json"
    _write_case(case_path, dim=3)
    record = dspec_raw_snapshot_report.load_snapshots([tmp_path])[0]

    row = dspec_raw_snapshot_report.measure_snapshot(record)

    assert row["n_points"] == 180
    assert row["stored_dspec"] == 2.75
    assert row["weighted_covariance_dimension"] is not None
    assert row["shape_effective_dimension"] is not None
    assert row["heat_valid_count"] >= 0


def test_empty_report_explains_missing_snapshots(tmp_path: Path) -> None:
    report = dspec_raw_snapshot_report._build_report(
        report_path=tmp_path / "report.md",
        summary_json=tmp_path / "summary.json",
        source_dirs=[tmp_path],
        rows=[],
        summary=[],
        figure_paths=[],
    )

    assert "No case JSON" in report
    assert "--memory-snapshot-points" in report
