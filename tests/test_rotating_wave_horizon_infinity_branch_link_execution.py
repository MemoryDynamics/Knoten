from __future__ import annotations

import ast
import copy
import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXECUTION_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_infinity_branch_link_execution.py"
)


def _load_execution():
    specification = importlib.util.spec_from_file_location(
        "infinity_branch_link_execution_under_test", EXECUTION_PATH
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@pytest.fixture
def execution():
    return _load_execution()


def test_tracked_governance_is_closed_and_has_no_target_call(execution):
    governance = execution._load_governance()

    assert governance["state"] == "closed"
    assert governance["target_authorized"] is False
    assert governance["authorization"] is None
    assert governance["target_calls_recorded"] == []


def test_closed_governance_stops_before_metadata_receipt_or_modules(
    execution, monkeypatch
):
    def forbidden(*args, **kwargs):
        raise AssertionError("closed governance crossed a target boundary")

    monkeypatch.setattr(execution, "_create_receipt", forbidden)
    monkeypatch.setattr(execution, "_load_module", forbidden)
    with pytest.raises(RuntimeError, match="sealed by machine governance"):
        execution.require_target_authorization(metadata_fn=forbidden)
    with pytest.raises(RuntimeError, match="sealed by machine governance"):
        execution.execute_once()


def test_governance_rejects_recorded_target_call(execution, tmp_path: Path):
    payload = json.loads(
        (execution.ROOT / execution.GOVERNANCE_REL).read_text(encoding="utf-8")
    )
    payload["target_calls_recorded"] = ["forbidden"]
    path = tmp_path / "governance.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(RuntimeError, match="contains a target call"):
        execution._load_governance(path)


def test_readiness_parser_requires_exact_blob_table(execution):
    revision = "1" * 40
    rows = "\n".join(
        f"Blob `{path}`: `{'2' * 40}`" for path in execution.PROTECTED_PATHS
    )
    text = (
        f"Implementation revision: `{revision}`\n"
        "Verdict: **`g-infinity-branch-link-attempt-4-implementation-ready-target-closed`**\n"
        "https://github.com/MemoryDynamics/Knoten/actions/runs/123\n"
        f"{rows}\n"
    )

    parsed = execution._parse_readiness_review(text)

    assert parsed["implementation_revision"] == revision
    assert parsed["ci_run_id"] == 123
    with pytest.raises(RuntimeError, match="blob table mismatch"):
        execution._parse_readiness_review(text.replace(rows.splitlines()[0], ""))


def _authorized_governance(execution):
    implementation = "1" * 40
    run_id = 123456
    tracked = json.loads(
        (execution.ROOT / execution.GOVERNANCE_REL).read_text(encoding="utf-8")
    )
    schema_digest = hashlib.sha256(
        (execution.ROOT / execution.SCHEMA_REL).read_bytes()
    ).hexdigest()
    protected = {path: "2" * 40 for path in execution.PROTECTED_PATHS}
    protected[execution.PROTOCOL_REL.as_posix()] = tracked["protocol_blob"]
    return {
        "authorization": {
            "attempt": execution.ATTEMPT,
            "authorization_id": "12345678-1234-4abc-8def-123456789abc",
            "ci": {
                "api_url": (
                    "https://api.github.com/repos/MemoryDynamics/Knoten/"
                    f"actions/runs/{run_id}"
                ),
                "conclusion": "success",
                "head_sha": implementation,
                "run_id": run_id,
                "status": "completed",
            },
            "closed_governance_blob": "3" * 40,
            "dependencies": copy.deepcopy(execution.DEPENDENCIES),
            "implementation_revision": implementation,
            "protected_blobs": protected,
            "readiness_review_blob": "4" * 40,
            "readiness_review_path": execution.READINESS_REVIEW_REL.as_posix(),
            "schema_sha256": schema_digest,
        },
        "gate": "G-infinity-branch-link",
        "protocol_blob": tracked["protocol_blob"],
        "reason": "explicit-user-authorized-one-shot-branch-link",
        "result_schema_sha256": schema_digest,
        "schema": execution.GOVERNANCE_SCHEMA,
        "state": "authorized_once",
        "target_authorized": True,
        "target_calls_recorded": [],
    }


def _install_authorized_fakes(execution, monkeypatch, tmp_path: Path):
    payload = _authorized_governance(execution)
    source = tmp_path / "governance.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    authorization = payload["authorization"]
    head = "6" * 40

    def fake_blob(path: str, revision: str = "HEAD") -> str:
        if path == execution.PROTOCOL_REL.as_posix():
            return payload["protocol_blob"]
        if (
            path == execution.GOVERNANCE_REL.as_posix()
            and revision == authorization["implementation_revision"]
        ):
            return authorization["closed_governance_blob"]
        if path == execution.READINESS_REVIEW_REL.as_posix():
            return authorization["readiness_review_blob"]
        if path in authorization["protected_blobs"]:
            return authorization["protected_blobs"][path]
        raise AssertionError((path, revision))

    def fake_git(*arguments: str) -> str:
        if arguments[:2] == ("merge-base", "--is-ancestor"):
            return ""
        if arguments == (
            "diff",
            "--name-only",
            authorization["implementation_revision"],
            "HEAD",
        ):
            return (
                execution.READINESS_REVIEW_REL.as_posix()
                + "\n"
                + execution.GOVERNANCE_REL.as_posix()
            )
        if arguments == ("diff", "--name-only", "HEAD^", "HEAD"):
            return execution.GOVERNANCE_REL.as_posix()
        if arguments == ("status", "--porcelain", "--untracked-files=all"):
            return ""
        if arguments == ("rev-parse", "HEAD"):
            return head
        if arguments == ("rev-parse", "@{upstream}"):
            return head
        raise AssertionError(arguments)

    remote = {
        "conclusion": "success",
        "head_sha": authorization["implementation_revision"],
        "id": authorization["ci"]["run_id"],
        "repository": {"full_name": "MemoryDynamics/Knoten"},
        "status": "completed",
    }
    receipts = []
    events = []
    monkeypatch.setattr(execution, "_git_blob", fake_blob)
    monkeypatch.setattr(execution, "_git", fake_git)
    monkeypatch.setattr(
        execution,
        "_installed_dependencies",
        lambda: copy.deepcopy(execution.DEPENDENCIES),
    )
    monkeypatch.setattr(execution, "_validate_output_paths", lambda: None)
    monkeypatch.setattr(
        execution,
        "_load_module",
        lambda path, name: events.append(f"import:{path.name}")
        or SimpleNamespace(name=name),
    )
    review = [
        f"Implementation revision: `{authorization['implementation_revision']}`",
        "Verdict: **`g-infinity-branch-link-attempt-4-implementation-ready-target-closed`**",
        (
            "https://github.com/MemoryDynamics/Knoten/actions/runs/"
            f"{authorization['ci']['run_id']}"
        ),
    ]
    review.extend(
        f"Blob `{path}`: `{blob}`"
        for path, blob in authorization["protected_blobs"].items()
    )
    monkeypatch.setattr(execution, "_read_readiness_review", lambda: "\n".join(review))
    monkeypatch.setattr(
        execution,
        "_create_receipt",
        lambda **kwargs: events.append("receipt")
        or receipts.append(kwargs)
        or (execution.RECEIPT_REL.as_posix(), "7" * 64),
    )
    return source, remote, receipts, head, events


def test_authorization_binds_ci_blobs_upstream_and_consumes_once(
    execution, monkeypatch, tmp_path: Path
):
    source, remote, receipts, head, events = _install_authorized_fakes(
        execution, monkeypatch, tmp_path
    )

    result, gate, auditor = execution.require_target_authorization(
        governance_path=source, metadata_fn=lambda run_id: remote
    )

    assert result["revision"] == result["upstream_revision"] == head
    assert result["receipt_sha256"] == "7" * 64
    assert len(receipts) == 1
    assert gate.name == "authorized_infinity_branch_gate"
    assert auditor.name == "authorized_infinity_branch_auditor"
    assert events == [
        f"import:{execution.GATE_REL.name}",
        f"import:{execution.AUDITOR_REL.name}",
        "receipt",
    ]


def test_authorization_fails_before_receipt_on_remote_mismatch(
    execution, monkeypatch, tmp_path: Path
):
    source, remote, receipts, _, events = _install_authorized_fakes(
        execution, monkeypatch, tmp_path
    )
    remote["head_sha"] = "8" * 40

    with pytest.raises(RuntimeError, match="official CI"):
        execution.require_target_authorization(
            governance_path=source, metadata_fn=lambda run_id: remote
        )
    assert receipts == []
    assert events == []


@pytest.mark.parametrize("failure_index", [0, 1])
def test_import_failure_stops_before_receipt(
    execution, monkeypatch, tmp_path: Path, failure_index: int
):
    source, remote, receipts, _, events = _install_authorized_fakes(
        execution, monkeypatch, tmp_path
    )
    calls = []

    def failing_loader(path, name):
        calls.append((path, name))
        if len(calls) - 1 == failure_index:
            raise ImportError("synthetic incompatible runtime")
        return SimpleNamespace(name=name)

    with pytest.raises(ImportError, match="incompatible runtime"):
        execution.require_target_authorization(
            governance_path=source,
            metadata_fn=lambda run_id: remote,
            module_loader=failing_loader,
        )
    assert receipts == []
    assert "receipt" not in events
    assert len(calls) == failure_index + 1


@pytest.mark.parametrize("dependency", sorted(_load_execution().DEPENDENCIES))
def test_dependency_drift_stops_before_import_and_receipt(
    execution, monkeypatch, tmp_path: Path, dependency: str
):
    source, remote, receipts, _, events = _install_authorized_fakes(
        execution, monkeypatch, tmp_path
    )
    observed = copy.deepcopy(execution.DEPENDENCIES)
    observed[dependency] = "wrong"
    monkeypatch.setattr(execution, "_installed_dependencies", lambda: observed)

    with pytest.raises(RuntimeError, match="installed dependencies"):
        execution.require_target_authorization(
            governance_path=source, metadata_fn=lambda run_id: remote
        )
    assert receipts == []
    assert events == []


def test_missing_dependency_metadata_stops_before_import_and_receipt(
    execution, monkeypatch, tmp_path: Path
):
    source, remote, receipts, _, events = _install_authorized_fakes(
        execution, monkeypatch, tmp_path
    )

    def missing():
        raise importlib.metadata.PackageNotFoundError("numpy")

    monkeypatch.setattr(execution, "_installed_dependencies", missing)
    with pytest.raises(importlib.metadata.PackageNotFoundError):
        execution.require_target_authorization(
            governance_path=source, metadata_fn=lambda run_id: remote
        )
    assert receipts == []
    assert events == []


def test_receipt_is_exclusive(execution, monkeypatch, tmp_path: Path):
    monkeypatch.setattr(execution, "ROOT", tmp_path)
    monkeypatch.setattr(execution, "RECEIPT_REL", Path("receipt.json"))
    relative, digest = execution._create_receipt(
        authorization_id="00000000-0000-4000-8000-000000000001",
        ci_run_id=1,
        governance_sha256="a" * 64,
        implementation_revision="b" * 40,
        revision="c" * 40,
    )

    assert relative == "receipt.json"
    assert len(digest) == 64
    with pytest.raises(RuntimeError, match="already consumed"):
        execution._create_receipt(
            authorization_id="00000000-0000-4000-8000-000000000001",
            ci_run_id=1,
            governance_sha256="a" * 64,
            implementation_revision="b" * 40,
            revision="c" * 40,
        )


def test_execute_once_orders_guard_target_audit_publication_and_verification(
    execution, monkeypatch
):
    calls = []
    provenance = {
        "attempt": execution.ATTEMPT,
        "authorization_id": "00000000-0000-4000-8000-000000000001",
        "ci_run_id": 1,
        "governance_sha256": "a" * 64,
        "implementation_revision": "b" * 40,
        "receipt_path": "receipt.json",
        "receipt_sha256": "c" * 64,
        "revision": "d" * 40,
        "upstream_revision": "d" * 40,
    }
    payload = {"classification": {"decision": "synthetic"}}

    def run_contract(**kwargs):
        calls.append(("target", kwargs))
        return payload

    def publish(value, *, audit_fn):
        calls.append(("publish", value, audit_fn))

    gate = SimpleNamespace(run_contract=run_contract, publish=publish)
    auditor = SimpleNamespace(
        audit_payload_bytes=lambda *_: {},
        verify_publication=lambda: calls.append(("verify",)),
    )
    monkeypatch.setattr(
        execution,
        "require_target_authorization",
        lambda: calls.append(("guard",)) or (provenance, gate, auditor),
    )

    result = execution.execute_once()

    assert result is payload
    assert [row[0] for row in calls] == ["guard", "target", "publish", "verify"]


def test_module_import_has_no_top_level_target_call():
    tree = ast.parse(EXECUTION_PATH.read_text(encoding="utf-8"))
    calls = [
        node
        for node in tree.body
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
    ]

    assert calls == []
