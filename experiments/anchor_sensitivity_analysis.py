from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import SimulationConfig, covariance_dimension, residence_statistics
from emergenz_knoten.markov import (
    estimate_transfer_operator,
    leading_nontrivial_eigenvalues,
    spectral_gap,
    simulate_augmented_features,
    vector_autocorrelation,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run a small sensitivity analysis for the Paper-0 Markov layer. "
            "This is a diagnostic check, not a broad robustness claim."
        )
    )
    parser.add_argument("--steps", type=int, default=3000)
    parser.add_argument("--burn-in", type=int, default=300)
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3])
    parser.add_argument("--alpha", type=float, nargs="+", default=[0.02, 0.05])
    parser.add_argument("--epsilon", type=float, default=0.03)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=0.35)
    parser.add_argument("--max-memory", type=int, default=800)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--voxel-size", type=float, default=0.75)
    parser.add_argument("--feature-voxel-size", type=float, nargs="+", default=[0.75, 1.0, 1.25])
    parser.add_argument("--lag", type=int, nargs="+", default=[1, 3, 5])
    parser.add_argument("--base-lag", type=int, default=3)
    parser.add_argument("--base-feature-voxel-size", type=float, default=1.0)
    parser.add_argument("--max-ac-lag", type=int, default=10)
    parser.add_argument(
        "--controls",
        nargs="+",
        default=["baseline", "eta_zero", "shuffled_memory_features"],
        choices=["baseline", "eta_zero", "shuffled_memory_features"],
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/anchor_paper/sensitivity_summary.json",
        help="Machine-readable JSON output path.",
    )
    parser.add_argument(
        "--report",
        type=str,
        default="reports/anchor_sensitivity_2026-06-29.md",
        help="Markdown report output path.",
    )
    return parser.parse_args()


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


def _config(args: argparse.Namespace, *, alpha: float, eta: float | None = None) -> SimulationConfig:
    return SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=args.epsilon,
        eta=args.eta if eta is None else eta,
        alpha=alpha,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=args.amplitude_rep,
        amplitude_att=args.amplitude_att,
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )


def _finite_float(value: float | np.floating[Any] | None) -> float | None:
    if value is None:
        return None
    out = float(value)
    if not math.isfinite(out):
        return None
    return out


def _shuffle_memory_features(features: np.ndarray, *, dim: int, seed: int) -> np.ndarray:
    shuffled = np.asarray(features, dtype=float).copy()
    if shuffled.shape[0] < 2 or shuffled.shape[1] <= dim:
        return shuffled
    rng = np.random.default_rng(seed)
    permutation = rng.permutation(shuffled.shape[0])
    shuffled[:, dim:] = shuffled[permutation, dim:]
    return shuffled


def _mean_std(values: Iterable[float | None]) -> dict[str, float | None]:
    arr = np.asarray([v for v in values if v is not None], dtype=float)
    if arr.size == 0:
        return {"mean": None, "std": None}
    return {"mean": float(arr.mean()), "std": float(arr.std(ddof=0))}


def _fmt(value: float | None, *, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{value:.{digits}g}"


def _operator_metrics(
    *,
    samples: np.ndarray,
    sample_steps: np.ndarray,
    features: np.ndarray,
    args: argparse.Namespace,
    sample_lag: int,
    feature_voxel_size: float,
) -> dict[str, Any]:
    if len(samples) <= sample_lag:
        raise ValueError("not enough samples for requested sample_lag")
    transfer = estimate_transfer_operator(
        features,
        voxel_size=feature_voxel_size,
        sample_lag=sample_lag,
        sample_steps=sample_steps,
        lag_time=float(sample_lag * args.sample_every),
    )
    slow = leading_nontrivial_eigenvalues(transfer.eigenvalues, count=1)
    finite_rates = [float(r) for r in transfer.relaxation_rates if np.isfinite(r)]
    ac = vector_autocorrelation(samples, max_lag=args.max_ac_lag)
    residence = residence_statistics(samples, voxel_size=args.voxel_size, min_visits=3)
    return {
        "n_samples": int(len(samples)),
        "covariance_dimension": _finite_float(covariance_dimension(samples)),
        "autocorrelation_lag1": _finite_float(ac[1] if ac.size > 1 else None),
        "residence_mean": _finite_float(residence.get("mean_residence")),
        "residence_max": _finite_float(residence.get("max_residence")),
        "knot_count": _finite_float(residence.get("knot_count")),
        "n_states": int(transfer.transition_matrix.shape[0]),
        "nonzero_transitions": int(np.count_nonzero(transfer.counts)),
        "empty_rows": int(len(transfer.empty_rows)),
        "unit_eigenvalues": int(np.sum(np.isclose(np.abs(transfer.eigenvalues), 1.0))),
        "leading_nontrivial_abs": _finite_float(abs(slow[0]) if slow.size else None),
        "leading_relaxation_rate": _finite_float(finite_rates[0] if finite_rates else None),
        "spectral_gap": _finite_float(spectral_gap(transfer.eigenvalues)),
        "lag_updates": int(transfer.lag_updates or sample_lag * args.sample_every),
    }


def _case_specs(args: argparse.Namespace) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    seen: set[tuple[str, str, int, float]] = set()

    def add(category: str, control: str, sample_lag: int, feature_voxel_size: float) -> None:
        key = (category, control, sample_lag, float(feature_voxel_size))
        if key in seen:
            return
        seen.add(key)
        specs.append(
            {
                "category": category,
                "control": control,
                "sample_lag": int(sample_lag),
                "feature_voxel_size": float(feature_voxel_size),
            }
        )

    for lag in args.lag:
        add("lag_sensitivity", "baseline", int(lag), args.base_feature_voxel_size)
    for voxel_size in args.feature_voxel_size:
        add("voxel_sensitivity", "baseline", args.base_lag, float(voxel_size))
    for control in args.controls:
        add("negative_control", control, args.base_lag, args.base_feature_voxel_size)
    return specs


def run_case(
    args: argparse.Namespace,
    *,
    alpha: float,
    seed: int,
    spec: dict[str, Any],
    baseline: dict[str, np.ndarray],
    eta_zero: dict[str, np.ndarray] | None,
) -> dict[str, Any]:
    control = spec["control"]
    if control == "eta_zero":
        if eta_zero is None:
            raise ValueError("eta_zero control requested but not simulated")
        result = eta_zero
        features = result["augmented_features"]
    else:
        result = baseline
        features = result["augmented_features"]
        if control == "shuffled_memory_features":
            features = _shuffle_memory_features(features, dim=args.dim, seed=10_000 + seed)

    metrics = _operator_metrics(
        samples=result["samples"],
        sample_steps=result["sample_steps"],
        features=features,
        args=args,
        sample_lag=spec["sample_lag"],
        feature_voxel_size=spec["feature_voxel_size"],
    )
    return {
        "alpha": float(alpha),
        "seed": int(seed),
        "category": spec["category"],
        "control": control,
        "sample_lag": int(spec["sample_lag"]),
        "feature_voxel_size": float(spec["feature_voxel_size"]),
        "metrics": metrics,
    }


def aggregate_cases(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, float, int, float], list[dict[str, Any]]] = {}
    for case in cases:
        key = (
            case["category"],
            case["control"],
            case["alpha"],
            case["sample_lag"],
            case["feature_voxel_size"],
        )
        groups.setdefault(key, []).append(case)

    rows: list[dict[str, Any]] = []
    metric_names = [
        "leading_nontrivial_abs",
        "leading_relaxation_rate",
        "spectral_gap",
        "n_states",
        "empty_rows",
        "residence_mean",
        "autocorrelation_lag1",
    ]
    for key in sorted(groups):
        category, control, alpha, sample_lag, feature_voxel_size = key
        members = groups[key]
        metrics = {
            name: _mean_std([member["metrics"].get(name) for member in members])
            for name in metric_names
        }
        rows.append(
            {
                "category": category,
                "control": control,
                "alpha": alpha,
                "sample_lag": sample_lag,
                "feature_voxel_size": feature_voxel_size,
                "n_cases": len(members),
                "metrics": metrics,
            }
        )
    return rows


def build_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Anchor Markov Sensitivity Analysis",
        "",
        f"Date: {payload['date']}",
        "",
        "Scope: small diagnostic sensitivity run for the Paper-0 Markov layer. "
        "This is not a broad robustness claim.",
        "",
        "## Parameters",
        "",
        "```json",
        json.dumps(payload["parameters"], indent=2, sort_keys=True),
        "```",
        "",
        "## Aggregate Table",
        "",
        "| category | control | alpha | sample_lag | feature_voxel_size | n | slow_abs | rate | gap | n_states | empty_rows | residence_mean | ac_lag1 |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["aggregates"]:
        metrics = row["metrics"]
        lines.append(
            "| {category} | {control} | {alpha:.4g} | {sample_lag} | "
            "{feature_voxel_size:.4g} | {n_cases} | {slow} | {rate} | {gap} | "
            "{states} | {empty} | {residence} | {ac} |".format(
                category=row["category"],
                control=row["control"],
                alpha=row["alpha"],
                sample_lag=row["sample_lag"],
                feature_voxel_size=row["feature_voxel_size"],
                n_cases=row["n_cases"],
                slow=_fmt(metrics["leading_nontrivial_abs"]["mean"]),
                rate=_fmt(metrics["leading_relaxation_rate"]["mean"]),
                gap=_fmt(metrics["spectral_gap"]["mean"]),
                states=_fmt(metrics["n_states"]["mean"]),
                empty=_fmt(metrics["empty_rows"]["mean"]),
                residence=_fmt(metrics["residence_mean"]["mean"]),
                ac=_fmt(metrics["autocorrelation_lag1"]["mean"]),
            )
        )

    lines.extend(
        [
            "",
            "## Reading Notes",
            "",
            "- `sample_lag` is a lag in stored samples, not physical time.",
            "- `lag_updates` is recorded per raw case in the JSON output.",
            "- `shuffled_memory_features` keeps visible samples but permutes memory-summary columns; it is a feature-control, not a new dynamics run.",
            "- `eta_zero` is a dynamics control with the memory-gradient coupling removed.",
            "- Voxel results are baseline diagnostics; they are not a final PCCA or HMM decomposition.",
            "",
            "## Git",
            "",
            f"- revision: `{payload['git']['revision']}`",
            "- status at run:",
            "",
            "```text",
            payload["git"]["status"] or "clean",
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    specs = _case_specs(args)
    cases: list[dict[str, Any]] = []
    needs_eta_zero = "eta_zero" in args.controls

    for alpha in args.alpha:
        for seed in args.seeds:
            baseline = simulate_augmented_features(_config(args, alpha=alpha), seed=seed)
            eta_zero = (
                simulate_augmented_features(_config(args, alpha=alpha, eta=0.0), seed=seed)
                if needs_eta_zero
                else None
            )
            for spec in specs:
                cases.append(
                    run_case(
                        args,
                        alpha=alpha,
                        seed=seed,
                        spec=spec,
                        baseline=baseline,
                        eta_zero=eta_zero,
                    )
                )

    payload: dict[str, Any] = {
        "date": "2026-06-29",
        "description": "Small sensitivity analysis for the Paper-0 Markov layer.",
        "git": {
            "revision": _git_output(["rev-parse", "HEAD"]),
            "status": _git_output(["status", "--short"]),
        },
        "parameters": {
            "steps": args.steps,
            "burn_in": args.burn_in,
            "sample_every": args.sample_every,
            "dim": args.dim,
            "seeds": args.seeds,
            "alpha": args.alpha,
            "epsilon": args.epsilon,
            "eta": args.eta,
            "sigma_rep": args.sigma_rep,
            "sigma_att": args.sigma_att,
            "amplitude_rep": args.amplitude_rep,
            "amplitude_att": args.amplitude_att,
            "max_memory": args.max_memory,
            "memory_factor": args.memory_factor,
            "voxel_size": args.voxel_size,
            "feature_voxel_size": args.feature_voxel_size,
            "lag": args.lag,
            "base_lag": args.base_lag,
            "base_feature_voxel_size": args.base_feature_voxel_size,
            "controls": args.controls,
        },
        "aggregates": aggregate_cases(cases),
        "cases": cases,
    }

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )

    report_path = Path(args.report)
    if not report_path.is_absolute():
        report_path = ROOT / report_path
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_report(payload), encoding="utf-8")

    print(f"Wrote sensitivity JSON to {output_path}")
    print(f"Wrote sensitivity report to {report_path}")


if __name__ == "__main__":
    main()
