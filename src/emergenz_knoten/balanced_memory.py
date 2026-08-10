"""Balanced finite-horizon diagnostics for the passive oriented-memory delay line."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse.linalg import LinearOperator, svds


@dataclass(frozen=True)
class BalancedMemorySpectrum:
    """Leading finite-horizon Hankel singular values and state-space modes."""

    singular_values: np.ndarray
    state_modes: np.ndarray
    energy_fractions: np.ndarray
    gap_ratios: np.ndarray
    total_hankel_energy: float
    tail_energy_relative_se: float


def passive_delay_reachability(
    n_memory: int,
    horizon: int,
    *,
    carrier_decay: float,
    deposition_gain: float,
) -> np.ndarray:
    """Return ``[B, AB, ...]`` for one component of the passive delay line.

    The state is ``(p_n, m_{n,1}, ..., m_{n,H-1})``. Its homogeneous update is
    ``p' = q p`` and ``m'_1 = p, m'_j = m_{j-1}``; the trajectory direction
    enters the carrier with ``B = deposition_gain * e_0``.
    """

    if n_memory < 1 or horizon < 1:
        raise ValueError("n_memory and horizon must be positive")
    q = float(carrier_decay)
    beta = float(deposition_gain)
    if not np.isfinite(q) or not 0.0 <= q < 1.0:
        raise ValueError("carrier_decay must lie in [0, 1)")
    if not np.isfinite(beta) or beta < 0.0:
        raise ValueError("deposition_gain must be finite and non-negative")

    ages = np.arange(n_memory)[:, None]
    powers = np.arange(horizon)[None, :]
    active = ages <= powers
    exponents = np.maximum(powers - ages, 0)
    return np.where(active, beta * np.power(q, exponents), 0.0)


def observation_block_weights(sample_steps: np.ndarray) -> np.ndarray:
    """Return endpoint block widths for cadence-comparable observations."""

    steps = np.asarray(sample_steps, dtype=int)
    if (
        steps.ndim != 1
        or steps.size < 1
        or steps[0] != 0
        or np.any(np.diff(steps) <= 0)
    ):
        raise ValueError("sample_steps must start at zero and increase strictly")
    widths = np.ones(steps.size, dtype=float)
    if steps.size > 1:
        widths[1:] = np.diff(steps)
    return widths


def passive_delay_observability(
    readout_rows: np.ndarray,
    sample_steps: np.ndarray,
    *,
    carrier_decay: float,
    block_weighted: bool = True,
) -> np.ndarray:
    """Map an initial full-memory perturbation to sampled future readouts.

    ``readout_rows[t, j]`` is the scalar coefficient multiplying orientation
    age ``j`` at the corresponding absolute sample step. The returned matrix
    contains ``C_t A^t`` without materializing the delay operator.
    """

    rows = np.asarray(readout_rows, dtype=float)
    steps = np.asarray(sample_steps, dtype=int)
    if (
        rows.ndim != 2
        or rows.shape[0] != steps.size
        or rows.shape[1] < 1
        or not np.isfinite(rows).all()
    ):
        raise ValueError("readout_rows must be finite and match sample_steps")
    if steps[0] != 0 or np.any(np.diff(steps) <= 0) or np.any(steps < 0):
        raise ValueError("sample_steps must start at zero and increase strictly")
    q = float(carrier_decay)
    if not np.isfinite(q) or not 0.0 <= q < 1.0:
        raise ValueError("carrier_decay must lie in [0, 1)")

    n_memory = rows.shape[1]
    result = np.zeros_like(rows)
    for index, step in enumerate(steps):
        retained = min(int(step), n_memory - 1)
        ages = np.arange(retained + 1)
        result[index, 0] = np.dot(
            rows[index, : retained + 1],
            np.power(q, int(step) - ages),
        )
        remaining = n_memory - int(step) - 1
        if remaining > 0:
            result[index, 1 : remaining + 1] = rows[index, int(step) + 1 :]
    if block_weighted:
        result *= np.sqrt(observation_block_weights(steps))[:, None]
    return result


def gaussian_memory_readout_rows(
    probe_positions: np.ndarray,
    memory_positions: np.ndarray,
    weights: np.ndarray,
    *,
    kernel_sigma: float,
) -> np.ndarray:
    """Evaluate the existing Gaussian field readout for every retained age."""

    probes = np.asarray(probe_positions, dtype=float)
    memories = np.asarray(memory_positions, dtype=float)
    mass = np.asarray(weights, dtype=float)
    if (
        probes.ndim != 2
        or memories.ndim != 3
        or probes.shape[0] != memories.shape[0]
        or probes.shape[1] != memories.shape[2]
        or mass.shape != (memories.shape[1],)
        or not np.isfinite(probes).all()
        or not np.isfinite(memories).all()
        or not np.isfinite(mass).all()
    ):
        raise ValueError("probe, memory and weight shapes must be compatible")
    if np.any(mass < 0.0):
        raise ValueError("weights must be non-negative")
    sigma = float(kernel_sigma)
    if not np.isfinite(sigma) or sigma <= 0.0:
        raise ValueError("kernel_sigma must be positive")
    differences = probes[:, None, :] - memories
    radius2 = np.einsum("thd,thd->th", differences, differences)
    return mass[None, :] * np.exp(-0.5 * radius2 / sigma**2)


def balanced_hankel_spectrum(
    observability: np.ndarray,
    reachability: np.ndarray,
    *,
    max_modes: int = 12,
    random_seed: int = 0,
    energy_probe_count: int = 128,
) -> BalancedMemorySpectrum:
    """Estimate leading singular modes of ``observability @ reachability``.

    A linear operator keeps the calculation memory-light for long horizons.
    State modes are the orthonormalized reachable images of the right Hankel
    singular vectors. Their span, not their arbitrary signs, is compared.
    """

    observable = np.asarray(observability, dtype=float)
    reachable = np.asarray(reachability, dtype=float)
    if (
        observable.ndim != 2
        or reachable.ndim != 2
        or observable.shape[1] != reachable.shape[0]
        or not np.isfinite(observable).all()
        or not np.isfinite(reachable).all()
    ):
        raise ValueError("observability and reachability must be compatible")
    if max_modes < 1 or energy_probe_count < 2:
        raise ValueError("max_modes must be positive and energy probes at least two")
    shape = (observable.shape[0], reachable.shape[1])
    available = min(shape)
    if available < 1:
        raise ValueError("Hankel operator must be non-empty")
    requested = min(max_modes + 1, available)

    exact_spectrum = requested == available or available <= 24
    if exact_spectrum:
        _, all_singular_values, right = np.linalg.svd(
            observable @ reachable, full_matrices=False
        )
        total_energy = float(np.dot(all_singular_values, all_singular_values))
        singular_values = all_singular_values[:requested]
        right = right[:requested].T
        tail_relative_se = 0.0
    else:
        operator = LinearOperator(
            shape,
            matvec=lambda value: observable @ (reachable @ value),
            rmatvec=lambda value: reachable.T @ (observable.T @ value),
            matmat=lambda value: observable @ (reachable @ value),
            rmatmat=lambda value: reachable.T @ (observable.T @ value),
            dtype=float,
        )
        _, singular_values, right_transposed = svds(
            operator,
            k=requested,
            which="LM",
            return_singular_vectors=True,
            rng=np.random.default_rng(random_seed),
        )
        order = np.argsort(singular_values)[::-1]
        singular_values = singular_values[order]
        right = right_transposed[order].T

        # Estimate only the energy outside the computed right-singular
        # subspace. Normalizing by the returned singular values alone would
        # make every truncated spectrum appear spuriously low-rank.
        rng = np.random.default_rng(random_seed + 1)
        probes = rng.choice((-1.0, 1.0), size=(shape[1], energy_probe_count))
        probes -= right @ (right.T @ probes)
        residual_outputs = observable @ (reachable @ probes)
        residual_energies = np.einsum("ij,ij->j", residual_outputs, residual_outputs)
        tail_energy = max(0.0, float(np.mean(residual_energies)))
        tail_se = float(np.std(residual_energies, ddof=1)) / np.sqrt(energy_probe_count)
        leading_energy = float(np.dot(singular_values, singular_values))
        total_energy = leading_energy + tail_energy
        tail_relative_se = tail_se / max(total_energy, np.finfo(float).tiny)

    tolerance = np.finfo(float).eps * max(shape) * max(1.0, float(singular_values[0]))
    supported = singular_values > tolerance
    singular_values = singular_values[supported]
    right = right[:, supported]
    if singular_values.size == 0:
        return BalancedMemorySpectrum(
            singular_values=np.zeros(0),
            state_modes=np.zeros((reachable.shape[0], 0)),
            energy_fractions=np.zeros(0),
            gap_ratios=np.zeros(0),
            total_hankel_energy=0.0,
            tail_energy_relative_se=0.0,
        )

    raw_modes = reachable @ right
    modes, _ = np.linalg.qr(raw_modes, mode="reduced")
    squared = singular_values**2
    energy = np.cumsum(squared) / max(total_energy, np.finfo(float).tiny)
    gaps = np.divide(
        singular_values[:-1],
        singular_values[1:],
        out=np.full(max(0, singular_values.size - 1), np.inf),
        where=singular_values[1:] > 0.0,
    )
    return BalancedMemorySpectrum(
        singular_values=singular_values,
        state_modes=modes,
        energy_fractions=energy,
        gap_ratios=gaps,
        total_hankel_energy=total_energy,
        tail_energy_relative_se=tail_relative_se,
    )


def select_balanced_rank(
    spectrum: BalancedMemorySpectrum,
    *,
    max_rank: int = 8,
    minimum_gap: float = 3.0,
    minimum_energy: float = 0.90,
) -> int | None:
    """Return the first preregistered low-rank gap satisfying both gates."""

    if max_rank < 1:
        raise ValueError("max_rank must be positive")
    if minimum_gap <= 1.0 or not 0.0 < minimum_energy <= 1.0:
        raise ValueError("invalid gap or energy threshold")
    limit = min(max_rank, spectrum.gap_ratios.size)
    for index in range(limit):
        if (
            spectrum.gap_ratios[index] >= minimum_gap
            and spectrum.energy_fractions[index] >= minimum_energy
        ):
            return index + 1
    return None


def minimum_principal_cosine(left: np.ndarray, right: np.ndarray) -> float:
    """Return the weakest principal-axis overlap of two equal-rank subspaces."""

    first = np.asarray(left, dtype=float)
    second = np.asarray(right, dtype=float)
    if (
        first.ndim != 2
        or second.ndim != 2
        or first.shape[0] != second.shape[0]
        or first.shape[1] != second.shape[1]
        or first.shape[1] < 1
        or not np.isfinite(first).all()
        or not np.isfinite(second).all()
    ):
        raise ValueError("subspace bases must be finite, equal-rank matrices")
    q_left, _ = np.linalg.qr(first, mode="reduced")
    q_right, _ = np.linalg.qr(second, mode="reduced")
    values = np.linalg.svd(q_left.T @ q_right, compute_uv=False)
    return float(np.clip(values[-1], 0.0, 1.0))


def randomized_holdout_error(
    observability: np.ndarray,
    reachability: np.ndarray,
    state_modes: np.ndarray,
    *,
    probe_count: int = 64,
    random_seed: int = 0,
) -> float:
    """Estimate Hankel-output loss after projection onto selected state modes."""

    observable = np.asarray(observability, dtype=float)
    reachable = np.asarray(reachability, dtype=float)
    modes = np.asarray(state_modes, dtype=float)
    if (
        observable.ndim != 2
        or reachable.ndim != 2
        or modes.ndim != 2
        or observable.shape[1] != reachable.shape[0]
        or modes.shape[0] != reachable.shape[0]
        or modes.shape[1] < 1
        or probe_count < 1
        or not np.isfinite(observable).all()
        or not np.isfinite(reachable).all()
        or not np.isfinite(modes).all()
    ):
        raise ValueError("holdout factors and state modes are incompatible")
    q_modes, _ = np.linalg.qr(modes, mode="reduced")
    rng = np.random.default_rng(random_seed)
    probes = rng.normal(size=(reachable.shape[1], probe_count))
    states = reachable @ probes
    truth = observable @ states
    approximation = observable @ (q_modes @ (q_modes.T @ states))
    denominator = max(float(np.linalg.norm(truth)), np.finfo(float).tiny)
    return float(np.linalg.norm(truth - approximation) / denominator)
