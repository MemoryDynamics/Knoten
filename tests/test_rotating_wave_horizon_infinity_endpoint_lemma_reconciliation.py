from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_infinity_endpoint_lemma_reconciliation.py"
)


@pytest.fixture
def audit_module():
    specification = importlib.util.spec_from_file_location(
        "endpoint_lemma_reconciliation_under_test", SCRIPT
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@pytest.fixture
def records(audit_module):
    return (
        audit_module._load_json(audit_module.ATTEMPT_RESULT),
        audit_module._load_json(audit_module.BRIDGE_RESULT),
        audit_module._load_json(audit_module.G4_RESULT),
        audit_module._load_json(audit_module.ATTEMPT_AUDIT),
    )


def _reconcile(audit_module, records):
    return audit_module.reconcile_records(
        *records,
        provenance_pass=True,
        created_utc="2026-10-01T00:00:00+00:00",
    )


def test_published_records_reconcile_without_changing_attempt_decision(
    audit_module, records
):
    result = _reconcile(audit_module, records)

    assert result["decision"] == audit_module.PASS_DECISION
    assert set(result["gates"].values()) == {"pass"}
    assert result["source_attempt_decision"] == "g-infinity-branch-link-inconclusive"
    assert result["source_attempt_decision_unchanged"] is True
    assert result["diagnostics"]["boxes_byte_equal"] is False
    assert all(result["diagnostics"]["finite_image_in_uniform_box"])
    assert all(result["diagnostics"]["g4_image_in_uniform_box"])


@pytest.mark.parametrize("panel_index,coordinate,endpoint", [(0, "radius", 0), (1, "theta", 1)])
def test_g4_image_outside_uniform_box_falsifies_r4(
    audit_module, records, panel_index, coordinate, endpoint
):
    attempt, bridge, g4, attempt_audit = copy.deepcopy(records)
    coordinate_index = 0 if coordinate == "radius" else 1
    box_endpoint = "-9" if endpoint == 0 else "9"
    attempt["sealed_inputs"]["g4_tail_images"][panel_index][coordinate_index][
        endpoint
    ] = box_endpoint
    if endpoint == 0:
        attempt["sealed_inputs"]["g4_tail_images"][panel_index][coordinate_index][
            1
        ] = box_endpoint
    else:
        attempt["sealed_inputs"]["g4_tail_images"][panel_index][coordinate_index][
            0
        ] = box_endpoint

    result = audit_module.reconcile_records(
        attempt,
        bridge,
        g4,
        attempt_audit,
        provenance_pass=True,
        created_utc="synthetic",
    )

    assert result["gates"]["R4"] == "fail"
    assert result["decision"] == audit_module.FAIL_DECISION


def test_finite_image_outside_uniform_box_falsifies_r3(audit_module, records):
    attempt, bridge, g4, attempt_audit = copy.deepcopy(records)
    bridge_panel = next(
        row for row in bridge["finite_branch"]["root_panels"] if row["horizon"] == 3600
    )
    outside = "9"
    bridge_panel["inner_certificate_80"]["krawczyk_image"][0] = [outside, outside]

    result = audit_module.reconcile_records(
        attempt,
        bridge,
        g4,
        attempt_audit,
        provenance_pass=True,
        created_utc="synthetic",
    )

    assert result["gates"]["R3"] == "fail"
    assert result["decision"] == audit_module.FAIL_DECISION


@pytest.mark.parametrize("field", ["krawczyk_strict_interior", "uniform_regularity"])
def test_non_strict_or_nonregular_uniform_panel_falsifies_r2(
    audit_module, records, field
):
    attempt, bridge, g4, attempt_audit = copy.deepcopy(records)
    attempt["homotopy"]["panels"][0]["gates"][field] = False

    result = audit_module.reconcile_records(
        attempt,
        bridge,
        g4,
        attempt_audit,
        provenance_pass=True,
        created_utc="synthetic",
    )

    assert result["gates"]["R2"] == "fail"
    assert result["decision"] == audit_module.FAIL_DECISION


def test_changed_attempt_decision_or_extra_negative_gate_falsifies_r1(
    audit_module, records
):
    attempt, bridge, g4, attempt_audit = copy.deepcopy(records)
    attempt["classification"]["gates"]["U3"] = "inconclusive"

    result = audit_module.reconcile_records(
        attempt,
        bridge,
        g4,
        attempt_audit,
        provenance_pass=True,
        created_utc="synthetic",
    )

    assert result["gates"]["R1"] == "fail"
    assert result["decision"] == audit_module.FAIL_DECISION


def test_equal_boxes_do_not_substitute_for_image_inclusion(audit_module, records):
    attempt, bridge, g4, attempt_audit = copy.deepcopy(records)
    for index, panel in enumerate(attempt["homotopy"]["panels"]):
        attempt["sealed_inputs"]["g4_tail_boxes"][index] = copy.deepcopy(panel["box"])
    outside = "9"
    attempt["sealed_inputs"]["g4_tail_images"][0][0] = [outside, outside]

    result = audit_module.reconcile_records(
        attempt,
        bridge,
        g4,
        attempt_audit,
        provenance_pass=True,
        created_utc="synthetic",
    )

    assert result["gates"]["R4"] == "fail"
    assert result["gates"]["R5"] == "fail"
    assert result["decision"] == audit_module.FAIL_DECISION


def test_provenance_or_audit_failure_falsifies_r0(audit_module, records):
    attempt, bridge, g4, attempt_audit = copy.deepcopy(records)
    attempt_audit["checks"]["sealed_git_blobs_verified"] = False

    result = audit_module.reconcile_records(
        attempt,
        bridge,
        g4,
        attempt_audit,
        provenance_pass=False,
        created_utc="synthetic",
    )

    assert result["gates"]["R0"] == "fail"
    assert result["decision"] == audit_module.FAIL_DECISION


def test_manifest_hash_mutation_is_rejected(audit_module, tmp_path: Path, monkeypatch):
    result = tmp_path / "result.json"
    report = tmp_path / "report.md"
    independent = tmp_path / "audit.json"
    result.write_text("{}", encoding="utf-8")
    report.write_text("report", encoding="utf-8")
    independent.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(audit_module, "ROOT", tmp_path)
    monkeypatch.setattr(audit_module, "ATTEMPT_RESULT", tmp_path / "source.json")
    manifest = {
        "schema": (
            "scalar-memory-rotating-wave-horizon-infinity-branch-link-"
            "publication-v1"
        ),
        "execution_commit": "ee87ad931c4c8b27cff2cb44b445459ad4c79511",
        "protocol_sha256": (
            "598cdf73a7ccdfa45bd163165c2dd2be54d47209cacdb0b297ce0e05472132cd"
        ),
        "artifacts": [
            {"path": str(result.relative_to(tmp_path)), "role": "result-json", "sha256": "0" * 64},
            {"path": str(report.relative_to(tmp_path)), "role": "readable-report", "sha256": "0" * 64},
            {"path": str(independent.relative_to(tmp_path)), "role": "independent-audit", "sha256": "0" * 64},
        ]
    }

    assert audit_module.verify_manifest(manifest) is False


def test_git_blob_mutation_is_rejected(audit_module):
    first = next(iter(audit_module.EXPECTED_BLOBS))

    def blob(path):
        if path == first:
            return "0" * 40
        return audit_module.EXPECTED_BLOBS[path]

    assert audit_module.verify_git_blobs(blob) is False


def test_import_has_no_top_level_execution():
    source = SCRIPT.read_text(encoding="utf-8")

    assert "if __name__ == \"__main__\":" in source
    assert not (ROOT / "reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_infinity_endpoint_lemma_reconciliation_2026-10-01.json").exists()
