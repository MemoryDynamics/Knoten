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
    / "oriented_memory_source_eligibility_gate.py"
)
SPEC = importlib.util.spec_from_file_location(
    "oriented_memory_source_eligibility_gate",
    SCRIPT,
)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def _thresholds() -> dict[str, float]:
    return {
        "null_separation_min": 2.0,
        "axis_cosine_min": 0.8,
        "amplitude_cv_max": 0.5,
        "source_radius_max_change": 0.5,
        "source_spectrum_max_drift": 0.25,
    }


def test_sample_steps_are_strict_and_include_endpoints() -> None:
    steps = gate.sample_steps(2_000, 100)

    assert steps[0] == 0
    assert steps[-1] == 2_000
    assert np.all(np.diff(steps) > 0)


def test_channel_metrics_detect_stable_axis_and_null_separation() -> None:
    values = np.tile(np.array([1.0, 0.0, 0.0]), (10, 1))
    coherences = np.full(10, 0.6)
    nulls = np.full(10, 0.2)
    metrics = gate.channel_metrics(
        values,
        coherences,
        nulls,
        late_mask=np.arange(10) >= 5,
    )

    assert np.isclose(metrics["null_separation_median"], 3.0)
    assert np.isclose(metrics["axis_cosine"], 1.0)
    assert np.isclose(metrics["amplitude_cv"], 0.0)


def test_classify_channel_requires_every_preregistered_gate() -> None:
    metrics = {
        "null_separation_median": 3.0,
        "axis_cosine": 0.9,
        "amplitude_cv": 0.2,
    }
    shape = {"radius_max_change": 0.1, "spectrum_max_drift": 0.1}

    gates, passed = gate.classify_channel(metrics, shape, _thresholds())

    assert all(gates.values())
    assert passed is True

    failed = dict(metrics, axis_cosine=0.5)
    gates, passed = gate.classify_channel(failed, shape, _thresholds())
    assert gates["axis_identity"] is False
    assert passed is False