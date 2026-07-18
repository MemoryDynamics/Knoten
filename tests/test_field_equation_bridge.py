from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "current" / "kernels"))
sys.path.insert(0, str(ROOT / "src"))

import field_equation_bridge as bridge  # noqa: E402


def test_bridge_distinguishes_exact_heat_flow_from_stationary_field() -> None:
    payload = bridge.bridge_payload(
        argparse.Namespace(
            gaussian_length=3.0,
            diffusivity=1.0,
            decay_rate=1.0,
            coupling=1.0,
            max_dimensionless_wavenumber=6.0,
        )
    )

    assert payload["exact_heat_max_error"] < 1.0e-14
    assert (
        payload["stationary_max_abs_error_u_le_3"]
        > payload["stationary_max_abs_error_u_le_0p5"]
    )
    assert payload["stationary_max_abs_error_u_le_0p5"] > 0.0
