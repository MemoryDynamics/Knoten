"""Independent standard-library audit for the horizon-transfer publication."""

from __future__ import annotations

import copy
from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import struct
from typing import Any, Sequence
import uuid


SCHEMA_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_transfer_result_schema_v3.json"
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


def _read_bytes(path: Path) -> bytes:
    return Path(path).read_bytes()


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant {value}")


def _json_loads(content: bytes, *, path: str) -> Any:
    try:
        return json.loads(content, parse_constant=_reject_json_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{path}: invalid UTF-8 JSON") from error


def _load_result_schema(path: Path = SCHEMA_PATH) -> dict[str, Any]:
    result = _json_loads(_read_bytes(path), path=str(path))
    if type(result) is not dict:
        raise TypeError("schema root must be an object")
    return result


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


def validate_result(
    payload: dict[str, Any],
    contract: dict[str, Any] | None = None,
) -> None:
    active_contract = _load_result_schema() if contract is None else contract
    _validate_schema_value(
        payload,
        active_contract["root"],
        path="$",
        contract=active_contract,
    )


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


def _decimal_box(center: str, half_width: str) -> list[str]:
    with localcontext() as context:
        context.prec = 180
        value = Decimal(center)
        width = Decimal(half_width)
        return [format(value - width, "f"), format(value + width, "f")]


def _set_certificate_witness(
    certificate: dict[str, Any],
    *,
    radius: str,
    theta: str,
    half_width: str,
) -> None:
    certificate["box"] = {
        "radius": _decimal_box(radius, half_width),
        "theta": _decimal_box(theta, half_width),
    }
    image_width = format(Decimal(half_width) / 2, "f")
    certificate["krawczyk_image"] = [
        _decimal_box(radius, image_width),
        _decimal_box(theta, image_width),
    ]
    certificate["strict_interior"] = True


def _vector_sha256(values: Sequence[float]) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(struct.pack("<d", float(value)))
    return digest.hexdigest()


def _registered_perturbation_vectors(
    *,
    radius: float,
    theta: float,
    horizon: int,
) -> tuple[float, dict[str, list[float]]]:
    amplitude = 1e-7 * radius
    dimension = 2 * horizon
    radial = [0.0] * dimension
    tangential = [0.0] * dimension
    radial[0] = amplitude
    tangential[1] = amplitude
    inverse_root_h = 1.0 / math.sqrt(horizon)
    translation_x = [
        inverse_root_h if index % 2 == 0 else 0.0 for index in range(dimension)
    ]
    translation_y = [
        0.0 if index % 2 == 0 else inverse_root_h for index in range(dimension)
    ]
    rotation = []
    for age in range(horizon):
        x = radius * math.cos(-theta * age)
        y = radius * math.sin(-theta * age)
        rotation.extend((-y, x))
    for basis in (translation_x, translation_y):
        projection = math.fsum(a * b for a, b in zip(rotation, basis, strict=True))
        rotation = [
            value - projection * direction
            for value, direction in zip(rotation, basis, strict=True)
        ]
    rotation_norm = math.sqrt(math.fsum(value * value for value in rotation))
    rotation = [value / rotation_norm for value in rotation]
    full = [
        math.sin(0.37 * index) + math.cos(0.11 * index)
        for index in range(dimension)
    ]
    for basis in (translation_x, translation_y, rotation):
        projection = math.fsum(a * b for a, b in zip(full, basis, strict=True))
        full = [
            value - projection * direction
            for value, direction in zip(full, basis, strict=True)
        ]
    full_norm = math.sqrt(math.fsum(value * value for value in full))
    full = [amplitude * value / full_norm for value in full]
    return amplitude, {
        "radial": radial,
        "tangential": tangential,
        "full-history-transverse": full,
    }


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
        radius = "0.946517504804225"
        theta = "0.015770381717135"
        for precision in (80, 120):
            panel[f"newton_{precision}"]["radius"] = radius
            panel[f"newton_{precision}"]["theta"] = theta
        for precision in (80, 120):
            _set_certificate_witness(
                panel[f"outer_certificate_{precision}"],
                radius=radius,
                theta=theta,
                half_width="1e-8",
            )
            _set_certificate_witness(
                panel[f"inner_certificate_{precision}"],
                radius=radius,
                theta=theta,
                half_width="1e-30",
            )
        panel["inner_intersection"] = {
            "radius": _decimal_box(radius, "5e-31"),
            "theta": _decimal_box(theta, "5e-31"),
        }
        panel["centers_agree"] = True
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
            slab["box"] = {
                "radius": _decimal_box("0.946517504804225", "1e-4"),
                "theta": _decimal_box("0.015770381717135", "1e-6"),
            }
            slab["krawczyk_image"] = [
                _decimal_box("0.946517504804225", "5e-5"),
                _decimal_box("0.015770381717135", "5e-7"),
            ]
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
    drift_rows = []
    for first_slot, second_slot in ((4, 5), (5, 6)):
        first_panel = result["finite_branch"]["root_panels"][first_slot]
        second_panel = result["finite_branch"]["root_panels"][second_slot]
        radius_component, theta_component = _interval_drift_components(
            first_panel["inner_intersection"],
            second_panel["inner_intersection"],
            radius_scale=0.946517504804225,
            theta_scale=0.015770381717135,
        )
        drift_rows.append(
            {
                "from_horizon": first_panel["horizon"],
                "to_horizon": second_panel["horizon"],
                "radius_component": radius_component,
                "theta_component": theta_component,
                "upper_bound": max(radius_component, theta_component),
            }
        )
    result["finite_branch"]["drift"] = {
        "center_diagnostics": copy.deepcopy(drift_rows),
        "interval_upper_bounds": drift_rows,
        "mutation_closes_pass": True,
        "pass": True,
    }
    result["infinite_tail"]["q_representations"] = q_representations(
        HORIZONS,
        alpha=PARAMETERS["alpha"],
    )
    result["infinite_tail"]["bounds"] = [
        {"horizon": horizon, **tail_bounds(horizon=horizon, parameters=PARAMETERS)}
        for horizon in HORIZONS
    ]
    for precision, panel in zip(
        (120, 160),
        result["infinite_tail"]["certificate_panels"],
        strict=True,
    ):
        panel["precision_dps"] = precision
        panel["root"] = ["0.946517504804225", "0.015770381717135"]
        _set_certificate_witness(
            panel["certificate"],
            radius=panel["root"][0],
            theta=panel["root"][1],
            half_width="1e-10",
        )
    result["infinite_tail"]["panel_comparison"] = {
        "intersection": {
            "radius": _decimal_box("0.946517504804225", "5e-11"),
            "theta": _decimal_box("0.015770381717135", "5e-11"),
        },
        "overlap": True,
    }
    result["stability"]["horizon"] = 2400
    result["stability"]["rounded_root"] = [
        0.946517504804225,
        0.015770381717135,
    ]
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
                    "eigenvalue": [
                        math.cos(0.015770381717135)
                        if classification == "translation"
                        else 1.0,
                        (1.0 if index == 0 else -1.0)
                        * math.sin(0.015770381717135)
                        if classification == "translation"
                        else 0.0,
                    ],
                    "modulus": 1.0,
                    "classification": classification,
                }
            )
            pair[f"{classification}_overlap"] = 1.0
    arm_names = ("radial", "tangential", "full-history-transverse")
    amplitude, perturbations = _registered_perturbation_vectors(
        radius=result["stability"]["rounded_root"][0],
        theta=result["stability"]["rounded_root"][1],
        horizon=2400,
    )
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
                "amplitude": amplitude,
                "perturbation": perturbations[name],
                "perturbation_sha256": _vector_sha256(perturbations[name]),
            }
        )
        for index, sample in enumerate(arm["samples"]):
            sample.update(
                {"step": 10 * index, "distance": 1.0 if index == 0 else 0.05}
            )
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


def _positive_float_bits(value: float) -> int:
    if not value > 0.0 or not math.isfinite(value):
        raise ValueError("ULP comparison requires a positive finite value")
    return struct.unpack(">Q", struct.pack(">d", value))[0]


def q_representations(
    horizons: Sequence[int],
    *,
    alpha: float,
) -> list[dict[str, Any]]:
    alpha64 = float(alpha)
    q64 = 1.0 - alpha64
    rows = []
    if alpha64 != 0.01:
        raise ValueError("auditor only accepts the registered alpha")
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


def tail_bounds(
    *,
    horizon: int,
    parameters: dict[str, float],
) -> dict[str, str]:
    with localcontext() as context:
        context.prec = 100
        q = Decimal(1) - Decimal(str(parameters["alpha"]))
        eta = Decimal(str(parameters["eta"]))
        mass = Decimal(str(parameters["memory_mass"]))
        amplitude_rep = Decimal(str(parameters["amplitude_rep"]))
        amplitude_att = Decimal(str(parameters["amplitude_att"]))
        sigma_rep = Decimal(str(parameters["sigma_rep"]))
        sigma_att = Decimal(str(parameters["sigma_att"]))
        phi0 = amplitude_rep / sigma_rep**2 + amplitude_att / sigma_att**2
        phi1 = (-Decimal("0.5")).exp() * (
            amplitude_rep / sigma_rep**3 + amplitude_att / sigma_att**3
        )
        q_power = q**horizon
        return {
            "residual_bound": _outward_decimal(2 * eta * mass * phi0 * q_power),
            "jacobian_radius_bound": _outward_decimal(4 * eta * mass * phi1 * q_power),
            "jacobian_theta_bound": _outward_decimal(
                eta
                * mass
                * (phi0 + 2 * Decimal("1.1") * phi1)
                * q_power
                * (Decimal(horizon) + q / Decimal(str(parameters["alpha"])))
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


def _decimal_interval(values: Sequence[str], *, path: str) -> tuple[Decimal, Decimal]:
    if len(values) != 2:
        raise ValueError(f"{path}: expected two endpoints")
    lower, upper = (Decimal(value) for value in values)
    if lower > upper:
        raise ValueError(f"{path}: reversed interval")
    return lower, upper


def _interval_intersection(
    first: Sequence[str], second: Sequence[str], *, path: str
) -> list[str] | None:
    first_lower, first_upper = _decimal_interval(first, path=f"{path}.first")
    second_lower, second_upper = _decimal_interval(second, path=f"{path}.second")
    lower = max(first_lower, second_lower)
    upper = min(first_upper, second_upper)
    return None if lower > upper else [format(lower, "f"), format(upper, "f")]


def _image_intersection(
    first: Sequence[Sequence[str]],
    second: Sequence[Sequence[str]],
    *,
    path: str,
) -> dict[str, list[str]] | None:
    radius = _interval_intersection(first[0], second[0], path=f"{path}.radius")
    theta = _interval_intersection(first[1], second[1], path=f"{path}.theta")
    return None if radius is None or theta is None else {"radius": radius, "theta": theta}


def _strict_image_in_box(
    image: Sequence[Sequence[str]],
    box: dict[str, Sequence[str]],
    *,
    path: str,
) -> bool:
    for index, name in enumerate(("radius", "theta")):
        image_lower, image_upper = _decimal_interval(
            image[index], path=f"{path}.image.{name}"
        )
        box_lower, box_upper = _decimal_interval(
            box[name], path=f"{path}.box.{name}"
        )
        if not box_lower < image_lower <= image_upper < box_upper:
            return False
    return True


def _verify_certificate(
    certificate: dict[str, Any],
    *,
    center: Sequence[str] | None = None,
    half_width: str,
    path: str,
) -> bool:
    with localcontext() as context:
        context.prec = 180
        expected_width = 2 * Decimal(half_width)
        for index, name in enumerate(("radius", "theta")):
            lower, upper = _decimal_interval(
                certificate["box"][name], path=f"{path}.box.{name}"
            )
            if upper - lower != expected_width:
                raise ValueError(f"{path}.box.{name}: half-width mismatch")
            if center is not None and (lower + upper) / 2 != Decimal(center[index]):
                raise ValueError(f"{path}.box.{name}: center mismatch")
    strict = _strict_image_in_box(
        certificate["krawczyk_image"], certificate["box"], path=path
    )
    if certificate["strict_interior"] is not strict:
        raise ValueError(f"{path}.strict_interior: reconstruction mismatch")
    return strict


def _verify_root_panel(panel: dict[str, Any], *, path: str) -> bool:
    if (
        panel["newton_80"]["precision_dps"],
        panel["newton_120"]["precision_dps"],
        panel["newton_80"]["steps"],
        panel["newton_120"]["steps"],
    ) != (80, 120, 8, 8):
        raise ValueError(f"{path}: Newton configuration mismatch")
    with localcontext() as context:
        context.prec = 180
        centers_agree = all(
            abs(
                Decimal(panel["newton_80"][name])
                - Decimal(panel["newton_120"][name])
            )
            <= Decimal("1e-50")
            for name in ("radius", "theta")
        )
    if panel["centers_agree"] is not centers_agree:
        raise ValueError(f"{path}.centers_agree: reconstruction mismatch")
    certificates = []
    for precision in (80, 120):
        center = (
            panel[f"newton_{precision}"]["radius"],
            panel[f"newton_{precision}"]["theta"],
        )
        for scale, half_width in (("outer", "1e-8"), ("inner", "1e-30")):
            certificates.append(
                _verify_certificate(
                    panel[f"{scale}_certificate_{precision}"],
                    center=center,
                    half_width=half_width,
                    path=f"{path}.{scale}_certificate_{precision}",
                )
            )
    intersection = _image_intersection(
        panel["inner_certificate_80"]["krawczyk_image"],
        panel["inner_certificate_120"]["krawczyk_image"],
        path=f"{path}.inner_intersection",
    )
    if panel["inner_intersection"] != intersection:
        raise ValueError(f"{path}.inner_intersection: reconstruction mismatch")
    return bool(centers_agree and intersection is not None and all(certificates))


def _verify_root_and_homotopy_slots(payload: dict[str, Any]) -> list[bool | None]:
    roots = payload["finite_branch"]["root_panels"]
    for index, panel in enumerate(roots):
        if panel is not None and panel["horizon"] != HORIZONS[index]:
            raise ValueError("$.finite_branch.root_panels: horizon order mismatch")
    for previous, current in ((2, 3), (3, 4), (4, 5), (5, 6), (2, 1), (1, 0)):
        if roots[current] is not None and roots[previous] is None:
            raise ValueError("$.finite_branch.root_panels: dependency gap")
    root_evidence = [
        None
        if panel is None
        else _verify_root_panel(panel, path=f"$.finite_branch.root_panels[{index}]")
        for index, panel in enumerate(roots)
    ]

    edges = (
        (1200, 1500, "forward", 2, 3),
        (1500, 1800, "forward", 3, 4),
        (1800, 2400, "forward", 4, 5),
        (2400, 3600, "forward", 5, 6),
        (1200, 900, "lower-tail", 2, 1),
        (900, 600, "lower-tail", 1, 0),
    )
    homotopies = payload["finite_branch"]["homotopies"]
    _nonnull_prefix_length(homotopies[:4], path="$.finite_branch.homotopies[0:4]")
    _nonnull_prefix_length(homotopies[4:], path="$.finite_branch.homotopies[4:6]")
    for index, (homotopy, edge) in enumerate(zip(homotopies, edges, strict=True)):
        if homotopy is None:
            continue
        first, second, direction, first_slot, second_slot = edge
        if roots[first_slot] is None or roots[second_slot] is None:
            raise ValueError(
                f"$.finite_branch.homotopies[{index}]: missing endpoint root"
            )
        if (
            homotopy["from_horizon"],
            homotopy["to_horizon"],
            homotopy["direction"],
        ) != (first, second, direction):
            raise ValueError(f"$.finite_branch.homotopies[{index}]: edge mismatch")
        count = _nonnull_prefix_length(
            homotopy["slabs"],
            path=f"$.finite_branch.homotopies[{index}].slabs",
        )
        passing = count == 64
        for slab_index, slab in enumerate(homotopy["slabs"][:count]):
            if slab["index"] != slab_index:
                raise ValueError(
                    f"$.finite_branch.homotopies[{index}].slabs: index mismatch"
                )
            path = f"$.finite_branch.homotopies[{index}].slabs[{slab_index}]"
            expected_s = [
                format(Decimal(slab_index) / Decimal(64), "f"),
                format(Decimal(slab_index + 1) / Decimal(64), "f"),
            ]
            if slab["s_interval"] != expected_s:
                raise ValueError(f"{path}.s_interval: reconstruction mismatch")
            for coordinate, half_width in (("radius", "1e-4"), ("theta", "1e-6")):
                lower, upper = _decimal_interval(
                    slab["box"][coordinate], path=f"{path}.box.{coordinate}"
                )
                if upper - lower != 2 * Decimal(half_width):
                    raise ValueError(f"{path}.box.{coordinate}: width mismatch")
                with localcontext() as context:
                    context.prec = 180
                    interpolation = Decimal(2 * slab_index + 1) / Decimal(128)
                    start = Decimal(roots[first_slot]["newton_120"][coordinate])
                    stop = Decimal(roots[second_slot]["newton_120"][coordinate])
                    expected_center = (1 - interpolation) * start + interpolation * stop
                    if (lower + upper) / 2 != expected_center:
                        raise ValueError(f"{path}.box.{coordinate}: center mismatch")
            strict = _strict_image_in_box(
                slab["krawczyk_image"], slab["box"], path=path
            )
            if slab["strict_interior"] is not strict:
                raise ValueError(f"{path}.strict_interior: reconstruction mismatch")
            overlap = None
            if slab_index:
                overlap = _image_intersection(
                    homotopy["slabs"][slab_index - 1]["krawczyk_image"],
                    slab["krawczyk_image"],
                    path=f"{path}.overlap",
                ) is not None
            if slab["overlaps_previous"] is not overlap:
                raise ValueError(f"{path}.overlaps_previous: reconstruction mismatch")
            passing = passing and strict and (slab_index == 0 or overlap)
        if homotopy["status"] == "pass" and not (
            passing and homotopy["pass"]
        ):
            raise ValueError(f"$.finite_branch.homotopies[{index}]: false pass")
    return root_evidence


def _arnoldi_start_vectors() -> dict[str, list[float]]:
    component = float.fromhex("0x1.d8f7208e6b82cp-7")
    result = {}
    for name, seed in (("primary", 0x243F6A88), ("convergence", 0x85A308D3)):
        state = seed
        values = []
        for _ in range(4800):
            state = (1664525 * state + 1013904223) & 0xFFFFFFFF
            values.append(component if state & 0x80000000 else -component)
        result[name] = values
    return result


def _arnoldi_start_hashes() -> dict[str, str]:
    return {
        name: _vector_sha256(values)
        for name, values in _arnoldi_start_vectors().items()
    }


def _verify_stability_inputs(payload: dict[str, Any]) -> None:
    stability = payload["stability"]
    root_panel = payload["finite_branch"]["root_panels"][5]
    if root_panel is None:
        has_spectral_output = any(
            pair is not None
            for name in ("primary", "convergence")
            for pair in stability["arnoldi"][name]["eigenpairs"]
        )
        if (
            stability["rounded_root"] is not None
            or has_spectral_output
            or any(arm is not None for arm in stability["continuation_arms"])
            or stability["exact_arm"] is not None
        ):
            raise ValueError("$.stability: inputs without H=2400 root")
        return
    expected_root = [
        float(root_panel["newton_120"]["radius"]),
        float(root_panel["newton_120"]["theta"]),
    ]
    if stability["rounded_root"] != expected_root:
        raise ValueError("$.stability.rounded_root: reconstruction mismatch")
    starts = _arnoldi_start_hashes()
    for name in ("primary", "convergence"):
        if stability["arnoldi"][name]["start_sha256"] != starts[name]:
            raise ValueError(f"$.stability.arnoldi.{name}.start_sha256: mismatch")
    amplitude, perturbations = _registered_perturbation_vectors(
        radius=expected_root[0], theta=expected_root[1], horizon=2400
    )
    for index, (name, arm) in enumerate(
        zip(
            ("radial", "tangential", "full-history-transverse"),
            stability["continuation_arms"],
            strict=True,
        )
    ):
        if arm is None:
            continue
        path = f"$.stability.continuation_arms[{index}]"
        expected = perturbations[name]
        if arm["name"] != name or arm["amplitude"] != amplitude:
            raise ValueError(f"{path}: registered perturbation mismatch")
        if arm["perturbation"] != expected:
            raise ValueError(f"{path}.perturbation: reconstruction mismatch")
        if arm["perturbation_sha256"] != _vector_sha256(expected):
            raise ValueError(f"{path}.perturbation_sha256: reconstruction mismatch")


def _verify_partial_panels_and_trajectories(payload: dict[str, Any]) -> None:
    for name, expected in (("primary", 24), ("convergence", 36)):
        panel = payload["stability"]["arnoldi"][name]
        count = _nonnull_prefix_length(
            panel["eigenpairs"], path=f"$.stability.arnoldi.{name}.eigenpairs"
        )
        missing_vector = any(
            row["vector"] is None for row in panel["eigenpairs"][:count]
        )
        if panel["expected_count"] != expected or panel["requested_count"] != expected:
            raise ValueError(f"$.stability.arnoldi.{name}: count mismatch")
        configuration = {24: (96, 20000, 1e-10), 36: (144, 40000, 1e-12)}[
            expected
        ]
        if (panel["ncv"], panel["max_iterations"], panel["tolerance"]) != configuration:
            raise ValueError(f"$.stability.arnoldi.{name}: configuration mismatch")
        if panel["status"] == "complete" and (count != expected or missing_vector):
            raise ValueError(
                f"$.stability.arnoldi.{name}: false complete status"
            )
        if panel["status"] == "missing-vectors" and not missing_vector:
            raise ValueError(
                f"$.stability.arnoldi.{name}: missing vector not represented"
            )
        previous_modulus = math.inf
        for index, pair in enumerate(panel["eigenpairs"][:count]):
            modulus = abs(complex(*pair["eigenvalue"]))
            if pair["modulus"] != modulus:
                raise ValueError(
                    f"$.stability.arnoldi.{name}.eigenpairs[{index}].modulus: mismatch"
                )
            classification = (
                "translation"
                if pair["translation_overlap"] >= 0.99
                else "rotation"
                if pair["rotation_overlap"] >= 0.99
                else "transverse"
            )
            if pair["classification"] != classification:
                raise ValueError(
                    f"$.stability.arnoldi.{name}.eigenpairs[{index}].classification: mismatch"
                )
            if modulus > previous_modulus:
                raise ValueError(f"$.stability.arnoldi.{name}.eigenpairs: unsorted")
            previous_modulus = modulus

    arms = payload["stability"]["continuation_arms"]
    _nonnull_prefix_length(arms, path="$.stability.continuation_arms")
    trajectories = [
        (f"$.stability.continuation_arms[{index}]", arm)
        for index, arm in enumerate(arms)
        if arm is not None
    ]
    exact = payload["stability"]["exact_arm"]
    if exact is not None:
        trajectories.append(("$.stability.exact_arm", exact))
    for path, arm in trajectories:
        count = _nonnull_prefix_length(arm["samples"], path=f"{path}.samples")
        for index, sample in enumerate(arm["samples"][:count]):
            if (index < count - 1 or arm["completed"]) and sample["step"] != 10 * index:
                raise ValueError(f"{path}.samples: step mismatch")
        if arm["completed"] and (count != 501 or arm["stopped"]):
            raise ValueError(f"{path}: false complete status")
        distances = [sample["distance"] for sample in arm["samples"][:count]]
        if "initial_distance" in arm and distances:
            initial = distances[0]
            final = distances[-1]
            ratio = final / initial if initial > 0.0 else math.inf
            growth = max(distances) / initial if initial > 0.0 else math.inf
            if (
                arm["initial_distance"] != initial
                or arm["final_distance"] != final
                or arm["final_ratio"] != ratio
                or arm["growth_factor"] != growth
            ):
                raise ValueError(f"{path}: trajectory summary mismatch")
        if "maximum_distance" in arm and distances:
            if arm["maximum_distance"] != max(distances):
                raise ValueError(f"{path}.maximum_distance: reconstruction mismatch")


def _verify_arnoldi_summary(payload: dict[str, Any]) -> None:
    panels = [
        payload["stability"]["arnoldi"][name]
        for name in ("primary", "convergence")
    ]
    complete = all(panel["status"] == "complete" for panel in panels)
    rounded_root = payload["stability"]["rounded_root"]
    theta = 0.0 if rounded_root is None else rounded_root[1]
    expected_translations = (
        complex(math.cos(theta), math.sin(theta)),
        complex(math.cos(theta), -math.sin(theta)),
    )
    symmetry_pass = complete
    for panel in panels:
        pairs = [pair for pair in panel["eigenpairs"] if pair is not None]
        translations = [pair for pair in pairs if pair["classification"] == "translation"]
        rotations = [pair for pair in pairs if pair["classification"] == "rotation"]
        symmetry_pass = bool(
            symmetry_pass
            and len(translations) >= 2
            and all(
                min(abs(complex(*pair["eigenvalue"]) - expected) for pair in translations)
                <= 1e-7
                for expected in expected_translations
            )
            and any(abs(complex(*pair["eigenvalue"]) - 1.0) <= 1e-7 for pair in rotations)
        )
    primary = [
        pair
        for pair in panels[0]["eigenpairs"]
        if pair is not None and pair["classification"] == "transverse"
    ]
    convergence = [
        pair
        for pair in panels[1]["eigenpairs"]
        if pair is not None and pair["classification"] == "transverse"
    ]
    distance = None
    if primary and convergence:
        leading = complex(*primary[0]["eigenvalue"])
        distance = min(abs(leading - complex(*pair["eigenvalue"])) for pair in convergence)
    agreement = payload["stability"]["arnoldi"]["panel_agreement"]
    expected_pass = bool(
        complete and symmetry_pass and distance is not None and distance <= 1e-5
    )
    if agreement["symmetry_pass"] is not symmetry_pass:
        raise ValueError("$.stability.arnoldi.panel_agreement.symmetry_pass: mismatch")
    if agreement["leading_transverse_distance"] != distance:
        raise ValueError(
            "$.stability.arnoldi.panel_agreement.leading_transverse_distance: mismatch"
        )
    if agreement["pass"] is not expected_pass:
        raise ValueError("$.stability.arnoldi.panel_agreement.pass: mismatch")


def _stability_evidence(payload: dict[str, Any]) -> dict[str, bool]:
    stability = payload["stability"]
    panels = (
        stability["arnoldi"]["primary"],
        stability["arnoldi"]["convergence"],
    )
    panels_complete = all(
        panel["status"] == "complete"
        and all(
            pair is not None and pair["vector"] is not None
            for pair in panel["eigenpairs"]
        )
        for panel in panels
    )
    ritz_residuals = panels_complete and all(
        pair["normalized_residual"] <= 1e-8
        for panel in panels
        for pair in panel["eigenpairs"]
    )
    agreement = bool(
        panels_complete and stability["arnoldi"]["panel_agreement"]["pass"]
    )
    symmetries = bool(
        panels_complete
        and stability["arnoldi"]["panel_agreement"]["symmetry_pass"]
    )
    arms = stability["continuation_arms"]
    continuations_complete = all(
        arm is not None and arm["completed"] and not arm["stopped"] for arm in arms
    )
    contraction = bool(
        continuations_complete and all(arm["final_ratio"] <= 0.1 for arm in arms)
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
    leading = [
        max(
            (
                pair["modulus"]
                for pair in panel["eigenpairs"]
                if pair is not None and pair["classification"] == "transverse"
            ),
            default=-math.inf,
        )
        for panel in panels
    ]
    unstable_spectrum = bool(
        panels_complete
        and agreement
        and all(value > 1.0 + 1e-6 for value in leading)
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
    circular = controls["circular_cases"]
    eta_zero = controls["eta_zero_cases"]
    mutations = controls["mutations"]
    return bool(
        [row["horizon"] for row in circular] == [17, 257, *HORIZONS]
        and all(
            row["pass"]
            is (
                row["complete_state_relative_error"] < 5e-14
                and row["new_point_relative_error"] < 5e-14
            )
            for row in circular
        )
        and all(row["pass"] for row in circular)
        and [row["horizon"] for row in eta_zero] == list(HORIZONS)
        and all(
            row["steps"] == row["horizon"] + 1
            and row["pass"] is (row["maximum_deviation"] < 1e-14)
            and row["pass"]
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


def _verify_reconstructed_values(payload: dict[str, Any]) -> None:
    expected_parameters = {
        **PARAMETERS,
        "anchor_radius": 0.946517504804225,
        "anchor_theta": 0.015770381717135,
        "epsilon": 0.0,
    }
    if payload["identity"]["parameters"] != expected_parameters:
        raise ValueError("$.identity.parameters: registered values do not match")

    expected_q = q_representations(HORIZONS, alpha=PARAMETERS["alpha"])
    observed_q = payload["infinite_tail"]["q_representations"]
    if observed_q != expected_q:
        raise ValueError("$.infinite_tail.q_representations: reconstruction mismatch")

    expected_bounds = [
        {"horizon": horizon, **tail_bounds(horizon=horizon, parameters=PARAMETERS)}
        for horizon in HORIZONS
    ]
    if payload["infinite_tail"]["bounds"] != expected_bounds:
        raise ValueError("$.infinite_tail.bounds: reconstruction mismatch")

    root_evidence = _verify_root_and_homotopy_slots(payload)
    _verify_partial_panels_and_trajectories(payload)
    _verify_stability_inputs(payload)
    _verify_arnoldi_summary(payload)
    root_panels = payload["finite_branch"]["root_panels"]
    panels = {
        panel["horizon"]: panel["inner_intersection"]
        for panel in root_panels
        if panel is not None and panel["inner_intersection"] is not None
    }
    expected_pairs = ((1800, 2400), (2400, 3600))
    observed_drift = payload["finite_branch"]["drift"]["interval_upper_bounds"]
    for index, (first_horizon, second_horizon) in enumerate(expected_pairs):
        row = observed_drift[index]
        if first_horizon not in panels or second_horizon not in panels:
            if row is not None:
                raise ValueError(
                    f"$.finite_branch.drift.interval_upper_bounds[{index}]: "
                    "value without prerequisite root"
                )
            continue
        radius_component, theta_component = _interval_drift_components(
            panels[first_horizon],
            panels[second_horizon],
            radius_scale=0.946517504804225,
            theta_scale=0.015770381717135,
        )
        if (
            row["from_horizon"] != first_horizon
            or row["to_horizon"] != second_horizon
            or row["radius_component"] != radius_component
            or row["theta_component"] != theta_component
            or row["upper_bound"] != max(radius_component, theta_component)
        ):
            raise ValueError(
                f"$.finite_branch.drift.interval_upper_bounds[{index}]: "
                "reconstruction mismatch"
            )

    drift_pass = bool(
        all(row is not None for row in observed_drift)
        and observed_drift[1]["upper_bound"] <= 1e-8
        and observed_drift[1]["upper_bound"]
        <= 0.01 * observed_drift[0]["upper_bound"] + 1e-14
    )
    if payload["finite_branch"]["drift"]["pass"] is not drift_pass:
        raise ValueError("$.finite_branch.drift.pass: reconstruction mismatch")

    observed_classification = payload["classification"]
    gates = observed_classification["gates"]
    complete_exclusion = False
    exclusion_edges = ((1200, 1500), (1500, 1800), (1800, 2400), (2400, 3600))
    for index, attempt in enumerate(payload["finite_branch"]["exclusions"]):
        if attempt is None:
            continue
        if (attempt["from_horizon"], attempt["to_horizon"]) != exclusion_edges[index]:
            raise ValueError(f"$.finite_branch.exclusions[{index}]: edge mismatch")
        if attempt["max_depth"] != 20:
            raise ValueError(f"$.finite_branch.exclusions[{index}]: depth mismatch")
        classifications = [row["classification"] for row in attempt["leaves"]]
        for leaf_index, leaf in enumerate(attempt["leaves"]):
            path = f"$.finite_branch.exclusions[{index}].leaves[{leaf_index}]"
            classification = leaf["classification"]
            residual = leaf["residual_box"]
            image = leaf["krawczyk_image"]
            strict_field = leaf["strict_interior"]
            if classification == "residual-excluded":
                if residual is None or image is not None or strict_field is not None:
                    raise ValueError(f"{path}: residual witness mismatch")
                excludes_zero = any(
                    not (lower <= 0 <= upper)
                    for lower, upper in (
                        _decimal_interval(component, path=f"{path}.residual_box")
                        for component in residual
                    )
                )
                if not excludes_zero:
                    raise ValueError(f"{path}: residual does not exclude zero")
            elif classification == "krawczyk-root":
                if residual is not None or image is None or strict_field is None:
                    raise ValueError(f"{path}: Krawczyk witness mismatch")
                strict = _strict_image_in_box(image, leaf["box"], path=path)
                if strict_field is not strict or not strict:
                    raise ValueError(f"{path}: false Krawczyk inclusion")
            elif any(value is not None for value in (residual, image, strict_field)):
                raise ValueError(f"{path}: unresolved leaf carries a claim witness")
        if attempt["status"] == "all-residual-excluded":
            if any(value != "residual-excluded" for value in classifications):
                raise ValueError(
                    f"$.finite_branch.exclusions[{index}]: false exclusion"
                )
            complete_exclusion = True
        if attempt["status"] == "other-root" and "krawczyk-root" not in classifications:
            raise ValueError(
                f"$.finite_branch.exclusions[{index}]: missing other root"
            )
    if gates["local_branch_excluded"] is not complete_exclusion:
        raise ValueError("$.classification.gates.local_branch_excluded: mismatch")

    homotopies = payload["finite_branch"]["homotopies"]
    tail_panels = payload["infinite_tail"]["certificate_panels"]
    stability_evidence = _stability_evidence(payload)
    if payload["stability"]["gates"] != stability_evidence:
        raise ValueError("$.stability.gates: reconstruction mismatch")
    controls_evidence = _controls_evidence(payload)
    if payload["controls"]["pass"] is not controls_evidence:
        raise ValueError("$.controls.pass: reconstruction mismatch")

    def complete_root(index: int) -> bool:
        return root_evidence[index] is True

    tail_complete = False
    _nonnull_prefix_length(tail_panels, path="$.infinite_tail.certificate_panels")
    certificates = []
    for index, row in enumerate(tail_panels):
        if row is None:
            certificates.append(False)
            continue
        expected_precision = (120, 160)[index]
        if row["precision_dps"] != expected_precision:
            raise ValueError(
                f"$.infinite_tail.certificate_panels[{index}]: precision mismatch"
            )
        certificates.append(
            _verify_certificate(
                row["certificate"],
                center=row["root"],
                half_width="1e-10",
                path=f"$.infinite_tail.certificate_panels[{index}].certificate",
            )
        )
    if all(row is not None for row in tail_panels):
        intersection = _image_intersection(
            tail_panels[0]["certificate"]["krawczyk_image"],
            tail_panels[1]["certificate"]["krawczyk_image"],
            path="$.infinite_tail.panel_comparison",
        )
        comparison = payload["infinite_tail"]["panel_comparison"]
        overlap = intersection is not None
        if comparison["intersection"] != intersection or comparison["overlap"] is not overlap:
            raise ValueError("$.infinite_tail.panel_comparison: reconstruction mismatch")
        tail_complete = bool(overlap and all(certificates))
    else:
        if payload["infinite_tail"]["panel_comparison"] != {
            "intersection": None,
            "overlap": False,
        }:
            raise ValueError("$.infinite_tail.panel_comparison: value without panels")

    prerequisites = {
        "G1F": all(complete_root(index) for index in range(2, 7)),
        "G1R": all(complete_root(index) for index in (2, 1, 0)),
        "G2F": all(
            row is not None and row["status"] == "pass"
            for row in homotopies[:4]
        ),
        "G2R": all(
            row is not None and row["status"] == "pass"
            for row in homotopies[4:]
        ),
        "G3": drift_pass,
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
    if observed_classification["finite_large_h_stability_only"] is not expected_finite_only:
        raise ValueError("$.classification.finite_large_h_stability_only: mismatch")

    expected_classification = classify_horizon(
        gates,
        lower_tail_status=observed_classification["lower_tail_status"],
    )
    for key in ("decision", "precedence_rank", "p5_governance_review_open"):
        if observed_classification[key] != expected_classification[key]:
            raise ValueError(f"$.classification.{key}: reconstruction mismatch")


def audit_publication(
    *,
    manifest_path: Path,
    schema_path: Path = SCHEMA_PATH,
) -> dict[str, Any]:
    manifest_file = Path(manifest_path)
    manifest_content = _read_bytes(manifest_file)
    manifest = _json_loads(manifest_content, path=str(manifest_file))
    if type(manifest) is not dict or set(manifest) != {"schema", "artifacts"}:
        raise ValueError("manifest: invalid root fields")
    if manifest["schema"] != "scalar-memory-rotating-wave-horizon-publication-v3":
        raise ValueError("manifest: invalid schema")
    artifacts = manifest["artifacts"]
    if type(artifacts) is not list or len(artifacts) != 2:
        raise ValueError("manifest: expected exactly two artifacts")
    by_role: dict[str, bytes] = {}
    for index, row in enumerate(artifacts):
        if type(row) is not dict or set(row) != {"role", "path", "sha256"}:
            raise ValueError(f"manifest.artifacts[{index}]: invalid fields")
        role = row["role"]
        if role not in ("result-json", "readable-report") or role in by_role:
            raise ValueError(f"manifest.artifacts[{index}]: invalid role")
        relative = PurePosixPath(row["path"])
        if relative.is_absolute() or ".." in relative.parts or "\\" in row["path"]:
            raise ValueError(f"manifest.artifacts[{index}]: invalid path")
        content = _read_bytes(manifest_file.parent / Path(*relative.parts))
        digest = hashlib.sha256(content).hexdigest()
        if type(row["sha256"]) is not str or digest != row["sha256"]:
            raise ValueError(f"manifest.artifacts[{index}].sha256 mismatch")
        by_role[role] = content
    if set(by_role) != {"result-json", "readable-report"}:
        raise ValueError("manifest: missing artifact role")
    contract = _load_result_schema(Path(schema_path))
    payload = _json_loads(by_role["result-json"], path="result-json")
    validate_result(payload, contract)
    _verify_reconstructed_values(payload)
    if not by_role["readable-report"].strip():
        raise ValueError("readable report is empty")
    return {
        "schema": "scalar-memory-rotating-wave-horizon-audit-v1",
        "manifest_sha256": hashlib.sha256(manifest_content).hexdigest(),
        "hashes_pass": True,
        "schema_pass": True,
        "decision": payload["classification"]["decision"],
    }
