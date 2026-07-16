from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from emergenz_knoten import (
    FiniteMemoryCheckpoint,
    FiniteMemoryState,
    SimulationConfig,
    finite_memory_checkpoint_manifest,
    load_finite_memory_checkpoint,
    save_finite_memory_checkpoint,
    simulate_final_finite_memory_state,
)
from emergenz_knoten.core import simulate_finite_memory_numba


def _config() -> SimulationConfig:
    return SimulationConfig(
        steps=120,
        dim=2,
        epsilon=1e-3,
        eta=0.15,
        alpha=0.1,
        memory_mass=1.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=2.0,
        memory_factor=2.0,
        max_memory=50,
        burn_in=0,
        sample_every=20,
    )


def _checkpoint() -> FiniteMemoryCheckpoint:
    config = _config()
    state = simulate_final_finite_memory_state(config, seed=17)
    return FiniteMemoryCheckpoint(
        state=state,
        config=config,
        update_index=config.steps,
        formation_seed=17,
        created_utc="2026-07-16T12:00:00Z",
        git_revision="abc1234",
        generator="tests/test_checkpoints.py",
    )


def test_final_state_runner_matches_sampled_numba_backend() -> None:
    config = _config()

    expected = simulate_finite_memory_numba(config, seed=17)
    actual = simulate_final_finite_memory_state(config, seed=17)

    np.testing.assert_allclose(actual.x, expected["final_x"], rtol=0.0, atol=0.0)
    np.testing.assert_allclose(actual.memory, expected["memory"], rtol=0.0, atol=0.0)
    np.testing.assert_allclose(actual.weights, expected["weights"], rtol=0.0, atol=0.0)


def test_checkpoint_round_trip_preserves_complete_state(tmp_path: Path) -> None:
    checkpoint = _checkpoint()
    path = save_finite_memory_checkpoint(checkpoint, tmp_path / "state.npz")

    loaded = load_finite_memory_checkpoint(path)

    assert loaded.config == checkpoint.config
    assert loaded.update_index == checkpoint.update_index
    assert loaded.formation_seed == checkpoint.formation_seed
    assert loaded.continuation_noise_policy == checkpoint.continuation_noise_policy
    np.testing.assert_array_equal(loaded.state.x, checkpoint.state.x)
    np.testing.assert_array_equal(loaded.state.memory, checkpoint.state.memory)
    np.testing.assert_array_equal(loaded.state.weights, checkpoint.state.weights)
    manifest = finite_memory_checkpoint_manifest(loaded)
    assert manifest["memory_order"] == "youngest_first"
    assert manifest["arrays"]["memory"]["shape"] == [20, 2]


def test_checkpoint_rejects_incomplete_retained_memory() -> None:
    checkpoint = _checkpoint()
    incomplete = FiniteMemoryState(
        x=checkpoint.state.x,
        memory=checkpoint.state.memory[:-1],
        weights=checkpoint.state.weights[:-1],
    )

    with pytest.raises(ValueError, match="complete retained memory"):
        FiniteMemoryCheckpoint(
            state=incomplete,
            config=checkpoint.config,
            update_index=checkpoint.update_index,
            formation_seed=checkpoint.formation_seed,
            created_utc=checkpoint.created_utc,
            git_revision=checkpoint.git_revision,
            generator=checkpoint.generator,
        )


def test_checkpoint_detects_array_tampering(tmp_path: Path) -> None:
    path = save_finite_memory_checkpoint(_checkpoint(), tmp_path / "state.npz")
    with np.load(path, allow_pickle=False) as data:
        x = data["x"].copy()
        memory = data["memory"].copy()
        weights = data["weights"].copy()
        manifest = data["manifest"].copy()
    memory[-1, -1] += 1.0
    with path.open("wb") as handle:
        np.savez_compressed(
            handle,
            x=x,
            memory=memory,
            weights=weights,
            manifest=manifest,
        )

    with pytest.raises(ValueError, match="checksum"):
        load_finite_memory_checkpoint(path)


def test_checkpoint_rejects_config_weight_mismatch() -> None:
    checkpoint = _checkpoint()

    with pytest.raises(ValueError, match="weights"):
        replace(checkpoint, config=replace(checkpoint.config, memory_mass=2.0))
