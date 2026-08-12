from __future__ import annotations

from experiments.current.memory.closure.dynamic_green_kernel_selection_gate import (
    run_audit,
)


def test_dynamic_green_kernel_selection_gate_passes_registered_identities() -> None:
    result = run_audit()
    assert (
        result["decision"]
        == "structural-pass-adjoint-gradient-mediator-candidate"
    )
    assert all(result["gates"].values())
    assert result["inverse_transform_max_error"] < 2.0e-10
    assert result["first_pair_barrier"]["radius"] > 3.9
    assert result["first_finite_pair_minimum"]["radius"] > 6.9
    assert result["claim_limits"]["state_boundary"].endswith("canonical occupancy rho")
    assert result["claim_limits"]["nonlinear_nodes"] == "not simulated"
