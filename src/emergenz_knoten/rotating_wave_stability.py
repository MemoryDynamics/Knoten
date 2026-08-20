"""Full FIFO-map stability utilities for scalar-memory rotating waves."""

from __future__ import annotations

import math

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix

from .rotating_wave import double_gaussian_gradient_factor


def rotation_matrix(angle: float) -> np.ndarray:
    """Return the two-dimensional proper rotation matrix."""

    value = float(angle)
    if not math.isfinite(value):
        raise ValueError("angle must be finite")
    return np.asarray(
        [
            [math.cos(value), -math.sin(value)],
            [math.sin(value), math.cos(value)],
        ]
    )


def circular_history(*, radius: float, theta: float, horizon: int) -> np.ndarray:
    """Return history[j]=R(-j theta)(radius,0)."""

    orbit_radius = float(radius)
    angle = float(theta)
    if not math.isfinite(orbit_radius) or orbit_radius <= 0.0:
        raise ValueError("radius must be positive and finite")
    if not math.isfinite(angle) or not 0.0 < angle < math.pi:
        raise ValueError("theta must lie strictly between zero and pi")
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    ages = np.arange(horizon, dtype=float)
    return np.column_stack(
        (
            orbit_radius * np.cos(-angle * ages),
            orbit_radius * np.sin(-angle * ages),
        )
    )


def finite_memory_weights(
    *, alpha: float, horizon: int, memory_mass: float
) -> np.ndarray:
    """Return the native unnormalized finite-memory weights."""

    forgetting = float(alpha)
    mass = float(memory_mass)
    if not math.isfinite(forgetting) or not 0.0 < forgetting < 1.0:
        raise ValueError("alpha must lie strictly between zero and one")
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    if not math.isfinite(mass) or mass <= 0.0:
        raise ValueError("memory_mass must be positive and finite")
    ages = np.arange(horizon, dtype=float)
    return forgetting * mass * np.power(1.0 - forgetting, ages)


def native_fifo_step(
    history: np.ndarray,
    *,
    alpha: float,
    memory_mass: float,
    eta: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float,
    amplitude_att: float,
) -> np.ndarray:
    """Advance one deterministic native K0-H FIFO update."""

    state = np.asarray(history, dtype=float)
    if (
        state.ndim != 2
        or state.shape[0] < 1
        or state.shape[1] != 2
        or not np.isfinite(state).all()
    ):
        raise ValueError("history must be a finite array with shape (H,2)")
    gain = float(eta)
    if not math.isfinite(gain) or gain <= 0.0:
        raise ValueError("eta must be positive and finite")
    weights = finite_memory_weights(
        alpha=alpha,
        horizon=state.shape[0],
        memory_mass=memory_mass,
    )
    displacement = state[0] - state
    radii = np.linalg.norm(displacement, axis=1)
    factor = np.asarray(
        double_gaussian_gradient_factor(
            radii,
            sigma_rep=sigma_rep,
            sigma_att=sigma_att,
            amplitude_rep=amplitude_rep,
            amplitude_att=amplitude_att,
        )
    )
    gradient = np.sum(
        weights[:, None] * factor[:, None] * displacement,
        axis=0,
    )
    result = np.empty_like(state)
    result[0] = state[0] - gain * gradient
    if state.shape[0] > 1:
        result[1:] = state[:-1]
    return result


def co_rotating_fifo_step(
    history: np.ndarray,
    *,
    theta: float,
    **parameters: float,
) -> np.ndarray:
    """Advance the FIFO map and rotate every output coordinate by -theta."""

    native = native_fifo_step(history, **parameters)
    return native @ rotation_matrix(-theta).T


def _gradient_hessian_blocks(
    history: np.ndarray,
    *,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float,
    amplitude_att: float,
) -> np.ndarray:
    """Return Hessian blocks of grad K(x-h_j) for every history age."""

    state = np.asarray(history, dtype=float)
    displacement = state[0] - state
    radii_squared = np.sum(displacement * displacement, axis=1)
    rep_exp = np.exp(-radii_squared / (2.0 * sigma_rep**2))
    att_exp = np.exp(-radii_squared / (2.0 * sigma_att**2))
    factor = (
        -amplitude_rep / sigma_rep**2 * rep_exp + amplitude_att / sigma_att**2 * att_exp
    )
    derivative_over_radius = (
        amplitude_rep / sigma_rep**4 * rep_exp - amplitude_att / sigma_att**4 * att_exp
    )
    identity = np.eye(2)
    return (
        factor[:, None, None] * identity[None, :, :]
        + derivative_over_radius[:, None, None]
        * displacement[:, :, None]
        * displacement[:, None, :]
    )


def co_rotating_fifo_jacobian(
    history: np.ndarray,
    *,
    theta: float,
    alpha: float,
    memory_mass: float,
    eta: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float,
    amplitude_att: float,
) -> csr_matrix:
    """Return the sparse exact Jacobian of the co-rotating full FIFO map."""

    state = np.asarray(history, dtype=float)
    if (
        state.ndim != 2
        or state.shape[0] < 1
        or state.shape[1] != 2
        or not np.isfinite(state).all()
    ):
        raise ValueError("history must be a finite array with shape (H,2)")
    horizon = state.shape[0]
    weights = finite_memory_weights(
        alpha=alpha,
        horizon=horizon,
        memory_mass=memory_mass,
    )
    hessian = _gradient_hessian_blocks(
        state,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )
    rotate_back = rotation_matrix(-theta)
    summed = np.sum(weights[1:, None, None] * hessian[1:], axis=0)
    first_blocks = [rotate_back @ (np.eye(2) - eta * summed)]
    first_blocks.extend(
        rotate_back @ (eta * weights[j] * hessian[j]) for j in range(1, horizon)
    )

    rows: list[int] = []
    columns: list[int] = []
    data: list[float] = []

    def append_block(row_block: int, column_block: int, block: np.ndarray) -> None:
        for local_row in range(2):
            for local_column in range(2):
                rows.append(2 * row_block + local_row)
                columns.append(2 * column_block + local_column)
                data.append(float(block[local_row, local_column]))

    for column_block, block in enumerate(first_blocks):
        append_block(0, column_block, block)
    for row_block in range(1, horizon):
        append_block(row_block, row_block - 1, rotate_back)

    dimension = 2 * horizon
    return coo_matrix(
        (data, (rows, columns)),
        shape=(dimension, dimension),
    ).tocsr()


def symmetry_tangent_vectors(history: np.ndarray) -> dict[str, np.ndarray]:
    """Return native translation and rotation tangent vectors."""

    state = np.asarray(history, dtype=float)
    if state.ndim != 2 or state.shape[1] != 2:
        raise ValueError("history must have shape (H,2)")
    translation_x = np.tile([1.0, 0.0], (state.shape[0], 1)).ravel()
    translation_y = np.tile([0.0, 1.0], (state.shape[0], 1)).ravel()
    generator = np.asarray([[0.0, -1.0], [1.0, 0.0]])
    rotation = (state @ generator.T).ravel()
    return {
        "translation_x": translation_x,
        "translation_y": translation_y,
        "rotation": rotation,
    }


def translation_reduced_features(
    history: np.ndarray,
    *,
    alpha: float,
    memory_mass: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the D0 feature array and its fixed component weights."""

    state = np.asarray(history, dtype=float)
    if state.ndim != 2 or state.shape[0] < 1 or state.shape[1] != 2:
        raise ValueError("history must have shape (H,2)")
    raw_weights = finite_memory_weights(
        alpha=alpha,
        horizon=state.shape[0],
        memory_mass=memory_mass,
    )
    normalized = raw_weights / np.sum(raw_weights)
    center = np.sum(normalized[:, None] * state, axis=0)
    features = np.empty_like(state)
    features[0] = state[0] - center
    if state.shape[0] > 1:
        features[1:] = state[1:] - center
    metric_weights = normalized.copy()
    metric_weights[0] = 1.0
    return features, metric_weights


def rotation_translation_quotient_distance(
    history: np.ndarray,
    reference: np.ndarray,
    *,
    alpha: float,
    memory_mass: float,
) -> tuple[float, float]:
    """Return D0 distance after optimal common translation and proper rotation."""

    features, weights = translation_reduced_features(
        history,
        alpha=alpha,
        memory_mass=memory_mass,
    )
    reference_features, reference_weights = translation_reduced_features(
        reference,
        alpha=alpha,
        memory_mass=memory_mass,
    )
    if weights.shape != reference_weights.shape or not np.array_equal(
        weights, reference_weights
    ):
        raise ValueError("history and reference must use the same horizon")
    values = features[:, 0] + 1j * features[:, 1]
    target = reference_features[:, 0] + 1j * reference_features[:, 1]
    correlation = np.sum(weights * values * np.conjugate(target))
    alignment_angle = -float(np.angle(correlation))
    aligned = values * np.exp(1j * alignment_angle)
    distance_squared = np.sum(weights * np.abs(aligned - target) ** 2)
    return float(math.sqrt(max(0.0, distance_squared))), alignment_angle


def translation_reduced_norm(
    history: np.ndarray,
    *,
    alpha: float,
    memory_mass: float,
) -> float:
    """Return the norm induced by the frozen D0 metric."""

    features, weights = translation_reduced_features(
        history,
        alpha=alpha,
        memory_mass=memory_mass,
    )
    return float(math.sqrt(np.sum(weights[:, None] * features * features)))
