from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPTS = (
    ROOT / "paper/paper_i/manuscript/main.tex",
    ROOT / "paper/paper_i/manuscript/main_compact.tex",
)


@pytest.mark.parametrize("path", MANUSCRIPTS)
def test_rotating_wave_section_preserves_claim_boundaries(path):
    text = path.read_text(encoding="utf-8")
    lower = text.lower()

    assert "B_H(z)" in text
    assert r"F_H(R,\theta)=0" in text
    assert "prospective uniform-tail run remains formally inconclusive" in lower
    assert "post-hoc" in lower
    assert "R0--R6" in text
    assert r"H\to\infty" in text
    assert r"\mu_F" in text
    assert "interval backend" in lower or "interval-backend" in lower
    assert "physical mass" in lower
    assert "claim-to-result, code, audit, test, and exclusion map" in lower
    assert "ace7000351b7c4ccba8f9cfc8b7464c3361993f2" in text
    assert "certified to $H=\\infty$" not in text


def test_long_manuscript_reserves_h_for_fifo_horizon():
    text = MANUSCRIPTS[0].read_text(encoding="utf-8")

    assert r"let $\mathcal H$ be the Hessian" in text
    assert r"let $H$ be the Hessian" not in text
    assert r"q=1-\alpha" in text
    assert r"H=(600,900,1200,1500,1800,2400,3600)" in text


def test_active_claim_register_records_posthoc_reconciliation():
    claims = (ROOT / "docs/status/paper_claims.md").read_text(encoding="utf-8")
    guide = (ROOT / "docs/reference/horizon_transfer_guide.md").read_text(
        encoding="utf-8"
    )

    assert "Endpoint-Lemma-Reconciliation -- reviewed post-hoc Pass" in claims
    assert "der letzte zertifizierte Rootasttransfer" not in claims
    assert "besteht jedoch" in guide
    assert "R0--R6" in guide
    assert "dynamische $H\\to\\infty$-Stabilitaet offen" in guide
