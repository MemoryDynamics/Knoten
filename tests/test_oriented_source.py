from __future__ import annotations

import numpy as np

from emergenz_knoten import (
    FiniteMemoryState,
    OrientedMemoryState,
    SimulationConfig,
    autonomous_oriented_source_trace,
    initialize_oriented_memory_state,
    one_way_oriented_response,
    oriented_response_metrics,
    place_oriented_memory_state,
    memory_centroid,
    translate_finite_memory_state,
    update_persistent_orientation,
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


def _response(
    source: OrientedMemoryState,
    *,
    vector_eta: float,
    target: FiniteMemoryState | None = None,
    noise: np.ndarray | None = None,
):
    steps = 10
    values = np.zeros((steps, 2)) if noise is None else noise
    return one_way_oriented_response(
        _state() if target is None else target,
        source,
        _config(epsilon=0.0, eta=0.0) if noise is None else _config(),
        source_center_offset=[1.0, 0.0],
        target_noise=values,
        source_noise=values[::-1].copy(),
        sample_steps=[0, 1, 5, steps],
        vector_eta=vector_eta,
        vector_sigma=1.0,
        randomization_count=4,
        random_seed=17,
    )


def test_persistent_orientation_is_linear_low_pass_not_unit_projection() -> None:
    updated = update_persistent_orientation(
        np.array([1.0, 0.0]),
        np.array([0.0, 3.0]),
        relaxation=0.25,
    )

    np.testing.assert_allclose(updated, [0.75, 0.25])
    assert not np.isclose(np.linalg.norm(updated), 1.0)
    np.testing.assert_allclose(
        update_persistent_orientation(
            np.array([0.4, -0.2]),
            np.zeros(2),
            relaxation=0.25,
        ),
        [0.3, -0.15],
    )


def test_initialization_reconstructs_age_ordered_vector_fibre() -> None:
    state = FiniteMemoryState(
        x=np.array([3.0, 0.0]),
        memory=np.array([[3.0, 0.0], [2.0, 0.0], [1.0, 0.0], [0.0, 0.0]]),
        weights=np.ones(4),
    )
    oriented = initialize_oriented_memory_state(
        state,
        lambda_vector=0.5,
        vector_mass=2.0,
        orientation_relaxation=0.5,
    )

    np.testing.assert_allclose(oriented.orientations[:, 0], [0.875, 0.75, 0.5, 0.0])
    np.testing.assert_allclose(oriented.orientations[:, 1], 0.0)
    np.testing.assert_allclose(oriented.weights, [1.0, 0.5, 0.25, 0.125])
    np.testing.assert_array_equal(
        oriented.carrier_orientation,
        oriented.orientations[0],
    )
    assert oriented.orientations.flags.writeable is False


def test_oriented_state_rigid_rotation_transforms_positions_and_vectors() -> None:
    oriented = initialize_oriented_memory_state(
        _state(),
        lambda_vector=0.2,
        orientation_relaxation=0.2,
    )
    rotation = np.array([[0.0, -1.0], [1.0, 0.0]])
    placed = place_oriented_memory_state(
        oriented,
        [2.0, 3.0],
        rotation=rotation,
    )

    np.testing.assert_allclose(
        placed.orientations,
        oriented.orientations @ rotation.T,
    )
    np.testing.assert_allclose(
        placed.carrier_orientation,
        rotation @ oriented.carrier_orientation,
    )
    np.testing.assert_allclose(
        np.average(
            placed.scalar_state.memory,
            axis=0,
            weights=placed.scalar_state.weights,
        ),
        [2.0, 3.0],
    )


def test_zero_vector_eta_keeps_every_target_path_identical() -> None:
    noise = np.arange(20, dtype=float).reshape(10, 2) / 100.0
    source = initialize_oriented_memory_state(
        _state(),
        lambda_vector=0.2,
        orientation_relaxation=0.2,
    )
    response = _response(source, vector_eta=0.0, noise=noise)

    for path in range(1, len(response.target_conditions)):
        np.testing.assert_array_equal(
            response.target_positions[:, path],
            response.target_positions[:, 0],
        )
        np.testing.assert_array_equal(
            response.target_memory_centers[:, path],
            response.target_memory_centers[:, 0],
        )


def test_zero_vector_mass_matches_channel_off_with_nonzero_coupling() -> None:
    source = initialize_oriented_memory_state(
        _state(),
        lambda_vector=0.2,
        vector_mass=0.0,
        orientation_relaxation=0.2,
    )
    response = _response(source, vector_eta=3.0)

    active, sign_flip, channel_off = range(3)
    np.testing.assert_array_equal(
        response.target_positions[:, active],
        response.target_positions[:, channel_off],
    )
    np.testing.assert_array_equal(
        response.target_positions[:, sign_flip],
        response.target_positions[:, channel_off],
    )


def test_global_sign_flip_reverses_deterministic_target_response() -> None:
    scalar = _state()
    orientations = np.tile(np.array([0.0, 0.5]), (scalar.n_memory, 1))
    source = OrientedMemoryState(
        scalar_state=scalar,
        orientations=orientations,
        weights=np.array([0.4, 0.2, 0.1, 0.05, 0.025]),
        carrier_orientation=np.array([0.0, 0.5]),
        orientation_relaxation=0.2,
    )
    response = _response(source, vector_eta=0.02)
    active, sign_flip, channel_off = range(3)
    active_delta = (
        response.target_memory_centers[:, active]
        - response.target_memory_centers[:, channel_off]
    )
    flip_delta = (
        response.target_memory_centers[:, sign_flip]
        - response.target_memory_centers[:, channel_off]
    )

    active_final = active_delta[-1]
    flip_final = flip_delta[-1]
    active_norm = np.linalg.norm(active_final)
    flip_norm = np.linalg.norm(flip_final)
    cosine = float(np.dot(active_final, flip_final) / (active_norm * flip_norm))

    assert active_norm > 0.0
    assert cosine < -0.999
    assert np.isclose(active_norm, flip_norm, rtol=1e-3)


def test_target_readout_does_not_change_autonomous_source() -> None:
    noise = np.arange(20, dtype=float).reshape(10, 2) / 100.0
    source = initialize_oriented_memory_state(
        _state(),
        lambda_vector=0.2,
        orientation_relaxation=0.2,
    )
    off = _response(source, vector_eta=0.0, noise=noise)
    active = _response(source, vector_eta=0.03, noise=noise)

    np.testing.assert_array_equal(active.source_positions, off.source_positions)
    np.testing.assert_array_equal(
        active.source_memory_centers,
        off.source_memory_centers,
    )
    np.testing.assert_array_equal(
        active.source_carrier_orientations,
        off.source_carrier_orientations,
    )


def test_source_only_trace_matches_one_way_source_bitwise() -> None:
    scalar = _state()
    source = initialize_oriented_memory_state(
        scalar,
        lambda_vector=0.2,
        orientation_relaxation=0.2,
    )
    steps = np.array([0, 1, 5, 10])
    target_noise = np.arange(20, dtype=float).reshape(10, 2) / 100.0
    source_noise = target_noise[::-1].copy()
    full = one_way_oriented_response(
        scalar,
        source,
        _config(),
        source_center_offset=[1.0, 0.0],
        target_noise=target_noise,
        source_noise=source_noise,
        sample_steps=steps,
        vector_eta=0.0,
        vector_sigma=1.0,
        randomization_count=1,
    )
    placed = place_oriented_memory_state(
        source,
        memory_centroid(scalar) + np.array([1.0, 0.0]),
    )
    source_only = autonomous_oriented_source_trace(
        placed,
        _config(),
        source_noise=source_noise,
        sample_steps=steps,
    )

    np.testing.assert_array_equal(source_only.positions, full.source_positions)
    np.testing.assert_array_equal(
        source_only.memory_centers,
        full.source_memory_centers,
    )
    np.testing.assert_array_equal(
        source_only.shape_tensors,
        full.source_shape_tensors,
    )
    np.testing.assert_array_equal(
        source_only.radius_ratios,
        full.source_radius_ratios,
    )
    np.testing.assert_array_equal(
        source_only.carrier_orientations,
        full.source_carrier_orientations,
    )


def test_oriented_response_is_translation_equivariant() -> None:
    shift = np.array([5.0, -3.0])
    source = initialize_oriented_memory_state(
        _state(),
        lambda_vector=0.2,
        orientation_relaxation=0.2,
    )
    original = _response(source, vector_eta=0.02)
    shifted_scalar = translate_finite_memory_state(_state(), shift)
    shifted_source = OrientedMemoryState(
        scalar_state=translate_finite_memory_state(source.scalar_state, shift),
        orientations=source.orientations,
        weights=source.weights,
        carrier_orientation=source.carrier_orientation,
        orientation_relaxation=source.orientation_relaxation,
    )
    translated = _response(
        shifted_source,
        vector_eta=0.02,
        target=shifted_scalar,
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


def test_one_step_control_shares_exact_scalar_source_and_off_target() -> None:
    scalar = _state()
    persistent = initialize_oriented_memory_state(
        scalar,
        lambda_vector=0.2,
        orientation_relaxation=0.2,
    )
    one_step = initialize_oriented_memory_state(
        scalar,
        lambda_vector=1.0,
        orientation_relaxation=1.0,
    )

    persistent_response = _response(persistent, vector_eta=0.02)
    one_step_response = _response(one_step, vector_eta=0.02)
    channel_off = 2

    np.testing.assert_array_equal(
        persistent_response.source_positions,
        one_step_response.source_positions,
    )
    np.testing.assert_array_equal(
        persistent_response.source_memory_centers,
        one_step_response.source_memory_centers,
    )
    np.testing.assert_array_equal(
        persistent_response.target_positions[:, channel_off],
        one_step_response.target_positions[:, channel_off],
    )
    np.testing.assert_array_equal(
        persistent_response.target_memory_centers[:, channel_off],
        one_step_response.target_memory_centers[:, channel_off],
    )


def test_oriented_response_metrics_preserve_paired_control_geometry() -> None:
    scalar = _state()
    source = OrientedMemoryState(
        scalar_state=scalar,
        orientations=np.tile(np.array([0.0, 0.5]), (scalar.n_memory, 1)),
        weights=np.array([0.4, 0.2, 0.1, 0.05, 0.025]),
        carrier_orientation=np.array([0.0, 0.5]),
        orientation_relaxation=0.2,
    )
    response = _response(source, vector_eta=0.02)

    metrics = oriented_response_metrics(
        response,
        radius=1.0,
        radial_direction=np.array([-1.0, 0.0]),
        random_quantile=0.95,
    )

    assert metrics["active_response_r"] > 0.0
    assert metrics["flip_cosine"] < -0.99
    assert metrics["tangential_fraction"] > 0.99
    assert metrics["target_radius_max_change"] >= 0.0
