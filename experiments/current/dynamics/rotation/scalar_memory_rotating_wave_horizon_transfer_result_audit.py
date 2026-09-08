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
    result["infinite_tail"]["q_representations"] = q_representations(
        HORIZONS,
        alpha=PARAMETERS["alpha"],
    )
    result["infinite_tail"]["bounds"] = [
        {"horizon": horizon, **tail_bounds(horizon=horizon, parameters=PARAMETERS)}
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

    root_panels = payload["finite_branch"]["root_panels"]
    if [panel["horizon"] for panel in root_panels] != list(HORIZONS):
        raise ValueError("$.finite_branch.root_panels: horizon order mismatch")
    panels = {
        panel["horizon"]: panel["inner_intersection"]
        for panel in root_panels
    }
    expected_pairs = ((1800, 2400), (2400, 3600))
    observed_drift = payload["finite_branch"]["drift"]["interval_upper_bounds"]
    for index, (first_horizon, second_horizon) in enumerate(expected_pairs):
        radius_component, theta_component = _interval_drift_components(
            panels[first_horizon],
            panels[second_horizon],
            radius_scale=0.946517504804225,
            theta_scale=0.015770381717135,
        )
        row = observed_drift[index]
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

    drift_pass = (
        observed_drift[1]["upper_bound"] <= 1e-8
        and observed_drift[1]["upper_bound"]
        <= 0.01 * observed_drift[0]["upper_bound"] + 1e-14
    )
    if payload["finite_branch"]["drift"]["pass"] is not drift_pass:
        raise ValueError("$.finite_branch.drift.pass: reconstruction mismatch")

    observed_classification = payload["classification"]
    expected_classification = classify_horizon(
        observed_classification["gates"],
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
    if manifest["schema"] != "scalar-memory-rotating-wave-horizon-publication-v1":
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
