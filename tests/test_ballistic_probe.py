from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

from emergenz_knoten import SimulationConfig
from emergenz_knoten.markov.validation import (
    ballistic_scaling_slope,
    critical_eta,
    critical_gamma,
    mean_squared_displacement,
    self_consistency_residual,
)


def test_mean_squared_displacement_is_quadratic_for_linear_motion() -> None:
    positions = np.arange(100, dtype=float)[:, None]

    msd = mean_squared_displacement(positions, max_lag=50)
    expected = np.arange(1, 51, dtype=float) ** 2

    assert np.isclose(msd[0], 0.0)
    assert np.allclose(msd[1:], expected)

    slope = ballistic_scaling_slope(positions, fit_window=(5, 50))
    assert 1.95 <= slope <= 2.05


def test_critical_gamma_eta_and_residual_match_expected_values() -> None:
    gamma_c = critical_gamma(0.1)
    eta_c = critical_eta(0.1)

    assert np.isclose(gamma_c, 0.011111111111111112)
    assert np.isclose(eta_c, 0.11111111111111112)
    assert np.isclose(0.1 * eta_c, gamma_c)

    residual = self_consistency_residual(0.0, gamma=gamma_c, lambda_value=0.1)
    assert abs(residual) < 1e-6


def _load_ballistic_probe_module():
    path = Path("experiments/propagation_speed/ballistic_kernel_probe.py")
    spec = importlib.util.spec_from_file_location("ballistic_kernel_probe", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_ballistic_probe_sweep_uses_eta_threshold() -> None:
    module = _load_ballistic_probe_module()
    cases = module._sweep_cases()

    assert cases
    assert np.isclose(cases[0]["eta_c"], critical_eta(0.1))
    assert np.isclose(cases[0]["gamma_c"], critical_gamma(0.1))
    assert np.isclose(cases[0]["gamma"], cases[0]["eta"] * 0.1)


def test_ballistic_probe_smoke_uses_lambda_and_repulsive_sign() -> None:
    module = _load_ballistic_probe_module()
    config = SimulationConfig(
        steps=200,
        dim=1,
        epsilon=0.0,
        eta=1.1 * critical_eta(0.1),
        alpha=0.1,
        sample_every=1,
        burn_in=20,
        max_memory=100,
    )

    samples = module._simulate_repulsive_probe(
        config,
        seed=1,
        lambda_value=0.1,
        eta=config.eta,
        epsilon=0.0,
    )

    assert samples.shape[0] > 0
    assert np.isfinite(samples).all()
    assert float(np.max(np.abs(samples))) > 0.0
