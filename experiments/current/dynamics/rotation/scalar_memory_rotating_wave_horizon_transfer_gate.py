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
    "scalar_memory_rotating_wave_horizon_transfer_result_schema_v1.json"
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
        if len(value) != definition["length"]:
            raise ValueError(
                f"{path}: array:{name} expected length {definition['length']}"
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


def _witness_value(specification: str, contract: dict[str, Any]) -> Any:
    if specification.startswith("nullable:"):
        return None
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
        return [
            _witness_value(definition["item"], contract)
            for _ in range(definition["length"])
        ]
    if kind == "object":
        return {
            key: _witness_value(child, contract)
            for key, child in contract["objects"][name].items()
        }
    raise ValueError(f"unknown witness specification {specification}")


def contract_witness() -> dict[str, Any]:
    contract = _load_result_schema()
    result = _witness_value(contract["root"], contract)
    result["identity"]["parameters"] = {
        **PARAMETERS,
        "anchor_radius": 0.946517504804225,
        "anchor_theta": 0.015770381717135,
        "epsilon": 0.0,
    }
    result["publication"]["artifacts"][0]["role"] = "result-json"
    result["publication"]["artifacts"][1]["role"] = "readable-report"
    result["publication"]["manifest_published_last"] = True
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
    result["stability"]["horizon"] = 2400
    primary = result["stability"]["arnoldi"]["primary"]
    convergence = result["stability"]["arnoldi"]["convergence"]
    primary.update(
        {"expected_count": 24, "requested_count": 24, "ncv": 96, "max_iterations": 20000, "tolerance": 1e-10}
    )
    convergence.update(
        {"expected_count": 36, "requested_count": 36, "ncv": 144, "max_iterations": 40000, "tolerance": 1e-12}
    )
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


def _verify_result_semantics(payload: dict[str, Any]) -> None:
    expected_parameters = {
        **PARAMETERS,
        "anchor_radius": 0.946517504804225,
        "anchor_theta": 0.015770381717135,
        "epsilon": 0.0,
    }
    if payload["identity"]["parameters"] != expected_parameters:
        raise ValueError("$.identity.parameters: registered values do not match")
    root_horizons = [
        panel["horizon"] for panel in payload["finite_branch"]["root_panels"]
    ]
    if root_horizons != list(HORIZONS):
        raise ValueError("$.finite_branch.root_panels: horizon order mismatch")
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
    drift_rows = payload["finite_branch"]["drift"]["interval_upper_bounds"]
    root_boxes = {
        panel["horizon"]: panel["inner_intersection"]
        for panel in payload["finite_branch"]["root_panels"]
    }
    for index, (first_horizon, second_horizon) in enumerate(
        ((1800, 2400), (2400, 3600))
    ):
        radius_component, theta_component = _interval_drift_components(
            root_boxes[first_horizon],
            root_boxes[second_horizon],
            radius_scale=0.946517504804225,
            theta_scale=0.015770381717135,
        )
        row = drift_rows[index]
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
    observed = payload["classification"]
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
        "schema": "scalar-memory-rotating-wave-horizon-publication-v1",
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
