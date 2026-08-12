from __future__ import annotations

from experiments.current.memory.synchronization.reciprocity.quasistatic_two_knot_discrimination import (
    run_audit,
)


def test_quasistatic_two_knot_discrimination_passes_registered_gates() -> None:
    result = run_audit()
    assert result["decision"] == "quasistatic-discrimination-pass-pointlike-full-memory"
    assert all(result["gates"].values())
    assert result["force_at_discrimination_radius"]["static_compensated"] < 0.0
    assert result["force_at_discrimination_radius"]["gradient_mediator"] > 0.0
    assert (
        result["canonical_readout_comparison_at_discrimination_radius"]
        ["gradient_mediator"]["reciprocal_visible_memory_force"]
        > 0.0
    )
    assert result["maximum_readout_mass_residual"] < 2.0e-8
    assert result["claim_limits"]["dynamics"].startswith("no state is advanced")
