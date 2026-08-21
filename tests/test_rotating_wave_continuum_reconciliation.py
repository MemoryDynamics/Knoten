import json

import pytest

from emergenz_knoten.rotating_wave import (
    ContinuumRotatingWaveBalance,
    RotatingWaveComponents,
)
from experiments.current.dynamics.rotation import (
    scalar_memory_rotating_wave_continuum_reconciliation as reconciliation,
)


def test_registered_continuum_problem_matches_frozen_ladder_scaling():
    assert reconciliation.TAIL_EXTENT == 12.0
    assert reconciliation.ETA_PER_ALPHA == 15.0
    assert reconciliation.AMPLITUDE_ATT == 3.5
    assert reconciliation.NEWTON_ITERATIONS == 8
    assert reconciliation.PANELS == (
        {
            "name": "numpy-256",
            "quadrature_backend": "numpy",
            "quadrature_order": 256,
        },
        {
            "name": "numpy-512",
            "quadrature_backend": "numpy",
            "quadrature_order": 512,
        },
        {
            "name": "scipy-1024",
            "quadrature_backend": "scipy",
            "quadrature_order": 1024,
        },
    )


def test_fixed_newton_uses_declared_count_without_early_stop():
    def linear_balance(radius, omega):
        return ContinuumRotatingWaveBalance(
            components=RotatingWaveComponents(radial=0.0, tangential=-1.0),
            residual=(2.0 * radius + omega - 5.0, radius - omega - 1.0),
            jacobian=((2.0, 1.0), (1.0, -1.0)),
            required_eta_per_alpha=15.0,
        )

    result = reconciliation.fixed_newton(
        linear_balance,
        radius_start=0.5,
        omega_start=0.5,
        iterations=3,
    )

    assert result["radius"] == pytest.approx(2.0)
    assert result["omega"] == pytest.approx(1.0)
    assert len(result["iterations"]) == 4
    assert [row["iteration"] for row in result["iterations"]] == [0, 1, 2, 3]


def test_source_audit_reproduces_preexisting_gain_mismatch():
    discovery = json.loads(
        (reconciliation.ROOT / reconciliation.DISCOVERY_RESULT).read_text(
            encoding="utf-8"
        )
    )

    audit = reconciliation._source_audit(discovery)

    assert audit["pass"]
    assert audit["observed"]["required_eta_per_alpha"] != 15.0


def test_scaling_diagnostics_accept_exact_first_order_family():
    target_radius = 0.9
    target_omega = 1.6
    rows = [
        {
            "alpha": alpha,
            "radius": target_radius + 0.4 * alpha,
            "omega": target_omega - 0.7 * alpha,
        }
        for _, alpha, _, _ in reconciliation.EXPECTED_LADDER_CELLS
    ]

    diagnostics = reconciliation.scaling_diagnostics(
        rows,
        target_radius=target_radius,
        target_omega=target_omega,
    )

    assert diagnostics["pass"]
    assert diagnostics["radius_slope"] == pytest.approx(1.0, abs=1.0e-12)
    assert diagnostics["omega_slope"] == pytest.approx(1.0, abs=1.0e-12)


def test_scaling_diagnostics_reject_target_offset_from_family_limit():
    family_radius = 0.9
    family_omega = 1.6
    rows = [
        {
            "alpha": alpha,
            "radius": family_radius + 0.4 * alpha,
            "omega": family_omega - 0.7 * alpha,
        }
        for _, alpha, _, _ in reconciliation.EXPECTED_LADDER_CELLS
    ]

    diagnostics = reconciliation.scaling_diagnostics(
        rows,
        target_radius=family_radius - 0.01,
        target_omega=family_omega + 0.02,
    )

    assert not diagnostics["pass"]
    assert not diagnostics["gates"]["radius_richardson"]
    assert not diagnostics["gates"]["omega_richardson"]


def test_frozen_ladder_source_preserves_integrity_controls():
    ladder = json.loads(
        (reconciliation.ROOT / reconciliation.LADDER_RESULT).read_text(
            encoding="utf-8"
        )
    )

    rows, integrity = reconciliation._ladder_rows_and_integrity(ladder)

    assert integrity["pass"]
    assert len(rows) == 5
    assert [row["alpha"] for row in rows] == [0.04, 0.02, 0.01, 0.005, 0.0025]
