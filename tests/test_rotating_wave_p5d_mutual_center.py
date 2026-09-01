from __future__ import annotations

import ast
import copy
import inspect
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
    assert p5d.PHASES == tuple(
        (2 * index + 1) * math.pi / 8.0 for index in range(8)
    )
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
        assert readout_a.write_gain == pytest.approx(
            p5d.EXPECTED_WRITE_GAIN, abs=5e-16
        )
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
                "step": step,
                "center_a": p5d._pair(base_a),
                "center_b": p5d._pair(base_b),
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
                "initial_distance": initial_distance,
                "completed": True,
                "finite": True,
                "final_history_sha256_a": f"a-{distance}-{phase_index}-{chirality_a}-{chirality_b}",
                "final_history_sha256_b": f"b-{distance}-{phase_index}-{chirality_a}-{chirality_b}",
                "trace": off_trace,
                "ledger_gates": {"off": True},
                "loop_gates": {"off": True},
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
                                "step": step,
                                "center_a": p5d._pair(center_a),
                                "center_b": p5d._pair(center_b),
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
                            "coupling": sign * p5d.KAPPA_VALUES[kappa_name],
                            "initial_distance": initial_distance,
                            "completed": True,
                            "finite": True,
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
                            "ledger_gates": {"synthetic": True},
                            "loop_gates": {"synthetic": True},
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


def test_p5d_exactly_additive_reciprocal_trace_is_rejected(
    synthetic_panel: tuple[list[dict[str, object]], list[dict[str, object]]],
) -> None:
    off, active = copy.deepcopy(synthetic_panel)
    index = {p5d._active_key(row): row for row in active}
    for base in p5d.expected_base_keys():
        baseline = {sample["step"]: sample for sample in off[p5d.expected_base_keys().index(base)]["trace"]}
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
                        + 0.5
                        * (separation - p5d._complex(control["separation"]))
                    )
                    target["center_b"] = p5d._pair(
                        p5d._complex(control["center_b"])
                        - 0.5
                        * (separation - p5d._complex(control["separation"]))
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
    assert p5d.decision_from_gates(doubly_failed) == (
        "p5d-ledger-or-reciprocity-fail"
    )


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
    p5d._write_complete_outputs(
        summary_path=summary,
        summary_content='{"complete": true}\n',
        report_path=report,
        report_content="# P5-D complete\n",
    )
    assert summary.read_text(encoding="utf-8") == '{"complete": true}\n'
    assert report.read_text(encoding="utf-8") == "# P5-D complete\n"
    with pytest.raises(RuntimeError, match="existing P5-D output"):
        p5d._write_complete_outputs(
            summary_path=summary,
            summary_content="blocked",
            report_path=report,
            report_content="blocked",
        )
