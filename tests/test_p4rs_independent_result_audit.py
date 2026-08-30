from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4rs_result_audit as audit,
)


@pytest.fixture(scope="module")
def result_audit() -> dict[str, object]:
    return audit.run_audit()


def test_p4rs_auditor_does_not_import_target_or_numeric_stack() -> None:
    tree = ast.parse(Path(audit.__file__).read_text(encoding="utf-8"))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported.append(node.module)
    assert not any("scalar_memory_loop_p4rs_anchor_scale_gate" in name for name in imported)
    assert not any(name.split(".")[0] in {"numpy", "scipy", "mpmath"} for name in imported)


def test_p4rs_independent_raw_recompute_agrees(
    result_audit: dict[str, object],
) -> None:
    assert result_audit["decision"] == "p4rs-independent-audit-agrees"
    assert result_audit["stored_decision"] == audit.EXPECTED_RESULT_DECISION
    assert result_audit["recomputed_decision"] == audit.EXPECTED_RESULT_DECISION
    assert result_audit["differences"] == []
    assert all(result_audit["checks"].values())
    assert all(result_audit["provenance_checks"].values())


def test_p4rs_independent_summary_has_complete_registered_panel(
    result_audit: dict[str, object],
) -> None:
    summary = result_audit["summary"]
    assert summary["active_arm_count"] == 32
    assert summary["channel_off_arm_count"] == 16
    assert summary["samples_per_arm"] == 401
    assert summary["high_precision_reference_count"] == 96
    assert summary["positive_phase_support"] == {"center": 8, "actuator": 8}
    assert max(summary["transient_rms"].values()) < audit.THRESHOLDS.scale_tolerance
    assert max(summary["profile_rms"].values()) < audit.THRESHOLDS.scale_tolerance
    assert max(summary["mean_absolute_differences"].values()) < (
        audit.THRESHOLDS.scale_tolerance
    )


def test_p4rs_independent_decision_precedence_is_fail_closed() -> None:
    response = {
        "available": True,
        "pass": True,
        "means": {"A_C": 0.2, "B_C": 0.2, "A_Q": 0.2, "B_Q": 0.2},
        "positive_phase_support": {"center": 8, "actuator": 8},
    }
    cross_scale = {
        "pass": True,
        "gates": {"common_memory_time_grid": True},
    }
    common = {
        "pipeline": True,
        "registration": True,
        "validity": True,
        "ledger": True,
        "dynamics": True,
        "response": response,
        "cross_scale": cross_scale,
    }
    assert audit._decision(**common)[0] == "p4rs-anchor-scale-transfer-pass"
    assert audit._decision(**{**common, "ledger": False})[0] == (
        "p4rs-ledger-or-metrology-fail"
    )
    mismatch = {**cross_scale, "pass": False}
    assert audit._decision(**{**common, "cross_scale": mismatch})[0] == (
        "p4rs-cross-scale-mismatch"
    )
    no_grid = {"pass": False, "gates": {"common_memory_time_grid": False}}
    assert audit._decision(**{**common, "cross_scale": no_grid})[0] == (
        "p4rs-inconclusive"
    )


def test_p4rs_independent_audit_rejects_corrupted_stored_scale_summary() -> None:
    source_path = audit.ROOT / audit.SOURCE
    report_path = audit.ROOT / audit.SOURCE_REPORT
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    payload["cross_scale"]["transient_rms"]["A_C"] = 0.123
    result = audit.audit_payload(
        payload,
        l3_payload=json.loads(
            (audit.ROOT / audit.L3_SOURCE).read_text(encoding="utf-8")
        ),
        interval_payload=json.loads(
            (audit.ROOT / audit.INTERVAL_SOURCE).read_text(encoding="utf-8")
        ),
        report_text=report_path.read_text(encoding="utf-8"),
        source_sha256=audit.EXPECTED_SOURCE_SHA256,
        report_sha256=audit.EXPECTED_REPORT_SHA256,
        source_blob=audit.EXPECTED_SOURCE_BLOB,
        report_blob=audit.EXPECTED_REPORT_BLOB,
    )
    assert result["recomputed_decision"] == audit.EXPECTED_RESULT_DECISION
    assert result["checks"]["stored_summary_agreement"] is False
    assert result["decision"] == "p4rs-independent-audit-disagrees"
    assert any("cross_scale.transient_rms.A_C" in row for row in result["differences"])


def test_p4rs_independent_audit_output_is_atomic_and_nonoverwriting(
    tmp_path: Path,
) -> None:
    output = tmp_path / "audit.json"
    audit._atomic_write(output, '{"complete": true}\n')
    assert output.read_text(encoding="utf-8") == '{"complete": true}\n'
    assert not output.with_name(output.name + ".tmp").exists()
    with pytest.raises(RuntimeError, match="refusing existing audit output"):
        audit._atomic_write(output, "blocked")
