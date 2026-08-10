from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments" / "current" / "memory" / "synchronization" / "one_way" / "oriented_vector_fixed_pair_distance_gate.py"
)
SPEC = importlib.util.spec_from_file_location(
    "oriented_vector_fixed_pair_distance_gate", SCRIPT
)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def _metrics(**updates: float) -> dict[str, float]:
    values = {
        "active_response_r": 0.01,
        "null_separation": 4.0,
        "flip_cosine": -0.99,
        "flip_magnitude_ratio": 1.0,
        "tangential_fraction": 0.1,
        "target_radius_max_change": 0.01,
        "target_shape_max_change": 0.01,
        "source_radius_max_change": 0.1,
        "source_spectrum_max_drift": 0.1,
    }
    values.update(updates)
    return values


def _thresholds() -> dict[str, float]:
    return {
        "response_min_r": 1e-3,
        "null_separation_min": 2.0,
        "memory_gain_min": 1.25,
        "flip_cosine_max": -0.9,
        "flip_magnitude_min": 0.5,
        "flip_magnitude_max": 2.0,
        "target_radius_max_change": 0.1,
        "target_shape_max_change": 0.1,
        "source_radius_max_change": 0.5,
        "source_spectrum_max_drift": 0.25,
    }


def _distance_rows(responses: list[float]) -> list[dict[str, object]]:
    return [
        {
            "initial_field_norm": response,
            "persistent": {"active_response_r": response},
        }
        for response in responses
    ]


def test_pairing_and_distance_parsing_are_fixed_and_independent() -> None:
    assert gate.parse_distance_ratios("2.5,5,10") == [2.5, 5.0, 10.0]
    assert gate.cyclic_seed_pairs([1, 2, 3]) == [(1, 2), (2, 3), (3, 1)]
    with pytest.raises(ValueError, match="increasing"):
        gate.parse_distance_ratios("2.5,2,10")
    with pytest.raises(ValueError, match="at least two"):
        gate.cyclic_seed_pairs([1])


def test_near_gate_does_not_confuse_arbitrary_pair_axis_with_field_response() -> None:
    gates, memory_gain = gate.classify_near_response(
        _metrics(tangential_fraction=0.0),
        {"null_separation": 2.0},
        _thresholds(),
    )

    assert memory_gain == pytest.approx(2.0)
    assert "transverse" not in gates
    assert all(gates.values())


def test_distance_gate_requires_monotone_attenuation_and_far_null() -> None:
    passing = gate.classify_distance_profile(
        _distance_rows([1.0, 0.2, 0.02]),
        monotonic_tolerance=0.1,
        far_near_max_ratio=0.1,
    )
    nonmonotone = gate.classify_distance_profile(
        _distance_rows([1.0, 0.2, 0.3]),
        monotonic_tolerance=0.1,
        far_near_max_ratio=0.1,
    )

    assert passing["attenuation_pass"]
    assert np.allclose(passing["response_ratios_to_near"], [1.0, 0.2, 0.02])
    assert not nonmonotone["response_monotone_pass"]
    assert not nonmonotone["far_null_pass"]
    assert not nonmonotone["attenuation_pass"]


def test_report_keeps_universal_field_and_qft_claims_closed(tmp_path: Path) -> None:
    persistent = _metrics()
    persistent.update({"random_threshold_r": 0.002})
    row = {
        "target_seed": 1,
        "source_seed": 2,
        "target_case_path": "data/target.json",
        "source_case_path": "data/source.json",
        "target_case_sha256": "a" * 64,
        "source_case_sha256": "b" * 64,
        "near_memory_gain": 2.0,
        "distance_rows": [
            {
                "distance_ratio_pair_radius": 2.5,
                "distance_over_source_radius": 2.6,
                "initial_field_norm": 0.1,
                "persistent": persistent,
                "one_step": {"null_separation": 2.0},
            }
        ],
        "profile": {
            "far_to_near_response": 0.01,
            "response_monotone_pass": True,
        },
        "gates": {"target_shape_bounded": True, "source_shape_bounded": True},
        "pair_pass": True,
    }
    payload = {
        "decision": {
            "status": "pass",
            "passing_pairs": 1,
            "pair_count": 1,
            "selected_next_step": "local_or_retarded_oriented_mediator_gate",
        },
        "generated_utc": "2026-07-26T00:00:00+00:00",
        "pairs": ["1<-2"],
        "vector_eta": 5.079e-6,
        "distance_ratios": [2.5, 5.0, 10.0],
        "randomizations": 64,
        "minimum_passing_pairs": 1,
        "thresholds": {
            "distance_monotonic_tolerance": 0.1,
            "far_near_max_ratio": 0.1,
            "null_separation_min": 2.0,
        },
        "rows": [row],
        "formation_config": {"dim": 3},
        "git_revision": "revision",
        "git_status_at_start": "",
        "summary_json": tmp_path / "summary.json",
        "command": ["python", "gate.py"],
    }

    report = gate.build_report(payload, tmp_path / "report.md", tmp_path / "figure.png")

    assert "not yet one universal absolute length scale" in report
    assert "not establish a universal potential" in report
    assert "QFT, spin, charge, photons" in report
    assert "local_or_retarded_oriented_mediator_gate" in report
