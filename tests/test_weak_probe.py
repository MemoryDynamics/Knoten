import numpy as np

from emergenz_knoten import (
    FiniteMemoryState,
    SimulationConfig,
    paired_uniform_probe_response,
    translate_finite_memory_state,
)


def _state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.array([0.0, 0.0]),
        memory=np.array([[0.0, 0.0], [-0.1, 0.0], [0.0, -0.1]]),
        weights=np.array([0.5, 0.3, 0.2]),
    )


def _config(*, eta: float) -> SimulationConfig:
    return SimulationConfig(
        steps=10,
        dim=2,
        epsilon=0.0,
        eta=eta,
        alpha=0.2,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=2.0,
        memory_factor=1.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )


def test_eta_zero_uniform_probe_has_known_direct_position_rank() -> None:
    response = paired_uniform_probe_response(
        _state(),
        _config(eta=0.0),
        directions=np.eye(2),
        noise=np.zeros((4, 2)),
        sample_steps=[0, 2, 4],
        per_step_strength=0.01,
        pulse_steps=2,
    )

    np.testing.assert_allclose(response.position_matrices[0], np.zeros((2, 2)))
    np.testing.assert_allclose(response.position_matrices[1], 2.0 * np.eye(2))
    np.testing.assert_allclose(response.position_matrices[2], 2.0 * np.eye(2))
    assert response.memory_center_matrices.shape == (3, 2, 2)
    assert response.shape_matrices.shape == (3, 3, 2)
    assert response.radius_ratios.shape == (3, 2, 2)
    np.testing.assert_allclose(response.control_positions, np.zeros((3, 2)))
    assert response.control_memory_centers.shape == (3, 2)
    assert response.control_shape_vectors.shape == (3, 3)
    assert response.control_radius_ratios.shape == (3,)


def test_probe_response_is_translation_equivariant() -> None:
    state = _state()
    shifted = translate_finite_memory_state(state, [12.0, -7.0])
    rng = np.random.default_rng(11)
    noise = rng.normal(size=(5, 2))
    kwargs = {
        "directions": np.eye(2),
        "noise": noise,
        "sample_steps": [1, 3, 5],
        "per_step_strength": 0.001,
        "pulse_steps": 1,
    }

    original = paired_uniform_probe_response(state, _config(eta=0.15), **kwargs)
    translated = paired_uniform_probe_response(shifted, _config(eta=0.15), **kwargs)

    np.testing.assert_allclose(translated.position_matrices, original.position_matrices, atol=1e-10)
    np.testing.assert_allclose(
        translated.memory_center_matrices,
        original.memory_center_matrices,
        atol=1e-10,
    )
    np.testing.assert_allclose(translated.shape_matrices, original.shape_matrices, atol=1e-10)
    np.testing.assert_allclose(translated.radius_ratios, original.radius_ratios, atol=1e-10)
