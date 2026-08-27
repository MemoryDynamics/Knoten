from __future__ import annotations

import json
from pathlib import Path

import pytest

from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4r_phase_metrology_gate as target,
)
from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4r_result_audit as audit,
)


@pytest.fixture(scope="module")
def source_payload() -> dict[str, object]:
    return json.loads((audit.ROOT / audit.SOURCE).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def source_report() -> str:
    return (audit.ROOT / audit.SOURCE_REPORT).read_text(encoding="utf-8")


def _run_mutated(
    payload: dict[str, object],
    report: str,
) -> dict[str, object]:
    return audit.audit_payload(
        payload,
        report_text=report,
        source_sha256=audit.EXPECTED_SOURCE_SHA256,
    )


def test_independent_p4r_audit_imports_no_target_or_numeric_stack() -> None:
    source = Path(audit.__file__).read_text(encoding="utf-8")
    assert "scalar_memory_loop_p4r_phase_metrology_gate" not in source
    assert "import numpy" not in source
    assert "import scipy" not in source
    assert "import mpmath" not in source


def test_independent_p4r_audit_recomputes_the_frozen_decision() -> None:
    result = audit.run_audit()

    assert result["decision"] == "p4r-independent-audit-agrees"
    assert result["stored_decision"] == audit.EXPECTED_RESULT_DECISION
    assert result["recomputed_decision"] == audit.EXPECTED_RESULT_DECISION
    assert all(result["checks"].values())
    assert result["differences"] == []
    assert result["summary"]["active_arm_count"] == 32
    assert result["summary"]["channel_off_arm_count"] == 16
    assert result["summary"]["high_precision_reference_count"] == 96


def test_independent_audit_rejects_duplicate_registration(
    source_payload,
    source_report,
) -> None:
    arms = source_payload["active_arms"]
    original = arms[-1]
    arms[-1] = arms[0]
    try:
        result = _run_mutated(source_payload, source_report)
    finally:
        arms[-1] = original

    assert result["decision"] == "p4r-independent-audit-disagrees"
    assert result["checks"]["registration"] is False
    assert result["recomputed_decision"] == "p4r-inconclusive"


@pytest.mark.parametrize("field", ["ledger", "center_local"])
def test_independent_audit_rejects_corrupted_ledger_or_local_identity(
    field,
    source_payload,
    source_report,
) -> None:
    arm = source_payload["active_arms"][0]
    maxima = arm["residual_maxima"]
    original = maxima[field]
    scale = (
        arm["residual_scales"]["initial_energy"]
        if field == "ledger"
        else arm["residual_scales"]["initial_coupling_displacement"]
    )
    maxima[field] = 1.0e-8 * scale
    try:
        result = _run_mutated(source_payload, source_report)
    finally:
        maxima[field] = original

    assert result["decision"] == "p4r-independent-audit-disagrees"
    assert result["checks"]["ledger_and_metrology"] is False
    assert result["recomputed_decision"] == "p4r-ledger-or-metrology-fail"


def test_independent_audit_rejects_reversed_response_sign(
    source_payload,
    source_report,
) -> None:
    arm = source_payload["active_arms"][0]
    original = list(arm["trace"][-1]["center"])
    arm["trace"][-1]["center"] = [-original[0], -original[1]]
    try:
        result = _run_mutated(source_payload, source_report)
    finally:
        arm["trace"][-1]["center"] = original

    assert result["decision"] == "p4r-independent-audit-disagrees"
    assert result["checks"]["response_recomputation"] is False
    assert result["recomputed_decision"] == "p4r-inconclusive"


def test_independent_audit_rejects_corrupted_cumulative_work_term(
    source_payload,
    source_report,
) -> None:
    arm = source_payload["active_arms"][0]
    cumulative = arm["cumulative_work"]
    original = cumulative["write_work"]
    cumulative["write_work"] += (
        1.0e-8 * arm["residual_scales"]["initial_energy"]
    )
    try:
        result = _run_mutated(source_payload, source_report)
    finally:
        cumulative["write_work"] = original

    assert result["decision"] == "p4r-independent-audit-disagrees"
    assert result["checks"]["ledger_and_metrology"] is False
    assert result["recomputed_decision"] == "p4r-ledger-or-metrology-fail"


def test_independent_audit_rejects_threshold_contract_mutation(
    source_payload,
    source_report,
) -> None:
    thresholds = source_payload["protocol"]["thresholds"]
    original = thresholds["chiral_minimum"]
    thresholds["chiral_minimum"] = 0.01
    try:
        result = _run_mutated(source_payload, source_report)
    finally:
        thresholds["chiral_minimum"] = original

    assert result["decision"] == "p4r-independent-audit-disagrees"
    assert result["checks"]["threshold_contract"] is False


def test_registered_age_and_raw_center_rivals_remain_discriminating(
    source_payload,
) -> None:
    arms = source_payload["active_arms"]
    truncated = max(
        arm["residual_maxima"]["truncated_ledger"]
        / arm["residual_scales"]["initial_energy"]
        for arm in arms
    )
    raw = max(
        arm["residual_maxima"]["raw_center_ledger"]
        / arm["residual_scales"]["initial_energy"]
        for arm in arms
    )
    assert truncated > 1.0
    assert raw > 1.0


def test_target_provenance_rejects_a_protocol_blob_mutation(monkeypatch) -> None:
    protocol_path = target.PROTOCOL.as_posix()
    mutated = dict(target.EXPECTED_HEAD_BLOBS)
    mutated[protocol_path] = "0" * 40
    original_git_output = target._git_output

    def clean_git_output(arguments: list[str]) -> str:
        if arguments == ["status", "--short"]:
            return ""
        return original_git_output(arguments)

    monkeypatch.setattr(target, "EXPECTED_HEAD_BLOBS", mutated)
    monkeypatch.setattr(target, "_git_output", clean_git_output)
    with pytest.raises(RuntimeError, match="frozen P4-R dependencies changed"):
        target._verify_provenance()
