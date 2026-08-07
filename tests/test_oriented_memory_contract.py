from __future__ import annotations

import numpy as np

from emergenz_knoten import (
    FiniteMemoryState,
    OrientedMemoryState,
    SimulationConfig,
    advance_oriented_memory_state,
    autonomous_oriented_source_trace,
    initialize_oriented_memory_state,
    oriented_memory_moments,
    place_oriented_memory_state,
    random_sign_memory_coherences,
)


def _scalar_state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.array([1.0, 0.0, 0.0]),
        memory=np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [-1.0, 0.0, 0.0],
                [0.0, -1.0, 0.0],
            ]
        ),
        weights=np.array([0.4, 0.3, 0.2, 0.1]),
    )


def _oriented_state() -> OrientedMemoryState:
    return OrientedMemoryState(
        scalar_state=_scalar_state(),
        orientations=np.array(
            [
                [0.0, 1.0, 0.0],
                [-1.0, 0.0, 0.0],
                [0.0, -1.0, 0.0],
                [1.0, 0.0, 0.0],
            ]
        ),
        weights=np.array([0.4, 0.3, 0.2, 0.1]),
        carrier_orientation=np.array([0.0, 1.0, 0.0]),
        orientation_relaxation=0.2,
    )


def _config() -> SimulationConfig:
    return SimulationConfig(
        steps=10,
        dim=3,
        epsilon=0.01,
        eta=0.15,
        alpha=0.2,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=20.0,
        max_memory=4,
        sample_every=1,
    )


def test_oriented_moments_use_every_retained_deposit() -> None:
    moments = oriented_memory_moments(_oriented_state())

    assert np.isclose(moments.total_weight, 1.0)
    assert moments.rms_radius > 0.0
    assert moments.orientation_power > 0.0
    assert moments.polarization_coherence > 0.0
    assert moments.circulation_coherence > 0.0
    np.testing.assert_allclose(
        moments.circulation_bivector,
        -moments.circulation_bivector.T,
        atol=1e-15,
    )


def test_oriented_moments_are_translation_invariant_and_rotation_covariant() -> None:
    state = _oriented_state()
    original = oriented_memory_moments(state)
    rotation = np.array(
        [
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    placed = place_oriented_memory_state(
        state,
        [5.0, -2.0, 3.0],
        rotation=rotation,
    )
    transformed = oriented_memory_moments(placed)

    np.testing.assert_allclose(
        transformed.polarization,
        rotation @ original.polarization,
        atol=1e-15,
    )
    np.testing.assert_allclose(
        transformed.circulation_bivector,
        rotation @ original.circulation_bivector @ rotation.T,
        atol=1e-15,
    )
    assert np.isclose(transformed.rms_radius, original.rms_radius)
    assert np.isclose(
        transformed.circulation_coherence,
        original.circulation_coherence,
    )


def test_global_vector_sign_flip_reverses_moments_not_coherences() -> None:
    state = _oriented_state()
    flipped = OrientedMemoryState(
        scalar_state=state.scalar_state,
        orientations=-state.orientations,
        weights=state.weights,
        carrier_orientation=-state.carrier_orientation,
        orientation_relaxation=state.orientation_relaxation,
    )
    original_moments = oriented_memory_moments(state)
    flipped_moments = oriented_memory_moments(flipped)

    np.testing.assert_allclose(
        flipped_moments.polarization,
        -original_moments.polarization,
    )
    np.testing.assert_allclose(
        flipped_moments.circulation_bivector,
        -original_moments.circulation_bivector,
    )
    assert np.isclose(
        flipped_moments.polarization_coherence,
        original_moments.polarization_coherence,
    )
    assert np.isclose(
        flipped_moments.circulation_coherence,
        original_moments.circulation_coherence,
    )


def test_zero_vector_mass_has_zero_vector_observables() -> None:
    state = initialize_oriented_memory_state(
        _scalar_state(),
        lambda_vector=0.2,
        vector_mass=0.0,
    )
    moments = oriented_memory_moments(state)

    assert moments.total_weight == 0.0
    assert moments.polarization_coherence == 0.0
    assert moments.circulation_coherence == 0.0
    np.testing.assert_array_equal(moments.polarization, np.zeros(3))


def test_advance_preserves_full_age_order_and_scalar_null_boundary() -> None:
    state = initialize_oriented_memory_state(
        _scalar_state(),
        lambda_vector=0.2,
        orientation_relaxation=0.2,
    )
    advanced = advance_oriented_memory_state(
        state,
        _config(),
        noise_increment=[0.2, -0.1, 0.3],
    )

    np.testing.assert_array_equal(
        advanced.scalar_state.memory[1:],
        state.scalar_state.memory[:-1],
    )
    np.testing.assert_array_equal(
        advanced.orientations[1:],
        state.orientations[:-1],
    )
    np.testing.assert_array_equal(
        advanced.orientations[0],
        advanced.carrier_orientation,
    )
    np.testing.assert_array_equal(advanced.weights, state.weights)
    np.testing.assert_array_equal(
        advanced.scalar_state.weights,
        state.scalar_state.weights,
    )

def test_random_sign_null_reproduces_observed_coherence_for_all_plus() -> None:
    state = _oriented_state()
    moments = oriented_memory_moments(state)
    polarization, circulation = random_sign_memory_coherences(
        state,
        np.ones((1, state.scalar_state.n_memory)),
    )

    np.testing.assert_allclose(polarization, [moments.polarization_coherence])
    np.testing.assert_allclose(circulation, [moments.circulation_coherence])


def test_random_sign_null_validates_sign_matrix() -> None:
    state = _oriented_state()

    with np.testing.assert_raises(ValueError):
        random_sign_memory_coherences(state, np.zeros((2, 4)))
    with np.testing.assert_raises(ValueError):
        random_sign_memory_coherences(state, np.ones((2, 3)))

def test_single_advance_matches_batched_autonomous_source() -> None:
    state = initialize_oriented_memory_state(
        _scalar_state(),
        lambda_vector=0.2,
        orientation_relaxation=0.2,
    )
    config = _config()
    noise = np.array([[0.2, -0.1, 0.3]])
    advanced = advance_oriented_memory_state(
        state,
        config,
        noise_increment=noise[0],
    )
    trace = autonomous_oriented_source_trace(
        state,
        config,
        source_noise=noise,
        sample_steps=[0, 1],
    )

    np.testing.assert_allclose(advanced.scalar_state.x, trace.positions[-1])
    np.testing.assert_allclose(
        advanced.carrier_orientation,
        trace.carrier_orientations[-1],
    )