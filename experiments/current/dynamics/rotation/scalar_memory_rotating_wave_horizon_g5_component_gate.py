"""Target-free orchestration for the preregistered isolated G5 component.

Importing this module performs no numerical target evaluation and writes no
artifacts.  ``assemble_component`` only calls explicitly injected stage
backends and fails closed between finite root, direct-map preflight, Arnoldi,
and nonlinear continuation.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal, localcontext
import copy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import struct
from typing import Any, Sequence

from emergenz_knoten.strict_json_contract import validate_payload as validate_contract


ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_g5_component_result_schema_v2.json"
)
HORIZON_GATE_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_transfer_gate.py"
)
PROTOCOL = ROOT / (
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_horizon_g5_component_attempt_3_protocol_2026-09-17.md"
)
REGISTERED_ATTEMPT = 3
RESULT_NAME = (
    "scalar_memory_rotating_wave_horizon_g5_component_attempt_3_2026-09-17.json"
)
REPORT_NAME = RESULT_NAME.removesuffix(".json") + ".md"
MANIFEST_NAME = RESULT_NAME.removesuffix(".json") + ".publication.json"
ATTEMPT_RECEIPT_PATH = (
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g5_component_attempt_3_receipt.json"
)
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
SCHEMA = "scalar-memory-rotating-wave-horizon-g5-component-v2"
EQUATION_ID = "deterministic-native-k0h-full-fifo-v1"
CLAIM_BOUNDARY = (
    "local direct H=2400 FIFO dynamics only; no H-infinity, formation, "
    "interaction, inertia, or mass claim"
)
ARM_NAMES = ("radial", "tangential", "full-history-transverse")
PANEL_CONFIGURATIONS = {
    "primary": (24, 96, 1e-10, 20000),
    "convergence": (36, 144, 1e-12, 40000),
}


def load_contract(path: Path = SCHEMA_PATH) -> dict[str, Any]:
    """Load the tracked exact-key result contract."""

    contract = json.loads(path.read_text(encoding="utf-8"))
    if contract.get("schema") != (
        "scalar-memory-rotating-wave-horizon-g5-result-contract-v2"
    ):
        raise ValueError("G5 component result-contract identity mismatch")
    return contract


def _load_horizon_gate() -> Any:
    specification = importlib.util.spec_from_file_location(
        "horizon_transfer_gate_for_g5_component", HORIZON_GATE_PATH
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load horizon-transfer numerical adapters")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class RegisteredBackend:
    """Lazy bridge to the existing numerical backends; never run on import."""

    def __init__(self) -> None:
        self._gate: Any | None = None

    @property
    def gate(self) -> Any:
        if self._gate is None:
            self._gate = _load_horizon_gate()
        return self._gate

    def finite_root(self) -> dict[str, Any] | None:
        return self.gate.finite_root_backend_record(
            horizon=2400, precision_dps=120, start=START
        )

    def preflight(self, *, rounded_root: tuple[float, float]) -> dict[str, Any]:
        return self.gate.g5_preflight_backend_record(rounded_root=rounded_root)

    def arnoldi_panel(
        self,
        *,
        name: str,
        rounded_root: tuple[float, float],
        start: Sequence[float],
    ) -> dict[str, Any]:
        return self.gate.arnoldi_backend_record(
            name=name, rounded_root=rounded_root, start=start
        )

    def continuation_arm(
        self,
        *,
        name: str,
        rounded_root: tuple[float, float],
        perturbation: Sequence[float],
    ) -> dict[str, Any]:
        return self.gate.continuation_backend_record(
            name=name, rounded_root=rounded_root, perturbation=perturbation
        )

    def exact_arm(self, *, rounded_root: tuple[float, float]) -> dict[str, Any]:
        return self.gate.exact_backend_record(rounded_root=rounded_root)


def _vector_sha256(values: Sequence[float]) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(struct.pack("<d", float(value)))
    return digest.hexdigest()


def arnoldi_start_vectors() -> dict[str, list[float]]:
    """Reconstruct both preregistered integer-LCG Arnoldi starts."""

    component = float.fromhex("0x1.d8f7208e6b82cp-7")
    result: dict[str, list[float]] = {}
    for name, seed in (("primary", 0x243F6A88), ("convergence", 0x85A308D3)):
        state = seed
        values = []
        for _ in range(4800):
            state = (1664525 * state + 1013904223) & 0xFFFFFFFF
            values.append(component if state & 0x80000000 else -component)
        result[name] = values
    return result


def registered_perturbations(
    *, radius: float, theta: float
) -> tuple[float, dict[str, list[float]]]:
    """Reconstruct the three preregistered direct-map perturbations."""

    horizon = 2400
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
    full = [amplitude * value / full_norm for value in full]
    return amplitude, {
        "radial": radial,
        "tangential": tangential,
        "full-history-transverse": full,
    }


def _empty_panel(name: str) -> dict[str, Any]:
    count, ncv, tolerance, iterations = PANEL_CONFIGURATIONS[name]
    start = arnoldi_start_vectors()[name]
    return {
        "eigenpairs": [None] * count,
        "expected_count": count,
        "max_iterations": iterations,
        "ncv": ncv,
        "requested_count": count,
        "start_sha256": _vector_sha256(start),
        "status": "arpack-no-convergence",
        "tolerance": tolerance,
    }


def _nonnull_prefix(values: Sequence[Any], *, path: str) -> int:
    count = 0
    saw_null = False
    for value in values:
        if value is None:
            saw_null = True
        elif saw_null:
            raise ValueError(f"{path}: non-null entries must form a prefix")
        else:
            count += 1
    return count


def panel_agreement(
    primary: dict[str, Any], convergence: dict[str, Any], *, theta: float
) -> dict[str, Any]:
    """Reconstruct the registered symmetry and transverse-panel comparison."""

    panels = (primary, convergence)
    complete = all(panel["status"] == "complete" for panel in panels)
    expected_translations = (
        complex(math.cos(theta), math.sin(theta)),
        complex(math.cos(theta), -math.sin(theta)),
    )
    symmetry_pass = complete
    transverse = []
    for panel in panels:
        pairs = [pair for pair in panel["eigenpairs"] if pair is not None]
        translations = [
            pair for pair in pairs if pair["classification"] == "translation"
        ]
        rotations = [
            pair for pair in pairs if pair["classification"] == "rotation"
        ]
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
            complete and symmetry_pass and distance is not None and distance <= 1e-5
        ),
        "symmetry_pass": symmetry_pass,
    }


def _panels_ready(arnoldi: dict[str, Any]) -> bool:
    expected = {"primary": 24, "convergence": 36}
    for name, count in expected.items():
        panel = arnoldi[name]
        if panel["status"] != "complete":
            return False
        if _nonnull_prefix(panel["eigenpairs"], path=f"$.arnoldi.{name}") != count:
            return False
        if any(
            pair["vector"] is None or pair["normalized_residual"] > 1e-8
            for pair in panel["eigenpairs"]
        ):
            return False
    return bool(
        arnoldi["panel_agreement"]["pass"]
        and arnoldi["panel_agreement"]["symmetry_pass"]
    )


def evidence(payload: dict[str, Any]) -> dict[str, bool]:
    """Reconstruct every decision gate from primitive records."""

    preflight = payload["preflight"]
    preflight_pass = bool(
        preflight is not None and preflight["record"]["gates"]["pass"]
    )
    panels = (payload["arnoldi"]["primary"], payload["arnoldi"]["convergence"])
    panels_complete = all(
        panel["status"] == "complete"
        and all(pair is not None and pair["vector"] is not None for pair in panel["eigenpairs"])
        for panel in panels
    )
    ritz_residuals = bool(
        panels_complete
        and all(
            0.0 <= pair["normalized_residual"] <= 1e-8
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
    continuations_complete = all(
        arm is not None and arm["completed"] and not arm["stopped"] for arm in arms
    )
    contraction = bool(
        continuations_complete
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
    unstable_spectrum = bool(
        panels_complete
        and agreement
        and primary
        and matched is not None
        and primary[0]["modulus"] > 1.0 + 1e-6
        and matched["modulus"] > 1.0 + 1e-6
    )
    growth = any(
        arm is not None and arm["growth_factor"] >= 100.0 for arm in arms
    )
    return {
        "continuations_complete": continuations_complete,
        "exact_arm": exact_pass,
        "instability_supported": bool(
            preflight_pass
            and ritz_residuals
            and symmetries
            and unstable_spectrum
            and growth
        ),
        "panel_agreement": agreement,
        "panels_complete": panels_complete,
        "perturbation_contraction": contraction,
        "preflight": preflight_pass,
        "ritz_residuals": ritz_residuals,
        "stable_spectrum": stable_spectrum,
        "symmetries": symmetries,
    }


def classification(payload: dict[str, Any]) -> dict[str, Any]:
    gates = evidence(payload)
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
        decision = "g5-local-direct-stability-pass"
        state = "pass"
    elif gates["instability_supported"]:
        decision = "g5-local-direct-instability-supported"
        state = "pass"
    else:
        decision = "g5-inconclusive"
        state = "inconclusive"
    return {
        "G5": state,
        "claim_boundary": CLAIM_BOUNDARY,
        "decision": decision,
        "gates": gates,
    }


def _canonical_sha256(value: Any) -> str:
    content = json.dumps(
        value, allow_nan=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def _verify_trajectory(arm: dict[str, Any], *, path: str) -> None:
    dense_count = _nonnull_prefix(
        arm["dense_distances"], path=f"{path}.dense_distances"
    )
    dense = arm["dense_distances"][:dense_count]
    if not dense or any(
        type(value) not in (int, float) or not math.isfinite(value) or value < 0.0
        for value in dense
    ):
        raise ValueError(f"{path}.dense_distances: invalid distance")
    final_step = dense_count - 1
    complete = bool(not arm["stopped"] and final_step == 5000)
    if arm["completed"] is not complete or (not complete and not arm["stopped"]):
        raise ValueError(f"{path}: completion state mismatch")
    sample_count = _nonnull_prefix(arm["samples"], path=f"{path}.samples")
    samples = arm["samples"][:sample_count]
    expected_steps = list(range(0, final_step + 1, 10))
    if expected_steps[-1] != final_step:
        expected_steps.append(final_step)
    if [sample["step"] for sample in samples] != expected_steps:
        raise ValueError(f"{path}.samples: grid mismatch")
    if any(sample["distance"] != dense[sample["step"]] for sample in samples):
        raise ValueError(f"{path}.samples: dense projection mismatch")
    maximum = max(dense)
    maximum_step = dense.index(maximum)
    if "initial_distance" in arm:
        initial = dense[0]
        if initial <= 0.0:
            raise ValueError(f"{path}: nonpositive initial distance")
        expected = (
            initial,
            dense[-1],
            dense[-1] / initial,
            maximum,
            maximum_step,
            maximum / initial,
        )
        observed = (
            arm["initial_distance"],
            arm["final_distance"],
            arm["final_ratio"],
            arm["maximum_distance"],
            arm["maximum_step"],
            arm["growth_factor"],
        )
        if observed != expected:
            raise ValueError(f"{path}: trajectory summary mismatch")
    elif (arm["maximum_distance"], arm["maximum_step"]) != (
        maximum,
        maximum_step,
    ):
        raise ValueError(f"{path}: exact-control summary mismatch")


def validate_payload(payload: dict[str, Any]) -> None:
    """Apply the exact contract and independently reconstructed relations."""

    validate_contract(payload, load_contract())
    identity = payload["identity"]
    if identity["parameters"] != PARAMETERS or identity["start"] != list(START):
        raise ValueError("$.identity: registered input mismatch")
    if identity["equation_id"] != EQUATION_ID:
        raise ValueError("$.identity.equation_id: mismatch")
    authorization = identity["authorization"]
    if (
        authorization["attempt"] != REGISTERED_ATTEMPT
        or authorization["attempt_receipt_path"] != ATTEMPT_RECEIPT_PATH
        or authorization["ci_run_id"] <= 0
        or authorization["upstream_revision"] != identity["execution_commit"]
    ):
        raise ValueError("$.identity.authorization: execution binding mismatch")
    created = datetime.fromisoformat(identity["created_utc"])
    if created.tzinfo is None or created.utcoffset() != UTC.utcoffset(created):
        raise ValueError("$.identity.created_utc: UTC timestamp required")
    finite = payload["finite_root"]
    if finite is None:
        if payload["preflight"] is not None:
            raise ValueError("$.preflight: evidence without finite root")
    else:
        newton = finite["newton"]
        if newton["precision_dps"] != 120 or newton["steps"] != 8:
            raise ValueError("$.finite_root.newton: configuration mismatch")
        for name, width in (("outer_certificate", Decimal("1e-8")), ("inner_certificate", Decimal("1e-30"))):
            certificate = finite[name]
            if certificate["interval_backend"] != "mpmath.iv" or not certificate["strict_interior"]:
                raise ValueError(f"$.finite_root.{name}: certificate mismatch")
            with localcontext() as context:
                context.prec = 180
                for index, coordinate in enumerate(("radius", "theta")):
                    lower, upper = map(Decimal, certificate["box"][coordinate])
                    center = Decimal((newton["radius"], newton["theta"])[index])
                    if not lower <= center - width < center + width <= upper:
                        raise ValueError(f"$.finite_root.{name}.box: root binding mismatch")
                    image_lower, image_upper = map(Decimal, certificate["krawczyk_image"][index])
                    if not lower < image_lower <= image_upper < upper:
                        raise ValueError(f"$.finite_root.{name}: non-strict image")
    preflight = payload["preflight"]
    if preflight is not None:
        record = preflight["record"]
        if preflight["record_sha256"] != _canonical_sha256(record):
            raise ValueError("$.preflight.record_sha256: mismatch")
        if finite is None:
            raise ValueError("$.preflight: missing root")
        expected_root = [
            float(finite["newton"]["radius"]),
            float(finite["newton"]["theta"]),
        ]
        if [record["candidate"]["radius"], record["candidate"]["theta"]] != expected_root:
            raise ValueError("$.preflight.record.candidate: root mismatch")
        if record["candidate"]["horizon"] != 2400:
            raise ValueError("$.preflight.record.candidate.horizon: mismatch")
        equation = record["equation"]
        if equation != {
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
        }:
            raise ValueError("$.preflight.record.equation: mismatch")
        if record["jacobian"]["shape"] != [4800, 4800] or record["jacobian"]["nnz"] != 19196:
            raise ValueError("$.preflight.record.jacobian: structure mismatch")
        if record["thresholds"] != {
            "fixed_point_maximum": 1e-14,
            "symmetry_residual_maximum": 1e-10,
        }:
            raise ValueError("$.preflight.record.thresholds: mismatch")
        expected_weight = 1.0 - 0.99**2400
        memory = record["memory"]
        if memory["closed_form_retained_weight"] != expected_weight:
            raise ValueError("$.preflight.record.memory: closed form mismatch")
        if memory["identity_absolute_error"] != abs(
            memory["direct_retained_weight"]
            - memory["closed_form_retained_weight"]
        ):
            raise ValueError("$.preflight.record.memory: identity error mismatch")
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
        expected_gates = {
            "finite": True,
            "fixed_point": (
                record["orbit"]["co_rotating_fixed_point_max_abs_error"]
                <= 1e-14
            ),
            "jacobian_structure": True,
            "native_circle_covariance": (
                record["orbit"]["native_circle_covariance_max_abs_error"]
                <= 1e-14
            ),
            "symmetries": expected_symmetry,
            "weight_identity": (
                memory["identity_absolute_error"]
                <= 8.0 * math.ulp(max(1.0, abs(expected_weight)))
            ),
        }
        expected_gates["pass"] = all(expected_gates.values())
        if record["gates"] != expected_gates:
            raise ValueError("$.preflight.record.gates: reconstruction mismatch")
    expected_starts = {
        name: _vector_sha256(values)
        for name, values in arnoldi_start_vectors().items()
    }
    for name, configuration in PANEL_CONFIGURATIONS.items():
        panel = payload["arnoldi"][name]
        count, ncv, tolerance, iterations = configuration
        if (
            panel["expected_count"], panel["requested_count"], panel["ncv"],
            panel["tolerance"], panel["max_iterations"], panel["start_sha256"]
        ) != (count, count, ncv, tolerance, iterations, expected_starts[name]):
            raise ValueError(f"$.arnoldi.{name}: registration mismatch")
        _nonnull_prefix(panel["eigenpairs"], path=f"$.arnoldi.{name}.eigenpairs")
        for pair in (value for value in panel["eigenpairs"] if value is not None):
            if pair["modulus"] != abs(complex(*pair["eigenvalue"])):
                raise ValueError(f"$.arnoldi.{name}: modulus mismatch")
            if pair["normalized_residual"] < 0.0:
                raise ValueError(f"$.arnoldi.{name}: negative residual")
            if pair["vector"] is not None and not any(
                real != 0.0 or imag != 0.0 for real, imag in pair["vector"]
            ):
                raise ValueError(f"$.arnoldi.{name}: zero Ritz vector")
            if not (0.0 <= pair["translation_overlap"] <= 1.0 and 0.0 <= pair["rotation_overlap"] <= 1.0):
                raise ValueError(f"$.arnoldi.{name}: overlap outside [0,1]")
            expected_classification = (
                "translation"
                if pair["translation_overlap"] >= 0.99
                else "rotation"
                if pair["rotation_overlap"] >= 0.99
                else "transverse"
            )
            if pair["classification"] != expected_classification:
                raise ValueError(f"$.arnoldi.{name}: classification mismatch")
    preflight_pass = bool(
        preflight is not None and preflight["record"]["gates"]["pass"]
    )
    if not preflight_pass and any(
        pair is not None
        for name in PANEL_CONFIGURATIONS
        for pair in payload["arnoldi"][name]["eigenpairs"]
    ):
        raise ValueError("$.arnoldi: evidence without passing preflight")
    theta = float(finite["newton"]["theta"]) if finite is not None else float(START[1])
    agreement = panel_agreement(
        payload["arnoldi"]["primary"], payload["arnoldi"]["convergence"], theta=theta
    )
    if payload["arnoldi"]["panel_agreement"] != agreement:
        raise ValueError("$.arnoldi.panel_agreement: reconstruction mismatch")
    arms = payload["trajectories"]["perturbation_arms"]
    _nonnull_prefix(arms, path="$.trajectories.perturbation_arms")
    ready = _panels_ready(payload["arnoldi"])
    if any(arm is not None for arm in arms) and not ready:
        raise ValueError("$.trajectories: evidence without complete panels")
    if finite is not None:
        amplitude, perturbations = registered_perturbations(
            radius=float(finite["newton"]["radius"]), theta=theta
        )
        for index, arm in enumerate(arms):
            if arm is None:
                continue
            name = ARM_NAMES[index]
            expected = perturbations[name]
            if arm["name"] != name or arm["amplitude"] != amplitude or arm["perturbation"] != expected:
                raise ValueError(f"$.trajectories.perturbation_arms[{index}]: perturbation mismatch")
            if arm["perturbation_sha256"] != _vector_sha256(expected):
                raise ValueError(f"$.trajectories.perturbation_arms[{index}]: hash mismatch")
            _verify_trajectory(arm, path=f"$.trajectories.perturbation_arms[{index}]")
    exact = payload["trajectories"]["exact_control"]
    if (exact is not None) is not all(arm is not None for arm in arms):
        raise ValueError("$.trajectories.exact_control: arm dependency mismatch")
    if exact is not None:
        _verify_trajectory(exact, path="$.trajectories.exact_control")
    if payload["classification"] != classification(payload):
        raise ValueError("$.classification: reconstruction mismatch")
    if payload["publication"] != {
        "artifacts": [
            {"path": RESULT_NAME, "role": "result-json"},
            {"path": REPORT_NAME, "role": "readable-report"},
        ],
        "manifest_path": MANIFEST_NAME,
        "manifest_published_last": True,
    }:
        raise ValueError("$.publication: registration mismatch")


def assemble_component(
    *, backend: Any, identity: dict[str, Any], publication: dict[str, Any]
) -> dict[str, Any]:
    """Compose one isolated G5 record from injected target-free stages."""

    finite = copy.deepcopy(backend.finite_root())
    preflight = None
    panels = {name: _empty_panel(name) for name in PANEL_CONFIGURATIONS}
    arms: list[dict[str, Any] | None] = [None, None, None]
    exact = None
    if finite is not None:
        rounded_root = (
            float(finite["newton"]["radius"]),
            float(finite["newton"]["theta"]),
        )
        preflight = copy.deepcopy(backend.preflight(rounded_root=rounded_root))
        if preflight["record"]["gates"]["pass"] is True:
            starts = arnoldi_start_vectors()
            panels = {
                name: copy.deepcopy(
                    backend.arnoldi_panel(
                        name=name, rounded_root=rounded_root, start=starts[name]
                    )
                )
                for name in PANEL_CONFIGURATIONS
            }
            agreement = panel_agreement(
                panels["primary"], panels["convergence"], theta=rounded_root[1]
            )
            arnoldi = {**panels, "panel_agreement": agreement}
            if _panels_ready(arnoldi):
                _, perturbations = registered_perturbations(
                    radius=rounded_root[0], theta=rounded_root[1]
                )
                arms = [
                    copy.deepcopy(
                        backend.continuation_arm(
                            name=name,
                            rounded_root=rounded_root,
                            perturbation=perturbations[name],
                        )
                    )
                    for name in ARM_NAMES
                ]
                exact = copy.deepcopy(backend.exact_arm(rounded_root=rounded_root))
    arnoldi = {
        **panels,
        "panel_agreement": panel_agreement(
            panels["primary"],
            panels["convergence"],
            theta=(float(finite["newton"]["theta"]) if finite is not None else float(START[1])),
        ),
    }
    payload = {
        "arnoldi": arnoldi,
        "classification": {},
        "finite_root": finite,
        "identity": copy.deepcopy(identity),
        "preflight": preflight,
        "publication": copy.deepcopy(publication),
        "trajectories": {
            "exact_control": exact,
            "perturbation_arms": arms,
        },
    }
    payload["classification"] = classification(payload)
    validate_payload(payload)
    return payload


def render_report(payload: dict[str, Any]) -> str:
    """Render the deliberately narrow readable companion to one result."""

    gates = payload["classification"]["gates"]
    completed_panels = sum(
        payload["arnoldi"][name]["status"] == "complete"
        for name in PANEL_CONFIGURATIONS
    )
    completed_arms = sum(
        arm is not None and arm["completed"]
        for arm in payload["trajectories"]["perturbation_arms"]
    )
    return "\n".join(
        (
            "# Isolated G5 direct-FIFO component result",
            "",
            f"Decision: **`{payload['classification']['decision']}`**.",
            "",
            "## Measured",
            "",
            f"- direct-equation preflight: `{gates['preflight']}`",
            f"- complete Arnoldi panels: `{completed_panels}/2`",
            f"- complete nonlinear perturbation arms: `{completed_arms}/3`",
            f"- exact-control gate: `{gates['exact_arm']}`",
            "",
            "## Claim boundary",
            "",
            payload["classification"]["claim_boundary"] + ".",
            "",
            "The audit reconstructs record relations and the decision, but is not",
            "a second sparse eigensolver and does not recompute Jv-lambda-v.",
            "",
        )
    )


def _atomic_write(path: Path, content: bytes) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("xb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def publish_payload(payload: dict[str, Any], *, directory: Path) -> dict[str, Path]:
    """Write result and report before the publication manifest, exactly once."""

    validate_payload(payload)
    result_path = directory / RESULT_NAME
    report_path = directory / REPORT_NAME
    manifest_path = directory / MANIFEST_NAME
    paths = (result_path, report_path, manifest_path)
    if any(path.exists() for path in paths):
        raise FileExistsError("refusing to overwrite a G5 component artifact")
    result_bytes = (
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    report_bytes = render_report(payload).encode("utf-8")
    _atomic_write(result_path, result_bytes)
    _atomic_write(report_path, report_bytes)
    manifest = {
        "artifacts": [
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
        ],
        "execution_commit": payload["identity"]["execution_commit"],
        "protocol_sha256": payload["identity"]["protocol_sha256"],
        "schema": "scalar-memory-rotating-wave-horizon-g5-publication-v1",
    }
    manifest_bytes = (
        json.dumps(manifest, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    _atomic_write(manifest_path, manifest_bytes)
    return {
        "manifest": manifest_path,
        "report": report_path,
        "result": result_path,
    }
