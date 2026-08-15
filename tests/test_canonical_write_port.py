from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten import (
    FiniteMemoryState,
    SimulationConfig,
    paired_canonical_write_response,
)
from emergenz_knoten.kernels import exponential_memory_weights


def _state() -> FiniteMemoryState:
    memory = np.array(
        [
            [0.2, -0.1],
            [0.1, -0.2],
            [-0.1, -0.1],
            [-0.2, 0.1],
            [0.0, 0.2],
        ]
    )
    return FiniteMemoryState(
        x=memory[0],
        memory=memory,
        weights=exponential_memory_weights(0.2, memory.shape[0]),
    )


def _config(*, eta: float) -> SimulationConfig:
    return SimulationConfig(
        steps=20,
        dim=2,
        epsilon=0.03,
        eta=eta,
        alpha=0.2,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=5.0,
        memory_factor=5.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )


def test_eta_zero_write_returns_visible_paths_but_leaves_memory_response() -> None:
    state = _state()
    steps = np.arange(0, 11)
    noise = np.random.default_rng(8).normal(size=(steps[-1], state.dim))

    response = paired_canonical_write_response(
        state,
        _config(eta=0.0),
        direction=[1.0, 0.0],
        kr_values=[0.5, 1.0],
        perturbation_fraction=0.01,
        noise=noise,
        sample_steps=steps,
    )

    np.testing.assert_allclose(response.plus_kicks.sum(axis=0), 0.0, atol=0.0)
    np.testing.assert_allclose(response.position_response[1], [1.0, 0.0])
    np.testing.assert_allclose(response.position_response[2:], 0.0, atol=1e-12)
    np.testing.assert_allclose(
        response.branch_positions[2:, 0],
        response.control_positions[2:],
        atol=1e-14,
    )
    np.testing.assert_allclose(
        response.branch_positions[2:, 1],
        response.control_positions[2:],
        atol=1e-14,
    )
    assert np.linalg.norm(response.memory_center_response[2:5]) > 0.0
    assert np.linalg.norm(response.centered_mode_response[2:5]) > 0.0
    np.testing.assert_allclose(response.self_drift_response, 0.0, atol=0.0)


def test_active_write_response_is_finite_and_translation_invariant() -> None:
    state = _state()
    shift = np.array([7.0, -3.0])
    translated = FiniteMemoryState(
        x=state.x + shift,
        memory=state.memory + shift,
        weights=state.weights,
    )
    steps = np.arange(0, 13)
    noise = np.random.default_rng(12).normal(size=(steps[-1], state.dim))
    kwargs = {
        "direction": [0.0, 1.0],
        "kr_values": [0.5, 1.0, 2.0],
        "perturbation_fraction": 0.005,
        "noise": noise,
        "sample_steps": steps,
    }

    baseline = paired_canonical_write_response(state, _config(eta=0.15), **kwargs)
    moved = paired_canonical_write_response(translated, _config(eta=0.15), **kwargs)

    for values in (
        baseline.position_response,
        baseline.memory_center_response,
        baseline.centered_mode_response,
        baseline.self_drift_response,
        baseline.position_even_leakage,
    ):
        assert np.isfinite(values).all()
    np.testing.assert_allclose(moved.position_response, baseline.position_response)
    np.testing.assert_allclose(
        moved.memory_center_response,
        baseline.memory_center_response,
    )
    np.testing.assert_allclose(
        moved.centered_mode_response,
        baseline.centered_mode_response,
        atol=1e-11,
    )


def test_write_response_rejects_horizon_before_return_kick() -> None:
    with pytest.raises(ValueError, match="reach two"):
        paired_canonical_write_response(
            _state(),
            _config(eta=0.0),
            direction=[1.0, 0.0],
            kr_values=[1.0],
            perturbation_fraction=0.01,
            noise=np.zeros((1, 2)),
            sample_steps=[0, 1],
        )
