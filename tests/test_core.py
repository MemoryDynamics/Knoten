from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (
    SimulationConfig,  # noqa: E402
    covariance_dimension,
    exponential_memory_weights,
    exponential_weights,
    fit_occupancy_scaling_window,
    occupancy_dimension,
    occupancy_local_slopes,
    residence_statistics,
    shape_statistics,
    repulsive_gaussian_gradient,
    simulate_finite_memory,
    simulate_finite_memory_numba,
)
from emergenz_knoten.core import finite_memory_step  # noqa: E402


def test_covariance_dimension_synthetic_clouds() -> None:
    rng = np.random.default_rng(123)

    line = np.column_stack([np.linspace(-1, 1, 500), np.zeros(500), np.zeros(500)])
    assert 0.99 <= covariance_dimension(line) <= 1.01

    plane = np.column_stack([rng.normal(size=(1000, 2)), np.zeros(1000)])
    assert 1.8 <= covariance_dimension(plane) <= 2.2

    cloud = rng.normal(size=(2000, 3))
    assert 2.7 <= covariance_dimension(cloud) <= 3.1


def test_occupancy_dimension_line_is_finite() -> None:
    line = np.column_stack([np.linspace(0, 10, 1000), np.zeros(1000)])
    value = occupancy_dimension(line)
    assert np.isfinite(value)
    assert 0.7 <= value <= 1.3


def test_shape_statistics_detects_weighted_center_and_roundness() -> None:
    points = np.array(
        [
            [-1.0, 0.0],
            [1.0, 0.0],
            [0.0, -1.0],
            [0.0, 1.0],
        ]
    )
    stats = shape_statistics(points, weights=[1.0, 1.0, 1.0, 3.0])

    assert np.allclose(stats["center"], [0.0, 1.0 / 3.0])
    assert stats["effective_dimension"] is not None
    assert 1.5 <= float(stats["effective_dimension"]) <= 2.0
    assert stats["axis_ratio_min_max"] is not None
    assert 0.5 <= float(stats["axis_ratio_min_max"]) <= 1.0


def test_occupancy_scaling_window_skips_sample_saturation() -> None:
    scales = np.geomspace(0.001, 1.0, 10)
    counts = np.array([1000, 990, 920, 600, 129, 28, 6, 3, 2, 1], dtype=float)

    slopes = occupancy_local_slopes(scales, counts)
    assert slopes.shape == (9,)

    window = fit_occupancy_scaling_window(
        scales,
        counts,
        n_samples=1000,
        min_points=4,
        min_boxes=5,
        max_count_fraction=0.8,
    )

    assert window.start_index >= 3
    assert window.n_points >= 4
    assert window.valid_scaling
    assert 1.7 <= window.dimension <= 2.3
    assert window.r_squared >= 0.98


def test_residence_statistics_counts_repeated_voxels() -> None:
    points = np.array(
        [
            [0.1, 0.1],
            [0.2, 0.1],
            [0.3, 0.2],
            [3.0, 3.0],
            [3.1, 3.1],
            [3.2, 3.2],
        ]
    )
    stats = residence_statistics(points, voxel_size=1.0, min_visits=2)
    assert stats["knot_count"] == 2.0
    assert stats["max_residence"] >= 2.0


def test_exponential_weights_are_finite_memory() -> None:
    weights = exponential_weights(alpha=0.1, horizon=5)
    expected_sum = 1.0 - (1.0 - 0.1) ** 5
    assert np.all(weights > 0)
    assert abs(weights.sum() - expected_sum) < 1e-12


def test_exponential_memory_weights_allow_zero_memory_mass() -> None:
    weights = exponential_memory_weights(0.1, 5, memory_mass=0.0)
    assert np.all(weights == 0.0)


def test_exponential_memory_weights_scale_with_memory_mass() -> None:
    weights = exponential_memory_weights(0.1, 5, memory_mass=2.0)
    expected_sum = 2.0 * (1.0 - (1.0 - 0.1) ** 5)
    assert np.all(weights > 0)
    assert abs(weights.sum() - expected_sum) < 1e-12
    assert np.allclose(weights, 2.0 * exponential_weights(0.1, 5))


def test_repulsive_gaussian_gradient_points_away_from_memory() -> None:
    x = np.array([1.0, 0.0])
    memory = np.array([[0.0, 0.0]])
    weights = np.array([1.0])
    grad = repulsive_gaussian_gradient(x, memory, weights, sigma=1.0, amplitude=1.0)
    assert grad[0] > 0.0
    assert grad[1] == 0.0


def test_reference_simulation_runs() -> None:
    cfg = SimulationConfig(steps=200, dim=3, alpha=0.05, sample_every=10, max_memory=50)
    result = simulate_finite_memory(cfg, seed=42)
    samples = result["samples"]
    assert samples.shape == (20, 3)
    assert np.isfinite(samples).all()



def test_zero_memory_mass_matches_eta_zero_for_same_seed() -> None:
    base = SimulationConfig(
        steps=100,
        dim=2,
        alpha=0.1,
        memory_mass=0.0,
        eta=0.15,
        sample_every=10,
        max_memory=20,
    )
    eta_zero = SimulationConfig(
        steps=100,
        dim=2,
        alpha=0.1,
        memory_mass=1.0,
        eta=0.0,
        sample_every=10,
        max_memory=20,
    )

    zero_mass_result = simulate_finite_memory(base, seed=123)
    eta_zero_result = simulate_finite_memory(eta_zero, seed=123)

    assert np.allclose(zero_mass_result["samples"], eta_zero_result["samples"])
    assert np.all(zero_mass_result["weights"] == 0.0)


def test_alpha_one_matches_zero_memory_mass_for_same_seed() -> None:
    alpha_one = SimulationConfig(
        steps=100,
        dim=3,
        alpha=1.0,
        memory_mass=1.0,
        eta=0.15,
        sample_every=10,
        max_memory=20,
    )
    zero_mass = SimulationConfig(
        steps=100,
        dim=3,
        alpha=0.1,
        memory_mass=0.0,
        eta=0.15,
        sample_every=10,
        max_memory=20,
    )

    alpha_one_result = simulate_finite_memory(alpha_one, seed=456)
    zero_mass_result = simulate_finite_memory(zero_mass, seed=456)

    assert np.allclose(alpha_one_result["samples"], zero_mass_result["samples"])


def test_finite_memory_step_accepts_seeded_rng() -> None:

    cfg = SimulationConfig(dim=2, epsilon=0.1)
    x = np.zeros(2)
    history = np.zeros((0, 2))
    weights = np.zeros(0)
    rng1 = np.random.default_rng(7)
    rng2 = np.random.default_rng(7)

    assert np.allclose(
        finite_memory_step(x, history, weights, cfg, rng=rng1),
        finite_memory_step(x, history, weights, cfg, rng=rng2),
    )


def test_simulation_config_rejects_invalid_scales_and_horizon() -> None:
    invalid_cases = [
        ({"sigma_rep": 0.0}, "sigma_rep"),
        ({"sigma_att": 0.0}, "sigma_att"),
        ({"memory_factor": 0.0}, "memory_factor"),
        ({"memory_mass": -1.0}, "memory_mass"),
        ({"burn_in": -1}, "burn_in"),
    ]
    for kwargs, expected in invalid_cases:
        cfg = SimulationConfig(steps=10, **kwargs)
        try:
            simulate_finite_memory(cfg, seed=1)
        except ValueError as exc:
            assert expected in str(exc)
        else:
            raise AssertionError(f"expected ValueError for {expected}")


def test_numba_reference_simulation_runs() -> None:
    try:
        import numba  # noqa: F401
    except ImportError:
        return

    cfg = SimulationConfig(steps=100, dim=2, alpha=0.05, sample_every=10, max_memory=50)
    result = simulate_finite_memory_numba(cfg, seed=42)
    assert result["samples"].shape == (10, 2)
    assert np.isfinite(result["samples"]).all()
    assert result["memory"].shape[1] == 2
    assert result["weights"].shape[0] == result["memory"].shape[0]


def test_numba_wrapper_reuses_config_validation() -> None:
    try:
        import numba  # noqa: F401
    except ImportError:
        return

    cfg = SimulationConfig(steps=10, sigma_rep=0.0)
    try:
        simulate_finite_memory_numba(cfg, seed=42)
    except ValueError as exc:
        assert "sigma_rep" in str(exc)
    else:
        raise AssertionError("expected numba wrapper to validate sigma_rep")


if __name__ == "__main__":
    test_covariance_dimension_synthetic_clouds()
    test_occupancy_dimension_line_is_finite()
    test_shape_statistics_detects_weighted_center_and_roundness()
    test_residence_statistics_counts_repeated_voxels()
    test_exponential_weights_are_finite_memory()
    test_exponential_memory_weights_allow_zero_memory_mass()
    test_exponential_memory_weights_scale_with_memory_mass()
    test_zero_memory_mass_matches_eta_zero_for_same_seed()
    test_reference_simulation_runs()
    test_finite_memory_step_accepts_seeded_rng()
    test_simulation_config_rejects_invalid_scales_and_horizon()
    test_numba_reference_simulation_runs()
    test_numba_wrapper_reuses_config_validation()
    print("core tests ok")
