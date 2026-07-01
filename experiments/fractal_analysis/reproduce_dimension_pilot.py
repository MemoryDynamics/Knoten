from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
from datetime import date
import json
import math
from pathlib import Path
import subprocess
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    bootstrap_mean_ci,
    covariance_dimension,
    fit_occupancy_scaling_window,
    occupancy_dimension,
    occupancy_local_slopes,
    residence_statistics,
    spectral_dimension,
)

try:
    from numba import njit

    _NUMBA_AVAILABLE = True
except ImportError:  # pragma: no cover
    _NUMBA_AVAILABLE = False

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


@dataclass(frozen=True)
class ArchiveFractalConfig:
    """Parameter set used by the archived fractal-dimension scans."""

    steps: int = 60_000
    dim: int = 5
    epsilon: float = 0.05
    eta: float = 2.0
    alpha: float = 0.01
    deposit_beta: float | None = None
    amplitude_rep: float = 1.0
    amplitude_att: float = 3.0
    sigma_rep: float = 1.0
    sigma_att: float = 0.15
    memory_factor: float = 5.0
    max_memory: int = 300
    burn_in: int = 0
    sample_every: int = 10


@dataclass(frozen=True)
class OccupancyDetails:
    dimension: float
    scales: np.ndarray
    counts: np.ndarray


def parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("list must contain at least one integer")
    return values


def parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("list must contain at least one float")
    return values


def parse_conditions(value: str) -> list[str]:
    allowed = {"baseline", "eta_zero", "single_scale", "shuffled_memory"}
    values = [item.strip() for item in value.split(",") if item.strip()]
    unknown = [item for item in values if item not in allowed]
    if unknown:
        raise argparse.ArgumentTypeError(f"unknown condition(s): {', '.join(unknown)}")
    if not values:
        raise argparse.ArgumentTypeError("conditions must contain at least one entry")
    return values


def git_revision() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return result.stdout.strip() or "unknown"


def deposit_beta(config: ArchiveFractalConfig) -> float:
    """Return the deposited memory weight beta.

    The historical convention is beta=lambda_m=alpha. A separate beta lets
    memory mass and memory decay be scanned independently without changing old
    command lines.
    """

    return float(config.alpha if config.deposit_beta is None else config.deposit_beta)


def beta_over_alpha(config: ArchiveFractalConfig) -> float:
    return float(deposit_beta(config) / config.alpha)


def horizon(config: ArchiveFractalConfig) -> int:
    if not 0.0 < config.alpha <= 1.0:
        raise ValueError("alpha must satisfy 0 < alpha <= 1")
    return min(config.max_memory, uncapped_horizon(config.alpha, config.memory_factor))


def uncapped_horizon(alpha: float, memory_factor: float) -> int:
    if not 0.0 < alpha <= 1.0:
        raise ValueError("alpha must satisfy 0 < alpha <= 1")
    return max(1, int(memory_factor / alpha) + 1)


def horizon_for_tail_mass(alpha: float, target_mass: float) -> int:
    if not 0.0 < alpha <= 1.0:
        raise ValueError("alpha must satisfy 0 < alpha <= 1")
    if not 0.0 < target_mass < 1.0:
        raise ValueError("target_mass must satisfy 0 < target_mass < 1")
    if alpha == 1.0:
        return 1
    return max(1, int(math.ceil(math.log(1.0 - target_mass) / math.log(1.0 - alpha))))


def max_memory_for_mode(
    *,
    alpha: float,
    memory_factor: float,
    configured_max_memory: int,
    memory_mode: str,
    target_mass: float,
) -> int:
    full_horizon = uncapped_horizon(alpha, memory_factor)
    if memory_mode == "capped":
        return configured_max_memory
    if memory_mode == "full":
        return full_horizon
    if memory_mode == "tail-mass":
        return min(full_horizon, horizon_for_tail_mass(alpha, target_mass))
    raise ValueError(f"unknown memory mode: {memory_mode}")


def stored_weight_mass(config: ArchiveFractalConfig) -> float:
    beta = deposit_beta(config)
    return float(beta * (1.0 - (1.0 - config.alpha) ** horizon(config)) / config.alpha)


def config_metrics(config: ArchiveFractalConfig) -> dict[str, float | int]:
    return {
        "uncapped_horizon": int(uncapped_horizon(config.alpha, config.memory_factor)),
        "used_horizon": int(horizon(config)),
        "deposit_beta": deposit_beta(config),
        "beta_over_alpha": beta_over_alpha(config),
        "stored_weight_mass": stored_weight_mass(config),
        "eta_alpha": float(config.eta * config.alpha),
    }


def apply_condition(
    config: ArchiveFractalConfig, condition: str
) -> ArchiveFractalConfig:
    if condition == "baseline" or condition == "shuffled_memory":
        return config
    if condition == "eta_zero":
        return replace(config, eta=0.0)
    if condition == "single_scale":
        return replace(config, amplitude_att=0.0)
    raise ValueError(f"unknown condition: {condition}")


def archive_force(
    x: np.ndarray,
    memory: np.ndarray,
    weights: np.ndarray,
    config: ArchiveFractalConfig,
) -> np.ndarray:
    if len(memory) == 0:
        return np.zeros(config.dim, dtype=float)
    r = x[None, :] - memory
    r2 = np.einsum("ij,ij->i", r, r)
    rep = (
        config.amplitude_rep
        * np.exp(-r2 / (2.0 * config.sigma_rep * config.sigma_rep))
        / (config.sigma_rep * config.sigma_rep)
    )
    att = (
        config.amplitude_att
        * np.exp(-r2 / (2.0 * config.sigma_att * config.sigma_att))
        / (config.sigma_att * config.sigma_att)
    )
    return np.sum((weights * (rep - att))[:, None] * r, axis=0)


def simulate_archive_fractal_numpy(
    config: ArchiveFractalConfig,
    *,
    seed: int,
    shuffle_memory: bool = False,
) -> dict[str, np.ndarray]:
    if config.steps < 1:
        raise ValueError("steps must be positive")
    if config.dim < 1:
        raise ValueError("dim must be positive")
    if config.sample_every < 1:
        raise ValueError("sample_every must be positive")
    if config.max_memory < 1:
        raise ValueError("max_memory must be positive")

    rng = np.random.default_rng(seed)
    memory_horizon = horizon(config)
    memory = np.zeros((memory_horizon, config.dim), dtype=float)
    weights = np.zeros(memory_horizon, dtype=float)
    idx = 0
    filled = 0
    beta = deposit_beta(config)
    x = np.zeros(config.dim, dtype=float)
    samples = []
    sample_steps = []

    for step in range(1, config.steps + 1):
        if filled:
            if shuffle_memory:
                order = rng.permutation(filled)
                gradient_memory = memory[:filled][order]
            else:
                gradient_memory = memory[:filled]
            force = archive_force(x, gradient_memory, weights[:filled], config)
        else:
            force = np.zeros(config.dim, dtype=float)

        x = x + config.epsilon * rng.normal(size=config.dim) + config.eta * config.alpha * force

        weights *= 1.0 - config.alpha
        memory[idx] = x
        weights[idx] = beta
        if filled < memory_horizon:
            filled += 1
        idx = (idx + 1) % memory_horizon

        if step >= config.burn_in and step % config.sample_every == 0:
            samples.append(x.copy())
            sample_steps.append(step)

    return {
        "samples": np.asarray(samples, dtype=float),
        "sample_steps": np.asarray(sample_steps, dtype=int),
        "final_x": x.copy(),
        "memory": memory[:filled].copy(),
        "weights": weights[:filled].copy(),
    }


@njit(cache=True)
def _simulate_archive_fractal_numba(
    steps: int,
    dim: int,
    epsilon: float,
    eta: float,
    alpha: float,
    deposit_beta: float,
    amplitude_rep: float,
    amplitude_att: float,
    sigma_rep: float,
    sigma_att: float,
    memory_factor: float,
    max_memory: int,
    burn_in: int,
    sample_every: int,
    seed: int,
):
    np.random.seed(seed)
    memory_horizon = int(memory_factor / alpha) + 1
    if memory_horizon > max_memory:
        memory_horizon = max_memory
    if memory_horizon < 1:
        memory_horizon = 1

    memory = np.zeros((memory_horizon, dim), np.float64)
    weights = np.zeros(memory_horizon, np.float64)
    x = np.zeros(dim, np.float64)
    max_samples = steps // sample_every + 2
    samples = np.zeros((max_samples, dim), np.float64)
    sample_steps = np.zeros(max_samples, np.int64)
    n_sample = 0
    idx = 0
    filled = 0
    sigma_rep2 = sigma_rep * sigma_rep
    sigma_att2 = sigma_att * sigma_att

    for step in range(1, steps + 1):
        force = np.zeros(dim, np.float64)
        for k in range(filled):
            r2 = 0.0
            for d in range(dim):
                diff = x[d] - memory[k, d]
                r2 += diff * diff
            rep = amplitude_rep * np.exp(-r2 / (2.0 * sigma_rep2)) / sigma_rep2
            att = amplitude_att * np.exp(-r2 / (2.0 * sigma_att2)) / sigma_att2
            fac = weights[k] * (rep - att)
            for d in range(dim):
                force[d] += fac * (x[d] - memory[k, d])

        for d in range(dim):
            x[d] = x[d] + epsilon * np.random.normal(0.0, 1.0) + eta * alpha * force[d]

        for k in range(memory_horizon):
            weights[k] *= 1.0 - alpha
        for d in range(dim):
            memory[idx, d] = x[d]
        weights[idx] = deposit_beta
        if filled < memory_horizon:
            filled += 1
        idx = (idx + 1) % memory_horizon

        if step >= burn_in and step % sample_every == 0:
            for d in range(dim):
                samples[n_sample, d] = x[d]
            sample_steps[n_sample] = step
            n_sample += 1

    return samples[:n_sample], sample_steps[:n_sample], x, memory, weights, n_sample, filled


def simulate_archive_fractal_numba(
    config: ArchiveFractalConfig, *, seed: int
) -> dict[str, np.ndarray]:
    if not _NUMBA_AVAILABLE:
        raise ImportError("numba is not installed")
    samples, sample_steps, x, memory, weights, n_sample, filled = (
        _simulate_archive_fractal_numba(
            config.steps,
            config.dim,
            config.epsilon,
            config.eta,
            config.alpha,
            deposit_beta(config),
            config.amplitude_rep,
            config.amplitude_att,
            config.sigma_rep,
            config.sigma_att,
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
        "memory": memory[:filled].copy(),
        "weights": weights[:filled].copy(),
    }


def run_simulation(
    config: ArchiveFractalConfig,
    *,
    condition: str,
    seed: int,
    engine: str,
) -> tuple[dict[str, np.ndarray], str]:
    shuffle_memory = condition == "shuffled_memory"
    if engine in {"auto", "numba"} and not shuffle_memory:
        try:
            return simulate_archive_fractal_numba(config, seed=seed), "numba"
        except ImportError:
            if engine == "numba":
                raise
    return (
        simulate_archive_fractal_numpy(config, seed=seed, shuffle_memory=shuffle_memory),
        "numpy-shuffled" if shuffle_memory else "numpy",
    )


def legacy_occupancy_dimension(points: np.ndarray) -> OccupancyDetails:
    if len(points) < 3:
        empty = np.array([], dtype=float)
        return OccupancyDetails(float("nan"), empty, empty)

    pts = points - np.min(points, axis=0, keepdims=True)
    ranges = np.max(pts, axis=0)
    max_range = float(np.max(ranges))
    if not np.isfinite(max_range) or max_range <= 0.0:
        empty = np.array([], dtype=float)
        return OccupancyDetails(float("nan"), empty, empty)

    sizes = np.logspace(np.log10(max_range / 200.0), np.log10(max_range / 5.0), 12)
    counts = []
    for size in sizes:
        boxes = np.floor(pts / size).astype(np.int64)
        counts.append(len(np.unique(boxes, axis=0)))
    counts_arr = np.asarray(counts, dtype=float)
    if np.unique(counts_arr).size < 2:
        dimension = float("nan")
    else:
        coeff = np.polyfit(np.log(1.0 / sizes), np.log(counts_arr), 1)
        dimension = float(coeff[0])
    return OccupancyDetails(dimension, sizes, counts_arr)


def occupancy_window_metrics(
    scales: list[float] | np.ndarray,
    counts: list[float] | np.ndarray,
    *,
    n_samples: int,
) -> tuple[dict[str, object], list[float]]:
    window = fit_occupancy_scaling_window(scales, counts, n_samples=n_samples)
    scales_arr = np.asarray(scales, dtype=float)
    counts_arr = np.asarray(counts, dtype=float)
    payload: dict[str, object] = asdict(window)
    if window.start_index >= 0 and window.stop_index > window.start_index:
        window_scales = scales_arr[window.start_index : window.stop_index]
        window_counts = counts_arr[window.start_index : window.stop_index]
        payload.update(
            {
                "scale_min": float(np.min(window_scales)),
                "scale_max": float(np.max(window_scales)),
                "count_min": float(np.min(window_counts)),
                "count_max": float(np.max(window_counts)),
            }
        )
    else:
        payload.update(
            {
                "scale_min": float("nan"),
                "scale_max": float("nan"),
                "count_min": float("nan"),
                "count_max": float("nan"),
            }
        )
    slopes = occupancy_local_slopes(scales_arr, counts_arr)
    return payload, slopes.tolist()


def add_occupancy_window_metrics(run: dict[str, object]) -> dict[str, object]:
    if "occupancy_scales" not in run or "occupancy_counts" not in run:
        return run
    metrics, local_slopes = occupancy_window_metrics(
        run["occupancy_scales"],
        run["occupancy_counts"],
        n_samples=int(run.get("n_samples", 0)),
    )
    run["D_occ_windowed"] = float(metrics["dimension"])
    run["D_occ_window_valid"] = bool(metrics["valid_scaling"])
    run["occupancy_fit_window"] = metrics
    run["occupancy_local_slopes"] = local_slopes
    return run

def spectral_subset(points: np.ndarray, max_points: int) -> np.ndarray:
    if len(points) <= max_points:
        return points
    idx = np.linspace(0, len(points) - 1, max_points).astype(int)
    return points[idx]


def finite_values(values: list[float]) -> list[float]:
    return [value for value in values if math.isfinite(value)]


def summarize(values: list[float], *, n_boot: int = 1000) -> dict[str, float | int]:
    vals = finite_values(values)
    if not vals:
        return {
            "n": 0,
            "mean": float("nan"),
            "std": float("nan"),
            "min": float("nan"),
            "max": float("nan"),
            "ci_95_lo": float("nan"),
            "ci_95_hi": float("nan"),
        }
    mean, lo, hi = bootstrap_mean_ci(vals, level=0.95, n_boot=n_boot, seed=0)
    return {
        "n": len(vals),
        "mean": float(mean),
        "std": float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0,
        "min": float(np.min(vals)),
        "max": float(np.max(vals)),
        "ci_95_lo": float(lo),
        "ci_95_hi": float(hi),
    }


def run_case(
    *,
    base_config: ArchiveFractalConfig,
    condition: str,
    seed: int,
    steps: int,
    burn_in_fraction: float,
    engine: str,
    voxel_size: float,
    spectral_max_points: int,
) -> dict[str, object]:
    config = replace(
        base_config,
        steps=steps,
        burn_in=int(steps * burn_in_fraction),
    )
    config = apply_condition(config, condition)

    started = time.perf_counter()
    result, engine_used = run_simulation(config, condition=condition, seed=seed, engine=engine)
    elapsed = time.perf_counter() - started
    samples = result["samples"]

    occ = legacy_occupancy_dimension(samples)
    occ_window, occ_local_slopes = occupancy_window_metrics(
        occ.scales, occ.counts, n_samples=len(samples)
    )
    reference_occ = occupancy_dimension(samples, n_scales=10, min_count=2)
    spec_points = spectral_subset(samples, spectral_max_points)
    metrics = config_metrics(config)

    return {
        "condition": condition,
        "seed": seed,
        "steps": steps,
        "dim": int(config.dim),
        "alpha": float(config.alpha),
        "deposit_beta": metrics["deposit_beta"],
        "beta_over_alpha": metrics["beta_over_alpha"],
        "eta": float(config.eta),
        "eta_alpha": metrics["eta_alpha"],
        "sigma_rep": float(config.sigma_rep),
        "sigma_att": float(config.sigma_att),
        "amplitude_rep": float(config.amplitude_rep),
        "amplitude_att": float(config.amplitude_att),
        "uncapped_horizon": metrics["uncapped_horizon"],
        "used_horizon": metrics["used_horizon"],
        "stored_weight_mass": metrics["stored_weight_mass"],
        "max_memory": int(config.max_memory),
        "engine": engine_used,
        "n_samples": int(len(samples)),
        "elapsed_seconds": float(elapsed),
        "steps_per_second": float(steps / elapsed) if elapsed > 0 else None,
        "D_occ": float(occ.dimension),
        "D_occ_estimator": "archive_fraktale_box_counting",
        "D_occ_reference": float(reference_occ),
        "D_occ_windowed": float(occ_window["dimension"]),
        "D_occ_window_valid": bool(occ_window["valid_scaling"]),
        "D_cov": float(covariance_dimension(samples)),
        "D_spec": float(spectral_dimension(spec_points)),
        "spectral_points": int(len(spec_points)),
        "occupancy_scales": occ.scales.tolist(),
        "occupancy_counts": occ.counts.tolist(),
        "occupancy_fit_window": occ_window,
        "occupancy_local_slopes": occ_local_slopes,
        "residence": residence_statistics(samples, voxel_size=voxel_size, min_visits=3),
        "config": asdict(config),
    }


def summarize_runs(runs: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[int, float, float, float, float, str, int], list[dict[str, object]]] = {}
    for run in runs:
        key = (
            int(run["dim"]),
            float(run["alpha"]),
            float(run["deposit_beta"]),
            float(run["sigma_rep"]),
            float(run["sigma_att"]),
            str(run["condition"]),
            int(run["steps"]),
        )
        groups.setdefault(key, []).append(run)

    summary = []
    for (dim, alpha, beta, sigma_rep, sigma_att, condition, steps), group in sorted(
        groups.items(), key=lambda item: (item[0][6], item[0][0], item[0][1], item[0][2], item[0][5])
    ):
        speeds = [
            float(run["steps_per_second"])
            for run in group
            if run["steps_per_second"] is not None
        ]
        row = {
            "dim": dim,
            "alpha": alpha,
            "deposit_beta": beta,
            "beta_over_alpha": float(group[0]["beta_over_alpha"]),
            "sigma_rep": sigma_rep,
            "sigma_att": sigma_att,
            "condition": condition,
            "steps": steps,
            "n_runs": len(group),
            "eta": float(group[0]["eta"]),
            "eta_alpha": float(group[0]["eta_alpha"]),
            "used_horizon": int(group[0]["used_horizon"]),
            "stored_weight_mass": float(group[0]["stored_weight_mass"]),
            "D_occ": summarize([float(run["D_occ"]) for run in group]),
            "D_occ_reference": summarize(
                [float(run["D_occ_reference"]) for run in group]
            ),
            "D_occ_windowed": summarize(
                [float(run.get("D_occ_windowed", float("nan"))) for run in group]
            ),
            "D_occ_window_valid_fraction": float(
                np.mean([bool(run.get("D_occ_window_valid", False)) for run in group])
            ),
            "D_cov": summarize([float(run["D_cov"]) for run in group]),
            "D_spec": summarize([float(run["D_spec"]) for run in group]),
            "mean_steps_per_second": float(np.mean(speeds)) if speeds else None,
        }
        summary.append(row)
    return summary


def markdown_table(summary: list[dict[str, object]]) -> str:
    lines = [
        (
            "| dim | alpha | beta/alpha | sigma_att | condition | steps | runs | D_occ mean | "
            "D_occ 95% CI | D_win mean | valid win | D_cov mean | D_spec mean | horizon | mass |"
        ),
        "| ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary:
        d_occ = row["D_occ"]
        d_win = row["D_occ_windowed"]
        d_cov = row["D_cov"]
        d_spec = row["D_spec"]
        assert isinstance(d_occ, dict)
        assert isinstance(d_win, dict)
        assert isinstance(d_cov, dict)
        assert isinstance(d_spec, dict)
        ci = f"{d_occ['ci_95_lo']:.3f}..{d_occ['ci_95_hi']:.3f}"
        lines.append(
            "| "
            f"{row['dim']} | "
            f"{row['alpha']:.5g} | "
            f"{row['beta_over_alpha']:.5g} | "
            f"{row['sigma_att']:.5g} | "
            f"{row['condition']} | "
            f"{row['steps']} | "
            f"{row['n_runs']} | "
            f"{d_occ['mean']:.3f} | "
            f"{ci} | "
            f"{d_win['mean']:.3f} | "
            f"{row['D_occ_window_valid_fraction']:.2f} | "
            f"{d_cov['mean']:.3f} | "
            f"{d_spec['mean']:.3f} | "
            f"{row['used_horizon']} | "
            f"{row['stored_weight_mass']:.3f} |"
        )
    return "\n".join(lines)


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def write_report(
    *,
    output_path: Path,
    output_json: Path,
    metadata: dict[str, object],
    summary: list[dict[str, object]],
) -> None:
    text = f"""# Dimension Reproduction Pilot

Datum: {date.today().isoformat()}

Quelle:

- Skript: `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- JSON: `{relative_path(output_json)}`
- Git-Revision: `{metadata["git_revision"]}`

## Ziel

Ressourcenschonender Seed-Pilot fuer den archivierten Dimensionsbefund aus
`experiments/fractal_analysis/Fraktale/resultsN.csv`. Der Lauf nutzt den
historischen Fraktal-Parametersatz und den historischen Box-Counting-Schaetzer.
Er ersetzt nicht den `N=60,000,000`-Befund, sondern prueft, ob bei kleineren
`N` bereits eine trennbare Signatur gegen einfache Negativkontrollen sichtbar
wird.

## Parameter

- embedding dimensions: `{metadata["dims"]}`
- alpha/lambda_m values: `{metadata["alpha_values"]}`
- beta values: `{metadata["beta_values"]}`
- beta/alpha values: `{metadata["beta_over_alpha_values"]}`
- seeds: `{metadata["seeds"]}`
- steps ladder: `{metadata["steps_list"]}`
- conditions: `{metadata["conditions"]}`
- engine request: `{metadata["engine_request"]}`
- coupling mode: `{metadata["coupling_mode"]}`
- eta-alpha target: `{metadata["eta_alpha_target"]}`
- memory mode: `{metadata["memory_mode"]}`
- memory tail mass: `{metadata["memory_tail_mass"]}`
- sample_every: `{metadata["sample_every"]}`
- configured max_memory: `{metadata["configured_max_memory"]}`
- burn-in fraction: `{metadata["burn_in_fraction"]}`
- estimator: `archive_fraktale_box_counting`

## Ergebnis

{markdown_table(summary)}

## Interpretation

Dieser Pilot ist ein Ressourcen-Test und ein Kontrollpfad. Ein belastbarer
Claim braucht weiterhin groessere `N`, mehr Seeds und stabilere Fitfenster.
Ein starkes Ergebnis waere hier nicht `D_occ` nahe 3 allein, sondern eine
konsistente Trennung des Baseline-Regimes von `eta_zero`, `single_scale` und
`shuffled_memory` ueber mehrere Diagnostiken.
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def reanalyze_occupancy_windows(payload: dict[str, object]) -> dict[str, object]:
    runs = payload.get("runs", [])
    if not isinstance(runs, list):
        raise ValueError("payload must contain a runs list")
    for run in runs:
        if isinstance(run, dict):
            add_occupancy_window_metrics(run)
    payload["summary"] = summarize_runs([run for run in runs if isinstance(run, dict)])
    metadata = payload.setdefault("metadata", {})
    if isinstance(metadata, dict):
        metadata["occupancy_window_method"] = {
            "min_points": 4,
            "min_boxes": 20,
            "max_count_fraction": 0.8,
            "min_r_squared": 0.98,
            "max_local_slope_std": 0.35,
        }
        metadata["occupancy_window_reanalysis_date"] = date.today().isoformat()
    return payload


def resolved_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def reanalyze_json_file(
    *,
    input_path: Path,
    output_path: Path,
    report_output: Path | None,
) -> None:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    payload = reanalyze_occupancy_windows(payload)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    metadata = payload.get("metadata", {})
    summary = payload.get("summary", [])
    if report_output is not None:
        if not isinstance(metadata, dict) or not isinstance(summary, list):
            raise ValueError("reanalyzed payload has invalid metadata or summary")
        write_report(
            output_path=report_output,
            output_json=output_path,
            metadata=metadata,
            summary=summary,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run a resource-bounded seed pilot for the archived near-3 "
            "fractal-dimension signal with negative controls."
        )
    )
    parser.add_argument("--dim", type=int, default=5, help="Embedding dimension")
    parser.add_argument(
        "--dims",
        type=parse_int_list,
        default=None,
        help="Comma-separated embedding dimensions. Overrides --dim.",
    )
    parser.add_argument(
        "--steps-list",
        type=parse_int_list,
        default=parse_int_list("10000,30000,60000"),
        help="Comma-separated step counts",
    )
    parser.add_argument(
        "--seeds",
        type=parse_int_list,
        default=parse_int_list("1,2,3"),
        help="Comma-separated seed list",
    )
    parser.add_argument(
        "--conditions",
        type=parse_conditions,
        default=parse_conditions("baseline,eta_zero,single_scale,shuffled_memory"),
        help="Comma-separated conditions",
    )
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--burn-in-fraction", type=float, default=0.2)
    parser.add_argument("--max-memory", type=int, default=300)
    parser.add_argument("--epsilon", type=float, default=0.05)
    parser.add_argument("--eta", type=float, default=2.0)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument(
        "--alpha-list",
        type=parse_float_list,
        default=None,
        help="Comma-separated alpha/lambda_m values. Overrides --alpha.",
    )
    parser.add_argument(
        "--beta",
        type=float,
        default=None,
        help="Deposited memory weight beta. Defaults to beta=alpha for legacy runs.",
    )
    parser.add_argument(
        "--beta-list",
        type=parse_float_list,
        default=None,
        help="Comma-separated deposited beta values. Mutually exclusive with --beta-over-alpha-list.",
    )
    parser.add_argument(
        "--beta-over-alpha-list",
        type=parse_float_list,
        default=None,
        help="Comma-separated beta/alpha ratios. Mutually exclusive with --beta-list.",
    )
    parser.add_argument(
        "--coupling-mode",
        choices=("historical", "fixed-eta-alpha"),
        default="historical",
        help=(
            "historical keeps eta fixed; fixed-eta-alpha adjusts eta so eta*alpha "
            "stays constant."
        ),
    )
    parser.add_argument(
        "--eta-alpha-target",
        type=float,
        default=None,
        help=(
            "Target eta*alpha for --coupling-mode fixed-eta-alpha. Defaults to "
            "the product of --eta and --alpha."
        ),
    )
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=0.15)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=3.0)
    parser.add_argument("--memory-factor", type=float, default=5.0)
    parser.add_argument(
        "--memory-mode",
        choices=("capped", "full", "tail-mass"),
        default="capped",
        help=(
            "capped uses --max-memory; full uses int(memory_factor/alpha)+1; "
            "tail-mass chooses the horizon needed for --memory-tail-mass."
        ),
    )
    parser.add_argument(
        "--memory-tail-mass",
        type=float,
        default=0.95,
        help="Target stored exponential weight mass for --memory-mode tail-mass.",
    )
    parser.add_argument("--voxel-size", type=float, default=0.5)
    parser.add_argument("--spectral-max-points", type=int, default=300)
    parser.add_argument(
        "--engine",
        choices=("auto", "numpy", "numba"),
        default="auto",
        help="Simulation engine. auto uses numba when importable.",
    )
    parser.add_argument(
        "--reanalyze-json",
        type=Path,
        default=None,
        help="Existing result JSON to annotate with automatic occupancy fit windows.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="With --reanalyze-json, overwrite the input JSON path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/fractal_analysis/dimension_reproduction_pilot.json"),
        help="Output JSON path",
    )
    parser.add_argument(
        "--report-output",
        type=Path,
        default=None,
        help="Optional Markdown report path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.reanalyze_json is not None:
        input_path = resolved_path(args.reanalyze_json)
        output_path = input_path if args.in_place else resolved_path(args.output)
        report_output = resolved_path(args.report_output) if args.report_output else None
        reanalyze_json_file(
            input_path=input_path,
            output_path=output_path,
            report_output=report_output,
        )
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        print(f"reanalyzed JSON to {output_path}")
        if report_output is not None:
            print(f"wrote report to {report_output}")
        print(markdown_table(payload["summary"]))
        return

    if not 0.0 <= args.burn_in_fraction < 1.0:
        raise SystemExit("--burn-in-fraction must be in [0, 1)")
    if args.max_memory < 1:
        raise SystemExit("--max-memory must be positive")
    if not 0.0 < args.memory_tail_mass < 1.0:
        raise SystemExit("--memory-tail-mass must satisfy 0 < value < 1")
    beta_sources = sum(value is not None for value in (args.beta, args.beta_list, args.beta_over_alpha_list))
    if beta_sources > 1:
        raise SystemExit("Use only one of --beta, --beta-list, or --beta-over-alpha-list")
    if args.beta is not None and args.beta < 0.0:
        raise SystemExit("--beta must be non-negative")
    if args.beta_list is not None and any(beta < 0.0 for beta in args.beta_list):
        raise SystemExit("--beta-list values must be non-negative")
    if args.beta_over_alpha_list is not None and any(ratio < 0.0 for ratio in args.beta_over_alpha_list):
        raise SystemExit("--beta-over-alpha-list values must be non-negative")

    dim_values = args.dims if args.dims is not None else [args.dim]
    alpha_values = args.alpha_list if args.alpha_list is not None else [args.alpha]
    eta_alpha_target = args.eta_alpha_target
    if args.coupling_mode == "fixed-eta-alpha" and eta_alpha_target is None:
        eta_alpha_target = args.eta * args.alpha

    def beta_values_for_alpha(alpha: float) -> list[float]:
        if args.beta_list is not None:
            return args.beta_list
        if args.beta_over_alpha_list is not None:
            return [ratio * alpha for ratio in args.beta_over_alpha_list]
        if args.beta is not None:
            return [args.beta]
        return [alpha]

    base_configs = []
    for dim in dim_values:
        for alpha in alpha_values:
            for beta in beta_values_for_alpha(alpha):
                eta = args.eta
                if args.coupling_mode == "fixed-eta-alpha":
                    assert eta_alpha_target is not None
                    eta = eta_alpha_target / alpha
                max_memory = max_memory_for_mode(
                    alpha=alpha,
                    memory_factor=args.memory_factor,
                    configured_max_memory=args.max_memory,
                    memory_mode=args.memory_mode,
                    target_mass=args.memory_tail_mass,
                )
                base_configs.append(
                    ArchiveFractalConfig(
                        steps=max(args.steps_list),
                        dim=dim,
                        epsilon=args.epsilon,
                        eta=eta,
                        alpha=alpha,
                        deposit_beta=beta,
                        sigma_rep=args.sigma_rep,
                        sigma_att=args.sigma_att,
                        amplitude_rep=args.amplitude_rep,
                        amplitude_att=args.amplitude_att,
                        memory_factor=args.memory_factor,
                        max_memory=max_memory,
                        burn_in=0,
                        sample_every=args.sample_every,
                    )
                )

    runs = []
    total_started = time.perf_counter()
    for base_config in base_configs:
        for steps in args.steps_list:
            for condition in args.conditions:
                for seed in args.seeds:
                    print(
                        "running "
                        f"dim={base_config.dim} alpha={base_config.alpha:g} beta/alpha={beta_over_alpha(base_config):g} "
                        f"condition={condition} steps={steps} seed={seed}"
                    )
                    runs.append(
                        run_case(
                            base_config=base_config,
                            condition=condition,
                            seed=seed,
                            steps=steps,
                            burn_in_fraction=args.burn_in_fraction,
                            engine=args.engine,
                            voxel_size=args.voxel_size,
                            spectral_max_points=args.spectral_max_points,
                        )
                    )
    total_elapsed = time.perf_counter() - total_started
    summary = summarize_runs(runs)

    output_path = args.output
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    metadata = {
        "git_revision": git_revision(),
        "base_configs": [asdict(config) for config in base_configs],
        "dims": dim_values,
        "alpha_values": alpha_values,
        "beta_values": sorted({deposit_beta(config) for config in base_configs}),
        "beta_over_alpha_values": sorted({beta_over_alpha(config) for config in base_configs}),
        "steps_list": args.steps_list,
        "seeds": args.seeds,
        "conditions": args.conditions,
        "engine_request": args.engine,
        "coupling_mode": args.coupling_mode,
        "eta_alpha_target": eta_alpha_target,
        "memory_mode": args.memory_mode,
        "memory_tail_mass": args.memory_tail_mass,
        "sample_every": args.sample_every,
        "configured_max_memory": args.max_memory,
        "burn_in_fraction": args.burn_in_fraction,
        "total_elapsed_seconds": float(total_elapsed),
    }
    payload = {
        "metadata": metadata,
        "summary": summary,
        "runs": runs,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    report_output = args.report_output
    if report_output is not None:
        if not report_output.is_absolute():
            report_output = ROOT / report_output
        write_report(
            output_path=report_output,
            output_json=output_path,
            metadata=metadata,
            summary=summary,
        )

    print(f"wrote JSON to {output_path}")
    if report_output is not None:
        print(f"wrote report to {report_output}")
    print(markdown_table(summary))


if __name__ == "__main__":
    main()
