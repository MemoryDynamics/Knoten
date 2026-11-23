"""Deterministic scalar FIFO reference with reciprocal kernel modulation."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, sin, sqrt

import numpy as np

from emergenz_knoten.kernels import (
    exponential_memory_weights,
    gaussian_gradient,
    gaussian_potential,
)


@dataclass(frozen=True)
class KernelOscillator:
    base_amplitude: float = 1.0
    base_sigma: float = 1.0
    modulation_amplitude: float = 1.0
    modulation_sigma: float = 1.0
    inertia: float = 1.0
    stiffness: float = 1.0
    retention: float = 0.6
    mobility: float = 1.0
    dt: float = 0.1

    def __post_init__(self):
        if not np.all(np.isfinite(tuple(vars(self).values()))):
            raise ValueError("reference parameters must be finite")
        if not 0 <= self.retention < 1:
            raise ValueError("retention must be in [0, 1)")
        if (
            min(
                self.base_sigma,
                self.modulation_sigma,
                self.inertia,
                self.stiffness,
                self.dt,
            )
            <= 0
        ):
            raise ValueError("widths, oscillator parameters and dt must be positive")
        if self.mobility < 0:
            raise ValueError("mobility must be nonnegative")

    def oscillator_energy(self, amplitude, momentum):
        return momentum**2 / (2 * self.inertia) + self.stiffness * amplitude**2 / 2


@dataclass(frozen=True)
class KernelState:
    x: np.ndarray
    memory: np.ndarray
    amplitude: float
    momentum: float


@dataclass(frozen=True)
class KernelLedger:
    initial_energy: float
    final_energy: float
    motion: float
    modulation: float
    oscillator: float
    write: float

    @property
    def reciprocal_residual(self):
        return self.modulation + self.oscillator

    @property
    def net_residual(self):
        return self.final_energy - self.initial_energy - self.motion - self.write


def _read_setup(state, model):
    x, memory = np.asarray(state.x, dtype=float), np.asarray(state.memory, dtype=float)
    if (
        x.ndim != 1
        or memory.ndim != 2
        or memory.shape[1:] != x.shape
        or not len(memory)
    ):
        raise ValueError(
            "a finite filled memory and a matching vector head are required"
        )
    if not np.isfinite([state.amplitude, state.momentum]).all():
        raise ValueError("oscillator state must be finite")
    weights = exponential_memory_weights(1 - model.retention, len(memory))
    base = dict(sigma=model.base_sigma, amplitude=model.base_amplitude)
    modulation = dict(
        sigma=model.modulation_sigma, amplitude=model.modulation_amplitude
    )

    return x, memory, weights, base, modulation


def _components(head, history, weights, base, modulation):
    return (
        gaussian_potential(head, history, weights, **base),
        gaussian_potential(head, history, weights, **modulation),
    )


def oscillator_write_split(state, model, *, write=True):
    """One fixed-step split; the filled FIFO write is booked, not powered here."""
    x, memory, weights, base, modulation = _read_setup(state, model)
    a, p = state.amplitude, state.momentum

    def components(head, history):
        return _components(head, history, weights, base, modulation)

    oscillator_energy = model.oscillator_energy
    base0, mod0 = components(x, memory)
    energy0 = base0 + a * mod0 + oscillator_energy(a, p)
    step = model.mobility * model.dt
    lipschitz = weights.sum() * (
        abs(model.base_amplitude) / model.base_sigma**2
        + abs(a * model.modulation_amplitude) / model.modulation_sigma**2
    )
    if step * lipschitz >= 2:
        raise ValueError("fixed motion step falls outside the certified descent regime")
    gradient = gaussian_gradient(x, memory, weights, **base)
    gradient += a * gaussian_gradient(x, memory, weights, **modulation)
    x1 = x - step * gradient
    base1, mod1 = components(x1, memory)
    motion = base1 - base0 + a * (mod1 - mod0)

    omega = sqrt(model.stiffness / model.inertia)
    center = -mod1 / model.stiffness
    c, s = cos(omega * model.dt), sin(omega * model.dt)
    a1 = center + c * (a - center) + s * p / (model.inertia * omega)
    p1 = c * p - model.inertia * omega * s * (a - center)
    modulation_work = (a1 - a) * mod1
    oscillator = oscillator_energy(a1, p1) - oscillator_energy(a, p)

    memory1 = np.vstack((x1, memory[:-1])) if write else memory
    base2, mod2 = components(x1, memory1)
    write_work = base2 - base1 + a1 * (mod2 - mod1)
    energy1 = base2 + a1 * mod2 + oscillator_energy(a1, p1)
    return KernelState(x1, memory1, a1, p1), KernelLedger(
        energy0, energy1, motion, modulation_work, oscillator, write_work
    )


@dataclass(frozen=True)
class MatchedWriteLedger:
    minimum_change: float
    excitation_before: float
    excitation_after: float
    read_change: float
    oscillator_change: float

    @property
    def energy_residual(self):
        return self.read_change + self.oscillator_change


def energy_matched_fifo_write(state, model, *, phase_shift=0.0, birth_phase=None):
    """Write at fixed x by transferring energy between the read and oscillator terms.

    A positive excitation is moved to the new shell at the old phase plus
    phase_shift. Launch from zero excitation needs an explicit birth_phase.
    No write is performed if the new shell is energetically inaccessible.
    """
    x, old, weights, base, modulation = _read_setup(state, model)
    if not np.isfinite(phase_shift) or (
        birth_phase is not None and not np.isfinite(birth_phase)
    ):
        raise ValueError("phase inputs must be finite")
    new = np.vstack((x, old[:-1]))
    u0, u1 = _components(x, old, weights, base, modulation)
    v0, v1 = _components(x, new, weights, base, modulation)
    stiffness, inertia = model.stiffness, model.inertia
    old_center, new_center = -u1 / stiffness, -v1 / stiffness
    scale_a, scale_p = sqrt(stiffness), sqrt(inertia)
    za = scale_a * (state.amplitude - old_center)
    zp = state.momentum / scale_p
    excitation = (za**2 + zp**2) / 2
    change = (v0 - u0) - (v1 - u1) * (v1 + u1) / (2 * stiffness)
    available = excitation - change

    if available < 0:
        raise ValueError("new FIFO minimum exceeds the available energy")
    if available == 0:
        za1, zp1 = 0.0, 0.0
    elif excitation == 0:
        if birth_phase is None:
            raise ValueError("positive excitation from zero requires a declared phase")
        radius = sqrt(2 * available)
        angle = birth_phase + phase_shift
        za1, zp1 = radius * cos(angle), radius * sin(angle)
    else:
        scale = sqrt(available / excitation)
        c, s = cos(phase_shift), sin(phase_shift)
        za1, zp1 = scale * (c * za - s * zp), scale * (s * za + c * zp)

    a1, p1 = new_center + za1 / scale_a, scale_p * zp1
    read_change = v0 - u0 + a1 * v1 - state.amplitude * u1
    oscillator = model.oscillator_energy
    oscillator_change = oscillator(a1, p1) - oscillator(state.amplitude, state.momentum)
    return KernelState(x, new, a1, p1), MatchedWriteLedger(
        change, excitation, (za1**2 + zp1**2) / 2, read_change, oscillator_change
    )


def energy_closed_step(state, model, *, phase_shift=0.0, birth_phase=None):
    """Combine passive motion, reciprocal modulation, and a paid FIFO write."""
    moved, before_write = oscillator_write_split(state, model, write=False)
    written, paid = energy_matched_fifo_write(
        moved, model, phase_shift=phase_shift, birth_phase=birth_phase
    )
    return written, before_write, paid
