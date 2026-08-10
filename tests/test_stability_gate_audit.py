from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "current" / "dynamics" / "long_runs" / "stability_gate_audit.py"
SPEC = importlib.util.spec_from_file_location("stability_gate_audit", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_report_keeps_stability_claims_provisional() -> None:
    payload = {
        "question": "test",
        "status": "supported_method_conditional",
        "aggregate": {
            "checkpoint_pass_count": 1,
            "local_radius_pass_count": 1,
            "provisional_pass_count": 1,
            "seed_count": 1,
        },
        "rows": [
            {
                "seed": 1,
                "checkpoint_gate": {
                    "training_radius_relative_range": 0.01,
                    "training_radius_trend_per_decade": 0.01,
                    "holdout_radius_relative_change": 0.01,
                    "training_shape_spectrum_tv_max": 0.01,
                    "holdout_shape_spectrum_tv": 0.01,
                },
                "local_radius_gate": {
                    "training_radius_relative_range": 0.01,
                    "training_radius_cv_max": 0.01,
                },
                "provisional_stability_pass": True,
            }
        ],
        "git_revision": "abc",
        "git_status": "clean",
    }

    report = MODULE.render_report(
        payload,
        generated="2026-07-30T00:00:00Z",
        figure_link="figure.png",
    )

    assert "retrospective provisional" in report
    assert "No first-formation time is identified" in report
    assert "not evidence for a physical particle" in report
