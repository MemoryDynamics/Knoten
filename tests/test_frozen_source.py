import numpy as np
import pytest

from emergenz_knoten import (
    FiniteMemoryState,
    ScalarReadoutKernel,
    SimulationConfig,
    calibrate_frozen_source_cross_eta,
    paired_frozen_source_response,
    translate_finite_memory_state,
)


def _target_state() -> FiniteMemoryState:
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


def _source_state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.array([0.0, 0.0]),
        memory=np.array([[0.0, 0.0]]),
        weights=np.array([1.0]),
    )


def _config(*, eta: float, epsilon: float = 0.0) -> SimulationConfig:
    return SimulationConfig(
        steps=10,
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


def test_eta_zero_frozen_source_returns_local_translation_jacobian() -> None:
    response = paired_frozen_source_response(
        _target_state(),
        _source_state(),
        _config(eta=0.0),
        directions=np.eye(2),
        source_center_offset=[1.0, 0.0],
        perturbation=0.1,
        noise=np.zeros((1, 2)),
        sample_steps=[0, 1],
        cross_eta=1e-3,
        pulse_steps=1,
    )

    np.testing.assert_array_equal(response.position_jacobians[0], np.zeros((2, 2)))
    diagonal = np.diag(response.position_jacobians[1])
    assert np.all(np.abs(diagonal) > 0.0)
    np.testing.assert_allclose(
        response.position_jacobians[1] - np.diag(diagonal),
        0.0,
        atol=1e-15,
    )
    assert response.baseline_positions[1, 0] > response.free_positions[1, 0]
    assert response.baseline_source_center.tolist() == pytest.approx([1.0, 0.0])
    assert response.source_centers.shape == (2, 2, 2)


def test_zero_cross_coupling_reproduces_baseline_and_free_controls() -> None:
    response = paired_frozen_source_response(
        _target_state(),
        _source_state(),
        _config(eta=0.15, epsilon=0.01),
        directions=np.eye(2),
        source_center_offset=[1.0, 0.0],
        perturbation=0.1,
        noise=np.arange(6, dtype=float).reshape(3, 2) / 10.0,
        sample_steps=[1, 3],
        cross_eta=0.0,
        pulse_steps=1,
    )

    np.testing.assert_array_equal(response.position_jacobians, 0.0)
    np.testing.assert_array_equal(response.memory_center_jacobians, 0.0)
    np.testing.assert_array_equal(response.shape_jacobians, 0.0)
    np.testing.assert_array_equal(response.position_even_offsets, 0.0)
    np.testing.assert_array_equal(response.memory_center_even_offsets, 0.0)
    np.testing.assert_array_equal(response.shape_even_vectors, 0.0)
    np.testing.assert_array_equal(response.radius_even_offsets, 0.0)
    np.testing.assert_array_equal(response.baseline_positions, response.free_positions)
    np.testing.assert_array_equal(
        response.baseline_memory_centers,
        response.free_memory_centers,
    )
    np.testing.assert_array_equal(
        response.baseline_radius_ratios,
        response.free_radius_ratios,
    )


def test_cross_eta_calibration_matches_requested_baseline_fraction() -> None:
    calibration = calibrate_frozen_source_cross_eta(
        _target_state(),
        _source_state(),
        _config(eta=0.15),
        source_center_offset=[1.0, 0.0],
        response_fraction=0.03,
        pulse_steps=5,
    )

    reconstructed = (
        calibration.cross_eta
        * calibration.baseline_directional_drift
        * calibration.pulse_steps
        / calibration.target_radius
    )
    assert reconstructed == pytest.approx(0.03)
    np.testing.assert_array_equal(calibration.source_center_offset, [1.0, 0.0])
    assert calibration.cross_eta > 0.0


def test_cross_eta_calibration_accepts_independent_readout_resolution() -> None:
    readout = ScalarReadoutKernel(
        sigma_rep=0.25,
        sigma_att=0.75,
        amplitude_rep=1.0,
        amplitude_att=20.0,
    )
    calibration = calibrate_frozen_source_cross_eta(
        _target_state(),
        _source_state(),
        _config(eta=0.15),
        source_center_offset=[1.0, 0.0],
        response_fraction=0.03,
        pulse_steps=5,
        cross_readout=readout,
    )

    reconstructed = (
        calibration.cross_eta
        * calibration.baseline_directional_drift
        * calibration.pulse_steps
        / calibration.target_radius
    )
    assert reconstructed == pytest.approx(0.03)
    assert calibration.cross_readout == readout


def test_cross_eta_uses_source_axis_projection_for_off_center_visible_state() -> None:
    base = _target_state()
    target = FiniteMemoryState(
        x=np.array([0.0, 0.08]),
        memory=base.memory,
        weights=base.weights,
    )
    calibration = calibrate_frozen_source_cross_eta(
        target,
        _source_state(),
        _config(eta=0.15),
        source_center_offset=[0.5, 0.0],
        response_fraction=0.03,
        pulse_steps=5,
    )

    reconstructed = (
        calibration.cross_eta
        * calibration.baseline_directional_drift
        * calibration.pulse_steps
        / calibration.target_radius
    )
    assert reconstructed == pytest.approx(0.03)
    assert calibration.baseline_directional_drift < calibration.baseline_gradient_norm


def test_frozen_source_response_is_translation_equivariant() -> None:
    target = _target_state()
    source = _source_state()
    offset = np.array([12.0, -7.0])
    noise = np.random.default_rng(17).normal(size=(4, 2))
    kwargs = {
        "directions": np.eye(2),
        "source_center_offset": [1.0, 0.0],
        "perturbation": 0.1,
        "noise": noise,
        "sample_steps": [1, 2, 4],
        "cross_eta": 1e-4,
        "pulse_steps": 2,
    }

    original = paired_frozen_source_response(
        target,
        source,
        _config(eta=0.15, epsilon=0.01),
        **kwargs,
    )
    translated = paired_frozen_source_response(
        translate_finite_memory_state(target, offset),
        translate_finite_memory_state(source, offset),
        _config(eta=0.15, epsilon=0.01),
        **kwargs,
    )

    np.testing.assert_allclose(
        translated.position_jacobians,
        original.position_jacobians,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        translated.memory_center_jacobians,
        original.memory_center_jacobians,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        translated.shape_jacobians,
        original.shape_jacobians,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        translated.radius_even_offsets,
        original.radius_even_offsets,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        translated.free_positions,
        original.free_positions + offset,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        translated.baseline_positions,
        original.baseline_positions + offset,
        atol=1e-12,
    )


def test_frozen_source_rejects_dimension_mismatch() -> None:
    source = FiniteMemoryState(
        x=np.zeros(3),
        memory=np.zeros((1, 3)),
        weights=np.ones(1),
    )
    with pytest.raises(ValueError, match="share one dimension"):
        paired_frozen_source_response(
            _target_state(),
            source,
            _config(eta=0.15),
            directions=np.eye(2),
            source_center_offset=[1.0, 0.0],
            perturbation=0.1,
            noise=np.zeros((1, 2)),
            sample_steps=[1],
            cross_eta=1e-3,
            pulse_steps=1,
        )
