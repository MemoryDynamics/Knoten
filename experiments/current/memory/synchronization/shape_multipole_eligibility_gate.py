"""P3.2d autonomous shape-multipole source-eligibility gate."""

from __future__ import annotations

import argparse
from dataclasses import asdict, replace
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
import time
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch

from emergenz_knoten import autonomous_knot_trace, load_finite_memory_checkpoint


ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CHECKPOINT = Path(
    "data/processed/reference_states/"
    "scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/"
    "scalar_Aatt35_d3_seed1_N100000000.npz"
)
CONDITIONS = ("baseline", "eta_zero")
SOURCES = ("shape", "shape_rate")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--future-seeds", default="1,2,3,4,5")
    parser.add_argument("--updates", type=int, default=150_000)
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--burn-memory-times", type=float, default=100.0)
    parser.add_argument("--segments", type=int, default=4)
    parser.add_argument("--frequency-min", type=float, default=0.05)
    parser.add_argument("--frequency-max", type=float, default=2.0)
    parser.add_argument("--peak-ratio-min", type=float, default=5.0)
    parser.add_argument("--peak-fraction-min", type=float, default=0.10)
    parser.add_argument("--segment-fraction-min", type=float, default=0.05)
    parser.add_argument("--frequency-relative-range-max", type=float, default=0.25)
    parser.add_argument("--min-segment-passes", type=int, default=3)
    parser.add_argument("--min-baseline-seeds", type=int, default=4)
    parser.add_argument("--max-control-seeds", type=int, default=1)
    parser.add_argument("--shuffle-count", type=int, default=64)
    parser.add_argument("--shuffle-block-memory-times", type=float, default=1.0)
    parser.add_argument("--radius-q95-max", type=float, default=1.10)
    parser.add_argument("--radius-max", type=float, default=1.20)
    parser.add_argument("--noise-seed-offset", type=int, default=20_260_806)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/p32d_shape_multipole_gate_2026-08-06.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/p32d_shape_multipole_gate_2026-08-06.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path("figures/draft/response/p32d_shape_multipole_gate_2026-08-06.png"),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _git(*arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def normalized_traceless_shape_components(tensors: np.ndarray) -> np.ndarray:
    """Return scale-free traceless shape tensors flattened without axis choice."""

    values = np.asarray(tensors, dtype=float)
    if (
        values.ndim != 3
        or values.shape[1] != values.shape[2]
        or not np.isfinite(values).all()
    ):
        raise ValueError("tensors must be finite with shape (samples, dim, dim)")
    traces = np.trace(values, axis1=1, axis2=2)
    if np.any(traces <= 0.0):
        raise ValueError("shape traces must be positive")
    dim = values.shape[1]
    normalized = values / traces[:, None, None]
    traceless = normalized - np.eye(dim)[None, :, :] / dim
    return traceless.reshape(values.shape[0], dim * dim)


def _relative_range(values: list[float]) -> float:
    finite = np.asarray(values, dtype=float)
    if finite.size == 0 or not np.isfinite(finite).all():
        return float("inf")
    median = float(np.median(finite))
    if median <= 0.0:
        return float("inf")
    return float((np.max(finite) - np.min(finite)) / median)


def _spectral_metrics(
    signal: np.ndarray,
    *,
    sample_interval: float,
    frequency_min: float,
    frequency_max: float,
) -> dict[str, Any]:
    values = np.asarray(signal, dtype=float)
    if values.ndim != 2 or values.shape[0] < 32 or not np.isfinite(values).all():
        raise ValueError("signal must be a finite samples-by-components array")
    centered = values - np.mean(values, axis=0, keepdims=True)
    nperseg = min(1024, values.shape[0])
    frequencies, component_psd = welch(
        centered,
        fs=1.0 / sample_interval,
        window="hann",
        nperseg=nperseg,
        noverlap=nperseg // 2,
        detrend="linear",
        scaling="density",
        axis=0,
    )
    total_psd = np.sum(component_psd, axis=1)
    band = (frequencies >= frequency_min) & (frequencies <= frequency_max)
    if np.count_nonzero(band) < 7:
        raise ValueError("frequency band contains fewer than seven Welch bins")
    band_indices = np.flatnonzero(band)
    peak_index = int(band_indices[np.argmax(total_psd[band])])
    resolution = float(frequencies[1] - frequencies[0])
    exclusion = max(2.0 * resolution, 0.1 * float(frequencies[peak_index]))
    background_mask = band & (
        np.abs(frequencies - frequencies[peak_index]) > exclusion
    )
    background = float(np.median(total_psd[background_mask]))
    peak = float(total_psd[peak_index])
    peak_ratio = float(peak / max(background, np.finfo(float).tiny))
    peak_band = band & (
        np.abs(frequencies - frequencies[peak_index])
        <= max(2.0 * resolution, 0.1 * float(frequencies[peak_index]))
    )
    band_power = float(np.sum(total_psd[band]))
    peak_fraction = float(np.sum(total_psd[peak_band]) / max(band_power, np.finfo(float).tiny))
    return {
        "peak_frequency_cycles_per_memory_time": float(frequencies[peak_index]),
        "peak_omega_per_memory_time": float(2.0 * np.pi * frequencies[peak_index]),
        "peak_to_background": peak_ratio,
        "peak_band_power_fraction": peak_fraction,
        "rms_frobenius": float(np.sqrt(np.mean(np.sum(centered * centered, axis=1)))),
        "frequencies": frequencies[band],
        "power_spectrum": total_psd[band],
    }


def _shuffle_null_q99(
    signal: np.ndarray,
    *,
    sample_interval: float,
    block_memory_times: float,
    count: int,
    seed: int,
    frequency_min: float,
    frequency_max: float,
) -> float:
    values = np.asarray(signal, dtype=float)
    block_size = max(1, int(round(block_memory_times / sample_interval)))
    block_count = values.shape[0] // block_size
    if block_count < 8:
        raise ValueError("shuffle null needs at least eight complete blocks")
    trimmed = values[: block_count * block_size]
    blocks = trimmed.reshape(block_count, block_size, values.shape[1])
    rng = np.random.default_rng(seed)
    maxima = []
    for _ in range(count):
        shuffled = blocks[rng.permutation(block_count)].reshape(
            block_count * block_size, values.shape[1]
        )
        maxima.append(
            _spectral_metrics(
                shuffled,
                sample_interval=sample_interval,
                frequency_min=frequency_min,
                frequency_max=frequency_max,
            )["peak_to_background"]
        )
    return float(np.quantile(maxima, 0.99))


def analyze_source(
    signal: np.ndarray,
    *,
    sample_interval: float,
    args: argparse.Namespace,
    null_seed: int,
) -> dict[str, Any]:
    full = _spectral_metrics(
        signal,
        sample_interval=sample_interval,
        frequency_min=args.frequency_min,
        frequency_max=args.frequency_max,
    )
    shuffle_q99 = _shuffle_null_q99(
        signal,
        sample_interval=sample_interval,
        block_memory_times=args.shuffle_block_memory_times,
        count=args.shuffle_count,
        seed=null_seed,
        frequency_min=args.frequency_min,
        frequency_max=args.frequency_max,
    )
    segments = []
    for segment_index, indices in enumerate(np.array_split(np.arange(signal.shape[0]), args.segments), 1):
        metrics = _spectral_metrics(
            signal[indices],
            sample_interval=sample_interval,
            frequency_min=args.frequency_min,
            frequency_max=args.frequency_max,
        )
        metrics["segment"] = segment_index
        metrics["segment_pass"] = bool(
            metrics["peak_to_background"] >= args.peak_ratio_min
            and metrics["peak_band_power_fraction"] >= args.segment_fraction_min
        )
        segments.append(metrics)
    passing_frequencies = [
        row["peak_frequency_cycles_per_memory_time"]
        for row in segments
        if row["segment_pass"]
    ]
    frequency_range = _relative_range(passing_frequencies)
    segment_count = sum(bool(row["segment_pass"]) for row in segments)
    candidate = bool(
        full["peak_to_background"] >= args.peak_ratio_min
        and full["peak_band_power_fraction"] >= args.peak_fraction_min
        and full["peak_to_background"] > shuffle_q99
        and segment_count >= args.min_segment_passes
        and frequency_range <= args.frequency_relative_range_max
    )
    return {
        "full": full,
        "shuffle_peak_ratio_q99": shuffle_q99,
        "segments": segments,
        "passing_segment_count": segment_count,
        "segment_frequency_relative_range": frequency_range,
        "candidate_pass": candidate,
    }


def _jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        number = float(value)
        return number if np.isfinite(number) else None
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def run_gate(args: argparse.Namespace) -> dict[str, Any]:
    if not args.allow_dirty and _git("status", "--porcelain"):
        raise SystemExit("working tree is dirty; commit first or pass --allow-dirty")
    checkpoint_path = _resolve(args.checkpoint)
    checkpoint = load_finite_memory_checkpoint(checkpoint_path)
    config = checkpoint.config
    if config.dim != 3:
        raise ValueError("the registered P3.2d gate requires the d=3 checkpoint")
    seeds = [int(value) for value in args.future_seeds.split(",")]
    if len(seeds) != len(set(seeds)) or len(seeds) < 2:
        raise ValueError("future seeds must be unique")
    if args.updates % args.sample_every != 0:
        raise ValueError("updates must be divisible by sample_every")
    sample_steps = np.arange(0, args.updates + 1, args.sample_every, dtype=int)
    sample_interval = config.alpha * args.sample_every
    burn_index = int(np.searchsorted(sample_steps * config.alpha, args.burn_memory_times))
    if sample_steps.size - burn_index < 128 * args.segments:
        raise ValueError("post-burn trace is too short for the registered segments")

    rows: list[dict[str, Any]] = []
    plot_traces: list[dict[str, Any]] = []
    started = time.perf_counter()
    for seed in seeds:
        noise = np.random.default_rng(args.noise_seed_offset + seed).standard_normal(
            (args.updates, config.dim)
        )
        condition_rows: dict[str, Any] = {}
        for condition_index, condition in enumerate(CONDITIONS):
            condition_config = config if condition == "baseline" else replace(config, eta=0.0)
            trace = autonomous_knot_trace(
                checkpoint.state,
                condition_config,
                noise=noise,
                sample_steps=sample_steps,
            )
            shape = normalized_traceless_shape_components(trace.shape_tensors)
            post_shape = shape[burn_index:]
            post_rate = np.diff(shape[burn_index - 1 :], axis=0) / sample_interval
            sources = {
                "shape": analyze_source(
                    post_shape,
                    sample_interval=sample_interval,
                    args=args,
                    null_seed=args.noise_seed_offset + 10_000 * seed + 100 * condition_index,
                ),
                "shape_rate": analyze_source(
                    post_rate,
                    sample_interval=sample_interval,
                    args=args,
                    null_seed=args.noise_seed_offset + 10_000 * seed + 100 * condition_index + 1,
                ),
            }
            condition_rows[condition] = {
                "radius_ratio_q95": float(np.quantile(trace.radius_ratios[burn_index:], 0.95)),
                "radius_ratio_max": float(np.max(trace.radius_ratios[burn_index:])),
                "shape_bounded_pass": bool(
                    np.quantile(trace.radius_ratios[burn_index:], 0.95) <= args.radius_q95_max
                    and np.max(trace.radius_ratios[burn_index:]) <= args.radius_max
                ),
                "sources": sources,
            }
            stride = max(1, post_shape.shape[0] // 1200)
            plot_traces.append(
                {
                    "seed": seed,
                    "condition": condition,
                    "times": sample_steps[burn_index::stride] * config.alpha,
                    "shape_norm": np.linalg.norm(post_shape[::stride], axis=1),
                }
            )
        rows.append({"future_seed": seed, "conditions": condition_rows})

    source_gates: dict[str, Any] = {}
    for source in SOURCES:
        baseline_rows = [row["conditions"]["baseline"]["sources"][source] for row in rows]
        control_rows = [row["conditions"]["eta_zero"]["sources"][source] for row in rows]
        baseline_candidates = [row for row in baseline_rows if row["candidate_pass"]]
        control_count = sum(bool(row["candidate_pass"]) for row in control_rows)
        frequencies = [
            row["full"]["peak_frequency_cycles_per_memory_time"]
            for row in baseline_candidates
        ]
        seed_frequency_range = _relative_range(frequencies)
        baseline_count = len(baseline_candidates)
        shape_count = sum(
            bool(row["conditions"]["baseline"]["shape_bounded_pass"])
            for row in rows
        )
        source_gates[source] = {
            "baseline_candidate_count": baseline_count,
            "eta_zero_candidate_count": control_count,
            "baseline_shape_bounded_count": shape_count,
            "baseline_frequency_relative_range": seed_frequency_range,
            "candidate_pass": bool(
                baseline_count >= args.min_baseline_seeds
                and control_count <= args.max_control_seeds
                and shape_count == len(seeds)
                and seed_frequency_range <= args.frequency_relative_range_max
            ),
        }
    any_pass = any(source_gates[source]["candidate_pass"] for source in SOURCES)
    payload = {
        "schema": "emergenz-knoten.p32d-shape-multipole-eligibility",
        "schema_version": 1,
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": _git("rev-parse", "HEAD"),
        "git_status": _git("status", "--porcelain"),
        "preregistration": "reports/project/meta/p32d_shape_multipole_preregistration_2026-08-06.md",
        "checkpoint": args.checkpoint.as_posix(),
        "checkpoint_update_index": checkpoint.update_index,
        "formation_seed": checkpoint.formation_seed,
        "config": asdict(config),
        "parameters": vars(args),
        "derived": {
            "continuation_memory_times": args.updates * config.alpha,
            "sample_interval_memory_times": sample_interval,
            "burn_samples": burn_index,
            "post_burn_samples": int(sample_steps.size - burn_index),
        },
        "runtime_seconds": time.perf_counter() - started,
        "rows": rows,
        "gate": {
            "source_gates": source_gates,
            "candidate_pass": any_pass,
            "classification": (
                "autonomous scalar shape-multipole source candidate"
                if any_pass
                else "no control-separated autonomous scalar shape-multipole source"
            ),
        },
        "plot_traces": plot_traces,
    }
    return _jsonable(payload)


def _plot(payload: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = payload["rows"]
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.6), constrained_layout=True)
    colors = {"baseline": "#0072B2", "eta_zero": "#888888"}
    for trace in payload["plot_traces"]:
        axes[0, 0].plot(
            trace["times"],
            trace["shape_norm"],
            color=colors[trace["condition"]],
            alpha=0.35,
            linewidth=0.8,
        )
    for condition in CONDITIONS:
        axes[0, 0].plot([], [], color=colors[condition], label=condition)
    axes[0, 0].set(
        xlabel="continuation / memory times",
        ylabel="||Q||F",
        title="Autonomous normalized traceless shape",
    )
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.25)

    for condition in CONDITIONS:
        for row in rows:
            spectrum = row["conditions"][condition]["sources"]["shape"]["full"]
            axes[0, 1].loglog(
                spectrum["frequencies"],
                spectrum["power_spectrum"],
                color=colors[condition],
                alpha=0.35,
                linewidth=0.8,
            )
        axes[0, 1].plot([], [], color=colors[condition], label=condition)
    axes[0, 1].set(
        xlabel="frequency / memory-time^-1",
        ylabel="summed Welch PSD",
        title="Shape-multipole spectra",
    )
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.25)

    x = np.arange(len(rows))
    width = 0.18
    for source_index, source in enumerate(SOURCES):
        for condition_index, condition in enumerate(CONDITIONS):
            ratios = [
                row["conditions"][condition]["sources"][source]["full"]["peak_to_background"]
                for row in rows
            ]
            offset = (2 * source_index + condition_index - 1.5) * width
            axes[1, 0].bar(
                x + offset,
                ratios,
                width,
                label=f"{source}:{condition}",
                alpha=0.8,
            )
    axes[1, 0].axhline(5.0, color="black", linestyle=":", linewidth=1)
    axes[1, 0].set(
        xticks=x,
        xticklabels=[str(row["future_seed"]) for row in rows],
        xlabel="future-noise seed",
        ylabel="peak / background",
        title="Primary spectral prominence",
    )
    axes[1, 0].legend(fontsize=7)
    axes[1, 0].grid(axis="y", alpha=0.25)

    markers = {"shape": "o", "shape_rate": "s"}
    for source in SOURCES:
        for row in rows:
            seed = row["future_seed"]
            metrics = row["conditions"]["baseline"]["sources"][source]
            frequencies = [
                segment["peak_frequency_cycles_per_memory_time"]
                for segment in metrics["segments"]
                if segment["segment_pass"]
            ]
            axes[1, 1].scatter(
                [seed] * len(frequencies),
                frequencies,
                marker=markers[source],
                label=source if seed == rows[0]["future_seed"] else None,
            )
    axes[1, 1].set(
        xticks=x + 1,
        xlabel="future-noise seed",
        ylabel="passing segment frequency / memory-time^-1",
        title="Baseline segment identity",
    )
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.25)
    fig.suptitle("P3.2d shape-multipole source eligibility")
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _format_metric(value: float | None, spec: str = ".4g") -> str:
    return "inf" if value is None else format(float(value), spec)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    gate = payload["gate"]
    lines = [
        "# P3.2d shape-multipole source eligibility",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Result",
        "",
        f"Classification: **{gate['classification']}**.",
        "",
    ]
    for source in SOURCES:
        item = gate["source_gates"][source]
        lines.extend(
            [
                f"- `{source}`: baseline {item['baseline_candidate_count']}/5, eta-zero {item['eta_zero_candidate_count']}/5, shape-bounded {item['baseline_shape_bounded_count']}/5, cross-seed frequency range {item['baseline_frequency_relative_range']}; pass={item['candidate_pass']}.",
            ]
        )
    lines.extend(
        [
            "",
            f"![P3.2d shape multipole]({(Path('../..') / figure.relative_to(ROOT)).as_posix()})",
            "",
            "## Seed diagnostics",
            "",
            "| seed | condition | source | peak f | peak/background | shuffle q99 | peak fraction | passing segments | segment frequency range | candidate |",
            "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in payload["rows"]:
        for condition in CONDITIONS:
            for source in SOURCES:
                item = row["conditions"][condition]["sources"][source]
                full = item["full"]
                lines.append(
                    f"| {row['future_seed']} | {condition} | {source} | {full['peak_frequency_cycles_per_memory_time']:.5g} | {full['peak_to_background']:.4g} | {item['shuffle_peak_ratio_q99']:.4g} | {full['peak_band_power_fraction']:.4g} | {item['passing_segment_count']}/4 | {_format_metric(item['segment_frequency_relative_range'])} | {item['candidate_pass']} |"
                )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This gate tests whether one autonomous scalar shape observable is eligible to source a later tensor channel. It does not insert that channel. A positive spectral peak would not establish propagation, reciprocal loading, spin, charge, dimension, quantization, or a particle identity.",
            "",
            "The five future-noise paths still branch from one formation state. They are not five independent knot basins.",
            "",
            "## Reproducibility",
            "",
            f"- preregistration: `{payload['preregistration']}`;",
            f"- checkpoint: `{payload['checkpoint']}` at N={payload['checkpoint_update_index']};",
            f"- git revision: `{payload['git_revision']}`;",
            f"- git status at start: `{'clean' if not payload['git_status'] else payload['git_status']}`;",
            f"- runtime: `{payload['runtime_seconds']:.3f} s`;",
            "- command: `python experiments/current/memory/synchronization/shape_multipole_eligibility_gate.py`;",
            f"- machine-readable summary: `{Path(payload['parameters']['summary_json']).as_posix()}`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    payload = run_gate(args)
    summary = _resolve(args.summary_json)
    report = _resolve(args.report)
    figure = _resolve(args.figure)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _plot(payload, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")
    print(payload["gate"]["classification"])
    print(report.relative_to(ROOT))


if __name__ == "__main__":
    main()
