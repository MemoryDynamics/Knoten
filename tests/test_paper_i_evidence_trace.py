import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "paper/paper_i/supplement/evidence_manifest.json"


def _load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_manifest_has_one_bounded_claim_register() -> None:
    manifest = _load_manifest()

    assert manifest["schema"] == "paper-i-claim-evidence-trace-v1"
    assert manifest["version"] == 1
    assert re.fullmatch(r"[0-9a-f]{40}", manifest["evidence_snapshot_commit"])
    assert re.fullmatch(r"[0-9a-f]{40}", manifest["manuscript_snapshot_commit"])

    claims = manifest["claims"]
    assert 1 <= len(claims) <= 7
    assert [claim["id"] for claim in claims] == [
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "C6",
    ]
    assert len({claim["short_name"] for claim in claims}) == len(claims)
    assert len(manifest["release_blockers"]) <= 7


def test_every_evidence_path_exists_now_and_at_the_frozen_snapshot() -> None:
    manifest = _load_manifest()
    revision = manifest["evidence_snapshot_commit"]

    for claim in manifest["claims"]:
        for field in ("results", "code", "tests"):
            assert claim[field], f"{claim['id']} has no {field}"
            for relative in claim[field]:
                assert (ROOT / relative).is_file(), relative
                completed = subprocess.run(
                    ["git", "cat-file", "-e", f"{revision}:{relative}"],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                assert completed.returncode == 0, (
                    relative,
                    completed.stderr,
                )


def test_manifest_preserves_positive_and_negative_decisions() -> None:
    g1_g3 = json.loads(
        (
            ROOT
            / "reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_attempt_2_2026-09-27.json"
        ).read_text(encoding="utf-8")
    )
    g5 = json.loads(
        (
            ROOT
            / "reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_attempt_3_2026-09-17.json"
        ).read_text(encoding="utf-8")
    )
    g4 = json.loads(
        (
            ROOT
            / "reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.json"
        ).read_text(encoding="utf-8")
    )
    attempt4 = json.loads(
        (
            ROOT
            / "reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_4_2026-10-01.json"
        ).read_text(encoding="utf-8")
    )
    reconciliation = json.loads(
        (
            ROOT
            / "reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_infinity_endpoint_lemma_reconciliation_2026-10-01.json"
        ).read_text(encoding="utf-8")
    )

    assert (
        g1_g3["classification"]["decision"]
        == "rotating-wave-root-branch-connected-with-h2400-local-stability-support"
    )
    assert g5["classification"]["decision"] == "g5-local-direct-stability-pass"
    assert g4["classification"]["decision"] == "g4-local-infinite-root-pass"
    assert (
        attempt4["classification"]["decision"]
        == "g-infinity-branch-link-inconclusive"
    )
    assert (
        reconciliation["decision"]
        == "g-infinity-endpoint-lemma-reconciled-posthoc"
    )
    assert reconciliation["source_attempt_decision_unchanged"] is True


def test_scalar_summary_numbers_are_copied_exactly() -> None:
    manifest = _load_manifest()
    c1 = next(claim for claim in manifest["claims"] if claim["id"] == "C1")
    source = json.loads(
        (
            ROOT
            / "reports/long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.json"
        ).read_text(encoding="utf-8")
    )["baseline_error_summary"]

    assert str(source["median_retained_relative_error"]) in c1["supported_statement"]
    assert str(source["max_retained_relative_error"]) in c1["supported_statement"]
    assert source["n_slices"] == 9
