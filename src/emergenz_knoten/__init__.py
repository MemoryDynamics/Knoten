"""Core utilities for the Emergenz Knoten model."""

from .core import (
    SimulationConfig,
    simulate_finite_memory,
    simulate_finite_memory_numba,
)
from .diagnostics import (
    bootstrap_mean_ci,
    covariance_dimension,
    fit_occupancy_scaling_window,
    occupancy_dimension,
    occupancy_local_slopes,
    residence_statistics,
    spectral_dimension,
)
from .experiments import (
    SimulationResult,
    SimulationRunner,
    load_simulation_result,
    run_simulation,
    save_simulation_result,
)
from .kernels import double_gaussian_gradient, exponential_weights, gaussian_gradient
from .synchronization import (
    LaggedCorrelationResult,
    ResponseRankResult,
    lagged_cross_correlation,
    phase_locking_value,
    radius_from_shape,
    response_rank,
    shape_tensor,
)

__all__ = [
    "LaggedCorrelationResult",
    "ResponseRankResult",
    "SimulationConfig",
    "SimulationRunner",
    "SimulationResult",
    "bootstrap_mean_ci",
    "covariance_dimension",
    "fit_occupancy_scaling_window",
    "double_gaussian_gradient",
    "exponential_weights",
    "gaussian_gradient",
    "lagged_cross_correlation",
    "load_simulation_result",
    "occupancy_dimension",
    "occupancy_local_slopes",
    "phase_locking_value",
    "radius_from_shape",
    "residence_statistics",
    "response_rank",
    "run_simulation",
    "save_simulation_result",
    "shape_tensor",
    "simulate_finite_memory",
    "simulate_finite_memory_numba",
    "spectral_dimension",
]
