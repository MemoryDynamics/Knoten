from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "current" / "dynamics"))
sys.path.insert(0, str(ROOT / "src"))

import linear_long_run_reconciliation as reconciliation  # noqa: E402


def test_retained_memory_mass_matches_canonical_horizon() -> None:
    value = reconciliation.retained_memory_mass(
        lambda_value=0.01,
        memory_mass=1.0,
        horizon=600,
    )

    assert value == pytest.approx(0.997594990708689)


def test_retained_memory_mass_scales_with_m0() -> None:
    value = reconciliation.retained_memory_mass(
        lambda_value=0.1,
        memory_mass=2.5,
        horizon=3,
    )

    assert value == pytest.approx(2.5 * (1.0 - 0.9**3))
