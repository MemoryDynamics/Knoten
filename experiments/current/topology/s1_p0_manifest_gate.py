"""Validate the provenance freeze required before S1 candidate analysis.

The gate checks completeness and internal auditability only.  It does not
choose a candidate, infer missing values, or inspect D0/D1 target topology.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MANIFEST = (
    PROJECT_ROOT
    / "reports"
    / "project"
    / "meta"
    / "preregistration"
    / "s1_candidate_p0_manifest_2026-08-16.json"
)
DEFAULT_AUDIT = DEFAULT_MANIFEST.with_name("s1_candidate_p0_audit_2026-08-16.json")

PLACEHOLDERS = {
    "",
    "n/a",
    "na",
    "none",
    "null",
    "pending",
    "tbd",
    "to-be-determined",
    "unknown",
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

FULL_PARAMETER_COMPONENTS = (
    "noise",
    "memory",
    "kernel",
    "coupling",
    "integration",
    "horizon_and_boundary",
    "external_system",
    "initialization",
)
DISCOVERY_FIELDS = (
    "seeds",
    "run_lengths_and_cadence",
    "forcing_and_external_system",
    "observables_inspected",
    "parameter_cells_or_optimizers_inspected",
    "selection_rule",
    "artifacts_and_hashes",
)
CONFIRMATORY_FIELDS = (
    "seed_generation_rule",
    "untouched_parameter_holdout",
)


@dataclass(frozen=True)
class AuditIssue:
    code: str
    path: str
    message: str


def _is_concrete(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip().lower() not in PLACEHOLDERS
    if isinstance(value, dict):
        return bool(value) and all(_is_concrete(item) for item in value.values())
    if isinstance(value, list):
        return bool(value) and all(_is_concrete(item) for item in value)
    return True


def _add_missing_if_needed(
    issues: list[AuditIssue],
    container: dict[str, Any],
    field: str,
    prefix: str,
) -> None:
    path = f"{prefix}.{field}" if prefix else field
    if field not in container or not _is_concrete(container[field]):
        issues.append(
            AuditIssue(
                code="missing-or-placeholder",
                path=path,
                message="required value is absent, empty, or a placeholder",
            )
        )


def _audit_hash_records(
    issues: list[AuditIssue],
    records: Any,
    path: str,
    *,
    repository_root: Path | None = None,
) -> None:
    if not isinstance(records, list) or not records:
        return
    for index, record in enumerate(records):
        item_path = f"{path}[{index}]"
        if not isinstance(record, dict):
            issues.append(
                AuditIssue(
                    code="invalid-record",
                    path=item_path,
                    message="record must be an object containing source/path and sha256",
                )
            )
            continue
        source = record.get("source", record.get("path"))
        digest = record.get("sha256")
        if not _is_concrete(source):
            issues.append(
                AuditIssue(
                    code="missing-source",
                    path=f"{item_path}.source",
                    message="artifact or state source is required",
                )
            )
        valid_digest = isinstance(digest, str) and bool(HEX64.fullmatch(digest.lower()))
        if not valid_digest:
            issues.append(
                AuditIssue(
                    code="invalid-sha256",
                    path=f"{item_path}.sha256",
                    message="sha256 must contain exactly 64 hexadecimal characters",
                )
            )
        if repository_root is None or not isinstance(source, str):
            continue

        source_path = Path(source)
        resolved = (repository_root / source_path).resolve()
        if source_path.is_absolute() or not resolved.is_relative_to(
            repository_root.resolve()
        ):
            issues.append(
                AuditIssue(
                    code="artifact-outside-repository",
                    path=f"{item_path}.source",
                    message="P0 artifacts must use repository-relative paths",
                )
            )
        elif not resolved.is_file():
            issues.append(
                AuditIssue(
                    code="artifact-not-found",
                    path=f"{item_path}.source",
                    message="the declared state or discovery artifact does not exist",
                )
            )
        elif valid_digest and _sha256(resolved) != digest.lower():
            issues.append(
                AuditIssue(
                    code="artifact-hash-mismatch",
                    path=f"{item_path}.sha256",
                    message="declared sha256 does not match the repository artifact",
                )
            )


def _revision_exists(repository_root: Path, revision: str) -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}^{{commit}}"],
        cwd=repository_root,
        capture_output=True,
        check=False,
        text=True,
    )
    return completed.returncode == 0


def audit_manifest(
    manifest: dict[str, Any],
    *,
    repository_root: Path | None = None,
) -> list[AuditIssue]:
    """Return every P0 defect without short-circuiting downstream fields."""

    issues: list[AuditIssue] = []
    for field in (
        "schema_version",
        "manifest_status",
        "candidate_id",
        "candidate_claim",
        "architecture_level",
        "time_law",
        "code_revision",
        "working_tree_status",
        "quarantined_predecessor_relation",
    ):
        _add_missing_if_needed(issues, manifest, field, "")

    if manifest.get("schema_version") != "1.0":
        issues.append(
            AuditIssue(
                code="unsupported-schema",
                path="schema_version",
                message="the executable P0 gate currently accepts schema_version 1.0",
            )
        )
    if manifest.get("manifest_status") != "frozen":
        issues.append(
            AuditIssue(
                code="manifest-not-frozen",
                path="manifest_status",
                message="P0 can pass only an explicitly frozen manifest",
            )
        )

    architecture = manifest.get("architecture_level")
    if _is_concrete(architecture) and not (
        architecture in {"K0", "K1", "K2", "K3"}
        or (isinstance(architecture, str) and architecture.startswith("new:"))
    ):
        issues.append(
            AuditIssue(
                code="invalid-architecture-level",
                path="architecture_level",
                message="use K0, K1, K2, K3, or new:<explicit-name>",
            )
        )

    time_law = manifest.get("time_law")
    allowed_time_laws = {
        "native-discrete-map",
        "continuous-model",
        "validated-continuum-limit",
    }
    if _is_concrete(time_law) and time_law not in allowed_time_laws:
        issues.append(
            AuditIssue(
                code="invalid-time-law",
                path="time_law",
                message=f"time_law must be one of {sorted(allowed_time_laws)}",
            )
        )

    revision = manifest.get("code_revision")
    if _is_concrete(revision):
        normalized_revision = str(revision).lower()
        if not HEX40.fullmatch(normalized_revision):
            issues.append(
                AuditIssue(
                    code="invalid-code-revision",
                    path="code_revision",
                    message="code_revision must be a full 40-character commit hash",
                )
            )
        elif repository_root is not None and not _revision_exists(
            repository_root, normalized_revision
        ):
            issues.append(
                AuditIssue(
                    code="unknown-code-revision",
                    path="code_revision",
                    message="the declared discovery revision is not present locally",
                )
            )

    if (
        _is_concrete(manifest.get("working_tree_status"))
        and manifest.get("working_tree_status") != "clean"
    ):
        issues.append(
            AuditIssue(
                code="dirty-discovery-worktree",
                path="working_tree_status",
                message=(
                    "a dirty discovery tree needs a committed reconstruction before P0"
                ),
            )
        )

    parameters = manifest.get("full_parameter_tuple")
    if not isinstance(parameters, dict):
        issues.append(
            AuditIssue(
                code="missing-object",
                path="full_parameter_tuple",
                message="full_parameter_tuple must be an object",
            )
        )
    else:
        for field in FULL_PARAMETER_COMPONENTS:
            _add_missing_if_needed(issues, parameters, field, "full_parameter_tuple")

    states = manifest.get("initial_state_source_and_hashes")
    if not _is_concrete(states):
        issues.append(
            AuditIssue(
                code="missing-or-placeholder",
                path="initial_state_source_and_hashes",
                message="at least one reproducible initial-state record is required",
            )
        )
    _audit_hash_records(
        issues,
        states,
        "initial_state_source_and_hashes",
        repository_root=repository_root,
    )

    discovery = manifest.get("discovery_provenance")
    if not isinstance(discovery, dict):
        issues.append(
            AuditIssue(
                code="missing-object",
                path="discovery_provenance",
                message="discovery_provenance must be an object",
            )
        )
    else:
        for field in DISCOVERY_FIELDS:
            _add_missing_if_needed(issues, discovery, field, "discovery_provenance")
        _audit_hash_records(
            issues,
            discovery.get("artifacts_and_hashes"),
            "discovery_provenance.artifacts_and_hashes",
            repository_root=repository_root,
        )

    confirmatory = manifest.get("confirmatory_design")
    if not isinstance(confirmatory, dict):
        issues.append(
            AuditIssue(
                code="missing-object",
                path="confirmatory_design",
                message="confirmatory_design must be an object",
            )
        )
    else:
        for field in CONFIRMATORY_FIELDS:
            _add_missing_if_needed(issues, confirmatory, field, "confirmatory_design")
        if confirmatory.get("new_seeds_disjoint_from_discovery") is not True:
            issues.append(
                AuditIssue(
                    code="confirmatory-seeds-not-sealed",
                    path="confirmatory_design.new_seeds_disjoint_from_discovery",
                    message="new confirmatory seeds must be explicitly disjoint",
                )
            )
        if confirmatory.get("target_data_opened") is not False:
            issues.append(
                AuditIssue(
                    code="target-data-not-sealed",
                    path="confirmatory_design.target_data_opened",
                    message="target_data_opened must be false at P0",
                )
            )

    return issues


def load_manifest(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("P0 manifest root must be a JSON object")
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_audit_record(
    manifest_path: Path,
    issues: list[AuditIssue],
    *,
    generated_at: str,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "gate": "P0-candidate-and-discovery-freeze",
        "decision": "pass" if not issues else "fail",
        "downstream": {
            "D0": "authorized" if not issues else "blocked",
            "D1": "blocked-until-D0-pass" if not issues else "blocked",
            "target_simulation": "sealed" if issues else "eligible-after-D0-contract",
        },
        "generated_at": generated_at,
        "manifest_path": manifest_path.relative_to(PROJECT_ROOT).as_posix(),
        "manifest_sha256": _sha256(manifest_path),
        "issue_count": len(issues),
        "issues": [asdict(issue) for issue in issues],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--audit-output", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument(
        "--generated-at",
        default=None,
        help="fixed ISO timestamp for a reproducible recorded audit",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest_path = args.manifest.resolve()
    manifest = load_manifest(manifest_path)
    issues = audit_manifest(manifest, repository_root=PROJECT_ROOT)
    generated_at = args.generated_at or datetime.now(timezone.utc).isoformat()
    record = build_audit_record(
        manifest_path,
        issues,
        generated_at=generated_at,
    )
    args.audit_output.parent.mkdir(parents=True, exist_ok=True)
    args.audit_output.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"P0 decision: {record['decision']} ({len(issues)} issue(s))")
    print(f"Audit: {args.audit_output.resolve().relative_to(PROJECT_ROOT)}")
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
