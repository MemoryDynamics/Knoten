"""Post-hoc, read-only reconciliation of the infinity endpoint lemma.

The audit consumes published JSON records only.  It never calls a numerical
backend and never changes the Attempt-4 decision.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import json
import math
from pathlib import Path
import subprocess
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[4]
PROTOCOL = ROOT / (
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_horizon_infinity_endpoint_lemma_"
    "reconciliation_protocol_2026-10-01.md"
)
ATTEMPT_RESULT = ROOT / (
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_"
    "attempt_4_2026-10-01.json"
)
ATTEMPT_MANIFEST = ATTEMPT_RESULT.with_suffix(".publication.json")
ATTEMPT_AUDIT = ROOT / (
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_"
    "attempt_4_independent_audit_2026-10-01.json"
)
ATTEMPT_REVIEW = ROOT / (
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_"
    "attempt_4_result_review_2026-10-01.md"
)
BRIDGE_RESULT = ROOT / (
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g1_g3_bridge_attempt_2_2026-09-27.json"
)
G4_RESULT = ROOT / (
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.json"
)
OUTPUT = ROOT / (
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_infinity_endpoint_lemma_"
    "reconciliation_2026-10-01.json"
)
REPORT = OUTPUT.with_suffix(".md")
PROTOCOL_BLOB = "0b85720fcdac9d31cba964ce743352de1decb1db"
PROTOCOL_SHA256 = "2d1c8c982a1db6763b6711680341ec27bae67b1cdd005e62cf209936a749efaf"
PASS_DECISION = "g-infinity-endpoint-lemma-reconciled-posthoc"
FAIL_DECISION = "g-infinity-endpoint-lemma-not-reconciled"
EXPECTED_BLOBS = {
    PROTOCOL.relative_to(ROOT).as_posix(): PROTOCOL_BLOB,
    ATTEMPT_RESULT.relative_to(ROOT).as_posix(): "fe25d5a4e222d98faa8628882726597bf0455b90",
    ATTEMPT_MANIFEST.relative_to(ROOT).as_posix(): "a39388c2012d94b59f9d214457d98611dd096e4b",
    ATTEMPT_AUDIT.relative_to(ROOT).as_posix(): "9e8790256ec08c75e51b2c26c28c8bdb15c3087b",
    ATTEMPT_REVIEW.relative_to(ROOT).as_posix(): "792d0c66fd79b2f5501b29eadb304e2b50536410",
    BRIDGE_RESULT.relative_to(ROOT).as_posix(): "385a7c736bb2974144dffcea0b11c760f5313a1e",
    G4_RESULT.relative_to(ROOT).as_posix(): "0e6ccaba8665bfcce735f8a8d596224c39fd6323",
}


def _reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)
    if type(value) is not dict:
        raise ValueError(f"{path.name}: JSON root is not an object")
    return value


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
        for key, item in value.items():
            if type(key) is not str:
                raise ValueError(f"{path}: non-string key")
            _native_json(item, path=f"{path}.{key}")
        return
    raise ValueError(f"{path}: non-native JSON value")


def _decimal(value: Any, *, path: str) -> Decimal:
    if type(value) is not str:
        raise ValueError(f"{path}: expected decimal string")
    try:
        result = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{path}: invalid decimal") from error
    if not result.is_finite():
        raise ValueError(f"{path}: nonfinite decimal")
    return result


def _pair(value: Any, *, path: str) -> tuple[Decimal, Decimal]:
    if type(value) is not list or len(value) != 2:
        raise ValueError(f"{path}: expected interval pair")
    lower = _decimal(value[0], path=f"{path}[0]")
    upper = _decimal(value[1], path=f"{path}[1]")
    if lower > upper:
        raise ValueError(f"{path}: reversed interval")
    return lower, upper


def _image_in_box(image: Any, box: Any, *, path: str) -> bool:
    if type(image) is not list or len(image) != 2 or type(box) is not dict:
        raise ValueError(f"{path}: malformed image or box")
    for index, coordinate in enumerate(("radius", "theta")):
        image_lower, image_upper = _pair(image[index], path=f"{path}.image[{index}]")
        box_lower, box_upper = _pair(box[coordinate], path=f"{path}.box.{coordinate}")
        if not (box_lower <= image_lower and image_upper <= box_upper):
            return False
    return True


def _images_equal(left: Any, right: Any, *, path: str) -> bool:
    if type(left) is not list or type(right) is not list or len(left) != len(right):
        raise ValueError(f"{path}: malformed images")
    return all(
        _pair(a, path=f"{path}.left[{index}]")
        == _pair(b, path=f"{path}.right[{index}]")
        for index, (a, b) in enumerate(zip(left, right, strict=True))
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_blob(path: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def verify_git_blobs(blob_fn: Callable[[str], str] = _git_blob) -> bool:
    return all(blob_fn(path) == expected for path, expected in EXPECTED_BLOBS.items())


def verify_manifest(manifest: dict[str, Any]) -> bool:
    if manifest.get("schema") != (
        "scalar-memory-rotating-wave-horizon-infinity-branch-link-publication-v1"
    ):
        return False
    if manifest.get("execution_commit") != "ee87ad931c4c8b27cff2cb44b445459ad4c79511":
        return False
    if manifest.get("protocol_sha256") != (
        "598cdf73a7ccdfa45bd163165c2dd2be54d47209cacdb0b297ce0e05472132cd"
    ):
        return False
    rows = manifest.get("artifacts")
    if type(rows) is not list or len(rows) != 3:
        return False
    expected_roles = {"result-json", "readable-report", "independent-audit"}
    if {row.get("role") for row in rows if type(row) is dict} != expected_roles:
        return False
    for row in rows:
        if type(row) is not dict or type(row.get("path")) is not str:
            return False
        relative = Path(row["path"])
        path = ATTEMPT_RESULT.parent / relative if len(relative.parts) == 1 else ROOT / relative
        if not path.is_file() or _sha256(path) != row.get("sha256"):
            return False
    return True


def _box_differences(attempt: dict[str, Any]) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    panels = attempt["homotopy"]["panels"]
    g4_boxes = attempt["sealed_inputs"]["g4_tail_boxes"]
    with localcontext() as context:
        context.prec = 800
        for index, (panel, g4_box) in enumerate(zip(panels, g4_boxes, strict=True)):
            for coordinate in ("radius", "theta"):
                uniform = panel["box"][coordinate]
                for endpoint in range(2):
                    delta = _decimal(
                        g4_box[coordinate][endpoint], path="g4_box"
                    ) - _decimal(uniform[endpoint], path="uniform_box")
                    rows.append(
                        {
                            "coordinate": coordinate,
                            "delta_g4_minus_uniform": format(delta, "E"),
                            "endpoint": endpoint,
                            "precision_dps": panel["precision_dps"],
                        }
                    )
    return rows


def reconcile_records(
    attempt: dict[str, Any],
    bridge: dict[str, Any],
    g4: dict[str, Any],
    attempt_audit: dict[str, Any],
    *,
    provenance_pass: bool,
    created_utc: str | None = None,
) -> dict[str, Any]:
    for value in (attempt, bridge, g4, attempt_audit):
        _native_json(value)

    panels = attempt["homotopy"]["panels"]
    expected_u = {
        "U0": "pass",
        "U1": "pass",
        "U2": "pass",
        "U3": "pass",
        "U4": "inconclusive",
        "U5": "pass",
    }
    attempt_unchanged = (
        attempt["classification"]["decision"]
        == "g-infinity-branch-link-inconclusive"
        and attempt["classification"]["gates"] == expected_u
        and type(panels) is list
        and len(panels) == 2
        and all(type(panel) is dict and panel.get("pass") is True for panel in panels)
    )
    audit_agrees = (
        attempt_audit.get("verdict")
        == "g-infinity-branch-link-independent-audit-agrees"
        and attempt_audit.get("audited_decision")
        == "g-infinity-branch-link-inconclusive"
        and type(attempt_audit.get("checks")) is dict
        and all(attempt_audit["checks"].values())
    )
    regularity_values = [
        _decimal(panel["regularity_infinity_norm_upper"], path="regularity")
        for panel in panels
    ]
    uniform_unique = all(
        panel["gates"]["krawczyk_strict_interior"] is True
        and panel["gates"]["uniform_regularity"] is True
        and value < 1
        for panel, value in zip(panels, regularity_values, strict=True)
    )

    bridge_panel = next(
        row for row in bridge["finite_branch"]["root_panels"] if row["horizon"] == 3600
    )
    bridge_link = next(
        row for row in bridge["endpoint_links"] if row["component"] == "G4"
    )
    finite_images = [
        bridge_panel["inner_certificate_80"]["krawczyk_image"],
        bridge_panel["inner_certificate_120"]["krawczyk_image"],
    ]
    finite_inclusions = [
        _image_in_box(
            image,
            panel["box"],
            path=f"finite[{image_index}].uniform[{panel_index}]",
        )
        for image_index, image in enumerate(finite_images)
        for panel_index, panel in enumerate(panels)
    ]
    bridge_root = [
        bridge_panel["newton_120"]["radius"],
        bridge_panel["newton_120"]["theta"],
    ]
    finite_endpoint = (
        bridge["classification"]["gates"]["H3600_link"] == "pass"
        and bridge_link["pass"] is True
        and bridge_root == attempt["sealed_inputs"]["bridge_root"]
        and attempt["sealed_inputs"]["bridge_root"]
        == attempt["sealed_inputs"]["g4_finite_root"]
        and all(finite_inclusions)
    )

    g4_panels = g4["infinite_tail"]["certificate_panels"]
    sealed_g4_images = attempt["sealed_inputs"]["g4_tail_images"]
    g4_record_images = [row["certificate"]["krawczyk_image"] for row in g4_panels]
    g4_image_consistency = [
        _images_equal(recorded, sealed, path=f"g4_image[{index}]")
        for index, (recorded, sealed) in enumerate(
            zip(g4_record_images, sealed_g4_images, strict=True)
        )
    ]
    infinite_inclusions = [
        _image_in_box(image, panels[index]["box"], path=f"infinite[{index}]")
        for index, image in enumerate(sealed_g4_images)
    ]
    infinite_endpoint = (
        g4["classification"]["G4"] == "pass"
        and g4["classification"]["decision"] == "g4-local-infinite-root-pass"
        and all(row["certificate"]["strict_interior"] is True for row in g4_panels)
        and all(g4_image_consistency)
        and all(infinite_inclusions)
    )

    boxes_differ = any(
        g4_box != panel["box"]
        for g4_box, panel in zip(
            attempt["sealed_inputs"]["g4_tail_boxes"], panels, strict=True
        )
    )
    exact_reproduction = all(finite_inclusions + infinite_inclusions + g4_image_consistency)
    gates = {
        "R0": "pass" if provenance_pass and audit_agrees else "fail",
        "R1": "pass" if attempt_unchanged else "fail",
        "R2": "pass" if uniform_unique else "fail",
        "R3": "pass" if finite_endpoint else "fail",
        "R4": "pass" if infinite_endpoint else "fail",
        "R5": "pass" if boxes_differ else "fail",
        "R6": "pass" if exact_reproduction else "fail",
    }
    decision = PASS_DECISION if all(value == "pass" for value in gates.values()) else FAIL_DECISION
    return {
        "schema": "scalar-memory-rotating-wave-infinity-endpoint-lemma-reconciliation-v1",
        "created_utc": created_utc or datetime.now(UTC).isoformat(),
        "protocol_blob": PROTOCOL_BLOB,
        "protocol_sha256": PROTOCOL_SHA256,
        "evidence_classification": "outcome-informed-posthoc-reconciliation",
        "source_attempt_decision": attempt["classification"]["decision"],
        "source_attempt_decision_unchanged": True,
        "gates": gates,
        "decision": decision,
        "diagnostics": {
            "box_endpoint_deltas": _box_differences(attempt),
            "boxes_byte_equal": not boxes_differ,
            "finite_image_in_uniform_box": finite_inclusions,
            "g4_image_matches_sealed_snapshot": g4_image_consistency,
            "g4_image_in_uniform_box": infinite_inclusions,
            "regularity_infinity_norm_upper": [format(value, "f") for value in regularity_values],
        },
        "claim_boundary": (
            "post-hoc endpoint-identity reconciliation from already published "
            "Krawczyk-image inclusions; Attempt 4 remains inconclusive; no "
            "independent interval backend or H-infinity stability claim"
        ),
    }


def render_report(record: dict[str, Any]) -> str:
    lines = [
        "# Infinity endpoint-lemma reconciliation",
        "",
        f"Decision: **`{record['decision']}`**.",
        "",
        "Evidence class: **outcome-informed post-hoc reconciliation**.",
        "",
        "The Attempt-4 decision remains **`g-infinity-branch-link-inconclusive`**.",
        "",
        "## Gates",
        "",
    ]
    lines.extend(f"- {name}: `{value}`" for name, value in record["gates"].items())
    lines.extend(
        [
            "",
            "## Discriminating relations",
            "",
            f"- exact G4/uniform box text equality: `{record['diagnostics']['boxes_byte_equal']}`",
            "- finite certified images in both uniform boxes: "
            f"`{all(record['diagnostics']['finite_image_in_uniform_box'])}`",
            "- G4 certified images in corresponding uniform boxes: "
            f"`{all(record['diagnostics']['g4_image_in_uniform_box'])}`",
            "",
            "## Claim boundary",
            "",
            record["claim_boundary"] + ".",
            "",
        ]
    )
    return "\n".join(lines)


def run() -> dict[str, Any]:
    if OUTPUT.exists() or REPORT.exists():
        raise RuntimeError("endpoint reconciliation output already exists")
    provenance_pass = verify_git_blobs()
    if hashlib.sha256(PROTOCOL.read_bytes()).hexdigest() != PROTOCOL_SHA256:
        provenance_pass = False
    manifest = _load_json(ATTEMPT_MANIFEST)
    provenance_pass = provenance_pass and verify_manifest(manifest)
    record = reconcile_records(
        _load_json(ATTEMPT_RESULT),
        _load_json(BRIDGE_RESULT),
        _load_json(G4_RESULT),
        _load_json(ATTEMPT_AUDIT),
        provenance_pass=provenance_pass,
    )
    _native_json(record)
    OUTPUT.write_text(
        json.dumps(record, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    REPORT.write_text(render_report(record), encoding="utf-8", newline="\n")
    return record


if __name__ == "__main__":
    result = run()
    print(f"Decision: {result['decision']}")
