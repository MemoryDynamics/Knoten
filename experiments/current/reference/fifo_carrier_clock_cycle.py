"""One return of a prepared classical rotor/record-carrier reference."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin, sqrt

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
        relative = np.zeros(len(position))
        relative[[0, -1]] = (1, -1)
        balance = np.r_[0.5, -np.asarray(self.weights), 0.5]
        modes = (relative, self.frequency), (balance, self.balance_frequency)
        return _modal_flight(position, momentum, duration, inverse_mass, modes)


def _modal_flight(position, momentum, duration, inverse_mass, modes):
    velocity = inverse_mass[:, None] * momentum
    q = position + duration * velocity
    v = velocity.copy()
    # Each mass-orthogonal oscillator replaces its free-flight contribution.
    for normal, frequency in modes:
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


@dataclass(frozen=True)
class TwoCenterClock(CarrierClock):
    """Three mobile history rows read by two symmetric convex profiles."""

    record_mass: float = 3 / 572
    profile_offset: float = sqrt(27 / 572)

    def __post_init__(self):
        super().__post_init__()
        if not np.isfinite(self.record_mass) or self.record_mass <= 0:
            raise ValueError("record mass must be finite and positive")
        if not 0 < self.profile_offset <= 0.25:
            raise ValueError("profile offset must give two distinct convex profiles")

    @property
    def balance_frequencies(self):
        ratio = self.body_mass / self.record_mass
        return (
            self.frequency * sqrt(1 + 0.75 * ratio),
            self.frequency * 2 * self.profile_offset * sqrt(ratio),
        )

    def internal_energy(self, q, p):
        if len(q) != 5:
            raise ValueError(
                "the symmetric two-center reference has three history rows"
            )
        relative = q[0] - q[-1]
        symmetric = (q[0] + q[-1]) / 2 - (q[1] + 2 * q[2] + q[3]) / 4
        antisymmetric = self.profile_offset * (q[1] - q[3])
        kinetic = np.square(p[[0, -1]]).sum() / (2 * self.body_mass)
        kinetic += np.square(p[1:-1]).sum() / (2 * self.record_mass)
        return kinetic + self.spring * (
            (relative @ relative) / 2
            + 2 * (symmetric @ symmetric + antisymmetric @ antisymmetric)
        )

    def _modes(self):
        symmetric, antisymmetric = self.balance_frequencies
        return (
            (np.array([1, 0, 0, 0, -1]), self.frequency),
            (np.array([0.5, -0.25, -0.5, -0.25, 0.5]), symmetric),
            (np.array([0, 1, 0, -1, 0]), antisymmetric),
        )

    def _inverse_masses(self):
        inverse_mass = np.full(5, 1 / self.record_mass)
        inverse_mass[[0, -1]] = 1 / self.body_mass
        return inverse_mass

    def flight(self, position, momentum, duration):
        if len(position) != 5:
            raise ValueError(
                "the symmetric two-center reference has three history rows"
            )
        return _modal_flight(
            position, momentum, duration, self._inverse_masses(), self._modes()
        )


@dataclass(frozen=True)
class RestoredCenterClock(TwoCenterClock):
    """Bind the last internal free coordinate without pinning translation."""

    restoring_ratio: float = 6.0

    def __post_init__(self):
        super().__post_init__()
        if not np.isfinite(self.restoring_ratio) or self.restoring_ratio <= 0:
            raise ValueError("restoring frequency ratio must be finite and positive")

    def _restoring_mode(self):
        ratio = self.record_mass / self.body_mass
        normal = np.array([-0.5, 1 + ratio, -1 - 2 * ratio, 1 + ratio, -0.5])
        return normal, self.restoring_ratio * self.frequency

    def _modes(self):
        return (*super()._modes(), self._restoring_mode())

    def internal_energy(self, q, p):
        base = super().internal_energy(q, p)
        normal, frequency = self._restoring_mode()
        coordinate = normal @ q
        norm = normal @ (self._inverse_masses() * normal)
        return base + (frequency**2 / (2 * norm)) * (coordinate @ coordinate)


def prepared_hexagon(radius=1.0):
    """Return the normalized two-center model and its exact planar seed."""
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("hexagon radius must be finite and positive")
    model = TwoCenterClock(spring=0.5)
    angle = pi / 3
    rotation = complex(cos(angle), sin(angle))
    history = rotation ** -np.arange(1, 4)
    pair = 2j * model.body_mass * model.frequency * radius / rotation
    carrier = (1 - rotation) * pair / 2
    positions = np.r_[radius, radius * history, -radius]
    momenta = np.r_[pair - carrier, carrier * history, carrier]
    q = np.column_stack((positions.real, positions.imag))
    p = np.column_stack((momenta.real, momenta.imag))
    clock = model.clock_mass * model.circumference * model.frequency / angle
    return model, BoundaryState(q, p, clock)


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
