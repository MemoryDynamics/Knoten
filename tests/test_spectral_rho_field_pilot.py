from __future__ import annotations

import argparse

import numpy as np

from experiments.current.memory import spectral_rho_field_pilot as pilot


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        steps=300,
        burn_in=30,
        sample_every=10,
        seeds=[1],
        epsilon=[1e-6, 1e-4],
        eta=0.15,
        lambda_value=0.01,
        memory_mass=1.0,
        box_length=80.0,
        n_modes=16,
        deposition_sigma=0.0,
        amplitude_att=26.0,
        sigma_att=3.0,
        sigma_comp=10.0,
        convergence_modes=[8, 16],
        grid_points=101,
        report=None,
        summary_json=None,
        metrics_figure=None,
        field_figure=None,
    )


def test_eta_zero_case_replays_periodic_random_walk_and_preserves_mass() -> None:
    args = _args()
    noise = np.random.default_rng(4).normal(size=args.steps)

    row, snapshot = pilot.run_case(
        args,
        epsilon=1e-4,
        eta=0.0,
        seed=4,
        n_modes=args.n_modes,
        noise=noise,
    )

    assert snapshot is None
    assert row["condition"] == "eta_zero"
    assert row["sample_count"] == 27
    assert row["eta_zero_random_walk_error"] < 1e-12
    assert row["memory_mass_absolute_error"] < 1e-14


def test_pilot_kernel_has_exact_zero_integral_coefficient() -> None:
    args = _args()
    config = pilot._config(args, n_modes=args.n_modes)

    assert pilot.kernel_integral_coefficient(config) == 0.0
