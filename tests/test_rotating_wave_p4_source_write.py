from __future__ import annotations

import copy
import subprocess

from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4_source_write_gate as p4,
)


def test_p4_registration_matches_frozen_candidate_and_protocol() -> None:
    assert p4.CANDIDATE.candidate_id == p4.CANDIDATE_ID
    assert p4.CANDIDATE.horizon == 2400
    assert p4.THRESHOLDS.active_updates == 4_000
    assert p4.THRESHOLDS.late_start == 3_600
    assert p4.THRESHOLDS.phase_start == 3_000
    assert p4.THRESHOLDS.coupling_strength == 0.25
    assert p4.THRESHOLDS.offset_fractions == (5.0e-4, 1.0e-3, 2.0e-3)


def test_static_p4_construction_controls_pass_without_target_continuation() -> None:
    controls = p4._construction_controls()

    assert controls["pass"] is True
    assert all(controls["gates"].values())
    assert controls["age_ledger_control"]["truncated_ledger_fraction"] >= 0.01
    assert controls["values"]["wrong_chirality_amplitude"] >= (
        0.5 * p4.CANDIDATE.radius
    )


def test_frozen_p4_protocol_and_dependency_blobs_are_unchanged() -> None:
    assert p4._git_blob(p4.PROTOCOL.as_posix()) == p4.EXPECTED_BLOBS[
        p4.PROTOCOL.as_posix()
    ]
    assert all(
        p4._git_blob(path) == expected
        for path, expected in p4.EXPECTED_BLOBS.items()
    )
    result = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            p4.FREEZE_REVISION,
            "HEAD",
            "--",
            p4.PROTOCOL.as_posix(),
        ],
        cwd=p4.ROOT,
        check=False,
    )
    assert result.returncode == 0


def _arms() -> list[dict[str, object]]:
    return [
        {
            "chirality": chirality,
            "direction": direction,
            "offset_sign": offset_sign,
            "offset_fraction": offset_fraction,
            "complete": True,
            "ledger_pass": True,
            "dynamic_pass": True,
            "dynamic_gates": {"informative_signal": True},
        }
        for chirality in (1, -1)
        for direction in ("x", "y")
        for offset_sign in (1, -1)
        for offset_fraction in p4.THRESHOLDS.offset_fractions
    ]


def test_p4_layered_decision_does_not_promote_ledger_only() -> None:
    arms = _arms()
    decision, gates = p4._decision(
        pipeline=True,
        arms=arms,
        response={"pass": True},
    )
    assert decision == "p4-source-write-mechanics-pass"
    assert all(gates.values())

    dynamic_failure = copy.deepcopy(arms)
    dynamic_failure[0]["dynamic_pass"] = False
    decision, gates = p4._decision(
        pipeline=True,
        arms=dynamic_failure,
        response={"pass": True},
    )
    assert decision == "p4-source-write-ledger-only"
    assert gates["reciprocal_ledger"] is True
    assert gates["nonlinear_loop_mechanics"] is False

    ledger_failure = copy.deepcopy(arms)
    ledger_failure[0]["ledger_pass"] = False
    decision, _ = p4._decision(
        pipeline=True,
        arms=ledger_failure,
        response={"pass": True},
    )
    assert decision == "p4-source-write-architecture-fail"


def test_p4_signal_floor_and_pipeline_failures_remain_inconclusive() -> None:
    arms = _arms()
    no_signal = copy.deepcopy(arms)
    no_signal[0]["dynamic_gates"]["informative_signal"] = False
    decision, _ = p4._decision(
        pipeline=True,
        arms=no_signal,
        response={"pass": True},
    )
    assert decision == "p4-inconclusive"

    decision, _ = p4._decision(
        pipeline=False,
        arms=arms,
        response={"pass": True},
    )
    assert decision == "p4-inconclusive"


def test_p4_rejects_duplicate_registration_and_unavailable_response() -> None:
    arms = _arms()
    arms[-1] = copy.deepcopy(arms[0])
    decision, gates = p4._decision(
        pipeline=True,
        arms=arms,
        response={"available": True, "pass": True},
    )
    assert decision == "p4-inconclusive"
    assert gates["registration"] is False

    arms = _arms()
    decision, gates = p4._decision(
        pipeline=True,
        arms=arms,
        response={"available": False, "pass": False},
    )
    assert decision == "p4-inconclusive"
    assert gates["response_available"] is False

    incomplete = _arms()
    for arm in incomplete:
        arm["trace"] = [{"step": 0, "center": [0.0, 0.0]}]
    channel_off = {
        chirality: {"trace": [{"step": 0, "center": [0.0, 0.0]}]}
        for chirality in (1, -1)
    }
    response = p4._response_controls(incomplete, channel_off)
    assert response["available"] is False
    assert response["pass"] is False


def test_ideal_cayley_reference_is_exact_and_non_decisional() -> None:
    readout = p4.candidate_orbit_center_readout(p4.CANDIDATE, chirality=1)
    initial = 1.0e-3 * p4.CANDIDATE.radius * (1.0 + 0.0j)
    rival = p4._ideal_cayley_reference(initial, readout=readout)
    expected_factor = (
        1.0
        - p4.CANDIDATE.alpha
        * readout.write_gain
        * p4.THRESHOLDS.coupling_strength
    ) / (
        1.0
        + p4.CANDIDATE.alpha
        * readout.write_gain
        * p4.THRESHOLDS.coupling_strength
    )
    assert rival["factor_per_update"] == expected_factor
    assert rival["trace"][0]["center"] == [0.0, 0.0]
    assert rival["trace"][0]["actuator"] == [initial.real, initial.imag]
    assert rival["final_separation_ratio"] == expected_factor**4000


def test_failed_report_does_not_activate_conditional_claim_boundary() -> None:
    payload = {
        "decision": "p4-source-write-architecture-fail",
        "claim_boundary": {"established_if_full_pass": "conditional claim"},
    }
    lines = p4._claim_boundary_lines(payload)
    assert lines[0] == "Conditional full-pass boundary not activated."
    assert "would have established" in lines[1]

    payload["decision"] = "p4-source-write-mechanics-pass"
    lines = p4._claim_boundary_lines(payload)
    assert lines == ["Established by this full pass: conditional claim."]
