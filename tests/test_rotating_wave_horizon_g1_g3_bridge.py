from __future__ import annotations

import copy
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


def _load_gate():
    spec = importlib.util.spec_from_file_location("g1_g3_bridge_under_test", GATE_PATH)
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


def test_root_panel_requires_cross_inclusion_not_only_overlap() -> None:
    gate = _load_gate()
    payload = gate.contract_witness()
    panel = payload["finite_branch"]["root_panels"][2]
    assert panel["inner_intersection"] is not None
    panel["inner_certificate_80"]["krawczyk_image"][0] = ["2", "3"]
    panel["cross_80_inner_in_120_outer"] = True
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
