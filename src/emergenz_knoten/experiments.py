"""Common experiment utilities for simulation runners, checkpoints, and outputs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any

import numpy as np

from .core import SimulationConfig, simulate_finite_memory

SimulationResult = dict[str, np.ndarray]


def _ndarray_to_json_value(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, dict):
        return {k: _ndarray_to_json_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_ndarray_to_json_value(v) for v in value]
    return value


def save_simulation_result(result: SimulationResult, path: Path) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.suffix == ".npz":
        np.savez_compressed(path, **result)
    elif path.suffix == ".json":
        json_data = _ndarray_to_json_value(result)
        path.write_text(json.dumps(json_data, indent=2), encoding="utf-8")
    else:
        raise ValueError("Unsupported output format: use .npz or .json")


def load_simulation_result(path: Path) -> SimulationResult:
    path = path.expanduser().resolve()
    if path.suffix == ".npz":
        with np.load(path, allow_pickle=False) as data:
            return {key: data[key] for key in data.files}
    if path.suffix == ".json":
        raw = json.loads(path.read_text(encoding="utf-8"))
        return {key: np.asarray(value) for key, value in raw.items()}
    raise ValueError("Unsupported input format: use .npz or .json")


def run_simulation(
    config: SimulationConfig,
    *,
    seed: int = 0,
    output_path: Path | None = None,
) -> SimulationResult:
    result = simulate_finite_memory(config, seed=seed)
    if output_path is not None:
        save_simulation_result(result, output_path)
    return result


@dataclass
class SimulationRunner:
    config: SimulationConfig
    seed: int = 0
    output_path: Path | None = None

    def run(self) -> SimulationResult:
        return run_simulation(self.config, seed=self.seed, output_path=self.output_path)
