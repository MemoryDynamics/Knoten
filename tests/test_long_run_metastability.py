from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

from emergenz_knoten import SimulationConfig


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "experiments" / "current" / "dynamics" / "long_run_metastability.py"
SPEC = importlib.util.spec_from_file_location("long_run_metastability", SCRIPT_PATH)
assert SPEC is not None
long_run_metastability = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(long_run_metastability)



def test_trace_targets_support_fixed_and_log_schedules() -> None:
    fixed = long_run_metastability._trace_targets(
        steps=100,
        burn_in=0,
        trace_every=25,
        trace_points=0,
        trace_spacing="log",
    )
    assert fixed.tolist() == [25, 50, 75, 100]

    log_targets = long_run_metastability._trace_targets(
        steps=1000,
        burn_in=0,
        trace_every=0,
        trace_points=8,
        trace_spacing="log",
    )
    assert log_targets[0] == 1
    assert log_targets[-1] == 1000
    assert len(log_targets) <= 8
    assert np.all(np.diff(log_targets) > 0)
    assert np.diff(log_targets)[0] < np.diff(log_targets)[-1]

    hybrid = long_run_metastability._trace_targets(
        steps=100,
        burn_in=0,
        trace_every=10,
        trace_points=5,
        trace_spacing="log",
        trace_window_updates=30,
    )
    assert hybrid[-4:].tolist() == [70, 80, 90, 100]
    assert np.all(hybrid[:-4] < 70)

def test_apply_condition_keeps_baseline_and_sets_controls() -> None:
    cfg = SimulationConfig(steps=100, eta=0.15, amplitude_att=0.35)

    baseline = long_run_metastability._apply_condition(cfg, "baseline")
    eta_zero = long_run_metastability._apply_condition(cfg, "eta_zero")
    single_scale = long_run_metastability._apply_condition(cfg, "single_scale")
    rep_zero = long_run_metastability._apply_condition(cfg, "rep_zero")
    m0_zero = long_run_metastability._apply_condition(cfg, "m0_zero")
    alpha_one = long_run_metastability._apply_condition(cfg, "alpha_one")
    matched = long_run_metastability._apply_condition(cfg, "matched_deposition")
    renormalized = long_run_metastability._apply_condition(cfg, "matched_deposition_renormalized")
    zero_mean = long_run_metastability._apply_condition(cfg, "zero_mean_two_scale")

    assert baseline == cfg
    assert eta_zero.eta == 0.0
    assert eta_zero.amplitude_att == cfg.amplitude_att
    assert single_scale.eta == cfg.eta
    assert single_scale.amplitude_att == 0.0
    assert single_scale.amplitude_rep == cfg.amplitude_rep
    assert rep_zero.eta == cfg.eta
    assert rep_zero.amplitude_rep == 0.0
    assert rep_zero.amplitude_att == cfg.amplitude_att
    assert m0_zero.memory_mass == 0.0
    assert m0_zero.eta == cfg.eta
    assert alpha_one.alpha == 1.0
    assert alpha_one.memory_mass == cfg.memory_mass
    assert matched.deposition_kernel == "matched_gaussian"
    assert matched.deposition_sigma == 0.0
    assert renormalized.deposition_kernel == "matched_gaussian"
    assert renormalized.amplitude_rep > cfg.amplitude_rep
    assert renormalized.amplitude_att > cfg.amplitude_att
    assert np.isclose(zero_mean.amplitude_att, cfg.amplitude_rep * (cfg.sigma_rep / cfg.sigma_att) ** cfg.dim)


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


def test_dynamic_center_trace_diagnostics_reports_comoving_runs() -> None:
    cfg = SimulationConfig(steps=40, dim=2, alpha=0.1, sample_every=10)
    result = {
        "trace_steps": np.array([10, 20, 30, 40], dtype=np.int64),
        "trace_centers": np.array(
            [[0.0, 0.0], [0.1, 0.0], [0.2, 0.0], [0.3, 0.0]],
            dtype=float,
        ),
        "trace_mean_radii": np.array([1.0, 1.0, 1.0, 1.0], dtype=float),
        "trace_rms_radii": np.array([1.0, 1.0, 1.0, 1.0], dtype=float),
        "trace_x_distances": np.array([0.5, 1.5, 3.0, 0.2], dtype=float),
    }

    diagnostics = long_run_metastability._dynamic_center_trace_diagnostics(
        result,
        config=cfg,
        trace_every=10,
        primary_radius_factor=2.0,
    )

    assert diagnostics is not None
    assert diagnostics["n_traces"] == 4
    assert diagnostics["comoving_inside_fraction"] == 0.75
    assert diagnostics["max_run_trace_points"] == 2
    assert diagnostics["max_run_memory_times"] == 2.0
    assert np.isclose(diagnostics["center_drift_per_memory_time_median"], 0.1)
    assert diagnostics["trace"]["inside_primary_radius"] == [True, True, False, True]

    zero_radius = {
        "trace_steps": np.array([10, 20], dtype=np.int64),
        "trace_centers": np.zeros((2, 2), dtype=float),
        "trace_mean_radii": np.zeros(2, dtype=float),
        "trace_rms_radii": np.zeros(2, dtype=float),
        "trace_x_distances": np.zeros(2, dtype=float),
    }
    degenerate = long_run_metastability._dynamic_center_trace_diagnostics(
        zero_radius,
        config=cfg,
        trace_every=10,
    )

    assert degenerate is not None
    assert degenerate["comoving_inside_fraction"] == 0.0
    assert degenerate["degenerate_radius_fraction"] == 1.0

def test_dynamic_center_trace_reports_spin_proxy() -> None:
    cfg = SimulationConfig(steps=50, dim=2, alpha=0.1, sample_every=10)
    result = {
        "trace_steps": np.array([10, 20, 30, 40, 50], dtype=np.int64),
        "trace_centers": np.zeros((5, 2), dtype=float),
        "trace_positions": np.array(
            [[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0], [1.0, 0.0]],
            dtype=float,
        ),
        "trace_mean_radii": np.ones(5, dtype=float),
        "trace_rms_radii": np.ones(5, dtype=float),
        "trace_x_distances": np.ones(5, dtype=float),
    }

    diagnostics = long_run_metastability._dynamic_center_trace_diagnostics(
        result,
        config=cfg,
        trace_every=10,
        primary_radius_factor=2.0,
    )

    assert diagnostics is not None
    spin = diagnostics["spin_proxy"]
    assert spin["component_count"] == 1
    assert spin["sample_count"] == 5
    assert np.isclose(spin["sample_interval_memory_times"], 1.0)
    assert np.isclose(spin["window_span_memory_times"], 4.0)
    assert np.isclose(spin["valid_fraction"], 1.0)
    assert spin["amplitude_median"] > 0.0
    assert spin["angular_speed_median"] > 0.0
    assert spin["axis_polarization"] > 0.99
    assert spin["signed_component_median"] > 0.0
    assert len(spin["transition_memory_times"]) == 4
    assert len(spin["amplitudes"]) == 4
    assert len(spin["angular_speeds"]) == 4
    assert diagnostics["trace"]["positions"][0] == [1.0, 0.0]

def test_hybrid_trace_separates_log_trend_from_local_spin_window() -> None:
    cfg = SimulationConfig(steps=100, dim=2, alpha=0.1, sample_every=10)
    steps = np.array([1, 10, 70, 80, 90, 100], dtype=np.int64)
    result = {
        "trace_steps": steps,
        "trace_centers": np.column_stack((0.01 * steps, np.zeros(len(steps)))),
        "trace_positions": np.column_stack((0.01 * steps + 1.0, np.zeros(len(steps)))),
        "trace_mean_radii": np.array([1.0, 1.0, 2.0, 2.0, 2.0, 2.0]),
        "trace_rms_radii": np.array([1.0, 1.0, 2.0, 2.0, 2.0, 2.0]),
        "trace_x_distances": np.ones(len(steps), dtype=float),
    }

    diagnostics = long_run_metastability._dynamic_center_trace_diagnostics(
        result,
        config=cfg,
        trace_every=10,
        primary_radius_factor=2.0,
    )

    assert diagnostics is not None
    assert diagnostics["spin_proxy"]["sample_count"] == 4
    assert diagnostics["trend"]["n_traces"] == 3
    assert diagnostics["trend"]["trace_interval_updates_min"] == 9.0
    assert diagnostics["trend"]["trace_interval_updates_max"] == 90.0
    assert diagnostics["rms_radius_median"] == 2.0
    assert diagnostics["trend"]["rms_radius_median"] == 1.0
    assert long_run_metastability._dynamic_center_field(
        {"dynamic_center_trace": diagnostics}, "rms_radius_median"
    ) == 1.0


def test_irregular_log_trace_does_not_report_local_spin_proxy() -> None:
    cfg = SimulationConfig(steps=100, dim=2, alpha=0.1, sample_every=10)
    result = {
        "trace_steps": np.array([1, 3, 10, 30, 100], dtype=np.int64),
        "trace_centers": np.zeros((5, 2), dtype=float),
        "trace_positions": np.array(
            [[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0], [1.0, 0.0]],
            dtype=float,
        ),
        "trace_mean_radii": np.ones(5, dtype=float),
        "trace_rms_radii": np.ones(5, dtype=float),
        "trace_x_distances": np.ones(5, dtype=float),
    }

    diagnostics = long_run_metastability._dynamic_center_trace_diagnostics(
        result,
        config=cfg,
        trace_every=0,
        primary_radius_factor=2.0,
    )

    assert diagnostics is not None
    assert "spin_proxy" not in diagnostics


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
    assert "center_residence" in diagnostics
    sample_center = diagnostics["center_residence"]["sample_center"]
    assert sample_center["primary_max_run_memory_times"] >= 5.0
    assert sample_center["by_radius_factor"]["1"]["max_run_memory_times"] == 5.0


def test_run_case_reports_memory_center_residence(tmp_path: Path) -> None:
    cfg = SimulationConfig(
        steps=200,
        dim=2,
        eta=0.15,
        alpha=0.1,
        burn_in=20,
        sample_every=10,
        max_memory=20,
    )

    payload = long_run_metastability.run_case(
        base_config=cfg,
        condition="baseline",
        seed=7,
        voxel_sizes=[1.0],
        max_ac_lag=2,
        min_memory_times=2.0,
        output_dir=tmp_path,
    )

    diagnostics = payload["diagnostics"]
    center_residence = diagnostics["center_residence"]
    assert "sample_center" in center_residence
    assert "memory_center" in center_residence
    assert "2" in center_residence["memory_center"]["by_radius_factor"]

    summary = long_run_metastability.summarize_cases([payload])[0]
    assert summary["sample_center_primary_max_run_memory_times"] is not None
    assert summary["memory_center_primary_max_run_memory_times"] is not None

def test_force_component_diagnostics_reports_update_channels() -> None:
    cfg = SimulationConfig(
        steps=200,
        dim=2,
        eta=0.15,
        alpha=0.1,
        burn_in=20,
        sample_every=10,
        max_memory=20,
    )

    diagnostics = long_run_metastability._force_component_diagnostics(cfg, seed=7)

    assert diagnostics["n_samples"] == 19
    assert diagnostics["rep_step_norm_median"] is not None
    assert diagnostics["net_drift_norm_median"] is not None
    assert diagnostics["noise_norm_median"] is not None
    assert diagnostics["rep_step_norm_median"] >= 0.0


def test_force_component_diagnostics_zero_eta_has_zero_drift() -> None:
    cfg = SimulationConfig(
        steps=100,
        dim=2,
        eta=0.0,
        alpha=0.1,
        burn_in=10,
        sample_every=10,
        max_memory=20,
    )

    diagnostics = long_run_metastability._force_component_diagnostics(cfg, seed=7)

    assert diagnostics["rep_step_norm_median"] == 0.0
    assert diagnostics["att_step_norm_median"] == 0.0
    assert diagnostics["net_drift_norm_median"] == 0.0
    assert diagnostics["noise_norm_median"] is not None
