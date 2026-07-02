"""Canonical model core for memory-driven trajectory simulations."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .kernels import double_gaussian_gradient, exponential_weights

try:
    import numba
    from numba import njit

    _NUMBA_AVAILABLE = True
except ImportError:  # pragma: no cover
    _NUMBA_AVAILABLE = False

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


@dataclass(frozen=True)
class SimulationConfig:
    steps: int = 10_000
    dim: int = 3
    epsilon: float = 0.03
    eta: float = 0.15
    alpha: float = 0.002
    sigma_rep: float = 1.0
    sigma_att: float = 3.0
    amplitude_rep: float = 1.0
    amplitude_att: float = 0.35
    memory_factor: float = 6.0
    max_memory: int = 2_000
    burn_in: int = 0
    sample_every: int = 100


def _validate_config(config: SimulationConfig) -> None:
    if config.steps < 1:
        raise ValueError("steps must be positive")
    if config.dim < 1:
        raise ValueError("dim must be positive")
    if config.sample_every < 1:
        raise ValueError("sample_every must be positive")
    if config.max_memory < 1:
        raise ValueError("max_memory must be positive")
    if config.burn_in < 0:
        raise ValueError("burn_in must be non-negative")
    if not np.isfinite(config.memory_factor) or config.memory_factor <= 0.0:
        raise ValueError("memory_factor must be positive")
    if not np.isfinite(config.alpha) or not 0.0 < config.alpha <= 1.0:
        raise ValueError("alpha must satisfy 0 < alpha <= 1")
    if not np.isfinite(config.sigma_rep) or config.sigma_rep <= 0.0:
        raise ValueError("sigma_rep must be positive")
    if not np.isfinite(config.sigma_att) or config.sigma_att <= 0.0:
        raise ValueError("sigma_att must be positive")


def _horizon(config: SimulationConfig) -> int:
    return min(config.max_memory, max(1, int(config.memory_factor / config.alpha)))


def initialize_history(config: SimulationConfig) -> tuple[np.ndarray, int]:
    horizon = _horizon(config)
    return np.zeros((horizon, config.dim), dtype=float), 0


def update_history(
    history: np.ndarray,
    x: np.ndarray,
    filled: int,
) -> tuple[np.ndarray, int]:
    if filled < history.shape[0]:
        if filled > 0:
            history[1 : filled + 1] = history[:filled]
        filled += 1
    else:
        history[1:] = history[:-1]
    history[0] = x
    return history, filled


def finite_memory_step(
    x: np.ndarray,
    history: np.ndarray,
    weights: np.ndarray,
    config: SimulationConfig,
    *,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    if history.shape[0] and history.shape[0] > 0 and weights.size > 0:
        grad = double_gaussian_gradient(
            x,
            history,
            weights,
            sigma_rep=config.sigma_rep,
            sigma_att=config.sigma_att,
            amplitude_rep=config.amplitude_rep,
            amplitude_att=config.amplitude_att,
        )
    else:
        grad = np.zeros_like(x)
    if rng is None:
        rng = np.random.default_rng()
    noise = rng.normal(size=config.dim)
    return x + config.epsilon * noise - config.eta * grad


def simulate_finite_memory(
    config: SimulationConfig, *, seed: int = 0
) -> dict[str, np.ndarray]:
    _validate_config(config)
    rng = np.random.default_rng(seed)
    horizon = _horizon(config)
    weights = exponential_weights(config.alpha, horizon)

    history = np.zeros((horizon, config.dim), dtype=float)
    filled = 0
    x = np.zeros(config.dim, dtype=float)
    samples = []
    sample_steps = []

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
            samples.append(x.copy())
            sample_steps.append(step)

    return {
        "samples": np.asarray(samples, dtype=float),
        "sample_steps": np.asarray(sample_steps, dtype=int),
        "final_x": x.copy(),
        "memory": history[:filled].copy(),
        "weights": weights[:filled].copy(),
    }


@njit(cache=True)
def _exponential_weights_numba(alpha: float, horizon: int) -> np.ndarray:
    out = np.empty(horizon, np.float64)
    factor = 1.0 - alpha
    val = 1.0
    for i in range(horizon):
        out[i] = alpha * val
        val *= factor
    return out


@njit(cache=True)
def _gaussian_gradient_numba(
    x: np.ndarray,
    memory: np.ndarray,
    weights: np.ndarray,
    sigma: float,
    amplitude: float,
) -> np.ndarray:
    dim = x.shape[0]
    nmem = memory.shape[0]
    grad = np.zeros(dim, np.float64)
    if nmem == 0:
        return grad
    sigma2 = sigma * sigma
    for i in range(nmem):
        r2 = 0.0
        for d in range(dim):
            dx = x[d] - memory[i, d]
            r2 += dx * dx
        fac = amplitude * np.exp(-0.5 * r2 / sigma2) / sigma2
        for d in range(dim):
            grad[d] += weights[i] * fac * (x[d] - memory[i, d])
    return grad


@njit(cache=True)
def _double_gaussian_gradient_numba(
    x: np.ndarray,
    memory: np.ndarray,
    weights: np.ndarray,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float,
    amplitude_att: float,
) -> np.ndarray:
    rep = _gaussian_gradient_numba(x, memory, weights, sigma_rep, amplitude_rep)
    att = _gaussian_gradient_numba(x, memory, weights, sigma_att, amplitude_att)
    return rep - att


@njit(cache=True)
def _simulate_finite_memory_numba(
    steps: int,
    dim: int,
    epsilon: float,
    eta: float,
    alpha: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float,
    amplitude_att: float,
    memory_factor: float,
    max_memory: int,
    burn_in: int,
    sample_every: int,
    seed: int,
):
    if steps < 1:
        raise ValueError("steps must be positive")
    if dim < 1:
        raise ValueError("dim must be positive")
    if sample_every < 1:
        raise ValueError("sample_every must be positive")

    np.random.seed(seed)
    horizon = min(max_memory, max(1, int(memory_factor / alpha)))
    weights = _exponential_weights_numba(alpha, horizon)
    history = np.zeros((horizon, dim), np.float64)
    filled = 0
    x = np.zeros(dim, np.float64)
    max_samples = steps // sample_every + 2
    samples = np.zeros((max_samples, dim), np.float64)
    sample_steps = np.zeros(max_samples, np.int64)
    n_sample = 0

    for step in range(1, steps + 1):
        if filled:
            grad = _double_gaussian_gradient_numba(
                x,
                history[:filled],
                weights[:filled],
                sigma_rep,
                sigma_att,
                amplitude_rep,
                amplitude_att,
            )
        else:
            grad = np.zeros(dim, np.float64)

        noise = np.empty(dim, np.float64)
        for d in range(dim):
            noise[d] = np.random.normal(0.0, 1.0)
        x = x + epsilon * noise - eta * grad

        if filled < horizon:
            if filled > 0:
                for j in range(filled, 0, -1):
                    history[j] = history[j - 1]
            filled += 1
        else:
            for j in range(horizon - 1, 0, -1):
                history[j] = history[j - 1]
        history[0] = x

        if step >= burn_in and step % sample_every == 0:
            samples[n_sample] = x
            sample_steps[n_sample] = step
            n_sample += 1

    return samples[:n_sample], sample_steps[:n_sample], x, history, weights, n_sample, filled


def simulate_finite_memory_numba(
    config: SimulationConfig, *, seed: int = 0
) -> dict[str, np.ndarray]:
    if not _NUMBA_AVAILABLE:
        raise ImportError("numba is not installed")
    _validate_config(config)
    samples, sample_steps, x, history, weights, n_sample, filled = (
        _simulate_finite_memory_numba(
            config.steps,
            config.dim,
            config.epsilon,
            config.eta,
            config.alpha,
            config.sigma_rep,
            config.sigma_att,
            config.amplitude_rep,
            config.amplitude_att,
            config.memory_factor,
            config.max_memory,
            config.burn_in,
            config.sample_every,
            seed,
        )
    )
    return {
        "samples": samples[:n_sample],
        "sample_steps": sample_steps[:n_sample],
        "final_x": x.copy(),
        "memory": history[:filled].copy(),
        "weights": weights[:filled].copy(),
    }
