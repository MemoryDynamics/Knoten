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
    payload["finite_branch"]["homotopies"][3] = None
    payload["finite_branch"]["drift"]["center_diagnostics"][1] = None
    payload["finite_branch"]["drift"]["interval_upper_bounds"][1] = None
    payload["finite_branch"]["drift"]["pass"] = False
    payload["endpoint_links"][1] = None
    payload["classification"]["gates"].update(
        {
            "G1F": "inconclusive",
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

    def direct_replay(self) -> bool:
        self.calls.append(("direct_replay",))
        return True

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
