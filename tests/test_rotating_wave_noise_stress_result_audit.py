from __future__ import annotations

from experiments.current.dynamics.rotation import (
    scalar_memory_rotating_wave_noise_stress_result_audit as audit,
)


def test_independent_audit_recomputes_registered_n0_result() -> None:
    result = audit.audit()
    assert result["all_primary_checks_pass"] is True
    assert result["decision_agrees"] is True
    assert result["recomputed_decision"] == (
        "n0-noise-stability-window-bracketed"
    )
    assert result["last_stable_chi"] == 1.0e-4
    assert result["first_higher_failing_chi"] == 1.0e-3
    assert result["resolution_mismatches"] == []
    assert result["gate_mismatches"] == []


def test_audit_uses_canonical_repository_blob_across_line_endings() -> None:
    result = audit.audit()
    assert result["embedded_matches_repository_blob"] is True
    assert result["integrity_finding"] in {
        "canonical-repository-hash-agrees",
        "working-tree-line-ending-transform-canonical-repository-hash-agrees",
    }
    if not result["embedded_matches_bytes"]:
        assert result["embedded_matches_lf_normalized"] is True


def test_independent_resolution_thresholds_are_fail_closed() -> None:
    assert (
        audit.classify_resolution(
            {"effective_to_intended_rms": 0.1, "nonzero_fraction": 1.0},
            1.0,
        )
        == "unresolved"
    )
    assert (
        audit.classify_resolution(
            {"effective_to_intended_rms": 0.5, "nonzero_fraction": 0.5},
            1.0,
        )
        == "resolved"
    )
    assert audit.study_decision(
        ["all-cell-stable"] * 3 + ["stress-fail"]
    ) == "n0-noise-stability-window-bracketed"
    assert audit.study_decision(
        ["all-cell-stable", "stress-fail", "all-cell-stable"]
    ) == "n0-inconclusive"


def test_registered_and_exploratory_slopes_remain_near_linear() -> None:
    result = audit.audit()
    for rows in result["scaling_slopes"].values():
        assert 0.75 <= rows["registered_window"] <= 1.25
        assert 0.75 <= rows["exploratory_next_window"] <= 1.25
