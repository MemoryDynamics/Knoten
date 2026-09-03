from __future__ import annotations

import math

import numpy as np
import pytest

from emergenz_knoten.mutual_center_coupling import (
    mutual_center_rounding_metrology,
    mutual_center_step,
)
from emergenz_knoten.orbit_center_actuator import (
    candidate_orbit_center_readout,
)
from emergenz_knoten.rotating_wave_stability import (
    native_fifo_step,
    rotation_matrix,
)
from emergenz_knoten.rotating_wave_stability_gate import RotatingWaveCandidate


def _candidate() -> RotatingWaveCandidate:
    return RotatingWaveCandidate(
        candidate_id="mutual-small-h17",
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


def _history(*, phase: float, center: complex) -> np.ndarray:
    ages = np.arange(17, dtype=float)
    base = np.column_stack(
        (
            0.1 * ages + np.sin(0.37 * ages),
            -0.05 * ages + np.cos(0.23 * ages),
        )
    )
    rotated = base @ rotation_matrix(phase).T
    return rotated + np.asarray([center.real, center.imag])


def _pair(*, mode: str, coupling: float = 0.0125):
    candidate = _candidate()
    readout_a = candidate_orbit_center_readout(candidate, chirality=1)
    readout_b = candidate_orbit_center_readout(candidate, chirality=-1)
    history_a = _history(phase=0.2, center=-1.5 + 0.1j)
    history_b = _history(phase=-0.3, center=1.5 - 0.1j)
    return mutual_center_step(
        history_a,
        history_b,
        candidate_a=candidate,
        candidate_b=candidate,
        readout_a=readout_a,
        readout_b=readout_b,
        coupling=coupling,
        mode=mode,
    )


def test_reciprocal_step_closes_force_midpoint_and_pair_ledgers() -> None:
    result = _pair(mode="reciprocal")
    assert result.loop_a.center_force == -result.loop_b.center_force
    assert abs(result.applied_force_balance_residual) < 1e-15
    assert abs(result.completed_force_balance_residual) < 1e-15
    assert abs(result.midpoint_force_residual_a) < 1e-13
    assert abs(result.midpoint_force_residual_b) < 1e-13
    assert abs(result.loop_a.work_split_residual) < 1e-12
    assert abs(result.loop_b.work_split_residual) < 1e-12
    assert abs(result.pair_ledger_residual) < 1e-12
    assert abs(result.closed_pair_ledger_residual) < 1e-12
    assert result.reservoir_work == 0.0
    assert result.loop_a.write_mobility_dissipation >= 0.0
    assert result.loop_b.write_mobility_dissipation >= 0.0


@pytest.mark.parametrize(
    ("mode", "source_name"),
    (("a_to_b", "a"), ("b_to_a", "b")),
)
def test_one_way_source_is_bitwise_native_and_reservoir_closes(
    mode: str,
    source_name: str,
) -> None:
    result = _pair(mode=mode)
    candidate = _candidate()
    source = result.loop_a if source_name == "a" else result.loop_b
    native = native_fifo_step(
        source.history_before,
        **candidate.step_parameters(),
    )
    assert np.array_equal(source.history_after, native)
    assert source.center_force == 0.0j
    assert source.history_increment == 0.0j
    assert abs(result.completed_force_balance_residual) < 1e-15
    assert abs(result.midpoint_force_residual_a) < 1e-13
    assert abs(result.midpoint_force_residual_b) < 1e-13
    assert abs(result.pair_ledger_residual) < 1e-12
    assert abs(result.closed_pair_ledger_residual) > 1e-7
    assert abs(result.reservoir_work) > 1e-7


def test_off_pair_is_exactly_two_native_steps() -> None:
    candidate = _candidate()
    readout_a = candidate_orbit_center_readout(candidate, chirality=1)
    readout_b = candidate_orbit_center_readout(candidate, chirality=-1)
    history_a = _history(phase=0.2, center=-1.5 + 0.1j)
    history_b = _history(phase=-0.3, center=1.5 - 0.1j)
    result = mutual_center_step(
        history_a,
        history_b,
        candidate_a=candidate,
        candidate_b=candidate,
        readout_a=readout_a,
        readout_b=readout_b,
        coupling=0.0,
        mode="off",
    )
    assert np.array_equal(
        result.loop_a.history_after,
        native_fifo_step(history_a, **candidate.step_parameters()),
    )
    assert np.array_equal(
        result.loop_b.history_after,
        native_fifo_step(history_b, **candidate.step_parameters()),
    )
    assert result.loop_a.center_force == 0.0j
    assert result.loop_b.center_force == 0.0j
    assert result.interaction_before == 0.0
    assert result.interaction_after == 0.0
    assert result.pair_ledger_residual == 0.0


def test_reciprocal_step_is_covariant_under_swap() -> None:
    candidate = _candidate()
    readout_a = candidate_orbit_center_readout(candidate, chirality=1)
    readout_b = candidate_orbit_center_readout(candidate, chirality=-1)
    history_a = _history(phase=0.2, center=-1.5 + 0.1j)
    history_b = _history(phase=-0.3, center=1.5 - 0.1j)
    forward = mutual_center_step(
        history_a,
        history_b,
        candidate_a=candidate,
        candidate_b=candidate,
        readout_a=readout_a,
        readout_b=readout_b,
        coupling=0.0125,
        mode="reciprocal",
    )
    swapped = mutual_center_step(
        history_b,
        history_a,
        candidate_a=candidate,
        candidate_b=candidate,
        readout_a=readout_b,
        readout_b=readout_a,
        coupling=0.0125,
        mode="reciprocal",
    )
    assert np.array_equal(
        forward.loop_a.history_after,
        swapped.loop_b.history_after,
    )
    assert np.array_equal(
        forward.loop_b.history_after,
        swapped.loop_a.history_after,
    )
    assert forward.loop_a.center_force == swapped.loop_b.center_force
    assert forward.loop_b.center_force == swapped.loop_a.center_force
    assert forward.separation_after == -swapped.separation_after
    assert forward.pair_ledger_residual == swapped.pair_ledger_residual


def test_reciprocal_step_is_translation_and_rotation_covariant() -> None:
    candidate = _candidate()
    readout_a = candidate_orbit_center_readout(candidate, chirality=1)
    readout_b = candidate_orbit_center_readout(candidate, chirality=-1)
    history_a = _history(phase=0.2, center=-1.5 + 0.1j)
    history_b = _history(phase=-0.3, center=1.5 - 0.1j)
    baseline = mutual_center_step(
        history_a,
        history_b,
        candidate_a=candidate,
        candidate_b=candidate,
        readout_a=readout_a,
        readout_b=readout_b,
        coupling=0.0125,
        mode="reciprocal",
    )

    translation = np.asarray([0.7, -0.4])
    translated = mutual_center_step(
        history_a + translation,
        history_b + translation,
        candidate_a=candidate,
        candidate_b=candidate,
        readout_a=readout_a,
        readout_b=readout_b,
        coupling=0.0125,
        mode="reciprocal",
    )
    assert (
        np.max(
            np.abs(
                translated.loop_a.history_after
                - translation
                - baseline.loop_a.history_after
            )
        )
        < 2e-14
    )
    assert (
        np.max(
            np.abs(
                translated.loop_b.history_after
                - translation
                - baseline.loop_b.history_after
            )
        )
        < 2e-14
    )

    angle = 0.31
    rotation = rotation_matrix(angle)
    rotated = mutual_center_step(
        history_a @ rotation.T,
        history_b @ rotation.T,
        candidate_a=candidate,
        candidate_b=candidate,
        readout_a=readout_a,
        readout_b=readout_b,
        coupling=0.0125,
        mode="reciprocal",
    )
    expected_force = baseline.loop_a.center_force * complex(
        math.cos(angle),
        math.sin(angle),
    )
    assert abs(rotated.loop_a.center_force - expected_force) < 2e-14
    assert (
        np.max(
            np.abs(
                rotated.loop_a.history_after
                - baseline.loop_a.history_after @ rotation.T
            )
        )
        < 2e-14
    )
    assert (
        np.max(
            np.abs(
                rotated.loop_b.history_after
                - baseline.loop_b.history_after @ rotation.T
            )
        )
        < 2e-14
    )


def test_rounding_metrology_bounds_both_full_center_residuals() -> None:
    candidate = _candidate()
    readout_a = candidate_orbit_center_readout(candidate, chirality=1)
    readout_b = candidate_orbit_center_readout(candidate, chirality=-1)
    result = _pair(mode="reciprocal")
    observed = mutual_center_rounding_metrology(
        result,
        readout_a=readout_a,
        readout_b=readout_b,
    )
    for loop in (observed.loop_a, observed.loop_b):
        assert loop.normal_operands is True
        assert abs(loop.center_local_residual) < 1e-15
        assert abs(loop.center_full_residual) <= loop.center_full_envelope
        assert loop.weighted_sum_after_upper > 0.0
        assert loop.weighted_sum_provisional_upper > 0.0


def test_age_and_raw_center_rivals_are_resolved() -> None:
    result = _pair(mode="reciprocal")
    scale = max(
        abs(result.interaction_before),
        abs(result.interaction_after),
    )
    assert abs(result.omitted_age_a_residual) / scale > 1e-5
    assert abs(result.omitted_age_b_residual) / scale > 1e-5
    assert abs(result.omitted_both_ages_residual) / scale > 1e-5
    assert abs(result.raw_center_ledger_residual) / scale > 1e-5
    assert abs(result.flipped_force_a_ledger_residual) / scale > 1e-5


@pytest.mark.parametrize("coupling", (0.0125, -0.0125))
@pytest.mark.parametrize("mode", ("a_to_b", "b_to_a", "reciprocal"))
def test_midpoint_force_matches_the_frozen_closed_form(
    mode: str,
    coupling: float,
) -> None:
    result = _pair(mode=mode, coupling=coupling)
    candidate = _candidate()
    readout_a = candidate_orbit_center_readout(candidate, chirality=1)
    readout_b = candidate_orbit_center_readout(candidate, chirality=-1)
    mobility_a = candidate.alpha * readout_a.write_gain
    mobility_b = candidate.alpha * readout_b.write_gain
    numerator = coupling * (result.separation_before + result.separation_provisional)
    if mode == "a_to_b":
        assert result.loop_a.center_force == 0.0j
        assert result.loop_b.center_force == pytest.approx(
            numerator / (2.0 + coupling * mobility_b), abs=1e-15
        )
    elif mode == "b_to_a":
        assert result.loop_b.center_force == 0.0j
        assert result.loop_a.center_force == pytest.approx(
            -numerator / (2.0 + coupling * mobility_a), abs=1e-15
        )
    else:
        expected = -numerator / (2.0 + coupling * (mobility_a + mobility_b))
        assert result.loop_a.center_force == pytest.approx(expected, abs=1e-15)
        assert result.loop_b.center_force == pytest.approx(-expected, abs=1e-15)


@pytest.mark.parametrize("coupling", (0.0125, -0.0125))
def test_reciprocal_separation_is_the_exact_first_order_midpoint_map(
    coupling: float,
) -> None:
    result = _pair(mode="reciprocal", coupling=coupling)
    candidate = _candidate()
    readout_a = candidate_orbit_center_readout(candidate, chirality=1)
    readout_b = candidate_orbit_center_readout(candidate, chirality=-1)
    mobility_sum = candidate.alpha * (readout_a.write_gain + readout_b.write_gain)
    expected = (
        2.0 * result.separation_provisional
        - coupling * mobility_sum * result.separation_before
    ) / (2.0 + coupling * mobility_sum)
    assert result.separation_after == pytest.approx(expected, abs=2e-15)


@pytest.mark.parametrize("mode", ("a_to_b", "b_to_a", "reciprocal"))
def test_mutual_step_is_reflection_covariant_with_chirality_flip(mode: str) -> None:
    candidate = _candidate()
    history_a = _history(phase=0.2, center=-1.5 + 0.1j)
    history_b = _history(phase=-0.3, center=1.5 - 0.1j)
    readout_a = candidate_orbit_center_readout(candidate, chirality=1)
    readout_b = candidate_orbit_center_readout(candidate, chirality=-1)
    baseline = mutual_center_step(
        history_a,
        history_b,
        candidate_a=candidate,
        candidate_b=candidate,
        readout_a=readout_a,
        readout_b=readout_b,
        coupling=0.0125,
        mode=mode,
    )
    reflected_a = history_a.copy()
    reflected_b = history_b.copy()
    reflected_a[:, 1] *= -1.0
    reflected_b[:, 1] *= -1.0
    reflected = mutual_center_step(
        reflected_a,
        reflected_b,
        candidate_a=candidate,
        candidate_b=candidate,
        readout_a=candidate_orbit_center_readout(candidate, chirality=-1),
        readout_b=candidate_orbit_center_readout(candidate, chirality=1),
        coupling=0.0125,
        mode=mode,
    )
    expected_a = baseline.loop_a.history_after.copy()
    expected_b = baseline.loop_b.history_after.copy()
    expected_a[:, 1] *= -1.0
    expected_b[:, 1] *= -1.0
    assert np.max(np.abs(reflected.loop_a.history_after - expected_a)) < 2e-14
    assert np.max(np.abs(reflected.loop_b.history_after - expected_b)) < 2e-14
    assert reflected.loop_a.center_force == pytest.approx(
        baseline.loop_a.center_force.conjugate(), abs=2e-14
    )
    assert reflected.loop_b.center_force == pytest.approx(
        baseline.loop_b.center_force.conjugate(), abs=2e-14
    )


def test_validation_rejects_off_coupling_bad_mode_and_singular_denominator() -> None:
    candidate = _candidate()
    readout = candidate_orbit_center_readout(candidate, chirality=1)
    history_a = _history(phase=0.2, center=-1.5 + 0.1j)
    history_b = _history(phase=-0.3, center=1.5 - 0.1j)
    with pytest.raises(ValueError, match="off mode requires zero coupling"):
        mutual_center_step(
            history_a,
            history_b,
            candidate_a=candidate,
            candidate_b=candidate,
            readout_a=readout,
            readout_b=readout,
            coupling=0.1,
            mode="off",
        )
    with pytest.raises(ValueError, match="unsupported"):
        mutual_center_step(
            history_a,
            history_b,
            candidate_a=candidate,
            candidate_b=candidate,
            readout_a=readout,
            readout_b=readout,
            coupling=0.0,
            mode="bad",  # type: ignore[arg-type]
        )
    mobility = candidate.alpha * readout.write_gain
    with pytest.raises(ValueError, match="denominator is singular"):
        mutual_center_step(
            history_a,
            history_b,
            candidate_a=candidate,
            candidate_b=candidate,
            readout_a=readout,
            readout_b=readout,
            coupling=-1.0 / mobility,
            mode="reciprocal",
        )
