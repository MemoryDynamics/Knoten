#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import concurrent.futures
import os

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (
    SimulationConfig,
    bootstrap_mean_ci,
    covariance_dimension,
    occupancy_dimension,
    simulate_finite_memory,
    simulate_finite_memory_numba,
    spectral_dimension,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Alpha sweep and plateau plot for D_cov, D_occ, and D_spec."
    )
    parser.add_argument(
        "--alpha-values",
        type=str,
        default="0.001,0.0015,0.002,0.0025,0.003,0.004,0.005,0.007,0.01,0.015,0.02",
        help="Comma-separated alpha values to sweep.",
    )
    parser.add_argument(
        "--alpha-log", action="store_true", help="Plot alpha on a logarithmic x-axis"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["alpha", "D_vs_N"],
        default="alpha",
        help="Run mode: alpha sweep or D_vs_N time stability",
    )
    parser.add_argument(
        "--n-seeds",
        type=int,
        default=3,
        help="Number of seeds per alpha (reduce seed count for longer N)",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=100000,
        help="Number of update steps (increase for stronger temporal stability)",
    )
    parser.add_argument(
        "--sample-every", type=int, default=200, help="Sampling interval"
    )
    parser.add_argument(
        "--n-checkpoints",
        type=int,
        default=30,
        help="Number of log-spaced checkpoints for D_vs_N mode",
    )
    parser.add_argument(
        "--use-numba",
        action="store_true",
        help="Use the numba-accelerated finite-memory simulator",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default="alpha_plateau_data.json",
        help="Save sweep data to JSON",
    )
    parser.add_argument(
        "--output-plot",
        type=str,
        default="alpha_plateau_plot.png",
        help="Save plot image",
    )
    parser.add_argument(
        "--show", action="store_true", help="Show the plot interactively"
    )
    return parser.parse_args()


def run_seed(cfg: SimulationConfig, seed: int, simulate_fn) -> dict[str, float]:
    result = simulate_fn(cfg, seed=seed)
    samples = result["samples"]
    return {
        "seed": seed,
        "D_cov": float(covariance_dimension(samples)),
        "D_occ": float(occupancy_dimension(samples, n_scales=10, min_count=2)),
        "D_spec": float(spectral_dimension(samples)),
        "n_samples": int(len(samples)),
    }


def summarize(values: list[float]) -> dict[str, float]:
    mean, lo, hi = bootstrap_mean_ci(values, level=0.95, n_boot=1000, seed=0)
    std = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
    return {
        "mean": float(mean),
        "std": std,
        "ci_95_lo": float(lo),
        "ci_95_hi": float(hi),
    }


def _log_spaced_indices(n: int, n_points: int) -> np.ndarray:
    if n <= 1 or n_points <= 0:
        return np.array([], dtype=int)
    num = min(n_points, n - 1)
    indices = np.unique(np.geomspace(2, n, num=num, dtype=int) - 1)
    if indices.size == 0 or indices[-1] != n - 1:
        indices = np.append(indices, n - 1)
    return indices


def run_stability_curve(
    cfg: SimulationConfig, seed: int, n_checkpoints: int, simulate_fn
) -> dict[str, object]:
    result = simulate_fn(cfg, seed=seed)
    samples = result["samples"]
    sample_steps = result["sample_steps"].tolist()
    n_samples = len(samples)
    indices = _log_spaced_indices(n_samples, n_checkpoints)

    d_cov_series = []
    d_occ_series = []
    d_spec_series = []
    selected_steps = []

    for idx in indices:
        prefix = samples[: idx + 1]
        selected_steps.append(sample_steps[idx])
        d_cov_series.append(float(covariance_dimension(prefix)))
        d_occ_series.append(
            float(occupancy_dimension(prefix, n_scales=10, min_count=2))
        )
        d_spec_series.append(float(spectral_dimension(prefix)))

    return {
        "seed": seed,
        "sample_steps": selected_steps,
        "D_cov": d_cov_series,
        "D_occ": d_occ_series,
        "D_spec": d_spec_series,
        "n_samples": int(n_samples),
    }


def make_plot(
    alphas: list[float],
    summary: dict[str, dict[str, float]],
    output_path: Path,
    alpha_log: bool = False,
) -> None:
    fig, ax1 = plt.subplots(figsize=(9, 6))

    cov_means = [summary[a]["D_cov_stats"]["mean"] for a in alphas]
    cov_stds = [summary[a]["D_cov_stats"]["std"] for a in alphas]
    occ_means = [summary[a]["D_occ_stats"]["mean"] for a in alphas]
    occ_stds = [summary[a]["D_occ_stats"]["std"] for a in alphas]

    ax1.errorbar(
        alphas,
        cov_means,
        yerr=cov_stds,
        marker="o",
        capsize=4,
        label="D_cov",
        color="#1f77b4",
    )
    ax1.set_xlabel("alpha")
    ax1.set_ylabel("D_cov", color="#1f77b4")
    ax1.tick_params(axis="y", labelcolor="#1f77b4")
    ax1.axhline(3.0, color="#1f77b4", linestyle="--", alpha=0.5)
    ax1.set_title("Alpha sweep plateau with seed error bars")
    ax1.set_xlim(min(alphas) * 0.95, max(alphas) * 1.05)

    ax2 = ax1.twinx()
    ax2.errorbar(
        alphas,
        occ_means,
        yerr=occ_stds,
        marker="s",
        capsize=4,
        label="D_occ",
        color="#ff7f0e",
    )
    ax2.set_ylabel("D_occ", color="#ff7f0e")
    ax2.tick_params(axis="y", labelcolor="#ff7f0e")

    if alpha_log:
        ax1.set_xscale("log")
        ax1.grid(which="both", axis="x", linestyle=":", alpha=0.4)

    fig.tight_layout()
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    fig.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper right")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def make_plot_d_vs_n(
    alpha_values: list[float],
    curve_data: dict[float, dict[str, object]],
    output_path: Path,
    alpha_log: bool = False,
) -> None:
    fig, axs = plt.subplots(3, 1, figsize=(10, 14), sharex=True)
    metrics = [
        ("D_cov", "D_cov", "blue", 3.0),
        ("D_occ", "D_occ", "orange", None),
        ("D_spec", "D_spec", "green", None),
    ]

    for alpha in alpha_values:
        data = curve_data[alpha]
        steps = np.asarray(data["sample_steps"], dtype=float)
        for idx, (key, label, color, ref) in enumerate(metrics):
            mean = np.asarray(data[f"{key}_mean"], dtype=float)
            std = np.asarray(data[f"{key}_std"], dtype=float)
            axs[idx].plot(
                steps,
                mean,
                marker="o",
                markersize=3,
                color=color,
                label=f"alpha={alpha}",
            )
            axs[idx].fill_between(steps, mean - std, mean + std, color=color, alpha=0.2)
            if ref is not None:
                axs[idx].axhline(ref, color="gray", linestyle="--", alpha=0.7)

    for idx, (key, label, color, ref) in enumerate(metrics):
        axs[idx].set_ylabel(label)
        axs[idx].grid(True, which="both", linestyle=":", alpha=0.4)
        axs[idx].legend()

    if alpha_log:
        for ax in axs:
            ax.set_xscale("log")
    axs[-1].set_xlabel("N (sampled steps)")
    fig.suptitle("D metrics vs N for selected alpha values", y=0.97)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    alpha_values = [float(v.strip()) for v in args.alpha_values.split(",") if v.strip()]
    alpha_values = sorted(alpha_values)

    summary: dict[str, dict[str, float]] = {}
    sweep_data: list[dict] = []
    curve_data: dict[float, dict[str, object]] = {}

    for alpha in alpha_values:
        cfg = SimulationConfig(
            steps=args.steps,
            dim=7,
            epsilon=0.03,
            eta=0.15,
            alpha=alpha,
            sigma_rep=1.0,
            sigma_att=3.0,
            amplitude_rep=1.0,
            amplitude_att=0.35,
            memory_factor=6.0,
            max_memory=3000,
            burn_in=0,
            sample_every=args.sample_every,
        )
        print(f"Running alpha={alpha} with {args.n_seeds} seeds...")
        start = time.perf_counter()

        simulate_fn = (
            simulate_finite_memory_numba if args.use_numba else simulate_finite_memory
        )
        max_workers = min(args.n_seeds, (os.cpu_count() or 1))
        if args.mode == "alpha":
            seeds = list(range(1, args.n_seeds + 1))
            runs: list[dict[str, object]] = []
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as ex:
                futures = [
                    ex.submit(run_seed, cfg, seed, simulate_fn) for seed in seeds
                ]
                for f in concurrent.futures.as_completed(futures):
                    runs.append(f.result())

            elapsed = time.perf_counter() - start
            d_cov_values = [run["D_cov"] for run in runs if not np.isnan(run["D_cov"])]
            d_occ_values = [run["D_occ"] for run in runs if not np.isnan(run["D_occ"])]
            d_spec_values = [
                run["D_spec"] for run in runs if not np.isnan(run["D_spec"])
            ]

            stats = {
                "D_cov_stats": summarize(d_cov_values),
                "D_occ_stats": summarize(d_occ_values),
                "D_spec_stats": summarize(d_spec_values),
                "runs": runs,
                "elapsed_seconds": float(elapsed),
            }
            summary[alpha] = stats
            sweep_data.append({"alpha": alpha, **stats})

        else:
            seeds = list(range(1, args.n_seeds + 1))
            curves: list[dict[str, object]] = []
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as ex:
                futures = [
                    ex.submit(
                        run_stability_curve, cfg, seed, args.n_checkpoints, simulate_fn
                    )
                    for seed in seeds
                ]
                for f in concurrent.futures.as_completed(futures):
                    curves.append(f.result())
            elapsed = time.perf_counter() - start

            lengths = [len(curve["D_cov"]) for curve in curves]
            min_len = min(lengths)
            if min_len == 0:
                continue

            common_steps = curves[0]["sample_steps"][:min_len]
            d_cov_arrays = np.vstack(
                [np.asarray(curve["D_cov"][:min_len], dtype=float) for curve in curves]
            )
            d_occ_arrays = np.vstack(
                [np.asarray(curve["D_occ"][:min_len], dtype=float) for curve in curves]
            )
            d_spec_arrays = np.vstack(
                [np.asarray(curve["D_spec"][:min_len], dtype=float) for curve in curves]
            )

            d_cov_mean = np.full(d_cov_arrays.shape[1], np.nan, dtype=float)
            d_cov_std = np.full(d_cov_arrays.shape[1], 0.0, dtype=float)
            d_occ_mean = np.full(d_cov_arrays.shape[1], np.nan, dtype=float)
            d_occ_std = np.full(d_cov_arrays.shape[1], 0.0, dtype=float)
            d_spec_mean = np.full(d_cov_arrays.shape[1], np.nan, dtype=float)
            d_spec_std = np.full(d_cov_arrays.shape[1], 0.0, dtype=float)

            for idx in range(d_cov_arrays.shape[1]):
                valid = np.isfinite(d_cov_arrays[:, idx])
                if np.count_nonzero(valid) > 0:
                    d_cov_mean[idx] = float(np.nanmean(d_cov_arrays[valid, idx]))
                if np.count_nonzero(valid) > 1:
                    d_cov_std[idx] = float(np.nanstd(d_cov_arrays[valid, idx], ddof=1))

                valid_occ = np.isfinite(d_occ_arrays[:, idx])
                if np.count_nonzero(valid_occ) > 0:
                    d_occ_mean[idx] = float(np.nanmean(d_occ_arrays[valid_occ, idx]))
                if np.count_nonzero(valid_occ) > 1:
                    d_occ_std[idx] = float(
                        np.nanstd(d_occ_arrays[valid_occ, idx], ddof=1)
                    )

                valid_spec = np.isfinite(d_spec_arrays[:, idx])
                if np.count_nonzero(valid_spec) > 0:
                    d_spec_mean[idx] = float(np.nanmean(d_spec_arrays[valid_spec, idx]))
                if np.count_nonzero(valid_spec) > 1:
                    d_spec_std[idx] = float(
                        np.nanstd(d_spec_arrays[valid_spec, idx], ddof=1)
                    )

            curve_data[alpha] = {
                "sample_steps": common_steps,
                "D_cov_mean": d_cov_mean.tolist(),
                "D_cov_std": d_cov_std.tolist(),
                "D_occ_mean": d_occ_mean.tolist(),
                "D_occ_std": d_occ_std.tolist(),
                "D_spec_mean": d_spec_mean.tolist(),
                "D_spec_std": d_spec_std.tolist(),
                "runs": curves,
                "elapsed_seconds": float(elapsed),
            }
            sweep_data.append({"alpha": alpha, **curve_data[alpha]})

    output_json = ROOT / args.output_json
    if args.mode == "alpha":
        output_json.write_text(
            json.dumps({"summary": summary, "sweep_data": sweep_data}, indent=2)
        )
        print(f"Wrote sweep data to {output_json}")

        plot_path = ROOT / args.output_plot
        make_plot(alpha_values, summary, plot_path, alpha_log=args.alpha_log)
        print(f"Wrote plot to {plot_path}")
    else:
        output_json.write_text(
            json.dumps({"curve_data": curve_data, "sweep_data": sweep_data}, indent=2)
        )
        print(f"Wrote D_vs_N data to {output_json}")

        plot_path = ROOT / args.output_plot
        make_plot_d_vs_n(alpha_values, curve_data, plot_path, alpha_log=args.alpha_log)
        print(f"Wrote D_vs_N plot to {plot_path}")
    if args.show:
        import matplotlib.pyplot as plt

        img = plt.imread(plot_path)
        plt.imshow(img)
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    main()
