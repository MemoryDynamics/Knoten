from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np

from emergenz_knoten import (
    FiniteMemoryCheckpoint,
    FiniteMemoryState,
    SimulationConfig,
    memory_shape_tensor,
    save_finite_memory_checkpoint,
)


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "frozen_source_response.py"
)
SPEC = importlib.util.spec_from_file_location("frozen_source_response", SCRIPT_PATH)
frozen_source_response = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = frozen_source_response
SPEC.loader.exec_module(frozen_source_response)


def _config() -> SimulationConfig:
    return SimulationConfig(
        steps=20,
        dim=2,
        epsilon=0.001,
        eta=0.15,
        alpha=0.2,
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


def _state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.array([0.0, 0.0]),
        memory=np.array([[0.0, 0.0], [-0.1, 0.0], [0.0, -0.1], [0.1, 0.0], [0.0, 0.1]]),
        weights=np.array([0.2, 0.16, 0.128, 0.1024, 0.08192]),
    )


def _case(path: Path) -> frozen_source_response.CheckpointCase:
    state = _state()
    radius = float(np.sqrt(np.trace(memory_shape_tensor(state))))
    return frozen_source_response.CheckpointCase(
        path=path,
        seed=1,
        update_index=100,
        formation_revision="abc123",
        config=_config(),
        state=state,
        initial_radius=radius,
    )


def test_checkpoint_loader_reads_complete_state(tmp_path: Path) -> None:
    checkpoint = FiniteMemoryCheckpoint(
        state=_state(),
        config=_config(),
        update_index=100,
        formation_seed=3,
        created_utc="2026-07-17T00:00:00Z",
        git_revision="abc123",
        generator="test",
    )
    path = tmp_path / "state.npz"
    save_finite_memory_checkpoint(checkpoint, path)

    [loaded] = frozen_source_response.load_checkpoint_cases(tmp_path)

    assert loaded.seed == 3
    assert loaded.update_index == 100
    np.testing.assert_array_equal(loaded.state.memory, checkpoint.state.memory)


def test_frozen_source_case_has_exact_zero_control_and_rank_rows(
    tmp_path: Path,
) -> None:
    results = frozen_source_response.run_checkpoint_case(
        _case(tmp_path / "state.npz"),
        interaction_fraction=0.03,
        perturbation_sigma_rep=[0.03, 0.10],
        separation_sigma_rep=1.0,
        pulse_memory_times=0.2,
        lag_memory_times=[0.0, 1.0],
        noise_base_seed=17,
    )

    assert len(results) == 2
    for result in results:
        assert result["quality"]["zero_cross_max_abs"] == 0.0
        assert result["responses"]["memory_center_feedback"].shape == (2, 2, 2)
        assert result["responses"]["shape_feedback"].shape == (2, 3, 2)
        assert result["quality"]["bare_baseline_pulse_fraction"] > 0.0

    ranks = frozen_source_response.rank_rows(results)
    linearity = frozen_source_response.linearity_rows(results)

    assert ranks
    assert linearity
    assert {row["observable"] for row in linearity} == set(results[0]["responses"])


def test_report_keeps_cloned_source_guardrails(tmp_path: Path) -> None:
    results = frozen_source_response.run_checkpoint_case(
        _case(tmp_path / "state.npz"),
        interaction_fraction=0.03,
        perturbation_sigma_rep=[0.03, 0.10],
        separation_sigma_rep=1.0,
        pulse_memory_times=0.2,
        lag_memory_times=[0.0, 1.0],
        noise_base_seed=17,
    )
    payload = {
        "generated_utc": "2026-07-17T00:00:00Z",
        "git_revision": "abc123",
        "command": ["python", "frozen_source_response.py"],
        "checkpoint_dir": "checkpoints",
        "summary_json": tmp_path / "summary.json",
        "lag_memory_times": [0.0, 1.0],
        "case_results": results,
        "rank_rows": frozen_source_response.rank_rows(results),
        "linearity_rows": frozen_source_response.linearity_rows(results),
    }

    report = frozen_source_response.build_report(
        payload,
        report_path=tmp_path / "report.md",
        figure_paths=(
            tmp_path / "response.png",
            tmp_path / "spectra.png",
            tmp_path / "quality.png",
        ),
    )

    assert "One checkpoint per" in report
    assert "not synchronization" in report
    assert "must not be interpreted as an" in report
    assert "Independent source and target seeds" in report
