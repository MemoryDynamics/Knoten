from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np

from emergenz_knoten import FiniteMemoryState


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "oriented_history_current_audit.py"
)
SPEC = importlib.util.spec_from_file_location(
    "oriented_history_current_audit", SCRIPT_PATH
)
audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)


def _straight_state() -> FiniteMemoryState:
    memory = np.column_stack([np.arange(20.0, -1.0, -1.0), np.zeros(21)])
    weights = np.geomspace(1.0, 0.2, len(memory))
    return FiniteMemoryState(x=memory[0], memory=memory, weights=weights)


def test_parser_keeps_current_modes_and_ratios_explicit() -> None:
    assert audit.parse_resolution_ratios("2.5,10,5") == [10.0, 5.0, 2.5]
    assert audit.parse_modes("displacement,unit") == ["displacement", "unit"]
    assert audit._safe_ratio(0.0, 0.0) == 0.0


def test_straight_history_exceeds_sign_randomization_null() -> None:
    row = audit.evaluate_current_row(
        _straight_state(),
        radius_ratio=2.5,
        mode="displacement",
        null_samples=1000,
        null_quantile=0.99,
        random_seed=17,
        minimum_distinctness=1.25,
    )

    assert np.isclose(row["coherence"], 1.0)
    assert row["null_threshold"] < 1.0
    assert row["exceeds_null"] is True
    assert row["eligible_distinctness"] is True


def test_gate_uses_displacement_current_and_direction_stability() -> None:
    rows = []
    for ratio in (2.5, 5.0):
        row = audit.evaluate_current_row(
            _straight_state(),
            radius_ratio=ratio,
            mode="displacement",
            null_samples=1000,
            null_quantile=0.99,
            random_seed=17 + int(ratio),
            minimum_distinctness=1.25,
        )
        rows.append(row)

    summaries, decision = audit.summarize_gate(
        rows,
        primary_ratio=2.5,
        stability_ratio=5.0,
        direction_cosine_min=0.9,
    )

    assert summaries[0]["polar_direction_cosine"] == 1.0
    assert summaries[0]["polar_pass"] is True
    assert summaries[0]["gate_pass"] is True
    assert decision["status"] == "pass"
    assert (
        decision["selected_next_mechanism"] == "derived_history_current_cross_channel"
    )


def test_gate_can_select_bivector_circulation_without_polar_current() -> None:
    rows = []
    for ratio in (2.5, 5.0):
        rows.append(
            {
                "dim": 3,
                "mode": "displacement",
                "radius_ratio": ratio,
                "eligible_distinctness": True,
                "exceeds_null": False,
                "field_direction": np.array([1.0, 0.0, 0.0]),
                "coherence": 0.01,
                "null_threshold": 0.1,
                "p_upper": 0.9,
                "circulation_exceeds_null": True,
                "circulation_direction": np.array(
                    [0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                )
                / np.sqrt(2.0),
                "circulation_coherence": 0.8,
                "circulation_null_threshold": 0.2,
                "circulation_p_upper": 0.001,
            }
        )

    summaries, decision = audit.summarize_gate(
        rows,
        primary_ratio=2.5,
        stability_ratio=5.0,
        direction_cosine_min=0.9,
    )

    assert summaries[0]["polar_pass"] is False
    assert summaries[0]["circulation_pass"] is True
    assert decision["selected_next_mechanism"] == "derived_history_circulation_channel"
