"""Core utilities for the Emergenz Knoten model."""

from .diagnostics import (
    bootstrap_mean_ci,
    covariance_dimension,
    occupancy_dimension,
    residence_statistics,
    spectral_dimension,
)
from .kernels import double_gaussian_gradient, exponential_weights, gaussian_gradient
from .simulation import (
    SimulationConfig,
    simulate_finite_memory,
    simulate_finite_memory_numba,
)

__all__ = [
    "SimulationConfig",
    "bootstrap_mean_ci",
    "covariance_dimension",
    "double_gaussian_gradient",
    "exponential_weights",
    "gaussian_gradient",
    "occupancy_dimension",
    "residence_statistics",
    "simulate_finite_memory",
    "simulate_finite_memory_numba",
    "spectral_dimension",
]
