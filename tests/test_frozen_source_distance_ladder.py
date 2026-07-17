from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest

from emergenz_knoten import FiniteMemoryState, SimulationConfig, memory_shape_tensor


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "frozen_source_distance_ladder.py"
)
SPEC = importlib.util.spec_from_file_location(
    "frozen_source_distance_ladder", SCRIPT_PATH
)
distance_ladder = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = distance_ladder
SPEC.loader.exec_module(distance_ladder)


def _state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.zeros(2),
        memory=np.array(
            [
                [0.0, 0.0],
                [-0.1, 0.0],
                [0.0, -0.1],
                [0.1, 0.0],
                [0.0, 0.1],
            ]
        ),
        weights=np.array([0.2, 0.16, 0.128, 0.1024, 0.08192]),
    )


def _case(tmp_path: Path):
    state = _state()
    radius = float(np.sqrt(np.trace(memory_shape_tensor(state))))
    config = SimulationConfig(
        steps=100,
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
    return distance_ladder.RESPONSE.CheckpointCase(
        path=tmp_path / "state.npz",
        seed=1,
        update_index=100,
        formation_revision="abc123",
        config=config,
        state=state,
        initial_radius=radius,
    )


def test_distance_parser_keeps_radius_and_kernel_units_explicit() -> None:
    specs = distance_ladder.parse_distance_specs("R:5,S:0.1")

    assert [(spec.scale, spec.multiplier) for spec in specs] == [
        ("radius", 5.0),
        ("sigma", 0.1),
    ]
    assert [spec.label for spec in specs] == ["5 R_mem", "0.1 sigma_rep"]

    with pytest.raises(ValueError, match="must not contain duplicates"):
        distance_ladder.parse_distance_specs("R:5,R:5")


def test_short_distance_ladder_preserves_controls_and_compact_rows(
    tmp_path: Path,
) -> None:
    rows = distance_ladder.run_distance_ladder(
        [_case(tmp_path)],
        distance_specs=distance_ladder.parse_distance_specs("R:5,S:1"),
        interaction_fraction=0.03,
        source_shift_fractions=[0.03, 0.10],
        pulse_memory_times=0.2,
        lag_memory_times=[0.0, 1.0, 10.0],
        noise_base_seed=17,
    )

    assert len(rows) == 2
    assert {row["distance_label"] for row in rows} == {"5 R_mem", "1 sigma_rep"}
    for row in rows:
        assert row["zero_cross_max_abs"] == 0.0
        assert row["center_feedback_rank"] == 2
        assert row["shape_feedback_rank"] <= 2
        assert row["source_shift_low_fraction"] == pytest.approx(0.03)
        assert row["source_shift_high_fraction"] == pytest.approx(0.10)
        assert row["realized_baseline_fraction"] == pytest.approx(0.03, rel=1e-4)


def test_distance_report_rejects_dimension_and_charge_overclaim(tmp_path: Path) -> None:
    rows = distance_ladder.run_distance_ladder(
        [_case(tmp_path)],
        distance_specs=distance_ladder.parse_distance_specs("R:5"),
        interaction_fraction=0.03,
        source_shift_fractions=[0.03, 0.10],
        pulse_memory_times=0.2,
        lag_memory_times=[0.0, 1.0, 10.0],
        noise_base_seed=17,
    )
    payload = {
        "generated_utc": "2026-07-17T00:00:00Z",
        "git_revision": "abc123",
        "command": ["python", "frozen_source_distance_ladder.py"],
        "summary_json": tmp_path / "summary.json",
        "rows": rows,
    }
    report = distance_ladder.build_report(
        payload,
        report_path=tmp_path / "report.md",
        figure_paths=(
            tmp_path / "deformation.png",
            tmp_path / "feedback.png",
            tmp_path / "symmetry.png",
        ),
    )

    assert "does not test source orientation, charge" in report
    assert "cannot establish charge" in report
    assert "three selected external dimensions" in report
