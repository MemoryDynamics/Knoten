from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest

from emergenz_knoten import FiniteMemoryState, SimulationConfig
from emergenz_knoten.local_mediator import LocalMediatorGrid, TelegraphMediator
from emergenz_knoten.retarded_reciprocal import retarded_reciprocal_pair_response


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments" / "current" / "memory" / "synchronization" / "reciprocity" / "retarded_reciprocal_full_knot_gate.py"
)
SPEC = importlib.util.spec_from_file_location("retarded_sampling_gate", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


def _response(sample_steps: np.ndarray):
    steps = int(sample_steps[-1])
    state = FiniteMemoryState(
        x=np.zeros(2),
        memory=np.array(
            [[0.0, 0.0], [-0.1, 0.0], [0.1, 0.0], [0.0, -0.1], [0.0, 0.1]]
        ),
        weights=np.array([0.4, 0.15, 0.15, 0.15, 0.15]),
    )
    config = SimulationConfig(
        steps=steps,
        dim=2,
        epsilon=0.01,
        eta=0.15,
        alpha=0.1,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=20.0,
        memory_factor=1.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )
    grid = LocalMediatorGrid(0.25, 0.1, 20, 30)
    mediator = TelegraphMediator(0.5, 0.1, 0.1)
    first_noise = np.arange(2 * steps, dtype=float).reshape(steps, 2) / 100.0
    second_noise = first_noise[::-1].copy()
    return retarded_reciprocal_pair_response(
        state,
        state,
        config,
        initial_center_separation=[1.0, 0.0],
        first_noise=first_noise,
        second_noise=second_noise,
        sample_steps=sample_steps,
        cross_eta=1e-3,
        mediator_grid=grid,
        mediator=mediator,
        mediator_readout_position=1.0,
    )


def test_sparse_sampling_is_exact_subsampling_of_the_same_update_path() -> None:
    dense = _response(np.arange(41))
    sparse = _response(np.arange(0, 41, 5))

    np.testing.assert_array_equal(sparse.positions, dense.positions[::5])
    np.testing.assert_array_equal(sparse.memory_centers, dense.memory_centers[::5])
    np.testing.assert_array_equal(sparse.shape_tensors, dense.shape_tensors[::5])
    np.testing.assert_array_equal(sparse.mediator_readouts, dense.mediator_readouts[::5])


def test_mode_rates_are_invariant_under_exact_subsampling() -> None:
    matrix = np.array([[0.995, -0.02], [0.02, 0.995]])
    positions, centers = GATE._trace(matrix, samples=2400) if hasattr(GATE, "_trace") else (None, None)
    if positions is None:
        state = np.empty((2400, 3, 2), dtype=float)
        state[0] = np.array([[1.0, 0.2], [-0.4, 0.7], [0.3, -0.8]])
        for index in range(1, state.shape[0]):
            state[index] = state[index - 1] @ matrix.T
        positions, centers = state[:, :, 0], state[:, :, 1]
    thresholds = {
        "min_complex_segments": 3,
        "frequency_min_per_memory_time": 0.05,
        "mode_relative_range_max": 0.25,
        "phase_coherence_min": 0.5,
        "fit_residual_ratio_max": 0.8,
        "fit_condition_max": 1e8,
    }
    dense = GATE._mode_row(
        positions,
        centers,
        alpha=0.01,
        sample_every=1,
        thresholds=thresholds,
    )
    sparse = GATE._mode_row(
        positions[::5],
        centers[::5],
        alpha=0.01,
        sample_every=5,
        thresholds=thresholds,
    )

    assert sparse["frequency_per_memory_time"] == pytest.approx(
        dense["frequency_per_memory_time"], rel=1e-10
    )
    assert sparse["damping_per_memory_time"] == pytest.approx(
        dense["damping_per_memory_time"], rel=1e-10
    )
