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
    / "ambient_dimension_memory_shape_report.py"
)
SPEC = importlib.util.spec_from_file_location("ambient_dimension_memory_shape_report", SCRIPT_PATH)
assert SPEC is not None
ambient_report = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = ambient_report
SPEC.loader.exec_module(ambient_report)


def _write_case(
    directory: Path,
    *,
    dim: int,
    condition: str,
    seed: int,
    radius: float,
    drift: float,
    d_mem: float,
    roundness: float,
    d_spec_sample: float | None = None,
    d_spec_memory: float | None = None,
) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    payload = {
        "condition": condition,
        "seed": seed,
        "config": {"dim": dim, "steps": 1000},
        "diagnostics": {
            "dynamic_center_trace": {
                "trend": {
                    "rms_radius_median": radius,
                    "center_drift_radius_fraction_per_memory_time_median": drift,
                }
            },
            "sample_spectral": {"dimension": d_spec_sample},
            "memory_cloud": {
                "shape": {
                    "effective_dimension": d_mem,
                    "axis_ratio_min_max": roundness,
                    "mean_radius": radius,
                },
                "spectral": {"dimension": d_spec_memory},
            },
            "center_residence": {
                "memory_center": {"primary_max_run_memory_times": 12.0}
            },
            "residence_by_voxel_size": {
                "1": {"max_residence_memory_times": 15.0}
            },
        },
    }
    path = directory / f"case_{condition}_seed{seed}_steps1000.json"
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_ambient_dimension_report_groups_by_dim_and_condition(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _write_case(
        source,
        dim=4,
        condition="baseline",
        seed=1,
        radius=0.2,
        drift=0.05,
        d_mem=2.9,
        roundness=0.8,
        d_spec_sample=3.1,
        d_spec_memory=3.0,
    )
    _write_case(
        source,
        dim=4,
        condition="eta_zero",
        seed=1,
        radius=1.0,
        drift=0.3,
        d_mem=1.9,
        roundness=0.4,
        d_spec_sample=1.5,
        d_spec_memory=1.4,
    )

    cases = ambient_report.load_cases([source])
    rows = [ambient_report.case_row(case) for case in cases]
    summary = ambient_report.build_summary(rows)

    by_key = {(item["dim"], item["condition"]): item for item in summary}
    assert by_key[(4, "baseline")]["memory_shape_dimension_median"] == 2.9
    assert by_key[(4, "baseline")]["sample_spectral_dimension_median"] == 3.1
    assert by_key[(4, "baseline")]["memory_spectral_dimension_median"] == 3.0
    assert by_key[(4, "eta_zero")]["dynamic_rms_radius_median_median"] == 1.0

    report = ambient_report.build_report(
        rows=rows,
        summary=summary,
        source_dirs=[source],
        summary_json=tmp_path / "summary.json",
    )

    assert "Ambient-Dimension Memory-Shape Check" in report
    assert "| `4` | `baseline`" in report
    assert "radius gain eta0/baseline" in report
    assert "D_spec memory delta" in report
