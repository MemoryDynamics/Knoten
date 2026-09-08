"""Target-free infrastructure for the registered rotating-wave horizon gate.

This module deliberately contains no top-level target execution.  The numerical
root, interval homotopy, Arnoldi holdout and registered publication entry point
remain closed until a separate implementation-readiness review.
"""

from __future__ import annotations

import copy
from decimal import Decimal, localcontext
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import struct
from typing import Any, Sequence
import uuid

import mpmath as mp
import numpy as np

from emergenz_knoten.rotating_wave_stability import native_fifo_step


ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_transfer_result_schema_v2.json"
)
HORIZONS = (600, 900, 1200, 1500, 1800, 2400, 3600)
DECISION_PASS = (
    "rotating-wave-horizon-root-transfer-pass-with-large-h-stability-support"
)
PARAMETERS = {
    "alpha": 0.01,
    "memory_mass": 1.0,
    "eta": 0.15,
    "sigma_rep": 1.0,
    "sigma_att": 3.0,
    "amplitude_rep": 1.0,
    "amplitude_att": 3.5,
}
_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def _finite_decimal(value: str, *, path: str) -> Decimal:
    if type(value) is not str:
        raise TypeError(f"{path}: expected decimal string")
    try:
        result = Decimal(value)
    except Exception as error:
        raise ValueError(f"{path}: invalid decimal string") from error
    if not result.is_finite():
        raise ValueError(f"{path}: decimal must be finite")
    return result


def _load_result_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _validate_primitive(value: Any, specification: str, *, path: str) -> None:
    if specification == "boolean":
        valid = type(value) is bool
    elif specification == "integer":
        valid = type(value) is int
    elif specification == "number":
        valid = type(value) in (int, float) and math.isfinite(value)
    elif specification == "string":
        valid = type(value) is str
    elif specification == "null":
        valid = value is None
    elif specification == "decimal":
        _finite_decimal(value, path=path)
        return
    elif specification == "sha1":
        valid = type(value) is str and _SHA1.fullmatch(value) is not None
    elif specification == "sha256":
        valid = type(value) is str and _SHA256.fullmatch(value) is not None
    elif specification == "uuid4":
        try:
            parsed = uuid.UUID(value) if type(value) is str else None
            valid = parsed is not None and parsed.version == 4 and str(parsed) == value
        except (ValueError, AttributeError):
            valid = False
    elif specification == "path":
        valid = (
            type(value) is str
            and value != ""
            and "\\" not in value
            and not PurePosixPath(value).is_absolute()
            and ".." not in PurePosixPath(value).parts
        )
    else:
        raise ValueError(f"{path}: unknown primitive {specification}")
    if not valid:
        raise TypeError(f"{path}: expected {specification}")


def _validate_schema_value(
    value: Any,
    specification: str,
    *,
    path: str,
    contract: dict[str, Any],
) -> None:
    if specification.startswith("nullable:"):
        if value is None:
            return
        specification = specification.split(":", 1)[1]
    if ":" not in specification:
        _validate_primitive(value, specification, path=path)
        return
    kind, name = specification.split(":", 1)
    if kind == "const":
        expected = contract["constants"][name]
        if not _exact_constant(value, expected):
            raise TypeError(f"{path}: expected const:{name}")
        return
    if kind == "enum":
        allowed = contract["enums"][name]
        if not any(type(value) is type(item) and value == item for item in allowed):
            raise TypeError(f"{path}: expected enum:{name}")
        return
    if kind == "array":
        definition = contract["arrays"][name]
        if type(value) is not list:
            raise TypeError(f"{path}: expected array:{name}")
        if "length" in definition and len(value) != definition["length"]:
            raise ValueError(f"{path}: array:{name} expected length {definition['length']}")
        minimum = definition.get("min_length", 0)
        maximum = definition.get("max_length", math.inf)
        if not minimum <= len(value) <= maximum:
            raise ValueError(
                f"{path}: array:{name} expected length in [{minimum}, {maximum}]"
            )
        for index, item in enumerate(value):
            _validate_schema_value(
                item,
                definition["item"],
                path=f"{path}[{index}]",
                contract=contract,
            )
        return
    if kind == "object":
        definition = contract["objects"][name]
        if type(value) is not dict:
            raise TypeError(f"{path}: expected object:{name}")
        observed = set(value)
        expected = set(definition)
        if observed != expected:
            missing = sorted(expected - observed)
            unknown = sorted(observed - expected)
            raise ValueError(f"{path}: missing={missing}, unknown={unknown}")
        for key, child_specification in definition.items():
            _validate_schema_value(
                value[key],
                child_specification,
                path=f"{path}.{key}",
                contract=contract,
            )
        return
    raise ValueError(f"{path}: unknown specification {specification}")


def _exact_constant(value: Any, expected: Any) -> bool:
    if type(value) is not type(expected):
        return False
    if type(expected) is list:
        return len(value) == len(expected) and all(
            _exact_constant(left, right)
            for left, right in zip(value, expected, strict=True)
        )
    if type(expected) is dict:
        return set(value) == set(expected) and all(
            _exact_constant(value[key], expected[key]) for key in expected
        )
    return value == expected


def validate_result(payload: dict[str, Any]) -> None:
    contract = _load_result_schema()
    _validate_schema_value(payload, contract["root"], path="$", contract=contract)
    _verify_result_semantics(payload)


def _witness_value(
    specification: str,
    contract: dict[str, Any],
    *,
    fill_nullable: bool,
) -> Any:
    if specification.startswith("nullable:"):
        if not fill_nullable:
            return None
        specification = specification.split(":", 1)[1]
    primitives: dict[str, Any] = {
        "boolean": False,
        "integer": 0,
        "number": 0.0,
        "string": "fixture",
        "null": None,
        "decimal": "0",
        "sha1": "0" * 40,
        "sha256": "0" * 64,
        "uuid4": "00000000-0000-4000-8000-000000000000",
        "path": "fixture/value",
    }
    if ":" not in specification:
        return copy.deepcopy(primitives[specification])
    kind, name = specification.split(":", 1)
    if kind == "const":
        return copy.deepcopy(contract["constants"][name])
    if kind == "enum":
        return copy.deepcopy(contract["enums"][name][0])
    if kind == "array":
        definition = contract["arrays"][name]
        length = definition.get("length", definition.get("min_length", 0))
        return [
            _witness_value(
                definition["item"], contract, fill_nullable=fill_nullable
            )
            for _ in range(length)
        ]
    if kind == "object":
        return {
            key: _witness_value(child, contract, fill_nullable=fill_nullable)
            for key, child in contract["objects"][name].items()
        }
    raise ValueError(f"unknown witness specification {specification}")


def contract_witness() -> dict[str, Any]:
    contract = _load_result_schema()
    result = _witness_value(contract["root"], contract, fill_nullable=True)
    result["identity"]["parameters"] = {
        **PARAMETERS,
        "anchor_radius": 0.946517504804225,
        "anchor_theta": 0.015770381717135,
        "epsilon": 0.0,
    }
    result["publication"]["artifacts"][0]["role"] = "result-json"
    result["publication"]["artifacts"][1]["role"] = "readable-report"
    result["publication"]["manifest_published_last"] = True
    homotopy_edges = (
        (1200, 1500, "forward"),
        (1500, 1800, "forward"),
        (1800, 2400, "forward"),
        (2400, 3600, "forward"),
        (1200, 900, "lower-tail"),
        (900, 600, "lower-tail"),
    )
    for index, panel in enumerate(result["finite_branch"]["root_panels"]):
        panel["horizon"] = HORIZONS[index]
        panel["newton_80"]["precision_dps"] = 80
        panel["newton_120"]["precision_dps"] = 120
        panel["newton_80"]["steps"] = 8
        panel["newton_120"]["steps"] = 8
        panel["inner_intersection"] = {
            "radius": ["0.946517504804225", "0.946517504804225"],
            "theta": ["0.015770381717135", "0.015770381717135"],
        }
        panel["centers_agree"] = True
        panel["certificate_80"]["strict_interior"] = True
        panel["certificate_120"]["strict_interior"] = True
    for homotopy, (first, second, direction) in zip(
        result["finite_branch"]["homotopies"],
        homotopy_edges,
        strict=True,
    ):
        homotopy.update(
            {
                "from_horizon": first,
                "to_horizon": second,
                "direction": direction,
                "pass": True,
                "status": "pass",
            }
        )
        for index, slab in enumerate(homotopy["slabs"]):
            slab.update(
                {
                    "index": index,
                    "s_interval": [
                        format(Decimal(index) / Decimal(64), "f"),
                        format(Decimal(index + 1) / Decimal(64), "f"),
                    ],
                    "strict_interior": True,
                    "overlaps_previous": None if index == 0 else True,
                }
            )
    result["finite_branch"]["exclusions"] = [None] * 4
    result["finite_branch"]["direct_replay_pass"] = True
    drift_rows = [
        {
            "from_horizon": 1800,
            "to_horizon": 2400,
            "radius_component": 0.0,
            "theta_component": 0.0,
            "upper_bound": 0.0,
        },
        {
            "from_horizon": 2400,
            "to_horizon": 3600,
            "radius_component": 0.0,
            "theta_component": 0.0,
            "upper_bound": 0.0,
        },
    ]
    result["finite_branch"]["drift"] = {
        "center_diagnostics": copy.deepcopy(drift_rows),
        "interval_upper_bounds": drift_rows,
        "mutation_closes_pass": True,
        "pass": True,
    }
    result["infinite_tail"]["q_representations"] = q_representations(HORIZONS)
    result["infinite_tail"]["bounds"] = [
        {"horizon": horizon, **tail_bounds(horizon=horizon, precision_dps=80)}
        for horizon in HORIZONS
    ]
    for precision, panel in zip(
        (120, 160),
        result["infinite_tail"]["certificate_panels"],
        strict=True,
    ):
        panel["precision_dps"] = precision
        panel["certificate"]["strict_interior"] = True
    result["infinite_tail"]["panel_comparison"]["overlap"] = True
    result["stability"]["horizon"] = 2400
    primary = result["stability"]["arnoldi"]["primary"]
    convergence = result["stability"]["arnoldi"]["convergence"]
    primary.update(
        {"expected_count": 24, "requested_count": 24, "ncv": 96, "max_iterations": 20000, "tolerance": 1e-10}
    )
    convergence.update(
        {"expected_count": 36, "requested_count": 36, "ncv": 144, "max_iterations": 40000, "tolerance": 1e-12}
    )
    primary["status"] = "complete"
    convergence["status"] = "complete"
    for panel in (primary, convergence):
        for pair in panel["eigenpairs"]:
            pair.update(
                {
                    "eigenvalue": [0.9, 0.0],
                    "modulus": 0.9,
                    "normalized_residual": 0.0,
                    "translation_overlap": 0.0,
                    "rotation_overlap": 0.0,
                    "classification": "transverse",
                }
            )
        for index, classification in enumerate(
            ("translation", "translation", "rotation")
        ):
            pair = panel["eigenpairs"][index]
            pair.update(
                {
                    "eigenvalue": [1.0, 0.0],
                    "modulus": 1.0,
                    "classification": classification,
                }
            )
            pair[f"{classification}_overlap"] = 1.0
    arm_names = ("radial", "tangential", "full-history-transverse")
    for arm, name in zip(
        result["stability"]["continuation_arms"], arm_names, strict=True
    ):
        arm.update(
            {
                "name": name,
                "completed": True,
                "stopped": False,
                "initial_distance": 1.0,
                "final_distance": 0.05,
                "final_ratio": 0.05,
                "growth_factor": 1.0,
            }
        )
        for index, sample in enumerate(arm["samples"]):
            sample.update({"step": 10 * index, "distance": 0.0})
    exact_arm = result["stability"]["exact_arm"]
    exact_arm.update(
        {"completed": True, "stopped": False, "maximum_distance": 0.0}
    )
    for index, sample in enumerate(exact_arm["samples"]):
        sample.update({"step": 10 * index, "distance": 0.0})
    result["stability"]["gates"] = {
        "continuations_complete": True,
        "exact_arm": True,
        "instability_supported": False,
        "panels_complete": True,
        "panel_agreement": True,
        "perturbation_contraction": True,
        "ritz_residuals": True,
        "symmetries": True,
    }
    result["stability"]["arnoldi"]["panel_agreement"].update(
        {"pass": True, "symmetry_pass": True}
    )
    result["controls"]["pass"] = True
    circular_cases = (
        ("noncircle-H17", 17),
        ("noncircle-H257", 257),
        *((f"anchor-H{horizon}", horizon) for horizon in HORIZONS),
    )
    for row, (case_id, horizon) in zip(
        result["controls"]["circular_cases"], circular_cases, strict=True
    ):
        row.update({"case_id": case_id, "horizon": horizon, "pass": True})
    for row, horizon in zip(
        result["controls"]["eta_zero_cases"], HORIZONS, strict=True
    ):
        row.update({"horizon": horizon, "steps": horizon + 1, "pass": True})
    mutation_names = (
        "drift-width",
        "reverse-modulo",
        "overwrite-before-read",
        "wrong-oldest-slot",
    )
    for row, name in zip(
        result["controls"]["mutations"], mutation_names, strict=True
    ):
        row.update({"name": name, "detected": True})
    gates = {
        "G0": "pass",
        "G1F": "pass",
        "G1R": "pass",
        "G2F": "pass",
        "G2R": "pass",
        "G3": "pass",
        "G4": "pass",
        "G5": "pass",
        "G6": "pass",
        "local_branch_excluded": False,
        "large_h_instability_supported": False,
    }
    classification = classify_horizon(
        gates,
        lower_tail_status="lower-tail-stress-pass",
    )
    result["classification"].update(classification)
    result["classification"]["gates"] = gates
    result["classification"]["finite_large_h_stability_only"] = False
    return result


def finite_residual_and_jacobian(
    *,
    radius: float,
    theta: float,
    horizon: int,
    precision_dps: int,
) -> dict[str, list[Any]]:
    if horizon < 2 or precision_dps not in (80, 120, 160):
        raise ValueError("unregistered horizon or precision")
    with mp.workdps(precision_dps):
        radius_mp = mp.mpf(str(radius))
        theta_mp = mp.mpf(str(theta))
        alpha = mp.mpf("0.01")
        q = mp.mpf("0.99")
        eta = mp.mpf("0.15")
        first = mp.cos(theta_mp) - 1
        second = mp.sin(theta_mp)
        jacobian = [[mp.mpf("0"), -mp.sin(theta_mp)], [mp.mpf("0"), mp.cos(theta_mp)]]
        for age in range(1, horizon):
            phase = age * theta_mp
            half_sine = mp.sin(phase / 2)
            sign = mp.sign(half_sine)
            distance = 2 * radius_mp * abs(half_sine)
            rep = mp.exp(-(distance**2) / 2)
            att = mp.exp(-(distance**2) / 18)
            phi = -rep + mp.mpf("3.5") / 9 * att
            phi_prime = distance * rep - mp.mpf("3.5") * distance / 81 * att
            vector = (1 - mp.cos(phase), mp.sin(phase))
            vector_prime = (age * mp.sin(phase), age * mp.cos(phase))
            weight = eta * alpha * q**age
            first += weight * phi * vector[0]
            second += weight * phi * vector[1]
            dr_radius = 2 * abs(half_sine)
            dr_theta = radius_mp * age * mp.cos(phase / 2) * sign
            for row in range(2):
                jacobian[row][0] += weight * phi_prime * dr_radius * vector[row]
                jacobian[row][1] += weight * (
                    phi_prime * dr_theta * vector[row] + phi * vector_prime[row]
                )
        return {
            "residual": [float(first), float(second)],
            "jacobian": [[float(value) for value in row] for row in jacobian],
        }


def _positive_float_bits(value: float) -> int:
    if not value > 0.0 or not math.isfinite(value):
        raise ValueError("ULP comparison requires a positive finite value")
    return struct.unpack(">Q", struct.pack(">d", value))[0]


def q_representations(horizons: Sequence[int]) -> list[dict[str, Any]]:
    alpha64 = float("0.01")
    q64 = 1.0 - alpha64
    rows = []
    for horizon in horizons:
        if type(horizon) is not int or horizon < 1:
            raise ValueError("horizons must be positive integers")
        direct = q64**horizon
        exp_log = math.exp(horizon * math.log(q64))
        diagnostic = math.exp(horizon * math.log1p(-alpha64))
        ulps = abs(_positive_float_bits(direct) - _positive_float_bits(exp_log))
        rows.append(
            {
                "horizon": horizon,
                "decimal_power": _exact_q_decimal_power(horizon),
                "direct_power": direct,
                "exp_log_power": exp_log,
                "diagnostic_exp_log1p": diagnostic,
                "diagnostic_relative_difference": abs(direct - diagnostic) / direct,
                "ulp_difference": ulps,
                "two_ulp_gate": ulps <= 2,
                "nonzero_finite": all(
                    value > 0.0 and math.isfinite(value)
                    for value in (direct, exp_log, diagnostic)
                ),
            }
        )
    return rows


def _exact_q_decimal_power(horizon: int) -> str:
    with localcontext() as context:
        context.prec = 2 * horizon + 10
        return format(Decimal("0.99") ** horizon, "f")


def _outward_decimal(value: Decimal) -> str:
    rounded = float(value)
    if Decimal.from_float(rounded) < value:
        rounded = math.nextafter(rounded, math.inf)
    return repr(rounded)


def tail_bounds(*, horizon: int, precision_dps: int) -> dict[str, str]:
    if type(horizon) is not int or horizon < 1 or precision_dps not in (80, 120, 160):
        raise ValueError("invalid tail-bound registration")
    with localcontext() as context:
        context.prec = precision_dps
        q = Decimal("0.99")
        eta = Decimal("0.15")
        phi0 = Decimal(1) + Decimal("3.5") / Decimal(9)
        phi1 = (-Decimal("0.5")).exp() * (Decimal(1) + Decimal("3.5") / Decimal(27))
        q_power = q**horizon
        return {
            "residual_bound": _outward_decimal(2 * eta * phi0 * q_power),
            "jacobian_radius_bound": _outward_decimal(4 * eta * phi1 * q_power),
            "jacobian_theta_bound": _outward_decimal(
                eta
                * (phi0 + 2 * Decimal("1.1") * phi1)
                * q_power
                * (Decimal(horizon) + q / Decimal("0.01"))
            ),
        }


def interval_drift_upper(
    first: dict[str, Sequence[float]],
    second: dict[str, Sequence[float]],
    *,
    radius_scale: float,
    theta_scale: float,
) -> float:
    return max(
        _interval_drift_components(
            first,
            second,
            radius_scale=radius_scale,
            theta_scale=theta_scale,
        )
    )


def _interval_drift_components(
    first: dict[str, Sequence[float]],
    second: dict[str, Sequence[float]],
    *,
    radius_scale: float,
    theta_scale: float,
) -> tuple[float, float]:
    if not radius_scale > 0.0 or not theta_scale > 0.0:
        raise ValueError("drift scales must be positive")
    components = []
    for name, scale in (("radius", radius_scale), ("theta", theta_scale)):
        left = tuple(Decimal(str(value)) for value in first[name])
        right = tuple(Decimal(str(value)) for value in second[name])
        if len(left) != 2 or len(right) != 2 or left[0] > left[1] or right[0] > right[1]:
            raise ValueError("invalid interval")
        supremum = max(abs(a - b) for a in left for b in right) / Decimal(str(scale))
        rounded = float(supremum)
        if Decimal.from_float(rounded) < supremum:
            rounded = math.nextafter(rounded, math.inf)
        components.append(rounded)
    return components[0], components[1]


def drift_gates(*, previous_upper: float, final_upper: float) -> dict[str, bool]:
    absolute = final_upper <= 1e-8
    contraction = final_upper <= 0.01 * previous_upper + 1e-14
    return {"absolute": absolute, "contraction": contraction, "pass": absolute and contraction}


def evaluate_homotopy_slabs(slabs: Sequence[dict[str, Any]]) -> str:
    if len(slabs) != 64:
        return "inconclusive"
    for index, slab in enumerate(slabs):
        if type(slab.get("strict_interior")) is not bool or not slab["strict_interior"]:
            return "inconclusive"
        if index > 0 and slab.get("overlaps_previous") is not True:
            return "inconclusive"
    return "pass"


def evaluate_arnoldi_panel(panel: dict[str, Any], *, expected_count: int) -> dict[str, str]:
    pairs = panel.get("eigenpairs")
    if panel.get("status") != "complete" or type(pairs) is not list or len(pairs) != expected_count:
        return {"gate_state": "inconclusive"}
    for pair in pairs:
        vector = pair.get("vector")
        scalars = (
            pair.get("modulus"),
            pair.get("normalized_residual"),
            pair.get("translation_overlap"),
            pair.get("rotation_overlap"),
        )
        if (
            type(vector) is not list
            or len(vector) != 4800
            or any(type(value) not in (int, float) or not math.isfinite(value) for value in scalars)
            or pair["normalized_residual"] > 1e-8
        ):
            return {"gate_state": "inconclusive"}
        if any(
            type(component) is not list
            or len(component) != 2
            or any(type(value) not in (int, float) or not math.isfinite(value) for value in component)
            for component in vector
        ):
            return {"gate_state": "inconclusive"}
    return {"gate_state": "pass"}


def circular_fifo_from_age_order(history: np.ndarray) -> dict[str, Any]:
    state = np.asarray(history, dtype=float)
    if state.ndim != 2 or state.shape[1] != 2 or state.shape[0] < 1 or not np.isfinite(state).all():
        raise ValueError("history must have finite shape (H,2)")
    return {"buffer": state.copy(), "head": 0}


def materialize_circular_fifo(state: dict[str, Any]) -> np.ndarray:
    buffer = np.asarray(state["buffer"], dtype=float)
    head = state["head"]
    if type(head) is not int or not 0 <= head < len(buffer):
        raise ValueError("invalid circular head")
    return np.asarray([buffer[(head + age) % len(buffer)] for age in range(len(buffer))])


def circular_fifo_step(
    state: dict[str, Any],
    *,
    alpha: float,
    memory_mass: float,
    eta: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float,
    amplitude_att: float,
    _mutation: str | None = None,
) -> dict[str, Any]:
    buffer = np.asarray(state["buffer"], dtype=float).copy()
    head = int(state["head"])
    horizon = len(buffer)
    current = buffer[head].copy()
    oldest = (head + horizon - 1) % horizon
    if _mutation == "overwrite-before-read":
        buffer[oldest] = current
    gradient = np.zeros(2, dtype=float)
    q = 1.0 - alpha
    for age in range(horizon):
        direction = -age if _mutation == "reverse-modulo" else age
        index = (head + direction) % horizon
        displacement = current - buffer[index]
        radius = float(np.linalg.norm(displacement))
        phi = -amplitude_rep / sigma_rep**2 * math.exp(
            -(radius**2) / (2 * sigma_rep**2)
        ) + amplitude_att / sigma_att**2 * math.exp(
            -(radius**2) / (2 * sigma_att**2)
        )
        gradient += alpha * memory_mass * q**age * phi * displacement
    new_point = current - eta * gradient
    new_head = head if _mutation == "wrong-oldest-slot" else oldest
    buffer[new_head] = new_point
    return {"buffer": buffer, "head": new_head}


def _relative_error(first: np.ndarray, second: np.ndarray) -> float:
    numerator = float(np.linalg.norm(np.asarray(first) - np.asarray(second)))
    denominator = max(1.0, float(np.linalg.norm(first)), float(np.linalg.norm(second)))
    return numerator / denominator


def run_circular_control(
    history: np.ndarray,
    *,
    parameters: dict[str, float],
    mutation: str | None = None,
) -> dict[str, Any]:
    initial = np.asarray(history, dtype=float)
    state = circular_fifo_from_age_order(initial)
    materialized = materialize_circular_fifo(state)
    initial_hash = hashlib.sha256(np.ascontiguousarray(initial).tobytes()).hexdigest()
    materialized_hash = hashlib.sha256(
        np.ascontiguousarray(materialized).tobytes()
    ).hexdigest()
    expected = native_fifo_step(history, **parameters)
    advanced = circular_fifo_step(state, _mutation=mutation, **parameters)
    observed = materialize_circular_fifo(advanced)
    new_point_error = _relative_error(expected[0], observed[0])
    state_error = _relative_error(expected, observed)
    return {
        "mutation": mutation,
        "age_history_sha256": materialized_hash,
        "age_hash_equal": initial_hash == materialized_hash,
        "new_point_relative_error": new_point_error,
        "complete_state_relative_error": state_error,
        "pass": (
            initial_hash == materialized_hash
            and new_point_error < 5e-14
            and state_error < 5e-14
        ),
    }


def eta_zero_collapse(history: np.ndarray, *, steps: int) -> np.ndarray:
    result = np.asarray(history, dtype=float).copy()
    for _ in range(steps):
        shifted = np.empty_like(result)
        shifted[0] = result[0]
        if len(result) > 1:
            shifted[1:] = result[:-1]
        result = shifted
    return result


def classify_horizon(
    gates: dict[str, Any],
    *,
    lower_tail_status: str,
) -> dict[str, Any]:
    if gates["G0"] == "fail" or gates["G6"] == "fail":
        decision = "rotating-wave-horizon-experiment-invalid"
        rank = 1
    elif gates["local_branch_excluded"]:
        decision = "registered-local-horizon-branch-loss"
        rank = 2
    elif gates["G1F"] == gates["G2F"] == "pass" and gates["G3"] == "fail":
        decision = "rotating-wave-horizon-branch-drift"
        rank = 3
    else:
        prerequisites = all(gates[name] == "pass" for name in ("G0", "G1F", "G2F", "G3", "G4", "G6"))
        if prerequisites and gates["large_h_instability_supported"]:
            decision = "rotating-wave-infinite-root-certified-large-h-instability"
            rank = 4
        elif prerequisites and gates["G5"] == "pass":
            decision = DECISION_PASS
            rank = 5
        elif prerequisites:
            decision = "infinite-memory-local-root-certified-stability-open"
            rank = 6
        else:
            decision = "rotating-wave-horizon-transfer-inconclusive"
            rank = 7
    return {
        "decision": decision,
        "precedence_rank": rank,
        "lower_tail_status": lower_tail_status,
        "p5_governance_review_open": decision == DECISION_PASS,
    }


def _nonnull_prefix_length(values: Sequence[Any], *, path: str) -> int:
    count = 0
    saw_null = False
    for value in values:
        if value is None:
            saw_null = True
        elif saw_null:
            raise ValueError(f"{path}: non-null values must form a prefix")
        else:
            count += 1
    return count


def _verify_root_slots(root_panels: list[dict[str, Any] | None]) -> None:
    for index, panel in enumerate(root_panels):
        if panel is not None and panel["horizon"] != HORIZONS[index]:
            raise ValueError(
                f"$.finite_branch.root_panels[{index}]: horizon order mismatch"
            )
    for previous, current in ((2, 3), (3, 4), (4, 5), (5, 6)):
        if root_panels[current] is not None and root_panels[previous] is None:
            raise ValueError("$.finite_branch.root_panels: forward dependency gap")
    if root_panels[1] is not None and root_panels[2] is None:
        raise ValueError("$.finite_branch.root_panels: lower dependency gap")
    if root_panels[0] is not None and root_panels[1] is None:
        raise ValueError("$.finite_branch.root_panels: lower dependency gap")


def _verify_homotopy_slots(
    homotopies: list[dict[str, Any] | None],
    root_panels: list[dict[str, Any] | None],
) -> None:
    edges = (
        (1200, 1500, "forward", 2, 3),
        (1500, 1800, "forward", 3, 4),
        (1800, 2400, "forward", 4, 5),
        (2400, 3600, "forward", 5, 6),
        (1200, 900, "lower-tail", 2, 1),
        (900, 600, "lower-tail", 1, 0),
    )
    _nonnull_prefix_length(homotopies[:4], path="$.finite_branch.homotopies[0:4]")
    _nonnull_prefix_length(homotopies[4:], path="$.finite_branch.homotopies[4:6]")
    for index, (homotopy, edge) in enumerate(zip(homotopies, edges, strict=True)):
        if homotopy is None:
            continue
        first, second, direction, first_slot, second_slot = edge
        if root_panels[first_slot] is None or root_panels[second_slot] is None:
            raise ValueError(
                f"$.finite_branch.homotopies[{index}]: missing endpoint root"
            )
        if (
            homotopy["from_horizon"],
            homotopy["to_horizon"],
            homotopy["direction"],
        ) != (first, second, direction):
            raise ValueError(f"$.finite_branch.homotopies[{index}]: edge mismatch")
        slab_count = _nonnull_prefix_length(
            homotopy["slabs"],
            path=f"$.finite_branch.homotopies[{index}].slabs",
        )
        for slab_index, slab in enumerate(homotopy["slabs"][:slab_count]):
            if slab["index"] != slab_index:
                raise ValueError(
                    f"$.finite_branch.homotopies[{index}].slabs: index mismatch"
                )
        slab_state = evaluate_homotopy_slabs(homotopy["slabs"][:slab_count])
        if homotopy["status"] == "pass":
            if slab_state != "pass" or homotopy["pass"] is not True:
                raise ValueError(
                    f"$.finite_branch.homotopies[{index}]: false pass"
                )
        elif homotopy["pass"] is not False:
            raise ValueError(
                f"$.finite_branch.homotopies[{index}]: non-pass status mismatch"
            )


def _verify_exclusions(
    exclusions: list[dict[str, Any] | None],
    *,
    local_branch_excluded: bool,
) -> None:
    edges = ((1200, 1500), (1500, 1800), (1800, 2400), (2400, 3600))
    complete_exclusion = False
    for index, (attempt, edge) in enumerate(zip(exclusions, edges, strict=True)):
        if attempt is None:
            continue
        if (attempt["from_horizon"], attempt["to_horizon"]) != edge:
            raise ValueError(f"$.finite_branch.exclusions[{index}]: edge mismatch")
        if attempt["max_depth"] != 20:
            raise ValueError(f"$.finite_branch.exclusions[{index}]: depth mismatch")
        leaves = attempt["leaves"]
        status = attempt["status"]
        classifications = [leaf["classification"] for leaf in leaves]
        if status == "all-residual-excluded":
            if any(value != "residual-excluded" for value in classifications):
                raise ValueError(
                    f"$.finite_branch.exclusions[{index}]: false exclusion"
                )
            complete_exclusion = True
        elif status == "other-root" and "krawczyk-root" not in classifications:
            raise ValueError(
                f"$.finite_branch.exclusions[{index}]: missing other root"
            )
    if local_branch_excluded is not complete_exclusion:
        raise ValueError("$.classification.gates.local_branch_excluded: mismatch")


def _verify_arnoldi_panel(
    panel: dict[str, Any],
    *,
    path: str,
    expected_count: int,
) -> None:
    pairs = panel["eigenpairs"]
    count = _nonnull_prefix_length(pairs, path=f"{path}.eigenpairs")
    missing_vector = any(
        pair["vector"] is None for pair in pairs[:count]
    )
    if panel["expected_count"] != expected_count or panel["requested_count"] != expected_count:
        raise ValueError(f"{path}: registered count mismatch")
    if panel["status"] == "complete" and (count != expected_count or missing_vector):
        raise ValueError(f"{path}: complete status with incomplete slots")
    if panel["status"] == "missing-vectors" and not missing_vector:
        raise ValueError(f"{path}: missing-vectors status without missing vector")
    if panel["status"] == "wrong-cardinality" and count == expected_count:
        raise ValueError(f"{path}: wrong-cardinality status with full count")


def _verify_trajectory(
    arm: dict[str, Any],
    *,
    path: str,
) -> None:
    samples = arm["samples"]
    count = _nonnull_prefix_length(samples, path=f"{path}.samples")
    for index, sample in enumerate(samples[:count]):
        expected_step = 10 * index
        if index < count - 1 or arm["completed"]:
            if sample["step"] != expected_step:
                raise ValueError(f"{path}.samples: step mismatch")
        elif not 10 * (index - 1 if index else 0) <= sample["step"] <= expected_step:
            raise ValueError(f"{path}.samples: stop step mismatch")
    if arm["completed"] and (count != 501 or arm["stopped"]):
        raise ValueError(f"{path}: complete trajectory has missing samples")
    if arm["stopped"] and arm["completed"]:
        raise ValueError(f"{path}: stopped trajectory marked complete")


def _stability_evidence(payload: dict[str, Any]) -> dict[str, bool]:
    stability = payload["stability"]
    panels = (
        stability["arnoldi"]["primary"],
        stability["arnoldi"]["convergence"],
    )
    panels_complete = all(
        panel["status"] == "complete"
        and all(pair is not None and pair["vector"] is not None for pair in panel["eigenpairs"])
        for panel in panels
    )
    ritz_residuals = panels_complete and all(
        pair["normalized_residual"] <= 1e-8
        for panel in panels
        for pair in panel["eigenpairs"]
    )
    symmetries = bool(
        panels_complete
        and stability["arnoldi"]["panel_agreement"]["symmetry_pass"]
    )
    agreement = bool(
        panels_complete and stability["arnoldi"]["panel_agreement"]["pass"]
    )
    arms = stability["continuation_arms"]
    continuations_complete = all(
        arm is not None and arm["completed"] and not arm["stopped"] for arm in arms
    )
    contraction = bool(
        continuations_complete
        and all(arm["final_ratio"] <= 0.1 for arm in arms)
    )
    exact = stability["exact_arm"]
    exact_pass = bool(
        exact is not None
        and exact["completed"]
        and not exact["stopped"]
        and exact["maximum_distance"] <= 1e-10
    )
    transverse = [
        pair
        for panel in panels
        for pair in panel["eigenpairs"]
        if pair is not None and pair["classification"] == "transverse"
    ]
    stable_spectrum = bool(
        panels_complete
        and transverse
        and all(pair["modulus"] < 1.0 - 1e-4 for pair in transverse)
    )
    primary_transverse = [
        pair for pair in panels[0]["eigenpairs"] if pair is not None and pair["classification"] == "transverse"
    ]
    convergence_transverse = [
        pair for pair in panels[1]["eigenpairs"] if pair is not None and pair["classification"] == "transverse"
    ]
    unstable_spectrum = bool(
        panels_complete
        and agreement
        and primary_transverse
        and convergence_transverse
        and max(pair["modulus"] for pair in primary_transverse) > 1.0 + 1e-6
        and max(pair["modulus"] for pair in convergence_transverse) > 1.0 + 1e-6
    )
    growth = any(
        arm is not None and arm["growth_factor"] >= 100.0 for arm in arms
    )
    return {
        "continuations_complete": continuations_complete,
        "exact_arm": exact_pass,
        "instability_supported": bool(
            ritz_residuals and symmetries and unstable_spectrum and growth
        ),
        "panels_complete": panels_complete,
        "panel_agreement": agreement,
        "perturbation_contraction": bool(stable_spectrum and contraction),
        "ritz_residuals": ritz_residuals,
        "symmetries": symmetries,
    }


def _controls_evidence(payload: dict[str, Any]) -> bool:
    controls = payload["controls"]
    expected_horizons = [17, 257, *HORIZONS]
    circular = controls["circular_cases"]
    eta_zero = controls["eta_zero_cases"]
    mutations = controls["mutations"]
    return bool(
        [row["horizon"] for row in circular] == expected_horizons
        and all(row["pass"] for row in circular)
        and [row["horizon"] for row in eta_zero] == list(HORIZONS)
        and all(
            row["steps"] == row["horizon"] + 1 and row["pass"]
            for row in eta_zero
        )
        and [row["name"] for row in mutations]
        == [
            "drift-width",
            "reverse-modulo",
            "overwrite-before-read",
            "wrong-oldest-slot",
        ]
        and all(row["detected"] for row in mutations)
    )


def _verify_result_semantics(payload: dict[str, Any]) -> None:
    expected_parameters = {
        **PARAMETERS,
        "anchor_radius": 0.946517504804225,
        "anchor_theta": 0.015770381717135,
        "epsilon": 0.0,
    }
    if payload["identity"]["parameters"] != expected_parameters:
        raise ValueError("$.identity.parameters: registered values do not match")
    root_panels = payload["finite_branch"]["root_panels"]
    _verify_root_slots(root_panels)
    _verify_homotopy_slots(payload["finite_branch"]["homotopies"], root_panels)
    if payload["stability"]["horizon"] != 2400:
        raise ValueError("$.stability.horizon: expected 2400")
    roles = [row["role"] for row in payload["publication"]["artifacts"]]
    if roles != ["result-json", "readable-report"]:
        raise ValueError("$.publication.artifacts: role order mismatch")
    if payload["infinite_tail"]["q_representations"] != q_representations(HORIZONS):
        raise ValueError("$.infinite_tail.q_representations: reconstruction mismatch")
    expected_bounds = [
        {"horizon": horizon, **tail_bounds(horizon=horizon, precision_dps=80)}
        for horizon in HORIZONS
    ]
    if payload["infinite_tail"]["bounds"] != expected_bounds:
        raise ValueError("$.infinite_tail.bounds: reconstruction mismatch")
    drift = payload["finite_branch"]["drift"]
    drift_rows = drift["interval_upper_bounds"]
    root_boxes = {
        panel["horizon"]: panel["inner_intersection"]
        for panel in root_panels
        if panel is not None
    }
    for index, (first_horizon, second_horizon) in enumerate(
        ((1800, 2400), (2400, 3600))
    ):
        row = drift_rows[index]
        if first_horizon not in root_boxes or second_horizon not in root_boxes:
            if row is not None:
                raise ValueError(
                    f"$.finite_branch.drift.interval_upper_bounds[{index}]: "
                    "value without prerequisite root"
                )
            continue
        radius_component, theta_component = _interval_drift_components(
            root_boxes[first_horizon],
            root_boxes[second_horizon],
            radius_scale=0.946517504804225,
            theta_scale=0.015770381717135,
        )
        expected_row = {
            "from_horizon": first_horizon,
            "to_horizon": second_horizon,
            "radius_component": radius_component,
            "theta_component": theta_component,
            "upper_bound": max(radius_component, theta_component),
        }
        if row != expected_row:
            raise ValueError(
                f"$.finite_branch.drift.interval_upper_bounds[{index}]: "
                "reconstruction mismatch"
            )
    if any(row is None for row in drift_rows):
        expected_drift_pass = False
    else:
        expected_drift_pass = drift_gates(
            previous_upper=drift_rows[0]["upper_bound"],
            final_upper=drift_rows[1]["upper_bound"],
        )["pass"]
    if drift["pass"] is not expected_drift_pass:
        raise ValueError("$.finite_branch.drift.pass: reconstruction mismatch")

    observed = payload["classification"]
    gates = observed["gates"]
    _verify_exclusions(
        payload["finite_branch"]["exclusions"],
        local_branch_excluded=gates["local_branch_excluded"],
    )
    _verify_arnoldi_panel(
        payload["stability"]["arnoldi"]["primary"],
        path="$.stability.arnoldi.primary",
        expected_count=24,
    )
    _verify_arnoldi_panel(
        payload["stability"]["arnoldi"]["convergence"],
        path="$.stability.arnoldi.convergence",
        expected_count=36,
    )
    arms = payload["stability"]["continuation_arms"]
    _nonnull_prefix_length(arms, path="$.stability.continuation_arms")
    for index, arm in enumerate(arms):
        if arm is not None:
            _verify_trajectory(
                arm, path=f"$.stability.continuation_arms[{index}]"
            )
    exact_arm = payload["stability"]["exact_arm"]
    if exact_arm is not None:
        _verify_trajectory(exact_arm, path="$.stability.exact_arm")

    stability_evidence = _stability_evidence(payload)
    if payload["stability"]["gates"] != stability_evidence:
        raise ValueError("$.stability.gates: reconstruction mismatch")
    controls_evidence = _controls_evidence(payload)
    if payload["controls"]["pass"] is not controls_evidence:
        raise ValueError("$.controls.pass: reconstruction mismatch")

    def complete_root(index: int) -> bool:
        panel = root_panels[index]
        return bool(
            panel is not None
            and panel["centers_agree"]
            and panel["certificate_80"]["strict_interior"]
            and panel["certificate_120"]["strict_interior"]
        )

    forward_roots_complete = all(complete_root(index) for index in range(2, 7))
    lower_roots_complete = all(complete_root(index) for index in (2, 1, 0))
    forward_homotopies_complete = all(
        row is not None and row["status"] == "pass"
        for row in payload["finite_branch"]["homotopies"][:4]
    )
    lower_homotopies_complete = all(
        row is not None and row["status"] == "pass"
        for row in payload["finite_branch"]["homotopies"][4:]
    )
    tail_panels = payload["infinite_tail"]["certificate_panels"]
    tail_complete = bool(
        all(
            row is not None and row["certificate"]["strict_interior"]
            for row in tail_panels
        )
        and payload["infinite_tail"]["panel_comparison"]["overlap"]
    )
    prerequisites = {
        "G1F": forward_roots_complete,
        "G1R": lower_roots_complete,
        "G2F": forward_homotopies_complete,
        "G2R": lower_homotopies_complete,
        "G3": drift["pass"],
        "G4": tail_complete,
        "G5": all(
            stability_evidence[name]
            for name in (
                "continuations_complete",
                "exact_arm",
                "panels_complete",
                "panel_agreement",
                "perturbation_contraction",
                "ritz_residuals",
                "symmetries",
            )
        ),
        "G6": controls_evidence,
    }
    g0_complete = bool(
        payload["finite_branch"]["direct_replay_pass"]
        and all(
            row["two_ulp_gate"] and row["nonzero_finite"]
            for row in payload["infinite_tail"]["q_representations"]
        )
    )
    if gates["G0"] == "pass" and not g0_complete:
        raise ValueError("$.classification.gates.G0: false pass")
    for gate_name, complete in prerequisites.items():
        if gates[gate_name] == "pass" and not complete:
            raise ValueError(f"$.classification.gates.{gate_name}: false pass")
    if gates["large_h_instability_supported"] is not stability_evidence[
        "instability_supported"
    ]:
        raise ValueError(
            "$.classification.gates.large_h_instability_supported: mismatch"
        )
    expected_finite_only = bool(gates["G5"] == "pass" and gates["G4"] != "pass")
    if observed["finite_large_h_stability_only"] is not expected_finite_only:
        raise ValueError("$.classification.finite_large_h_stability_only: mismatch")
    expected = classify_horizon(
        observed["gates"],
        lower_tail_status=observed["lower_tail_status"],
    )
    for key in ("decision", "precedence_rank", "p5_governance_review_open"):
        if observed[key] != expected[key]:
            raise ValueError(f"$.classification.{key}: reconstruction mismatch")


def _atomic_write_bytes(path: Path, content: bytes) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.tmp")
    temporary.write_bytes(content)
    os.replace(temporary, destination)


def publish_result(
    payload: dict[str, Any],
    *,
    result_path: Path,
    report_path: Path,
    manifest_path: Path,
) -> None:
    validate_result(payload)
    result_bytes = (
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    report_bytes = (
        "# Rotating-wave horizon-transfer result\n\n"
        f"Decision: `{payload['classification']['decision']}`.\n"
    ).encode("utf-8")
    _atomic_write_bytes(Path(result_path), result_bytes)
    _atomic_write_bytes(Path(report_path), report_bytes)
    manifest = {
        "schema": "scalar-memory-rotating-wave-horizon-publication-v2",
        "artifacts": [
            {
                "role": "result-json",
                "path": Path(result_path).name,
                "sha256": hashlib.sha256(result_bytes).hexdigest(),
            },
            {
                "role": "readable-report",
                "path": Path(report_path).name,
                "sha256": hashlib.sha256(report_bytes).hexdigest(),
            },
        ],
    }
    manifest_bytes = (
        json.dumps(manifest, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    _atomic_write_bytes(Path(manifest_path), manifest_bytes)
