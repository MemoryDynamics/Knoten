"""One return of a prepared classical rotor/record-carrier reference."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, sin, sqrt

import numpy as np

from .fifo_reversible_carrier import BoundaryState, write_boundary


@dataclass(frozen=True)
class CarrierClock:
    body_mass: float = 1.0
    spring: float = 1.0
    clock_mass: float = 1.0
    circumference: float = 1.0

    def __post_init__(self):
        values = (self.body_mass, self.spring, self.clock_mass, self.circumference)
        if min(values) <= 0 or not np.isfinite(values).all():
            raise ValueError(
                "masses, stiffness and circumference must be finite and positive"
            )

    @property
    def frequency(self):
        return sqrt(2 * self.spring / self.body_mass)

    def internal_energy(self, q, p):
        displacement = q[0] - q[-1]
        kinetic = (p[0] @ p[0] + p[-1] @ p[-1]) / (2 * self.body_mass)
        return kinetic + self.spring * (displacement @ displacement) / 2

    def flight(self, position, momentum, duration):
        q, p = position.copy(), momentum.copy()
        # The register rows between head and carrier do not stream.
        center = (q[0] + q[-1]) / 2
        displacement = q[0] - q[-1]
        total, difference = p[0] + p[-1], p[0] - p[-1]
        mw = self.body_mass * self.frequency
        c, s = cos(self.frequency * duration), sin(self.frequency * duration)
        moved_center = center + total * duration / (2 * self.body_mass)
        moved_displacement = c * displacement + s * difference / mw
        moved_difference = c * difference - mw * s * displacement
        q[0] = moved_center + moved_displacement / 2
        q[-1] = moved_center - moved_displacement / 2
        p[0] = (total + moved_difference) / 2
        p[-1] = (total - moved_difference) / 2
        return q, p


@dataclass(frozen=True)
class MemoryCenterClock(CarrierClock):
    """Attach both bodies to the same point read from the FIFO."""

    weights: tuple[float, ...] = (0.5, 0.5, 0.0)

    def __post_init__(self):
        super().__post_init__()
        w = np.asarray(self.weights, dtype=float)
        if (
            w.ndim != 1
            or len(w) == 0
            or not np.isfinite(w).all()
            or (w < 0).any()
            or not np.isclose(w.sum(), 1, rtol=0, atol=2e-15)
        ):
            raise ValueError("memory weights must be nonnegative and sum to one")

    def _center(self, position):
        if len(self.weights) != len(position) - 2:
            raise ValueError("one weight is required for each memory row")
        return np.asarray(self.weights) @ position[1:-1]

    def internal_energy(self, q, p):
        offsets = q[[0, -1]] - self._center(q)
        kinetic = np.square(p[[0, -1]]).sum() / (2 * self.body_mass)
        return kinetic + self.spring * np.square(offsets).sum()

    def flight(self, position, momentum, duration):
        q, p = position.copy(), momentum.copy()
        center = self._center(q)
        bodies = [0, -1]
        offsets = q[bodies] - center
        before = p[bodies]
        mw = self.body_mass * self.frequency
        c, s = cos(self.frequency * duration), sin(self.frequency * duration)
        q[bodies] = center + c * offsets + s * before / mw
        p[bodies] = c * before - mw * s * offsets
        # The frozen records still receive the reciprocal momentum.
        p[1:-1] += np.asarray(self.weights)[:, None] * (before - p[bodies]).sum(axis=0)
        return q, p


def clock_return(incoming, model):
    """Resolve the seam and advance to the next arrival without clock resets."""
    event = write_boundary(incoming, model.internal_energy, clock_mass=model.clock_mass)
    outgoing = event.state
    clock = outgoing.clock_momentum
    duration = model.clock_mass * model.circumference / abs(clock)
    q, p = model.flight(outgoing.position, outgoing.momentum, duration)

    # Both ends of the cut strip are the same seam of the circular clock.
    arrival = BoundaryState(q, p, clock, -1 if clock > 0 else 1)
    return arrival, event, duration
