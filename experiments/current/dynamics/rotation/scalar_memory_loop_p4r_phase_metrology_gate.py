"""Execute the frozen P4-R-phi metrology and phase-response gate."""

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

import mpmath as mp
import numpy as np

from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4_source_write_gate as p4,
)
from emergenz_knoten.orbit_center_actuator import (
    OrbitCenterReadout,
    SourceWriteRoundingMetrology,
    SourceWriteStep,
    candidate_orbit_center_readout,
    complex_to_vector,
    real_inner,
    reciprocal_source_write_step,
    source_write_rounding_metrology,
)
from emergenz_knoten.rotating_wave_formation import (
    FormationThresholds,
    phase_increment_metrics,
    target_history,
)
from emergenz_knoten.rotating_wave_stability import (
    native_fifo_step,
    rotation_matrix,
)


ROOT = p4.ROOT
CANDIDATE = p4.CANDIDATE
CANDIDATE_ID = p4.CANDIDATE_ID
RADIUS_DECIMAL = p4.RADIUS_DECIMAL
THETA_DECIMAL = p4.THETA_DECIMAL
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_loop_p4r_phase_metrology_protocol_2026-08-26.md"
)
REFEREE_CHARTER = Path(
    "reports/project/meta/preregistration/"
    "p4_publication_source_referee_audit_charter_2026-08-26.md"
)
DESIGN_AUDIT = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_loop_p4r_phase_metrology_design_audit_2026-08-26.md"
)
P4_REVIEW = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_loop_p4_source_write_review_2026-08-26.md"
)
P4_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4_source_write_2026-08-26.json"
)
P4_PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_loop_p4_source_write_protocol_2026-08-26.md"
)
HISTORICAL_P4_RUNNER = Path(
    "experiments/current/dynamics/rotation/"
    "scalar_memory_loop_p4_source_write_gate.py"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4r_phase_metrology_2026-08-26.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4r_phase_metrology_2026-08-26.json"
)

PROTOCOL_FREEZE_REVISION = "cb863d4a88c1072637116a0296ab9fc20356a675"
TARGET_BASE_REVISION = "071c9d33c8611d0a1ef1cb3da620acb7dcdb5f7d"
EXPECTED_P4_SHA256 = (
    "ea0651e206451e5f87ec08ab3f66ec68df2c04bee2d1b9d67219736058a275cc"
)
EXPECTED_HEAD_BLOBS = {
    PROTOCOL.as_posix(): "b81fa535c1921c2f11f83e5585bf38b05e0a08d5",
    REFEREE_CHARTER.as_posix(): "2bc9bba4c2c5f9184201987f2f97faac2c91aec5",
    DESIGN_AUDIT.as_posix(): "45920014d5b98087ecadca832b216818b4d6d18a",
    P4_REVIEW.as_posix(): "4412f6050896a33a275ad10e1d1c0e524bcfba3f",
    P4_RESULT.as_posix(): "41ddfb5ec2d4c907607995523775072ad12544f7",
    P4_PROTOCOL.as_posix(): "fb1f41c66fad0e6df9c7dc8a226517940deab939",
    HISTORICAL_P4_RUNNER.as_posix(): (
        "c44b186bfb56567b300903e846540e5a21231ff0"
    ),
    "src/emergenz_knoten/rotating_wave_stability.py": (
        "9defb5a6876371202e1ba57cea030c997b9c6edd"
    ),
    "src/emergenz_knoten/rotating_wave_formation.py": (
        "38f16f11a790a64470bab3a34505825cf815e7f0"
    ),
    "src/emergenz_knoten/rotating_wave_stability_gate.py": (
        "630beb9952abefea823d91388dcbb2de8f1a2927"
    ),
    "src/emergenz_knoten/loop_center_response.py": (
        "a8b8a002be3a3e4d75f8bd6b00989f1dafe61e0b"
    ),
}
EXPECTED_PREIMPLEMENTATION_BLOBS = {
    "src/emergenz_knoten/orbit_center_actuator.py": (
        "d8de95f4f46adc43c37d6d1affdc73be14f70ec3"
    ),
}
IMPLEMENTATION_PATHS = (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_loop_p4r_phase_metrology_gate.py",
    "src/emergenz_knoten/orbit_center_actuator.py",
    "tests/test_orbit_center_actuator.py",
    "tests/test_rotating_wave_p4r_phase_metrology.py",
)


@dataclass(frozen=True)
class P4RThresholds:
    """Frozen P4-R-phi panel and decision thresholds."""

    active_updates: int = 4_000
    sample_every: int = 10
    late_start: int = 3_600
    phase_start: int = 3_000
    coupling_strength: float = 0.25
    offset_fraction: float = 1.5e-3
    maximum_d0_fraction: float = 0.01
    late_d0_fraction: float = 0.002
    opposite_d0_fraction: float = 0.5
    final_separation_fraction: float = 0.10
    projection_minimum: float = 0.20
    projection_maximum: float = 0.80
    energy_ratio_maximum: float = 0.01
    phase_mean_error_fraction: float = 0.01
    phase_rms_error_fraction: float = 0.05
    step_ledger_relative: float = 5.0e-11
    cumulative_ledger_relative: float = 5.0e-9
    force_relative: float = 5.0e-12
    local_displacement_relative: float = 5.0e-12
    actuator_displacement_relative: float = 5.0e-12
    even_response_relative: float = 0.02
    signal_fraction: float = 0.25
    coefficient_tolerance: float = 5.0e-13
    center_tolerance_fraction: float = 1.0e-12
    channel_off_d0_fraction: float = 1.0e-10
    covariance_fraction: float = 1.0e-11
    scalar_null_maximum: float = 0.05
    chiral_minimum: float = 0.10
    sign_support_minimum: int = 6
    reference_dps: int = 80
    reference_steps: tuple[int, ...] = (1, 2_000, 4_000)


THRESHOLDS = P4RThresholds()
PHASES = tuple((2 * index + 1) * math.pi / 8.0 for index in range(8))


def _git_output(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def _git_blob(path: str, *, revision: str = "HEAD") -> str:
    return _git_output(["rev-parse", f"{revision}:{path}"])


def _canonical_lf_sha256(path: Path) -> str:
    content = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(content).hexdigest()


def _verify_provenance() -> dict[str, Any]:
    status = _git_output(["status", "--short"])
    if status:
        raise RuntimeError("P4-R target gate requires a clean prospective revision")
    revision = _git_output(["rev-parse", "HEAD"])
    for ancestor in (PROTOCOL_FREEZE_REVISION, TARGET_BASE_REVISION):
        check = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, revision],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if check.returncode != 0:
            raise RuntimeError(f"required freeze revision is not an ancestor: {ancestor}")
    observed = {path: _git_blob(path) for path in EXPECTED_HEAD_BLOBS}
    if observed != EXPECTED_HEAD_BLOBS:
        raise RuntimeError("one or more frozen P4-R dependencies changed")
    preimplementation = {
        path: _git_blob(path, revision=PROTOCOL_FREEZE_REVISION)
        for path in EXPECTED_PREIMPLEMENTATION_BLOBS
    }
    if preimplementation != EXPECTED_PREIMPLEMENTATION_BLOBS:
        raise RuntimeError("preimplementation source blob does not match protocol")
    if _canonical_lf_sha256(ROOT / P4_RESULT) != EXPECTED_P4_SHA256:
        raise RuntimeError("authoritative P4 JSON hash changed")
    p4_result = json.loads((ROOT / P4_RESULT).read_text(encoding="utf-8"))
    if p4_result.get("decision") != "p4-source-write-architecture-fail":
        raise RuntimeError("P4-R requires the immutable historical P4 fail")
    upstream = _git_output(
        ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"]
    )
    ahead_behind = _git_output(
        ["rev-list", "--left-right", "--count", f"HEAD...{upstream}"]
    ).split()
    if ahead_behind != ["0", "0"]:
        raise RuntimeError("P4-R target gate requires a fully pushed revision")
    return {
        "clean_pre_run_status": status,
        "revision": revision,
        "protocol_freeze_revision": PROTOCOL_FREEZE_REVISION,
        "target_base_revision": TARGET_BASE_REVISION,
        "freeze_revisions_are_ancestors": True,
        "expected_head_blobs": EXPECTED_HEAD_BLOBS,
        "observed_head_blobs": observed,
        "expected_preimplementation_blobs": EXPECTED_PREIMPLEMENTATION_BLOBS,
        "observed_preimplementation_blobs": preimplementation,
        "implementation_blobs": {
            path: _git_blob(path) for path in IMPLEMENTATION_PATHS
        },
        "upstream": upstream,
        "upstream_synchronized": True,
        "origin": _git_output(["remote", "get-url", "origin"]),
        "p4_decision": p4_result["decision"],
        "p4_sha256": EXPECTED_P4_SHA256,
    }


def _phase_history(*, chirality: int, phase_index: int) -> np.ndarray:
    base = target_history(CANDIDATE, chirality=chirality)
    return base @ rotation_matrix(PHASES[phase_index]).T


def _expected_active_keys() -> list[tuple[int, int, int]]:
    return [
        (phase_index, chirality, offset_sign)
        for phase_index in range(8)
        for chirality in (1, -1)
        for offset_sign in (1, -1)
    ]


def _expected_channel_off_keys() -> list[tuple[int, int]]:
    return [
        (phase_index, chirality)
        for phase_index in range(8)
        for chirality in (1, -1)
    ]


def _registration_controls() -> dict[str, Any]:
    phase_separation = min(
        abs(PHASES[right] - PHASES[left])
        for left in range(8)
        for right in range(left + 1, 8)
    )
    old_relative_phases = (0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0)
    old_distance = min(
        abs(math.remainder(phase - old, 2.0 * math.pi))
        for phase in PHASES
        for old in old_relative_phases
    )
    mirror_errors = []
    half_turn_errors = []
    for phase_index in range(8):
        plus = _phase_history(chirality=1, phase_index=phase_index)
        minus_mate = _phase_history(
            chirality=-1,
            phase_index=7 - phase_index,
        )
        expected_mirror = plus.copy()
        expected_mirror[:, 1] *= -1.0
        mirror_errors.append(float(np.max(np.abs(minus_mate - expected_mirror))))
        half = _phase_history(
            chirality=1,
            phase_index=(phase_index + 4) % 8,
        )
        half_turn_errors.append(float(np.max(np.abs(half + plus))))
    tolerance = THRESHOLDS.covariance_fraction * CANDIDATE.radius
    gates = {
        "eight_unique_phases": bool(
            len(set(PHASES)) == 8 and phase_separation > 0.0
        ),
        "unopened_relative_phase_grid": bool(old_distance > 0.0),
        "unopened_amplitude": bool(
            THRESHOLDS.offset_fraction
            not in p4.THRESHOLDS.offset_fractions
        ),
        "mirror_pairing": bool(max(mirror_errors) <= tolerance),
        "half_turn_pairing": bool(max(half_turn_errors) <= tolerance),
        "active_registration": bool(len(_expected_active_keys()) == 32),
        "channel_off_registration": bool(
            len(_expected_channel_off_keys()) == 16
        ),
    }
    return {
        "phases": list(PHASES),
        "minimum_phase_separation": phase_separation,
        "minimum_old_relative_phase_distance": old_distance,
        "maximum_mirror_history_error": max(mirror_errors),
        "maximum_half_turn_history_error": max(half_turn_errors),
        "active_order": [list(key) for key in _expected_active_keys()],
        "channel_off_order": [
            list(key) for key in _expected_channel_off_keys()
        ],
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _sample_metrics(
    state: np.ndarray,
    actuator: np.ndarray,
    *,
    step: int,
    chirality: int,
    readout: OrbitCenterReadout,
    targets: dict[int, np.ndarray],
    coupling_strength: float,
) -> dict[str, Any]:
    sample = p4._sample_metrics(
        state,
        actuator,
        step=step,
        chirality=chirality,
        readout=readout,
        targets=targets,
    )
    center = complex(*sample["center"])
    q_value = complex(*sample["actuator"])
    sample["interaction_energy"] = (
        0.5 * coupling_strength * abs(center - q_value) ** 2
    )
    return sample


def _mp_float(value: float) -> mp.mpf:
    numerator, denominator = float(value).as_integer_ratio()
    return mp.mpf(numerator) / mp.mpf(denominator)


def _mp_complex(value: complex) -> mp.mpc:
    number = complex(value)
    return mp.mpc(_mp_float(number.real), _mp_float(number.imag))


def _mp_history_dot(
    history: np.ndarray,
    *,
    readout: OrbitCenterReadout,
) -> mp.mpc:
    total = mp.mpc(0)
    state = np.asarray(history, dtype=float)
    for coefficient, row in zip(
        readout.coefficients,
        state,
        strict=True,
    ):
        total += _mp_complex(complex(coefficient)) * mp.mpc(
            _mp_float(float(row[0])),
            _mp_float(float(row[1])),
        )
    return total


def _mp_pair(value: mp.mpc, *, digits: int) -> list[str]:
    return [mp.nstr(value.real, digits), mp.nstr(value.imag, digits)]


def _high_precision_reference(
    step: SourceWriteStep,
    metrology: SourceWriteRoundingMetrology,
    *,
    readout: OrbitCenterReadout,
    update: int,
) -> dict[str, Any]:
    with mp.workdps(THRESHOLDS.reference_dps):
        center_after = _mp_history_dot(step.history, readout=readout)
        center_provisional = _mp_history_dot(
            step.provisional_history,
            readout=readout,
        )
        center_residual = (
            center_after
            - center_provisional
            - _mp_complex(step.center_prescribed_increment)
        )
        coupling_residual = (
            center_after
            - center_provisional
            + _mp_complex(step.actuator_after)
            - _mp_complex(step.actuator_before)
        )
        center_distance = abs(
            center_residual - _mp_complex(step.center_actuation_residual)
        )
        coupling_distance = abs(
            coupling_residual
            - _mp_complex(step.coupling_displacement_residual)
        )
        center_absolute = abs(center_residual)
        coupling_absolute = abs(coupling_residual)
    dot_bound = metrology.gamma_8h * (
        metrology.weighted_sum_after_upper
        + metrology.weighted_sum_provisional_upper
    )
    center_eval_envelope = dot_bound + metrology.gamma_8 * (
        abs(step.center_after)
        + abs(step.center_provisional)
        + abs(step.center_prescribed_increment)
    )
    coupling_eval_envelope = dot_bound + metrology.gamma_8 * (
        abs(step.center_after)
        + abs(step.center_provisional)
        + abs(step.actuator_after)
        + abs(step.actuator_before)
    )
    gates = {
        "center_inside_full_envelope": bool(
            center_absolute <= metrology.center_full_envelope
        ),
        "coupling_inside_full_envelope": bool(
            coupling_absolute <= metrology.coupling_full_envelope
        ),
        "center_binary64_distance": bool(
            center_distance <= center_eval_envelope
        ),
        "coupling_binary64_distance": bool(
            coupling_distance <= coupling_eval_envelope
        ),
    }
    return {
        "update": update,
        "precision_dps": THRESHOLDS.reference_dps,
        "center_residual": _mp_pair(
            center_residual,
            digits=THRESHOLDS.reference_dps,
        ),
        "coupling_residual": _mp_pair(
            coupling_residual,
            digits=THRESHOLDS.reference_dps,
        ),
        "center_absolute": float(center_absolute),
        "coupling_absolute": float(coupling_absolute),
        "center_binary64_distance": float(center_distance),
        "coupling_binary64_distance": float(coupling_distance),
        "center_full_envelope": metrology.center_full_envelope,
        "coupling_full_envelope": metrology.coupling_full_envelope,
        "center_eval_envelope": center_eval_envelope,
        "coupling_eval_envelope": coupling_eval_envelope,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _run_channel_off(*, phase_index: int, chirality: int) -> dict[str, Any]:
    readout = candidate_orbit_center_readout(CANDIDATE, chirality=chirality)
    state = _phase_history(chirality=chirality, phase_index=phase_index)
    actuator = np.zeros(2)
    targets = {
        sign: target_history(CANDIDATE, chirality=sign)
        for sign in (1, -1)
    }
    trace = [
        _sample_metrics(
            state,
            actuator,
            step=0,
            chirality=chirality,
            readout=readout,
            targets=targets,
            coupling_strength=0.0,
        )
    ]
    bitwise = True
    finite = True
    for update in range(1, THRESHOLDS.active_updates + 1):
        expected = native_fifo_step(state, **CANDIDATE.step_parameters())
        result = reciprocal_source_write_step(
            state,
            actuator,
            candidate=CANDIDATE,
            readout=readout,
            coupling_strength=0.0,
        )
        finite = bool(finite and p4._all_finite(result))
        bitwise = bool(bitwise and np.array_equal(result.history, expected))
        state = result.history
        actuator = result.actuator
        if update % THRESHOLDS.sample_every == 0:
            trace.append(
                _sample_metrics(
                    state,
                    actuator,
                    step=update,
                    chirality=chirality,
                    readout=readout,
                    targets=targets,
                    coupling_strength=0.0,
                )
            )
    maximum_d0 = max(row["expected_d0_fraction"] for row in trace)
    maximum_center = max(
        abs(complex(*row["center"])) / CANDIDATE.radius for row in trace
    )
    gates = {
        "complete": bool(trace[-1]["step"] == THRESHOLDS.active_updates),
        "finite": finite,
        "bitwise_native": bitwise,
        "prepared_orbit": bool(
            maximum_d0 <= THRESHOLDS.channel_off_d0_fraction
        ),
        "stationary_orbit_center": bool(
            maximum_center <= THRESHOLDS.channel_off_d0_fraction
        ),
    }
    return {
        "name": f"phase-{phase_index}-s{chirality:+d}-channel-off",
        "phase_index": phase_index,
        "phase": PHASES[phase_index],
        "chirality": chirality,
        "trace": trace,
        "maximum_d0_fraction": maximum_d0,
        "maximum_center_fraction": maximum_center,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _run_active_arm(
    *,
    phase_index: int,
    chirality: int,
    offset_sign: int,
    baseline: dict[str, Any],
) -> dict[str, Any]:
    readout = candidate_orbit_center_readout(CANDIDATE, chirality=chirality)
    state = _phase_history(chirality=chirality, phase_index=phase_index)
    delta = THRESHOLDS.offset_fraction * CANDIDATE.radius
    signed_direction = complex(float(offset_sign), 0.0)
    q_initial = delta * signed_direction
    actuator = complex_to_vector(q_initial)
    targets = {
        sign: target_history(CANDIDATE, chirality=sign)
        for sign in (1, -1)
    }
    trace = [
        _sample_metrics(
            state,
            actuator,
            step=0,
            chirality=chirality,
            readout=readout,
            targets=targets,
            coupling_strength=THRESHOLDS.coupling_strength,
        )
    ]
    initial_energy = 0.5 * THRESHOLDS.coupling_strength * delta**2
    initial_force_scale: float | None = None
    initial_displacement_scale: float | None = None
    maxima = {
        "work_split": 0.0,
        "ledger": 0.0,
        "force_balance": 0.0,
        "midpoint": 0.0,
        "center_local": 0.0,
        "coupling_local": 0.0,
        "center_full": 0.0,
        "coupling_full": 0.0,
        "actuator_full": 0.0,
        "center_envelope_ratio": 0.0,
        "coupling_envelope_ratio": 0.0,
        "actuator_envelope_ratio": 0.0,
        "truncated_ledger": 0.0,
        "raw_center_ledger": 0.0,
    }
    minimum_margins = {
        "center_full": math.inf,
        "coupling_full": math.inf,
        "actuator_full": math.inf,
    }
    cumulative = {
        "work_split": 0.0,
        "ledger": 0.0,
        "write_work": 0.0,
        "age_work": 0.0,
        "center_work": 0.0,
        "raw_center_work": 0.0,
        "external_work": 0.0,
        "truncated_ledger": 0.0,
        "raw_center_ledger": 0.0,
        "write_dissipation": 0.0,
        "external_dissipation": 0.0,
    }
    minimum_dissipation = math.inf
    normal_operands = True
    finite = True
    complete = True
    stop_reason = "completed"
    reference_checks: list[dict[str, Any]] = []
    for update in range(1, THRESHOLDS.active_updates + 1):
        result = reciprocal_source_write_step(
            state,
            actuator,
            candidate=CANDIDATE,
            readout=readout,
            coupling_strength=THRESHOLDS.coupling_strength,
        )
        if not p4._all_finite(result):
            finite = False
            complete = False
            stop_reason = "nonfinite-transition"
            break
        metrology = source_write_rounding_metrology(result, readout=readout)
        if not p4._all_finite(metrology):
            finite = False
            complete = False
            stop_reason = "nonfinite-metrology"
            break
        normal_operands = bool(normal_operands and metrology.normal_operands)
        if initial_force_scale is None:
            initial_force_scale = abs(result.center_force)
            initial_displacement_scale = (
                CANDIDATE.alpha * readout.write_gain * initial_force_scale
            )
        maxima["work_split"] = max(
            maxima["work_split"], abs(result.work_split_residual)
        )
        maxima["ledger"] = max(maxima["ledger"], abs(result.ledger_residual))
        maxima["force_balance"] = max(
            maxima["force_balance"], abs(result.force_balance_residual)
        )
        maxima["midpoint"] = max(
            maxima["midpoint"], abs(result.midpoint_force_residual)
        )
        maxima["center_local"] = max(
            maxima["center_local"], abs(metrology.center_local_residual)
        )
        maxima["coupling_local"] = max(
            maxima["coupling_local"], abs(metrology.coupling_local_residual)
        )
        maxima["center_full"] = max(
            maxima["center_full"], abs(metrology.center_full_residual)
        )
        maxima["coupling_full"] = max(
            maxima["coupling_full"], abs(metrology.coupling_full_residual)
        )
        maxima["actuator_full"] = max(
            maxima["actuator_full"], abs(metrology.actuator_full_residual)
        )
        center_ratio = abs(metrology.center_full_residual) / max(
            metrology.center_full_envelope,
            np.finfo(float).tiny,
        )
        coupling_ratio = abs(metrology.coupling_full_residual) / max(
            metrology.coupling_full_envelope,
            np.finfo(float).tiny,
        )
        actuator_ratio = abs(metrology.actuator_full_residual) / max(
            metrology.actuator_full_envelope,
            np.finfo(float).tiny,
        )
        maxima["center_envelope_ratio"] = max(
            maxima["center_envelope_ratio"], center_ratio
        )
        maxima["coupling_envelope_ratio"] = max(
            maxima["coupling_envelope_ratio"], coupling_ratio
        )
        maxima["actuator_envelope_ratio"] = max(
            maxima["actuator_envelope_ratio"], actuator_ratio
        )
        minimum_margins["center_full"] = min(
            minimum_margins["center_full"],
            metrology.center_full_envelope
            - abs(metrology.center_full_residual),
        )
        minimum_margins["coupling_full"] = min(
            minimum_margins["coupling_full"],
            metrology.coupling_full_envelope
            - abs(metrology.coupling_full_residual),
        )
        minimum_margins["actuator_full"] = min(
            minimum_margins["actuator_full"],
            metrology.actuator_full_envelope
            - abs(metrology.actuator_full_residual),
        )
        maxima["truncated_ledger"] = max(
            maxima["truncated_ledger"],
            abs(result.truncated_ledger_residual),
        )
        maxima["raw_center_ledger"] = max(
            maxima["raw_center_ledger"],
            abs(result.raw_center_ledger_residual),
        )
        cumulative["work_split"] += result.work_split_residual
        cumulative["ledger"] += result.ledger_residual
        cumulative["write_work"] += result.write_work
        cumulative["age_work"] += result.age_work
        cumulative["center_work"] += result.center_work
        cumulative["raw_center_work"] += result.raw_center_work
        cumulative["external_work"] += result.external_work
        cumulative["truncated_ledger"] += result.truncated_ledger_residual
        cumulative["raw_center_ledger"] += result.raw_center_ledger_residual
        cumulative["write_dissipation"] += result.write_mobility_dissipation
        cumulative["external_dissipation"] += (
            result.external_mobility_dissipation
        )
        minimum_dissipation = min(
            minimum_dissipation,
            result.write_mobility_dissipation,
            result.external_mobility_dissipation,
        )
        if update in THRESHOLDS.reference_steps:
            reference_checks.append(
                _high_precision_reference(
                    result,
                    metrology,
                    readout=readout,
                    update=update,
                )
            )
        state = result.history
        actuator = result.actuator
        if update % THRESHOLDS.sample_every == 0:
            trace.append(
                _sample_metrics(
                    state,
                    actuator,
                    step=update,
                    chirality=chirality,
                    readout=readout,
                    targets=targets,
                    coupling_strength=THRESHOLDS.coupling_strength,
                )
            )
    if initial_force_scale is None or initial_displacement_scale is None:
        initial_force_scale = 0.0
        initial_displacement_scale = 0.0
    baseline_by_step = {row["step"]: row for row in baseline["trace"]}
    response_trace = []
    for row in trace:
        control = baseline_by_step[row["step"]]
        response_trace.append(
            {
                "step": row["step"],
                "center": p4._complex_pair(
                    complex(*row["center"]) - complex(*control["center"])
                ),
                "actuator": p4._complex_pair(
                    complex(*row["actuator"])
                    - complex(*control["actuator"])
                ),
            }
        )
    final = trace[-1]
    final_response = response_trace[-1]
    final_center = complex(*final["center"])
    final_actuator = complex(*final["actuator"])
    response_center = complex(*final_response["center"])
    response_actuator = complex(*final_response["actuator"])
    final_separation_ratio = abs(final_center - final_actuator) / delta
    center_projection = real_inner(signed_direction, response_center) / delta
    actuator_projection = (
        real_inner(signed_direction, response_actuator) / delta
    )
    energy_ratio = final["interaction_energy"] / initial_energy
    late = [row for row in trace if row["step"] >= THRESHOLDS.late_start]
    late_maximum_d0 = (
        max(row["expected_d0_fraction"] for row in late) if late else None
    )
    late_opposite_minimum = (
        min(row["opposite_d0_fraction"] for row in late) if late else None
    )
    phase_thresholds = FormationThresholds(
        active_updates=THRESHOLDS.active_updates,
        sample_every=THRESHOLDS.sample_every,
        phase_start=THRESHOLDS.phase_start,
    )
    phase = phase_increment_metrics(
        trace,
        chirality=chirality,
        candidate=CANDIDATE,
        thresholds=phase_thresholds,
    )
    maximum_center_response = max(
        abs(complex(*row["center"])) for row in response_trace
    ) / delta
    force_scale = max(initial_force_scale, np.finfo(float).tiny)
    displacement_scale = max(initial_displacement_scale, np.finfo(float).tiny)
    reference_pass = bool(
        len(reference_checks) == len(THRESHOLDS.reference_steps)
        and all(row["pass"] for row in reference_checks)
    )
    ledger_gates = {
        "work_split_step": bool(
            maxima["work_split"] / initial_energy
            <= THRESHOLDS.step_ledger_relative
        ),
        "total_ledger_step": bool(
            maxima["ledger"] / initial_energy
            <= THRESHOLDS.step_ledger_relative
        ),
        "work_split_cumulative": bool(
            abs(cumulative["work_split"]) / initial_energy
            <= THRESHOLDS.cumulative_ledger_relative
        ),
        "total_ledger_cumulative": bool(
            abs(cumulative["ledger"]) / initial_energy
            <= THRESHOLDS.cumulative_ledger_relative
        ),
        "force_balance": bool(
            maxima["force_balance"] / force_scale
            <= THRESHOLDS.force_relative
        ),
        "midpoint_force": bool(
            maxima["midpoint"] / force_scale <= THRESHOLDS.force_relative
        ),
        "center_local": bool(
            maxima["center_local"] / displacement_scale
            <= THRESHOLDS.local_displacement_relative
        ),
        "coupling_local": bool(
            maxima["coupling_local"] / displacement_scale
            <= THRESHOLDS.local_displacement_relative
        ),
        "center_full_envelope": bool(
            maxima["center_envelope_ratio"] <= 1.0
            and minimum_margins["center_full"] >= 0.0
        ),
        "coupling_full_envelope": bool(
            maxima["coupling_envelope_ratio"] <= 1.0
            and minimum_margins["coupling_full"] >= 0.0
        ),
        "actuator_update_relative": bool(
            maxima["actuator_full"] / displacement_scale
            <= THRESHOLDS.actuator_displacement_relative
        ),
        "actuator_update_envelope": bool(
            maxima["actuator_envelope_ratio"] <= 1.0
            and minimum_margins["actuator_full"] >= 0.0
        ),
        "high_precision_reference": reference_pass,
        "nonnegative_mobility": bool(
            math.isfinite(minimum_dissipation)
            and minimum_dissipation >= -1.0e-30
        ),
    }
    dynamic_gates = {
        "maximum_d0": bool(
            max(row["expected_d0_fraction"] for row in trace)
            <= THRESHOLDS.maximum_d0_fraction
        ),
        "late_d0": bool(
            late_maximum_d0 is not None
            and late_maximum_d0 <= THRESHOLDS.late_d0_fraction
        ),
        "opposite_chirality": bool(
            late_opposite_minimum is not None
            and late_opposite_minimum >= THRESHOLDS.opposite_d0_fraction
        ),
        "final_separation": bool(
            final_separation_ratio <= THRESHOLDS.final_separation_fraction
        ),
        "center_projection": bool(
            THRESHOLDS.projection_minimum
            <= center_projection
            <= THRESHOLDS.projection_maximum
        ),
        "actuator_projection": bool(
            THRESHOLDS.projection_minimum
            <= actuator_projection
            <= THRESHOLDS.projection_maximum
        ),
        "interaction_energy": bool(
            energy_ratio <= THRESHOLDS.energy_ratio_maximum
        ),
        "phase": bool(phase["pass"]),
        "informative_signal": bool(
            maximum_center_response >= THRESHOLDS.signal_fraction
        ),
    }
    validity_gates = {
        "complete": bool(
            complete and trace[-1]["step"] == THRESHOLDS.active_updates
        ),
        "finite": finite,
        "normal_operands": normal_operands,
    }
    return {
        "name": f"phase-{phase_index}-s{chirality:+d}-q{offset_sign:+d}",
        "phase_index": phase_index,
        "phase": PHASES[phase_index],
        "chirality": chirality,
        "offset_sign": offset_sign,
        "offset_fraction": THRESHOLDS.offset_fraction,
        "offset": delta,
        "stop_reason": stop_reason,
        "trace": trace,
        "response_trace": response_trace,
        "residual_scales": {
            "initial_energy": initial_energy,
            "initial_force": initial_force_scale,
            "initial_coupling_displacement": initial_displacement_scale,
        },
        "residual_maxima": maxima,
        "minimum_envelope_margins": minimum_margins,
        "cumulative_work": cumulative,
        "minimum_mobility_dissipation": minimum_dissipation,
        "high_precision_references": reference_checks,
        "maximum_d0_fraction": max(
            row["expected_d0_fraction"] for row in trace
        ),
        "late_maximum_d0_fraction": late_maximum_d0,
        "late_opposite_minimum_fraction": late_opposite_minimum,
        "final_separation_ratio": final_separation_ratio,
        "center_projection_ratio": center_projection,
        "actuator_projection_ratio": actuator_projection,
        "energy_ratio": energy_ratio,
        "maximum_center_response_ratio": maximum_center_response,
        "phase_metrics": phase,
        "validity_gates": validity_gates,
        "ledger_gates": ledger_gates,
        "dynamic_gates": dynamic_gates,
        "valid": bool(all(validity_gates.values())),
        "ledger_pass": bool(all(ledger_gates.values())),
        "dynamic_pass": bool(all(dynamic_gates.values())),
        "nondecisional_rivals": {
            "truncated_age_ledger": {
                "maximum_residual": maxima["truncated_ledger"],
                "cumulative_residual": cumulative["truncated_ledger"],
            },
            "raw_memory_center_ledger": {
                "maximum_residual": maxima["raw_center_ledger"],
                "cumulative_residual": cumulative["raw_center_ledger"],
            },
        },
    }


def _trace_complex(
    arm: dict[str, Any],
    key: str,
    *,
    trace_key: str = "trace",
) -> np.ndarray:
    return np.asarray(
        [complex(*row[key]) for row in arm[trace_key]],
        dtype=np.complex128,
    )


def _rms(values: np.ndarray) -> float:
    array = np.asarray(values, dtype=np.complex128)
    return float(math.sqrt(float(np.mean(np.abs(array) ** 2))))


def _active_key(arm: dict[str, Any]) -> tuple[int, int, int]:
    return (
        int(arm["phase_index"]),
        int(arm["chirality"]),
        int(arm["offset_sign"]),
    )


def _channel_off_key(arm: dict[str, Any]) -> tuple[int, int]:
    return int(arm["phase_index"]), int(arm["chirality"])


def _registered_panel(
    active_arms: list[dict[str, Any]],
    channel_off_arms: list[dict[str, Any]],
) -> bool:
    return bool(
        [_active_key(arm) for arm in active_arms]
        == _expected_active_keys()
        and [_channel_off_key(arm) for arm in channel_off_arms]
        == _expected_channel_off_keys()
    )


def _unavailable_response(reason: str) -> dict[str, Any]:
    gates = {
        "odd_signal_resolved": False,
        "even_response": False,
        "mirror_equivariance": False,
        "half_turn_equivariance": False,
    }
    return {
        "available": False,
        "reason": reason,
        "even_response": [],
        "mirror_equivariance": [],
        "half_turn_equivariance": [],
        "phase_chirality_response": [],
        "phase_averages": [],
        "phase_averaged_transverse_response": {
            "center": None,
            "actuator": None,
        },
        "positive_phase_support": {"center": 0, "actuator": 0},
        "gates": gates,
        "pass": False,
    }


def _response_controls(
    active_arms: list[dict[str, Any]],
    channel_off_arms: list[dict[str, Any]],
) -> dict[str, Any]:
    if not _registered_panel(active_arms, channel_off_arms):
        return _unavailable_response("misregistered-panel")

    expected_steps = list(
        range(
            0,
            THRESHOLDS.active_updates + 1,
            THRESHOLDS.sample_every,
        )
    )
    all_arms = [*active_arms, *channel_off_arms]
    if any(
        [row["step"] for row in arm["trace"]] != expected_steps
        or not p4._all_finite(arm["trace"])
        for arm in all_arms
    ):
        return _unavailable_response("incomplete-or-nonfinite-traces")

    active = {_active_key(arm): arm for arm in active_arms}
    controls = {
        _channel_off_key(arm): arm for arm in channel_off_arms
    }
    delta = THRESHOLDS.offset_fraction * CANDIDATE.radius

    responses: dict[tuple[int, int, int, str], np.ndarray] = {}
    for phase_index, chirality, offset_sign in _expected_active_keys():
        arm = active[(phase_index, chirality, offset_sign)]
        baseline = controls[(phase_index, chirality)]
        for component in ("center", "actuator"):
            responses[
                (phase_index, chirality, offset_sign, component)
            ] = _trace_complex(arm, component) - _trace_complex(
                baseline,
                component,
            )

    even_rows: list[dict[str, Any]] = []
    response_rows: list[dict[str, Any]] = []
    response_index: dict[tuple[int, int], dict[str, Any]] = {}
    for phase_index in range(8):
        for chirality in (1, -1):
            row: dict[str, Any] = {
                "phase_index": phase_index,
                "phase": PHASES[phase_index],
                "chirality": chirality,
            }
            even_row: dict[str, Any] = {
                "phase_index": phase_index,
                "chirality": chirality,
            }
            component_passes = []
            for component, label in (
                ("center", "center"),
                ("actuator", "actuator"),
            ):
                plus = responses[(phase_index, chirality, 1, component)]
                minus = responses[(phase_index, chirality, -1, component)]
                odd = (plus - minus) / (2.0 * delta)
                even = (plus + minus) / (2.0 * delta)
                odd_rms = _rms(odd)
                even_rms = _rms(even)
                resolved = bool(math.isfinite(odd_rms) and odd_rms > 0.0)
                ratio = even_rms / odd_rms if resolved else None
                passed = bool(
                    resolved
                    and ratio is not None
                    and math.isfinite(ratio)
                    and ratio <= THRESHOLDS.even_response_relative
                )
                final_odd = complex(odd[-1])
                row[f"{label}_odd_final"] = p4._complex_pair(final_odd)
                row[f"{label}_longitudinal"] = float(final_odd.real)
                row[f"{label}_transverse"] = float(
                    -chirality * final_odd.imag
                )
                even_row[f"{label}_odd_rms"] = odd_rms
                even_row[f"{label}_even_rms"] = even_rms
                even_row[f"{label}_even_to_odd_rms"] = ratio
                even_row[f"{label}_odd_resolved"] = resolved
                component_passes.append(passed)
            even_row["pass"] = bool(all(component_passes))
            even_rows.append(even_row)
            response_rows.append(row)
            response_index[(phase_index, chirality)] = row

    covariance_limit = THRESHOLDS.covariance_fraction
    mirror_rows = []
    for phase_index in range(8):
        for offset_sign in (1, -1):
            plus = active[(phase_index, 1, offset_sign)]
            minus = active[(7 - phase_index, -1, offset_sign)]
            center_error = float(
                np.max(
                    np.abs(
                        _trace_complex(minus, "center")
                        - np.conjugate(_trace_complex(plus, "center"))
                    )
                )
                / CANDIDATE.radius
            )
            actuator_error = float(
                np.max(
                    np.abs(
                        _trace_complex(minus, "actuator")
                        - np.conjugate(_trace_complex(plus, "actuator"))
                    )
                )
                / CANDIDATE.radius
            )
            mirror_rows.append(
                {
                    "plus_phase_index": phase_index,
                    "minus_phase_index": 7 - phase_index,
                    "offset_sign": offset_sign,
                    "center_error_fraction": center_error,
                    "actuator_error_fraction": actuator_error,
                    "pass": bool(
                        max(center_error, actuator_error) <= covariance_limit
                    ),
                }
            )

    half_turn_rows = []
    for phase_index in range(4):
        for chirality in (1, -1):
            for offset_sign in (1, -1):
                first = active[(phase_index, chirality, offset_sign)]
                second = active[
                    (phase_index + 4, chirality, -offset_sign)
                ]
                center_error = float(
                    np.max(
                        np.abs(
                            _trace_complex(second, "center")
                            + _trace_complex(first, "center")
                        )
                    )
                    / CANDIDATE.radius
                )
                actuator_error = float(
                    np.max(
                        np.abs(
                            _trace_complex(second, "actuator")
                            + _trace_complex(first, "actuator")
                        )
                    )
                    / CANDIDATE.radius
                )
                half_turn_rows.append(
                    {
                        "phase_index": phase_index,
                        "mate_phase_index": phase_index + 4,
                        "chirality": chirality,
                        "offset_sign": offset_sign,
                        "mate_offset_sign": -offset_sign,
                        "center_error_fraction": center_error,
                        "actuator_error_fraction": actuator_error,
                        "pass": bool(
                            max(center_error, actuator_error)
                            <= covariance_limit
                        ),
                    }
                )

    phase_rows = []
    for phase_index in range(8):
        plus = response_index[(phase_index, 1)]
        minus = response_index[(phase_index, -1)]
        center_transverse = 0.5 * (
            plus["center_transverse"] + minus["center_transverse"]
        )
        actuator_transverse = 0.5 * (
            plus["actuator_transverse"] + minus["actuator_transverse"]
        )
        phase_rows.append(
            {
                "phase_index": phase_index,
                "phase": PHASES[phase_index],
                "center_transverse": center_transverse,
                "actuator_transverse": actuator_transverse,
                "center_positive": bool(center_transverse > 0.0),
                "actuator_positive": bool(actuator_transverse > 0.0),
            }
        )
    center_mean = math.fsum(
        row["center_transverse"] for row in phase_rows
    ) / len(phase_rows)
    actuator_mean = math.fsum(
        row["actuator_transverse"] for row in phase_rows
    ) / len(phase_rows)
    center_support = sum(row["center_positive"] for row in phase_rows)
    actuator_support = sum(row["actuator_positive"] for row in phase_rows)

    gates = {
        "odd_signal_resolved": bool(
            all(
                row["center_odd_resolved"]
                and row["actuator_odd_resolved"]
                for row in even_rows
            )
        ),
        "even_response": bool(all(row["pass"] for row in even_rows)),
        "mirror_equivariance": bool(
            all(row["pass"] for row in mirror_rows)
        ),
        "half_turn_equivariance": bool(
            all(row["pass"] for row in half_turn_rows)
        ),
    }
    return {
        "available": True,
        "reason": None,
        "even_response": even_rows,
        "mirror_equivariance": mirror_rows,
        "half_turn_equivariance": half_turn_rows,
        "phase_chirality_response": response_rows,
        "phase_averages": phase_rows,
        "phase_averaged_transverse_response": {
            "center": center_mean,
            "actuator": actuator_mean,
        },
        "positive_phase_support": {
            "center": center_support,
            "actuator": actuator_support,
        },
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _decision(
    *,
    pipeline: bool,
    active_arms: list[dict[str, Any]],
    channel_off_arms: list[dict[str, Any]],
    response: dict[str, Any],
) -> tuple[str, dict[str, bool]]:
    registration = _registered_panel(active_arms, channel_off_arms)
    validity = bool(
        registration and all(arm["valid"] for arm in active_arms)
    )
    response_available = bool(response.get("available", False))
    ledger = bool(
        registration and all(arm["ledger_pass"] for arm in active_arms)
    )
    dynamic = bool(
        registration and all(arm["dynamic_pass"] for arm in active_arms)
    )
    response_pass = bool(response.get("pass", False))
    means = response.get("phase_averaged_transverse_response", {})
    center_mean = means.get("center")
    actuator_mean = means.get("actuator")
    finite_means = bool(
        center_mean is not None
        and actuator_mean is not None
        and math.isfinite(center_mean)
        and math.isfinite(actuator_mean)
    )
    scalar_region = bool(
        finite_means
        and abs(center_mean) <= THRESHOLDS.scalar_null_maximum
        and abs(actuator_mean) <= THRESHOLDS.scalar_null_maximum
    )
    positive_chiral_region = bool(
        finite_means
        and center_mean >= THRESHOLDS.chiral_minimum
        and actuator_mean >= THRESHOLDS.chiral_minimum
    )
    support = response.get("positive_phase_support", {})
    sign_support = bool(
        support.get("center", 0) >= THRESHOLDS.sign_support_minimum
        and support.get("actuator", 0) >= THRESHOLDS.sign_support_minimum
    )
    directional_fail = bool(
        finite_means
        and (
            center_mean <= -THRESHOLDS.chiral_minimum
            or actuator_mean <= -THRESHOLDS.chiral_minimum
            or (
                abs(center_mean) >= THRESHOLDS.chiral_minimum
                and abs(actuator_mean) >= THRESHOLDS.chiral_minimum
                and math.copysign(1.0, center_mean)
                != math.copysign(1.0, actuator_mean)
            )
        )
    )

    if (
        not pipeline
        or not registration
        or not validity
        or not response_available
        or not finite_means
    ):
        decision = "p4r-inconclusive"
    elif not ledger:
        decision = "p4r-ledger-or-metrology-fail"
    elif not dynamic or not response_pass:
        decision = "p4r-inconclusive"
    elif scalar_region:
        decision = "p4r-phase-averaged-scalar-response"
    elif positive_chiral_region and sign_support:
        decision = "p4r-phase-averaged-chiral-response-pass"
    elif directional_fail:
        decision = "p4r-phase-averaged-chiral-hypothesis-fail"
    else:
        decision = "p4r-inconclusive"
    return decision, {
        "pipeline": pipeline,
        "registration": registration,
        "valid_active_arms": validity,
        "response_available": response_available,
        "reciprocal_ledger_and_metrology": ledger,
        "nonlinear_loop_dynamics": dynamic,
        "response_symmetry_and_odd_signal": response_pass,
        "finite_phase_averages": finite_means,
        "scalar_region": scalar_region,
        "positive_chiral_region": positive_chiral_region,
        "positive_phase_support": sign_support,
        "directional_fail_region": directional_fail,
    }


def run_gate() -> dict[str, Any]:
    """Execute the frozen P4-R-phi target calculation."""

    started = time.perf_counter()
    provenance = _verify_provenance()
    construction = p4._construction_controls()
    registration = _registration_controls()
    channel_off_arms = [
        _run_channel_off(phase_index=phase_index, chirality=chirality)
        for phase_index, chirality in _expected_channel_off_keys()
    ]
    channel_off = {
        _channel_off_key(arm): arm for arm in channel_off_arms
    }
    active_arms = [
        _run_active_arm(
            phase_index=phase_index,
            chirality=chirality,
            offset_sign=offset_sign,
            baseline=channel_off[(phase_index, chirality)],
        )
        for phase_index, chirality, offset_sign in _expected_active_keys()
    ]
    response = _response_controls(active_arms, channel_off_arms)
    channel_off_pass = bool(all(arm["pass"] for arm in channel_off_arms))
    pipeline = bool(
        construction["pass"] and registration["pass"] and channel_off_pass
    )
    decision, gates = _decision(
        pipeline=pipeline,
        active_arms=active_arms,
        channel_off_arms=channel_off_arms,
        response=response,
    )
    return {
        "schema_version": 1,
        "gate": "P4-R-phi phase-averaged source/write response metrology",
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
            "mpmath": importlib.metadata.version("mpmath"),
        },
        "historical_p4": {
            "decision": provenance["p4_decision"],
            "json_sha256": provenance["p4_sha256"],
            "unchanged_by_p4r": True,
        },
        "protocol": {
            "path": PROTOCOL.as_posix(),
            "freeze_revision": PROTOCOL_FREEZE_REVISION,
            "referee_charter": REFEREE_CHARTER.as_posix(),
            "target_base_revision": TARGET_BASE_REVISION,
            "thresholds": asdict(THRESHOLDS),
            "phases": list(PHASES),
            "active_order": [list(key) for key in _expected_active_keys()],
            "channel_off_order": [
                list(key) for key in _expected_channel_off_keys()
            ],
            "no_target_fit": True,
            "no_mass_spin_momentum_or_p5_claim": True,
        },
        "registration_controls": registration,
        "construction_controls": construction,
        "channel_off_arms": channel_off_arms,
        "active_arms": active_arms,
        "response_controls": response,
        "gates": gates,
        "decision": decision,
        "claim_boundary": {
            "established_if_chiral_pass": (
                "a registered eight-node discrete phase-averaged chiral "
                "response of the reciprocal source/write L3 loop for the "
                "single frozen perturbation amplitude"
            ),
            "not_established": (
                "continuous phase independence, amplitude scaling, material "
                "center of mass, physical mass, spin, conserved momentum, "
                "noise robustness, P4-R-S or P5"
            ),
        },
    }


def _format(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.6g}"


def _claim_boundary_lines(payload: dict[str, Any]) -> list[str]:
    claim = payload["claim_boundary"]["established_if_chiral_pass"]
    if payload["decision"] == "p4r-phase-averaged-chiral-response-pass":
        return ["Established by this registered pass: " + claim + "."]
    return [
        "The conditional chiral-pass boundary was not activated.",
        "A chiral pass would have established only: " + claim + ".",
    ]


def render_report(payload: dict[str, Any], *, summary_sha256: str) -> str:
    """Render a compact human-readable record of the frozen decision."""

    response = payload["response_controls"]
    means = response["phase_averaged_transverse_response"]
    support = response["positive_phase_support"]
    active = payload["active_arms"]
    maximum_metrology = {
        "center_local_relative": max(
            arm["residual_maxima"]["center_local"]
            / max(
                arm["residual_scales"]["initial_coupling_displacement"],
                np.finfo(float).tiny,
            )
            for arm in active
        ),
        "coupling_local_relative": max(
            arm["residual_maxima"]["coupling_local"]
            / max(
                arm["residual_scales"]["initial_coupling_displacement"],
                np.finfo(float).tiny,
            )
            for arm in active
        ),
        "center_envelope_ratio": max(
            arm["residual_maxima"]["center_envelope_ratio"]
            for arm in active
        ),
        "coupling_envelope_ratio": max(
            arm["residual_maxima"]["coupling_envelope_ratio"]
            for arm in active
        ),
        "actuator_envelope_ratio": max(
            arm["residual_maxima"]["actuator_envelope_ratio"]
            for arm in active
        ),
    }
    lines = [
        "# P4-R-phi phase-averaged source/write response",
        "",
        f"Date: {payload['generated_at_utc'][:10]}.",
        "",
        f"Decision: **`{payload['decision']}`**.",
        "",
        "This is the first execution of the prospectively frozen eight-phase",
        "holdout and binary64 metrology protocol. The phase nodes are a",
        "deterministic quadrature with four mirror-related pairs, not",
        "independent statistical replications.",
        "",
        "## Gate summary",
        "",
        "| gate | status |",
        "| --- | :---: |",
    ]
    for name, passed in payload["gates"].items():
        lines.append(f"| `{name}` | {'pass' if passed else 'fail'} |")
    lines.extend(
        [
            "",
            "## Frozen phase classifier",
            "",
            "| quantity | center | actuator |",
            "| --- | ---: | ---: |",
            (
                "| phase-averaged transverse response | "
                f"{_format(means['center'])} | "
                f"{_format(means['actuator'])} |"
            ),
            (
                "| positive phase nodes | "
                f"{support['center']}/8 | {support['actuator']}/8 |"
            ),
            "",
            "| phase node | center transverse | actuator transverse |",
            "| ---: | ---: | ---: |",
        ]
    )
    for row in response["phase_averages"]:
        lines.append(
            f"| {row['phase_index']} | "
            f"{_format(row['center_transverse'])} | "
            f"{_format(row['actuator_transverse'])} |"
        )
    lines.extend(
        [
            "",
            "## Arithmetic metrology",
            "",
            "| diagnostic maximum over 32 active arms | value |",
            "| --- | ---: |",
        ]
    )
    for name, value in maximum_metrology.items():
        lines.append(f"| `{name}` | {_format(value)} |")
    lines.extend(
        [
            "",
            "All active arms include 80-decimal-digit exact-ratio replays at",
            "updates 1, 2000 and 4000. Passing a full-dot envelope establishes",
            "compatibility with the declared rounding model, not a formal",
            "interval proof.",
            "",
            "## Interpretation boundary",
            "",
            *_claim_boundary_lines(payload),
            "",
            "Not established: "
            + payload["claim_boundary"]["not_established"]
            + ".",
            "",
            "The historical P4 decision remains "
            f"`{payload['historical_p4']['decision']}`.",
            "",
            "## Provenance",
            "",
            "- Protocol freeze revision: "
            f"`{payload['protocol']['freeze_revision']}`.",
            f"- Execution revision: `{payload['provenance']['revision']}`.",
            f"- Runtime: Python `{payload['runtime']['python']}`, NumPy "
            f"`{payload['runtime']['numpy']}`, SciPy "
            f"`{payload['runtime']['scipy']}`, mpmath "
            f"`{payload['runtime']['mpmath']}`.",
            f"- Machine-readable JSON SHA-256: `{summary_sha256}`.",
            "",
        ]
    )
    return "\n".join(lines)


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, np.generic):
        return _json_safe(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _is_default_output(path: Path, default: Path) -> bool:
    candidate = path if path.is_absolute() else ROOT / path
    reference = default if default.is_absolute() else ROOT / default
    return candidate.resolve() == reference.resolve()


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    if temporary.exists():
        raise RuntimeError(f"refusing to replace stale temporary file: {temporary}")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()
    summary_path = args.summary if args.summary.is_absolute() else ROOT / args.summary
    report_path = args.report if args.report.is_absolute() else ROOT / args.report
    if _is_default_output(args.summary, DEFAULT_SUMMARY) and summary_path.exists():
        raise RuntimeError("refusing to overwrite the registered P4-R JSON")
    if _is_default_output(args.report, DEFAULT_REPORT) and report_path.exists():
        raise RuntimeError("refusing to overwrite the registered P4-R report")

    payload = _json_safe(run_gate())
    serialized = json.dumps(
        payload,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
    summary_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    report = render_report(payload, summary_sha256=summary_hash)
    _atomic_write(summary_path, serialized)
    _atomic_write(report_path, report)
    print(
        json.dumps(
            {"decision": payload["decision"], "json_sha256": summary_hash}
        )
    )


if __name__ == "__main__":
    main()
