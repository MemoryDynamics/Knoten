"""Fixed two-phase compensation reference, without an orbit or parameter search."""

from dataclasses import dataclass
from functools import lru_cache
from math import pi, sqrt, tan

import numpy as np
from scipy.optimize import brentq

from .fifo_carrier_clock_cycle import CarrierClock, _modal_flight
from .fifo_reversible_carrier import BoundaryState


@lru_cache(maxsize=1)
def _compensated_modes():
    symmetric = np.array([1 / 3, 1, -8 / 3, 1, 1 / 3]) / sqrt(385 / 72)
    antisymmetric = np.array([0, 1, 0, -1, 0]) / sqrt(9 / 8)
    robin = (
        np.array([[15 * sqrt(3), 5 * sqrt(1155)], [5 * sqrt(1155), -77 * sqrt(3)]])
        / 224
    )
    values, directions = np.linalg.eigh(robin)
    basis = np.vstack((antisymmetric, symmetric))
    result = []
    for target, direction in zip(values, directions.T, strict=True):
        # Use just the first branch of the requested sign, away from the pole.
        lo, hi = (3 + 1e-8, 6) if target < 0 else (0, 3 - 1e-8)
        ratio = brentq(lambda r: r * tan(r * pi / 6) - target, lo, hi, xtol=2e-14)
        result.append((direction @ basis, ratio))
    return tuple(result)


@dataclass(frozen=True)
class CompensatedCenterClock(CarrierClock):
    """Two distinct detuned modes with one full-turn mode and no free internal drift."""

    @property
    def record_mass(self):
        return (16 / 9) * self.body_mass

    def _modal_data(self, row_count):
        if row_count != 5:
            raise ValueError("the compensated reference has three history rows")
        inverse = np.array([1, 9 / 16, 9 / 16, 9 / 16, 1]) / self.body_mass
        modes = (
            (np.array([1, 0, 0, 0, -1]), 1),
            (np.array([-9 / 8, 1, 1 / 4, 1, -9 / 8]), 6),
            *_compensated_modes(),
        )
        return inverse, tuple(
            (normal, ratio * self.frequency) for normal, ratio in modes
        )

    def internal_energy(self, q, p):
        inverse, modes = self._modal_data(len(q))
        energy = (inverse @ np.square(p).sum(axis=1)) / 2
        for normal, frequency in modes:
            coordinate = normal @ q
            energy += (
                frequency**2
                * (coordinate @ coordinate)
                / (2 * (normal @ (inverse * normal)))
            )
        return energy

    def flight(self, position, momentum, duration):
        inverse, modes = self._modal_data(len(position))
        return _modal_flight(position, momentum, duration, inverse, modes)


def prepared_compensated_hexagon(radius=1):
    """Return the fixed dimensionless model and its analytical rotating seed."""
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("hexagon radius must be finite and positive")
    model = CompensatedCenterClock(spring=0.5)
    angle = pi / 3
    phase = complex(0.5, sqrt(3) / 2)
    relative = 2j * radius
    k = 3 * phase / 4
    sigma = (1 + phase) * relative / (-9 / 4 - phase * k)
    carrier = sigma * k / 2
    newest = (-carrier + sigma) / phase
    second = (-newest + sigma / 4) / phase
    positions = np.r_[radius, radius * phase ** -np.arange(1, 4), -radius]
    momenta = np.r_[relative + carrier, newest, second, -carrier, carrier]
    q = np.c_[positions.real, positions.imag]
    p = np.c_[momenta.real, momenta.imag]
    return model, BoundaryState(q, p, model.clock_mass * model.circumference / angle)
