"""Execute the frozen P2 local Loop--Center response gate at L3."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import subprocess
import time
from typing import Any

import numpy as np

from emergenz_knoten.loop_center_response import (
    co_rotating_fifo_forced_step,
    finite_h_center_recurrence,
    laboratory_center_displacement,
    memory_center,
    native_fifo_forced_step,
    normalized_memory_weights,
    registered_zero_sum_waveforms,
    tangent_fifo_forced_step,
)
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    co_rotating_fifo_jacobian,
    co_rotating_fifo_step,
    rotation_matrix,
    rotation_translation_quotient_distance,
)
from emergenz_knoten.rotating_wave_stability_gate import RotatingWaveCandidate


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_loop_center_p2_protocol_2026-08-25.md"
)
LINEARIZATION_AUDIT = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_loop_center_linearization_audit_2026-08-25.md"
)
P1_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_l3_stability_2026-08-22.json"
)
P1_REVIEW = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_l3_stability_review_2026-08-22.md"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/scalar_memory_loop_center_p2_2026-08-25.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/scalar_memory_loop_center_p2_2026-08-25.json"
)

FREEZE_REVISION = "60aa3d12f891008eb579dcf56e96cf8fbb3fa54d"
EXPECTED_BLOBS = {
    PROTOCOL.as_posix(): "13b7c65557f911d74a47846fa3ba5b59368661d6",
    P1_RESULT.as_posix(): "18821ed0235e5e915424f61c665be86d569d58cc",
    P1_REVIEW.as_posix(): "8fa25608f165789662ca1fb92d2507791dc143ea",
    "src/emergenz_knoten/rotating_wave_stability.py": (
        "9defb5a6876371202e1ba57cea030c997b9c6edd"
    ),
    "src/emergenz_knoten/rotating_wave_stability_gate.py": (
        "630beb9952abefea823d91388dcbb2de8f1a2927"
    ),
}

CANDIDATE_ID = "k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1"
RADIUS_DECIMAL = (
    "0.944805811705743656419366118422595657454474452804188781825799206245348"
    "464567689511866917417017911971955244464"
)
THETA_DECIMAL = (
    "0.007906661462435523749384967030309742461978034595274092598156965831417"
    "08245813094145986593003659167675765833059"
)
CANDIDATE = RotatingWaveCandidate(
    candidate_id=CANDIDATE_ID,
    radius=float(RADIUS_DECIMAL),
    theta=float(THETA_DECIMAL),
    alpha=0.005,
    horizon=2400,
    memory_mass=1.0,
    eta=0.075,
    sigma_rep=1.0,
    sigma_att=3.0,
    amplitude_rep=1.0,
    amplitude_att=3.5,
)

PRIMARY_AMPLITUDES = (1.0e-5, 3.0e-5, 1.0e-4)
HOLDOUT_AMPLITUDE = 3.0e-5
PROBE_UPDATES = 400
RECOVERY_UPDATES = 2000
TOTAL_UPDATES = PROBE_UPDATES + RECOVERY_UPDATES
TAIL_UPDATES = 400
TRACE_EVERY = 10
DIRECTIONS = {
    "radial": np.asarray([1.0, 0.0]),
    "tangential": np.asarray([0.0, 1.0]),
}
PHASES = (0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0)


@dataclass(frozen=True)
class P2Thresholds:
    """Frozen thresholds from the published P2 protocol."""

    fixed_point_component: float = 1.0e-14
    jacobian_relative: float = 2.0e-9
    center_recurrence_fraction: float = 5.0e-13
    phase_covariance_fraction: float = 1.0e-11
    probe_off_fraction: float = 1.0e-10
    primary_tangent_relative: float = 0.005
    primary_even_relative: float = 0.02
    primary_remainder_relative: float = 0.02
    primary_collapse_relative: float = 0.005
    signal_fraction: float = 1.0e-3
    remainder_slope_minimum: float = 1.5
    remainder_slope_maximum: float = 2.5
    holdout_tangent_relative: float = 0.01
    holdout_even_relative: float = 0.03
    loop_maximum_fraction: float = 0.01
    loop_final_ratio: float = 0.05
    loop_tail_slope_per_memory_time: float = 1.0e-3


THRESHOLDS = P2Thresholds()


def _git_output(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def _git_blob(path: str) -> str:
    return _git_output(["rev-parse", f"HEAD:{path}"])


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _verify_provenance() -> dict[str, Any]:
    status = _git_output(["status", "--short"])
    if status:
        raise RuntimeError("P2 target gate requires a clean prospective revision")
    revision = _git_output(["rev-parse", "HEAD"])
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", FREEZE_REVISION, revision],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("published P2 freeze revision is not an ancestor")
    observed_blobs = {path: _git_blob(path) for path in EXPECTED_BLOBS}
    if observed_blobs != EXPECTED_BLOBS:
        raise RuntimeError("one or more frozen P2 dependencies changed")

    p1 = json.loads((ROOT / P1_RESULT).read_text(encoding="utf-8"))
    candidate = p1.get("candidate", {})
    if p1.get("decision") != "numerically-stable-source-pass":
        raise RuntimeError("P2 requires the reviewed P1 L3 pass")
    if candidate.get("candidate_id") != CANDIDATE_ID:
        raise RuntimeError("P1 candidate identifier does not match P2")
    if candidate.get("radius_decimal") != RADIUS_DECIMAL:
        raise RuntimeError("P1 radius decimal does not match P2")
    if candidate.get("theta_decimal") != THETA_DECIMAL:
        raise RuntimeError("P1 theta decimal does not match P2")

    script_path = Path(__file__).resolve().relative_to(ROOT).as_posix()
    module_path = "src/emergenz_knoten/loop_center_response.py"
    return {
        "clean_pre_run_status": status,
        "revision": revision,
        "freeze_revision": FREEZE_REVISION,
        "freeze_is_ancestor": True,
        "expected_blobs": EXPECTED_BLOBS,
        "observed_blobs": observed_blobs,
        "implementation_blobs": {
            script_path: _git_blob(script_path),
            module_path: _git_blob(module_path),
        },
        "p1_decision": p1["decision"],
    }


def _weighted_squared(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.sum(weights[:, None] * values * values))


def _safe_ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0.0 or not math.isfinite(denominator):
        return math.inf
    return float(numerator / denominator)


def _tail_slope(distances: list[float], maximum: float) -> float:
    if maximum <= 0.0 or len(distances) < TAIL_UPDATES:
        return math.inf
    values = np.asarray(distances[-TAIL_UPDATES:], dtype=float)
    x = np.arange(values.size, dtype=float)
    x -= np.mean(x)
    slope = float(np.dot(x, values - np.mean(values)) / np.dot(x, x))
    return abs(slope) / maximum / CANDIDATE.alpha


def _force_at_step(
    waveform: np.ndarray,
    *,
    step_index: int,
    amplitude: float,
    direction: np.ndarray,
) -> np.ndarray:
    profile = float(waveform[step_index]) if step_index < waveform.size else 0.0
    return amplitude * CANDIDATE.radius * profile * direction


def _run_mirrored_branch(
    *,
    history: np.ndarray,
    jacobian: Any,
    weights: np.ndarray,
    waveform_name: str,
    waveform: np.ndarray,
    direction_name: str,
    direction: np.ndarray,
    amplitude: float,
    baseline_normalized_odd: np.ndarray | None = None,
    capture_normalized_odd: bool = False,
) -> tuple[dict[str, Any], np.ndarray | None]:
    plus = history.copy()
    minus = history.copy()
    off = history.copy()
    tangent = np.zeros_like(history)

    previous_center_odd = np.zeros(2)
    previous_center_tangent = np.zeros(2)
    sums = {
        "odd_state": 0.0,
        "tangent_state": 0.0,
        "state_error": 0.0,
        "even_state": 0.0,
        "plus_remainder": 0.0,
        "center_velocity_odd": 0.0,
        "center_velocity_tangent": 0.0,
        "center_velocity_error": 0.0,
        "collapse_difference": 0.0,
        "collapse_reference": 0.0,
    }
    normalized_trace = (
        np.empty((TOTAL_UPDATES, CANDIDATE.horizon, 2), dtype=np.float64)
        if capture_normalized_odd
        else None
    )
    plus_distances: list[float] = []
    minus_distances: list[float] = []
    thinned_trace: list[dict[str, Any]] = []
    complete = True

    for step_index in range(TOTAL_UPDATES):
        force = _force_at_step(
            waveform,
            step_index=step_index,
            amplitude=amplitude,
            direction=direction,
        )
        plus = co_rotating_fifo_forced_step(
            plus,
            force_lab=force,
            step_index=step_index,
            theta=CANDIDATE.theta,
            **CANDIDATE.step_parameters(),
        )
        minus = co_rotating_fifo_forced_step(
            minus,
            force_lab=-force,
            step_index=step_index,
            theta=CANDIDATE.theta,
            **CANDIDATE.step_parameters(),
        )
        off = co_rotating_fifo_step(
            off,
            theta=CANDIDATE.theta,
            **CANDIDATE.step_parameters(),
        )
        tangent = tangent_fifo_forced_step(
            tangent,
            jacobian=jacobian,
            force_lab=force,
            step_index=step_index,
            theta=CANDIDATE.theta,
            alpha=CANDIDATE.alpha,
        )

        if not all(np.isfinite(value).all() for value in (plus, minus, off, tangent)):
            complete = False
            break

        plus_delta = plus - off
        minus_delta = minus - off
        odd = 0.5 * (plus_delta - minus_delta)
        even = 0.5 * (plus_delta + minus_delta)
        state_error = odd - tangent
        plus_remainder = plus_delta - tangent

        sums["odd_state"] += _weighted_squared(odd, weights)
        sums["tangent_state"] += _weighted_squared(tangent, weights)
        sums["state_error"] += _weighted_squared(state_error, weights)
        sums["even_state"] += _weighted_squared(even, weights)
        sums["plus_remainder"] += _weighted_squared(plus_remainder, weights)

        normalized = odd / amplitude
        if normalized_trace is not None:
            normalized_trace[step_index] = normalized
        if baseline_normalized_odd is not None:
            baseline = baseline_normalized_odd[step_index]
            sums["collapse_difference"] += _weighted_squared(
                normalized - baseline,
                weights,
            )
            sums["collapse_reference"] += _weighted_squared(baseline, weights)

        completed_step = step_index + 1
        center_odd = laboratory_center_displacement(
            odd,
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
            theta=CANDIDATE.theta,
            step=completed_step,
        )
        center_tangent = laboratory_center_displacement(
            tangent,
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
            theta=CANDIDATE.theta,
            step=completed_step,
        )
        velocity_odd = (center_odd - previous_center_odd) / CANDIDATE.alpha
        velocity_tangent = (
            center_tangent - previous_center_tangent
        ) / CANDIDATE.alpha
        velocity_error = velocity_odd - velocity_tangent
        previous_center_odd = center_odd
        previous_center_tangent = center_tangent
        sums["center_velocity_odd"] += float(np.dot(velocity_odd, velocity_odd))
        sums["center_velocity_tangent"] += float(
            np.dot(velocity_tangent, velocity_tangent)
        )
        sums["center_velocity_error"] += float(
            np.dot(velocity_error, velocity_error)
        )

        plus_distance, _ = rotation_translation_quotient_distance(
            plus,
            off,
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
        )
        minus_distance, _ = rotation_translation_quotient_distance(
            minus,
            off,
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
        )
        plus_distances.append(plus_distance)
        minus_distances.append(minus_distance)

        if completed_step % TRACE_EVERY == 0 or completed_step in (
            1,
            PROBE_UPDATES,
            TOTAL_UPDATES,
        ):
            thinned_trace.append(
                {
                    "step": completed_step,
                    "driven": completed_step <= PROBE_UPDATES,
                    "center_velocity_odd": velocity_odd.tolist(),
                    "center_velocity_tangent": velocity_tangent.tolist(),
                    "plus_d0": plus_distance,
                    "minus_d0": minus_distance,
                }
            )

    completed_updates = len(plus_distances)
    count = max(1, completed_updates)
    tangent_state_rms = math.sqrt(sums["tangent_state"] / count)
    odd_state_rms = math.sqrt(sums["odd_state"] / count)
    absolute_remainder_rms = math.sqrt(sums["plus_remainder"] / count)
    tangent_center_velocity_rms = math.sqrt(
        sums["center_velocity_tangent"] / count
    )
    maximum_plus = max(plus_distances, default=math.inf)
    maximum_minus = max(minus_distances, default=math.inf)
    maximum_d0 = max(maximum_plus, maximum_minus)
    final_plus = plus_distances[-1] if plus_distances else math.inf
    final_minus = minus_distances[-1] if minus_distances else math.inf
    final_ratio = max(
        _safe_ratio(final_plus, maximum_plus),
        _safe_ratio(final_minus, maximum_minus),
    )
    tail_slope = max(
        _tail_slope(plus_distances, maximum_plus),
        _tail_slope(minus_distances, maximum_minus),
    )
    collapse = (
        math.sqrt(
            _safe_ratio(
                sums["collapse_difference"],
                sums["collapse_reference"],
            )
        )
        if baseline_normalized_odd is not None
        else 0.0
    )

    metrics = {
        "waveform": waveform_name,
        "direction": direction_name,
        "amplitude_fraction": amplitude,
        "completed_updates": completed_updates,
        "complete_and_finite": bool(complete and completed_updates == TOTAL_UPDATES),
        "state_tangent_relative_rms": math.sqrt(
            _safe_ratio(sums["state_error"], sums["tangent_state"])
        ),
        "center_velocity_tangent_relative_rms": math.sqrt(
            _safe_ratio(
                sums["center_velocity_error"],
                sums["center_velocity_tangent"],
            )
        ),
        "even_state_relative_rms": math.sqrt(
            _safe_ratio(sums["even_state"], sums["odd_state"])
        ),
        "single_sign_remainder_relative_rms": _safe_ratio(
            absolute_remainder_rms,
            tangent_state_rms,
        ),
        "normalized_odd_collapse_relative_rms": collapse,
        "odd_state_rms": odd_state_rms,
        "tangent_state_rms": tangent_state_rms,
        "absolute_single_sign_remainder_rms": absolute_remainder_rms,
        "tangent_center_velocity_rms": tangent_center_velocity_rms,
        "signal_floor": THRESHOLDS.signal_fraction * amplitude * CANDIDATE.radius,
        "signal_above_floor": bool(
            tangent_center_velocity_rms
            >= THRESHOLDS.signal_fraction * amplitude * CANDIDATE.radius
        ),
        "maximum_d0": maximum_d0,
        "maximum_d0_fraction": maximum_d0 / CANDIDATE.radius,
        "final_d0_ratio": final_ratio,
        "tail_slope_fraction_per_memory_time": tail_slope,
        "trace": thinned_trace,
    }
    return metrics, normalized_trace


def _fixed_point_control(history: np.ndarray) -> dict[str, Any]:
    advanced = co_rotating_fifo_step(
        history,
        theta=CANDIDATE.theta,
        **CANDIDATE.step_parameters(),
    )
    error = float(np.max(np.abs(advanced - history)))
    return {
        "maximum_component_error": error,
        "threshold": THRESHOLDS.fixed_point_component,
        "pass": bool(error <= THRESHOLDS.fixed_point_component),
    }


def _jacobian_control() -> dict[str, Any]:
    horizon = 17
    theta = 0.13
    history = circular_history(radius=1.1, theta=theta, horizon=horizon)
    parameters = {
        "alpha": 0.07,
        "memory_mass": 1.2,
        "eta": 0.18,
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 4.5,
    }
    jacobian = co_rotating_fifo_jacobian(history, theta=theta, **parameters)
    direction = np.random.default_rng(20260825).normal(size=history.shape)
    direction /= np.linalg.norm(direction)
    force = np.asarray([0.17, -0.31])
    finite_step = 2.0e-6
    upper = co_rotating_fifo_forced_step(
        history + finite_step * direction,
        force_lab=finite_step * force,
        step_index=9,
        theta=theta,
        **parameters,
    )
    lower = co_rotating_fifo_forced_step(
        history - finite_step * direction,
        force_lab=-finite_step * force,
        step_index=9,
        theta=theta,
        **parameters,
    )
    finite_difference = (upper - lower) / (2.0 * finite_step)
    analytic = tangent_fifo_forced_step(
        direction,
        jacobian=jacobian,
        force_lab=force,
        step_index=9,
        theta=theta,
        alpha=parameters["alpha"],
    )
    relative = float(
        np.linalg.norm(analytic - finite_difference) / np.linalg.norm(analytic)
    )
    return {
        "horizon": horizon,
        "relative_error": relative,
        "threshold": THRESHOLDS.jacobian_relative,
        "pass": bool(relative <= THRESHOLDS.jacobian_relative),
    }


def _center_recurrence_control(
    history: np.ndarray,
    waveform: np.ndarray,
) -> dict[str, Any]:
    state = history.copy()
    center = memory_center(
        state,
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    maximum = 0.0
    direction = DIRECTIONS["radial"]
    for step_index in range(PROBE_UPDATES):
        force = _force_at_step(
            waveform,
            step_index=step_index,
            amplitude=HOLDOUT_AMPLITUDE,
            direction=direction,
        )
        retiring = state[-1].copy()
        state = native_fifo_forced_step(
            state,
            force=force,
            **CANDIDATE.step_parameters(),
        )
        recurrent = finite_h_center_recurrence(
            center,
            new_visible=state[0],
            retiring_visible=retiring,
            alpha=CANDIDATE.alpha,
            horizon=CANDIDATE.horizon,
        )
        direct = memory_center(
            state,
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
        )
        maximum = max(maximum, float(np.linalg.norm(recurrent - direct)))
        center = direct
    threshold = THRESHOLDS.center_recurrence_fraction * CANDIDATE.radius
    return {
        "updates": PROBE_UPDATES,
        "maximum_absolute_error": maximum,
        "maximum_fraction_of_radius": maximum / CANDIDATE.radius,
        "threshold": threshold,
        "pass": bool(maximum <= threshold),
    }


def _phase_covariance_control(
    history: np.ndarray,
    waveform: np.ndarray,
) -> dict[str, Any]:
    step_index = 101
    force = _force_at_step(
        waveform,
        step_index=step_index,
        amplitude=HOLDOUT_AMPLITUDE,
        direction=DIRECTIONS["radial"],
    )
    base = native_fifo_forced_step(
        history,
        force=force,
        **CANDIDATE.step_parameters(),
    )
    base_center = memory_center(
        base,
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    rows = []
    maximum = 0.0
    for phase in PHASES:
        rotation = rotation_matrix(phase)
        transformed = native_fifo_forced_step(
            history @ rotation.T,
            force=rotation @ force,
            **CANDIDATE.step_parameters(),
        )
        expected = base @ rotation.T
        state_error = float(np.max(np.abs(transformed - expected)))
        transformed_center = memory_center(
            transformed,
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
        )
        center_error = float(np.linalg.norm(transformed_center - rotation @ base_center))
        normalized = max(state_error, center_error) / CANDIDATE.radius
        maximum = max(maximum, normalized)
        rows.append(
            {
                "phase": phase,
                "state_maximum_error": state_error,
                "center_error": center_error,
                "normalized_maximum_error": normalized,
            }
        )
    return {
        "rows": rows,
        "maximum_normalized_error": maximum,
        "threshold": THRESHOLDS.phase_covariance_fraction,
        "pass": bool(maximum <= THRESHOLDS.phase_covariance_fraction),
    }


def _scalar_origin_comparator() -> dict[str, Any]:
    q = 1.0 - CANDIDATE.alpha
    q_h = q**CANDIDATE.horizon
    memory_mass_h = CANDIDATE.memory_mass * (1.0 - q_h)
    curvature = (
        CANDIDATE.amplitude_att / CANDIDATE.sigma_att**2
        - CANDIDATE.amplitude_rep / CANDIDATE.sigma_rep**2
    )
    gain = CANDIDATE.eta * memory_mass_h * curvature
    pole = q * (1.0 - gain)
    eligible = bool(0.0 < gain < 1.0 and abs(pole) < 1.0)
    return {
        "q_h": q_h,
        "finite_memory_mass": memory_mass_h,
        "origin_curvature": curvature,
        "g_h": gain,
        "untruncated_scalar_pole": pole,
        "eligibility_conditions": "0 < g_H < 1 and abs(q*(1-g_H)) < 1",
        "eligible": eligible,
        "decision": "scalar-origin-eligible" if eligible else "scalar-origin-ineligible",
        "refit_allowed": False,
    }


def _primary_row_pass(row: dict[str, Any]) -> bool:
    return bool(
        row["complete_and_finite"]
        and row["state_tangent_relative_rms"] <= THRESHOLDS.primary_tangent_relative
        and row["center_velocity_tangent_relative_rms"]
        <= THRESHOLDS.primary_tangent_relative
        and row["even_state_relative_rms"] <= THRESHOLDS.primary_even_relative
        and row["single_sign_remainder_relative_rms"]
        <= THRESHOLDS.primary_remainder_relative
        and row["normalized_odd_collapse_relative_rms"]
        <= THRESHOLDS.primary_collapse_relative
        and row["signal_above_floor"]
        and row["maximum_d0_fraction"] <= THRESHOLDS.loop_maximum_fraction
        and row["final_d0_ratio"] <= THRESHOLDS.loop_final_ratio
        and row["tail_slope_fraction_per_memory_time"]
        <= THRESHOLDS.loop_tail_slope_per_memory_time
    )


def _holdout_row_pass(row: dict[str, Any]) -> bool:
    return bool(
        row["complete_and_finite"]
        and row["state_tangent_relative_rms"] <= THRESHOLDS.holdout_tangent_relative
        and row["center_velocity_tangent_relative_rms"]
        <= THRESHOLDS.holdout_tangent_relative
        and row["even_state_relative_rms"] <= THRESHOLDS.holdout_even_relative
        and row["signal_above_floor"]
        and row["maximum_d0_fraction"] <= THRESHOLDS.loop_maximum_fraction
        and row["final_d0_ratio"] <= THRESHOLDS.loop_final_ratio
        and row["tail_slope_fraction_per_memory_time"]
        <= THRESHOLDS.loop_tail_slope_per_memory_time
    )


def _evaluate_decision(
    *,
    controls: dict[str, Any],
    primary: list[dict[str, Any]],
    slopes: list[dict[str, Any]],
    holdout: list[dict[str, Any]],
) -> tuple[str, dict[str, bool]]:
    controls_pass = all(control["pass"] for control in controls.values())
    complete = all(row["complete_and_finite"] for row in (*primary, *holdout))
    signals = all(row["signal_above_floor"] for row in (*primary, *holdout))
    primary_pass = all(_primary_row_pass(row) for row in primary)
    slope_pass = all(row["pass"] for row in slopes)
    holdout_pass = all(_holdout_row_pass(row) for row in holdout)
    gates = {
        "controls": controls_pass,
        "complete_traces": complete,
        "signals_above_floor": signals,
        "primary_response": primary_pass,
        "quadratic_remainder_slopes": slope_pass,
        "waveform_holdout": holdout_pass,
    }
    if not controls_pass or not complete or not signals:
        decision = "loop-center-matrix-local-inconclusive"
    elif all(gates.values()):
        decision = "loop-center-matrix-local-pass"
    else:
        decision = "loop-center-matrix-local-fail"
    return decision, gates


def run_gate() -> dict[str, Any]:
    """Run all frozen P2 controls and target branches."""

    started = time.perf_counter()
    provenance = _verify_provenance()
    history = circular_history(
        radius=CANDIDATE.radius,
        theta=CANDIDATE.theta,
        horizon=CANDIDATE.horizon,
    )
    weights = normalized_memory_weights(
        alpha=CANDIDATE.alpha,
        horizon=CANDIDATE.horizon,
        memory_mass=CANDIDATE.memory_mass,
    )
    waveforms = registered_zero_sum_waveforms(PROBE_UPDATES)
    waveform_sums = {name: float(np.sum(values)) for name, values in waveforms.items()}
    if any(abs(value) > 1.0e-13 for value in waveform_sums.values()):
        raise RuntimeError("registered P2 waveform is not zero sum")

    controls = {
        "fixed_point": _fixed_point_control(history),
        "unrelated_joint_jacobian": _jacobian_control(),
        "center_recurrence": _center_recurrence_control(
            history,
            waveforms["sine_cycle"],
        ),
        "phase_covariance": _phase_covariance_control(
            history,
            waveforms["sine_cycle"],
        ),
    }

    jacobian = co_rotating_fifo_jacobian(
        history,
        theta=CANDIDATE.theta,
        **CANDIDATE.step_parameters(),
    )
    primary: list[dict[str, Any]] = []
    slopes: list[dict[str, Any]] = []
    for direction_name, direction in DIRECTIONS.items():
        baseline: np.ndarray | None = None
        direction_rows: list[dict[str, Any]] = []
        for index, amplitude in enumerate(PRIMARY_AMPLITUDES):
            row, captured = _run_mirrored_branch(
                history=history,
                jacobian=jacobian,
                weights=weights,
                waveform_name="sine_cycle",
                waveform=waveforms["sine_cycle"],
                direction_name=direction_name,
                direction=direction,
                amplitude=amplitude,
                baseline_normalized_odd=baseline,
                capture_normalized_odd=index == 0,
            )
            if captured is not None:
                baseline = captured
            row["pass"] = _primary_row_pass(row)
            direction_rows.append(row)
            primary.append(row)
        lower = direction_rows[-2]
        upper = direction_rows[-1]
        slope = math.log(
            upper["absolute_single_sign_remainder_rms"]
            / lower["absolute_single_sign_remainder_rms"]
        ) / math.log(
            upper["amplitude_fraction"] / lower["amplitude_fraction"]
        )
        slopes.append(
            {
                "direction": direction_name,
                "lower_amplitude": lower["amplitude_fraction"],
                "upper_amplitude": upper["amplitude_fraction"],
                "secant_slope": slope,
                "minimum": THRESHOLDS.remainder_slope_minimum,
                "maximum": THRESHOLDS.remainder_slope_maximum,
                "pass": bool(
                    THRESHOLDS.remainder_slope_minimum
                    <= slope
                    <= THRESHOLDS.remainder_slope_maximum
                ),
            }
        )
        del baseline

    holdout: list[dict[str, Any]] = []
    for direction_name, direction in DIRECTIONS.items():
        row, _ = _run_mirrored_branch(
            history=history,
            jacobian=jacobian,
            weights=weights,
            waveform_name="hann_doublet",
            waveform=waveforms["hann_doublet"],
            direction_name=direction_name,
            direction=direction,
            amplitude=HOLDOUT_AMPLITUDE,
        )
        row["pass"] = _holdout_row_pass(row)
        holdout.append(row)

    off = history.copy()
    for _ in range(TOTAL_UPDATES):
        off = co_rotating_fifo_step(
            off,
            theta=CANDIDATE.theta,
            **CANDIDATE.step_parameters(),
        )
    off_distance, _ = rotation_translation_quotient_distance(
        off,
        history,
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    controls["probe_off"] = {
        "final_d0": off_distance,
        "final_fraction_of_radius": off_distance / CANDIDATE.radius,
        "threshold": THRESHOLDS.probe_off_fraction * CANDIDATE.radius,
        "pass": bool(
            off_distance <= THRESHOLDS.probe_off_fraction * CANDIDATE.radius
        ),
    }

    decision, gates = _evaluate_decision(
        controls=controls,
        primary=primary,
        slopes=slopes,
        holdout=holdout,
    )
    tangent_rms = {
        row["direction"]: row["tangent_center_velocity_rms"]
        for row in primary
        if row["amplitude_fraction"] == HOLDOUT_AMPLITUDE
    }
    anisotropy = max(tangent_rms.values()) / min(tangent_rms.values())
    return {
        "schema_version": 1,
        "gate": "P2 local Loop--Center response at L3",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "elapsed_seconds": time.perf_counter() - started,
        "candidate_id": CANDIDATE_ID,
        "candidate": {
            **asdict(CANDIDATE),
            "radius_decimal": RADIUS_DECIMAL,
            "theta_decimal": THETA_DECIMAL,
            "deposition_kernel": "delta",
            "epsilon": 0.0,
        },
        "provenance": provenance,
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": importlib.metadata.version("numpy"),
            "scipy": importlib.metadata.version("scipy"),
        },
        "protocol": {
            "path": PROTOCOL.as_posix(),
            "freeze_revision": FREEZE_REVISION,
            "thresholds": asdict(THRESHOLDS),
            "primary_amplitudes": list(PRIMARY_AMPLITUDES),
            "holdout_amplitude": HOLDOUT_AMPLITUDE,
            "probe_updates": PROBE_UPDATES,
            "recovery_updates": RECOVERY_UPDATES,
            "tail_updates": TAIL_UPDATES,
            "trace_every": TRACE_EVERY,
            "directions": list(DIRECTIONS),
            "phases": list(PHASES),
            "waveform_sums": waveform_sums,
            "no_response_fit": True,
        },
        "scalar_origin_comparator": _scalar_origin_comparator(),
        "controls": controls,
        "primary": primary,
        "quadratic_remainder_slopes": slopes,
        "waveform_holdout": holdout,
        "diagnostics": {
            "center_velocity_tangent_rms_at_3e-5": tangent_rms,
            "radial_tangential_anisotropy_ratio": anisotropy,
        },
        "gates": gates,
        "decision": decision,
        "claim_boundary": {
            "established_if_pass": (
                "local phase-covariant matrix-valued Loop--Center response of "
                "one prepared L3 relative equilibrium in the frozen amplitude "
                "and waveform panel"
            ),
            "not_established": (
                "scalar-origin center merger, transfer of B-star filter mass, "
                "formation, finite basin, microscopic center-conjugate actuator, "
                "physical work or mass, internal S1, or interactions"
            ),
        },
    }


def _format(value: float) -> str:
    return f"{value:.6g}"


def render_report(payload: dict[str, Any], *, summary_sha256: str) -> str:
    """Render the human-readable P2 report from the frozen JSON payload."""

    scalar = payload["scalar_origin_comparator"]
    controls = payload["controls"]
    primary = payload["primary"]
    holdout = payload["waveform_holdout"]
    slopes = payload["quadratic_remainder_slopes"]
    lines = [
        "# P2 local Loop--Center response at L3",
        "",
        f"Date: {payload['generated_at_utc'][:10]}.",
        "",
        f"Decision: **`{payload['decision']}`**.",
        "",
        "The full nonlinear finite-memory loop was compared with the frozen",
        "full-FIFO tangent recurrence. No response pole, gain, damping, phase",
        "or normalization was fitted.",
        "",
        "## Analytic scalar comparator",
        "",
        "| quantity | value |",
        "| --- | ---: |",
        f"| origin curvature | {_format(scalar['origin_curvature'])} |",
        f"| finite-H $g_H$ | {_format(scalar['g_h'])} |",
        f"| scalar pole $q(1-g_H)$ | {_format(scalar['untruncated_scalar_pole'])} |",
        f"| decision | `{scalar['decision']}` |",
        "",
        "This analytic result is separate from the matrix-local decision and",
        "was not repaired by fitting an effective scalar gain.",
        "",
        "## Controls",
        "",
        "| control | observed | threshold | pass |",
        "| --- | ---: | ---: | :---: |",
        (
            "| fixed point | "
            f"{_format(controls['fixed_point']['maximum_component_error'])} | "
            f"{_format(controls['fixed_point']['threshold'])} | "
            f"{controls['fixed_point']['pass']} |"
        ),
        (
            "| unrelated joint Jacobian | "
            f"{_format(controls['unrelated_joint_jacobian']['relative_error'])} | "
            f"{_format(controls['unrelated_joint_jacobian']['threshold'])} | "
            f"{controls['unrelated_joint_jacobian']['pass']} |"
        ),
        (
            "| center recurrence | "
            f"{_format(controls['center_recurrence']['maximum_absolute_error'])} | "
            f"{_format(controls['center_recurrence']['threshold'])} | "
            f"{controls['center_recurrence']['pass']} |"
        ),
        (
            "| rotation covariance | "
            f"{_format(controls['phase_covariance']['maximum_normalized_error'])} | "
            f"{_format(controls['phase_covariance']['threshold'])} | "
            f"{controls['phase_covariance']['pass']} |"
        ),
        (
            "| probe off final D0 | "
            f"{_format(controls['probe_off']['final_d0'])} | "
            f"{_format(controls['probe_off']['threshold'])} | "
            f"{controls['probe_off']['pass']} |"
        ),
        "",
        "## Primary amplitude ladder",
        "",
        "| direction | amplitude | state tangent error | center-velocity error | even leakage | first-order remainder | amplitude collapse | max D0/R | final/peak | tail slope | pass |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |",
    ]
    for row in primary:
        lines.append(
            f"| {row['direction']} | {_format(row['amplitude_fraction'])} | "
            f"{_format(row['state_tangent_relative_rms'])} | "
            f"{_format(row['center_velocity_tangent_relative_rms'])} | "
            f"{_format(row['even_state_relative_rms'])} | "
            f"{_format(row['single_sign_remainder_relative_rms'])} | "
            f"{_format(row['normalized_odd_collapse_relative_rms'])} | "
            f"{_format(row['maximum_d0_fraction'])} | "
            f"{_format(row['final_d0_ratio'])} | "
            f"{_format(row['tail_slope_fraction_per_memory_time'])} | "
            f"{row['pass']} |"
        )
    lines.extend(
        [
            "",
            "## Quadratic remainder and waveform holdout",
            "",
            "| panel | direction | diagnostic | value | pass |",
            "| --- | --- | --- | ---: | :---: |",
        ]
    )
    for row in slopes:
        lines.append(
            f"| primary | {row['direction']} | remainder secant slope | "
            f"{_format(row['secant_slope'])} | {row['pass']} |"
        )
    for row in holdout:
        lines.append(
            f"| holdout | {row['direction']} | state / center tangent error | "
            f"{_format(row['state_tangent_relative_rms'])} / "
            f"{_format(row['center_velocity_tangent_relative_rms'])} | "
            f"{row['pass']} |"
        )
    lines.extend(
        [
            "",
            "## Decision and limits",
            "",
            f"Gate components: `{json.dumps(payload['gates'], sort_keys=True)}`.",
            "",
            "A pass supports only the local matrix-valued response of this one",
            "prepared L3 loop. The exact center readout and covariance controls",
            "are structural. The finite amplitude ladder, quadratic remainder,",
            "waveform holdout and D0 recovery are the discriminating numerical",
            "content.",
            "",
            "The result does not transfer the former scalar B-star filter mass",
            "to L3 and does not identify a microscopic center-conjugate port.",
            "Formation, a finite basin, physical work or mass, internal topology",
            "and interactions remain outside P2.",
            "",
            "## Provenance",
            "",
            f"- freeze revision: `{payload['provenance']['freeze_revision']}`;",
            f"- execution revision: `{payload['provenance']['revision']}`;",
            f"- JSON SHA-256: `{summary_sha256}`;",
            f"- elapsed seconds: `{_format(payload['elapsed_seconds'])}`;",
            f"- Python / NumPy / SciPy: `{payload['runtime']['python']}` / "
            f"`{payload['runtime']['numpy']}` / `{payload['runtime']['scipy']}`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    arguments = parser.parse_args()

    payload = run_gate()
    summary = ROOT / arguments.summary
    report = ROOT / arguments.report
    summary.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report.write_text(
        render_report(payload, summary_sha256=_sha256(summary)),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "decision": payload["decision"],
                "report": report.relative_to(ROOT).as_posix(),
                "summary": summary.relative_to(ROOT).as_posix(),
                "elapsed_seconds": payload["elapsed_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
