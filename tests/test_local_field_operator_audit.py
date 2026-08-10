from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "current" / "kernels" / "field"))

import local_field_operator_audit as audit  # noqa: E402


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        gaussian_length=3.0,
        ambient_dimension=10,
        max_dimensionless_wavenumber=3.0,
    )


def test_k4_operator_improves_fixed_low_wavenumber_match() -> None:
    payload = audit.build_payload(_args())
    matching = payload["gaussian_matching"]

    assert (
        matching["k4_max_abs_error_u_le_0p5"]
        < matching["rd_max_abs_error_u_le_0p5"]
    )
    assert matching["k4_max_abs_error_u_le_1"] < matching["rd_max_abs_error_u_le_1"]


def test_audit_separates_stable_critical_and_unstable_shells() -> None:
    stability = audit.build_payload(_args())["stability"]

    assert stability["finite_k_stable"]["stable"]
    assert stability["finite_k_critical"]["classification"] == (
        "critical_finite_wavenumber"
    )
    assert stability["finite_k_unstable"]["classification"] == (
        "finite_wavenumber_instability"
    )


def test_audit_records_zero_mean_and_full_rank_nulls() -> None:
    payload = audit.build_payload(_args())

    assert payload["compensated_source"]["zero_mean"]
    assert payload["compensated_source"]["zero_mode_response"] == 0.0
    assert payload["ambient_rank_null"]["transfer_is_scalar_identity"]
    assert payload["ambient_rank_null"]["input_rank"] == 10
    assert payload["ambient_rank_null"]["output_rank"] == 10
    assert not payload["claims"]["quantization_established"]
