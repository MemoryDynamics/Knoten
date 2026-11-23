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


def oscillator_write_split(state, model, *, write=True):
    """One fixed-step split; the filled FIFO write is booked, not powered here."""
    x, memory = np.asarray(state.x, dtype=float), np.asarray(state.memory, dtype=float)
    a, p = state.amplitude, state.momentum
    if (
        x.ndim != 1
        or memory.ndim != 2
        or memory.shape[1:] != x.shape
        or not len(memory)
    ):
        raise ValueError(
            "a finite filled memory and a matching vector head are required"
        )
    if not np.isfinite([a, p]).all():
        raise ValueError("oscillator state must be finite")
    weights = exponential_memory_weights(1 - model.retention, len(memory))
    base = dict(sigma=model.base_sigma, amplitude=model.base_amplitude)
    modulation = dict(
        sigma=model.modulation_sigma, amplitude=model.modulation_amplitude
    )

    def components(head, history):
        return (
            gaussian_potential(head, history, weights, **base),
            gaussian_potential(head, history, weights, **modulation),
        )

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
