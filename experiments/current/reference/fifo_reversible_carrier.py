"""Conditional Hamiltonian write event with a retained FIFO tail."""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import copysign, sqrt

import numpy as np


def carrier_map(position, momentum, *, reverse=False):
    """Cotangent lift on rows [head, newest ... oldest, carrier]."""
    q, p = np.asarray(position, dtype=float), np.asarray(momentum, dtype=float)
    if q.ndim != 2 or q.shape != p.shape or q.shape[0] < 3 or not q.shape[1]:
        raise ValueError("head, nonempty memory and carrier need matching q and p")
    if not np.isfinite(q).all() or not np.isfinite(p).all():
        raise ValueError("register coordinates must be finite")
    out_q, out_p = q.copy(), p.copy()
    if reverse:
        out_q[1:-2] = q[2:-1]
        out_q[-2] = q[-1]
        out_q[-1] = q[1] - q[0] + q[-1]
        out_p[0] = p[0] + p[1]
        out_p[1:-2] = p[2:-1]
        out_p[-2] = p[-1] - p[1]
        out_p[-1] = p[1]
    else:
        out_q[1] = q[0] + q[-1] - q[-2]
        out_q[2:-1] = q[1:-2]
        out_q[-1] = q[-2]
        out_p[0] = p[0] - p[-1]
        out_p[1] = p[-1]
        out_p[2:-1] = p[1:-2]
        out_p[-1] = p[-2] + p[-1]
    return out_q, out_p


@dataclass(frozen=True)
class BoundaryState:
    position: np.ndarray
    momentum: np.ndarray
    clock_momentum: float
    side: int = -1


@dataclass(frozen=True)
class BoundaryEvent:
    state: BoundaryState
    crossed: bool
    energy_gap: float


def write_boundary(state, internal_energy, *, clock_mass=1.0):
    """Transmit or reflect an incoming clock at a prescribed interface.

    The internal Hamiltonian on each side is given in that side's register
    coordinates. No clock reset, carrier preparation or finite-time flow
    is supplied by this boundary rule.
    """
    clock = state.clock_momentum
    if not np.isfinite([clock, clock_mass]).all() or clock_mass <= 0:
        raise ValueError("finite clock momentum and a positive mass are required")
    if state.side not in (-1, 1) or state.side * clock >= 0:
        raise ValueError("the clock must be incoming on the declared side")
    q, p = carrier_map(state.position, state.momentum, reverse=(state.side == 1))
    gap = internal_energy(q, p) - internal_energy(state.position, state.momentum)
    remaining = clock**2 / (2 * clock_mass) - gap
    if not np.isfinite(remaining):
        raise ValueError("the interface requires finite energies")
    if remaining == 0:
        raise ValueError("grazing threshold is not resolved by this reference")
    if remaining < 0:
        return BoundaryEvent(replace(state, clock_momentum=-clock), False, gap)
    new_clock = copysign(sqrt(2 * clock_mass * remaining), clock)
    return BoundaryEvent(BoundaryState(q, p, new_clock, -state.side), True, gap)
