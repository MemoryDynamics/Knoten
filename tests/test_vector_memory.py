from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    SimulationConfig,
    VectorMemoryConfig,
    normalize_orientation,
    simulate_finite_memory,
    simulate_vector_memory,
    vector_gaussian_field,
    vector_memory_force,
)


def _scalar_config() -> SimulationConfig:
    return SimulationConfig(
        steps=120,
        dim=3,
        epsilon=0.03,
        eta=0.15,
        alpha=0.1,
        memory_mass=1.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=8.0,
        max_memory=30,
        sample_every=10,
    )


def test_eta_vector_zero_matches_scalar_simulation_for_same_seed() -> None:
    scalar = _scalar_config()
    vector = VectorMemoryConfig(
        scalar=scalar,
        lambda_vector=0.2,
        vector_mass=3.0,
        eta_vector=0.0,
        sigma_vector=2.0,
    )

    scalar_result = simulate_finite_memory(scalar, seed=123)
    vector_result = simulate_vector_memory(vector, seed=123)

    assert np.allclose(vector_result["samples"], scalar_result["samples"])
    assert np.allclose(vector_result["sample_steps"], scalar_result["sample_steps"])
    assert np.allclose(vector_result["final_x"], scalar_result["final_x"])
    assert np.allclose(vector_result["memory"], scalar_result["memory"])
    assert np.allclose(vector_result["weights"], scalar_result["weights"])


def test_zero_vector_mass_matches_scalar_simulation_even_with_eta_vector() -> None:
    scalar = _scalar_config()
    vector = VectorMemoryConfig(
        scalar=scalar,
        lambda_vector=0.2,
        vector_mass=0.0,
        eta_vector=5.0,
        sigma_vector=2.0,
    )

    scalar_result = simulate_finite_memory(scalar, seed=456)
    vector_result = simulate_vector_memory(vector, seed=456)

    assert np.allclose(vector_result["samples"], scalar_result["samples"])
    assert np.allclose(vector_result["vector_weights"], 0.0)


def test_vector_orientations_are_unit_or_zero() -> None:
    scalar = SimulationConfig(
        steps=30,
        dim=3,
        epsilon=0.03,
        eta=0.0,
        alpha=0.2,
        max_memory=10,
        sample_every=5,
    )
    result = simulate_vector_memory(VectorMemoryConfig(scalar=scalar), seed=11)

    norms = np.linalg.norm(result["vector_orientations"], axis=1)
    assert norms.shape[0] == result["vector_positions"].shape[0]
    assert np.all((np.isclose(norms, 1.0)) | (np.isclose(norms, 0.0)))
    assert np.any(np.isclose(norms, 1.0))


def test_normalize_orientation_handles_zero_displacement() -> None:
    assert np.allclose(normalize_orientation(np.zeros(3)), np.zeros(3))
    assert np.allclose(normalize_orientation(np.array([3.0, 4.0])), [0.6, 0.8])


def test_vector_gaussian_field_and_transverse_force() -> None:
    x = np.array([0.0, 0.0])
    positions = np.array([[0.0, 0.0]])
    orientations = np.array([[1.0, 0.0]])
    weights = np.array([2.0])

    assert np.allclose(
        vector_gaussian_field(x, positions, orientations, weights, sigma=1.0),
        [2.0, 0.0],
    )
    assert np.allclose(
        vector_memory_force(
            x,
            positions,
            orientations,
            weights,
            sigma=1.0,
            mode="transverse_2d",
        ),
        [0.0, 2.0],
    )


def test_transverse_mode_requires_two_dimensions() -> None:
    scalar = SimulationConfig(steps=10, dim=3, alpha=0.1, sample_every=5)
    vector = VectorMemoryConfig(scalar=scalar, force_mode="transverse_2d")

    try:
        simulate_vector_memory(vector, seed=1)
    except ValueError as exc:
        assert "dim=2" in str(exc)
    else:
        raise AssertionError("expected transverse_2d to reject dim=3")
