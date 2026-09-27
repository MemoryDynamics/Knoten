"""Independent standard-library audit for the registered G1--G3 bridge."""

from __future__ import annotations

from decimal import Decimal
from functools import cache
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_g1_g3_bridge_result_schema_v1.json"
)
LEGACY_AUDIT_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_transfer_result_audit.py"
)
HORIZONS = (600, 900, 1200, 1500, 1800, 2400, 3600)
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
        "e83309992fe8b964c507930664f557367a50d87d32aedf7bf39ecbe1bb346d19",
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
REPLAY_SEMANTICS = "independent finite-sum replay; not a second interval proof"


def _git_blob_bytes(repository: Path, relative: str) -> bytes:
    return subprocess.run(
        ["git", "cat-file", "blob", f"HEAD:{relative}"],
        cwd=repository,
        check=True,
        capture_output=True,
    ).stdout


@cache
def _legacy() -> Any:
    spec = importlib.util.spec_from_file_location(
        "g1_g3_independent_legacy_audit", LEGACY_AUDIT_PATH
    )
    if spec is None or spec.loader is None:
        raise ImportError("cannot load standard-library horizon audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _json(path: Path) -> dict[str, Any]:
    def reject(value: str) -> None:
        raise ValueError(f"non-finite JSON constant: {value}")

    result = json.loads(path.read_bytes(), parse_constant=reject)
    if type(result) is not dict:
        raise TypeError(f"{path}: JSON root must be an object")
    return result


def _decimal(value: str, *, path: str) -> Decimal:
    if type(value) is not str:
        raise TypeError(f"{path}: expected decimal string")
    result = Decimal(value)
    if not result.is_finite():
        raise ValueError(f"{path}: decimal must be finite")
    return result


def _pair(values: Sequence[str], *, path: str) -> tuple[Decimal, Decimal]:
    if type(values) is not list or len(values) != 2:
        raise TypeError(f"{path}: expected decimal interval")
    lower = _decimal(values[0], path=f"{path}[0]")
    upper = _decimal(values[1], path=f"{path}[1]")
    if lower > upper:
        raise ValueError(f"{path}: reversed interval")
    return lower, upper


def _contains(
    container: Sequence[str], subject: Sequence[str], *, path: str
) -> bool:
    lower, upper = _pair(container, path=f"{path}.container")
    subject_lower, subject_upper = _pair(subject, path=f"{path}.subject")
    return lower <= subject_lower and subject_upper <= upper


def _image_in_box(
    image: Sequence[Sequence[str]], box: dict[str, Any], *, path: str
) -> bool:
    return bool(
        len(image) == 2
        and _contains(box["radius"], image[0], path=f"{path}.radius")
        and _contains(box["theta"], image[1], path=f"{path}.theta")
    )


def _verify_sealed(payload: dict[str, Any], *, repository: Path) -> None:
    expected_rows = [
        {"role": role, "path": relative, "sha256": digest}
        for role, relative, digest in SEALED_FILES
    ]
    if payload["sealed_components"]["files"] != expected_rows:
        raise ValueError("$.sealed_components.files: registered rows mismatch")
    documents: dict[str, dict[str, Any]] = {}
    root = repository.resolve()
    for role, relative, digest in SEALED_FILES:
        path = (root / relative).resolve()
        if root not in path.parents:
            raise ValueError("sealed path escaped repository")
        raw = _git_blob_bytes(root, relative)
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError(f"sealed hash mismatch: {role}")
        if role in {"g4-result", "g5-result"}:
            document = json.loads(raw)
            if type(document) is not dict:
                raise TypeError(f"sealed JSON root is not an object: {role}")
            documents[role] = document
    for name, role, horizon, decision in (
        ("g4_root", "g4-result", 3600, "g4-local-infinite-root-pass"),
        ("g5_root", "g5-result", 2400, "g5-local-direct-stability-pass"),
    ):
        document = documents[role]
        finite = document["finite_root"]
        expected = {
            "decision": decision,
            "horizon": horizon,
            "inner_image": finite["inner_certificate"]["krawczyk_image"],
            "outer_box": finite["outer_certificate"]["box"],
        }
        if document["classification"]["decision"] != decision:
            raise ValueError(f"sealed decision mismatch: {role}")
        if payload["sealed_components"][name] != expected:
            raise ValueError(f"$.sealed_components.{name}: extraction mismatch")


def _verify_roots_and_homotopies(payload: dict[str, Any]) -> list[bool]:
    evidence = _legacy()._verify_root_and_homotopy_slots(payload)
    for index, row in enumerate(payload["finite_branch"]["homotopies"]):
        if row is None:
            continue
        count = _legacy()._nonnull_prefix_length(
            row["slabs"], path=f"$.finite_branch.homotopies[{index}].slabs"
        )
        passed = bool(
            count == 64
            and all(
                slab["strict_interior"]
                and (slab_index == 0 or slab["overlaps_previous"] is True)
                for slab_index, slab in enumerate(row["slabs"][:count])
            )
        )
        if row["pass"] is not passed or row["status"] != (
            "pass" if passed else "inconclusive"
        ):
            raise ValueError(f"homotopy {index} status reconstruction mismatch")
    results = []
    for index, panel in enumerate(payload["finite_branch"]["root_panels"]):
        if panel is None:
            results.append(False)
            continue
        cross_80 = _image_in_box(
            panel["inner_certificate_80"]["krawczyk_image"],
            panel["outer_certificate_120"]["box"],
            path=f"$.finite_branch.root_panels[{index}].cross_80",
        )
        cross_120 = _image_in_box(
            panel["inner_certificate_120"]["krawczyk_image"],
            panel["outer_certificate_80"]["box"],
            path=f"$.finite_branch.root_panels[{index}].cross_120",
        )
        if panel["cross_80_inner_in_120_outer"] is not cross_80:
            raise ValueError("root cross-precision 80-to-120 mismatch")
        if panel["cross_120_inner_in_80_outer"] is not cross_120:
            raise ValueError("root cross-precision 120-to-80 mismatch")
        results.append(bool(evidence[index] and cross_80 and cross_120))
    return results


def _verify_replays(payload: dict[str, Any]) -> list[bool | None]:
    panels = payload["finite_branch"]["root_panels"]
    rows = payload["finite_branch"]["direct_replays"]
    states: list[bool | None] = []
    for index, (panel, row, horizon) in enumerate(
        zip(panels, rows, HORIZONS, strict=True)
    ):
        path = f"$.finite_branch.direct_replays[{index}]"
        if panel is None:
            if row is not None:
                raise ValueError(f"{path}: replay without root")
            states.append(None)
            continue
        if row is None:
            states.append(None)
            continue
        if (
            row["horizon"] != horizon
            or row["precision_dps"] != 70
            or row["radius"] != panel["newton_120"]["radius"]
            or row["theta"] != panel["newton_120"]["theta"]
            or row["semantics"] != REPLAY_SEMANTICS
        ):
            raise ValueError(f"{path}: registered replay identity mismatch")
        radial = _decimal(row["radial_residual"], path=f"{path}.radial")
        tangential = _decimal(
            row["tangential_residual"], path=f"{path}.tangential"
        )
        maximum = max(abs(radial), abs(tangential))
        radial_sum = _decimal(row["radial_sum"], path=f"{path}.radial_sum")
        tangential_sum = _decimal(
            row["tangential_sum"], path=f"{path}.tangential_sum"
        )
        residual_gate = maximum <= Decimal("1e-45")
        signs = radial_sum > 0 and tangential_sum < 0
        passed = residual_gate and signs
        if (
            _decimal(row["residual_maximum"], path=f"{path}.maximum") != maximum
            or row["residual_gate"] is not residual_gate
            or row["physical_signs"] is not signs
            or row["pass"] is not passed
        ):
            raise ValueError(f"{path}: replay reconstruction mismatch")
        states.append(passed)
    summary = all(states[index] is True for index in range(2, 7))
    if payload["finite_branch"]["direct_replay_pass"] is not summary:
        raise ValueError("$.finite_branch.direct_replay_pass: mismatch")
    return states


def _verify_drift(payload: dict[str, Any]) -> str:
    rows = payload["finite_branch"]["drift"]["interval_upper_bounds"]
    if payload["finite_branch"]["drift"]["center_diagnostics"] != rows:
        raise ValueError("drift diagnostics reconstruction mismatch")
    panels = {
        panel["horizon"]: panel["inner_intersection"]
        for panel in payload["finite_branch"]["root_panels"]
        if panel is not None and panel["inner_intersection"] is not None
    }
    for index, (first, second) in enumerate(((1800, 2400), (2400, 3600))):
        row = rows[index]
        if first not in panels or second not in panels:
            if row is not None:
                raise ValueError("drift row exists without endpoint roots")
            continue
        radius, theta = _legacy()._interval_drift_components(
            panels[first],
            panels[second],
            radius_scale=PARAMETERS["anchor_radius"],
            theta_scale=PARAMETERS["anchor_theta"],
        )
        expected = {
            "from_horizon": first,
            "radius_component": radius,
            "theta_component": theta,
            "to_horizon": second,
            "upper_bound": max(radius, theta),
        }
        if row != expected:
            raise ValueError(f"drift row {index} reconstruction mismatch")
    complete = all(row is not None for row in rows)
    passed = bool(
        complete
        and rows[1]["upper_bound"] <= 1e-8
        and rows[1]["upper_bound"]
        <= 0.01 * rows[0]["upper_bound"] + 1e-14
    )
    if payload["finite_branch"]["drift"]["pass"] is not passed:
        raise ValueError("drift pass reconstruction mismatch")
    return "pass" if passed else "fail" if complete else "inconclusive"


def _verify_controls(payload: dict[str, Any]) -> bool:
    controls = payload["controls"]
    cases = [
        ("noncircle-H17", 17),
        ("noncircle-H257", 257),
        *((f"anchor-H{horizon}", horizon) for horizon in HORIZONS),
    ]
    passed = True
    for row, (case_id, horizon) in zip(
        controls["circular_cases"], cases, strict=True
    ):
        expected = bool(
            row["case_id"] == case_id
            and row["horizon"] == horizon
            and row["expected_age_history_sha256"]
            == row["observed_age_history_sha256"]
            and row["new_point_relative_error"] < 5e-14
            and row["complete_state_relative_error"] < 5e-14
        )
        if row["pass"] is not expected:
            raise ValueError("circular control pass mismatch")
        passed = passed and expected
    for row, horizon in zip(controls["eta_zero_cases"], HORIZONS, strict=True):
        expected = bool(
            row["horizon"] == horizon
            and row["steps"] == horizon + 1
            and row["maximum_deviation"] < 1e-14
        )
        if row["pass"] is not expected:
            raise ValueError("eta-zero control pass mismatch")
        passed = passed and expected
    for row, name in zip(
        controls["mutations"],
        ("reverse-modulo", "overwrite-before-read", "wrong-oldest-slot"),
        strict=True,
    ):
        detected = bool(
            row["name"] == name
            and row["horizon"] == 17
            and (
                row["new_point_relative_error"] >= 5e-14
                or row["complete_state_relative_error"] >= 5e-14
            )
        )
        if row["detected"] is not detected:
            raise ValueError("FIFO mutation reconstruction mismatch")
        passed = passed and detected
    if controls["pass"] is not passed:
        raise ValueError("$.controls.pass: reconstruction mismatch")
    return passed


def _verify_endpoints(payload: dict[str, Any]) -> list[str]:
    states = []
    for index, (component, horizon) in enumerate((("G5", 2400), ("G4", 3600))):
        link = payload["endpoint_links"][index]
        panel = payload["finite_branch"]["root_panels"][HORIZONS.index(horizon)]
        if link is None or panel is None:
            states.append("inconclusive")
            continue
        component_root = payload["sealed_components"][f"{component.lower()}_root"]
        expected = {
            "bridge_120_inner_in_component_outer": _image_in_box(
                panel["inner_certificate_120"]["krawczyk_image"],
                component_root["outer_box"],
                path=f"endpoint[{index}].bridge120",
            ),
            "bridge_80_inner_in_component_outer": _image_in_box(
                panel["inner_certificate_80"]["krawczyk_image"],
                component_root["outer_box"],
                path=f"endpoint[{index}].bridge80",
            ),
            "component_inner_in_bridge_120_outer": _image_in_box(
                component_root["inner_image"],
                panel["outer_certificate_120"]["box"],
                path=f"endpoint[{index}].component120",
            ),
            "component_inner_in_bridge_80_outer": _image_in_box(
                component_root["inner_image"],
                panel["outer_certificate_80"]["box"],
                path=f"endpoint[{index}].component80",
            ),
        }
        if (
            link["component"] != component
            or link["horizon"] != horizon
            or link["component_inner_image"] != component_root["inner_image"]
            or link["component_outer_box"] != component_root["outer_box"]
        ):
            raise ValueError(f"endpoint {index} identity mismatch")
        for name, value in expected.items():
            if link[name] is not value:
                raise ValueError(f"endpoint {index} inclusion mismatch")
        passed = all(expected.values())
        if link["pass"] is not passed:
            raise ValueError(f"endpoint {index} pass mismatch")
        states.append("pass" if passed else "fail")
    return states


def _classify(gates: dict[str, Any]) -> tuple[str, int]:
    if gates["G0"] == "fail" or gates["G6"] == "fail":
        return "g1-g3-bridge-experiment-invalid", 1
    if gates["local_branch_excluded"]:
        return "registered-local-horizon-branch-loss", 2
    if gates["G0"] != "pass" or gates["G1F"] != "pass" or gates["G2F"] != "pass":
        return "g1-g3-bridge-inconclusive", 3
    if gates["G3"] == "fail":
        return "rotating-wave-horizon-branch-drift", 4
    if gates["G3"] != "pass" or gates["G4"] != "pass" or gates["G5"] != "pass":
        return "g1-g3-bridge-inconclusive", 3
    if gates["H2400_link"] == "fail" or gates["H3600_link"] == "fail":
        return "sealed-component-endpoint-mismatch", 5
    if gates["H2400_link"] != "pass" or gates["H3600_link"] != "pass":
        return "g1-g3-bridge-inconclusive", 3
    return (
        "rotating-wave-root-branch-connected-with-h2400-local-stability-support",
        6,
    )


def audit_payload(
    payload: dict[str, Any], *, repository_root: Path = ROOT
) -> dict[str, Any]:
    """Reconstruct every decision-relevant bridge relationship."""

    schema = _json(SCHEMA_PATH)
    _legacy().validate_result(payload, schema)
    if payload["identity"]["parameters"] != PARAMETERS:
        raise ValueError("$.identity.parameters: registered values mismatch")
    publication = payload["publication"]
    if (
        [row["role"] for row in publication["artifacts"]]
        != ["result-json", "readable-report"]
        or publication["manifest_published_last"] is not True
    ):
        raise ValueError("$.publication: registered order/manifest-last mismatch")
    publication_paths = [
        *(row["path"] for row in publication["artifacts"]),
        publication["auditor_output_path"],
        publication["manifest_path"],
    ]
    if len(set(publication_paths)) != 4:
        raise ValueError("$.publication: paths must be distinct")
    _verify_sealed(payload, repository=repository_root)
    roots = _verify_roots_and_homotopies(payload)
    replays = _verify_replays(payload)
    expected_q = _legacy().q_representations(HORIZONS, alpha=0.01)
    if payload["q_representations"] != expected_q:
        raise ValueError("$.q_representations: reconstruction mismatch")
    drift_state = _verify_drift(payload)
    controls_pass = _verify_controls(payload)
    endpoint_states = _verify_endpoints(payload)
    homotopies = payload["finite_branch"]["homotopies"]
    exclusions = payload["finite_branch"]["exclusions"]
    local_excluded = False
    edges = ((1200, 1500), (1500, 1800), (1800, 2400), (2400, 3600))
    for index, attempt in enumerate(exclusions):
        if attempt is None:
            continue
        if (attempt["from_horizon"], attempt["to_horizon"]) != edges[index]:
            raise ValueError("branch-exclusion edge mismatch")
        previous = payload["finite_branch"]["root_panels"][index + 2]
        if previous is None:
            raise ValueError("branch exclusion lacks previous root")
        radius = Decimal(previous["newton_120"]["radius"])
        theta = Decimal(previous["newton_120"]["theta"])
        domain = {
            "radius": [
                format(max(Decimal("0.8"), radius - Decimal("0.02")), "f"),
                format(min(Decimal("1.1"), radius + Decimal("0.02")), "f"),
            ],
            "theta": [
                format(max(Decimal("0.01"), theta - Decimal("0.002")), "f"),
                format(min(Decimal("0.022"), theta + Decimal("0.002")), "f"),
            ],
        }
        _legacy()._audit_partition(
            attempt, domain, path=f"$.finite_branch.exclusions[{index}]"
        )
        classifications = []
        for leaf in attempt["leaves"]:
            classification = leaf["classification"]
            classifications.append(classification)
            residual = leaf["residual_box"]
            image = leaf["krawczyk_image"]
            strict = leaf["strict_interior"]
            if classification == "residual-excluded":
                if residual is None or image is not None or strict is not None:
                    raise ValueError("residual exclusion witness mismatch")
                if not any(
                    not (lower <= 0 <= upper)
                    for lower, upper in (
                        _pair(item, path="exclusion.residual") for item in residual
                    )
                ):
                    raise ValueError("exclusion residual does not exclude zero")
            elif classification == "krawczyk-root":
                reconstructed = bool(
                    residual is None
                    and image is not None
                    and _image_in_box(image, leaf["box"], path="exclusion.root")
                )
                if strict is not reconstructed or not reconstructed:
                    raise ValueError("exclusion root witness mismatch")
            elif not (
                classification == "unresolved"
                and residual is None
                and image is None
                and strict is None
            ):
                raise ValueError("unresolved exclusion witness mismatch")
        expected_status = (
            "all-residual-excluded"
            if all(value == "residual-excluded" for value in classifications)
            else "other-root"
            if "krawczyk-root" in classifications
            else "inconclusive"
        )
        if attempt["status"] != expected_status:
            raise ValueError("branch exclusion status mismatch")
        local_excluded = local_excluded or expected_status == "all-residual-excluded"
    q_pass = all(
        row["two_ulp_gate"] and row["nonzero_finite"]
        for row in payload["q_representations"]
    )
    forward_replays = replays[2:]
    if not q_pass or any(state is False for state in forward_replays):
        g0 = "fail"
    elif all(state is True for state in forward_replays):
        g0 = "pass"
    else:
        g0 = "inconclusive"
    gates = {
        "G0": g0,
        "G1F": "pass" if all(roots[2:]) else "inconclusive",
        "G1R": (
            "pass"
            if all(roots[index] and replays[index] is True for index in (2, 1, 0))
            else "inconclusive"
        ),
        "G2F": (
            "pass"
            if all(row is not None and row["status"] == "pass" and row["pass"] for row in homotopies[:4])
            else "inconclusive"
        ),
        "G2R": (
            "pass"
            if all(row is not None and row["status"] == "pass" and row["pass"] for row in homotopies[4:])
            else "inconclusive"
        ),
        "G3": drift_state,
        "G4": "pass",
        "G5": "pass",
        "G6": "pass" if controls_pass else "fail",
        "H2400_link": endpoint_states[0],
        "H3600_link": endpoint_states[1],
        "local_branch_excluded": local_excluded,
    }
    if payload["classification"]["gates"] != gates:
        raise ValueError("$.classification.gates: reconstruction mismatch")
    lower = (
        "lower-tail-stress-pass"
        if gates["G1R"] == gates["G2R"] == "pass"
        else "lower-tail-stress-inconclusive"
    )
    if (
        payload["finite_branch"]["lower_tail_status"] != lower
        or payload["classification"]["lower_tail_status"] != lower
    ):
        raise ValueError("lower-tail status reconstruction mismatch")
    decision, rank = _classify(gates)
    if (
        payload["classification"]["decision"] != decision
        or payload["classification"]["precedence_rank"] != rank
    ):
        raise ValueError("classification reconstruction mismatch")
    return {
        "checks": {
            "classification": True,
            "controls": True,
            "drift": True,
            "endpoint_identity": True,
            "finite_branch": True,
            "replays": True,
            "schema": True,
            "sealed_hashes": True,
        },
        "decision": decision,
        "schema": "scalar-memory-rotating-wave-horizon-g1-g3-bridge-audit-v1",
        "trust_boundary": (
            "record/hash/decimal-relationship audit; not a second interval backend"
        ),
        "verdict": "g1-g3-bridge-independent-audit-agrees",
    }


def audit_publication(
    manifest_path: Path,
    *,
    publication_root: Path = ROOT,
    evidence_root: Path = ROOT,
) -> dict[str, Any]:
    """Verify a manifest-last publication and independently re-audit its result."""

    root = Path(publication_root).resolve()
    manifest_location = Path(manifest_path).resolve()
    if root not in manifest_location.parents:
        raise ValueError("manifest path escaped publication root")
    manifest = _json(manifest_location)
    if manifest.get("schema") != (
        "scalar-memory-rotating-wave-horizon-g1-g3-publication-v1"
    ):
        raise ValueError("publication schema mismatch")
    rows = manifest.get("artifacts")
    if type(rows) is not list or [row.get("role") for row in rows] != [
        "result-json",
        "readable-report",
        "independent-audit",
    ]:
        raise ValueError("publication artifact order mismatch")
    contents: dict[str, bytes] = {}
    for row in rows:
        relative = row.get("path")
        if type(relative) is not str or not relative or "\\" in relative:
            raise ValueError("invalid publication artifact path")
        path = (root / relative).resolve()
        if root not in path.parents:
            raise ValueError("publication artifact escaped root")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != row.get("sha256"):
            raise ValueError(f"publication artifact hash mismatch: {row['role']}")
        contents[row["role"]] = raw
    result = json.loads(contents["result-json"])
    if type(result) is not dict:
        raise TypeError("published result root must be an object")
    report = audit_payload(result, repository_root=evidence_root)
    publication = result["publication"]
    expected_rows = [
        {"path": publication["artifacts"][0]["path"], "role": "result-json"},
        {"path": publication["artifacts"][1]["path"], "role": "readable-report"},
        {
            "path": publication["auditor_output_path"],
            "role": "independent-audit",
        },
    ]
    if any(
        row["path"] != expected["path"] or row["role"] != expected["role"]
        for row, expected in zip(rows, expected_rows, strict=True)
    ):
        raise ValueError("manifest artifacts do not match result publication paths")
    published_audit = json.loads(contents["independent-audit"])
    if (
        type(published_audit) is not dict
        or published_audit.get("verdict") != report["verdict"]
        or published_audit.get("decision") != report["decision"]
        or published_audit.get("result_sha256")
        != hashlib.sha256(contents["result-json"]).hexdigest()
    ):
        raise ValueError("published independent audit does not bind result")
    readable = contents["readable-report"].decode("utf-8")
    if result["classification"]["decision"] not in readable:
        raise ValueError("readable report does not state reconstructed decision")
    expected_manifest = result["publication"]["manifest_path"]
    if manifest_location.relative_to(root).as_posix() != expected_manifest:
        raise ValueError("payload manifest path mismatch")
    if manifest.get("execution_commit") != result["identity"]["execution_commit"]:
        raise ValueError("manifest execution commit mismatch")
    if manifest.get("protocol_sha256") != result["identity"]["protocol_sha256"]:
        raise ValueError("manifest protocol hash mismatch")
    return {
        **report,
        "manifest_sha256": hashlib.sha256(manifest_location.read_bytes()).hexdigest(),
        "publication_verified": True,
    }
