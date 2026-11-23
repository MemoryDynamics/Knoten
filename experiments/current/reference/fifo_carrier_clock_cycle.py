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


@dataclass(frozen=True)
class MobileMemoryClock(MemoryCenterClock):
    """Give each record an independent kinetic term with a common mass."""

    record_mass: float = 1.0

    def __post_init__(self):
        super().__post_init__()
        if not np.isfinite(self.record_mass) or self.record_mass <= 0:
            raise ValueError("record mass must be finite and positive")

    @property
    def balance_frequency(self):
        return self.frequency * sqrt(
            1 + 2 * self.body_mass * np.square(self.weights).sum() / self.record_mass
        )

    def internal_energy(self, q, p):
        return super().internal_energy(q, p) + np.square(p[1:-1]).sum() / (
            2 * self.record_mass
        )

    def flight(self, position, momentum, duration):
        if len(self.weights) != len(position) - 2:
            raise ValueError("one weight is required for each memory row")
        inverse_mass = np.full(len(position), 1 / self.record_mass)
        inverse_mass[[0, -1]] = 1 / self.body_mass
        velocity = inverse_mass[:, None] * momentum
        q = position + duration * velocity
        v = velocity.copy()
        relative = np.zeros(len(position))
        relative[[0, -1]] = (1, -1)
        balance = np.r_[0.5, -np.asarray(self.weights), 0.5]

        # The two mass-orthogonal oscillators replace their free-flight pieces.
        for normal, frequency in (
            (relative, self.frequency),
            (balance, self.balance_frequency),
        ):
            direction = inverse_mass * normal
            direction /= normal @ direction
            coordinate, speed = normal @ position, normal @ velocity
            phase = frequency * duration
            c, s = cos(phase), sin(phase)
            q += direction[:, None] * (
                (c - 1) * coordinate + (s / frequency - duration) * speed
            )
            v += direction[:, None] * ((c - 1) * speed - frequency * s * coordinate)
        return q, v / inverse_mass[:, None]


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
