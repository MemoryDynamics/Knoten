from __future__ import annotations

import copy
import hashlib
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g4_component_gate.py"
)
AUDITOR_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g4_component_result_audit.py"
)


def _load(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@pytest.fixture
def runner():
    return _load(RUNNER_PATH, "g4_component_runner_under_test")


@pytest.fixture
def auditor():
    return _load(AUDITOR_PATH, "g4_component_auditor_under_test")


def _certificate(root: tuple[str, str], half_width: str, image_shift: str = "0"):
    from decimal import Decimal, localcontext

    with localcontext() as context:
        context.prec = 180
        width = Decimal(half_width)
        shift = Decimal(image_shift)
        centers = [Decimal(value) for value in root]
        return {
            "box": {
                coordinate: [format(center - width, "f"), format(center + width, "f")]
                for coordinate, center in zip(("radius", "theta"), centers, strict=True)
            },
            "interval_backend": "mpmath.iv",
            "jacobian_box": [
                [["1", "2"], ["3", "4"]],
                [["5", "6"], ["7", "8"]],
            ],
            "krawczyk_image": [
                [format(center + shift, "f"), format(center + shift, "f")]
                for center in centers
            ],
            "strict_interior": True,
        }


def _finite(root: tuple[str, str] = ("0.95", "0.015")):
    return {
        "newton": {
            "jacobian": [["1", "0"], ["0", "1"]],
            "precision_dps": 120,
            "radius": root[0],
            "residual": ["0", "0"],
            "steps": 8,
            "theta": root[1],
        },
        "outer_certificate": _certificate(root, "1e-8"),
        "inner_certificate": _certificate(root, "1e-30"),
    }


def _payload(runner, *, tail_failure: int | None = None, disjoint: bool = False):
    finite = _finite()
    root = (finite["newton"]["radius"], finite["newton"]["theta"])
    calls = []

    def finite_fn(**kwargs):
        calls.append(("finite", kwargs))
        return copy.deepcopy(finite)

    def tail_fn(**kwargs):
        calls.append(("tail", kwargs))
        if kwargs["precision_dps"] == tail_failure:
            return None
        shift = "-5e-11" if kwargs["precision_dps"] == 120 else "5e-11"
        if not disjoint:
            shift = "0"
        return {
            "certificate": _certificate(root, "1e-10", shift),
            "precision_dps": kwargs["precision_dps"],
            "root": list(root),
        }

    payload = runner.run_component(
        execution_commit="a" * 40,
        protocol_sha256="b" * 64,
        finite_root_fn=finite_fn,
        tail_fn=tail_fn,
        created_utc="2026-09-13T00:00:00+00:00",
    )
    return payload, calls


def test_component_pass_uses_only_registered_finite_root_and_two_tail_panels(runner):
    payload, calls = _payload(runner)

    assert [(name, values.get("precision_dps")) for name, values in calls] == [
        ("finite", 120),
        ("tail", 120),
        ("tail", 160),
    ]
    assert calls[0][1] == {"horizon": 3600, "precision_dps": 120, "start": runner.START}
    assert payload["classification"] == {
        "G4": "pass",
        "decision": "g4-local-infinite-root-pass",
        "claim_boundary": (
            "local F_infinity root conditional on registered tail bounds and "
            "mpmath.iv; no branch-transfer, stability, formation, interaction, or mass claim"
        ),
    }


def test_component_stops_after_failed_tail_panel(runner):
    payload, calls = _payload(runner, tail_failure=120)

    assert [name for name, _ in calls] == ["finite", "tail"]
    assert payload["infinite_tail"]["certificate_panels"] == [None, None]
    assert payload["classification"]["decision"] == "g4-inconclusive"


def test_disjoint_strict_tail_images_are_inconclusive(runner):
    payload, _ = _payload(runner, disjoint=True)

    assert payload["infinite_tail"]["panel_comparison"] == {
        "intersection": None,
        "overlap": False,
    }
    assert payload["classification"]["G4"] == "inconclusive"


def test_runner_validator_rejects_unknown_fields_and_false_pass(runner):
    payload, _ = _payload(runner)
    gate = runner._load_horizon_gate()

    unknown = copy.deepcopy(payload)
    unknown["unexpected"] = True
    with pytest.raises(ValueError, match="root fields"):
        runner.validate_payload(unknown, gate=gate)

    false_pass = copy.deepcopy(payload)
    false_pass["infinite_tail"]["certificate_panels"][1] = None
    with pytest.raises(ValueError, match="panel_comparison"):
        runner.validate_payload(false_pass, gate=gate)

    invalid_newton = copy.deepcopy(payload)
    invalid_newton["finite_root"]["newton"]["residual"] = ["0", "NaN"]
    with pytest.raises(ValueError, match="residual"):
        runner.validate_payload(invalid_newton, gate=gate)


def test_registered_box_accepts_only_tiny_outward_serialization_slack(runner):
    from decimal import Decimal, localcontext

    payload, _ = _payload(runner)
    gate = runner._load_horizon_gate()
    interval = payload["finite_root"]["outer_certificate"]["box"]["radius"]
    with localcontext() as context:
        context.prec = 200
        interval[0] = format(Decimal(interval[0]) - Decimal("1e-121"), "f")
        interval[1] = format(Decimal(interval[1]) + Decimal("1e-121"), "f")
    runner.validate_payload(payload, gate=gate)

    with localcontext() as context:
        context.prec = 200
        interval[0] = format(Decimal(interval[0]) - Decimal("1e-115"), "f")
    with pytest.raises(ValueError, match="registered box"):
        runner.validate_payload(payload, gate=gate)


def _redirect_outputs(module, temporary: Path) -> None:
    module.RESULT = temporary / "scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.json"
    module.REPORT = module.RESULT.with_suffix(".md")
    module.MANIFEST = module.RESULT.with_suffix(".publication.json")


def _rehash_result(auditor) -> None:
    manifest = auditor._load_json(auditor.MANIFEST)
    manifest["artifacts"][0]["sha256"] = hashlib.sha256(
        auditor.RESULT.read_bytes()
    ).hexdigest()
    auditor.MANIFEST.write_text(
        auditor.json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_publication_and_independent_audit_agree(runner, auditor, tmp_path: Path):
    _redirect_outputs(runner, tmp_path)
    _redirect_outputs(auditor, tmp_path)
    payload, _ = _payload(runner)
    payload["identity"]["protocol_sha256"] = hashlib.sha256(
        runner.PROTOCOL.read_bytes()
    ).hexdigest()
    runner.publish(payload)

    observed = auditor.audit()

    assert observed["verdict"] == "g4-independent-audit-agrees"
    assert observed["decision"] == "g4-local-infinite-root-pass"
    assert all(observed["checks"].values())


def test_independent_audit_accepts_bounded_outward_box_serialization(
    runner, auditor, tmp_path: Path
):
    from decimal import Decimal, localcontext

    _redirect_outputs(runner, tmp_path)
    _redirect_outputs(auditor, tmp_path)
    payload, _ = _payload(runner)
    payload["identity"]["protocol_sha256"] = hashlib.sha256(
        runner.PROTOCOL.read_bytes()
    ).hexdigest()
    interval = payload["finite_root"]["outer_certificate"]["box"]["radius"]
    with localcontext() as context:
        context.prec = 200
        interval[0] = format(Decimal(interval[0]) - Decimal("1e-121"), "f")
        interval[1] = format(Decimal(interval[1]) + Decimal("1e-121"), "f")
    runner.publish(payload)

    observed = auditor.audit()

    assert observed["verdict"] == "g4-independent-audit-agrees"
    assert all(observed["checks"].values())


def test_auditor_rejects_hash_and_bound_mutations(runner, auditor, tmp_path: Path):
    _redirect_outputs(runner, tmp_path)
    _redirect_outputs(auditor, tmp_path)
    payload, _ = _payload(runner)
    payload["identity"]["protocol_sha256"] = hashlib.sha256(
        runner.PROTOCOL.read_bytes()
    ).hexdigest()
    runner.publish(payload)

    runner.REPORT.write_text("mutated", encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        auditor.audit()

    runner.publish(payload)
    result = runner.RESULT.read_text(encoding="utf-8").replace(
        '"residual_bound":', '"mutated_bound":', 1
    )
    runner.RESULT.write_text(result, encoding="utf-8")
    _rehash_result(auditor)
    with pytest.raises(ValueError, match="tail bounds"):
        auditor.audit()


def test_auditor_rejects_nonprefix_panels_and_report_drift(
    runner, auditor, tmp_path: Path
):
    _redirect_outputs(runner, tmp_path)
    _redirect_outputs(auditor, tmp_path)
    payload, _ = _payload(runner)
    payload["identity"]["protocol_sha256"] = hashlib.sha256(
        runner.PROTOCOL.read_bytes()
    ).hexdigest()
    runner.publish(payload)

    mutated = auditor._load_json(auditor.RESULT)
    mutated["infinite_tail"]["certificate_panels"][0] = None
    auditor.RESULT.write_text(
        auditor.json.dumps(mutated, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _rehash_result(auditor)
    with pytest.raises(ValueError, match="completed prefix"):
        auditor.audit()

    runner.publish(payload)
    runner.REPORT.write_text(
        runner.REPORT.read_text(encoding="utf-8") + "unregistered note\n",
        encoding="utf-8",
    )
    manifest = auditor._load_json(auditor.MANIFEST)
    manifest["artifacts"][1]["sha256"] = hashlib.sha256(
        runner.REPORT.read_bytes()
    ).hexdigest()
    auditor.MANIFEST.write_text(
        auditor.json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="readable report"):
        auditor.audit()


def test_execution_context_refuses_dirty_or_existing_artifacts(runner, monkeypatch):
    monkeypatch.setattr(runner.mpmath, "__version__", "1.3.0")
    monkeypatch.setattr(runner, "_git_output", lambda *args: "dirty" if args[0] == "status" else "a" * 40)
    with pytest.raises(RuntimeError, match="clean worktree"):
        runner.require_execution_context()
