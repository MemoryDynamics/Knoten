"""Attempt-2 one-shot guard for the uniform H=3600 to infinity branch-link gate.

Importing this module performs no target work.  The tracked governance is
closed.  A later governance-only commit must bind a reviewed implementation,
successful official CI, protected blobs and one fresh receipt.
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
BASE = "experiments/current/dynamics/rotation/"
GOVERNANCE_REL = Path(
    BASE
    + "scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_2_governance.json"
)
PROTOCOL_REL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_2_protocol_2026-09-30.md"
)
SCHEMA_REL = Path(
    BASE
    + "scalar_memory_rotating_wave_horizon_infinity_branch_link_result_schema_v2.json"
)
GATE_REL = Path(
    BASE + "scalar_memory_rotating_wave_horizon_infinity_branch_link_gate.py"
)
AUDITOR_REL = Path(
    BASE
    + "scalar_memory_rotating_wave_horizon_infinity_branch_link_result_audit.py"
)
EXECUTION_REL = Path(
    BASE
    + "scalar_memory_rotating_wave_horizon_infinity_branch_link_execution.py"
)
READINESS_REVIEW_REL = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_2_execution_readiness_review_2026-09-30.md"
)
RECEIPT_REL = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_2_receipt_2026-09-30.json"
)
RESULT_REL = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_2_2026-09-30.json"
)
REPORT_REL = RESULT_REL.with_suffix(".md")
MANIFEST_REL = RESULT_REL.with_suffix(".publication.json")
AUDIT_REL = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_2_independent_audit_2026-09-30.json"
)
GOVERNANCE_SCHEMA = (
    "scalar-memory-rotating-wave-horizon-infinity-branch-link-governance-v2"
)
ATTEMPT = 2
DEPENDENCIES = {"mpmath": "1.3.0", "python": "3.12"}
PROTECTED_PATHS = (
    "requirements-dev.txt",
    PROTOCOL_REL.as_posix(),
    SCHEMA_REL.as_posix(),
    GATE_REL.as_posix(),
    AUDITOR_REL.as_posix(),
    EXECUTION_REL.as_posix(),
    BASE + "scalar_memory_rotating_wave_horizon_transfer_gate.py",
    "src/emergenz_knoten/rotating_wave_interval.py",
    "src/emergenz_knoten/strict_json_contract.py",
    "tests/test_rotating_wave_tail_homotopy_interval.py",
    "tests/test_rotating_wave_horizon_infinity_branch_link.py",
    "tests/test_rotating_wave_horizon_infinity_branch_link_execution.py",
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_receipt_2026-09-29.json",
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_1_serialization_incident_2026-09-30.md",
)
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
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
    }


def _load_governance(path: Path | None = None) -> dict[str, Any]:
    source = ROOT / GOVERNANCE_REL if path is None else Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError("infinity branch-link governance is unreadable") from error
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
        raise RuntimeError("infinity branch-link governance keys mismatch")
    if (
        payload["schema"] != GOVERNANCE_SCHEMA
        or payload["gate"] != "G-infinity-branch-link"
    ):
        raise RuntimeError("infinity branch-link governance identity mismatch")
    if type(payload["reason"]) is not str or not payload["reason"]:
        raise RuntimeError("infinity branch-link governance reason is empty")
    if payload["state"] not in {"closed", "authorized_once"}:
        raise RuntimeError("infinity branch-link governance state is unregistered")
    if type(payload["target_authorized"]) is not bool:
        raise RuntimeError("infinity branch-link authorization flag is not Boolean")
    if payload["target_calls_recorded"] != []:
        raise RuntimeError("infinity branch-link governance contains a target call")
    if payload["result_schema_sha256"] != _sha256_file(ROOT / SCHEMA_REL):
        raise RuntimeError("infinity branch-link schema digest mismatch")
    if payload["protocol_blob"] != _git_blob(PROTOCOL_REL.as_posix()):
        raise RuntimeError("infinity branch-link protocol blob mismatch")
    schema = json.loads((ROOT / SCHEMA_REL).read_text(encoding="utf-8"))
    if (
        schema["constants"]["protocol_blob"] != payload["protocol_blob"]
        or schema["constants"]["protocol_sha256"]
        != _sha256_file(ROOT / PROTOCOL_REL)
    ):
        raise RuntimeError("infinity branch-link schema/protocol binding mismatch")
    if payload["state"] == "closed" and (
        payload["target_authorized"] is not False
        or payload["authorization"] is not None
    ):
        raise RuntimeError("closed infinity branch-link governance authorizes target")
    return payload


def _github_run_metadata(run_id: int) -> dict[str, Any]:
    process = subprocess.run(
        ["gh", "api", f"repos/MemoryDynamics/Knoten/actions/runs/{run_id}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(process.stdout)
    if type(payload) is not dict:
        raise RuntimeError("infinity branch-link CI metadata is not an object")
    return payload


def _parse_readiness_review(text: str) -> dict[str, Any]:
    revision = re.search(r"Implementation revision: `([0-9a-f]{40})`", text)
    verdict = re.search(r"Verdict: \*\*`([^`]+)`\*\*", text)
    ci_run = re.search(r"actions/runs/(\d+)", text)
    blobs = dict(re.findall(r"Blob `([^`]+)`: `([0-9a-f]{40})`", text))
    if revision is None or verdict is None or ci_run is None:
        raise RuntimeError("infinity branch-link readiness review is incomplete")
    if (
        verdict.group(1)
        != "g-infinity-branch-link-attempt-2-implementation-ready-target-closed"
    ):
        raise RuntimeError("infinity branch-link readiness verdict is not upheld")
    if set(blobs) != set(PROTECTED_PATHS):
        raise RuntimeError("infinity branch-link protected blob table mismatch")
    return {
        "blobs": blobs,
        "ci_run_id": int(ci_run.group(1)),
        "implementation_revision": revision.group(1),
    }


def _read_readiness_review() -> str:
    return (ROOT / READINESS_REVIEW_REL).read_text(encoding="utf-8")


def _validate_output_paths() -> None:
    paths = (
        ROOT / RESULT_REL,
        ROOT / REPORT_REL,
        ROOT / MANIFEST_REL,
        ROOT / AUDIT_REL,
        ROOT / RECEIPT_REL,
    )
    existing = [path.as_posix() for path in paths if path.exists()]
    if existing:
        raise RuntimeError(
            f"infinity branch-link target path already exists: {existing}"
        )


def _create_receipt(
    *,
    authorization_id: str,
    ci_run_id: int,
    governance_sha256: str,
    implementation_revision: str,
    revision: str,
) -> tuple[str, str]:
    path = ROOT / RECEIPT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    receipt = {
        "attempt": ATTEMPT,
        "authorization_id": authorization_id,
        "ci_run_id": ci_run_id,
        "created_utc": datetime.now(UTC).isoformat(),
        "governance_sha256": governance_sha256,
        "implementation_revision": implementation_revision,
        "revision": revision,
        "schema": "scalar-memory-rotating-wave-horizon-infinity-branch-link-receipt-v2",
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
        raise RuntimeError(
            "infinity branch-link authorization was already consumed"
        ) from error
    return RECEIPT_REL.as_posix(), hashlib.sha256(content).hexdigest()


def require_target_authorization(
    *,
    governance_path: Path | None = None,
    metadata_fn: Callable[[int], dict[str, Any]] = _github_run_metadata,
) -> dict[str, Any]:
    governance = _load_governance(governance_path)
    if governance["state"] == "closed":
        raise RuntimeError("infinity branch-link target sealed by machine governance")
    if governance["target_authorized"] is not True:
        raise RuntimeError("infinity branch-link target is not authorized")
    authorization = governance["authorization"]
    if type(authorization) is not dict or set(authorization) != AUTHORIZATION_KEYS:
        raise RuntimeError("infinity branch-link authorization keys mismatch")
    authorization_id = authorization["authorization_id"]
    implementation = authorization["implementation_revision"]
    if authorization["attempt"] != ATTEMPT:
        raise RuntimeError("infinity branch-link attempt mismatch")
    if type(authorization_id) is not str or _UUID4.fullmatch(authorization_id) is None:
        raise RuntimeError("infinity branch-link authorization ID is invalid")
    if type(implementation) is not str or _SHA1.fullmatch(implementation) is None:
        raise RuntimeError("infinity branch-link implementation revision is invalid")
    if authorization["schema_sha256"] != _sha256_file(ROOT / SCHEMA_REL):
        raise RuntimeError("infinity branch-link authorized schema digest mismatch")
    if authorization["dependencies"] != DEPENDENCIES:
        raise RuntimeError("infinity branch-link dependency registration mismatch")
    if _installed_dependencies() != DEPENDENCIES:
        raise RuntimeError("infinity branch-link installed dependencies mismatch")
    protected = authorization["protected_blobs"]
    if type(protected) is not dict or set(protected) != set(PROTECTED_PATHS):
        raise RuntimeError("infinity branch-link protected blob table mismatch")
    for path, expected in protected.items():
        if type(expected) is not str or _SHA1.fullmatch(expected) is None:
            raise RuntimeError(f"infinity branch-link protected blob invalid: {path}")
        if _git_blob(path, implementation) != expected or _git_blob(path) != expected:
            raise RuntimeError(f"infinity branch-link protected blob drift: {path}")
    closed_blob = authorization["closed_governance_blob"]
    if _git_blob(GOVERNANCE_REL.as_posix(), implementation) != closed_blob:
        raise RuntimeError("infinity branch-link closed-governance blob mismatch")
    if authorization["readiness_review_path"] != READINESS_REVIEW_REL.as_posix():
        raise RuntimeError("infinity branch-link readiness path mismatch")
    if _git_blob(READINESS_REVIEW_REL.as_posix()) != authorization[
        "readiness_review_blob"
    ]:
        raise RuntimeError("infinity branch-link readiness blob mismatch")
    readiness = _parse_readiness_review(_read_readiness_review())
    if (
        readiness["implementation_revision"] != implementation
        or readiness["blobs"] != protected
    ):
        raise RuntimeError("infinity branch-link readiness binding mismatch")
    ci = authorization["ci"]
    if type(ci) is not dict or set(ci) != CI_KEYS:
        raise RuntimeError("infinity branch-link CI authorization keys mismatch")
    run_id = ci["run_id"]
    expected_api = (
        f"https://api.github.com/repos/MemoryDynamics/Knoten/actions/runs/{run_id}"
    )
    if type(run_id) is not int or run_id <= 0 or ci != {
        "api_url": expected_api,
        "conclusion": "success",
        "head_sha": implementation,
        "run_id": run_id,
        "status": "completed",
    }:
        raise RuntimeError("infinity branch-link CI authorization mismatch")
    if readiness["ci_run_id"] != run_id:
        raise RuntimeError("infinity branch-link readiness CI mismatch")
    remote = metadata_fn(run_id)
    repository = remote.get("repository")
    if not (
        remote.get("id") == run_id
        and type(repository) is dict
        and repository.get("full_name") == "MemoryDynamics/Knoten"
        and remote.get("status") == "completed"
        and remote.get("conclusion") == "success"
        and remote.get("head_sha") == implementation
    ):
        raise RuntimeError("infinity branch-link official CI metadata mismatch")
    _git("merge-base", "--is-ancestor", implementation, "HEAD")
    drift = set(_git("diff", "--name-only", implementation, "HEAD").splitlines())
    forbidden = sorted(
        path
        for path in drift
        if path != GOVERNANCE_REL.as_posix() and not path.endswith(".md")
    )
    if forbidden:
        raise RuntimeError(f"infinity branch-link implementation drift: {forbidden}")
    changed_last = set(_git("diff", "--name-only", "HEAD^", "HEAD").splitlines())
    if changed_last != {GOVERNANCE_REL.as_posix()}:
        raise RuntimeError(
            "infinity branch-link authorization commit must be governance-only"
        )
    if _git("status", "--porcelain", "--untracked-files=all"):
        raise RuntimeError("infinity branch-link target requires a clean worktree")
    head = _git("rev-parse", "HEAD")
    upstream = _git("rev-parse", "@{upstream}")
    if head != upstream:
        raise RuntimeError("infinity branch-link requires upstream synchronization")
    _validate_output_paths()
    source = ROOT / GOVERNANCE_REL if governance_path is None else Path(governance_path)
    governance_sha256 = _sha256_file(source)
    receipt_path, receipt_sha256 = _create_receipt(
        authorization_id=authorization_id,
        ci_run_id=run_id,
        governance_sha256=governance_sha256,
        implementation_revision=implementation,
        revision=head,
    )
    return {
        "attempt": ATTEMPT,
        "authorization_id": authorization_id,
        "ci_run_id": run_id,
        "governance_sha256": governance_sha256,
        "implementation_revision": implementation,
        "receipt_path": receipt_path,
        "receipt_sha256": receipt_sha256,
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
    """Consume authorization, calculate two panels, audit, and publish."""

    provenance = require_target_authorization()
    gate = _load_module(ROOT / GATE_REL, "authorized_infinity_branch_gate")
    auditor = _load_module(ROOT / AUDITOR_REL, "authorized_infinity_branch_auditor")
    authorization = {
        key: provenance[key]
        for key in (
            "attempt",
            "authorization_id",
            "ci_run_id",
            "governance_sha256",
            "implementation_revision",
            "receipt_path",
            "receipt_sha256",
            "upstream_revision",
        )
    }
    payload = gate.run_contract(
        execution_commit=provenance["revision"],
        authorization=authorization,
    )
    gate.publish(payload, audit_fn=auditor.audit_payload_bytes)
    auditor.verify_publication()
    return payload


if __name__ == "__main__":
    result = execute_once()
    print(f"Decision: {result['classification']['decision']}")
