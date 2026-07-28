from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "dynamic_common_source_mediator_gate.py"
)
SPEC = importlib.util.spec_from_file_location(
    "dynamic_common_source_mediator_gate", SCRIPT
)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def _thresholds() -> dict[str, float]:
    return {
        "response_rms_min_r": 1e-4,
        "response_rms_max_r": 0.1,
        "odd_symmetry_max": 0.1,
        "flip_rms_min": 0.9,
        "flip_rms_max": 1.1,
        "target_radius_max_change": 0.1,
        "target_shape_max_change": 0.1,
        "far_near_max_ratio": 0.5,
        "model_trace_separation_min": 0.25,
    }


def _metrics(**updates: float) -> dict[str, float]:
    values = {
        "active_response_rms_r": 0.01,
        "active_response_peak_r": 0.02,
        "active_response_final_r": 0.01,
        "odd_symmetry_relative_rms": 0.01,
        "flip_response_rms_ratio": 1.0,
        "target_radius_max_change": 0.01,
        "target_shape_max_change": 0.01,
    }
    values.update(updates)
    return values


def test_relative_trace_separation_is_zero_for_same_and_two_for_sign_flip() -> None:
    trace = np.array([[1.0, 0.0], [0.0, 2.0]])

    assert gate.relative_trace_separation(trace, trace) == 0.0
    assert np.isclose(gate.relative_trace_separation(trace, -trace), 2.0)


def test_response_gate_requires_window_oddness_and_shape() -> None:
    passing = gate.response_gates(_metrics(), _thresholds())
    failing = gate.response_gates(
        _metrics(active_response_rms_r=0.2, odd_symmetry_relative_rms=0.2),
        _thresholds(),
    )

    assert all(passing.values())
    assert not failing["response_window"]
    assert not failing["sign_flip"]


def test_attenuation_gate_checks_local_monotonicity_and_far_ratio() -> None:
    passing = gate.attenuation_gates(
        np.array([1.0, 0.4, 0.2]), tolerance=0.25, far_near_max_ratio=0.5
    )
    failing = gate.attenuation_gates(
        np.array([1.0, 0.4, 0.8]), tolerance=0.25, far_near_max_ratio=0.5
    )

    assert passing["response_monotone"]
    assert passing["far_near_bounded"]
    assert not failing["response_monotone"]
    assert not failing["far_near_bounded"]


def test_report_keeps_physical_law_and_dimension_claims_closed(
    tmp_path: Path,
) -> None:
    distance = {
        "distance_ratio_pair_radius": 2.5,
        "persistent": _metrics(),
        "one_step": _metrics(),
    }
    model_row = {"pair_pass": True, "distances": [distance]}
    payload = {
        "generated_utc": "2026-07-28T00:00:00+00:00",
        "burn_memory_times": 20.0,
        "analysis_memory_times": 50.0,
        "thresholds": _thresholds(),
        "minimum_passing_pairs": 1,
        "decision": {
            "status": "dynamic_architectures_separated_mechanism_underdetermined",
            "interpretation": "Architecture only.",
        },
        "model_summary": {
            model: {
                "passing_pairs": 1,
                "pair_count": 1,
                "response_rms_min": 0.01,
                "response_rms_max": 0.01,
                "odd_residual_max": 0.01,
                "target_radius_change_max": 0.01,
                "target_shape_change_max": 0.01,
            }
            for model in ("relaxation_diffusion", "telegraph")
        },
        "rows": [
            {
                "target_seed": 1,
                "source_seed": 2,
                "source_gates": {"shape": True},
                "models": {
                    "relaxation_diffusion": model_row,
                    "telegraph": model_row,
                },
                "model_separation": [
                    {"persistent": 1.0, "one_step": 1.0}
                ],
                "pair_pass": True,
            }
        ],
        "identifiability_summary": "reports/ident.json",
        "mediator_summary": "reports/mediator.json",
        "source_reference": "reports/source.json",
        "git_revision": "abc",
        "git_status_at_start": "",
        "command": ["python", "gate.py"],
    }

    report = gate.build_report(
        payload, tmp_path / "report.md", tmp_path / "figure.png"
    )

    assert "not discovery of a physical field law" in report
    assert "neither selects three dimensions" in report
    assert "No reciprocity" in report
