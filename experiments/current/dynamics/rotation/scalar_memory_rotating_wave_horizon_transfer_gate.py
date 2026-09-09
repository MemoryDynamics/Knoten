"""Target-free infrastructure for the registered rotating-wave horizon gate.

This module deliberately contains no top-level target execution.  Scientific
adapters may be tested target-free, but the registered numerical execution and
publication entry point remain closed until a separate readiness review.
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

from emergenz_knoten.rotating_wave_interval import (
    IntervalRotatingWaveParameters,
    certify_rotating_wave_box,
    certify_rotating_wave_homotopy_box,
    refine_rotating_wave_root,
)
from emergenz_knoten.rotating_wave_stability import native_fifo_step


ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_transfer_result_schema_v3.json"
)
HORIZONS = (600, 900, 1200, 1500, 1800, 2400, 3600)
_ROOT_EXECUTION_ORDER = (1200, 1500, 1800, 2400, 3600, 900, 600)
_HOMOTOPY_EDGES = (
    (1200, 1500, "forward"),
    (1500, 1800, "forward"),
    (1800, 2400, "forward"),
    (2400, 3600, "forward"),
    (1200, 900, "lower-tail"),
    (900, 600, "lower-tail"),
)
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


def _finite_interval_parameters(horizon: int) -> IntervalRotatingWaveParameters:
    if type(horizon) is not int or horizon not in HORIZONS:
        raise ValueError("horizon is outside the registered ladder")
    return IntervalRotatingWaveParameters(
        alpha="0.01",
        horizon=horizon,
        memory_mass="1.0",
        eta="0.15",
        sigma_rep="1.0",
        sigma_att="3.0",
        amplitude_rep="1.0",
        amplitude_att="3.5",
    )


def _interval_pair(record: dict[str, Any]) -> list[str]:
    return [str(record["lower"]), str(record["upper"])]


def _v3_certificate(record: dict[str, Any]) -> dict[str, Any] | None:
    if record.get("pass") is not True:
        return None
    gates = record.get("gates")
    if type(gates) is not dict or gates.get("krawczyk_strict_interior") is not True:
        return None
    return {
        "box": {
            "radius": _interval_pair(record["box"][0]),
            "theta": _interval_pair(record["box"][1]),
        },
        "interval_backend": "mpmath.iv",
        "jacobian_box": [
            [_interval_pair(value) for value in row]
            for row in record["jacobian_box"]
        ],
        "krawczyk_image": [
            _interval_pair(value) for value in record["krawczyk_image"]
        ],
        "strict_interior": True,
    }


def finite_root_backend_record(
    *,
    horizon: int,
    precision_dps: int,
    start: tuple[str, str],
) -> dict[str, Any] | None:
    """Map the reusable finite-root library to one strict v3 backend record."""

    if type(precision_dps) is not int or precision_dps not in (80, 120):
        raise ValueError("finite root precision must be 80 or 120 dps")
    if (
        type(start) is not tuple
        or len(start) != 2
        or any(type(value) is not str for value in start)
    ):
        raise TypeError("finite root start must contain two decimal strings")
    for index, value in enumerate(start):
        _finite_decimal(value, path=f"start[{index}]")
    parameters = _finite_interval_parameters(horizon)
    refined = refine_rotating_wave_root(
        radius=start[0],
        theta=start[1],
        parameters=parameters,
        precision_dps=precision_dps,
        iterations=8,
    )
    certificates = []
    for half_width in ("1e-8", "1e-30"):
        raw = certify_rotating_wave_box(
            radius=refined["radius"],
            theta=refined["theta"],
            radius_half_width=half_width,
            theta_half_width=half_width,
            parameters=parameters,
            precision_dps=precision_dps,
        )
        certificate = _v3_certificate(raw)
        if certificate is None:
            return None
        certificates.append(certificate)
    return {
        "newton": {
            "jacobian": refined["jacobian"],
            "precision_dps": precision_dps,
            "radius": refined["radius"],
            "residual": refined["balance"],
            "steps": 8,
            "theta": refined["theta"],
        },
        "outer_certificate": certificates[0],
        "inner_certificate": certificates[1],
    }


def homotopy_backend_record(
    *,
    from_horizon: int,
    to_horizon: int,
    from_root: tuple[str, str],
    to_root: tuple[str, str],
) -> dict[str, Any]:
    """Certify one registered edge through exactly 64 fixed slabs."""

    edge = next(
        (
            item
            for item in _HOMOTOPY_EDGES
            if item[0] == from_horizon and item[1] == to_horizon
        ),
        None,
    )
    if edge is None:
        raise ValueError("unregistered horizon homotopy edge")
    for name, root in (("from_root", from_root), ("to_root", to_root)):
        if (
            type(root) is not tuple
            or len(root) != 2
            or any(type(value) is not str for value in root)
        ):
            raise TypeError(f"{name} must contain two decimal strings")
        for index, value in enumerate(root):
            _finite_decimal(value, path=f"{name}[{index}]")

    first_parameters = _finite_interval_parameters(from_horizon)
    second_parameters = _finite_interval_parameters(to_horizon)
    slabs: list[dict[str, Any] | None] = [None] * 64
    previous_image: list[list[str]] | None = None
    complete = True
    with localcontext() as context:
        context.prec = 180
        first_center = tuple(Decimal(value) for value in from_root)
        second_center = tuple(Decimal(value) for value in to_root)
        for index in range(64):
            s_lower = Decimal(index) / Decimal(64)
            s_upper = Decimal(index + 1) / Decimal(64)
            s_midpoint = (s_lower + s_upper) / Decimal(2)
            center = tuple(
                first_center[coordinate]
                + s_midpoint
                * (second_center[coordinate] - first_center[coordinate])
                for coordinate in range(2)
            )
            try:
                raw = certify_rotating_wave_homotopy_box(
                    radius=format(center[0], "f"),
                    theta=format(center[1], "f"),
                    radius_half_width="1e-4",
                    theta_half_width="1e-6",
                    s_interval=(format(s_lower, "f"), format(s_upper, "f")),
                    first_parameters=first_parameters,
                    second_parameters=second_parameters,
                    precision_dps=120,
                )
            except ArithmeticError:
                complete = False
                break
            image = [_interval_pair(value) for value in raw["krawczyk_image"]]
            box = {
                "radius": _interval_pair(raw["box"][0]),
                "theta": _interval_pair(raw["box"][1]),
            }
            overlaps_previous = None
            if previous_image is not None:
                overlaps_previous = (
                    _image_intersection(
                        previous_image,
                        image,
                        path=f"homotopy[{from_horizon},{to_horizon},{index}]",
                    )
                    is not None
                )
            reported_strict = bool(
                raw.get("pass") is True
                and type(raw.get("gates")) is dict
                and raw["gates"].get("krawczyk_strict_interior") is True
            )
            strict = _strict_image_in_box(
                image,
                box,
                path=f"homotopy[{from_horizon},{to_horizon},{index}]",
            )
            if strict is not reported_strict:
                raise ValueError("homotopy certificate summary mismatch")
            slabs[index] = {
                "box": box,
                "index": index,
                "krawczyk_image": image,
                "overlaps_previous": overlaps_previous,
                "s_interval": [format(s_lower, "f"), format(s_upper, "f")],
                "strict_interior": strict,
            }
            if not strict or overlaps_previous is False:
                complete = False
                break
            previous_image = image
    return {
        "direction": edge[2],
        "from_horizon": from_horizon,
        "pass": complete,
        "slabs": slabs,
        "status": "pass" if complete else "inconclusive",
        "to_horizon": to_horizon,
    }


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
    translation_x = [inverse_root_h if index % 2 == 0 else 0.0 for index in range(dimension)]
    translation_y = [0.0 if index % 2 == 0 else inverse_root_h for index in range(dimension)]
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


def _decimal_interval(values: Sequence[str], *, path: str) -> tuple[Decimal, Decimal]:
    if len(values) != 2:
        raise ValueError(f"{path}: expected two endpoints")
    lower, upper = (Decimal(value) for value in values)
    if lower > upper:
        raise ValueError(f"{path}: reversed interval")
    return lower, upper


def _interval_intersection(
    first: Sequence[str],
    second: Sequence[str],
    *,
    path: str,
) -> list[str] | None:
    first_lower, first_upper = _decimal_interval(first, path=f"{path}.first")
    second_lower, second_upper = _decimal_interval(second, path=f"{path}.second")
    lower = max(first_lower, second_lower)
    upper = min(first_upper, second_upper)
    if lower > upper:
        return None
    return [format(lower, "f"), format(upper, "f")]


def _image_intersection(
    first: Sequence[Sequence[str]],
    second: Sequence[Sequence[str]],
    *,
    path: str,
) -> dict[str, list[str]] | None:
    radius = _interval_intersection(first[0], second[0], path=f"{path}.radius")
    theta = _interval_intersection(first[1], second[1], path=f"{path}.theta")
    if radius is None or theta is None:
        return None
    return {"radius": radius, "theta": theta}


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
        for name in ("radius", "theta"):
            lower, upper = _decimal_interval(
                certificate["box"][name], path=f"{path}.box.{name}"
            )
            if upper - lower != expected_width:
                raise ValueError(f"{path}.box.{name}: half-width mismatch")
            if center is not None and (lower + upper) / 2 != Decimal(
                center[0 if name == "radius" else 1]
            ):
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
        radius_agreement = abs(
            Decimal(panel["newton_80"]["radius"])
            - Decimal(panel["newton_120"]["radius"])
        ) <= Decimal("1e-50")
        theta_agreement = abs(
            Decimal(panel["newton_80"]["theta"])
            - Decimal(panel["newton_120"]["theta"])
        ) <= Decimal("1e-50")
    centers_agree = radius_agreement and theta_agreement
    if panel["centers_agree"] is not centers_agree:
        raise ValueError(f"{path}.centers_agree: reconstruction mismatch")
    certificates = {
        name: _verify_certificate(
            panel[name],
            center=(
                panel["newton_80"]["radius"],
                panel["newton_80"]["theta"],
            )
            if name.endswith("80")
            else (
                panel["newton_120"]["radius"],
                panel["newton_120"]["theta"],
            ),
            half_width="1e-8" if name.startswith("outer") else "1e-30",
            path=f"{path}.{name}",
        )
        for name in (
            "outer_certificate_80",
            "inner_certificate_80",
            "outer_certificate_120",
            "inner_certificate_120",
        )
    }
    intersection = _image_intersection(
        panel["inner_certificate_80"]["krawczyk_image"],
        panel["inner_certificate_120"]["krawczyk_image"],
        path=f"{path}.inner_intersection",
    )
    if panel["inner_intersection"] != intersection:
        raise ValueError(f"{path}.inner_intersection: reconstruction mismatch")
    return bool(centers_agree and intersection is not None and all(certificates.values()))


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
            slab_path = f"$.finite_branch.homotopies[{index}].slabs[{slab_index}]"
            expected_s = [
                format(Decimal(slab_index) / Decimal(64), "f"),
                format(Decimal(slab_index + 1) / Decimal(64), "f"),
            ]
            if slab["s_interval"] != expected_s:
                raise ValueError(f"{slab_path}.s_interval: reconstruction mismatch")
            for coordinate, half_width in (("radius", "1e-4"), ("theta", "1e-6")):
                lower, upper = _decimal_interval(
                    slab["box"][coordinate], path=f"{slab_path}.box.{coordinate}"
                )
                if upper - lower != 2 * Decimal(half_width):
                    raise ValueError(f"{slab_path}.box.{coordinate}: width mismatch")
                with localcontext() as context:
                    context.prec = 180
                    interpolation = Decimal(2 * slab_index + 1) / Decimal(128)
                    start = Decimal(root_panels[first_slot]["newton_120"][coordinate])
                    stop = Decimal(root_panels[second_slot]["newton_120"][coordinate])
                    expected_center = (1 - interpolation) * start + interpolation * stop
                    if (lower + upper) / 2 != expected_center:
                        raise ValueError(f"{slab_path}.box.{coordinate}: center mismatch")
            strict = _strict_image_in_box(
                slab["krawczyk_image"], slab["box"], path=slab_path
            )
            if slab["strict_interior"] is not strict:
                raise ValueError(f"{slab_path}.strict_interior: reconstruction mismatch")
            overlap = None
            if slab_index:
                overlap = _image_intersection(
                    homotopy["slabs"][slab_index - 1]["krawczyk_image"],
                    slab["krawczyk_image"],
                    path=f"{slab_path}.overlap",
                ) is not None
            if slab["overlaps_previous"] is not overlap:
                raise ValueError(f"{slab_path}.overlaps_previous: reconstruction mismatch")
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


def _box_key(box: dict[str, Any], *, path: str) -> tuple[Decimal, ...]:
    radius = _decimal_interval(box["radius"], path=f"{path}.radius")
    theta = _decimal_interval(box["theta"], path=f"{path}.theta")
    return radius[0], radius[1], theta[0], theta[1]


def _split_exclusion_box(box: tuple[Decimal, ...]) -> tuple[tuple[Decimal, ...], tuple[Decimal, ...]]:
    radius_lower, radius_upper, theta_lower, theta_upper = box
    radius_width = (radius_upper - radius_lower) / Decimal("0.3")
    theta_width = (theta_upper - theta_lower) / Decimal("0.012")
    if radius_width >= theta_width:
        midpoint = (radius_lower + radius_upper) / 2
        return (
            (radius_lower, midpoint, theta_lower, theta_upper),
            (midpoint, radius_upper, theta_lower, theta_upper),
        )
    midpoint = (theta_lower + theta_upper) / 2
    return (
        (radius_lower, radius_upper, theta_lower, midpoint),
        (radius_lower, radius_upper, midpoint, theta_upper),
    )


def _contained_box(child: tuple[Decimal, ...], parent: tuple[Decimal, ...]) -> bool:
    return bool(
        parent[0] <= child[0] <= child[1] <= parent[1]
        and parent[2] <= child[2] <= child[3] <= parent[3]
    )


def _verify_exclusion_partition(
    attempt: dict[str, Any],
    *,
    expected_domain: dict[str, list[str]],
    path: str,
) -> None:
    if attempt["local_domain"] != expected_domain:
        raise ValueError(f"{path}.local_domain: root-bound domain mismatch")
    domain = _box_key(attempt["local_domain"], path=f"{path}.local_domain")
    paths: list[str] = []
    for index, leaf in enumerate(attempt["leaves"]):
        leaf_path = f"{path}.leaves[{index}]"
        depth = leaf["depth"]
        if not 0 <= depth <= attempt["max_depth"]:
            raise ValueError(f"{leaf_path}.depth: outside registered range")
        leaf_box = _box_key(leaf["box"], path=f"{leaf_path}.box")
        current = domain
        bits = []
        for _ in range(depth):
            lower, upper = _split_exclusion_box(current)
            in_lower = _contained_box(leaf_box, lower)
            in_upper = _contained_box(leaf_box, upper)
            if in_lower == in_upper:
                raise ValueError(f"{leaf_path}.box: not a deterministic partition leaf")
            if in_lower:
                bits.append("0")
                current = lower
            else:
                bits.append("1")
                current = upper
        if leaf_box != current:
            raise ValueError(f"{leaf_path}.box: not a deterministic partition leaf")
        paths.append("".join(bits))
    ordered = sorted(paths)
    if len(set(ordered)) != len(ordered) or any(
        second.startswith(first) for first, second in zip(ordered, ordered[1:])
    ):
        raise ValueError(f"{path}.leaves: partition paths overlap")
    maximum_depth = max((len(bits) for bits in paths), default=0)
    covered = sum(1 << (maximum_depth - len(bits)) for bits in paths)
    if covered != 1 << maximum_depth:
        raise ValueError(f"{path}.leaves: partition does not cover local domain")


def _verify_exclusions(
    exclusions: list[dict[str, Any] | None],
    *,
    local_branch_excluded: bool,
    root_panels: Sequence[dict[str, Any] | None],
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
        previous_panel = next(
            (
                panel
                for panel in root_panels
                if panel is not None and panel["horizon"] == edge[0]
            ),
            None,
        )
        if previous_panel is None:
            raise ValueError(
                f"$.finite_branch.exclusions[{index}]: missing previous root"
            )
        radius, theta = (
            Decimal(value) for value in _root_coordinates(previous_panel, 120)
        )
        expected_domain = {
            "radius": [
                format(max(Decimal("0.8"), radius - Decimal("0.02")), "f"),
                format(min(Decimal("1.1"), radius + Decimal("0.02")), "f"),
            ],
            "theta": [
                format(max(Decimal("0.01"), theta - Decimal("0.002")), "f"),
                format(min(Decimal("0.022"), theta + Decimal("0.002")), "f"),
            ],
        }
        _verify_exclusion_partition(
            attempt,
            expected_domain=expected_domain,
            path=f"$.finite_branch.exclusions[{index}]",
        )
        leaves = attempt["leaves"]
        status = attempt["status"]
        classifications = [leaf["classification"] for leaf in leaves]
        for leaf_index, leaf in enumerate(leaves):
            leaf_path = f"$.finite_branch.exclusions[{index}].leaves[{leaf_index}]"
            classification = leaf["classification"]
            residual = leaf["residual_box"]
            image = leaf["krawczyk_image"]
            strict_field = leaf["strict_interior"]
            if classification == "residual-excluded":
                if image is not None or strict_field is not None or residual is None:
                    raise ValueError(f"{leaf_path}: residual witness mismatch")
                excludes_zero = any(
                    not (lower <= 0 <= upper)
                    for lower, upper in (
                        _decimal_interval(component, path=f"{leaf_path}.residual_box")
                        for component in residual
                    )
                )
                if not excludes_zero:
                    raise ValueError(f"{leaf_path}: residual does not exclude zero")
            elif classification == "krawczyk-root":
                if residual is not None or image is None or strict_field is None:
                    raise ValueError(f"{leaf_path}: Krawczyk witness mismatch")
                strict = _strict_image_in_box(image, leaf["box"], path=leaf_path)
                if strict_field is not strict or not strict:
                    raise ValueError(f"{leaf_path}: false Krawczyk inclusion")
            elif any(value is not None for value in (residual, image, strict_field)):
                raise ValueError(f"{leaf_path}: unresolved leaf carries a claim witness")
        if status == "all-residual-excluded":
            if any(value != "residual-excluded" for value in classifications):
                raise ValueError(
                    f"$.finite_branch.exclusions[{index}]: false exclusion"
                )
            target_panel = next(
                (
                    panel
                    for panel in root_panels
                    if panel is not None and panel["horizon"] == edge[1]
                ),
                None,
            )
            if target_panel is not None and _verify_root_panel(
                target_panel,
                path=f"$.finite_branch.exclusions[{index}].target_root",
            ):
                target_radius, target_theta = (
                    Decimal(value) for value in _root_coordinates(target_panel, 120)
                )
                domain_key = _box_key(
                    attempt["local_domain"],
                    path=f"$.finite_branch.exclusions[{index}].local_domain",
                )
                if (
                    domain_key[0] <= target_radius <= domain_key[1]
                    and domain_key[2] <= target_theta <= domain_key[3]
                ):
                    raise ValueError(
                        f"$.finite_branch.exclusions[{index}]: certified target root "
                        "inside excluded domain"
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
    expected_configuration = {
        24: (96, 20000, 1e-10),
        36: (144, 40000, 1e-12),
    }[expected_count]
    if (
        panel["ncv"],
        panel["max_iterations"],
        panel["tolerance"],
    ) != expected_configuration:
        raise ValueError(f"{path}: registered solver configuration mismatch")
    if panel["status"] == "complete" and (count != expected_count or missing_vector):
        raise ValueError(f"{path}: complete status with incomplete slots")
    if panel["status"] == "missing-vectors" and not missing_vector:
        raise ValueError(f"{path}: missing-vectors status without missing vector")
    if panel["status"] == "wrong-cardinality" and count == expected_count:
        raise ValueError(f"{path}: wrong-cardinality status with full count")
    previous_modulus = math.inf
    for index, pair in enumerate(pairs[:count]):
        value = complex(*pair["eigenvalue"])
        modulus = abs(value)
        if pair["modulus"] != modulus:
            raise ValueError(f"{path}.eigenpairs[{index}].modulus: mismatch")
        expected_classification = (
            "translation"
            if pair["translation_overlap"] >= 0.99
            else "rotation"
            if pair["rotation_overlap"] >= 0.99
            else "transverse"
        )
        if pair["classification"] != expected_classification:
            raise ValueError(f"{path}.eigenpairs[{index}].classification: mismatch")
        if modulus > previous_modulus:
            raise ValueError(f"{path}.eigenpairs: not sorted by modulus")
        previous_modulus = modulus


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
        leading = primary[0]
        leading_value = complex(*leading["eigenvalue"])
        distance = min(
            abs(leading_value - complex(*pair["eigenvalue"])) for pair in convergence
        )
    agreement = payload["stability"]["arnoldi"]["panel_agreement"]
    expected_pass = bool(
        complete and symmetry_pass and distance is not None and distance <= 1e-5
    )
    if agreement["symmetry_pass"] is not symmetry_pass:
        raise ValueError("$.stability.arnoldi.panel_agreement.symmetry_pass: mismatch")
    if agreement["leading_transverse_distance"] != distance:
        raise ValueError("$.stability.arnoldi.panel_agreement.leading_transverse_distance: mismatch")
    if agreement["pass"] is not expected_pass:
        raise ValueError("$.stability.arnoldi.panel_agreement.pass: mismatch")


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
    names = ("radial", "tangential", "full-history-transverse")
    for index, (name, arm) in enumerate(
        zip(names, stability["continuation_arms"], strict=True)
    ):
        if arm is None:
            continue
        path = f"$.stability.continuation_arms[{index}]"
        expected = perturbations[name]
        if arm["name"] != name or arm["amplitude"] != amplitude:
            raise ValueError(f"{path}: registered perturbation mismatch")
        if arm["perturbation"] != expected:
            raise ValueError(f"{path}.perturbation: reconstruction mismatch")
        digest = _vector_sha256(expected)
        if arm["perturbation_sha256"] != digest:
            raise ValueError(f"{path}.perturbation_sha256: reconstruction mismatch")


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
    distances = [sample["distance"] for sample in samples[:count]]
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
    root_evidence = [
        None
        if panel is None
        else _verify_root_panel(
            panel, path=f"$.finite_branch.root_panels[{index}]"
        )
        for index, panel in enumerate(root_panels)
    ]
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
        if panel is not None and panel["inner_intersection"] is not None
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
        root_panels=root_panels,
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
    _verify_stability_inputs(payload)
    _verify_arnoldi_summary(payload)
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
        return root_evidence[index] is True

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
    _nonnull_prefix_length(tail_panels, path="$.infinite_tail.certificate_panels")
    tail_certificates = []
    for index, row in enumerate(tail_panels):
        if row is None:
            tail_certificates.append(False)
            continue
        expected_precision = (120, 160)[index]
        if row["precision_dps"] != expected_precision:
            raise ValueError(
                f"$.infinite_tail.certificate_panels[{index}]: precision mismatch"
            )
        tail_certificates.append(
            _verify_certificate(
                row["certificate"],
                center=row["root"],
                half_width="1e-10",
                path=f"$.infinite_tail.certificate_panels[{index}].certificate",
            )
        )
    tail_complete = False
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
        tail_complete = bool(overlap and all(tail_certificates))
    else:
        comparison = payload["infinite_tail"]["panel_comparison"]
        if comparison != {"intersection": None, "overlap": False}:
            raise ValueError("$.infinite_tail.panel_comparison: value without panels")
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


def _root_coordinates(panel: dict[str, Any], precision_dps: int) -> tuple[str, str]:
    newton = panel[f"newton_{precision_dps}"]
    return newton["radius"], newton["theta"]


def _combine_root_panel(
    horizon: int,
    precision_records: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    panel: dict[str, Any] = {"horizon": horizon}
    for precision in (80, 120):
        record = precision_records[precision]
        panel[f"newton_{precision}"] = copy.deepcopy(record["newton"])
        panel[f"outer_certificate_{precision}"] = copy.deepcopy(
            record["outer_certificate"]
        )
        panel[f"inner_certificate_{precision}"] = copy.deepcopy(
            record["inner_certificate"]
        )
    centers = [_root_coordinates(panel, precision) for precision in (80, 120)]
    panel["centers_agree"] = all(
        abs(Decimal(centers[0][index]) - Decimal(centers[1][index])) <= Decimal("1e-50")
        for index in range(2)
    )
    panel["inner_intersection"] = _image_intersection(
        panel["inner_certificate_80"]["krawczyk_image"],
        panel["inner_certificate_120"]["krawczyk_image"],
        path=f"orchestration.root[{horizon}].inner_intersection",
    )
    return panel


def _drift_record(root_panels: Sequence[dict[str, Any] | None]) -> dict[str, Any]:
    by_horizon = {
        panel["horizon"]: panel
        for panel in root_panels
        if panel is not None and panel["inner_intersection"] is not None
    }
    rows: list[dict[str, Any] | None] = []
    for first, second in ((1800, 2400), (2400, 3600)):
        if first not in by_horizon or second not in by_horizon:
            rows.append(None)
            continue
        radius_component, theta_component = _interval_drift_components(
            by_horizon[first]["inner_intersection"],
            by_horizon[second]["inner_intersection"],
            radius_scale=0.946517504804225,
            theta_scale=0.015770381717135,
        )
        rows.append(
            {
                "from_horizon": first,
                "to_horizon": second,
                "radius_component": radius_component,
                "theta_component": theta_component,
                "upper_bound": max(radius_component, theta_component),
            }
        )
    passed = bool(
        all(row is not None for row in rows)
        and drift_gates(
            previous_upper=rows[0]["upper_bound"],
            final_upper=rows[1]["upper_bound"],
        )["pass"]
    )
    return {
        "center_diagnostics": copy.deepcopy(rows),
        "interval_upper_bounds": rows,
        "mutation_closes_pass": True,
        "pass": passed,
    }


def _empty_arnoldi_panel(name: str) -> dict[str, Any]:
    configuration = {
        "primary": (24, 96, 1e-10, 20000),
        "convergence": (36, 144, 1e-12, 40000),
    }
    count, ncv, tolerance, iterations = configuration[name]
    return {
        "eigenpairs": [None] * count,
        "expected_count": count,
        "requested_count": count,
        "ncv": ncv,
        "tolerance": tolerance,
        "max_iterations": iterations,
        "start_sha256": _arnoldi_start_hashes()[name],
        "status": "arpack-no-convergence",
    }


def _arnoldi_agreement(
    primary: dict[str, Any],
    convergence: dict[str, Any],
    *,
    theta: float,
) -> dict[str, Any]:
    panels = (primary, convergence)
    complete = all(panel["status"] == "complete" for panel in panels)
    expected_translations = (
        complex(math.cos(theta), math.sin(theta)),
        complex(math.cos(theta), -math.sin(theta)),
    )
    symmetry_pass = complete
    for panel in panels:
        pairs = [pair for pair in panel["eigenpairs"] if pair is not None]
        translations = [
            pair for pair in pairs if pair["classification"] == "translation"
        ]
        rotations = [pair for pair in pairs if pair["classification"] == "rotation"]
        symmetry_pass = bool(
            symmetry_pass
            and len(translations) >= 2
            and all(
                min(
                    abs(complex(*pair["eigenvalue"]) - expected)
                    for pair in translations
                )
                <= 1e-7
                for expected in expected_translations
            )
            and any(
                abs(complex(*pair["eigenvalue"]) - 1.0) <= 1e-7
                for pair in rotations
            )
        )
    transverse = [
        [
            pair
            for pair in panel["eigenpairs"]
            if pair is not None and pair["classification"] == "transverse"
        ]
        for panel in panels
    ]
    distance = None
    if transverse[0] and transverse[1]:
        leading = complex(*transverse[0][0]["eigenvalue"])
        distance = min(
            abs(leading - complex(*pair["eigenvalue"])) for pair in transverse[1]
        )
    return {
        "leading_transverse_distance": distance,
        "pass": bool(
            complete and symmetry_pass and distance is not None and distance <= 1e-5
        ),
        "symmetry_pass": symmetry_pass,
    }


def _gate_state(condition: bool, *, complete: bool) -> str:
    if not complete:
        return "inconclusive"
    return "pass" if condition else "fail"


def orchestrate_horizon_transfer(
    *,
    backend: Any,
    identity: dict[str, Any],
    publication: dict[str, Any],
) -> dict[str, Any]:
    """Assemble one target-free run from injected primitive stage backends.

    This function performs no publication and owns no scientific numerical
    implementation.  Missing primitive evidence closes dependent stages.
    """

    contract = _load_result_schema()
    payload = _witness_value(contract["root"], contract, fill_nullable=False)
    payload["identity"] = copy.deepcopy(identity)
    payload["publication"] = copy.deepcopy(publication)

    direct_replay_pass = bool(backend.direct_replay())
    root_panels: list[dict[str, Any] | None] = [None] * len(HORIZONS)
    index_by_horizon = {horizon: index for index, horizon in enumerate(HORIZONS)}
    panel_starts = {
        precision: (
            str(identity["parameters"]["anchor_radius"]),
            str(identity["parameters"]["anchor_theta"]),
        )
        for precision in (80, 120)
    }
    forward_open = True
    lower_open = True
    exclusions: list[dict[str, Any] | None] = [None] * 4
    for horizon in _ROOT_EXECUTION_ORDER:
        is_forward = horizon in (1200, 1500, 1800, 2400, 3600)
        if horizon != 1200 and ((is_forward and not forward_open) or (not is_forward and not lower_open)):
            continue
        if horizon == 900:
            anchor = root_panels[index_by_horizon[1200]]
            if anchor is None:
                lower_open = False
                continue
            panel_starts = {
                precision: _root_coordinates(anchor, precision)
                for precision in (80, 120)
            }
        records: dict[int, dict[str, Any]] = {}
        for precision in (80, 120):
            record = backend.finite_root_panel(
                horizon=horizon,
                precision_dps=precision,
                start=panel_starts[precision],
            )
            if record is None:
                break
            records[precision] = record
        if len(records) != 2:
            if is_forward and horizon != 1200:
                previous = _ROOT_EXECUTION_ORDER[_ROOT_EXECUTION_ORDER.index(horizon) - 1]
                exclusions[(1500, 1800, 2400, 3600).index(horizon)] = (
                    backend.local_branch_exclusion(
                        from_horizon=previous,
                        to_horizon=horizon,
                        previous_root=panel_starts[120],
                    )
                )
                forward_open = False
            elif horizon == 1200:
                forward_open = False
                lower_open = False
            else:
                lower_open = False
            continue
        panel = _combine_root_panel(horizon, records)
        root_panels[index_by_horizon[horizon]] = panel
        panel_starts = {
            precision: _root_coordinates(panel, precision)
            for precision in (80, 120)
        }

    homotopies: list[dict[str, Any] | None] = [None] * 6
    forward_homotopy_open = True
    lower_homotopy_open = True
    for edge_index, (first, second, direction) in enumerate(_HOMOTOPY_EDGES):
        if direction == "forward" and not forward_homotopy_open:
            continue
        if direction == "lower-tail" and not lower_homotopy_open:
            continue
        first_panel = root_panels[index_by_horizon[first]]
        second_panel = root_panels[index_by_horizon[second]]
        if first_panel is None or second_panel is None:
            if direction == "forward":
                forward_homotopy_open = False
            else:
                lower_homotopy_open = False
            continue
        row = backend.homotopy_edge(
            from_horizon=first,
            to_horizon=second,
            from_root=_root_coordinates(first_panel, 120),
            to_root=_root_coordinates(second_panel, 120),
        )
        homotopies[edge_index] = copy.deepcopy(row)
        if row["status"] != "pass":
            if direction == "forward":
                if exclusions[edge_index] is None:
                    exclusions[edge_index] = backend.local_branch_exclusion(
                        from_horizon=first,
                        to_horizon=second,
                        previous_root=_root_coordinates(first_panel, 120),
                    )
                forward_homotopy_open = False
            else:
                lower_homotopy_open = False

    drift = _drift_record(root_panels)
    payload["finite_branch"] = {
        "direct_replay_pass": direct_replay_pass,
        "drift": drift,
        "exclusions": exclusions,
        "forward_horizons": [1200, 1500, 1800, 2400, 3600],
        "homotopies": homotopies,
        "horizons": list(HORIZONS),
        "lower_horizons": [900, 600],
        "lower_tail_status": "lower-tail-stress-inconclusive",
        "root_panels": root_panels,
    }

    q_rows = q_representations(HORIZONS)
    bound_rows = [
        {"horizon": horizon, **tail_bounds(horizon=horizon, precision_dps=80)}
        for horizon in HORIZONS
    ]
    tail_panels: list[dict[str, Any] | None] = [None, None]
    tail_comparison: dict[str, Any] = {"intersection": None, "overlap": False}
    horizon_3600 = root_panels[index_by_horizon[3600]]
    if horizon_3600 is not None:
        tail_root = _root_coordinates(horizon_3600, 120)
        for index, precision in enumerate((120, 160)):
            panel = backend.tail_certificate_panel(
                precision_dps=precision,
                root=tail_root,
            )
            if panel is None:
                break
            tail_panels[index] = copy.deepcopy(panel)
        if all(panel is not None for panel in tail_panels):
            intersection = _image_intersection(
                tail_panels[0]["certificate"]["krawczyk_image"],
                tail_panels[1]["certificate"]["krawczyk_image"],
                path="orchestration.infinite_tail.panel_comparison",
            )
            tail_comparison = {
                "intersection": intersection,
                "overlap": intersection is not None,
            }
    phi0 = Decimal("1") + Decimal("3.5") / Decimal("9")
    with localcontext() as context:
        context.prec = 80
        phi1 = (-Decimal("0.5")).exp() * (
            Decimal("1") + Decimal("3.5") / Decimal("27")
        )
    payload["infinite_tail"] = {
        "bounds": bound_rows,
        "certificate_panels": tail_panels,
        "constants": {
            "phi0_bound": format(phi0, "f"),
            "phi1_bound": format(phi1, "f"),
            "radius_maximum": "1.1",
        },
        "panel_comparison": tail_comparison,
        "q_representations": q_rows,
    }

    empty_panels = {
        name: _empty_arnoldi_panel(name) for name in ("primary", "convergence")
    }
    stability: dict[str, Any] = {
        "arnoldi": {
            **empty_panels,
            "panel_agreement": {
                "leading_transverse_distance": None,
                "pass": False,
                "symmetry_pass": False,
            },
        },
        "continuation_arms": [None, None, None],
        "exact_arm": None,
        "gates": {},
        "horizon": 2400,
        "rounded_root": None,
    }
    horizon_2400 = root_panels[index_by_horizon[2400]]
    if horizon_2400 is not None:
        root_2400 = _root_coordinates(horizon_2400, 120)
        rounded_root = (float(root_2400[0]), float(root_2400[1]))
        stability["rounded_root"] = list(rounded_root)
        starts = _arnoldi_start_vectors()
        panels = {
            name: copy.deepcopy(
                backend.arnoldi_panel(
                    name=name,
                    rounded_root=rounded_root,
                    start=starts[name],
                )
            )
            for name in ("primary", "convergence")
        }
        stability["arnoldi"].update(panels)
        stability["arnoldi"]["panel_agreement"] = _arnoldi_agreement(
            panels["primary"], panels["convergence"], theta=rounded_root[1]
        )
        if all(panel["status"] == "complete" for panel in panels.values()):
            _, perturbations = _registered_perturbation_vectors(
                radius=rounded_root[0], theta=rounded_root[1], horizon=2400
            )
            stability["continuation_arms"] = [
                copy.deepcopy(
                    backend.continuation_arm(
                        name=name,
                        rounded_root=rounded_root,
                        perturbation=perturbations[name],
                    )
                )
                for name in ("radial", "tangential", "full-history-transverse")
            ]
            stability["exact_arm"] = copy.deepcopy(
                backend.exact_arm(rounded_root=rounded_root)
            )
    payload["stability"] = stability
    stability["gates"] = _stability_evidence(payload)

    payload["controls"] = copy.deepcopy(backend.controls())
    controls_pass = _controls_evidence(payload)
    payload["controls"]["pass"] = controls_pass
    root_complete = [panel is not None and _verify_root_panel(panel, path="orchestration.root") for panel in root_panels]
    forward_roots = all(root_complete[index] for index in range(2, 7))
    lower_roots = all(root_complete[index] for index in (2, 1, 0))
    forward_homotopies = all(
        row is not None and row["status"] == "pass" for row in homotopies[:4]
    )
    lower_homotopies = all(
        row is not None and row["status"] == "pass" for row in homotopies[4:]
    )
    lower_tail_status = (
        "lower-tail-stress-pass"
        if lower_roots and lower_homotopies
        else "lower-tail-stress-inconclusive"
    )
    payload["finite_branch"]["lower_tail_status"] = lower_tail_status
    tail_complete = bool(
        all(panel is not None for panel in tail_panels) and tail_comparison["overlap"]
    )
    stable_complete = all(
        stability["gates"][name]
        for name in (
            "continuations_complete",
            "exact_arm",
            "panels_complete",
            "panel_agreement",
            "perturbation_contraction",
            "ritz_residuals",
            "symmetries",
        )
    )
    local_branch_excluded = any(
        row is not None and row["status"] == "all-residual-excluded"
        for row in exclusions
    )
    gates = {
        "G0": "pass" if direct_replay_pass and all(row["two_ulp_gate"] and row["nonzero_finite"] for row in q_rows) else "fail",
        "G1F": "pass" if forward_roots else "inconclusive",
        "G1R": "pass" if lower_roots else "inconclusive",
        "G2F": "pass" if forward_homotopies else "inconclusive",
        "G2R": "pass" if lower_homotopies else "inconclusive",
        "G3": _gate_state(drift["pass"], complete=all(row is not None for row in drift["interval_upper_bounds"])),
        "G4": "pass" if tail_complete else "inconclusive",
        "G5": "pass" if stable_complete else "inconclusive",
        "G6": "pass" if controls_pass else "fail",
        "local_branch_excluded": local_branch_excluded,
        "large_h_instability_supported": stability["gates"]["instability_supported"],
    }
    classification = classify_horizon(gates, lower_tail_status=lower_tail_status)
    payload["classification"] = {
        **classification,
        "claim_boundary": contract["constants"]["claim_boundary"],
        "finite_large_h_stability_only": bool(gates["G5"] == "pass" and gates["G4"] != "pass"),
        "gates": gates,
    }
    validate_result(payload)
    return payload


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
        "schema": "scalar-memory-rotating-wave-horizon-publication-v3",
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
