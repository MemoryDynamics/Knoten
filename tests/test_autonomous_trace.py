from __future__ import annotations

import numpy as np

from emergenz_knoten import SimulationConfig
from emergenz_knoten.autonomous_trace import autonomous_knot_trace
from emergenz_knoten.oriented_source import (
    autonomous_oriented_source_trace,
    initialize_oriented_memory_state,
)
from emergenz_knoten.state import FiniteMemoryState


def _state() -> FiniteMemoryState:
    points = np.asarray(
        [[0.2, -0.1], [0.1, -0.05], [0.0, 0.0], [-0.1, 0.02]],
        dtype=float,
    )
    return FiniteMemoryState(
        x=points[0],
        memory=points,
        weights=np.asarray([0.4, 0.3, 0.2, 0.1]),
    )


def _config() -> SimulationConfig:
    return SimulationConfig(
        dim=2,
        epsilon=1e-3,
        eta=0.15,
        alpha=0.2,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=0.0,
        amplitude_att=5.0,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        memory_factor=6.0,
        max_memory=100,
    )


def test_scalar_trace_matches_existing_autonomous_source_path_bitwise() -> None:
    state = _state()
    config = _config()
    steps = np.arange(0, 101, 5)
    noise = np.random.default_rng(81).standard_normal((100, 2))

    scalar = autonomous_knot_trace(
        state,
        config,
        noise=noise,
        sample_steps=steps,
    )
    oriented = autonomous_oriented_source_trace(
        initialize_oriented_memory_state(state, lambda_vector=0.2),
        config,
        source_noise=noise,
        sample_steps=steps,
    )

    assert np.array_equal(scalar.positions, oriented.positions)
    assert np.array_equal(scalar.memory_centers, oriented.memory_centers)
    assert np.array_equal(scalar.shape_tensors, oriented.shape_tensors)
    assert np.array_equal(scalar.radius_ratios, oriented.radius_ratios)


def test_sparse_sampling_is_exact_subsampling_of_hidden_scalar_path() -> None:
    state = _state()
    config = _config()
    noise = np.random.default_rng(91).standard_normal((100, 2))
    dense_steps = np.arange(0, 101)
    sparse_steps = dense_steps[::10]

    dense = autonomous_knot_trace(
        state,
        config,
        noise=noise,
        sample_steps=dense_steps,
    )
    sparse = autonomous_knot_trace(
        state,
        config,
        noise=noise,
        sample_steps=sparse_steps,
    )

    assert np.array_equal(sparse.positions, dense.positions[::10])
    assert np.array_equal(sparse.memory_centers, dense.memory_centers[::10])
    assert np.array_equal(sparse.shape_tensors, dense.shape_tensors[::10])
    assert np.array_equal(sparse.radius_ratios, dense.radius_ratios[::10])
