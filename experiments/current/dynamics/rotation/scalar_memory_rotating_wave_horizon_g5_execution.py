"""One-shot execution guard for the isolated G5 component.

The tracked governance is closed by default.  Importing this module performs
no target work.  A later governance-only authorization commit must bind the
reviewed implementation, official successful CI, protected Git blobs, exact
dependencies, and one receipt path before ``execute_once`` can reach the
numerical backend.
"""

from __future__ import annotations

from datetime import UTC, datetime
import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[4]
GOVERNANCE_REL = Path(
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g5_component_governance.json"
)
PROTOCOL_REL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_horizon_g5_component_protocol_2026-09-14.md"
)
SCHEMA_REL = Path(
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g5_component_result_schema_v1.json"
)
COMPONENT_REL = Path(
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g5_component_gate.py"
)
AUDITOR_REL = Path(
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g5_component_result_audit.py"
)
READINESS_REVIEW_REL = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_horizon_g5_execution_readiness_review_2026-09-15.md"
)
ATTEMPT_RECEIPT_REL = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g5_component_attempt_1_receipt.json"
)
OUTPUT_DIRECTORY_REL = Path("reports/dynamics/rotation")
RESULT_NAME = "scalar_memory_rotating_wave_horizon_g5_component_2026-09-14.json"
REPORT_NAME = RESULT_NAME.removesuffix(".json") + ".md"
MANIFEST_NAME = RESULT_NAME.removesuffix(".json") + ".publication.json"
GOVERNANCE_SCHEMA = "scalar-memory-rotating-wave-horizon-g5-governance-v1"
AUTHORIZATION_KEYS = {
    "attempt",
    "authorization_id",
    "ci",
    "closed_governance_blob",
    "dependencies",
    "implementation_revision",
    "protected_blobs",
    "readiness_review_blob",
    "readiness_review_path",
    "schema_sha256",
}
CI_KEYS = {"api_url", "conclusion", "head_sha", "run_id", "status"}
DEPENDENCIES = {
    "mpmath": "1.3.0",
    "numpy": "2.3.5",
    "python": "3.12",
    "scipy": "1.17.1",
}
PROTECTED_PATHS = (
    PROTOCOL_REL.as_posix(),
    SCHEMA_REL.as_posix(),
    COMPONENT_REL.as_posix(),
    AUDITOR_REL.as_posix(),
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g5_execution.py",
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_transfer_gate.py",
    "src/emergenz_knoten/rotating_wave_horizon_stability.py",
    "src/emergenz_knoten/rotating_wave_stability.py",
    "src/emergenz_knoten/strict_json_contract.py",
    "tests/test_rotating_wave_horizon_g5_component.py",
    "tests/test_rotating_wave_horizon_g5_execution.py",
)
_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_UUID4 = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z"
)


def _git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _git_blob(path: str, revision: str = "HEAD") -> str:
    return _git("rev-parse", f"{revision}:{path}")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _installed_dependencies() -> dict[str, str]:
    return {
        "mpmath": importlib.metadata.version("mpmath"),
        "numpy": importlib.metadata.version("numpy"),
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
        "scipy": importlib.metadata.version("scipy"),
    }


def _load_governance(path: Path | None = None) -> dict[str, Any]:
    source = ROOT / GOVERNANCE_REL if path is None else path
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError("G5 governance is unreadable") from error
    expected_keys = {
        "authorization",
        "gate",
        "protocol_blob",
        "reason",
        "result_schema_sha256",
        "schema",
        "state",
        "target_authorized",
        "target_calls_recorded",
    }
    if type(payload) is not dict or set(payload) != expected_keys:
        raise RuntimeError("G5 governance keys mismatch")
    if payload["schema"] != GOVERNANCE_SCHEMA or payload["gate"] != "G5":
        raise RuntimeError("G5 governance identity mismatch")
    if type(payload["reason"]) is not str or not payload["reason"]:
        raise RuntimeError("G5 governance reason is empty")
    if payload["state"] not in {"closed", "authorized_once"}:
        raise RuntimeError("G5 governance state is unregistered")
    if type(payload["target_authorized"]) is not bool:
        raise RuntimeError("G5 governance authorization flag is not Boolean")
    if payload["target_calls_recorded"] != []:
        raise RuntimeError("G5 governance contains an unregistered target call")
    if (
        type(payload["result_schema_sha256"]) is not str
        or _SHA256.fullmatch(payload["result_schema_sha256"]) is None
        or payload["result_schema_sha256"]
        != _sha256_file(ROOT / SCHEMA_REL)
    ):
        raise RuntimeError("G5 governance result-schema digest mismatch")
    if (
        type(payload["protocol_blob"]) is not str
        or _SHA1.fullmatch(payload["protocol_blob"]) is None
        or payload["protocol_blob"] != _git_blob(PROTOCOL_REL.as_posix())
    ):
        raise RuntimeError("G5 governance protocol blob mismatch")
    if payload["state"] == "closed":
        if payload["target_authorized"] is not False:
            raise RuntimeError("closed G5 governance cannot authorize a target")
        if payload["authorization"] is not None:
            raise RuntimeError("closed G5 governance must have null authorization")
    return payload


def _github_run_metadata(run_id: int) -> dict[str, Any]:
    process = subprocess.run(
        [
            "gh",
            "api",
            f"repos/MemoryDynamics/Knoten/actions/runs/{run_id}",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(process.stdout)
    if type(payload) is not dict:
        raise RuntimeError("G5 CI metadata is not an object")
    return payload


def _read_readiness_review() -> str:
    return (ROOT / READINESS_REVIEW_REL).read_text(encoding="utf-8")


def _parse_readiness_review(text: str) -> dict[str, Any]:
    revision = re.search(r"Implementation revision: `([0-9a-f]{40})`", text)
    verdict = re.search(r"Verdict: \*\*`([^`]+)`\*\*", text)
    ci_run = re.search(r"actions/runs/(\d+)", text)
    blobs = dict(re.findall(r"Blob `([^`]+)`: `([0-9a-f]{40})`", text))
    if revision is None or verdict is None or ci_run is None:
        raise RuntimeError("G5 readiness review is incomplete")
    if verdict.group(1) != "g5-implementation-ready-target-closed":
        raise RuntimeError("G5 readiness verdict is not upheld")
    if set(blobs) != set(PROTECTED_PATHS):
        raise RuntimeError("G5 readiness review protected blob table mismatch")
    return {
        "blobs": blobs,
        "ci_run_id": int(ci_run.group(1)),
        "implementation_revision": revision.group(1),
        "verdict": verdict.group(1),
    }


def _validate_output_paths(directory: Path = ROOT / OUTPUT_DIRECTORY_REL) -> None:
    expected = (ROOT / OUTPUT_DIRECTORY_REL).resolve()
    if directory.resolve() != expected:
        raise RuntimeError("G5 permits only the registered output directory")
    targets = (
        directory / RESULT_NAME,
        directory / REPORT_NAME,
        directory / MANIFEST_NAME,
        ROOT / ATTEMPT_RECEIPT_REL,
    )
    existing = [path.name for path in targets if path.exists()]
    if existing:
        raise RuntimeError(f"G5 registered target path already exists: {existing}")


def _create_attempt_receipt(
    *,
    authorization_id: str,
    ci_run_id: int,
    governance_sha256: str,
    implementation_revision: str,
    revision: str,
) -> tuple[str, str]:
    path = ROOT / ATTEMPT_RECEIPT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    receipt = {
        "attempt": 1,
        "authorization_id": authorization_id,
        "ci_run_id": ci_run_id,
        "created_utc": datetime.now(UTC).isoformat(),
        "governance_sha256": governance_sha256,
        "implementation_revision": implementation_revision,
        "revision": revision,
        "schema": "scalar-memory-rotating-wave-horizon-g5-attempt-receipt-v1",
    }
    content = (
        json.dumps(receipt, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    try:
        with path.open("xb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError as error:
        raise RuntimeError("G5 one-shot authorization was already consumed") from error
    return ATTEMPT_RECEIPT_REL.as_posix(), hashlib.sha256(content).hexdigest()


def require_target_authorization(
    *,
    governance_path: Path | None = None,
    metadata_fn: Callable[[int], dict[str, Any]] = _github_run_metadata,
    output_directory: Path = ROOT / OUTPUT_DIRECTORY_REL,
) -> dict[str, Any]:
    """Validate and consume one explicit G5 authorization before target work."""

    governance = _load_governance(governance_path)
    if governance["state"] == "closed":
        raise RuntimeError("G5 target sealed by machine governance")
    if governance["target_authorized"] is not True:
        raise RuntimeError("G5 target is not authorized")
    authorization = governance["authorization"]
    if type(authorization) is not dict or set(authorization) != AUTHORIZATION_KEYS:
        raise RuntimeError("G5 authorization keys mismatch")
    if authorization["attempt"] != 1:
        raise RuntimeError("G5 authorization attempt mismatch")
    authorization_id = authorization["authorization_id"]
    if type(authorization_id) is not str or _UUID4.fullmatch(authorization_id) is None:
        raise RuntimeError("G5 authorization identifier is not canonical UUIDv4")
    implementation = authorization["implementation_revision"]
    if type(implementation) is not str or _SHA1.fullmatch(implementation) is None:
        raise RuntimeError("G5 implementation revision is invalid")
    if authorization["schema_sha256"] != _sha256_file(ROOT / SCHEMA_REL):
        raise RuntimeError("G5 authorization schema digest mismatch")
    if authorization["dependencies"] != DEPENDENCIES:
        raise RuntimeError("G5 authorized dependency set mismatch")
    if _installed_dependencies() != DEPENDENCIES:
        raise RuntimeError("G5 installed dependency set mismatch")
    protected = authorization["protected_blobs"]
    if type(protected) is not dict or set(protected) != set(PROTECTED_PATHS):
        raise RuntimeError("G5 protected blob table mismatch")
    for path, expected in protected.items():
        if type(expected) is not str or _SHA1.fullmatch(expected) is None:
            raise RuntimeError(f"G5 protected blob is invalid: {path}")
        if _git_blob(path, implementation) != expected or _git_blob(path) != expected:
            raise RuntimeError(f"G5 protected blob drift: {path}")
    closed_blob = authorization["closed_governance_blob"]
    if _git_blob(GOVERNANCE_REL.as_posix(), implementation) != closed_blob:
        raise RuntimeError("G5 closed governance blob mismatch")
    if authorization["readiness_review_path"] != READINESS_REVIEW_REL.as_posix():
        raise RuntimeError("G5 readiness-review path mismatch")
    if _git_blob(READINESS_REVIEW_REL.as_posix()) != authorization["readiness_review_blob"]:
        raise RuntimeError("G5 readiness-review blob mismatch")
    try:
        readiness = _parse_readiness_review(_read_readiness_review())
    except OSError as error:
        raise RuntimeError("G5 readiness review is unreadable") from error
    if (
        readiness["implementation_revision"] != implementation
        or readiness["blobs"] != protected
    ):
        raise RuntimeError("G5 readiness review implementation binding mismatch")
    ci = authorization["ci"]
    if type(ci) is not dict or set(ci) != CI_KEYS:
        raise RuntimeError("G5 CI authorization keys mismatch")
    run_id = ci["run_id"]
    expected_api = f"https://api.github.com/repos/MemoryDynamics/Knoten/actions/runs/{run_id}"
    if (
        type(run_id) is not int
        or run_id <= 0
        or ci
        != {
            "api_url": expected_api,
            "conclusion": "success",
            "head_sha": implementation,
            "run_id": run_id,
            "status": "completed",
        }
    ):
        raise RuntimeError("G5 CI authorization record mismatch")
    if readiness["ci_run_id"] != run_id:
        raise RuntimeError("G5 readiness review CI binding mismatch")
    try:
        remote = metadata_fn(run_id)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        raise RuntimeError("G5 official CI metadata is unavailable") from error
    repository = remote.get("repository")
    if not (
        remote.get("id") == run_id
        and type(repository) is dict
        and repository.get("full_name") == "MemoryDynamics/Knoten"
        and remote.get("status") == "completed"
        and remote.get("conclusion") == "success"
        and remote.get("head_sha") == implementation
    ):
        raise RuntimeError("G5 official CI metadata mismatch")
    _git("merge-base", "--is-ancestor", implementation, "HEAD")
    changed_last = set(_git("diff", "--name-only", "HEAD^", "HEAD").splitlines())
    if changed_last != {GOVERNANCE_REL.as_posix()}:
        raise RuntimeError("G5 authorization commit changed more than governance")
    if _git("status", "--porcelain", "--untracked-files=all"):
        raise RuntimeError("G5 target requires a clean worktree")
    head = _git("rev-parse", "HEAD")
    upstream = _git("rev-parse", "@{upstream}")
    if head != upstream:
        raise RuntimeError("G5 target requires exact upstream synchronization")
    _validate_output_paths(output_directory)
    governance_source = ROOT / GOVERNANCE_REL if governance_path is None else governance_path
    governance_sha256 = _sha256_file(governance_source)
    receipt_path, receipt_sha256 = _create_attempt_receipt(
        authorization_id=authorization_id,
        ci_run_id=run_id,
        governance_sha256=governance_sha256,
        implementation_revision=implementation,
        revision=head,
    )
    return {
        "attempt": 1,
        "attempt_receipt_path": receipt_path,
        "attempt_receipt_sha256": receipt_sha256,
        "authorization_id": authorization_id,
        "ci_run_id": run_id,
        "governance_sha256": governance_sha256,
        "implementation_revision": implementation,
        "revision": head,
        "upstream_revision": upstream,
    }


def _load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {path.name}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def execute_once() -> dict[str, Any]:
    """Consume authorization, run exactly one component, audit, and publish it."""

    provenance = require_target_authorization()
    component = _load_module(ROOT / COMPONENT_REL, "authorized_g5_component")
    auditor = _load_module(ROOT / AUDITOR_REL, "authorized_g5_auditor")
    identity = {
        "authorization": {
            key: provenance[key]
            for key in (
                "attempt",
                "attempt_receipt_path",
                "attempt_receipt_sha256",
                "authorization_id",
                "ci_run_id",
                "governance_sha256",
                "implementation_revision",
                "upstream_revision",
            )
        },
        "created_utc": datetime.now(UTC).isoformat(),
        "dependencies": {
            name: DEPENDENCIES[name] for name in ("mpmath", "numpy", "scipy")
        },
        "equation_id": component.EQUATION_ID,
        "execution_commit": provenance["revision"],
        "parameters": component.PARAMETERS,
        "protocol_path": PROTOCOL_REL.as_posix(),
        "protocol_sha256": _sha256_file(ROOT / PROTOCOL_REL),
        "schema": component.SCHEMA,
        "start": list(component.START),
    }
    publication = {
        "artifacts": [
            {"path": RESULT_NAME, "role": "result-json"},
            {"path": REPORT_NAME, "role": "readable-report"},
        ],
        "manifest_path": MANIFEST_NAME,
        "manifest_published_last": True,
    }
    payload = component.assemble_component(
        backend=component.RegisteredBackend(),
        identity=identity,
        publication=publication,
    )
    auditor.audit_payload(payload)
    paths = component.publish_payload(
        payload, directory=ROOT / OUTPUT_DIRECTORY_REL
    )
    auditor.audit_publication(
        result_path=paths["result"],
        report_path=paths["report"],
        manifest_path=paths["manifest"],
        receipt_path=ROOT / ATTEMPT_RECEIPT_REL,
    )
    return payload
