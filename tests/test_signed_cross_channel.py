import numpy as np
import pytest

from emergenz_knoten import (
    FiniteMemoryState,
    SimulationConfig,
    calibrate_signed_cross_eta,
    paired_signed_cross_response,
    zero_mean_curvature_matched_amplitudes,
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
        amplitude_att=35.0,
        memory_factor=1.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )


def _cross_parameters() -> tuple[SimulationConfig, float]:
    target = _config(eta=0.15)
    target_curvature = target.amplitude_att / target.sigma_att**2 - (
        target.amplitude_rep / target.sigma_rep**2
    )
    amplitude_att, amplitude_comp = zero_mean_curvature_matched_amplitudes(
        dim=target.dim,
        sigma_rep=target.sigma_rep,
        sigma_att=target.sigma_att,
        sigma_comp=10.0,
        target_curvature=target_curvature,
        amplitude_rep=target.amplitude_rep,
    )
    source = SimulationConfig(**{**target.__dict__, "amplitude_att": amplitude_att})
    return source, amplitude_comp


def test_signed_cross_calibration_uses_compensated_initial_field() -> None:
    source_config, amplitude_comp = _cross_parameters()
    calibration = calibrate_signed_cross_eta(
        _target_state(),
        _source_state(),
        _config(eta=0.15),
        source_center_offset=[1.0, 0.0],
        response_fraction=0.03,
        pulse_steps=5,
        source_config=source_config,
        sigma_comp=10.0,
        amplitude_comp=amplitude_comp,
    )

    reconstructed = (
        calibration.cross_eta
        * abs(calibration.canonical_directional_drift)
        * calibration.pulse_steps
        / calibration.target_radius
    )
    assert reconstructed == pytest.approx(0.03)
    assert calibration.canonical_directional_drift > 0.0
    assert calibration.cross_eta > 0.0


def test_signed_cross_channel_has_exact_nulls_and_product_symmetry() -> None:
    source_config, amplitude_comp = _cross_parameters()
    labels = [(1, 1), (1, -1), (0, 1), (1, 0), (0, 0), (-1, -1), (-1, 1)]
    response = paired_signed_cross_response(
        _target_state(),
        _source_state(),
        _config(eta=0.15, epsilon=0.01),
        label_pairs=labels,
        source_center_offset=[1.0, 0.0],
        noise=np.arange(8, dtype=float).reshape(4, 2) / 100.0,
        sample_steps=[0, 1, 4],
        cross_eta=1.0e-4,
        pulse_steps=2,
        source_config=source_config,
        sigma_comp=10.0,
        amplitude_comp=amplitude_comp,
    )

    for index in (2, 3, 4):
        np.testing.assert_array_equal(
            response.positions[:, index],
            response.free_positions,
        )
        np.testing.assert_array_equal(
            response.memory_centers[:, index],
            response.free_memory_centers,
        )
        np.testing.assert_array_equal(
            response.shape_vectors[:, index],
            response.free_shape_vectors,
        )
        np.testing.assert_array_equal(
            response.radius_ratios[:, index],
            response.free_radius_ratios,
        )

    np.testing.assert_array_equal(response.positions[:, 0], response.positions[:, 5])
    np.testing.assert_array_equal(response.positions[:, 1], response.positions[:, 6])
    np.testing.assert_allclose(
        response.position_displacements[1, 0],
        -response.position_displacements[1, 1],
        atol=2.0e-18,
    )
    source_direction = response.source_center_offset / np.linalg.norm(
        response.source_center_offset
    )
    assert np.dot(response.position_displacements[1, 0], source_direction) > 0.0
    assert np.dot(response.position_displacements[1, 1], source_direction) < 0.0


def test_signed_cross_zero_coupling_keeps_every_label_on_free_path() -> None:
    response = paired_signed_cross_response(
        _target_state(),
        _source_state(),
        _config(eta=0.15, epsilon=0.01),
        label_pairs=[(1, 1), (1, -1), (0, 1)],
        source_center_offset=[1.0, 0.0],
        noise=np.ones((3, 2)),
        sample_steps=[1, 3],
        cross_eta=0.0,
        pulse_steps=1,
    )

    expected = np.repeat(response.free_positions[:, None, :], 3, axis=1)
    np.testing.assert_array_equal(response.positions, expected)
    np.testing.assert_array_equal(response.position_displacements, 0.0)


def test_signed_cross_rejects_non_discrete_labels() -> None:
    with pytest.raises(ValueError, match="labels"):
        paired_signed_cross_response(
            _target_state(),
            _source_state(),
            _config(eta=0.15),
            label_pairs=[(1, 0.5)],
            source_center_offset=[1.0, 0.0],
            noise=np.zeros((1, 2)),
            sample_steps=[1],
            cross_eta=1.0e-4,
            pulse_steps=1,
        )
