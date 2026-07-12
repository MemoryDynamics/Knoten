from __future__ import annotations

import argparse
from dataclasses import asdict, replace
from datetime import UTC, datetime
import json
import math
from pathlib import Path
import subprocess
import sys
import time
from typing import Iterable

import numpy as np

def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()

sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    DEPOSITION_KERNELS,
    ball_residence_statistics,
    SimulationConfig,
    covariance_dimension,
    effective_double_gaussian_parameters,
    exponential_memory_weights,
    fit_occupancy_scaling_window,
    gaussian_gradient,
    matched_local_stiffness_renormalization,
    occupancy_dimension,
    residence_statistics,
    shape_statistics,
    simulate_finite_memory,
    zero_mean_attractive_amplitude,
)
from emergenz_knoten.markov import vector_autocorrelation  # noqa: E402

try:
    from numba import njit

    _NUMBA_AVAILABLE = True
except ImportError:  # pragma: no cover
    _NUMBA_AVAILABLE = False

    def njit(*args, **kwargs):  # type: ignore[no-redef]
        def wrapper(func):
            return func

        return wrapper


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def _parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one float")
    return values


def _parse_conditions(value: str) -> list[str]:
    allowed = {"baseline", "eta_zero", "single_scale", "rep_zero", "m0_zero", "alpha_one", "matched_deposition", "matched_deposition_renormalized", "zero_mean_two_scale"}
    values = [item.strip() for item in value.split(",") if item.strip()]
    unknown = sorted(set(values) - allowed)
    if unknown:
        raise argparse.ArgumentTypeError(f"unknown condition(s): {', '.join(unknown)}")
    if not values:
        raise argparse.ArgumentTypeError("expected at least one condition")
    return values



def _trace_targets(
    *,
    steps: int,
    burn_in: int,
    trace_every: int,
    trace_points: int,
    trace_spacing: str,
) -> np.ndarray:
    if trace_points > 0:
        start = max(1, burn_in)
        if trace_points == 1:
            raw = np.asarray([steps], dtype=float)
        elif trace_spacing == "linear":
            raw = np.linspace(start, steps, trace_points)
        elif trace_spacing == "log":
            raw = np.geomspace(start, steps, trace_points)
        else:
            raise ValueError(f"unknown trace spacing: {trace_spacing}")
        targets = np.unique(np.rint(raw).astype(np.int64))
        targets = targets[(targets >= start) & (targets <= steps)]
        if len(targets) == 0 or targets[-1] != steps:
            targets = np.unique(np.append(targets, np.int64(steps)))
        return targets.astype(np.int64)

    if trace_every <= 0:
        return np.empty(0, dtype=np.int64)
    start = max(1, burn_in)
    first = int(math.ceil(start / trace_every) * trace_every)
    if first > steps:
        return np.empty(0, dtype=np.int64)
    return np.arange(first, steps + 1, trace_every, dtype=np.int64)

def _git_output(args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return completed.stdout.strip()


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _horizon(config: SimulationConfig) -> int:
    return min(config.max_memory, max(1, int(config.memory_factor / config.alpha)))


def _stored_weight_mass(alpha: float, horizon: int, memory_mass: float) -> float:
    return float(memory_mass * (1.0 - (1.0 - alpha) ** horizon))


def _apply_condition(config: SimulationConfig, condition: str) -> SimulationConfig:
    if condition == "baseline":
        return config
    if condition == "eta_zero":
        return replace(config, eta=0.0)
    if condition == "single_scale":
        return replace(config, amplitude_att=0.0)
    if condition == "rep_zero":
        return replace(config, amplitude_rep=0.0)
    if condition == "m0_zero":
        return replace(config, memory_mass=0.0)
    if condition == "alpha_one":
        return replace(config, alpha=1.0)
    if condition == "matched_deposition":
        return replace(config, deposition_kernel="matched_gaussian", deposition_sigma=0.0)
    if condition == "matched_deposition_renormalized":
        factor = matched_local_stiffness_renormalization(config.dim)
        return replace(
            config,
            deposition_kernel="matched_gaussian",
            deposition_sigma=0.0,
            amplitude_rep=config.amplitude_rep * factor,
            amplitude_att=config.amplitude_att * factor,
        )
    if condition == "zero_mean_two_scale":
        return replace(
            config,
            amplitude_att=zero_mean_attractive_amplitude(
                dim=config.dim,
                sigma_rep=config.sigma_rep,
                sigma_att=config.sigma_att,
                amplitude_rep=config.amplitude_rep,
            ),
        )
    raise ValueError(f"unknown condition: {condition}")

@njit(cache=False)
def _simulate_circular_numba(
    steps: int,
    dim: int,
    epsilon: float,
    eta: float,
    alpha: float,
    memory_mass: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float,
    amplitude_att: float,
    memory_factor: float,
    max_memory: int,
    burn_in: int,
    sample_every: int,
    trace_targets: np.ndarray,
    seed: int,
):
    np.random.seed(seed)
    horizon = int(memory_factor / alpha)
    if horizon < 1:
        horizon = 1
    if horizon > max_memory:
        horizon = max_memory

    weights = np.empty(horizon, np.float64)
    weight = alpha
    decay = 1.0 - alpha
    for age in range(horizon):
        weights[age] = memory_mass * weight
        weight *= decay

    memory = np.zeros((horizon, dim), np.float64)
    x = np.zeros(dim, np.float64)
    max_samples = steps // sample_every + 2
    samples = np.zeros((max_samples, dim), np.float64)
    sample_steps = np.zeros(max_samples, np.int64)
    max_traces = len(trace_targets)
    trace_steps = np.zeros(max_traces, np.int64)
    trace_centers = np.zeros((max_traces, dim), np.float64)
    trace_positions = np.zeros((max_traces, dim), np.float64)
    trace_mean_radii = np.zeros(max_traces, np.float64)
    trace_rms_radii = np.zeros(max_traces, np.float64)
    trace_x_distances = np.zeros(max_traces, np.float64)
    idx = 0
    filled = 0
    n_sample = 0
    n_trace = 0
    sigma_rep2 = sigma_rep * sigma_rep
    sigma_att2 = sigma_att * sigma_att

    for step in range(1, steps + 1):
        grad = np.zeros(dim, np.float64)
        if eta != 0.0 and memory_mass != 0.0:
            for age in range(filled):
                mem_idx = (idx - 1 - age) % horizon
                r2 = 0.0
                for d in range(dim):
                    diff = x[d] - memory[mem_idx, d]
                    r2 += diff * diff
                rep = amplitude_rep * np.exp(-0.5 * r2 / sigma_rep2) / sigma_rep2
                att = amplitude_att * np.exp(-0.5 * r2 / sigma_att2) / sigma_att2
                factor = weights[age] * (att - rep)
                for d in range(dim):
                    grad[d] += factor * (x[d] - memory[mem_idx, d])

        for d in range(dim):
            x[d] = x[d] + epsilon * np.random.normal(0.0, 1.0) - eta * grad[d]

        for d in range(dim):
            memory[idx, d] = x[d]
        idx = (idx + 1) % horizon
        if filled < horizon:
            filled += 1

        if step >= burn_in and step % sample_every == 0:
            for d in range(dim):
                samples[n_sample, d] = x[d]
            sample_steps[n_sample] = step
            n_sample += 1

        if n_trace < max_traces and step == trace_targets[n_trace]:
            mass = 0.0
            for age in range(filled):
                mass += weights[age]

            center = np.zeros(dim, np.float64)
            if mass > 0.0:
                for age in range(filled):
                    mem_idx = (idx - 1 - age) % horizon
                    w = weights[age]
                    for d in range(dim):
                        center[d] += w * memory[mem_idx, d]
                for d in range(dim):
                    center[d] /= mass
            else:
                for d in range(dim):
                    center[d] = x[d]

            mean_radius = 0.0
            rms_radius2 = 0.0
            if mass > 0.0:
                for age in range(filled):
                    mem_idx = (idx - 1 - age) % horizon
                    w = weights[age]
                    r2 = 0.0
                    for d in range(dim):
                        diff = memory[mem_idx, d] - center[d]
                        r2 += diff * diff
                    radius = np.sqrt(r2)
                    mean_radius += w * radius
                    rms_radius2 += w * r2
                mean_radius /= mass
                rms_radius2 /= mass

            x_dist2 = 0.0
            for d in range(dim):
                diff = x[d] - center[d]
                x_dist2 += diff * diff

            trace_steps[n_trace] = step
            for d in range(dim):
                trace_centers[n_trace, d] = center[d]
                trace_positions[n_trace, d] = x[d]
            trace_mean_radii[n_trace] = mean_radius
            trace_rms_radii[n_trace] = np.sqrt(rms_radius2)
            trace_x_distances[n_trace] = np.sqrt(x_dist2)
            n_trace += 1

    return (
        samples[:n_sample],
        sample_steps[:n_sample],
        x,
        memory,
        weights,
        filled,
        idx,
        trace_steps[:n_trace],
        trace_centers[:n_trace],
        trace_positions[:n_trace],
        trace_mean_radii[:n_trace],
        trace_rms_radii[:n_trace],
        trace_x_distances[:n_trace],
    )

def simulate_long_run(
    config: SimulationConfig,
    *,
    seed: int,
    trace_every: int = 0,
    trace_targets: np.ndarray | None = None,
) -> dict[str, np.ndarray]:
    effective_kernel = effective_double_gaussian_parameters(
        dim=config.dim,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )
    if trace_targets is None:
        trace_targets = _trace_targets(
            steps=config.steps,
            burn_in=config.burn_in,
            trace_every=trace_every,
            trace_points=0,
            trace_spacing="log",
        )
    else:
        trace_targets = np.asarray(trace_targets, dtype=np.int64)

    if not _NUMBA_AVAILABLE:
        result = simulate_finite_memory(config, seed=seed)
        empty_trace = np.empty((0, config.dim), dtype=float)
        return {
            **result,
            "effective_kernel": effective_kernel,
            "trace_steps": np.empty(0, dtype=np.int64),
            "trace_centers": empty_trace,
            "trace_positions": empty_trace,
            "trace_mean_radii": np.empty(0, dtype=float),
            "trace_rms_radii": np.empty(0, dtype=float),
            "trace_x_distances": np.empty(0, dtype=float),
        }

    (
        samples,
        sample_steps,
        final_x,
        memory,
        weights,
        filled,
        idx,
        trace_steps,
        trace_centers,
        trace_positions,
        trace_mean_radii,
        trace_rms_radii,
        trace_x_distances,
    ) = _simulate_circular_numba(
        config.steps,
        config.dim,
        config.epsilon,
        config.eta,
        config.alpha,
        config.memory_mass,
        effective_kernel["sigma_rep"],
        effective_kernel["sigma_att"],
        effective_kernel["amplitude_rep"],
        effective_kernel["amplitude_att"],
        config.memory_factor,
        config.max_memory,
        config.burn_in,
        config.sample_every,
        trace_targets,
        seed,
    )
    if filled > 0:
        order = np.asarray([(idx - 1 - age) % memory.shape[0] for age in range(filled)])
        ordered_memory = memory[order].copy()
    else:
        ordered_memory = memory[:0].copy()
    return {
        "samples": samples,
        "sample_steps": sample_steps,
        "final_x": final_x.copy(),
        "memory": ordered_memory,
        "weights": weights[:filled].copy(),
        "effective_kernel": effective_kernel,
        "trace_steps": trace_steps.copy(),
        "trace_centers": trace_centers.copy(),
        "trace_positions": trace_positions.copy(),
        "trace_mean_radii": trace_mean_radii.copy(),
        "trace_rms_radii": trace_rms_radii.copy(),
        "trace_x_distances": trace_x_distances.copy(),
    }



def _median_or_none(values: list[float]) -> float | None:
    if not values:
        return None
    return float(np.median(np.asarray(values, dtype=float)))


def _mean_or_none(values: list[float]) -> float | None:
    if not values:
        return None
    return float(np.mean(np.asarray(values, dtype=float)))


def _cosine_or_none(step: np.ndarray, target: np.ndarray) -> float | None:
    step_norm = float(np.linalg.norm(step))
    target_norm = float(np.linalg.norm(target))
    if step_norm == 0.0 or target_norm == 0.0:
        return None
    return float(np.dot(step, target) / (step_norm * target_norm))


def _force_component_diagnostics(config: SimulationConfig, *, seed: int) -> dict[str, object]:
    """Return sampled force-component summaries for the current update sign."""

    rng = np.random.default_rng(seed)
    horizon = _horizon(config)
    weights = exponential_memory_weights(config.alpha, horizon, memory_mass=config.memory_mass)
    effective = effective_double_gaussian_parameters(
        dim=config.dim,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )

    history = np.zeros((horizon, config.dim), dtype=float)
    filled = 0
    x = np.zeros(config.dim, dtype=float)
    rep_norms: list[float] = []
    att_norms: list[float] = []
    net_norms: list[float] = []
    noise_norms: list[float] = []
    rep_center_cos: list[float] = []
    att_center_cos: list[float] = []
    net_center_cos: list[float] = []

    for step in range(1, config.steps + 1):
        rep_grad = np.zeros(config.dim, dtype=float)
        att_grad = np.zeros(config.dim, dtype=float)
        memory_center = x.copy()
        if filled and config.eta != 0.0 and config.memory_mass != 0.0:
            mem = history[:filled]
            w = weights[:filled]
            rep_grad = gaussian_gradient(
                x,
                mem,
                w,
                sigma=effective["sigma_rep"],
                amplitude=effective["amplitude_rep"],
            )
            att_grad = gaussian_gradient(
                x,
                mem,
                w,
                sigma=effective["sigma_att"],
                amplitude=effective["amplitude_att"],
            )
            weight_sum = float(np.sum(w))
            if weight_sum > 0.0:
                memory_center = np.average(mem, axis=0, weights=w)
        noise = config.epsilon * rng.normal(size=config.dim)
        rep_step = -config.eta * rep_grad
        att_step = config.eta * att_grad
        net_step = rep_step + att_step
        x = x + noise + net_step

        if filled < horizon:
            if filled > 0:
                history[1 : filled + 1] = history[:filled]
            filled += 1
        else:
            history[1:] = history[:-1]
        history[0] = x

        if step >= config.burn_in and step % config.sample_every == 0:
            target = memory_center - x
            rep_norms.append(float(np.linalg.norm(rep_step)))
            att_norms.append(float(np.linalg.norm(att_step)))
            net_norms.append(float(np.linalg.norm(net_step)))
            noise_norms.append(float(np.linalg.norm(noise)))
            for bucket, vector in (
                (rep_center_cos, rep_step),
                (att_center_cos, att_step),
                (net_center_cos, net_step),
            ):
                cosine = _cosine_or_none(vector, target)
                if cosine is not None and math.isfinite(cosine):
                    bucket.append(cosine)

    rep_median = _median_or_none(rep_norms)
    att_median = _median_or_none(att_norms)
    net_median = _median_or_none(net_norms)
    noise_median = _median_or_none(noise_norms)
    return {
        "n_samples": len(net_norms),
        "rep_step_norm_median": rep_median,
        "att_step_norm_median": att_median,
        "net_drift_norm_median": net_median,
        "noise_norm_median": noise_median,
        "rep_to_att_norm_median_ratio": (
            rep_median / att_median if rep_median is not None and att_median not in (None, 0.0) else None
        ),
        "noise_to_net_drift_median_ratio": (
            noise_median / net_median if noise_median is not None and net_median not in (None, 0.0) else None
        ),
        "rep_step_memory_center_cos_median": _median_or_none(rep_center_cos),
        "att_step_memory_center_cos_median": _median_or_none(att_center_cos),
        "net_step_memory_center_cos_median": _median_or_none(net_center_cos),
        "rep_step_norm_mean": _mean_or_none(rep_norms),
        "att_step_norm_mean": _mean_or_none(att_norms),
        "net_drift_norm_mean": _mean_or_none(net_norms),
        "noise_norm_mean": _mean_or_none(noise_norms),
    }


def _finite_float(value: float | np.floating | None) -> float | None:
    if value is None:
        return None
    out = float(value)
    return out if math.isfinite(out) else None


def _sample_span(samples: np.ndarray) -> list[float]:
    if samples.size == 0:
        return []
    return (samples.max(axis=0) - samples.min(axis=0)).astype(float).tolist()


def _run_lengths(mask: np.ndarray) -> np.ndarray:
    if mask.size == 0:
        return np.empty(0, dtype=int)
    runs: list[int] = []
    current = 0
    for value in mask.astype(bool):
        if value:
            current += 1
        elif current:
            runs.append(current)
            current = 0
    if current:
        runs.append(current)
    return np.asarray(runs, dtype=int)



def _trace_point_update_weights(steps: np.ndarray, fallback_stride: float) -> np.ndarray:
    if len(steps) == 0:
        return np.empty(0, dtype=float)
    stride = float(fallback_stride) if fallback_stride > 0.0 else 1.0
    if len(steps) == 1:
        return np.asarray([stride], dtype=float)
    gaps = np.diff(steps).astype(float)
    safe_gaps = np.where(gaps > 0.0, gaps, stride)
    weights = np.empty(len(steps), dtype=float)
    weights[0] = safe_gaps[0]
    weights[-1] = safe_gaps[-1]
    if len(steps) > 2:
        weights[1:-1] = 0.5 * (safe_gaps[:-1] + safe_gaps[1:])
    return weights


def _weighted_run_sums(mask: np.ndarray, weights: np.ndarray) -> np.ndarray:
    if mask.size == 0:
        return np.empty(0, dtype=float)
    runs: list[float] = []
    current = 0.0
    for flag, weight in zip(mask, weights, strict=False):
        if bool(flag):
            current += float(weight)
        elif current > 0.0:
            runs.append(current)
            current = 0.0
    if current > 0.0:
        runs.append(current)
    return np.asarray(runs, dtype=float)


def _bivector_components(rel: np.ndarray, velocity: np.ndarray) -> np.ndarray:
    if rel.ndim != 2 or velocity.ndim != 2 or rel.shape != velocity.shape:
        return np.empty((0, 0), dtype=float)
    n_points, dim = rel.shape
    if n_points == 0 or dim < 2:
        return np.empty((n_points, 0), dtype=float)
    if dim == 3:
        return np.cross(rel, velocity)
    components: list[np.ndarray] = []
    for i in range(dim):
        for j in range(i + 1, dim):
            components.append(rel[:, i] * velocity[:, j] - rel[:, j] * velocity[:, i])
    return np.stack(components, axis=1) if components else np.empty((n_points, 0), dtype=float)


def _direction_autocorrelation(unit_vectors: np.ndarray, *, max_lag: int) -> np.ndarray:
    arr = np.asarray(unit_vectors, dtype=float)
    if arr.ndim != 2 or arr.shape[0] < 2 or max_lag < 0:
        return np.empty(0, dtype=float)
    lag_max = min(max_lag, arr.shape[0] - 1)
    out = np.empty(lag_max + 1, dtype=float)
    out[0] = 1.0
    for lag in range(1, lag_max + 1):
        dots = np.sum(arr[:-lag] * arr[lag:], axis=1)
        out[lag] = float(np.mean(dots)) if len(dots) else float("nan")
    return out


def _lag_memory_times(times: np.ndarray, *, max_lag: int) -> np.ndarray:
    arr = np.asarray(times, dtype=float)
    if arr.ndim != 1 or arr.size < 2 or max_lag < 0:
        return np.empty(0, dtype=float)
    lag_max = min(max_lag, arr.size - 1)
    out = np.zeros(lag_max + 1, dtype=float)
    for lag in range(1, lag_max + 1):
        deltas = arr[lag:] - arr[:-lag]
        finite = deltas[np.isfinite(deltas) & (deltas > 0.0)]
        out[lag] = float(np.median(finite)) if len(finite) else float("nan")
    return out


def _first_dephasing_time(correlation: np.ndarray, lag_times: np.ndarray) -> float | None:
    if len(correlation) == 0 or len(lag_times) != len(correlation):
        return None
    threshold = math.exp(-1.0)
    for value, lag_time in zip(correlation[1:], lag_times[1:], strict=False):
        if not (math.isfinite(float(value)) and math.isfinite(float(lag_time))):
            continue
        if float(value) <= threshold:
            return float(lag_time)
    return None


def _finite_percentile(values: np.ndarray, percentile: float) -> float | None:
    arr = np.asarray(values, dtype=float)
    finite = arr[np.isfinite(arr)]
    if len(finite) == 0:
        return None
    return float(np.percentile(finite, percentile))


def _spin_proxy_diagnostics(
    *,
    steps: np.ndarray,
    centers: np.ndarray,
    positions: np.ndarray,
    rms_radii: np.ndarray,
    alpha: float,
    max_lag: int = 20,
) -> dict[str, object] | None:
    if positions.shape != centers.shape or len(steps) != len(centers) or len(steps) < 3:
        return None
    gaps = np.diff(steps).astype(float)
    memory_gaps = gaps * float(alpha)
    valid_gap = np.isfinite(memory_gaps) & (memory_gaps > 0.0)
    if not np.any(valid_gap):
        return None

    rel = positions - centers
    displacements = np.diff(positions, axis=0)
    velocity = displacements[valid_gap] / memory_gaps[valid_gap, None]
    rel_mid = 0.5 * (rel[:-1] + rel[1:])[valid_gap]
    radius_mid = 0.5 * (rms_radii[:-1] + rms_radii[1:])[valid_gap]
    transition_times = 0.5 * (steps[:-1] + steps[1:])[valid_gap].astype(float) * float(alpha)

    spin_components = _bivector_components(rel_mid, velocity)
    if spin_components.shape[1] == 0:
        return None
    amplitude = np.linalg.norm(spin_components, axis=1)
    valid_amplitude = np.isfinite(amplitude) & (amplitude > 0.0)
    if not np.any(valid_amplitude):
        return {
            "valid_fraction": 0.0,
            "component_count": int(spin_components.shape[1]),
            "amplitude_median": 0.0,
            "amplitude_q25": 0.0,
            "amplitude_q75": 0.0,
            "amplitude_cv": None,
            "angular_speed_median": None,
            "axis_polarization": None,
            "direction_dephasing_memory_times": None,
            "transition_memory_times": [_finite_float(value) for value in transition_times],
            "amplitudes": [_finite_float(value) for value in amplitude],
            "angular_speeds": [],
        }
    amplitude_valid = amplitude[valid_amplitude]
    unit = spin_components[valid_amplitude] / amplitude_valid[:, None]
    finite_radius = np.isfinite(radius_mid) & (radius_mid > 0.0) & valid_amplitude
    angular_speed_full = np.full(amplitude.shape, np.nan, dtype=float)
    if np.any(finite_radius):
        angular_speed_full[finite_radius] = amplitude[finite_radius] / (radius_mid[finite_radius] ** 2)
    angular_speed = angular_speed_full[np.isfinite(angular_speed_full)]
    direction_ac = _direction_autocorrelation(unit, max_lag=max_lag)
    valid_times = transition_times[valid_amplitude]
    lag_times = _lag_memory_times(valid_times, max_lag=max_lag)
    dephasing = _first_dephasing_time(direction_ac, lag_times)
    mean_unit = np.mean(unit, axis=0)
    axis_norm = float(np.linalg.norm(mean_unit)) if len(mean_unit) else None
    amplitude_mean = float(np.mean(amplitude_valid))
    amplitude_std = float(np.std(amplitude_valid))
    signed_component_median = None
    signed_component_mean = None
    if spin_components.shape[1] == 1:
        signed_values = spin_components[valid_amplitude, 0]
        signed_component_median = _finite_float(float(np.median(signed_values)))
        signed_component_mean = _finite_float(float(np.mean(signed_values)))

    return {
        "valid_fraction": _finite_float(float(np.mean(valid_amplitude))),
        "component_count": int(spin_components.shape[1]),
        "amplitude_median": _finite_float(float(np.median(amplitude_valid))),
        "amplitude_q25": _finite_percentile(amplitude_valid, 25.0),
        "amplitude_q75": _finite_percentile(amplitude_valid, 75.0),
        "amplitude_cv": _finite_float(amplitude_std / amplitude_mean) if amplitude_mean > 0.0 else None,
        "angular_speed_median": _finite_percentile(angular_speed, 50.0),
        "angular_speed_q25": _finite_percentile(angular_speed, 25.0),
        "angular_speed_q75": _finite_percentile(angular_speed, 75.0),
        "axis_polarization": _finite_float(axis_norm),
        "signed_component_median": signed_component_median,
        "signed_component_mean": signed_component_mean,
        "transition_memory_times": [_finite_float(value) for value in transition_times],
        "amplitudes": [_finite_float(value) for value in amplitude],
        "angular_speeds": [_finite_float(value) for value in angular_speed_full],
        "direction_autocorrelation": [_finite_float(value) for value in direction_ac],
        "direction_autocorrelation_lag_memory_times": [_finite_float(value) for value in lag_times],
        "direction_dephasing_memory_times": _finite_float(dephasing),
    }

def _dynamic_center_trace_diagnostics(
    result: dict[str, np.ndarray],
    *,
    config: SimulationConfig,
    trace_every: int,
    primary_radius_factor: float = 2.0,
    include_trace: bool = True,
    max_trace_points: int = 50_000,
) -> dict[str, object] | None:
    steps = np.asarray(result.get("trace_steps", np.empty(0, dtype=np.int64)), dtype=np.int64)
    centers = np.asarray(result.get("trace_centers", np.empty((0, config.dim))), dtype=float)
    positions = np.asarray(result.get("trace_positions", np.empty((0, config.dim))), dtype=float)
    mean_radii = np.asarray(result.get("trace_mean_radii", np.empty(0)), dtype=float)
    rms_radii = np.asarray(result.get("trace_rms_radii", np.empty(0)), dtype=float)
    x_distances = np.asarray(result.get("trace_x_distances", np.empty(0)), dtype=float)
    if len(steps) == 0:
        return None
    if centers.shape != (len(steps), config.dim):
        return None
    has_positions = positions.shape == centers.shape
    if not (len(mean_radii) == len(steps) == len(rms_radii) == len(x_distances)):
        return None

    valid_radius = np.isfinite(rms_radii) & (rms_radii > 0.0)
    degenerate_radius = ~valid_radius
    inside = np.zeros(len(steps), dtype=bool)
    inside[valid_radius] = x_distances[valid_radius] <= primary_radius_factor * rms_radii[valid_radius]
    runs = _run_lengths(inside)

    if len(steps) > 1:
        gaps = np.diff(steps).astype(float)
        positive_gaps = gaps[gaps > 0.0]
        trace_stride_updates = float(np.median(positive_gaps)) if len(positive_gaps) else float(trace_every)
        trace_interval_updates_min = float(np.min(positive_gaps)) if len(positive_gaps) else None
        trace_interval_updates_max = float(np.max(positive_gaps)) if len(positive_gaps) else None
    else:
        gaps = np.empty(0, dtype=float)
        trace_stride_updates = float(trace_every)
        trace_interval_updates_min = None
        trace_interval_updates_max = None
    if trace_stride_updates <= 0.0:
        trace_stride_updates = float(config.sample_every)
    trace_stride_memory_times = trace_stride_updates * config.alpha
    trace_point_update_weights = _trace_point_update_weights(steps, trace_stride_updates)
    trace_point_memory_times = trace_point_update_weights * config.alpha
    run_memory_times = _weighted_run_sums(inside, trace_point_memory_times)
    trace_time_memory_times = float(np.sum(trace_point_memory_times)) if len(trace_point_memory_times) else 0.0
    if trace_time_memory_times > 0.0:
        comoving_inside_fraction_time_weighted = float(
            np.sum(trace_point_memory_times[inside]) / trace_time_memory_times
        )
    else:
        comoving_inside_fraction_time_weighted = 0.0

    center_steps = np.linalg.norm(np.diff(centers, axis=0), axis=1) if len(steps) > 1 else np.empty(0)
    center_path_length = float(np.sum(center_steps)) if len(center_steps) else 0.0
    center_net_displacement = float(np.linalg.norm(centers[-1] - centers[0])) if len(steps) > 1 else 0.0
    center_path_to_chord = center_path_length / center_net_displacement if center_net_displacement > 0.0 else None

    drift_per_memory_time = np.empty(0, dtype=float)
    drift_radius_fraction_per_memory_time = np.empty(0, dtype=float)
    if len(center_steps):
        memory_gaps = gaps * config.alpha
        valid_gap = memory_gaps > 0.0
        drift_per_memory_time = center_steps[valid_gap] / memory_gaps[valid_gap]
        radius_mid = 0.5 * (rms_radii[:-1] + rms_radii[1:])
        valid_radius_gap = valid_gap & np.isfinite(radius_mid) & (radius_mid > 0.0)
        drift_radius_fraction_per_memory_time = (
            center_steps[valid_radius_gap] / radius_mid[valid_radius_gap] / memory_gaps[valid_radius_gap]
        )

    radius_ratio = np.full(len(steps), np.nan, dtype=float)
    radius_ratio[valid_radius] = x_distances[valid_radius] / rms_radii[valid_radius]
    finite_ratio = radius_ratio[np.isfinite(radius_ratio)]

    out: dict[str, object] = {
        "n_traces": int(len(steps)),
        "trace_stride_updates": _finite_float(trace_stride_updates),
        "trace_stride_memory_times": _finite_float(trace_stride_memory_times),
        "trace_interval_updates_min": _finite_float(trace_interval_updates_min),
        "trace_interval_updates_max": _finite_float(trace_interval_updates_max),
        "trace_time_memory_times": _finite_float(trace_time_memory_times),
        "primary_radius_factor": float(primary_radius_factor),
        "valid_radius_fraction": _finite_float(float(np.mean(valid_radius))),
        "degenerate_radius_fraction": _finite_float(float(np.mean(degenerate_radius))),
        "comoving_inside_fraction": _finite_float(float(np.mean(inside))),
        "comoving_inside_fraction_time_weighted": _finite_float(comoving_inside_fraction_time_weighted),
        "max_run_trace_points": int(runs.max()) if len(runs) else 0,
        "mean_run_trace_points": _finite_float(float(np.mean(runs))) if len(runs) else 0.0,
        "max_run_memory_times": _finite_float(float(run_memory_times.max())) if len(run_memory_times) else 0.0,
        "mean_run_memory_times": _finite_float(float(np.mean(run_memory_times))) if len(run_memory_times) else 0.0,
        "rms_radius_median": _finite_float(float(np.median(rms_radii))),
        "rms_radius_mean": _finite_float(float(np.mean(rms_radii))),
        "mean_radius_median": _finite_float(float(np.median(mean_radii))),
        "x_distance_median": _finite_float(float(np.median(x_distances))),
        "x_distance_to_rms_radius_median": (
            _finite_float(float(np.median(finite_ratio))) if len(finite_ratio) else None
        ),
        "center_step_median": _finite_float(float(np.median(center_steps))) if len(center_steps) else 0.0,
        "center_drift_per_memory_time_median": (
            _finite_float(float(np.median(drift_per_memory_time)))
            if len(drift_per_memory_time)
            else 0.0
        ),
        "center_drift_radius_fraction_per_memory_time_median": (
            _finite_float(float(np.median(drift_radius_fraction_per_memory_time)))
            if len(drift_radius_fraction_per_memory_time)
            else None
        ),
        "center_path_length": _finite_float(center_path_length),
        "center_net_displacement": _finite_float(center_net_displacement),
        "center_path_to_chord": _finite_float(center_path_to_chord),
    }
    if has_positions:
        spin_proxy = _spin_proxy_diagnostics(
            steps=steps,
            centers=centers,
            positions=positions,
            rms_radii=rms_radii,
            alpha=config.alpha,
        )
        if spin_proxy is not None:
            out["spin_proxy"] = spin_proxy
    if include_trace:
        stride = max(1, int(math.ceil(len(steps) / max_trace_points)))
        sl = slice(None, None, stride)
        out["trace"] = {
            "stored_point_count": int(len(steps[sl])),
            "decimation_stride": int(stride),
            "steps": steps[sl].astype(int).tolist(),
            "centers": centers[sl].astype(float).tolist(),
            "positions": positions[sl].astype(float).tolist() if has_positions else [],
            "mean_radii": mean_radii[sl].astype(float).tolist(),
            "rms_radii": rms_radii[sl].astype(float).tolist(),
            "x_distances": x_distances[sl].astype(float).tolist(),
            "inside_primary_radius": inside[sl].astype(bool).tolist(),
        }
    return out


def _occupancy_payload(points: np.ndarray) -> dict[str, object]:
    details = occupancy_dimension(points, return_details=True)
    window = fit_occupancy_scaling_window(
        details.scales,
        details.counts,
        n_samples=len(points),
    )
    return {
        "dimension": _finite_float(details.dimension),
        "scales": details.scales.astype(float).tolist(),
        "counts": details.counts.astype(float).tolist(),
        "scaling_window": {
            "dimension": _finite_float(window.dimension),
            "start_index": int(window.start_index),
            "stop_index": int(window.stop_index),
            "r_squared": _finite_float(window.r_squared),
            "local_slope_mean": _finite_float(window.local_slope_mean),
            "local_slope_std": _finite_float(window.local_slope_std),
            "log_width": _finite_float(window.log_width),
            "n_points": int(window.n_points),
            "valid_scaling": bool(window.valid_scaling),
        },
    }


def _memory_cloud_diagnostics(memory: np.ndarray, weights: np.ndarray) -> dict[str, object] | None:
    if len(memory) < 2 or float(np.sum(weights)) <= 0.0:
        return None
    return {
        "shape": shape_statistics(memory, weights=weights),
        "occupancy": _occupancy_payload(memory),
    }


def _center_residence_payload(
    samples: np.ndarray,
    *,
    config: SimulationConfig,
    center: object,
    base_radius: object,
    radius_factors: Iterable[float],
    primary_radius_factor: float,
    min_memory_times: float,
) -> dict[str, object] | None:
    if center is None or base_radius is None:
        return None
    try:
        radius0 = float(base_radius)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(radius0) or radius0 <= 0.0:
        return None

    memory_persistence_updates = 1.0 / config.alpha
    out: dict[str, object] = {
        "center": list(center) if isinstance(center, list) else center,
        "base_radius": radius0,
        "radius_factors": [float(factor) for factor in radius_factors],
        "primary_radius_factor": float(primary_radius_factor),
        "valid_radius_fraction": 1.0,
        "degenerate_radius_fraction": 0.0,
    }
    by_factor: dict[str, object] = {}
    unconstrained_best = 0.0
    primary_key = f"{float(primary_radius_factor):g}"
    for factor in radius_factors:
        stats = ball_residence_statistics(
            samples,
            center=center,  # type: ignore[arg-type]
            radius=radius0 * float(factor),
            min_run_length=1,
        )
        mean_updates = float(float(stats["mean_run_length"]) * config.sample_every)
        max_updates = float(float(stats["max_run_length"]) * config.sample_every)
        max_memory_times = max_updates / memory_persistence_updates
        is_long_lived = bool(max_updates >= min_memory_times * memory_persistence_updates)
        unconstrained_best = max(unconstrained_best, max_memory_times)
        by_factor[f"{float(factor):g}"] = {
            **stats,
            "mean_run_updates": mean_updates,
            "max_run_updates": max_updates,
            "mean_run_memory_times": mean_updates / memory_persistence_updates,
            "max_run_memory_times": max_memory_times,
            "candidate_long_lived": is_long_lived,
        }

    primary = by_factor.get(primary_key)
    primary_candidate = False
    if isinstance(primary, dict):
        primary_max = primary.get("max_run_memory_times")
        primary_inside = primary.get("inside_fraction")
        primary_candidate = bool(primary.get("candidate_long_lived"))
    else:
        primary_max = None
        primary_inside = None

    out["unconstrained_best_max_run_memory_times"] = unconstrained_best
    out["primary_max_run_memory_times"] = primary_max
    out["primary_inside_fraction"] = primary_inside
    out["candidate_long_lived"] = primary_candidate
    out["by_radius_factor"] = by_factor
    return out


def metastability_diagnostics(
    samples: np.ndarray,
    *,
    config: SimulationConfig,
    voxel_sizes: Iterable[float],
    max_ac_lag: int,
    min_memory_times: float,
) -> dict[str, object]:
    if len(samples) < 2:
        raise ValueError("at least two samples are required")

    memory_persistence_updates = 1.0 / config.alpha
    voxel_results: dict[str, dict[str, float | bool | None]] = {}
    for voxel_size in voxel_sizes:
        residence = residence_statistics(samples, voxel_size=voxel_size, min_visits=3)
        mean_updates = float(residence["mean_residence"] * config.sample_every)
        max_updates = float(residence["max_residence"] * config.sample_every)
        voxel_results[str(voxel_size)] = {
            **residence,
            "mean_residence_updates": mean_updates,
            "max_residence_updates": max_updates,
            "mean_residence_memory_times": mean_updates / memory_persistence_updates,
            "max_residence_memory_times": max_updates / memory_persistence_updates,
            "candidate_long_lived": bool(
                max_updates >= min_memory_times * memory_persistence_updates
            ),
        }

    lag = min(max_ac_lag, len(samples) - 1)
    autocorrelation = vector_autocorrelation(samples, max_lag=lag)
    increments = np.linalg.norm(np.diff(samples, axis=0), axis=1)
    centered = samples - samples.mean(axis=0, keepdims=True)
    radii = np.linalg.norm(centered, axis=1)
    occupancy = _occupancy_payload(samples)
    sample_shape = shape_statistics(samples)
    sample_center_residence = _center_residence_payload(
        samples,
        config=config,
        center=sample_shape.get("center"),
        base_radius=sample_shape.get("mean_radius"),
        radius_factors=[1.0, 2.0, 4.0, 8.0, 16.0],
        primary_radius_factor=2.0,
        min_memory_times=min_memory_times,
    )

    return {
        "n_samples": int(len(samples)),
        "memory_persistence_updates": float(memory_persistence_updates),
        "sample_every": int(config.sample_every),
        "sample_span": _sample_span(samples),
        "mean_sample_increment": _finite_float(increments.mean()),
        "max_sample_increment": _finite_float(increments.max()),
        "mean_centered_radius": _finite_float(radii.mean()),
        "max_centered_radius": _finite_float(radii.max()),
        "covariance_dimension": _finite_float(covariance_dimension(samples)),
        "occupancy_dimension": occupancy["dimension"],
        "occupancy": occupancy,
        "sample_shape": sample_shape,
        "center_residence": {"sample_center": sample_center_residence}
        if sample_center_residence is not None
        else {},
        "autocorrelation": [_finite_float(value) for value in autocorrelation],
        "residence_by_voxel_size": voxel_results,
    }


def _case_filename(condition: str, seed: int, steps: int) -> str:
    return f"case_{condition}_seed{seed}_steps{steps}.json"


def run_case(
    *,
    base_config: SimulationConfig,
    condition: str,
    seed: int,
    voxel_sizes: Iterable[float],
    max_ac_lag: int,
    min_memory_times: float,
    output_dir: Path,
    force_components: bool = False,
    trace_every: int = 0,
    trace_targets: np.ndarray | None = None,
) -> dict[str, object]:
    config = _apply_condition(base_config, condition)
    started = time.perf_counter()
    result = simulate_long_run(config, seed=seed, trace_every=trace_every, trace_targets=trace_targets)
    elapsed = time.perf_counter() - started
    samples = result["samples"]
    horizon = _horizon(config)
    diagnostics = metastability_diagnostics(
        samples,
        config=config,
        voxel_sizes=voxel_sizes,
        max_ac_lag=max_ac_lag,
        min_memory_times=min_memory_times,
    )
    dynamic_center_trace = _dynamic_center_trace_diagnostics(
        result,
        config=config,
        trace_every=trace_every,
    )
    if dynamic_center_trace is not None:
        diagnostics["dynamic_center_trace"] = dynamic_center_trace
    memory_cloud = _memory_cloud_diagnostics(result["memory"], result["weights"])
    if memory_cloud is not None:
        diagnostics["memory_cloud"] = memory_cloud
        memory_shape = memory_cloud.get("shape")
        if isinstance(memory_shape, dict):
            memory_center_residence = _center_residence_payload(
                samples,
                config=config,
                center=memory_shape.get("center"),
                base_radius=memory_shape.get("mean_radius"),
                radius_factors=[1.0, 2.0, 4.0, 8.0, 16.0],
                primary_radius_factor=2.0,
                min_memory_times=min_memory_times,
            )
            if memory_center_residence is not None:
                center_residence = diagnostics.setdefault("center_residence", {})
                if isinstance(center_residence, dict):
                    center_residence["memory_center"] = memory_center_residence
    if force_components:
        diagnostics["force_components"] = _force_component_diagnostics(config, seed=seed)
    payload: dict[str, object] = {
        "condition": condition,
        "seed": int(seed),
        "git_revision": _git_output(["rev-parse", "--short", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "started_utc": _utc_now(),
        "elapsed_seconds": float(elapsed),
        "steps_per_second": float(config.steps / elapsed) if elapsed > 0 else None,
        "config": asdict(config),
        "effective_kernel": result["effective_kernel"],
        "memory_horizon": int(horizon),
        "stored_weight_mass": _stored_weight_mass(config.alpha, horizon, config.memory_mass),
        "diagnostics": diagnostics,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    case_path = output_dir / _case_filename(condition, seed, config.steps)
    case_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )
    return payload


def _center_residence_field(diagnostics: dict[str, object], key: str, field: str) -> float | None:
    center_residence = diagnostics.get("center_residence")
    if not isinstance(center_residence, dict):
        return None
    payload = center_residence.get(key)
    if not isinstance(payload, dict):
        return None
    value = payload.get(field)
    if isinstance(value, (float, int)) and math.isfinite(float(value)):
        return float(value)
    return None


def _dynamic_center_field(diagnostics: dict[str, object], field: str) -> float | int | None:
    payload = diagnostics.get("dynamic_center_trace")
    if not isinstance(payload, dict):
        return None
    value = payload.get(field)
    if isinstance(value, int):
        return value
    if isinstance(value, float) and math.isfinite(value):
        return value
    return None


def _dynamic_center_spin_field(diagnostics: dict[str, object], field: str) -> float | int | None:
    payload = diagnostics.get("dynamic_center_trace")
    if not isinstance(payload, dict):
        return None
    spin = payload.get("spin_proxy")
    if not isinstance(spin, dict):
        return None
    value = spin.get(field)
    if isinstance(value, int):
        return value
    if isinstance(value, float) and math.isfinite(value):
        return value
    return None

def summarize_cases(cases: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for case in cases:
        diagnostics = case["diagnostics"]
        assert isinstance(diagnostics, dict)
        residence = diagnostics["residence_by_voxel_size"]
        assert isinstance(residence, dict)
        best_ratio = 0.0
        candidate = False
        for metrics in residence.values():
            assert isinstance(metrics, dict)
            ratio = metrics.get("max_residence_memory_times")
            if isinstance(ratio, (float, int)) and math.isfinite(float(ratio)):
                best_ratio = max(best_ratio, float(ratio))
            candidate = candidate or bool(metrics.get("candidate_long_lived"))
        occupancy = diagnostics.get("occupancy")
        occupancy_window = {}
        if isinstance(occupancy, dict):
            maybe_window = occupancy.get("scaling_window")
            if isinstance(maybe_window, dict):
                occupancy_window = maybe_window
        sample_shape = diagnostics.get("sample_shape")
        if not isinstance(sample_shape, dict):
            sample_shape = {}
        memory_cloud = diagnostics.get("memory_cloud")
        memory_shape = {}
        if isinstance(memory_cloud, dict) and isinstance(memory_cloud.get("shape"), dict):
            memory_shape = memory_cloud["shape"]
        rows.append(
            {
                "condition": case["condition"],
                "seed": case["seed"],
                "steps": case["config"]["steps"],  # type: ignore[index]
                "elapsed_seconds": case["elapsed_seconds"],
                "steps_per_second": case["steps_per_second"],
                "covariance_dimension": diagnostics["covariance_dimension"],
                "occupancy_dimension": diagnostics["occupancy_dimension"],
                "occupancy_window_dimension": occupancy_window.get("dimension"),
                "occupancy_window_valid": occupancy_window.get("valid_scaling"),
                "sample_shape_dimension": sample_shape.get("effective_dimension"),
                "sample_axis_ratio_min_max": sample_shape.get("axis_ratio_min_max"),
                "memory_shape_dimension": memory_shape.get("effective_dimension"),
                "memory_axis_ratio_min_max": memory_shape.get("axis_ratio_min_max"),
                "best_max_residence_memory_times": best_ratio,
                "sample_center_primary_max_run_memory_times": _center_residence_field(
                    diagnostics, "sample_center", "primary_max_run_memory_times"
                ),
                "sample_center_primary_inside_fraction": _center_residence_field(
                    diagnostics, "sample_center", "primary_inside_fraction"
                ),
                "memory_center_primary_max_run_memory_times": _center_residence_field(
                    diagnostics, "memory_center", "primary_max_run_memory_times"
                ),
                "memory_center_primary_inside_fraction": _center_residence_field(
                    diagnostics, "memory_center", "primary_inside_fraction"
                ),
                "dynamic_center_trace_count": _dynamic_center_field(diagnostics, "n_traces"),
                "dynamic_center_rms_radius_median": _dynamic_center_field(diagnostics, "rms_radius_median"),
                "dynamic_center_comoving_inside_fraction": _dynamic_center_field(
                    diagnostics, "comoving_inside_fraction"
                ),
                "dynamic_center_comoving_inside_fraction_time_weighted": _dynamic_center_field(
                    diagnostics, "comoving_inside_fraction_time_weighted"
                ),
                "dynamic_center_max_run_memory_times": _dynamic_center_field(diagnostics, "max_run_memory_times"),
                "dynamic_center_drift_per_memory_time_median": _dynamic_center_field(
                    diagnostics, "center_drift_per_memory_time_median"
                ),
                "dynamic_center_drift_radius_fraction_per_memory_time_median": _dynamic_center_field(
                    diagnostics, "center_drift_radius_fraction_per_memory_time_median"
                ),
                "spin_proxy_valid_fraction": _dynamic_center_spin_field(diagnostics, "valid_fraction"),
                "spin_proxy_amplitude_median": _dynamic_center_spin_field(diagnostics, "amplitude_median"),
                "spin_proxy_amplitude_cv": _dynamic_center_spin_field(diagnostics, "amplitude_cv"),
                "spin_proxy_angular_speed_median": _dynamic_center_spin_field(diagnostics, "angular_speed_median"),
                "spin_proxy_axis_polarization": _dynamic_center_spin_field(diagnostics, "axis_polarization"),
                "spin_proxy_signed_component_median": _dynamic_center_spin_field(diagnostics, "signed_component_median"),
                "spin_proxy_direction_dephasing_memory_times": _dynamic_center_spin_field(
                    diagnostics, "direction_dephasing_memory_times"
                ),
                "candidate_long_lived": candidate,
            }
        )
    return rows


def write_summary(output_dir: Path, payload: dict[str, object]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run long-N metastability diagnostics for the canonical finite-memory "
            "model. This is an evidence campaign, not a Paper-0 structural proof."
        )
    )
    parser.add_argument("--steps", type=int, default=10_000_000)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument("--seeds", type=_parse_int_list, default=_parse_int_list("1"))
    parser.add_argument(
        "--conditions",
        type=_parse_conditions,
        default=_parse_conditions("baseline"),
    )
    parser.add_argument("--epsilon", type=float, default=0.03)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--deposition-kernel", choices=sorted(DEPOSITION_KERNELS), default="delta")
    parser.add_argument("--deposition-sigma", type=float, default=0.0)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=0.35)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--max-memory", type=int, default=800)
    parser.add_argument("--burn-in", type=int, default=1_000_000)
    parser.add_argument("--sample-every", type=int, default=1000)
    parser.add_argument(
        "--trace-every",
        type=int,
        default=0,
        help="store time-local memory-center traces every N updates; 0 disables it",
    )
    parser.add_argument(
        "--trace-points",
        type=int,
        default=0,
        help="store this many explicit trace points; overrides --trace-every when positive",
    )
    parser.add_argument(
        "--trace-spacing",
        choices=("linear", "log"),
        default="log",
        help="spacing for --trace-points",
    )
    parser.add_argument(
        "--voxel-sizes",
        type=_parse_float_list,
        default=_parse_float_list("0.5,1.0,2.0"),
    )
    parser.add_argument("--max-ac-lag", type=int, default=50)
    parser.add_argument("--min-memory-times", type=float, default=10.0)
    parser.add_argument("--allow-slow-python", action="store_true")
    parser.add_argument(
        "--force-components",
        action="store_true",
        help="store sampled force-component summaries; re-simulates each case in Python",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed/long_run_metastability/2026-06-29_initial"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.steps < 1:
        raise SystemExit("--steps must be positive")
    if args.burn_in < 0 or args.burn_in >= args.steps:
        raise SystemExit("--burn-in must satisfy 0 <= burn_in < steps")
    if args.sample_every < 1:
        raise SystemExit("--sample-every must be positive")
    if args.trace_every < 0:
        raise SystemExit("--trace-every must be non-negative")
    if args.trace_points < 0:
        raise SystemExit("--trace-points must be non-negative")
    if args.max_memory < 1:
        raise SystemExit("--max-memory must be positive")
    if not 0.0 < args.alpha <= 1.0:
        raise SystemExit("--alpha must satisfy 0 < alpha <= 1")
    if not math.isfinite(args.memory_mass) or args.memory_mass < 0.0:
        raise SystemExit("--memory-mass must be non-negative")
    if not math.isfinite(args.deposition_sigma) or args.deposition_sigma < 0.0:
        raise SystemExit("--deposition-sigma must be non-negative")
    if args.deposition_kernel == "delta" and args.deposition_sigma != 0.0:
        raise SystemExit("--deposition-sigma must be zero for delta deposition")
    if args.deposition_kernel == "gaussian" and args.deposition_sigma <= 0.0:
        raise SystemExit("--deposition-sigma must be positive for gaussian deposition")
    if args.deposition_kernel == "matched_gaussian" and args.deposition_sigma != 0.0:
        raise SystemExit("--deposition-sigma must be zero for matched_gaussian deposition")
    if not _NUMBA_AVAILABLE and not args.allow_slow_python:
        raise SystemExit("numba is required for long-run simulations unless --allow-slow-python is set")

    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    base_config = SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=args.epsilon,
        eta=args.eta,
        alpha=args.alpha,
        memory_mass=args.memory_mass,
        deposition_kernel=args.deposition_kernel,
        deposition_sigma=args.deposition_sigma,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=args.amplitude_rep,
        amplitude_att=args.amplitude_att,
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )

    trace_targets = _trace_targets(
        steps=base_config.steps,
        burn_in=base_config.burn_in,
        trace_every=args.trace_every,
        trace_points=args.trace_points,
        trace_spacing=args.trace_spacing,
    )

    run_started = _utc_now()
    cases: list[dict[str, object]] = []
    total_started = time.perf_counter()
    for condition in args.conditions:
        for seed in args.seeds:
            case_config = _apply_condition(base_config, condition)
            print(
                "running "
                f"condition={condition} seed={seed} steps={case_config.steps} "
                f"alpha={case_config.alpha:g} memory_mass={case_config.memory_mass:g} deposition={case_config.deposition_kernel} dim={case_config.dim}",
                flush=True,
            )
            cases.append(
                run_case(
                    base_config=base_config,
                    condition=condition,
                    seed=seed,
                    voxel_sizes=args.voxel_sizes,
                    max_ac_lag=args.max_ac_lag,
                    min_memory_times=args.min_memory_times,
                    output_dir=output_dir,
                    force_components=args.force_components,
                    trace_every=args.trace_every,
                    trace_targets=trace_targets,
                )
            )

    total_elapsed = time.perf_counter() - total_started
    summary_payload: dict[str, object] = {
        "description": "Long-N metastability diagnostics for the canonical finite-memory model.",
        "started_utc": run_started,
        "finished_utc": _utc_now(),
        "total_elapsed_seconds": float(total_elapsed),
        "git_revision": _git_output(["rev-parse", "--short", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "parameters": {
            "conditions": args.conditions,
            "seeds": args.seeds,
            "voxel_sizes": args.voxel_sizes,
            "max_ac_lag": args.max_ac_lag,
            "min_memory_times": args.min_memory_times,
            "trace_every": args.trace_every,
            "trace_points": args.trace_points,
            "trace_spacing": args.trace_spacing,
            "trace_target_count": int(len(trace_targets)),
            "trace_first_step": int(trace_targets[0]) if len(trace_targets) else None,
            "trace_last_step": int(trace_targets[-1]) if len(trace_targets) else None,
        },
        "base_config": asdict(base_config),
        "case_summaries": summarize_cases(cases),
        "case_files": [
            _case_filename(str(case["condition"]), int(case["seed"]), base_config.steps)
            for case in cases
        ],
    }
    write_summary(output_dir, summary_payload)
    print(f"wrote summary to {output_dir / 'summary.json'}", flush=True)


if __name__ == "__main__":
    main()
