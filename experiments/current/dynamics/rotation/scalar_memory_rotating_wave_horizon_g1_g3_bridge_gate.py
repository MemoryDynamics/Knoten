"""Fail-closed contract core for the registered G1--G3 horizon bridge.

This module contains no target execution and writes no result artifact.  It
validates primitive finite-branch evidence and the hash-bound composition with
the sealed G4/G5 components.
"""

from __future__ import annotations

import copy
from decimal import Decimal, localcontext
from functools import cache
import importlib.util
import json
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

    if gates["G0"] != "pass" or gates["G6"] != "pass":
        return {"decision": "g1-g3-bridge-experiment-invalid", "precedence_rank": 1}
    if gates["local_branch_excluded"]:
        return {
            "decision": "registered-local-horizon-branch-loss",
            "precedence_rank": 2,
        }
    if gates["G1F"] != "pass" or gates["G2F"] != "pass":
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
    g1f = all(panel_pass[index] for index in range(2, 7))
    g1r = all(panel_pass[index] for index in (2, 1, 0))
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
    return {
        "G0": (
            "pass"
            if branch["direct_replay_pass"]
            and all(row["two_ulp_gate"] and row["nonzero_finite"] for row in payload["q_representations"])
            else "fail"
        ),
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
        "G6": "pass" if _transfer_gate()._controls_evidence(payload) else "fail",
        "H2400_link": link_states[0],
        "H3600_link": link_states[1],
        "local_branch_excluded": local_branch_excluded,
    }


def validate_result(payload: dict[str, Any]) -> None:
    """Validate schema plus all decision-relevant semantic relationships."""

    contract = _load_schema()
    validate_contract(payload, contract)
    if payload["identity"]["parameters"] != PARAMETERS:
        raise ValueError("$.identity.parameters: registered parameters mismatch")
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
    if payload["q_representations"] != reused.q_representations(HORIZONS):
        raise ValueError("$.q_representations: reconstruction mismatch")
    drift = payload["finite_branch"]["drift"]
    drift_rows = drift["interval_upper_bounds"]
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
    controls_pass = reused._controls_evidence(payload)
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

    direct_replay_pass = bool(backend.direct_replay())
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
    lower_complete = bool(
        all(root_panels[index_by_horizon[horizon]] is not None for horizon in (1200, 900, 600))
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
    payload["controls"]["pass"] = reused._controls_evidence(payload)
    gates = _reconstructed_gates(payload)
    decision = classify_bridge(gates)
    payload["classification"].update(decision)
    payload["classification"]["gates"] = gates
    validate_result(payload)
    return payload


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
                "age_history_sha256": f"{index + 1:064x}",
                "case_id": f"case-H{horizon}",
                "complete_state_relative_error": 0.0,
                "horizon": horizon,
                "new_point_relative_error": 0.0,
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
            {"detected": True, "name": name}
            for name in (
                "drift-width",
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
            "drift": {
                "center_diagnostics": copy.deepcopy(drift_rows),
                "interval_upper_bounds": drift_rows,
                "mutation_closes_pass": True,
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
