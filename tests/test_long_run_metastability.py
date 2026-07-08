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
    m0_zero = long_run_metastability._apply_condition(cfg, "m0_zero")
    alpha_one = long_run_metastability._apply_condition(cfg, "alpha_one")
    matched = long_run_metastability._apply_condition(cfg, "matched_deposition")

    assert baseline == cfg
    assert eta_zero.eta == 0.0
    assert eta_zero.amplitude_att == cfg.amplitude_att
    assert single_scale.eta == cfg.eta
    assert single_scale.amplitude_att == 0.0
    assert m0_zero.memory_mass == 0.0
    assert m0_zero.eta == cfg.eta
    assert alpha_one.alpha == 1.0
    assert alpha_one.memory_mass == cfg.memory_mass
    assert matched.deposition_kernel == "matched_gaussian"
    assert matched.deposition_sigma == 0.0


def test_stored_weight_mass_scales_with_memory_mass() -> None:
    assert np.isclose(
        long_run_metastability._stored_weight_mass(0.1, 5, 1.0),
        1.0 - 0.9**5,
    )
    assert np.isclose(
        long_run_metastability._stored_weight_mass(0.1, 5, 2.0),
        2.0 * (1.0 - 0.9**5),
    )
    assert long_run_metastability._stored_weight_mass(0.1, 5, 0.0) == 0.0


def test_memory_cloud_diagnostics_skips_zero_weight_mass() -> None:
    memory = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=float)
    weights = np.array([0.0, 0.0], dtype=float)

    assert long_run_metastability._memory_cloud_diagnostics(memory, weights) is None


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