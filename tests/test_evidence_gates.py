from __future__ import annotations

import pytest

from emergenz_knoten import EvidenceGate, GateStatus, evaluate_evidence_gate


def test_inadequate_measurement_is_inconclusive_not_physical_failure() -> None:
    validity = evaluate_evidence_gate(
        "experimental-validity",
        {"controls": True, "shape-bounded": True},
    )
    identifiability = evaluate_evidence_gate(
        "identifiability",
        {"input-rank": True, "signal-holdout": False},
        prerequisites=(validity,),
        failed_status=GateStatus.INCONCLUSIVE,
    )
    second_state = evaluate_evidence_gate(
        "second-state",
        {"predictive-order": True},
        prerequisites=(identifiability,),
    )

    assert validity.status is GateStatus.PASS
    assert identifiability.status is GateStatus.INCONCLUSIVE
    assert identifiability.failed_checks == ("signal-holdout",)
    assert second_state.status is GateStatus.BLOCKED
    assert second_state.blocked_by == ("identifiability",)


def test_not_run_gate_is_distinct_from_failure() -> None:
    gate = evaluate_evidence_gate("two-node-channel", None)

    assert gate == EvidenceGate(
        name="two-node-channel",
        status=GateStatus.NOT_RUN,
    )


def test_gate_rejects_non_boolean_checks_and_invalid_failure_status() -> None:
    with pytest.raises(TypeError, match="must be bool"):
        evaluate_evidence_gate("bad-check", {"count": 1})  # type: ignore[dict-item]
    with pytest.raises(ValueError, match="fail or inconclusive"):
        evaluate_evidence_gate(
            "bad-status",
            {"check": False},
            failed_status=GateStatus.BLOCKED,
        )
