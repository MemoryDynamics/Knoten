from decimal import Decimal

from experiments.current.dynamics.rotation import (
    scalar_memory_rotating_wave_refinement_ladder as ladder,
)


def test_registered_cells_preserve_tail_extent_and_eta_per_alpha():
    for cell in ladder.CELLS:
        alpha = Decimal(cell["alpha"])
        eta = Decimal(cell["eta"])
        assert alpha * cell["horizon"] == Decimal("12")
        assert eta / alpha == Decimal("15")


def test_scaling_diagnostics_accept_exact_first_order_family():
    radius_limit = float(ladder.CONTINUUM_RADIUS_GUIDE)
    omega_limit = float(ladder.CONTINUUM_OMEGA_GUIDE)
    rows = [
        {
            "alpha": float(cell["alpha"]),
            "radius": radius_limit + 0.4 * float(cell["alpha"]),
            "omega": omega_limit - 0.7 * float(cell["alpha"]),
        }
        for cell in ladder.CELLS
    ]

    diagnostics = ladder.scaling_diagnostics(rows)

    assert diagnostics["pass"]
    assert abs(diagnostics["radius_slope"] - 1.0) < 1.0e-12
    assert abs(diagnostics["omega_slope"] - 1.0) < 1.0e-12
    assert diagnostics["radius_richardson_relative_error"] < 1.0e-11
    assert diagnostics["omega_richardson_relative_error"] < 1.0e-11


def test_scaling_diagnostics_reject_nonconvergent_family():
    radius_limit = float(ladder.CONTINUUM_RADIUS_GUIDE)
    omega_limit = float(ladder.CONTINUUM_OMEGA_GUIDE)
    rows = [
        {
            "alpha": float(cell["alpha"]),
            "radius": radius_limit + 0.01,
            "omega": omega_limit - 0.02,
        }
        for cell in ladder.CELLS
    ]

    diagnostics = ladder.scaling_diagnostics(rows)

    assert not diagnostics["pass"]
    assert not diagnostics["gates"]["radius_error_monotone"]
    assert not diagnostics["gates"]["omega_error_monotone"]


def test_corridor_rejects_intermediate_branch_excursion():
    alpha = "0.02"
    initial_theta = ladder._scaled(ladder.OMEGA_START, alpha)
    valid = [
        {"radius": ladder.RADIUS_START, "theta": initial_theta},
        {
            "radius": str(Decimal(ladder.RADIUS_START) + Decimal("0.01")),
            "theta": str(Decimal(initial_theta) + Decimal(alpha) * Decimal("0.01")),
        },
    ]
    excursion = valid + [
        {
            "radius": str(Decimal(ladder.RADIUS_START) + Decimal("0.2")),
            "theta": initial_theta,
        }
    ]

    assert ladder._corridor_pass(valid, alpha=alpha)
    assert not ladder._corridor_pass(excursion, alpha=alpha)
