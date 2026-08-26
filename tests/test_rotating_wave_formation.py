from __future__ import annotations

import numpy as np

from emergenz_knoten.rotating_wave_formation import (
    FormationThresholds,
    achiral_history,
    damped_hook_history,
    ellipse_history,
    evaluate_layered_decision,
    fifo_only_step,
    phase_increment_metrics,
    raw_mirror_error,
    reflect_history,
    registered_history_pairs,
    run_mirrored_pair,
    target_history,
    warped_history,
    wrong_rate_ellipse_history,
)
from emergenz_knoten.rotating_wave_stability_gate import RotatingWaveCandidate


def _candidate(*, horizon: int = 17) -> RotatingWaveCandidate:
    return RotatingWaveCandidate(
        candidate_id="synthetic-formation-control",
        radius=0.9,
        theta=0.08,
        alpha=0.1,
        horizon=horizon,
        memory_mass=1.0,
        eta=0.02,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=3.5,
    )


def test_registered_histories_are_exact_mirror_pairs() -> None:
    candidate = _candidate()
    pairs = registered_history_pairs(candidate)

    assert [row["panel"] for row in pairs] == [
        "prepared",
        "basin",
        "basin",
        "basin",
        "formation",
        "formation",
    ]
    assert all(
        np.array_equal(row["minus"], reflect_history(row["plus"])) for row in pairs
    )
    assert np.array_equal(
        target_history(candidate, chirality=-1),
        reflect_history(target_history(candidate, chirality=1)),
    )


def test_constructors_use_the_registered_geometries() -> None:
    candidate = _candidate(horizon=9)

    ellipse = ellipse_history(candidate, chirality=1, eccentricity=0.1)
    warped = warped_history(candidate, chirality=-1)
    wrong_rate = wrong_rate_ellipse_history(candidate, chirality=1)
    hook = damped_hook_history(candidate, chirality=-1)
    achiral = achiral_history(candidate)

    assert ellipse.shape == warped.shape == wrong_rate.shape == hook.shape == (9, 2)
    assert np.isclose(ellipse[0, 0], 1.1 * candidate.radius)
    assert np.isclose(wrong_rate[0, 0], candidate.sigma_rep)
    assert np.isclose(hook[0, 0], candidate.sigma_rep)
    assert np.count_nonzero(achiral[:, 1]) == 0
    assert not np.array_equal(ellipse, target_history(candidate, chirality=1))


def test_fifo_only_step_collapses_after_one_horizon() -> None:
    candidate = _candidate(horizon=11)
    state = damped_hook_history(candidate, chirality=1)
    visible = state[0].copy()

    for _ in range(candidate.horizon):
        state = fifo_only_step(state)

    assert np.array_equal(state, np.tile(visible, (candidate.horizon, 1)))


def test_phase_increment_metrics_accepts_only_registered_sign_and_rate() -> None:
    candidate = _candidate()
    thresholds = FormationThresholds(
        active_updates=20,
        sample_every=2,
        entrance_deadline=10,
        phase_start=10,
    )
    steps = range(thresholds.phase_start, thresholds.active_updates + 1, 2)
    plus_trace = [
        {"step": step, "alignment_phase": -candidate.theta * step}
        for step in steps
    ]

    accepted = phase_increment_metrics(
        plus_trace,
        chirality=1,
        candidate=candidate,
        thresholds=thresholds,
    )
    rejected = phase_increment_metrics(
        plus_trace,
        chirality=-1,
        candidate=candidate,
        thresholds=thresholds,
    )

    assert accepted["pass"] is True
    assert abs(accepted["mean_increment"] - candidate.theta) < 1.0e-15
    assert rejected["pass"] is False


def test_small_unrelated_pair_preserves_reflection_without_claiming_pass() -> None:
    candidate = _candidate(horizon=13)
    thresholds = FormationThresholds(
        active_updates=8,
        negative_updates=8,
        sample_every=1,
        entrance_deadline=4,
        phase_start=4,
    )
    plus = wrong_rate_ellipse_history(candidate, chirality=1)
    minus = reflect_history(plus)
    pair = run_mirrored_pair(
        name="synthetic_pair",
        panel="formation",
        plus_history=plus,
        minus_history=minus,
        candidate=candidate,
        thresholds=thresholds,
    )

    assert pair["mirror"]["pass"] is True
    assert pair["mirror"]["maximum_error"] == 0.0
    assert pair["plus"]["final_step"] == thresholds.active_updates
    assert pair["minus"]["final_step"] == thresholds.active_updates


def _arms(count: int, *, passed: bool) -> list[dict[str, bool]]:
    return [{"pass": passed} for _ in range(count)]


def test_layered_decision_does_not_promote_basin_only() -> None:
    decision, gates = evaluate_layered_decision(
        pipeline_controls=True,
        basin_arms=_arms(6, passed=True),
        formation_arms=_arms(4, passed=True),
    )
    assert decision == "p3-formation-basin-pass"
    assert gates["sampled_basin"] and gates["target_blind_formation"]

    decision, _ = evaluate_layered_decision(
        pipeline_controls=True,
        basin_arms=_arms(6, passed=True),
        formation_arms=_arms(4, passed=False),
    )
    assert decision == "p3-basin-only"

    decision, _ = evaluate_layered_decision(
        pipeline_controls=True,
        basin_arms=_arms(6, passed=False),
        formation_arms=_arms(4, passed=True),
    )
    assert decision == "p3-finite-basin-fail"

    decision, _ = evaluate_layered_decision(
        pipeline_controls=False,
        basin_arms=_arms(6, passed=True),
        formation_arms=_arms(4, passed=True),
    )
    assert decision == "p3-inconclusive"


def test_raw_mirror_error_rejects_unmirrored_changes() -> None:
    candidate = _candidate(horizon=7)
    plus = target_history(candidate, chirality=1)
    minus = reflect_history(plus)
    weights = np.full(candidate.horizon, 1.0 / candidate.horizon)

    assert raw_mirror_error(plus, minus, weights=weights) == 0.0
    minus[0, 0] += 0.01
    assert raw_mirror_error(plus, minus, weights=weights) > 0.0
