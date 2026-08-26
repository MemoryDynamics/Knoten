from __future__ import annotations

import copy
from dataclasses import replace
import math

import numpy as np
import pytest

from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4r_phase_metrology_gate as p4r,
)
from emergenz_knoten.orbit_center_actuator import (
    candidate_orbit_center_readout,
    reciprocal_source_write_step,
    source_write_rounding_metrology,
)
from emergenz_knoten.rotating_wave_stability_gate import RotatingWaveCandidate


def test_p4r_registration_matches_frozen_protocol() -> None:
    assert p4r.CANDIDATE.candidate_id == p4r.CANDIDATE_ID
    assert p4r.CANDIDATE.horizon == 2400
    assert p4r.THRESHOLDS.active_updates == 4_000
    assert p4r.THRESHOLDS.sample_every == 10
    assert p4r.THRESHOLDS.coupling_strength == 0.25
    assert p4r.THRESHOLDS.offset_fraction == 1.5e-3
    assert p4r.THRESHOLDS.reference_steps == (1, 2_000, 4_000)
    assert p4r.THRESHOLDS.reference_dps == 80
    assert p4r.THRESHOLDS.scalar_null_maximum == 0.05
    assert p4r.THRESHOLDS.chiral_minimum == 0.10
    assert p4r.THRESHOLDS.sign_support_minimum == 6
    assert p4r.PHASES == tuple(
        (2 * index + 1) * math.pi / 8.0 for index in range(8)
    )
    assert p4r._expected_channel_off_keys() == [
        (phase_index, chirality)
        for phase_index in range(8)
        for chirality in (1, -1)
    ]
    assert p4r._expected_active_keys() == [
        (phase_index, chirality, offset_sign)
        for phase_index in range(8)
        for chirality in (1, -1)
        for offset_sign in (1, -1)
    ]


def test_p4r_static_controls_pass_without_target_continuation() -> None:
    construction = p4r.p4._construction_controls()
    registration = p4r._registration_controls()

    assert construction["pass"] is True
    assert all(construction["gates"].values())
    assert registration["pass"] is True
    assert all(registration["gates"].values())
    assert registration["maximum_mirror_history_error"] < 1e-14
    assert registration["maximum_half_turn_history_error"] < 1e-14


def test_frozen_p4r_protocol_charter_and_dependencies_are_unchanged() -> None:
    assert all(
        p4r._git_blob(path) == expected
        for path, expected in p4r.EXPECTED_HEAD_BLOBS.items()
    )
    assert all(
        p4r._git_blob(path, revision=p4r.PROTOCOL_FREEZE_REVISION)
        == expected
        for path, expected in p4r.EXPECTED_PREIMPLEMENTATION_BLOBS.items()
    )


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
        for phase_index, chirality, offset_sign in p4r._expected_active_keys()
    ]


def _decision_channel_off() -> list[dict[str, int]]:
    return [
        {"phase_index": phase_index, "chirality": chirality}
        for phase_index, chirality in p4r._expected_channel_off_keys()
    ]


def _decision_response(
    center: float,
    actuator: float,
    *,
    center_support: int = 8,
    actuator_support: int = 8,
) -> dict[str, object]:
    return {
        "available": True,
        "pass": True,
        "phase_averaged_transverse_response": {
            "center": center,
            "actuator": actuator,
        },
        "positive_phase_support": {
            "center": center_support,
            "actuator": actuator_support,
        },
    }


def _decide(
    response: dict[str, object],
    *,
    pipeline: bool = True,
    active_arms: list[dict[str, object]] | None = None,
    channel_off_arms: list[dict[str, int]] | None = None,
) -> tuple[str, dict[str, bool]]:
    return p4r._decision(
        pipeline=pipeline,
        active_arms=active_arms or _decision_arms(),
        channel_off_arms=channel_off_arms or _decision_channel_off(),
        response=response,
    )


def test_p4r_decision_table_covers_all_registered_outcomes() -> None:
    decision, _ = _decide(_decision_response(0.04, -0.05))
    assert decision == "p4r-phase-averaged-scalar-response"

    decision, _ = _decide(_decision_response(0.12, 0.11))
    assert decision == "p4r-phase-averaged-chiral-response-pass"

    decision, _ = _decide(_decision_response(-0.10, 0.12))
    assert decision == "p4r-phase-averaged-chiral-hypothesis-fail"

    decision, _ = _decide(_decision_response(0.12, -0.10))
    assert decision == "p4r-phase-averaged-chiral-hypothesis-fail"

    decision, _ = _decide(_decision_response(0.07, 0.08))
    assert decision == "p4r-inconclusive"

    decision, _ = _decide(
        _decision_response(
            0.12,
            0.11,
            center_support=5,
            actuator_support=8,
        )
    )
    assert decision == "p4r-inconclusive"


def test_p4r_decision_precedence_is_layered() -> None:
    response = _decision_response(0.12, 0.11)
    ledger_failure = copy.deepcopy(_decision_arms())
    ledger_failure[0]["ledger_pass"] = False
    decision, gates = _decide(response, active_arms=ledger_failure)
    assert decision == "p4r-ledger-or-metrology-fail"
    assert gates["reciprocal_ledger_and_metrology"] is False

    invalid = copy.deepcopy(ledger_failure)
    invalid[0]["valid"] = False
    decision, gates = _decide(response, active_arms=invalid)
    assert decision == "p4r-inconclusive"
    assert gates["valid_active_arms"] is False

    dynamic_failure = copy.deepcopy(_decision_arms())
    dynamic_failure[0]["dynamic_pass"] = False
    decision, gates = _decide(response, active_arms=dynamic_failure)
    assert decision == "p4r-inconclusive"
    assert gates["nonlinear_loop_dynamics"] is False

    unavailable = copy.deepcopy(response)
    unavailable["available"] = False
    unavailable["pass"] = False
    decision, _ = _decide(unavailable)
    assert decision == "p4r-inconclusive"

    misregistered = _decision_arms()
    misregistered[-1] = copy.deepcopy(misregistered[0])
    decision, gates = _decide(response, active_arms=misregistered)
    assert decision == "p4r-inconclusive"
    assert gates["registration"] is False

    decision, _ = _decide(response, pipeline=False)
    assert decision == "p4r-inconclusive"


def _pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def _synthetic_response_panel(
    *,
    center_transverse: float = 0.20,
    actuator_transverse: float = 0.15,
    even_fraction: float = 0.0,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    steps = np.arange(
        0,
        p4r.THRESHOLDS.active_updates + 1,
        p4r.THRESHOLDS.sample_every,
    )
    ramp = steps / p4r.THRESHOLDS.active_updates
    delta = p4r.THRESHOLDS.offset_fraction * p4r.CANDIDATE.radius
    controls: list[dict[str, object]] = []
    active: list[dict[str, object]] = []
    for phase_index, chirality in p4r._expected_channel_off_keys():
        zero_trace = [
            {
                "step": int(step),
                "center": [0.0, 0.0],
                "actuator": [0.0, 0.0],
            }
            for step in steps
        ]
        controls.append(
            {
                "phase_index": phase_index,
                "chirality": chirality,
                "trace": zero_trace,
            }
        )
    for phase_index, chirality, offset_sign in p4r._expected_active_keys():
        center_odd = ramp * (0.45 - 1j * chirality * center_transverse)
        actuator_odd = ramp * (
            0.40 - 1j * chirality * actuator_transverse
        )
        center_even = even_fraction * center_odd
        actuator_even = even_fraction * actuator_odd
        center = delta * (offset_sign * center_odd + center_even)
        actuator = delta * (offset_sign * actuator_odd + actuator_even)
        trace = [
            {
                "step": int(step),
                "center": _pair(complex(center[index])),
                "actuator": _pair(complex(actuator[index])),
            }
            for index, step in enumerate(steps)
        ]
        active.append(
            {
                "phase_index": phase_index,
                "chirality": chirality,
                "offset_sign": offset_sign,
                "trace": trace,
            }
        )
    return active, controls


def test_p4r_synthetic_phase_response_recovers_registered_chiral_signal() -> None:
    active, controls = _synthetic_response_panel()
    response = p4r._response_controls(active, controls)

    assert response["available"] is True
    assert response["pass"] is True
    assert all(response["gates"].values())
    means = response["phase_averaged_transverse_response"]
    assert math.isclose(means["center"], 0.20, abs_tol=2e-15)
    assert math.isclose(means["actuator"], 0.15, abs_tol=2e-15)
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


def test_p4r_synthetic_response_falsifies_even_and_registration_controls() -> None:
    active, controls = _synthetic_response_panel(even_fraction=0.03)
    response = p4r._response_controls(active, controls)
    assert response["available"] is True
    assert response["gates"]["even_response"] is False
    assert response["pass"] is False

    response = p4r._response_controls(active[:-1], controls)
    assert response["available"] is False
    assert response["reason"] == "misregistered-panel"


def _small_candidate() -> RotatingWaveCandidate:
    return RotatingWaveCandidate(
        candidate_id="p4r-synthetic-h17",
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


def test_p4r_exact_ratio_high_precision_reference_detects_corruption() -> None:
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
    reference = p4r._high_precision_reference(
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
    reference = p4r._high_precision_reference(
        corrupted,
        corrupted_metrology,
        readout=readout,
        update=1,
    )
    assert reference["pass"] is False
    assert reference["gates"]["center_binary64_distance"] is False


def test_p4r_default_outputs_are_registered_and_writes_are_atomic(
    tmp_path,
) -> None:
    assert p4r._is_default_output(p4r.DEFAULT_SUMMARY, p4r.DEFAULT_SUMMARY)
    assert p4r._is_default_output(p4r.DEFAULT_REPORT, p4r.DEFAULT_REPORT)

    output = tmp_path / "synthetic.json"
    p4r._atomic_write(output, "complete\n")
    assert output.read_text(encoding="utf-8") == "complete\n"
    assert not output.with_name("synthetic.json.tmp").exists()

    stale = tmp_path / "blocked.json"
    stale.with_name("blocked.json.tmp").write_text("stale", encoding="utf-8")
    with pytest.raises(RuntimeError, match="stale temporary"):
        p4r._atomic_write(stale, "must-not-write\n")
    assert not stale.exists()
