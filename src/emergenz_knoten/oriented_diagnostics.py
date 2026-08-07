"""Diagnostics for controlled one-way oriented-memory responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .oriented_source import OrientedMemoryState, OrientedOneWayResponse


@dataclass(frozen=True)
class OrientedMemoryMoments:
    """Rotation-covariant moments of every retained oriented deposit."""

    total_weight: float
    center: np.ndarray
    rms_radius: float
    polarization: np.ndarray
    polarization_coherence: float
    circulation_bivector: np.ndarray
    circulation_coherence: float
    orientation_power: float


def oriented_memory_moments(state: OrientedMemoryState) -> OrientedMemoryMoments:
    """Summarize the full retained vector fibre without selecting coordinates.

    The polarization is a polar vector. The circulation bivector is an
    antisymmetric rank-2 tensor; only in three dimensions may it be dualized to
    an axial vector. Neither observable is a quantized spin or a charge.
    """

    positions = np.asarray(state.scalar_state.memory, dtype=float)
    orientations = np.asarray(state.orientations, dtype=float)
    weights = np.asarray(state.weights, dtype=float)
    mass = float(np.sum(weights))
    dim = state.dim
    if mass <= 0.0:
        return OrientedMemoryMoments(
            total_weight=0.0,
            center=np.zeros(dim, dtype=float),
            rms_radius=0.0,
            polarization=np.zeros(dim, dtype=float),
            polarization_coherence=0.0,
            circulation_bivector=np.zeros((dim, dim), dtype=float),
            circulation_coherence=0.0,
            orientation_power=0.0,
        )

    normalized = weights / mass
    center = np.sum(normalized[:, None] * positions, axis=0)
    radial = positions - center
    polarization = np.sum(normalized[:, None] * orientations, axis=0)
    absolute_polarization = float(
        np.sum(weights * np.linalg.norm(orientations, axis=1))
    )
    polarization_coherence = (
        float(
            np.linalg.norm(np.sum(weights[:, None] * orientations, axis=0))
            / absolute_polarization
        )
        if absolute_polarization > 0.0
        else 0.0
    )

    wedges = (
        radial[:, :, None] * orientations[:, None, :]
        - orientations[:, :, None] * radial[:, None, :]
    )
    circulation = np.sum(normalized[:, None, None] * wedges, axis=0)
    absolute_circulation = float(
        np.sum(weights * np.linalg.norm(wedges, axis=(1, 2)))
    )
    circulation_coherence = (
        float(
            np.linalg.norm(np.sum(weights[:, None, None] * wedges, axis=0))
            / absolute_circulation
        )
        if absolute_circulation > 0.0
        else 0.0
    )
    rms_radius = float(
        np.sqrt(np.sum(normalized * np.einsum("ij,ij->i", radial, radial)))
    )
    orientation_power = float(
        np.sum(normalized * np.einsum("ij,ij->i", orientations, orientations))
    )
    return OrientedMemoryMoments(
        total_weight=mass,
        center=center,
        rms_radius=rms_radius,
        polarization=polarization,
        polarization_coherence=polarization_coherence,
        circulation_bivector=circulation,
        circulation_coherence=circulation_coherence,
        orientation_power=orientation_power,
    )


def random_sign_memory_coherences(
    state: OrientedMemoryState,
    random_signs: Any,
) -> tuple[np.ndarray, np.ndarray]:
    """Return polarization and circulation coherences for deposit-sign nulls."""

    signs = np.asarray(random_signs, dtype=float)
    n_memory = state.scalar_state.n_memory
    if (
        signs.ndim != 2
        or signs.shape[1] != n_memory
        or not np.isfinite(signs).all()
        or not np.all(np.isin(signs, (-1.0, 1.0)))
    ):
        raise ValueError("random_signs must contain +/-1 with shape (draws, memory)")
    weights = np.asarray(state.weights, dtype=float)
    orientations = np.asarray(state.orientations, dtype=float)
    mass = float(np.sum(weights))
    if mass <= 0.0:
        zeros = np.zeros(signs.shape[0], dtype=float)
        return zeros, zeros.copy()

    center = np.sum(
        (weights / mass)[:, None] * state.scalar_state.memory,
        axis=0,
    )
    radial = state.scalar_state.memory - center
    weighted_orientations = weights[:, None] * orientations
    polarization_sums = signs @ weighted_orientations
    polarization_denominator = float(
        np.sum(weights * np.linalg.norm(orientations, axis=1))
    )
    if polarization_denominator > 0.0:
        polarization = (
            np.linalg.norm(polarization_sums, axis=1) / polarization_denominator
        )
    else:
        polarization = np.zeros(signs.shape[0], dtype=float)

    wedges = (
        radial[:, :, None] * orientations[:, None, :]
        - orientations[:, :, None] * radial[:, None, :]
    )
    circulation_sums = np.einsum(
        "rn,n,nij->rij",
        signs,
        weights,
        wedges,
    )
    circulation_denominator = float(
        np.sum(weights * np.linalg.norm(wedges, axis=(1, 2)))
    )
    if circulation_denominator > 0.0:
        circulation = (
            np.linalg.norm(circulation_sums, axis=(1, 2))
            / circulation_denominator
        )
    else:
        circulation = np.zeros(signs.shape[0], dtype=float)
    return polarization, circulation


def normalized_shape_spectra(shape_tensors: Any) -> np.ndarray:
    """Return non-negative, trace-normalized eigenvalue spectra."""

    tensors = np.asarray(shape_tensors, dtype=float)
    if (
        tensors.ndim != 3
        or tensors.shape[1] != tensors.shape[2]
        or not np.isfinite(tensors).all()
    ):
        raise ValueError("shape_tensors must be finite with shape (samples, dim, dim)")
    values = np.linalg.eigvalsh(tensors)
    values = np.clip(values, 0.0, None)
    totals = np.sum(values, axis=-1, keepdims=True)
    return np.divide(values, totals, out=np.zeros_like(values), where=totals > 0.0)


def oriented_response_metrics(
    response: OrientedOneWayResponse,
    *,
    radius: float,
    radial_direction: Any,
    random_quantile: float,
) -> dict[str, Any]:
    """Measure active response against paired off, flip, and random-sign paths."""

    if not np.isfinite(radius) or radius <= 0.0:
        raise ValueError("radius must be positive")
    if not 0.5 < random_quantile < 1.0:
        raise ValueError("random_quantile must lie between 0.5 and 1")
    radial = np.asarray(radial_direction, dtype=float)
    if radial.shape != (response.target_positions.shape[-1],):
        raise ValueError("radial_direction must match response dimension")
    radial_norm = float(np.linalg.norm(radial))
    if not np.isfinite(radial).all() or radial_norm <= 0.0:
        raise ValueError("radial_direction must be finite and non-zero")
    radial = radial / radial_norm

    centers = np.asarray(response.target_memory_centers, dtype=float)
    active_delta = centers[:, 0] - centers[:, 2]
    flip_delta = centers[:, 1] - centers[:, 2]
    random_delta = centers[:, 3:] - centers[:, 2, None, :]
    active_norm = np.linalg.norm(active_delta, axis=1)
    flip_norm = np.linalg.norm(flip_delta, axis=1)
    random_norm = np.linalg.norm(random_delta, axis=2)
    random_threshold = np.quantile(random_norm, random_quantile, axis=1)
    final_active = active_delta[-1]
    final_flip = flip_delta[-1]
    final_active_norm = float(active_norm[-1])
    final_flip_norm = float(flip_norm[-1])
    tiny = np.finfo(float).tiny
    flip_cosine = float(
        np.dot(final_active, final_flip)
        / max(final_active_norm * final_flip_norm, tiny)
    )
    tangential = final_active - np.dot(final_active, radial) * radial
    tangential_fraction = float(
        np.linalg.norm(tangential) / max(final_active_norm, tiny)
    )

    active_radius = np.asarray(response.target_radius_ratios[:, 0], dtype=float)
    off_radius = np.asarray(response.target_radius_ratios[:, 2], dtype=float)
    radius_ratio = np.divide(
        active_radius,
        off_radius,
        out=np.ones_like(active_radius),
        where=np.abs(off_radius) > tiny,
    )
    target_radius_change = float(np.max(np.abs(radius_ratio - 1.0)))
    active_tensors = np.asarray(response.target_shape_tensors[:, 0], dtype=float)
    off_tensors = np.asarray(response.target_shape_tensors[:, 2], dtype=float)
    tensor_denominator = np.maximum(
        np.trace(off_tensors, axis1=1, axis2=2),
        tiny,
    )
    target_shape_change = float(
        np.max(
            np.linalg.norm(active_tensors - off_tensors, axis=(1, 2))
            / tensor_denominator
        )
    )
    source_spectra = normalized_shape_spectra(response.source_shape_tensors)
    source_spectrum_drift = float(
        np.max(np.linalg.norm(source_spectra - source_spectra[0], axis=1))
    )
    final_random_threshold = float(random_threshold[-1])
    return {
        "active_response_r": final_active_norm / radius,
        "active_response_vector_r": final_active / radius,
        "random_threshold_r": final_random_threshold / radius,
        "null_separation": final_active_norm / max(final_random_threshold, tiny),
        "flip_cosine": flip_cosine,
        "flip_magnitude_ratio": final_flip_norm / max(final_active_norm, tiny),
        "tangential_fraction": tangential_fraction,
        "target_radius_max_change": target_radius_change,
        "target_shape_max_change": target_shape_change,
        "source_radius_max_change": float(
            np.max(np.abs(response.source_radius_ratios - 1.0))
        ),
        "source_spectrum_max_drift": source_spectrum_drift,
        "carrier_initial_norm": float(
            np.linalg.norm(response.source_carrier_orientations[0])
        ),
        "carrier_final_norm": float(
            np.linalg.norm(response.source_carrier_orientations[-1])
        ),
        "trace_active_response_r": active_norm / radius,
        "trace_random_threshold_r": random_threshold / radius,
    }
