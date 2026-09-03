"""Execute the frozen deterministic P5-D mutual-center gate.

Importing this module is target-free.  The registered panel can only be
entered through :func:`run_gate`, whose first operation is the provenance and
readiness guard.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from typing import Any, Iterable, Literal

import mpmath as mp
import numpy as np

from emergenz_knoten.mutual_center_coupling import (
    MutualCenterMode,
    MutualCenterStep,
    mutual_center_rounding_metrology,
    mutual_center_step,
)
from emergenz_knoten.orbit_center_actuator import (
    OrbitCenterReadout,
    candidate_orbit_center_readout,
    complex_to_vector,
    orbit_center,
)
from emergenz_knoten.rotating_wave_formation import target_history
from emergenz_knoten.rotating_wave_stability import (
    native_fifo_step,
    rotation_matrix,
    rotation_translation_quotient_distance,
)
from emergenz_knoten.rotating_wave_stability_gate import RotatingWaveCandidate


ROOT = Path(__file__).resolve().parents[4]
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_loop_p5d_mutual_center_protocol_2026-09-01.md"
)
DESIGN_AUDIT = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_loop_p5d_mutual_center_design_audit_2026-09-01.md"
)
READINESS_REVIEW = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_loop_p5d_serialization_recovery_readiness_2026-09-02.md"
)
RECOVERY_PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_loop_p5d_serialization_recovery_protocol_2026-09-02.md"
)
GOVERNANCE = Path(
    "experiments/current/dynamics/rotation/"
    "scalar_memory_loop_p5d_governance.json"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p5d_mutual_center_2026-09-01.json"
)
DEFAULT_REPORT = DEFAULT_SUMMARY.with_suffix(".md")

DESIGN_FREEZE_REVISION = "f68c8f89f4d62fcfc7f440d78e4e2a6011ce6344"
PROTOCOL_FREEZE_REVISION = "d7a4c5ec4d40f1899940161877b0ab80b7a8c0c7"
PROTOCOL_FREEZE_BLOB = "bf3325d550ae2288d8e4012e0480077abf51032e"
RECOVERY_PROTOCOL_REVISION = "9fdab8d534ebadfdd155bde55c3c7e509783dd53"
RECOVERY_PROTOCOL_BLOB = "508b642b12884996ccb87f354e875053bdf36c5a"
EXPECTED_HEAD_BLOBS = {
    DESIGN_AUDIT.as_posix(): "0f02d86bcbfacd2154d21df4a40f853174085d0b",
    "src/emergenz_knoten/orbit_center_actuator.py": (
        "63d31bc47291f76c65a5633f14436ccd2105fe9a"
    ),
    "src/emergenz_knoten/rotating_wave_stability.py": (
        "9defb5a6876371202e1ba57cea030c997b9c6edd"
    ),
    "src/emergenz_knoten/rotating_wave_stability_gate.py": (
        "630beb9952abefea823d91388dcbb2de8f1a2927"
    ),
    "src/emergenz_knoten/rotating_wave_formation.py": (
        "38f16f11a790a64470bab3a34505825cf815e7f0"
    ),
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4rs_anchor_scale_2026-08-30.json": (
        "e4eae06ada6860455e49a08691235b9f6e818f51"
    ),
    "reports/project/meta/reviews/"
    "scalar_memory_loop_p4rs_anchor_scale_result_review_2026-08-30.md": (
        "4d3297c2bfb0fd191bd73e8e9cad7f7d85a86b87"
    ),
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_noise_stress_2026-08-31.json": (
        "0bcf489068fc0c7004f0c65b973f7be49dfe1621"
    ),
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_noise_stress_result_review_2026-09-01.md": (
        "5f5e374aa554eb795172110c2ddccb32dcb48de0"
    ),
    "reports/project/meta/reviews/"
    "p4_publication_source_referee_audit_2026-08-27.md": (
        "273acc3a86a9f3757e853236ce386f064835194c"
    ),
}
IMPLEMENTATION_PATHS = (
    "src/emergenz_knoten/mutual_center_coupling.py",
    "experiments/current/dynamics/rotation/"
    "scalar_memory_loop_p5d_mutual_center_gate.py",
    "experiments/current/dynamics/rotation/"
    "scalar_memory_loop_p5d_mutual_center_result_audit.py",
    "tests/test_mutual_center_coupling.py",
    "tests/test_rotating_wave_p5d_mutual_center.py",
    "tests/test_rotating_wave_p5d_result_audit.py",
)

GOVERNANCE_SCHEMA = "scalar-memory-loop-p5d-governance-v1"
GOVERNANCE_KEYS = {
    "authorization",
    "gate",
    "reason",
    "schema",
    "state",
    "target_authorized",
    "target_calls_recorded",
}
INCIDENT_KEYS = {"attempt", "incident_blob", "incident_path", "status"}
EXPECTED_INCIDENTS = (
    (
        1,
        "reports/project/meta/reviews/"
        "scalar_memory_loop_p5d_first_target_serialization_failure_2026-09-02.md",
        "e8a8de1c405c6ee0cc8994bed5983b4b4f5b3b6c",
        "p5d-inconclusive-serialization-failure",
    ),
    (
        2,
        "reports/project/meta/reviews/"
        "scalar_memory_loop_p5d_replacement_nonfinite_serialization_failure_2026-09-02.md",
        "5710a9d02eb02f6bd27cf8c556dd8c34c4758467",
        "p5d-inconclusive-nonfinite-serialization-failure",
    ),
)

CANDIDATE_ID = "k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1"
RADIUS_DECIMAL = (
    "0.946517504804223960990626662735384935160072399313332184824852189820406"
    "142783597632634323623097735558253263801"
)
THETA_DECIMAL = (
    "0.015770381717134991901268964141341323131632114098006250776592366366328"
    "4306507309780740587352166842324150748019"
)
CANDIDATE = RotatingWaveCandidate(
    candidate_id=CANDIDATE_ID,
    radius=float(RADIUS_DECIMAL),
    theta=float(THETA_DECIMAL),
    alpha=0.01,
    horizon=1200,
    memory_mass=1.0,
    eta=0.15,
    sigma_rep=1.0,
    sigma_att=3.0,
    amplitude_rep=1.0,
    amplitude_att=3.5,
)
EXPECTED_WRITE_GAIN = 0.4020914043226352
EXPECTED_MOBILITY = 0.004020914043226352
PHASES = tuple((2 * index + 1) * math.pi / 8.0 for index in range(8))
DISTANCE_FRACTIONS = (3, 6)
CHIRALITY_PAIRS = ((1, 1), (1, -1), (-1, 1), (-1, -1))
KAPPAS = ("low", "high")
KAPPA_VALUES = {"low": 0.000625, "high": 0.00125}
SIGNS = (1, -1)
DIRECTIONS: tuple[MutualCenterMode, ...] = (
    "a_to_b",
    "b_to_a",
    "reciprocal",
)

P5DDecision = Literal[
    "p5d-inconclusive",
    "p5d-ledger-or-reciprocity-fail",
    "p5d-loop-integrity-fail",
    "p5d-directional-causality-fail",
    "p5d-mutual-hypothesis-fail",
    "p5d-independent-superposition",
    "p5d-mutual-center-response-pass",
]


@dataclass(frozen=True)
class P5DThresholds:
    """All numerical choices frozen by the P5-D protocol."""

    active_updates: int = 2_000
    sample_every: int = 20
    late_start: int = 1_800
    phase_start: int = 1_500
    reference_dps: int = 80
    reference_steps: tuple[int, ...] = (1, 1_000, 2_000)
    channel_off_d0_fraction: float = 1.0e-10
    channel_off_center_fraction: float = 1.0e-10
    maximum_d0_fraction: float = 0.01
    late_d0_fraction: float = 0.002
    opposite_d0_fraction: float = 0.5
    phase_mean_error_fraction: float = 0.01
    phase_rms_error_fraction: float = 0.05
    minimum_separation_fraction: float = 2.25
    maximum_center_response_fraction: float = 0.10
    center_local_relative: float = 5.0e-12
    force_relative: float = 5.0e-12
    step_ledger_relative: float = 5.0e-11
    cumulative_ledger_relative: float = 5.0e-9
    minimum_mobility_dissipation: float = -1.0e-30
    response_resolution: float = 1.0e-12
    reciprocal_low_minimum: float = 0.0025
    reciprocal_high_minimum: float = 0.005
    one_way_low_minimum: float = 0.00125
    one_way_high_minimum: float = 0.0025
    response_low_high_minimum: float = 0.35
    response_low_high_maximum: float = 0.65
    response_symmetry_rms: float = 0.05
    normalized_distance_difference: float = 0.10
    raw_distance_ratio_minimum: float = 1.8
    raw_distance_ratio_maximum: float = 2.2
    covariance_fraction: float = 1.0e-11
    phase_support_minimum: int = 6
    excess_low_minimum: float = 2.0e-6
    excess_high_minimum: float = 1.0e-5
    excess_low_high_minimum: float = 0.10
    excess_low_high_maximum: float = 0.40
    excess_response_minimum: float = 5.0e-4
    excess_response_maximum: float = 0.02
    excess_distance_difference: float = 0.20


THRESHOLDS = P5DThresholds()


def _pair(value: complex) -> list[float]:
    number = complex(value)
    return [float(number.real), float(number.imag)]


def _complex(value: Iterable[float]) -> complex:
    row = tuple(float(item) for item in value)
    if len(row) != 2 or not all(math.isfinite(item) for item in row):
        raise ValueError("complex pair must contain two finite numbers")
    return complex(row[0], row[1])


def expected_base_keys() -> list[tuple[int, int, int, int]]:
    """Return the frozen order of the 64 pair initial conditions."""

    return [
        (distance, phase_index, chirality_a, chirality_b)
        for distance in DISTANCE_FRACTIONS
        for phase_index in range(8)
        for chirality_a, chirality_b in CHIRALITY_PAIRS
    ]


def expected_active_keys() -> list[tuple[int, int, int, int, str, int, str]]:
    """Return the frozen order of the 768 active arms."""

    return [
        (*base, kappa, sign, direction)
        for base in expected_base_keys()
        for kappa in KAPPAS
        for sign in SIGNS
        for direction in DIRECTIONS
    ]


def reflection_key(
    key: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    """Return the corrected in-panel reflection mate."""

    distance, phase_index, chirality_a, chirality_b = key
    return distance, 7 - phase_index, -chirality_a, -chirality_b


def swap_half_turn_key(
    key: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    """Return the corrected A/B-swap plus half-turn mate."""

    distance, phase_index, chirality_a, chirality_b = key
    return distance, (3 - phase_index) % 8, chirality_b, chirality_a


def swap_direction(mode: MutualCenterMode) -> MutualCenterMode:
    """Exchange the two one-way directions and preserve reciprocal/off."""

    if mode == "a_to_b":
        return "b_to_a"
    if mode == "b_to_a":
        return "a_to_b"
    return mode


def _base_key(row: dict[str, Any]) -> tuple[int, int, int, int]:
    return (
        int(row["distance_fraction"]),
        int(row["phase_index"]),
        int(row["chirality_a"]),
        int(row["chirality_b"]),
    )


def _active_key(
    row: dict[str, Any],
) -> tuple[int, int, int, int, str, int, str]:
    return (
        *_base_key(row),
        str(row["kappa_name"]),
        int(row["sign"]),
        str(row["mode"]),
    )


def panel_registration(
    channel_off_arms: list[dict[str, Any]],
    active_arms: list[dict[str, Any]],
    *,
    require_references: bool = False,
) -> dict[str, Any]:
    """Validate counts, exact order, uniqueness and trace grids."""

    off_keys = [_base_key(row) for row in channel_off_arms]
    active_keys = [_active_key(row) for row in active_arms]
    expected_steps = list(
        range(0, THRESHOLDS.active_updates + 1, THRESHOLDS.sample_every)
    )
    traces = channel_off_arms + active_arms
    trace_grids = all(
        [int(sample["step"]) for sample in row.get("trace", [])]
        == expected_steps
        for row in traces
    )
    finite = _all_finite(traces)
    reference_rows = [
        reference
        for row in active_arms
        for reference in row.get("high_precision_references", [])
    ]
    references = bool(
        not require_references
        or (
            len(reference_rows) == 192
            and all(reference.get("pass", False) for reference in reference_rows)
            and all(
                len(row.get("high_precision_references", []))
                == (
                    len(THRESHOLDS.reference_steps)
                    if row.get("kappa_name") == "high"
                    and row.get("sign") == 1
                    and row.get("mode") == "reciprocal"
                    else 0
                )
                for row in active_arms
            )
        )
    )
    gates = {
        "channel_off_count": len(channel_off_arms) == 64,
        "active_count": len(active_arms) == 768,
        "channel_off_order": off_keys == expected_base_keys(),
        "active_order": active_keys == expected_active_keys(),
        "channel_off_unique": len(set(off_keys)) == len(off_keys),
        "active_unique": len(set(active_keys)) == len(active_keys),
        "complete_trace_grids": trace_grids,
        "finite": finite,
        "high_precision_references": references,
    }
    return {"gates": gates, "pass": bool(all(gates.values()))}


def _all_finite(value: Any) -> bool:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return True
    if isinstance(value, np.bool_):
        return True
    if isinstance(value, np.integer):
        return True
    if isinstance(value, np.floating):
        return math.isfinite(float(value))
    if isinstance(value, np.complexfloating):
        number = complex(value)
        return math.isfinite(number.real) and math.isfinite(number.imag)
    if isinstance(value, complex):
        return math.isfinite(value.real) and math.isfinite(value.imag)
    if isinstance(value, np.ndarray):
        try:
            return bool(np.isfinite(value).all())
        except TypeError:
            return False
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    if isinstance(value, dict):
        return all(_all_finite(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return all(_all_finite(item) for item in value)
    return False


def _history_sha256(history: np.ndarray) -> str:
    state = np.ascontiguousarray(np.asarray(history, dtype="<f8"))
    return hashlib.sha256(state.tobytes(order="C")).hexdigest()


def _trace_map(row: dict[str, Any]) -> dict[int, dict[str, Any]]:
    trace = row.get("trace", [])
    return {int(sample["step"]): sample for sample in trace}


def _response_trace(
    active: dict[str, Any],
    baseline: dict[str, Any],
) -> list[dict[str, Any]]:
    control = _trace_map(baseline)
    rows = []
    initial_distance = float(active["initial_distance"])
    coupling = float(active["coupling"])
    sign = 1.0 if coupling > 0.0 else -1.0
    e0 = _complex(baseline["trace"][0]["separation"])
    e0 /= abs(e0)
    for sample in active["trace"]:
        reference = control[int(sample["step"])]
        separation = _complex(sample["separation"])
        off_separation = _complex(reference["separation"])
        delta = separation - off_separation
        delta_a = _complex(sample["center_a"]) - _complex(
            reference["center_a"]
        )
        delta_b = _complex(sample["center_b"]) - _complex(
            reference["center_b"]
        )
        longitudinal = -sign * (delta * e0.conjugate()).real / initial_distance
        transverse = (delta * e0.conjugate()).imag / initial_distance
        rows.append(
            {
                "step": int(sample["step"]),
                "delta_separation": _pair(delta),
                "delta_a": _pair(delta_a),
                "delta_b": _pair(delta_b),
                "longitudinal": float(longitudinal),
                "transverse": float(transverse),
            }
        )
    return rows


def response_controls(
    channel_off_arms: list[dict[str, Any]],
    active_arms: list[dict[str, Any]],
    *,
    require_references: bool = False,
) -> dict[str, Any]:
    """Construct baseline-subtracted responses and closed-loop excesses."""

    registration = panel_registration(
        channel_off_arms,
        active_arms,
        require_references=require_references,
    )
    if not registration["pass"]:
        return {
            "available": False,
            "reason": "misregistered-panel",
            "registration": registration,
            "rows": [],
            "triplets": [],
            "gates": {},
            "pass": False,
        }
    off = {_base_key(row): row for row in channel_off_arms}
    active = {_active_key(row): row for row in active_arms}
    rows = []
    responses: dict[
        tuple[int, int, int, int, str, int, str], list[dict[str, Any]]
    ] = {}
    for key in expected_active_keys():
        trace = _response_trace(active[key], off[key[:4]])
        responses[key] = trace
        final = trace[-1]
        late = [sample for sample in trace if sample["step"] >= THRESHOLDS.late_start]
        rows.append(
            {
                "key": list(key),
                "final_longitudinal": final["longitudinal"],
                "final_transverse": final["transverse"],
                "late_mean_longitudinal": float(
                    np.mean([sample["longitudinal"] for sample in late])
                ),
                "late_rms_longitudinal": float(
                    np.sqrt(np.mean([sample["longitudinal"] ** 2 for sample in late]))
                ),
            }
        )

    triplets = []
    for base in expected_base_keys():
        baseline = off[base]
        initial_distance = float(baseline["initial_distance"])
        e0 = _complex(baseline["trace"][0]["separation"])
        e0 /= abs(e0)
        for kappa in KAPPAS:
            for sign in SIGNS:
                prefix = (*base, kappa, sign)
                one_ab = responses[(*prefix, "a_to_b")]
                one_ba = responses[(*prefix, "b_to_a")]
                reciprocal = responses[(*prefix, "reciprocal")]
                excess_trace = []
                for ab, ba, rec in zip(one_ab, one_ba, reciprocal, strict=True):
                    excess = (
                        _complex(rec["delta_separation"])
                        - _complex(ab["delta_separation"])
                        - _complex(ba["delta_separation"])
                    )
                    excess_trace.append(
                        {
                            "step": rec["step"],
                            "excess": _pair(excess),
                            "longitudinal": float(
                                (excess * e0.conjugate()).real / initial_distance
                            ),
                            "transverse": float(
                                (excess * e0.conjugate()).imag / initial_distance
                            ),
                        }
                    )
                late = [
                    sample
                    for sample in excess_trace
                    if sample["step"] >= THRESHOLDS.late_start
                ]
                triplets.append(
                    {
                        "key": list(prefix),
                        "trace": excess_trace,
                        "final_longitudinal": excess_trace[-1]["longitudinal"],
                        "late_mean_longitudinal": float(
                            np.mean([sample["longitudinal"] for sample in late])
                        ),
                        "late_rms_longitudinal": float(
                            np.sqrt(
                                np.mean(
                                    [sample["longitudinal"] ** 2 for sample in late]
                                )
                            )
                        ),
                    }
                )

    gates, diagnostics = _aggregate_response_gates(
        rows=rows,
        triplets=triplets,
        responses=responses,
    )
    return {
        "available": True,
        "registration": registration,
        "rows": rows,
        "triplets": triplets,
        "diagnostics": diagnostics,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _aggregate_response_gates(
    *,
    rows: list[dict[str, Any]],
    triplets: list[dict[str, Any]],
    responses: dict[
        tuple[int, int, int, int, str, int, str], list[dict[str, Any]]
    ],
) -> tuple[dict[str, bool], dict[str, Any]]:
    row_by_key = {tuple(row["key"]): row for row in rows}
    excess_by_key = {tuple(row["key"]): row for row in triplets}

    minima = {
        "reciprocal_low": min(
            row["final_longitudinal"]
            for key, row in row_by_key.items()
            if key[4] == "low" and key[6] == "reciprocal"
        ),
        "reciprocal_high": min(
            row["final_longitudinal"]
            for key, row in row_by_key.items()
            if key[4] == "high" and key[6] == "reciprocal"
        ),
        "one_way_low": min(
            row["final_longitudinal"]
            for key, row in row_by_key.items()
            if key[4] == "low" and key[6] != "reciprocal"
        ),
        "one_way_high": min(
            row["final_longitudinal"]
            for key, row in row_by_key.items()
            if key[4] == "high" and key[6] != "reciprocal"
        ),
        "excess_low": min(
            row["final_longitudinal"]
            for key, row in excess_by_key.items()
            if key[4] == "low"
        ),
        "excess_high": min(
            row["final_longitudinal"]
            for key, row in excess_by_key.items()
            if key[4] == "high"
        ),
    }

    low_high = []
    excess_low_high = []
    excess_fraction = []
    for base in expected_base_keys():
        for sign in SIGNS:
            for mode in DIRECTIONS:
                low = row_by_key[(*base, "low", sign, mode)][
                    "final_longitudinal"
                ]
                high = row_by_key[(*base, "high", sign, mode)][
                    "final_longitudinal"
                ]
                low_high.append(low / high if high != 0.0 else math.nan)
            low_x = excess_by_key[(*base, "low", sign)]["final_longitudinal"]
            high_x = excess_by_key[(*base, "high", sign)]["final_longitudinal"]
            reciprocal = row_by_key[(*base, "high", sign, "reciprocal")][
                "final_longitudinal"
            ]
            excess_low_high.append(low_x / high_x if high_x != 0.0 else math.nan)
            excess_fraction.append(high_x / reciprocal if reciprocal != 0.0 else math.nan)

    reflection_errors = []
    swap_errors = []
    for key in expected_active_keys():
        base = key[:4]
        reflected = (*reflection_key(base), *key[4:])
        swapped = (
            *swap_half_turn_key(base),
            key[4],
            key[5],
            swap_direction(key[6]),
        )
        trace = responses[key]
        reflected_trace = responses[reflected]
        swapped_trace = responses[swapped]
        reflection_errors.append(
            _trace_rms(
                [
                    _complex(a["delta_separation"])
                    - _complex(b["delta_separation"]).conjugate()
                    for a, b in zip(trace, reflected_trace, strict=True)
                ]
            )
            / CANDIDATE.radius
        )
        swap_errors.append(
            _trace_rms(
                [
                    _complex(a["delta_separation"])
                    - _complex(b["delta_separation"])
                    for a, b in zip(trace, swapped_trace, strict=True)
                ]
            )
            / CANDIDATE.radius
        )

    distance_errors = []
    raw_distance_ratios = []
    excess_distance_errors = []
    for phase_index in range(8):
        for chirality_a, chirality_b in CHIRALITY_PAIRS:
            for kappa in KAPPAS:
                for sign in SIGNS:
                    for mode in DIRECTIONS:
                        small = row_by_key[
                            (3, phase_index, chirality_a, chirality_b, kappa, sign, mode)
                        ]["final_longitudinal"]
                        large = row_by_key[
                            (6, phase_index, chirality_a, chirality_b, kappa, sign, mode)
                        ]["final_longitudinal"]
                        scale = max(abs(small), abs(large), np.finfo(float).tiny)
                        distance_errors.append(abs(small - large) / scale)
                        raw_distance_ratios.append(
                            (6.0 * large) / (3.0 * small)
                            if small != 0.0
                            else math.nan
                        )
                    small_x = excess_by_key[
                        (3, phase_index, chirality_a, chirality_b, kappa, sign)
                    ]["final_longitudinal"]
                    large_x = excess_by_key[
                        (6, phase_index, chirality_a, chirality_b, kappa, sign)
                    ]["final_longitudinal"]
                    scale_x = max(abs(small_x), abs(large_x), np.finfo(float).tiny)
                    excess_distance_errors.append(abs(small_x - large_x) / scale_x)

    sign_errors = []
    for base in expected_base_keys():
        for kappa in KAPPAS:
            for mode in DIRECTIONS:
                plus = row_by_key[(*base, kappa, 1, mode)]["final_longitudinal"]
                minus = row_by_key[(*base, kappa, -1, mode)]["final_longitudinal"]
                scale = max(abs(plus), abs(minus), np.finfo(float).tiny)
                sign_errors.append(abs(plus - minus) / scale)

    support = {}
    excess_support = {}
    for distance in DISTANCE_FRACTIONS:
        for chirality_pair in CHIRALITY_PAIRS:
            for kappa in KAPPAS:
                for sign in SIGNS:
                    label = f"d{distance}-s{chirality_pair[0]}{chirality_pair[1]}-{kappa}-{sign:+d}"
                    support[label] = sum(
                        row_by_key[
                            (
                                distance,
                                phase_index,
                                *chirality_pair,
                                kappa,
                                sign,
                                "reciprocal",
                            )
                        ]["final_longitudinal"]
                        > 0.0
                        for phase_index in range(8)
                    )
                    excess_support[label] = sum(
                        excess_by_key[
                            (distance, phase_index, *chirality_pair, kappa, sign)
                        ]["final_longitudinal"]
                        > 0.0
                        for phase_index in range(8)
                    )

    primary_resolved = all(
        abs(row["final_longitudinal"]) >= THRESHOLDS.response_resolution
        for row in rows
    )
    excess_resolved = all(
        abs(row["final_longitudinal"]) >= THRESHOLDS.response_resolution
        for row in triplets
    )
    gates = {
        "primary_resolved": primary_resolved,
        "reciprocal_low_signal": minima["reciprocal_low"]
        >= THRESHOLDS.reciprocal_low_minimum,
        "reciprocal_high_signal": minima["reciprocal_high"]
        >= THRESHOLDS.reciprocal_high_minimum,
        "one_way_low_signal": minima["one_way_low"]
        >= THRESHOLDS.one_way_low_minimum,
        "one_way_high_signal": minima["one_way_high"]
        >= THRESHOLDS.one_way_high_minimum,
        "phase_support": min(support.values()) >= THRESHOLDS.phase_support_minimum,
        "strength_scaling": _inside(
            low_high,
            THRESHOLDS.response_low_high_minimum,
            THRESHOLDS.response_low_high_maximum,
        ),
        "sign_symmetry": max(sign_errors) <= THRESHOLDS.response_symmetry_rms,
        "distance_normalization": max(distance_errors)
        <= THRESHOLDS.normalized_distance_difference,
        "raw_distance_scaling": _inside(
            raw_distance_ratios,
            THRESHOLDS.raw_distance_ratio_minimum,
            THRESHOLDS.raw_distance_ratio_maximum,
        ),
        "reflection_covariance": max(reflection_errors)
        <= THRESHOLDS.covariance_fraction,
        "swap_covariance": max(swap_errors) <= THRESHOLDS.covariance_fraction,
        "excess_resolved": excess_resolved,
        "excess_low_signal": minima["excess_low"] >= THRESHOLDS.excess_low_minimum,
        "excess_high_signal": minima["excess_high"]
        >= THRESHOLDS.excess_high_minimum,
        "excess_phase_support": min(excess_support.values())
        >= THRESHOLDS.phase_support_minimum,
        "excess_strength_scaling": _inside(
            excess_low_high,
            THRESHOLDS.excess_low_high_minimum,
            THRESHOLDS.excess_low_high_maximum,
        ),
        "excess_response_fraction": _inside(
            excess_fraction,
            THRESHOLDS.excess_response_minimum,
            THRESHOLDS.excess_response_maximum,
        ),
        "excess_distance_normalization": max(excess_distance_errors)
        <= THRESHOLDS.excess_distance_difference,
    }
    diagnostics = {
        "minima": minima,
        "low_high_range": [min(low_high), max(low_high)],
        "excess_low_high_range": [min(excess_low_high), max(excess_low_high)],
        "excess_response_fraction_range": [
            min(excess_fraction),
            max(excess_fraction),
        ],
        "maximum_sign_error": max(sign_errors),
        "maximum_distance_error": max(distance_errors),
        "raw_distance_ratio_range": [
            min(raw_distance_ratios),
            max(raw_distance_ratios),
        ],
        "maximum_excess_distance_error": max(excess_distance_errors),
        "maximum_reflection_rms_fraction": max(reflection_errors),
        "maximum_swap_rms_fraction": max(swap_errors),
        "phase_support": support,
        "excess_phase_support": excess_support,
    }
    return gates, diagnostics


def _inside(values: Iterable[float], minimum: float, maximum: float) -> bool:
    rows = [float(value) for value in values]
    return bool(
        rows
        and all(math.isfinite(value) and minimum <= value <= maximum for value in rows)
    )


def _trace_rms(values: Iterable[complex]) -> float:
    rows = [abs(complex(value)) ** 2 for value in values]
    return float(math.sqrt(math.fsum(rows) / len(rows))) if rows else math.inf


def decision_from_gates(gates: dict[str, bool]) -> P5DDecision:
    """Apply the frozen fail-closed decision precedence."""

    if not gates.get("pipeline", False):
        return "p5d-inconclusive"
    if not gates.get("ledger_and_reciprocity", False):
        return "p5d-ledger-or-reciprocity-fail"
    if not gates.get("loop_integrity", False):
        return "p5d-loop-integrity-fail"
    if not gates.get("directional_causality", False):
        return "p5d-directional-causality-fail"
    if not gates.get("mutual_hypothesis", False):
        return "p5d-mutual-hypothesis-fail"
    if not gates.get("closed_loop_excess", False):
        return "p5d-independent-superposition"
    if not gates.get("scaling", False):
        return "p5d-inconclusive"
    return "p5d-mutual-center-response-pass"


def classify_panel(
    *,
    registration: dict[str, Any],
    channel_off_arms: list[dict[str, Any]],
    active_arms: list[dict[str, Any]],
    response: dict[str, Any],
) -> tuple[P5DDecision, dict[str, bool]]:
    """Reduce raw arm, causality and response gates in registered order."""

    response_gates = response.get("gates", {})
    all_arms = channel_off_arms + active_arms
    pipeline = bool(
        registration.get("pass", False)
        and all(row.get("completed", False) for row in all_arms)
        and all(row.get("finite", False) for row in all_arms)
        and response.get("available", False)
        and response_gates.get("primary_resolved", False)
    )
    ledger = all(
        all(row.get("ledger_gates", {}).values())
        for row in active_arms
    )
    loop = all(
        all(row.get("loop_gates", {}).values())
        for row in all_arms
    )
    off_by_key = {_base_key(row): row for row in channel_off_arms}
    causality_checks = []
    for row in active_arms:
        if row["mode"] not in ("a_to_b", "b_to_a"):
            continue
        baseline = off_by_key[_base_key(row)]
        final = row["trace"][-1]
        control = baseline["trace"][-1]
        if row["mode"] == "a_to_b":
            source_hash = row["final_history_sha256_a"]
            control_hash = baseline["final_history_sha256_a"]
            source_trace_equal = all(
                sample["center_a"] == reference["center_a"]
                for sample, reference in zip(
                    row["trace"], baseline["trace"], strict=True
                )
            )
            response = abs(
                _complex(final["center_b"]) - _complex(control["center_b"])
            ) / float(row["initial_distance"])
        else:
            source_hash = row["final_history_sha256_b"]
            control_hash = baseline["final_history_sha256_b"]
            source_trace_equal = all(
                sample["center_b"] == reference["center_b"]
                for sample, reference in zip(
                    row["trace"], baseline["trace"], strict=True
                )
            )
            response = abs(
                _complex(final["center_a"]) - _complex(control["center_a"])
            ) / float(row["initial_distance"])
        causality_checks.append(
            bool(
                row.get("source_bitwise_native", False)
                and source_hash == control_hash
                and source_trace_equal
                and response >= THRESHOLDS.response_resolution
            )
        )
    causality = bool(causality_checks and all(causality_checks))
    mutual = bool(
        response_gates.get("reciprocal_low_signal", False)
        and response_gates.get("reciprocal_high_signal", False)
        and response_gates.get("one_way_low_signal", False)
        and response_gates.get("one_way_high_signal", False)
        and response_gates.get("phase_support", False)
        and response_gates.get("sign_symmetry", False)
        and response_gates.get("reflection_covariance", False)
        and response_gates.get("swap_covariance", False)
    )
    closed_loop = bool(
        response_gates.get("excess_resolved", False)
        and response_gates.get("excess_low_signal", False)
        and response_gates.get("excess_high_signal", False)
        and response_gates.get("excess_phase_support", False)
    )
    scaling = bool(
        response_gates.get("strength_scaling", False)
        and response_gates.get("distance_normalization", False)
        and response_gates.get("raw_distance_scaling", False)
        and response_gates.get("excess_strength_scaling", False)
        and response_gates.get("excess_response_fraction", False)
        and response_gates.get("excess_distance_normalization", False)
    )
    gates = {
        "pipeline": pipeline,
        "ledger_and_reciprocity": ledger,
        "loop_integrity": loop,
        "directional_causality": causality,
        "mutual_hypothesis": mutual,
        "closed_loop_excess": closed_loop,
        "scaling": scaling,
    }
    return decision_from_gates(gates), gates


def _initial_pair(
    key: tuple[int, int, int, int],
) -> tuple[np.ndarray, np.ndarray, OrbitCenterReadout, OrbitCenterReadout]:
    distance_fraction, phase_index, chirality_a, chirality_b = key
    distance = distance_fraction * CANDIDATE.radius
    phase = PHASES[phase_index]
    readout_a = candidate_orbit_center_readout(CANDIDATE, chirality=chirality_a)
    readout_b = candidate_orbit_center_readout(CANDIDATE, chirality=chirality_b)
    history_a = target_history(CANDIDATE, chirality=chirality_a)
    history_b = target_history(CANDIDATE, chirality=chirality_b)
    history_a = history_a @ rotation_matrix(phase).T
    history_b = history_b @ rotation_matrix(-phase).T
    target_a = complex(-0.5 * distance, 0.0)
    target_b = complex(0.5 * distance, 0.0)
    history_a = history_a + complex_to_vector(
        target_a - orbit_center(history_a, readout=readout_a)
    )
    history_b = history_b + complex_to_vector(
        target_b - orbit_center(history_b, readout=readout_b)
    )
    if np.shares_memory(history_a, history_b):
        raise AssertionError("P5-D pair histories must not share storage")
    return history_a, history_b, readout_a, readout_b


def _sample_loop(
    history: np.ndarray,
    *,
    chirality: int,
    readout: OrbitCenterReadout,
    targets: dict[int, np.ndarray],
) -> dict[str, Any]:
    own, alignment = rotation_translation_quotient_distance(
        history,
        targets[chirality],
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    opposite, _ = rotation_translation_quotient_distance(
        history,
        targets[-chirality],
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    return {
        "center": orbit_center(history, readout=readout),
        "own_d0_fraction": own / CANDIDATE.radius,
        "opposite_d0_fraction": opposite / CANDIDATE.radius,
        "alignment_phase": alignment,
    }


def _phase_metrics(trace: list[dict[str, Any]], role: str, chirality: int) -> dict[str, Any]:
    rows = [sample for sample in trace if sample["step"] >= THRESHOLDS.phase_start]
    if len(rows) < 2:
        return {"pass": False, "reason": "insufficient-phase-window"}
    steps = np.asarray([sample["step"] for sample in rows], dtype=float)
    angles = np.unwrap(
        np.asarray([sample[f"alignment_{role}"] for sample in rows], dtype=float)
    )
    increments = -np.diff(angles) / np.diff(steps)
    expected = chirality * CANDIDATE.theta
    mean_error = abs(float(np.mean(increments)) - expected)
    rms_error = float(np.sqrt(np.mean((increments - expected) ** 2)))
    return {
        "mean_error": mean_error,
        "rms_error": rms_error,
        "pass": bool(
            mean_error <= THRESHOLDS.phase_mean_error_fraction * CANDIDATE.theta
            and rms_error
            <= THRESHOLDS.phase_rms_error_fraction * CANDIDATE.theta
        ),
    }


def _step_ledger_metrics(
    step: MutualCenterStep,
    *,
    readout_a: OrbitCenterReadout,
    readout_b: OrbitCenterReadout,
) -> dict[str, float | bool]:
    metrology = mutual_center_rounding_metrology(
        step,
        readout_a=readout_a,
        readout_b=readout_b,
    )
    return {
        "work_split_a": abs(step.loop_a.work_split_residual),
        "work_split_b": abs(step.loop_b.work_split_residual),
        "pair_ledger": abs(step.pair_ledger_residual),
        "force_balance": abs(step.completed_force_balance_residual),
        "midpoint_a": abs(step.midpoint_force_residual_a),
        "midpoint_b": abs(step.midpoint_force_residual_b),
        "center_local_a": abs(metrology.loop_a.center_local_residual),
        "center_local_b": abs(metrology.loop_b.center_local_residual),
        "center_envelope_a": (
            abs(metrology.loop_a.center_full_residual)
            / metrology.loop_a.center_full_envelope
            if metrology.loop_a.center_full_envelope > 0.0
            else 0.0
        ),
        "center_envelope_b": (
            abs(metrology.loop_b.center_full_residual)
            / metrology.loop_b.center_full_envelope
            if metrology.loop_b.center_full_envelope > 0.0
            else 0.0
        ),
        "normal_operands": bool(
            metrology.loop_a.normal_operands and metrology.loop_b.normal_operands
        ),
        "minimum_dissipation": min(
            step.loop_a.write_mobility_dissipation,
            step.loop_b.write_mobility_dissipation,
        ),
        "omitted_age_a": abs(step.omitted_age_a_residual),
        "omitted_age_b": abs(step.omitted_age_b_residual),
        "omitted_both_ages": abs(step.omitted_both_ages_residual),
        "raw_center": abs(step.raw_center_ledger_residual),
        "one_way_without_reservoir": abs(step.closed_pair_ledger_residual),
        "flipped_force_a": abs(step.flipped_force_a_ledger_residual),
    }


def _run_arm(
    *,
    base_key: tuple[int, int, int, int],
    mode: MutualCenterMode,
    coupling: float,
    baseline: dict[str, Any] | None = None,
    high_precision_enabled: bool = False,
) -> dict[str, Any]:
    """Run one registered arm; callers must pass the provenance guard first."""

    distance_fraction, phase_index, chirality_a, chirality_b = base_key
    state_a, state_b, readout_a, readout_b = _initial_pair(base_key)
    targets = {
        chirality: target_history(CANDIDATE, chirality=chirality)
        for chirality in (1, -1)
    }
    initial_a = orbit_center(state_a, readout=readout_a)
    initial_b = orbit_center(state_b, readout=readout_b)
    initial_distance = abs(initial_a - initial_b)
    reference_a = state_a.copy()
    reference_b = state_b.copy()
    source_bitwise = True
    finite = True
    completed = False
    stop_reason: str | None = None
    trace: list[dict[str, Any]] = []
    internal_centers_a: list[complex] = []
    internal_centers_b: list[complex] = []
    ledger_maxima = {
        name: 0.0
        for name in (
            "work_split_a",
            "work_split_b",
            "pair_ledger",
            "force_balance",
            "midpoint_a",
            "midpoint_b",
            "center_local_a",
            "center_local_b",
            "center_envelope_a",
            "center_envelope_b",
        )
    }
    rival_maxima = {
        name: 0.0
        for name in (
            "omitted_age_a",
            "omitted_age_b",
            "omitted_both_ages",
            "raw_center",
            "one_way_without_reservoir",
            "flipped_force_a",
        )
    }
    cumulative = {"work_split_a": 0.0, "work_split_b": 0.0, "pair_ledger": 0.0}
    minimum_dissipation: float | None = None if mode == "off" else math.inf
    normal_operands = True
    ledger_evaluation_count = 0
    shape_evaluation_count = 0
    force_scale: float | None = None
    displacement_scale: float | None = None
    maximum_d0_a = maximum_d0_b = 0.0
    late_d0_a = late_d0_b = 0.0
    late_opposite_a = late_opposite_b = math.inf
    minimum_separation = initial_distance
    high_precision = []
    center_stationarity: float | None = None

    def measure(update: int, *, store: bool) -> None:
        nonlocal shape_evaluation_count
        nonlocal maximum_d0_a, maximum_d0_b
        nonlocal late_d0_a, late_d0_b, late_opposite_a, late_opposite_b
        loop_a = _sample_loop(
            state_a,
            chirality=chirality_a,
            readout=readout_a,
            targets=targets,
        )
        loop_b = _sample_loop(
            state_b,
            chirality=chirality_b,
            readout=readout_b,
            targets=targets,
        )
        shape_evaluation_count += 1
        maximum_d0_a = max(maximum_d0_a, loop_a["own_d0_fraction"])
        maximum_d0_b = max(maximum_d0_b, loop_b["own_d0_fraction"])
        if update >= THRESHOLDS.late_start:
            late_d0_a = max(late_d0_a, loop_a["own_d0_fraction"])
            late_d0_b = max(late_d0_b, loop_b["own_d0_fraction"])
            late_opposite_a = min(
                late_opposite_a, loop_a["opposite_d0_fraction"]
            )
            late_opposite_b = min(
                late_opposite_b, loop_b["opposite_d0_fraction"]
            )
        center_a = loop_a["center"]
        center_b = loop_b["center"]
        if store:
            trace.append(
                {
                    "step": update,
                    "center_a": _pair(center_a),
                    "center_b": _pair(center_b),
                    "separation": _pair(center_a - center_b),
                    "d0_a": loop_a["own_d0_fraction"],
                    "d0_b": loop_b["own_d0_fraction"],
                    "opposite_d0_a": loop_a["opposite_d0_fraction"],
                    "opposite_d0_b": loop_b["opposite_d0_fraction"],
                    "alignment_a": loop_a["alignment_phase"],
                    "alignment_b": loop_b["alignment_phase"],
                }
            )

    measure(0, store=True)
    internal_centers_a.append(initial_a)
    internal_centers_b.append(initial_b)
    energy_scale = max(
        0.5 * abs(coupling) * initial_distance**2,
        np.finfo(float).tiny,
    )
    for update in range(1, THRESHOLDS.active_updates + 1):
        ledger_violation = False
        if mode in ("off", "a_to_b"):
            reference_a = native_fifo_step(
                reference_a, **CANDIDATE.step_parameters()
            )
        if mode in ("off", "b_to_a"):
            reference_b = native_fifo_step(
                reference_b, **CANDIDATE.step_parameters()
            )
        step = mutual_center_step(
            state_a,
            state_b,
            candidate_a=CANDIDATE,
            candidate_b=CANDIDATE,
            readout_a=readout_a,
            readout_b=readout_b,
            coupling=coupling,
            mode=mode,
        )
        if mode in ("off", "a_to_b"):
            source_bitwise = bool(
                source_bitwise and np.array_equal(step.loop_a.history_after, reference_a)
            )
        if mode in ("off", "b_to_a"):
            source_bitwise = bool(
                source_bitwise and np.array_equal(step.loop_b.history_after, reference_b)
            )
        if mode != "off":
            ledger_evaluation_count += 1
            metrics = _step_ledger_metrics(
                step,
                readout_a=readout_a,
                readout_b=readout_b,
            )
            for name in ledger_maxima:
                ledger_maxima[name] = max(ledger_maxima[name], float(metrics[name]))
            for name in rival_maxima:
                rival_maxima[name] = max(rival_maxima[name], float(metrics[name]))
            for name in cumulative:
                if name == "pair_ledger":
                    cumulative[name] += step.pair_ledger_residual
                elif name == "work_split_a":
                    cumulative[name] += step.loop_a.work_split_residual
                else:
                    cumulative[name] += step.loop_b.work_split_residual
            minimum_dissipation = min(
                float(minimum_dissipation),
                float(metrics["minimum_dissipation"]),
            )
            normal_operands = bool(normal_operands and metrics["normal_operands"])
            if force_scale is None:
                force_scale = max(
                    abs(step.loop_a.center_force),
                    abs(step.loop_b.center_force),
                    np.finfo(float).tiny,
                )
                displacement_scale = max(
                    abs(step.loop_a.center_prescribed_increment),
                    abs(step.loop_b.center_prescribed_increment),
                    np.finfo(float).tiny,
                )
            ledger_violation = bool(
                not metrics["normal_operands"]
                or max(
                    float(metrics["center_envelope_a"]),
                    float(metrics["center_envelope_b"]),
                )
                > 1.0
                or float(metrics["force_balance"]) / force_scale
                > THRESHOLDS.force_relative
                or max(
                    float(metrics["midpoint_a"]),
                    float(metrics["midpoint_b"]),
                )
                / force_scale
                > THRESHOLDS.force_relative
                or max(
                    float(metrics["work_split_a"]),
                    float(metrics["work_split_b"]),
                )
                / energy_scale
                > THRESHOLDS.step_ledger_relative
                or float(metrics["pair_ledger"]) / energy_scale
                > THRESHOLDS.step_ledger_relative
                or float(metrics["minimum_dissipation"])
                < THRESHOLDS.minimum_mobility_dissipation
            )
            if high_precision_enabled and update in THRESHOLDS.reference_steps:
                reference = _high_precision_reference(
                    step,
                    readout_a=readout_a,
                    readout_b=readout_b,
                    update=update,
                )
                high_precision.append(reference)
                ledger_violation = bool(
                    ledger_violation or not reference["pass"]
                )
        state_a = step.loop_a.history_after
        state_b = step.loop_b.history_after
        center_a = step.loop_a.center_after
        center_b = step.loop_b.center_after
        internal_centers_a.append(center_a)
        internal_centers_b.append(center_b)
        finite = bool(
            finite
            and np.isfinite(state_a).all()
            and np.isfinite(state_b).all()
            and _all_finite(asdict(step))
        )
        if not finite:
            stop_reason = "nonfinite-state-or-ledger"
            break
        minimum_separation = min(minimum_separation, abs(center_a - center_b))
        if minimum_separation < THRESHOLDS.minimum_separation_fraction * CANDIDATE.radius:
            stop_reason = "collision-boundary"
            break
        measure(update, store=update % THRESHOLDS.sample_every == 0)
        if ledger_violation:
            stop_reason = "ledger-or-reciprocity-boundary"
            break
        if max(maximum_d0_a, maximum_d0_b) > THRESHOLDS.maximum_d0_fraction:
            stop_reason = "loop-shape-boundary"
            break
        if (
            update >= THRESHOLDS.late_start
            and min(late_opposite_a, late_opposite_b)
            < THRESHOLDS.opposite_d0_fraction
        ):
            stop_reason = "chirality-boundary"
            break
    else:
        completed = True

    phase_a = _phase_metrics(trace, "a", chirality_a)
    phase_b = _phase_metrics(trace, "b", chirality_b)
    force_scale = force_scale or np.finfo(float).tiny
    displacement_scale = displacement_scale or np.finfo(float).tiny
    if mode == "off":
        center_stationarity = max(
            max(abs(value - initial_a) for value in internal_centers_a),
            max(abs(value - initial_b) for value in internal_centers_b),
        ) / CANDIDATE.radius
        ledger_gates = {"not_applicable_channel_off": True}
        loop_gates = {
            "complete_shape_evaluation_count": shape_evaluation_count
            == THRESHOLDS.active_updates + 1,
            "bitwise_native": source_bitwise,
            "prepared_orbit": max(maximum_d0_a, maximum_d0_b)
            <= THRESHOLDS.channel_off_d0_fraction,
            "stationary_center": center_stationarity
            <= THRESHOLDS.channel_off_center_fraction,
        }
    else:
        if minimum_dissipation is None:
            raise AssertionError("active P5-D arm lacks mobility metrology")
        ledger_gates = {
            "complete_evaluation_count": ledger_evaluation_count
            == THRESHOLDS.active_updates,
            "normal_operands": normal_operands,
            "center_local": max(
                ledger_maxima["center_local_a"], ledger_maxima["center_local_b"]
            )
            / displacement_scale
            <= THRESHOLDS.center_local_relative,
            "center_full_envelope": max(
                ledger_maxima["center_envelope_a"],
                ledger_maxima["center_envelope_b"],
            )
            <= 1.0,
            "force_balance": ledger_maxima["force_balance"] / force_scale
            <= THRESHOLDS.force_relative,
            "midpoint_force": max(
                ledger_maxima["midpoint_a"], ledger_maxima["midpoint_b"]
            )
            / force_scale
            <= THRESHOLDS.force_relative,
            "work_split_step": max(
                ledger_maxima["work_split_a"], ledger_maxima["work_split_b"]
            )
            / energy_scale
            <= THRESHOLDS.step_ledger_relative,
            "pair_ledger_step": ledger_maxima["pair_ledger"] / energy_scale
            <= THRESHOLDS.step_ledger_relative,
            "work_split_cumulative": max(
                abs(cumulative["work_split_a"]), abs(cumulative["work_split_b"])
            )
            / energy_scale
            <= THRESHOLDS.cumulative_ledger_relative,
            "pair_ledger_cumulative": abs(cumulative["pair_ledger"])
            / energy_scale
            <= THRESHOLDS.cumulative_ledger_relative,
            "nonnegative_mobility": minimum_dissipation
            >= THRESHOLDS.minimum_mobility_dissipation,
            "high_precision_references": bool(
                not high_precision_enabled
                or (
                    len(high_precision) == len(THRESHOLDS.reference_steps)
                    and all(row["pass"] for row in high_precision)
                )
            ),
        }
        loop_gates = {
            "complete_shape_evaluation_count": shape_evaluation_count
            == THRESHOLDS.active_updates + 1,
            "maximum_d0": max(maximum_d0_a, maximum_d0_b)
            <= THRESHOLDS.maximum_d0_fraction,
            "late_d0": max(late_d0_a, late_d0_b)
            <= THRESHOLDS.late_d0_fraction,
            "opposite_chirality": min(late_opposite_a, late_opposite_b)
            >= THRESHOLDS.opposite_d0_fraction,
            "phase_a": bool(phase_a["pass"]),
            "phase_b": bool(phase_b["pass"]),
            "separation": minimum_separation
            >= THRESHOLDS.minimum_separation_fraction * CANDIDATE.radius,
        }

    rival_fractions = {
        name: value / energy_scale for name, value in rival_maxima.items()
    }
    rival_resolved = {
        name: value > THRESHOLDS.step_ledger_relative
        for name, value in rival_fractions.items()
    }

    maximum_center_response = None
    receiver_response_resolved = mode == "off"
    if baseline is not None and completed:
        baseline_a = baseline["_internal_centers_a"]
        baseline_b = baseline["_internal_centers_b"]
        response_a = [
            abs(value - reference)
            for value, reference in zip(internal_centers_a, baseline_a, strict=True)
        ]
        response_b = [
            abs(value - reference)
            for value, reference in zip(internal_centers_b, baseline_b, strict=True)
        ]
        maximum_center_response = max(max(response_a), max(response_b)) / initial_distance
        loop_gates["center_response_bound"] = (
            maximum_center_response <= THRESHOLDS.maximum_center_response_fraction
        )
        if mode == "a_to_b":
            receiver_response_resolved = response_b[-1] / initial_distance >= (
                THRESHOLDS.response_resolution
            )
        elif mode == "b_to_a":
            receiver_response_resolved = response_a[-1] / initial_distance >= (
                THRESHOLDS.response_resolution
            )
        else:
            receiver_response_resolved = True

    result = {
        "distance_fraction": distance_fraction,
        "phase_index": phase_index,
        "phase": PHASES[phase_index],
        "chirality_a": chirality_a,
        "chirality_b": chirality_b,
        "mode": mode,
        "coupling": coupling,
        "initial_distance": initial_distance,
        "completed": completed,
        "finite": finite,
        "stopped": not completed,
        "stop_reason": stop_reason,
        "source_bitwise_native": source_bitwise,
        "receiver_response_resolved": receiver_response_resolved,
        "final_history_sha256_a": _history_sha256(state_a),
        "final_history_sha256_b": _history_sha256(state_b),
        "trace": trace,
        "ledger_maxima": ledger_maxima,
        "ledger_cumulative": cumulative,
        "ledger_rival_maxima": rival_maxima,
        "ledger_rival_fractions": rival_fractions,
        "ledger_rival_resolved": rival_resolved,
        "ledger_evaluation_count": ledger_evaluation_count,
        "shape_evaluation_count": shape_evaluation_count,
        "ledger_scales": {
            "energy": energy_scale,
            "force": force_scale,
            "displacement": displacement_scale,
        },
        "minimum_mobility_dissipation": minimum_dissipation,
        "normal_metrology_operands": normal_operands,
        "ledger_gates": ledger_gates,
        "loop_gates": loop_gates,
        "loop_summary": {
            "maximum_d0_a": maximum_d0_a,
            "maximum_d0_b": maximum_d0_b,
            "late_d0_a": late_d0_a,
            "late_d0_b": late_d0_b,
            "late_opposite_a": late_opposite_a,
            "late_opposite_b": late_opposite_b,
            "center_stationarity_fraction": center_stationarity,
        },
        "phase_metrics": {"a": phase_a, "b": phase_b},
        "minimum_separation": minimum_separation,
        "maximum_center_response_fraction": maximum_center_response,
        "high_precision_references": high_precision,
        "_internal_centers_a": internal_centers_a,
        "_internal_centers_b": internal_centers_b,
    }
    return result


def _high_precision_reference(
    step: MutualCenterStep,
    *,
    readout_a: OrbitCenterReadout,
    readout_b: OrbitCenterReadout,
    update: int,
) -> dict[str, Any]:
    """Re-evaluate stored binary64 center dots and midpoint identities at 80 dps."""

    with mp.workdps(THRESHOLDS.reference_dps):
        def dot(coefficients: np.ndarray, history: np.ndarray) -> mp.mpc:
            total = mp.mpc(0)
            for coefficient, point in zip(coefficients, history, strict=True):
                total += mp.mpc(str(coefficient.real), str(coefficient.imag)) * mp.mpc(
                    str(point[0]), str(point[1])
                )
            return total

        before_a = dot(readout_a.coefficients, step.loop_a.history_before)
        before_b = dot(readout_b.coefficients, step.loop_b.history_before)
        after_a = dot(readout_a.coefficients, step.loop_a.history_after)
        after_b = dot(readout_b.coefficients, step.loop_b.history_after)
        force_a = mp.mpc(
            str(step.loop_a.center_force.real), str(step.loop_a.center_force.imag)
        )
        force_b = mp.mpc(
            str(step.loop_b.center_force.real), str(step.loop_b.center_force.imag)
        )
        reservoir_a = mp.mpc(
            str(step.reservoir_force_a.real), str(step.reservoir_force_a.imag)
        )
        reservoir_b = mp.mpc(
            str(step.reservoir_force_b.real), str(step.reservoir_force_b.imag)
        )
        strength = mp.mpf(str(step.coupling))
        separation_before = before_a - before_b
        separation_after = after_a - after_b
        gradient_a = -strength * (separation_before + separation_after) / 2
        midpoint_a = abs(force_a + reservoir_a - gradient_a)
        midpoint_b = abs(force_b + reservoir_b + gradient_a)
        balance = abs(force_a + force_b + reservoir_a + reservoir_b)
        force_scale = max(
            abs(force_a),
            abs(force_b),
            abs(reservoir_a),
            abs(reservoir_b),
            mp.mpf("1e-100"),
        )
        tolerance = mp.mpf(str(THRESHOLDS.force_relative)) * force_scale
        return {
            "update": int(update),
            "precision_dps": THRESHOLDS.reference_dps,
            "midpoint_a_residual": float(midpoint_a),
            "midpoint_b_residual": float(midpoint_b),
            "completed_force_balance_residual": float(balance),
            "relative_tolerance": float(tolerance / force_scale),
            "pass": bool(
                midpoint_a <= tolerance
                and midpoint_b <= tolerance
                and balance <= tolerance
            ),
        }


def _strip_internal(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if not key.startswith("_")}


def _run_registered_panel() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    channel_off = []
    active = []
    baselines: dict[tuple[int, int, int, int], dict[str, Any]] = {}
    for base in expected_base_keys():
        arm = _run_arm(base_key=base, mode="off", coupling=0.0)
        if not arm["completed"]:
            raise RuntimeError(
                f"P5-D channel-off arm stopped before completion: {base}"
            )
        baselines[base] = arm
        channel_off.append(arm)
    for key in expected_active_keys():
        base = key[:4]
        kappa_name = key[4]
        sign = key[5]
        mode = key[6]
        arm = _run_arm(
            base_key=base,
            mode=mode,  # type: ignore[arg-type]
            coupling=sign * KAPPA_VALUES[kappa_name],
            baseline=baselines[base],
            high_precision_enabled=(
                kappa_name == "high" and sign == 1 and mode == "reciprocal"
            ),
        )
        arm["kappa_name"] = kappa_name
        arm["sign"] = sign
        if not arm["completed"]:
            raise RuntimeError(f"P5-D active arm stopped before completion: {key}")
        active.append(arm)
    return (
        [_strip_internal(row) for row in channel_off],
        [_strip_internal(row) for row in active],
    )


def _git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _git_blob(path: str, revision: str = "HEAD") -> str:
    return _git("rev-parse", f"{revision}:{path}")


def _parse_readiness_review(text: str) -> dict[str, Any]:
    revision = re.search(r"Implementation revision: `([0-9a-f]{40})`", text)
    verdict = re.search(r"Verdict: \*\*`([^`]+)`\*\*", text)
    ci_run = re.search(r"actions/runs/(\d+)", text)
    blobs = dict(re.findall(r"Blob `([^`]+)`: `([0-9a-f]{40})`", text))
    if revision is None or verdict is None or ci_run is None:
        raise RuntimeError("P5-D readiness review is incomplete")
    if verdict.group(1) != "p5d-implementation-ready":
        raise RuntimeError("P5-D implementation readiness is not upheld")
    missing = sorted(set(IMPLEMENTATION_PATHS) - set(blobs))
    if missing:
        raise RuntimeError(f"P5-D readiness review lacks blobs: {missing}")
    return {
        "implementation_revision": revision.group(1),
        "ci_run": ci_run.group(1),
        "verdict": verdict.group(1),
        "blobs": blobs,
    }


def _load_governance(path: Path | None = None) -> dict[str, Any]:
    """Load the exact executable governance record and fail closed."""

    source = ROOT / GOVERNANCE if path is None else path
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError("P5-D governance is unreadable") from error
    if type(payload) is not dict or set(payload) != GOVERNANCE_KEYS:
        raise RuntimeError("P5-D governance has invalid top-level keys")
    if payload["schema"] != GOVERNANCE_SCHEMA or payload["gate"] != "P5-D":
        raise RuntimeError("P5-D governance identity mismatch")
    if type(payload["reason"]) is not str or not payload["reason"]:
        raise RuntimeError("P5-D governance reason must be a nonempty string")
    if type(payload["target_authorized"]) is not bool:
        raise RuntimeError("P5-D governance authorization flag must be Boolean")
    if type(payload["target_calls_recorded"]) is not list:
        raise RuntimeError("P5-D governance incidents must be a list")
    incidents = payload["target_calls_recorded"]
    if len(incidents) != len(EXPECTED_INCIDENTS):
        raise RuntimeError("P5-D governance incident count mismatch")
    for row, expected in zip(incidents, EXPECTED_INCIDENTS, strict=True):
        if type(row) is not dict or set(row) != INCIDENT_KEYS:
            raise RuntimeError("P5-D governance incident keys mismatch")
        attempt, incident_path, incident_blob, status = expected
        if row != {
            "attempt": attempt,
            "incident_blob": incident_blob,
            "incident_path": incident_path,
            "status": status,
        }:
            raise RuntimeError(f"P5-D governance attempt {attempt} mismatch")
        if _git_blob(incident_path) != incident_blob:
            raise RuntimeError(f"P5-D governance incident {attempt} blob mismatch")
    state = payload["state"]
    if state not in {"closed", "authorized_once"}:
        raise RuntimeError("P5-D governance state is unregistered")
    if state == "closed":
        if payload["target_authorized"] is not False:
            raise RuntimeError("P5-D closed governance cannot authorize target")
        if payload["authorization"] is not None:
            raise RuntimeError("P5-D closed governance must have null authorization")
    return payload


def _require_target_authorization() -> dict[str, Any]:
    """Enforce the machine record before any legacy provenance or target work."""

    governance = _load_governance()
    if governance["state"] == "closed":
        raise RuntimeError("P5-D target sealed by machine governance")
    if governance["target_authorized"] is not True:
        raise RuntimeError("P5-D target is not authorized")
    raise RuntimeError("P5-D authorized-once verification is not implemented")


def _verify_provenance() -> dict[str, Any]:
    """Fail before pair initialization unless every frozen guard is green."""

    _require_target_authorization()

    if (
        _git_blob(RECOVERY_PROTOCOL.as_posix(), RECOVERY_PROTOCOL_REVISION)
        != RECOVERY_PROTOCOL_BLOB
    ):
        raise RuntimeError("P5-D recovery protocol freeze blob mismatch")
    if _git_blob(RECOVERY_PROTOCOL.as_posix()) != RECOVERY_PROTOCOL_BLOB:
        raise RuntimeError("P5-D recovery protocol changed after freeze")
    if not (ROOT / READINESS_REVIEW).exists():
        raise RuntimeError(
            "P5-D replacement target sealed: recovery readiness does not exist"
        )
    if _git_blob(PROTOCOL.as_posix(), PROTOCOL_FREEZE_REVISION) != PROTOCOL_FREEZE_BLOB:
        raise RuntimeError("P5-D protocol freeze blob mismatch")
    for path, expected in EXPECTED_HEAD_BLOBS.items():
        if _git_blob(path) != expected:
            raise RuntimeError(f"P5-D frozen dependency changed: {path}")
    if _git_blob(PROTOCOL.as_posix()) != PROTOCOL_FREEZE_BLOB:
        raise RuntimeError("P5-D protocol changed after its correction freeze")
    readiness = _parse_readiness_review(
        (ROOT / READINESS_REVIEW).read_text(encoding="utf-8")
    )
    revision = readiness["implementation_revision"]
    if _git("merge-base", "--is-ancestor", PROTOCOL_FREEZE_REVISION, revision) != "":
        raise RuntimeError("unexpected merge-base output")
    for path, expected in readiness["blobs"].items():
        if _git_blob(path, revision) != expected or _git_blob(path) != expected:
            raise RuntimeError(f"P5-D implementation blob mismatch: {path}")
    if _git("status", "--porcelain"):
        raise RuntimeError("P5-D target requires a clean worktree")
    upstream = _git("rev-parse", "@{upstream}")
    head = _git("rev-parse", "HEAD")
    if upstream != head:
        raise RuntimeError("P5-D target requires exact upstream synchronization")
    _validate_default_output_paths(DEFAULT_SUMMARY, DEFAULT_REPORT)
    return {
        "revision": head,
        "protocol_revision": PROTOCOL_FREEZE_REVISION,
        "protocol_blob": PROTOCOL_FREEZE_BLOB,
        "recovery_protocol_revision": RECOVERY_PROTOCOL_REVISION,
        "recovery_protocol_blob": RECOVERY_PROTOCOL_BLOB,
        "first_target_status": "p5d-inconclusive-serialization-failure",
        "readiness": readiness,
        "upstream_revision": upstream,
        "clean": True,
    }


def _validate_default_output_paths(summary: Path, report: Path) -> None:
    summary_path = summary if summary.is_absolute() else ROOT / summary
    report_path = report if report.is_absolute() else ROOT / report
    if summary_path.resolve() != (ROOT / DEFAULT_SUMMARY).resolve():
        raise RuntimeError("P5-D permits only the registered JSON output")
    if report_path.resolve() != (ROOT / DEFAULT_REPORT).resolve():
        raise RuntimeError("P5-D permits only the registered report output")
    if summary_path.exists() or report_path.exists():
        raise RuntimeError("refusing to overwrite registered P5-D outputs")


def _write_complete_outputs(
    *,
    summary_path: Path,
    summary_content: str,
    report_path: Path,
    report_content: str,
) -> None:
    paths = (summary_path, report_path)
    if any(path.exists() for path in paths):
        raise RuntimeError("refusing existing P5-D output")
    temporary = tuple(path.with_name(path.name + ".tmp") for path in paths)
    if any(path.exists() for path in temporary):
        raise RuntimeError("refusing stale P5-D temporary output")
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    try:
        temporary[0].write_text(summary_content, encoding="utf-8")
        temporary[1].write_text(report_content, encoding="utf-8")
        json.loads(temporary[0].read_text(encoding="utf-8"))
        if not temporary[1].read_text(encoding="utf-8").startswith("# P5-D"):
            raise RuntimeError("P5-D report validation failed")
        temporary[0].replace(paths[0])
        temporary[1].replace(paths[1])
    except Exception:
        for path in temporary:
            if path.exists():
                path.unlink()
        raise


def _render_report(payload: dict[str, Any], json_sha256: str) -> str:
    response = payload["response"]
    lines = [
        "# P5-D mutual-center result",
        "",
        f"Decision: **`{payload['decision']}`**.",
        "",
        f"JSON SHA256: `{json_sha256}`",
        "",
        "This is one deterministic control panel, not a replication series.",
        "The coupling is explicitly inserted; no spontaneous force, charge,",
        "spin, momentum, inertia or mass follows from this result.",
        "",
    ]
    if response["available"]:
        diagnostics = response["diagnostics"]
        lines.extend(
            (
                "Response status: `available`.",
                "",
                "Maximum reflection RMS/R: "
                f"`{diagnostics['maximum_reflection_rms_fraction']}`",
                "Maximum swap RMS/R: "
                f"`{diagnostics['maximum_swap_rms_fraction']}`",
                "Closed-loop low/high range: "
                f"`{diagnostics['excess_low_high_range']}`",
                "",
            )
        )
    else:
        lines.extend(
            (
                "Response status: `unavailable`.",
                f"Reason: `{response['reason']}`.",
                "No response diagnostics were evaluated.",
                "",
            )
        )
    return "\n".join(lines)


def _json_default(value: Any) -> bool | int | float:
    """Convert only frozen NumPy scalar families for standard JSON output."""

    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    raise TypeError(
        f"Object of type {value.__class__.__name__} is not JSON serializable"
    )


def _serialize_payload(payload: dict[str, Any]) -> str:
    """Serialize the complete payload under the recovery freeze."""

    return json.dumps(
        payload,
        allow_nan=False,
        default=_json_default,
        indent=2,
        sort_keys=True,
    ) + "\n"


def run_gate(
    *,
    summary_path: Path = DEFAULT_SUMMARY,
    report_path: Path = DEFAULT_REPORT,
) -> dict[str, Any]:
    """Run the single registered panel after the sealed provenance guard."""

    provenance = _verify_provenance()
    channel_off, active = _run_registered_panel()
    registration = panel_registration(
        channel_off,
        active,
        require_references=True,
    )
    response = response_controls(
        channel_off,
        active,
        require_references=True,
    )
    decision, gates = classify_panel(
        registration=registration,
        channel_off_arms=channel_off,
        active_arms=active,
        response=response,
    )
    payload = {
        "schema": "scalar-memory-loop-p5d-mutual-center-v1",
        "created_utc": datetime.now(UTC).isoformat(),
        "provenance": provenance,
        "candidate": asdict(CANDIDATE),
        "thresholds": asdict(THRESHOLDS),
        "panel": {
            "channel_off_arms": channel_off,
            "active_arms": active,
        },
        "registration": registration,
        "response": response,
        "decision_gates": gates,
        "decision": decision,
        "claim_boundary": (
            "explicit operational mutual-center architecture only; no spontaneous "
            "interaction, charge, spin, momentum, inertia or mass"
        ),
    }
    summary_content = _serialize_payload(payload)
    digest = hashlib.sha256(summary_content.encode("utf-8")).hexdigest()
    report_content = _render_report(payload, digest)
    summary = summary_path if summary_path.is_absolute() else ROOT / summary_path
    report = report_path if report_path.is_absolute() else ROOT / report_path
    _write_complete_outputs(
        summary_path=summary,
        summary_content=summary_content,
        report_path=report,
        report_content=report_content,
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    _validate_default_output_paths(args.summary, args.report)
    result = run_gate(summary_path=args.summary, report_path=args.report)
    print(json.dumps({"decision": result["decision"]}))


if __name__ == "__main__":
    main()
