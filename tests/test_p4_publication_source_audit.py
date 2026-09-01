from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
REVIEW_ROOT = ROOT / "reports" / "project" / "meta" / "reviews"
AUDIT = REVIEW_ROOT / "p4_publication_source_referee_audit_2026-08-27.md"
FINDINGS = (
    REVIEW_ROOT / "p4_publication_source_referee_findings_2026-08-27.json"
)
TRACE = REVIEW_ROOT / "p4_publication_source_claim_trace_2026-08-27.json"
REPRODUCTION = (
    REVIEW_ROOT / "p4_publication_source_reproduction_2026-08-27.json"
)
INDEPENDENT = (
    REVIEW_ROOT / "p4r_independent_result_recompute_2026-08-27.json"
)
VERDICT = "referee-source-ready-with-major-claim-restrictions"


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _path_from_immutable_url(artifact: dict[str, object]) -> str:
    marker = f"/blob/{artifact['commit']}/"
    url = str(artifact["url"])
    assert marker in url
    assert "/blob/main/" not in url
    return url.split(marker, maxsplit=1)[1]


def _git_output(*arguments: str, text: bool = True):
    return subprocess.check_output(
        ["git", *arguments],
        cwd=ROOT,
        text=text,
    )


def test_required_source_audit_artifacts_are_complete() -> None:
    for path in (AUDIT, FINDINGS, TRACE, REPRODUCTION, INDEPENDENT):
        assert path.is_file()
        assert path.stat().st_size > 0

    report = AUDIT.read_text(encoding="utf-8")
    assert f"Verdict: **`{VERDICT}`**." in report
    for label in (
        "Pass A",
        "Pass B",
        "Pass C",
        "Pass D",
        "Pass E",
        "Pass F",
        "Pass G",
    ):
        assert label in report


def test_claim_trace_rows_have_immutable_and_reproducible_sources() -> None:
    payload = _load(TRACE)
    claims = payload["claims"]
    required = {
        "claim_id",
        "exact_wording",
        "evidence_class",
        "protocol",
        "raw_result",
        "critical_review",
        "code",
        "scope",
        "excluded_claims",
        "status_consistency",
    }
    assert len(claims) == 11
    assert len({row["claim_id"] for row in claims}) == len(claims)

    for row in claims:
        assert required <= set(row)
        assert row["status_consistency"]["consistent"] is True
        artifacts = [
            row["protocol"],
            row["raw_result"],
            row["critical_review"],
            *row["code"],
        ]
        for artifact in artifacts:
            path = _path_from_immutable_url(artifact)
            observed = _git_output(
                "rev-parse",
                f"{artifact['commit']}:{path}",
            ).strip()
            assert observed == artifact["blob"]

        raw = row["raw_result"]
        raw_path = _path_from_immutable_url(raw)
        content = _git_output(
            "show",
            f"{raw['commit']}:{raw_path}",
            text=False,
        )
        assert hashlib.sha256(content).hexdigest() == raw["canonical_lf_sha256"]


def test_claim_trace_preserves_all_major_claim_restrictions() -> None:
    claims = {row["claim_id"]: row for row in _load(TRACE)["claims"]}
    existence = claims["RW-EXISTENCE-02"]
    assert "konditional" in existence["exact_wording"]
    assert "mpmath.iv" in existence["exact_wording"]

    assert claims["LOOP-CENTER-P2-07"]["raw_result"]["decision"] == (
        "loop-center-matrix-local-fail"
    )
    assert claims["LOOP-PORT-P4-10"]["raw_result"]["decision"] == (
        "p4-source-write-architecture-fail"
    )
    p4r = claims["LOOP-PORT-P4R-11"]
    exclusions = " ".join(p4r["excluded_claims"]).lower()
    assert "continuous phase" in exclusions
    assert "replications" in exclusions
    assert "spin" in exclusions
    assert "mass" in exclusions


def test_findings_schema_and_restricted_verdict_agree() -> None:
    payload = _load(FINDINGS)
    assert payload["verdict"] == VERDICT
    required = {
        "finding_id",
        "severity",
        "domain",
        "claim_id",
        "summary",
        "evidence_paths",
        "reproduction_command",
        "observed",
        "expected",
        "scientific_impact",
        "required_remediation",
        "status",
    }
    findings = payload["findings"]
    assert len({row["finding_id"] for row in findings}) == len(findings)
    assert all(required == set(row) for row in findings)
    assert not any(row["severity"] == "critical" for row in findings)
    assert sum(row["severity"] == "major" for row in findings) == 3
    assert payload["counts"]["critical_open"] == 0
    assert payload["counts"]["major_open"] == 3
    assert payload["p4rs_compatibility"][
        "eligible_after_claim_language_commit_is_pushed"
    ] is True
    assert payload["p4rs_compatibility"]["p5_open"] is False


def test_reproduction_and_independent_recompute_agree_exactly() -> None:
    reproduction = _load(REPRODUCTION)
    assert reproduction["conclusion"][
        "scientific_decision_invariant_across_environments"
    ] is True
    assert reproduction["conclusion"]["full_source_ready"] is False
    assert reproduction["predeclared_replay_comparison"][
        "observed_maximum_scientific_difference"
    ] == 0.0
    assert len(reproduction["environments"]) == 2
    for environment in reproduction["environments"]:
        replay = environment["p4r_replay"]
        assert replay["exact_scientific_top_level_blocks"] is True
        assert replay["decision_equal"] is True
        assert replay["all_gate_booleans_equal"] is True
        assert replay["all_decisive_floats_equal"] is True

    independent = _load(INDEPENDENT)
    assert independent["decision"] == "p4r-independent-audit-agrees"
    assert independent["recomputed_decision"] == (
        "p4r-phase-averaged-chiral-response-pass"
    )
    assert independent["differences"] == []
    content = INDEPENDENT.read_bytes().replace(b"\r\n", b"\n").replace(
        b"\r", b"\n"
    )
    assert hashlib.sha256(content).hexdigest() == (
        reproduction["independent_result_recomputation"][
            "output_canonical_lf_sha256"
        ]
    )


def test_public_status_surfaces_propagate_source_and_p4rs_boundaries() -> None:
    required_phrases = {
        "README.md": (VERDICT, "P4-R-S-Anchor-Holdout", "keine Replikation"),
        "docs/index.md": (
            VERDICT,
            "P4-R-S-Anchor-Holdout",
            "0.00232715",
            "Implementierung, Interaktionsziellauf und Evidenz bleiben",
        ),
        "docs/status/current_status.md": (
            VERDICT,
            "p4rs-anchor-scale-transfer-pass",
            "P5-Implementierung, Targetzugriff und Interaktionsevidenz",
        ),
        "docs/status/paper_claims.md": (
            VERDICT,
            "P4-R-S Anchor-Skalenholdout -- reviewed Pass",
            "keine Konvergenzordnung",
        ),
        "docs/status/project_priorities.md": (
            "p4rs-anchor-scale-transfer-pass",
            "n0-noise-stability-window-bracketed-reviewed-pass",
            "Prioritaet 1: P5-Designaudit ohne Targetzugriff",
            "P5 Target<br/>weiter versiegelt",
        ),
        "reports/README.md": (
            VERDICT,
            "P4-R-S-Anchor-Lauf",
            "P5-Implementierung",
        ),
        "reports/dynamics/rotation/README.md": (
            VERDICT,
            "p4rs-anchor-scale-transfer-pass",
            "P5-Implementierung",
        ),
        "experiments/current/dynamics/rotation/README.md": (
            VERDICT,
            "p4rs-anchor-scale-transfer-pass",
            "P5-Implementierung",
        ),
        "docs/reference/repository_map.md": (
            "P4-R-phi reviewed pass",
            "P4-R-S reviewed pass",
            "N0 reviewed pass",
            "P5 design active",
            "keine Replikationen",
        ),
        "docs/reference/experiment_catalog.md": (
            VERDICT,
            "p4r-independent-audit-agrees",
            "p4rs-anchor-scale-transfer-pass",
            "keine Konvergenzordnung",
        ),
    }
    for relative, phrases in required_phrases.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        for phrase in phrases:
            assert phrase.casefold() in content.casefold(), (
                f"{phrase!r} missing from {relative}"
            )
