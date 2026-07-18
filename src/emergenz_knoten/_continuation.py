"""Internal finite-memory primitives shared by paired continuations."""

from __future__ import annotations

import numpy as np

try:
    from numba import njit
except ImportError:  # pragma: no cover

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


@njit(cache=True)
def path_gradient(
    x: np.ndarray,
    history: np.ndarray,
    head: int,
    weights: np.ndarray,
    coupling: float,
    sigma_rep2: float,
    sigma_att2: float,
    amplitude_rep: float,
    amplitude_att: float,
) -> np.ndarray:
    """Return the two-scale gradient for an age-ordered circular buffer."""

    dim = x.shape[0]
    n_memory = history.shape[0]
    gradient = np.zeros(dim, np.float64)
    if coupling == 0.0:
        return gradient
    for age in range(n_memory):
        memory_index = (head + age) % n_memory
        r2 = 0.0
        for coord in range(dim):
            delta = x[coord] - history[memory_index, coord]
            r2 += delta * delta
        rep_factor = -amplitude_rep * np.exp(-0.5 * r2 / sigma_rep2) / sigma_rep2
        att_factor = -amplitude_att * np.exp(-0.5 * r2 / sigma_att2) / sigma_att2
        factor = weights[age] * (rep_factor - att_factor)
        for coord in range(dim):
            gradient[coord] += factor * (x[coord] - history[memory_index, coord])
    return gradient


@njit(cache=True)
def path_three_scale_gradient(
    x: np.ndarray,
    history: np.ndarray,
    head: int,
    weights: np.ndarray,
    coupling: float,
    sigma_rep2: float,
    sigma_att2: float,
    sigma_comp2: float,
    amplitude_rep: float,
    amplitude_att: float,
    amplitude_comp: float,
) -> np.ndarray:
    """Return the three-scale gradient for an age-ordered circular buffer."""

    dim = x.shape[0]
    n_memory = history.shape[0]
    gradient = np.zeros(dim, np.float64)
    if coupling == 0.0:
        return gradient
    for age in range(n_memory):
        memory_index = (head + age) % n_memory
        r2 = 0.0
        for coord in range(dim):
            delta = x[coord] - history[memory_index, coord]
            r2 += delta * delta
        rep_factor = -amplitude_rep * np.exp(-0.5 * r2 / sigma_rep2) / sigma_rep2
        att_factor = -amplitude_att * np.exp(-0.5 * r2 / sigma_att2) / sigma_att2
        comp_factor = -amplitude_comp * np.exp(-0.5 * r2 / sigma_comp2) / sigma_comp2
        factor = weights[age] * (rep_factor - att_factor + comp_factor)
        for coord in range(dim):
            gradient[coord] += factor * (x[coord] - history[memory_index, coord])
    return gradient


@njit(cache=True)
def path_observables(
    x: np.ndarray,
    history: np.ndarray,
    head: int,
    weights: np.ndarray,
    weight_mass: float,
):
    """Return position, memory center, shape tensor, and RMS radius."""

    dim = x.shape[0]
    n_memory = history.shape[0]
    center = np.zeros(dim, np.float64)
    tensor = np.zeros((dim, dim), np.float64)
    for age in range(n_memory):
        memory_index = (head + age) % n_memory
        for coord in range(dim):
            center[coord] += weights[age] * history[memory_index, coord]
    center /= weight_mass

    radius2 = 0.0
    for row in range(dim):
        for col in range(dim):
            value = 0.0
            for age in range(n_memory):
                memory_index = (head + age) % n_memory
                delta_row = history[memory_index, row] - center[row]
                delta_col = history[memory_index, col] - center[col]
                value += weights[age] * delta_row * delta_col
            value /= weight_mass
            tensor[row, col] = value
            if row == col:
                radius2 += value
    return x.copy(), center, tensor, np.sqrt(max(radius2, 0.0))


def symmetric_tensor_vector(tensor: np.ndarray) -> np.ndarray:
    """Vectorize a symmetric tensor while preserving its Frobenius norm."""

    dim = tensor.shape[0]
    values = []
    for row in range(dim):
        for col in range(row, dim):
            scale = 1.0 if row == col else np.sqrt(2.0)
            values.append(scale * float(tensor[row, col]))
    return np.asarray(values, dtype=float)
