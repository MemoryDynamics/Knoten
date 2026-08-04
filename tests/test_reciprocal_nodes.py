from __future__ import annotations

import numpy as np

from emergenz_knoten import FiniteMemoryState, SimulationConfig
from emergenz_knoten.reciprocal_nodes import reciprocal_pair_response


def _state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.array([0.0, 0.0]),
        memory=np.array(
            [
                [0.0, 0.0],
                [-0.1, 0.0],
                [0.1, 0.0],
                [0.0, -0.1],
                [0.0, 0.1],
            ]
        ),
        weights=np.array([0.4, 0.15, 0.15, 0.15, 0.15]),
    )


def _config(*, epsilon: float = 0.01, eta: float = 0.15) -> SimulationConfig:
    return SimulationConfig(
        steps=20,
        dim=2,
        epsilon=epsilon,
        eta=eta,
        alpha=0.2,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=20.0,
        memory_factor=1.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )


def _run(*, cross_eta: float, epsilon: float = 0.01, eta: float = 0.15):
    first_noise = np.arange(20, dtype=float).reshape(10, 2) / 100.0
    second_noise = first_noise[::-1].copy()
    return reciprocal_pair_response(
        _state(),
        _state(),
        _config(epsilon=epsilon, eta=eta),
        initial_center_separation=[1.0, 0.0],
        first_noise=first_noise,
        second_noise=second_noise,
        sample_steps=[0, 1, 5, 10],
        cross_eta=cross_eta,
    )


def test_zero_cross_makes_all_conditions_bitwise_identical() -> None:
    response = _run(cross_eta=0.0)

    for condition in (1, 2):
        np.testing.assert_array_equal(
            response.positions[:, condition],
            response.positions[:, 0],
        )
        np.testing.assert_array_equal(
            response.memory_centers[:, condition],
            response.memory_centers[:, 0],
        )
    assert response.positions.shape == (4, 3, 2, 2)
    assert response.shape_tensors.shape == (4, 3, 2, 2, 2)
    np.testing.assert_allclose(response.radius_ratios[0], 1.0)


def test_one_way_leaves_first_node_on_channel_off_path() -> None:
    response = _run(cross_eta=1e-3)

    np.testing.assert_array_equal(
        response.positions[:, 1, 0],
        response.positions[:, 0, 0],
    )
    assert not np.array_equal(
        response.positions[-1, 1, 1],
        response.positions[-1, 0, 1],
    )


def test_reciprocal_channel_updates_both_nodes_from_pre_update_state() -> None:
    response = _run(cross_eta=1e-3, epsilon=0.0, eta=0.0)
    off = response.positions[1, 0]
    reciprocal = response.positions[1, 2]

    assert reciprocal[0, 0] > off[0, 0]
    assert reciprocal[1, 0] < off[1, 0]
    np.testing.assert_allclose(
        reciprocal[:, 0] - off[:, 0],
        np.array([1.0, -1.0]) * abs(reciprocal[0, 0] - off[0, 0]),
        rtol=1e-12,
        atol=1e-12,
    )


def test_reciprocal_pair_is_translation_equivariant() -> None:
    base = _state()
    shifted = FiniteMemoryState(
        x=base.x + np.array([4.0, -2.0]),
        memory=base.memory + np.array([4.0, -2.0]),
        weights=base.weights,
    )
    noise = np.zeros((3, 2))
    kwargs = {
        "initial_center_separation": [1.0, 0.0],
        "first_noise": noise,
        "second_noise": noise,
        "sample_steps": [0, 1, 3],
        "cross_eta": 1e-3,
    }
    original = reciprocal_pair_response(base, base, _config(), **kwargs)
    translated = reciprocal_pair_response(shifted, shifted, _config(), **kwargs)

    np.testing.assert_allclose(
        translated.positions,
        original.positions + np.array([4.0, -2.0]),
        atol=1e-12,
    )
    np.testing.assert_allclose(
        translated.shape_tensors,
        original.shape_tensors,
        atol=1e-12,
    )
