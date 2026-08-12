from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten import (
    FiniteMemoryState,
    centered_finite_difference_pair_force,
    rigid_full_memory_pair_interaction,
    reciprocal_visible_memory_pair_interaction,
    three_scale_radial_derivative,
    three_scale_radial_potential,
)


def _point(position: list[float], mass: float = 1.0) -> FiniteMemoryState:
    point = np.asarray(position, dtype=float)
    return FiniteMemoryState(
        x=point,
        memory=point[None, :],
        weights=np.array([mass]),
    )


def _law():
    parameters = {
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "sigma_comp": 10.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 35.0,
        "amplitude_comp": 0.944,
    }
    return (
        lambda radius: three_scale_radial_potential(radius, **parameters),
        lambda radius: three_scale_radial_derivative(radius, **parameters),
    )


def test_point_pair_matches_radial_law_and_action_reaction() -> None:
    potential, derivative = _law()
    result = rigid_full_memory_pair_interaction(
        _point([0.0, 0.0], mass=2.0),
        _point([0.0, 0.0], mass=3.0),
        [4.0, 0.0],
        radial_pair_energy=potential,
        radial_pair_energy_derivative=derivative,
    )
    assert result.energy == pytest.approx(6.0 * float(potential(np.asarray(4.0))))
    assert result.radial_force_on_second == pytest.approx(
        -6.0 * float(derivative(np.asarray(4.0)))
    )
    np.testing.assert_allclose(result.force_on_first, -result.force_on_second)


def test_pair_force_is_negative_energy_derivative() -> None:
    potential, derivative = _law()
    state = FiniteMemoryState(
        x=np.array([0.0, 0.0]),
        memory=np.array([[0.0, 0.0], [0.1, -0.05], [-0.04, 0.08]]),
        weights=np.array([0.5, 0.3, 0.2]),
    )
    result = rigid_full_memory_pair_interaction(
        state,
        state,
        [6.0, 0.0],
        radial_pair_energy=potential,
        radial_pair_energy_derivative=derivative,
    )
    finite_difference = centered_finite_difference_pair_force(
        state,
        state,
        [6.0, 0.0],
        radial_pair_energy=potential,
        radial_pair_energy_derivative=derivative,
        step=1.0e-5,
    )
    assert result.radial_force_on_second == pytest.approx(
        finite_difference, rel=2.0e-8, abs=2.0e-10
    )


def test_pair_interaction_is_orthogonally_covariant() -> None:
    potential, derivative = _law()
    state = FiniteMemoryState(
        x=np.array([0.0, 0.0]),
        memory=np.array([[0.0, 0.0], [0.1, -0.05], [-0.04, 0.08]]),
        weights=np.array([0.5, 0.3, 0.2]),
    )
    rotation = np.array([[0.0, -1.0], [1.0, 0.0]])
    original = rigid_full_memory_pair_interaction(
        state,
        state,
        [6.0, 0.0],
        radial_pair_energy=potential,
        radial_pair_energy_derivative=derivative,
    )
    rotated_state = FiniteMemoryState(
        x=rotation @ state.x,
        memory=state.memory @ rotation.T,
        weights=state.weights,
    )
    rotated = rigid_full_memory_pair_interaction(
        rotated_state,
        rotated_state,
        rotation @ np.array([6.0, 0.0]),
        radial_pair_energy=potential,
        radial_pair_energy_derivative=derivative,
    )
    assert rotated.energy == pytest.approx(original.energy)
    np.testing.assert_allclose(rotated.force_on_second, rotation @ original.force_on_second)


def test_reciprocal_visible_memory_energy_has_action_reaction_and_gradient_force() -> None:
    potential, derivative = _law()
    state = FiniteMemoryState(
        x=np.array([0.02, -0.01]),
        memory=np.array([[0.0, 0.0], [0.1, -0.05], [-0.04, 0.08]]),
        weights=np.array([0.5, 0.3, 0.2]),
    )
    result = reciprocal_visible_memory_pair_interaction(
        state,
        state,
        [6.0, 0.0],
        radial_pair_energy=potential,
        radial_pair_energy_derivative=derivative,
    )
    step = 1.0e-5
    energies = []
    for radius in (6.0 - step, 6.0 + step):
        energies.append(
            reciprocal_visible_memory_pair_interaction(
                state,
                state,
                [radius, 0.0],
                radial_pair_energy=potential,
                radial_pair_energy_derivative=derivative,
            ).energy
        )
    finite_difference = -(energies[1] - energies[0]) / (2.0 * step)
    assert result.radial_force_on_second == pytest.approx(
        finite_difference, rel=2.0e-8, abs=2.0e-10
    )
    np.testing.assert_allclose(result.force_on_first, -result.force_on_second)
