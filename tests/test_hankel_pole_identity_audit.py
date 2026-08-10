from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from emergenz_knoten import hankel_pole_identity as AUDIT
from emergenz_knoten import hankel_pole_identity_report as REPORT


ROOT = Path(__file__).resolve().parents[1]


def _encoded(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imag": float(value.imag)}


def _audits(value: complex) -> list[dict]:
    return [
        {
            "delay_depth": depth,
            "rank_fits": [
                {
                    "retained_rank": rank,
                    "eigenvalues": [_encoded(value), _encoded(value.conjugate())],
                }
                for rank in AUDIT.RANKS
            ],
        }
        for depth in AUDIT.DEPTHS
    ]


def test_candidate_filter_and_track_recover_stable_complex_pole() -> None:
    interval = 0.5
    value = 0.98 * np.exp(0.1j)
    poles = AUDIT.candidate_poles(
        {
            "eigenvalues": [
                _encoded(value),
                _encoded(value.conjugate()),
                _encoded(1.01 * np.exp(0.1j)),
                _encoded(0.9 + 0.0j),
            ]
        },
        interval,
    )

    assert len(poles) == 1
    track = AUDIT.fit_track(_audits(value), poles[0], interval)

    assert track["identity_pass"]
    assert track["matching_cells"] == 12
    np.testing.assert_allclose(track["median_frequency"], 0.2, atol=1e-12)


def test_seed_cluster_requires_control_separation() -> None:
    base = {
        "median_frequency": 0.2,
        "median_damping": 0.04,
        "control_matching_cells": 4,
    }
    passing = AUDIT.seed_clusters({1: [base], 2: [base], 3: []})
    failing = AUDIT.seed_clusters(
        {
            1: [{**base, "control_matching_cells": 7}],
            2: [{**base, "control_matching_cells": 8}],
            3: [],
        }
    )

    assert passing[0]["control_separated"]
    assert not failing[0]["control_separated"]


def test_stored_hankel_summary_has_no_control_separated_identity() -> None:
    source = ROOT / "reports/response/reciprocal/long_horizon_hankel_gate_2026-08-04.json"
    result = REPORT.analyze(json.loads(source.read_text(encoding="utf-8")))

    assert not result["pass"]
    assert result["cross_correlation_candidate_count"] == 4
    assert result["control_separated_cross_correlation_candidate_count"] == 0
