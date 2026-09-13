"""Independently audit the isolated G4 component publication with stdlib."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PROTOCOL = ROOT / (
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_horizon_g4_component_protocol_2026-09-13.md"
)
RESULT = ROOT / (
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.json"
)
REPORT = RESULT.with_suffix(".md")
MANIFEST = RESULT.with_suffix(".publication.json")
AUDIT_OUTPUT = ROOT / (
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_horizon_g4_component_independent_audit_2026-09-13.json"
)
START = ["0.946517504804225", "0.015770381717135"]
PARAMETERS = {
    "alpha": 0.01,
    "memory_mass": 1.0,
    "eta": 0.15,
    "sigma_rep": 1.0,
    "sigma_att": 3.0,
    "amplitude_rep": 1.0,
    "amplitude_att": 3.5,
    "horizon": 3600,
}
PASS_DECISION = "g4-local-infinite-root-pass"
INCONCLUSIVE_DECISION = "g4-inconclusive"
CLAIM_BOUNDARY = (
    "local F_infinity root conditional on registered tail bounds and "
    "mpmath.iv; no branch-transfer, stability, formation, interaction, or mass claim"
)
_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)


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
    raise TypeError(f"{path}: non-native JSON value")


def _outward_decimal(value: Decimal) -> str:
    rounded = float(value)
    if Decimal.from_float(rounded) < value:
        rounded = math.nextafter(rounded, math.inf)
    return repr(rounded)


def _tail_bounds(precision_dps: int) -> dict[str, Any]:
    with localcontext() as context:
        context.prec = precision_dps
        q = Decimal("0.99")
        eta = Decimal("0.15")
        phi0 = Decimal(1) + Decimal("3.5") / Decimal(9)
        phi1 = (-Decimal("0.5")).exp() * (
            Decimal(1) + Decimal("3.5") / Decimal(27)
        )
        q_power = q**3600
        return {
            "precision_dps": precision_dps,
            "residual_bound": _outward_decimal(2 * eta * phi0 * q_power),
            "jacobian_radius_bound": _outward_decimal(4 * eta * phi1 * q_power),
            "jacobian_theta_bound": _outward_decimal(
                eta
                * (phi0 + 2 * Decimal("1.1") * phi1)
                * q_power
                * (Decimal(3600) + q / Decimal("0.01"))
            ),
        }


def _interval(values: Any, *, path: str) -> tuple[Decimal, Decimal]:
    if type(values) is not list or len(values) != 2 or any(
        type(value) is not str for value in values
    ):
        raise TypeError(f"{path}: expected two decimal strings")
    lower, upper = (Decimal(value) for value in values)
    if not (lower.is_finite() and upper.is_finite() and lower <= upper):
        raise ValueError(f"{path}: invalid interval")
    return lower, upper


def _decimal_vector(value: Any, *, path: str) -> list[Decimal]:
    if type(value) is not list or len(value) != 2 or any(
        type(item) is not str for item in value
    ):
        raise TypeError(f"{path}: expected two decimal strings")
    result = [Decimal(item) for item in value]
    if not all(item.is_finite() for item in result):
        raise ValueError(f"{path}: nonfinite value")
    return result


def _decimal_matrix(value: Any, *, path: str) -> list[list[Decimal]]:
    if type(value) is not list or len(value) != 2:
        raise TypeError(f"{path}: expected a 2x2 decimal-string matrix")
    return [
        _decimal_vector(row, path=f"{path}[{index}]")
        for index, row in enumerate(value)
    ]


def _certificate(
    value: Any,
    *,
    root: list[str],
    half_width: str,
    precision_dps: int,
    path: str,
) -> bool:
    if type(value) is not dict or set(value) != {
        "box",
        "interval_backend",
        "jacobian_box",
        "krawczyk_image",
        "strict_interior",
    }:
        raise ValueError(f"{path}: fields mismatch")
    if value["interval_backend"] != "mpmath.iv" or value["strict_interior"] is not True:
        return False
    if set(value["box"]) != {"radius", "theta"}:
        raise ValueError(f"{path}.box: fields mismatch")
    if type(value["krawczyk_image"]) is not list or len(value["krawczyk_image"]) != 2:
        raise ValueError(f"{path}.krawczyk_image: dimensionality mismatch")
    width = Decimal(half_width)
    for index, coordinate in enumerate(("radius", "theta")):
        box = _interval(value["box"][coordinate], path=f"{path}.box.{coordinate}")
        center = Decimal(root[index])
        with localcontext() as context:
            context.prec = 200
            expected_lower = center - width
            expected_upper = center + width
            serialization_tolerance = max(abs(center), Decimal(1)).scaleb(
                4 - precision_dps
            )
        if not (
            box[0] <= expected_lower
            and expected_upper <= box[1]
            and expected_lower - box[0] <= serialization_tolerance
            and box[1] - expected_upper <= serialization_tolerance
        ):
            raise ValueError(f"{path}.box.{coordinate}: registration mismatch")
        image = _interval(
            value["krawczyk_image"][index],
            path=f"{path}.krawczyk_image[{index}]",
        )
        if not box[0] < image[0] <= image[1] < box[1]:
            return False
    jacobian = value["jacobian_box"]
    if type(jacobian) is not list or len(jacobian) != 2:
        raise ValueError(f"{path}.jacobian_box: dimensionality mismatch")
    for row_index, row in enumerate(jacobian):
        if type(row) is not list or len(row) != 2:
            raise ValueError(f"{path}.jacobian_box: dimensionality mismatch")
        for column_index, item in enumerate(row):
            _interval(item, path=f"{path}.jacobian_box[{row_index}][{column_index}]")
    return True


def _intersection(first: Any, second: Any) -> dict[str, list[str]] | None:
    result = {}
    for index, coordinate in enumerate(("radius", "theta")):
        first_interval = _interval(first[index], path=f"first[{index}]")
        second_interval = _interval(second[index], path=f"second[{index}]")
        lower = max(first_interval[0], second_interval[0])
        upper = min(first_interval[1], second_interval[1])
        if lower > upper:
            return None
        result[coordinate] = [format(lower, "f"), format(upper, "f")]
    return result


def _expected_report(payload: dict[str, Any]) -> str:
    panels = payload["infinite_tail"]["certificate_panels"]
    lines = [
        "# Isolated G4 infinite-tail component result",
        "",
        f"Decision: **`{payload['classification']['decision']}`**.",
        "",
        "## Measured",
        "",
        "The fixed H=3600 finite root and the preregistered 120/160-dps ",
        "tail-augmented Krawczyk panels were evaluated without parameter search.",
        "",
    ]
    if payload["finite_root"] is not None:
        root = payload["finite_root"]["newton"]
        lines.extend(
            [
                f"- finite root radius: `{root['radius']}`",
                f"- finite root theta: `{root['theta']}`",
            ]
        )
    lines.extend(
        [
            f"- completed tail panels: `{sum(panel is not None for panel in panels)}/2`",
            f"- panel overlap: `{payload['infinite_tail']['panel_comparison']['overlap']}`",
            "",
            "## Claim boundary",
            "",
            payload["classification"]["claim_boundary"] + ".",
            "",
            "A failed panel would be inconclusive, not a nonexistence proof. The",
            "standard-library audit checks record relations and hashes but is not",
            "a second interval backend.",
            "",
        ]
    )
    return "\n".join(lines)


def _verify_manifest() -> tuple[dict[str, Any], dict[str, bytes]]:
    if not MANIFEST.is_file():
        raise FileNotFoundError("publication manifest is missing")
    manifest = _load_json(MANIFEST)
    if set(manifest) != {"schema", "execution_commit", "protocol_sha256", "artifacts"}:
        raise ValueError("manifest fields mismatch")
    if manifest["schema"] != "scalar-memory-rotating-wave-horizon-g4-publication-v1":
        raise ValueError("manifest schema mismatch")
    if not _SHA1.fullmatch(manifest["execution_commit"]):
        raise ValueError("manifest execution commit invalid")
    if not _SHA256.fullmatch(manifest["protocol_sha256"]):
        raise ValueError("manifest protocol hash invalid")
    expected = [(RESULT, "result-json"), (REPORT, "readable-report")]
    if type(manifest["artifacts"]) is not list or len(manifest["artifacts"]) != 2:
        raise ValueError("manifest artifacts mismatch")
    contents = {}
    for record, (path, role) in zip(manifest["artifacts"], expected, strict=True):
        if set(record) != {"path", "role", "sha256"}:
            raise ValueError("manifest artifact fields mismatch")
        if record["path"] != path.name or record["role"] != role:
            raise ValueError("manifest artifact binding mismatch")
        content = path.read_bytes()
        if record["sha256"] != _sha256(content):
            raise ValueError(f"manifest hash mismatch: {path.name}")
        contents[role] = content
    if manifest["protocol_sha256"] != _sha256(PROTOCOL.read_bytes()):
        raise ValueError("manifest protocol hash mismatch")
    return manifest, contents


def audit() -> dict[str, Any]:
    manifest, contents = _verify_manifest()
    payload = json.loads(contents["result-json"], parse_constant=_reject_constant)
    _native_json(payload)
    checks = {
        "manifest_first_and_hashes": True,
        "root_contract": False,
        "registered_identity": False,
        "finite_root_certificate": False,
        "tail_bounds": False,
        "tail_certificates_and_overlap": False,
        "decision_reconstructed": False,
        "readable_report_reconstructed": False,
    }
    if set(payload) != {
        "identity",
        "finite_root",
        "infinite_tail",
        "classification",
        "publication",
    }:
        raise ValueError("payload root fields mismatch")
    checks["root_contract"] = True
    identity = payload["identity"]
    if set(identity) != {
        "schema",
        "created_utc",
        "execution_commit",
        "protocol_path",
        "protocol_sha256",
        "dependencies",
        "parameters",
        "start",
    }:
        raise ValueError("identity fields mismatch")
    if (
        identity["schema"] != "scalar-memory-rotating-wave-horizon-g4-component-v1"
        or identity["execution_commit"] != manifest["execution_commit"]
        or identity["protocol_sha256"] != manifest["protocol_sha256"]
        or identity["protocol_path"]
        != "reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_g4_component_protocol_2026-09-13.md"
        or identity["dependencies"] != {"mpmath": "1.3.0"}
        or identity["parameters"] != PARAMETERS
        or identity["start"] != START
    ):
        raise ValueError("registered identity mismatch")
    if type(identity["created_utc"]) is not str:
        raise ValueError("created timestamp invalid")
    try:
        created = datetime.fromisoformat(identity["created_utc"])
    except ValueError as error:
        raise ValueError("created timestamp invalid") from error
    if created.tzinfo is None or created.utcoffset() != UTC.utcoffset(created):
        raise ValueError("created timestamp is not UTC")
    checks["registered_identity"] = True

    finite = payload["finite_root"]
    finite_ok = False
    root = None
    if finite is not None:
        if set(finite) != {"newton", "outer_certificate", "inner_certificate"}:
            raise ValueError("finite root fields mismatch")
        newton = finite["newton"]
        if set(newton) != {
            "jacobian",
            "precision_dps",
            "radius",
            "residual",
            "steps",
            "theta",
        }:
            raise ValueError("finite Newton fields mismatch")
        if newton["precision_dps"] != 120 or newton["steps"] != 8:
            raise ValueError("finite Newton registration mismatch")
        root = [newton["radius"], newton["theta"]]
        _decimal_vector(root, path="finite.newton.root")
        _decimal_vector(newton["residual"], path="finite.newton.residual")
        _decimal_matrix(newton["jacobian"], path="finite.newton.jacobian")
        finite_ok = _certificate(
            finite["outer_certificate"],
            root=root,
            half_width="1e-8",
            precision_dps=120,
            path="outer",
        ) and _certificate(
            finite["inner_certificate"],
            root=root,
            half_width="1e-30",
            precision_dps=120,
            path="inner",
        )
    checks["finite_root_certificate"] = finite_ok

    tail = payload["infinite_tail"]
    if set(tail) != {"bounds", "certificate_panels", "panel_comparison"}:
        raise ValueError("infinite tail fields mismatch")
    if tail["bounds"] != [_tail_bounds(120), _tail_bounds(160)]:
        raise ValueError("tail bounds mismatch")
    checks["tail_bounds"] = True
    panels = tail["certificate_panels"]
    if type(panels) is not list or len(panels) != 2:
        raise ValueError("tail panel count mismatch")
    panel_ok = []
    nonnull = 0
    for index, panel in enumerate(panels):
        if panel is None:
            panel_ok.append(False)
            continue
        if index != nonnull or root is None:
            raise ValueError("tail panels are not a valid completed prefix")
        nonnull += 1
        if type(panel) is not dict or set(panel) != {
            "certificate",
            "precision_dps",
            "root",
        }:
            raise ValueError("tail panel fields mismatch")
        if panel["precision_dps"] != (120, 160)[index] or panel["root"] != root:
            raise ValueError("tail panel binding mismatch")
        panel_ok.append(
            _certificate(
                panel["certificate"],
                root=root,
                half_width="1e-10",
                precision_dps=(120, 160)[index],
                path=f"tail[{index}]",
            )
        )
    if all(panel is not None for panel in panels):
        intersection = _intersection(
            panels[0]["certificate"]["krawczyk_image"],
            panels[1]["certificate"]["krawczyk_image"],
        )
        expected_comparison = {"intersection": intersection, "overlap": intersection is not None}
    else:
        expected_comparison = {"intersection": None, "overlap": False}
    if tail["panel_comparison"] != expected_comparison:
        raise ValueError("tail panel comparison mismatch")
    tail_ok = bool(all(panel_ok) and expected_comparison["overlap"])
    checks["tail_certificates_and_overlap"] = tail_ok
    passed = bool(finite_ok and tail_ok)
    expected_classification = {
        "G4": "pass" if passed else "inconclusive",
        "decision": PASS_DECISION if passed else INCONCLUSIVE_DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if payload["classification"] != expected_classification:
        raise ValueError("classification mismatch")
    if payload["publication"] != {
        "artifacts": [
            {"path": RESULT.name, "role": "result-json"},
            {"path": REPORT.name, "role": "readable-report"},
        ],
        "manifest_path": MANIFEST.name,
        "manifest_published_last": True,
    }:
        raise ValueError("publication contract mismatch")
    checks["decision_reconstructed"] = True
    if contents["readable-report"].decode("utf-8") != _expected_report(payload):
        raise ValueError("readable report does not match result record")
    checks["readable_report_reconstructed"] = True
    return {
        "schema": "scalar-memory-rotating-wave-horizon-g4-independent-audit-v1",
        "result_sha256": _sha256(contents["result-json"]),
        "execution_commit": identity["execution_commit"],
        "checks": checks,
        "decision": payload["classification"]["decision"],
        "verdict": "g4-independent-audit-agrees",
        "trust_boundary": "record and hash audit; not a second interval backend",
    }


def main() -> None:
    result = audit()
    AUDIT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"Verdict: {result['verdict']}")
    print(f"Decision: {result['decision']}")


if __name__ == "__main__":
    main()
