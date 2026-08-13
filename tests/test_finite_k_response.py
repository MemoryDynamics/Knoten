from __future__ import annotations

import numpy as np

from emergenz_knoten import (
    double_gaussian_gradient,
    FiniteMemoryState,
    SimulationConfig,
    longitudinal_memory_mode_profiles,
    paired_finite_k_memory_response,
    scalar_memory_fourier_modes,
    translate_finite_memory_state,
)


def _state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.array([0.0, 0.0]),
        memory=np.array(
            [[0.0, 0.0], [-0.2, 0.05], [0.1, -0.15], [0.25, 0.2]]
        ),
        weights=np.array([0.4, 0.3, 0.2, 0.1]),
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


def test_longitudinal_profiles_preserve_youngest_point_and_centroid() -> None:
    state = _state()
    profiles, wavevectors, radius = longitudinal_memory_mode_profiles(
        state,
        direction=[1.0, 0.0],
        kr_values=[0.5, 1.0, 2.0],
    )

    assert profiles.shape == (3, 4)
    assert wavevectors.shape == (3, 2)
    assert radius > 0.0
    np.testing.assert_allclose(profiles[:, 0], 0.0, atol=1e-15)
    np.testing.assert_allclose(profiles @ state.weights, 0.0, atol=1e-15)
    np.testing.assert_allclose(
        np.sum(state.weights[None, :] * profiles * profiles, axis=1),
        np.sum(state.weights),
    )


def test_centered_scalar_fourier_modes_are_translation_invariant() -> None:
    state = _state()
    shifted = translate_finite_memory_state(state, [11.0, -8.0])
    wavevectors = np.array([[1.0, 0.0], [0.3, -0.7]])

    np.testing.assert_allclose(
        scalar_memory_fourier_modes(state, wavevectors),
        scalar_memory_fourier_modes(shifted, wavevectors),
        atol=1e-14,
    )


def test_eta_zero_forgets_finite_k_deformation_after_retained_horizon() -> None:
    state = _state()
    response = paired_finite_k_memory_response(
        state,
        _config(eta=0.0),
        direction=[1.0, 0.0],
        kr_values=[0.5, 1.0, 2.0],
        perturbation_fraction=0.01,
        noise=np.zeros((5, 2)),
        sample_steps=np.arange(6),
    )

    assert response.centered_mode_matrices.shape == (6, 3, 3)
    assert response.position_matrices.shape == (6, 2, 3)
    np.testing.assert_allclose(response.position_matrices, 0.0, atol=1e-14)
    np.testing.assert_allclose(response.memory_center_matrices[-1], 0.0, atol=1e-14)
    np.testing.assert_allclose(response.centered_mode_matrices[-1], 0.0, atol=1e-12)


def test_finite_k_response_is_translation_equivariant() -> None:
    state = _state()
    shifted = translate_finite_memory_state(state, [4.0, -3.0])
    kwargs = {
        "direction": [0.0, 1.0],
        "kr_values": [0.5, 1.0],
        "perturbation_fraction": 0.005,
        "noise": np.zeros((3, 2)),
        "sample_steps": np.arange(4),
    }

    original = paired_finite_k_memory_response(state, _config(eta=0.15), **kwargs)
    translated = paired_finite_k_memory_response(
        shifted,
        _config(eta=0.15),
        **kwargs,
    )

    np.testing.assert_allclose(
        translated.position_matrices,
        original.position_matrices,
        atol=1e-10,
    )
    np.testing.assert_allclose(
        translated.memory_center_matrices,
        original.memory_center_matrices,
        atol=1e-10,
    )
    np.testing.assert_allclose(
        translated.centered_mode_matrices,
        original.centered_mode_matrices,
        atol=1e-10,
    )


def test_one_step_response_matches_public_kernel_central_difference() -> None:
    state = _state()
    config = _config(eta=0.15)
    direction = np.array([0.0, 1.0])
    kr_values = [0.5, 2.0]
    fraction = 0.005
    profiles, _, radius = longitudinal_memory_mode_profiles(
        state,
        direction=direction,
        kr_values=kr_values,
    )
    amplitude = fraction * radius
    expected = []
    for profile in profiles:
        displacement = amplitude * profile[:, None] * direction[None, :]
        branch_positions = []
        for sign in (1.0, -1.0):
            gradient = double_gaussian_gradient(
                state.x,
                state.memory + sign * displacement,
                state.weights,
                sigma_rep=config.sigma_rep,
                sigma_att=config.sigma_att,
                amplitude_rep=config.amplitude_rep,
                amplitude_att=config.amplitude_att,
                deposition_kernel=config.deposition_kernel,
                deposition_sigma=config.deposition_sigma,
            )
            branch_positions.append(state.x - config.eta * gradient)
        expected.append((branch_positions[0] - branch_positions[1]) / (2.0 * amplitude))

    response = paired_finite_k_memory_response(
        state,
        config,
        direction=direction,
        kr_values=kr_values,
        perturbation_fraction=fraction,
        noise=np.zeros((1, state.dim)),
        sample_steps=[0, 1],
    )

    np.testing.assert_allclose(
        response.position_matrices[1],
        np.column_stack(expected),
        atol=1e-12,
    )
