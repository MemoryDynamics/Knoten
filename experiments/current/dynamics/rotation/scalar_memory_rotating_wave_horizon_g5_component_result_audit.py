"""Standard-library audit for an isolated G5 component result.

This module deliberately imports neither the numerical runner nor NumPy,
SciPy, mpmath, or a sparse eigensolver.  It reconstructs record hashes,
registered inputs, panel matching, trajectory summaries, thresholds, and the
final decision.  It cannot independently recompute ``J v - lambda v``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path
import struct
from typing import Any, Sequence

from emergenz_knoten.strict_json_contract import validate_payload as validate_contract


ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_g5_component_result_schema_v1.json"
)
SCHEMA = "scalar-memory-rotating-wave-horizon-g5-component-v1"
EQUATION_ID = "deterministic-native-k0h-full-fifo-v1"
START = ("0.946517504804225", "0.015770381717135")
PARAMETERS = {
    "alpha": 0.01,
    "amplitude_att": 3.5,
    "amplitude_rep": 1.0,
    "epsilon": 0.0,
    "eta": 0.15,
    "horizon": 2400,
    "memory_mass": 1.0,
    "q": 0.99,
    "sigma_att": 3.0,
    "sigma_rep": 1.0,
}
CLAIM_BOUNDARY = (
    "local direct H=2400 FIFO dynamics only; no H-infinity, formation, "
    "interaction, inertia, or mass claim"
)
ARM_NAMES = ("radial", "tangential", "full-history-transverse")
PANEL_CONFIGURATIONS = {
    "primary": (24, 96, 1e-10, 20000, 0x243F6A88),
    "convergence": (36, 144, 1e-12, 40000, 0x85A308D3),
}
RESULT_NAME = "scalar_memory_rotating_wave_horizon_g5_component_2026-09-14.json"
REPORT_NAME = RESULT_NAME.removesuffix(".json") + ".md"
MANIFEST_NAME = RESULT_NAME.removesuffix(".json") + ".publication.json"


def _contract() -> dict[str, Any]:
    contract = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if contract.get("schema") != (
        "scalar-memory-rotating-wave-horizon-g5-result-contract-v1"
    ):
        raise ValueError("audit: result-contract identity mismatch")
    return contract


def _canonical_sha256(value: Any) -> str:
    content = json.dumps(
        value, allow_nan=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def _vector_sha256(values: Sequence[float]) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(struct.pack("<d", float(value)))
    return digest.hexdigest()


def _start_hash(seed: int) -> str:
    component = float.fromhex("0x1.d8f7208e6b82cp-7")
    state = seed
    values = []
    for _ in range(4800):
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        values.append(component if state & 0x80000000 else -component)
    return _vector_sha256(values)


def _nonnull_prefix(values: Sequence[Any], *, path: str) -> int:
    count = 0
    saw_null = False
    for value in values:
        if value is None:
            saw_null = True
        elif saw_null:
            raise ValueError(f"{path}: non-null entries do not form a prefix")
        else:
            count += 1
    return count


def _registered_perturbations(
    *, radius: float, theta: float
) -> tuple[float, dict[str, list[float]]]:
    horizon = 2400
    dimension = 2 * horizon
    amplitude = 1e-7 * radius
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
        projection = math.fsum(
            value * direction
            for value, direction in zip(rotation, basis, strict=True)
        )
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
        projection = math.fsum(
            value * direction
            for value, direction in zip(full, basis, strict=True)
        )
        full = [
            value - projection * direction
            for value, direction in zip(full, basis, strict=True)
        ]
    full_norm = math.sqrt(math.fsum(value * value for value in full))
    return amplitude, {
        "radial": radial,
        "tangential": tangential,
        "full-history-transverse": [
            amplitude * value / full_norm for value in full
        ],
    }


def _verify_finite_root(finite: dict[str, Any]) -> tuple[float, float]:
    newton = finite["newton"]
    if (newton["precision_dps"], newton["steps"]) != (120, 8):
        raise ValueError("$.finite_root.newton: configuration mismatch")
    root = (newton["radius"], newton["theta"])
    for name, width in (
        ("outer_certificate", Decimal("1e-8")),
        ("inner_certificate", Decimal("1e-30")),
    ):
        certificate = finite[name]
        if (
            certificate["interval_backend"] != "mpmath.iv"
            or certificate["strict_interior"] is not True
        ):
            raise ValueError(f"$.finite_root.{name}: backend/inclusion mismatch")
        with localcontext() as context:
            context.prec = 180
            for index, coordinate in enumerate(("radius", "theta")):
                lower, upper = map(Decimal, certificate["box"][coordinate])
                center = Decimal(root[index])
                if not lower <= center - width < center + width <= upper:
                    raise ValueError(f"$.finite_root.{name}: root/box mismatch")
                image_lower, image_upper = map(
                    Decimal, certificate["krawczyk_image"][index]
                )
                if not lower < image_lower <= image_upper < upper:
                    raise ValueError(f"$.finite_root.{name}: false strict inclusion")
    return float(root[0]), float(root[1])


def _verify_preflight(
    preflight: dict[str, Any], *, rounded_root: tuple[float, float]
) -> bool:
    record = preflight["record"]
    if preflight["record_sha256"] != _canonical_sha256(record):
        raise ValueError("$.preflight.record_sha256: mismatch")
    if (
        record["candidate"]["horizon"],
        record["candidate"]["radius"],
        record["candidate"]["theta"],
    ) != (2400, *rounded_root):
        raise ValueError("$.preflight.record.candidate: root binding mismatch")
    expected_equation = {
        "alpha": 0.01,
        "amplitude_att": 3.5,
        "amplitude_rep": 1.0,
        "deposition_weight": 0.01,
        "equation_id": EQUATION_ID,
        "eta": 0.15,
        "memory_mass": 1.0,
        "noise_amplitude": 0.0,
        "q": 0.99,
        "sigma_att": 3.0,
        "sigma_rep": 1.0,
    }
    if record["equation"] != expected_equation:
        raise ValueError("$.preflight.record.equation: mismatch")
    if record["thresholds"] != {
        "fixed_point_maximum": 1e-14,
        "symmetry_residual_maximum": 1e-10,
    }:
        raise ValueError("$.preflight.record.thresholds: mismatch")
    if record["jacobian"]["shape"] != [4800, 4800] or (
        record["jacobian"]["dimension"], record["jacobian"]["nnz"]
    ) != (4800, 19196):
        raise ValueError("$.preflight.record.jacobian: structure mismatch")
    memory = record["memory"]
    closed = 1.0 - 0.99**2400
    if memory["closed_form_retained_weight"] != closed:
        raise ValueError("$.preflight.record.memory: closed form mismatch")
    if memory["identity_absolute_error"] != abs(
        memory["direct_retained_weight"] - memory["closed_form_retained_weight"]
    ):
        raise ValueError("$.preflight.record.memory: error mismatch")
    symmetry = record["symmetry"]
    expected_symmetry = all(
        symmetry[name] <= 1e-10
        for name in (
            "rotation_relative_residual",
            "translation_x_relative_residual",
            "translation_y_relative_residual",
        )
    )
    if symmetry["pass"] is not expected_symmetry:
        raise ValueError("$.preflight.record.symmetry.pass: mismatch")
    gates = record["gates"]
    expected_gates = {
        "finite": True,
        "fixed_point": (
            record["orbit"]["co_rotating_fixed_point_max_abs_error"] <= 1e-14
        ),
        "jacobian_structure": True,
        "native_circle_covariance": (
            record["orbit"]["native_circle_covariance_max_abs_error"] <= 1e-14
        ),
        "symmetries": expected_symmetry,
        "weight_identity": (
            memory["identity_absolute_error"]
            <= 8.0 * math.ulp(max(1.0, abs(closed)))
        ),
    }
    expected_gates["pass"] = all(expected_gates.values())
    if gates != expected_gates:
        raise ValueError("$.preflight.record.gates: reconstruction mismatch")
    return gates["pass"]


def _panel_agreement(
    primary: dict[str, Any], convergence: dict[str, Any], *, theta: float
) -> dict[str, Any]:
    panels = (primary, convergence)
    complete = all(panel["status"] == "complete" for panel in panels)
    targets = (
        complex(math.cos(theta), math.sin(theta)),
        complex(math.cos(theta), -math.sin(theta)),
    )
    symmetry = complete
    transverse = []
    for panel in panels:
        pairs = [pair for pair in panel["eigenpairs"] if pair is not None]
        translations = [
            pair for pair in pairs if pair["classification"] == "translation"
        ]
        rotations = [
            pair for pair in pairs if pair["classification"] == "rotation"
        ]
        symmetry = bool(
            symmetry
            and len(translations) >= 2
            and all(
                min(
                    abs(complex(*pair["eigenvalue"]) - target)
                    for pair in translations
                )
                <= 1e-7
                for target in targets
            )
            and any(
                abs(complex(*pair["eigenvalue"]) - 1.0) <= 1e-7
                for pair in rotations
            )
        )
        transverse.append(
            [pair for pair in pairs if pair["classification"] == "transverse"]
        )
    distance = None
    if transverse[0] and transverse[1]:
        leading = complex(*transverse[0][0]["eigenvalue"])
        distance = min(
            abs(leading - complex(*pair["eigenvalue"]))
            for pair in transverse[1]
        )
    return {
        "leading_transverse_distance": distance,
        "pass": bool(
            complete and symmetry and distance is not None and distance <= 1e-5
        ),
        "symmetry_pass": symmetry,
    }


def _verify_panel(panel: dict[str, Any], *, name: str) -> None:
    count, ncv, tolerance, iterations, seed = PANEL_CONFIGURATIONS[name]
    if (
        panel["expected_count"],
        panel["requested_count"],
        panel["ncv"],
        panel["tolerance"],
        panel["max_iterations"],
        panel["start_sha256"],
    ) != (count, count, ncv, tolerance, iterations, _start_hash(seed)):
        raise ValueError(f"$.arnoldi.{name}: registration mismatch")
    available = _nonnull_prefix(
        panel["eigenpairs"], path=f"$.arnoldi.{name}.eigenpairs"
    )
    pairs = panel["eigenpairs"][:available]
    for pair in pairs:
        if pair["modulus"] != abs(complex(*pair["eigenvalue"])):
            raise ValueError(f"$.arnoldi.{name}: modulus mismatch")
        if pair["normalized_residual"] < 0.0:
            raise ValueError(f"$.arnoldi.{name}: negative residual")
        if not (
            0.0 <= pair["translation_overlap"] <= 1.0
            and 0.0 <= pair["rotation_overlap"] <= 1.0
        ):
            raise ValueError(f"$.arnoldi.{name}: invalid overlap")
        expected_classification = (
            "translation"
            if pair["translation_overlap"] >= 0.99
            else "rotation"
            if pair["rotation_overlap"] >= 0.99
            else "transverse"
        )
        if pair["classification"] != expected_classification:
            raise ValueError(f"$.arnoldi.{name}: classification mismatch")
    if any(
        pairs[index]["modulus"] < pairs[index + 1]["modulus"]
        for index in range(len(pairs) - 1)
    ):
        raise ValueError(f"$.arnoldi.{name}: pairs not modulus-sorted")
    complete = bool(
        available == count
        and all(pair["vector"] is not None for pair in pairs)
        and all(pair["normalized_residual"] <= 1e-8 for pair in pairs)
    )
    if panel["status"] == "complete" and not complete:
        raise ValueError(f"$.arnoldi.{name}.status: false completion")


def _verify_trajectory(arm: dict[str, Any], *, path: str) -> None:
    count = _nonnull_prefix(arm["samples"], path=f"{path}.samples")
    samples = arm["samples"][:count]
    if not samples:
        raise ValueError(f"{path}: initial sample missing")
    for index, sample in enumerate(samples):
        if index < count - 1 or arm["completed"]:
            if sample["step"] != 10 * index:
                raise ValueError(f"{path}.samples: grid mismatch")
    if arm["completed"] and (arm["stopped"] or count != 501):
        raise ValueError(f"{path}: false completion")
    distances = [sample["distance"] for sample in samples]
    if "initial_distance" in arm:
        initial = distances[0]
        if initial <= 0.0:
            raise ValueError(f"{path}: invalid initial distance")
        if (
            arm["initial_distance"],
            arm["final_distance"],
            arm["final_ratio"],
            arm["growth_factor"],
        ) != (
            initial,
            distances[-1],
            distances[-1] / initial,
            max(distances) / initial,
        ):
            raise ValueError(f"{path}: summary mismatch")
    elif arm["maximum_distance"] != max(distances):
        raise ValueError(f"{path}: exact-control summary mismatch")


def _reconstruct_evidence(payload: dict[str, Any], *, preflight_pass: bool) -> dict[str, bool]:
    panels = (payload["arnoldi"]["primary"], payload["arnoldi"]["convergence"])
    panels_complete = all(
        panel["status"] == "complete"
        and all(pair is not None and pair["vector"] is not None for pair in panel["eigenpairs"])
        for panel in panels
    )
    residuals = bool(
        panels_complete
        and all(
            pair["normalized_residual"] <= 1e-8
            for panel in panels
            for pair in panel["eigenpairs"]
        )
    )
    agreement = bool(
        panels_complete and payload["arnoldi"]["panel_agreement"]["pass"]
    )
    symmetries = bool(
        panels_complete
        and payload["arnoldi"]["panel_agreement"]["symmetry_pass"]
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
    arms = payload["trajectories"]["perturbation_arms"]
    complete_arms = all(
        arm is not None and arm["completed"] and not arm["stopped"] for arm in arms
    )
    contraction = bool(
        complete_arms
        and all(
            arm["growth_factor"] <= 10.0 and arm["final_ratio"] <= 0.1
            for arm in arms
        )
    )
    exact = payload["trajectories"]["exact_control"]
    exact_pass = bool(
        exact is not None
        and exact["completed"]
        and not exact["stopped"]
        and exact["maximum_distance"] <= 1e-10
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
    matched = None
    if primary and convergence:
        matched = min(
            convergence,
            key=lambda pair: abs(
                complex(*pair["eigenvalue"]) - complex(*primary[0]["eigenvalue"])
            ),
        )
    unstable = bool(
        panels_complete
        and agreement
        and primary
        and matched is not None
        and primary[0]["modulus"] > 1.0 + 1e-6
        and matched["modulus"] > 1.0 + 1e-6
        and any(arm is not None and arm["growth_factor"] >= 100.0 for arm in arms)
    )
    return {
        "continuations_complete": complete_arms,
        "exact_arm": exact_pass,
        "instability_supported": bool(
            preflight_pass and residuals and symmetries and unstable
        ),
        "panel_agreement": agreement,
        "panels_complete": panels_complete,
        "perturbation_contraction": contraction,
        "preflight": preflight_pass,
        "ritz_residuals": residuals,
        "stable_spectrum": stable_spectrum,
        "symmetries": symmetries,
    }


def audit_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Audit one in-memory component record and return an independent verdict."""

    validate_contract(payload, _contract())
    identity = payload["identity"]
    if (
        identity["schema"] != SCHEMA
        or identity["equation_id"] != EQUATION_ID
        or identity["parameters"] != PARAMETERS
        or identity["start"] != list(START)
    ):
        raise ValueError("$.identity: registered input mismatch")
    created = datetime.fromisoformat(identity["created_utc"])
    if created.tzinfo is None or created.utcoffset() != UTC.utcoffset(created):
        raise ValueError("$.identity.created_utc: UTC required")
    finite = payload["finite_root"]
    rounded_root = _verify_finite_root(finite) if finite is not None else None
    preflight = payload["preflight"]
    if (preflight is None) is not (finite is None):
        raise ValueError("$.preflight: finite-root dependency mismatch")
    preflight_pass = bool(
        preflight is not None
        and rounded_root is not None
        and _verify_preflight(preflight, rounded_root=rounded_root)
    )
    for name in PANEL_CONFIGURATIONS:
        _verify_panel(payload["arnoldi"][name], name=name)
    theta = rounded_root[1] if rounded_root is not None else float(START[1])
    agreement = _panel_agreement(
        payload["arnoldi"]["primary"],
        payload["arnoldi"]["convergence"],
        theta=theta,
    )
    if payload["arnoldi"]["panel_agreement"] != agreement:
        raise ValueError("$.arnoldi.panel_agreement: reconstruction mismatch")
    arms = payload["trajectories"]["perturbation_arms"]
    arm_count = _nonnull_prefix(arms, path="$.trajectories.perturbation_arms")
    panels_ready = bool(
        preflight_pass
        and all(payload["arnoldi"][name]["status"] == "complete" for name in PANEL_CONFIGURATIONS)
        and agreement["pass"]
        and agreement["symmetry_pass"]
    )
    if arm_count and not panels_ready:
        raise ValueError("$.trajectories: opened without complete spectral prerequisite")
    exact = payload["trajectories"]["exact_control"]
    if (exact is not None) is not (arm_count == 3):
        raise ValueError("$.trajectories.exact_control: arm dependency mismatch")
    if rounded_root is not None:
        amplitude, perturbations = _registered_perturbations(
            radius=rounded_root[0], theta=rounded_root[1]
        )
        for index, arm in enumerate(arms[:arm_count]):
            name = ARM_NAMES[index]
            expected = perturbations[name]
            if (
                arm["name"] != name
                or arm["amplitude"] != amplitude
                or arm["perturbation"] != expected
                or arm["perturbation_sha256"] != _vector_sha256(expected)
            ):
                raise ValueError(f"$.trajectories.perturbation_arms[{index}]: mismatch")
            _verify_trajectory(
                arm, path=f"$.trajectories.perturbation_arms[{index}]"
            )
    if exact is not None:
        _verify_trajectory(exact, path="$.trajectories.exact_control")
    gates = _reconstruct_evidence(payload, preflight_pass=preflight_pass)
    stable = all(
        gates[name]
        for name in (
            "continuations_complete",
            "exact_arm",
            "panel_agreement",
            "panels_complete",
            "perturbation_contraction",
            "preflight",
            "ritz_residuals",
            "stable_spectrum",
            "symmetries",
        )
    )
    if stable:
        decision, state = "g5-local-direct-stability-pass", "pass"
    elif gates["instability_supported"]:
        decision, state = "g5-local-direct-instability-supported", "pass"
    else:
        decision, state = "g5-inconclusive", "inconclusive"
    expected_classification = {
        "G5": state,
        "claim_boundary": CLAIM_BOUNDARY,
        "decision": decision,
        "gates": gates,
    }
    if payload["classification"] != expected_classification:
        raise ValueError("$.classification: independent reconstruction mismatch")
    return {
        "decision": decision,
        "pass": True,
        "schema": "scalar-memory-rotating-wave-horizon-g5-independent-audit-v1",
        "trust_base": (
            "record relations independently reconstructed; sparse eigensolver and "
            "stored Jv-lambda-v residuals not independently recomputed"
        ),
    }


def audit_publication(
    *, result_path: Path, report_path: Path, manifest_path: Path
) -> dict[str, Any]:
    """Verify the manifest-last publication envelope and audit its payload."""

    if (result_path.name, report_path.name, manifest_path.name) != (
        RESULT_NAME,
        REPORT_NAME,
        MANIFEST_NAME,
    ):
        raise ValueError("publication: registered filenames mismatch")
    result_bytes = result_path.read_bytes()
    report_bytes = report_path.read_bytes()
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if type(manifest) is not dict or set(manifest) != {
        "artifacts",
        "execution_commit",
        "protocol_sha256",
        "schema",
    }:
        raise ValueError("manifest: fields mismatch")
    if manifest["schema"] != (
        "scalar-memory-rotating-wave-horizon-g5-publication-v1"
    ):
        raise ValueError("manifest: schema mismatch")
    expected_artifacts = [
        {
            "path": RESULT_NAME,
            "role": "result-json",
            "sha256": hashlib.sha256(result_bytes).hexdigest(),
        },
        {
            "path": REPORT_NAME,
            "role": "readable-report",
            "sha256": hashlib.sha256(report_bytes).hexdigest(),
        },
    ]
    if manifest["artifacts"] != expected_artifacts:
        raise ValueError("manifest: artifact hash mismatch")
    payload = json.loads(result_bytes)
    if (
        manifest["execution_commit"] != payload["identity"]["execution_commit"]
        or manifest["protocol_sha256"] != payload["identity"]["protocol_sha256"]
    ):
        raise ValueError("manifest: provenance binding mismatch")
    if manifest_path.stat().st_mtime_ns < max(
        result_path.stat().st_mtime_ns, report_path.stat().st_mtime_ns
    ):
        raise ValueError("manifest: not published last")
    result = audit_payload(payload)
    return {
        **result,
        "publication_pass": True,
        "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
    }
