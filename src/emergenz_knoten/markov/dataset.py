"""Sample-index datasets for augmented finite-memory Markov estimates."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..core import SimulationConfig
from ..kernels import (
    double_gaussian_gradient,
    exponential_memory_weights,
)
from .features import augmented_feature_names, memory_summary_features


@dataclass(frozen=True)
class AugmentedTrajectory:
    """Reduced sampled trajectory of augmented states ``z_i``.

    ``sample_steps`` stores the original update indices ``n``. The row index
    ``i`` of ``augmented_features`` is only a sample counter, not physical time.
    """

    samples: np.ndarray
    sample_steps: np.ndarray
    augmented_features: np.ndarray
    feature_names: np.ndarray
    final_x: np.ndarray
    memory: np.ndarray
    weights: np.ndarray

    def as_dict(self) -> dict[str, np.ndarray]:
        """Return the legacy dictionary representation."""

        return {
            "samples": self.samples,
            "sample_steps": self.sample_steps,
            "augmented_features": self.augmented_features,
            "feature_names": self.feature_names,
            "final_x": self.final_x,
            "memory": self.memory,
            "weights": self.weights,
        }


@dataclass(frozen=True)
class LaggedDataset:
    """Lagged pairs of sampled augmented states.

    ``sample_lag`` counts rows in the sampled feature array. ``lag_updates``
    is inferred from ``sample_steps`` when the update index spacing is known.
    No continuum or physical-time parametrization is assumed.
    """

    current: np.ndarray
    future: np.ndarray
    current_sample_steps: np.ndarray | None
    future_sample_steps: np.ndarray | None
    sample_lag: int
    lag_updates: int | None


def _validate_config(config: SimulationConfig) -> None:
    if config.steps < 1:
        raise ValueError("steps must be positive")
    if config.dim < 1:
        raise ValueError("dim must be positive")
    if config.sample_every < 1:
        raise ValueError("sample_every must be positive")
    if config.max_memory < 1:
        raise ValueError("max_memory must be positive")
    if not 0.0 < config.alpha <= 1.0:
        raise ValueError("alpha must satisfy 0 < alpha <= 1")
    if not np.isfinite(config.memory_mass) or config.memory_mass < 0.0:
        raise ValueError("memory_mass must be non-negative")
    if config.deposition_kernel not in {"delta", "gaussian", "matched_gaussian"}:
        raise ValueError("unknown deposition_kernel")
    if not np.isfinite(config.deposition_sigma) or config.deposition_sigma < 0.0:
        raise ValueError("deposition_sigma must be non-negative")
    if config.deposition_kernel == "delta" and config.deposition_sigma != 0.0:
        raise ValueError("deposition_sigma must be zero for delta deposition")
    if config.deposition_kernel == "gaussian" and config.deposition_sigma <= 0.0:
        raise ValueError("deposition_sigma must be positive for gaussian deposition")
    if config.deposition_kernel == "matched_gaussian" and config.deposition_sigma != 0.0:
        raise ValueError("deposition_sigma must be zero for matched_gaussian deposition")


def _horizon(config: SimulationConfig) -> int:
    return min(config.max_memory, max(1, int(config.memory_factor / config.alpha)))


def simulate_augmented_features(
    config: SimulationConfig,
    *,
    seed: int = 0,
    as_dataclass: bool = False,
) -> dict[str, np.ndarray] | AugmentedTrajectory:
    """Run the finite-memory model and record reduced augmented-state features."""

    _validate_config(config)
    rng = np.random.default_rng(seed)
    horizon = _horizon(config)
    weights = exponential_memory_weights(
        config.alpha,
        horizon,
        memory_mass=config.memory_mass,
    )
    history = np.zeros((horizon, config.dim), dtype=float)
    filled = 0
    x = np.zeros(config.dim, dtype=float)
    samples: list[np.ndarray] = []
    sample_steps: list[int] = []
    features: list[np.ndarray] = []

    for step in range(1, config.steps + 1):
        if filled:
            grad = double_gaussian_gradient(
                x,
                history[:filled],
                weights[:filled],
                sigma_rep=config.sigma_rep,
                sigma_att=config.sigma_att,
                amplitude_rep=config.amplitude_rep,
                amplitude_att=config.amplitude_att,
                deposition_kernel=config.deposition_kernel,
                deposition_sigma=config.deposition_sigma,
            )
        else:
            grad = np.zeros(config.dim, dtype=float)

        x = x + config.epsilon * rng.normal(size=config.dim) - config.eta * grad

        if filled < horizon:
            if filled > 0:
                history[1 : filled + 1] = history[:filled]
            filled += 1
        else:
            history[1:] = history[:-1]
        history[0] = x

        if step >= config.burn_in and step % config.sample_every == 0:
            current_memory = history[:filled].copy()
            current_weights = weights[:filled].copy()
            samples.append(x.copy())
            sample_steps.append(step)
            features.append(memory_summary_features(x, current_memory, current_weights))

    trajectory = AugmentedTrajectory(
        samples=np.asarray(samples, dtype=float),
        sample_steps=np.asarray(sample_steps, dtype=int),
        augmented_features=np.asarray(features, dtype=float),
        feature_names=np.asarray(augmented_feature_names(config.dim), dtype=str),
        final_x=x.copy(),
        memory=history[:filled].copy(),
        weights=weights[:filled].copy(),
    )
    if as_dataclass:
        return trajectory
    return trajectory.as_dict()


def lagged_pairs(
    features: np.ndarray,
    *,
    sample_lag: int = 1,
    sample_steps: np.ndarray | None = None,
) -> LaggedDataset:
    """Return lagged pairs ``(z_i, z_{i+sample_lag})`` from sampled features."""

    arr = np.asarray(features, dtype=float)
    if arr.ndim != 2:
        raise ValueError("features must be a 2D array")
    if sample_lag < 1:
        raise ValueError("sample_lag must be positive")
    if arr.shape[0] <= sample_lag:
        raise ValueError("need more feature rows than sample_lag")

    current_steps: np.ndarray | None = None
    future_steps: np.ndarray | None = None
    lag_updates: int | None = None
    if sample_steps is not None:
        steps = np.asarray(sample_steps, dtype=int)
        if steps.ndim != 1:
            raise ValueError("sample_steps must be a 1D array")
        if steps.shape[0] != arr.shape[0]:
            raise ValueError("sample_steps length must match features")
        current_steps = steps[:-sample_lag].copy()
        future_steps = steps[sample_lag:].copy()
        update_lags = future_steps - current_steps
        if np.all(update_lags == update_lags[0]):
            lag_updates = int(update_lags[0])

    return LaggedDataset(
        current=arr[:-sample_lag].copy(),
        future=arr[sample_lag:].copy(),
        current_sample_steps=current_steps,
        future_sample_steps=future_steps,
        sample_lag=int(sample_lag),
        lag_updates=lag_updates,
    )
