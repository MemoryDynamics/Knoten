"""Finite Gaussian influence reference, not a quantization of the native FIFO."""

import numpy as np


def _arrays(histories, response, noise):
    if any(np.iscomplexobj(item) for item in (histories, response, noise)):
        raise ValueError("histories, response and noise must be real")
    paths, response, noise = (
        np.asarray(item, dtype=float) for item in (histories, response, noise)
    )
    if paths.ndim != 2 or min(paths.shape) < 1:
        raise ValueError("histories must have shape (paths, times)")
    size = paths.shape[1]
    if response.shape != (size, size) or noise.shape != response.shape:
        raise ValueError("response and noise must be square matrices on the same times")
    if not all(np.isfinite(item).all() for item in (paths, response, noise)):
        raise ValueError("histories, response and noise must be finite")
    if not np.array_equal(noise, noise.T):
        raise ValueError("noise must be symmetric")
    return paths, response, noise


def influence_matrix(histories, response, noise):
    """Evaluate the ansatz without assuming positivity."""
    paths, response, noise = _arrays(histories, response, noise)
    difference = paths[:, None] - paths[None, :]
    mean = (paths[:, None] + paths[None, :]) / 2
    phase = np.einsum("ijk,kl,ijl->ij", difference, response, mean)
    decay = np.einsum("ijk,kl,ijl->ij", difference, noise, difference) / 2
    return np.exp(1j * phase - decay)


def vacuum_displacement_matrix(histories, response, noise):
    """Realize admissible causal data by chronological vacuum displacements."""
    paths, response, noise = _arrays(histories, response, noise)
    if np.any(np.triu(response, k=1)):
        raise ValueError("response must be causal")
    covariance = noise + 0.5j * (response - response.T)
    eigenvalues, vectors = np.linalg.eigh(covariance)
    tolerance = 32 * np.finfo(float).eps * np.max(np.abs(eigenvalues))
    if np.min(eigenvalues) < -tolerance:
        raise ValueError("noise is below the Gaussian positivity bound")
    couplings = (vectors * np.sqrt(np.maximum(eigenvalues, 0))).T
    amplitudes = np.zeros((len(paths), paths.shape[1]), dtype=complex)
    phase = (paths**2 @ np.diag(response)) / 2
    for column, coupling in zip(paths.T, couplings.T, strict=True):
        displacement = column[:, None] * coupling
        phase -= np.sum(displacement.conj() * amplitudes, axis=1).imag
        amplitudes += displacement
    overlap = amplitudes @ amplitudes.conj().T
    norm = overlap.diagonal().real
    return np.exp(
        overlap
        - (norm[:, None] + norm[None, :]) / 2
        + 1j * (phase[:, None] - phase[None, :])
    )
