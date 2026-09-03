from __future__ import annotations

import ast
import copy
import hashlib
import inspect
import json
import math
from pathlib import Path

import numpy as np
import pytest

from emergenz_knoten import mutual_center_coupling as kernel
from emergenz_knoten.orbit_center_actuator import candidate_orbit_center_readout
from emergenz_knoten.rotating_wave_stability_gate import RotatingWaveCandidate
from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p5d_mutual_center_gate as p5d,
)


def test_p5d_frozen_constants_panel_and_corrected_symmetry_maps() -> None:
    assert p5d.CANDIDATE.candidate_id == p5d.CANDIDATE_ID
    assert p5d.CANDIDATE.alpha == 0.01
    assert p5d.CANDIDATE.horizon == 1200
    assert p5d.CANDIDATE.eta == 0.15
    assert p5d.CANDIDATE.alpha * p5d.CANDIDATE.horizon == 12.0
    assert p5d.CANDIDATE.eta / p5d.CANDIDATE.alpha == 15.0
    assert p5d.PHASES == tuple((2 * index + 1) * math.pi / 8.0 for index in range(8))
    assert len(p5d.expected_base_keys()) == 64
    assert len(p5d.expected_active_keys()) == 768
    assert len(set(p5d.expected_base_keys())) == 64
    assert len(set(p5d.expected_active_keys())) == 768
    for key in p5d.expected_base_keys():
        assert p5d.reflection_key(p5d.reflection_key(key)) == key
        assert p5d.swap_half_turn_key(p5d.swap_half_turn_key(key)) == key
    assert p5d.reflection_key((3, 0, 1, -1)) == (3, 7, -1, 1)
    assert p5d.swap_half_turn_key((6, 0, 1, -1)) == (6, 3, -1, 1)
    assert p5d.swap_direction("a_to_b") == "b_to_a"
    assert p5d.swap_direction("b_to_a") == "a_to_b"
    assert p5d.swap_direction("reciprocal") == "reciprocal"


def test_p5d_static_initialization_has_distinct_arrays_and_measured_centers() -> None:
    for key in ((3, 0, 1, -1), (6, 7, -1, 1)):
        history_a, history_b, readout_a, readout_b = p5d._initial_pair(key)
        assert not np.shares_memory(history_a, history_b)
        center_a = kernel._loop_centers(history_a, readout=readout_a)[0]
        center_b = kernel._loop_centers(history_b, readout=readout_b)[0]
        expected = key[0] * p5d.CANDIDATE.radius
        assert abs(center_a + 0.5 * expected) < 2e-15
        assert abs(center_b - 0.5 * expected) < 2e-15
        assert abs(abs(center_a - center_b) - expected) < 4e-15
        assert readout_a.write_gain == pytest.approx(p5d.EXPECTED_WRITE_GAIN, abs=5e-16)
        assert p5d.CANDIDATE.alpha * readout_a.write_gain == pytest.approx(
            p5d.EXPECTED_MOBILITY, abs=5e-18
        )


def test_p5d_high_precision_midpoint_replay_passes_small_static_fixture() -> None:
    candidate = RotatingWaveCandidate(
        candidate_id="p5d-static-h17",
        radius=0.8,
        theta=0.19,
        alpha=0.08,
        horizon=17,
        memory_mass=1.0,
        eta=0.03,
        sigma_rep=1.0,
        sigma_att=2.5,
        amplitude_rep=1.0,
        amplitude_att=2.0,
    )
    ages = np.arange(candidate.horizon, dtype=float)
    history_a = np.column_stack((np.sin(0.31 * ages), np.cos(0.23 * ages)))
    history_b = np.column_stack((np.cos(0.17 * ages), -np.sin(0.29 * ages)))
    history_a += np.asarray([-1.5, 0.1])
    history_b += np.asarray([1.5, -0.1])
    readout_a = candidate_orbit_center_readout(candidate, chirality=1)
    readout_b = candidate_orbit_center_readout(candidate, chirality=-1)
    step = kernel.mutual_center_step(
        history_a,
        history_b,
        candidate_a=candidate,
        candidate_b=candidate,
        readout_a=readout_a,
        readout_b=readout_b,
        coupling=0.00125,
        mode="reciprocal",
    )
    reference = p5d._high_precision_reference(
        step,
        readout_a=readout_a,
        readout_b=readout_b,
        update=1,
    )
    assert reference["precision_dps"] == 80
    assert reference["pass"] is True
    assert reference["relative_tolerance"] == p5d.THRESHOLDS.force_relative


def _synthetic_panel() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    steps = list(
        range(0, p5d.THRESHOLDS.active_updates + 1, p5d.THRESHOLDS.sample_every)
    )
    off = []
    active = []
    for distance, phase_index, chirality_a, chirality_b in p5d.expected_base_keys():
        initial_distance = distance * p5d.CANDIDATE.radius
        base_a = complex(-0.5 * initial_distance, 0.0)
        base_b = complex(0.5 * initial_distance, 0.0)
        off_trace = [
            {
                "alignment_a": 0.0,
                "alignment_b": 0.0,
                "step": step,
                "center_a": p5d._pair(base_a),
                "center_b": p5d._pair(base_b),
                "d0_a": 0.0,
                "d0_b": 0.0,
                "opposite_d0_a": 1.0,
                "opposite_d0_b": 1.0,
                "separation": p5d._pair(base_a - base_b),
            }
            for step in steps
        ]
        off.append(
            {
                "distance_fraction": distance,
                "phase_index": phase_index,
                "chirality_a": chirality_a,
                "chirality_b": chirality_b,
                "mode": "off",
                "phase": p5d.PHASES[phase_index],
                "coupling": 0.0,
                "initial_distance": initial_distance,
                "completed": True,
                "finite": True,
                "stopped": False,
                "stop_reason": None,
                "kappa_name": None,
                "sign": None,
                "source_bitwise_native": True,
                "receiver_response_resolved": True,
                "final_history_sha256_a": f"a-{distance}-{phase_index}-{chirality_a}-{chirality_b}",
                "final_history_sha256_b": f"b-{distance}-{phase_index}-{chirality_a}-{chirality_b}",
                "trace": off_trace,
                "ledger_maxima": {
                    name: 0.0
                    for name in (
                        "work_split_a",
                        "work_split_b",
                        "pair_ledger",
                        "force_balance",
                        "midpoint_a",
                        "midpoint_b",
                        "center_local_a",
                        "center_local_b",
                        "center_envelope_a",
                        "center_envelope_b",
                    )
                },
                "ledger_cumulative": {
                    "work_split_a": 0.0,
                    "work_split_b": 0.0,
                    "pair_ledger": 0.0,
                },
                "ledger_rival_maxima": {
                    name: 0.0
                    for name in (
                        "omitted_age_a",
                        "omitted_age_b",
                        "omitted_both_ages",
                        "raw_center",
                        "one_way_without_reservoir",
                        "flipped_force_a",
                    )
                },
                "ledger_rival_fractions": {
                    name: 0.0
                    for name in (
                        "omitted_age_a",
                        "omitted_age_b",
                        "omitted_both_ages",
                        "raw_center",
                        "one_way_without_reservoir",
                        "flipped_force_a",
                    )
                },
                "ledger_rival_resolved": {
                    name: False
                    for name in (
                        "omitted_age_a",
                        "omitted_age_b",
                        "omitted_both_ages",
                        "raw_center",
                        "one_way_without_reservoir",
                        "flipped_force_a",
                    )
                },
                "ledger_evaluation_count": 0,
                "shape_evaluation_count": 2_001,
                "ledger_scales": {"energy": 1.0, "force": 1.0, "displacement": 1.0},
                "minimum_mobility_dissipation": None,
                "normal_metrology_operands": True,
                "ledger_gates": {"not_applicable_channel_off": True},
                "loop_gates": {
                    "complete_shape_evaluation_count": True,
                    "bitwise_native": True,
                    "prepared_orbit": True,
                    "stationary_center": True,
                },
                "loop_summary": {
                    "maximum_d0_a": 0.0,
                    "maximum_d0_b": 0.0,
                    "late_d0_a": 0.0,
                    "late_d0_b": 0.0,
                    "late_opposite_a": 1.0,
                    "late_opposite_b": 1.0,
                    "center_stationarity_fraction": 0.0,
                },
                "phase_metrics": {
                    "a": {"mean_error": 0.0, "rms_error": 0.0, "pass": True},
                    "b": {"mean_error": 0.0, "rms_error": 0.0, "pass": True},
                },
                "minimum_separation": initial_distance,
                "maximum_center_response_fraction": None,
                "high_precision_references": [],
            }
        )
        for kappa_name in p5d.KAPPAS:
            for sign in p5d.SIGNS:
                one_way = 0.003 if kappa_name == "low" else 0.006
                excess = 0.00003 if kappa_name == "low" else 0.00012
                reciprocal = 2.0 * one_way - sign * excess
                for mode in p5d.DIRECTIONS:
                    longitudinal = reciprocal if mode == "reciprocal" else one_way
                    final_delta = sign * longitudinal * initial_distance
                    trace = []
                    for step in steps:
                        delta = final_delta * step / p5d.THRESHOLDS.active_updates
                        if mode == "a_to_b":
                            center_a = base_a
                            center_b = base_b - delta
                        elif mode == "b_to_a":
                            center_a = base_a + delta
                            center_b = base_b
                        else:
                            center_a = base_a + 0.5 * delta
                            center_b = base_b - 0.5 * delta
                        trace.append(
                            {
                                "alignment_a": 0.0,
                                "alignment_b": 0.0,
                                "step": step,
                                "center_a": p5d._pair(center_a),
                                "center_b": p5d._pair(center_b),
                                "d0_a": 0.0,
                                "d0_b": 0.0,
                                "opposite_d0_a": 1.0,
                                "opposite_d0_b": 1.0,
                                "separation": p5d._pair(center_a - center_b),
                            }
                        )
                    active.append(
                        {
                            "distance_fraction": distance,
                            "phase_index": phase_index,
                            "chirality_a": chirality_a,
                            "chirality_b": chirality_b,
                            "kappa_name": kappa_name,
                            "sign": sign,
                            "mode": mode,
                            "phase": p5d.PHASES[phase_index],
                            "coupling": sign * p5d.KAPPA_VALUES[kappa_name],
                            "initial_distance": initial_distance,
                            "completed": True,
                            "finite": True,
                            "stopped": False,
                            "stop_reason": None,
                            "source_bitwise_native": True,
                            "receiver_response_resolved": True,
                            "final_history_sha256_a": (
                                f"a-{distance}-{phase_index}-{chirality_a}-{chirality_b}"
                                if mode == "a_to_b"
                                else f"active-a-{kappa_name}-{sign}-{mode}"
                            ),
                            "final_history_sha256_b": (
                                f"b-{distance}-{phase_index}-{chirality_a}-{chirality_b}"
                                if mode == "b_to_a"
                                else f"active-b-{kappa_name}-{sign}-{mode}"
                            ),
                            "trace": trace,
                            "ledger_maxima": {
                                name: 0.0
                                for name in (
                                    "work_split_a",
                                    "work_split_b",
                                    "pair_ledger",
                                    "force_balance",
                                    "midpoint_a",
                                    "midpoint_b",
                                    "center_local_a",
                                    "center_local_b",
                                    "center_envelope_a",
                                    "center_envelope_b",
                                )
                            },
                            "ledger_cumulative": {
                                "work_split_a": 0.0,
                                "work_split_b": 0.0,
                                "pair_ledger": 0.0,
                            },
                            "ledger_rival_maxima": {
                                name: 0.0
                                for name in (
                                    "omitted_age_a",
                                    "omitted_age_b",
                                    "omitted_both_ages",
                                    "raw_center",
                                    "one_way_without_reservoir",
                                    "flipped_force_a",
                                )
                            },
                            "ledger_rival_fractions": {
                                name: 0.0
                                for name in (
                                    "omitted_age_a",
                                    "omitted_age_b",
                                    "omitted_both_ages",
                                    "raw_center",
                                    "one_way_without_reservoir",
                                    "flipped_force_a",
                                )
                            },
                            "ledger_rival_resolved": {
                                name: False
                                for name in (
                                    "omitted_age_a",
                                    "omitted_age_b",
                                    "omitted_both_ages",
                                    "raw_center",
                                    "one_way_without_reservoir",
                                    "flipped_force_a",
                                )
                            },
                            "ledger_evaluation_count": 2_000,
                            "shape_evaluation_count": 2_001,
                            "ledger_scales": {
                                "energy": 1.0,
                                "force": 1.0,
                                "displacement": 1.0,
                            },
                            "minimum_mobility_dissipation": 0.0,
                            "normal_metrology_operands": True,
                            "ledger_gates": {
                                "complete_evaluation_count": True,
                                "normal_operands": True,
                                "center_local": True,
                                "center_full_envelope": True,
                                "force_balance": True,
                                "midpoint_force": True,
                                "work_split_step": True,
                                "pair_ledger_step": True,
                                "work_split_cumulative": True,
                                "pair_ledger_cumulative": True,
                                "nonnegative_mobility": True,
                                "high_precision_references": True,
                            },
                            "loop_gates": {
                                "complete_shape_evaluation_count": True,
                                "maximum_d0": True,
                                "late_d0": True,
                                "opposite_chirality": True,
                                "phase_a": True,
                                "phase_b": True,
                                "separation": True,
                                "center_response_bound": True,
                            },
                            "loop_summary": {
                                "maximum_d0_a": 0.0,
                                "maximum_d0_b": 0.0,
                                "late_d0_a": 0.0,
                                "late_d0_b": 0.0,
                                "late_opposite_a": 1.0,
                                "late_opposite_b": 1.0,
                                "center_stationarity_fraction": None,
                            },
                            "phase_metrics": {
                                "a": {
                                    "mean_error": 0.0,
                                    "rms_error": 0.0,
                                    "pass": True,
                                },
                                "b": {
                                    "mean_error": 0.0,
                                    "rms_error": 0.0,
                                    "pass": True,
                                },
                            },
                            "minimum_separation": initial_distance,
                            "maximum_center_response_fraction": 0.01,
                            "high_precision_references": (
                                [
                                    {
                                        "update": update,
                                        "precision_dps": 80,
                                        "midpoint_a_residual": 0.0,
                                        "midpoint_b_residual": 0.0,
                                        "completed_force_balance_residual": 0.0,
                                        "relative_tolerance": 5.0e-12,
                                        "pass": True,
                                    }
                                    for update in (1, 1_000, 2_000)
                                ]
                                if kappa_name == "high"
                                and sign == 1
                                and mode == "reciprocal"
                                else []
                            ),
                        }
                    )
    return off, active


@pytest.fixture(scope="module")
def synthetic_panel() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    return _synthetic_panel()


def test_p5d_synthetic_complete_panel_passes_every_response_family(
    synthetic_panel: tuple[list[dict[str, object]], list[dict[str, object]]],
) -> None:
    off, active = synthetic_panel
    registration = p5d.panel_registration(off, active)
    response = p5d.response_controls(off, active)
    decision, gates = p5d.classify_panel(
        registration=registration,
        channel_off_arms=off,
        active_arms=active,
        response=response,
    )
    assert registration["pass"] is True
    assert response["available"] is True
    assert all(response["gates"].values())
    assert all(gates.values())
    assert decision == "p5d-mutual-center-response-pass"
    assert response["diagnostics"]["excess_low_high_range"] == pytest.approx(
        [0.25, 0.25], abs=2e-12
    )
    assert response["diagnostics"]["maximum_reflection_rms_fraction"] < 1e-15
    assert response["diagnostics"]["maximum_swap_rms_fraction"] < 1e-15


def test_p5d_recovery_serializer_handles_full_panel_and_numpy_scalars(
    synthetic_panel: tuple[list[dict[str, object]], list[dict[str, object]]],
) -> None:
    off, active = synthetic_panel
    payload = {
        "panel": {"channel_off_arms": off, "active_arms": active},
        "numpy_scalars": {
            "boolean": np.bool_(True),
            "signed": np.int64(-7),
            "unsigned": np.uint64(9),
            "floating": np.float32(0.125),
        },
        "python_native": {"boolean": False, "integer": 11, "floating": 0.5},
    }
    encoded = p5d._serialize_payload(payload)
    decoded = json.loads(encoded)
    assert decoded["numpy_scalars"] == {
        "boolean": True,
        "signed": -7,
        "unsigned": 9,
        "floating": 0.125,
    }
    assert decoded["python_native"] == {
        "boolean": False,
        "integer": 11,
        "floating": 0.5,
    }
    assert len(decoded["panel"]["channel_off_arms"]) == 64
    assert len(decoded["panel"]["active_arms"]) == 768


def _synthetic_v2_payload(
    panel: tuple[list[dict[str, object]], list[dict[str, object]]],
) -> dict[str, object]:
    off, active = copy.deepcopy(panel)
    registration = p5d.panel_registration(off, active, require_references=True)
    response = p5d.response_controls(off, active, require_references=True)
    decision, gates = p5d.classify_panel(
        registration=registration,
        channel_off_arms=off,
        active_arms=active,
        response=response,
    )
    thresholds = p5d.asdict(p5d.THRESHOLDS)
    thresholds["reference_steps"] = list(thresholds["reference_steps"])
    return {
        "schema": "scalar-memory-loop-p5d-mutual-center-v2",
        "created_utc": "2026-09-03T12:00:00+00:00",
        "provenance": {
            "attempt_receipt_path": "attempt.json",
            "attempt_receipt_sha256": "1" * 64,
            "authorization_id": "12345678-1234-4123-8123-123456789abc",
            "ci_run_id": 123,
            "clean": True,
            "governance_sha256": "2" * 64,
            "implementation_revision": "3" * 40,
            "revision": "4" * 40,
            "upstream_revision": "4" * 40,
        },
        "candidate": p5d.asdict(p5d.CANDIDATE),
        "thresholds": thresholds,
        "panel": {"channel_off_arms": off, "active_arms": active},
        "registration": registration,
        "response": response,
        "decision_gates": gates,
        "decision": decision,
        "claim_boundary": (
            "explicit operational mutual-center architecture only; no spontaneous "
            "interaction, charge, spin, momentum, inertia or mass"
        ),
    }


def test_p5d_v2_full_synthetic_payload_round_trips_and_audits(
    synthetic_panel: tuple[list[dict[str, object]], list[dict[str, object]]],
) -> None:
    payload = _synthetic_v2_payload(synthetic_panel)
    p5d._validate_v2_payload(payload)
    encoded = p5d._serialize_payload(payload)
    decoded = json.loads(encoded)
    p5d._validate_v2_payload(decoded)

    from experiments.current.dynamics.rotation import (
        scalar_memory_loop_p5d_mutual_center_result_audit as independent,
    )

    independent._validate_v2_payload(decoded)
    result = independent.audit_payload(decoded)
    assert result["decision"] == "p5d-independent-audit-agrees"
    assert result["recomputed_decision"] == "p5d-mutual-center-response-pass"


def test_p5d_v2_schema_errors_name_the_exact_json_path(
    synthetic_panel: tuple[list[dict[str, object]], list[dict[str, object]]],
) -> None:
    payload = _synthetic_v2_payload(synthetic_panel)
    payload["panel"]["active_arms"][0]["trace"][7]["step"] = True
    with pytest.raises(
        TypeError, match=r"\$\.panel\.active_arms\[0\]\.trace\[7\]\.step"
    ):
        p5d._validate_v2_payload(payload)


def test_p5d_v2_arm_contract_is_exact_in_runner_and_independent_auditor(
    synthetic_panel: tuple[list[dict[str, object]], list[dict[str, object]]],
) -> None:
    from experiments.current.dynamics.rotation import (
        scalar_memory_loop_p5d_mutual_center_result_audit as independent,
    )

    validators = (
        (p5d._validate_schema_value, p5d._load_result_schema()),
        (independent._validate_schema_value, independent._load_result_schema()),
    )
    off, active = synthetic_panel
    for validate, contract in validators:
        validate(
            copy.deepcopy(off[0]),
            "object:off_arm",
            path="$.off[0]",
            contract=contract,
        )
        validate(
            copy.deepcopy(active[0]),
            "object:active_arm",
            path="$.active[0]",
            contract=contract,
        )
        mutations = []
        unknown = copy.deepcopy(active[0])
        unknown["unknown"] = 1
        mutations.append(unknown)
        missing = copy.deepcopy(active[0])
        missing.pop("coupling")
        mutations.append(missing)
        wrong_length = copy.deepcopy(active[0])
        wrong_length["trace"].pop()
        mutations.append(wrong_length)
        nonfinite = copy.deepcopy(active[0])
        nonfinite["trace"][4]["d0_a"] = float("nan")
        mutations.append(nonfinite)
        unsupported = copy.deepcopy(active[0])
        unsupported["coupling"] = np.float64(unsupported["coupling"])
        mutations.append(unsupported)
        for row in mutations:
            with pytest.raises(TypeError, match=r"\$\.active\[0\]"):
                validate(
                    row,
                    "object:active_arm",
                    path="$.active[0]",
                    contract=contract,
                )


def test_p5d_unavailable_response_schema_is_exact() -> None:
    contract = p5d._load_result_schema()
    p5d._validate_schema_value(
        {"available": False, "reason": "misregistered-panel"},
        "variant:response",
        path="$.response",
        contract=contract,
    )
    with pytest.raises(TypeError, match="key mismatch"):
        p5d._validate_schema_value(
            {
                "available": False,
                "reason": "misregistered-panel",
                "diagnostics": {},
            },
            "variant:response",
            path="$.response",
            contract=contract,
        )


def test_p5d_v2_publication_round_trip_is_manifest_first(
    synthetic_panel: tuple[list[dict[str, object]], list[dict[str, object]]],
    monkeypatch,
    tmp_path: Path,
) -> None:
    from experiments.current.dynamics.rotation import (
        scalar_memory_loop_p5d_mutual_center_result_audit as independent,
    )

    payload = _synthetic_v2_payload(synthetic_panel)
    summary_content = p5d._serialize_payload(payload)
    summary_digest = hashlib.sha256(summary_content.encode("utf-8")).hexdigest()
    report_content = p5d._render_report(payload, summary_digest)
    summary = tmp_path / "result.json"
    report = tmp_path / "result.md"
    manifest = tmp_path / "result.publication.json"
    receipt = tmp_path / "attempt.json"
    receipt_content = (
        json.dumps(
            {
                "authorization_id": payload["provenance"]["authorization_id"],
                "created_utc": "2026-09-03T11:59:00+00:00",
                "governance_sha256": payload["provenance"]["governance_sha256"],
                "revision": payload["provenance"]["revision"],
                "schema": "scalar-memory-loop-p5d-attempt-receipt-v1",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    receipt.write_text(receipt_content, encoding="utf-8", newline="")
    receipt_digest = hashlib.sha256(receipt_content.encode("utf-8")).hexdigest()
    payload["provenance"]["attempt_receipt_sha256"] = receipt_digest
    summary_content = p5d._serialize_payload(payload)
    summary_digest = hashlib.sha256(summary_content.encode("utf-8")).hexdigest()
    report_content = p5d._render_report(payload, summary_digest)
    p5d._write_complete_outputs(
        summary_path=summary,
        summary_content=summary_content,
        report_path=report,
        report_content=report_content,
        manifest_path=manifest,
        authorization_id=payload["provenance"]["authorization_id"],
        attempt_receipt_path="attempt.json",
        attempt_receipt_sha256=receipt_digest,
    )
    monkeypatch.setattr(independent, "ROOT", tmp_path)
    monkeypatch.setattr(independent, "RESULT", summary)
    monkeypatch.setattr(independent, "REPORT", report)
    monkeypatch.setattr(independent, "MANIFEST", manifest)
    result = independent.audit()
    assert result["decision"] == "p5d-independent-audit-agrees"
    report.write_text(report_content + "tampered\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="report digest mismatch"):
        independent.audit()


@pytest.mark.parametrize("fail_at", (1, 2, 3))
def test_p5d_publication_failure_never_leaves_a_valid_manifest(
    fail_at: int, monkeypatch, tmp_path: Path
) -> None:
    summary = tmp_path / "result.json"
    report = tmp_path / "result.md"
    manifest = tmp_path / "result.publication.json"
    original_replace = Path.replace
    calls = 0

    def injected_replace(path: Path, target: Path):
        nonlocal calls
        calls += 1
        if calls == fail_at:
            raise OSError("injected publication failure")
        return original_replace(path, target)

    monkeypatch.setattr(Path, "replace", injected_replace)
    with pytest.raises(OSError, match="injected publication failure"):
        p5d._write_complete_outputs(
            summary_path=summary,
            summary_content='{"complete": true}\n',
            report_path=report,
            report_content="# P5-D complete\n",
            manifest_path=manifest,
            authorization_id="12345678-1234-4123-8123-123456789abc",
            attempt_receipt_path="attempt.json",
            attempt_receipt_sha256="1" * 64,
        )
    assert not summary.exists()
    assert not report.exists()
    assert not manifest.exists()
    assert not any(tmp_path.glob("*.tmp"))


def test_p5d_channel_off_mobility_minimum_has_explicit_null_semantics() -> None:
    encoded = p5d._serialize_payload(
        {
            "mode": "off",
            "minimum_mobility_dissipation": None,
            "ledger_gates": {"not_applicable_channel_off": True},
        }
    )
    decoded = json.loads(encoded)
    assert decoded["minimum_mobility_dissipation"] is None
    assert p5d._all_finite(decoded)


def test_p5d_recursive_finite_check_rejects_unknown_and_numpy_nonfinite() -> None:
    assert p5d._all_finite(np.float32(0.125))
    assert not p5d._all_finite(np.float32(np.nan))
    assert not p5d._all_finite({"nested": [object()]})


def test_p5d_unavailable_response_report_needs_no_diagnostics() -> None:
    report = p5d._render_report(
        {
            "decision": "p5d-inconclusive",
            "response": {"available": False, "reason": "misregistered-panel"},
        },
        "0" * 64,
    )
    assert "Response status: `unavailable`" in report
    assert "Reason: `misregistered-panel`" in report
    assert "No response diagnostics were evaluated" in report


@pytest.mark.parametrize(
    "value",
    (np.float64(np.nan), np.float64(np.inf), np.float64(-np.inf)),
)
def test_p5d_recovery_serializer_rejects_nonfinite_numpy_scalars(value) -> None:
    with pytest.raises(ValueError, match="Out of range float"):
        p5d._serialize_payload({"value": value})


@pytest.mark.parametrize(
    "value",
    (np.asarray([1.0]), np.complex128(1.0 + 2.0j), object()),
)
def test_p5d_recovery_serializer_rejects_unregistered_objects(value) -> None:
    with pytest.raises(TypeError, match="not JSON serializable"):
        p5d._serialize_payload({"value": value})


def test_p5d_exactly_additive_reciprocal_trace_is_rejected(
    synthetic_panel: tuple[list[dict[str, object]], list[dict[str, object]]],
) -> None:
    off, active = copy.deepcopy(synthetic_panel)
    index = {p5d._active_key(row): row for row in active}
    for base in p5d.expected_base_keys():
        baseline = {
            sample["step"]: sample
            for sample in off[p5d.expected_base_keys().index(base)]["trace"]
        }
        for kappa in p5d.KAPPAS:
            for sign in p5d.SIGNS:
                ab = index[(*base, kappa, sign, "a_to_b")]
                ba = index[(*base, kappa, sign, "b_to_a")]
                rec = index[(*base, kappa, sign, "reciprocal")]
                for target, left, right in zip(
                    rec["trace"], ab["trace"], ba["trace"], strict=True
                ):
                    control = baseline[target["step"]]
                    separation = (
                        p5d._complex(left["separation"])
                        + p5d._complex(right["separation"])
                        - p5d._complex(control["separation"])
                    )
                    target["separation"] = p5d._pair(separation)
                    target["center_a"] = p5d._pair(
                        p5d._complex(control["center_a"])
                        + 0.5 * (separation - p5d._complex(control["separation"]))
                    )
                    target["center_b"] = p5d._pair(
                        p5d._complex(control["center_b"])
                        - 0.5 * (separation - p5d._complex(control["separation"]))
                    )
    response = p5d.response_controls(off, active)
    decision, gates = p5d.classify_panel(
        registration=p5d.panel_registration(off, active),
        channel_off_arms=off,
        active_arms=active,
        response=response,
    )
    assert response["gates"]["excess_resolved"] is False
    assert gates["mutual_hypothesis"] is True
    assert gates["closed_loop_excess"] is False
    assert decision == "p5d-independent-superposition"


def test_p5d_incomplete_panel_and_swap_corruption_fail_closed(
    synthetic_panel: tuple[list[dict[str, object]], list[dict[str, object]]],
) -> None:
    off, active = synthetic_panel
    unavailable = p5d.response_controls(off, active[:-1])
    assert unavailable["available"] is False
    assert unavailable["reason"] == "misregistered-panel"

    corrupted = copy.deepcopy(active)
    target = next(
        row
        for row in corrupted
        if p5d._active_key(row) == (3, 0, 1, 1, "high", 1, "reciprocal")
    )
    target["trace"][-1]["center_a"][1] += 0.01
    target["trace"][-1]["separation"][1] += 0.01
    response = p5d.response_controls(off, corrupted)
    decision, gates = p5d.classify_panel(
        registration=p5d.panel_registration(off, corrupted),
        channel_off_arms=off,
        active_arms=corrupted,
        response=response,
    )
    assert response["gates"]["swap_covariance"] is False
    assert gates["mutual_hypothesis"] is False
    assert decision == "p5d-mutual-hypothesis-fail"


def test_p5d_decision_precedence_covers_every_registered_branch() -> None:
    good = {
        "pipeline": True,
        "ledger_and_reciprocity": True,
        "loop_integrity": True,
        "directional_causality": True,
        "mutual_hypothesis": True,
        "closed_loop_excess": True,
        "scaling": True,
    }
    assert p5d.decision_from_gates(good) == "p5d-mutual-center-response-pass"
    labels = (
        ("pipeline", "p5d-inconclusive"),
        ("ledger_and_reciprocity", "p5d-ledger-or-reciprocity-fail"),
        ("loop_integrity", "p5d-loop-integrity-fail"),
        ("directional_causality", "p5d-directional-causality-fail"),
        ("mutual_hypothesis", "p5d-mutual-hypothesis-fail"),
        ("closed_loop_excess", "p5d-independent-superposition"),
        ("scaling", "p5d-inconclusive"),
    )
    for gate, expected in labels:
        failed = {**good, gate: False}
        assert p5d.decision_from_gates(failed) == expected
    doubly_failed = {**good, "ledger_and_reciprocity": False, "loop_integrity": False}
    assert p5d.decision_from_gates(doubly_failed) == ("p5d-ledger-or-reciprocity-fail")


def test_p5d_target_guard_precedes_registered_panel(monkeypatch) -> None:
    calls: list[str] = []

    def sealed() -> dict[str, object]:
        raise RuntimeError("sealed-before-readiness")

    def forbidden_panel():
        calls.append("target")
        raise AssertionError("registered target panel was reached")

    monkeypatch.setattr(p5d, "_verify_provenance", sealed)
    monkeypatch.setattr(p5d, "_run_registered_panel", forbidden_panel)
    with pytest.raises(RuntimeError, match="sealed-before-readiness"):
        p5d.run_gate()
    assert calls == []


def test_p5d_machine_governance_is_closed_and_binds_both_incidents() -> None:
    governance = p5d._load_governance()
    assert governance["schema"] == "scalar-memory-loop-p5d-governance-v1"
    assert governance["state"] == "closed"
    assert governance["target_authorized"] is False
    assert governance["authorization"] is None
    assert [row["attempt"] for row in governance["target_calls_recorded"]] == [1, 2]
    assert (
        governance["result_schema_sha256"]
        == hashlib.sha256((p5d.ROOT / p5d.RESULT_SCHEMA).read_bytes()).hexdigest()
    )


def _synthetic_authorized_governance() -> dict[str, object]:
    implementation = "a" * 40
    protected = {
        path: f"{index + 1:x}" * 40 for index, path in enumerate(p5d.PROTECTED_PATHS)
    }
    return {
        "schema": p5d.GOVERNANCE_SCHEMA,
        "gate": "P5-D",
        "reason": "prospective-one-shot-review",
        "result_schema_sha256": "e" * 64,
        "state": "authorized_once",
        "target_authorized": True,
        "target_calls_recorded": [],
        "authorization": {
            "attempt": 3,
            "authorization_id": "12345678-1234-4123-8123-123456789abc",
            "ci": {
                "api_url": "https://api.github.com/repos/MemoryDynamics/Knoten/actions/runs/123",
                "conclusion": "success",
                "head_sha": implementation,
                "run_id": 123,
                "status": "completed",
            },
            "closed_governance_blob": "b" * 40,
            "implementation_revision": implementation,
            "protected_blobs": protected,
            "readiness_review_blob": "c" * 40,
            "readiness_review_path": p5d.READINESS_REVIEW.as_posix(),
            "remediation_protocol_blob": p5d.RECOVERY_PROTOCOL_BLOB,
            "schema_sha256": "e" * 64,
        },
    }


def _mock_authorization_dependencies(monkeypatch, governance, *, remote=None) -> None:
    authorization = governance["authorization"]
    implementation = authorization["implementation_revision"]
    head = "f" * 40

    def fake_blob(path: str, revision: str = "HEAD") -> str:
        if path == p5d.RECOVERY_PROTOCOL.as_posix():
            return p5d.RECOVERY_PROTOCOL_BLOB
        if path in authorization["protected_blobs"]:
            return authorization["protected_blobs"][path]
        if path == p5d.GOVERNANCE.as_posix() and revision == implementation:
            return authorization["closed_governance_blob"]
        if path == p5d.READINESS_REVIEW.as_posix():
            return authorization["readiness_review_blob"]
        raise AssertionError((path, revision))

    def fake_git(*arguments: str) -> str:
        if arguments[:2] == ("merge-base", "--is-ancestor"):
            return ""
        if arguments == ("status", "--porcelain"):
            return ""
        if arguments == ("rev-parse", "@{upstream}"):
            return head
        if arguments == ("rev-parse", "HEAD"):
            return head
        if arguments[:2] == ("diff", "--name-only"):
            return p5d.GOVERNANCE.as_posix()
        raise AssertionError(arguments)

    official = {
        "id": 123,
        "repository": {"full_name": "MemoryDynamics/Knoten"},
        "status": "completed",
        "conclusion": "success",
        "head_sha": implementation,
    }
    monkeypatch.setattr(p5d, "_load_governance", lambda: governance)
    monkeypatch.setattr(p5d, "_git_blob", fake_blob)
    monkeypatch.setattr(p5d, "_git", fake_git)
    monkeypatch.setattr(
        p5d,
        "_sha256_file",
        lambda path: "e" * 64 if path.name.endswith("schema_v2.json") else "d" * 64,
    )
    monkeypatch.setattr(
        p5d, "_gh_run_metadata", lambda run_id: official if remote is None else remote
    )
    monkeypatch.setattr(p5d, "_validate_default_output_paths", lambda *args: None)
    monkeypatch.setattr(
        p5d,
        "_create_attempt_receipt",
        lambda **kwargs: (p5d.ATTEMPT_RECEIPT.as_posix(), "9" * 64),
    )


def test_p5d_authorized_once_binds_ci_blobs_and_consumes_receipt(monkeypatch) -> None:
    governance = _synthetic_authorized_governance()
    _mock_authorization_dependencies(monkeypatch, governance)
    result = p5d._require_target_authorization()
    assert result["authorization_id"] == governance["authorization"]["authorization_id"]
    assert result["attempt_receipt_sha256"] == "9" * 64
    assert result["ci_run_id"] == 123


@pytest.mark.parametrize(
    "remote",
    (
        {
            "id": 123,
            "repository": {"full_name": "MemoryDynamics/Knoten"},
            "status": "completed",
            "conclusion": "failure",
            "head_sha": "a" * 40,
        },
        {
            "id": 123,
            "repository": {"full_name": "MemoryDynamics/Knoten"},
            "status": "completed",
            "conclusion": "success",
            "head_sha": "0" * 40,
        },
    ),
)
def test_p5d_authorization_rejects_untrusted_ci_metadata(monkeypatch, remote) -> None:
    governance = _synthetic_authorized_governance()
    _mock_authorization_dependencies(monkeypatch, governance, remote=remote)
    with pytest.raises(RuntimeError, match="official CI metadata mismatch"):
        p5d._require_target_authorization()


def test_p5d_authorization_fails_closed_when_ci_is_offline(monkeypatch) -> None:
    governance = _synthetic_authorized_governance()
    _mock_authorization_dependencies(monkeypatch, governance)

    def offline(run_id: int):
        raise OSError("offline")

    monkeypatch.setattr(p5d, "_gh_run_metadata", offline)
    with pytest.raises(RuntimeError, match="official CI metadata is unavailable"):
        p5d._require_target_authorization()


def test_p5d_authorization_rejects_protected_blob_drift(monkeypatch) -> None:
    governance = _synthetic_authorized_governance()
    _mock_authorization_dependencies(monkeypatch, governance)
    clean_blob = p5d._git_blob
    drift_path = p5d.PROTECTED_PATHS[0]

    def drifted(path: str, revision: str = "HEAD") -> str:
        if path == drift_path and revision == "HEAD":
            return "0" * 40
        return clean_blob(path, revision)

    monkeypatch.setattr(p5d, "_git_blob", drifted)
    with pytest.raises(RuntimeError, match="protected blob drift"):
        p5d._require_target_authorization()


def test_p5d_attempt_receipt_is_exclusive_and_consumes_the_lease(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(p5d, "ROOT", tmp_path)
    first = p5d._create_attempt_receipt(
        authorization_id="12345678-1234-4123-8123-123456789abc",
        revision="a" * 40,
        governance_sha256="b" * 64,
    )
    assert first[0] == p5d.ATTEMPT_RECEIPT.as_posix()
    with pytest.raises(RuntimeError, match="already consumed"):
        p5d._create_attempt_receipt(
            authorization_id="12345678-1234-4123-8123-123456789abc",
            revision="a" * 40,
            governance_sha256="b" * 64,
        )


def test_p5d_machine_governance_seals_before_legacy_provenance_and_target(
    monkeypatch,
) -> None:
    calls: list[str] = []

    def forbidden_readiness(*args, **kwargs):
        calls.append("legacy-provenance")
        raise AssertionError("legacy provenance was reached")

    def forbidden_panel():
        calls.append("target")
        raise AssertionError("registered target panel was reached")

    monkeypatch.setattr(p5d, "_parse_readiness_review", forbidden_readiness)
    monkeypatch.setattr(p5d, "_run_registered_panel", forbidden_panel)
    with pytest.raises(RuntimeError, match="sealed by machine governance"):
        p5d.run_gate()
    assert calls == []


def test_p5d_machine_governance_rejects_unknown_keys(
    monkeypatch, tmp_path: Path
) -> None:
    malformed = json.loads((p5d.ROOT / p5d.GOVERNANCE).read_text(encoding="utf-8"))
    malformed["prose_verdict"] = "ready"
    path = tmp_path / "governance.json"
    path.write_text(json.dumps(malformed), encoding="utf-8")
    monkeypatch.setattr(p5d, "GOVERNANCE", path)
    with pytest.raises(RuntimeError, match="invalid top-level keys"):
        p5d._require_target_authorization()


def test_p5d_recovery_readiness_guard_precedes_registered_panel(
    monkeypatch, tmp_path: Path
) -> None:
    calls: list[str] = []

    def forbidden_panel():
        calls.append("target")
        raise AssertionError("registered target panel was reached")

    def missing_readiness():
        raise RuntimeError("readiness review is absent")

    monkeypatch.setattr(p5d, "_require_target_authorization", missing_readiness)
    monkeypatch.setattr(p5d, "_run_registered_panel", forbidden_panel)
    with pytest.raises(RuntimeError, match="readiness review is absent"):
        p5d.run_gate()
    assert calls == []


def test_p5d_registered_panel_aborts_on_first_incomplete_arm(monkeypatch) -> None:
    calls = []

    def stopped_arm(**kwargs):
        calls.append(kwargs)
        return {"completed": False, "stop_reason": "synthetic-stop"}

    monkeypatch.setattr(p5d, "_run_arm", stopped_arm)
    with pytest.raises(RuntimeError, match="channel-off arm stopped"):
        p5d._run_registered_panel()
    assert len(calls) == 1
    assert calls[0]["mode"] == "off"


def test_p5d_imports_and_unit_tests_do_not_invoke_target_runner() -> None:
    tree = ast.parse(Path(p5d.__file__).read_text(encoding="utf-8"))
    calls = [
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    ]
    assert calls.count("main") == 1
    source = inspect.getsource(kernel.mutual_center_step)
    for forbidden in (
        "velocity",
        "momentum",
        "target_phase",
        "target_distance",
        "target_trajectory",
        "second_difference",
    ):
        assert forbidden not in source


def test_p5d_atomic_outputs_are_nonoverwriting(tmp_path: Path) -> None:
    summary = tmp_path / "result.json"
    report = tmp_path / "result.md"
    manifest = tmp_path / "result.publication.json"
    receipt_digest = "1" * 64
    p5d._write_complete_outputs(
        summary_path=summary,
        summary_content='{"complete": true}\n',
        report_path=report,
        report_content="# P5-D complete\n",
        manifest_path=manifest,
        authorization_id="12345678-1234-4123-8123-123456789abc",
        attempt_receipt_path="attempt.json",
        attempt_receipt_sha256=receipt_digest,
    )
    assert summary.read_text(encoding="utf-8") == '{"complete": true}\n'
    assert report.read_text(encoding="utf-8") == "# P5-D complete\n"
    assert (
        json.loads(manifest.read_text(encoding="utf-8"))["attempt_receipt_sha256"]
        == receipt_digest
    )
    with pytest.raises(RuntimeError, match="existing P5-D output"):
        p5d._write_complete_outputs(
            summary_path=summary,
            summary_content="blocked",
            report_path=report,
            report_content="blocked",
            manifest_path=manifest,
            authorization_id="12345678-1234-4123-8123-123456789abc",
            attempt_receipt_path="attempt.json",
            attempt_receipt_sha256=receipt_digest,
        )
