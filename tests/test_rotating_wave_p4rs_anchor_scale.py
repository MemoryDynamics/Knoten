from __future__ import annotations

import copy
from dataclasses import replace
import hashlib
import math

import numpy as np
import pytest

from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4r_phase_metrology_gate as p4r,
)
from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4rs_anchor_scale_gate as p4rs,
)
from emergenz_knoten.orbit_center_actuator import (
    candidate_orbit_center_readout,
    reciprocal_source_write_step,
    source_write_rounding_metrology,
)
from emergenz_knoten.rotating_wave_stability_gate import RotatingWaveCandidate


def test_p4rs_frozen_anchor_registration_and_common_grid() -> None:
    assert p4rs.CANDIDATE.candidate_id == p4rs.CANDIDATE_ID
    assert p4rs.CANDIDATE.horizon == 1200
    assert p4rs.CANDIDATE.alpha == 0.01
    assert p4rs.CANDIDATE.eta == 0.15
    assert p4rs.CANDIDATE.horizon * p4rs.CANDIDATE.alpha == 12.0
    assert p4rs.CANDIDATE.eta / p4rs.CANDIDATE.alpha == 15.0
    assert p4rs.THRESHOLDS.active_updates == 2_000
    assert p4rs.THRESHOLDS.sample_every == 5
    assert p4rs.THRESHOLDS.late_start == 1_800
    assert p4rs.THRESHOLDS.phase_start == 1_500
    assert p4rs.THRESHOLDS.reference_steps == (1, 1_000, 2_000)
    assert p4rs.THRESHOLDS.reference_dps == 80
    assert p4rs.THRESHOLDS.scale_tolerance == 0.05
    assert p4rs.PHASES == tuple(
        (2 * index + 1) * math.pi / 8.0 for index in range(8)
    )
    assert p4rs._expected_channel_off_keys() == [
        (phase_index, chirality)
        for phase_index in range(8)
        for chirality in (1, -1)
    ]
    assert p4rs._expected_active_keys() == [
        (phase_index, chirality, offset_sign)
        for phase_index in range(8)
        for chirality in (1, -1)
        for offset_sign in (1, -1)
    ]
    assert len(p4rs.ANCHOR_STEPS) == len(p4rs.L3_STEPS) == 401
    assert p4rs.ANCHOR_STEPS == tuple(5 * k for k in range(401))
    assert p4rs.L3_STEPS == tuple(10 * k for k in range(401))
    assert all(
        math.isclose(
            p4rs.CANDIDATE.alpha * anchor,
            p4r.CANDIDATE.alpha * l3,
            rel_tol=0.0,
            abs_tol=1e-15,
        )
        for anchor, l3 in zip(
            p4rs.ANCHOR_STEPS, p4rs.L3_STEPS, strict=True
        )
    )


def test_p4rs_frozen_dependencies_and_hashes_are_unchanged() -> None:
    assert all(
        p4rs._git_blob(path) == expected
        for path, expected in p4rs.EXPECTED_HEAD_BLOBS.items()
    )
    assert all(
        p4rs._canonical_lf_sha256(p4rs.ROOT / path) == expected
        for path, expected in p4rs.EXPECTED_CANONICAL_SHA256.items()
    )
    assert p4rs._is_ancestor(
        p4rs.DESIGN_FREEZE_REVISION,
        p4rs.PROTOCOL_FREEZE_REVISION,
    )


def test_p4rs_canonical_hash_is_line_ending_independent(tmp_path) -> None:
    canonical = b'{\n  "decision": "historical"\n}\n'
    lf_path = tmp_path / "lf.json"
    crlf_path = tmp_path / "crlf.json"
    lf_path.write_bytes(canonical)
    crlf_path.write_bytes(canonical.replace(b"\n", b"\r\n"))
    expected = hashlib.sha256(canonical).hexdigest()
    assert p4rs._canonical_lf_sha256(lf_path) == expected
    assert p4rs._canonical_lf_sha256(crlf_path) == expected


def test_p4rs_exact_anchor_root_and_static_port_pass_without_trajectory() -> None:
    controls = p4rs._anchor_root_controls()
    assert controls["pass"] is True
    assert all(controls["gates"].values())
    assert controls["refined_root"] == {
        "radius": p4rs.RADIUS_DECIMAL,
        "theta": p4rs.THETA_DECIMAL,
    }
    assert controls["interval_membership"] == {
        "radius": True,
        "theta": True,
    }
    assert controls["executable_offset"] == 0.0014197762572063359
    assert controls["write_gain"] == controls["actuator_mobility"]
    assert controls["write_gain"] != p4r.CANDIDATE.alpha
    assert max(controls["static_absolute_errors"].values()) < 5e-15


def test_p4rs_readiness_review_parser_is_strict() -> None:
    tick = chr(96)
    sha = "a" * 40
    blob = "b" * 40
    test_blob = "c" * 40
    text = (
        f"Implementation revision: {tick}{sha}{tick}\n"
        f"Runner blob: {tick}{blob}{tick}\n"
        f"Test blob: {tick}{test_blob}{tick}\n"
        "https://github.com/MemoryDynamics/Knoten/actions/runs/123456\n"
        f"Verdict: **{tick}p4rs-implementation-ready{tick}**\n"
    )
    parsed = p4rs._parse_readiness_review(text)
    assert parsed == {
        "implementation_revision": sha,
        "runner_blob": blob,
        "test_blob": test_blob,
        "ci_run": "123456",
        "verdict": "p4rs-implementation-ready",
    }
    with pytest.raises(RuntimeError, match="not upheld"):
        p4rs._parse_readiness_review(
            text.replace("p4rs-implementation-ready", "rejected")
        )
    with pytest.raises(RuntimeError, match="lacks test_blob"):
        p4rs._parse_readiness_review(
            text.replace(f"Test blob: {tick}{test_blob}{tick}\n", "")
        )


def test_p4rs_frozen_default_outputs_and_pair_write_refuses_reuse(
    tmp_path,
) -> None:
    summary_path = p4rs.ROOT / p4rs.DEFAULT_SUMMARY
    report_path = p4rs.ROOT / p4rs.DEFAULT_REPORT
    assert summary_path.exists()
    assert report_path.exists()
    assert p4rs._canonical_lf_sha256(summary_path) == (
        "daf127a55adf0eaa60325725493781a94fad3601bf52e90c38ba8c5e13ff62a7"
    )
    assert p4rs._canonical_lf_sha256(report_path) == (
        "f2a76ddbd79337b7a527fcd9951b6ab6b890b0fda7137d0791531cd8094132d0"
    )
    with pytest.raises(RuntimeError, match="refusing to overwrite"):
        p4rs._validate_default_output_paths(
            p4rs.DEFAULT_SUMMARY,
            p4rs.DEFAULT_REPORT,
        )
    with pytest.raises(RuntimeError, match="only the registered JSON"):
        p4rs._validate_default_output_paths(
            tmp_path / "leak.json",
            p4rs.DEFAULT_REPORT,
        )

    summary = tmp_path / "complete.json"
    report = tmp_path / "complete.md"
    p4rs._write_complete_outputs(
        summary_path=summary,
        summary_content='{"complete": true}\n',
        report_path=report,
        report_content="# Complete\n",
    )
    assert summary.read_text(encoding="utf-8") == '{"complete": true}\n'
    assert report.read_text(encoding="utf-8") == "# Complete\n"
    assert not summary.with_name(summary.name + ".tmp").exists()
    assert not report.with_name(report.name + ".tmp").exists()
    with pytest.raises(RuntimeError, match="existing output"):
        p4rs._write_complete_outputs(
            summary_path=summary,
            summary_content="blocked",
            report_path=report,
            report_content="blocked",
        )


@pytest.fixture(scope="module")
def l3_reference() -> dict[str, object]:
    return p4rs._load_l3_reference()


def test_p4rs_reconstructs_complete_l3_raw_panel(
    l3_reference: dict[str, object],
) -> None:
    assert l3_reference["pass"] is True
    assert all(l3_reference["gates"].values())
    assert l3_reference["raw_arm_counts"] == {
        "active": 32,
        "channel_off": 16,
    }
    assert (
        l3_reference["reconstruction_maximum_absolute_error"]
        <= p4rs.THRESHOLDS.reconstruction_tolerance
    )
    assert (
        max(l3_reference["frozen_mean_errors"].values())
        <= p4rs.THRESHOLDS.reconstruction_tolerance
    )
    response = l3_reference["response"]
    assert response["steps"] == list(p4rs.L3_STEPS)
    assert len(response["phase_chirality_response"]) == 16
    assert len(response["phase_profiles"]) == 8
    assert response["means"] == pytest.approx(
        p4rs.EXPECTED_L3_MEANS,
        abs=5e-15,
    )
    assert all(
        len(row[key]) == 401
        for row in response["phase_chirality_response"]
        for key in (
            "center_A_trace",
            "center_B_trace",
            "actuator_A_trace",
            "actuator_B_trace",
        )
    )


def _pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def _synthetic_raw_panel(
    *,
    steps: tuple[int, ...] = (0, 1, 2, 3, 4),
    even_fraction: float = 0.0,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    ramp = np.linspace(0.0, 1.0, len(steps))
    delta = 0.0015
    controls = []
    active = []
    for phase_index, chirality in p4rs._expected_channel_off_keys():
        controls.append(
            {
                "phase_index": phase_index,
                "phase": p4rs.PHASES[phase_index],
                "chirality": chirality,
                "trace": [
                    {
                        "step": step,
                        "center": [0.0, 0.0],
                        "actuator": [0.0, 0.0],
                    }
                    for step in steps
                ],
            }
        )
    for phase_index, chirality, offset_sign in p4rs._expected_active_keys():
        center_odd = ramp * (0.24 - 1j * chirality * 0.20)
        actuator_odd = ramp * (0.30 - 1j * chirality * 0.15)
        center_even = even_fraction * center_odd
        actuator_even = even_fraction * actuator_odd
        center = delta * (offset_sign * center_odd + center_even)
        actuator = delta * (offset_sign * actuator_odd + actuator_even)
        active.append(
            {
                "phase_index": phase_index,
                "phase": p4rs.PHASES[phase_index],
                "chirality": chirality,
                "offset_sign": offset_sign,
                "trace": [
                    {
                        "step": step,
                        "center": _pair(complex(center[index])),
                        "actuator": _pair(complex(actuator[index])),
                    }
                    for index, step in enumerate(steps)
                ],
            }
        )
    return active, controls


def test_p4rs_synthetic_response_recovers_components_and_symmetries() -> None:
    steps = (0, 1, 2, 3, 4)
    active, controls = _synthetic_raw_panel(steps=steps)
    response = p4rs._response_controls(
        active,
        controls,
        radius=1.0,
        delta=0.0015,
        expected_steps=steps,
        alpha=0.01,
    )
    assert response["available"] is True
    assert response["pass"] is True
    assert all(response["gates"].values())
    assert response["means"] == pytest.approx(
        {"A_C": 0.24, "B_C": 0.20, "A_Q": 0.30, "B_Q": 0.15},
        abs=2e-15,
    )
    assert response["positive_phase_support"] == {
        "center": 8,
        "actuator": 8,
    }
    assert max(
        row["center_error_fraction"]
        for row in response["mirror_equivariance"]
    ) < 1e-15
    assert max(
        row["center_error_fraction"]
        for row in response["half_turn_equivariance"]
    ) < 1e-15

    active, controls = _synthetic_raw_panel(
        steps=steps,
        even_fraction=0.03,
    )
    failed = p4rs._response_controls(
        active,
        controls,
        radius=1.0,
        delta=0.0015,
        expected_steps=steps,
        alpha=0.01,
    )
    assert failed["gates"]["even_response"] is False
    assert failed["pass"] is False
    unavailable = p4rs._response_controls(
        active[:-1],
        controls,
        radius=1.0,
        delta=0.0015,
        expected_steps=steps,
        alpha=0.01,
    )
    assert unavailable["available"] is False
    assert unavailable["reason"] == "misregistered-panel"


def _synthetic_scale_response(*, anchor: bool) -> dict[str, object]:
    steps = p4rs.ANCHOR_STEPS if anchor else p4rs.L3_STEPS
    alpha = p4rs.CANDIDATE.alpha if anchor else p4r.CANDIDATE.alpha
    time = np.asarray([alpha * step for step in steps])
    ramp = time / time[-1]
    rows = []
    for phase_index, chirality in p4rs._expected_channel_off_keys():
        rows.append(
            {
                "phase_index": phase_index,
                "chirality": chirality,
                "center_A_trace": (0.24 * ramp).tolist(),
                "center_B_trace": (0.20 * ramp).tolist(),
                "actuator_A_trace": (0.30 * ramp).tolist(),
                "actuator_B_trace": (0.15 * ramp).tolist(),
            }
        )
    profiles = [
        {
            "phase_index": phase_index,
            "A_C": 0.24,
            "B_C": 0.20,
            "A_Q": 0.30,
            "B_Q": 0.15,
        }
        for phase_index in range(8)
    ]
    return {
        "steps": list(steps),
        "memory_times": time.tolist(),
        "phase_chirality_response": rows,
        "phase_profiles": profiles,
        "means": {"A_C": 0.24, "B_C": 0.20, "A_Q": 0.30, "B_Q": 0.15},
    }


def test_p4rs_cross_scale_identical_synthetic_panel_passes() -> None:
    comparison = p4rs._compare_scales(
        _synthetic_scale_response(anchor=True),
        _synthetic_scale_response(anchor=False),
    )
    assert comparison["pass"] is True
    assert all(comparison["gates"].values())
    assert max(comparison["transient_rms"].values()) < 1e-15
    assert max(comparison["profile_rms"].values()) == 0.0
    assert all(
        row["absolute_difference"] == 0.0
        for row in comparison["mean_comparison"].values()
    )


def test_p4rs_cross_scale_transient_only_mismatch_is_detected() -> None:
    anchor = _synthetic_scale_response(anchor=True)
    l3 = _synthetic_scale_response(anchor=False)
    for row in anchor["phase_chirality_response"]:
        values = np.asarray(row["center_A_trace"])
        values[:-1] += 0.06
        row["center_A_trace"] = values.tolist()
    comparison = p4rs._compare_scales(anchor, l3)
    assert comparison["trace_gates"]["A_C"] is False
    assert all(comparison["profile_gates"].values())
    assert all(comparison["mean_gates"].values())
    assert comparison["pass"] is False


def test_p4rs_cross_scale_phase_local_and_mean_mismatches_are_detected() -> None:
    l3 = _synthetic_scale_response(anchor=False)
    local = _synthetic_scale_response(anchor=True)
    for row in local["phase_chirality_response"]:
        if row["phase_index"] == 0:
            row["center_A_trace"][-1] += 0.20
    local["phase_profiles"][0]["A_C"] += 0.20
    local["means"]["A_C"] += 0.025
    comparison = p4rs._compare_scales(local, l3)
    assert comparison["trace_gates"]["A_C"] is True
    assert comparison["profile_gates"]["A_C"] is False
    assert comparison["mean_gates"]["A_C"] is True

    mean_shift = _synthetic_scale_response(anchor=True)
    for row in mean_shift["phase_chirality_response"]:
        row["actuator_B_trace"][-1] += 0.06
    for row in mean_shift["phase_profiles"]:
        row["B_Q"] += 0.06
    mean_shift["means"]["B_Q"] += 0.06
    comparison = p4rs._compare_scales(mean_shift, l3)
    assert comparison["trace_gates"]["B_Q"] is True
    assert comparison["profile_gates"]["B_Q"] is False
    assert comparison["mean_gates"]["B_Q"] is False


def _decision_arms() -> list[dict[str, object]]:
    return [
        {
            "phase_index": phase_index,
            "chirality": chirality,
            "offset_sign": offset_sign,
            "valid": True,
            "ledger_pass": True,
            "dynamic_pass": True,
        }
        for phase_index, chirality, offset_sign in p4rs._expected_active_keys()
    ]


def _decision_controls() -> list[dict[str, int]]:
    return [
        {"phase_index": phase_index, "chirality": chirality}
        for phase_index, chirality in p4rs._expected_channel_off_keys()
    ]


def _decision_response(
    center: float,
    actuator: float,
    *,
    support: int = 8,
) -> dict[str, object]:
    return {
        "available": True,
        "pass": True,
        "means": {
            "A_C": 0.2,
            "B_C": center,
            "A_Q": 0.3,
            "B_Q": actuator,
        },
        "positive_phase_support": {
            "center": support,
            "actuator": support,
        },
    }


def _decide(
    response: dict[str, object],
    *,
    cross_pass: bool = True,
    pipeline: bool = True,
    arms: list[dict[str, object]] | None = None,
) -> tuple[str, dict[str, bool]]:
    return p4rs._decision(
        pipeline=pipeline,
        active_arms=arms or _decision_arms(),
        channel_off_arms=_decision_controls(),
        response=response,
        cross_scale={
            "pass": cross_pass,
            "gates": {"common_memory_time_grid": True},
        },
    )


def test_p4rs_decision_table_covers_every_registered_label() -> None:
    assert _decide(_decision_response(0.04, -0.05))[0] == (
        "p4rs-anchor-scalar-response"
    )
    assert _decide(_decision_response(-0.10, 0.12))[0] == (
        "p4rs-anchor-chiral-hypothesis-fail"
    )
    assert _decide(_decision_response(0.12, -0.10))[0] == (
        "p4rs-anchor-chiral-hypothesis-fail"
    )
    assert _decide(_decision_response(0.12, 0.11), cross_pass=False)[0] == (
        "p4rs-cross-scale-mismatch"
    )
    assert _decide(_decision_response(0.12, 0.11))[0] == (
        "p4rs-anchor-scale-transfer-pass"
    )
    assert _decide(_decision_response(0.07, 0.08))[0] == "p4rs-inconclusive"
    assert _decide(_decision_response(0.12, 0.11, support=5))[0] == (
        "p4rs-inconclusive"
    )
    assert _decide(_decision_response(0.12, 0.11), pipeline=False)[0] == (
        "p4rs-inconclusive"
    )


def test_p4rs_decision_precedence_separates_validity_ledger_and_loop() -> None:
    response = _decision_response(0.12, 0.11)
    ledger_failure = copy.deepcopy(_decision_arms())
    ledger_failure[0]["ledger_pass"] = False
    decision, gates = _decide(response, arms=ledger_failure)
    assert decision == "p4rs-ledger-or-metrology-fail"
    assert gates["reciprocal_ledger_and_metrology"] is False

    invalid = copy.deepcopy(ledger_failure)
    invalid[0]["valid"] = False
    decision, gates = _decide(response, arms=invalid)
    assert decision == "p4rs-inconclusive"
    assert gates["valid_active_arms"] is False

    dynamic_failure = copy.deepcopy(_decision_arms())
    dynamic_failure[0]["dynamic_pass"] = False
    decision, gates = _decide(response, arms=dynamic_failure)
    assert decision == "p4rs-inconclusive"
    assert gates["nonlinear_loop_dynamics"] is False

    decision, gates = p4rs._decision(
        pipeline=True,
        active_arms=_decision_arms(),
        channel_off_arms=_decision_controls(),
        response=response,
        cross_scale={
            "pass": False,
            "gates": {"common_memory_time_grid": False},
        },
    )
    assert decision == "p4rs-inconclusive"
    assert gates["common_memory_time_grid"] is False


def _small_candidate() -> RotatingWaveCandidate:
    return RotatingWaveCandidate(
        candidate_id="p4rs-synthetic-h17",
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


def test_p4rs_small_h_algebra_envelopes_and_exact_ratio_rejection() -> None:
    algebra = p4rs._small_h_algebraic_control()
    assert algebra["pass"] is True
    assert all(algebra["gates"].values())
    assert algebra["truncated_ledger_fraction"] >= 0.01

    candidate = _small_candidate()
    readout = candidate_orbit_center_readout(candidate, chirality=1)
    ages = np.arange(candidate.horizon, dtype=float)
    history = np.column_stack(
        (
            0.1 * ages + np.sin(0.37 * ages),
            -0.05 * ages + np.cos(0.23 * ages),
        )
    )
    result = reciprocal_source_write_step(
        history,
        np.asarray([0.7, -0.4]),
        candidate=candidate,
        readout=readout,
        coupling_strength=0.25,
    )
    metrology = source_write_rounding_metrology(result, readout=readout)
    assert metrology.normal_operands is True
    assert (
        abs(metrology.center_full_residual)
        <= metrology.center_full_envelope
    )
    assert (
        abs(metrology.coupling_full_residual)
        <= metrology.coupling_full_envelope
    )
    assert (
        abs(metrology.actuator_full_residual)
        <= metrology.actuator_full_envelope
    )
    reference = p4rs._high_precision_reference(
        result,
        metrology,
        readout=readout,
        update=1,
    )
    assert reference["precision_dps"] == 80
    assert reference["pass"] is True
    assert all(reference["gates"].values())

    corrupted = replace(result, center_actuation_residual=1.0e-8 + 0.0j)
    corrupted_metrology = source_write_rounding_metrology(
        corrupted,
        readout=readout,
    )
    rejected = p4rs._high_precision_reference(
        corrupted,
        corrupted_metrology,
        readout=readout,
        update=1,
    )
    assert rejected["pass"] is False
    assert rejected["gates"]["center_binary64_distance"] is False


def test_p4rs_provenance_guard_precedes_every_registered_target_call(
    monkeypatch,
) -> None:
    calls: list[str] = []

    def blocked_provenance() -> dict[str, object]:
        raise RuntimeError("sealed-before-readiness")

    def target_call(**_kwargs) -> dict[str, object]:
        calls.append("target")
        raise AssertionError("registered target was reached")

    monkeypatch.setattr(p4rs, "_verify_provenance", blocked_provenance)
    monkeypatch.setattr(p4rs, "_run_anchor_channel_off", target_call)
    monkeypatch.setattr(p4rs, "_run_anchor_active_arm", target_call)
    with pytest.raises(RuntimeError, match="sealed-before-readiness"):
        p4rs.run_gate()
    assert calls == []


def test_p4rs_does_not_mutate_historical_runner_globals() -> None:
    assert p4r.CANDIDATE_ID == (
        "k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1"
    )
    assert p4r.CANDIDATE.horizon == 2400
    assert p4r.THRESHOLDS.active_updates == 4_000
    assert p4r.THRESHOLDS.sample_every == 10
    assert p4rs.CANDIDATE is not p4r.CANDIDATE
    assert p4rs.THRESHOLDS is not p4r.THRESHOLDS
