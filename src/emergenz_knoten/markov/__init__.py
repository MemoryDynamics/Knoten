"""Markov and transfer-operator utilities for augmented finite-memory states.

This package deliberately uses update/sample-index language. It estimates
operators from sampled augmented states ``z_i``; no physical time
reparametrization is assumed here.
"""

from .dataset import (
    AugmentedTrajectory,
    LaggedDataset,
    lagged_pairs,
    simulate_augmented_features,
)
from .features import (
    augmented_feature_names,
    memory_summary_features,
    memory_weight_in_ball,
)
from .metastability import (
    leading_nontrivial_eigenvalues,
    spectral_gap,
)
from .transition import (
    TransferOperatorEstimate,
    estimate_transfer_operator,
    row_stochastic_matrix,
    transition_count_matrix,
    voxel_labels,
)
from .validation import (
    ballistic_scaling_slope,
    chapman_kolmogorov_error,
    critical_eta,
    critical_gamma,
    implied_relaxation_rates,
    implied_timescales,
    mean_squared_displacement,
    self_consistency_residual,
    vector_autocorrelation,
)

__all__ = [
    "AugmentedTrajectory",
    "LaggedDataset",
    "TransferOperatorEstimate",
    "augmented_feature_names",
    "ballistic_scaling_slope",
    "chapman_kolmogorov_error",
    "critical_eta",
    "critical_gamma",
    "estimate_transfer_operator",
    "implied_relaxation_rates",
    "implied_timescales",
    "lagged_pairs",
    "leading_nontrivial_eigenvalues",
    "mean_squared_displacement",
    "memory_summary_features",
    "memory_weight_in_ball",
    "row_stochastic_matrix",
    "self_consistency_residual",
    "simulate_augmented_features",
    "spectral_gap",
    "transition_count_matrix",
    "vector_autocorrelation",
    "voxel_labels",
]
