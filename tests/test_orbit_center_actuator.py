from __future__ import annotations

from dataclasses import replace
import math

import numpy as np

from emergenz_knoten.orbit_center_actuator import (
    adjoint_slot_forces,
    build_orbit_center_readout,
    candidate_orbit_center_readout,
    complex_to_vector,
    memory_center,
    orbit_center,
    real_inner,
    reciprocal_source_write_step,
    source_write_rounding_metrology,
)
from emergenz_knoten.rotating_wave_formation import target_history
from emergenz_knoten.rotating_wave_stability import native_fifo_step, rotation_matrix
from emergenz_knoten.rotating_wave_stability_gate import RotatingWaveCandidate


def _l3_candidate() -> RotatingWaveCandidate:
    return RotatingWaveCandidate(
        candidate_id="l3-test",
        radius=0.9448058117057437,
        theta=0.007906661462435524,
        alpha=0.005,
        horizon=2400,
        memory_mass=1.0,
        eta=0.075,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=3.5,
    )


def _small_candidate() -> RotatingWaveCandidate:
    return RotatingWaveCandidate(
        candidate_id="unrelated-h17",
        radius=0.8,
        theta=0.19,
        alpha=0.08,
        horizon=17,
        memory_mass=1.0,
        eta=0.03,
        sigma_rep=1.0,
        sigma_att=2.5,
        amplitude_rep=1.0,
        amplitude_att=2.0,
    )


def _small_history() -> np.ndarray:
    ages = np.arange(17, dtype=float)
    return np.column_stack(
        (
            0.1 * ages + np.sin(0.37 * ages),
            -0.05 * ages + np.cos(0.23 * ages),
        )
    )


def test_l3_readout_matches_frozen_coefficients_and_notch() -> None:
    candidate = _l3_candidate()
    plus = candidate_orbit_center_readout(candidate, chirality=1)
    minus = candidate_orbit_center_readout(candidate, chirality=-1)
    assert abs(plus.beta - complex(0.28847300317511804, -0.45107951349124853)) < 5e-15
    assert abs(
        plus.coefficients[0]
        - complex(0.002499571092111443, 0.6323751736574267)
    ) < 5e-15
    assert math.isclose(
        plus.write_gain,
        0.399904608113905,
        rel_tol=0.0,
        abs_tol=5e-15,
    )
    assert abs(np.sum(plus.coefficients) - 1.0) < 5e-13
    ages = np.arange(candidate.horizon, dtype=float)
    mode = np.exp(-1j * candidate.theta * ages)
    assert abs(np.dot(plus.coefficients, mode)) < 5e-13
    assert abs(minus.beta - plus.beta.conjugate()) < 5e-15
    assert np.max(
        np.abs(minus.coefficients - np.conjugate(plus.coefficients))
    ) < 5e-15


def test_readout_recovers_translation_and_rejects_registered_rotation() -> None:
    candidate = _l3_candidate()
    plus = candidate_orbit_center_readout(candidate, chirality=1)
    minus = candidate_orbit_center_readout(candidate, chirality=-1)
    target = target_history(candidate, chirality=1)
    translation = np.asarray([0.37, -0.21])
    phase = rotation_matrix(math.pi / 7.0)
    transformed = target @ phase.T + translation
    observed = orbit_center(transformed, readout=plus)
    assert np.linalg.norm(complex_to_vector(observed) - translation) < 1e-12
    assert abs(memory_center(target, readout=plus)) > 0.5 * candidate.radius
    assert abs(orbit_center(target, readout=plus)) < 1e-12 * candidate.radius
    assert abs(orbit_center(target, readout=minus)) > 0.5 * candidate.radius


def test_adjoint_slot_forces_close_virtual_work_and_force_balance() -> None:
    readout = build_orbit_center_readout(
        alpha=0.08,
        horizon=17,
        theta=0.19,
        chirality=1,
    )
    rng = np.random.default_rng(20260826)
    variation = rng.normal(size=(17, 2))
    center_force = np.asarray([0.17, -0.31])
    slot_forces = adjoint_slot_forces(center_force, readout=readout)
    center_variation = orbit_center(variation, readout=readout)
    microscopic = float(np.sum(slot_forces * variation))
    generalized = real_inner(
        complex(*center_force),
        center_variation,
    )
    assert abs(microscopic - generalized) < 1e-12
    assert np.linalg.norm(np.sum(slot_forces, axis=0) - center_force) < 1e-12


def test_source_write_step_closes_full_ledger_and_exposes_age_term() -> None:
    candidate = _small_candidate()
    readout = candidate_orbit_center_readout(candidate, chirality=1)
    result = reciprocal_source_write_step(
        _small_history(),
        np.asarray([0.7, -0.4]),
        candidate=candidate,
        readout=readout,
        coupling_strength=0.25,
    )
    scale = max(
        abs(result.center_work),
        abs(result.write_work) + abs(result.age_work),
    )
    assert abs(result.work_split_residual) < 1e-12
    assert abs(result.ledger_residual) < 1e-12
    assert abs(
        result.truncated_ledger_residual
        - (result.ledger_residual - result.age_work)
    ) < 1e-12
    assert abs(
        result.raw_center_ledger_residual
        - (
            result.ledger_residual
            + result.raw_center_work
            - result.center_work
        )
    ) < 1e-12
    assert abs(
        result.raw_center_before - memory_center(_small_history(), readout=readout)
    ) < 1e-12
    assert abs(result.raw_center_ledger_residual) > 1e-6
    assert abs(result.age_work) / scale > 0.01
    assert abs(result.force_balance_residual) < 1e-12
    assert abs(result.midpoint_force_residual) < 1e-12
    assert abs(result.center_actuation_residual) < 1e-12
    assert abs(result.actuator_update_residual) < 1e-12
    assert abs(result.coupling_displacement_residual) < 1e-12
    assert result.write_mobility_dissipation >= 0.0
    assert result.external_mobility_dissipation >= 0.0


def test_source_write_rounding_metrology_resolves_local_identities() -> None:
    candidate = _small_candidate()
    readout = candidate_orbit_center_readout(candidate, chirality=1)
    result = reciprocal_source_write_step(
        _small_history(),
        np.asarray([0.7, -0.4]),
        candidate=candidate,
        readout=readout,
        coupling_strength=0.25,
    )
    observed = source_write_rounding_metrology(result, readout=readout)

    assert observed.epsilon64 == np.finfo(float).eps
    assert observed.gamma_4 < observed.gamma_8 < observed.gamma_8h
    assert observed.normal_operands is True
    assert abs(observed.center_local_residual) < 1e-15
    assert abs(observed.coupling_local_residual) < 1e-15
    assert abs(observed.center_full_residual) <= observed.center_full_envelope
    assert (
        abs(observed.coupling_full_residual)
        <= observed.coupling_full_envelope
    )
    assert (
        abs(observed.actuator_full_residual)
        <= observed.actuator_full_envelope
    )
    assert observed.weighted_sum_after_upper > 0.0
    assert observed.weighted_sum_provisional_upper > 0.0


def test_source_write_rounding_metrology_rejects_corruption_and_subnormal() -> None:
    candidate = _small_candidate()
    readout = candidate_orbit_center_readout(candidate, chirality=1)
    result = reciprocal_source_write_step(
        _small_history(),
        np.asarray([0.7, -0.4]),
        candidate=candidate,
        readout=readout,
        coupling_strength=0.25,
    )
    corrupted = replace(result, center_actuation_residual=1.0e-8 + 0.0j)
    observed = source_write_rounding_metrology(corrupted, readout=readout)
    assert abs(observed.center_full_residual) > observed.center_full_envelope

    subnormal = replace(result, history_increment=1.0e-320 + 0.0j)
    observed = source_write_rounding_metrology(subnormal, readout=readout)
    assert observed.normal_operands is False


def test_full_dot_reordering_stays_inside_envelope_and_not_local_gate() -> None:
    candidate = _small_candidate()
    readout = candidate_orbit_center_readout(candidate, chirality=1)
    result = reciprocal_source_write_step(
        _small_history(),
        np.asarray([0.7, -0.4]),
        candidate=candidate,
        readout=readout,
        coupling_strength=0.25,
    )
    metrology = source_write_rounding_metrology(result, readout=readout)
    after = result.history[:, 0] + 1j * result.history[:, 1]
    provisional = (
        result.provisional_history[:, 0]
        + 1j * result.provisional_history[:, 1]
    )
    after_terms = list(readout.coefficients * after)
    provisional_terms = list(readout.coefficients * provisional)
    forward = (
        sum(after_terms)
        - sum(provisional_terms)
        - result.center_prescribed_increment
    )
    reverse = (
        sum(reversed(after_terms))
        - sum(reversed(provisional_terms))
        - result.center_prescribed_increment
    )

    assert np.isfinite([forward.real, forward.imag, reverse.real, reverse.imag]).all()
    assert abs(forward) <= metrology.center_full_envelope
    assert abs(reverse) <= metrology.center_full_envelope
    assert abs(metrology.center_local_residual) < 1e-15


def test_channel_off_step_is_bitwise_native() -> None:
    candidate = _small_candidate()
    history = _small_history()
    readout = candidate_orbit_center_readout(candidate, chirality=1)
    expected = native_fifo_step(history, **candidate.step_parameters())
    result = reciprocal_source_write_step(
        history,
        np.asarray([0.7, -0.4]),
        candidate=candidate,
        readout=readout,
        coupling_strength=0.0,
    )
    assert np.array_equal(result.history, expected)
    assert np.array_equal(result.actuator, np.asarray([0.7, -0.4]))


def test_source_write_step_is_translation_and_rotation_covariant() -> None:
    candidate = _small_candidate()
    history = _small_history()
    actuator = np.asarray([0.7, -0.4])
    readout = candidate_orbit_center_readout(candidate, chirality=1)
    base = reciprocal_source_write_step(
        history,
        actuator,
        candidate=candidate,
        readout=readout,
        coupling_strength=0.25,
    )

    translation = np.asarray([0.31, -0.27])
    translated = reciprocal_source_write_step(
        history + translation,
        actuator + translation,
        candidate=candidate,
        readout=readout,
        coupling_strength=0.25,
    )
    assert np.max(np.abs(translated.history - base.history - translation)) < 2e-14
    assert np.max(np.abs(translated.actuator - base.actuator - translation)) < 2e-14

    rotation = rotation_matrix(0.61)
    rotated = reciprocal_source_write_step(
        history @ rotation.T,
        rotation @ actuator,
        candidate=candidate,
        readout=readout,
        coupling_strength=0.25,
    )
    assert np.max(np.abs(rotated.history - base.history @ rotation.T)) < 2e-13
    assert np.max(np.abs(rotated.actuator - rotation @ base.actuator)) < 2e-13


def test_reflection_switches_registered_chirality() -> None:
    candidate = _small_candidate()
    history = _small_history()
    actuator = np.asarray([0.7, -0.4])
    plus = reciprocal_source_write_step(
        history,
        actuator,
        candidate=candidate,
        readout=candidate_orbit_center_readout(candidate, chirality=1),
        coupling_strength=0.25,
    )
    reflected_history = history.copy()
    reflected_history[:, 1] *= -1.0
    reflected_actuator = actuator * np.asarray([1.0, -1.0])
    minus = reciprocal_source_write_step(
        reflected_history,
        reflected_actuator,
        candidate=candidate,
        readout=candidate_orbit_center_readout(candidate, chirality=-1),
        coupling_strength=0.25,
    )
    expected_history = plus.history.copy()
    expected_history[:, 1] *= -1.0
    expected_actuator = plus.actuator * np.asarray([1.0, -1.0])
    assert np.max(np.abs(minus.history - expected_history)) < 2e-13
    assert np.max(np.abs(minus.actuator - expected_actuator)) < 2e-13
