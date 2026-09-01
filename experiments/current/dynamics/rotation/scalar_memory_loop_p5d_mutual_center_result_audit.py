"""Independently reconstruct a P5-D decision from the immutable raw JSON.

This module intentionally does not import the target runner or its decision
helpers.  It duplicates the frozen panel, response, symmetry and precedence
rules using only the Python standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[4]
RESULT = ROOT / (
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p5d_mutual_center_2026-09-01.json"
)
REPORT = RESULT.with_suffix(".md")
DEFAULT_OUTPUT = ROOT / (
    "reports/project/meta/reviews/"
    "scalar_memory_loop_p5d_mutual_center_independent_recompute_2026-09-01.json"
)

RADIUS = float(
    "0.946517504804223960990626662735384935160072399313332184824852189820406"
    "142783597632634323623097735558253263801"
)
DISTANCES = (3, 6)
CHIRALITIES = ((1, 1), (1, -1), (-1, 1), (-1, -1))
KAPPAS = ("low", "high")
SIGNS = (1, -1)
MODES = ("a_to_b", "b_to_a", "reciprocal")
ACTIVE_UPDATES = 2_000
SAMPLE_EVERY = 20
LATE_START = 1_800
RESPONSE_RESOLUTION = 1.0e-12


def _base_keys() -> list[tuple[int, int, int, int]]:
    return [
        (distance, phase, chirality_a, chirality_b)
        for distance in DISTANCES
        for phase in range(8)
        for chirality_a, chirality_b in CHIRALITIES
    ]


def _active_keys() -> list[tuple[int, int, int, int, str, int, str]]:
    return [
        (*base, kappa, sign, mode)
        for base in _base_keys()
        for kappa in KAPPAS
        for sign in SIGNS
        for mode in MODES
    ]


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


def _reflection(key: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    distance, phase, chirality_a, chirality_b = key
    return distance, 7 - phase, -chirality_a, -chirality_b


def _swap(key: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    distance, phase, chirality_a, chirality_b = key
    return distance, (3 - phase) % 8, chirality_b, chirality_a


def _swap_mode(mode: str) -> str:
    return {"a_to_b": "b_to_a", "b_to_a": "a_to_b"}.get(mode, mode)


def _complex(value: Iterable[float]) -> complex:
    row = tuple(float(item) for item in value)
    if len(row) != 2 or not all(math.isfinite(item) for item in row):
        raise ValueError("invalid complex pair")
    return complex(*row)


def _finite(value: Any) -> bool:
    if value is None or isinstance(value, (str, bool)):
        return True
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    if isinstance(value, dict):
        return all(_finite(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return all(_finite(item) for item in value)
    return True


def _rms(values: Iterable[complex | float]) -> float:
    rows = [abs(value) ** 2 for value in values]
    return math.sqrt(math.fsum(rows) / len(rows)) if rows else math.inf


def _inside(values: Iterable[float], minimum: float, maximum: float) -> bool:
    rows = list(values)
    return bool(
        rows
        and all(math.isfinite(value) and minimum <= value <= maximum for value in rows)
    )


def _registration(
    off: list[dict[str, Any]],
    active: list[dict[str, Any]],
    *,
    require_references: bool,
) -> dict[str, bool]:
    expected_steps = list(range(0, ACTIVE_UPDATES + 1, SAMPLE_EVERY))
    off_keys = [_base_key(row) for row in off]
    active_keys = [_active_key(row) for row in active]
    traces = off + active
    reference_rows = [
        reference
        for row in active
        for reference in row.get("high_precision_references", [])
    ]
    return {
        "channel_off_count": len(off) == 64,
        "active_count": len(active) == 768,
        "channel_off_order": off_keys == _base_keys(),
        "active_order": active_keys == _active_keys(),
        "channel_off_unique": len(off_keys) == len(set(off_keys)),
        "active_unique": len(active_keys) == len(set(active_keys)),
        "complete_trace_grids": all(
            [int(sample["step"]) for sample in row.get("trace", [])]
            == expected_steps
            for row in traces
        ),
        "finite": _finite(traces),
        "high_precision_references": bool(
            not require_references
            or (
                len(reference_rows) == 192
                and all(reference.get("pass", False) for reference in reference_rows)
                and all(
                    len(row.get("high_precision_references", []))
                    == (
                        3
                        if row.get("kappa_name") == "high"
                        and row.get("sign") == 1
                        and row.get("mode") == "reciprocal"
                        else 0
                    )
                    for row in active
                )
            )
        ),
    }


def _responses(
    off_rows: list[dict[str, Any]],
    active_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    off = {_base_key(row): row for row in off_rows}
    active = {_active_key(row): row for row in active_rows}
    traces: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    finals: dict[tuple[Any, ...], float] = {}
    for key in _active_keys():
        arm = active[key]
        control = off[key[:4]]
        distance = float(arm["initial_distance"])
        e0 = _complex(control["trace"][0]["separation"])
        e0 /= abs(e0)
        sign = 1.0 if float(arm["coupling"]) > 0.0 else -1.0
        trace = []
        for sample, baseline in zip(arm["trace"], control["trace"], strict=True):
            delta = _complex(sample["separation"]) - _complex(
                baseline["separation"]
            )
            trace.append(
                {
                    "step": int(sample["step"]),
                    "delta": delta,
                    "longitudinal": -sign
                    * (delta * e0.conjugate()).real
                    / distance,
                }
            )
        traces[key] = trace
        finals[key] = float(trace[-1]["longitudinal"])

    excess_traces: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    excess_finals: dict[tuple[Any, ...], float] = {}
    for base in _base_keys():
        distance = float(off[base]["initial_distance"])
        e0 = _complex(off[base]["trace"][0]["separation"])
        e0 /= abs(e0)
        for kappa in KAPPAS:
            for sign in SIGNS:
                prefix = (*base, kappa, sign)
                trace = []
                for ab, ba, rec in zip(
                    traces[(*prefix, "a_to_b")],
                    traces[(*prefix, "b_to_a")],
                    traces[(*prefix, "reciprocal")],
                    strict=True,
                ):
                    excess = rec["delta"] - ab["delta"] - ba["delta"]
                    trace.append(
                        {
                            "step": rec["step"],
                            "value": excess,
                            "longitudinal": (excess * e0.conjugate()).real
                            / distance,
                        }
                    )
                excess_traces[prefix] = trace
                excess_finals[prefix] = float(trace[-1]["longitudinal"])

    minima = {
        "reciprocal_low": min(
            value
            for key, value in finals.items()
            if key[4] == "low" and key[6] == "reciprocal"
        ),
        "reciprocal_high": min(
            value
            for key, value in finals.items()
            if key[4] == "high" and key[6] == "reciprocal"
        ),
        "one_way_low": min(
            value
            for key, value in finals.items()
            if key[4] == "low" and key[6] != "reciprocal"
        ),
        "one_way_high": min(
            value
            for key, value in finals.items()
            if key[4] == "high" and key[6] != "reciprocal"
        ),
        "excess_low": min(
            value for key, value in excess_finals.items() if key[4] == "low"
        ),
        "excess_high": min(
            value for key, value in excess_finals.items() if key[4] == "high"
        ),
    }

    low_high = []
    excess_low_high = []
    excess_fraction = []
    sign_errors = []
    for base in _base_keys():
        for sign in SIGNS:
            for mode in MODES:
                low = finals[(*base, "low", sign, mode)]
                high = finals[(*base, "high", sign, mode)]
                low_high.append(low / high if high else math.nan)
            low_x = excess_finals[(*base, "low", sign)]
            high_x = excess_finals[(*base, "high", sign)]
            rec = finals[(*base, "high", sign, "reciprocal")]
            excess_low_high.append(low_x / high_x if high_x else math.nan)
            excess_fraction.append(high_x / rec if rec else math.nan)
        for kappa in KAPPAS:
            for mode in MODES:
                plus = finals[(*base, kappa, 1, mode)]
                minus = finals[(*base, kappa, -1, mode)]
                scale = max(abs(plus), abs(minus), 5e-324)
                sign_errors.append(abs(plus - minus) / scale)

    reflection_errors = []
    swap_errors = []
    for key in _active_keys():
        reflected = (*_reflection(key[:4]), *key[4:])
        swapped = (*_swap(key[:4]), key[4], key[5], _swap_mode(key[6]))
        reflection_errors.append(
            _rms(
                left["delta"] - right["delta"].conjugate()
                for left, right in zip(
                    traces[key], traces[reflected], strict=True
                )
            )
            / RADIUS
        )
        swap_errors.append(
            _rms(
                left["delta"] - right["delta"]
                for left, right in zip(traces[key], traces[swapped], strict=True)
            )
            / RADIUS
        )

    distance_errors = []
    raw_distance_ratios = []
    excess_distance_errors = []
    for phase in range(8):
        for chirality_a, chirality_b in CHIRALITIES:
            for kappa in KAPPAS:
                for sign in SIGNS:
                    for mode in MODES:
                        small = finals[
                            (3, phase, chirality_a, chirality_b, kappa, sign, mode)
                        ]
                        large = finals[
                            (6, phase, chirality_a, chirality_b, kappa, sign, mode)
                        ]
                        scale = max(abs(small), abs(large), 5e-324)
                        distance_errors.append(abs(small - large) / scale)
                        raw_distance_ratios.append(
                            2.0 * large / small if small else math.nan
                        )
                    small_x = excess_finals[
                        (3, phase, chirality_a, chirality_b, kappa, sign)
                    ]
                    large_x = excess_finals[
                        (6, phase, chirality_a, chirality_b, kappa, sign)
                    ]
                    scale_x = max(abs(small_x), abs(large_x), 5e-324)
                    excess_distance_errors.append(abs(small_x - large_x) / scale_x)

    support = []
    excess_support = []
    for distance in DISTANCES:
        for chirality_a, chirality_b in CHIRALITIES:
            for kappa in KAPPAS:
                for sign in SIGNS:
                    support.append(
                        sum(
                            finals[
                                (
                                    distance,
                                    phase,
                                    chirality_a,
                                    chirality_b,
                                    kappa,
                                    sign,
                                    "reciprocal",
                                )
                            ]
                            > 0.0
                            for phase in range(8)
                        )
                    )
                    excess_support.append(
                        sum(
                            excess_finals[
                                (
                                    distance,
                                    phase,
                                    chirality_a,
                                    chirality_b,
                                    kappa,
                                    sign,
                                )
                            ]
                            > 0.0
                            for phase in range(8)
                        )
                    )

    gates = {
        "primary_resolved": all(abs(value) >= RESPONSE_RESOLUTION for value in finals.values()),
        "reciprocal_low_signal": minima["reciprocal_low"] >= 0.0025,
        "reciprocal_high_signal": minima["reciprocal_high"] >= 0.005,
        "one_way_low_signal": minima["one_way_low"] >= 0.00125,
        "one_way_high_signal": minima["one_way_high"] >= 0.0025,
        "phase_support": min(support) >= 6,
        "strength_scaling": _inside(low_high, 0.35, 0.65),
        "sign_symmetry": max(sign_errors) <= 0.05,
        "distance_normalization": max(distance_errors) <= 0.10,
        "raw_distance_scaling": _inside(raw_distance_ratios, 1.8, 2.2),
        "reflection_covariance": max(reflection_errors) <= 1.0e-11,
        "swap_covariance": max(swap_errors) <= 1.0e-11,
        "excess_resolved": all(
            abs(value) >= RESPONSE_RESOLUTION for value in excess_finals.values()
        ),
        "excess_low_signal": minima["excess_low"] >= 2.0e-6,
        "excess_high_signal": minima["excess_high"] >= 1.0e-5,
        "excess_phase_support": min(excess_support) >= 6,
        "excess_strength_scaling": _inside(excess_low_high, 0.10, 0.40),
        "excess_response_fraction": _inside(excess_fraction, 5.0e-4, 0.02),
        "excess_distance_normalization": max(excess_distance_errors) <= 0.20,
    }
    return {
        "gates": gates,
        "minima": minima,
        "maximum_reflection_rms_fraction": max(reflection_errors),
        "maximum_swap_rms_fraction": max(swap_errors),
        "excess_low_high_range": [min(excess_low_high), max(excess_low_high)],
    }


def _causality(off_rows: list[dict[str, Any]], active_rows: list[dict[str, Any]]) -> bool:
    off = {_base_key(row): row for row in off_rows}
    checks = []
    for row in active_rows:
        mode = row["mode"]
        if mode not in ("a_to_b", "b_to_a"):
            continue
        control = off[_base_key(row)]
        if mode == "a_to_b":
            role = "a"
            receiver = "b"
        else:
            role = "b"
            receiver = "a"
        source_equal = all(
            sample[f"center_{role}"] == reference[f"center_{role}"]
            for sample, reference in zip(row["trace"], control["trace"], strict=True)
        )
        hash_equal = row[f"final_history_sha256_{role}"] == control[
            f"final_history_sha256_{role}"
        ]
        response = abs(
            _complex(row["trace"][-1][f"center_{receiver}"])
            - _complex(control["trace"][-1][f"center_{receiver}"])
        ) / float(row["initial_distance"])
        checks.append(
            bool(
                row.get("source_bitwise_native", False)
                and source_equal
                and hash_equal
                and response >= RESPONSE_RESOLUTION
            )
        )
    return bool(checks and all(checks))


def _recompute_arm_gates(
    row: dict[str, Any],
    *,
    strict_numeric: bool,
) -> tuple[dict[str, bool], dict[str, bool]]:
    """Rebuild local numeric gates without trusting stored gate booleans."""

    if not strict_numeric:
        return (
            {key: bool(value) for key, value in row["ledger_gates"].items()},
            {key: bool(value) for key, value in row["loop_gates"].items()},
        )
    mode = str(row["mode"])
    summary = row["loop_summary"]
    if mode == "off":
        ledger = {"not_applicable_channel_off": True}
        loop = {
            "complete_shape_evaluation_count": int(
                row["shape_evaluation_count"]
            )
            == ACTIVE_UPDATES + 1,
            "bitwise_native": bool(row["source_bitwise_native"]),
            "prepared_orbit": max(
                float(summary["maximum_d0_a"]),
                float(summary["maximum_d0_b"]),
            )
            <= 1.0e-10,
            "stationary_center": float(summary["center_stationarity_fraction"])
            <= 1.0e-10,
        }
        return ledger, loop

    maxima = row["ledger_maxima"]
    cumulative = row["ledger_cumulative"]
    scales = row["ledger_scales"]
    force_scale = float(scales["force"])
    displacement_scale = float(scales["displacement"])
    energy_scale = float(scales["energy"])
    references = row["high_precision_references"]
    references_expected = (
        row["kappa_name"] == "high"
        and int(row["sign"]) == 1
        and mode == "reciprocal"
    )
    ledger = {
        "complete_evaluation_count": int(row["ledger_evaluation_count"])
        == ACTIVE_UPDATES,
        "normal_operands": bool(row["normal_metrology_operands"]),
        "center_local": max(
            float(maxima["center_local_a"]),
            float(maxima["center_local_b"]),
        )
        / displacement_scale
        <= 5.0e-12,
        "center_full_envelope": max(
            float(maxima["center_envelope_a"]),
            float(maxima["center_envelope_b"]),
        )
        <= 1.0,
        "force_balance": float(maxima["force_balance"]) / force_scale
        <= 5.0e-12,
        "midpoint_force": max(
            float(maxima["midpoint_a"]),
            float(maxima["midpoint_b"]),
        )
        / force_scale
        <= 5.0e-12,
        "work_split_step": max(
            float(maxima["work_split_a"]),
            float(maxima["work_split_b"]),
        )
        / energy_scale
        <= 5.0e-11,
        "pair_ledger_step": float(maxima["pair_ledger"]) / energy_scale
        <= 5.0e-11,
        "work_split_cumulative": max(
            abs(float(cumulative["work_split_a"])),
            abs(float(cumulative["work_split_b"])),
        )
        / energy_scale
        <= 5.0e-9,
        "pair_ledger_cumulative": abs(float(cumulative["pair_ledger"]))
        / energy_scale
        <= 5.0e-9,
        "nonnegative_mobility": float(row["minimum_mobility_dissipation"])
        >= -1.0e-30,
        "high_precision_references": bool(
            not references_expected
            or (
                len(references) == 3
                and all(reference.get("pass", False) for reference in references)
            )
        ),
    }
    phase = row["phase_metrics"]
    loop = {
        "complete_shape_evaluation_count": int(row["shape_evaluation_count"])
        == ACTIVE_UPDATES + 1,
        "maximum_d0": max(
            float(summary["maximum_d0_a"]),
            float(summary["maximum_d0_b"]),
        )
        <= 0.01,
        "late_d0": max(
            float(summary["late_d0_a"]),
            float(summary["late_d0_b"]),
        )
        <= 0.002,
        "opposite_chirality": min(
            float(summary["late_opposite_a"]),
            float(summary["late_opposite_b"]),
        )
        >= 0.5,
        "phase_a": bool(phase["a"]["pass"]),
        "phase_b": bool(phase["b"]["pass"]),
        "separation": float(row["minimum_separation"]) >= 2.25 * RADIUS,
        "center_response_bound": float(row["maximum_center_response_fraction"])
        <= 0.10,
    }
    return ledger, loop


def _decision(gates: dict[str, bool]) -> str:
    if not gates["pipeline"]:
        return "p5d-inconclusive"
    if not gates["ledger_and_reciprocity"]:
        return "p5d-ledger-or-reciprocity-fail"
    if not gates["loop_integrity"]:
        return "p5d-loop-integrity-fail"
    if not gates["directional_causality"]:
        return "p5d-directional-causality-fail"
    if not gates["mutual_hypothesis"]:
        return "p5d-mutual-hypothesis-fail"
    if not gates["closed_loop_excess"]:
        return "p5d-independent-superposition"
    if not gates["scaling"]:
        return "p5d-inconclusive"
    return "p5d-mutual-center-response-pass"


def audit_payload(payload: dict[str, Any]) -> dict[str, Any]:
    panel = payload["panel"]
    off = panel["channel_off_arms"]
    active = panel["active_arms"]
    registration = _registration(
        off,
        active,
        require_references=(
            payload.get("schema") == "scalar-memory-loop-p5d-mutual-center-v1"
        ),
    )
    response = _responses(off, active) if all(registration.values()) else None
    response_gates = response["gates"] if response is not None else {}
    strict_numeric = (
        payload.get("schema") == "scalar-memory-loop-p5d-mutual-center-v1"
    )
    rebuilt_arm_gates = [
        _recompute_arm_gates(row, strict_numeric=strict_numeric)
        for row in off + active
    ]
    pipeline = bool(
        all(registration.values())
        and all(row.get("completed", False) for row in off + active)
        and all(row.get("finite", False) for row in off + active)
        and response_gates.get("primary_resolved", False)
    )
    ledger = all(
        all(ledger_gates.values())
        for ledger_gates, _ in rebuilt_arm_gates[len(off) :]
    )
    loop = all(all(loop_gates.values()) for _, loop_gates in rebuilt_arm_gates)
    gates = {
        "pipeline": pipeline,
        "ledger_and_reciprocity": ledger,
        "loop_integrity": loop,
        "directional_causality": _causality(off, active),
        "mutual_hypothesis": bool(
            response_gates.get("reciprocal_low_signal", False)
            and response_gates.get("reciprocal_high_signal", False)
            and response_gates.get("one_way_low_signal", False)
            and response_gates.get("one_way_high_signal", False)
            and response_gates.get("phase_support", False)
            and response_gates.get("sign_symmetry", False)
            and response_gates.get("reflection_covariance", False)
            and response_gates.get("swap_covariance", False)
        ),
        "closed_loop_excess": bool(
            response_gates.get("excess_resolved", False)
            and response_gates.get("excess_low_signal", False)
            and response_gates.get("excess_high_signal", False)
            and response_gates.get("excess_phase_support", False)
        ),
        "scaling": bool(
            response_gates.get("strength_scaling", False)
            and response_gates.get("distance_normalization", False)
            and response_gates.get("raw_distance_scaling", False)
            and response_gates.get("excess_strength_scaling", False)
            and response_gates.get("excess_response_fraction", False)
            and response_gates.get("excess_distance_normalization", False)
        ),
    }
    decision = _decision(gates)
    differences = []
    for index, (row, rebuilt) in enumerate(
        zip(off + active, rebuilt_arm_gates, strict=True)
    ):
        ledger_gates, loop_gates = rebuilt
        if row.get("ledger_gates") != ledger_gates:
            differences.append(f"arm[{index}].ledger_gates")
        if row.get("loop_gates") != loop_gates:
            differences.append(f"arm[{index}].loop_gates")
        if strict_numeric:
            energy_scale = float(row["ledger_scales"]["energy"])
            rival_fractions = {
                key: float(value) / energy_scale
                for key, value in row["ledger_rival_maxima"].items()
            }
            rival_resolved = {
                key: value > 5.0e-11
                for key, value in rival_fractions.items()
            }
            if row.get("ledger_rival_fractions") != rival_fractions:
                differences.append(f"arm[{index}].ledger_rival_fractions")
            if row.get("ledger_rival_resolved") != rival_resolved:
                differences.append(f"arm[{index}].ledger_rival_resolved")
    if payload.get("decision") != decision:
        differences.append(
            f"decision: stored={payload.get('decision')!r}, recomputed={decision!r}"
        )
    if payload.get("decision_gates") != gates:
        differences.append("decision_gates")
    if response is not None and payload.get("response", {}).get("gates") != response_gates:
        differences.append("response.gates")
    return {
        "schema": "scalar-memory-loop-p5d-mutual-center-independent-audit-v1",
        "registration_gates": registration,
        "response": response,
        "decision_gates": gates,
        "stored_decision": payload.get("decision"),
        "recomputed_decision": decision,
        "differences": differences,
        "decision": (
            "p5d-independent-audit-agrees"
            if not differences
            else "p5d-independent-audit-disagrees"
        ),
    }


def audit() -> dict[str, Any]:
    raw = RESULT.read_bytes()
    payload = json.loads(raw)
    result = audit_payload(payload)
    result["source_sha256"] = hashlib.sha256(raw).hexdigest()
    result["source_path"] = RESULT.relative_to(ROOT).as_posix()
    return result


def _atomic_write(path: Path, content: str) -> None:
    if path.exists():
        raise RuntimeError("refusing existing P5-D audit output")
    temporary = path.with_name(path.name + ".tmp")
    if temporary.exists():
        raise RuntimeError("refusing stale P5-D audit temporary")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if output.resolve() != DEFAULT_OUTPUT.resolve():
        raise RuntimeError("P5-D audit permits only its registered output")
    result = audit()
    _atomic_write(
        output,
        json.dumps(result, allow_nan=False, indent=2, sort_keys=True) + "\n",
    )
    print(json.dumps({"decision": result["decision"]}))


if __name__ == "__main__":
    main()
