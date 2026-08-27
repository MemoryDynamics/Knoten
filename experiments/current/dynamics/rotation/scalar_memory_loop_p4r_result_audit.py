"""Independently recompute the frozen P4-R decision from raw result JSON."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
SOURCE = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4r_phase_metrology_2026-08-26.json"
)
SOURCE_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4r_phase_metrology_2026-08-26.md"
)
DEFAULT_OUTPUT = Path(
    "reports/project/meta/reviews/"
    "p4r_independent_result_recompute_2026-08-27.json"
)
EXPECTED_SOURCE_SHA256 = (
    "807cf915d1602d87a779e7bf587387559b1b19d7de60dc43c6e1e220b73682c8"
)
EXPECTED_CANDIDATE_ID = (
    "k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1"
)
EXPECTED_EXECUTION_REVISION = "59dc8875cf991e3d7472db1496c9ae8ffae16ca8"
EXPECTED_RESULT_DECISION = "p4r-phase-averaged-chiral-response-pass"
EXPECTED_P4_DECISION = "p4-source-write-architecture-fail"
ABSOLUTE_RECOMPUTE_TOLERANCE = 5.0e-13
RELATIVE_RECOMPUTE_TOLERANCE = 5.0e-12
LEDGER_RECOMBINATION_RELATIVE_TOLERANCE = 2.0e-11


@dataclass(frozen=True)
class AuditThresholds:
    """Independent transcription of the frozen P4-R thresholds."""

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


THRESHOLDS = AuditThresholds()
PHASES = tuple((2 * index + 1) * math.pi / 8.0 for index in range(8))


def canonical_lf_sha256(path: Path) -> str:
    """Hash UTF-8/byte content after canonical line-ending conversion."""

    content = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(content).hexdigest()


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


def _active_key(arm: dict[str, Any]) -> tuple[int, int, int]:
    return (
        int(arm["phase_index"]),
        int(arm["chirality"]),
        int(arm["offset_sign"]),
    )


def _channel_off_key(arm: dict[str, Any]) -> tuple[int, int]:
    return int(arm["phase_index"]), int(arm["chirality"])


def _expected_steps() -> list[int]:
    return list(
        range(
            0,
            THRESHOLDS.active_updates + 1,
            THRESHOLDS.sample_every,
        )
    )


def _pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def _trace(arm: dict[str, Any], component: str) -> list[complex]:
    return [complex(*row[component]) for row in arm["trace"]]


def _finite(value: Any) -> bool:
    if isinstance(value, dict):
        return all(_finite(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return all(_finite(item) for item in value)
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return True
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    return False


def _rms(values: list[complex]) -> float:
    return math.sqrt(
        math.fsum(abs(value) ** 2 for value in values) / len(values)
    )


def _close(left: float, right: float) -> bool:
    return math.isclose(
        float(left),
        float(right),
        rel_tol=RELATIVE_RECOMPUTE_TOLERANCE,
        abs_tol=ABSOLUTE_RECOMPUTE_TOLERANCE,
    )


def _compare_tree(
    label: str,
    observed: Any,
    expected: Any,
    differences: list[str],
) -> None:
    if isinstance(expected, bool) or expected is None or isinstance(expected, str):
        if observed != expected:
            differences.append(f"{label}: {observed!r} != {expected!r}")
        return
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        if not isinstance(observed, (int, float)) or not _close(observed, expected):
            differences.append(f"{label}: {observed!r} != {expected!r}")
        return
    if isinstance(expected, dict):
        if not isinstance(observed, dict) or set(observed) != set(expected):
            differences.append(f"{label}: mapping keys differ")
            return
        for key in expected:
            _compare_tree(
                f"{label}.{key}",
                observed[key],
                expected[key],
                differences,
            )
        return
    if isinstance(expected, list):
        if not isinstance(observed, list) or len(observed) != len(expected):
            differences.append(f"{label}: sequence shape differs")
            return
        for index, (left, right) in enumerate(zip(observed, expected, strict=True)):
            _compare_tree(f"{label}[{index}]", left, right, differences)
        return
    if observed != expected:
        differences.append(f"{label}: unsupported values differ")


def _unwrap(angles: list[float]) -> list[float]:
    unwrapped = [angles[0]]
    offset = 0.0
    for previous, current in zip(angles, angles[1:], strict=False):
        difference = current - previous
        adjusted = (difference + math.pi) % (2.0 * math.pi) - math.pi
        if adjusted == -math.pi and difference > 0.0:
            adjusted = math.pi
        offset += adjusted - difference
        unwrapped.append(current + offset)
    return unwrapped


def _phase_metrics(
    trace: list[dict[str, Any]],
    *,
    chirality: int,
    theta: float,
) -> dict[str, float | int | bool]:
    rows = [row for row in trace if row["step"] >= THRESHOLDS.phase_start]
    steps = [float(row["step"]) for row in rows]
    angles = _unwrap([float(row["alignment_phase"]) for row in rows])
    increments = [
        -(right_angle - left_angle) / (right_step - left_step)
        for left_angle, right_angle, left_step, right_step in zip(
            angles,
            angles[1:],
            steps,
            steps[1:],
            strict=False,
        )
    ]
    expected = chirality * theta
    mean = math.fsum(increments) / len(increments)
    mean_error = abs(mean - expected)
    rms_error = math.sqrt(
        math.fsum((value - expected) ** 2 for value in increments)
        / len(increments)
    )
    expected_count = (
        (THRESHOLDS.active_updates - THRESHOLDS.phase_start)
        // THRESHOLDS.sample_every
        + 1
    )
    return {
        "sample_count": len(rows),
        "expected_sample_count": expected_count,
        "mean_increment": mean,
        "expected_increment": expected,
        "mean_absolute_error": mean_error,
        "mean_error_threshold": THRESHOLDS.phase_mean_error_fraction * theta,
        "rms_error": rms_error,
        "rms_error_threshold": THRESHOLDS.phase_rms_error_fraction * theta,
        "pass": bool(
            len(rows) == expected_count
            and mean_error <= THRESHOLDS.phase_mean_error_fraction * theta
            and rms_error <= THRESHOLDS.phase_rms_error_fraction * theta
        ),
    }


def _registration(
    active_arms: list[dict[str, Any]],
    channel_off_arms: list[dict[str, Any]],
) -> bool:
    return bool(
        [_active_key(arm) for arm in active_arms]
        == _expected_active_keys()
        and [_channel_off_key(arm) for arm in channel_off_arms]
        == _expected_channel_off_keys()
    )


def _channel_off_audit(
    arms: list[dict[str, Any]],
    *,
    radius: float,
) -> tuple[bool, dict[str, float | int | bool], list[str]]:
    differences: list[str] = []
    maximum_d0 = 0.0
    maximum_center = 0.0
    expected_steps = _expected_steps()
    all_pass = True
    for arm in arms:
        trace = arm["trace"]
        complete = [row["step"] for row in trace] == expected_steps
        finite = _finite(trace)
        observed_d0 = max(float(row["expected_d0_fraction"]) for row in trace)
        observed_center = max(abs(value) / radius for value in _trace(arm, "center"))
        maximum_d0 = max(maximum_d0, observed_d0)
        maximum_center = max(maximum_center, observed_center)
        gates = {
            "complete": complete,
            "finite": finite,
            "bitwise_native": bool(arm["gates"]["bitwise_native"]),
            "prepared_orbit": bool(
                observed_d0 <= THRESHOLDS.channel_off_d0_fraction
            ),
            "stationary_orbit_center": bool(
                observed_center <= THRESHOLDS.channel_off_d0_fraction
            ),
        }
        _compare_tree(
            f"channel_off[{arm['name']}].gates",
            gates,
            arm["gates"],
            differences,
        )
        if not _close(observed_d0, arm["maximum_d0_fraction"]):
            differences.append(f"channel_off[{arm['name']}].maximum_d0")
        if not _close(observed_center, arm["maximum_center_fraction"]):
            differences.append(f"channel_off[{arm['name']}].maximum_center")
        all_pass = bool(all_pass and all(gates.values()) and arm["pass"])
    return all_pass, {
        "arm_count": len(arms),
        "maximum_d0_fraction": maximum_d0,
        "maximum_center_fraction": maximum_center,
        "bitwise_native_evidence_source": "stored per-arm gate; histories unavailable",
    }, differences


def _reference_consistency(arm: dict[str, Any]) -> tuple[bool, float]:
    references = arm["high_precision_references"]
    if [row["update"] for row in references] != list(THRESHOLDS.reference_steps):
        return False, math.inf
    maximum_relative_difference = 0.0
    valid = True
    with localcontext() as context:
        context.prec = 100
        for row in references:
            for prefix in ("center", "coupling"):
                real = Decimal(row[f"{prefix}_residual"][0])
                imag = Decimal(row[f"{prefix}_residual"][1])
                reconstructed = (real * real + imag * imag).sqrt()
                stored = Decimal(str(row[f"{prefix}_absolute"]))
                scale = max(abs(stored), Decimal("1e-300"))
                relative = float(abs(reconstructed - stored) / scale)
                maximum_relative_difference = max(
                    maximum_relative_difference,
                    relative,
                )
                valid = bool(valid and relative <= 5.0e-15)
            gates = {
                "center_inside_full_envelope": bool(
                    row["center_absolute"] <= row["center_full_envelope"]
                ),
                "coupling_inside_full_envelope": bool(
                    row["coupling_absolute"] <= row["coupling_full_envelope"]
                ),
                "center_binary64_distance": bool(
                    row["center_binary64_distance"]
                    <= row["center_eval_envelope"]
                ),
                "coupling_binary64_distance": bool(
                    row["coupling_binary64_distance"]
                    <= row["coupling_eval_envelope"]
                ),
            }
            valid = bool(
                valid
                and gates == row["gates"]
                and row["pass"] == all(gates.values())
                and row["precision_dps"] == THRESHOLDS.reference_dps
            )
    return valid, maximum_relative_difference


def _ledger_audit(
    arm: dict[str, Any],
) -> tuple[dict[str, bool], dict[str, float], bool, list[str]]:
    differences: list[str] = []
    maxima = arm["residual_maxima"]
    margins = arm["minimum_envelope_margins"]
    cumulative = arm["cumulative_work"]
    scales = arm["residual_scales"]
    initial_energy = float(scales["initial_energy"])
    force_scale = float(scales["initial_force"])
    displacement_scale = float(scales["initial_coupling_displacement"])
    reference_pass, reference_relative_difference = _reference_consistency(arm)
    gates = {
        "work_split_step": bool(
            abs(maxima["work_split"]) / initial_energy
            <= THRESHOLDS.step_ledger_relative
        ),
        "total_ledger_step": bool(
            abs(maxima["ledger"]) / initial_energy
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
            abs(maxima["force_balance"]) / force_scale
            <= THRESHOLDS.force_relative
        ),
        "midpoint_force": bool(
            abs(maxima["midpoint"]) / force_scale
            <= THRESHOLDS.force_relative
        ),
        "center_local": bool(
            abs(maxima["center_local"]) / displacement_scale
            <= THRESHOLDS.local_displacement_relative
        ),
        "coupling_local": bool(
            abs(maxima["coupling_local"]) / displacement_scale
            <= THRESHOLDS.local_displacement_relative
        ),
        "center_full_envelope": bool(
            maxima["center_envelope_ratio"] <= 1.0
            and margins["center_full"] >= 0.0
        ),
        "coupling_full_envelope": bool(
            maxima["coupling_envelope_ratio"] <= 1.0
            and margins["coupling_full"] >= 0.0
        ),
        "actuator_update_relative": bool(
            abs(maxima["actuator_full"]) / displacement_scale
            <= THRESHOLDS.actuator_displacement_relative
        ),
        "actuator_update_envelope": bool(
            maxima["actuator_envelope_ratio"] <= 1.0
            and margins["actuator_full"] >= 0.0
        ),
        "high_precision_reference": reference_pass,
        "nonnegative_mobility": bool(
            math.isfinite(arm["minimum_mobility_dissipation"])
            and arm["minimum_mobility_dissipation"] >= -1.0e-30
        ),
    }
    _compare_tree(
        f"active[{arm['name']}].ledger_gates",
        gates,
        arm["ledger_gates"],
        differences,
    )
    final_energy = float(arm["trace"][-1]["interaction_energy"])
    split_rebuilt = math.fsum(
        (
            cumulative["write_work"],
            cumulative["age_work"],
            -cumulative["center_work"],
        )
    )
    ledger_rebuilt = math.fsum(
        (
            final_energy,
            -initial_energy,
            cumulative["write_work"],
            cumulative["age_work"],
            cumulative["external_work"],
        )
    )
    truncated_rebuilt = math.fsum(
        (
            final_energy,
            -initial_energy,
            cumulative["write_work"],
            cumulative["external_work"],
        )
    )
    raw_rebuilt = math.fsum(
        (
            final_energy,
            -initial_energy,
            cumulative["raw_center_work"],
            cumulative["external_work"],
        )
    )
    recombination = {
        "work_split_relative_difference": abs(
            split_rebuilt - cumulative["work_split"]
        )
        / initial_energy,
        "total_ledger_relative_difference": abs(
            ledger_rebuilt - cumulative["ledger"]
        )
        / initial_energy,
        "truncated_ledger_relative_difference": abs(
            truncated_rebuilt - cumulative["truncated_ledger"]
        )
        / initial_energy,
        "raw_center_ledger_relative_difference": abs(
            raw_rebuilt - cumulative["raw_center_ledger"]
        )
        / initial_energy,
        "reference_absolute_reconstruction_relative_difference": (
            reference_relative_difference
        ),
    }
    recombination_pass = bool(
        max(recombination.values())
        <= LEDGER_RECOMBINATION_RELATIVE_TOLERANCE
    )
    if not recombination_pass:
        differences.append(f"active[{arm['name']}].ledger_recombination")
    return gates, recombination, recombination_pass, differences


def _dynamic_audit(
    arm: dict[str, Any],
    baseline: dict[str, Any],
    *,
    radius: float,
    theta: float,
) -> tuple[dict[str, bool], dict[str, float | None], list[str]]:
    differences: list[str] = []
    trace = arm["trace"]
    delta = THRESHOLDS.offset_fraction * radius
    late = [row for row in trace if row["step"] >= THRESHOLDS.late_start]
    maximum_d0 = max(float(row["expected_d0_fraction"]) for row in trace)
    late_d0 = max(float(row["expected_d0_fraction"]) for row in late)
    opposite = min(float(row["opposite_d0_fraction"]) for row in late)
    final_center = complex(*trace[-1]["center"])
    final_actuator = complex(*trace[-1]["actuator"])
    separation = abs(final_center - final_actuator) / delta
    center_response = [
        value - control
        for value, control in zip(
            _trace(arm, "center"),
            _trace(baseline, "center"),
            strict=True,
        )
    ]
    actuator_response = [
        value - control
        for value, control in zip(
            _trace(arm, "actuator"),
            _trace(baseline, "actuator"),
            strict=True,
        )
    ]
    offset_sign = int(arm["offset_sign"])
    center_projection = offset_sign * center_response[-1].real / delta
    actuator_projection = offset_sign * actuator_response[-1].real / delta
    energy_ratio = trace[-1]["interaction_energy"] / arm["residual_scales"][
        "initial_energy"
    ]
    signal = max(abs(value) for value in center_response) / delta
    phase = _phase_metrics(
        trace,
        chirality=int(arm["chirality"]),
        theta=theta,
    )
    gates = {
        "maximum_d0": bool(maximum_d0 <= THRESHOLDS.maximum_d0_fraction),
        "late_d0": bool(late_d0 <= THRESHOLDS.late_d0_fraction),
        "opposite_chirality": bool(opposite >= THRESHOLDS.opposite_d0_fraction),
        "final_separation": bool(
            separation <= THRESHOLDS.final_separation_fraction
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
        "informative_signal": bool(signal >= THRESHOLDS.signal_fraction),
    }
    metrics: dict[str, float | None] = {
        "maximum_d0_fraction": maximum_d0,
        "late_maximum_d0_fraction": late_d0,
        "late_opposite_minimum_fraction": opposite,
        "final_separation_ratio": separation,
        "center_projection_ratio": center_projection,
        "actuator_projection_ratio": actuator_projection,
        "energy_ratio": energy_ratio,
        "maximum_center_response_ratio": signal,
    }
    _compare_tree(
        f"active[{arm['name']}].dynamic_gates",
        gates,
        arm["dynamic_gates"],
        differences,
    )
    for key, value in metrics.items():
        if not _close(value, arm[key]):
            differences.append(f"active[{arm['name']}].{key}")
    _compare_tree(
        f"active[{arm['name']}].phase_metrics",
        phase,
        arm["phase_metrics"],
        differences,
    )
    return gates, metrics, differences


def _response_audit(
    active_arms: list[dict[str, Any]],
    channel_off_arms: list[dict[str, Any]],
    *,
    radius: float,
) -> dict[str, Any]:
    active = {_active_key(arm): arm for arm in active_arms}
    controls = {_channel_off_key(arm): arm for arm in channel_off_arms}
    delta = THRESHOLDS.offset_fraction * radius
    responses: dict[tuple[int, int, int, str], list[complex]] = {}
    for phase_index, chirality, offset_sign in _expected_active_keys():
        arm = active[(phase_index, chirality, offset_sign)]
        baseline = controls[(phase_index, chirality)]
        for component in ("center", "actuator"):
            responses[(phase_index, chirality, offset_sign, component)] = [
                value - control
                for value, control in zip(
                    _trace(arm, component),
                    _trace(baseline, component),
                    strict=True,
                )
            ]

    even_rows: list[dict[str, Any]] = []
    response_rows: list[dict[str, Any]] = []
    response_index: dict[tuple[int, int], dict[str, Any]] = {}
    for phase_index in range(8):
        for chirality in (1, -1):
            response_row: dict[str, Any] = {
                "phase_index": phase_index,
                "phase": PHASES[phase_index],
                "chirality": chirality,
            }
            even_row: dict[str, Any] = {
                "phase_index": phase_index,
                "chirality": chirality,
            }
            passes = []
            for component in ("center", "actuator"):
                plus = responses[(phase_index, chirality, 1, component)]
                minus = responses[(phase_index, chirality, -1, component)]
                odd = [
                    (left - right) / (2.0 * delta)
                    for left, right in zip(plus, minus, strict=True)
                ]
                even = [
                    (left + right) / (2.0 * delta)
                    for left, right in zip(plus, minus, strict=True)
                ]
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
                final = odd[-1]
                response_row[f"{component}_odd_final"] = _pair(final)
                response_row[f"{component}_longitudinal"] = final.real
                response_row[f"{component}_transverse"] = (
                    -chirality * final.imag
                )
                even_row[f"{component}_odd_rms"] = odd_rms
                even_row[f"{component}_even_rms"] = even_rms
                even_row[f"{component}_even_to_odd_rms"] = ratio
                even_row[f"{component}_odd_resolved"] = resolved
                passes.append(passed)
            even_row["pass"] = all(passes)
            even_rows.append(even_row)
            response_rows.append(response_row)
            response_index[(phase_index, chirality)] = response_row

    mirror_rows = []
    for phase_index in range(8):
        for offset_sign in (1, -1):
            plus = active[(phase_index, 1, offset_sign)]
            minus = active[(7 - phase_index, -1, offset_sign)]
            center_error = max(
                abs(right - left.conjugate())
                for left, right in zip(
                    _trace(plus, "center"),
                    _trace(minus, "center"),
                    strict=True,
                )
            ) / radius
            actuator_error = max(
                abs(right - left.conjugate())
                for left, right in zip(
                    _trace(plus, "actuator"),
                    _trace(minus, "actuator"),
                    strict=True,
                )
            ) / radius
            mirror_rows.append(
                {
                    "plus_phase_index": phase_index,
                    "minus_phase_index": 7 - phase_index,
                    "offset_sign": offset_sign,
                    "center_error_fraction": center_error,
                    "actuator_error_fraction": actuator_error,
                    "pass": bool(
                        max(center_error, actuator_error)
                        <= THRESHOLDS.covariance_fraction
                    ),
                }
            )

    half_turn_rows = []
    for phase_index in range(4):
        for chirality in (1, -1):
            for offset_sign in (1, -1):
                first = active[(phase_index, chirality, offset_sign)]
                second = active[(phase_index + 4, chirality, -offset_sign)]
                center_error = max(
                    abs(left + right)
                    for left, right in zip(
                        _trace(first, "center"),
                        _trace(second, "center"),
                        strict=True,
                    )
                ) / radius
                actuator_error = max(
                    abs(left + right)
                    for left, right in zip(
                        _trace(first, "actuator"),
                        _trace(second, "actuator"),
                        strict=True,
                    )
                ) / radius
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
                            <= THRESHOLDS.covariance_fraction
                        ),
                    }
                )

    phase_rows = []
    for phase_index in range(8):
        plus = response_index[(phase_index, 1)]
        minus = response_index[(phase_index, -1)]
        center = 0.5 * (
            plus["center_transverse"] + minus["center_transverse"]
        )
        actuator = 0.5 * (
            plus["actuator_transverse"] + minus["actuator_transverse"]
        )
        phase_rows.append(
            {
                "phase_index": phase_index,
                "phase": PHASES[phase_index],
                "center_transverse": center,
                "actuator_transverse": actuator,
                "center_positive": bool(center > 0.0),
                "actuator_positive": bool(actuator > 0.0),
            }
        )
    center_mean = math.fsum(row["center_transverse"] for row in phase_rows) / 8
    actuator_mean = (
        math.fsum(row["actuator_transverse"] for row in phase_rows) / 8
    )
    center_support = sum(row["center_positive"] for row in phase_rows)
    actuator_support = sum(row["actuator_positive"] for row in phase_rows)
    gates = {
        "odd_signal_resolved": all(
            row["center_odd_resolved"] and row["actuator_odd_resolved"]
            for row in even_rows
        ),
        "even_response": all(row["pass"] for row in even_rows),
        "mirror_equivariance": all(row["pass"] for row in mirror_rows),
        "half_turn_equivariance": all(row["pass"] for row in half_turn_rows),
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
        "pass": all(gates.values()),
    }


def _classify(
    *,
    pipeline: bool,
    registration: bool,
    validity: bool,
    ledger: bool,
    dynamic: bool,
    response: dict[str, Any],
) -> tuple[str, dict[str, bool]]:
    means = response.get("phase_averaged_transverse_response", {})
    center = means.get("center")
    actuator = means.get("actuator")
    response_available = bool(response.get("available", False))
    finite_means = bool(
        center is not None
        and actuator is not None
        and math.isfinite(center)
        and math.isfinite(actuator)
    )
    scalar = bool(
        finite_means
        and abs(center) <= THRESHOLDS.scalar_null_maximum
        and abs(actuator) <= THRESHOLDS.scalar_null_maximum
    )
    chiral = bool(
        finite_means
        and center >= THRESHOLDS.chiral_minimum
        and actuator >= THRESHOLDS.chiral_minimum
    )
    support = response.get("positive_phase_support", {})
    support_pass = bool(
        support.get("center", 0) >= THRESHOLDS.sign_support_minimum
        and support.get("actuator", 0) >= THRESHOLDS.sign_support_minimum
    )
    directional_fail = bool(
        finite_means
        and (
            center <= -THRESHOLDS.chiral_minimum
            or actuator <= -THRESHOLDS.chiral_minimum
            or (
                abs(center) >= THRESHOLDS.chiral_minimum
                and abs(actuator) >= THRESHOLDS.chiral_minimum
                and math.copysign(1.0, center) != math.copysign(1.0, actuator)
            )
        )
    )
    response_pass = bool(response.get("pass", False))
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
    elif scalar:
        decision = "p4r-phase-averaged-scalar-response"
    elif chiral and support_pass:
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
        "scalar_region": scalar,
        "positive_chiral_region": chiral,
        "positive_phase_support": support_pass,
        "directional_fail_region": directional_fail,
    }


def audit_payload(
    payload: dict[str, Any],
    *,
    report_text: str,
    source_sha256: str,
) -> dict[str, Any]:
    """Recompute all decision-bearing summaries without target imports."""

    differences: list[str] = []
    thresholds = asdict(THRESHOLDS)
    thresholds["reference_steps"] = list(THRESHOLDS.reference_steps)
    threshold_contract = payload["protocol"]["thresholds"] == thresholds
    active_arms = payload["active_arms"]
    channel_off_arms = payload["channel_off_arms"]
    registration = _registration(active_arms, channel_off_arms)
    radius = float(payload["candidate"]["radius"])
    theta = float(payload["candidate"]["theta"])
    expected_steps = _expected_steps()
    trace_contract = bool(
        registration
        and all(
            [row["step"] for row in arm["trace"]] == expected_steps
            and _finite(arm["trace"])
            for arm in [*active_arms, *channel_off_arms]
        )
    )
    channel_pass, channel_summary, channel_differences = _channel_off_audit(
        channel_off_arms,
        radius=radius,
    )
    differences.extend(channel_differences)

    ledger_passes = []
    dynamic_passes = []
    validity_passes = []
    maximum_recombination = 0.0
    controls = {_channel_off_key(arm): arm for arm in channel_off_arms}
    dynamic_summaries = []
    for arm in active_arms:
        (
            ledger_gates,
            recombination,
            recombination_pass,
            ledger_differences,
        ) = _ledger_audit(arm)
        differences.extend(ledger_differences)
        maximum_recombination = max(
            maximum_recombination,
            *recombination.values(),
        )
        baseline = controls[(int(arm["phase_index"]), int(arm["chirality"]))]
        dynamic_gates, dynamic_metrics, dynamic_differences = _dynamic_audit(
            arm,
            baseline,
            radius=radius,
            theta=theta,
        )
        differences.extend(dynamic_differences)
        complete = [row["step"] for row in arm["trace"]] == expected_steps
        finite = _finite(arm["trace"])
        validity_gates = {
            "complete": complete,
            "finite": finite,
            "normal_operands": bool(arm["validity_gates"]["normal_operands"]),
        }
        _compare_tree(
            f"active[{arm['name']}].validity_gates",
            validity_gates,
            arm["validity_gates"],
            differences,
        )
        ledger_pass = bool(all(ledger_gates.values()) and recombination_pass)
        dynamic_pass = all(dynamic_gates.values())
        valid = all(validity_gates.values())
        if ledger_pass != arm["ledger_pass"]:
            differences.append(f"active[{arm['name']}].ledger_pass")
        if dynamic_pass != arm["dynamic_pass"]:
            differences.append(f"active[{arm['name']}].dynamic_pass")
        if valid != arm["valid"]:
            differences.append(f"active[{arm['name']}].valid")
        ledger_passes.append(ledger_pass)
        dynamic_passes.append(dynamic_pass)
        validity_passes.append(valid)
        dynamic_summaries.append(dynamic_metrics)

    response = (
        _response_audit(active_arms, channel_off_arms, radius=radius)
        if registration and trace_contract
        else {
            "available": False,
            "pass": False,
            "phase_averaged_transverse_response": {
                "center": None,
                "actuator": None,
            },
            "positive_phase_support": {"center": 0, "actuator": 0},
        }
    )
    _compare_tree(
        "response_controls",
        response,
        payload["response_controls"],
        differences,
    )
    construction_pass = bool(
        payload["construction_controls"]["pass"]
        and all(payload["construction_controls"]["gates"].values())
    )
    pipeline = bool(construction_pass and channel_pass and registration)
    decision, gates = _classify(
        pipeline=pipeline,
        registration=registration,
        validity=bool(registration and all(validity_passes)),
        ledger=bool(registration and all(ledger_passes)),
        dynamic=bool(registration and all(dynamic_passes)),
        response=response,
    )
    _compare_tree("gates", gates, payload["gates"], differences)
    if decision != payload["decision"]:
        differences.append(f"decision: {decision} != {payload['decision']}")

    report_center = response["phase_averaged_transverse_response"]["center"]
    report_actuator = response["phase_averaged_transverse_response"]["actuator"]
    report_checks = {
        "decision": f"Decision: **`{payload['decision']}`**." in report_text,
        "source_sha256": source_sha256 in report_text,
        "center_mean": (
            report_center is not None
            and f"{report_center:.6g}" in report_text
        ),
        "actuator_mean": (
            report_actuator is not None
            and f"{report_actuator:.6g}" in report_text
        ),
        "support": (
            f"{response['positive_phase_support']['center']}/8"
            in report_text
            and f"{response['positive_phase_support']['actuator']}/8"
            in report_text
        ),
    }
    checks = {
        "canonical_source_hash": source_sha256 == EXPECTED_SOURCE_SHA256,
        "candidate_contract": bool(
            payload["candidate_id"] == EXPECTED_CANDIDATE_ID
            and payload["candidate"]["horizon"] == 2400
            and payload["candidate"]["alpha"] == 0.005
            and payload["candidate"]["eta"] == 0.075
        ),
        "threshold_contract": threshold_contract,
        "execution_revision": (
            payload["provenance"]["revision"] == EXPECTED_EXECUTION_REVISION
        ),
        "historical_p4_preserved": bool(
            payload["historical_p4"]["decision"] == EXPECTED_P4_DECISION
            and payload["historical_p4"]["unchanged_by_p4r"]
        ),
        "registration": registration,
        "trace_shape_and_finiteness": trace_contract,
        "channel_off": channel_pass,
        "active_validity": bool(all(validity_passes)),
        "ledger_and_metrology": bool(all(ledger_passes)),
        "loop_dynamics": bool(all(dynamic_passes)),
        "response_recomputation": bool(response.get("pass", False)),
        "decision_recomputation": bool(
            decision == payload["decision"] == EXPECTED_RESULT_DECISION
        ),
        "stored_summary_agreement": not differences,
        "markdown_summary_agreement": all(report_checks.values()),
    }
    response_summary = response["phase_averaged_transverse_response"]
    summary = {
        "active_arm_count": len(active_arms),
        "channel_off_arm_count": len(channel_off_arms),
        "samples_per_arm": len(active_arms[0]["trace"]),
        "high_precision_reference_count": sum(
            len(arm["high_precision_references"]) for arm in active_arms
        ),
        "center_phase_averaged_transverse_response": response_summary["center"],
        "actuator_phase_averaged_transverse_response": response_summary[
            "actuator"
        ],
        "center_positive_phase_support": response["positive_phase_support"][
            "center"
        ],
        "actuator_positive_phase_support": response[
            "positive_phase_support"
        ]["actuator"],
        "maximum_ledger_recombination_relative_difference": (
            maximum_recombination
        ),
        "maximum_d0_fraction": max(
            row["maximum_d0_fraction"] for row in dynamic_summaries
        ),
        "maximum_final_separation_ratio": max(
            row["final_separation_ratio"] for row in dynamic_summaries
        ),
        "maximum_energy_ratio": max(
            row["energy_ratio"] for row in dynamic_summaries
        ),
    }
    return {
        "schema_version": 1,
        "audit": "independent P4-R raw-JSON recomputation",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "source": {
            "path": SOURCE.as_posix(),
            "canonical_lf_sha256": source_sha256,
            "expected_canonical_lf_sha256": EXPECTED_SOURCE_SHA256,
        },
        "independence_boundary": {
            "target_runner_imported": False,
            "third_party_numeric_package_imported": False,
            "shared_raw_simulation": True,
            "unavailable_for_independent_recompute": [
                "per-update full histories",
                "per-update raw ledger terms",
                "channel-off bitwise histories",
                "per-update subnormal operands",
            ],
        },
        "tolerances": {
            "absolute_recompute": ABSOLUTE_RECOMPUTE_TOLERANCE,
            "relative_recompute": RELATIVE_RECOMPUTE_TOLERANCE,
            "ledger_recombination_relative": (
                LEDGER_RECOMBINATION_RELATIVE_TOLERANCE
            ),
        },
        "checks": checks,
        "report_checks": report_checks,
        "summary": summary,
        "stored_decision": payload["decision"],
        "recomputed_decision": decision,
        "recomputed_gates": gates,
        "differences": differences,
        "decision": (
            "p4r-independent-audit-agrees"
            if all(checks.values())
            else "p4r-independent-audit-disagrees"
        ),
    }


def run_audit(source: Path = SOURCE, report: Path = SOURCE_REPORT) -> dict[str, Any]:
    source_path = source if source.is_absolute() else ROOT / source
    report_path = report if report.is_absolute() else ROOT / report
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    return audit_payload(
        payload,
        report_text=report_path.read_text(encoding="utf-8"),
        source_sha256=canonical_lf_sha256(source_path),
    )


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    if temporary.exists():
        raise RuntimeError(f"refusing stale audit temporary file: {temporary}")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--report", type=Path, default=SOURCE_REPORT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    default = DEFAULT_OUTPUT if DEFAULT_OUTPUT.is_absolute() else ROOT / DEFAULT_OUTPUT
    if output.resolve() == default.resolve() and output.exists():
        raise RuntimeError("refusing to overwrite independent audit output")
    result = run_audit(args.source, args.report)
    serialized = json.dumps(result, allow_nan=False, indent=2, sort_keys=True) + "\n"
    _atomic_write(output, serialized)
    print(
        json.dumps(
            {
                "decision": result["decision"],
                "recomputed_decision": result["recomputed_decision"],
                "output_sha256": hashlib.sha256(
                    serialized.encode("utf-8")
                ).hexdigest(),
            }
        )
    )


if __name__ == "__main__":
    main()
