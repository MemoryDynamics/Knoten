from __future__ import annotations

import argparse
import math

import numpy as np

from experiments.current.memory import relaxation_diffusion_field_pilot as pilot


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        steps=300,
        burn_in=30,
        sample_every=10,
        seeds=[1],
        diffusion_length_ratios=[0.0, 0.3, 1.0],
        epsilon=1e-4,
        eta=0.15,
        lambda_value=0.01,
        memory_mass=1.0,
        box_length=80.0,
        n_modes=16,
        deposition_sigma=0.0,
        amplitude_att=26.0,
        sigma_att=3.0,
        sigma_comp=10.0,
        grid_points=101,
        report=None,
        summary_json=None,
        figure=None,
    )


def test_diffusion_ratio_maps_to_requested_memory_time_length() -> None:
    args = _args()
    nu = pilot.diffusion_per_update(args, 1.0)

    assert math.isclose(nu, 0.045, rel_tol=0.0, abs_tol=1e-15)


def test_eta_zero_path_is_independent_of_field_diffusion() -> None:
    args = _args()
    noise = np.random.default_rng(8).normal(size=args.steps)
    displacements = []
    for ratio in args.diffusion_length_ratios:
        row, _ = pilot.run_case(
            args,
            diffusion_length_ratio=ratio,
            eta=0.0,
            seed=8,
            noise=noise,
        )
        displacements.append(row["final_unwrapped_displacement"])
        assert row["eta_zero_random_walk_error"] < 1e-12
        assert row["memory_mass_absolute_error"] < 1e-14

    np.testing.assert_array_equal(displacements, [displacements[0]] * 3)
