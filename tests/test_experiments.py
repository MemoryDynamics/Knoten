from __future__ import annotations

from pathlib import Path

import numpy as np

from emergenz_knoten import SimulationConfig, load_simulation_result, run_simulation, save_simulation_result


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
