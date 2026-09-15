from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXECUTION_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g5_execution.py"
)


def _load():
    specification = importlib.util.spec_from_file_location(
        "g5_execution_under_test", EXECUTION_PATH
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@pytest.fixture
def execution():
    return _load()


def test_tracked_governance_is_closed_and_blocks_before_receipt(execution, monkeypatch):
    called = []
    tracked_governance = json.loads(
        (execution.ROOT / execution.GOVERNANCE_REL).read_text(encoding="utf-8")
    )
    clean_blob = execution._git_blob

    def current_protocol(path: str, revision: str = "HEAD") -> str:
        if path == execution.PROTOCOL_REL.as_posix() and revision == "HEAD":
            return tracked_governance["protocol_blob"]
        return clean_blob(path, revision)

    monkeypatch.setattr(execution, "_git_blob", current_protocol)
    monkeypatch.setattr(
        execution,
        "_create_attempt_receipt",
        lambda **kwargs: called.append(kwargs),
    )

    governance = execution._load_governance()

    assert governance["state"] == "closed"
    assert governance["target_authorized"] is False
    assert governance["authorization"] is None
    with pytest.raises(RuntimeError, match="sealed by machine governance"):
        execution.require_target_authorization()
    assert called == []


def _authorized_governance(execution):
    implementation = "1" * 40
    run_id = 123456
    schema_digest = hashlib.sha256((execution.ROOT / execution.SCHEMA_REL).read_bytes()).hexdigest()
    protected = {path: "2" * 40 for path in execution.PROTECTED_PATHS}
    protected[execution.PROTOCOL_REL.as_posix()] = "5" * 40
    return {
        "authorization": {
            "attempt": 1,
            "authorization_id": "12345678-1234-4abc-8def-123456789abc",
            "ci": {
                "api_url": f"https://api.github.com/repos/MemoryDynamics/Knoten/actions/runs/{run_id}",
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
        "gate": "G5",
        "protocol_blob": "5" * 40,
        "reason": "explicit-user-authorized-one-shot-attempt-1",
        "result_schema_sha256": schema_digest,
        "schema": execution.GOVERNANCE_SCHEMA,
        "state": "authorized_once",
        "target_authorized": True,
        "target_calls_recorded": [],
    }


def _install_authorized_fakes(execution, monkeypatch, tmp_path, *, governance=None):
    payload = governance or _authorized_governance(execution)
    source = tmp_path / "governance.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    authorization = payload["authorization"]
    head = "6" * 40

    def fake_blob(path: str, revision: str = "HEAD") -> str:
        if path == execution.PROTOCOL_REL.as_posix():
            return payload["protocol_blob"]
        if path == execution.GOVERNANCE_REL.as_posix() and revision == authorization["implementation_revision"]:
            return authorization["closed_governance_blob"]
        if path == execution.READINESS_REVIEW_REL.as_posix():
            return authorization["readiness_review_blob"]
        if path in authorization["protected_blobs"]:
            return authorization["protected_blobs"][path]
        raise AssertionError((path, revision))

    def fake_git(*arguments: str) -> str:
        if arguments[:2] == ("merge-base", "--is-ancestor"):
            return ""
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
    monkeypatch.setattr(execution, "_git_blob", fake_blob)
    monkeypatch.setattr(execution, "_git", fake_git)
    monkeypatch.setattr(
        execution, "_installed_dependencies", lambda: copy.deepcopy(execution.DEPENDENCIES)
    )
    monkeypatch.setattr(execution, "_validate_output_paths", lambda directory: None)
    review_lines = [
        f"Implementation revision: `{authorization['implementation_revision']}`",
        "",
        "Verdict: **`g5-implementation-ready-target-closed`**",
        "",
        f"https://github.com/MemoryDynamics/Knoten/actions/runs/{authorization['ci']['run_id']}",
        "",
    ]
    review_lines.extend(
        f"- Blob `{path}`: `{blob}`"
        for path, blob in authorization["protected_blobs"].items()
    )
    monkeypatch.setattr(
        execution, "_read_readiness_review", lambda: "\n".join(review_lines)
    )
    monkeypatch.setattr(
        execution,
        "_create_attempt_receipt",
        lambda **kwargs: receipts.append(kwargs)
        or (execution.ATTEMPT_RECEIPT_REL.as_posix(), "7" * 64),
    )
    return source, remote, receipts, head


def test_authorization_binds_ci_blobs_dependencies_upstream_and_consumes_once(
    execution, monkeypatch, tmp_path
):
    source, remote, receipts, head = _install_authorized_fakes(
        execution, monkeypatch, tmp_path
    )

    result = execution.require_target_authorization(
        governance_path=source,
        metadata_fn=lambda run_id: remote,
        output_directory=tmp_path,
    )

    assert result["attempt"] == 1
    assert result["revision"] == result["upstream_revision"] == head
    assert result["attempt_receipt_sha256"] == "7" * 64
    assert len(receipts) == 1
    assert receipts[0]["revision"] == head


@pytest.mark.parametrize(
    "mutation",
    ("remote-head", "dependency", "protected-blob", "mixed-commit", "readiness"),
)
def test_authorization_fails_before_receipt_on_context_mutations(
    execution, monkeypatch, tmp_path, mutation
):
    governance = _authorized_governance(execution)
    if mutation == "dependency":
        governance["authorization"]["dependencies"]["numpy"] = "0.0"
    source, remote, receipts, _ = _install_authorized_fakes(
        execution, monkeypatch, tmp_path, governance=governance
    )
    if mutation == "remote-head":
        remote["head_sha"] = "8" * 40
    elif mutation == "protected-blob":
        clean_blob = execution._git_blob

        def drifted(path: str, revision: str = "HEAD") -> str:
            if path == execution.PROTECTED_PATHS[0] and revision == "HEAD":
                return "9" * 40
            return clean_blob(path, revision)

        monkeypatch.setattr(execution, "_git_blob", drifted)
    elif mutation == "mixed-commit":
        clean_git = execution._git

        def mixed(*arguments: str) -> str:
            if arguments == ("diff", "--name-only", "HEAD^", "HEAD"):
                return execution.GOVERNANCE_REL.as_posix() + "\nREADME.md"
            return clean_git(*arguments)

        monkeypatch.setattr(execution, "_git", mixed)
    elif mutation == "readiness":
        monkeypatch.setattr(
            execution,
            "_read_readiness_review",
            lambda: "Verdict: **`g5-inconclusive`**",
        )

    with pytest.raises(RuntimeError):
        execution.require_target_authorization(
            governance_path=source,
            metadata_fn=lambda run_id: remote,
            output_directory=tmp_path,
        )
    assert receipts == []


def test_execute_once_cannot_import_numerical_target_while_governance_is_closed(
    execution, monkeypatch
):
    tracked_governance = json.loads(
        (execution.ROOT / execution.GOVERNANCE_REL).read_text(encoding="utf-8")
    )
    clean_blob = execution._git_blob

    def current_protocol(path: str, revision: str = "HEAD") -> str:
        if path == execution.PROTOCOL_REL.as_posix() and revision == "HEAD":
            return tracked_governance["protocol_blob"]
        return clean_blob(path, revision)

    monkeypatch.setattr(execution, "_git_blob", current_protocol)
    monkeypatch.setattr(
        execution,
        "_load_module",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("numerical module reached")
        ),
    )

    with pytest.raises(RuntimeError, match="sealed by machine governance"):
        execution.execute_once()


def test_execution_module_has_no_top_level_target_call():
    source = EXECUTION_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    for statement in tree.body:
        assert not (
            isinstance(statement, ast.If)
            and isinstance(statement.test, ast.Compare)
            and isinstance(statement.test.left, ast.Name)
            and statement.test.left.id == "__name__"
        )
        assert not (
            isinstance(statement, ast.Expr)
            and isinstance(statement.value, ast.Call)
            and isinstance(statement.value.func, ast.Name)
            and statement.value.func.id == "execute_once"
        )
