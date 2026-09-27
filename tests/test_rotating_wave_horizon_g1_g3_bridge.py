from __future__ import annotations

import copy
from decimal import Decimal
import importlib.util
import json
from pathlib import Path

import pytest

from emergenz_knoten.strict_json_contract import validate_payload


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g1_g3_bridge_result_schema_v1.json"
)
GATE_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g1_g3_bridge_gate.py"
)
AUDIT_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g1_g3_bridge_result_audit.py"
)


def _load_gate():
    spec = importlib.util.spec_from_file_location("g1_g3_bridge_under_test", GATE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_audit():
    spec = importlib.util.spec_from_file_location("g1_g3_audit_under_test", AUDIT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def test_bridge_schema_is_strict_and_self_contained() -> None:
    contract = _schema()
    assert set(contract) == {"arrays", "constants", "enums", "objects", "root", "schema"}
    assert contract["root"] == "object:payload"
    assert contract["constants"]["horizons"] == [600, 900, 1200, 1500, 1800, 2400, 3600]
    assert contract["arrays"]["sealed_files"]["length"] == 5


def test_contract_witness_validates_and_extra_fields_fail() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    gate.validate_result(payload)
    validate_payload(payload, _schema())
    broken = copy.deepcopy(payload)
    broken["unexpected"] = True
    with pytest.raises(ValueError):
        gate.validate_result(broken)
    broken = copy.deepcopy(payload)
    broken["publication"]["manifest_published_last"] = False
    with pytest.raises(ValueError, match="manifest_published_last"):
        gate.validate_result(broken)


def test_root_panel_requires_cross_inclusion_not_only_overlap() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    panel = payload["finite_branch"]["root_panels"][2]
    assert panel["inner_intersection"] is not None
    panel["cross_80_inner_in_120_outer"] = False
    with pytest.raises(ValueError, match="cross inclusion"):
        gate.validate_result(payload)


def test_endpoint_link_booleans_are_reconstructed_from_intervals() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    link = payload["endpoint_links"][0]
    link["component_inner_image"][0] = ["2", "3"]
    link["component_inner_in_bridge_80_outer"] = True
    link["pass"] = True
    with pytest.raises(ValueError, match="endpoint"):
        gate.validate_result(payload)


def test_sealed_component_hash_drift_fails_before_decision() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    payload["sealed_components"]["files"][0]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="sealed"):
        gate.validate_result(payload)


def test_g0_replay_is_reconstructed_from_signed_primitive_values() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    row = payload["finite_branch"]["direct_replays"][2]
    row["radial_residual"] = "1e-40"
    row["residual_maximum"] = "1e-40"
    with pytest.raises(ValueError, match="residual gate"):
        gate.validate_result(payload)


def test_g6_age_hash_and_mutation_detection_are_reconstructed() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    payload["controls"]["circular_cases"][0][
        "observed_age_history_sha256"
    ] = "f" * 64
    with pytest.raises(ValueError, match="circular_cases"):
        gate.validate_result(payload)
    payload = gate.contract_witness()
    payload["controls"]["mutations"][0]["new_point_relative_error"] = 0.0
    payload["controls"]["mutations"][0]["complete_state_relative_error"] = 0.0
    with pytest.raises(ValueError, match="mutations"):
        gate.validate_result(payload)


def test_registered_g6_controls_run_from_frozen_histories() -> None:
    gate = _load_gate()
    controls = gate.registered_controls_backend_record()
    assert controls["pass"] is True
    assert [row["case_id"] for row in controls["circular_cases"]] == [
        "noncircle-H17",
        "noncircle-H257",
        "anchor-H600",
        "anchor-H900",
        "anchor-H1200",
        "anchor-H1500",
        "anchor-H1800",
        "anchor-H2400",
        "anchor-H3600",
    ]
    assert all(
        row["expected_age_history_sha256"]
        == row["observed_age_history_sha256"]
        for row in controls["circular_cases"]
    )
    assert all(row["detected"] for row in controls["mutations"])


def test_sealed_loader_hashes_and_extracts_only_registered_endpoint_roots() -> None:
    gate = _load_gate()
    sealed = gate.load_sealed_components()
    assert sealed["g4_root"]["horizon"] == 3600
    assert sealed["g5_root"]["horizon"] == 2400
    assert set(sealed) == {"files", "g4_root", "g5_root"}


def test_sealed_loader_reads_canonical_git_blobs_not_checkout_bytes(
    monkeypatch,
) -> None:
    gate = _load_gate()

    def forbidden(self):
        raise AssertionError("sealed loader read platform-dependent checkout bytes")

    monkeypatch.setattr(Path, "read_bytes", forbidden)
    sealed = gate.load_sealed_components()
    audit = next(row for row in sealed["files"] if row["role"] == "g4-audit")
    assert audit["sha256"] == (
        "e83309992fe8b964c507930664f557367a50d87d32aedf7bf39ecbe1bb346d19"
    )


def test_sealed_loader_fails_before_parse_on_registered_hash_drift(
    monkeypatch,
) -> None:
    gate = _load_gate()
    rows = list(gate.SEALED_FILES)
    rows[0] = (rows[0][0], rows[0][1], "0" * 64)
    monkeypatch.setattr(gate, "SEALED_FILES", tuple(rows))
    with pytest.raises(ValueError, match="hash mismatch"):
        gate.load_sealed_components()


def test_direct_replay_backend_does_not_call_root_or_interval_solver(
    monkeypatch,
) -> None:
    gate = _load_gate()
    reused = gate._transfer_gate()
    g4 = json.loads(
        (
            ROOT
            / "reports/dynamics/rotation/"
            "scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.json"
        ).read_text(encoding="utf-8")
    )
    newton = g4["finite_root"]["newton"]

    def forbidden(*args, **kwargs):
        raise AssertionError("direct replay called a root or interval solver")

    monkeypatch.setattr(reused, "refine_rotating_wave_root", forbidden)
    monkeypatch.setattr(reused, "certify_rotating_wave_box", forbidden)
    row = reused.finite_sum_replay_backend_record(
        horizon=3600,
        root=(newton["radius"], newton["theta"]),
    )
    assert row["pass"] is True
    assert Decimal(row["residual_maximum"]) <= Decimal("1e-45")


def test_registered_bridge_backend_has_no_g4_or_g5_execution_methods() -> None:
    gate = _load_gate()
    backend = gate.RegisteredBridgeBackend()
    assert not hasattr(backend, "tail_certificate_panel")
    assert not hasattr(backend, "arnoldi_panel")


def test_independent_auditor_accepts_target_free_composition() -> None:
    gate = _load_gate()
    audit = _load_audit()
    template = gate.contract_witness()
    payload = gate.orchestrate_bridge(
        backend=_SyntheticBridgeBackend(template),
        identity=template["identity"],
        publication=template["publication"],
        sealed_components=gate.load_sealed_components(),
    )
    report = audit.audit_payload(payload)
    assert report["verdict"] == "g1-g3-bridge-independent-audit-agrees"
    assert report["decision"] == "sealed-component-endpoint-mismatch"


def test_independent_auditor_rejects_replay_and_endpoint_mutations() -> None:
    gate = _load_gate()
    audit = _load_audit()
    template = gate.contract_witness()
    payload = gate.orchestrate_bridge(
        backend=_SyntheticBridgeBackend(template),
        identity=template["identity"],
        publication=template["publication"],
        sealed_components=gate.load_sealed_components(),
    )
    broken = copy.deepcopy(payload)
    broken["finite_branch"]["direct_replays"][2]["residual_maximum"] = "1"
    with pytest.raises(ValueError, match="replay reconstruction"):
        audit.audit_payload(broken)
    broken = copy.deepcopy(payload)
    broken["endpoint_links"][0]["pass"] = True
    with pytest.raises(ValueError, match="endpoint"):
        audit.audit_payload(broken)


def test_manifest_last_publication_round_trip_is_independently_audited(
    tmp_path: Path, monkeypatch
) -> None:
    gate = _load_gate()
    audit = _load_audit()
    template = gate.contract_witness()
    template["publication"] = {
        "artifacts": [
            {"path": "result.json", "role": "result-json"},
            {"path": "result.md", "role": "readable-report"},
        ],
        "auditor_output_path": "result.audit.json",
        "manifest_path": "result.publication.json",
        "manifest_published_last": True,
    }
    payload = gate.orchestrate_bridge(
        backend=_SyntheticBridgeBackend(template),
        identity=template["identity"],
        publication=template["publication"],
        sealed_components=gate.load_sealed_components(),
    )
    audit_report = audit.audit_payload(payload)
    writes = []
    original = gate._atomic_write_bytes

    def recording_write(path, content):
        writes.append(Path(path).name)
        original(path, content)

    monkeypatch.setattr(gate, "_atomic_write_bytes", recording_write)
    gate.publish_bridge_result(payload, audit_report, repository_root=tmp_path)
    assert writes == [
        "result.json",
        "result.md",
        "result.audit.json",
        "result.publication.json",
    ]
    verified = audit.audit_publication(
        tmp_path / "result.publication.json",
        publication_root=tmp_path,
        evidence_root=ROOT,
    )
    assert verified["publication_verified"] is True
    with pytest.raises(FileExistsError):
        gate.publish_bridge_result(payload, audit_report, repository_root=tmp_path)


def test_publication_audit_rejects_post_manifest_artifact_mutation(
    tmp_path: Path,
) -> None:
    gate = _load_gate()
    audit = _load_audit()
    template = gate.contract_witness()
    template["publication"] = {
        "artifacts": [
            {"path": "result.json", "role": "result-json"},
            {"path": "result.md", "role": "readable-report"},
        ],
        "auditor_output_path": "result.audit.json",
        "manifest_path": "result.publication.json",
        "manifest_published_last": True,
    }
    payload = gate.orchestrate_bridge(
        backend=_SyntheticBridgeBackend(template),
        identity=template["identity"],
        publication=template["publication"],
        sealed_components=gate.load_sealed_components(),
    )
    gate.publish_bridge_result(
        payload, audit.audit_payload(payload), repository_root=tmp_path
    )
    (tmp_path / "result.md").write_text("tampered\n", encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        audit.audit_publication(
            tmp_path / "result.publication.json",
            publication_root=tmp_path,
            evidence_root=ROOT,
        )


@pytest.mark.parametrize(
    ("updates", "decision"),
    [
        ({"G0": "fail"}, "g1-g3-bridge-experiment-invalid"),
        ({"local_branch_excluded": True}, "registered-local-horizon-branch-loss"),
        ({"G1F": "inconclusive"}, "g1-g3-bridge-inconclusive"),
        ({"G3": "fail"}, "rotating-wave-horizon-branch-drift"),
        ({"H2400_link": "fail"}, "sealed-component-endpoint-mismatch"),
        ({}, "rotating-wave-root-branch-connected-with-h2400-local-stability-support"),
    ],
)
def test_decision_precedence(updates: dict[str, object], decision: str) -> None:
    gate = _load_gate()
    gates = {
        "G0": "pass",
        "G1F": "pass",
        "G1R": "pass",
        "G2F": "pass",
        "G2R": "pass",
        "G3": "pass",
        "G4": "pass",
        "G5": "pass",
        "G6": "pass",
        "H2400_link": "pass",
        "H3600_link": "pass",
        "local_branch_excluded": False,
    }
    gates.update(updates)
    assert gate.classify_bridge(gates)["decision"] == decision


def test_lower_tail_loss_is_not_in_contract() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    payload["finite_branch"]["lower_tail_status"] = "lower-tail-stress-loss"
    with pytest.raises(ValueError):
        gate.validate_result(payload)


def test_incomplete_forward_prefix_is_an_honest_inconclusive_record() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    payload["finite_branch"]["root_panels"][6] = None
    payload["finite_branch"]["direct_replays"][6] = None
    payload["finite_branch"]["direct_replay_pass"] = False
    payload["finite_branch"]["homotopies"][3] = None
    payload["finite_branch"]["drift"]["center_diagnostics"][1] = None
    payload["finite_branch"]["drift"]["interval_upper_bounds"][1] = None
    payload["finite_branch"]["drift"]["pass"] = False
    payload["endpoint_links"][1] = None
    payload["classification"]["gates"].update(
        {
            "G1F": "inconclusive",
            "G0": "inconclusive",
            "G2F": "inconclusive",
            "G3": "inconclusive",
            "H3600_link": "inconclusive",
        }
    )
    payload["classification"]["decision"] = "g1-g3-bridge-inconclusive"
    payload["classification"]["precedence_rank"] = 3
    gate.validate_result(payload)


def test_homotopy_pass_rejects_wrong_registered_s_interval() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    payload["finite_branch"]["homotopies"][0]["slabs"][1]["s_interval"] = [
        "0",
        "1",
    ]
    with pytest.raises(ValueError, match="s_interval"):
        gate.validate_result(payload)


def test_drift_pass_is_reconstructed_from_root_intervals() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    payload["finite_branch"]["drift"]["interval_upper_bounds"][1][
        "upper_bound"
    ] = 1.0
    payload["finite_branch"]["drift"]["pass"] = True
    with pytest.raises(ValueError, match="drift"):
        gate.validate_result(payload)


def test_g6_pass_is_reconstructed_from_errors_and_horizon_order() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    payload["controls"]["circular_cases"][0]["complete_state_relative_error"] = (
        5e-14
    )
    payload["controls"]["circular_cases"][0]["pass"] = True
    payload["controls"]["pass"] = True
    with pytest.raises(ValueError, match="controls"):
        gate.validate_result(payload)


def test_false_local_exclusion_requires_complete_partition() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    panel = payload["finite_branch"]["root_panels"][2]
    radius = Decimal(panel["newton_120"]["radius"])
    theta = Decimal(panel["newton_120"]["theta"])
    radius_domain = [
        format(radius - Decimal("0.02"), "f"),
        format(radius + Decimal("0.02"), "f"),
    ]
    theta_domain = [
        format(theta - Decimal("0.002"), "f"),
        format(theta + Decimal("0.002"), "f"),
    ]
    payload["finite_branch"]["exclusions"][0] = {
        "from_horizon": 1200,
        "leaves": [
            {
                "box": {
                    "radius": radius_domain,
                    "theta": [theta_domain[0], format(theta, "f")],
                },
                "classification": "residual-excluded",
                "depth": 1,
                "krawczyk_image": None,
                "residual_box": [["1", "2"], ["-1", "1"]],
                "strict_interior": None,
            }
        ],
        "local_domain": {
            "radius": radius_domain,
            "theta": theta_domain,
        },
        "max_depth": 20,
        "status": "all-residual-excluded",
        "to_horizon": 1500,
    }
    payload["classification"]["gates"]["local_branch_excluded"] = True
    payload["classification"]["decision"] = "registered-local-horizon-branch-loss"
    payload["classification"]["precedence_rank"] = 2
    with pytest.raises(ValueError, match="partition"):
        gate.validate_result(payload)


class _SyntheticBridgeBackend:
    def __init__(self, template: dict, *, fail_horizon: int | None = None) -> None:
        self.template = template
        self.fail_horizon = fail_horizon
        self.calls: list[tuple] = []

    def finite_root_panel(
        self, *, horizon: int, precision_dps: int, start: tuple[str, str]
    ) -> dict | None:
        self.calls.append(("root", horizon, precision_dps, start))
        if horizon == self.fail_horizon:
            return None
        panel = self.template["finite_branch"]["root_panels"]
        row = panel[[600, 900, 1200, 1500, 1800, 2400, 3600].index(horizon)]
        return copy.deepcopy(
            {
                "inner_certificate": row[f"inner_certificate_{precision_dps}"],
                "newton": row[f"newton_{precision_dps}"],
                "outer_certificate": row[f"outer_certificate_{precision_dps}"],
            }
        )

    def finite_sum_replay(
        self, *, horizon: int, root: tuple[str, str]
    ) -> dict:
        self.calls.append(("replay", horizon, root))
        row = self.template["finite_branch"]["direct_replays"][
            [600, 900, 1200, 1500, 1800, 2400, 3600].index(horizon)
        ]
        return copy.deepcopy(row)

    def homotopy_edge(
        self,
        *,
        from_horizon: int,
        to_horizon: int,
        from_root: tuple[str, str],
        to_root: tuple[str, str],
    ) -> dict:
        self.calls.append(
            ("homotopy", from_horizon, to_horizon, from_root, to_root)
        )
        for row in self.template["finite_branch"]["homotopies"]:
            if (row["from_horizon"], row["to_horizon"]) == (
                from_horizon,
                to_horizon,
            ):
                return copy.deepcopy(row)
        raise AssertionError("unregistered synthetic edge")

    def local_branch_exclusion(self, **kwargs) -> None:
        self.calls.append(("exclusion", kwargs["from_horizon"], kwargs["to_horizon"]))
        return None

    def controls(self) -> dict:
        self.calls.append(("controls",))
        return copy.deepcopy(self.template["controls"])

    def tail_certificate_panel(self, **kwargs):
        raise AssertionError("G1--G3 bridge must not rerun G4")

    def arnoldi_panel(self, **kwargs):
        raise AssertionError("G1--G3 bridge must not rerun G5")


def test_orchestrator_composes_finite_branch_without_rerunning_g4_or_g5() -> None:
    gate = _load_gate()
    template = gate.contract_witness()
    backend = _SyntheticBridgeBackend(template)
    payload = gate.orchestrate_bridge(
        backend=backend,
        identity=template["identity"],
        publication=template["publication"],
        sealed_components=template["sealed_components"],
    )
    assert payload["classification"]["decision"] == (
        "rotating-wave-root-branch-connected-with-h2400-local-stability-support"
    )
    assert sum(call[0] == "root" for call in backend.calls) == 14
    assert sum(call[0] == "homotopy" for call in backend.calls) == 6
    assert backend.calls[-1] == ("controls",)


def test_orchestrator_preserves_inconclusive_prefix_after_root_failure() -> None:
    gate = _load_gate()
    template = gate.contract_witness()
    backend = _SyntheticBridgeBackend(template, fail_horizon=3600)
    payload = gate.orchestrate_bridge(
        backend=backend,
        identity=template["identity"],
        publication=template["publication"],
        sealed_components=template["sealed_components"],
    )
    assert payload["finite_branch"]["root_panels"][6] is None
    assert payload["finite_branch"]["homotopies"][3] is None
    assert payload["endpoint_links"][1] is None
    assert payload["classification"]["decision"] == "g1-g3-bridge-inconclusive"
    assert ("exclusion", 2400, 3600) in backend.calls
