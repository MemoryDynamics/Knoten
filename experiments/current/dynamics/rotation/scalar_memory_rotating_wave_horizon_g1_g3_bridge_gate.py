"""Fail-closed contract core for the registered G1--G3 horizon bridge.

This module contains no target execution and writes no result artifact.  It
validates primitive finite-branch evidence and the hash-bound composition with
the sealed G4/G5 components.
"""

from __future__ import annotations

import copy
from decimal import Decimal, localcontext
from functools import cache
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Sequence

from emergenz_knoten.strict_json_contract import validate_payload as validate_contract


ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_g1_g3_bridge_result_schema_v1.json"
)
TRANSFER_GATE_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_transfer_gate.py"
)
HORIZONS = (600, 900, 1200, 1500, 1800, 2400, 3600)
FORWARD_HORIZONS = (1200, 1500, 1800, 2400, 3600)
LOWER_HORIZONS = (900, 600)
REPLAY_DPS = 70
REPLAY_RESIDUAL_MAXIMUM = Decimal("1e-45")
REPLAY_SEMANTICS = "independent finite-sum replay; not a second interval proof"
PARAMETERS = {
    "alpha": 0.01,
    "amplitude_att": 3.5,
    "amplitude_rep": 1.0,
    "anchor_radius": 0.946517504804225,
    "anchor_theta": 0.015770381717135,
    "epsilon": 0.0,
    "eta": 0.15,
    "memory_mass": 1.0,
    "q": 0.99,
    "sigma_att": 3.0,
    "sigma_rep": 1.0,
}
SEALED_FILES = (
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
        "366d221e6d14093da48f7a8f4ea1a439d4b26e5635b65c95bcb763bc968a2aa5",
    ),
    (
        "g5-result",
        "reports/dynamics/rotation/"
        "scalar_memory_rotating_wave_horizon_g5_component_attempt_3_2026-09-17.json",
        "3321ee6392a6eb2a3c5098fa437cb41bb57b9da7e1c0ada521bdd1e894f4ec39",
    ),
    (
        "g5-manifest",
        "reports/dynamics/rotation/"
        "scalar_memory_rotating_wave_horizon_g5_component_attempt_3_2026-09-17.publication.json",
        "62ed914737028678be360633f4c97b8cb28cd0ef9fae6e7077684fa272a9df8e",
    ),
)


@cache
def _transfer_gate() -> Any:
    """Load the already reviewed v3 finite-branch semantic validator."""

    spec = importlib.util.spec_from_file_location(
        "g1_g3_reused_horizon_transfer_gate", TRANSFER_GATE_PATH
    )
    if spec is None or spec.loader is None:
        raise ImportError("cannot load registered horizon-transfer gate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_sealed_components(*, root: Path = ROOT) -> dict[str, Any]:
    """Hash and minimally extract the registered G4/G5 endpoint evidence."""

    repository = Path(root).resolve()
    documents: dict[str, dict[str, Any]] = {}
    files = []
    for role, relative, expected_sha256 in SEALED_FILES:
        path = (repository / relative).resolve()
        if repository not in path.parents:
            raise ValueError("sealed component path escaped repository")
        raw = path.read_bytes()
        observed = hashlib.sha256(raw).hexdigest()
        if observed != expected_sha256:
            raise ValueError(f"sealed component hash mismatch: {role}")
        files.append({"role": role, "path": relative, "sha256": observed})
        if role in {"g4-result", "g4-manifest", "g4-audit", "g5-result", "g5-manifest"}:
            parsed = json.loads(raw)
            if type(parsed) is not dict:
                raise TypeError(f"sealed component root is not an object: {role}")
            documents[role] = parsed

    g4 = documents["g4-result"]
    g5 = documents["g5-result"]
    g4_manifest = documents["g4-manifest"]
    g5_manifest = documents["g5-manifest"]
    g4_audit = documents["g4-audit"]
    if (
        g4["identity"]["schema"]
        != "scalar-memory-rotating-wave-horizon-g4-component-v1"
        or g4["classification"]["decision"] != "g4-local-infinite-root-pass"
        or g4_audit["verdict"] != "g4-independent-audit-agrees"
        or g5["identity"]["schema"]
        != "scalar-memory-rotating-wave-horizon-g5-component-v2"
        or g5["classification"]["decision"] != "g5-local-direct-stability-pass"
    ):
        raise ValueError("sealed component decision or schema mismatch")
    expected_manifest_rows = {
        "g4-manifest": (Path(SEALED_FILES[0][1]).name, SEALED_FILES[0][2]),
        "g5-manifest": (Path(SEALED_FILES[3][1]).name, SEALED_FILES[3][2]),
    }
    for role, manifest in (
        ("g4-manifest", g4_manifest),
        ("g5-manifest", g5_manifest),
    ):
        name, digest = expected_manifest_rows[role]
        rows = manifest["artifacts"]
        if not any(
            row.get("role") == "result-json"
            and row.get("path") == name
            and row.get("sha256") == digest
            for row in rows
        ):
            raise ValueError(f"sealed manifest does not bind result: {role}")
    if g4_audit.get("result_sha256") != SEALED_FILES[0][2]:
        raise ValueError("sealed G4 audit does not bind registered result")

    expected_g4_parameters = {
        "alpha": 0.01,
        "amplitude_att": 3.5,
        "amplitude_rep": 1.0,
        "eta": 0.15,
        "horizon": 3600,
        "memory_mass": 1.0,
        "sigma_att": 3.0,
        "sigma_rep": 1.0,
    }
    expected_g5_parameters = {
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
    if g4["identity"]["parameters"] != expected_g4_parameters:
        raise ValueError("sealed G4 parameter mismatch")
    if g5["identity"]["parameters"] != expected_g5_parameters:
        raise ValueError("sealed G5 parameter mismatch")

    def root_record(
        document: dict[str, Any], *, horizon: int, decision: str
    ) -> dict[str, Any]:
        finite = document["finite_root"]
        if not (
            finite["inner_certificate"]["strict_interior"]
            and finite["outer_certificate"]["strict_interior"]
        ):
            raise ValueError("sealed component root certificate is not strict")
        return {
            "decision": decision,
            "horizon": horizon,
            "inner_image": copy.deepcopy(
                finite["inner_certificate"]["krawczyk_image"]
            ),
            "outer_box": copy.deepcopy(finite["outer_certificate"]["box"]),
        }

    result = {
        "files": files,
        "g4_root": root_record(
            g4, horizon=3600, decision="g4-local-infinite-root-pass"
        ),
        "g5_root": root_record(
            g5, horizon=2400, decision="g5-local-direct-stability-pass"
        ),
    }
    _sealed_files({"sealed_components": result})
    return result


def _load_schema() -> dict[str, Any]:
    payload = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if type(payload) is not dict:
        raise TypeError("bridge schema root must be an object")
    return payload


def _finite_decimal(value: str, *, path: str) -> Decimal:
    if type(value) is not str:
        raise TypeError(f"{path}: expected decimal string")
    parsed = Decimal(value)
    if not parsed.is_finite():
        raise ValueError(f"{path}: decimal must be finite")
    return parsed


def _pair(values: Sequence[str], *, path: str) -> tuple[Decimal, Decimal]:
    if type(values) is not list or len(values) != 2:
        raise TypeError(f"{path}: expected decimal pair")
    lower = _finite_decimal(values[0], path=f"{path}[0]")
    upper = _finite_decimal(values[1], path=f"{path}[1]")
    if lower > upper:
        raise ValueError(f"{path}: reversed interval")
    return lower, upper


def _pair_contains(
    container: Sequence[str], subject: Sequence[str], *, path: str
) -> bool:
    container_lower, container_upper = _pair(container, path=f"{path}.container")
    subject_lower, subject_upper = _pair(subject, path=f"{path}.subject")
    return container_lower <= subject_lower and subject_upper <= container_upper


def _image_in_box(
    image: Sequence[Sequence[str]], box: dict[str, Sequence[str]], *, path: str
) -> bool:
    if type(image) is not list or len(image) != 2:
        raise TypeError(f"{path}.image: expected two-dimensional image")
    if type(box) is not dict or set(box) != {"radius", "theta"}:
        raise TypeError(f"{path}.box: expected root box")
    return bool(
        _pair_contains(box["radius"], image[0], path=f"{path}.radius")
        and _pair_contains(box["theta"], image[1], path=f"{path}.theta")
    )


def _validate_root_panel(panel: dict[str, Any], *, path: str) -> bool:
    cross_80 = _image_in_box(
        panel["inner_certificate_80"]["krawczyk_image"],
        panel["outer_certificate_120"]["box"],
        path=f"{path}.cross_80_inner_in_120_outer",
    )
    cross_120 = _image_in_box(
        panel["inner_certificate_120"]["krawczyk_image"],
        panel["outer_certificate_80"]["box"],
        path=f"{path}.cross_120_inner_in_80_outer",
    )
    if panel["cross_80_inner_in_120_outer"] is not cross_80:
        raise ValueError(f"{path}: 80-to-120 cross inclusion mismatch")
    if panel["cross_120_inner_in_80_outer"] is not cross_120:
        raise ValueError(f"{path}: 120-to-80 cross inclusion mismatch")
    return bool(
        panel["centers_agree"]
        and cross_80
        and cross_120
        and panel["inner_certificate_80"]["strict_interior"]
        and panel["inner_certificate_120"]["strict_interior"]
        and panel["outer_certificate_80"]["strict_interior"]
        and panel["outer_certificate_120"]["strict_interior"]
    )


def _validate_endpoint_link(
    link: dict[str, Any], panel: dict[str, Any], *, path: str
) -> bool:
    reconstructed = {
        "bridge_80_inner_in_component_outer": _image_in_box(
            panel["inner_certificate_80"]["krawczyk_image"],
            link["component_outer_box"],
            path=f"{path}.bridge_80",
        ),
        "bridge_120_inner_in_component_outer": _image_in_box(
            panel["inner_certificate_120"]["krawczyk_image"],
            link["component_outer_box"],
            path=f"{path}.bridge_120",
        ),
        "component_inner_in_bridge_80_outer": _image_in_box(
            link["component_inner_image"],
            panel["outer_certificate_80"]["box"],
            path=f"{path}.component_to_80",
        ),
        "component_inner_in_bridge_120_outer": _image_in_box(
            link["component_inner_image"],
            panel["outer_certificate_120"]["box"],
            path=f"{path}.component_to_120",
        ),
    }
    for name, value in reconstructed.items():
        if link[name] is not value:
            raise ValueError(f"{path}: endpoint {name} mismatch")
    passed = all(reconstructed.values())
    if link["pass"] is not passed:
        raise ValueError(f"{path}: endpoint pass mismatch")
    return passed


def classify_bridge(gates: dict[str, Any]) -> dict[str, Any]:
    """Apply the preregistered bridge decision precedence."""

    if gates["G0"] == "fail" or gates["G6"] == "fail":
        return {"decision": "g1-g3-bridge-experiment-invalid", "precedence_rank": 1}
    if gates["local_branch_excluded"]:
        return {
            "decision": "registered-local-horizon-branch-loss",
            "precedence_rank": 2,
        }
    if (
        gates["G0"] != "pass"
        or gates["G1F"] != "pass"
        or gates["G2F"] != "pass"
    ):
        return {"decision": "g1-g3-bridge-inconclusive", "precedence_rank": 3}
    if gates["G3"] == "fail":
        return {
            "decision": "rotating-wave-horizon-branch-drift",
            "precedence_rank": 4,
        }
    if gates["G3"] != "pass" or gates["G4"] != "pass" or gates["G5"] != "pass":
        return {"decision": "g1-g3-bridge-inconclusive", "precedence_rank": 3}
    if gates["H2400_link"] == "fail" or gates["H3600_link"] == "fail":
        return {
            "decision": "sealed-component-endpoint-mismatch",
            "precedence_rank": 5,
        }
    if gates["H2400_link"] != "pass" or gates["H3600_link"] != "pass":
        return {"decision": "g1-g3-bridge-inconclusive", "precedence_rank": 3}
    return {
        "decision": (
            "rotating-wave-root-branch-connected-with-h2400-"
            "local-stability-support"
        ),
        "precedence_rank": 6,
    }


def _sealed_files(payload: dict[str, Any]) -> None:
    expected = [
        {"role": role, "path": path, "sha256": digest}
        for role, path, digest in SEALED_FILES
    ]
    if payload["sealed_components"]["files"] != expected:
        raise ValueError("$.sealed_components.files: sealed artifact mismatch")
    g4 = payload["sealed_components"]["g4_root"]
    g5 = payload["sealed_components"]["g5_root"]
    if (
        g4["horizon"] != 3600
        or g4["decision"] != "g4-local-infinite-root-pass"
        or g5["horizon"] != 2400
        or g5["decision"] != "g5-local-direct-stability-pass"
    ):
        raise ValueError("$.sealed_components: sealed decision mismatch")


def _reconstructed_gates(payload: dict[str, Any]) -> dict[str, Any]:
    branch = payload["finite_branch"]
    panels = branch["root_panels"]
    panel_pass = [
        panel is not None
        and _validate_root_panel(panel, path=f"$.finite_branch.root_panels[{index}]")
        for index, panel in enumerate(panels)
    ]
    homotopies = branch["homotopies"]
    replays = branch["direct_replays"]
    g1f = all(panel_pass[index] for index in range(2, 7))
    g1r = all(
        panel_pass[index]
        and replays[index] is not None
        and replays[index]["pass"]
        for index in (2, 1, 0)
    )
    g2f = all(
        row is not None and row["status"] == "pass" and row["pass"]
        for row in homotopies[:4]
    )
    g2r = all(
        row is not None and row["status"] == "pass" and row["pass"]
        for row in homotopies[4:]
    )
    drift_rows = branch["drift"]["interval_upper_bounds"]
    drift_complete = all(row is not None for row in drift_rows)
    links = payload["endpoint_links"]
    link_states: list[str] = []
    for index, (link, horizon) in enumerate(zip(links, (2400, 3600), strict=True)):
        panel = panels[HORIZONS.index(horizon)]
        if link is None or panel is None:
            link_states.append("inconclusive")
            continue
        if link["horizon"] != horizon:
            raise ValueError(f"$.endpoint_links[{index}]: endpoint horizon mismatch")
        link_states.append(
            "pass"
            if _validate_endpoint_link(
                link, panel, path=f"$.endpoint_links[{index}]"
            )
            else "fail"
        )
    local_branch_excluded = any(
        row is not None and row["status"] == "all-residual-excluded"
        for row in branch["exclusions"]
    )
    q_pass = all(
        row["two_ulp_gate"] and row["nonzero_finite"]
        for row in payload["q_representations"]
    )
    forward_replays = [replays[index] for index in range(2, 7)]
    if not q_pass or any(
        row is not None and not row["pass"] for row in forward_replays
    ):
        g0 = "fail"
    elif all(row is not None and row["pass"] for row in forward_replays):
        g0 = "pass"
    else:
        g0 = "inconclusive"
    return {
        "G0": g0,
        "G1F": "pass" if g1f else "inconclusive",
        "G1R": "pass" if g1r else "inconclusive",
        "G2F": "pass" if g2f else "inconclusive",
        "G2R": "pass" if g2r else "inconclusive",
        "G3": (
            "pass"
            if drift_complete and branch["drift"]["pass"]
            else "fail" if drift_complete else "inconclusive"
        ),
        "G4": "pass",
        "G5": "pass",
        "G6": "pass" if _controls_evidence(payload) else "fail",
        "H2400_link": link_states[0],
        "H3600_link": link_states[1],
        "local_branch_excluded": local_branch_excluded,
    }


def _verify_replays(payload: dict[str, Any]) -> None:
    branch = payload["finite_branch"]
    panels = branch["root_panels"]
    replays = branch["direct_replays"]
    for index, (panel, row, horizon) in enumerate(
        zip(panels, replays, HORIZONS, strict=True)
    ):
        path = f"$.finite_branch.direct_replays[{index}]"
        if panel is None:
            if row is not None:
                raise ValueError(f"{path}: replay without root panel")
            continue
        if row is None:
            continue
        if row["horizon"] != horizon or row["precision_dps"] != REPLAY_DPS:
            raise ValueError(f"{path}: registered horizon or precision mismatch")
        root = panel["newton_120"]
        if row["radius"] != root["radius"] or row["theta"] != root["theta"]:
            raise ValueError(f"{path}: replay center does not match 120-dps root")
        if row["semantics"] != REPLAY_SEMANTICS:
            raise ValueError(f"{path}: replay semantics mismatch")
        radial = _finite_decimal(row["radial_residual"], path=f"{path}.radial_residual")
        tangential = _finite_decimal(
            row["tangential_residual"], path=f"{path}.tangential_residual"
        )
        residual_maximum = _finite_decimal(
            row["residual_maximum"], path=f"{path}.residual_maximum"
        )
        radial_sum = _finite_decimal(row["radial_sum"], path=f"{path}.radial_sum")
        tangential_sum = _finite_decimal(
            row["tangential_sum"], path=f"{path}.tangential_sum"
        )
        expected_maximum = max(abs(radial), abs(tangential))
        if residual_maximum != expected_maximum:
            raise ValueError(f"{path}: residual maximum mismatch")
        residual_gate = residual_maximum <= REPLAY_RESIDUAL_MAXIMUM
        physical_signs = radial_sum > 0 and tangential_sum < 0
        if row["residual_gate"] is not residual_gate:
            raise ValueError(f"{path}: residual gate mismatch")
        if row["physical_signs"] is not physical_signs:
            raise ValueError(f"{path}: physical-sign gate mismatch")
        if row["pass"] is not (residual_gate and physical_signs):
            raise ValueError(f"{path}: replay pass mismatch")
    expected_summary = all(
        replays[index] is not None and replays[index]["pass"]
        for index in range(2, 7)
    )
    if branch["direct_replay_pass"] is not expected_summary:
        raise ValueError("$.finite_branch.direct_replay_pass: reconstruction mismatch")


def _controls_evidence(payload: dict[str, Any]) -> bool:
    controls = payload["controls"]
    expected_cases = [
        ("noncircle-H17", 17),
        ("noncircle-H257", 257),
        *((f"anchor-H{horizon}", horizon) for horizon in HORIZONS),
    ]
    circular = controls["circular_cases"]
    circular_pass = True
    for row, (case_id, horizon) in zip(circular, expected_cases, strict=True):
        expected = bool(
            row["case_id"] == case_id
            and row["horizon"] == horizon
            and row["expected_age_history_sha256"]
            == row["observed_age_history_sha256"]
            and row["new_point_relative_error"] < 5e-14
            and row["complete_state_relative_error"] < 5e-14
        )
        if row["pass"] is not expected:
            raise ValueError("$.controls.circular_cases: pass reconstruction mismatch")
        circular_pass = circular_pass and expected
    eta_pass = True
    for row, horizon in zip(controls["eta_zero_cases"], HORIZONS, strict=True):
        expected = bool(
            row["horizon"] == horizon
            and row["steps"] == horizon + 1
            and row["maximum_deviation"] < 1e-14
        )
        if row["pass"] is not expected:
            raise ValueError("$.controls.eta_zero_cases: pass reconstruction mismatch")
        eta_pass = eta_pass and expected
    mutation_names = (
        "reverse-modulo",
        "overwrite-before-read",
        "wrong-oldest-slot",
    )
    mutation_pass = True
    for row, name in zip(controls["mutations"], mutation_names, strict=True):
        detected = bool(
            row["horizon"] == 17
            and row["name"] == name
            and (
                row["new_point_relative_error"] >= 5e-14
                or row["complete_state_relative_error"] >= 5e-14
            )
        )
        if row["detected"] is not detected:
            raise ValueError("$.controls.mutations: detection reconstruction mismatch")
        mutation_pass = mutation_pass and detected
    return bool(circular_pass and eta_pass and mutation_pass)


def validate_result(payload: dict[str, Any]) -> None:
    """Validate schema plus all decision-relevant semantic relationships."""

    contract = _load_schema()
    validate_contract(payload, contract)
    if payload["identity"]["parameters"] != PARAMETERS:
        raise ValueError("$.identity.parameters: registered parameters mismatch")
    publication = payload["publication"]
    if [row["role"] for row in publication["artifacts"]] != [
        "result-json",
        "readable-report",
    ]:
        raise ValueError("$.publication.artifacts: role order mismatch")
    if publication["manifest_published_last"] is not True:
        raise ValueError("$.publication.manifest_published_last: must be true")
    publication_paths = [
        *(row["path"] for row in publication["artifacts"]),
        publication["auditor_output_path"],
        publication["manifest_path"],
    ]
    if len(set(publication_paths)) != 4:
        raise ValueError("$.publication: paths must be distinct")
    _sealed_files(payload)
    if payload["finite_branch"]["horizons"] != list(HORIZONS):
        raise ValueError("$.finite_branch.horizons: order mismatch")
    root_panels = payload["finite_branch"]["root_panels"]
    for index, panel in enumerate(root_panels):
        if panel is not None and panel["horizon"] != HORIZONS[index]:
            raise ValueError("$.finite_branch.root_panels: horizon order mismatch")
    legacy_panels = []
    for panel in root_panels:
        if panel is None:
            legacy_panels.append(None)
            continue
        legacy = copy.deepcopy(panel)
        legacy.pop("cross_80_inner_in_120_outer")
        legacy.pop("cross_120_inner_in_80_outer")
        legacy_panels.append(legacy)
    reused = _transfer_gate()
    reused._verify_root_slots(legacy_panels)
    for index, panel in enumerate(legacy_panels):
        if panel is not None:
            reused._verify_root_panel(
                panel, path=f"$.finite_branch.root_panels[{index}]"
            )
    reused._verify_homotopy_slots(
        payload["finite_branch"]["homotopies"], legacy_panels
    )
    _verify_replays(payload)
    if payload["q_representations"] != reused.q_representations(HORIZONS):
        raise ValueError("$.q_representations: reconstruction mismatch")
    drift = payload["finite_branch"]["drift"]
    drift_rows = drift["interval_upper_bounds"]
    if drift["center_diagnostics"] != drift_rows:
        raise ValueError(
            "$.finite_branch.drift.center_diagnostics: reconstruction mismatch"
        )
    root_boxes = {
        panel["horizon"]: panel["inner_intersection"]
        for panel in legacy_panels
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
        radius_component, theta_component = reused._interval_drift_components(
            root_boxes[first_horizon],
            root_boxes[second_horizon],
            radius_scale=PARAMETERS["anchor_radius"],
            theta_scale=PARAMETERS["anchor_theta"],
        )
        expected_row = {
            "from_horizon": first_horizon,
            "radius_component": radius_component,
            "theta_component": theta_component,
            "to_horizon": second_horizon,
            "upper_bound": max(radius_component, theta_component),
        }
        if row != expected_row:
            raise ValueError(
                f"$.finite_branch.drift.interval_upper_bounds[{index}]: "
                "drift reconstruction mismatch"
            )
    expected_drift_pass = bool(
        all(row is not None for row in drift_rows)
        and reused.drift_gates(
            previous_upper=drift_rows[0]["upper_bound"],
            final_upper=drift_rows[1]["upper_bound"],
        )["pass"]
    )
    if drift["pass"] is not expected_drift_pass:
        raise ValueError("$.finite_branch.drift.pass: drift reconstruction mismatch")
    controls_pass = _controls_evidence(payload)
    if payload["controls"]["pass"] is not controls_pass:
        raise ValueError("$.controls.pass: controls reconstruction mismatch")
    reconstructed = _reconstructed_gates(payload)
    stored = payload["classification"]["gates"]
    if stored != reconstructed:
        raise ValueError("$.classification.gates: reconstruction mismatch")
    reused._verify_exclusions(
        payload["finite_branch"]["exclusions"],
        local_branch_excluded=reconstructed["local_branch_excluded"],
        root_panels=legacy_panels,
    )
    expected_lower = (
        "lower-tail-stress-pass"
        if reconstructed["G1R"] == reconstructed["G2R"] == "pass"
        else "lower-tail-stress-inconclusive"
    )
    if payload["finite_branch"]["lower_tail_status"] != expected_lower:
        raise ValueError("$.finite_branch.lower_tail_status: reconstruction mismatch")
    if payload["classification"]["lower_tail_status"] != expected_lower:
        raise ValueError("$.classification.lower_tail_status: reconstruction mismatch")
    expected = classify_bridge(reconstructed)
    if payload["classification"]["decision"] != expected["decision"]:
        raise ValueError("$.classification.decision: reconstruction mismatch")
    if payload["classification"]["precedence_rank"] != expected["precedence_rank"]:
        raise ValueError("$.classification.precedence_rank: reconstruction mismatch")


def _root_coordinates(
    panel: dict[str, Any], precision_dps: int
) -> tuple[str, str]:
    newton = panel[f"newton_{precision_dps}"]
    return newton["radius"], newton["theta"]


def _bridge_root_panel(
    horizon: int, precision_records: dict[int, dict[str, Any]]
) -> dict[str, Any]:
    """Add cross-precision identity checks to the reviewed v3 root panel."""

    panel = _transfer_gate()._combine_root_panel(horizon, precision_records)
    panel["cross_80_inner_in_120_outer"] = _image_in_box(
        panel["inner_certificate_80"]["krawczyk_image"],
        panel["outer_certificate_120"]["box"],
        path=f"orchestration.root[{horizon}].cross_80_to_120",
    )
    panel["cross_120_inner_in_80_outer"] = _image_in_box(
        panel["inner_certificate_120"]["krawczyk_image"],
        panel["outer_certificate_80"]["box"],
        path=f"orchestration.root[{horizon}].cross_120_to_80",
    )
    return panel


def _endpoint_link(
    *,
    component: str,
    component_root: dict[str, Any],
    panel: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if panel is None:
        return None
    outer_box = copy.deepcopy(component_root["outer_box"])
    inner_image = copy.deepcopy(component_root["inner_image"])
    link = {
        "bridge_120_inner_in_component_outer": _image_in_box(
            panel["inner_certificate_120"]["krawczyk_image"],
            outer_box,
            path=f"orchestration.endpoint.{component}.bridge_120",
        ),
        "bridge_80_inner_in_component_outer": _image_in_box(
            panel["inner_certificate_80"]["krawczyk_image"],
            outer_box,
            path=f"orchestration.endpoint.{component}.bridge_80",
        ),
        "component": component,
        "component_inner_image": inner_image,
        "component_inner_in_bridge_120_outer": _image_in_box(
            inner_image,
            panel["outer_certificate_120"]["box"],
            path=f"orchestration.endpoint.{component}.component_to_120",
        ),
        "component_inner_in_bridge_80_outer": _image_in_box(
            inner_image,
            panel["outer_certificate_80"]["box"],
            path=f"orchestration.endpoint.{component}.component_to_80",
        ),
        "component_outer_box": outer_box,
        "horizon": component_root["horizon"],
    }
    link["pass"] = all(
        link[name]
        for name in (
            "bridge_120_inner_in_component_outer",
            "bridge_80_inner_in_component_outer",
            "component_inner_in_bridge_120_outer",
            "component_inner_in_bridge_80_outer",
        )
    )
    return link


def registered_controls_backend_record() -> dict[str, Any]:
    """Run the preregistered finite-memory implementation controls."""

    reused = _transfer_gate()
    np = reused.np
    parameters = {
        name: PARAMETERS[name]
        for name in (
            "alpha",
            "memory_mass",
            "eta",
            "sigma_rep",
            "sigma_att",
            "amplitude_rep",
            "amplitude_att",
        )
    }
    histories: list[tuple[str, int, Any]] = []
    for horizon in (17, 257):
        ages = np.arange(horizon, dtype=float)
        history = np.column_stack(
            (
                np.sin(0.17 * ages) + 0.03 * ages,
                np.cos(0.11 * ages) - 0.02 * ages,
            )
        )
        histories.append((f"noncircle-H{horizon}", horizon, history))
    for horizon in HORIZONS:
        history = reused.circular_history(
            radius=PARAMETERS["anchor_radius"],
            theta=PARAMETERS["anchor_theta"],
            horizon=horizon,
        )
        histories.append((f"anchor-H{horizon}", horizon, history))

    circular_cases = []
    for case_id, horizon, history in histories:
        expected_hash = hashlib.sha256(
            np.ascontiguousarray(history).tobytes()
        ).hexdigest()
        observed = reused.run_circular_control(history, parameters=parameters)
        circular_cases.append(
            {
                "case_id": case_id,
                "complete_state_relative_error": observed[
                    "complete_state_relative_error"
                ],
                "expected_age_history_sha256": expected_hash,
                "horizon": horizon,
                "new_point_relative_error": observed["new_point_relative_error"],
                "observed_age_history_sha256": observed["age_history_sha256"],
                "pass": observed["pass"],
            }
        )

    eta_zero_cases = []
    for horizon in HORIZONS:
        history = reused.circular_history(
            radius=PARAMETERS["anchor_radius"],
            theta=PARAMETERS["anchor_theta"],
            horizon=horizon,
        )
        collapsed = reused.eta_zero_collapse(history, steps=horizon + 1)
        expected = np.repeat(history[[0]], horizon, axis=0)
        maximum_deviation = float(np.max(np.abs(collapsed - expected)))
        eta_zero_cases.append(
            {
                "horizon": horizon,
                "maximum_deviation": maximum_deviation,
                "pass": maximum_deviation < 1e-14,
                "steps": horizon + 1,
            }
        )

    ages = np.arange(17, dtype=float)
    mutation_history = np.column_stack(
        (0.025 * ages + 0.003 * ages**2, 0.4 * np.sin(0.09 * ages))
    )
    mutations = []
    for name in (
        "reverse-modulo",
        "overwrite-before-read",
        "wrong-oldest-slot",
    ):
        observed = reused.run_circular_control(
            mutation_history, parameters=parameters, mutation=name
        )
        mutations.append(
            {
                "complete_state_relative_error": observed[
                    "complete_state_relative_error"
                ],
                "detected": not observed["pass"],
                "horizon": 17,
                "name": name,
                "new_point_relative_error": observed["new_point_relative_error"],
            }
        )
    controls = {
        "circular_cases": circular_cases,
        "eta_zero_cases": eta_zero_cases,
        "mutations": mutations,
        "pass": False,
    }
    controls["pass"] = _controls_evidence({"controls": controls})
    return controls


class RegisteredBridgeBackend:
    """Thin adapter over the reviewed primitive finite-memory backends."""

    def finite_root_panel(self, **kwargs: Any) -> dict[str, Any] | None:
        return _transfer_gate().finite_root_backend_record(**kwargs)

    def finite_sum_replay(self, **kwargs: Any) -> dict[str, Any]:
        return _transfer_gate().finite_sum_replay_backend_record(**kwargs)

    def homotopy_edge(self, **kwargs: Any) -> dict[str, Any]:
        return _transfer_gate().homotopy_backend_record(**kwargs)

    def local_branch_exclusion(self, **kwargs: Any) -> dict[str, Any]:
        return _transfer_gate().local_branch_exclusion_backend_record(**kwargs)

    def controls(self) -> dict[str, Any]:
        return registered_controls_backend_record()


def orchestrate_bridge(
    *,
    backend: Any,
    identity: dict[str, Any],
    publication: dict[str, Any],
    sealed_components: dict[str, Any],
) -> dict[str, Any]:
    """Compose G1--G3 evidence without rerunning sealed G4 or G5 stages.

    The injected backend owns only primitive finite-root, homotopy, exclusion,
    replay and control operations.  Missing evidence closes every dependent
    prefix.  This function neither publishes files nor calls tail/stability
    backends.
    """

    reused = _transfer_gate()
    execution_order = (1200, 1500, 1800, 2400, 3600, 900, 600)
    homotopy_edges = (
        (1200, 1500, "forward"),
        (1500, 1800, "forward"),
        (1800, 2400, "forward"),
        (2400, 3600, "forward"),
        (1200, 900, "lower-tail"),
        (900, 600, "lower-tail"),
    )
    index_by_horizon = {horizon: index for index, horizon in enumerate(HORIZONS)}
    root_panels: list[dict[str, Any] | None] = [None] * len(HORIZONS)
    starts = {
        precision: (
            str(identity["parameters"]["anchor_radius"]),
            str(identity["parameters"]["anchor_theta"]),
        )
        for precision in (80, 120)
    }
    exclusions: list[dict[str, Any] | None] = [None] * 4
    forward_open = True
    lower_open = True

    for horizon in execution_order:
        forward = horizon in FORWARD_HORIZONS
        if horizon != 1200 and (
            (forward and not forward_open) or (not forward and not lower_open)
        ):
            continue
        if horizon == 900:
            anchor = root_panels[index_by_horizon[1200]]
            if anchor is None:
                lower_open = False
                continue
            starts = {
                precision: _root_coordinates(anchor, precision)
                for precision in (80, 120)
            }
        records: dict[int, dict[str, Any]] = {}
        for precision in (80, 120):
            record = backend.finite_root_panel(
                horizon=horizon,
                precision_dps=precision,
                start=starts[precision],
            )
            if record is None:
                break
            records[precision] = record
        if len(records) != 2:
            if forward and horizon != 1200:
                previous = execution_order[execution_order.index(horizon) - 1]
                exclusions[(1500, 1800, 2400, 3600).index(horizon)] = (
                    backend.local_branch_exclusion(
                        from_horizon=previous,
                        to_horizon=horizon,
                        previous_root=starts[120],
                    )
                )
                forward_open = False
            elif horizon == 1200:
                forward_open = False
                lower_open = False
            else:
                lower_open = False
            continue
        panel = _bridge_root_panel(horizon, records)
        root_panels[index_by_horizon[horizon]] = panel
        starts = {
            precision: _root_coordinates(panel, precision)
            for precision in (80, 120)
        }

    direct_replays: list[dict[str, Any] | None] = [None] * len(HORIZONS)
    for index, panel in enumerate(root_panels):
        if panel is None:
            continue
        direct_replays[index] = copy.deepcopy(
            backend.finite_sum_replay(
                horizon=panel["horizon"],
                root=_root_coordinates(panel, 120),
            )
        )
    direct_replay_pass = all(
        direct_replays[index] is not None and direct_replays[index]["pass"]
        for index in range(2, 7)
    )

    homotopies: list[dict[str, Any] | None] = [None] * 6
    forward_homotopy_open = True
    lower_homotopy_open = True
    for edge_index, (first, second, direction) in enumerate(homotopy_edges):
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

    legacy_panels = []
    for panel in root_panels:
        if panel is None:
            legacy_panels.append(None)
            continue
        legacy = copy.deepcopy(panel)
        legacy.pop("cross_80_inner_in_120_outer")
        legacy.pop("cross_120_inner_in_80_outer")
        legacy_panels.append(legacy)
    drift = reused._drift_record(legacy_panels)
    drift.pop("mutation_closes_pass")
    lower_complete = bool(
        all(
            root_panels[index_by_horizon[horizon]] is not None
            and direct_replays[index_by_horizon[horizon]] is not None
            and direct_replays[index_by_horizon[horizon]]["pass"]
            for horizon in (1200, 900, 600)
        )
        and all(row is not None and row["status"] == "pass" for row in homotopies[4:])
    )
    lower_status = (
        "lower-tail-stress-pass"
        if lower_complete
        else "lower-tail-stress-inconclusive"
    )
    payload: dict[str, Any] = {
        "classification": {
            "claim_boundary": _load_schema()["constants"]["claim_boundary"],
            "decision": "g1-g3-bridge-inconclusive",
            "gates": {},
            "lower_tail_status": lower_status,
            "precedence_rank": 3,
        },
        "controls": {},
        "endpoint_links": [
            _endpoint_link(
                component="G5",
                component_root=sealed_components["g5_root"],
                panel=root_panels[index_by_horizon[2400]],
            ),
            _endpoint_link(
                component="G4",
                component_root=sealed_components["g4_root"],
                panel=root_panels[index_by_horizon[3600]],
            ),
        ],
        "finite_branch": {
            "direct_replay_pass": direct_replay_pass,
            "direct_replays": direct_replays,
            "drift": drift,
            "exclusions": exclusions,
            "forward_horizons": list(FORWARD_HORIZONS),
            "homotopies": homotopies,
            "horizons": list(HORIZONS),
            "lower_horizons": list(LOWER_HORIZONS),
            "lower_tail_status": lower_status,
            "root_panels": root_panels,
        },
        "identity": copy.deepcopy(identity),
        "publication": copy.deepcopy(publication),
        "q_representations": reused.q_representations(HORIZONS),
        "sealed_components": copy.deepcopy(sealed_components),
    }
    # Keep controls last: G4/G5 are sealed data above and are never backend calls.
    payload["controls"] = copy.deepcopy(backend.controls())
    payload["controls"]["pass"] = _controls_evidence(payload)
    gates = _reconstructed_gates(payload)
    decision = classify_bridge(gates)
    payload["classification"].update(decision)
    payload["classification"]["gates"] = gates
    validate_result(payload)
    return payload


def _atomic_write_bytes(path: Path, content: bytes) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.tmp")
    temporary.write_bytes(content)
    os.replace(temporary, destination)


def _publication_path(repository: Path, relative: str, *, field: str) -> Path:
    if type(relative) is not str or not relative or "\\" in relative:
        raise ValueError(f"{field}: expected nonempty POSIX repository path")
    candidate = (repository / relative).resolve()
    if repository not in candidate.parents:
        raise ValueError(f"{field}: path escaped repository")
    return candidate


def publish_bridge_result(
    payload: dict[str, Any],
    audit_report: dict[str, Any],
    *,
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    """Publish result, report and audit atomically, with the manifest last."""

    validate_result(payload)
    if (
        audit_report.get("verdict")
        != "g1-g3-bridge-independent-audit-agrees"
        or audit_report.get("decision") != payload["classification"]["decision"]
    ):
        raise ValueError("independent audit does not bind the bridge decision")
    artifacts = payload["publication"]["artifacts"]
    if [row["role"] for row in artifacts] != ["result-json", "readable-report"]:
        raise ValueError("publication artifact order mismatch")
    repository = Path(repository_root).resolve()
    result_path = _publication_path(
        repository, artifacts[0]["path"], field="publication.result"
    )
    report_path = _publication_path(
        repository, artifacts[1]["path"], field="publication.report"
    )
    audit_path = _publication_path(
        repository,
        payload["publication"]["auditor_output_path"],
        field="publication.audit",
    )
    manifest_path = _publication_path(
        repository,
        payload["publication"]["manifest_path"],
        field="publication.manifest",
    )
    destinations = (result_path, report_path, audit_path, manifest_path)
    if len(set(destinations)) != 4:
        raise ValueError("publication paths must be distinct")
    existing = [path for path in destinations if path.exists()]
    if existing:
        raise FileExistsError(f"refusing to overwrite publication: {existing[0]}")

    result_bytes = (
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    gates = payload["classification"]["gates"]
    report_lines = [
        "# Rotating-wave G1--G3 horizon bridge",
        "",
        f"Decision: `{payload['classification']['decision']}`.",
        "",
        f"Claim boundary: {payload['classification']['claim_boundary']}",
        "",
        "| Gate | State |",
        "| --- | --- |",
    ]
    report_lines.extend(
        f"| {name} | `{value}` |"
        for name, value in gates.items()
        if name != "local_branch_excluded"
    )
    report_lines.extend(
        [
            "",
            "This record composes finite-root branch evidence with hash-bound ",
            "G4/G5 endpoints. It does not establish H-infinity stability, ",
            "formation, interaction, inertia or mass.",
            "",
        ]
    )
    report_bytes = "\n".join(report_lines).encode("utf-8")
    bound_audit = copy.deepcopy(audit_report)
    bound_audit["result_sha256"] = hashlib.sha256(result_bytes).hexdigest()
    audit_bytes = (
        json.dumps(bound_audit, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    rows = [
        {
            "path": artifacts[0]["path"],
            "role": "result-json",
            "sha256": hashlib.sha256(result_bytes).hexdigest(),
        },
        {
            "path": artifacts[1]["path"],
            "role": "readable-report",
            "sha256": hashlib.sha256(report_bytes).hexdigest(),
        },
        {
            "path": payload["publication"]["auditor_output_path"],
            "role": "independent-audit",
            "sha256": hashlib.sha256(audit_bytes).hexdigest(),
        },
    ]
    manifest = {
        "artifacts": rows,
        "execution_commit": payload["identity"]["execution_commit"],
        "protocol_sha256": payload["identity"]["protocol_sha256"],
        "schema": "scalar-memory-rotating-wave-horizon-g1-g3-publication-v1",
    }
    manifest_bytes = (
        json.dumps(manifest, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    _atomic_write_bytes(result_path, result_bytes)
    _atomic_write_bytes(report_path, report_bytes)
    _atomic_write_bytes(audit_path, audit_bytes)
    _atomic_write_bytes(manifest_path, manifest_bytes)
    return manifest


def _centered_pair(center: str, half_width: str) -> list[str]:
    with localcontext() as context:
        context.prec = 180
        middle = Decimal(center)
        width = Decimal(half_width)
        return [format(middle - width, "f"), format(middle + width, "f")]


def _box(
    radius_half_width: str = "1e-8", theta_half_width: str = "1e-8"
) -> dict[str, list[str]]:
    return {
        "radius": _centered_pair("0.95", radius_half_width),
        "theta": _centered_pair("0.016", theta_half_width),
    }


def _root_image(
    radius_half_width: str = "5e-9", theta_half_width: str = "5e-9"
) -> list[list[str]]:
    return [
        _centered_pair("0.95", radius_half_width),
        _centered_pair("0.016", theta_half_width),
    ]


def _point_jacobian() -> list[list[str]]:
    return [["-1", "1"], ["-1", "1"]]


def _interval_jacobian() -> list[list[list[str]]]:
    return [
        [["-1", "1"], ["-1", "1"]],
        [["-1", "1"], ["-1", "1"]],
    ]


def _certificate(*, inner: bool) -> dict[str, Any]:
    return {
        "box": _box("1e-30", "1e-30") if inner else _box(),
        "interval_backend": "mpmath.iv",
        "jacobian_box": _interval_jacobian(),
        "krawczyk_image": (
            _root_image("5e-31", "5e-31") if inner else _root_image()
        ),
        "strict_interior": True,
    }


def _newton(precision: int) -> dict[str, Any]:
    return {
        "jacobian": _point_jacobian(),
        "precision_dps": precision,
        "radius": "0.95",
        "residual": ["0", "0"],
        "steps": 8,
        "theta": "0.016",
    }


def _root_panel(horizon: int) -> dict[str, Any]:
    return {
        "centers_agree": True,
        "cross_120_inner_in_80_outer": True,
        "cross_80_inner_in_120_outer": True,
        "horizon": horizon,
        "inner_certificate_120": _certificate(inner=True),
        "inner_certificate_80": _certificate(inner=True),
        "inner_intersection": {
            "radius": _centered_pair("0.95", "5e-31"),
            "theta": _centered_pair("0.016", "5e-31"),
        },
        "newton_120": _newton(120),
        "newton_80": _newton(80),
        "outer_certificate_120": _certificate(inner=False),
        "outer_certificate_80": _certificate(inner=False),
    }


def _homotopy(first: int, second: int, direction: str) -> dict[str, Any]:
    slabs = []
    for index in range(64):
        slabs.append(
            {
                "box": _box("1e-4", "1e-6"),
                "index": index,
                "krawczyk_image": _root_image("5e-5", "5e-7"),
                "overlaps_previous": None if index == 0 else True,
                "s_interval": [
                    format(Decimal(index) / 64, "f"),
                    format(Decimal(index + 1) / 64, "f"),
                ],
                "strict_interior": True,
            }
        )
    return {
        "direction": direction,
        "from_horizon": first,
        "pass": True,
        "slabs": slabs,
        "status": "pass",
        "to_horizon": second,
    }


def _endpoint(component: str, horizon: int) -> dict[str, Any]:
    return {
        "bridge_120_inner_in_component_outer": True,
        "bridge_80_inner_in_component_outer": True,
        "component": component,
        "component_inner_image": _root_image("5e-31", "5e-31"),
        "component_inner_in_bridge_120_outer": True,
        "component_inner_in_bridge_80_outer": True,
        "component_outer_box": _box(),
        "horizon": horizon,
        "pass": True,
    }


def _replay(horizon: int) -> dict[str, Any]:
    return {
        "horizon": horizon,
        "pass": True,
        "physical_signs": True,
        "precision_dps": REPLAY_DPS,
        "radial_residual": "0",
        "radial_sum": "1",
        "radius": "0.95",
        "residual_gate": True,
        "residual_maximum": "0",
        "semantics": REPLAY_SEMANTICS,
        "tangential_residual": "0",
        "tangential_sum": "-1",
        "theta": "0.016",
    }


def contract_witness() -> dict[str, Any]:
    """Return a complete synthetic positive payload without target access."""

    panels = [_root_panel(horizon) for horizon in HORIZONS]
    homotopies = [
        _homotopy(1200, 1500, "forward"),
        _homotopy(1500, 1800, "forward"),
        _homotopy(1800, 2400, "forward"),
        _homotopy(2400, 3600, "forward"),
        _homotopy(1200, 900, "lower-tail"),
        _homotopy(900, 600, "lower-tail"),
    ]
    drift_rows = []
    for first_horizon, second_horizon in ((1800, 2400), (2400, 3600)):
        first = panels[HORIZONS.index(first_horizon)]["inner_intersection"]
        second = panels[HORIZONS.index(second_horizon)]["inner_intersection"]
        radius_component, theta_component = (
            _transfer_gate()._interval_drift_components(
                first,
                second,
                radius_scale=PARAMETERS["anchor_radius"],
                theta_scale=PARAMETERS["anchor_theta"],
            )
        )
        drift_rows.append(
            {
                "from_horizon": first_horizon,
                "radius_component": radius_component,
                "theta_component": theta_component,
                "to_horizon": second_horizon,
                "upper_bound": max(radius_component, theta_component),
            }
        )
    q_rows = _transfer_gate().q_representations(HORIZONS)
    circular_horizons = (17, 257, *HORIZONS)
    controls = {
        "circular_cases": [
            {
                "case_id": (
                    f"noncircle-H{horizon}"
                    if horizon in (17, 257)
                    else f"anchor-H{horizon}"
                ),
                "complete_state_relative_error": 0.0,
                "expected_age_history_sha256": f"{index + 1:064x}",
                "horizon": horizon,
                "new_point_relative_error": 0.0,
                "observed_age_history_sha256": f"{index + 1:064x}",
                "pass": True,
            }
            for index, horizon in enumerate(circular_horizons)
        ],
        "eta_zero_cases": [
            {
                "horizon": horizon,
                "maximum_deviation": 0.0,
                "pass": True,
                "steps": horizon + 1,
            }
            for horizon in HORIZONS
        ],
        "mutations": [
            {
                "complete_state_relative_error": 1e-6,
                "detected": True,
                "horizon": 17,
                "name": name,
                "new_point_relative_error": 1e-6,
            }
            for name in (
                "reverse-modulo",
                "overwrite-before-read",
                "wrong-oldest-slot",
            )
        ],
        "pass": True,
    }
    payload: dict[str, Any] = {
        "classification": {
            "claim_boundary": _load_schema()["constants"]["claim_boundary"],
            "decision": (
                "rotating-wave-root-branch-connected-with-h2400-"
                "local-stability-support"
            ),
            "gates": {},
            "lower_tail_status": "lower-tail-stress-pass",
            "precedence_rank": 6,
        },
        "controls": controls,
        "endpoint_links": [_endpoint("G5", 2400), _endpoint("G4", 3600)],
        "finite_branch": {
            "direct_replay_pass": True,
            "direct_replays": [_replay(horizon) for horizon in HORIZONS],
            "drift": {
                "center_diagnostics": copy.deepcopy(drift_rows),
                "interval_upper_bounds": drift_rows,
                "pass": True,
            },
            "exclusions": [None, None, None, None],
            "forward_horizons": list(FORWARD_HORIZONS),
            "homotopies": homotopies,
            "horizons": list(HORIZONS),
            "lower_horizons": list(LOWER_HORIZONS),
            "lower_tail_status": "lower-tail-stress-pass",
            "root_panels": panels,
        },
        "identity": {
            "authorization": {
                "authorization_id": "00000000-0000-4000-8000-000000000001",
                "ci_run_id": 1,
                "governance_sha256": "1" * 64,
                "implementation_revision": "1" * 40,
                "receipt_path": "synthetic/receipt.json",
                "receipt_sha256": "2" * 64,
                "upstream_revision": "3" * 40,
            },
            "created_utc": "2000-01-01T00:00:00+00:00",
            "execution_commit": "3" * 40,
            "parameters": copy.deepcopy(PARAMETERS),
            "protocol_blob": _load_schema()["constants"]["protocol_blob"],
            "protocol_sha256": _load_schema()["constants"]["protocol_sha256"],
            "schema": _load_schema()["constants"]["payload_schema"],
            "version": 1,
        },
        "publication": {
            "artifacts": [
                {"path": "synthetic.json", "role": "result-json"},
                {"path": "synthetic.md", "role": "readable-report"},
            ],
            "auditor_output_path": "synthetic.audit.json",
            "manifest_path": "synthetic.publication.json",
            "manifest_published_last": True,
        },
        "q_representations": q_rows,
        "sealed_components": {
            "files": [
                {"role": role, "path": path, "sha256": digest}
                for role, path, digest in SEALED_FILES
            ],
            "g4_root": {
                "decision": "g4-local-infinite-root-pass",
                "horizon": 3600,
                "inner_image": _root_image("5e-31", "5e-31"),
                "outer_box": _box(),
            },
            "g5_root": {
                "decision": "g5-local-direct-stability-pass",
                "horizon": 2400,
                "inner_image": _root_image("5e-31", "5e-31"),
                "outer_box": _box(),
            },
        },
    }
    payload["classification"]["gates"] = _reconstructed_gates(payload)
    validate_result(payload)
    return payload
