"""Execute the frozen P4 reciprocal orbit-center source/write gate."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, fields, is_dataclass
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

from emergenz_knoten.loop_center_response import memory_center as vector_memory_center
from emergenz_knoten.orbit_center_actuator import (
    adjoint_slot_forces,
    build_orbit_center_readout,
    candidate_orbit_center_readout,
    complex_to_vector,
    memory_center,
    orbit_center,
    readout_payload,
    real_inner,
    reciprocal_source_write_step,
)
from emergenz_knoten.rotating_wave_formation import (
    FormationThresholds,
    phase_increment_metrics,
    target_history,
)
from emergenz_knoten.rotating_wave_stability import (
    native_fifo_step,
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
    "scalar_memory_loop_p4_source_write_protocol_2026-08-26.md"
)
ARCHITECTURE_AUDIT = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_loop_p4_actuator_architecture_audit_2026-08-26.md"
)
P3_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_p3_formation_basin_2026-08-26.json"
)
P3_REVIEW = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_p3_formation_basin_review_2026-08-26.md"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4_source_write_2026-08-26.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4_source_write_2026-08-26.json"
)

FREEZE_REVISION = "15ccd714ba595c92ae5d0aff936977f78977f632"
EXPECTED_P3_SHA256 = (
    "42469985488ee73e2bd8bb1c6dc4cd339b58684b85f2743fa1b2df340e82fc2b"
)
EXPECTED_BLOBS = {
    PROTOCOL.as_posix(): "fb1f41c66fad0e6df9c7dc8a226517940deab939",
    ARCHITECTURE_AUDIT.as_posix(): "91620a60f7af84fb9eeeb5c8a5ce0036b9e04906",
    P3_RESULT.as_posix(): "35b46192c2c4dc7ace3751d321a4e25bd3a80096",
    P3_REVIEW.as_posix(): "5897be4ba6c4011eb7afbd32f6f3cacf538600ca",
    "src/emergenz_knoten/rotating_wave_stability.py": (
        "9defb5a6876371202e1ba57cea030c997b9c6edd"
    ),
    "src/emergenz_knoten/loop_center_response.py": (
        "a8b8a002be3a3e4d75f8bd6b00989f1dafe61e0b"
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


@dataclass(frozen=True)
class P4Thresholds:
    active_updates: int = 4_000
    sample_every: int = 10
    late_start: int = 3_600
    phase_start: int = 3_000
    coupling_strength: float = 0.25
    offset_fractions: tuple[float, ...] = (5.0e-4, 1.0e-3, 2.0e-3)
    maximum_d0_fraction: float = 0.01
    late_d0_fraction: float = 0.002
    opposite_d0_fraction: float = 0.5
    final_separation_fraction: float = 0.10
    projection_minimum: float = 0.20
    projection_maximum: float = 0.80
    orthogonal_maximum: float = 0.05
    energy_ratio_maximum: float = 0.01
    phase_mean_error_fraction: float = 0.01
    phase_rms_error_fraction: float = 0.05
    step_ledger_relative: float = 5.0e-11
    cumulative_ledger_relative: float = 5.0e-9
    force_displacement_relative: float = 5.0e-12
    even_response_relative: float = 0.02
    amplitude_collapse_relative: float = 0.02
    signal_fraction: float = 0.25
    coefficient_tolerance: float = 5.0e-13
    center_tolerance_fraction: float = 1.0e-12
    channel_off_d0_fraction: float = 1.0e-10
    covariance_fraction: float = 1.0e-11


THRESHOLDS = P4Thresholds()
EXPECTED_CONSTRUCTION = {
    "q_power_h": 5.9620249581892009e-06,
    "weight_zero": 0.0050000298103025208,
    "beta_real": 0.28847300317511804,
    "beta_imag": -0.45107951349124853,
    "beta_abs": 0.53543384376818492,
    "write_real": 0.0024995710921114429,
    "write_imag": 0.63237517365742668,
    "write_gain": 0.39990460811390499,
    "raw_center_amplitude": 0.50588100737612629,
    "wrong_chirality_amplitude": 1.0117541055435313,
}


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
        raise RuntimeError("P4 target gate requires a clean prospective revision")
    revision = _git_output(["rev-parse", "HEAD"])
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", FREEZE_REVISION, revision],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("published P4 freeze revision is not an ancestor")
    observed = {path: _git_blob(path) for path in EXPECTED_BLOBS}
    if observed != EXPECTED_BLOBS:
        raise RuntimeError("one or more frozen P4 dependencies changed")
    if _sha256(ROOT / P3_RESULT) != EXPECTED_P3_SHA256:
        raise RuntimeError("authoritative P3 JSON hash changed")
    p3 = json.loads((ROOT / P3_RESULT).read_text(encoding="utf-8"))
    if p3.get("decision") != "p3-formation-basin-pass":
        raise RuntimeError("P4 requires the reviewed P3 full pass")
    script_path = Path(__file__).resolve().relative_to(ROOT).as_posix()
    module_path = "src/emergenz_knoten/orbit_center_actuator.py"
    return {
        "clean_pre_run_status": status,
        "revision": revision,
        "freeze_revision": FREEZE_REVISION,
        "freeze_is_ancestor": True,
        "expected_blobs": EXPECTED_BLOBS,
        "observed_blobs": observed,
        "implementation_blobs": {
            script_path: _git_blob(script_path),
            module_path: _git_blob(module_path),
        },
        "p3_decision": p3["decision"],
        "p3_sha256": EXPECTED_P3_SHA256,
    }


def _complex_pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def _relative_error(observed: float, expected: float) -> float:
    return abs(float(observed) - float(expected)) / max(1.0, abs(float(expected)))


def _all_finite(value: Any) -> bool:
    """Return whether a nested numerical record contains only finite values."""

    if is_dataclass(value) and not isinstance(value, type):
        return all(
            _all_finite(getattr(value, field.name)) for field in fields(value)
        )
    if isinstance(value, np.ndarray):
        return bool(np.isfinite(value).all())
    if isinstance(value, dict):
        return all(_all_finite(item) for item in value.values())
    if isinstance(value, (tuple, list)):
        return all(_all_finite(item) for item in value)
    if isinstance(value, (complex, np.complexfloating)):
        number = complex(value)
        return bool(math.isfinite(number.real) and math.isfinite(number.imag))
    if isinstance(value, (float, np.floating)):
        return bool(math.isfinite(float(value)))
    if isinstance(value, (bool, int, np.integer)) or value is None:
        return True
    return False


def _expected_arm_keys() -> set[tuple[int, str, int, float]]:
    return {
        (chirality, direction, offset_sign, offset_fraction)
        for chirality in (1, -1)
        for direction in ("x", "y")
        for offset_sign in (1, -1)
        for offset_fraction in THRESHOLDS.offset_fractions
    }


def _arm_key(arm: dict[str, Any]) -> tuple[int, str, int, float] | None:
    try:
        return (
            int(arm["chirality"]),
            str(arm["direction"]),
            int(arm["offset_sign"]),
            float(arm["offset_fraction"]),
        )
    except (KeyError, TypeError, ValueError):
        return None


def _registered_panel(arms: list[dict[str, Any]]) -> bool:
    keys = [_arm_key(arm) for arm in arms]
    return bool(
        len(keys) == len(_expected_arm_keys())
        and None not in keys
        and set(keys) == _expected_arm_keys()
    )


def _construction_controls() -> dict[str, Any]:
    plus = candidate_orbit_center_readout(CANDIDATE, chirality=1)
    minus = candidate_orbit_center_readout(CANDIDATE, chirality=-1)
    target_plus = target_history(CANDIDATE, chirality=1)
    target_minus = target_history(CANDIDATE, chirality=-1)
    ages = np.arange(CANDIDATE.horizon, dtype=float)
    notch_plus = complex(
        np.dot(plus.coefficients, np.exp(-1j * CANDIDATE.theta * ages))
    )
    values = {
        "q_power_h": (1.0 - CANDIDATE.alpha) ** CANDIDATE.horizon,
        "weight_zero": float(plus.weights[0]),
        "beta_real": plus.beta.real,
        "beta_imag": plus.beta.imag,
        "beta_abs": abs(plus.beta),
        "write_real": plus.coefficients[0].real,
        "write_imag": plus.coefficients[0].imag,
        "write_gain": plus.write_gain,
        "raw_center_amplitude": abs(memory_center(target_plus, readout=plus)),
        "wrong_chirality_amplitude": abs(
            orbit_center(target_plus, readout=minus)
        ),
    }
    static_errors = {
        key: _relative_error(values[key], expected)
        for key, expected in EXPECTED_CONSTRUCTION.items()
    }
    translation = np.asarray([0.37, -0.21])
    phase = rotation_matrix(math.pi / 7.0)
    transformed = target_plus @ phase.T + translation
    translated_center = orbit_center(transformed, readout=plus)
    target_centers = {
        "plus": abs(orbit_center(target_plus, readout=plus)),
        "minus": abs(orbit_center(target_minus, readout=minus)),
        "translated_error": float(
            np.linalg.norm(complex_to_vector(translated_center) - translation)
        ),
    }
    coefficient = {
        "sum_error_plus": abs(complex(np.sum(plus.coefficients)) - 1.0),
        "sum_error_minus": abs(complex(np.sum(minus.coefficients)) - 1.0),
        "notch_error_plus": abs(notch_plus),
        "conjugacy_error": max(
            abs(minus.beta - plus.beta.conjugate()),
            float(
                np.max(
                    np.abs(minus.coefficients - np.conjugate(plus.coefficients))
                )
            ),
        ),
    }

    rng = np.random.default_rng(20260826)
    small = build_orbit_center_readout(
        alpha=0.08,
        horizon=17,
        theta=0.19,
        chirality=1,
    )
    variation = rng.normal(size=(17, 2))
    center_force_vector = np.asarray([0.17, -0.31])
    slot_forces = adjoint_slot_forces(center_force_vector, readout=small)
    center_variation = orbit_center(variation, readout=small)
    virtual_work_error = abs(
        float(np.sum(slot_forces * variation))
        - real_inner(complex(*center_force_vector), center_variation)
    )
    force_sum_error = float(
        np.linalg.norm(np.sum(slot_forces, axis=0) - center_force_vector)
    )

    old = np.column_stack(
        (
            0.1 * np.arange(17) + np.sin(0.37 * np.arange(17)),
            -0.05 * np.arange(17) + np.cos(0.23 * np.arange(17)),
        )
    )
    old_values = old[:, 0] + 1j * old[:, 1]
    new_zero = complex(0.7, -0.4)
    new_values = np.concatenate(([new_zero], old_values[:-1]))
    force = complex(0.3, -0.2)
    write_force = small.coefficients[0].conjugate() * force
    write_work = real_inner(write_force, new_values[0] - old_values[0])
    age_displacement = complex(
        np.dot(small.coefficients[1:], old_values[:-1] - old_values[1:])
    )
    age_work = real_inner(force, age_displacement)
    center_work = real_inner(
        force,
        complex(np.dot(small.coefficients, new_values - old_values)),
    )
    full_work_error = abs(write_work + age_work - center_work)
    truncated_fraction = abs(age_work) / max(
        abs(center_work), abs(write_work) + abs(age_work)
    )

    q0 = np.asarray([1.0e-3 * CANDIDATE.radius, 0.0])
    off = reciprocal_source_write_step(
        target_plus,
        q0,
        candidate=CANDIDATE,
        readout=plus,
        coupling_strength=0.0,
    )
    native = native_fifo_step(target_plus, **CANDIDATE.step_parameters())
    bitwise_off = bool(np.array_equal(off.history, native))

    active = reciprocal_source_write_step(
        target_plus,
        q0,
        candidate=CANDIDATE,
        readout=plus,
        coupling_strength=THRESHOLDS.coupling_strength,
    )
    shift = np.asarray([0.31, -0.27])
    shifted = reciprocal_source_write_step(
        target_plus + shift,
        q0 + shift,
        candidate=CANDIDATE,
        readout=plus,
        coupling_strength=THRESHOLDS.coupling_strength,
    )
    translation_error = max(
        float(np.max(np.abs(shifted.history - active.history - shift))),
        float(np.max(np.abs(shifted.actuator - active.actuator - shift))),
    )
    rotation = rotation_matrix(0.61)
    rotated = reciprocal_source_write_step(
        target_plus @ rotation.T,
        rotation @ q0,
        candidate=CANDIDATE,
        readout=plus,
        coupling_strength=THRESHOLDS.coupling_strength,
    )
    rotation_error = max(
        float(np.max(np.abs(rotated.history - active.history @ rotation.T))),
        float(np.max(np.abs(rotated.actuator - rotation @ active.actuator))),
    )
    reflected_q = q0 * np.asarray([1.0, -1.0])
    reflected = reciprocal_source_write_step(
        target_minus,
        reflected_q,
        candidate=CANDIDATE,
        readout=minus,
        coupling_strength=THRESHOLDS.coupling_strength,
    )
    expected_reflection = active.history.copy()
    expected_reflection[:, 1] *= -1.0
    reflection_error = max(
        float(np.max(np.abs(reflected.history - expected_reflection))),
        float(
            np.max(
                np.abs(
                    reflected.actuator
                    - active.actuator * np.asarray([1.0, -1.0])
                )
            )
        ),
    )
    tolerance = THRESHOLDS.coefficient_tolerance
    center_tolerance = THRESHOLDS.center_tolerance_fraction * CANDIDATE.radius
    covariance_tolerance = THRESHOLDS.covariance_fraction * CANDIDATE.radius
    gates = {
        "frozen_values": bool(max(static_errors.values()) <= tolerance),
        "coefficient_identities": bool(max(coefficient.values()) <= tolerance),
        "target_centers": bool(max(target_centers.values()) <= center_tolerance),
        "raw_center_negative": bool(
            abs(
                values["raw_center_amplitude"]
                - EXPECTED_CONSTRUCTION["raw_center_amplitude"]
            )
            <= tolerance
        ),
        "wrong_chirality_negative": bool(
            values["wrong_chirality_amplitude"] >= 0.5 * CANDIDATE.radius
        ),
        "adjoint_virtual_work": bool(
            virtual_work_error <= tolerance and force_sum_error <= tolerance
        ),
        "full_age_ledger": bool(
            full_work_error <= tolerance and truncated_fraction >= 0.01
        ),
        "channel_off_bitwise": bitwise_off,
        "translation_covariance": bool(
            translation_error <= covariance_tolerance
        ),
        "rotation_covariance": bool(rotation_error <= covariance_tolerance),
        "reflection_covariance": bool(
            reflection_error <= covariance_tolerance
        ),
    }
    return {
        "readouts": {
            "plus": readout_payload(plus),
            "minus": readout_payload(minus),
        },
        "values": values,
        "expected_values": EXPECTED_CONSTRUCTION,
        "static_relative_errors": static_errors,
        "coefficient_controls": coefficient,
        "target_center_controls": target_centers,
        "adjoint_controls": {
            "virtual_work_error": virtual_work_error,
            "force_sum_error": force_sum_error,
        },
        "age_ledger_control": {
            "write_work": write_work,
            "age_work": age_work,
            "center_work": center_work,
            "full_work_error": full_work_error,
            "truncated_ledger_fraction": truncated_fraction,
        },
        "covariance_controls": {
            "translation_error": translation_error,
            "rotation_error": rotation_error,
            "reflection_error": reflection_error,
        },
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _sample_metrics(
    state: np.ndarray,
    actuator: np.ndarray,
    *,
    step: int,
    chirality: int,
    readout: Any,
    targets: dict[int, np.ndarray],
) -> dict[str, Any]:
    own, alignment = rotation_translation_quotient_distance(
        state,
        targets[chirality],
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    opposite, _ = rotation_translation_quotient_distance(
        state,
        targets[-chirality],
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    center = orbit_center(state, readout=readout)
    raw = vector_memory_center(
        state,
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    q_value = complex(float(actuator[0]), float(actuator[1]))
    return {
        "step": int(step),
        "center": _complex_pair(center),
        "actuator": _complex_pair(q_value),
        "separation": abs(center - q_value),
        "expected_d0_fraction": own / CANDIDATE.radius,
        "opposite_d0_fraction": opposite / CANDIDATE.radius,
        "alignment_phase": alignment,
        "raw_memory_center": [float(raw[0]), float(raw[1])],
        "interaction_energy": (
            0.5 * THRESHOLDS.coupling_strength * abs(center - q_value) ** 2
        ),
    }


def _run_channel_off(chirality: int) -> dict[str, Any]:
    readout = candidate_orbit_center_readout(CANDIDATE, chirality=chirality)
    state = target_history(CANDIDATE, chirality=chirality)
    actuator = np.zeros(2)
    targets = {
        1: target_history(CANDIDATE, chirality=1),
        -1: target_history(CANDIDATE, chirality=-1),
    }
    trace = [
        _sample_metrics(
            state,
            actuator,
            step=0,
            chirality=chirality,
            readout=readout,
            targets=targets,
        )
    ]
    bitwise = True
    finite = True
    for step in range(1, THRESHOLDS.active_updates + 1):
        expected = native_fifo_step(state, **CANDIDATE.step_parameters())
        result = reciprocal_source_write_step(
            state,
            actuator,
            candidate=CANDIDATE,
            readout=readout,
            coupling_strength=0.0,
        )
        if not _all_finite(result):
            finite = False
            break
        bitwise = bool(bitwise and np.array_equal(result.history, expected))
        state = result.history
        actuator = result.actuator
        if step % THRESHOLDS.sample_every == 0:
            sample = _sample_metrics(
                state,
                actuator,
                step=step,
                chirality=chirality,
                readout=readout,
                targets=targets,
            )
            if not _all_finite(sample):
                finite = False
                break
            trace.append(sample)
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
        "chirality": chirality,
        "trace": trace,
        "maximum_d0_fraction": maximum_d0,
        "maximum_center_fraction": maximum_center,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _ideal_cayley_reference(
    q_initial: complex,
    *,
    readout: Any,
) -> dict[str, Any]:
    """Return the frozen ideal neutral-translation comparison trace."""

    rate = CANDIDATE.alpha * readout.write_gain * THRESHOLDS.coupling_strength
    factor = (1.0 - rate) / (1.0 + rate)
    midpoint = 0.5 * q_initial
    trace = []
    for step in range(
        0,
        THRESHOLDS.active_updates + 1,
        THRESHOLDS.sample_every,
    ):
        relative = -q_initial * factor**step
        center = midpoint + 0.5 * relative
        actuator = midpoint - 0.5 * relative
        trace.append(
            {
                "step": step,
                "center": _complex_pair(center),
                "actuator": _complex_pair(actuator),
                "separation_ratio": abs(relative) / abs(q_initial),
            }
        )
    return {
        "factor_per_update": factor,
        "trace": trace,
        "final_separation_ratio": trace[-1]["separation_ratio"],
        "final_center_projection_ratio": real_inner(
            q_initial / abs(q_initial),
            complex(*trace[-1]["center"]),
        )
        / abs(q_initial),
        "final_actuator_projection_ratio": real_inner(
            q_initial / abs(q_initial),
            complex(*trace[-1]["actuator"]),
        )
        / abs(q_initial),
    }


def _run_active_arm(
    *,
    chirality: int,
    direction_name: str,
    direction: complex,
    offset_sign: int,
    offset_fraction: float,
) -> dict[str, Any]:
    readout = candidate_orbit_center_readout(CANDIDATE, chirality=chirality)
    state = target_history(CANDIDATE, chirality=chirality)
    delta = offset_fraction * CANDIDATE.radius
    signed_direction = float(offset_sign) * direction
    q_initial = delta * signed_direction
    actuator = complex_to_vector(q_initial)
    ideal_cayley = _ideal_cayley_reference(q_initial, readout=readout)
    targets = {
        1: target_history(CANDIDATE, chirality=1),
        -1: target_history(CANDIDATE, chirality=-1),
    }
    trace = [
        _sample_metrics(
            state,
            actuator,
            step=0,
            chirality=chirality,
            readout=readout,
            targets=targets,
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
        "center_actuation": 0.0,
        "actuator_update": 0.0,
        "coupling_displacement": 0.0,
        "truncated_ledger": 0.0,
        "raw_center_ledger": 0.0,
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
    complete = True
    stop_reason = "completed"
    for step in range(1, THRESHOLDS.active_updates + 1):
        result = reciprocal_source_write_step(
            state,
            actuator,
            candidate=CANDIDATE,
            readout=readout,
            coupling_strength=THRESHOLDS.coupling_strength,
        )
        if not _all_finite(result):
            complete = False
            stop_reason = "nonfinite-transition"
            break
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
        maxima["center_actuation"] = max(
            maxima["center_actuation"], abs(result.center_actuation_residual)
        )
        maxima["actuator_update"] = max(
            maxima["actuator_update"], abs(result.actuator_update_residual)
        )
        maxima["coupling_displacement"] = max(
            maxima["coupling_displacement"],
            abs(result.coupling_displacement_residual),
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
        cumulative["raw_center_ledger"] += (
            result.raw_center_ledger_residual
        )
        cumulative["write_dissipation"] += result.write_mobility_dissipation
        cumulative["external_dissipation"] += (
            result.external_mobility_dissipation
        )
        minimum_dissipation = min(
            minimum_dissipation,
            result.write_mobility_dissipation,
            result.external_mobility_dissipation,
        )
        state = result.history
        actuator = result.actuator
        if not np.isfinite(state).all() or not np.isfinite(actuator).all():
            complete = False
            stop_reason = "nonfinite-state"
            break
        if step % THRESHOLDS.sample_every == 0:
            sample = _sample_metrics(
                state,
                actuator,
                step=step,
                chirality=chirality,
                readout=readout,
                targets=targets,
            )
            if not _all_finite(sample):
                complete = False
                stop_reason = "nonfinite-sample"
                break
            trace.append(sample)
    if initial_force_scale is None or initial_displacement_scale is None:
        initial_force_scale = 0.0
        initial_displacement_scale = 0.0
    final = trace[-1]
    final_center = complex(*final["center"])
    final_actuator = complex(*final["actuator"])
    final_separation_ratio = abs(final_center - final_actuator) / delta
    center_projection = real_inner(signed_direction, final_center) / delta
    actuator_projection = real_inner(signed_direction, final_actuator) / delta
    center_orthogonal = abs(real_inner(1j * signed_direction, final_center)) / delta
    actuator_orthogonal = abs(
        real_inner(1j * signed_direction, final_actuator)
    ) / delta
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
        abs(complex(*row["center"])) for row in trace
    ) / delta
    ideal_trace = ideal_cayley["trace"]
    if len(trace) == len(ideal_trace):
        actual_centers = np.asarray(
            [complex(*row["center"]) for row in trace]
        )
        actual_actuators = np.asarray(
            [complex(*row["actuator"]) for row in trace]
        )
        ideal_centers = np.asarray(
            [complex(*row["center"]) for row in ideal_trace]
        )
        ideal_actuators = np.asarray(
            [complex(*row["actuator"]) for row in ideal_trace]
        )
        ideal_comparison = {
            "center_relative_rms": _rms(actual_centers - ideal_centers)
            / delta,
            "actuator_relative_rms": _rms(
                actual_actuators - ideal_actuators
            )
            / delta,
        }
    else:
        ideal_comparison = {
            "center_relative_rms": None,
            "actuator_relative_rms": None,
        }
    force_scale = max(initial_force_scale, np.finfo(float).tiny)
    displacement_scale = max(initial_displacement_scale, np.finfo(float).tiny)
    finite_dissipation = math.isfinite(minimum_dissipation)
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
            <= THRESHOLDS.force_displacement_relative
        ),
        "midpoint_force": bool(
            maxima["midpoint"] / force_scale
            <= THRESHOLDS.force_displacement_relative
        ),
        "center_actuation": bool(
            maxima["center_actuation"] / displacement_scale
            <= THRESHOLDS.force_displacement_relative
        ),
        "actuator_update": bool(
            maxima["actuator_update"] / displacement_scale
            <= THRESHOLDS.force_displacement_relative
        ),
        "coupling_displacement": bool(
            maxima["coupling_displacement"] / displacement_scale
            <= THRESHOLDS.force_displacement_relative
        ),
        "nonnegative_mobility": bool(
            finite_dissipation and minimum_dissipation >= -1.0e-30
        ),
    }
    dynamic_gates = {
        "complete": bool(
            complete and trace[-1]["step"] == THRESHOLDS.active_updates
        ),
        "maximum_d0": bool(
            max(row["expected_d0_fraction"] for row in trace)
            <= THRESHOLDS.maximum_d0_fraction
        ),
        "late_d0": bool(
            late_maximum_d0 is not None
            and late_maximum_d0 <= THRESHOLDS.late_d0_fraction
        ),
        "opposite_separation": bool(
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
        "center_orthogonal": bool(
            center_orthogonal <= THRESHOLDS.orthogonal_maximum
        ),
        "actuator_orthogonal": bool(
            actuator_orthogonal <= THRESHOLDS.orthogonal_maximum
        ),
        "interaction_energy": bool(
            energy_ratio <= THRESHOLDS.energy_ratio_maximum
        ),
        "phase": bool(phase["pass"]),
        "informative_signal": bool(
            maximum_center_response >= THRESHOLDS.signal_fraction
        ),
    }
    name = (
        f"s{'plus' if chirality == 1 else 'minus'}_{direction_name}_"
        f"offset{'plus' if offset_sign == 1 else 'minus'}_"
        f"d{offset_fraction:.4f}"
    )
    return {
        "name": name,
        "chirality": chirality,
        "direction": direction_name,
        "offset_sign": offset_sign,
        "offset_fraction": offset_fraction,
        "offset": delta,
        "initial_actuator": _complex_pair(q_initial),
        "complete": complete,
        "stop_reason": stop_reason,
        "trace": trace,
        "maximum_d0_fraction": max(
            row["expected_d0_fraction"] for row in trace
        ),
        "late_maximum_d0_fraction": late_maximum_d0,
        "late_opposite_minimum_fraction": late_opposite_minimum,
        "final_separation_ratio": final_separation_ratio,
        "center_projection_ratio": center_projection,
        "actuator_projection_ratio": actuator_projection,
        "center_orthogonal_ratio": center_orthogonal,
        "actuator_orthogonal_ratio": actuator_orthogonal,
        "energy_ratio": energy_ratio,
        "maximum_center_response_ratio": maximum_center_response,
        "phase": phase,
        "residual_maxima": maxima,
        "residual_scales": {
            "initial_energy": initial_energy,
            "initial_force": initial_force_scale,
            "initial_coupling_displacement": initial_displacement_scale,
        },
        "cumulative_ledger": cumulative,
        "nondecisional_rivals": {
            "ideal_cayley": {
                **ideal_cayley,
                "comparison_to_nonlinear": ideal_comparison,
            },
            "truncated_age_ledger": {
                "maximum_residual": maxima["truncated_ledger"],
                "cumulative_residual": cumulative["truncated_ledger"],
            },
            "raw_memory_center_ledger": {
                "maximum_residual": maxima["raw_center_ledger"],
                "cumulative_residual": cumulative["raw_center_ledger"],
                "cumulative_center_work": cumulative["raw_center_work"],
            },
        },
        "minimum_mobility_dissipation": (
            minimum_dissipation if finite_dissipation else None
        ),
        "ledger_gates": ledger_gates,
        "dynamic_gates": dynamic_gates,
        "ledger_pass": bool(all(ledger_gates.values())),
        "dynamic_pass": bool(all(dynamic_gates.values())),
    }


def _trace_complex(arm: dict[str, Any], key: str) -> np.ndarray:
    return np.asarray([complex(*row[key]) for row in arm["trace"]])


def _rms(values: np.ndarray) -> float:
    return float(math.sqrt(np.mean(np.abs(values) ** 2)))


def _response_controls(
    arms: list[dict[str, Any]],
    channel_off: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    unavailable = {
        "available": False,
        "reason": "incomplete-or-misregistered-traces",
        "even_response": [],
        "amplitude_collapse": [],
        "mirror_equivariance": [],
        "gates": {
            "even_response": False,
            "amplitude_collapse": False,
            "mirror_equivariance": False,
        },
        "pass": False,
    }
    if not _registered_panel(arms) or set(channel_off) != {1, -1}:
        return unavailable
    indexed = {
        _arm_key(row): row
        for row in arms
    }
    expected_steps = list(
        range(
            0,
            THRESHOLDS.active_updates + 1,
            THRESHOLDS.sample_every,
        )
    )
    all_traces = [row["trace"] for row in arms] + [
        control["trace"] for control in channel_off.values()
    ]
    if any(
        [sample["step"] for sample in trace] != expected_steps
        or not _all_finite(trace)
        for trace in all_traces
    ):
        return unavailable
    baselines = {
        chirality: _trace_complex(control, "center")
        for chirality, control in channel_off.items()
    }
    even_rows = []
    for chirality in (1, -1):
        for direction in ("x", "y"):
            for fraction in THRESHOLDS.offset_fractions:
                plus = _trace_complex(
                    indexed[(chirality, direction, 1, fraction)], "center"
                )
                minus = _trace_complex(
                    indexed[(chirality, direction, -1, fraction)], "center"
                )
                odd = 0.5 * (plus - minus)
                even = 0.5 * (plus + minus) - baselines[chirality]
                ratio = _rms(even) / max(_rms(odd), np.finfo(float).tiny)
                even_rows.append(
                    {
                        "chirality": chirality,
                        "direction": direction,
                        "offset_fraction": fraction,
                        "even_to_odd_rms": ratio,
                        "pass": bool(
                            ratio <= THRESHOLDS.even_response_relative
                        ),
                    }
                )
    collapse_rows = []
    reference_fraction = 1.0e-3
    for chirality in (1, -1):
        for direction in ("x", "y"):
            for offset_sign in (1, -1):
                reference_arm = indexed[
                    (chirality, direction, offset_sign, reference_fraction)
                ]
                reference = (
                    _trace_complex(reference_arm, "center")
                    - baselines[chirality]
                ) / (offset_sign * reference_arm["offset"])
                errors = []
                for fraction in THRESHOLDS.offset_fractions:
                    arm = indexed[(chirality, direction, offset_sign, fraction)]
                    normalized = (
                        _trace_complex(arm, "center") - baselines[chirality]
                    ) / (offset_sign * arm["offset"])
                    errors.append(
                        _rms(normalized - reference)
                        / max(_rms(reference), np.finfo(float).tiny)
                    )
                collapse_rows.append(
                    {
                        "chirality": chirality,
                        "direction": direction,
                        "offset_sign": offset_sign,
                        "maximum_relative_rms": max(errors),
                        "pass": bool(
                            max(errors)
                            <= THRESHOLDS.amplitude_collapse_relative
                        ),
                    }
                )
    mirror_rows = []
    for direction in ("x", "y"):
        for plus_sign in (1, -1):
            minus_sign = plus_sign if direction == "x" else -plus_sign
            for fraction in THRESHOLDS.offset_fractions:
                plus = indexed[(1, direction, plus_sign, fraction)]
                minus = indexed[(-1, direction, minus_sign, fraction)]
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
                        "direction": direction,
                        "plus_offset_sign": plus_sign,
                        "minus_offset_sign": minus_sign,
                        "offset_fraction": fraction,
                        "center_error_fraction": center_error,
                        "actuator_error_fraction": actuator_error,
                        "pass": bool(
                            max(center_error, actuator_error)
                            <= THRESHOLDS.covariance_fraction
                        ),
                    }
                )
    gates = {
        "even_response": bool(all(row["pass"] for row in even_rows)),
        "amplitude_collapse": bool(
            all(row["pass"] for row in collapse_rows)
        ),
        "mirror_equivariance": bool(
            all(row["pass"] for row in mirror_rows)
        ),
    }
    return {
        "available": True,
        "reason": None,
        "even_response": even_rows,
        "amplitude_collapse": collapse_rows,
        "mirror_equivariance": mirror_rows,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _decision(
    *,
    pipeline: bool,
    arms: list[dict[str, Any]],
    response: dict[str, Any],
) -> tuple[str, dict[str, bool]]:
    registration = _registered_panel(arms)
    complete = bool(registration and all(row["complete"] for row in arms))
    informative = bool(
        registration
        and all(row["dynamic_gates"]["informative_signal"] for row in arms)
    )
    ledger = bool(registration and all(row["ledger_pass"] for row in arms))
    dynamic = bool(
        registration
        and all(row["dynamic_pass"] for row in arms)
        and response["pass"]
    )
    response_available = bool(response.get("available", True))
    if (
        not pipeline
        or not registration
        or not complete
        or not informative
        or not response_available
    ):
        decision = "p4-inconclusive"
    elif not ledger:
        decision = "p4-source-write-architecture-fail"
    elif dynamic:
        decision = "p4-source-write-mechanics-pass"
    else:
        decision = "p4-source-write-ledger-only"
    return decision, {
        "pipeline": pipeline,
        "registration": registration,
        "complete": complete,
        "informative_signal": informative,
        "response_available": response_available,
        "reciprocal_ledger": ledger,
        "nonlinear_loop_mechanics": dynamic,
    }


def run_gate() -> dict[str, Any]:
    """Execute the frozen P4 target calculation."""

    started = time.perf_counter()
    provenance = _verify_provenance()
    construction = _construction_controls()
    channel_off = {
        chirality: _run_channel_off(chirality) for chirality in (1, -1)
    }
    arms = []
    for chirality in (1, -1):
        for direction_name, direction in (("x", 1.0 + 0.0j), ("y", 0.0 + 1.0j)):
            for offset_sign in (1, -1):
                for offset_fraction in THRESHOLDS.offset_fractions:
                    arms.append(
                        _run_active_arm(
                            chirality=chirality,
                            direction_name=direction_name,
                            direction=direction,
                            offset_sign=offset_sign,
                            offset_fraction=offset_fraction,
                        )
                    )
    response = _response_controls(arms, channel_off)
    channel_off_pass = bool(all(row["pass"] for row in channel_off.values()))
    pipeline = bool(construction["pass"] and channel_off_pass)
    decision, gates = _decision(
        pipeline=pipeline,
        arms=arms,
        response=response,
    )
    return {
        "schema_version": 1,
        "gate": "P4 reciprocal orbit-center source/write mechanics",
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
            "no_target_fit": True,
            "no_mass_or_second_difference": True,
        },
        "construction_controls": construction,
        "channel_off_controls": {
            str(chirality): row for chirality, row in channel_off.items()
        },
        "active_arms": arms,
        "response_controls": response,
        "gates": gates,
        "decision": decision,
        "claim_boundary": {
            "established_if_full_pass": (
                "an explicit first-order reciprocal source/write actuator, "
                "exact finite-H age ledger and weak nonlinear L3 orbit-center "
                "response for the registered panel"
            ),
            "not_established": (
                "material center of mass, unique microscopic ontology, "
                "conserved total momentum, physical mass, SI calibration, "
                "noise robustness, internal S1 or two-loop interaction"
            ),
        },
    }


def _format(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.6g}"


def _maximum(rows: list[dict[str, Any]], key: str) -> float | None:
    values = [row[key] for row in rows if row.get(key) is not None]
    return max(values) if values else None


def _claim_boundary_lines(payload: dict[str, Any]) -> list[str]:
    claim = payload["claim_boundary"]["established_if_full_pass"]
    if payload["decision"] == "p4-source-write-mechanics-pass":
        return ["Established by this full pass: " + claim + "."]
    return [
        "Conditional full-pass boundary not activated.",
        "A full pass would have established only: " + claim + ".",
    ]


def render_report(payload: dict[str, Any], *, summary_sha256: str) -> str:
    """Render a compact human-readable record of the frozen decision."""

    construction = payload["construction_controls"]
    lines = [
        "# P4 reciprocal orbit-center source/write mechanics",
        "",
        f"Date: {payload['generated_at_utc'][:10]}.",
        "",
        f"Decision: **`{payload['decision']}`**.",
        "",
        "The gate uses an exact linear orbit-center notch and adjoint port on",
        "the full nonlinear native L3 FIFO map. No mass, momentum state or",
        "second-order equation is inserted.",
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
            "## Static architecture controls",
            "",
            "| control | maximum/observed | status |",
            "| --- | ---: | :---: |",
            (
                "| coefficient identities | "
                f"{_format(max(construction['coefficient_controls'].values()))} | "
                f"{'pass' if construction['gates']['coefficient_identities'] else 'fail'} |"
            ),
            (
                "| target-center error | "
                f"{_format(max(construction['target_center_controls'].values()))} | "
                f"{'pass' if construction['gates']['target_centers'] else 'fail'} |"
            ),
            (
                "| adjoint virtual-work error | "
                f"{_format(construction['adjoint_controls']['virtual_work_error'])} | "
                f"{'pass' if construction['gates']['adjoint_virtual_work'] else 'fail'} |"
            ),
            (
                "| truncated-ledger omitted fraction | "
                f"{_format(construction['age_ledger_control']['truncated_ledger_fraction'])} | "
                f"{'pass' if construction['gates']['full_age_ledger'] else 'fail'} |"
            ),
            "",
            "## Active arms",
            "",
            (
                "| arm | dynamic | ledger | max D0/R | final separation/delta | "
                "C projection | Q projection | energy ratio | max ledger/U0 |"
            ),
            "| --- | :---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for arm in payload["active_arms"]:
        ledger_relative = (
            arm["residual_maxima"]["ledger"]
            / arm["residual_scales"]["initial_energy"]
        )
        lines.append(
            "| "
            f"`{arm['name']}` | "
            f"{'pass' if arm['dynamic_pass'] else 'fail'} | "
            f"{'pass' if arm['ledger_pass'] else 'fail'} | "
            f"{_format(arm['maximum_d0_fraction'])} | "
            f"{_format(arm['final_separation_ratio'])} | "
            f"{_format(arm['center_projection_ratio'])} | "
            f"{_format(arm['actuator_projection_ratio'])} | "
            f"{_format(arm['energy_ratio'])} | "
            f"{_format(ledger_relative)} |"
        )
    response = payload["response_controls"]
    even_maximum = _maximum(response["even_response"], "even_to_odd_rms")
    collapse_maximum = _maximum(
        response["amplitude_collapse"],
        "maximum_relative_rms",
    )
    mirror_maximum = max(
        (
            max(row["center_error_fraction"], row["actuator_error_fraction"])
            for row in response["mirror_equivariance"]
        ),
        default=None,
    )
    ideal_factor = payload["active_arms"][0]["nondecisional_rivals"][
        "ideal_cayley"
    ]["factor_per_update"]
    ideal_final = payload["active_arms"][0]["nondecisional_rivals"][
        "ideal_cayley"
    ]["final_separation_ratio"]
    raw_maximum = max(
        arm["nondecisional_rivals"]["raw_memory_center_ledger"][
            "maximum_residual"
        ]
        / arm["residual_scales"]["initial_energy"]
        for arm in payload["active_arms"]
    )
    truncated_maximum = max(
        arm["nondecisional_rivals"]["truncated_age_ledger"][
            "maximum_residual"
        ]
        / arm["residual_scales"]["initial_energy"]
        for arm in payload["active_arms"]
    )
    lines.extend(
        [
            "",
            "## Response and symmetry controls",
            "",
            f"- Response panel available: `{response['available']}`.",
            (
                "- Maximum even/odd response ratio: "
                f"`{_format(even_maximum)}`."
            ),
            (
                "- Maximum normalized amplitude-collapse error: "
                f"`{_format(collapse_maximum)}`."
            ),
            (
                "- Maximum mirror center/actuator error fraction: "
                f"`{_format(mirror_maximum)}`."
            ),
            "",
            "## Non-decisional rivals",
            "",
            f"- Ideal Cayley factor per update: `{_format(ideal_factor)}`; "
            f"final separation ratio: `{_format(ideal_final)}`.",
            "- Maximum raw-memory-center ledger residual / initial "
            f"interaction energy: `{_format(raw_maximum)}`.",
            "- Maximum age-truncated ledger residual / initial interaction "
            f"energy: `{_format(truncated_maximum)}`.",
            "- These comparisons are recorded but are not used by any gate.",
            "",
            "## Interpretation boundary",
            "",
            *_claim_boundary_lines(payload),
            "",
            "Not established: " + payload["claim_boundary"]["not_established"] + ".",
            "",
            "## Provenance",
            "",
            f"- Freeze revision: `{payload['provenance']['freeze_revision']}`.",
            f"- Execution revision: `{payload['provenance']['revision']}`.",
            f"- Runtime: `{payload['runtime']['python']}` / NumPy "
            f"`{payload['runtime']['numpy']}` / SciPy `{payload['runtime']['scipy']}`.",
            f"- Machine-readable JSON SHA-256: `{summary_sha256}`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()
    payload = run_gate()
    summary_path = ROOT / args.summary
    report_path = ROOT / args.report
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    summary_path.write_text(serialized, encoding="utf-8")
    summary_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    report_path.write_text(
        render_report(payload, summary_sha256=summary_hash),
        encoding="utf-8",
    )
    print(json.dumps({"decision": payload["decision"], "json_sha256": summary_hash}))


if __name__ == "__main__":
    main()
