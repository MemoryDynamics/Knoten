from __future__ import annotations

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
