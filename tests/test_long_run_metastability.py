from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

from emergenz_knoten import SimulationConfig


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "experiments" / "long_run_metastability.py"
SPEC = importlib.util.spec_from_file_location("long_run_metastability", SCRIPT_PATH)
assert SPEC is not None
long_run_metastability = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(long_run_metastability)


def test_apply_condition_keeps_baseline_and_sets_controls() -> None:
    cfg = SimulationConfig(steps=100, eta=0.15, amplitude_att=0.35)

    baseline = long_run_metastability._apply_condition(cfg, "baseline")
    eta_zero = long_run_metastability._apply_condition(cfg, "eta_zero")
    single_scale = long_run_metastability._apply_condition(cfg, "single_scale")

    assert baseline == cfg
    assert eta_zero.eta == 0.0
    assert eta_zero.amplitude_att == cfg.amplitude_att
    assert single_scale.eta == cfg.eta
    assert single_scale.amplitude_att == 0.0


def test_metastability_diagnostics_reports_memory_time_ratios() -> None:
    samples = np.array(
        [
            [0.0, 0.0],
            [0.1, 0.0],
            [0.2, 0.0],
            [0.3, 0.0],
            [0.4, 0.0],
            [3.0, 0.0],
        ],
        dtype=float,
    )
    cfg = SimulationConfig(
        steps=60,
        dim=2,
        alpha=0.1,
        sample_every=10,
        max_memory=20,
    )

    diagnostics = long_run_metastability.metastability_diagnostics(
        samples,
        config=cfg,
        voxel_sizes=[1.0],
        max_ac_lag=2,
        min_memory_times=2.0,
    )

    residence = diagnostics["residence_by_voxel_size"]["1.0"]
    assert diagnostics["memory_persistence_updates"] == 10.0
    assert residence["max_residence_updates"] == 50.0
    assert residence["max_residence_memory_times"] == 5.0
    assert residence["candidate_long_lived"] is True
    assert len(diagnostics["autocorrelation"]) == 3
    assert "occupancy" in diagnostics
    assert "scaling_window" in diagnostics["occupancy"]
    assert "sample_shape" in diagnostics
    assert diagnostics["sample_shape"]["effective_dimension"] is not None
