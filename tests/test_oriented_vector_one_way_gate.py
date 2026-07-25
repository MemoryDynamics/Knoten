from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "oriented_vector_one_way_gate.py"
)
SPEC = importlib.util.spec_from_file_location("oriented_vector_one_way_gate", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def _thresholds() -> dict[str, float]:
    return {
        "response_min_r": 1e-3,
        "null_separation_min": 2.0,
        "memory_gain_min": 1.25,
        "flip_cosine_max": -0.9,
        "flip_magnitude_min": 0.5,
        "flip_magnitude_max": 2.0,
        "tangential_fraction_min": 0.5,
        "target_radius_max_change": 0.1,
        "target_shape_max_change": 0.1,
        "source_radius_max_change": 0.5,
        "source_spectrum_max_drift": 0.25,
    }


def _persistent_metrics() -> dict[str, float]:
    return {
        "active_response_r": 0.01,
        "null_separation": 3.0,
        "flip_cosine": -0.99,
        "flip_magnitude_ratio": 1.0,
        "tangential_fraction": 0.8,
        "target_radius_max_change": 0.01,
        "target_shape_max_change": 0.01,
        "source_radius_max_change": 0.1,
        "source_spectrum_max_drift": 0.1,
    }


def test_parse_seeds_and_sample_steps_are_deterministic() -> None:
    assert gate.parse_seeds("3, 1,2") == [3, 1, 2]
    with pytest.raises(ValueError, match="unique"):
        gate.parse_seeds("1,1")

    steps = gate.make_sample_steps(2_000, 100)
    assert steps[0] == 0
    assert steps[-1] == 2_000
    assert np.all(np.diff(steps) > 0)
    assert 1 in steps


def test_classify_case_passes_only_when_every_preregistered_gate_passes() -> None:
    persistent = _persistent_metrics()
    one_step = {"null_separation": 2.0}

    gates, memory_gain, passed = gate.classify_case(
        persistent,
        one_step,
        _thresholds(),
    )

    assert memory_gain == pytest.approx(1.5)
    assert all(gates.values())
    assert passed is True


@pytest.mark.parametrize(
    ("metric", "value", "failed_gate"),
    [
        ("active_response_r", 1e-4, "response"),
        ("null_separation", 1.5, "random_sign"),
        ("flip_cosine", -0.5, "sign_flip"),
        ("flip_magnitude_ratio", 2.5, "sign_flip"),
        ("tangential_fraction", 0.2, "transverse"),
        ("target_radius_max_change", 0.2, "target_shape_bounded"),
        ("target_shape_max_change", 0.2, "target_shape_bounded"),
        ("source_radius_max_change", 0.6, "source_shape_bounded"),
        ("source_spectrum_max_drift", 0.3, "source_shape_bounded"),
    ],
)
def test_classify_case_rejects_each_failed_metric(
    metric: str,
    value: float,
    failed_gate: str,
) -> None:
    persistent = deepcopy(_persistent_metrics())
    persistent[metric] = value

    gates, _, passed = gate.classify_case(
        persistent,
        {"null_separation": 2.0},
        _thresholds(),
    )

    assert gates[failed_gate] is False
    assert passed is False


def test_classify_case_requires_persistent_advantage_over_one_step_control() -> None:
    gates, memory_gain, passed = gate.classify_case(
        _persistent_metrics(),
        {"null_separation": 3.0},
        _thresholds(),
    )

    assert memory_gain == pytest.approx(1.0)
    assert gates["persistent_memory"] is False
    assert passed is False
