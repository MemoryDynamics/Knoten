"""Rigid full-memory pair energies and forces for quasistatic discrimination.

The functions here translate complete retained memory clouds as rigid source
densities.  They do not advance the canonical knot process and do not imply
that a dynamic mediator has equilibrated instantaneously.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

import numpy as np

from .state import FiniteMemoryState, place_finite_memory_state


RadialLaw = Callable[[np.ndarray], np.ndarray]


@dataclass(frozen=True)
class RigidPairInteraction:
    """Energy and equal/opposite force of two rigid retained-memory clouds."""

    separation: np.ndarray
    energy: float
    force_on_first: np.ndarray
    force_on_second: np.ndarray
    radial_force_on_second: float
    first_mass: float
    second_mass: float


@dataclass(frozen=True)
class VisibleMemoryReciprocalInteraction:
    """Symmetric visible-to-foreign-memory energy and reciprocal forces."""

    separation: np.ndarray
    energy: float
    force_on_first: np.ndarray
    force_on_second: np.ndarray
    radial_force_on_second: float


def three_scale_radial_potential(
    radii: np.ndarray | float,
    *,
    sigma_rep: float,
    sigma_att: float,
    sigma_comp: float,
    amplitude_rep: float,
    amplitude_att: float,
    amplitude_comp: float,
) -> np.ndarray:
    """Return ``A_rep*G_rep-A_att*G_att+A_comp*G_comp``."""

    radius = np.asarray(radii, dtype=float)
    parameters = (
        ("sigma_rep", sigma_rep),
        ("sigma_att", sigma_att),
        ("sigma_comp", sigma_comp),
    )
    if not np.isfinite(radius).all() or np.any(radius < 0.0):
        raise ValueError("radii must be finite and non-negative")
    for name, value in parameters:
        if not np.isfinite(value) or value <= 0.0:
            raise ValueError(f"{name} must be positive and finite")
    amplitudes = (amplitude_rep, amplitude_att, amplitude_comp)
    if not all(np.isfinite(value) for value in amplitudes):
        raise ValueError("amplitudes must be finite")
    rep = amplitude_rep * np.exp(-0.5 * np.square(radius / sigma_rep))
    att = amplitude_att * np.exp(-0.5 * np.square(radius / sigma_att))
    comp = amplitude_comp * np.exp(-0.5 * np.square(radius / sigma_comp))
    return np.asarray(rep - att + comp, dtype=float)


def three_scale_radial_derivative(
    radii: np.ndarray | float,
    *,
    sigma_rep: float,
    sigma_att: float,
    sigma_comp: float,
    amplitude_rep: float,
    amplitude_att: float,
    amplitude_comp: float,
) -> np.ndarray:
    """Return the exact radial derivative of :func:`three_scale_radial_potential`."""

    radius = np.asarray(radii, dtype=float)
    potential_parameters = {
        "sigma_rep": sigma_rep,
        "sigma_att": sigma_att,
        "sigma_comp": sigma_comp,
        "amplitude_rep": amplitude_rep,
        "amplitude_att": amplitude_att,
        "amplitude_comp": amplitude_comp,
    }
    three_scale_radial_potential(radius, **potential_parameters)
    rep = (
        -amplitude_rep
        * radius
        * np.exp(-0.5 * np.square(radius / sigma_rep))
        / sigma_rep**2
    )
    att = (
        amplitude_att
        * radius
        * np.exp(-0.5 * np.square(radius / sigma_att))
        / sigma_att**2
    )
    comp = (
        -amplitude_comp
        * radius
        * np.exp(-0.5 * np.square(radius / sigma_comp))
        / sigma_comp**2
    )
    return np.asarray(rep + att + comp, dtype=float)


def rigid_full_memory_pair_interaction(
    first_state: FiniteMemoryState,
    second_state: FiniteMemoryState,
    separation: Iterable[float],
    *,
    radial_pair_energy: RadialLaw,
    radial_pair_energy_derivative: RadialLaw,
    second_rotation: Iterable[Iterable[float]] | None = None,
) -> RigidPairInteraction:
    """Evaluate one translational pair law on both complete memory clouds.

    ``separation`` points from the first cloud centre to the second.  The
    visible coordinates are placed with their clouds but do not receive a
    special weight: this is a source-density interaction between retained
    memories, not a continuation step of ``x``.
    """

    if first_state.dim != second_state.dim:
        raise ValueError("states must share one ambient dimension")
    separation_vector = np.asarray(separation, dtype=float)
    if (
        separation_vector.shape != (first_state.dim,)
        or not np.isfinite(separation_vector).all()
    ):
        raise ValueError("separation must be a finite vector matching state dimension")
    separation_norm = float(np.linalg.norm(separation_vector))
    if separation_norm <= 0.0:
        raise ValueError("separation must be non-zero")
    first = place_finite_memory_state(first_state, -0.5 * separation_vector)
    second = place_finite_memory_state(
        second_state,
        0.5 * separation_vector,
        rotation=second_rotation,
    )
    displacement = second.memory[None, :, :] - first.memory[:, None, :]
    radii = np.linalg.norm(displacement, axis=2)
    if np.any(radii <= 0.0):
        raise ValueError("pair law is undefined for coincident retained points")
    weights = first.weights[:, None] * second.weights[None, :]
    energy_values = np.asarray(radial_pair_energy(radii), dtype=float)
    derivative_values = np.asarray(radial_pair_energy_derivative(radii), dtype=float)
    if energy_values.shape != radii.shape or derivative_values.shape != radii.shape:
        raise ValueError("radial laws must preserve the input radius shape")
    if not np.isfinite(energy_values).all() or not np.isfinite(derivative_values).all():
        raise ValueError("radial laws returned non-finite values")
    force_terms = (
        (weights * derivative_values / radii)[:, :, None] * displacement
    )
    force_on_first = np.sum(force_terms, axis=(0, 1))
    force_on_second = -np.sum(force_terms, axis=(0, 1))
    axis = separation_vector / separation_norm
    first_mass = float(np.sum(first.weights))
    second_mass = float(np.sum(second.weights))
    return RigidPairInteraction(
        separation=separation_vector.copy(),
        energy=float(np.sum(weights * energy_values)),
        force_on_first=np.asarray(force_on_first, dtype=float),
        force_on_second=np.asarray(force_on_second, dtype=float),
        radial_force_on_second=float(np.dot(force_on_second, axis)),
        first_mass=first_mass,
        second_mass=second_mass,
    )


def reciprocal_visible_memory_pair_interaction(
    first_state: FiniteMemoryState,
    second_state: FiniteMemoryState,
    separation: Iterable[float],
    *,
    radial_pair_energy: RadialLaw,
    radial_pair_energy_derivative: RadialLaw,
    second_rotation: Iterable[Iterable[float]] | None = None,
) -> VisibleMemoryReciprocalInteraction:
    r"""Symmetrize the canonical visible-point/foreign-memory readout.

    The pair energy is
    ``0.5*(sum_b w_b U(|x_1-y_2b|) + sum_a w_a U(|x_2-y_1a|))``.
    Translating either complete state and differentiating this one energy gives
    equal and opposite forces. This is closer to the canonical readout than a
    memory-memory double integral, but the reciprocal symmetrization itself is
    still a cross-channel model choice.
    """

    if first_state.dim != second_state.dim:
        raise ValueError("states must share one ambient dimension")
    separation_vector = np.asarray(separation, dtype=float)
    if (
        separation_vector.shape != (first_state.dim,)
        or not np.isfinite(separation_vector).all()
    ):
        raise ValueError("separation must be a finite vector matching state dimension")
    separation_norm = float(np.linalg.norm(separation_vector))
    if separation_norm <= 0.0:
        raise ValueError("separation must be non-zero")
    first = place_finite_memory_state(first_state, -0.5 * separation_vector)
    second = place_finite_memory_state(
        second_state,
        0.5 * separation_vector,
        rotation=second_rotation,
    )
    first_to_second = first.x[None, :] - second.memory
    second_to_first = second.x[None, :] - first.memory
    first_radii = np.linalg.norm(first_to_second, axis=1)
    second_radii = np.linalg.norm(second_to_first, axis=1)
    if np.any(first_radii <= 0.0) or np.any(second_radii <= 0.0):
        raise ValueError("pair law is undefined for coincident visible/memory points")
    first_energy = np.asarray(radial_pair_energy(first_radii), dtype=float)
    second_energy = np.asarray(radial_pair_energy(second_radii), dtype=float)
    first_derivative = np.asarray(
        radial_pair_energy_derivative(first_radii), dtype=float
    )
    second_derivative = np.asarray(
        radial_pair_energy_derivative(second_radii), dtype=float
    )
    for values, radii in (
        (first_energy, first_radii),
        (second_energy, second_radii),
        (first_derivative, first_radii),
        (second_derivative, second_radii),
    ):
        if values.shape != radii.shape or not np.isfinite(values).all():
            raise ValueError("radial laws must return finite shape-preserving arrays")
    gradient_first = np.sum(
        (
            second.weights
            * first_derivative
            / first_radii
        )[:, None]
        * first_to_second,
        axis=0,
    )
    gradient_second = np.sum(
        (first.weights * second_derivative / second_radii)[:, None]
        * second_to_first,
        axis=0,
    )
    force_on_second = 0.5 * (gradient_first - gradient_second)
    axis = separation_vector / separation_norm
    return VisibleMemoryReciprocalInteraction(
        separation=separation_vector.copy(),
        energy=float(
            0.5
            * (
                np.dot(second.weights, first_energy)
                + np.dot(first.weights, second_energy)
            )
        ),
        force_on_first=np.asarray(-force_on_second, dtype=float),
        force_on_second=np.asarray(force_on_second, dtype=float),
        radial_force_on_second=float(np.dot(force_on_second, axis)),
    )


def centered_finite_difference_pair_force(
    first_state: FiniteMemoryState,
    second_state: FiniteMemoryState,
    separation: Iterable[float],
    *,
    radial_pair_energy: RadialLaw,
    radial_pair_energy_derivative: RadialLaw,
    step: float,
    second_rotation: Iterable[Iterable[float]] | None = None,
) -> float:
    """Return ``-dE/dR`` as an independent scalar force check."""

    separation_vector = np.asarray(separation, dtype=float)
    norm = float(np.linalg.norm(separation_vector))
    if not np.isfinite(step) or step <= 0.0 or step >= norm:
        raise ValueError("step must be positive, finite and smaller than separation")
    axis = separation_vector / norm
    energies = []
    for offset in (-step, step):
        result = rigid_full_memory_pair_interaction(
            first_state,
            second_state,
            separation_vector + offset * axis,
            radial_pair_energy=radial_pair_energy,
            radial_pair_energy_derivative=radial_pair_energy_derivative,
            second_rotation=second_rotation,
        )
        energies.append(result.energy)
    return float(-(energies[1] - energies[0]) / (2.0 * step))
