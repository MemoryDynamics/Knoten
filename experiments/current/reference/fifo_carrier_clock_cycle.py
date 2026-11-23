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
        values = tuple(vars(self).values())
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


def clock_return(incoming, model):
    """Resolve the seam and advance to the next arrival without clock resets."""
    event = write_boundary(incoming, model.internal_energy, clock_mass=model.clock_mass)
    outgoing = event.state
    clock = outgoing.clock_momentum
    duration = model.clock_mass * model.circumference / abs(clock)
    q, p = outgoing.position.copy(), outgoing.momentum.copy()

    # The register rows between head and carrier do not stream in this reference.
    center = (q[0] + q[-1]) / 2
    displacement = q[0] - q[-1]
    total, difference = p[0] + p[-1], p[0] - p[-1]
    mw = model.body_mass * model.frequency
    c, s = cos(model.frequency * duration), sin(model.frequency * duration)
    moved_center = center + total * duration / (2 * model.body_mass)
    moved_displacement = c * displacement + s * difference / mw
    moved_difference = c * difference - mw * s * displacement
    q[0] = moved_center + moved_displacement / 2
    q[-1] = moved_center - moved_displacement / 2
    p[0] = (total + moved_difference) / 2
    p[-1] = (total - moved_difference) / 2

    # Both ends of the cut strip are the same seam of the circular clock.
    arrival = BoundaryState(q, p, clock, -1 if clock > 0 else 1)
    return arrival, event, duration
