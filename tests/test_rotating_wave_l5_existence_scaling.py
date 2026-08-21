from decimal import Decimal
import json
import subprocess
from typing import Any

import mpmath
from mpmath import mp
import pytest

from emergenz_knoten.rotating_wave import finite_h_rotating_wave_residual
from experiments.current.dynamics.rotation import (
    scalar_memory_rotating_wave_l5_existence_scaling as l5,
)


def test_l5_registration_preserves_exact_matched_scaling():
    tail, gain = l5.exact_decimal_scaling(
        alpha=l5.L5_CELL["alpha"],
        horizon=l5.L5_CELL["horizon"],
        eta=l5.L5_CELL["eta"],
    )

    assert tail
    assert gain
    assert Decimal(l5.L5_CELL["alpha"]) * l5.L5_CELL["horizon"] == Decimal("12")
    assert Decimal(l5.L5_CELL["eta"]) / Decimal(l5.L5_CELL["alpha"]) == Decimal("15")


def test_frozen_l5_input_hashes_match_repository_git_blobs():
    result = l5.input_hash_audit()

    assert result["pass"]
    assert result["hash_domain"] == "git-head-blob"
    assert len(result["rows"]) == 3
    assert all(
        row["observed_sha256"] == row["expected_sha256"]
        for row in result["rows"]
    )


def test_l5_provenance_gate_preserves_sealed_inputs_and_transfer_center():
    ladder = json.loads((l5.ROOT / l5.REFINEMENT_LADDER).read_text(encoding="utf-8"))
    foundation = json.loads((l5.ROOT / l5.FOUNDATION_AUDIT).read_text(encoding="utf-8"))
    continuum = json.loads(
        (l5.ROOT / l5.CONTINUUM_RECONCILIATION).read_text(encoding="utf-8")
    )

    result = l5.provenance_audit(ladder, foundation, continuum)

    assert result["pass"]
    assert all(result["source_gates"].values())
    assert all(row["exists_and_is_ancestor"] for row in result["revisions"])


def test_independent_finite_sum_matches_project_residual_off_target():
    parameters = {
        "radius": 0.73,
        "theta": 0.11,
        "alpha": 0.07,
        "horizon": 17,
        "eta": 0.19,
    }
    with mp.workdps(50):
        observed = l5.independent_finite_balance(**parameters)
    expected = finite_h_rotating_wave_residual(
        **parameters,
        memory_mass=1.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=3.5,
    )

    assert float(observed[0]) == pytest.approx(expected.real, abs=2.0e-15)
    assert float(observed[1]) == pytest.approx(expected.imag, abs=2.0e-15)


def _synthetic_cell(name: str, alpha: str, radius: Any, omega: Any) -> dict:
    return {
        "cell": name,
        "alpha": alpha,
        "panels": [
            {
                "precision_dps": 120,
                "refined": {"radius": mp.nstr(radius, 50)},
                "omega": mp.nstr(omega, 50),
            }
        ],
    }


def _exact_first_order_cells() -> list[dict]:
    with mp.workdps(60):
        target_radius = mp.mpf(l5.CONTINUUM_RADIUS)
        target_omega = mp.mpf(l5.CONTINUUM_OMEGA)
        registered = [*l5.EXPECTED_LADDER_CELLS, ("L5", "0.00125", 9600, "0.01875")]
        return [
            _synthetic_cell(
                name,
                alpha,
                target_radius + mp.mpf("0.4") * mp.mpf(alpha),
                target_omega - mp.mpf("0.7") * mp.mpf(alpha),
            )
            for name, alpha, _, _ in registered
        ]


def test_scaling_gate_accepts_exact_first_order_family():
    cells = _exact_first_order_cells()

    result = l5.scaling_diagnostics(cells[:-1], cells[-1])

    assert result["pass"]
    assert float(result["radius"]["slope"]) == pytest.approx(1.0, abs=1.0e-12)
    assert float(result["omega"]["slope"]) == pytest.approx(1.0, abs=1.0e-12)
    assert float(result["radius"]["signed_error_contraction"]) == pytest.approx(0.5)
    assert float(result["omega"]["successive_difference_contraction"]) == pytest.approx(0.5)


def test_scaling_gate_rejects_l5_branch_crossing():
    cells = _exact_first_order_cells()
    with mp.workdps(60):
        target = mp.mpf(l5.CONTINUUM_RADIUS)
        crossed_radius = target - mp.mpf("0.4") * mp.mpf(cells[-1]["alpha"])
        cells[-1]["panels"][0]["refined"]["radius"] = mp.nstr(crossed_radius, 50)

    result = l5.scaling_diagnostics(cells[:-1], cells[-1])

    assert not result["pass"]
    assert not result["radius"]["gates"]["signed_error_contraction"]


def test_corridor_rejects_intermediate_branch_excursion():
    initial_theta = l5._scaled(l5.OMEGA_START, l5.L5_CELL["alpha"])
    valid = [
        {"radius": l5.RADIUS_START, "theta": initial_theta},
        {
            "radius": str(Decimal(l5.RADIUS_START) + Decimal("0.001")),
            "theta": str(
                Decimal(initial_theta)
                + Decimal(l5.L5_CELL["alpha"]) * Decimal("0.001")
            ),
        },
    ]
    excursion = [
        *valid,
        {
            "radius": str(Decimal(l5.RADIUS_START) + Decimal("0.02")),
            "theta": initial_theta,
        },
    ]

    assert l5._corridor_pass(valid)
    assert not l5._corridor_pass(excursion)


def test_inconclusive_report_never_renders_positive_claim():
    payload = {
        "generated_utc": "2026-08-21T00:00:00+00:00",
        "decision": "l5-existence-inconclusive",
        "execution_revision": "deadbeef",
        "protocol_revision": l5.PROTOCOL_REVISION,
        "exception": "RuntimeError: synthetic failure",
    }

    report = l5.render_report(payload)

    assert "No positive existence or scaling claim is authorized" in report
    assert "## L5 interval panels" not in report


def test_committed_l5_result_retains_every_registered_pass():
    payload = json.loads((l5.ROOT / l5.DEFAULT_SUMMARY).read_text(encoding="utf-8"))

    assert payload["decision"] == "l5-existence-scaling-pass"
    assert payload["execution_revision"] == "a8787cdefd12b86e13928613790708883e2c55e1"
    assert payload["protocol_revision"] == l5.PROTOCOL_REVISION
    assert payload["git_status_at_start"] == ""
    assert payload["exception"] is None
    assert payload["provenance"]["pass"]
    assert payload["l5_cell"]["pass"]
    assert payload["l5_cell"]["cross_precision"]["pass"]
    assert all(panel["pass"] for panel in payload["l5_cell"]["panels"])
    assert all(
        box["pass"]
        for panel in payload["l5_cell"]["panels"]
        for box in (panel["outer"], panel["inner"])
    )
    assert payload["independent_replay"]["pass"]
    assert payload["scaling"]["pass"]
    assert payload["scaling"]["radius"]["pass"]
    assert payload["scaling"]["omega"]["pass"]


def test_l5_protocol_is_unchanged_since_its_public_freeze():
    result = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            l5.PROTOCOL_REVISION,
            "HEAD",
            "--",
            l5.PROTOCOL.as_posix(),
        ],
        cwd=l5.ROOT,
        check=False,
    )

    assert result.returncode == 0
    assert mpmath.__version__ == "1.3.0"
