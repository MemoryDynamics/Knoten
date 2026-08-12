from __future__ import annotations

from emergenz_knoten import build_isotropic_mediator_modes
from experiments.current.memory.synchronization.reciprocity.dynamic_two_knot_mediator_gate import (
    _compact_summary,
    _simulate,
)


def test_dynamic_two_knot_experiment_glue_closes_and_compacts() -> None:
    modes = build_isotropic_mediator_modes(
        n_wavenumber=8,
        n_direction=8,
        k_max=8.0,
    )
    pilot = _simulate(
        dynamic_order="second",
        modes=modes,
        initial_separation=5.0,
        duration=2.0,
        time_step=0.1,
        relative_mobility=1.0,
        trace_every=1,
    )
    assert pilot["maximum_balance_residual"] < 2.0e-12
    assert pilot["maximum_source_work_residual"] < 2.0e-12
    assert pilot["maximum_energy_increase"] < 2.0e-12
    compact = _compact_summary(
        {
            "pilots": [pilot],
            "equilibrium_initialized_controls": [pilot],
        }
    )
    assert "times" not in compact["pilots"][0]
    assert "final_separation" in compact["pilots"][0]
