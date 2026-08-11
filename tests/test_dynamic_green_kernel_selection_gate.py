from __future__ import annotations

from experiments.current.memory.closure.dynamic_green_kernel_selection_gate import (
    run_audit,
)


def test_dynamic_green_kernel_selection_gate_passes_registered_identities() -> None:
    result = run_audit()
    assert result["decision"] == "structural-pass-dynamic-kernel-candidate"
    assert all(result["gates"].values())
    assert result["claim_limits"]["nonlinear_nodes"] == "not simulated"
