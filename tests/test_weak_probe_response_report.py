from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np

from emergenz_knoten import FiniteMemoryState, SimulationConfig, memory_shape_tensor


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "weak_probe_response.py"
)
SPEC = importlib.util.spec_from_file_location("weak_probe_response", SCRIPT_PATH)
weak_probe_response = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = weak_probe_response
SPEC.loader.exec_module(weak_probe_response)


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
        amplitude_att=2.0,
        memory_factor=1.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )


def _state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.array([0.0, 0.0]),
        memory=np.array(
            [[0.0, 0.0], [-0.1, 0.0], [0.0, -0.1], [0.1, 0.0], [0.0, 0.1]]
        ),
        weights=np.array([0.3, 0.25, 0.2, 0.15, 0.1]),
    )


def _case(seed: int, path: Path) -> weak_probe_response.SnapshotCase:
    state = _state()
    radius = float(np.sqrt(np.trace(memory_shape_tensor(state))))
    return weak_probe_response.SnapshotCase(path, seed, _config(), state, radius)


def test_snapshot_loader_requires_complete_memory(tmp_path: Path) -> None:
    config = _config()
    state = _state()
    payload = {
        "seed": 4,
        "config": vars(config),
        "diagnostics": {
            "memory_cloud": {
                "snapshot": {
                    "points": state.memory.tolist(),
                    "weights": state.weights.tolist(),
                    "n_points": 5,
                    "source_n_points": 5,
                }
            }
        },
    }
    path = tmp_path / "case_baseline_seed4_steps20.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    [loaded] = weak_probe_response.load_snapshot_cases([tmp_path])

    assert loaded.seed == 4
    assert loaded.dim == 2
    np.testing.assert_allclose(loaded.state.x, state.memory[0])


def test_weak_probe_case_calibrates_bare_identity_and_aggregates(tmp_path: Path) -> None:
    results = []
    for seed in (1, 2):
        results.extend(
            weak_probe_response.run_snapshot_case(
                _case(seed, tmp_path / f"case{seed}.json"),
                probe_fractions=[0.03, 0.1],
                pulse_memory_times=0.2,
                lag_memory_times=[0.0, 1.0],
            )
        )

    for result in results:
        assert np.max(result["quality"]["bare_position_identity_error"]) < 1e-10
        assert result["responses"]["memory_center_residual"].shape == (2, 2, 2)
        assert result["responses"]["shape_residual"].shape == (2, 3, 2)

    ranks = weak_probe_response.aggregate_ranks(results, confidence=0.5)
    linearity = weak_probe_response.linearity_rows(results)

    assert ranks
    assert linearity
    assert {row["observable"] for row in ranks} == {
        "bare_position",
        "position_residual",
        "memory_center_residual",
        "shape_residual",
    }


def test_report_states_statistical_and_physical_guardrails(tmp_path: Path) -> None:
    results = []
    for seed in (1, 2):
        results.extend(
            weak_probe_response.run_snapshot_case(
                _case(seed, tmp_path / f"case{seed}.json"),
                probe_fractions=[0.03, 0.1],
                pulse_memory_times=0.2,
                lag_memory_times=[0.0, 1.0],
            )
        )
    payload = {
        "generated_utc": "2026-07-16T00:00:00Z",
        "probe_fractions": [0.03, 0.1],
        "pulse_memory_times": 0.2,
        "lag_memory_times": [0.0, 1.0],
        "confidence": 0.5,
        "case_results": results,
        "rank_rows": weak_probe_response.aggregate_ranks(results, confidence=0.5),
        "linearity_rows": weak_probe_response.linearity_rows(results),
    }

    report = weak_probe_response.build_report(
        payload,
        report_path=tmp_path / "report.md",
        spectra_path=tmp_path / "spectra.png",
        quality_path=tmp_path / "quality.png",
    )

    assert "must not be interpreted as an emergent dimension" in report
    assert "minimum attainable" in report
    assert "localized frozen translated" in report
    assert "source-knot field" in report
