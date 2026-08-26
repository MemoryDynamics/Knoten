"""Formation and sampled-basin utilities for native rotating waves."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any

import numpy as np

from .rotating_wave_stability import (
    circular_history,
    finite_memory_weights,
    native_fifo_step,
    rotation_translation_quotient_distance,
)
from .rotating_wave_stability_gate import RotatingWaveCandidate


@dataclass(frozen=True)
class FormationThresholds:
    """Frozen thresholds for the P3 formation and sampled-basin gate."""

    active_updates: int = 12_000
    negative_updates: int = 2_400
    sample_every: int = 10
    entrance_deadline: int = 9_000
    phase_start: int = 10_000
    initial_distance_minimum_fraction: float = 0.02
    tube_fraction: float = 0.01
    final_fraction: float = 0.002
    opposite_target_minimum_fraction: float = 0.5
    phase_mean_error_fraction: float = 0.01
    phase_rms_error_fraction: float = 0.05
    mirror_error_fraction: float = 1.0e-11
    prepared_distance_fraction: float = 1.0e-10
    divergence_norm_sigma: float = 10.0
    centroid_stop_sigma: float = 1.0e6
    fifo_final_norm_fraction: float = 1.0e-12
    achiral_y_sigma: float = 1.0e-13
    achiral_target_minimum_fraction: float = 0.1


def _validate_chirality(chirality: int) -> int:
    if isinstance(chirality, bool) or chirality not in (-1, 1):
        raise ValueError("chirality must be +1 or -1")
    return int(chirality)


def reflect_history(history: np.ndarray) -> np.ndarray:
    """Reflect a planar FIFO history across the x axis."""

    state = np.asarray(history, dtype=float)
    if state.ndim != 2 or state.shape[1] != 2 or not np.isfinite(state).all():
        raise ValueError("history must be a finite array with shape (H,2)")
    result = state.copy()
    result[:, 1] *= -1.0
    return result


def target_history(
    candidate: RotatingWaveCandidate,
    *,
    chirality: int,
) -> np.ndarray:
    """Return the registered positive or reflected target history."""

    sign = _validate_chirality(chirality)
    plus = circular_history(
        radius=candidate.radius,
        theta=candidate.theta,
        horizon=candidate.horizon,
    )
    return plus if sign == 1 else reflect_history(plus)


def ellipse_history(
    candidate: RotatingWaveCandidate,
    *,
    chirality: int,
    eccentricity: float,
) -> np.ndarray:
    """Return the target-informed registered ellipse history."""

    sign = _validate_chirality(chirality)
    value = float(eccentricity)
    if not math.isfinite(value) or not 0.0 < value < 1.0:
        raise ValueError("eccentricity must lie strictly between zero and one")
    ages = np.arange(candidate.horizon, dtype=float)
    phase = ages * candidate.theta
    return np.column_stack(
        (
            candidate.radius * (1.0 + value) * np.cos(phase),
            -sign * candidate.radius * (1.0 - value) * np.sin(phase),
        )
    )


def warped_history(
    candidate: RotatingWaveCandidate,
    *,
    chirality: int,
) -> np.ndarray:
    """Return the frozen radial-plus-phase geometry holdout."""

    sign = _validate_chirality(chirality)
    ages = np.arange(candidate.horizon, dtype=float)
    base_phase = ages * candidate.theta
    radius = candidate.radius * (
        1.0 + 0.08 * np.cos(2.0 * base_phase + math.pi / 5.0)
    )
    phase = -sign * (base_phase + 0.08 * np.sin(base_phase))
    return np.column_stack((radius * np.cos(phase), radius * np.sin(phase)))


def wrong_rate_ellipse_history(
    candidate: RotatingWaveCandidate,
    *,
    chirality: int,
) -> np.ndarray:
    """Return a target-blind ellipse using alpha and sigma_rep only."""

    sign = _validate_chirality(chirality)
    ages = np.arange(candidate.horizon, dtype=float)
    phase = candidate.alpha * ages
    return candidate.sigma_rep * np.column_stack(
        (np.cos(phase), -0.6 * sign * np.sin(phase))
    )


def damped_hook_history(
    candidate: RotatingWaveCandidate,
    *,
    chirality: int,
) -> np.ndarray:
    """Return the target-blind nonperiodic damped-hook history."""

    sign = _validate_chirality(chirality)
    ages = np.arange(candidate.horizon, dtype=float)
    memory_time = candidate.alpha * ages
    decay = np.exp(-memory_time)
    return candidate.sigma_rep * np.column_stack(
        (decay, -sign * memory_time * decay)
    )


def achiral_history(candidate: RotatingWaveCandidate) -> np.ndarray:
    """Return the exactly collinear invariant-subspace control."""

    ages = np.arange(candidate.horizon, dtype=float)
    x_values = candidate.sigma_rep * np.exp(-candidate.alpha * ages)
    return np.column_stack((x_values, np.zeros(candidate.horizon)))


def registered_history_pairs(
    candidate: RotatingWaveCandidate,
) -> list[dict[str, Any]]:
    """Construct the six mirrored pairs frozen by the P3 protocol."""

    return [
        {
            "name": "prepared_circle",
            "panel": "prepared",
            "plus": target_history(candidate, chirality=1),
            "minus": target_history(candidate, chirality=-1),
        },
        {
            "name": "ellipse_e0p03",
            "panel": "basin",
            "plus": ellipse_history(candidate, chirality=1, eccentricity=0.03),
            "minus": ellipse_history(candidate, chirality=-1, eccentricity=0.03),
        },
        {
            "name": "ellipse_e0p10",
            "panel": "basin",
            "plus": ellipse_history(candidate, chirality=1, eccentricity=0.10),
            "minus": ellipse_history(candidate, chirality=-1, eccentricity=0.10),
        },
        {
            "name": "warped_geometry_holdout",
            "panel": "basin",
            "plus": warped_history(candidate, chirality=1),
            "minus": warped_history(candidate, chirality=-1),
        },
        {
            "name": "wrong_rate_ellipse",
            "panel": "formation",
            "plus": wrong_rate_ellipse_history(candidate, chirality=1),
            "minus": wrong_rate_ellipse_history(candidate, chirality=-1),
        },
        {
            "name": "damped_hook_holdout",
            "panel": "formation",
            "plus": damped_hook_history(candidate, chirality=1),
            "minus": damped_hook_history(candidate, chirality=-1),
        },
    ]


def normalized_memory_weights(candidate: RotatingWaveCandidate) -> np.ndarray:
    """Return normalized finite-H weights for one candidate."""

    weights = finite_memory_weights(
        alpha=candidate.alpha,
        horizon=candidate.horizon,
        memory_mass=candidate.memory_mass,
    )
    return weights / np.sum(weights)


def translation_reduced_metrics(
    history: np.ndarray,
    *,
    weights: np.ndarray,
) -> tuple[float, np.ndarray]:
    """Return D0-style translation-reduced norm and memory centroid."""

    state = np.asarray(history, dtype=float)
    normalized = np.asarray(weights, dtype=float)
    if state.ndim != 2 or state.shape[1] != 2:
        raise ValueError("history must have shape (H,2)")
    if normalized.shape != (state.shape[0],):
        raise ValueError("weights must match the history horizon")
    center = np.sum(normalized[:, None] * state, axis=0)
    features = state - center
    metric_weights = normalized.copy()
    metric_weights[0] = 1.0
    norm = math.sqrt(float(np.sum(metric_weights[:, None] * features * features)))
    return norm, center


def raw_mirror_error(
    plus: np.ndarray,
    minus: np.ndarray,
    *,
    weights: np.ndarray,
) -> float:
    """Return the unfitted registered reflection error of a mirrored pair."""

    reflected = reflect_history(plus)
    difference = np.asarray(minus, dtype=float) - reflected
    normalized = np.asarray(weights, dtype=float)
    if normalized.shape != (difference.shape[0],):
        raise ValueError("weights must match the history horizon")
    metric_weights = normalized.copy()
    metric_weights[0] = 1.0
    return math.sqrt(
        float(np.sum(metric_weights[:, None] * difference * difference))
    )


def _sample_metrics(
    state: np.ndarray,
    *,
    step: int,
    chirality: int,
    targets: dict[int, np.ndarray],
    candidate: RotatingWaveCandidate,
    weights: np.ndarray,
) -> dict[str, float | int]:
    expected_distance, alignment = rotation_translation_quotient_distance(
        state,
        targets[chirality],
        alpha=candidate.alpha,
        memory_mass=candidate.memory_mass,
    )
    opposite_distance, _ = rotation_translation_quotient_distance(
        state,
        targets[-chirality],
        alpha=candidate.alpha,
        memory_mass=candidate.memory_mass,
    )
    reduced_norm, center = translation_reduced_metrics(state, weights=weights)
    return {
        "step": int(step),
        "expected_d0": expected_distance,
        "expected_d0_fraction": expected_distance / candidate.radius,
        "opposite_d0": opposite_distance,
        "opposite_d0_fraction": opposite_distance / candidate.radius,
        "alignment_phase": alignment,
        "translation_reduced_norm": reduced_norm,
        "translation_reduced_norm_fraction": reduced_norm / candidate.radius,
        "centroid_x": float(center[0]),
        "centroid_y": float(center[1]),
        "centroid_norm": float(np.linalg.norm(center)),
    }


def _scientific_stop_reason(
    state: np.ndarray,
    *,
    candidate: RotatingWaveCandidate,
    thresholds: FormationThresholds,
    weights: np.ndarray,
) -> str | None:
    if not np.isfinite(state).all():
        return "nonfinite-state"
    reduced_norm, center = translation_reduced_metrics(state, weights=weights)
    if reduced_norm > thresholds.divergence_norm_sigma * candidate.sigma_rep:
        return "translation-reduced-norm-stop"
    if np.linalg.norm(center) > thresholds.centroid_stop_sigma * candidate.sigma_rep:
        return "centroid-stop"
    return None


def phase_increment_metrics(
    trace: list[dict[str, Any]],
    *,
    chirality: int,
    candidate: RotatingWaveCandidate,
    thresholds: FormationThresholds,
) -> dict[str, float | int | bool | None]:
    """Measure the registered late native phase increment."""

    sign = _validate_chirality(chirality)
    rows = [row for row in trace if row["step"] >= thresholds.phase_start]
    expected_count = (
        (thresholds.active_updates - thresholds.phase_start)
        // thresholds.sample_every
        + 1
    )
    if len(rows) != expected_count or len(rows) < 2:
        return {
            "sample_count": len(rows),
            "expected_sample_count": expected_count,
            "mean_increment": None,
            "expected_increment": sign * candidate.theta,
            "mean_absolute_error": None,
            "rms_error": None,
            "pass": False,
        }
    steps = np.asarray([row["step"] for row in rows], dtype=float)
    angles = np.unwrap(
        np.asarray([row["alignment_phase"] for row in rows], dtype=float)
    )
    increments = -np.diff(angles) / np.diff(steps)
    expected = sign * candidate.theta
    mean_increment = float(np.mean(increments))
    mean_error = abs(mean_increment - expected)
    rms_error = float(math.sqrt(np.mean((increments - expected) ** 2)))
    return {
        "sample_count": len(rows),
        "expected_sample_count": expected_count,
        "mean_increment": mean_increment,
        "expected_increment": expected,
        "mean_absolute_error": mean_error,
        "mean_error_threshold": thresholds.phase_mean_error_fraction
        * candidate.theta,
        "rms_error": rms_error,
        "rms_error_threshold": thresholds.phase_rms_error_fraction
        * candidate.theta,
        "pass": bool(
            mean_error
            <= thresholds.phase_mean_error_fraction * candidate.theta
            and rms_error <= thresholds.phase_rms_error_fraction * candidate.theta
        ),
    }


def evaluate_non_circular_arm(
    arm: dict[str, Any],
    *,
    candidate: RotatingWaveCandidate,
    thresholds: FormationThresholds,
) -> dict[str, Any]:
    """Apply the frozen entrance, dwell, chirality and phase gates."""

    trace = arm["trace"]
    initial = trace[0]["expected_d0_fraction"]
    entrance_rows = [
        row for row in trace if row["expected_d0_fraction"] <= thresholds.tube_fraction
    ]
    first_entrance = entrance_rows[0]["step"] if entrance_rows else None
    dwell = [row for row in trace if row["step"] >= thresholds.entrance_deadline]
    expected_dwell_count = (
        (thresholds.active_updates - thresholds.entrance_deadline)
        // thresholds.sample_every
        + 1
    )
    dwell_maximum = (
        max(row["expected_d0_fraction"] for row in dwell) if dwell else None
    )
    opposite_minimum = (
        min(row["opposite_d0_fraction"] for row in dwell) if dwell else None
    )
    final_fraction = (
        trace[-1]["expected_d0_fraction"]
        if trace and trace[-1]["step"] == thresholds.active_updates
        else None
    )
    phase = phase_increment_metrics(
        trace,
        chirality=arm["chirality"],
        candidate=candidate,
        thresholds=thresholds,
    )
    gates = {
        "initial_nontrivial": bool(
            initial >= thresholds.initial_distance_minimum_fraction
        ),
        "complete": bool(
            not arm["stopped"] and arm["final_step"] == thresholds.active_updates
        ),
        "entrance": bool(
            first_entrance is not None
            and first_entrance <= thresholds.entrance_deadline
        ),
        "dwell": bool(
            len(dwell) == expected_dwell_count
            and dwell_maximum is not None
            and dwell_maximum <= thresholds.tube_fraction
        ),
        "final": bool(
            final_fraction is not None
            and final_fraction <= thresholds.final_fraction
        ),
        "opposite_separation": bool(
            opposite_minimum is not None
            and opposite_minimum >= thresholds.opposite_target_minimum_fraction
        ),
        "phase": bool(phase["pass"]),
    }
    return {
        **arm,
        "first_entrance_step": first_entrance,
        "dwell_sample_count": len(dwell),
        "expected_dwell_sample_count": expected_dwell_count,
        "dwell_maximum_fraction": dwell_maximum,
        "opposite_dwell_minimum_fraction": opposite_minimum,
        "final_fraction": final_fraction,
        "phase": phase,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def evaluate_prepared_arm(
    arm: dict[str, Any],
    *,
    candidate: RotatingWaveCandidate,
    thresholds: FormationThresholds,
) -> dict[str, Any]:
    """Apply the exact prepared-circle positive-control gates."""

    trace = arm["trace"]
    phase = phase_increment_metrics(
        trace,
        chirality=arm["chirality"],
        candidate=candidate,
        thresholds=thresholds,
    )
    maximum_own = max(row["expected_d0_fraction"] for row in trace)
    opposite_rows = [row for row in trace if row["step"] > 0]
    opposite_minimum = min(row["opposite_d0_fraction"] for row in opposite_rows)
    gates = {
        "complete": bool(
            not arm["stopped"] and arm["final_step"] == thresholds.active_updates
        ),
        "own_target": bool(maximum_own <= thresholds.prepared_distance_fraction),
        "opposite_separation": bool(
            opposite_minimum >= thresholds.opposite_target_minimum_fraction
        ),
        "phase": bool(phase["pass"]),
    }
    return {
        **arm,
        "maximum_own_target_fraction": maximum_own,
        "opposite_minimum_fraction": opposite_minimum,
        "phase": phase,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def run_mirrored_pair(
    *,
    name: str,
    panel: str,
    plus_history: np.ndarray,
    minus_history: np.ndarray,
    candidate: RotatingWaveCandidate,
    thresholds: FormationThresholds,
) -> dict[str, Any]:
    """Advance one registered mirrored pair under the native FIFO map."""

    targets = {
        1: target_history(candidate, chirality=1),
        -1: target_history(candidate, chirality=-1),
    }
    weights = normalized_memory_weights(candidate)
    states = {1: np.asarray(plus_history, dtype=float).copy(), -1: np.asarray(minus_history, dtype=float).copy()}
    traces = {
        sign: [
            _sample_metrics(
                states[sign],
                step=0,
                chirality=sign,
                targets=targets,
                candidate=candidate,
                weights=weights,
            )
        ]
        for sign in (1, -1)
    }
    mirror_errors = [raw_mirror_error(states[1], states[-1], weights=weights)]
    stopped = {1: False, -1: False}
    reasons = {1: "completed", -1: "completed"}
    final_step = 0
    for step in range(1, thresholds.active_updates + 1):
        for sign in (1, -1):
            states[sign] = native_fifo_step(
                states[sign],
                **candidate.step_parameters(),
            )
        final_step = step
        step_reasons = {
            sign: _scientific_stop_reason(
                states[sign],
                candidate=candidate,
                thresholds=thresholds,
                weights=weights,
            )
            for sign in (1, -1)
        }
        should_sample = step % thresholds.sample_every == 0
        finite_pair = all(np.isfinite(states[sign]).all() for sign in (1, -1))
        if finite_pair and (should_sample or any(step_reasons.values())):
            for sign in (1, -1):
                traces[sign].append(
                    _sample_metrics(
                        states[sign],
                        step=step,
                        chirality=sign,
                        targets=targets,
                        candidate=candidate,
                        weights=weights,
                    )
                )
            mirror_errors.append(
                raw_mirror_error(states[1], states[-1], weights=weights)
            )
        if any(reason is not None for reason in step_reasons.values()):
            for sign in (1, -1):
                stopped[sign] = step_reasons[sign] is not None
                reasons[sign] = step_reasons[sign] or "paired-scientific-stop"
            break

    arms: dict[int, dict[str, Any]] = {}
    for sign in (1, -1):
        arms[sign] = {
            "name": f"{name}_{'plus' if sign == 1 else 'minus'}",
            "family": name,
            "panel": panel,
            "chirality": sign,
            "initial_expected_d0_fraction": traces[sign][0][
                "expected_d0_fraction"
            ],
            "initial_opposite_d0_fraction": traces[sign][0][
                "opposite_d0_fraction"
            ],
            "stopped": stopped[sign],
            "stop_reason": reasons[sign],
            "final_step": final_step,
            "trace": traces[sign],
        }
    evaluated = {
        sign: (
            evaluate_prepared_arm(
                arms[sign], candidate=candidate, thresholds=thresholds
            )
            if panel == "prepared"
            else evaluate_non_circular_arm(
                arms[sign], candidate=candidate, thresholds=thresholds
            )
        )
        for sign in (1, -1)
    }
    maximum_mirror = max(mirror_errors)
    same_stop = bool(
        stopped[1] == stopped[-1]
        and reasons[1] == reasons[-1]
        and evaluated[1]["final_step"] == evaluated[-1]["final_step"]
    )
    mirror = {
        "sample_count": len(mirror_errors),
        "maximum_error": maximum_mirror,
        "maximum_fraction": maximum_mirror / candidate.radius,
        "threshold": thresholds.mirror_error_fraction * candidate.radius,
        "same_stop": same_stop,
        "pass": bool(
            maximum_mirror <= thresholds.mirror_error_fraction * candidate.radius
            and same_stop
        ),
    }
    return {
        "name": name,
        "panel": panel,
        "plus": evaluated[1],
        "minus": evaluated[-1],
        "mirror": mirror,
        "pass": bool(evaluated[1]["pass"] and evaluated[-1]["pass"]),
    }


def fifo_only_step(history: np.ndarray) -> np.ndarray:
    """Advance the exact eta=0 FIFO limit without evaluating a force."""

    state = np.asarray(history, dtype=float)
    if state.ndim != 2 or state.shape[0] < 1 or state.shape[1] != 2:
        raise ValueError("history must have shape (H,2)")
    result = np.empty_like(state)
    result[0] = state[0]
    if state.shape[0] > 1:
        result[1:] = state[:-1]
    return result


def run_fifo_only_control(
    candidate: RotatingWaveCandidate,
    thresholds: FormationThresholds,
) -> dict[str, Any]:
    """Run the registered eta=0 FIFO-collapse negative control."""

    state = damped_hook_history(candidate, chirality=1)
    targets = {
        1: target_history(candidate, chirality=1),
        -1: target_history(candidate, chirality=-1),
    }
    weights = normalized_memory_weights(candidate)
    trace: list[dict[str, Any]] = []
    for step in range(thresholds.negative_updates + 1):
        if step % thresholds.sample_every == 0:
            plus_distance, _ = rotation_translation_quotient_distance(
                state,
                targets[1],
                alpha=candidate.alpha,
                memory_mass=candidate.memory_mass,
            )
            minus_distance, _ = rotation_translation_quotient_distance(
                state,
                targets[-1],
                alpha=candidate.alpha,
                memory_mass=candidate.memory_mass,
            )
            reduced_norm, _ = translation_reduced_metrics(state, weights=weights)
            trace.append(
                {
                    "step": step,
                    "plus_d0_fraction": plus_distance / candidate.radius,
                    "minus_d0_fraction": minus_distance / candidate.radius,
                    "translation_reduced_norm_fraction": reduced_norm
                    / candidate.radius,
                }
            )
        if step < thresholds.negative_updates:
            state = fifo_only_step(state)
    final = trace[-1]
    gates = {
        "complete": bool(trace[-1]["step"] == thresholds.negative_updates),
        "collapsed": bool(
            final["translation_reduced_norm_fraction"]
            <= thresholds.fifo_final_norm_fraction
        ),
        "not_target": bool(
            min(final["plus_d0_fraction"], final["minus_d0_fraction"])
            >= thresholds.opposite_target_minimum_fraction
        ),
    }
    return {
        "name": "fifo_only_eta0_damped_hook",
        "eta": 0.0,
        "trace": trace,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def run_achiral_control(
    candidate: RotatingWaveCandidate,
    thresholds: FormationThresholds,
) -> dict[str, Any]:
    """Run the registered exact-collinear invariant-subspace control."""

    state = achiral_history(candidate)
    targets = {
        1: target_history(candidate, chirality=1),
        -1: target_history(candidate, chirality=-1),
    }
    maximum_y = float(np.max(np.abs(state[:, 1])))
    trace: list[dict[str, Any]] = []
    complete = True
    for step in range(thresholds.negative_updates + 1):
        if step % thresholds.sample_every == 0:
            distances = []
            for sign in (1, -1):
                distance, _ = rotation_translation_quotient_distance(
                    state,
                    targets[sign],
                    alpha=candidate.alpha,
                    memory_mass=candidate.memory_mass,
                )
                distances.append(distance / candidate.radius)
            trace.append(
                {
                    "step": step,
                    "plus_d0_fraction": distances[0],
                    "minus_d0_fraction": distances[1],
                    "minimum_target_fraction": min(distances),
                }
            )
        if step < thresholds.negative_updates:
            state = native_fifo_step(state, **candidate.step_parameters())
            if not np.isfinite(state).all():
                complete = False
                break
            maximum_y = max(maximum_y, float(np.max(np.abs(state[:, 1]))))
    minimum_target = min(row["minimum_target_fraction"] for row in trace)
    gates = {
        "complete": bool(
            complete and trace[-1]["step"] == thresholds.negative_updates
        ),
        "invariant_subspace": bool(
            maximum_y <= thresholds.achiral_y_sigma * candidate.sigma_rep
        ),
        "not_target": bool(
            minimum_target >= thresholds.achiral_target_minimum_fraction
        ),
    }
    return {
        "name": "active_achiral_collinear",
        "maximum_absolute_y": maximum_y,
        "minimum_target_fraction": minimum_target,
        "trace": trace,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def evaluate_layered_decision(
    *,
    pipeline_controls: bool,
    basin_arms: list[dict[str, Any]],
    formation_arms: list[dict[str, Any]],
) -> tuple[str, dict[str, bool]]:
    """Apply the preregistered layered P3 decision semantics."""

    basin_registration = len(basin_arms) == 6
    formation_registration = len(formation_arms) == 4
    basin_pass = bool(basin_registration and all(row["pass"] for row in basin_arms))
    formation_pass = bool(
        formation_registration and all(row["pass"] for row in formation_arms)
    )
    controls = bool(
        pipeline_controls and basin_registration and formation_registration
    )
    if not controls:
        decision = "p3-inconclusive"
    elif basin_pass and formation_pass:
        decision = "p3-formation-basin-pass"
    elif basin_pass:
        decision = "p3-basin-only"
    else:
        decision = "p3-finite-basin-fail"
    return decision, {
        "pipeline_controls": controls,
        "basin_registration": basin_registration,
        "formation_registration": formation_registration,
        "sampled_basin": basin_pass,
        "target_blind_formation": formation_pass,
    }


def thresholds_payload(thresholds: FormationThresholds) -> dict[str, Any]:
    """Return a JSON-ready copy of the frozen thresholds."""

    return asdict(thresholds)
