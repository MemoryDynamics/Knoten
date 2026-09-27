from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXECUTION_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g1_g3_bridge_execution.py"
)


def _load_execution():
    spec = importlib.util.spec_from_file_location(
        "g1_g3_execution_under_test", EXECUTION_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def execution():
    return _load_execution()


def test_tracked_governance_is_closed_and_target_call_list_is_empty() -> None:
    execution = _load_execution()
    governance = execution._load_governance()
    assert governance["state"] == "closed"
    assert governance["target_authorized"] is False
    assert governance["authorization"] is None
    assert governance["target_calls_recorded"] == []


def test_closed_governance_stops_before_metadata_receipt_or_backend(
    monkeypatch,
) -> None:
    execution = _load_execution()

    def forbidden(*args, **kwargs):
        raise AssertionError("closed governance crossed a target boundary")

    monkeypatch.setattr(execution, "_github_run_metadata", forbidden)
    monkeypatch.setattr(execution, "_create_receipt", forbidden)
    monkeypatch.setattr(execution, "_load_module", forbidden)
    with pytest.raises(RuntimeError, match="sealed by machine governance"):
        execution.require_target_authorization(metadata_fn=forbidden)
    with pytest.raises(RuntimeError, match="sealed by machine governance"):
        execution.execute_once()


def test_governance_rejects_recorded_target_call(tmp_path: Path) -> None:
    execution = _load_execution()
    source = execution.ROOT / execution.GOVERNANCE_REL
    payload = json.loads(source.read_text(encoding="utf-8"))
    payload["target_calls_recorded"] = ["forbidden"]
    path = tmp_path / "governance.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(RuntimeError, match="contains a target call"):
        execution._load_governance(path)


def test_readiness_parser_requires_exact_protected_blob_table() -> None:
    execution = _load_execution()
    revision = "1" * 40
    rows = "\n".join(
        f"Blob `{path}`: `{'2' * 40}`" for path in execution.PROTECTED_PATHS
    )
    text = (
        f"Implementation revision: `{revision}`\n"
        "Verdict: **`g1-g3-implementation-ready-target-closed`**\n"
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
        "gate": "G1-G3",
        "protocol_blob": tracked["protocol_blob"],
        "reason": "explicit-user-authorized-one-shot-bridge",
        "result_schema_sha256": schema_digest,
        "schema": execution.GOVERNANCE_SCHEMA,
        "state": "authorized_once",
        "target_authorized": True,
        "target_calls_recorded": [],
    }


def _install_authorized_fakes(
    execution, monkeypatch, tmp_path: Path, *, governance=None
):
    payload = governance or _authorized_governance(execution)
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
    monkeypatch.setattr(execution, "_git_blob", fake_blob)
    monkeypatch.setattr(execution, "_git", fake_git)
    monkeypatch.setattr(
        execution,
        "_installed_dependencies",
        lambda: copy.deepcopy(execution.DEPENDENCIES),
    )
    monkeypatch.setattr(execution, "_validate_output_paths", lambda: None)
    review_lines = [
        f"Implementation revision: `{authorization['implementation_revision']}`",
        "",
        "Verdict: **`g1-g3-implementation-ready-target-closed`**",
        "",
        (
            "https://github.com/MemoryDynamics/Knoten/actions/runs/"
            f"{authorization['ci']['run_id']}"
        ),
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
        "_create_receipt",
        lambda **kwargs: receipts.append(kwargs)
        or (execution.RECEIPT_REL.as_posix(), "7" * 64),
    )
    return source, remote, receipts, head


def test_authorization_binds_ci_blobs_dependencies_upstream_and_consumes_once(
    execution, monkeypatch, tmp_path: Path
) -> None:
    source, remote, receipts, head = _install_authorized_fakes(
        execution, monkeypatch, tmp_path
    )

    result = execution.require_target_authorization(
        governance_path=source,
        metadata_fn=lambda run_id: remote,
    )

    assert result["revision"] == result["upstream_revision"] == head
    assert result["receipt_sha256"] == "7" * 64
    assert len(receipts) == 1
    assert receipts[0]["revision"] == head


@pytest.mark.parametrize(
    "mutation",
    (
        "remote-head",
        "dependency",
        "protected-blob",
        "source-drift",
        "mixed-commit",
        "readiness",
    ),
)
def test_authorization_fails_before_receipt_on_context_mutations(
    execution, monkeypatch, tmp_path: Path, mutation: str
) -> None:
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
    elif mutation == "source-drift":
        clean_git = execution._git

        def source_drift(*arguments: str) -> str:
            if arguments == (
                "diff",
                "--name-only",
                governance["authorization"]["implementation_revision"],
                "HEAD",
            ):
                return "src/emergenz_knoten/unreviewed.py"
            return clean_git(*arguments)

        monkeypatch.setattr(execution, "_git", source_drift)
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
            lambda: "Verdict: **`g1-g3-inconclusive`**",
        )

    with pytest.raises(RuntimeError):
        execution.require_target_authorization(
            governance_path=source,
            metadata_fn=lambda run_id: remote,
        )
    assert receipts == []


def test_receipt_is_exclusive_and_hash_bound(tmp_path: Path, monkeypatch) -> None:
    execution = _load_execution()
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


def test_execute_once_orders_guard_target_audit_and_publication(monkeypatch) -> None:
    execution = _load_execution()
    calls = []
    provenance = {
        "authorization_id": "00000000-0000-4000-8000-000000000001",
        "ci_run_id": 1,
        "governance_sha256": "a" * 64,
        "implementation_revision": "b" * 40,
        "receipt_path": "receipt.json",
        "receipt_sha256": "c" * 64,
        "revision": "d" * 40,
        "upstream_revision": "d" * 40,
    }

    class FakeBackend:
        pass

    def orchestrate_bridge(**kwargs):
        calls.append("target")
        assert isinstance(kwargs["backend"], FakeBackend)
        return {"classification": {"decision": "synthetic"}}

    component = SimpleNamespace(
        PARAMETERS={"synthetic": True},
        RegisteredBridgeBackend=FakeBackend,
        load_sealed_components=lambda: {"sealed": True},
        orchestrate_bridge=orchestrate_bridge,
        publish_bridge_result=lambda payload, report: calls.append("publish"),
    )
    auditor = SimpleNamespace(
        audit_payload=lambda payload: calls.append("audit")
        or {"decision": "synthetic"},
        audit_publication=lambda path: calls.append("reaudit"),
    )

    monkeypatch.setattr(
        execution,
        "require_target_authorization",
        lambda: calls.append("guard") or provenance,
    )
    monkeypatch.setattr(
        execution,
        "_load_module",
        lambda path, name: component if path == execution.ROOT / execution.COMPONENT_REL else auditor,
    )
    payload = execution.execute_once()
    assert payload["classification"]["decision"] == "synthetic"
    assert calls == ["guard", "target", "audit", "publish", "reaudit"]


def test_execution_module_has_no_top_level_target_call() -> None:
    tree = ast.parse(EXECUTION_PATH.read_text(encoding="utf-8"))

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


def test_guard_protects_complete_direct_numerical_dependency_set(execution) -> None:
    required = {
        "requirements.txt",
        "experiments/current/dynamics/rotation/"
        "scalar_memory_rotating_wave_horizon_transfer_gate.py",
        "experiments/current/dynamics/rotation/"
        "scalar_memory_rotating_wave_horizon_transfer_result_audit.py",
        "src/emergenz_knoten/rotating_wave.py",
        "src/emergenz_knoten/rotating_wave_dense_continuation.py",
        "src/emergenz_knoten/rotating_wave_interval.py",
        "src/emergenz_knoten/rotating_wave_horizon_stability.py",
        "src/emergenz_knoten/rotating_wave_stability.py",
        "src/emergenz_knoten/rotating_wave_stability_gate.py",
        "src/emergenz_knoten/strict_json_contract.py",
    }

    assert required <= set(execution.PROTECTED_PATHS)
