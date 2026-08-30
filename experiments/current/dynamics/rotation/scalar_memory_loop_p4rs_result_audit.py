"""Independently recompute the frozen P4-R-S decision from raw JSON."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path
import subprocess
from typing import Any

from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4r_result_audit as p4r_audit,
)


ROOT = Path(__file__).resolve().parents[4]
SOURCE = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4rs_anchor_scale_2026-08-30.json"
)
SOURCE_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4rs_anchor_scale_2026-08-30.md"
)
L3_SOURCE = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4r_phase_metrology_2026-08-26.json"
)
INTERVAL_SOURCE = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_interval_certificate_2026-08-21.json"
)
DEFAULT_OUTPUT = Path(
    "reports/project/meta/reviews/"
    "p4rs_independent_result_recompute_2026-08-30.json"
)

EXPECTED_SOURCE_SHA256 = (
    "daf127a55adf0eaa60325725493781a94fad3601bf52e90c38ba8c5e13ff62a7"
)
EXPECTED_REPORT_SHA256 = (
    "f2a76ddbd79337b7a527fcd9951b6ab6b890b0fda7137d0791531cd8094132d0"
)
EXPECTED_L3_SHA256 = (
    "807cf915d1602d87a779e7bf587387559b1b19d7de60dc43c6e1e220b73682c8"
)
EXPECTED_SOURCE_BLOB = "e4eae06ada6860455e49a08691235b9f6e818f51"
EXPECTED_REPORT_BLOB = "b5d085d665bc60d82279458072e775d0cf794ee8"
EXPECTED_RESULT_COMMIT = "6817d758c6287472c57c46780b938ab8fd7935a9"
EXPECTED_EXECUTION_REVISION = "83185e00dc30575ad57cf7f0ec7c76f6ba7baa77"
EXPECTED_IMPLEMENTATION_REVISION = "d5cc87617a790c7b4be3664e36b261fc0c29ecc2"
EXPECTED_DESIGN_REVISION = "11cabd66d0ba086116b29b3ea3d8a8548560cea1"
EXPECTED_PROTOCOL_REVISION = "3797c98c83ed61fa02e939583782fd7213e0b961"
EXPECTED_RUNNER_BLOB = "a3f1b2d4f9089d00f3786721ad1dcf13895377f7"
EXPECTED_TEST_BLOB = "0dc1177d4cd1921c5dd1c6a3c26e1614221979c2"
EXPECTED_REVIEW_BLOB = "64b771deff282a3c3bc2952f8f857d1c1d143383"
EXPECTED_CANDIDATE_ID = "k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1"
EXPECTED_L3_CANDIDATE_ID = (
    "k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1"
)
EXPECTED_RESULT_DECISION = "p4rs-anchor-scale-transfer-pass"
EXPECTED_L3_DECISION = "p4r-phase-averaged-chiral-response-pass"
EXPECTED_P4_DECISION = "p4-source-write-architecture-fail"
RADIUS_DECIMAL = (
    "0.946517504804223960990626662735384935160072399313332184824852189820406"
    "142783597632634323623097735558253263801"
)
THETA_DECIMAL = (
    "0.015770381717134991901268964141341323131632114098006250776592366366328"
    "4306507309780740587352166842324150748019"
)
EXPECTED_STATIC = {
    "beta_real": 0.2923957083606503,
    "beta_imag": -0.45093731944942195,
    "write_real": 0.004999787409710969,
    "write_imag": 0.6340870653534046,
    "write_gain": 0.4020914043226352,
}
EXPECTED_L3_MEANS = {
    "A_C": 0.24091330892887405,
    "B_C": 0.208421577193625,
    "A_Q": 0.303296080377988,
    "B_Q": 0.15375308546516817,
}
ABSOLUTE_RECOMPUTE_TOLERANCE = 5.0e-13
RELATIVE_RECOMPUTE_TOLERANCE = 5.0e-12
LEDGER_RECOMBINATION_RELATIVE_TOLERANCE = 2.0e-11


@dataclass(frozen=True)
class AuditThresholds:
    """Independent transcription of the frozen P4-R-S thresholds."""

    active_updates: int = 2_000
    sample_every: int = 5
    late_start: int = 1_800
    phase_start: int = 1_500
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
    scale_tolerance: float = 0.05
    reconstruction_tolerance: float = 5.0e-15
    reference_dps: int = 80
    reference_steps: tuple[int, ...] = (1, 1_000, 2_000)


THRESHOLDS = AuditThresholds()
PHASES = tuple((2 * index + 1) * math.pi / 8.0 for index in range(8))
ANCHOR_STEPS = tuple(range(0, 2_001, 5))
L3_STEPS = tuple(range(0, 4_001, 10))
MEMORY_TIMES = tuple(0.05 * index for index in range(401))


def _canonical_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_lf_sha256(path: Path) -> str:
    return hashlib.sha256(_canonical_bytes(path)).hexdigest()


def canonical_git_blob(path: Path) -> str:
    content = _canonical_bytes(path)
    header = f"blob {len(content)}\0".encode()
    return hashlib.sha1(header + content).hexdigest()  # noqa: S324


def _git_output(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _close(left: float, right: float) -> bool:
    return math.isclose(
        float(left),
        float(right),
        rel_tol=RELATIVE_RECOMPUTE_TOLERANCE,
        abs_tol=ABSOLUTE_RECOMPUTE_TOLERANCE,
    )


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


def _registered(
    active_arms: list[dict[str, Any]],
    channel_off_arms: list[dict[str, Any]],
) -> bool:
    return bool(
        [_active_key(arm) for arm in active_arms] == _expected_active_keys()
        and [_channel_off_key(arm) for arm in channel_off_arms]
        == _expected_channel_off_keys()
    )


def _trace(arm: dict[str, Any], component: str) -> list[complex]:
    return [complex(*row[component]) for row in arm["trace"]]


def _pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def _rms_complex(values: list[complex]) -> float:
    return math.sqrt(math.fsum(abs(value) ** 2 for value in values) / len(values))


def _rms_real(values: list[float]) -> float:
    return math.sqrt(math.fsum(value * value for value in values) / len(values))


def _phase_metrics(
    trace: list[dict[str, Any]],
    *,
    chirality: int,
    theta: float,
) -> dict[str, float | int | bool]:
    rows = [row for row in trace if int(row["step"]) >= THRESHOLDS.phase_start]
    steps = [float(row["step"]) for row in rows]
    angles = p4r_audit._unwrap([float(row["alignment_phase"]) for row in rows])
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
    rms_error = _rms_real([value - expected for value in increments])
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
                real = Decimal.from_float(float(row[f"{prefix}_residual"][0]))
                imag = Decimal.from_float(float(row[f"{prefix}_residual"][1]))
                reconstructed = (real * real + imag * imag).sqrt()
                stored = Decimal.from_float(float(row[f"{prefix}_absolute"]))
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
                    row["center_binary64_distance"] <= row["center_eval_envelope"]
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
) -> tuple[bool, dict[str, float], list[str]]:
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
        "work_split_step": abs(maxima["work_split"]) / initial_energy
        <= THRESHOLDS.step_ledger_relative,
        "total_ledger_step": abs(maxima["ledger"]) / initial_energy
        <= THRESHOLDS.step_ledger_relative,
        "work_split_cumulative": abs(cumulative["work_split"]) / initial_energy
        <= THRESHOLDS.cumulative_ledger_relative,
        "total_ledger_cumulative": abs(cumulative["ledger"]) / initial_energy
        <= THRESHOLDS.cumulative_ledger_relative,
        "force_balance": abs(maxima["force_balance"]) / force_scale
        <= THRESHOLDS.force_relative,
        "midpoint_force": abs(maxima["midpoint"]) / force_scale
        <= THRESHOLDS.force_relative,
        "center_local": abs(maxima["center_local"]) / displacement_scale
        <= THRESHOLDS.local_displacement_relative,
        "coupling_local": abs(maxima["coupling_local"]) / displacement_scale
        <= THRESHOLDS.local_displacement_relative,
        "center_full_envelope": bool(
            maxima["center_envelope_ratio"] <= 1.0
            and margins["center_full"] >= 0.0
        ),
        "coupling_full_envelope": bool(
            maxima["coupling_envelope_ratio"] <= 1.0
            and margins["coupling_full"] >= 0.0
        ),
        "actuator_update_relative": abs(maxima["actuator_full"])
        / displacement_scale
        <= THRESHOLDS.actuator_displacement_relative,
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
    p4r_audit._compare_tree(
        f"active[{arm['name']}].ledger_gates",
        gates,
        arm["ledger_gates"],
        differences,
    )
    final_energy = float(arm["trace"][-1]["interaction_energy"])
    rebuilt = {
        "work_split": math.fsum(
            (cumulative["write_work"], cumulative["age_work"], -cumulative["center_work"])
        ),
        "ledger": math.fsum(
            (
                final_energy,
                -initial_energy,
                cumulative["write_work"],
                cumulative["age_work"],
                cumulative["external_work"],
            )
        ),
        "truncated_ledger": math.fsum(
            (
                final_energy,
                -initial_energy,
                cumulative["write_work"],
                cumulative["external_work"],
            )
        ),
        "raw_center_ledger": math.fsum(
            (
                final_energy,
                -initial_energy,
                cumulative["raw_center_work"],
                cumulative["external_work"],
            )
        ),
    }
    recombination = {
        f"{key}_relative_difference": abs(value - cumulative[key]) / initial_energy
        for key, value in rebuilt.items()
    }
    recombination["reference_absolute_reconstruction_relative_difference"] = (
        reference_relative_difference
    )
    rivals = arm["nondecisional_rivals"]
    rival_consistency = bool(
        _close(
            rivals["truncated_age_ledger"]["cumulative_residual"],
            cumulative["truncated_ledger"],
        )
        and _close(
            rivals["truncated_age_ledger"]["maximum_residual"],
            maxima["truncated_ledger"],
        )
        and _close(
            rivals["raw_memory_center_ledger"]["cumulative_residual"],
            cumulative["raw_center_ledger"],
        )
        and _close(
            rivals["raw_memory_center_ledger"]["maximum_residual"],
            maxima["raw_center_ledger"],
        )
    )
    if not rival_consistency:
        differences.append(f"active[{arm['name']}].nondecisional_rivals")
    recombination_pass = bool(
        max(recombination.values()) <= LEDGER_RECOMBINATION_RELATIVE_TOLERANCE
    )
    if not recombination_pass:
        differences.append(f"active[{arm['name']}].ledger_recombination")
    passed = bool(all(gates.values()) and recombination_pass and rival_consistency)
    if passed != arm["ledger_pass"]:
        differences.append(f"active[{arm['name']}].ledger_pass")
    return passed, recombination, differences


def _dynamic_audit(
    arm: dict[str, Any],
    baseline: dict[str, Any],
    *,
    radius: float,
    theta: float,
) -> tuple[bool, dict[str, float], list[str]]:
    differences: list[str] = []
    trace = arm["trace"]
    delta = THRESHOLDS.offset_fraction * radius
    late = [row for row in trace if int(row["step"]) >= THRESHOLDS.late_start]
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
    final_center = complex(*trace[-1]["center"])
    final_actuator = complex(*trace[-1]["actuator"])
    metrics = {
        "maximum_d0_fraction": max(float(row["expected_d0_fraction"]) for row in trace),
        "late_maximum_d0_fraction": max(
            float(row["expected_d0_fraction"]) for row in late
        ),
        "late_opposite_minimum_fraction": min(
            float(row["opposite_d0_fraction"]) for row in late
        ),
        "final_separation_ratio": abs(final_center - final_actuator) / delta,
        "center_projection_ratio": offset_sign * center_response[-1].real / delta,
        "actuator_projection_ratio": offset_sign * actuator_response[-1].real / delta,
        "energy_ratio": float(trace[-1]["interaction_energy"])
        / float(arm["residual_scales"]["initial_energy"]),
        "maximum_center_response_ratio": max(abs(value) for value in center_response)
        / delta,
    }
    phase = _phase_metrics(trace, chirality=int(arm["chirality"]), theta=theta)
    gates = {
        "maximum_d0": metrics["maximum_d0_fraction"]
        <= THRESHOLDS.maximum_d0_fraction,
        "late_d0": metrics["late_maximum_d0_fraction"]
        <= THRESHOLDS.late_d0_fraction,
        "opposite_chirality": metrics["late_opposite_minimum_fraction"]
        >= THRESHOLDS.opposite_d0_fraction,
        "final_separation": metrics["final_separation_ratio"]
        <= THRESHOLDS.final_separation_fraction,
        "center_projection": THRESHOLDS.projection_minimum
        <= metrics["center_projection_ratio"]
        <= THRESHOLDS.projection_maximum,
        "actuator_projection": THRESHOLDS.projection_minimum
        <= metrics["actuator_projection_ratio"]
        <= THRESHOLDS.projection_maximum,
        "interaction_energy": metrics["energy_ratio"]
        <= THRESHOLDS.energy_ratio_maximum,
        "phase": bool(phase["pass"]),
        "informative_signal": metrics["maximum_center_response_ratio"]
        >= THRESHOLDS.signal_fraction,
    }
    p4r_audit._compare_tree(
        f"active[{arm['name']}].dynamic_gates",
        gates,
        arm["dynamic_gates"],
        differences,
    )
    p4r_audit._compare_tree(
        f"active[{arm['name']}].phase_metrics",
        phase,
        arm["phase_metrics"],
        differences,
    )
    for key, value in metrics.items():
        if not _close(value, arm[key]):
            differences.append(f"active[{arm['name']}].{key}")
    passed = bool(all(gates.values()))
    if passed != arm["dynamic_pass"]:
        differences.append(f"active[{arm['name']}].dynamic_pass")
    return passed, metrics, differences


def _channel_off_audit(
    arms: list[dict[str, Any]],
    *,
    radius: float,
    expected_steps: tuple[int, ...],
) -> tuple[bool, dict[str, float | int], list[str]]:
    differences: list[str] = []
    maximum_d0 = 0.0
    maximum_center = 0.0
    all_pass = True
    for arm in arms:
        trace = arm["trace"]
        observed_d0 = max(float(row["expected_d0_fraction"]) for row in trace)
        observed_center = max(abs(value) / radius for value in _trace(arm, "center"))
        maximum_d0 = max(maximum_d0, observed_d0)
        maximum_center = max(maximum_center, observed_center)
        gates = {
            "complete": tuple(int(row["step"]) for row in trace) == expected_steps,
            "finite": p4r_audit._finite(trace),
            "bitwise_native": bool(arm["gates"]["bitwise_native"]),
            "prepared_orbit": observed_d0 <= THRESHOLDS.channel_off_d0_fraction,
            "stationary_orbit_center": observed_center
            <= THRESHOLDS.channel_off_d0_fraction,
        }
        p4r_audit._compare_tree(
            f"channel_off[{arm['name']}].gates",
            gates,
            arm["gates"],
            differences,
        )
        if not _close(observed_d0, arm["maximum_d0_fraction"]):
            differences.append(f"channel_off[{arm['name']}].maximum_d0_fraction")
        if not _close(observed_center, arm["maximum_center_fraction"]):
            differences.append(f"channel_off[{arm['name']}].maximum_center_fraction")
        passed = bool(all(gates.values()))
        if passed != arm["pass"]:
            differences.append(f"channel_off[{arm['name']}].pass")
        all_pass = bool(all_pass and passed)
    return all_pass, {
        "arm_count": len(arms),
        "maximum_d0_fraction": maximum_d0,
        "maximum_center_fraction": maximum_center,
    }, differences


def _response(
    active_arms: list[dict[str, Any]],
    channel_off_arms: list[dict[str, Any]],
    *,
    radius: float,
    delta: float,
    expected_steps: tuple[int, ...],
    alpha: float,
) -> dict[str, Any]:
    all_arms = [*active_arms, *channel_off_arms]
    valid = bool(
        _registered(active_arms, channel_off_arms)
        and all(
            tuple(int(row["step"]) for row in arm["trace"]) == expected_steps
            and p4r_audit._finite(arm["trace"])
            and float(arm["phase"]) == PHASES[int(arm["phase_index"])]
            for arm in all_arms
        )
    )
    if not valid:
        return {"available": False, "reason": "invalid-raw-panel", "pass": False}
    active = {_active_key(arm): arm for arm in active_arms}
    controls = {_channel_off_key(arm): arm for arm in channel_off_arms}
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
            row: dict[str, Any] = {
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
                odd_rms = _rms_complex(odd)
                even_rms = _rms_complex(even)
                resolved = bool(math.isfinite(odd_rms) and odd_rms > 0.0)
                ratio = even_rms / odd_rms if resolved else None
                passed = bool(
                    resolved
                    and ratio is not None
                    and math.isfinite(ratio)
                    and ratio <= THRESHOLDS.even_response_relative
                )
                a_trace = [float(value.real) for value in odd]
                b_trace = [float(-chirality * value.imag) for value in odd]
                row[f"{component}_odd_final"] = _pair(odd[-1])
                row[f"{component}_A_trace"] = a_trace
                row[f"{component}_B_trace"] = b_trace
                row[f"{component}_A_final"] = a_trace[-1]
                row[f"{component}_B_final"] = b_trace[-1]
                even_row[f"{component}_odd_rms"] = odd_rms
                even_row[f"{component}_even_rms"] = even_rms
                even_row[f"{component}_even_to_odd_rms"] = ratio
                even_row[f"{component}_odd_resolved"] = resolved
                passes.append(passed)
            even_row["pass"] = all(passes)
            even_rows.append(even_row)
            response_rows.append(row)
            response_index[(phase_index, chirality)] = row

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
                    "pass": max(center_error, actuator_error)
                    <= THRESHOLDS.covariance_fraction,
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
                        "pass": max(center_error, actuator_error)
                        <= THRESHOLDS.covariance_fraction,
                    }
                )

    profiles = []
    for phase_index in range(8):
        plus = response_index[(phase_index, 1)]
        minus = response_index[(phase_index, -1)]
        profiles.append(
            {
                "phase_index": phase_index,
                "phase": PHASES[phase_index],
                "A_C": 0.5 * (plus["center_A_final"] + minus["center_A_final"]),
                "B_C": 0.5 * (plus["center_B_final"] + minus["center_B_final"]),
                "A_Q": 0.5
                * (plus["actuator_A_final"] + minus["actuator_A_final"]),
                "B_Q": 0.5
                * (plus["actuator_B_final"] + minus["actuator_B_final"]),
            }
        )
    means = {
        key: math.fsum(row[key] for row in profiles) / len(profiles)
        for key in EXPECTED_L3_MEANS
    }
    support = {
        "center": sum(row["B_C"] > 0.0 for row in profiles),
        "actuator": sum(row["B_Q"] > 0.0 for row in profiles),
    }
    gates = {
        "registered_complete_finite_panel": True,
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
        "steps": list(expected_steps),
        "memory_times": [alpha * step for step in expected_steps],
        "even_response": even_rows,
        "mirror_equivariance": mirror_rows,
        "half_turn_equivariance": half_turn_rows,
        "phase_chirality_response": response_rows,
        "phase_profiles": profiles,
        "means": means,
        "phase_averaged_transverse_response": {
            "center": means["B_C"],
            "actuator": means["B_Q"],
        },
        "positive_phase_support": support,
        "gates": gates,
        "pass": all(gates.values()),
    }


def _cross_scale(anchor: dict[str, Any], l3: dict[str, Any]) -> dict[str, Any]:
    labels = {
        "A_C": "center_A_trace",
        "B_C": "center_B_trace",
        "A_Q": "actuator_A_trace",
        "B_Q": "actuator_B_trace",
    }
    anchor_rows = {
        (int(row["phase_index"]), int(row["chirality"])): row
        for row in anchor["phase_chirality_response"]
    }
    l3_rows = {
        (int(row["phase_index"]), int(row["chirality"])): row
        for row in l3["phase_chirality_response"]
    }
    trace_differences = []
    flattened: dict[str, list[float]] = {key: [] for key in labels}
    for phase_index, chirality in _expected_channel_off_keys():
        first = anchor_rows[(phase_index, chirality)]
        second = l3_rows[(phase_index, chirality)]
        row: dict[str, Any] = {"phase_index": phase_index, "chirality": chirality}
        for label, key in labels.items():
            values = [
                float(left - right)
                for left, right in zip(first[key], second[key], strict=True)
            ]
            row[label] = values
            flattened[label].extend(values)
        trace_differences.append(row)
    transient_rms = {label: _rms_real(values) for label, values in flattened.items()}
    combined_complex_rms = {
        "center": _rms_real(
            [
                math.hypot(left, right)
                for left, right in zip(flattened["A_C"], flattened["B_C"], strict=True)
            ]
        ),
        "actuator": _rms_real(
            [
                math.hypot(left, right)
                for left, right in zip(flattened["A_Q"], flattened["B_Q"], strict=True)
            ]
        ),
    }
    anchor_profiles = {
        int(row["phase_index"]): row for row in anchor["phase_profiles"]
    }
    l3_profiles = {int(row["phase_index"]): row for row in l3["phase_profiles"]}
    profile_rows = []
    profile_values: dict[str, list[float]] = {key: [] for key in labels}
    for phase_index in range(8):
        row: dict[str, Any] = {
            "phase_index": phase_index,
            "phase": PHASES[phase_index],
        }
        for label in labels:
            value = anchor_profiles[phase_index][label] - l3_profiles[phase_index][label]
            row[label] = value
            profile_values[label].append(value)
        profile_rows.append(row)
    profile_rms = {label: _rms_real(values) for label, values in profile_values.items()}
    means = {}
    for label in labels:
        anchor_mean = float(anchor["means"][label])
        l3_mean = float(l3["means"][label])
        difference = anchor_mean - l3_mean
        means[label] = {
            "anchor": anchor_mean,
            "l3": l3_mean,
            "signed_difference": difference,
            "absolute_difference": abs(difference),
            "ratio": anchor_mean / l3_mean if l3_mean != 0.0 else None,
        }
    common_grid = bool(
        tuple(anchor["steps"]) == ANCHOR_STEPS
        and tuple(l3["steps"]) == L3_STEPS
        and len(anchor["memory_times"]) == len(l3["memory_times"]) == 401
        and all(
            math.isclose(left, right, rel_tol=0.0, abs_tol=1.0e-15)
            for left, right in zip(
                anchor["memory_times"], l3["memory_times"], strict=True
            )
        )
    )
    trace_gates = {
        label: value <= THRESHOLDS.scale_tolerance
        for label, value in transient_rms.items()
    }
    profile_gates = {
        label: value <= THRESHOLDS.scale_tolerance
        for label, value in profile_rms.items()
    }
    mean_gates = {
        label: row["absolute_difference"] <= THRESHOLDS.scale_tolerance
        for label, row in means.items()
    }
    gates = {
        "common_memory_time_grid": common_grid,
        "complete_transient": all(trace_gates.values()),
        "final_phase_profile": all(profile_gates.values()),
        "final_means": all(mean_gates.values()),
    }
    return {
        "scale_tolerance": THRESHOLDS.scale_tolerance,
        "common_memory_times": list(MEMORY_TIMES),
        "trace_differences": trace_differences,
        "transient_rms": transient_rms,
        "combined_complex_rms_nondecisional": combined_complex_rms,
        "profile_differences": profile_rows,
        "profile_rms": profile_rms,
        "mean_comparison": means,
        "trace_gates": trace_gates,
        "profile_gates": profile_gates,
        "mean_gates": mean_gates,
        "gates": gates,
        "pass": all(gates.values()),
    }


def _decision(
    *,
    pipeline: bool,
    registration: bool,
    validity: bool,
    ledger: bool,
    dynamics: bool,
    response: dict[str, Any],
    cross_scale: dict[str, Any],
) -> tuple[str, dict[str, bool]]:
    means = response.get("means", {})
    finite_means = bool(
        all(key in means and math.isfinite(float(means[key])) for key in EXPECTED_L3_MEANS)
    )
    center = float(means["B_C"]) if finite_means else math.nan
    actuator = float(means["B_Q"]) if finite_means else math.nan
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
    directional = bool(
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
    response_available = bool(response.get("available", False))
    response_pass = bool(response.get("pass", False))
    common_grid = bool(cross_scale.get("gates", {}).get("common_memory_time_grid"))
    scale_pass = bool(cross_scale.get("pass", False))
    if (
        not pipeline
        or not registration
        or not validity
        or not response_available
        or not finite_means
        or not common_grid
    ):
        decision = "p4rs-inconclusive"
    elif not ledger:
        decision = "p4rs-ledger-or-metrology-fail"
    elif not dynamics or not response_pass:
        decision = "p4rs-inconclusive"
    elif scalar:
        decision = "p4rs-anchor-scalar-response"
    elif directional:
        decision = "p4rs-anchor-chiral-hypothesis-fail"
    elif chiral and support_pass and not scale_pass:
        decision = "p4rs-cross-scale-mismatch"
    elif chiral and support_pass and scale_pass:
        decision = "p4rs-anchor-scale-transfer-pass"
    else:
        decision = "p4rs-inconclusive"
    return decision, {
        "pipeline": pipeline,
        "registration": registration,
        "valid_active_arms": validity,
        "response_available": response_available,
        "reciprocal_ledger_and_metrology": ledger,
        "nonlinear_loop_dynamics": dynamics,
        "response_symmetry_and_odd_signal": response_pass,
        "finite_response_means": finite_means,
        "scalar_region": scalar,
        "positive_chiral_region": chiral,
        "positive_phase_support": support_pass,
        "directional_fail_region": directional,
        "common_memory_time_grid": common_grid,
        "cross_scale_transfer": scale_pass,
    }


def _root_audit(payload: dict[str, Any], interval: dict[str, Any]) -> dict[str, Any]:
    candidate = payload["candidate"]
    radius_exact = Decimal(RADIUS_DECIMAL)
    theta_exact = Decimal(THETA_DECIMAL)
    certified = interval["certified_intersection"]
    refined = interval["panels"][-1]["refined"]
    alpha = float(candidate["alpha"])
    horizon = int(candidate["horizon"])
    theta = float(candidate["theta"])
    q = 1.0 - alpha
    denominator = 1.0 - q**horizon
    weights = [alpha * q**index / denominator for index in range(horizon)]
    beta = complex(
        math.fsum(weight * math.cos(-theta * index) for index, weight in enumerate(weights)),
        math.fsum(weight * math.sin(-theta * index) for index, weight in enumerate(weights)),
    )
    write = (weights[0] - beta) / (1.0 - beta)
    observed = {
        "beta_real": beta.real,
        "beta_imag": beta.imag,
        "write_real": write.real,
        "write_imag": write.imag,
        "write_gain": abs(write) ** 2,
    }
    static_errors = {
        key: abs(observed[key] - expected) for key, expected in EXPECTED_STATIC.items()
    }
    gates = {
        "candidate_id": interval.get("candidate_id") == EXPECTED_CANDIDATE_ID,
        "exact_interval_membership": bool(
            Decimal(certified["radius"]["lower"])
            <= radius_exact
            <= Decimal(certified["radius"]["upper"])
            and Decimal(certified["theta"]["lower"])
            <= theta_exact
            <= Decimal(certified["theta"]["upper"])
        ),
        "exact_refined_root": bool(
            refined["radius"] == RADIUS_DECIMAL and refined["theta"] == THETA_DECIMAL
        ),
        "binary64_parse": bool(
            float(RADIUS_DECIMAL) == candidate["radius"]
            and float(THETA_DECIMAL) == candidate["theta"]
        ),
        "matched_h_alpha": Decimal(str(candidate["alpha"]))
        * Decimal(candidate["horizon"])
        == Decimal(12),
        "matched_eta_alpha": Decimal(str(candidate["eta"]))
        / Decimal(str(candidate["alpha"]))
        == Decimal(15),
        "frozen_static_values": max(static_errors.values())
        <= THRESHOLDS.coefficient_tolerance,
        "conjugacy": 0.0 <= THRESHOLDS.coefficient_tolerance,
        "positive_equal_mobility": observed["write_gain"] > 0.0,
        "computed_offset": THRESHOLDS.offset_fraction * float(RADIUS_DECIMAL)
        == 0.0014197762572063359,
    }
    differences: list[str] = []
    p4r_audit._compare_tree(
        "anchor_root_controls.gates",
        gates,
        payload["anchor_root_controls"]["gates"],
        differences,
    )
    p4r_audit._compare_tree(
        "anchor_root_controls.observed_static",
        observed,
        payload["anchor_root_controls"]["observed_static"],
        differences,
    )
    return {
        "gates": gates,
        "recomputed_static": observed,
        "maximum_static_absolute_error": max(static_errors.values()),
        "stored_agreement": not differences,
        "differences": differences,
        "pass": bool(all(gates.values()) and not differences),
    }


def _provenance_audit(payload: dict[str, Any]) -> dict[str, bool]:
    provenance = payload["provenance"]
    runner_path = (
        "experiments/current/dynamics/rotation/"
        "scalar_memory_loop_p4rs_anchor_scale_gate.py"
    )
    test_path = "tests/test_rotating_wave_p4rs_anchor_scale.py"
    source_path = SOURCE.as_posix()
    report_path = SOURCE_REPORT.as_posix()
    result_parent = _git_output(["rev-parse", f"{EXPECTED_RESULT_COMMIT}^"])
    return {
        "execution_revision": provenance["revision"] == EXPECTED_EXECUTION_REVISION,
        "implementation_revision": provenance["implementation_readiness"][
            "implementation_revision"
        ]
        == EXPECTED_IMPLEMENTATION_REVISION,
        "design_and_protocol_revisions": bool(
            provenance["design_freeze_revision"] == EXPECTED_DESIGN_REVISION
            and provenance["protocol_freeze_revision"] == EXPECTED_PROTOCOL_REVISION
        ),
        "readiness_review": bool(
            provenance["implementation_readiness"]["review_blob"]
            == EXPECTED_REVIEW_BLOB
            and provenance["implementation_readiness"]["verdict"]
            == "p4rs-implementation-ready"
        ),
        "implementation_blobs_at_execution": bool(
            _git_output(
                ["rev-parse", f"{EXPECTED_IMPLEMENTATION_REVISION}:{runner_path}"]
            )
            == EXPECTED_RUNNER_BLOB
            and _git_output(
                ["rev-parse", f"{EXPECTED_IMPLEMENTATION_REVISION}:{test_path}"]
            )
            == EXPECTED_TEST_BLOB
            and provenance["implementation_blobs"][runner_path]
            == EXPECTED_RUNNER_BLOB
            and provenance["implementation_blobs"][test_path]
            == EXPECTED_TEST_BLOB
        ),
        "clean_pushed_preflight": bool(
            provenance["clean_pre_run_status"] == ""
            and provenance["upstream_synchronized"] is True
            and provenance["default_outputs_absent_at_start"] is True
            and provenance["freeze_revisions_are_ancestors"] is True
        ),
        "historical_decisions": provenance["decisions"]
        == {
            "interval": "interval-certified-unique-root-pass",
            "p4": EXPECTED_P4_DECISION,
            "p4r": EXPECTED_L3_DECISION,
            "source": "referee-source-ready-with-major-claim-restrictions",
            "stability": "numerically-stable-source-pass",
        },
        "source_restrictions_preserved": provenance[
            "open_major_source_restrictions"
        ]
        == ["SRC-MAJ-001", "SRC-MAJ-002", "SRC-MAJ-003"],
        "result_commit_parent_is_execution_revision": result_parent
        == EXPECTED_EXECUTION_REVISION,
        "result_blobs_at_freeze": bool(
            _git_output(["rev-parse", f"{EXPECTED_RESULT_COMMIT}:{source_path}"])
            == EXPECTED_SOURCE_BLOB
            and _git_output(["rev-parse", f"{EXPECTED_RESULT_COMMIT}:{report_path}"])
            == EXPECTED_REPORT_BLOB
        ),
    }


def _closest_contacts(
    active_arms: list[dict[str, Any]],
    response: dict[str, Any],
    cross_scale: dict[str, Any],
) -> dict[str, Any]:
    maxima = [arm["residual_maxima"] for arm in active_arms]
    scales = [arm["residual_scales"] for arm in active_arms]
    even = response["even_response"]
    mirror = response["mirror_equivariance"]
    half = response["half_turn_equivariance"]
    return {
        "largest_step_ledger_fraction": max(
            abs(row["ledger"]) / scale["initial_energy"]
            for row, scale in zip(maxima, scales, strict=True)
        ),
        "step_ledger_limit": THRESHOLDS.step_ledger_relative,
        "largest_full_envelope_ratio": max(
            max(
                row["center_envelope_ratio"],
                row["coupling_envelope_ratio"],
                row["actuator_envelope_ratio"],
            )
            for row in maxima
        ),
        "full_envelope_ratio_limit": 1.0,
        "largest_even_to_odd_ratio": max(
            max(row["center_even_to_odd_rms"], row["actuator_even_to_odd_rms"])
            for row in even
        ),
        "even_to_odd_limit": THRESHOLDS.even_response_relative,
        "largest_covariance_error_fraction": max(
            [
                max(row["center_error_fraction"], row["actuator_error_fraction"])
                for row in [*mirror, *half]
            ]
        ),
        "covariance_limit_fraction": THRESHOLDS.covariance_fraction,
        "smallest_positive_chiral_margin": min(
            response["means"]["B_C"] - THRESHOLDS.chiral_minimum,
            response["means"]["B_Q"] - THRESHOLDS.chiral_minimum,
        ),
        "smallest_cross_scale_slack": min(
            THRESHOLDS.scale_tolerance - value
            for group in (
                cross_scale["transient_rms"],
                cross_scale["profile_rms"],
                {
                    key: row["absolute_difference"]
                    for key, row in cross_scale["mean_comparison"].items()
                },
            )
            for value in group.values()
        ),
    }


def audit_payload(
    payload: dict[str, Any],
    *,
    l3_payload: dict[str, Any],
    interval_payload: dict[str, Any],
    report_text: str,
    source_sha256: str,
    report_sha256: str,
    source_blob: str,
    report_blob: str,
) -> dict[str, Any]:
    """Recompute every decision-bearing stored summary without target imports."""

    differences: list[str] = []
    thresholds = asdict(THRESHOLDS)
    thresholds["reference_steps"] = list(THRESHOLDS.reference_steps)
    active_arms = payload["active_arms"]
    channel_off_arms = payload["channel_off_arms"]
    registration = _registered(active_arms, channel_off_arms)
    radius = float(payload["candidate"]["radius"])
    theta = float(payload["candidate"]["theta"])
    trace_contract = bool(
        registration
        and all(
            tuple(int(row["step"]) for row in arm["trace"]) == ANCHOR_STEPS
            and p4r_audit._finite(arm["trace"])
            for arm in [*active_arms, *channel_off_arms]
        )
    )
    channel_pass, channel_summary, channel_differences = _channel_off_audit(
        channel_off_arms,
        radius=radius,
        expected_steps=ANCHOR_STEPS,
    )
    differences.extend(channel_differences)

    controls = {_channel_off_key(arm): arm for arm in channel_off_arms}
    validity_passes = []
    ledger_passes = []
    dynamic_passes = []
    dynamic_summaries = []
    maximum_recombination = 0.0
    for arm in active_arms:
        validity = bool(
            tuple(int(row["step"]) for row in arm["trace"]) == ANCHOR_STEPS
            and p4r_audit._finite(arm["trace"])
            and arm["validity_gates"]["normal_operands"] is True
        )
        expected_validity = {
            "complete": tuple(int(row["step"]) for row in arm["trace"])
            == ANCHOR_STEPS,
            "finite": p4r_audit._finite(arm["trace"]),
            "normal_operands": bool(arm["validity_gates"]["normal_operands"]),
        }
        p4r_audit._compare_tree(
            f"active[{arm['name']}].validity_gates",
            expected_validity,
            arm["validity_gates"],
            differences,
        )
        if validity != arm["valid"]:
            differences.append(f"active[{arm['name']}].valid")
        ledger_pass, recombination, ledger_differences = _ledger_audit(arm)
        differences.extend(ledger_differences)
        maximum_recombination = max(maximum_recombination, *recombination.values())
        dynamic_pass, dynamic_summary, dynamic_differences = _dynamic_audit(
            arm,
            controls[(int(arm["phase_index"]), int(arm["chirality"]))],
            radius=radius,
            theta=theta,
        )
        differences.extend(dynamic_differences)
        validity_passes.append(validity)
        ledger_passes.append(ledger_pass)
        dynamic_passes.append(dynamic_pass)
        dynamic_summaries.append(dynamic_summary)

    anchor_response = _response(
        active_arms,
        channel_off_arms,
        radius=radius,
        delta=THRESHOLDS.offset_fraction * radius,
        expected_steps=ANCHOR_STEPS,
        alpha=0.01,
    )
    p4r_audit._compare_tree(
        "anchor_response",
        anchor_response,
        payload["anchor_response"],
        differences,
    )

    l3_active = l3_payload["active_arms"]
    l3_channel_off = l3_payload["channel_off_arms"]
    l3_radius = float(l3_payload["candidate"]["radius"])
    l3_response = _response(
        l3_active,
        l3_channel_off,
        radius=l3_radius,
        delta=THRESHOLDS.offset_fraction * l3_radius,
        expected_steps=L3_STEPS,
        alpha=0.005,
    )
    p4r_audit._compare_tree(
        "l3_reference.response",
        l3_response,
        payload["l3_reference"]["response"],
        differences,
    )
    l3_mean_errors = {
        key: abs(l3_response["means"][key] - expected)
        for key, expected in EXPECTED_L3_MEANS.items()
    }
    cross_scale = _cross_scale(anchor_response, l3_response)
    p4r_audit._compare_tree(
        "cross_scale",
        cross_scale,
        payload["cross_scale"],
        differences,
    )
    root_audit = _root_audit(payload, interval_payload)
    differences.extend(root_audit["differences"])
    construction_pass = bool(
        payload["construction_controls"]["pass"]
        and all(payload["construction_controls"]["gates"].values())
        and payload["construction_controls"]["small_h_algebraic_control"]["pass"]
    )
    registration_controls_pass = bool(
        payload["registration_controls"]["pass"]
        and all(payload["registration_controls"]["gates"].values())
        and payload["registration_controls"]["anchor_steps"] == list(ANCHOR_STEPS)
        and payload["registration_controls"]["l3_steps"] == list(L3_STEPS)
    )
    l3_reference_pass = bool(
        payload["l3_reference"]["pass"]
        and all(payload["l3_reference"]["gates"].values())
        and max(l3_mean_errors.values()) <= THRESHOLDS.reconstruction_tolerance
        and l3_payload["decision"] == EXPECTED_L3_DECISION
        and l3_payload["historical_p4"]["decision"] == EXPECTED_P4_DECISION
    )
    pipeline = bool(
        root_audit["pass"]
        and construction_pass
        and registration_controls_pass
        and l3_reference_pass
        and channel_pass
    )
    decision, gates = _decision(
        pipeline=pipeline,
        registration=registration,
        validity=bool(registration and all(validity_passes)),
        ledger=bool(registration and all(ledger_passes)),
        dynamics=bool(registration and all(dynamic_passes)),
        response=anchor_response,
        cross_scale=cross_scale,
    )
    p4r_audit._compare_tree("gates", gates, payload["gates"], differences)
    if decision != payload["decision"]:
        differences.append(f"decision: {decision} != {payload['decision']}")

    provenance = _provenance_audit(payload)
    report_checks = {
        "decision": f"Decision: {EXPECTED_RESULT_DECISION}." in report_text,
        "source_sha256": EXPECTED_SOURCE_SHA256 in report_text,
        "execution_revision": EXPECTED_EXECUTION_REVISION in report_text,
        "claim_boundary": "Not established:" in report_text
        and "P5 evidence" in report_text,
    }
    checks = {
        "canonical_source_hash": source_sha256 == EXPECTED_SOURCE_SHA256,
        "canonical_report_hash": report_sha256 == EXPECTED_REPORT_SHA256,
        "source_git_blob": source_blob == EXPECTED_SOURCE_BLOB,
        "report_git_blob": report_blob == EXPECTED_REPORT_BLOB,
        "provenance": all(provenance.values()),
        "candidate_contract": bool(
            payload["candidate_id"] == EXPECTED_CANDIDATE_ID
            and payload["candidate"]["radius_decimal"] == RADIUS_DECIMAL
            and payload["candidate"]["theta_decimal"] == THETA_DECIMAL
            and payload["candidate"]["horizon"] == 1_200
            and payload["candidate"]["alpha"] == 0.01
            and payload["candidate"]["eta"] == 0.15
        ),
        "threshold_contract": payload["protocol"]["thresholds"] == thresholds,
        "root_and_static_gain": root_audit["pass"],
        "construction_controls": construction_pass,
        "registration_controls": registration_controls_pass,
        "raw_registration": registration,
        "trace_shape_and_finiteness": trace_contract,
        "channel_off": channel_pass,
        "active_validity": all(validity_passes),
        "ledger_metrology_and_rivals": all(ledger_passes),
        "all_96_high_precision_checkpoints": bool(
            sum(len(arm["high_precision_references"]) for arm in active_arms) == 96
            and all(_reference_consistency(arm)[0] for arm in active_arms)
        ),
        "loop_dynamics": all(dynamic_passes),
        "anchor_response_recomputation": bool(anchor_response.get("pass")),
        "raw_l3_reconstruction": l3_reference_pass,
        "historical_l3_hash": canonical_lf_sha256(ROOT / L3_SOURCE)
        == EXPECTED_L3_SHA256,
        "cross_scale_recomputation": bool(cross_scale.get("pass")),
        "decision_recomputation": decision
        == payload["decision"]
        == EXPECTED_RESULT_DECISION,
        "stored_summary_agreement": not differences,
        "markdown_summary_agreement": all(report_checks.values()),
    }
    contacts = _closest_contacts(active_arms, anchor_response, cross_scale)
    return {
        "schema_version": 1,
        "audit": "independent P4-R-S raw-JSON recomputation",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "source": {
            "path": SOURCE.as_posix(),
            "canonical_lf_sha256": source_sha256,
            "expected_canonical_lf_sha256": EXPECTED_SOURCE_SHA256,
            "canonical_git_blob": source_blob,
            "freeze_commit": EXPECTED_RESULT_COMMIT,
        },
        "independence_boundary": {
            "target_runner_imported": False,
            "third_party_numeric_package_imported": False,
            "older_independent_audit_primitives_reused": [
                "finite-tree validation",
                "phase unwrapping",
                "recursive stored/recomputed comparison",
            ],
            "shared_raw_simulation": True,
            "unavailable_for_independent_recompute": [
                "per-update full histories between stored stride-5 samples",
                "per-update raw ledger operands",
                "channel-off bitwise history arrays",
                "per-update normal/subnormal operand classifications",
            ],
        },
        "tolerances": {
            "absolute_recompute": ABSOLUTE_RECOMPUTE_TOLERANCE,
            "relative_recompute": RELATIVE_RECOMPUTE_TOLERANCE,
            "ledger_recombination_relative": LEDGER_RECOMBINATION_RELATIVE_TOLERANCE,
        },
        "provenance_checks": provenance,
        "checks": checks,
        "report_checks": report_checks,
        "root_audit": root_audit,
        "channel_off_summary": channel_summary,
        "summary": {
            "active_arm_count": len(active_arms),
            "channel_off_arm_count": len(channel_off_arms),
            "samples_per_arm": len(active_arms[0]["trace"]),
            "high_precision_reference_count": sum(
                len(arm["high_precision_references"]) for arm in active_arms
            ),
            "anchor_means": anchor_response["means"],
            "l3_means": l3_response["means"],
            "positive_phase_support": anchor_response["positive_phase_support"],
            "transient_rms": cross_scale["transient_rms"],
            "profile_rms": cross_scale["profile_rms"],
            "mean_absolute_differences": {
                key: row["absolute_difference"]
                for key, row in cross_scale["mean_comparison"].items()
            },
            "maximum_ledger_recombination_relative_difference": maximum_recombination,
            "maximum_d0_fraction": max(
                row["maximum_d0_fraction"] for row in dynamic_summaries
            ),
            "maximum_final_separation_ratio": max(
                row["final_separation_ratio"] for row in dynamic_summaries
            ),
            "maximum_energy_ratio": max(row["energy_ratio"] for row in dynamic_summaries),
        },
        "closest_threshold_contacts": contacts,
        "stored_decision": payload["decision"],
        "recomputed_decision": decision,
        "recomputed_gates": gates,
        "differences": differences,
        "decision": (
            "p4rs-independent-audit-agrees"
            if all(checks.values())
            else "p4rs-independent-audit-disagrees"
        ),
    }


def run_audit(
    source: Path = SOURCE,
    report: Path = SOURCE_REPORT,
    l3_source: Path = L3_SOURCE,
    interval_source: Path = INTERVAL_SOURCE,
) -> dict[str, Any]:
    source_path = source if source.is_absolute() else ROOT / source
    report_path = report if report.is_absolute() else ROOT / report
    l3_path = l3_source if l3_source.is_absolute() else ROOT / l3_source
    interval_path = (
        interval_source if interval_source.is_absolute() else ROOT / interval_source
    )
    return audit_payload(
        json.loads(source_path.read_text(encoding="utf-8")),
        l3_payload=json.loads(l3_path.read_text(encoding="utf-8")),
        interval_payload=json.loads(interval_path.read_text(encoding="utf-8")),
        report_text=report_path.read_text(encoding="utf-8"),
        source_sha256=canonical_lf_sha256(source_path),
        report_sha256=canonical_lf_sha256(report_path),
        source_blob=canonical_git_blob(source_path),
        report_blob=canonical_git_blob(report_path),
    )


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    if path.exists() or temporary.exists():
        raise RuntimeError(f"refusing existing audit output or temporary: {path}")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--report", type=Path, default=SOURCE_REPORT)
    parser.add_argument("--l3-source", type=Path, default=L3_SOURCE)
    parser.add_argument("--interval-source", type=Path, default=INTERVAL_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = run_audit(
        args.source,
        args.report,
        args.l3_source,
        args.interval_source,
    )
    serialized = json.dumps(result, allow_nan=False, indent=2, sort_keys=True) + "\n"
    _atomic_write(output, serialized)
    print(
        json.dumps(
            {
                "decision": result["decision"],
                "recomputed_decision": result["recomputed_decision"],
                "output_sha256": hashlib.sha256(serialized.encode()).hexdigest(),
            }
        )
    )


if __name__ == "__main__":
    main()
