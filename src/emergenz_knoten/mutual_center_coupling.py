"""Mutual notched-center coupling for two finite-memory rotating waves."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal

import numpy as np

from .orbit_center_actuator import (
    OrbitCenterReadout,
    complex_to_vector,
    real_inner,
)
from .rotating_wave_stability import native_fifo_step
from .rotating_wave_stability_gate import RotatingWaveCandidate


MutualCenterMode = Literal["off", "a_to_b", "b_to_a", "reciprocal"]


@dataclass(frozen=True)
class LoopCenterWrite:
    """One loop's native advance, optional newest-slot write, and work split."""

    history_before: np.ndarray
    provisional_history: np.ndarray
    history_after: np.ndarray
    center_before: complex
    center_provisional: complex
    center_after: complex
    raw_center_before: complex
    raw_center_after: complex
    center_force: complex
    write_force: complex
    history_increment: complex
    center_prescribed_increment: complex
    write_displacement: complex
    age_center_displacement: complex
    write_work: float
    age_work: float
    center_work: float
    raw_center_work: float
    work_split_residual: float
    center_actuation_residual: complex
    write_mobility_dissipation: float


@dataclass(frozen=True)
class MutualCenterStep:
    """One two-loop transition and its reciprocal or reservoir ledger."""

    mode: MutualCenterMode
    coupling: float
    loop_a: LoopCenterWrite
    loop_b: LoopCenterWrite
    reservoir_force_a: complex
    reservoir_force_b: complex
    reservoir_work: float
    reservoir_raw_work: float
    separation_before: complex
    separation_provisional: complex
    separation_after: complex
    interaction_before: float
    interaction_after: float
    applied_force_balance_residual: complex
    completed_force_balance_residual: complex
    midpoint_force_residual_a: complex
    midpoint_force_residual_b: complex
    pair_ledger_residual: float
    closed_pair_ledger_residual: float
    omitted_age_a_residual: float
    omitted_age_b_residual: float
    omitted_both_ages_residual: float
    raw_center_ledger_residual: float
    flipped_force_a_ledger_residual: float


@dataclass(frozen=True)
class LoopCenterRoundingMetrology:
    """Cancellation-safe binary64 envelope for one loop's center write."""

    epsilon64: float
    gamma_4: float
    gamma_8: float
    gamma_8h: float
    center_local_increment: complex
    center_local_residual: complex
    center_full_residual: complex
    weighted_sum_after_upper: float
    weighted_sum_provisional_upper: float
    history_insertion_bound: float
    center_local_bound: float
    center_full_envelope: float
    normal_operands: bool


@dataclass(frozen=True)
class MutualCenterRoundingMetrology:
    """Binary64 write metrology for both members of a mutual-center step."""

    loop_a: LoopCenterRoundingMetrology
    loop_b: LoopCenterRoundingMetrology


def _complex_history(history: np.ndarray) -> np.ndarray:
    state = np.asarray(history, dtype=float)
    if (
        state.ndim != 2
        or state.shape[0] < 1
        or state.shape[1] != 2
        or not np.isfinite(state).all()
    ):
        raise ValueError("history must be a finite array with shape (H,2)")
    return state[:, 0] + 1j * state[:, 1]


def _validate_loop(
    history: np.ndarray,
    *,
    candidate: RotatingWaveCandidate,
    readout: OrbitCenterReadout,
) -> np.ndarray:
    state = np.asarray(history, dtype=float)
    _complex_history(state)
    if state.shape != (candidate.horizon, 2):
        raise ValueError("history horizon does not match the candidate")
    if (
        readout.horizon != candidate.horizon
        or readout.chirality not in (-1, 1)
        or not math.isclose(
            readout.alpha,
            candidate.alpha,
            rel_tol=0.0,
            abs_tol=0.0,
        )
        or not math.isclose(
            readout.theta,
            candidate.theta,
            rel_tol=0.0,
            abs_tol=0.0,
        )
    ):
        raise ValueError("readout does not match the candidate")
    return state


def _loop_centers(
    history: np.ndarray,
    *,
    readout: OrbitCenterReadout,
) -> tuple[complex, complex]:
    values = _complex_history(history)
    return (
        complex(np.dot(readout.coefficients, values)),
        complex(np.dot(readout.weights, values)),
    )


def _apply_loop_write(
    history_before: np.ndarray,
    provisional_history: np.ndarray,
    *,
    candidate: RotatingWaveCandidate,
    readout: OrbitCenterReadout,
    center_force: complex,
) -> LoopCenterWrite:
    before = np.asarray(history_before, dtype=float)
    provisional = np.asarray(provisional_history, dtype=float)
    before_values = _complex_history(before)
    provisional_values = _complex_history(provisional)
    center_before = complex(np.dot(readout.coefficients, before_values))
    center_provisional = complex(
        np.dot(readout.coefficients, provisional_values)
    )
    raw_center_before = complex(np.dot(readout.weights, before_values))

    force = complex(center_force)
    write_force = readout.coefficients[0].conjugate() * force
    increment_vector = candidate.alpha * complex_to_vector(write_force)
    history_increment = complex(
        float(increment_vector[0]),
        float(increment_vector[1]),
    )
    advanced = provisional.copy()
    if force != 0.0j:
        advanced[0] += increment_vector
    advanced_values = _complex_history(advanced)
    center_after = complex(np.dot(readout.coefficients, advanced_values))
    raw_center_after = complex(np.dot(readout.weights, advanced_values))

    center_prescribed_increment = (
        candidate.alpha * readout.write_gain * force
    )
    write_displacement = advanced_values[0] - before_values[0]
    age_center_displacement = complex(
        np.dot(
            readout.coefficients[1:],
            before_values[:-1] - before_values[1:],
        )
    )
    center_displacement = center_after - center_before
    write_work = real_inner(write_force, write_displacement)
    age_work = real_inner(force, age_center_displacement)
    center_work = real_inner(force, center_displacement)
    raw_center_work = real_inner(
        force,
        raw_center_after - raw_center_before,
    )
    return LoopCenterWrite(
        history_before=before,
        provisional_history=provisional,
        history_after=advanced,
        center_before=center_before,
        center_provisional=center_provisional,
        center_after=center_after,
        raw_center_before=raw_center_before,
        raw_center_after=raw_center_after,
        center_force=force,
        write_force=write_force,
        history_increment=history_increment,
        center_prescribed_increment=center_prescribed_increment,
        write_displacement=write_displacement,
        age_center_displacement=age_center_displacement,
        write_work=write_work,
        age_work=age_work,
        center_work=center_work,
        raw_center_work=raw_center_work,
        work_split_residual=write_work + age_work - center_work,
        center_actuation_residual=(
            center_after
            - center_provisional
            - center_prescribed_increment
        ),
        write_mobility_dissipation=(
            candidate.alpha * abs(write_force) ** 2
        ),
    )


def mutual_center_step(
    history_a: np.ndarray,
    history_b: np.ndarray,
    *,
    candidate_a: RotatingWaveCandidate,
    candidate_b: RotatingWaveCandidate,
    readout_a: OrbitCenterReadout,
    readout_b: OrbitCenterReadout,
    coupling: float,
    mode: MutualCenterMode,
) -> MutualCenterStep:
    """Advance two loops under one frozen off, one-way, or reciprocal port."""

    state_a = _validate_loop(
        history_a,
        candidate=candidate_a,
        readout=readout_a,
    )
    state_b = _validate_loop(
        history_b,
        candidate=candidate_b,
        readout=readout_b,
    )
    if mode not in ("off", "a_to_b", "b_to_a", "reciprocal"):
        raise ValueError("unsupported mutual-center mode")
    strength = float(coupling)
    if not math.isfinite(strength):
        raise ValueError("coupling must be finite")
    if mode == "off" and strength != 0.0:
        raise ValueError("off mode requires zero coupling")

    center_a, _ = _loop_centers(state_a, readout=readout_a)
    center_b, _ = _loop_centers(state_b, readout=readout_b)
    provisional_a = native_fifo_step(
        state_a,
        **candidate_a.step_parameters(),
    )
    provisional_b = native_fifo_step(
        state_b,
        **candidate_b.step_parameters(),
    )
    center_a_provisional, _ = _loop_centers(
        provisional_a,
        readout=readout_a,
    )
    center_b_provisional, _ = _loop_centers(
        provisional_b,
        readout=readout_b,
    )
    separation_before = center_a - center_b
    separation_provisional = center_a_provisional - center_b_provisional
    mobility_a = candidate_a.alpha * readout_a.write_gain
    mobility_b = candidate_b.alpha * readout_b.write_gain

    force_a = 0.0j
    force_b = 0.0j
    reservoir_force_a = 0.0j
    reservoir_force_b = 0.0j
    if mode == "a_to_b":
        denominator = 2.0 + strength * mobility_b
        _validate_denominator(denominator)
        force_b = strength * (
            separation_before + separation_provisional
        ) / denominator
        reservoir_force_a = -force_b
    elif mode == "b_to_a":
        denominator = 2.0 + strength * mobility_a
        _validate_denominator(denominator)
        force_a = -strength * (
            separation_before + separation_provisional
        ) / denominator
        reservoir_force_b = -force_a
    elif mode == "reciprocal":
        denominator = 2.0 + strength * (mobility_a + mobility_b)
        _validate_denominator(denominator)
        force_a = -strength * (
            separation_before + separation_provisional
        ) / denominator
        force_b = -force_a

    loop_a = _apply_loop_write(
        state_a,
        provisional_a,
        candidate=candidate_a,
        readout=readout_a,
        center_force=force_a,
    )
    loop_b = _apply_loop_write(
        state_b,
        provisional_b,
        candidate=candidate_b,
        readout=readout_b,
        center_force=force_b,
    )
    separation_after = loop_a.center_after - loop_b.center_after
    interaction_before = 0.5 * strength * abs(separation_before) ** 2
    interaction_after = 0.5 * strength * abs(separation_after) ** 2
    reservoir_work = real_inner(
        reservoir_force_a,
        loop_a.center_after - loop_a.center_before,
    ) + real_inner(
        reservoir_force_b,
        loop_b.center_after - loop_b.center_before,
    )
    reservoir_raw_work = real_inner(
        reservoir_force_a,
        loop_a.raw_center_after - loop_a.raw_center_before,
    ) + real_inner(
        reservoir_force_b,
        loop_b.raw_center_after - loop_b.raw_center_before,
    )
    energy_change = interaction_after - interaction_before
    complete_work = (
        loop_a.write_work
        + loop_a.age_work
        + loop_b.write_work
        + loop_b.age_work
        + reservoir_work
    )
    gradient_force_a = -0.5 * strength * (
        separation_before + separation_after
    )
    gradient_force_b = -gradient_force_a
    return MutualCenterStep(
        mode=mode,
        coupling=strength,
        loop_a=loop_a,
        loop_b=loop_b,
        reservoir_force_a=reservoir_force_a,
        reservoir_force_b=reservoir_force_b,
        reservoir_work=reservoir_work,
        reservoir_raw_work=reservoir_raw_work,
        separation_before=separation_before,
        separation_provisional=separation_provisional,
        separation_after=separation_after,
        interaction_before=float(interaction_before),
        interaction_after=float(interaction_after),
        applied_force_balance_residual=force_a + force_b,
        completed_force_balance_residual=(
            force_a
            + force_b
            + reservoir_force_a
            + reservoir_force_b
        ),
        midpoint_force_residual_a=(
            force_a + reservoir_force_a - gradient_force_a
        ),
        midpoint_force_residual_b=(
            force_b + reservoir_force_b - gradient_force_b
        ),
        pair_ledger_residual=energy_change + complete_work,
        closed_pair_ledger_residual=(
            energy_change
            + loop_a.write_work
            + loop_a.age_work
            + loop_b.write_work
            + loop_b.age_work
        ),
        omitted_age_a_residual=(
            energy_change + complete_work - loop_a.age_work
        ),
        omitted_age_b_residual=(
            energy_change + complete_work - loop_b.age_work
        ),
        omitted_both_ages_residual=(
            energy_change
            + complete_work
            - loop_a.age_work
            - loop_b.age_work
        ),
        raw_center_ledger_residual=(
            energy_change
            + loop_a.raw_center_work
            + loop_b.raw_center_work
            + reservoir_raw_work
        ),
        flipped_force_a_ledger_residual=(
            energy_change
            + complete_work
            - 2.0 * (loop_a.write_work + loop_a.age_work)
        ),
    )


def _validate_denominator(denominator: float) -> None:
    if (
        not math.isfinite(denominator)
        or abs(denominator) <= 64.0 * np.finfo(float).eps
    ):
        raise ValueError("mutual-center midpoint denominator is singular")


def _rounding_gamma(operation_count: int, *, epsilon64: float) -> float:
    count = int(operation_count)
    if count < 1:
        raise ValueError("operation_count must be positive")
    product = count * epsilon64
    if not product < 1.0:
        raise ValueError("rounding gamma is undefined for n * epsilon >= 1")
    return product / (1.0 - product)


def _normal_or_zero(values: np.ndarray) -> bool:
    array = np.asarray(values, dtype=float)
    absolute = np.abs(array)
    return bool(
        np.isfinite(array).all()
        and np.all((absolute == 0.0) | (absolute >= np.finfo(float).tiny))
    )


def _weighted_sum_upper(
    history: np.ndarray,
    *,
    readout: OrbitCenterReadout,
    gamma_8h: float,
) -> tuple[float, bool]:
    state = np.asarray(history, dtype=float)
    coefficient_magnitudes = np.abs(readout.coefficients)
    history_magnitudes = np.hypot(state[:, 0], state[:, 1])
    terms = coefficient_magnitudes * history_magnitudes
    summed = math.fsum(terms)
    scaled = (1.0 + gamma_8h) * summed
    upper = math.nextafter(scaled, math.inf)
    return upper, bool(
        _normal_or_zero(coefficient_magnitudes)
        and _normal_or_zero(history_magnitudes)
        and _normal_or_zero(terms)
        and _normal_or_zero(np.asarray([summed, scaled, upper]))
    )


def _loop_rounding_metrology(
    loop: LoopCenterWrite,
    *,
    readout: OrbitCenterReadout,
) -> LoopCenterRoundingMetrology:
    epsilon64 = float(np.finfo(float).eps)
    gamma_4 = _rounding_gamma(4, epsilon64=epsilon64)
    gamma_8 = _rounding_gamma(8, epsilon64=epsilon64)
    gamma_8h = _rounding_gamma(
        8 * readout.horizon,
        epsilon64=epsilon64,
    )
    write_coefficient = complex(readout.coefficients[0])
    center_local_increment = write_coefficient * loop.history_increment
    center_local_residual = (
        center_local_increment - loop.center_prescribed_increment
    )
    provisional_zero = complex(
        float(loop.provisional_history[0, 0]),
        float(loop.provisional_history[0, 1]),
    )
    history_insertion_bound = gamma_4 * (
        abs(provisional_zero) + abs(loop.history_increment)
    )
    center_local_bound = abs(center_local_residual) + gamma_8 * (
        abs(write_coefficient) * abs(loop.history_increment)
        + abs(loop.center_prescribed_increment)
    )
    weighted_after, after_normal = _weighted_sum_upper(
        loop.history_after,
        readout=readout,
        gamma_8h=gamma_8h,
    )
    weighted_provisional, provisional_normal = _weighted_sum_upper(
        loop.provisional_history,
        readout=readout,
        gamma_8h=gamma_8h,
    )
    dot_bound = gamma_8h * (weighted_after + weighted_provisional)
    center_full_envelope = math.nextafter(
        dot_bound
        + abs(write_coefficient) * history_insertion_bound
        + center_local_bound
        + gamma_8
        * (
            abs(loop.center_after)
            + abs(loop.center_provisional)
            + abs(loop.center_prescribed_increment)
        ),
        math.inf,
    )
    normal_operands = bool(
        _normal_or_zero(loop.history_before)
        and _normal_or_zero(loop.provisional_history)
        and _normal_or_zero(loop.history_after)
        and after_normal
        and provisional_normal
        and _normal_or_zero(
            np.asarray(
                [
                    loop.center_force.real,
                    loop.center_force.imag,
                    loop.write_force.real,
                    loop.write_force.imag,
                    loop.history_increment.real,
                    loop.history_increment.imag,
                    loop.center_prescribed_increment.real,
                    loop.center_prescribed_increment.imag,
                    history_insertion_bound,
                    center_local_bound,
                    center_full_envelope,
                ]
            )
        )
    )
    return LoopCenterRoundingMetrology(
        epsilon64=epsilon64,
        gamma_4=gamma_4,
        gamma_8=gamma_8,
        gamma_8h=gamma_8h,
        center_local_increment=center_local_increment,
        center_local_residual=center_local_residual,
        center_full_residual=loop.center_actuation_residual,
        weighted_sum_after_upper=weighted_after,
        weighted_sum_provisional_upper=weighted_provisional,
        history_insertion_bound=history_insertion_bound,
        center_local_bound=center_local_bound,
        center_full_envelope=center_full_envelope,
        normal_operands=normal_operands,
    )


def mutual_center_rounding_metrology(
    step: MutualCenterStep,
    *,
    readout_a: OrbitCenterReadout,
    readout_b: OrbitCenterReadout,
) -> MutualCenterRoundingMetrology:
    """Evaluate cancellation-safe write envelopes for both loops."""

    return MutualCenterRoundingMetrology(
        loop_a=_loop_rounding_metrology(step.loop_a, readout=readout_a),
        loop_b=_loop_rounding_metrology(step.loop_b, readout=readout_b),
    )
