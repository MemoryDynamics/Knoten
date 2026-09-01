from __future__ import annotations

import ast
from pathlib import Path

from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p5d_mutual_center_gate as runner,
)
from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p5d_mutual_center_result_audit as audit,
)


def _payload(*, additive: bool = False) -> dict[str, object]:
    steps = list(
        range(
            0,
            runner.THRESHOLDS.active_updates + 1,
            runner.THRESHOLDS.sample_every,
        )
    )
    off = []
    active = []
    for distance, phase, chirality_a, chirality_b in runner.expected_base_keys():
        initial_distance = distance * runner.CANDIDATE.radius
        center_a = complex(-0.5 * initial_distance, 0.0)
        center_b = complex(0.5 * initial_distance, 0.0)
        control_trace = [
            {
                "step": step,
                "center_a": runner._pair(center_a),
                "center_b": runner._pair(center_b),
                "separation": runner._pair(center_a - center_b),
            }
            for step in steps
        ]
        hash_a = f"a-{distance}-{phase}-{chirality_a}-{chirality_b}"
        hash_b = f"b-{distance}-{phase}-{chirality_a}-{chirality_b}"
        off.append(
            {
                "distance_fraction": distance,
                "phase_index": phase,
                "chirality_a": chirality_a,
                "chirality_b": chirality_b,
                "mode": "off",
                "initial_distance": initial_distance,
                "completed": True,
                "finite": True,
                "final_history_sha256_a": hash_a,
                "final_history_sha256_b": hash_b,
                "trace": control_trace,
                "ledger_gates": {"off": True},
                "loop_gates": {"off": True},
            }
        )
        for kappa in runner.KAPPAS:
            for sign in runner.SIGNS:
                one = 0.003 if kappa == "low" else 0.006
                excess = 0.0 if additive else (0.00003 if kappa == "low" else 0.00012)
                reciprocal = 2.0 * one - sign * excess
                for mode in runner.DIRECTIONS:
                    longitudinal = reciprocal if mode == "reciprocal" else one
                    final_delta = sign * longitudinal * initial_distance
                    trace = []
                    for step in steps:
                        delta = final_delta * step / runner.THRESHOLDS.active_updates
                        if mode == "a_to_b":
                            moved_a, moved_b = center_a, center_b - delta
                        elif mode == "b_to_a":
                            moved_a, moved_b = center_a + delta, center_b
                        else:
                            moved_a = center_a + 0.5 * delta
                            moved_b = center_b - 0.5 * delta
                        trace.append(
                            {
                                "step": step,
                                "center_a": runner._pair(moved_a),
                                "center_b": runner._pair(moved_b),
                                "separation": runner._pair(moved_a - moved_b),
                            }
                        )
                    active.append(
                        {
                            "distance_fraction": distance,
                            "phase_index": phase,
                            "chirality_a": chirality_a,
                            "chirality_b": chirality_b,
                            "kappa_name": kappa,
                            "sign": sign,
                            "mode": mode,
                            "coupling": sign * runner.KAPPA_VALUES[kappa],
                            "initial_distance": initial_distance,
                            "completed": True,
                            "finite": True,
                            "source_bitwise_native": True,
                            "final_history_sha256_a": (
                                hash_a if mode == "a_to_b" else f"active-a-{kappa}-{sign}-{mode}"
                            ),
                            "final_history_sha256_b": (
                                hash_b if mode == "b_to_a" else f"active-b-{kappa}-{sign}-{mode}"
                            ),
                            "trace": trace,
                            "ledger_gates": {"synthetic": True},
                            "loop_gates": {"synthetic": True},
                        }
                    )
    registration = runner.panel_registration(off, active)
    response = runner.response_controls(off, active)
    decision, gates = runner.classify_panel(
        registration=registration,
        channel_off_arms=off,
        active_arms=active,
        response=response,
    )
    return {
        "panel": {"channel_off_arms": off, "active_arms": active},
        "registration": registration,
        "response": response,
        "decision_gates": gates,
        "decision": decision,
    }


def test_p5d_auditor_is_independent_of_target_runner_and_numeric_stack() -> None:
    tree = ast.parse(Path(audit.__file__).read_text(encoding="utf-8"))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    assert not any("scalar_memory_loop_p5d_mutual_center_gate" in name for name in imports)
    assert not any(name.split(".")[0] in {"numpy", "scipy", "mpmath"} for name in imports)


def test_p5d_independent_auditor_reconstructs_complete_synthetic_pass() -> None:
    result = audit.audit_payload(_payload())
    assert result["decision"] == "p5d-independent-audit-agrees"
    assert result["recomputed_decision"] == "p5d-mutual-center-response-pass"
    assert result["differences"] == []
    assert all(result["registration_gates"].values())
    assert all(result["response"]["gates"].values())


def test_p5d_independent_auditor_identifies_exact_superposition() -> None:
    result = audit.audit_payload(_payload(additive=True))
    assert result["decision"] == "p5d-independent-audit-agrees"
    assert result["recomputed_decision"] == "p5d-independent-superposition"
    assert result["response"]["gates"]["excess_resolved"] is False


def test_p5d_independent_auditor_detects_source_contamination() -> None:
    contaminated = _payload()
    arm = next(
        row
        for row in contaminated["panel"]["active_arms"]
        if row["mode"] == "a_to_b"
    )
    arm["final_history_sha256_a"] = "contaminated"
    contaminated["decision"] = "p5d-directional-causality-fail"
    contaminated["decision_gates"]["directional_causality"] = False
    result = audit.audit_payload(contaminated)
    assert result["recomputed_decision"] == "p5d-directional-causality-fail"
    assert result["decision"] == "p5d-independent-audit-agrees"


def test_p5d_auditor_recomputes_numeric_reducers_and_ledger_fail() -> None:
    maxima = {
        "center_local_a": 0.0,
        "center_local_b": 0.0,
        "center_envelope_a": 0.5,
        "center_envelope_b": 0.5,
        "force_balance": 0.0,
        "midpoint_a": 0.0,
        "midpoint_b": 0.0,
        "work_split_a": 0.0,
        "work_split_b": 0.0,
        "pair_ledger": 0.0,
    }
    row = {
        "mode": "reciprocal",
        "kappa_name": "high",
        "sign": 1,
        "ledger_evaluation_count": 2_000,
        "shape_evaluation_count": 2_001,
        "ledger_maxima": maxima,
        "ledger_cumulative": {
            "work_split_a": 0.0,
            "work_split_b": 0.0,
            "pair_ledger": 0.0,
        },
        "ledger_scales": {"force": 1.0, "displacement": 1.0, "energy": 1.0},
        "high_precision_references": [{"pass": True}] * 3,
        "normal_metrology_operands": True,
        "minimum_mobility_dissipation": 0.0,
        "loop_summary": {
            "maximum_d0_a": 0.001,
            "maximum_d0_b": 0.001,
            "late_d0_a": 0.001,
            "late_d0_b": 0.001,
            "late_opposite_a": 0.8,
            "late_opposite_b": 0.8,
        },
        "phase_metrics": {"a": {"pass": True}, "b": {"pass": True}},
        "minimum_separation": 3.0 * audit.RADIUS,
        "maximum_center_response_fraction": 0.01,
    }
    ledger, loop = audit._recompute_arm_gates(row, strict_numeric=True)
    assert all(ledger.values())
    assert all(loop.values())
    row["ledger_evaluation_count"] = 1_999
    row["ledger_maxima"]["pair_ledger"] = 1.0e-6
    ledger, _ = audit._recompute_arm_gates(row, strict_numeric=True)
    assert ledger["complete_evaluation_count"] is False
    assert ledger["pair_ledger_step"] is False

    ledger = _payload()
    ledger["panel"]["active_arms"][0]["ledger_gates"]["synthetic"] = False
    ledger["decision"] = "p5d-ledger-or-reciprocity-fail"
    ledger["decision_gates"]["ledger_and_reciprocity"] = False
    result = audit.audit_payload(ledger)
    assert result["recomputed_decision"] == "p5d-ledger-or-reciprocity-fail"
    assert result["decision"] == "p5d-independent-audit-agrees"


def test_p5d_independent_auditor_rejects_stored_summary_and_incomplete_panel() -> None:
    corrupted = _payload()
    corrupted["response"]["gates"]["swap_covariance"] = False
    result = audit.audit_payload(corrupted)
    assert result["decision"] == "p5d-independent-audit-disagrees"
    assert "response.gates" in result["differences"]

    incomplete = _payload()
    incomplete["panel"]["active_arms"].pop()
    result = audit.audit_payload(incomplete)
    assert result["recomputed_decision"] == "p5d-inconclusive"
    assert result["registration_gates"]["active_count"] is False


def test_p5d_independent_audit_output_is_atomic_and_nonoverwriting(tmp_path: Path) -> None:
    output = tmp_path / "audit.json"
    audit._atomic_write(output, '{"complete": true}\n')
    assert output.read_text(encoding="utf-8") == '{"complete": true}\n'
    try:
        audit._atomic_write(output, "blocked")
    except RuntimeError as error:
        assert "refusing existing" in str(error)
    else:
        raise AssertionError("audit output overwrite was not rejected")
