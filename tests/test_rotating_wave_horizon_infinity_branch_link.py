from __future__ import annotations

import copy
from decimal import Decimal, localcontext
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_gate.py"
)
AUDITOR_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_result_audit.py"
)


def _load_gate():
    specification = importlib.util.spec_from_file_location(
        "infinity_branch_link_gate_under_test", GATE_PATH
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@pytest.fixture
def gate():
    return _load_gate()


@pytest.fixture
def auditor():
    specification = importlib.util.spec_from_file_location(
        "infinity_branch_link_auditor_under_test", AUDITOR_PATH
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _authorization():
    return {
        "authorization_id": "00000000-0000-4000-8000-000000000001",
        "ci_run_id": 123,
        "governance_sha256": "a" * 64,
        "implementation_revision": "b" * 40,
        "receipt_path": "synthetic-receipt.json",
        "receipt_sha256": "c" * 64,
        "upstream_revision": "d" * 40,
    }


def _box(root, width="1e-10"):
    with localcontext() as context:
        context.prec = 200
        half_width = Decimal(width)
        return {
            coordinate: [
                format(Decimal(value) - half_width, "f"),
                format(Decimal(value) + half_width, "f"),
            ]
            for coordinate, value in zip(("radius", "theta"), root, strict=True)
        }


def _sealed(gate):
    root = ["0.95", "0.015"]
    box = _box(root)
    image = [[root[0], root[0]], [root[1], root[1]]]
    bounds = [
        {
            "precision_dps": precision,
            **gate._transfer_gate().tail_bounds(
                horizon=3600, precision_dps=precision
            ),
        }
        for precision in gate.PRECISIONS
    ]
    return {
        "files": [
            {"role": role, "path": path, "sha256": digest}
            for role, path, digest in gate.SEALED_FILES
        ],
        "bridge_root": list(root),
        "g4_finite_root": list(root),
        "bridge_endpoint_pass": True,
        "tail_bounds": bounds,
        "g4_tail_boxes": [copy.deepcopy(box), copy.deepcopy(box)],
        "g4_tail_images": [copy.deepcopy(image), copy.deepcopy(image)],
    }


def _panel(root, bounds, precision, *, shift="0", regular=True):
    box = _box(root)
    with localcontext() as context:
        context.prec = 200
        shifted = [format(Decimal(value) + Decimal(shift), "f") for value in root]
    zero = ["0", "0"]
    row_bound = ["0", "0"] if regular else ["1", "1"]
    gates = {
        "physical_domain": True,
        "inverse_nonsingular": True,
        "function_box_contains_zero": True,
        "krawczyk_strict_interior": True,
        "uniform_regularity": regular,
    }
    return {
        "precision_dps": precision,
        "scale_interval": ["0", "1"],
        "center": list(root),
        "box": box,
        "tail_bounds": copy.deepcopy(bounds),
        "jacobian_box": [[zero, zero], [zero, zero]],
        "inverse_point_jacobian": [["1", "0"], ["0", "1"]],
        "preconditioned_jacobian_defect": [[zero, zero], [zero, zero]],
        "regularity_row_sum_bounds": [row_bound, row_bound],
        "regularity_infinity_norm_upper": row_bound[1],
        "krawczyk_image": [
            [shifted[0], shifted[0]],
            [shifted[1], shifted[1]],
        ],
        "gates": gates,
        "pass": all(gates.values()),
    }


def _payload(gate, *, panel_factory=None, sealed=None):
    sealed = sealed or _sealed(gate)
    calls = []

    def panel_fn(*, precision_dps, root, bounds):
        calls.append((precision_dps, root, copy.deepcopy(bounds)))
        factory = panel_factory or _panel
        return factory(root, bounds, precision_dps)

    payload = gate.run_contract(
        execution_commit="e" * 40,
        authorization=_authorization(),
        sealed_inputs=sealed,
        panel_fn=panel_fn,
        created_utc="2026-09-29T00:00:00+00:00",
    )
    return payload, calls


def test_uniform_contract_passes_only_two_fixed_precision_panels(gate):
    payload, calls = _payload(gate)

    assert [call[0] for call in calls] == [120, 160]
    assert payload["classification"]["decision"] == gate.PASS_DECISION
    assert payload["classification"]["gates"] == {
        name: "pass" for name in ("U0", "U1", "U2", "U3", "U4", "U5")
    }


def test_uniform_contract_stops_after_failed_regularity(gate):
    def failed(root, bounds, precision):
        return _panel(root, bounds, precision, regular=False)

    payload, calls = _payload(gate, panel_factory=failed)

    assert [call[0] for call in calls] == [120]
    assert payload["homotopy"]["panels"][1] is None
    assert payload["classification"]["gates"]["U3"] == "inconclusive"
    assert payload["classification"]["decision"] == gate.INCONCLUSIVE_DECISION


def test_disjoint_precision_images_are_inconclusive(gate):
    def disjoint(root, bounds, precision):
        shift = "-5e-11" if precision == 120 else "5e-11"
        return _panel(root, bounds, precision, shift=shift)

    payload, _ = _payload(gate, panel_factory=disjoint)

    assert payload["homotopy"]["overlap"] is False
    assert payload["classification"]["gates"]["U5"] == "inconclusive"


def test_endpoint_mismatch_is_inconclusive_not_a_false_link(gate):
    sealed = _sealed(gate)
    sealed["bridge_root"][0] = "0.9500000000000000001"
    payload, _ = _payload(gate, sealed=sealed)

    assert payload["homotopy"]["endpoint_binding"]["pass"] is False
    assert payload["classification"]["gates"]["U4"] == "inconclusive"


def test_validator_rejects_inward_regularity_and_false_decision(gate):
    payload, _ = _payload(gate)
    inward = copy.deepcopy(payload)
    inward["homotopy"]["panels"][0]["preconditioned_jacobian_defect"][0][0] = [
        "-0.1",
        "0.1",
    ]
    with pytest.raises(ValueError, match="inward regularity"):
        gate.validate_payload(inward, sealed_reference=payload["sealed_inputs"])

    false_decision = copy.deepcopy(payload)
    false_decision["homotopy"]["overlap"] = False
    with pytest.raises(ValueError, match="overlap mismatch"):
        gate.validate_payload(
            false_decision, sealed_reference=payload["sealed_inputs"]
        )


def test_validator_rejects_sealed_hash_and_scale_mutations(gate):
    payload, _ = _payload(gate)
    sealed_hash = copy.deepcopy(payload)
    sealed_hash["sealed_inputs"]["files"][0]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="sealed_inputs.files"):
        gate.validate_payload(
            sealed_hash, sealed_reference=sealed_hash["sealed_inputs"]
        )

    scale = copy.deepcopy(payload)
    scale["homotopy"]["panels"][0]["scale_interval"] = ["0.1", "1"]
    with pytest.raises(ValueError, match="constant scale_interval"):
        gate.validate_payload(scale, sealed_reference=payload["sealed_inputs"])

    sealed_snapshot = copy.deepcopy(payload)
    sealed_snapshot["sealed_inputs"]["g4_finite_root"][0] = "0.96"
    with pytest.raises(ValueError, match="Git-blob snapshot"):
        gate.validate_payload(
            sealed_snapshot, sealed_reference=payload["sealed_inputs"]
        )


def test_real_sealed_inputs_are_hash_bound_without_target_evaluation(gate):
    sealed = gate.load_sealed_inputs()

    assert sealed["bridge_root"] == sealed["g4_finite_root"]
    assert sealed["bridge_endpoint_pass"] is True
    assert [row["precision_dps"] for row in sealed["tail_bounds"]] == [120, 160]


def test_independent_auditor_reconstructs_synthetic_pass(gate, auditor):
    payload, _ = _payload(gate)
    result_bytes = (
        gate.json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")
    report_bytes = gate.render_report(payload).encode("utf-8")

    audit = auditor.audit_payload_bytes(
        result_bytes,
        report_bytes,
        sealed_reference=payload["sealed_inputs"],
    )

    assert audit["audited_decision"] == gate.PASS_DECISION
    assert audit["verdict"] == "g-infinity-branch-link-independent-audit-agrees"
    assert all(audit["checks"].values())


def test_independent_auditor_rejects_inward_regularity(gate, auditor):
    payload, _ = _payload(gate)
    payload["homotopy"]["panels"][0]["preconditioned_jacobian_defect"][0][0] = [
        "-0.1",
        "0.1",
    ]
    result_bytes = (
        gate.json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")

    with pytest.raises(ValueError, match="inward regularity"):
        auditor.audit_payload_bytes(
            result_bytes,
            gate.render_report(payload).encode("utf-8"),
            sealed_reference=payload["sealed_inputs"],
        )


def test_auditor_does_not_import_production_gate_or_numeric_backends():
    source = AUDITOR_PATH.read_text(encoding="utf-8")

    assert "import mpmath" not in source
    assert "import numpy" not in source
    assert "import scipy" not in source
    assert "infinity_branch_link_gate" not in source


def test_independent_auditor_reextracts_the_same_sealed_snapshot(gate, auditor):
    assert auditor._sealed_snapshot_from_git() == gate.load_sealed_inputs()


def test_independent_auditor_binds_actual_snapshot_with_mocked_panels(gate, auditor):
    sealed = gate.load_sealed_inputs()

    def existing_boxes(root, bounds, precision):
        index = gate.PRECISIONS.index(precision)
        panel = _panel(root, bounds, precision)
        panel["box"] = copy.deepcopy(sealed["g4_tail_boxes"][index])
        panel["krawczyk_image"] = copy.deepcopy(sealed["g4_tail_images"][index])
        return panel

    payload, _ = _payload(gate, panel_factory=existing_boxes, sealed=sealed)
    result_bytes = (
        gate.json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")

    audit = auditor.audit_payload_bytes(
        result_bytes, gate.render_report(payload).encode("utf-8")
    )

    assert audit["verdict"] == "g-infinity-branch-link-independent-audit-agrees"


def test_manifest_last_publication_round_trip_with_mocked_panels(
    gate, auditor, tmp_path: Path, monkeypatch
):
    sealed = gate.load_sealed_inputs()

    def existing_boxes(root, bounds, precision):
        index = gate.PRECISIONS.index(precision)
        panel = _panel(root, bounds, precision)
        panel["box"] = copy.deepcopy(sealed["g4_tail_boxes"][index])
        panel["krawczyk_image"] = copy.deepcopy(sealed["g4_tail_images"][index])
        return panel

    result = tmp_path / gate.RESULT.relative_to(gate.ROOT)
    audit_path = tmp_path / gate.AUDIT.relative_to(gate.ROOT)
    monkeypatch.setattr(gate, "ROOT", tmp_path)
    monkeypatch.setattr(gate, "RESULT", result)
    monkeypatch.setattr(gate, "REPORT", result.with_suffix(".md"))
    monkeypatch.setattr(gate, "MANIFEST", result.with_suffix(".publication.json"))
    monkeypatch.setattr(gate, "AUDIT", audit_path)
    payload, _ = _payload(gate, panel_factory=existing_boxes, sealed=sealed)

    gate.publish(payload, audit_fn=auditor.audit_payload_bytes)
    verification = auditor.verify_publication(root=tmp_path)

    assert verification["verdict"] == (
        "g-infinity-branch-link-independent-audit-agrees"
    )
    assert gate.MANIFEST.exists()
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        gate.publish(payload, audit_fn=auditor.audit_payload_bytes)
