from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np

from emergenz_knoten import SimulationConfig, load_simulation_result, run_simulation, save_simulation_result


ROOT = Path(__file__).resolve().parents[1]


def load_reproduce_dimension_pilot():
    path = ROOT / "experiments" / "fractal_analysis" / "reproduce_dimension_pilot.py"
    spec = importlib.util.spec_from_file_location("reproduce_dimension_pilot", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_run_simulation_and_save_npz(tmp_path: Path) -> None:
    cfg = SimulationConfig(steps=100, dim=2, alpha=0.05, sample_every=10, max_memory=20)
    result = run_simulation(cfg, seed=42)
    assert isinstance(result["samples"], np.ndarray)
    assert result["samples"].shape == (10, 2)

    output_path = tmp_path / "sim_result.npz"
    save_simulation_result(result, output_path)

    loaded = load_simulation_result(output_path)
    assert np.array_equal(loaded["samples"], result["samples"])
    assert np.array_equal(loaded["sample_steps"], result["sample_steps"])


def test_save_and_load_json(tmp_path: Path) -> None:
    cfg = SimulationConfig(steps=50, dim=2, alpha=0.1, sample_every=25, max_memory=20)
    result = run_simulation(cfg, seed=13)
    output_path = tmp_path / "sim_result.json"
    save_simulation_result(result, output_path)

    loaded = load_simulation_result(output_path)
    assert np.allclose(loaded["samples"], result["samples"])
    assert np.array_equal(loaded["sample_steps"], result["sample_steps"])


def test_reproduce_dimension_pilot_separates_beta_from_alpha() -> None:
    pilot = load_reproduce_dimension_pilot()
    cfg = pilot.ArchiveFractalConfig(alpha=0.01, deposit_beta=0.005, max_memory=300)

    assert pilot.deposit_beta(cfg) == 0.005
    assert pilot.beta_over_alpha(cfg) == 0.5
    assert np.isclose(pilot.stored_weight_mass(cfg), 0.4754795529643571)


def test_reproduce_dimension_pilot_adds_occupancy_window_metrics() -> None:
    pilot = load_reproduce_dimension_pilot()
    run = {
        "n_samples": 1000,
        "occupancy_scales": np.geomspace(0.001, 0.1, 10).tolist(),
        "occupancy_counts": [1000, 990, 920, 700, 252, 91, 33, 12, 5, 2],
    }

    pilot.add_occupancy_window_metrics(run)

    assert run["D_occ_window_valid"] is True
    assert 1.7 <= run["D_occ_windowed"] <= 2.3
    assert run["occupancy_fit_window"]["start_index"] >= 3
    assert len(run["occupancy_local_slopes"]) == 9
