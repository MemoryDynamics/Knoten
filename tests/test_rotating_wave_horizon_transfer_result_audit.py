from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
AUDITOR_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_transfer_result_audit.py"
)
SCHEMA_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_transfer_result_schema_v3.json"
)
HORIZONS = (600, 900, 1200, 1500, 1800, 2400, 3600)


def _load_future_auditor():
    if not AUDITOR_PATH.is_file():
        return _MissingImplementation(AUDITOR_PATH.name)
    spec = importlib.util.spec_from_file_location(
        "horizon_transfer_auditor_under_test",
        AUDITOR_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class _MissingImplementation:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def __getattr__(self, name: str):
        raise AssertionError(
            f"{self.filename} is intentionally absent in the registered RED "
            "commit; the independent auditor is part of the next implementation "
            f"stage (first requested symbol: {name})"
        )


@pytest.fixture
def auditor():
    return _load_future_auditor()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest(result_path: Path, report_path: Path) -> dict[str, object]:
    return {
        "schema": "scalar-memory-rotating-wave-horizon-publication-v3",
        "artifacts": [
            {
                "role": "result-json",
                "path": result_path.name,
                "sha256": _sha256(result_path),
            },
            {
                "role": "readable-report",
                "path": report_path.name,
                "sha256": _sha256(report_path),
            },
        ],
    }


def test_auditor_source_does_not_import_runner_or_scientific_backend(auditor) -> None:
    source = Path(auditor.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    assert not any("horizon_transfer_gate" in name for name in imported)
    assert not any(name.startswith("emergenz_knoten") for name in imported)
    assert not any(name.startswith(("numpy", "scipy", "mpmath")) for name in imported)


def test_auditor_reads_manifest_before_schema_or_content(auditor, tmp_path: Path, monkeypatch) -> None:
    result_path = tmp_path / "result.json"
    report_path = tmp_path / "result.md"
    manifest_path = tmp_path / "result.publication.json"
    result_path.write_text("{}\n", encoding="utf-8")
    report_path.write_text("target-free fixture\n", encoding="utf-8")
    manifest_path.write_text(
        json.dumps(_manifest(result_path, report_path), sort_keys=True),
        encoding="utf-8",
    )
    reads: list[Path] = []
    original = auditor._read_bytes

    def recording_read(path: Path) -> bytes:
        reads.append(Path(path))
        return original(path)

    monkeypatch.setattr(auditor, "_read_bytes", recording_read)
    with pytest.raises((TypeError, ValueError)):
        auditor.audit_publication(manifest_path=manifest_path, schema_path=SCHEMA_PATH)
    assert reads[0] == manifest_path


def test_auditor_rejects_content_tampering_before_result_validation(
    auditor,
    tmp_path: Path,
    monkeypatch,
) -> None:
    result_path = tmp_path / "result.json"
    report_path = tmp_path / "result.md"
    manifest_path = tmp_path / "result.publication.json"
    result_path.write_text("{}\n", encoding="utf-8")
    report_path.write_text("target-free fixture\n", encoding="utf-8")
    manifest_path.write_text(
        json.dumps(_manifest(result_path, report_path), sort_keys=True),
        encoding="utf-8",
    )
    result_path.write_text('{"tampered":true}\n', encoding="utf-8")

    def forbidden(*args, **kwargs):
        raise AssertionError("result validation ran before the hash gate")

    monkeypatch.setattr(auditor, "validate_result", forbidden)
    with pytest.raises(ValueError, match="sha256"):
        auditor.audit_publication(manifest_path=manifest_path, schema_path=SCHEMA_PATH)


def test_auditor_independently_recomputes_q_and_tail_bounds(auditor) -> None:
    parameters = {
        "alpha": 0.01,
        "memory_mass": 1.0,
        "eta": 0.15,
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 3.5,
    }
    q_rows = auditor.q_representations(HORIZONS, alpha=parameters["alpha"])
    assert len(q_rows) == 7
    assert all(row["ulp_difference"] <= 2 for row in q_rows)
    assert q_rows[-1]["direct_power"] > 0.0

    phi0 = 1.0 + 3.5 / 9.0
    phi1 = math.exp(-0.5) * (1.0 + 3.5 / 27.0)
    observed = auditor.tail_bounds(horizon=3600, parameters=parameters)
    q_power = 0.99**3600
    assert float(observed["residual_bound"]) >= 2 * 0.15 * phi0 * q_power
    assert float(observed["jacobian_radius_bound"]) >= 4 * 0.15 * phi1 * q_power
    assert float(observed["jacobian_theta_bound"]) >= (
        0.15 * (phi0 + 2 * 1.1 * phi1) * q_power * (3600 + 0.99 / 0.01)
    )


def test_auditor_independently_recomputes_interval_drift_and_decision(auditor) -> None:
    first = {"radius": [0.946, 0.947], "theta": [0.0157, 0.0158]}
    second = {"radius": [0.9461, 0.9471], "theta": [0.01571, 0.01581]}
    drift = auditor.interval_drift_upper(
        first,
        second,
        radius_scale=0.946517504804225,
        theta_scale=0.015770381717135,
    )
    expected = max(
        0.0011 / 0.946517504804225,
        0.00011 / 0.015770381717135,
    )
    assert drift >= expected

    gates = {
        "G0": "pass",
        "G1F": "pass",
        "G1R": "inconclusive",
        "G2F": "pass",
        "G2R": "inconclusive",
        "G3": "pass",
        "G4": "pass",
        "G5": "pass",
        "G6": "pass",
        "local_branch_excluded": False,
        "large_h_instability_supported": False,
    }
    classification = auditor.classify_horizon(
        gates,
        lower_tail_status="lower-tail-stress-inconclusive",
    )
    assert classification["decision"] == (
        "rotating-wave-horizon-root-transfer-pass-with-large-h-stability-support"
    )
    assert classification["p5_governance_review_open"] is True


def test_auditor_rejects_wrong_root_keys_and_arnoldi_cardinality(auditor) -> None:
    witness = auditor.contract_witness()
    auditor.validate_result(witness)
    missing = dict(witness)
    missing.pop("controls")
    with pytest.raises((TypeError, ValueError), match="controls"):
        auditor.validate_result(missing)
    partial = json.loads(json.dumps(witness))
    partial["stability"]["arnoldi"]["primary"]["eigenpairs"].pop()
    with pytest.raises((TypeError, ValueError), match="eigenpairs"):
        auditor.validate_result(partial)


def test_auditor_accepts_a_complete_target_free_publication(auditor, tmp_path: Path) -> None:
    payload = auditor.contract_witness()
    result_path = tmp_path / "result.json"
    report_path = tmp_path / "result.md"
    manifest_path = tmp_path / "result.publication.json"
    result_path.write_text(
        json.dumps(payload, allow_nan=False, sort_keys=True),
        encoding="utf-8",
    )
    report_path.write_text("target-free complete fixture\n", encoding="utf-8")
    manifest_path.write_text(
        json.dumps(_manifest(result_path, report_path), sort_keys=True),
        encoding="utf-8",
    )
    result = auditor.audit_publication(
        manifest_path=manifest_path,
        schema_path=SCHEMA_PATH,
    )
    assert result["hashes_pass"] is True
    assert result["schema_pass"] is True
    assert result["decision"] == (
        "rotating-wave-horizon-root-transfer-pass-with-large-h-stability-support"
    )


def test_auditor_rejects_a_schema_valid_reconstruction_mismatch(
    auditor,
    tmp_path: Path,
) -> None:
    payload = auditor.contract_witness()
    payload["infinite_tail"]["q_representations"][0]["direct_power"] *= 1.0001
    result_path = tmp_path / "result.json"
    report_path = tmp_path / "result.md"
    manifest_path = tmp_path / "result.publication.json"
    result_path.write_text(
        json.dumps(payload, allow_nan=False, sort_keys=True),
        encoding="utf-8",
    )
    report_path.write_text("target-free mismatched fixture\n", encoding="utf-8")
    manifest_path.write_text(
        json.dumps(_manifest(result_path, report_path), sort_keys=True),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="q_representations"):
        auditor.audit_publication(
            manifest_path=manifest_path,
            schema_path=SCHEMA_PATH,
        )


def test_auditor_independently_rejects_null_holes_and_false_positive_gate(
    auditor,
) -> None:
    hole = auditor.contract_witness()
    hole["stability"]["continuation_arms"][0]["samples"][2] = None
    with pytest.raises(ValueError, match="prefix"):
        auditor._verify_reconstructed_values(hole)

    false_pass = auditor.contract_witness()
    false_pass["finite_branch"]["root_panels"][6] = None
    false_pass["finite_branch"]["homotopies"][3] = None
    false_pass["finite_branch"]["drift"]["center_diagnostics"][1] = None
    false_pass["finite_branch"]["drift"]["interval_upper_bounds"][1] = None
    false_pass["finite_branch"]["drift"]["pass"] = False
    false_pass["infinite_tail"]["certificate_panels"] = [None, None]
    false_pass["infinite_tail"]["panel_comparison"]["intersection"] = None
    false_pass["infinite_tail"]["panel_comparison"]["overlap"] = False
    with pytest.raises(ValueError, match="G1F"):
        auditor._verify_reconstructed_values(false_pass)

    false_summary = auditor.contract_witness()
    false_summary["controls"]["eta_zero_cases"][0]["pass"] = False
    with pytest.raises(ValueError, match="controls.pass"):
        auditor._verify_reconstructed_values(false_summary)


def test_auditor_independently_reconstructs_v3_interval_evidence(auditor) -> None:
    inner = auditor.contract_witness()
    inner["finite_branch"]["root_panels"][2]["inner_intersection"]["radius"][0] = "0"
    with pytest.raises(ValueError, match="inner_intersection"):
        auditor._verify_reconstructed_values(inner)

    slab = auditor.contract_witness()
    slab["finite_branch"]["homotopies"][0]["slabs"][3]["s_interval"] = ["0", "1"]
    with pytest.raises(ValueError, match="s_interval"):
        auditor._verify_reconstructed_values(slab)

    overlap = auditor.contract_witness()
    row = overlap["finite_branch"]["homotopies"][0]["slabs"][1]
    row["krawczyk_image"][0] = [
        "0.946577504804225",
        "0.946587504804225",
    ]
    with pytest.raises(ValueError, match="overlaps_previous"):
        auditor._verify_reconstructed_values(overlap)

    tail = auditor.contract_witness()
    tail["infinite_tail"]["panel_comparison"]["intersection"]["theta"][0] = "0"
    with pytest.raises(ValueError, match="panel_comparison"):
        auditor._verify_reconstructed_values(tail)


def test_auditor_independently_reconstructs_v3_stability_inputs(auditor) -> None:
    start = auditor.contract_witness()
    start["stability"]["arnoldi"]["primary"]["start_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="start_sha256"):
        auditor._verify_reconstructed_values(start)

    perturbation = auditor.contract_witness()
    perturbation["stability"]["continuation_arms"][2]["perturbation"][7] = 1.0
    with pytest.raises(ValueError, match="perturbation"):
        auditor._verify_reconstructed_values(perturbation)

    rounded = auditor.contract_witness()
    rounded["stability"]["rounded_root"][1] += 1e-12
    with pytest.raises(ValueError, match="rounded_root"):
        auditor._verify_reconstructed_values(rounded)

    spectral = auditor.contract_witness()
    spectral["stability"]["arnoldi"]["primary"]["eigenpairs"][3][
        "translation_overlap"
    ] = 1.0
    with pytest.raises(ValueError, match="classification"):
        auditor._verify_reconstructed_values(spectral)

    agreement = auditor.contract_witness()
    agreement["stability"]["arnoldi"]["panel_agreement"][
        "leading_transverse_distance"
    ] = 1e-6
    with pytest.raises(ValueError, match="leading_transverse_distance"):
        auditor._verify_reconstructed_values(agreement)

    trajectory = auditor.contract_witness()
    trajectory["stability"]["continuation_arms"][0]["growth_factor"] = 2.0
    with pytest.raises(ValueError, match="trajectory summary"):
        auditor._verify_reconstructed_values(trajectory)


def test_auditor_independently_rejects_unproved_exclusion(auditor) -> None:
    payload = auditor.contract_witness()
    contract = auditor._load_result_schema()
    attempt = auditor._witness_value(
        "object:branch_exclusion", contract, fill_nullable=True
    )
    attempt.update(
        {
            "from_horizon": 1200,
            "to_horizon": 1500,
            "max_depth": 20,
            "status": "all-residual-excluded",
        }
    )
    attempt["leaves"][0].update(
        {
            "classification": "residual-excluded",
            "residual_box": [["-1", "1"], ["-1", "1"]],
            "krawczyk_image": None,
            "strict_interior": None,
        }
    )
    payload["finite_branch"]["exclusions"][0] = attempt
    with pytest.raises(ValueError, match="does not exclude zero"):
        auditor._verify_reconstructed_values(payload)
