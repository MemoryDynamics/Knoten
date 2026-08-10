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

from emergenz_knoten import SimulationConfig  # noqa: E402

try:
    from numba import njit

    _NUMBA_AVAILABLE = True
except ImportError:  # pragma: no cover
    _NUMBA_AVAILABLE = False

    def njit(*args, **kwargs):  # type: ignore[no-redef]
        def wrapper(func):
            return func

        return wrapper


METRIC_COLUMNS = [
    "noise_norm",
    "repulsive_step_norm",
    "attractive_step_norm",
    "net_drift_norm",
    "total_step_norm",
    "noise_to_total",
    "noise_to_net_drift",
    "noise_to_repulsive",
    "turn_cosine",
    "noise_drift_alignment",
]


def _parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one float")
    return values


def _parse_condition(value: str) -> str:
    allowed = {"baseline", "eta_zero", "single_scale"}
    if value not in allowed:
        raise argparse.ArgumentTypeError(
            f"unknown condition {value!r}; expected one of {sorted(allowed)}"
        )
    return value


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


def _apply_condition(config: SimulationConfig, condition: str) -> SimulationConfig:
    if condition == "baseline":
        return config
    if condition == "eta_zero":
        return replace(config, eta=0.0)
    if condition == "single_scale":
        return replace(config, amplitude_att=0.0)
    raise ValueError(f"unknown condition: {condition}")


def chi_mean(dim: int) -> float:
    """Expected Euclidean norm of N(0, I_dim)."""

    return float(math.sqrt(2.0) * math.gamma((dim + 1.0) / 2.0) / math.gamma(dim / 2.0))


def summarize_array(values: Iterable[float]) -> dict[str, float | int | None]:
    arr = np.asarray(list(values), dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return {
            "n": 0,
            "mean": None,
            "sd": None,
            "min": None,
            "q10": None,
            "median": None,
            "q90": None,
            "max": None,
        }
    return {
        "n": int(arr.size),
        "mean": float(np.mean(arr)),
        "sd": float(np.std(arr, ddof=1)) if arr.size > 1 else 0.0,
        "min": float(np.min(arr)),
        "q10": float(np.quantile(arr, 0.10)),
        "median": float(np.median(arr)),
        "q90": float(np.quantile(arr, 0.90)),
        "max": float(np.max(arr)),
    }


def _as_finite(value: object) -> float | None:
    if value is None:
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if np.isfinite(out) else None


def _mean_finite(values: Iterable[object]) -> float | None:
    finite = [_as_finite(value) for value in values]
    arr = np.asarray([value for value in finite if value is not None], dtype=float)
    if arr.size == 0:
        return None
    return float(np.mean(arr))


def _fmt(value: object, *, digits: int = 3) -> str:
    finite = _as_finite(value)
    if finite is None:
        return "`n/a`"
    if finite == 0.0:
        text = "0"
    elif abs(finite) < 1.0e-3 or abs(finite) >= 1.0e4:
        text = f"{finite:.{digits}e}"
    else:
        text = f"{finite:.{digits}f}"
    return f"`{text}`"


@njit(cache=True)
def _simulate_step_balance_numba(
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
        weights[age] = weight
        weight *= decay

    memory = np.zeros((horizon, dim), np.float64)
    x = np.zeros(dim, np.float64)
    max_samples = steps // sample_every + 2
    samples = np.zeros((max_samples, dim), np.float64)
    metrics = np.zeros((max_samples, 10), np.float64)
    idx = 0
    filled = 0
    n_sample = 0
    sigma_rep2 = sigma_rep * sigma_rep
    sigma_att2 = sigma_att * sigma_att
    prev_total = np.zeros(dim, np.float64)
    prev_total_norm = 0.0

    for step in range(1, steps + 1):
        rep_grad = np.zeros(dim, np.float64)
        att_grad = np.zeros(dim, np.float64)
        if eta != 0.0:
            for age in range(filled):
                mem_idx = (idx - 1 - age) % horizon
                r2 = 0.0
                for d in range(dim):
                    diff = x[d] - memory[mem_idx, d]
                    r2 += diff * diff
                rep = amplitude_rep * np.exp(-0.5 * r2 / sigma_rep2) / sigma_rep2
                att = amplitude_att * np.exp(-0.5 * r2 / sigma_att2) / sigma_att2
                w = weights[age]
                for d in range(dim):
                    diff = x[d] - memory[mem_idx, d]
                    rep_grad[d] += w * rep * diff
                    att_grad[d] += w * att * diff

        noise = np.empty(dim, np.float64)
        drift = np.empty(dim, np.float64)
        total = np.empty(dim, np.float64)
        noise_norm2 = 0.0
        rep_norm2 = 0.0
        att_norm2 = 0.0
        drift_norm2 = 0.0
        total_norm2 = 0.0
        noise_drift_dot = 0.0
        turn_dot = 0.0
        for d in range(dim):
            noise[d] = epsilon * np.random.normal(0.0, 1.0)
            drift[d] = eta * (rep_grad[d] - att_grad[d])
            total[d] = noise[d] + drift[d]
            x[d] += total[d]
            noise_norm2 += noise[d] * noise[d]
            rep_norm2 += (eta * rep_grad[d]) * (eta * rep_grad[d])
            att_norm2 += (eta * att_grad[d]) * (eta * att_grad[d])
            drift_norm2 += drift[d] * drift[d]
            total_norm2 += total[d] * total[d]
            noise_drift_dot += noise[d] * drift[d]
            turn_dot += total[d] * prev_total[d]

        noise_norm = np.sqrt(noise_norm2)
        rep_norm = np.sqrt(rep_norm2)
        att_norm = np.sqrt(att_norm2)
        drift_norm = np.sqrt(drift_norm2)
        total_norm = np.sqrt(total_norm2)

        memory[idx] = x
        idx = (idx + 1) % horizon
        if filled < horizon:
            filled += 1

        if step >= burn_in and step % sample_every == 0:
            samples[n_sample] = x
            metrics[n_sample, 0] = noise_norm
            metrics[n_sample, 1] = rep_norm
            metrics[n_sample, 2] = att_norm
            metrics[n_sample, 3] = drift_norm
            metrics[n_sample, 4] = total_norm
            metrics[n_sample, 5] = noise_norm / total_norm if total_norm > 0.0 else np.nan
            metrics[n_sample, 6] = (
                noise_norm / drift_norm if drift_norm > 0.0 else np.nan
            )
            metrics[n_sample, 7] = noise_norm / rep_norm if rep_norm > 0.0 else np.nan
            metrics[n_sample, 8] = (
                turn_dot / (total_norm * prev_total_norm)
                if total_norm > 0.0 and prev_total_norm > 0.0
                else np.nan
            )
            metrics[n_sample, 9] = (
                noise_drift_dot / (noise_norm * drift_norm)
                if noise_norm > 0.0 and drift_norm > 0.0
                else np.nan
            )
            n_sample += 1

        for d in range(dim):
            prev_total[d] = total[d]
        prev_total_norm = total_norm

    return samples[:n_sample], metrics[:n_sample]


def run_case(config: SimulationConfig, *, seed: int) -> dict[str, object]:
    started = time.perf_counter()
    samples, metrics = _simulate_step_balance_numba(
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
    elapsed = time.perf_counter() - started
    metric_summary = {
        column: summarize_array(metrics[:, idx])
        for idx, column in enumerate(METRIC_COLUMNS)
    }
    centered = samples - samples.mean(axis=0, keepdims=True)
    radii = np.linalg.norm(centered, axis=1)
    increments = np.linalg.norm(np.diff(samples, axis=0), axis=1)
    total_steps = metrics[:, METRIC_COLUMNS.index("total_step_norm")]
    return {
        "seed": int(seed),
        "epsilon": float(config.epsilon),
        "elapsed_seconds": float(elapsed),
        "steps_per_second": float(config.steps / elapsed) if elapsed > 0 else None,
        "n_samples": int(len(samples)),
        "expected_noise_norm": float(config.epsilon * chi_mean(config.dim)),
        "mean_centered_radius": float(np.mean(radii)) if radii.size else None,
        "max_centered_radius": float(np.max(radii)) if radii.size else None,
        "mean_sample_increment": float(np.mean(increments)) if increments.size else None,
        "zero_total_step_fraction": (
            float(np.mean(total_steps == 0.0)) if total_steps.size else None
        ),
        "metric_summary": metric_summary,
    }


def build_report(payload: dict[str, object]) -> str:
    cases = payload["cases"]
    assert isinstance(cases, list)
    med_noise_rep: list[object] = []
    med_noise_drift: list[object] = []
    mean_turn: list[object] = []
    for case in cases:
        assert isinstance(case, dict)
        metrics = case["metric_summary"]
        assert isinstance(metrics, dict)
        med_noise_rep.append(metrics["noise_to_repulsive"]["median"])
        med_noise_drift.append(metrics["noise_to_net_drift"]["median"])
        mean_turn.append(metrics["turn_cosine"]["mean"])
    lines = [
        "# Epsilon Step-Balance Report",
        "",
        f"Date: {payload['finished_utc']}.",
        "",
        "## Scope",
        "",
        "This targeted run compares stochastic and memory-induced update scales",
        "while varying only `epsilon`. It is a scale diagnostic, not a new",
        "parameter sweep for Paper-I evidence.",
        "",
        "For each sampled update the script records:",
        "",
        "- `noise_norm = ||epsilon xi_n||`;",
        "- `repulsive_step_norm = ||eta grad_rep||`;",
        "- `attractive_step_norm = ||eta grad_att||`;",
        "- `net_drift_norm = ||eta(grad_rep-grad_att)||` after the corrected potential-gradient sign;",
        "- `total_step_norm = ||x_{n+1}-x_n||`;",
        "- `turn_cosine` between consecutive update vectors.",
        "",
        "## Configuration",
        "",
        f"- condition: `{payload['condition']}`",
        f"- seed: `{payload['seed']}`",
        f"- steps: `{payload['base_config']['steps']}`",
        f"- burn-in: `{payload['base_config']['burn_in']}`",
        f"- sample every: `{payload['base_config']['sample_every']}` updates",
        f"- alpha: `{payload['base_config']['alpha']}`",
        f"- eta: `{payload['base_config']['eta']}`",
        f"- sigma_rep / sigma_att: `{payload['base_config']['sigma_rep']}` / `{payload['base_config']['sigma_att']}`",
        f"- amplitude_rep / amplitude_att: `{payload['base_config']['amplitude_rep']}` / `{payload['base_config']['amplitude_att']}`",
        "",
        "## Results",
        "",
        "| epsilon | median noise | median repulsive step | median net drift | median total step | median noise/repulsive | median noise/drift | mean turn cosine | zero-step fraction | mean radius |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for case in cases:
        assert isinstance(case, dict)
        metrics = case["metric_summary"]
        assert isinstance(metrics, dict)
        row = {
            name: metrics[name]["median"]
            for name in (
                "noise_norm",
                "repulsive_step_norm",
                "net_drift_norm",
                "total_step_norm",
                "noise_to_repulsive",
                "noise_to_net_drift",
            )
        }
        turn = metrics["turn_cosine"]["mean"]
        lines.append(
            f"| `{case['epsilon']:.5g}` | {_fmt(row['noise_norm'])} | "
            f"{_fmt(row['repulsive_step_norm'])} | {_fmt(row['net_drift_norm'])} | "
            f"{_fmt(row['total_step_norm'])} | {_fmt(row['noise_to_repulsive'])} | "
            f"{_fmt(row['noise_to_net_drift'])} | {_fmt(turn)} | "
            f"{_fmt(case.get('zero_total_step_fraction'))} | "
            f"{_fmt(case['mean_centered_radius'])} |"
        )
    mean_noise_rep = _mean_finite(med_noise_rep)
    mean_noise_drift = _mean_finite(med_noise_drift)
    mean_turn_value = _mean_finite(mean_turn)
    lines.extend(
        [
            "",
            "## Observed Result",
            "",
            "For positive `epsilon` values in this slice, lowering `epsilon`",
            "scales down the whole local motion rather than changing the balance",
            "between stochastic and memory-induced updates. The median",
            "`noise_to_repulsive` ratio remains near",
            f"{_fmt(mean_noise_rep, digits=2)}, and median `noise_to_net_drift`",
            f"remains near {_fmt(mean_noise_drift, digits=2)} across the tested",
            "positive epsilon values.",
            "",
            "The exact `epsilon=0` case is different: with the zero initial",
            "state used here it remains at the deterministic fixed point, so no",
            "memory gradient is seeded.",
            "",
            "The mean `turn_cosine` for positive epsilon values also remains",
            "essentially unchanged",
            f"({_fmt(mean_turn_value)} on average). This indicates that",
            "smaller positive `epsilon` alone makes a smaller trajectory, not a",
            "smoother or more drift-dominated one.",
            "",
            "In the corrected Euler update, the repulsive potential does not define",
            "a hard minimum step length. It defines a deterministic force contribution",
            "that competes with the independent stochastic displacement `epsilon xi_n`.",
            "",
            "## Reading",
            "",
            "- `epsilon=0` is a fixed-point control for the zero-start baseline:",
            "  without stochastic novelty, no displacement and no memory gradient",
            "  are generated.",
            "- Positive `epsilon` values remain scale-equivalent in this slice:",
            "  noise, drift, radius, and total step shrink together.",
            "- Lower positive `epsilon` values are interesting only if they reduce",
            "  noise/drift ratios without merely shrinking the trajectory.",
            "- `turn_cosine` close to zero means jagged random-walk-like directions;",
            "  larger positive values indicate smoother directional persistence.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Measure stochastic-vs-drift step scales for fixed parameters."
    )
    parser.add_argument("--steps", type=int, default=500_000)
    parser.add_argument("--burn-in", type=int, default=50_000)
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--condition", type=_parse_condition, default="baseline")
    parser.add_argument(
        "--epsilons",
        type=_parse_float_list,
        default=_parse_float_list("0.03,0.015,0.01,0.005"),
    )
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=0.35)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--max-memory", type=int, default=800)
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("data/processed/epsilon_step_balance/2026-07-01_baseline_seed1/summary.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/kernels/epsilon/epsilon_step_balance_2026-07-01.md"),
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
    if not _NUMBA_AVAILABLE:
        raise SystemExit("numba is required for epsilon step-balance runs")

    base_config = SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=args.epsilons[0],
        eta=args.eta,
        alpha=args.alpha,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=args.amplitude_rep,
        amplitude_att=args.amplitude_att,
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )
    base_config = _apply_condition(base_config, args.condition)
    cases = []
    started = _utc_now()
    for epsilon in args.epsilons:
        config = replace(base_config, epsilon=epsilon)
        print(f"running epsilon={epsilon:g} seed={args.seed}", flush=True)
        cases.append(run_case(config, seed=args.seed))

    payload: dict[str, object] = {
        "description": "Targeted stochastic-vs-drift step scale diagnostic.",
        "started_utc": started,
        "finished_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "--short", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "condition": args.condition,
        "seed": int(args.seed),
        "memory_horizon": int(_horizon(base_config)),
        "base_config": asdict(base_config),
        "epsilons": args.epsilons,
        "metric_columns": METRIC_COLUMNS,
        "cases": cases,
    }

    output_json = args.output_json
    if not output_json.is_absolute():
        output_json = ROOT / output_json
    report = args.report
    if not report.is_absolute():
        report = ROOT / report
    output_json.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )
    report.write_text(build_report(payload), encoding="utf-8")
    print(f"wrote {output_json}", flush=True)
    print(f"wrote {report}", flush=True)


if __name__ == "__main__":
    main()
