from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (
    SimulationConfig,  # noqa: E402
    covariance_dimension,
    exponential_weights,
    occupancy_dimension,
    residence_statistics,
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


def test_reference_simulation_runs() -> None:
    cfg = SimulationConfig(steps=200, dim=3, alpha=0.05, sample_every=10, max_memory=50)
    result = simulate_finite_memory(cfg, seed=42)
    samples = result["samples"]
    assert samples.shape == (20, 3)
    assert np.isfinite(samples).all()


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


if __name__ == "__main__":
    test_covariance_dimension_synthetic_clouds()
    test_occupancy_dimension_line_is_finite()
    test_residence_statistics_counts_repeated_voxels()
    test_exponential_weights_are_finite_memory()
    test_reference_simulation_runs()
    test_finite_memory_step_accepts_seeded_rng()
    print("core tests ok")
