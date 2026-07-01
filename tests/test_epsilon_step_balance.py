from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "experiments" / "epsilon_step_balance.py"
)
SPEC = importlib.util.spec_from_file_location("epsilon_step_balance", SCRIPT_PATH)
assert SPEC is not None
epsilon_step_balance = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(epsilon_step_balance)


def test_parse_float_list() -> None:
    assert epsilon_step_balance._parse_float_list("0.03, 0.01,0.005") == [
        0.03,
        0.01,
        0.005,
    ]


def test_summarize_array_ignores_nonfinite_values() -> None:
    summary = epsilon_step_balance.summarize_array([1.0, 2.0, float("nan"), 3.0])

    assert summary["n"] == 3
    assert summary["mean"] == pytest.approx(2.0)
    assert summary["median"] == pytest.approx(2.0)
