"""One analytically selected, compensated hexagon with equal register masses."""

from dataclasses import dataclass
from functools import lru_cache
from math import pi, sqrt

import numpy as np

from .fifo_compensated_hexagon import CompensatedCenterClock, _robin_modes
from .fifo_reversible_carrier import BoundaryState, carrier_map


def _center_free_seed():
    phase = complex(0.5, sqrt(3) / 2)
    a = -(1 + sqrt(5)) / 2
    tail = -1 - a
    shift = a - phase + phase**2 * tail
    relative = 2j
    sigma = -(1 + phase) * relative / (phase * shift)
    carrier = sigma * shift / 2
    newest = (-carrier + sigma * a) / phase
    second = (-newest + sigma) / phase
    q = np.array([1, phase**-1, phase**-2, -1, -1])
    p = np.array([relative + carrier, newest, second, -carrier, carrier])
    return a, tail, q, p


def _lift_covectors(rows):
    return np.c_[rows[:, 0] / 2, rows[:, 1:], rows[:, 0] / 2]


@lru_cache(maxsize=1)
def _center_free_modes():
    a, tail, q, p = _center_free_seed()
    basis = np.array([[1, -1 / 3, -1 / 3, -1 / 3], [0, 1 - tail, tail - a, a - 1]])
    inverse = np.array([0.5, 1, 1, 1])
    basis /= np.sqrt(np.sum(inverse * basis**2, axis=1))[:, None]
    coords = basis @ np.r_[0, q[0], q[1:3]]
    impulses = (basis * inverse) @ np.r_[p[0] - p[-1], p[-1], p[1:3]]
    robin = np.linalg.solve(
        np.c_[coords.real, coords.imag].T, np.c_[impulses.real, impulses.imag].T
    ).T
    lifted = _lift_covectors(basis)
    detuned = _robin_modes((robin + robin.T) / 2, lifted)
    return (
        (np.array([1, 0, 0, 0, -1]), 1),
        (np.array([0, a, 1, tail, 0]), 6),
        *detuned,
    )


@dataclass(frozen=True)
class CenterFreeClock(CompensatedCenterClock):
    """The preserved mode acts entirely on the records, not on the pair center."""

    @property
    def record_mass(self):
        return self.body_mass

    def _modal_data(self, row_count):
        if row_count != 5:
            raise ValueError("the center-free reference has three history rows")
        modes = tuple(
            (normal, ratio * self.frequency) for normal, ratio in _center_free_modes()
        )
        return np.full(5, 1 / self.body_mass), modes


def prepared_center_free_hexagon(radius=0.04):
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("hexagon radius must be finite and positive")
    model = CenterFreeClock(spring=0.5)
    _, _, q, p = _center_free_seed()
    return model, BoundaryState(
        radius * np.c_[q.real, q.imag], radius * np.c_[p.real, p.imag], 3 / pi
    )


def planar_tangent(model, prepared):
    """Co-rotating derivative on the energy section, including the clock term."""
    duration = model.clock_mass * model.circumference / prepared.clock_momentum
    basis = np.eye(10)
    written = carrier_map(basis[:5], basis[5:])
    gate = np.concatenate(written)
    fixed = np.concatenate(model.flight(*written, duration))
    inverse, modes = model._modal_data(5)
    stiffness = sum(
        frequency**2 * np.outer(normal, normal) / (normal @ (inverse * normal))
        for normal, frequency in modes
    )
    phase = np.vstack((prepared.position, prepared.momentum))
    vector_field = np.vstack(
        (inverse[:, None] * prepared.momentum, -stiffness @ prepared.position)
    )
    after_write = gate @ phase
    energy_gradient = gate.T @ np.vstack(
        (stiffness @ after_write[:5], inverse[:, None] * after_write[5:])
    )
    clock_energy = prepared.clock_momentum**2 / (2 * model.clock_mass)
    factor = duration / (2 * clock_energy)
    inverse_rotation = np.array([[0.5, sqrt(3) / 2], [-sqrt(3) / 2, 0.5]])
    return np.kron(fixed, inverse_rotation) + factor * np.outer(
        vector_field.ravel(), energy_gradient.ravel()
    )
