"""Fixed-duration constraints for an autonomous mobile-memory return."""

from dataclasses import dataclass

import numpy as np

from .fifo_reversible_carrier import carrier_map


@dataclass(frozen=True)
class TimingCycle:
    returns: np.ndarray
    closure_and_copy: np.ndarray
    head_offsets: np.ndarray
    energy_forms: np.ndarray
    rotor_energy_loss: np.ndarray


def fixed_timing_constraints(model, durations):
    """Build linear geometry and quadratic energy constraints, not a solver.

    Each column of the initial register state is an independent spatial
    coordinate, ordered as all positions, then all momenta. No duration is
    assigned to the autonomous model: a proposed cycle must match the rotor.
    """
    times = np.asarray(durations, dtype=float)
    if (
        times.ndim != 1
        or len(times) == 0
        or not np.isfinite(times).all()
        or (times <= 0).any()
    ):
        raise ValueError("flight durations must be finite and positive")

    size = len(model.weights) + 2
    basis = np.eye(2 * size)
    written_q, written_p = carrier_map(basis[:size], basis[size:])
    maps = [basis]
    for duration in times:
        flight = model.flight(written_q, written_p, duration)
        maps.append(np.concatenate(flight) @ maps[-1])
    returns = np.array(maps)
    copy_rows = returns[:-1, size - 1] - returns[:-1, size - 2]
    constraints = np.vstack([returns[-1] - basis, copy_rows])
    head_offsets = returns[:-1, 0] - basis[0]

    offsets = basis[[0, size - 1]]
    offsets[:, 1 : size - 1] -= model.weights
    metric = model.spring * offsets.T @ offsets
    masses = np.full(size, model.record_mass, dtype=float)
    masses[[0, -1]] = model.body_mass
    metric[size:, size:] = np.diag(1 / (2 * masses))
    section_energy = returns.transpose(0, 2, 1) @ metric @ returns
    energy_forms = np.diff(section_energy, axis=0)
    rotor_energy = model.clock_mass / 2 * (model.circumference / times) ** 2
    if not np.isfinite(returns).all() or not np.isfinite(rotor_energy).all():
        raise ValueError("timings exceed the numerical range of the reference")
    return TimingCycle(
        returns,
        constraints,
        head_offsets,
        energy_forms,
        np.roll(rotor_energy, 1) - rotor_energy,
    )
