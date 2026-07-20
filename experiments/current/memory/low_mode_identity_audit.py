from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten.markov.closure import (  # noqa: E402
    ARSpectrum,
    fit_ar_spectrum,
    mode_subspace_overlap,
)
from emergenz_knoten.spectral_memory_field import (  # noqa: E402
    SpectralMemoryConfig,
    zero_mean_attractive_kernel,
)
from emergenz_knoten.spectral_memory_trace import (  # noqa: E402
    low_mode_feature_names,
    simulate_spectral_memory_trace,
)


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(item < 1 for item in values):
        raise argparse.ArgumentTypeError("expected positive comma-separated integers")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Identify low-mode AR eigenvectors across seeds and time segments."
    )
    parser.add_argument("--steps", type=int, default=300_000)
    parser.add_argument("--burn-in", type=int, default=15_000)
    parser.add_argument("--sample-every", type=int, default=20)
    parser.add_argument("--seeds", type=_parse_int_list, default=[1, 2, 3, 4, 5])
    parser.add_argument("--segments", type=int, default=5)
    parser.add_argument("--lags", type=_parse_int_list, default=[1, 5])
    parser.add_argument("--epsilon", type=float, default=1e-4)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--lambda-value", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--box-length", type=float, default=80.0)
    parser.add_argument("--n-modes", type=int, default=64)
    parser.add_argument("--n-low-modes", type=int, default=3)
    parser.add_argument("--diffusion-length-ratio", type=float, default=0.3)
    parser.add_argument("--amplitude-att", type=float, default=26.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--sigma-comp", type=float, default=10.0)
    parser.add_argument("--ridge", type=float, default=1e-6)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/memory/low_mode_identity_audit_2026-07-20.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/memory/low_mode_identity_audit_2026-07-20.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path("figures/draft/memory/low_mode_identity_audit_2026-07-20.png"),
    )
    return parser.parse_args()


def _validate_args(args: argparse.Namespace) -> None:
    if args.steps < 1_000 or not 0 <= args.burn_in < args.steps:
        raise SystemExit("steps must be >= 1000 and burn-in smaller than steps")
    if args.sample_every < 1 or args.segments < 2:
        raise SystemExit("sample-every must be positive and segments >= 2")
    if args.n_low_modes < 1 or args.n_low_modes > args.n_modes:
        raise SystemExit("n-low-modes must lie in [1, n-modes]")
    if not 0.0 < args.lambda_value <= 1.0:
        raise SystemExit("lambda-value must lie in (0, 1]")
    n_samples = args.steps // args.sample_every - args.burn_in // args.sample_every
    if n_samples // args.segments <= max(args.lags) + 2:
        raise SystemExit("segments are too short for the requested lags")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _git_output(arguments: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return result.stdout.strip()


def _config(args: argparse.Namespace) -> SpectralMemoryConfig:
    return SpectralMemoryConfig(
        box_length=float(args.box_length),
        n_modes=int(args.n_modes),
        lambda_value=float(args.lambda_value),
        memory_mass=float(args.memory_mass),
        deposition_sigma=0.0,
        kernel=zero_mean_attractive_kernel(
            amplitude_att=float(args.amplitude_att),
            sigma_att=float(args.sigma_att),
            sigma_comp=float(args.sigma_comp),
        ),
    )


def _diffusion(args: argparse.Namespace, ratio: float) -> float:
    length = float(ratio) * float(args.sigma_att)
    return float(0.5 * args.lambda_value * length**2)


def _active_indices(all_series: list[np.ndarray]) -> list[int]:
    pooled = np.concatenate(all_series, axis=0)
    scales = pooled.std(axis=0)
    reference = max(float(np.max(scales)), np.finfo(float).eps)
    indices = [
        index
        for index, scale in enumerate(scales)
        if float(scale) > 1e-10 * reference
    ]
    if not indices:
        raise RuntimeError("low-mode trace has no varying features")
    return indices


def _mode_indices(spectrum: ARSpectrum, kind: str) -> list[int]:
    indices = []
    for index, eigenvalue in enumerate(spectrum.eigenvalues):
        modulus = abs(eigenvalue)
        if not 0.05 < modulus < 1.0:
            continue
        if kind == "real" and abs(eigenvalue.imag) <= 1e-8:
            indices.append(index)
        elif kind == "complex" and eigenvalue.imag > 1e-8:
            indices.append(index)
    return indices


def _match_reference_mode(
    reference_vector: np.ndarray,
    spectrum: ARSpectrum,
    *,
    kind: str,
) -> tuple[int | None, float]:
    candidates = _mode_indices(spectrum, kind)
    if not candidates:
        return None, 0.0
    overlaps = [
        mode_subspace_overlap(reference_vector, spectrum.feature_eigenvectors[:, index])
        for index in candidates
    ]
    best = int(np.argmax(overlaps))
    return candidates[best], float(overlaps[best])


def _relative_mad(values: list[float]) -> float:
    finite = np.asarray([value for value in values if math.isfinite(value)], dtype=float)
    if finite.size == 0:
        return float("nan")
    median = float(np.median(finite))
    mad = float(np.median(np.abs(finite - median)))
    return mad / max(abs(median), 1e-12)


def _serialize_vector(vector: np.ndarray) -> dict[str, list[float]]:
    return {
        "real": [float(value) for value in vector.real],
        "imag": [float(value) for value in vector.imag],
        "magnitude": [float(value) for value in np.abs(vector)],
    }


def _arm_summary(
    *,
    arm: str,
    lag: int,
    lag_updates: int,
    lambda_value: float,
    series: list[np.ndarray],
    segments: int,
    ridge: float,
    feature_names: list[str],
) -> list[dict[str, Any]]:
    reference = fit_ar_spectrum(
        series,
        lag=lag,
        lag_updates=lag_updates,
        ridge=ridge,
    )
    rows: list[dict[str, Any]] = []
    for kind in ("real", "complex"):
        candidates = _mode_indices(reference, kind)
        if not candidates:
            rows.append(
                {
                    "arm": arm,
                    "kind": kind,
                    "lag_samples": lag,
                    "lag_updates": lag_updates,
                    "lag_memory_times": lag_updates * lambda_value,
                    "reference_present": False,
                    "matches": [],
                }
            )
            continue
        reference_index = candidates[0]
        reference_vector = reference.feature_eigenvectors[:, reference_index]
        matches: list[dict[str, Any]] = []
        for seed_index, values in enumerate(series):
            for segment_index, segment in enumerate(np.array_split(values, segments)):
                spectrum = fit_ar_spectrum(
                    [segment],
                    lag=lag,
                    lag_updates=lag_updates,
                    ridge=ridge,
                )
                match_index, overlap = _match_reference_mode(
                    reference_vector,
                    spectrum,
                    kind=kind,
                )
                if match_index is None:
                    matches.append(
                        {
                            "seed_index": seed_index,
                            "segment_index": segment_index,
                            "present": False,
                            "overlap": 0.0,
                        }
                    )
                    continue
                rate = float(spectrum.rates_per_update[match_index] / lambda_value)
                frequency = float(
                    abs(spectrum.angular_frequencies_per_update[match_index])
                    / lambda_value
                )
                matches.append(
                    {
                        "seed_index": seed_index,
                        "segment_index": segment_index,
                        "present": True,
                        "overlap": overlap,
                        "rate_per_memory_time": rate,
                        "frequency_per_memory_time": frequency,
                        "quality_factor": frequency / max(2.0 * rate, 1e-12),
                    }
                )
        present = [row for row in matches if row["present"]]
        overlaps = [float(row["overlap"]) for row in present]
        rates = [float(row["rate_per_memory_time"]) for row in present]
        frequencies = [
            float(row["frequency_per_memory_time"])
            for row in present
            if kind == "complex"
        ]
        rows.append(
            {
                "arm": arm,
                "kind": kind,
                "lag_samples": lag,
                "lag_updates": lag_updates,
                "lag_memory_times": lag_updates * lambda_value,
                "reference_present": True,
                "reference_eigenvalue": {
                    "real": float(reference.eigenvalues[reference_index].real),
                    "imag": float(reference.eigenvalues[reference_index].imag),
                    "modulus": float(abs(reference.eigenvalues[reference_index])),
                },
                "reference_vector": _serialize_vector(reference_vector),
                "reference_feature_loadings": {
                    name: float(abs(value))
                    for name, value in zip(feature_names, reference_vector, strict=True)
                },
                "match_fraction": len(present) / len(matches),
                "overlap_median": float(np.median(overlaps)) if overlaps else 0.0,
                "overlap_min": float(np.min(overlaps)) if overlaps else 0.0,
                "rate_median_per_memory_time": (
                    float(np.median(rates)) if rates else float("nan")
                ),
                "rate_relative_mad": _relative_mad(rates),
                "frequency_median_per_memory_time": (
                    float(np.median(frequencies)) if frequencies else 0.0
                ),
                "frequency_relative_mad": _relative_mad(frequencies),
                "quality_factor_median": (
                    float(
                        np.median(
                            [float(row["quality_factor"]) for row in present]
                        )
                    )
                    if kind == "complex" and present
                    else 0.0
                ),
                "matches": matches,
            }
        )
    return rows


def _reference_vector(row: dict[str, Any]) -> np.ndarray | None:
    if not row["reference_present"]:
        return None
    payload = row["reference_vector"]
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def _gate_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    active_real = [
        row for row in rows if row["arm"] == "active_nu03" and row["kind"] == "real"
    ]
    active_complex = [
        row
        for row in rows
        if row["arm"] == "active_nu03" and row["kind"] == "complex"
    ]
    real_identity = bool(
        active_real
        and all(
            row["reference_present"]
            and row["match_fraction"] >= 0.8
            and row["overlap_median"] >= 0.8
            and row["rate_relative_mad"] < 0.25
            for row in active_real
        )
    )
    complex_segment_identity = bool(
        active_complex
        and all(
            row["reference_present"]
            and row["match_fraction"] >= 0.8
            and row["overlap_median"] >= 0.8
            and row["frequency_relative_mad"] < 0.25
            and row["quality_factor_median"] >= 0.5
            for row in active_complex
        )
    )

    control_overlaps: list[dict[str, Any]] = []
    for active in active_complex:
        active_vector = _reference_vector(active)
        if active_vector is None:
            continue
        for control_arm in ("eta_zero_nu03", "active_nu0"):
            controls = [
                row
                for row in rows
                if row["arm"] == control_arm
                and row["kind"] == "complex"
                and math.isclose(
                    row["lag_memory_times"],
                    active["lag_memory_times"],
                )
            ]
            overlap = 0.0
            if controls:
                control_vector = _reference_vector(controls[0])
                if control_vector is not None:
                    overlap = mode_subspace_overlap(active_vector, control_vector)
            control_overlaps.append(
                {
                    "lag_memory_times": active["lag_memory_times"],
                    "control_arm": control_arm,
                    "reference_subspace_overlap": overlap,
                    "control_reference_present": bool(
                        controls and controls[0]["reference_present"]
                    ),
                }
            )
    complex_control_separated = bool(
        control_overlaps
        and all(
            not row["control_reference_present"]
            or row["reference_subspace_overlap"] < 0.5
            for row in control_overlaps
        )
    )
    return {
        "real_mode_identity_pass": real_identity,
        "complex_segment_identity_pass": complex_segment_identity,
        "complex_control_separation_pass": complex_control_separated,
        "oscillatory_mode_supported": bool(
            complex_segment_identity and complex_control_separated
        ),
        "control_reference_overlaps": control_overlaps,
    }


def run_audit(args: argparse.Namespace) -> dict[str, Any]:
    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    config = _config(args)
    arm_specs = (
        ("active_nu03", args.eta, args.diffusion_length_ratio),
        ("eta_zero_nu03", 0.0, args.diffusion_length_ratio),
        ("active_nu0", args.eta, 0.0),
    )
    noises = {
        seed: np.random.default_rng(seed).normal(size=args.steps)
        for seed in args.seeds
    }
    traces: dict[str, list[np.ndarray]] = {}
    all_series: list[np.ndarray] = []
    for arm, eta, ratio in arm_specs:
        traces[arm] = []
        for seed in args.seeds:
            trace = simulate_spectral_memory_trace(
                config,
                noise=noises[seed],
                diffusion_per_update=_diffusion(args, ratio),
                epsilon=float(args.epsilon),
                eta=float(eta),
                burn_in=int(args.burn_in),
                sample_every=int(args.sample_every),
                n_low_modes=int(args.n_low_modes),
                real_offsets=(),
                history_length=0,
            )
            traces[arm].append(trace.values)
            all_series.append(trace.values)

    indices = _active_indices(all_series)
    names = list(low_mode_feature_names(args.n_low_modes, ()))
    active_names = [names[index] for index in indices]
    rows: list[dict[str, Any]] = []
    for arm, _, _ in arm_specs:
        selected = [values[:, indices] for values in traces[arm]]
        for lag in args.lags:
            rows.extend(
                _arm_summary(
                    arm=arm,
                    lag=int(lag),
                    lag_updates=int(lag) * int(args.sample_every),
                    lambda_value=float(args.lambda_value),
                    series=selected,
                    segments=int(args.segments),
                    ridge=float(args.ridge),
                    feature_names=active_names,
                )
            )

    return {
        "description": "Eigenvector and time-segment identity audit for scalar low modes.",
        "created_utc": datetime.now(UTC).isoformat(),
        "git_revision": git_revision,
        "git_status": git_status,
        "parameters": {
            key: value
            for key, value in vars(args).items()
            if key not in {"report", "summary_json", "figure"}
        },
        "active_feature_names": active_names,
        "rows": rows,
        "gate": _gate_summary(rows),
    }


def _plot(payload: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = payload["rows"]
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.0))
    colors = {
        "active_nu03": "#0072B2",
        "eta_zero_nu03": "#D55E00",
        "active_nu0": "#009E73",
    }
    markers = {"real": "o", "complex": "s"}
    for arm, color in colors.items():
        for kind in ("real", "complex"):
            selected = sorted(
                [row for row in rows if row["arm"] == arm and row["kind"] == kind],
                key=lambda row: row["lag_memory_times"],
            )
            x = [row["lag_memory_times"] for row in selected]
            axes[0, 0].plot(
                x,
                [row.get("overlap_median", 0.0) for row in selected],
                marker=markers[kind],
                color=color,
                linestyle="-" if kind == "real" else "--",
                label=f"{arm}, {kind}",
            )
            if kind == "real":
                axes[0, 1].plot(
                    x,
                    [row.get("rate_median_per_memory_time", np.nan) for row in selected],
                    marker="o",
                    color=color,
                    label=arm,
                )
            else:
                axes[1, 0].plot(
                    x,
                    [
                        row.get("frequency_median_per_memory_time", np.nan)
                        for row in selected
                    ],
                    marker="s",
                    color=color,
                    label=arm,
                )
    axes[0, 0].axhline(0.8, color="#666666", linewidth=1)
    axes[0, 0].set_ylabel("median mode-subspace overlap")
    axes[0, 0].legend(fontsize=7, ncol=2)
    axes[0, 1].set_ylabel("real-mode rate / memory time")
    axes[0, 1].legend(fontsize=8)
    axes[1, 0].set_ylabel("complex frequency / memory time")
    axes[1, 0].legend(fontsize=8)
    for axis in axes.flat[:3]:
        axis.set_xscale("log")
        axis.set_xlabel("lag / memory time")
        axis.grid(alpha=0.25)

    active_complex = next(
        (
            row
            for row in rows
            if row["arm"] == "active_nu03"
            and row["kind"] == "complex"
            and row["reference_present"]
        ),
        None,
    )
    if active_complex is not None:
        loadings = active_complex["reference_feature_loadings"]
        names = list(loadings)
        values = [loadings[name] for name in names]
        axes[1, 1].bar(np.arange(len(names)), values, color="#CC79A7")
        axes[1, 1].set_xticks(
            np.arange(len(names)),
            names,
            rotation=35,
            ha="right",
        )
        axes[1, 1].set_ylabel("active complex-mode loading")
    axes[1, 1].grid(axis="y", alpha=0.25)
    fig.suptitle("Low-mode identity: eigenvectors, segments, and controls")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    gate = payload["gate"]
    lines = [
        "# Low-Mode Eigenvector and Segment Identity Audit",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Question",
        "",
        "Do the previously fitted real and complex AR eigenvalues represent the",
        "same feature-space modes across independent seeds and time segments?",
        "This is a diagnostic closure audit, not a search for new physics.",
        "",
        "## Controls",
        "",
        "- active feedback with diffusion-length ratio 0.3;",
        "- eta=0 under identical seed noise;",
        "- nu=0 under identical seed noise;",
        "- five non-overlapping time segments per seed;",
        "- physical feature eigenvectors compared as sign/phase-invariant real subspaces.",
        "",
        "## Gate",
        "",
        f"- Real-mode identity: {gate['real_mode_identity_pass']}.",
        f"- Complex segment identity: {gate['complex_segment_identity_pass']}.",
        f"- Complex control separation: {gate['complex_control_separation_pass']}.",
        f"- Oscillatory mode supported: {gate['oscillatory_mode_supported']}.",
        "",
        f"![Mode identity audit]({_relative(report, figure)})",
        "",
        "## Segment statistics",
        "",
        "| arm | kind | lag / memory time | match fraction | median overlap | "
        "relative rate MAD | relative frequency MAD | median Q |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['arm']} | {row['kind']} | {row['lag_memory_times']:.2f} | "
            f"{row.get('match_fraction', 0.0):.3f} | "
            f"{row.get('overlap_median', 0.0):.3f} | "
            f"{row.get('rate_relative_mad', float('nan')):.3f} | "
            f"{row.get('frequency_relative_mad', float('nan')):.3f} | "
            f"{row.get('quality_factor_median', 0.0):.3f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "A positive real-mode result only validates a reproducible reduced",
            "relaxation direction. A complex mode requires both segment identity",
            "and absence from eta=0 and nu=0 controls. Failure of either condition",
            "keeps it classified as a fitting, sampling, or representation mode.",
            "",
            "## Limits",
            "",
            "- Stochastic traces are exactly regenerated from recorded seeds rather",
            "  than archived.",
            "- Segment fits are descriptive and not independent basin samples.",
            "- The model remains one-dimensional and scalar.",
            "- No photon, spin, synchronization, or propagation claim follows.",
            "",
            "## Reproduction",
            "",
            "    python experiments/current/memory/low_mode_identity_audit.py",
            "",
            f"Git revision: {payload['git_revision']}.",
            f"Git status at generation: {payload['git_status'] or 'clean'}.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    _validate_args(args)
    payload = run_audit(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
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

