from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np

from emergenz_knoten import SimulationConfig, simulate_finite_memory

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "experiments" / "kernel_shape_probe.py"
SPEC = importlib.util.spec_from_file_location("kernel_shape_probe", SCRIPT_PATH)
assert SPEC is not None
kernel_shape_probe = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = kernel_shape_probe
assert SPEC.loader is not None
SPEC.loader.exec_module(kernel_shape_probe)


def test_turn_cosine_reports_straight_path() -> None:
    samples = np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0], [3.0, 0.0]])

    turn = kernel_shape_probe._turn_cosine(samples)

    assert abs(turn["mean"] - 1.0) < 1e-12
    assert abs(turn["median"] - 1.0) < 1e-12


def test_pca_projection_returns_three_columns() -> None:
    samples = np.array(
        [
            [0.0, 0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 1.0],
            [2.0, 0.0, 0.0, 1.0],
            [3.0, 0.0, 0.0, 1.0],
        ]
    )

    coords, energy = kernel_shape_probe._pca_projection(samples)

    assert coords.shape == (4, 3)
    assert abs(energy[0] - 1.0) < 1e-12


def test_probe_simulation_matches_package_core() -> None:
    config = SimulationConfig(
        steps=80,
        dim=3,
        alpha=0.1,
        epsilon=0.03,
        eta=0.15,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=0.35,
        max_memory=20,
        burn_in=10,
        sample_every=5,
    )

    probe_samples = kernel_shape_probe.simulate_probe_numpy(config, seed=11)
    core_samples = simulate_finite_memory(config, seed=11)["samples"]

    assert np.allclose(probe_samples, core_samples)


def test_local_scales_capture_current_sign_convention() -> None:
    rep_only = SimulationConfig(eta=0.15, sigma_rep=1.0, sigma_att=3.0, amplitude_rep=1.0, amplitude_att=0.0)
    att_only = SimulationConfig(eta=0.15, sigma_rep=1.0, sigma_att=3.0, amplitude_rep=0.0, amplitude_att=0.35)

    assert kernel_shape_probe._local_scales(rep_only)["net_restoring_scale"] > 0.0
    assert kernel_shape_probe._local_scales(att_only)["net_restoring_scale"] < 0.0

def test_metric_formatter_handles_degenerate_values() -> None:
    assert kernel_shape_probe._fmt_metric(None) == "n/a"
    assert kernel_shape_probe._fmt_metric(float("nan")) == "n/a"
    assert kernel_shape_probe._fmt_metric(0.0) == "0"
    assert kernel_shape_probe._fmt_metric(1.0e-20) == "1.000e-20"
