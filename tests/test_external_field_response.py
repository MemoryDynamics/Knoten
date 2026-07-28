from __future__ import annotations

import numpy as np

from emergenz_knoten import (
    FiniteMemoryState,
    SimulationConfig,
    external_field_response_metrics,
    paired_external_field_response,
)


def _state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.array([0.0, 0.0]),
        memory=np.array(
            [
                [0.0, 0.0],
                [-0.1, 0.0],
                [0.0, -0.1],
                [0.1, 0.0],
                [0.0, 0.1],
            ]
        ),
        weights=np.full(5, 0.2),
    )


def _config() -> SimulationConfig:
    return SimulationConfig(
        steps=10,
        dim=2,
        epsilon=0.0,
        eta=0.0,
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


def test_zero_external_field_keeps_all_three_branches_bitwise_identical() -> None:
    forcing = np.zeros((10, 2))
    response = paired_external_field_response(
        _state(),
        _config(),
        applied_displacements=forcing,
        noise=np.zeros_like(forcing),
        sample_steps=[0, 5, 10],
    )

    np.testing.assert_array_equal(
        response.target_memory_centers[:, 0],
        response.target_memory_centers[:, 2],
    )
    np.testing.assert_array_equal(
        response.target_memory_centers[:, 1],
        response.target_memory_centers[:, 2],
    )


def test_external_field_sign_flip_reverses_the_paired_response() -> None:
    forcing = np.zeros((10, 2))
    forcing[:4, 0] = 0.01
    response = paired_external_field_response(
        _state(),
        _config(),
        applied_displacements=forcing,
        noise=np.zeros_like(forcing),
        sample_steps=[0, 2, 4, 10],
    )
    metrics = external_field_response_metrics(response, radius=0.1)

    assert metrics["active_response_r"] > 0.0
    assert metrics["flip_cosine"] < -0.999999
    assert np.isclose(metrics["flip_magnitude_ratio"], 1.0)
    np.testing.assert_allclose(
        response.target_memory_centers[:, 0]
        - response.target_memory_centers[:, 2],
        -(
            response.target_memory_centers[:, 1]
            - response.target_memory_centers[:, 2]
        ),
        atol=1e-15,
    )
