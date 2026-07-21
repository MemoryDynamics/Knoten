from __future__ import annotations

import numpy as np

from emergenz_knoten import (
    FiniteMemoryState,
    ScalarReadoutKernel,
    SimulationConfig,
    one_way_coupled_response,
    relative_orbital_observables,
    translate_finite_memory_state,
)


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


def test_zero_cross_keeps_all_self_feedback_target_paths_identical() -> None:
    noise = np.arange(20, dtype=float).reshape(10, 2) / 100.0
    response = one_way_coupled_response(
        _state(),
        _state(),
        _config(),
        source_center_offset=[1.0, 0.0],
        target_noise=noise,
        source_noise=noise[::-1].copy(),
        sample_steps=[0, 1, 5, 10],
        cross_eta=0.0,
    )

    dynamic, frozen, free, _eta_zero = range(4)
    np.testing.assert_array_equal(
        response.target_positions[:, dynamic],
        response.target_positions[:, free],
    )
    assert response.source_shape_tensors.shape == (4, 2, 2)
    assert response.target_shape_tensors.shape == (4, 4, 2, 2)
    assert np.all(np.linalg.eigvalsh(response.source_shape_tensors) >= -1e-14)
    np.testing.assert_array_equal(
        response.target_positions[:, frozen],
        response.target_positions[:, free],
    )
    np.testing.assert_array_equal(
        response.target_memory_centers[:, dynamic],
        response.target_memory_centers[:, free],
    )
    assert not np.array_equal(
        response.source_positions[-1],
        response.source_positions[0],
    )


def test_source_drive_moves_only_source_when_cross_coupling_is_zero() -> None:
    steps = 10
    noise = np.zeros((steps, 2))
    drive = np.zeros((steps, 2))
    drive[:, 1] = 0.02
    baseline = one_way_coupled_response(
        _state(),
        _state(),
        _config(epsilon=0.0, eta=0.0),
        source_center_offset=[1.0, 0.0],
        target_noise=noise,
        source_noise=noise,
        sample_steps=[0, steps],
        cross_eta=0.0,
    )
    driven = one_way_coupled_response(
        _state(),
        _state(),
        _config(epsilon=0.0, eta=0.0),
        source_center_offset=[1.0, 0.0],
        target_noise=noise,
        source_noise=noise,
        source_drive=drive,
        sample_steps=[0, steps],
        cross_eta=0.0,
    )

    np.testing.assert_array_equal(driven.target_positions, baseline.target_positions)
    assert driven.source_positions[-1, 1] > baseline.source_positions[-1, 1]


def test_moving_source_separates_dynamic_from_frozen_target() -> None:
    target_noise = np.zeros((20, 2))
    source_noise = np.zeros((20, 2))
    source_noise[:, 1] = 0.5
    response = one_way_coupled_response(
        _state(),
        _state(),
        _config(epsilon=0.02),
        source_center_offset=[1.0, 0.0],
        target_noise=target_noise,
        source_noise=source_noise,
        sample_steps=[0, 5, 10, 20],
        cross_eta=2e-3,
    )

    dynamic, frozen, free, _eta_zero = range(4)
    assert (
        np.linalg.norm(
            response.target_positions[-1, dynamic]
            - response.target_positions[-1, frozen]
        )
        > 0.0
    )
    assert (
        np.linalg.norm(
            response.target_positions[-1, dynamic] - response.target_positions[-1, free]
        )
        > 0.0
    )


def test_explicit_matching_cross_readout_is_backward_compatible() -> None:
    noise = np.arange(20, dtype=float).reshape(10, 2) / 100.0
    kwargs = {
        "source_center_offset": [1.0, 0.0],
        "target_noise": noise,
        "source_noise": noise[::-1].copy(),
        "sample_steps": [0, 1, 5, 10],
        "cross_eta": 1e-3,
    }
    baseline = one_way_coupled_response(_state(), _state(), _config(), **kwargs)
    readout = ScalarReadoutKernel(1.0, 3.0, 1.0, 20.0)
    explicit = one_way_coupled_response(
        _state(),
        _state(),
        _config(),
        cross_readout=readout,
        **kwargs,
    )

    np.testing.assert_array_equal(explicit.target_positions, baseline.target_positions)
    np.testing.assert_array_equal(explicit.source_positions, baseline.source_positions)
    assert explicit.cross_readout == readout


def test_cross_readout_changes_target_without_changing_autonomous_source() -> None:
    noise = np.arange(20, dtype=float).reshape(10, 2) / 100.0
    kwargs = {
        "source_center_offset": [1.0, 0.0],
        "target_noise": noise,
        "source_noise": noise[::-1].copy(),
        "sample_steps": [0, 1, 5, 10],
        "cross_eta": 1e-3,
    }
    broad = one_way_coupled_response(_state(), _state(), _config(), **kwargs)
    narrow = one_way_coupled_response(
        _state(),
        _state(),
        _config(),
        cross_readout=ScalarReadoutKernel(0.3, 0.9, 1.0, 20.0),
        **kwargs,
    )

    np.testing.assert_array_equal(narrow.source_positions, broad.source_positions)
    assert not np.array_equal(narrow.target_positions, broad.target_positions)


def test_one_way_response_is_translation_equivariant() -> None:
    target = _state()
    source = _state()
    shift = np.array([5.0, -3.0])
    kwargs = {
        "source_center_offset": [1.0, 0.0],
        "target_noise": np.zeros((5, 2)),
        "source_noise": np.ones((5, 2)) * 0.1,
        "sample_steps": [0, 1, 5],
        "cross_eta": 1e-3,
    }
    original = one_way_coupled_response(target, source, _config(), **kwargs)
    translated = one_way_coupled_response(
        translate_finite_memory_state(target, shift),
        translate_finite_memory_state(source, shift),
        _config(),
        **kwargs,
    )

    np.testing.assert_allclose(
        translated.target_positions,
        original.target_positions + shift,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        translated.source_positions,
        original.source_positions + shift,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        translated.source_shape_tensors,
        original.source_shape_tensors,
        atol=1e-12,
    )


def test_relative_orbital_observables_recover_circular_motion() -> None:
    angles = np.linspace(0.0, 0.4, 5)
    target = np.column_stack((np.cos(angles), np.sin(angles)))
    source = np.zeros_like(target)
    orbital = relative_orbital_observables(target, source, np.arange(5))

    assert np.max(np.abs(orbital.radial_velocities)) < 1e-12
    assert np.all(orbital.tangential_speeds > 0.0)
    assert np.all(orbital.angular_momentum_norms > 0.0)
    np.testing.assert_allclose(
        orbital.angular_momentum_tensors[:, 0, 1],
        orbital.angular_momentum_norms,
        rtol=1e-12,
        atol=1e-12,
    )
