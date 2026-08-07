"""Discrete reciprocal trajectory-memory closures and local mode tests."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ReciprocalMemoryMode:
    """One singular mode of a discrete adjoint-reciprocal closure."""

    singular_value: float
    dimensionless_coupling: float
    eigenvalues: tuple[complex, complex]
    classification: str
    stable: bool


@dataclass(frozen=True)
class ReciprocalMemorySpectrum:
    """Spectrum and exact complex-mode window of the reciprocal closure."""

    forgetting_factor: float
    coupling: float
    complex_window: tuple[float, float]
    stability_upper_bound: float
    modes: tuple[ReciprocalMemoryMode, ...]


def _forgetting_factor(value: float) -> float:
    factor = float(value)
    if not np.isfinite(factor) or not 0.0 <= factor <= 1.0:
        raise ValueError("forgetting_factor must lie in [0, 1]")
    return factor


def _coupling(value: float) -> float:
    coupling = float(value)
    if not np.isfinite(coupling) or coupling < 0.0:
        raise ValueError("coupling must be finite and non-negative")
    return coupling


def _positive_metric(
    metric: np.ndarray | None,
    size: int,
    *,
    name: str,
) -> np.ndarray:
    if metric is None:
        return np.eye(size)
    matrix = np.asarray(metric, dtype=float)
    if matrix.shape != (size, size) or not np.isfinite(matrix).all():
        raise ValueError(f"{name} must be a finite square matrix of size {size}")
    if not np.allclose(matrix, matrix.T, rtol=1e-12, atol=1e-14):
        raise ValueError(f"{name} must be symmetric")
    if float(np.min(np.linalg.eigvalsh(matrix))) <= 0.0:
        raise ValueError(f"{name} must be positive definite")
    return matrix


def _symmetric_sqrt(matrix: np.ndarray, *, inverse: bool = False) -> np.ndarray:
    values, vectors = np.linalg.eigh(matrix)
    powers = np.reciprocal(np.sqrt(values)) if inverse else np.sqrt(values)
    return (vectors * powers) @ vectors.T


def metric_adjoint(
    forward_operator: np.ndarray,
    *,
    visible_metric: np.ndarray | None = None,
    memory_metric: np.ndarray | None = None,
) -> np.ndarray:
    r"""Return the metric adjoint ``B^dagger = G_x^-1 B^T G_h``.

    ``forward_operator`` maps visible perturbations to memory perturbations.
    The metrics are part of the model specification; changing their relative
    normalization changes the reciprocal feedback strength.
    """

    forward = np.asarray(forward_operator, dtype=float)
    if forward.ndim != 2 or not np.isfinite(forward).all():
        raise ValueError("forward_operator must be a finite matrix")
    memory_size, visible_size = forward.shape
    gx = _positive_metric(visible_metric, visible_size, name="visible_metric")
    gh = _positive_metric(memory_metric, memory_size, name="memory_metric")
    return np.linalg.solve(gx, forward.T @ gh)


def metric_singular_values(
    forward_operator: np.ndarray,
    *,
    visible_metric: np.ndarray | None = None,
    memory_metric: np.ndarray | None = None,
) -> np.ndarray:
    """Return singular values after whitening both state-space metrics."""

    forward = np.asarray(forward_operator, dtype=float)
    if forward.ndim != 2 or not np.isfinite(forward).all():
        raise ValueError("forward_operator must be a finite matrix")
    memory_size, visible_size = forward.shape
    gx = _positive_metric(visible_metric, visible_size, name="visible_metric")
    gh = _positive_metric(memory_metric, memory_size, name="memory_metric")
    whitened = _symmetric_sqrt(gh) @ forward @ _symmetric_sqrt(gx, inverse=True)
    return np.linalg.svd(whitened, compute_uv=False)


def reciprocal_memory_operator(
    forward_operator: np.ndarray,
    *,
    forgetting_factor: float,
    coupling: float,
    visible_metric: np.ndarray | None = None,
    memory_metric: np.ndarray | None = None,
) -> np.ndarray:
    r"""Build the discrete adjoint-reciprocal update matrix.

    The update order is

    ``x_next = x - sqrt(g) B^dagger h``
    ``h_next = q h + sqrt(g) B x_next``.

    Here ``x`` is a translation-reduced visible perturbation, not necessarily
    the absolute particle position. This closure is a proposed extension and
    is not the update law of the passive memory model.
    """

    forward = np.asarray(forward_operator, dtype=float)
    if forward.ndim != 2 or not np.isfinite(forward).all():
        raise ValueError("forward_operator must be a finite matrix")
    q = _forgetting_factor(forgetting_factor)
    gain = _coupling(coupling)
    root_gain = float(np.sqrt(gain))
    memory_size, visible_size = forward.shape
    adjoint = metric_adjoint(
        forward,
        visible_metric=visible_metric,
        memory_metric=memory_metric,
    )
    return np.block(
        [
            [np.eye(visible_size), -root_gain * adjoint],
            [
                root_gain * forward,
                q * np.eye(memory_size) - gain * forward @ adjoint,
            ],
        ]
    )


def reciprocal_mode_eigenvalues(
    dimensionless_coupling: float,
    *,
    forgetting_factor: float,
) -> tuple[complex, complex]:
    """Return the two roots for one singular mode."""

    q = _forgetting_factor(forgetting_factor)
    value = _coupling(dimensionless_coupling)
    trace = 1.0 + q - value
    discriminant = complex(trace * trace - 4.0 * q)
    root = np.sqrt(discriminant)
    return (0.5 * (trace + root), 0.5 * (trace - root))


def reciprocal_memory_spectrum(
    forward_operator: np.ndarray,
    *,
    forgetting_factor: float,
    coupling: float,
    visible_metric: np.ndarray | None = None,
    memory_metric: np.ndarray | None = None,
) -> ReciprocalMemorySpectrum:
    """Classify all metric singular modes of the reciprocal update."""

    q = _forgetting_factor(forgetting_factor)
    gain = _coupling(coupling)
    root_q = float(np.sqrt(q))
    lower = float((1.0 - root_q) ** 2)
    upper = float((1.0 + root_q) ** 2)
    stability_upper = float(2.0 * (1.0 + q))
    modes: list[ReciprocalMemoryMode] = []
    for singular_value in metric_singular_values(
        forward_operator,
        visible_metric=visible_metric,
        memory_metric=memory_metric,
    ):
        value = float(gain * singular_value * singular_value)
        scale = max(1.0, lower, upper, stability_upper, value)
        tolerance = float(64.0 * np.finfo(float).eps * scale)
        if value <= tolerance:
            classification = "uncoupled_neutral"
        elif value < lower - tolerance:
            classification = "overdamped"
        elif abs(value - lower) <= tolerance:
            classification = "critical_onset"
        elif value < upper - tolerance:
            classification = "undamped_rotation" if q == 1.0 else "damped_rotation"
        elif abs(value - upper) <= tolerance:
            classification = "critical_alternating"
        elif value < stability_upper - tolerance:
            classification = "alternating_relaxation"
        elif abs(value - stability_upper) <= tolerance:
            classification = "flip_boundary"
        else:
            classification = "flip_unstable"
        stable = bool(q < 1.0 and tolerance < value < stability_upper - tolerance)
        modes.append(
            ReciprocalMemoryMode(
                singular_value=float(singular_value),
                dimensionless_coupling=value,
                eigenvalues=reciprocal_mode_eigenvalues(
                    value,
                    forgetting_factor=q,
                ),
                classification=classification,
                stable=stable,
            )
        )
    return ReciprocalMemorySpectrum(
        forgetting_factor=q,
        coupling=gain,
        complex_window=(lower, upper),
        stability_upper_bound=stability_upper,
        modes=tuple(modes),
    )


def normalized_direction_jacobian(
    displacement: np.ndarray,
    *,
    relaxation: float,
) -> np.ndarray:
    r"""Linearize ``kappa * displacement / ||displacement||``.

    The Jacobian is ``kappa (I-u u^T) / ||displacement||``. It has one
    longitudinal zero mode and ``d-1`` degenerate transverse modes. This
    degeneracy does not select three ambient dimensions.
    """

    step = np.asarray(displacement, dtype=float)
    if step.ndim != 1 or step.size < 1 or not np.isfinite(step).all():
        raise ValueError("displacement must be a finite non-empty vector")
    kappa = float(relaxation)
    if not np.isfinite(kappa) or not 0.0 < kappa <= 1.0:
        raise ValueError("relaxation must lie in (0, 1]")
    radius = float(np.linalg.norm(step))
    if radius == 0.0:
        raise ValueError("normalized direction is not differentiable at zero")
    direction = step / radius
    return kappa * (np.eye(step.size) - np.outer(direction, direction)) / radius
