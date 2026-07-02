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
    shape_statistics,
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
from .knot_score import (
    best_residence_memory_times,
    occupancy_dimension_value,
    score_against_control,
    shape_roundness_value,
    threshold_score,
    voxel_stability_ratio,
)
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
    "best_residence_memory_times",
    "bootstrap_mean_ci",
    "covariance_dimension",
    "fit_occupancy_scaling_window",
    "double_gaussian_gradient",
    "exponential_weights",
    "gaussian_gradient",
    "lagged_cross_correlation",
    "load_simulation_result",
    "occupancy_dimension",
    "occupancy_dimension_value",
    "occupancy_local_slopes",
    "phase_locking_value",
    "radius_from_shape",
    "residence_statistics",
    "shape_roundness_value",
    "response_rank",
    "run_simulation",
    "save_simulation_result",
    "score_against_control",
    "shape_statistics",
    "shape_tensor",
    "simulate_finite_memory",
    "simulate_finite_memory_numba",
    "spectral_dimension",
    "threshold_score",
    "voxel_stability_ratio",
]
