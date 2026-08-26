"""Linear orbit-center readout and reciprocal source/write actuation."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .rotating_wave_stability import finite_memory_weights, native_fifo_step
from .rotating_wave_stability_gate import RotatingWaveCandidate


@dataclass(frozen=True)
class OrbitCenterReadout:
    """Exact chirality-conditioned linear readout of the loop orbit center."""

    chirality: int
    alpha: float
    horizon: int
    theta: float
    beta: complex
    weights: np.ndarray
    coefficients: np.ndarray
    write_gain: float


@dataclass(frozen=True)
class SourceWriteStep:
    """One reciprocal source/write transition and its exact work ledger."""

    history: np.ndarray
    actuator: np.ndarray
    center_before: complex
    center_provisional: complex
    center_after: complex
    raw_center_before: complex
    raw_center_after: complex
    actuator_before: complex
    actuator_after: complex
    center_force: complex
    external_force: complex
    write_force: complex
    total_slot_force: complex
    interaction_before: float
    interaction_after: float
    write_work: float
    age_work: float
    center_work: float
    raw_center_work: float
    external_work: float
    work_split_residual: float
    ledger_residual: float
    truncated_ledger_residual: float
    raw_center_ledger_residual: float
    force_balance_residual: complex
    midpoint_force_residual: complex
    center_actuation_residual: complex
    actuator_update_residual: complex
    coupling_displacement_residual: complex
    write_mobility_dissipation: float
    external_mobility_dissipation: float


def _validate_chirality(chirality: int) -> int:
    if isinstance(chirality, bool) or chirality not in (-1, 1):
        raise ValueError("chirality must be +1 or -1")
    return int(chirality)


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


def _complex_vector(vector: np.ndarray, *, name: str) -> complex:
    value = np.asarray(vector, dtype=float)
    if value.shape != (2,) or not np.isfinite(value).all():
        raise ValueError(f"{name} must be a finite vector with shape (2,)")
    return complex(float(value[0]), float(value[1]))


def complex_to_vector(value: complex) -> np.ndarray:
    """Return one complex planar coordinate as a real vector."""

    number = complex(value)
    if not math.isfinite(number.real) or not math.isfinite(number.imag):
        raise ValueError("complex coordinate must be finite")
    return np.asarray([number.real, number.imag], dtype=float)


def real_inner(left: complex, right: complex) -> float:
    """Return the Euclidean planar inner product in complex notation."""

    first = complex(left)
    second = complex(right)
    return float((first.conjugate() * second).real)


def build_orbit_center_readout(
    *,
    alpha: float,
    horizon: int,
    theta: float,
    chirality: int,
    memory_mass: float = 1.0,
) -> OrbitCenterReadout:
    """Build the exact finite-H orbit-center notch and adjoint coefficients."""

    sign = _validate_chirality(chirality)
    angle = float(theta)
    if not math.isfinite(angle) or not 0.0 < angle < math.pi:
        raise ValueError("theta must lie strictly between zero and pi")
    weights = finite_memory_weights(
        alpha=alpha,
        horizon=horizon,
        memory_mass=memory_mass,
    )
    weights = weights / np.sum(weights)
    ages = np.arange(horizon, dtype=float)
    rotating_mode = np.exp(-1j * sign * angle * ages)
    beta = complex(np.dot(weights, rotating_mode))
    denominator = 1.0 - beta
    if abs(denominator) <= 64.0 * np.finfo(float).eps:
        raise ValueError("orbit-center notch is singular at beta=1")
    coefficients = weights.astype(complex) / denominator
    coefficients[0] = (weights[0] - beta) / denominator
    write_gain = float(abs(coefficients[0]) ** 2)
    if not math.isfinite(write_gain) or write_gain <= 0.0:
        raise ValueError("write gain must be positive and finite")
    weights.setflags(write=False)
    coefficients.setflags(write=False)
    return OrbitCenterReadout(
        chirality=sign,
        alpha=float(alpha),
        horizon=int(horizon),
        theta=angle,
        beta=beta,
        weights=weights,
        coefficients=coefficients,
        write_gain=write_gain,
    )


def candidate_orbit_center_readout(
    candidate: RotatingWaveCandidate,
    *,
    chirality: int,
) -> OrbitCenterReadout:
    """Build the orbit-center readout associated with one frozen candidate."""

    return build_orbit_center_readout(
        alpha=candidate.alpha,
        horizon=candidate.horizon,
        theta=candidate.theta,
        chirality=chirality,
        memory_mass=candidate.memory_mass,
    )


def orbit_center(
    history: np.ndarray,
    *,
    readout: OrbitCenterReadout,
) -> complex:
    """Evaluate the exact linear orbit-center coordinate."""

    values = _complex_history(history)
    if values.shape != (readout.horizon,):
        raise ValueError("history horizon does not match the orbit-center readout")
    return complex(np.dot(readout.coefficients, values))


def memory_center(
    history: np.ndarray,
    *,
    readout: OrbitCenterReadout,
) -> complex:
    """Evaluate the normalized raw finite-memory center."""

    values = _complex_history(history)
    if values.shape != (readout.horizon,):
        raise ValueError("history horizon does not match the orbit-center readout")
    return complex(np.dot(readout.weights, values))


def adjoint_slot_forces(
    center_force: np.ndarray,
    *,
    readout: OrbitCenterReadout,
) -> np.ndarray:
    """Return every real slot force adjoint to the orbit-center readout."""

    forcing = _complex_vector(center_force, name="center_force")
    slot = np.conjugate(readout.coefficients) * forcing
    return np.column_stack((slot.real, slot.imag))


def reciprocal_source_write_step(
    history: np.ndarray,
    actuator: np.ndarray,
    *,
    candidate: RotatingWaveCandidate,
    readout: OrbitCenterReadout,
    coupling_strength: float,
    actuator_mobility: float | None = None,
) -> SourceWriteStep:
    """Advance one exact nonlinear L3 step under the frozen reciprocal port."""

    state = np.asarray(history, dtype=float)
    values = _complex_history(state)
    if state.shape[0] != candidate.horizon:
        raise ValueError("history horizon does not match the candidate")
    if (
        readout.horizon != candidate.horizon
        or readout.chirality not in (-1, 1)
        or not math.isclose(readout.alpha, candidate.alpha, rel_tol=0.0, abs_tol=0.0)
        or not math.isclose(readout.theta, candidate.theta, rel_tol=0.0, abs_tol=0.0)
    ):
        raise ValueError("readout does not match the candidate")
    q_before = _complex_vector(actuator, name="actuator")
    stiffness = float(coupling_strength)
    if not math.isfinite(stiffness) or stiffness < 0.0:
        raise ValueError("coupling_strength must be non-negative and finite")
    mobility = (
        readout.write_gain
        if actuator_mobility is None
        else float(actuator_mobility)
    )
    if not math.isfinite(mobility) or mobility <= 0.0:
        raise ValueError("actuator_mobility must be positive and finite")

    center_before = complex(np.dot(readout.coefficients, values))
    raw_center_before = complex(np.dot(readout.weights, values))
    provisional = native_fifo_step(state, **candidate.step_parameters())
    provisional_values = _complex_history(provisional)
    center_provisional = complex(
        np.dot(readout.coefficients, provisional_values)
    )
    if stiffness == 0.0:
        center_force = 0.0j
    else:
        denominator = 2.0 + candidate.alpha * stiffness * (
            readout.write_gain + mobility
        )
        center_force = -stiffness * (
            (center_before - q_before) + (center_provisional - q_before)
        ) / denominator
    external_force = -center_force
    write_force = readout.coefficients[0].conjugate() * center_force

    advanced = provisional.copy()
    if stiffness != 0.0:
        advanced[0] += candidate.alpha * complex_to_vector(write_force)
    q_after = q_before + candidate.alpha * mobility * external_force
    advanced_values = _complex_history(advanced)
    center_after = complex(np.dot(readout.coefficients, advanced_values))
    raw_center_after = complex(np.dot(readout.weights, advanced_values))

    write_displacement = advanced_values[0] - values[0]
    age_center_displacement = complex(
        np.dot(
            readout.coefficients[1:],
            values[:-1] - values[1:],
        )
    )
    center_displacement = center_after - center_before
    actuator_displacement = q_after - q_before
    write_work = real_inner(write_force, write_displacement)
    age_work = real_inner(center_force, age_center_displacement)
    center_work = real_inner(center_force, center_displacement)
    raw_center_work = real_inner(
        center_force,
        raw_center_after - raw_center_before,
    )
    external_work = real_inner(external_force, actuator_displacement)
    interaction_before = 0.5 * stiffness * abs(center_before - q_before) ** 2
    interaction_after = 0.5 * stiffness * abs(center_after - q_after) ** 2
    total_slot_force = complex(
        np.sum(np.conjugate(readout.coefficients)) * center_force
    )
    midpoint_force_residual = center_force + 0.5 * stiffness * (
        (center_before - q_before) + (center_after - q_after)
    )
    center_actuation_residual = (
        center_after
        - center_provisional
        - candidate.alpha * readout.write_gain * center_force
    )
    actuator_update_residual = (
        q_after
        - q_before
        - candidate.alpha * mobility * external_force
    )
    return SourceWriteStep(
        history=advanced,
        actuator=complex_to_vector(q_after),
        center_before=center_before,
        center_provisional=center_provisional,
        center_after=center_after,
        raw_center_before=raw_center_before,
        raw_center_after=raw_center_after,
        actuator_before=q_before,
        actuator_after=q_after,
        center_force=center_force,
        external_force=external_force,
        write_force=write_force,
        total_slot_force=total_slot_force,
        interaction_before=float(interaction_before),
        interaction_after=float(interaction_after),
        write_work=write_work,
        age_work=age_work,
        center_work=center_work,
        raw_center_work=raw_center_work,
        external_work=external_work,
        work_split_residual=write_work + age_work - center_work,
        ledger_residual=(
            interaction_after
            - interaction_before
            + write_work
            + age_work
            + external_work
        ),
        truncated_ledger_residual=(
            interaction_after
            - interaction_before
            + write_work
            + external_work
        ),
        raw_center_ledger_residual=(
            interaction_after
            - interaction_before
            + raw_center_work
            + external_work
        ),
        force_balance_residual=(
            total_slot_force + external_force
        ),
        midpoint_force_residual=midpoint_force_residual,
        center_actuation_residual=center_actuation_residual,
        actuator_update_residual=actuator_update_residual,
        coupling_displacement_residual=(
            center_after - center_provisional + actuator_displacement
        ),
        write_mobility_dissipation=(
            candidate.alpha * abs(write_force) ** 2
        ),
        external_mobility_dissipation=(
            candidate.alpha * mobility * abs(external_force) ** 2
        ),
    )


def readout_payload(readout: OrbitCenterReadout) -> dict[str, object]:
    """Return JSON-ready scalar metadata for one orbit-center readout."""

    return {
        "chirality": readout.chirality,
        "alpha": readout.alpha,
        "horizon": readout.horizon,
        "theta": readout.theta,
        "beta_real": readout.beta.real,
        "beta_imag": readout.beta.imag,
        "beta_abs": abs(readout.beta),
        "coefficient_sum_real": complex(np.sum(readout.coefficients)).real,
        "coefficient_sum_imag": complex(np.sum(readout.coefficients)).imag,
        "write_coefficient_real": readout.coefficients[0].real,
        "write_coefficient_imag": readout.coefficients[0].imag,
        "write_gain": readout.write_gain,
    }
