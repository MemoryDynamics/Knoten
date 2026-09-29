"""Independent stdlib audit for the uniform infinity branch-link record."""

from __future__ import annotations

from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[4]
RESULT = ROOT / (
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_2026-09-29.json"
)
REPORT = RESULT.with_suffix(".md")
MANIFEST = RESULT.with_suffix(".publication.json")
AUDIT_OUTPUT = ROOT / (
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_independent_audit_2026-09-29.json"
)
SCHEMA = "scalar-memory-rotating-wave-horizon-infinity-branch-link-v1"
PASS_DECISION = "g-infinity-uniform-tail-branch-link-pass"
INCONCLUSIVE_DECISION = "g-infinity-branch-link-inconclusive"
CLAIM_BOUNDARY = (
    "local uniform root-branch continuation from finite H=3600 to F_infinity "
    "under registered tail bounds and mpmath.iv; no H-infinity stability, "
    "global uniqueness, formation, interaction, spin, inertia or mass"
)
PROTOCOL_BLOB = "adf008c12cd698d61ac22f8edbd62d7e6771ac1b"
PROTOCOL_SHA256 = "4bba4b87b805e5d7238092782f59431b2e6e3cf4f7bf7115add8cacf4fe61be2"
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
PRECISIONS = (120, 160)
HALF_WIDTH = Decimal("1e-10")
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
_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_UUID4 = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z"
)


def _reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def _load_json_bytes(content: bytes) -> Any:
    return json.loads(content.decode("utf-8"), parse_constant=_reject_constant)


def _native_json(value: Any, *, path: str = "$") -> None:
    if value is None or type(value) in (str, bool, int):
        return
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError(f"{path}: nonfinite float")
        return
    if type(value) is list:
        for index, item in enumerate(value):
            _native_json(item, path=f"{path}[{index}]")
        return
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise TypeError(f"{path}: non-string key")
        for key, item in value.items():
            _native_json(item, path=f"{path}.{key}")
        return
    raise TypeError(f"{path}: non-native JSON type")


def _exact_fields(value: Any, expected: set[str], *, path: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != expected:
        raise ValueError(f"{path}: fields mismatch")
    return value


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


def _root_box(value: Any, *, path: str) -> dict[str, Any]:
    value = _exact_fields(value, {"radius", "theta"}, path=path)
    _pair(value["radius"], path=f"{path}.radius")
    _pair(value["theta"], path=f"{path}.theta")
    return value


def _image_in_box(image: Any, box: dict[str, Any], *, path: str) -> bool:
    if type(image) is not list or len(image) != 2:
        raise TypeError(f"{path}: expected two image intervals")
    for index, coordinate in enumerate(("radius", "theta")):
        image_pair = _pair(image[index], path=f"{path}[{index}]")
        box_pair = _pair(box[coordinate], path=f"box.{coordinate}")
        if not box_pair[0] < image_pair[0] <= image_pair[1] < box_pair[1]:
            return False
    return True


def _point_in_box(point: Any, box: dict[str, Any], *, path: str) -> bool:
    if type(point) is not list or len(point) != 2:
        raise TypeError(f"{path}: expected point pair")
    for index, coordinate in enumerate(("radius", "theta")):
        lower, upper = _pair(box[coordinate], path=f"box.{coordinate}")
        value = _decimal(point[index], path=f"{path}[{index}]")
        if not lower <= value <= upper:
            return False
    return True


def _boxes_equal(first: Any, second: Any) -> bool:
    first = _root_box(first, path="first_box")
    second = _root_box(second, path="second_box")
    return all(
        _pair(first[name], path=f"first.{name}")
        == _pair(second[name], path=f"second.{name}")
        for name in ("radius", "theta")
    )


def _intersection(first: Any, second: Any) -> dict[str, list[str]] | None:
    if type(first) is not list or type(second) is not list or len(first) != 2 or len(second) != 2:
        raise TypeError("images must be two-dimensional")
    result = {}
    for index, coordinate in enumerate(("radius", "theta")):
        left = _pair(first[index], path=f"first[{index}]")
        right = _pair(second[index], path=f"second[{index}]")
        lower = max(left[0], right[0])
        upper = min(left[1], right[1])
        if lower > upper:
            return None
        result[coordinate] = [format(lower, "f"), format(upper, "f")]
    return result


def _outward_decimal(value: Decimal) -> str:
    rounded = float(value)
    if Decimal.from_float(rounded) < value:
        rounded = math.nextafter(rounded, math.inf)
    return repr(rounded)


def _tail_bounds(precision: int) -> dict[str, Any]:
    with localcontext() as context:
        context.prec = precision
        q = Decimal("0.99")
        eta = Decimal("0.15")
        phi0 = Decimal(1) + Decimal("3.5") / Decimal(9)
        phi1 = (-Decimal("0.5")).exp() * (
            Decimal(1) + Decimal("3.5") / Decimal(27)
        )
        q_power = q**3600
        return {
            "precision_dps": precision,
            "residual_bound": _outward_decimal(2 * eta * phi0 * q_power),
            "jacobian_radius_bound": _outward_decimal(4 * eta * phi1 * q_power),
            "jacobian_theta_bound": _outward_decimal(
                eta
                * (phi0 + 2 * Decimal("1.1") * phi1)
                * q_power
                * (Decimal(3600) + q / Decimal("0.01"))
            ),
        }


def _git_blob_bytes(relative: str) -> bytes:
    return subprocess.run(
        ["git", "cat-file", "blob", f"HEAD:{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def _git_blob_sha256(relative: str) -> str:
    return hashlib.sha256(_git_blob_bytes(relative)).hexdigest()


def _sealed_snapshot_from_git() -> dict[str, Any]:
    documents = {
        role: _load_json_bytes(_git_blob_bytes(path))
        for role, path, _ in SEALED_FILES
    }
    bridge = documents["g1-g3-result"]
    g4 = documents["g4-result"]
    bridge_panel = bridge["finite_branch"]["root_panels"][-1]
    endpoint = next(
        (
            row
            for row in bridge["endpoint_links"]
            if row.get("component") == "G4" and row.get("horizon") == 3600
        ),
        None,
    )
    if endpoint is None:
        raise ValueError("sealed G4 endpoint missing")
    tail_panels = g4["infinite_tail"]["certificate_panels"]
    return {
        "files": [
            {"role": role, "path": path, "sha256": digest}
            for role, path, digest in SEALED_FILES
        ],
        "bridge_root": [
            bridge_panel["newton_120"]["radius"],
            bridge_panel["newton_120"]["theta"],
        ],
        "g4_finite_root": [
            g4["finite_root"]["newton"]["radius"],
            g4["finite_root"]["newton"]["theta"],
        ],
        "bridge_endpoint_pass": endpoint.get("pass") is True,
        "tail_bounds": [_tail_bounds(value) for value in PRECISIONS],
        "g4_tail_boxes": [
            panel["certificate"]["box"] for panel in tail_panels
        ],
        "g4_tail_images": [
            panel["certificate"]["krawczyk_image"] for panel in tail_panels
        ],
    }


def _row_norm_upper(row: Any, *, path: str) -> Decimal:
    if type(row) is not list or len(row) != 2:
        raise TypeError(f"{path}: expected two intervals")
    return sum(max(abs(lower), abs(upper)) for lower, upper in (_pair(value, path=f"{path}[{index}]") for index, value in enumerate(row)))


def _validate_panel(panel: Any, *, index: int, sealed: dict[str, Any]) -> dict[str, Any]:
    panel = _exact_fields(
        panel,
        {
            "box",
            "center",
            "gates",
            "inverse_point_jacobian",
            "jacobian_box",
            "krawczyk_image",
            "pass",
            "precision_dps",
            "preconditioned_jacobian_defect",
            "regularity_infinity_norm_upper",
            "regularity_row_sum_bounds",
            "scale_interval",
            "tail_bounds",
        },
        path=f"$.homotopy.panels[{index}]",
    )
    precision = PRECISIONS[index]
    if (
        panel["precision_dps"] != precision
        or panel["scale_interval"] != ["0", "1"]
        or panel["center"] != sealed["g4_finite_root"]
        or panel["tail_bounds"] != _tail_bounds(precision)
    ):
        raise ValueError("panel registration mismatch")
    box = _root_box(panel["box"], path="panel.box")
    for coordinate_index, coordinate in enumerate(("radius", "theta")):
        lower, upper = _pair(box[coordinate], path=f"panel.box.{coordinate}")
        center = _decimal(panel["center"][coordinate_index], path="panel.center")
        with localcontext() as context:
            context.prec = 200
            expected_lower = center - HALF_WIDTH
            expected_upper = center + HALF_WIDTH
            tolerance = max(abs(center), Decimal(1)).scaleb(4 - precision)
        if not (
            lower <= expected_lower
            and expected_upper <= upper
            and expected_lower - lower <= tolerance
            and upper - expected_upper <= tolerance
        ):
            raise ValueError("panel box mismatch")
    strict = _image_in_box(panel["krawczyk_image"], box, path="panel.image")
    defect = panel["preconditioned_jacobian_defect"]
    if type(defect) is not list or len(defect) != 2:
        raise TypeError("panel defect dimensionality mismatch")
    row_uppers = [
        _row_norm_upper(row, path=f"panel.defect[{row_index}]")
        for row_index, row in enumerate(defect)
    ]
    row_bounds = panel["regularity_row_sum_bounds"]
    if type(row_bounds) is not list or len(row_bounds) != 2:
        raise TypeError("panel row bounds dimensionality mismatch")
    recorded_rows = [
        _pair(value, path=f"panel.row_bounds[{row_index}]")
        for row_index, value in enumerate(row_bounds)
    ]
    if any(recorded[1] < observed for recorded, observed in zip(recorded_rows, row_uppers, strict=True)):
        raise ValueError("inward regularity bound")
    regularity_upper = max(value[1] for value in recorded_rows)
    if _decimal(panel["regularity_infinity_norm_upper"], path="panel.regularity") != regularity_upper:
        raise ValueError("regularity summary mismatch")
    regular = regularity_upper < 1
    gates = _exact_fields(
        panel["gates"],
        {
            "function_box_contains_zero",
            "inverse_nonsingular",
            "krawczyk_strict_interior",
            "physical_domain",
            "uniform_regularity",
        },
        path="panel.gates",
    )
    if any(type(value) is not bool for value in gates.values()):
        raise TypeError("panel gate must be boolean")
    if gates["krawczyk_strict_interior"] is not strict or gates["uniform_regularity"] is not regular:
        raise ValueError("panel gate summary mismatch")
    if panel["pass"] is not all(gates.values()):
        raise ValueError("panel pass mismatch")
    for matrix_name in ("jacobian_box", "preconditioned_jacobian_defect"):
        matrix = panel[matrix_name]
        if type(matrix) is not list or len(matrix) != 2 or any(type(row) is not list or len(row) != 2 for row in matrix):
            raise TypeError(f"{matrix_name}: dimensionality mismatch")
        for row_index, row in enumerate(matrix):
            for column_index, value in enumerate(row):
                _pair(value, path=f"{matrix_name}[{row_index}][{column_index}]")
    inverse = panel["inverse_point_jacobian"]
    if type(inverse) is not list or len(inverse) != 2 or any(type(row) is not list or len(row) != 2 for row in inverse):
        raise TypeError("inverse dimensionality mismatch")
    for row_index, row in enumerate(inverse):
        for column_index, value in enumerate(row):
            _decimal(value, path=f"inverse[{row_index}][{column_index}]")
    return {"strict": strict, "regular": regular, "pass": panel["pass"]}


def _expected_report(payload: dict[str, Any]) -> str:
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


def audit_payload_bytes(
    result_bytes: bytes,
    report_bytes: bytes,
    *,
    sealed_reference: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Audit a candidate publication without importing production code."""

    payload = _load_json_bytes(result_bytes)
    _native_json(payload)
    payload = _exact_fields(
        payload,
        {
            "classification",
            "homotopy",
            "identity",
            "model_identity",
            "publication",
            "sealed_inputs",
        },
        path="$",
    )
    identity = _exact_fields(
        payload["identity"],
        {
            "authorization",
            "created_utc",
            "execution_commit",
            "parameters",
            "protocol_blob",
            "protocol_sha256",
            "schema",
            "version",
        },
        path="$.identity",
    )
    if (
        identity["schema"] != SCHEMA
        or identity["version"] != 1
        or identity["protocol_blob"] != PROTOCOL_BLOB
        or identity["protocol_sha256"] != PROTOCOL_SHA256
        or identity["parameters"] != PARAMETERS
        or type(identity["created_utc"]) is not str
        or _SHA1.fullmatch(identity["execution_commit"]) is None
    ):
        raise ValueError("identity mismatch")
    authorization = _exact_fields(
        identity["authorization"],
        {
            "authorization_id",
            "ci_run_id",
            "governance_sha256",
            "implementation_revision",
            "receipt_path",
            "receipt_sha256",
            "upstream_revision",
        },
        path="$.identity.authorization",
    )
    if (
        _UUID4.fullmatch(authorization["authorization_id"]) is None
        or type(authorization["ci_run_id"]) is not int
        or _SHA256.fullmatch(authorization["governance_sha256"]) is None
        or _SHA1.fullmatch(authorization["implementation_revision"]) is None
        or type(authorization["receipt_path"]) is not str
        or _SHA256.fullmatch(authorization["receipt_sha256"]) is None
        or _SHA1.fullmatch(authorization["upstream_revision"]) is None
    ):
        raise ValueError("authorization mismatch")

    sealed = _exact_fields(
        payload["sealed_inputs"],
        {
            "bridge_endpoint_pass",
            "bridge_root",
            "files",
            "g4_finite_root",
            "g4_tail_boxes",
            "g4_tail_images",
            "tail_bounds",
        },
        path="$.sealed_inputs",
    )
    expected_sealed = sealed_reference or _sealed_snapshot_from_git()
    if sealed != expected_sealed:
        raise ValueError("sealed Git-blob snapshot mismatch")
    expected_files = [
        {"role": role, "path": path, "sha256": digest}
        for role, path, digest in SEALED_FILES
    ]
    if sealed["files"] != expected_files:
        raise ValueError("sealed file registry mismatch")
    if any(_git_blob_sha256(path) != digest for _, path, digest in SEALED_FILES):
        raise ValueError("sealed Git blob mismatch")
    if sealed["tail_bounds"] != [_tail_bounds(value) for value in PRECISIONS]:
        raise ValueError("tail-bound replay mismatch")
    for root_name in ("bridge_root", "g4_finite_root"):
        if type(sealed[root_name]) is not list or len(sealed[root_name]) != 2:
            raise TypeError("sealed root dimensionality mismatch")
        for index, value in enumerate(sealed[root_name]):
            _decimal(value, path=f"sealed.{root_name}[{index}]")
    if type(sealed["g4_tail_boxes"]) is not list or len(sealed["g4_tail_boxes"]) != 2:
        raise TypeError("sealed tail boxes mismatch")
    if type(sealed["g4_tail_images"]) is not list or len(sealed["g4_tail_images"]) != 2:
        raise TypeError("sealed tail images mismatch")
    for index in range(2):
        _root_box(sealed["g4_tail_boxes"][index], path=f"sealed.tail_box[{index}]")
        if not _image_in_box(sealed["g4_tail_images"][index], sealed["g4_tail_boxes"][index], path=f"sealed.tail_image[{index}]"):
            raise ValueError("sealed G4 tail image is not strict")

    model = _exact_fields(
        payload["model_identity"],
        {
            "finite_endpoint",
            "homotopy_family",
            "infinite_endpoint",
            "scale_interval",
            "tail_bounds_replayed",
        },
        path="$.model_identity",
    )
    if model != {
        "homotopy_family": "F_s=F_3600+s*T_3600",
        "scale_interval": ["0", "1"],
        "finite_endpoint": "F_3600",
        "infinite_endpoint": "F_infinity",
        "tail_bounds_replayed": True,
    }:
        raise ValueError("model identity mismatch")

    homotopy = _exact_fields(
        payload["homotopy"],
        {"endpoint_binding", "intersection", "overlap", "panels"},
        path="$.homotopy",
    )
    panels = homotopy["panels"]
    if type(panels) is not list or len(panels) != 2:
        raise TypeError("panel cardinality mismatch")
    states = []
    nonnull = 0
    for index, panel in enumerate(panels):
        if panel is None:
            states.append(None)
            continue
        if index != nonnull:
            raise ValueError("panels must form a prefix")
        nonnull += 1
        states.append(_validate_panel(panel, index=index, sealed=sealed))
    intersection = None
    if all(panel is not None for panel in panels):
        intersection = _intersection(
            panels[0]["krawczyk_image"], panels[1]["krawczyk_image"]
        )
    if homotopy["intersection"] != intersection or homotopy["overlap"] is not (intersection is not None):
        raise ValueError("homotopy overlap mismatch")

    complete = all(panel is not None for panel in panels)
    endpoint_values = {
        "bridge_endpoint_pass": sealed["bridge_endpoint_pass"] is True,
        "bridge_root_matches_g4": sealed["bridge_root"] == sealed["g4_finite_root"],
        "finite_root_in_uniform_box": bool(complete and all(_point_in_box(sealed["g4_finite_root"], panel["box"], path="finite_root") for panel in panels)),
        "g4_tail_boxes_match_uniform": bool(complete and all(_boxes_equal(sealed["g4_tail_boxes"][index], panels[index]["box"]) for index in range(2))),
        "g4_tail_images_in_uniform_box": bool(complete and all(_image_in_box(sealed["g4_tail_images"][index], panels[index]["box"], path=f"tail_image[{index}]") for index in range(2))),
    }
    expected_endpoint = {**endpoint_values, "pass": all(endpoint_values.values())}
    if homotopy["endpoint_binding"] != expected_endpoint:
        raise ValueError("endpoint binding mismatch")
    expected_gates = {
        "U0": "pass",
        "U1": "pass",
        "U2": "pass" if all(state is not None and state["strict"] for state in states) else "inconclusive",
        "U3": "pass" if all(state is not None and state["regular"] for state in states) else "inconclusive",
        "U4": "pass" if expected_endpoint["pass"] else "inconclusive",
        "U5": "pass" if intersection is not None else "inconclusive",
    }
    expected_decision = PASS_DECISION if all(value == "pass" for value in expected_gates.values()) else INCONCLUSIVE_DECISION
    if payload["classification"] != {
        "gates": expected_gates,
        "decision": expected_decision,
        "claim_boundary": CLAIM_BOUNDARY,
    }:
        raise ValueError("classification mismatch")
    expected_publication = {
        "artifacts": [
            {"path": RESULT.name, "role": "result-json"},
            {"path": REPORT.name, "role": "readable-report"},
        ],
        "auditor_output_path": AUDIT_OUTPUT.relative_to(ROOT).as_posix(),
        "manifest_path": MANIFEST.name,
        "manifest_published_last": True,
    }
    if payload["publication"] != expected_publication:
        raise ValueError("publication registration mismatch")
    expected_report = _expected_report(payload).encode("utf-8")
    if report_bytes != expected_report:
        raise ValueError("readable report mismatch")
    return {
        "schema": "scalar-memory-rotating-wave-horizon-infinity-branch-link-independent-audit-v1",
        "audited_decision": expected_decision,
        "checks": {
            "classification_reconstructed": True,
            "decimal_relations_reconstructed": True,
            "endpoint_binding_reconstructed": True,
            "model_identity_reconstructed": True,
            "report_reconstructed": True,
            "sealed_git_blobs_verified": True,
            "tail_bounds_replayed": True,
        },
        "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
        "report_sha256": hashlib.sha256(report_bytes).hexdigest(),
        "verdict": "g-infinity-branch-link-independent-audit-agrees",
    }


def verify_publication(*, root: Path = ROOT) -> dict[str, Any]:
    repository = Path(root).resolve()
    result = (repository / RESULT.relative_to(ROOT)).read_bytes()
    report = (repository / REPORT.relative_to(ROOT)).read_bytes()
    audit = _load_json_bytes((repository / AUDIT_OUTPUT.relative_to(ROOT)).read_bytes())
    manifest_bytes = (repository / MANIFEST.relative_to(ROOT)).read_bytes()
    manifest = _load_json_bytes(manifest_bytes)
    expected_audit = audit_payload_bytes(result, report)
    if audit != expected_audit:
        raise ValueError("published audit mismatch")
    artifacts = manifest.get("artifacts")
    expected_rows = [
        {"path": RESULT.name, "role": "result-json", "sha256": hashlib.sha256(result).hexdigest()},
        {"path": REPORT.name, "role": "readable-report", "sha256": hashlib.sha256(report).hexdigest()},
        {"path": AUDIT_OUTPUT.relative_to(ROOT).as_posix(), "role": "independent-audit", "sha256": hashlib.sha256((json.dumps(audit, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")).hexdigest()},
    ]
    if artifacts != expected_rows:
        raise ValueError("publication manifest mismatch")
    return {
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "result_sha256": expected_audit["result_sha256"],
        "verdict": expected_audit["verdict"],
    }
