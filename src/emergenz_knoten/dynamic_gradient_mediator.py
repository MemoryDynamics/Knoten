"""Energy-dissipative dynamics for the proposed longitudinal mediator.

This module implements the P3.8d reduced two-source experiment.  It does not
modify the canonical ``z=(x, rho)`` process.  Two identical scalar sources are
placed at ``+-R/2`` and coupled to the longitudinal mediator proposed in
``gradient_mediator``.  Angular and radial Fourier integrals are represented
by Gauss-Legendre modes.

For modal source vector ``B(R)`` and positive diagonal stiffness ``A``, the
second-order candidate is

``m_dot=p``
``p_dot=-Gamma*p-A*m+B(R)``
``R_dot=nu*B_R(R).m``.

It follows from ``E=|p|^2/2+m.A.m/2-B(R).m`` that

``E_dot=-Gamma*|p|^2-|R_dot|^2/nu``.

The separation substep uses a scalar discrete gradient.  Its source-work
identity is exact up to the nonlinear solve tolerance.  The fixed-source field
substep is evaluated analytically.  A first-order control with
``Gamma*m_dot=-A*m+B`` has the same static susceptibility and energy but no
reversible conjugate state.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal

import numpy as np
from numpy.polynomial.legendre import leggauss


DynamicOrder = Literal["second", "first"]


def _positive(name: str, value: float) -> float:
    result = float(value)
    if not math.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return result


def _nonnegative(name: str, value: float) -> float:
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be non-negative and finite")
    return result


@dataclass(frozen=True)
class IsotropicMediatorModes:
    """Flattened axisymmetric quadrature for two sources in three dimensions."""

    wavenumber: np.ndarray
    direction_cosine: np.ndarray
    restoring: np.ndarray
    source_prefactor: np.ndarray
    damping: float
    k_max: float
    n_wavenumber: int
    n_direction: int
    spectral_shape: float
    memory_loading: float
    source_mass: float
    coupling: float

    def __post_init__(self) -> None:
        arrays = tuple(
            np.asarray(value, dtype=float)
            for value in (
                self.wavenumber,
                self.direction_cosine,
                self.restoring,
                self.source_prefactor,
            )
        )
        if any(value.ndim != 1 for value in arrays):
            raise ValueError("mode arrays must be one-dimensional")
        if len({value.size for value in arrays}) != 1 or arrays[0].size < 1:
            raise ValueError("mode arrays must have one common non-zero length")
        if not all(np.isfinite(value).all() for value in arrays):
            raise ValueError("mode arrays must be finite")
        if np.any(arrays[0] <= 0.0) or np.any(arrays[2] <= 0.0):
            raise ValueError("wavenumbers and restoring coefficients must be positive")
        _positive("damping", self.damping)
        _positive("k_max", self.k_max)
        _positive("source_mass", self.source_mass)
        if int(self.n_wavenumber) < 2 or int(self.n_direction) < 2:
            raise ValueError("quadrature orders must be at least two")

        for name, value in zip(
            ("wavenumber", "direction_cosine", "restoring", "source_prefactor"),
            arrays,
            strict=True,
        ):
            copied = value.copy()
            copied.setflags(write=False)
            object.__setattr__(self, name, copied)

    @property
    def n_modes(self) -> int:
        return int(self.wavenumber.size)


@dataclass(frozen=True)
class SecondOrderMediatorState:
    """Separation and modal field/conjugate-velocity state."""

    separation: float
    field: np.ndarray
    conjugate_velocity: np.ndarray

    def __post_init__(self) -> None:
        separation = _positive("separation", self.separation)
        field = np.asarray(self.field, dtype=float)
        velocity = np.asarray(self.conjugate_velocity, dtype=float)
        if field.ndim != 1 or velocity.shape != field.shape or field.size < 1:
            raise ValueError("field and conjugate_velocity must be matching vectors")
        if not np.isfinite(field).all() or not np.isfinite(velocity).all():
            raise ValueError("field state must be finite")
        field = field.copy()
        velocity = velocity.copy()
        field.setflags(write=False)
        velocity.setflags(write=False)
        object.__setattr__(self, "separation", separation)
        object.__setattr__(self, "field", field)
        object.__setattr__(self, "conjugate_velocity", velocity)


@dataclass(frozen=True)
class FirstOrderMediatorState:
    """Separation and modal state of the matched first-order control."""

    separation: float
    field: np.ndarray

    def __post_init__(self) -> None:
        separation = _positive("separation", self.separation)
        field = np.asarray(self.field, dtype=float)
        if field.ndim != 1 or field.size < 1 or not np.isfinite(field).all():
            raise ValueError("field must be a finite non-empty vector")
        field = field.copy()
        field.setflags(write=False)
        object.__setattr__(self, "separation", separation)
        object.__setattr__(self, "field", field)


@dataclass(frozen=True)
class DynamicStepLedger:
    """Energy accounting for one symmetric split step."""

    energy_before: float
    energy_after: float
    source_dissipation: float
    mediator_dissipation: float
    balance_residual: float
    maximum_source_work_residual: float


def build_isotropic_mediator_modes(
    *,
    n_wavenumber: int = 64,
    n_direction: int = 64,
    k_max: float = 16.0,
    spectral_shape: float = -1.9,
    memory_loading: float = 0.3,
    memory_decay: float | None = None,
    conjugate_decay: float | None = None,
    source_mass: float = 1.0,
    coupling: float = 1.0,
) -> IsotropicMediatorModes:
    """Build the dimensionless 3D axisymmetric Fourier quadrature.

    The quadrature satisfies

    ``K(R)=sum weight*k^2/A(k)*cos(k*mu*R)``

    in the point-source limit.  The two-source loading is represented as
    ``B=-2*g*M*sqrt(weight)*k*cos(k*mu*R/2)``.  Consequently the equilibrium
    field energy has R-dependent part ``-g^2*M^2*K(R)``.
    """

    n_k = int(n_wavenumber)
    n_mu = int(n_direction)
    if n_k < 2 or n_mu < 2:
        raise ValueError("quadrature orders must be at least two")
    cutoff = _positive("k_max", k_max)
    loading = _positive("memory_loading", memory_loading)
    shape = float(spectral_shape)
    if not math.isfinite(shape):
        raise ValueError("spectral_shape must be finite")
    mass = _positive("source_mass", source_mass)
    gain = float(coupling)
    if not math.isfinite(gain):
        raise ValueError("coupling must be finite")
    if memory_decay is None:
        memory_decay = math.sqrt(loading)
    if conjugate_decay is None:
        conjugate_decay = math.sqrt(loading)
    decay_1 = _positive("memory_decay", memory_decay)
    decay_2 = _positive("conjugate_decay", conjugate_decay)
    if not math.isclose(decay_1 * decay_2, loading, rel_tol=1.0e-12, abs_tol=1.0e-14):
        raise ValueError("memory_decay*conjugate_decay must equal memory_loading")

    nodes_k, weights_k = leggauss(n_k)
    nodes_mu, weights_mu = leggauss(n_mu)
    k = 0.5 * cutoff * (nodes_k + 1.0)
    weight_k = 0.5 * cutoff * weights_k
    grid_k, grid_mu = np.meshgrid(k, nodes_mu, indexing="ij")
    quadrature_weight = (
        np.square(grid_k)
        * weight_k[:, None]
        * weights_mu[None, :]
        / (4.0 * np.pi**2)
    )
    k2 = np.square(grid_k)
    restoring = loading + k2 + shape * np.square(k2) + k2**3
    tolerance = 128.0 * np.finfo(float).eps * max(1.0, loading)
    if np.any(restoring <= tolerance):
        raise ValueError("modal restoring operator must be strictly positive")
    source_prefactor = -2.0 * gain * mass * np.sqrt(quadrature_weight) * grid_k
    return IsotropicMediatorModes(
        wavenumber=grid_k.ravel(),
        direction_cosine=grid_mu.ravel(),
        restoring=restoring.ravel(),
        source_prefactor=source_prefactor.ravel(),
        damping=decay_1 + decay_2,
        k_max=cutoff,
        n_wavenumber=n_k,
        n_direction=n_mu,
        spectral_shape=shape,
        memory_loading=loading,
        source_mass=mass,
        coupling=gain,
    )


def modal_source(modes: IsotropicMediatorModes, separation: float) -> np.ndarray:
    """Return the two-source modal loading ``B(R)``."""

    radius = _positive("separation", separation)
    phase = 0.5 * modes.wavenumber * modes.direction_cosine * radius
    return modes.source_prefactor * np.cos(phase)


def modal_source_derivative(
    modes: IsotropicMediatorModes,
    separation: float,
) -> np.ndarray:
    """Return ``dB/dR``."""

    radius = _positive("separation", separation)
    frequency = 0.5 * modes.wavenumber * modes.direction_cosine
    return -modes.source_prefactor * frequency * np.sin(frequency * radius)


def modal_source_second_derivative(
    modes: IsotropicMediatorModes,
    separation: float,
) -> np.ndarray:
    """Return ``d^2B/dR^2``."""

    radius = _positive("separation", separation)
    frequency = 0.5 * modes.wavenumber * modes.direction_cosine
    return -modes.source_prefactor * np.square(frequency) * np.cos(
        frequency * radius
    )


def modal_static_force(modes: IsotropicMediatorModes, separation: float) -> float:
    """Return the equilibrium outward force of the truncated modal field."""

    source = modal_source(modes, separation)
    source_derivative = modal_source_derivative(modes, separation)
    return float(np.dot(source_derivative, source / modes.restoring))


def modal_static_pair_energy(
    modes: IsotropicMediatorModes,
    separation: float,
) -> float:
    """Return equilibrium field energy, including an R-independent self term."""

    source = modal_source(modes, separation)
    return float(-0.5 * np.dot(source, source / modes.restoring))


def second_order_energy(
    state: SecondOrderMediatorState,
    modes: IsotropicMediatorModes,
) -> float:
    """Return total reduced field-plus-source energy."""

    _validate_state_size(state.field, modes)
    source = modal_source(modes, state.separation)
    return float(
        0.5 * np.dot(state.conjugate_velocity, state.conjugate_velocity)
        + 0.5 * np.dot(modes.restoring * state.field, state.field)
        - np.dot(source, state.field)
    )


def first_order_energy(
    state: FirstOrderMediatorState,
    modes: IsotropicMediatorModes,
) -> float:
    """Return the matched first-order control energy."""

    _validate_state_size(state.field, modes)
    source = modal_source(modes, state.separation)
    return float(
        0.5 * np.dot(modes.restoring * state.field, state.field)
        - np.dot(source, state.field)
    )


def _validate_state_size(field: np.ndarray, modes: IsotropicMediatorModes) -> None:
    if np.asarray(field).shape != (modes.n_modes,):
        raise ValueError("field size must match modal quadrature")


def zero_second_order_state(
    modes: IsotropicMediatorModes,
    *,
    separation: float,
) -> SecondOrderMediatorState:
    """Create a zero-field second-order state after the source quench."""

    zeros = np.zeros(modes.n_modes, dtype=float)
    return SecondOrderMediatorState(separation, zeros, zeros)


def zero_first_order_state(
    modes: IsotropicMediatorModes,
    *,
    separation: float,
) -> FirstOrderMediatorState:
    """Create a zero-field first-order state after the source quench."""

    return FirstOrderMediatorState(
        separation,
        np.zeros(modes.n_modes, dtype=float),
    )


def _second_order_fixed_source_values(
    field: np.ndarray,
    velocity: np.ndarray,
    source: np.ndarray,
    restoring: np.ndarray,
    damping: float,
    duration: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Analytic damped-oscillator values for one non-negative duration."""

    time = _nonnegative("duration", duration)
    if time == 0.0:
        return np.asarray(field, dtype=float).copy(), np.asarray(velocity, dtype=float).copy()
    equilibrium = source / restoring
    displacement = np.asarray(field, dtype=float) - equilibrium
    initial_velocity = np.asarray(velocity, dtype=float)
    half_damping = 0.5 * damping
    discriminant = restoring - half_damping**2
    decay = math.exp(-half_damping * time)
    next_displacement = np.empty_like(displacement)
    next_velocity = np.empty_like(initial_velocity)
    scale = np.maximum(1.0, restoring)
    tolerance = 256.0 * np.finfo(float).eps * scale
    under = discriminant > tolerance
    over = discriminant < -tolerance
    critical = ~(under | over)

    if np.any(under):
        omega = np.sqrt(discriminant[under])
        cosine = np.cos(omega * time)
        sine_over_omega = np.sin(omega * time) / omega
        y0 = displacement[under]
        v0 = initial_velocity[under]
        next_displacement[under] = decay * (
            (cosine + half_damping * sine_over_omega) * y0
            + sine_over_omega * v0
        )
        next_velocity[under] = decay * (
            -restoring[under] * sine_over_omega * y0
            + (cosine - half_damping * sine_over_omega) * v0
        )
    if np.any(over):
        rate = np.sqrt(-discriminant[over])
        cosine = np.cosh(rate * time)
        sine_over_rate = np.sinh(rate * time) / rate
        y0 = displacement[over]
        v0 = initial_velocity[over]
        next_displacement[over] = decay * (
            (cosine + half_damping * sine_over_rate) * y0
            + sine_over_rate * v0
        )
        next_velocity[over] = decay * (
            -restoring[over] * sine_over_rate * y0
            + (cosine - half_damping * sine_over_rate) * v0
        )
    if np.any(critical):
        y0 = displacement[critical]
        v0 = initial_velocity[critical]
        shifted_velocity = v0 + half_damping * y0
        next_displacement[critical] = decay * (y0 + shifted_velocity * time)
        next_velocity[critical] = decay * (
            v0 - half_damping * shifted_velocity * time
        )
    return next_displacement + equilibrium, next_velocity


def advance_second_order_fixed_source(
    state: SecondOrderMediatorState,
    modes: IsotropicMediatorModes,
    *,
    duration: float,
) -> SecondOrderMediatorState:
    """Advance ``(m,p)`` exactly while holding the source positions fixed."""

    _validate_state_size(state.field, modes)
    source = modal_source(modes, state.separation)
    field, velocity = _second_order_fixed_source_values(
        state.field,
        state.conjugate_velocity,
        source,
        modes.restoring,
        modes.damping,
        duration,
    )
    return SecondOrderMediatorState(state.separation, field, velocity)


def advance_first_order_fixed_source(
    state: FirstOrderMediatorState,
    modes: IsotropicMediatorModes,
    *,
    duration: float,
) -> FirstOrderMediatorState:
    """Advance the matched relaxation control exactly at fixed sources."""

    _validate_state_size(state.field, modes)
    time = _nonnegative("duration", duration)
    source = modal_source(modes, state.separation)
    equilibrium = source / modes.restoring
    decay = np.exp(-modes.restoring * time / modes.damping)
    field = equilibrium + decay * (state.field - equilibrium)
    return FirstOrderMediatorState(state.separation, field)


def _source_discrete_gradient_step(
    separation: float,
    field: np.ndarray,
    modes: IsotropicMediatorModes,
    *,
    duration: float,
    relative_mobility: float,
    max_iterations: int = 20,
) -> tuple[float, float, float]:
    """Advance R with an exact scalar source-work discrete gradient."""

    radius = _positive("separation", separation)
    time = _nonnegative("duration", duration)
    mobility = _positive("relative_mobility", relative_mobility)
    if time == 0.0 or modes.coupling == 0.0:
        return radius, 0.0, 0.0
    _validate_state_size(field, modes)
    derivative_old = modal_source_derivative(modes, radius)
    frequency = 0.5 * modes.wavenumber * modes.direction_cosine
    delta = time * mobility * float(np.dot(field, derivative_old))
    tolerance = 2.0e-13

    for _ in range(max_iterations):
        if radius + delta <= 0.0:
            delta = -0.5 * radius
        midpoint = radius + 0.5 * delta
        half_phase_change = 0.5 * frequency * delta
        sinc = np.sinc(half_phase_change / np.pi)
        quotient = (
            -modes.source_prefactor
            * frequency
            * np.sin(frequency * midpoint)
            * sinc
        )
        sinc_derivative = np.empty_like(half_phase_change)
        small = np.abs(half_phase_change) < 1.0e-4
        t = half_phase_change[small]
        sinc_derivative[small] = 0.5 * frequency[small] * (
            -t / 3.0 + t**3 / 30.0 - t**5 / 840.0
        )
        t = half_phase_change[~small]
        sinc_derivative[~small] = 0.5 * frequency[~small] * (
            (t * np.cos(t) - np.sin(t)) / np.square(t)
        )
        quotient_derivative = -modes.source_prefactor * frequency * (
            0.5 * frequency * np.cos(frequency * midpoint) * sinc
            + np.sin(frequency * midpoint) * sinc_derivative
        )
        residual = delta - time * mobility * float(np.dot(field, quotient))
        if abs(residual) <= tolerance * max(1.0, abs(delta)):
            break
        jacobian = 1.0 - time * mobility * float(
            np.dot(field, quotient_derivative)
        )
        if not math.isfinite(jacobian) or abs(jacobian) < 1.0e-12:
            raise RuntimeError("source discrete-gradient Jacobian is singular")
        correction = residual / jacobian
        trial = delta - correction
        while radius + trial <= 0.0:
            correction *= 0.5
            trial = delta - correction
        delta = trial
    else:
        raise RuntimeError("source discrete-gradient solve did not converge")

    new_radius = radius + delta
    midpoint = radius + 0.5 * delta
    half_phase_change = 0.5 * frequency * delta
    quotient = (
        -modes.source_prefactor
        * frequency
        * np.sin(frequency * midpoint)
        * np.sinc(half_phase_change / np.pi)
    )
    energy_change = -delta * float(np.dot(field, quotient))
    expected_change = -(delta * delta) / (time * mobility)
    return new_radius, -expected_change, energy_change - expected_change


def step_second_order_mediator(
    state: SecondOrderMediatorState,
    modes: IsotropicMediatorModes,
    *,
    time_step: float,
    relative_mobility: float = 1.0,
) -> tuple[SecondOrderMediatorState, DynamicStepLedger]:
    """Take one symmetric energy-dissipative source/field/source step."""

    dt = _positive("time_step", time_step)
    mobility = _positive("relative_mobility", relative_mobility)
    energy_before = second_order_energy(state, modes)
    first_radius, first_source_loss, first_residual = _source_discrete_gradient_step(
        state.separation,
        state.field,
        modes,
        duration=0.5 * dt,
        relative_mobility=mobility,
    )
    after_first_source = SecondOrderMediatorState(
        first_radius, state.field, state.conjugate_velocity
    )
    energy_after_first_source = second_order_energy(after_first_source, modes)
    after_field = advance_second_order_fixed_source(
        after_first_source,
        modes,
        duration=dt,
    )
    energy_after_field = second_order_energy(after_field, modes)
    second_radius, second_source_loss, second_residual = _source_discrete_gradient_step(
        after_field.separation,
        after_field.field,
        modes,
        duration=0.5 * dt,
        relative_mobility=mobility,
    )
    result = SecondOrderMediatorState(
        second_radius,
        after_field.field,
        after_field.conjugate_velocity,
    )
    energy_after = second_order_energy(result, modes)
    source_loss = first_source_loss + second_source_loss
    field_loss = energy_after_first_source - energy_after_field
    balance = energy_after - energy_before + source_loss + field_loss
    return result, DynamicStepLedger(
        energy_before=energy_before,
        energy_after=energy_after,
        source_dissipation=float(source_loss),
        mediator_dissipation=float(field_loss),
        balance_residual=float(balance),
        maximum_source_work_residual=float(
            max(abs(first_residual), abs(second_residual))
        ),
    )


def step_first_order_mediator(
    state: FirstOrderMediatorState,
    modes: IsotropicMediatorModes,
    *,
    time_step: float,
    relative_mobility: float = 1.0,
) -> tuple[FirstOrderMediatorState, DynamicStepLedger]:
    """Take one matched first-order source/field/source control step."""

    dt = _positive("time_step", time_step)
    mobility = _positive("relative_mobility", relative_mobility)
    energy_before = first_order_energy(state, modes)
    first_radius, first_source_loss, first_residual = _source_discrete_gradient_step(
        state.separation,
        state.field,
        modes,
        duration=0.5 * dt,
        relative_mobility=mobility,
    )
    after_first_source = FirstOrderMediatorState(first_radius, state.field)
    energy_after_first_source = first_order_energy(after_first_source, modes)
    after_field = advance_first_order_fixed_source(
        after_first_source,
        modes,
        duration=dt,
    )
    energy_after_field = first_order_energy(after_field, modes)
    second_radius, second_source_loss, second_residual = _source_discrete_gradient_step(
        after_field.separation,
        after_field.field,
        modes,
        duration=0.5 * dt,
        relative_mobility=mobility,
    )
    result = FirstOrderMediatorState(second_radius, after_field.field)
    energy_after = first_order_energy(result, modes)
    source_loss = first_source_loss + second_source_loss
    field_loss = energy_after_first_source - energy_after_field
    balance = energy_after - energy_before + source_loss + field_loss
    return result, DynamicStepLedger(
        energy_before=energy_before,
        energy_after=energy_after,
        source_dissipation=float(source_loss),
        mediator_dissipation=float(field_loss),
        balance_residual=float(balance),
        maximum_source_work_residual=float(
            max(abs(first_residual), abs(second_residual))
        ),
    )


def instantaneous_radial_force(
    separation: float,
    field: np.ndarray,
    modes: IsotropicMediatorModes,
) -> float:
    """Return the current outward generalized force on the separation."""

    _validate_state_size(field, modes)
    return float(np.dot(modal_source_derivative(modes, separation), field))


def second_order_fixed_source_damping_quadrature(
    state: SecondOrderMediatorState,
    modes: IsotropicMediatorModes,
    *,
    duration: float,
    quadrature_order: int = 32,
) -> float:
    """Independently integrate ``Gamma*|p(t)|^2`` over one exact field step."""

    time = _positive("duration", duration)
    order = int(quadrature_order)
    if order < 2:
        raise ValueError("quadrature_order must be at least two")
    nodes, weights = leggauss(order)
    times = 0.5 * time * (nodes + 1.0)
    time_weights = 0.5 * time * weights
    source = modal_source(modes, state.separation)
    integral = 0.0
    for sample_time, sample_weight in zip(times, time_weights, strict=True):
        _, velocity = _second_order_fixed_source_values(
            state.field,
            state.conjugate_velocity,
            source,
            modes.restoring,
            modes.damping,
            float(sample_time),
        )
        integral += float(sample_weight) * modes.damping * float(
            np.dot(velocity, velocity)
        )
    return float(integral)


def selected_mode_step_response(
    times: np.ndarray,
    *,
    restoring: float,
    damping: float,
    dynamic_order: DynamicOrder,
) -> np.ndarray:
    """Return unit-normalized fixed-source response from zero initial field."""

    sample_times = np.asarray(times, dtype=float)
    if sample_times.ndim != 1 or not np.isfinite(sample_times).all():
        raise ValueError("times must be a finite vector")
    if np.any(sample_times < 0.0):
        raise ValueError("times must be non-negative")
    stiffness = _positive("restoring", restoring)
    drag = _positive("damping", damping)
    if dynamic_order == "first":
        return np.asarray(1.0 - np.exp(-stiffness * sample_times / drag))
    if dynamic_order != "second":
        raise ValueError("dynamic_order must be second or first")
    response = np.empty_like(sample_times)
    for index, time in enumerate(sample_times):
        field, _ = _second_order_fixed_source_values(
            np.asarray([0.0]),
            np.asarray([0.0]),
            np.asarray([stiffness]),
            np.asarray([stiffness]),
            drag,
            float(time),
        )
        response[index] = field[0]
    return response
