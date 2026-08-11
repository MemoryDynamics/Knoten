from __future__ import annotations

from experiments.current.memory.closure.continuity_constrained_memory_gate import (
    run_audit,
)


def test_continuity_constrained_memory_gate_passes_registered_identities() -> None:
    result = run_audit()
    assert result["decision"] == "structural-pass-with-unresolved-force-balance"
    assert all(result["gates"].values())
    assert result["claim_limits"]["static_force_balance"].startswith("not supplied")
