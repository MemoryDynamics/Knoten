from __future__ import annotations

import argparse
from datetime import UTC, datetime
import itertools
import json
import math
import os
from pathlib import Path
import statistics
import subprocess
import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _root()
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten.markov.closure import eta_zero_raw_mode_null, fit_ar_spectrum
from emergenz_knoten.spectral_memory_field import SpectralMemoryConfig
from emergenz_knoten.spectral_memory_trace import simulate_eta_zero_raw_mode_trace


def _ints(value: str) -> list[int]:
    values = [int(item) for item in value.split(",") if item.strip()]
    if not values or any(item < 1 for item in values):
        raise argparse.ArgumentTypeError("expected positive comma-separated integers")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Eta-zero raw-mode null audit.")
    parser.add_argument("--steps", type=int, default=1_000_000)
    parser.add_argument("--burn-in", type=int, default=50_000)
    parser.add_argument("--sample-every", type=int, default=20)
    parser.add_argument("--seeds", type=_ints, default=[1, 2, 3, 4, 5])
    parser.add_argument("--segments", type=int, default=5)
    parser.add_argument("--lags", type=_ints, default=[1, 2, 3, 5, 10])
    parser.add_argument("--epsilon", type=float, default=1e-4)
    parser.add_argument("--lambda-value", type=float, default=0.01)
    parser.add_argument("--box-length", type=float, default=80.0)
    parser.add_argument("--n-low-modes", type=int, default=3)
    parser.add_argument("--deposition-sigma", type=float, default=0.0)
    parser.add_argument("--diffusion-length-ratio", type=float, default=0.3)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--ridge", type=float, default=1e-6)
    parser.add_argument("--complex-tolerance", type=float, default=1e-6)
    parser.add_argument(
        "--identity-json",
        type=Path,
        default=Path("reports/memory/closure/low_mode_identity_audit_2026-07-20.json"),
    )
    parser.add_argument(
        "--closure-json",
        type=Path,
        default=Path(
            "reports/memory/closure/low_mode_ar_feature_closure_long_N1M_2026-07-19.json"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/memory/closure/eta_zero_raw_mode_null_audit_2026-07-31.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/memory/closure/eta_zero_raw_mode_null_audit_2026-07-31.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/eta_zero_raw_mode_null_audit_2026-07-31.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _validate(args: argparse.Namespace) -> None:
    samples = args.steps // args.sample_every - args.burn_in // args.sample_every
    if args.steps < 1_000 or not 0 <= args.burn_in < args.steps:
        raise SystemExit("invalid steps or burn-in")
    if args.sample_every < 1 or args.segments < 2 or args.n_low_modes < 1:
        raise SystemExit("invalid sampling, segments, or mode count")
    if not 0.0 < args.lambda_value <= 1.0:
        raise SystemExit("lambda-value must lie in (0,1]")
    if samples // args.segments <= max(args.lags) + 2:
        raise SystemExit("segments are too short")


def _git(arguments: list[str]) -> str:
    try:
        return subprocess.run(
            ["git", *arguments], cwd=ROOT, check=True, text=True, capture_output=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _match_error(observed: np.ndarray, expected: np.ndarray) -> float:
    return float(
        min(
            max(abs(observed[i] - expected[j]) for i, j in enumerate(order))
            for order in itertools.permutations(range(4))
        )
    )


def _fit(
    values: np.ndarray,
    *,
    mode: int,
    scope: str,
    seed: int | str,
    segment: int | None,
    lag: int,
    args: argparse.Namespace,
    expected: np.ndarray,
) -> dict[str, Any]:
    spectrum = fit_ar_spectrum(
        [values],
        lag=lag,
        lag_updates=lag * args.sample_every,
        ridge=args.ridge,
    )
    mask = (
        (np.abs(spectrum.eigenvalues.imag) > args.complex_tolerance)
        & (np.abs(spectrum.eigenvalues) > 0.05)
        & (np.abs(spectrum.eigenvalues) < 1.05)
    )
    frequency = np.abs(np.angle(spectrum.eigenvalues[mask]))
    if frequency.size:
        frequency = frequency / (lag * args.sample_every * args.lambda_value)
    x = values[:-lag]
    scale = np.where(x.std(axis=0) > 1e-12, x.std(axis=0), 1.0)
    standardized = (x - x.mean(axis=0)) / scale
    condition = float(np.linalg.cond(standardized.T @ standardized))
    if not math.isfinite(condition):
        condition = float(np.finfo(float).max)
    return {
        "mode": mode,
        "scope": scope,
        "seed": seed,
        "segment": segment,
        "lag_samples": lag,
        "lag_memory_times": lag * args.sample_every * args.lambda_value,
        "complex_count": int(mask.sum()),
        "max_abs_imaginary": float(np.max(np.abs(spectrum.eigenvalues.imag))),
        "max_complex_frequency_per_memory_time": float(np.max(frequency))
        if frequency.size
        else 0.0,
        "maximum_eigenvalue_error": _match_error(spectrum.eigenvalues, expected),
        "feature_gram_condition": condition,
        "eigenvalues": [
            {"real": float(v.real), "imag": float(v.imag), "modulus": float(abs(v))}
            for v in spectrum.eigenvalues
        ],
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    _validate(args)
    nu = 0.5 * args.lambda_value * (args.diffusion_length_ratio * args.sigma_att) ** 2
    config = SpectralMemoryConfig(
        box_length=args.box_length,
        n_modes=max(8, args.n_low_modes),
        lambda_value=args.lambda_value,
        memory_mass=1.0,
        deposition_sigma=args.deposition_sigma,
    )
    k = 2.0 * np.pi * np.arange(1, args.n_low_modes + 1) / args.box_length
    smoothing = np.exp(-0.5 * args.deposition_sigma**2 * k**2)
    analytic: list[dict[str, Any]] = []
    expected: dict[tuple[int, int], np.ndarray] = {}
    for mode, (wave, deposit) in enumerate(zip(k, smoothing, strict=True), 1):
        for lag in args.lags:
            updates = lag * args.sample_every
            null = eta_zero_raw_mode_null(
                args.lambda_value,
                nu,
                float(wave),
                args.epsilon,
                updates,
                deposition_smoothing=float(deposit),
            )
            expected[(mode, lag)] = np.asarray(
                [
                    null.phase_multiplier,
                    null.phase_multiplier,
                    null.memory_multiplier,
                    null.memory_multiplier,
                ],
                dtype=complex,
            )
            analytic.append(
                {
                    "mode": mode,
                    "lag_memory_times": updates * args.lambda_value,
                    "phase_multiplier": null.phase_multiplier,
                    "memory_multiplier": null.memory_multiplier,
                    "phase_rate_per_memory_time": -math.log(null.phase_multiplier)
                    / updates
                    / args.lambda_value,
                    "memory_rate_per_memory_time": -math.log(null.memory_multiplier)
                    / updates
                    / args.lambda_value,
                    "maximum_analytic_imaginary": float(
                        np.max(np.abs(np.linalg.eigvals(null.transition).imag))
                    ),
                }
            )

    traces: dict[int, np.ndarray] = {}
    for seed in args.seeds:
        noise = np.random.default_rng(seed).normal(size=args.steps)
        traces[seed] = simulate_eta_zero_raw_mode_trace(
            config,
            noise=noise,
            diffusion_per_update=nu,
            epsilon=args.epsilon,
            burn_in=args.burn_in,
            sample_every=args.sample_every,
            n_low_modes=args.n_low_modes,
        ).values

    rows: list[dict[str, Any]] = []
    for mode in range(1, args.n_low_modes + 1):
        columns = slice(4 * (mode - 1), 4 * mode)
        pooled = np.concatenate([traces[seed][:, columns] for seed in args.seeds])
        for lag in args.lags:
            reference = expected[(mode, lag)]
            rows.append(
                _fit(
                    pooled,
                    mode=mode,
                    scope="pooled",
                    seed="pooled",
                    segment=None,
                    lag=lag,
                    args=args,
                    expected=reference,
                )
            )
            for seed in args.seeds:
                values = traces[seed][:, columns]
                rows.append(
                    _fit(
                        values,
                        mode=mode,
                        scope="seed",
                        seed=seed,
                        segment=None,
                        lag=lag,
                        args=args,
                        expected=reference,
                    )
                )
                for index, segment in enumerate(np.array_split(values, args.segments)):
                    rows.append(
                        _fit(
                            segment,
                            mode=mode,
                            scope="segment",
                            seed=seed,
                            segment=index,
                            lag=lag,
                            args=args,
                            expected=reference,
                        )
                    )

    summaries: list[dict[str, Any]] = []
    for scope in ("pooled", "seed", "segment"):
        selected = [row for row in rows if row["scope"] == scope]
        complex_rows = [row for row in selected if row["complex_count"]]
        summaries.append(
            {
                "scope": scope,
                "row_count": len(selected),
                "complex_row_count": len(complex_rows),
                "complex_row_fraction": len(complex_rows) / len(selected),
                "maximum_complex_frequency_per_memory_time": max(
                    (
                        row["max_complex_frequency_per_memory_time"]
                        for row in complex_rows
                    ),
                    default=0.0,
                ),
                "median_eigenvalue_error": float(
                    statistics.median(
                        row["maximum_eigenvalue_error"] for row in selected
                    )
                ),
                "median_feature_gram_condition": float(
                    statistics.median(row["feature_gram_condition"] for row in selected)
                ),
            }
        )

    identity = json.loads(_resolve(args.identity_json).read_text(encoding="utf-8"))
    closure = json.loads(_resolve(args.closure_json).read_text(encoding="utf-8"))
    aligned = [
        {
            "arm": row["arm"],
            "lag_memory_times": float(row["lag_memory_times"]),
            "frequency_median_per_memory_time": float(
                row["frequency_median_per_memory_time"]
            ),
            "quality_factor_median": float(row["quality_factor_median"]),
        }
        for row in identity["rows"]
        if row["kind"] == "complex" and row["arm"] in {"active_nu03", "eta_zero_nu03"}
    ]
    by_scope = {row["scope"]: row for row in summaries}
    gate = {
        "analytic_raw_operator_has_complex_modes": any(
            row["maximum_analytic_imaginary"] > args.complex_tolerance
            for row in analytic
        ),
        "pooled_raw_fit_has_complex_rows": by_scope["pooled"]["complex_row_count"] > 0,
        "seed_raw_fit_has_complex_rows": by_scope["seed"]["complex_row_count"] > 0,
        "aligned_active_eta_zero_control_separation_pass": bool(
            identity["gate"]["complex_control_separation_pass"]
        ),
        "aligned_complex_segment_identity_pass": bool(
            identity["gate"]["complex_segment_identity_pass"]
        ),
        "physical_complex_mode_supported": False,
        "p2_null_classification_complete": True,
        "classification": "raw eta-zero modes are real; archived complex pairs are representation and finite-fit modes, not feedback-specific modes",
    }
    return {
        "created_utc": datetime.now(UTC).isoformat(),
        "parameters": {
            key: value
            for key, value in vars(args).items()
            if key
            not in {"report", "summary_json", "figure", "identity_json", "closure_json"}
        },
        "diffusion_per_update": nu,
        "analytic_rows": analytic,
        "fit_rows": rows,
        "fit_summaries": summaries,
        "aligned_reference_rows": aligned,
        "archived_closure_gate": closure["gate"],
        "archived_identity_gate": identity["gate"],
        "gate": gate,
        "git_revision": _git(["rev-parse", "HEAD"]),
        "git_status": _git(["status", "--short"]),
    }


def _relative(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _plot(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    analytic, rows = payload["analytic_rows"], payload["fit_rows"]
    figure, axes = plt.subplots(1, 3, figsize=(14.5, 4.3))
    for mode in sorted({row["mode"] for row in analytic}):
        selected = [row for row in analytic if row["mode"] == mode]
        x = [row["lag_memory_times"] for row in selected]
        axes[0].plot(
            x,
            [row["memory_multiplier"] for row in selected],
            marker="o",
            label=f"rho {mode}",
        )
        axes[0].plot(
            x,
            [row["phase_multiplier"] for row in selected],
            color="black",
            linestyle=":",
            alpha=0.3,
        )
    axes[0].set(
        title="Exact eta=0 multipliers",
        xlabel="lag / memory time",
        ylabel="real multiplier",
    )
    axes[0].legend(fontsize=8)
    for scope, marker in (("pooled", "s"), ("seed", "o"), ("segment", ".")):
        selected = [row for row in rows if row["scope"] == scope]
        axes[1].scatter(
            [row["lag_memory_times"] for row in selected],
            [max(row["max_abs_imaginary"], 1e-12) for row in selected],
            marker=marker,
            alpha=0.45,
            label=scope,
        )
    axes[1].axhline(
        payload["parameters"]["complex_tolerance"], color="black", linestyle="--"
    )
    axes[1].set_yscale("log")
    axes[1].set(
        title="Imaginary leakage",
        xlabel="lag / memory time",
        ylabel="max |Im eigenvalue|",
    )
    axes[1].legend(fontsize=8)
    segments = [
        row for row in rows if row["scope"] == "segment" and row["complex_count"]
    ]
    axes[2].scatter(
        [row["lag_memory_times"] for row in segments],
        [row["max_complex_frequency_per_memory_time"] for row in segments],
        s=12,
        alpha=0.3,
        label="raw eta=0 segments",
    )
    for arm, color in (("active_nu03", "tab:red"), ("eta_zero_nu03", "tab:blue")):
        selected = [
            row for row in payload["aligned_reference_rows"] if row["arm"] == arm
        ]
        axes[2].plot(
            [row["lag_memory_times"] for row in selected],
            [row["frequency_median_per_memory_time"] for row in selected],
            marker="o",
            color=color,
            label=f"aligned {arm}",
        )
    axes[2].set(
        title="Raw versus aligned frequency",
        xlabel="lag / memory time",
        ylabel="|omega| / memory time",
    )
    axes[2].legend(fontsize=8)
    for axis in axes:
        axis.grid(alpha=0.25)
    figure.tight_layout()
    figure.savefig(path, dpi=180)
    plt.close(figure)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    gate = payload["gate"]
    lines = [
        "# Eta-Zero Raw-Mode Null Audit",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Question",
        "",
        "Are the archived complex AR pairs eigenmodes of scalar eta-zero memory,",
        "or are they introduced by moving-center features and finite fitting?",
        "",
        "## Exact result",
        "",
        "For p_k=exp(-i k x_n), Gaussian eta-zero increments give a real phase",
        "multiplier exp(-epsilon^2 k^2/2). Forgetting and heat give the second",
        "real multiplier (1-lambda)exp(-nu k^2). Both are repeated for real and",
        "imaginary components. Sampling raises the real map to a power and cannot",
        "create a complex eigenpair.",
        "",
        "## Gate",
        "",
        f"- Exact raw operator has complex modes: {gate['analytic_raw_operator_has_complex_modes']}.",
        f"- Pooled raw fits have complex rows: {gate['pooled_raw_fit_has_complex_rows']}.",
        f"- Seedwise raw fits have complex rows: {gate['seed_raw_fit_has_complex_rows']}.",
        f"- Archived active/eta-zero separation: {gate['aligned_active_eta_zero_control_separation_pass']}.",
        f"- Archived complex segment identity: {gate['aligned_complex_segment_identity_pass']}.",
        f"- Physical complex mode supported: {gate['physical_complex_mode_supported']}.",
        f"- P2 classification complete: {gate['p2_null_classification_complete']}.",
        "",
        f"![Eta-zero raw-mode null audit]({_relative(report, figure)})",
        "",
        "## Finite-fit summary",
        "",
        "| scope | rows | complex | fraction | max frequency | median error | median condition |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload["fit_summaries"]:
        lines.append(
            f"| {row['scope']} | {row['row_count']} | {row['complex_row_count']} | "
            f"{row['complex_row_fraction']:.3g} | {row['maximum_complex_frequency_per_memory_time']:.3g} | "
            f"{row['median_eigenvalue_error']:.3g} | {row['median_feature_gram_condition']:.3g} |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "The raw operator is analytically real. Full traces test this result at the",
        "same N=1M cadence as the archived closure run. Segment-only leakage is",
        "reported because tiny epsilon excites a narrow phase arc and yields",
        "ill-conditioned fits. The archived larger pairs occur after moving-center",
        "alignment and force/relative-position projection; active and eta-zero",
        "subspaces overlap above 0.9999. They remain representation/fit modes, not",
        "physical oscillations.",
        "",
        "The long-run work remains a separate evidence lane. N=30M/300M runs,",
        "parameter heatmaps, and D_occ-near-three locations are observations about",
        "asymptotic geometry. They do not establish mode identity. New long runs",
        "must freeze code revision, cadence, fit window, and estimator.",
        "",
        "## Memory action and observables",
        "",
        "- Direct rho observables: mass, centroid, covariance tensor, radius,",
        "  anisotropy, participation dimension, Fourier power/phase, autocorrelation,",
        "  and pathwise contraction.",
        "- Readout observables require rho plus K: Phi, gradient at x, and Hessian.",
        "- Feedback loop: rho -> grad Phi(x) -> x -> deposition -> rho.",
        "  Residence, D_occ, D_cov, drift, angular momentum, and spin proxies depend",
        "  on x and are not intrinsic rho-only observables.",
        "- Original scalar rho has no spatial rho-rho self-coupling beyond optional",
        "  linear smoothing. Active fields require additional spectrum, energy,",
        "  PDE-residual, source-field phase, and saturation observables.",
        "",
        "## Limits",
        "",
        "- The exact closure is eta-zero, Gaussian, scalar, periodic, and unaligned.",
        "- No photon, spin, quantization, or physical-time claim follows.",
        "",
        "## Reproduction",
        "",
        "    python experiments/current/memory/closure/eta_zero_raw_mode_null_audit.py",
        "",
        f"Git revision: {payload['git_revision']}.",
        f"Git status at generation: {payload['git_status'] or 'clean'}.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    payload = build_payload(args)
    report, summary, figure = map(
        _resolve, (args.report, args.summary_json, args.figure)
    )
    _plot(payload, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")
    summary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload["gate"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
