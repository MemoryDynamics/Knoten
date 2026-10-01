"""Fail-closed contract for the uniform H=3600 to infinity branch link.

This module contains the reusable target computation and result semantics.  It
does not authorize execution; the separate execution wrapper must validate a
one-shot governance record before calling :func:`run_contract`.
"""

from __future__ import annotations

import copy
from datetime import UTC, datetime
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import cache
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
from typing import Any, Callable, Sequence

from emergenz_knoten.rotating_wave_interval import (
    IntervalRotatingWaveParameters,
    certify_rotating_wave_tail_homotopy_box,
    exact_decimal_from_mpf_tuple,
)
from emergenz_knoten.strict_json_contract import validate_payload as validate_contract


ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_result_schema_v4.json"
)
TRANSFER_GATE_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_transfer_gate.py"
)
PROTOCOL = ROOT / (
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_4_protocol_2026-10-01.md"
)
RESULT = ROOT / (
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_4_2026-10-01.json"
)
REPORT = RESULT.with_suffix(".md")
MANIFEST = RESULT.with_suffix(".publication.json")
AUDIT = ROOT / (
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_4_independent_audit_2026-10-01.json"
)
SCHEMA = "scalar-memory-rotating-wave-horizon-infinity-branch-link-v4"
ATTEMPT = 4
PASS_DECISION = "g-infinity-uniform-tail-branch-link-pass"
INCONCLUSIVE_DECISION = "g-infinity-branch-link-inconclusive"
CLAIM_BOUNDARY = (
    "local uniform root-branch continuation from finite H=3600 to F_infinity "
    "under registered tail bounds and mpmath.iv; no H-infinity stability, "
    "global uniqueness, formation, interaction, spin, inertia or mass"
)
PARAMETERS = {
    "alpha": 0.01,
    "amplitude_att": 3.5,
    "amplitude_rep": 1.0,
    "eta": 0.15,
    "horizon": 3600,
    "memory_mass": 1.0,
    "q": 0.99,
    "sigma_att": 3.0,
    "sigma_rep": 1.0,
}
INTERVAL_PARAMETERS = IntervalRotatingWaveParameters(
    alpha="0.01",
    horizon=3600,
    memory_mass="1",
    eta="0.15",
    sigma_rep="1",
    sigma_att="3",
    amplitude_rep="1",
    amplitude_att="3.5",
)
SCALE_INTERVAL = ("0", "1")
HALF_WIDTH = "1e-10"
PRECISIONS = (120, 160)
SEALED_FILES = (
    (
        "g1-g3-result",
        "reports/dynamics/rotation/"
        "scalar_memory_rotating_wave_horizon_g1_g3_bridge_attempt_2_2026-09-27.json",
        "31bff4d3f1dfbede5060b43622aacd597b79a6f8b67ec09f2119d35759a0669d",
    ),
    (
        "g1-g3-manifest",
        "reports/dynamics/rotation/"
        "scalar_memory_rotating_wave_horizon_g1_g3_bridge_attempt_2_2026-09-27.publication.json",
        "394410f55fd3610a122f319c544296d7614185e6f2eae86bae6eb8a64962b31d",
    ),
    (
        "g1-g3-audit",
        "reports/project/meta/reviews/"
        "scalar_memory_rotating_wave_horizon_g1_g3_bridge_attempt_2_independent_audit_2026-09-27.json",
        "f4fdfd5dffa7eb3fc7a7ca17a8b9afdb742c69c815767608a8295bd017cad5a0",
    ),
    (
        "g4-result",
        "reports/dynamics/rotation/"
        "scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.json",
        "783328382545dbf4a08698ebd7a8ba7f3ef06ac344630f2b04e4ef7dd54c5a88",
    ),
    (
        "g4-manifest",
        "reports/dynamics/rotation/"
        "scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.publication.json",
        "63a54a572e4af3067609e93caea503b30f46013d89d968c4fdb2d9719a6597da",
    ),
    (
        "g4-audit",
        "reports/project/meta/reviews/"
        "scalar_memory_rotating_wave_horizon_g4_component_independent_audit_2026-09-13.json",
        "e83309992fe8b964c507930664f557367a50d87d32aedf7bf39ecbe1bb346d19",
    ),
)


def _git_blob_bytes(repository: Path, relative: str) -> bytes:
    return subprocess.run(
        ["git", "cat-file", "blob", f"HEAD:{relative}"],
        cwd=repository,
        check=True,
        capture_output=True,
    ).stdout


@cache
def _transfer_gate() -> Any:
    specification = importlib.util.spec_from_file_location(
        "infinity_branch_reused_transfer_gate", TRANSFER_GATE_PATH
    )
    if specification is None or specification.loader is None:
        raise ImportError("cannot load registered horizon-transfer gate")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _manifest_binds_result(
    manifest: dict[str, Any], *, registered_path: str, digest: str
) -> bool:
    rows = manifest.get("artifacts")
    return type(rows) is list and any(
        type(row) is dict
        and row.get("role") == "result-json"
        and row.get("path") == registered_path
        and row.get("sha256") == digest
        for row in rows
    )


def load_sealed_inputs(*, root: Path = ROOT) -> dict[str, Any]:
    """Load and bind the six preregistered G1--G3/G4 Git blobs."""

    repository = Path(root).resolve()
    documents: dict[str, dict[str, Any]] = {}
    files = []
    for role, relative, expected_sha256 in SEALED_FILES:
        path = (repository / relative).resolve()
        if repository not in path.parents:
            raise ValueError("sealed input escaped repository")
        raw = _git_blob_bytes(repository, relative)
        observed = hashlib.sha256(raw).hexdigest()
        if observed != expected_sha256:
            raise ValueError(f"sealed input hash mismatch: {role}")
        parsed = json.loads(raw)
        if type(parsed) is not dict:
            raise TypeError(f"sealed input root is not an object: {role}")
        documents[role] = parsed
        files.append({"role": role, "path": relative, "sha256": observed})

    bridge = documents["g1-g3-result"]
    g4 = documents["g4-result"]
    if (
        bridge.get("identity", {}).get("schema")
        != "scalar-memory-rotating-wave-horizon-g1-g3-bridge-v2"
        or bridge.get("classification", {}).get("decision")
        != "rotating-wave-root-branch-connected-with-h2400-local-stability-support"
        or documents["g1-g3-audit"].get("verdict")
        != "g1-g3-bridge-independent-audit-agrees"
        or documents["g1-g3-audit"].get("result_sha256") != SEALED_FILES[0][2]
        or g4.get("identity", {}).get("schema")
        != "scalar-memory-rotating-wave-horizon-g4-component-v1"
        or g4.get("classification", {}).get("decision")
        != "g4-local-infinite-root-pass"
        or documents["g4-audit"].get("verdict")
        != "g4-independent-audit-agrees"
        or documents["g4-audit"].get("result_sha256") != SEALED_FILES[3][2]
    ):
        raise ValueError("sealed input decision, schema, or audit mismatch")
    if not _manifest_binds_result(
        documents["g1-g3-manifest"],
        registered_path=SEALED_FILES[0][1],
        digest=SEALED_FILES[0][2],
    ) or not _manifest_binds_result(
        documents["g4-manifest"],
        registered_path=Path(SEALED_FILES[3][1]).name,
        digest=SEALED_FILES[3][2],
    ):
        raise ValueError("sealed manifest does not bind registered result")

    bridge_panel = bridge["finite_branch"]["root_panels"][-1]
    if bridge_panel.get("horizon") != 3600:
        raise ValueError("sealed bridge endpoint horizon mismatch")
    bridge_root = [
        bridge_panel["newton_120"]["radius"],
        bridge_panel["newton_120"]["theta"],
    ]
    g4_root = [
        g4["finite_root"]["newton"]["radius"],
        g4["finite_root"]["newton"]["theta"],
    ]
    endpoint = next(
        (
            row
            for row in bridge["endpoint_links"]
            if row.get("component") == "G4" and row.get("horizon") == 3600
        ),
        None,
    )
    if endpoint is None:
        raise ValueError("sealed G4 bridge endpoint missing")

    expected_bounds = [
        {
            "precision_dps": precision,
            **_transfer_gate().tail_bounds(horizon=3600, precision_dps=precision),
        }
        for precision in PRECISIONS
    ]
    if g4["infinite_tail"]["bounds"] != expected_bounds:
        raise ValueError("sealed G4 tail bounds mismatch")
    tail_panels = g4["infinite_tail"]["certificate_panels"]
    if (
        type(tail_panels) is not list
        or len(tail_panels) != 2
        or any(panel is None for panel in tail_panels)
        or any(not panel["certificate"]["strict_interior"] for panel in tail_panels)
    ):
        raise ValueError("sealed G4 tail certificate mismatch")

    sealed = {
        "files": files,
        "bridge_root": bridge_root,
        "g4_finite_root": g4_root,
        "bridge_endpoint_pass": endpoint.get("pass") is True,
        "tail_bounds": expected_bounds,
        "g4_tail_boxes": [
            copy.deepcopy(panel["certificate"]["box"]) for panel in tail_panels
        ],
        "g4_tail_images": [
            copy.deepcopy(panel["certificate"]["krawczyk_image"])
            for panel in tail_panels
        ],
    }
    _validate_sealed_inputs(sealed)
    return sealed


def _schema() -> dict[str, Any]:
    payload = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if type(payload) is not dict:
        raise TypeError("branch-link schema root must be an object")
    return payload


def _decimal(value: str, *, path: str) -> Decimal:
    if type(value) is not str:
        raise TypeError(f"{path}: expected decimal string")
    parsed = Decimal(value)
    if not parsed.is_finite():
        raise ValueError(f"{path}: nonfinite decimal")
    return parsed


def _pair(values: Sequence[str], *, path: str) -> tuple[Decimal, Decimal]:
    if type(values) is not list or len(values) != 2:
        raise TypeError(f"{path}: expected decimal pair")
    lower = _decimal(values[0], path=f"{path}[0]")
    upper = _decimal(values[1], path=f"{path}[1]")
    if lower > upper:
        raise ValueError(f"{path}: reversed interval")
    return lower, upper


def _raw_interval(value: Any, *, path: str) -> list[str]:
    if type(value) is not dict or "lower_binary" not in value or "upper_binary" not in value:
        raise TypeError(f"{path}: invalid raw interval")
    pair = [
        exact_decimal_from_mpf_tuple(value["lower_binary"]),
        exact_decimal_from_mpf_tuple(value["upper_binary"]),
    ]
    _pair(pair, path=path)
    return pair


def _point_in_box(point: Sequence[str], box: dict[str, Sequence[str]]) -> bool:
    for index, coordinate in enumerate(("radius", "theta")):
        lower, upper = _pair(box[coordinate], path=f"box.{coordinate}")
        value = _decimal(point[index], path=f"point[{index}]")
        if not lower <= value <= upper:
            return False
    return True


def _image_in_box(
    image: Sequence[Sequence[str]], box: dict[str, Sequence[str]]
) -> bool:
    if type(image) is not list or len(image) != 2:
        raise TypeError("image must contain two intervals")
    for index, coordinate in enumerate(("radius", "theta")):
        image_lower, image_upper = _pair(image[index], path=f"image[{index}]")
        box_lower, box_upper = _pair(box[coordinate], path=f"box.{coordinate}")
        if not box_lower < image_lower <= image_upper < box_upper:
            return False
    return True


def _boxes_equal(first: dict[str, Any], second: dict[str, Any]) -> bool:
    return all(
        _pair(first[name], path=f"first.{name}")
        == _pair(second[name], path=f"second.{name}")
        for name in ("radius", "theta")
    )


def _intersection(
    first: Sequence[Sequence[str]], second: Sequence[Sequence[str]]
) -> dict[str, list[str]] | None:
    result = {}
    for index, coordinate in enumerate(("radius", "theta")):
        first_pair = _pair(first[index], path=f"first[{index}]")
        second_pair = _pair(second[index], path=f"second[{index}]")
        lower = max(first_pair[0], second_pair[0])
        upper = min(first_pair[1], second_pair[1])
        if lower > upper:
            return None
        result[coordinate] = [format(lower, "f"), format(upper, "f")]
    return result


def _validate_sealed_inputs(sealed: dict[str, Any]) -> None:
    validate_contract(
        {
            "identity": {
                "attempt": ATTEMPT,
                "schema": SCHEMA,
                "version": 4,
                "created_utc": "synthetic",
                "execution_commit": "0" * 40,
                "protocol_blob": _schema()["constants"]["protocol_blob"],
                "protocol_sha256": _schema()["constants"]["protocol_sha256"],
                "parameters": PARAMETERS,
                "authorization": {
                    "attempt": ATTEMPT,
                    "authorization_id": "00000000-0000-4000-8000-000000000000",
                    "ci_run_id": 0,
                    "governance_sha256": "0" * 64,
                    "implementation_revision": "0" * 40,
                    "receipt_path": "synthetic",
                    "receipt_sha256": "0" * 64,
                    "upstream_revision": "0" * 40,
                },
            },
            "sealed_inputs": sealed,
            "model_identity": {
                "homotopy_family": "F_s=F_3600+s*T_3600",
                "scale_interval": ["0", "1"],
                "finite_endpoint": "F_3600",
                "infinite_endpoint": "F_infinity",
                "tail_bounds_replayed": True,
            },
            "homotopy": {
                "panels": [None, None],
                "intersection": None,
                "overlap": False,
                "endpoint_binding": {
                    "bridge_endpoint_pass": False,
                    "bridge_root_matches_g4": False,
                    "finite_root_in_uniform_box": False,
                    "g4_tail_boxes_match_uniform": False,
                    "g4_tail_images_in_uniform_box": False,
                    "pass": False,
                },
            },
            "classification": {
                "gates": {name: "inconclusive" for name in ("U0", "U1", "U2", "U3", "U4", "U5")},
                "decision": INCONCLUSIVE_DECISION,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            "publication": {
                "artifacts": [
                    {"path": RESULT.name, "role": "result-json"},
                    {"path": REPORT.name, "role": "readable-report"},
                ],
                "auditor_output_path": AUDIT.relative_to(ROOT).as_posix(),
                "manifest_path": MANIFEST.name,
                "manifest_published_last": True,
            },
        },
        _schema(),
    )


def _panel_record(raw: dict[str, Any], *, precision: int, root: list[str], bounds: dict[str, Any]) -> dict[str, Any]:
    if raw.get("precision_dps") != precision:
        raise ValueError("uniform panel precision mismatch")
    if raw.get("tail_scale_interval") != list(SCALE_INTERVAL):
        raise ValueError("uniform panel scale interval mismatch")
    if raw.get("center") != {"radius": root[0], "theta": root[1]} or raw.get(
        "half_width"
    ) != {"radius": HALF_WIDTH, "theta": HALF_WIDTH}:
        raise ValueError("uniform panel center or width mismatch")
    expected_tail = {
        "residual": bounds["residual_bound"],
        "jacobian_radius": bounds["jacobian_radius_bound"],
        "jacobian_theta": bounds["jacobian_theta_bound"],
    }
    if raw.get("tail_bounds") != expected_tail:
        raise ValueError("uniform panel tail bounds mismatch")

    box_pairs = [_raw_interval(value, path=f"box[{index}]") for index, value in enumerate(raw["box"])]
    image = [_raw_interval(value, path=f"image[{index}]") for index, value in enumerate(raw["krawczyk_image"])]
    jacobian = [
        [_raw_interval(value, path=f"jacobian[{row}][{column}]") for column, value in enumerate(values)]
        for row, values in enumerate(raw["jacobian_box"])
    ]
    defect = [
        [_raw_interval(value, path=f"defect[{row}][{column}]") for column, value in enumerate(values)]
        for row, values in enumerate(raw["preconditioned_jacobian_defect"])
    ]
    row_bounds = [
        _raw_interval(value, path=f"row_bounds[{index}]")
        for index, value in enumerate(raw["regularity_row_sum_bounds"])
    ]
    regularity_upper = max(_pair(value, path="row_bound")[1] for value in row_bounds)
    gates = copy.deepcopy(raw["gates"])
    if set(gates) != {
        "physical_domain",
        "inverse_nonsingular",
        "function_box_contains_zero",
        "krawczyk_strict_interior",
        "uniform_regularity",
    }:
        raise ValueError("uniform panel gate fields mismatch")
    box = {"radius": box_pairs[0], "theta": box_pairs[1]}
    strict = _image_in_box(image, box)
    regular = regularity_upper < 1
    if gates["krawczyk_strict_interior"] is not strict or gates[
        "uniform_regularity"
    ] is not regular:
        raise ValueError("uniform panel summary mismatch")
    passed = all(gates.values())
    if raw.get("pass") is not passed:
        raise ValueError("uniform panel pass mismatch")
    return {
        "precision_dps": precision,
        "scale_interval": list(SCALE_INTERVAL),
        "center": list(root),
        "box": box,
        "tail_bounds": copy.deepcopy(bounds),
        "jacobian_box": jacobian,
        "inverse_point_jacobian": copy.deepcopy(raw["inverse_point_jacobian"]),
        "preconditioned_jacobian_defect": defect,
        "regularity_row_sum_bounds": row_bounds,
        "regularity_infinity_norm_upper": format(regularity_upper, "f"),
        "krawczyk_image": image,
        "gates": gates,
        "pass": passed,
    }


def uniform_panel_backend_record(
    *, precision_dps: int, root: tuple[str, str], bounds: dict[str, Any]
) -> dict[str, Any]:
    """Evaluate the preregistered one-box tail homotopy panel."""

    raw = certify_rotating_wave_tail_homotopy_box(
        radius=root[0],
        theta=root[1],
        radius_half_width=HALF_WIDTH,
        theta_half_width=HALF_WIDTH,
        tail_scale_interval=SCALE_INTERVAL,
        parameters=INTERVAL_PARAMETERS,
        residual_tail_bound=bounds["residual_bound"],
        jacobian_radius_tail_bound=bounds["jacobian_radius_bound"],
        jacobian_theta_tail_bound=bounds["jacobian_theta_bound"],
        precision_dps=precision_dps,
    )
    return _panel_record(raw, precision=precision_dps, root=list(root), bounds=bounds)


def _endpoint_binding(sealed: dict[str, Any], panels: list[dict[str, Any] | None]) -> dict[str, bool]:
    complete = all(panel is not None for panel in panels)
    bridge_matches = sealed["bridge_root"] == sealed["g4_finite_root"]
    finite_in_box = bool(
        complete
        and all(_point_in_box(sealed["g4_finite_root"], panel["box"]) for panel in panels)
    )
    boxes_match = bool(
        complete
        and all(
            _boxes_equal(sealed["g4_tail_boxes"][index], panels[index]["box"])
            for index in range(2)
        )
    )
    images_in_box = bool(
        complete
        and all(
            _image_in_box(sealed["g4_tail_images"][index], panels[index]["box"])
            for index in range(2)
        )
    )
    values = {
        "bridge_endpoint_pass": sealed["bridge_endpoint_pass"] is True,
        "bridge_root_matches_g4": bridge_matches,
        "finite_root_in_uniform_box": finite_in_box,
        "g4_tail_boxes_match_uniform": boxes_match,
        "g4_tail_images_in_uniform_box": images_in_box,
    }
    return {**values, "pass": all(values.values())}


def run_contract(
    *,
    execution_commit: str,
    authorization: dict[str, Any],
    sealed_inputs: dict[str, Any] | None = None,
    panel_fn: Callable[..., dict[str, Any]] | None = None,
    created_utc: str | None = None,
) -> dict[str, Any]:
    """Compose the registered result without any adaptive retry."""

    sealed = copy.deepcopy(sealed_inputs or load_sealed_inputs())
    _validate_sealed_inputs(sealed)
    panel_fn = panel_fn or uniform_panel_backend_record
    root = tuple(sealed["g4_finite_root"])
    panels: list[dict[str, Any] | None] = [None, None]
    for index, precision in enumerate(PRECISIONS):
        try:
            panel = panel_fn(
                precision_dps=precision,
                root=root,
                bounds=copy.deepcopy(sealed["tail_bounds"][index]),
            )
        except ArithmeticError:
            break
        panels[index] = panel
        if not panel["pass"]:
            break
    intersection = None
    if all(panel is not None for panel in panels):
        intersection = _intersection(
            panels[0]["krawczyk_image"], panels[1]["krawczyk_image"]
        )
    overlap = intersection is not None
    endpoint = _endpoint_binding(sealed, panels)
    gates = {
        "U0": "pass",
        "U1": "pass",
        "U2": "pass" if all(panel is not None and panel["gates"]["krawczyk_strict_interior"] for panel in panels) else "inconclusive",
        "U3": "pass" if all(panel is not None and panel["gates"]["uniform_regularity"] for panel in panels) else "inconclusive",
        "U4": "pass" if endpoint["pass"] else "inconclusive",
        "U5": "pass" if overlap else "inconclusive",
    }
    decision = PASS_DECISION if all(value == "pass" for value in gates.values()) else INCONCLUSIVE_DECISION
    payload = {
        "identity": {
            "attempt": ATTEMPT,
            "schema": SCHEMA,
            "version": 4,
            "created_utc": created_utc or datetime.now(UTC).isoformat(),
            "execution_commit": execution_commit,
            "protocol_blob": _schema()["constants"]["protocol_blob"],
            "protocol_sha256": _schema()["constants"]["protocol_sha256"],
            "parameters": PARAMETERS,
            "authorization": copy.deepcopy(authorization),
        },
        "sealed_inputs": sealed,
        "model_identity": {
            "homotopy_family": "F_s=F_3600+s*T_3600",
            "scale_interval": list(SCALE_INTERVAL),
            "finite_endpoint": "F_3600",
            "infinite_endpoint": "F_infinity",
            "tail_bounds_replayed": True,
        },
        "homotopy": {
            "panels": panels,
            "intersection": intersection,
            "overlap": overlap,
            "endpoint_binding": endpoint,
        },
        "classification": {
            "gates": gates,
            "decision": decision,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "publication": {
            "artifacts": [
                {"path": RESULT.name, "role": "result-json"},
                {"path": REPORT.name, "role": "readable-report"},
            ],
            "auditor_output_path": AUDIT.relative_to(ROOT).as_posix(),
            "manifest_path": MANIFEST.name,
            "manifest_published_last": True,
        },
    }
    validate_payload(payload, sealed_reference=sealed)
    return payload


def _row_norm_upper(defect_row: Sequence[Sequence[str]], *, path: str) -> Fraction:
    terms = (
        max(abs(Fraction(lower)), abs(Fraction(upper)))
        for lower, upper in (
            _pair(value, path=f"{path}[{index}]")
            for index, value in enumerate(defect_row)
        )
    )
    return sum(terms, start=Fraction())


def validate_payload(
    payload: dict[str, Any], *, sealed_reference: dict[str, Any] | None = None
) -> None:
    """Validate schema plus every decision-bearing decimal relation."""

    contract = _schema()
    validate_contract(payload, contract)
    sealed = payload["sealed_inputs"]
    expected_sealed = sealed_reference or load_sealed_inputs()
    if sealed != expected_sealed:
        raise ValueError("$.sealed_inputs: extracted Git-blob snapshot mismatch")
    expected_files = [
        {"role": role, "path": relative, "sha256": digest}
        for role, relative, digest in SEALED_FILES
    ]
    if sealed["files"] != expected_files:
        raise ValueError("$.sealed_inputs.files: mismatch")
    if sealed["bridge_root"] != sealed["g4_finite_root"]:
        bridge_matches = False
    else:
        bridge_matches = True
    expected_bounds = [
        {
            "precision_dps": precision,
            **_transfer_gate().tail_bounds(horizon=3600, precision_dps=precision),
        }
        for precision in PRECISIONS
    ]
    if sealed["tail_bounds"] != expected_bounds:
        raise ValueError("$.sealed_inputs.tail_bounds: mismatch")

    panels = payload["homotopy"]["panels"]
    nonnull = 0
    for index, panel in enumerate(panels):
        if panel is None:
            continue
        if index != nonnull:
            raise ValueError("$.homotopy.panels: non-prefix panel")
        nonnull += 1
        if panel["precision_dps"] != PRECISIONS[index]:
            raise ValueError("$.homotopy.panels: precision mismatch")
        if panel["center"] != sealed["g4_finite_root"]:
            raise ValueError("$.homotopy.panels: center mismatch")
        if panel["tail_bounds"] != expected_bounds[index]:
            raise ValueError("$.homotopy.panels: tail-bound mismatch")
        for coordinate_index, coordinate in enumerate(("radius", "theta")):
            lower, upper = _pair(panel["box"][coordinate], path=f"panel.box.{coordinate}")
            center = _decimal(panel["center"][coordinate_index], path="panel.center")
            width = Decimal(HALF_WIDTH)
            with localcontext() as context:
                context.prec = 200
                expected_lower = center - width
                expected_upper = center + width
                tolerance = max(abs(center), Decimal(1)).scaleb(4 - PRECISIONS[index])
            if not (
                lower <= expected_lower
                and expected_upper <= upper
                and expected_lower - lower <= tolerance
                and upper - expected_upper <= tolerance
            ):
                raise ValueError("$.homotopy.panels: registered box mismatch")
        strict = _image_in_box(panel["krawczyk_image"], panel["box"])
        row_uppers = [
            _row_norm_upper(row, path=f"panel.defect[{row_index}]")
            for row_index, row in enumerate(panel["preconditioned_jacobian_defect"])
        ]
        recorded_rows = [
            _pair(value, path=f"panel.row_bounds[{row_index}]")
            for row_index, value in enumerate(panel["regularity_row_sum_bounds"])
        ]
        for observed, recorded in zip(row_uppers, recorded_rows, strict=True):
            if Fraction(recorded[1]) < observed:
                raise ValueError("$.homotopy.panels: inward regularity bound")
        regularity_upper = max(value[1] for value in recorded_rows)
        if _decimal(
            panel["regularity_infinity_norm_upper"], path="panel.regularity"
        ) != regularity_upper:
            raise ValueError("$.homotopy.panels: regularity summary mismatch")
        regular = regularity_upper < 1
        if panel["gates"]["krawczyk_strict_interior"] is not strict or panel[
            "gates"
        ]["uniform_regularity"] is not regular:
            raise ValueError("$.homotopy.panels: gate summary mismatch")
        if panel["pass"] is not all(panel["gates"].values()):
            raise ValueError("$.homotopy.panels: pass mismatch")

    expected_intersection = None
    if all(panel is not None for panel in panels):
        expected_intersection = _intersection(
            panels[0]["krawczyk_image"], panels[1]["krawczyk_image"]
        )
    if payload["homotopy"]["intersection"] != expected_intersection or payload[
        "homotopy"
    ]["overlap"] is not (expected_intersection is not None):
        raise ValueError("$.homotopy: overlap mismatch")
    expected_endpoint = _endpoint_binding(sealed, panels)
    if expected_endpoint["bridge_root_matches_g4"] is not bridge_matches or payload[
        "homotopy"
    ]["endpoint_binding"] != expected_endpoint:
        raise ValueError("$.homotopy.endpoint_binding: mismatch")
    expected_gates = {
        "U0": "pass",
        "U1": "pass",
        "U2": "pass" if all(panel is not None and panel["gates"]["krawczyk_strict_interior"] for panel in panels) else "inconclusive",
        "U3": "pass" if all(panel is not None and panel["gates"]["uniform_regularity"] for panel in panels) else "inconclusive",
        "U4": "pass" if expected_endpoint["pass"] else "inconclusive",
        "U5": "pass" if expected_intersection is not None else "inconclusive",
    }
    expected_decision = PASS_DECISION if all(value == "pass" for value in expected_gates.values()) else INCONCLUSIVE_DECISION
    if payload["classification"] != {
        "gates": expected_gates,
        "decision": expected_decision,
        "claim_boundary": CLAIM_BOUNDARY,
    }:
        raise ValueError("$.classification: reconstruction mismatch")
    expected_publication = {
        "artifacts": [
            {"path": RESULT.name, "role": "result-json"},
            {"path": REPORT.name, "role": "readable-report"},
        ],
        "auditor_output_path": AUDIT.relative_to(ROOT).as_posix(),
        "manifest_path": MANIFEST.name,
        "manifest_published_last": True,
    }
    if payload["publication"] != expected_publication:
        raise ValueError("$.publication: mismatch")


def render_report(payload: dict[str, Any]) -> str:
    panels = payload["homotopy"]["panels"]
    lines = [
        "# Uniform H=3600 to infinity branch-link result",
        "",
        f"Decision: **`{payload['classification']['decision']}`**.",
        "",
        "## Registered measurement",
        "",
        "- homotopy: `F_s=F_3600+s*T_3600`, `s in [0,1]`",
        f"- completed panels: `{sum(panel is not None for panel in panels)}/2`",
        f"- cross-precision overlap: `{payload['homotopy']['overlap']}`",
        f"- endpoint binding: `{payload['homotopy']['endpoint_binding']['pass']}`",
    ]
    for panel in panels:
        if panel is not None:
            lines.append(
                f"- {panel['precision_dps']}-dps regularity upper bound: "
                f"`{panel['regularity_infinity_norm_upper']}`"
            )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            payload["classification"]["claim_boundary"] + ".",
            "",
            "The standard-library audit checks records, decimal relations and",
            "hashes; it is not a second interval backend.",
            "",
        ]
    )
    return "\n".join(lines)


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(content)
    os.replace(temporary, path)


def publish(
    payload: dict[str, Any], *, audit_fn: Callable[[bytes, bytes], dict[str, Any]]
) -> None:
    """Publish result, report, independent audit, then the manifest last."""

    validate_payload(payload)
    paths = (RESULT, REPORT, AUDIT, MANIFEST)
    existing = [path for path in paths if path.exists()]
    if existing:
        raise FileExistsError(f"refusing to overwrite publication: {existing[0]}")
    result_bytes = (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")
    report_bytes = render_report(payload).encode("utf-8")
    audit_payload = audit_fn(result_bytes, report_bytes)
    audit_bytes = (
        json.dumps(audit_payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")
    _atomic_write(RESULT, result_bytes)
    _atomic_write(REPORT, report_bytes)
    _atomic_write(AUDIT, audit_bytes)
    artifacts = [
        {"path": RESULT.name, "role": "result-json", "sha256": hashlib.sha256(result_bytes).hexdigest()},
        {"path": REPORT.name, "role": "readable-report", "sha256": hashlib.sha256(report_bytes).hexdigest()},
        {"path": AUDIT.relative_to(ROOT).as_posix(), "role": "independent-audit", "sha256": hashlib.sha256(audit_bytes).hexdigest()},
    ]
    manifest = {
        "schema": "scalar-memory-rotating-wave-horizon-infinity-branch-link-publication-v1",
        "execution_commit": payload["identity"]["execution_commit"],
        "protocol_sha256": payload["identity"]["protocol_sha256"],
        "artifacts": artifacts,
    }
    _atomic_write(
        MANIFEST,
        (json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n").encode(
            "utf-8"
        ),
    )
