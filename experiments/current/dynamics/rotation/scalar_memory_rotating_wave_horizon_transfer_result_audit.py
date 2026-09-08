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


def _verify_root_and_homotopy_slots(payload: dict[str, Any]) -> None:
    roots = payload["finite_branch"]["root_panels"]
    for index, panel in enumerate(roots):
        if panel is not None and panel["horizon"] != HORIZONS[index]:
            raise ValueError("$.finite_branch.root_panels: horizon order mismatch")
    for previous, current in ((2, 3), (3, 4), (4, 5), (5, 6), (2, 1), (1, 0)):
        if roots[current] is not None and roots[previous] is None:
            raise ValueError("$.finite_branch.root_panels: dependency gap")

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
            passing = passing and slab["strict_interior"] and (
                slab_index == 0 or slab["overlaps_previous"] is True
            )
        if homotopy["status"] == "pass" and not (
            passing and homotopy["pass"]
        ):
            raise ValueError(f"$.finite_branch.homotopies[{index}]: false pass")


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
        if panel["status"] == "complete" and (count != expected or missing_vector):
            raise ValueError(
                f"$.stability.arnoldi.{name}: false complete status"
            )
        if panel["status"] == "missing-vectors" and not missing_vector:
            raise ValueError(
                f"$.stability.arnoldi.{name}: missing vector not represented"
            )

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

    _verify_root_and_homotopy_slots(payload)
    _verify_partial_panels_and_trajectories(payload)
    root_panels = payload["finite_branch"]["root_panels"]
    panels = {
        panel["horizon"]: panel["inner_intersection"]
        for panel in root_panels
        if panel is not None
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
    for index, attempt in enumerate(payload["finite_branch"]["exclusions"]):
        if attempt is None:
            continue
        classifications = [row["classification"] for row in attempt["leaves"]]
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
        panel = root_panels[index]
        return bool(
            panel is not None
            and panel["centers_agree"]
            and panel["certificate_80"]["strict_interior"]
            and panel["certificate_120"]["strict_interior"]
        )

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
        "G4": bool(
            all(
                row is not None and row["certificate"]["strict_interior"]
                for row in tail_panels
            )
            and payload["infinite_tail"]["panel_comparison"]["overlap"]
        ),
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
    if manifest["schema"] != "scalar-memory-rotating-wave-horizon-publication-v2":
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
