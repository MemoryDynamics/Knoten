from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments" / "current" / "memory" / "synchronization" / "mediation" / "local_oriented_mediator_gate.py"
)
SPEC = importlib.util.spec_from_file_location("local_oriented_mediator_gate", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def test_relaxation_diffusion_peak_prediction_has_correct_zero_decay_limit() -> None:
    predicted = gate.relaxation_diffusion_peak_prediction(
        2.0,
        diffusivity=4.0,
        decay_rate=0.0,
        pulse_duration=1.0,
    )

    assert predicted == pytest.approx(1.0)


def test_relaxation_shortens_the_diffusive_peak_lag() -> None:
    no_decay = gate.relaxation_diffusion_peak_prediction(
        10.0,
        diffusivity=2.5,
        decay_rate=0.0,
        pulse_duration=1.0,
    )
    relaxed = gate.relaxation_diffusion_peak_prediction(
        10.0,
        diffusivity=2.5,
        decay_rate=0.1,
        pulse_duration=1.0,
    )

    assert relaxed < no_decay
    assert relaxed == pytest.approx(8.307764, rel=1e-6)


def test_trace_lags_use_a_relative_local_threshold() -> None:
    metrics = gate.trace_lags(
        np.arange(6, dtype=float),
        np.array([0.0, 0.01, 0.2, 1.0, 0.5, 0.0]),
        onset_fraction=0.05,
    )

    assert metrics["onset"] == 2.0
    assert metrics["peak"] == 3.0
    assert metrics["amplitude"] == 1.0
