"""Execute the preregistered isolated G4 infinite-tail component gate."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal, localcontext
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import subprocess
from typing import Any, Callable

import mpmath


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PROTOCOL = ROOT / (
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_horizon_g4_component_retry_protocol_2026-09-13.md"
)
HORIZON_GATE_PATH = Path(__file__).with_name(
    "scalar_memory_rotating_wave_horizon_transfer_gate.py"
)
RESULT = ROOT / (
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.json"
)
REPORT = RESULT.with_suffix(".md")
MANIFEST = RESULT.with_suffix(".publication.json")
START = ("0.946517504804225", "0.015770381717135")
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
SCHEMA = "scalar-memory-rotating-wave-horizon-g4-component-v1"
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def _load_horizon_gate() -> Any:
    specification = importlib.util.spec_from_file_location(
        "horizon_transfer_gate_for_g4", HORIZON_GATE_PATH
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load horizon-transfer gate")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _git_output(*arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _protocol_sha256() -> str:
    return _sha256_bytes(PROTOCOL.read_bytes())


def require_execution_context() -> tuple[str, str]:
    """Return the clean execution commit and tracked protocol hash."""

    if mpmath.__version__ != "1.3.0":
        raise RuntimeError("G4 requires mpmath 1.3.0")
    if _git_output("status", "--porcelain", "--untracked-files=all"):
        raise RuntimeError("G4 execution requires a clean worktree")
    relative_protocol = PROTOCOL.relative_to(ROOT).as_posix()
    tracked = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{relative_protocol}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if tracked.returncode != 0:
        raise RuntimeError("G4 protocol is not tracked in HEAD")
    committed_protocol = subprocess.run(
        ["git", "show", f"HEAD:{relative_protocol}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    if committed_protocol != PROTOCOL.read_bytes():
        raise RuntimeError("working protocol differs from HEAD")
    for path in (RESULT, REPORT, MANIFEST):
        if path.exists():
            raise RuntimeError(f"refusing to overwrite existing G4 artifact: {path.name}")
    return _git_output("rev-parse", "HEAD"), _protocol_sha256()


def _decimal_interval(values: list[str], *, path: str) -> tuple[Decimal, Decimal]:
    if type(values) is not list or len(values) != 2 or any(
        type(value) is not str for value in values
    ):
        raise TypeError(f"{path} must be two decimal strings")
    lower, upper = (Decimal(value) for value in values)
    if not (lower.is_finite() and upper.is_finite() and lower <= upper):
        raise ValueError(f"{path} must be finite and ordered")
    return lower, upper


def _decimal_vector(value: Any, *, path: str) -> list[Decimal]:
    if type(value) is not list or len(value) != 2 or any(
        type(item) is not str for item in value
    ):
        raise TypeError(f"{path} must be two decimal strings")
    result = [Decimal(item) for item in value]
    if not all(item.is_finite() for item in result):
        raise ValueError(f"{path} must be finite")
    return result


def _decimal_matrix(value: Any, *, path: str) -> list[list[Decimal]]:
    if type(value) is not list or len(value) != 2:
        raise TypeError(f"{path} must be a 2x2 decimal-string matrix")
    return [
        _decimal_vector(row, path=f"{path}[{index}]")
        for index, row in enumerate(value)
    ]


def _strict_certificate(
    certificate: dict[str, Any],
    *,
    root: list[str],
    half_width: str,
    precision_dps: int,
    path: str,
) -> bool:
    if set(certificate) != {
        "box",
        "interval_backend",
        "jacobian_box",
        "krawczyk_image",
        "strict_interior",
    }:
        raise ValueError(f"{path}: certificate fields mismatch")
    if certificate["interval_backend"] != "mpmath.iv":
        raise ValueError(f"{path}: interval backend mismatch")
    if certificate["strict_interior"] is not True:
        return False
    if set(certificate["box"]) != {"radius", "theta"}:
        raise ValueError(f"{path}.box: fields mismatch")
    for index, coordinate in enumerate(("radius", "theta")):
        lower, upper = _decimal_interval(
            certificate["box"][coordinate], path=f"{path}.box.{coordinate}"
        )
        center = Decimal(root[index])
        width = Decimal(half_width)
        with localcontext() as context:
            context.prec = 200
            expected_lower = center - width
            expected_upper = center + width
            serialization_tolerance = max(abs(center), Decimal(1)).scaleb(
                4 - precision_dps
            )
        if not (
            lower <= expected_lower
            and expected_upper <= upper
            and expected_lower - lower <= serialization_tolerance
            and upper - expected_upper <= serialization_tolerance
        ):
            raise ValueError(f"{path}.box.{coordinate}: registered box mismatch")
        image_lower, image_upper = _decimal_interval(
            certificate["krawczyk_image"][index],
            path=f"{path}.krawczyk_image[{index}]",
        )
        if not lower < image_lower <= image_upper < upper:
            return False
    jacobian = certificate["jacobian_box"]
    if type(jacobian) is not list or len(jacobian) != 2:
        raise ValueError(f"{path}.jacobian_box: dimensionality mismatch")
    for row_index, row in enumerate(jacobian):
        if type(row) is not list or len(row) != 2:
            raise ValueError(f"{path}.jacobian_box: dimensionality mismatch")
        for column_index, value in enumerate(row):
            _decimal_interval(
                value,
                path=f"{path}.jacobian_box[{row_index}][{column_index}]",
            )
    return True


def _image_intersection(
    first: list[list[str]], second: list[list[str]]
) -> dict[str, list[str]] | None:
    result: dict[str, list[str]] = {}
    for index, coordinate in enumerate(("radius", "theta")):
        first_lower, first_upper = _decimal_interval(
            first[index], path=f"first[{index}]"
        )
        second_lower, second_upper = _decimal_interval(
            second[index], path=f"second[{index}]"
        )
        lower = max(first_lower, second_lower)
        upper = min(first_upper, second_upper)
        if lower > upper:
            return None
        result[coordinate] = [format(lower, "f"), format(upper, "f")]
    return result


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
    raise TypeError(f"{path}: non-native JSON type {type(value).__name__}")


def validate_payload(payload: dict[str, Any], *, gate: Any) -> None:
    _native_json(payload)
    if set(payload) != {
        "identity",
        "finite_root",
        "infinite_tail",
        "classification",
        "publication",
    }:
        raise ValueError("$: root fields mismatch")
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
        raise ValueError("$.identity: fields mismatch")
    if identity["schema"] != SCHEMA or identity["parameters"] != PARAMETERS:
        raise ValueError("$.identity: registered identity mismatch")
    if type(identity["created_utc"]) is not str:
        raise ValueError("$.identity: provenance mismatch")
    try:
        created = datetime.fromisoformat(identity["created_utc"])
    except ValueError as error:
        raise ValueError("$.identity: provenance mismatch") from error
    if (
        created.tzinfo is None
        or created.utcoffset() != UTC.utcoffset(created)
        or not re.fullmatch(r"[0-9a-f]{40}", identity["execution_commit"])
        or identity["protocol_path"] != PROTOCOL.relative_to(ROOT).as_posix()
    ):
        raise ValueError("$.identity: provenance mismatch")
    if identity["start"] != list(START):
        raise ValueError("$.identity.start: mismatch")
    if identity["dependencies"] != {"mpmath": "1.3.0"}:
        raise ValueError("$.identity.dependencies: mismatch")
    if not _SHA256.fullmatch(identity["protocol_sha256"]):
        raise ValueError("$.identity.protocol_sha256: invalid")

    finite = payload["finite_root"]
    finite_complete = finite is not None
    root: list[str] | None = None
    if finite_complete:
        if set(finite) != {"newton", "outer_certificate", "inner_certificate"}:
            raise ValueError("$.finite_root: fields mismatch")
        newton = finite["newton"]
        if set(newton) != {
            "jacobian",
            "precision_dps",
            "radius",
            "residual",
            "steps",
            "theta",
        }:
            raise ValueError("$.finite_root.newton: fields mismatch")
        if newton["precision_dps"] != 120 or newton["steps"] != 8:
            raise ValueError("$.finite_root.newton: registration mismatch")
        root = [newton["radius"], newton["theta"]]
        _decimal_vector(root, path="$.finite_root.newton.root")
        _decimal_vector(newton["residual"], path="$.finite_root.newton.residual")
        _decimal_matrix(newton["jacobian"], path="$.finite_root.newton.jacobian")
        if not _strict_certificate(
            finite["outer_certificate"],
            root=root,
            half_width="1e-8",
            precision_dps=120,
            path="$.finite_root.outer_certificate",
        ):
            raise ValueError("$.finite_root.outer_certificate: false inclusion")
        if not _strict_certificate(
            finite["inner_certificate"],
            root=root,
            half_width="1e-30",
            precision_dps=120,
            path="$.finite_root.inner_certificate",
        ):
            raise ValueError("$.finite_root.inner_certificate: false inclusion")

    tail = payload["infinite_tail"]
    if set(tail) != {"bounds", "certificate_panels", "panel_comparison"}:
        raise ValueError("$.infinite_tail: fields mismatch")
    expected_bounds = [
        {"precision_dps": precision, **gate.tail_bounds(horizon=3600, precision_dps=precision)}
        for precision in (120, 160)
    ]
    if tail["bounds"] != expected_bounds:
        raise ValueError("$.infinite_tail.bounds: reconstruction mismatch")
    panels = tail["certificate_panels"]
    if type(panels) is not list or len(panels) != 2:
        raise ValueError("$.infinite_tail.certificate_panels: dimensionality mismatch")
    nonnull = 0
    certificates: list[bool] = []
    for index, panel in enumerate(panels):
        if panel is None:
            certificates.append(False)
            continue
        if index != nonnull or root is None:
            raise ValueError("$.infinite_tail.certificate_panels: invalid prefix")
        nonnull += 1
        if set(panel) != {"certificate", "precision_dps", "root"}:
            raise ValueError(f"$.infinite_tail.certificate_panels[{index}]: fields mismatch")
        if panel["precision_dps"] != (120, 160)[index] or panel["root"] != root:
            raise ValueError(f"$.infinite_tail.certificate_panels[{index}]: binding mismatch")
        certificates.append(
            _strict_certificate(
                panel["certificate"],
                root=root,
                half_width="1e-10",
                precision_dps=(120, 160)[index],
                path=f"$.infinite_tail.certificate_panels[{index}].certificate",
            )
        )

    comparison = tail["panel_comparison"]
    if all(panel is not None for panel in panels):
        intersection = _image_intersection(
            panels[0]["certificate"]["krawczyk_image"],
            panels[1]["certificate"]["krawczyk_image"],
        )
        expected_comparison = {
            "intersection": intersection,
            "overlap": intersection is not None,
        }
    else:
        expected_comparison = {"intersection": None, "overlap": False}
    if comparison != expected_comparison:
        raise ValueError("$.infinite_tail.panel_comparison: reconstruction mismatch")
    passed = bool(finite_complete and all(certificates) and comparison["overlap"])
    expected_classification = {
        "G4": "pass" if passed else "inconclusive",
        "decision": PASS_DECISION if passed else INCONCLUSIVE_DECISION,
        "claim_boundary": (
            "local F_infinity root conditional on registered tail bounds and "
            "mpmath.iv; no branch-transfer, stability, formation, interaction, or mass claim"
        ),
    }
    if payload["classification"] != expected_classification:
        raise ValueError("$.classification: reconstruction mismatch")
    if payload["publication"] != {
        "artifacts": [
            {"path": RESULT.name, "role": "result-json"},
            {"path": REPORT.name, "role": "readable-report"},
        ],
        "manifest_path": MANIFEST.name,
        "manifest_published_last": True,
    }:
        raise ValueError("$.publication: registration mismatch")


def run_component(
    *,
    execution_commit: str,
    protocol_sha256: str,
    finite_root_fn: Callable[..., dict[str, Any] | None] | None = None,
    tail_fn: Callable[..., dict[str, Any] | None] | None = None,
    created_utc: str | None = None,
) -> dict[str, Any]:
    gate = _load_horizon_gate()
    finite_root_fn = finite_root_fn or gate.finite_root_backend_record
    tail_fn = tail_fn or gate.tail_certificate_backend_record
    finite = finite_root_fn(horizon=3600, precision_dps=120, start=START)
    panels: list[dict[str, Any] | None] = [None, None]
    comparison: dict[str, Any] = {"intersection": None, "overlap": False}
    if finite is not None:
        newton = finite["newton"]
        root = (newton["radius"], newton["theta"])
        for index, precision in enumerate((120, 160)):
            panel = tail_fn(precision_dps=precision, root=root)
            if panel is None:
                break
            panels[index] = panel
        if all(panel is not None for panel in panels):
            intersection = _image_intersection(
                panels[0]["certificate"]["krawczyk_image"],
                panels[1]["certificate"]["krawczyk_image"],
            )
            comparison = {
                "intersection": intersection,
                "overlap": intersection is not None,
            }
    passed = bool(finite is not None and all(panel is not None for panel in panels) and comparison["overlap"])
    payload = {
        "identity": {
            "schema": SCHEMA,
            "created_utc": created_utc or datetime.now(UTC).isoformat(),
            "execution_commit": execution_commit,
            "protocol_path": PROTOCOL.relative_to(ROOT).as_posix(),
            "protocol_sha256": protocol_sha256,
            "dependencies": {"mpmath": mpmath.__version__},
            "parameters": PARAMETERS,
            "start": list(START),
        },
        "finite_root": finite,
        "infinite_tail": {
            "bounds": [
                {"precision_dps": precision, **gate.tail_bounds(horizon=3600, precision_dps=precision)}
                for precision in (120, 160)
            ],
            "certificate_panels": panels,
            "panel_comparison": comparison,
        },
        "classification": {
            "G4": "pass" if passed else "inconclusive",
            "decision": PASS_DECISION if passed else INCONCLUSIVE_DECISION,
            "claim_boundary": (
                "local F_infinity root conditional on registered tail bounds and "
                "mpmath.iv; no branch-transfer, stability, formation, interaction, or mass claim"
            ),
        },
        "publication": {
            "artifacts": [
                {"path": RESULT.name, "role": "result-json"},
                {"path": REPORT.name, "role": "readable-report"},
            ],
            "manifest_path": MANIFEST.name,
            "manifest_published_last": True,
        },
    }
    validate_payload(payload, gate=gate)
    return payload


def render_report(payload: dict[str, Any]) -> str:
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


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(content)
    os.replace(temporary, path)


def publish(payload: dict[str, Any], *, gate: Any | None = None) -> None:
    gate = gate or _load_horizon_gate()
    validate_payload(payload, gate=gate)
    result_bytes = (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")
    report_bytes = render_report(payload).encode("utf-8")
    _atomic_write(RESULT, result_bytes)
    _atomic_write(REPORT, report_bytes)
    manifest = {
        "schema": "scalar-memory-rotating-wave-horizon-g4-publication-v1",
        "execution_commit": payload["identity"]["execution_commit"],
        "protocol_sha256": payload["identity"]["protocol_sha256"],
        "artifacts": [
            {"path": RESULT.name, "role": "result-json", "sha256": _sha256_bytes(result_bytes)},
            {"path": REPORT.name, "role": "readable-report", "sha256": _sha256_bytes(report_bytes)},
        ],
    }
    manifest_bytes = (
        json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")
    _atomic_write(MANIFEST, manifest_bytes)


def main() -> None:
    execution_commit, protocol_sha256 = require_execution_context()
    payload = run_component(
        execution_commit=execution_commit,
        protocol_sha256=protocol_sha256,
    )
    publish(payload)
    print(f"Decision: {payload['classification']['decision']}")
    print(f"Manifest: {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
