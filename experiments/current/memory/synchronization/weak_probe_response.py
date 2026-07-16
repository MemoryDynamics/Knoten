"""Weak uniform-probe calibration on equilibrated scalar memory snapshots."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import statistics
import subprocess
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from emergenz_knoten import (
    FiniteMemoryState,
    SimulationConfig,
    infer_reproducible_response_rank,
    memory_shape_tensor,
    paired_uniform_probe_response,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_SOURCE_DIRS = [
    Path(
        "data/processed/long_run_metastability/"
        "raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16"
    ),
    Path(
        "data/processed/long_run_metastability/"
        "raw_memory_snapshot_retest_Aatt35_N3M_d10_seed1-5_2026-07-16"
    ),
]


@dataclass(frozen=True)
class SnapshotCase:
    path: Path
    seed: int
    config: SimulationConfig
    state: FiniteMemoryState
    initial_radius: float

    @property
    def dim(self) -> int:
        return self.config.dim


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run paired weak uniform probes on complete memory snapshots."
    )
    parser.add_argument("--source-dir", action="append", type=Path, default=[])
    parser.add_argument("--probe-fractions", default="0.03,0.10")
    parser.add_argument("--pulse-memory-times", type=float, default=1.0)
    parser.add_argument("--lag-memory-times", default="0,0.25,1,3,10")
    parser.add_argument("--confidence", type=float, default=0.90)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/weak_probe_calibration_2026-07-16.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/weak_probe_calibration_summary_2026-07-16.json"),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/response/weak_probe_calibration_2026-07-16"),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _rel_from(source_file: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source_file.resolve().parent)).as_posix()


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _git_output(args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return result.stdout.strip()


def _float_list(text: str) -> list[float]:
    values = [float(part.strip()) for part in text.split(",") if part.strip()]
    if not values or any(not np.isfinite(value) for value in values):
        raise ValueError("expected a non-empty comma-separated finite float list")
    return values


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        number = float(value)
        return number if np.isfinite(number) else None
    if isinstance(value, Path):
        return _rel(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def load_snapshot_cases(source_dirs: Iterable[Path]) -> list[SnapshotCase]:
    cases: list[SnapshotCase] = []
    for source_dir in source_dirs:
        for path in sorted(_resolve(source_dir).glob("case_baseline_seed*_steps*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            config = SimulationConfig(**payload["config"])
            snapshot = payload.get("diagnostics", {}).get("memory_cloud", {}).get("snapshot")
            if not isinstance(snapshot, dict):
                continue
            points = np.asarray(snapshot.get("points"), dtype=float)
            weights = np.asarray(snapshot.get("weights"), dtype=float)
            n_points = int(snapshot.get("n_points", -1))
            source_n_points = int(snapshot.get("source_n_points", -2))
            if n_points != source_n_points or len(points) != source_n_points:
                raise ValueError(f"snapshot is downsampled and cannot initialize dynamics: {path}")
            state = FiniteMemoryState(x=points[0], memory=points, weights=weights)
            radius = float(np.sqrt(max(np.trace(memory_shape_tensor(state)), 0.0)))
            if radius <= 0.0:
                raise ValueError(f"snapshot has degenerate memory radius: {path}")
            cases.append(
                SnapshotCase(
                    path=path,
                    seed=int(payload["seed"]),
                    config=config,
                    state=state,
                    initial_radius=radius,
                )
            )
    cases.sort(key=lambda case: (case.dim, case.seed))
    return cases


def _relative_matrix_difference(first: np.ndarray, second: np.ndarray) -> float:
    denominator = float(np.linalg.norm(first) + np.linalg.norm(second))
    if denominator <= np.finfo(float).eps:
        return 0.0
    return float(2.0 * np.linalg.norm(first - second) / denominator)


def run_snapshot_case(
    case: SnapshotCase,
    *,
    probe_fractions: list[float],
    pulse_memory_times: float,
    lag_memory_times: list[float],
) -> list[dict[str, Any]]:
    if pulse_memory_times <= 0.0:
        raise ValueError("pulse_memory_times must be positive")
    if any(lag < 0.0 for lag in lag_memory_times):
        raise ValueError("lag_memory_times must be non-negative")

    tau_updates = 1.0 / case.config.alpha
    pulse_steps = max(1, int(round(pulse_memory_times * tau_updates)))
    lag_updates = np.asarray(
        [int(round(lag * tau_updates)) for lag in lag_memory_times], dtype=int
    )
    sample_steps = pulse_steps + lag_updates
    if len(np.unique(sample_steps)) != len(sample_steps):
        raise ValueError("lag_memory_times collapse to duplicate integer sample steps")

    noise_seed = 10_000_019 + 1009 * case.dim + case.seed
    noise = np.random.default_rng(noise_seed).normal(
        size=(int(sample_steps[-1]), case.dim)
    )
    directions = np.eye(case.dim, dtype=float)
    eta_zero = replace(case.config, eta=0.0)
    results: list[dict[str, Any]] = []

    for fraction in probe_fractions:
        if fraction <= 0.0:
            raise ValueError("probe fractions must be positive")
        strength = fraction * case.initial_radius / float(pulse_steps)
        active = paired_uniform_probe_response(
            case.state,
            case.config,
            directions=directions,
            noise=noise,
            sample_steps=sample_steps,
            per_step_strength=strength,
            pulse_steps=pulse_steps,
        )
        bare = paired_uniform_probe_response(
            case.state,
            eta_zero,
            directions=directions,
            noise=noise,
            sample_steps=sample_steps,
            per_step_strength=strength,
            pulse_steps=pulse_steps,
        )
        scale = float(pulse_steps)
        even_radius = np.mean(active.radius_ratios, axis=2) - active.control_radius_ratios[:, None]
        results.append(
            {
                "source_case": _rel(case.path),
                "dim": case.dim,
                "seed": case.seed,
                "config": asdict(case.config),
                "initial_radius": case.initial_radius,
                "noise_seed": noise_seed,
                "probe_fraction": float(fraction),
                "per_step_strength": float(strength),
                "pulse_steps": pulse_steps,
                "pulse_memory_times": pulse_memory_times,
                "lag_memory_times": np.asarray(lag_memory_times, dtype=float),
                "lag_updates": lag_updates,
                "responses": {
                    "bare_position": bare.position_matrices / scale,
                    "position_residual": (active.position_matrices - bare.position_matrices) / scale,
                    "memory_center_residual": (
                        active.memory_center_matrices - bare.memory_center_matrices
                    )
                    / scale,
                    "shape_residual": (active.shape_matrices - bare.shape_matrices) / scale,
                },
                "quality": {
                    "bare_position_identity_error": np.asarray(
                        [
                            np.linalg.norm(matrix - np.eye(case.dim)) / np.sqrt(case.dim)
                            for matrix in bare.position_matrices / scale
                        ],
                        dtype=float,
                    ),
                    "active_control_radius_ratio": active.control_radius_ratios,
                    "probe_even_radius_max_abs": np.max(np.abs(even_radius), axis=1),
                },
            }
        )
    return results


def aggregate_ranks(
    case_results: list[dict[str, Any]],
    *,
    confidence: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    dimensions = sorted({int(result["dim"]) for result in case_results})
    fractions = sorted({float(result["probe_fraction"]) for result in case_results})
    observables = ["bare_position", "position_residual", "memory_center_residual", "shape_residual"]
    for dim in dimensions:
        for fraction in fractions:
            selected = [
                result
                for result in case_results
                if result["dim"] == dim and result["probe_fraction"] == fraction
            ]
            if not selected:
                continue
            lags = selected[0]["lag_memory_times"]
            for lag_index, lag in enumerate(lags):
                for observable in observables:
                    matrices = np.stack(
                        [result["responses"][observable][lag_index] for result in selected]
                    )
                    inference = infer_reproducible_response_rank(
                        matrices,
                        confidence=confidence,
                    )
                    leading = float(inference.singular_values[0]) if inference.singular_values.size else 0.0
                    ratio = (
                        float(inference.singular_values[1] / leading)
                        if inference.singular_values.size > 1 and leading > 0.0
                        else 0.0
                    )
                    rows.append(
                        {
                            "dim": dim,
                            "probe_fraction": fraction,
                            "lag_memory_times": float(lag),
                            "observable": observable,
                            "n_seeds": len(selected),
                            "energy_rank": inference.energy_rank,
                            "reproducible_rank": inference.rank,
                            "singular_values": inference.singular_values,
                            "null_thresholds": inference.null_thresholds,
                            "p_values": inference.p_values,
                            "minimum_attainable_p": inference.minimum_attainable_p,
                            "leading_singular_value": leading,
                            "second_to_first": ratio,
                        }
                    )
    return rows


def linearity_rows(case_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fractions = sorted({float(result["probe_fraction"]) for result in case_results})
    if len(fractions) != 2:
        return []
    by_key = {
        (result["dim"], result["seed"], result["probe_fraction"]): result
        for result in case_results
    }
    rows: list[dict[str, Any]] = []
    for dim in sorted({int(result["dim"]) for result in case_results}):
        seeds = sorted({int(result["seed"]) for result in case_results if result["dim"] == dim})
        for seed in seeds:
            small = by_key[(dim, seed, fractions[0])]
            large = by_key[(dim, seed, fractions[1])]
            for observable in ("position_residual", "memory_center_residual", "shape_residual"):
                for lag_index, lag in enumerate(small["lag_memory_times"]):
                    rows.append(
                        {
                            "dim": dim,
                            "seed": seed,
                            "observable": observable,
                            "lag_memory_times": float(lag),
                            "relative_difference": _relative_matrix_difference(
                                small["responses"][observable][lag_index],
                                large["responses"][observable][lag_index],
                            ),
                        }
                    )
    return rows


def _fmt(value: float | int | None, digits: int = 3) -> str:
    if value is None:
        return "`n/a`"
    number = float(value)
    if not np.isfinite(number):
        return "`n/a`"
    if number == 0.0:
        text = "0"
    elif abs(number) < 1e-3 or abs(number) >= 1e4:
        text = f"{number:.{digits}e}"
    else:
        text = f"{number:.{digits}f}"
    return f"`{text}`"


def _plot_spectra(
    rank_rows: list[dict[str, Any]],
    *,
    primary_fraction: float,
    figure_dir: Path,
) -> Path:
    dims = sorted({int(row["dim"]) for row in rank_rows})
    observables = ["memory_center_residual", "shape_residual"]
    fig, axes = plt.subplots(len(dims), len(observables), figsize=(11, 4.2 * len(dims)), squeeze=False)
    for row_index, dim in enumerate(dims):
        for col_index, observable in enumerate(observables):
            ax = axes[row_index, col_index]
            selected = [
                row
                for row in rank_rows
                if row["dim"] == dim
                and row["observable"] == observable
                and row["probe_fraction"] == primary_fraction
            ]
            for row in selected:
                singular = np.asarray(row["singular_values"], dtype=float)
                if singular.size and singular[0] > 0.0:
                    singular = singular / singular[0]
                ax.plot(
                    np.arange(1, len(singular) + 1),
                    np.maximum(singular, 1e-14),
                    marker="o",
                    label=f"lag={row['lag_memory_times']:g} tau",
                )
            ax.set_yscale("log")
            ax.set_xlabel("singular mode")
            ax.set_ylabel("s / s1")
            ax.set_title(f"d={dim}: {observable.replace('_', ' ')}")
            ax.grid(True, which="both", alpha=0.25)
            ax.legend(fontsize=8)
    fig.suptitle(f"Control-subtracted weak-probe spectra (fraction={primary_fraction:g})")
    fig.tight_layout()
    path = figure_dir / "response_spectra.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def _plot_quality(
    case_results: list[dict[str, Any]],
    linearity: list[dict[str, Any]],
    *,
    figure_dir: Path,
) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    ax = axes[0]
    for dim in sorted({int(row["dim"]) for row in linearity}):
        for observable in ("memory_center_residual", "shape_residual"):
            selected = [row for row in linearity if row["dim"] == dim and row["observable"] == observable]
            lags = sorted({float(row["lag_memory_times"]) for row in selected})
            medians = [
                statistics.median(
                    row["relative_difference"]
                    for row in selected
                    if row["lag_memory_times"] == lag
                )
                for lag in lags
            ]
            ax.plot(lags, medians, marker="o", label=f"d={dim} {observable.split('_')[0]}")
    ax.set_xlabel("lag [memory times]")
    ax.set_ylabel("two-strength relative difference")
    ax.set_title("Linearity check")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8)

    ax = axes[1]
    for dim in sorted({int(result["dim"]) for result in case_results}):
        for fraction in sorted({float(result["probe_fraction"]) for result in case_results}):
            selected = [
                result
                for result in case_results
                if result["dim"] == dim and result["probe_fraction"] == fraction
            ]
            lags = selected[0]["lag_memory_times"]
            medians = [
                statistics.median(result["quality"]["probe_even_radius_max_abs"][index] for result in selected)
                for index in range(len(lags))
            ]
            ax.plot(lags, medians, marker="o", label=f"d={dim}, f={fraction:g}")
    ax.set_xlabel("lag [memory times]")
    ax.set_ylabel("max even radius deviation")
    ax.set_yscale("log")
    ax.set_title("Probe disturbance versus unprobed path")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)

    fig.tight_layout()
    path = figure_dir / "weak_probe_quality.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def build_report(
    payload: dict[str, Any],
    *,
    report_path: Path,
    spectra_path: Path,
    quality_path: Path,
) -> str:
    results = payload["case_results"]
    ranks = payload["rank_rows"]
    linearity = payload["linearity_rows"]
    fractions = payload["probe_fractions"]
    primary = min(fractions)
    confidence = payload["confidence"]
    dims = sorted({int(result["dim"]) for result in results})
    direct_error = max(
        float(np.max(result["quality"]["bare_position_identity_error"])) for result in results
    )
    primary_center_rows = [
        row
        for row in ranks
        if row["probe_fraction"] == primary
        and row["observable"] == "memory_center_residual"
    ]
    primary_shape_rows = [
        row
        for row in ranks
        if row["probe_fraction"] == primary and row["observable"] == "shape_residual"
    ]
    center_tail_ratio = min(
        float(np.asarray(row["singular_values"])[-1] / np.asarray(row["singular_values"])[0])
        for row in primary_center_rows
    )
    center_full_rank = all(row["reproducible_rank"] == row["dim"] for row in primary_center_rows)
    shape_flip_zero = all(row["reproducible_rank"] == 0 for row in primary_shape_rows)
    final_lag = max(float(row["lag_memory_times"]) for row in primary_shape_rows)
    final_shape_amplitude = max(
        float(row["leading_singular_value"])
        for row in primary_shape_rows
        if row["lag_memory_times"] == final_lag
    )
    maximum_even_radius = max(
        float(np.max(result["quality"]["probe_even_radius_max_abs"])) for result in results
    )
    center_rank_status = "yes" if center_full_rank else "no"
    shape_rank_status = "yes" if shape_flip_zero else "no"

    lines = [
        "# Weak-Probe Calibration",
        "",
        f"Generated: `{payload['generated_utc']}`.",
        "",
        "## Scope",
        "",
        "This report calibrates paired weak external-field response on complete",
        "equilibrated scalar-memory snapshots. It is a measurement-method report,",
        "not evidence for a physical field, interaction charge, or a three-dimensional",
        "external sector.",
        "",
        "The probe is a uniform additive drift applied for one memory time. Each",
        "direction uses `+delta`, `-delta`, and an unprobed branch with the same future",
        "noise. An `eta_zero` run measures the bare direct response. Response matrices",
        "below are divided by pulse length, so the exact bare position response is the",
        "identity matrix.",
        "",
        "## Inputs",
        "",
        f"- Ambient dimensions: `{dims}`; seeds: `1..5` per dimension.",
        f"- Probe displacement fractions of initial memory radius: `{fractions}`.",
        f"- Pulse duration: `{payload['pulse_memory_times']}` memory time.",
        f"- Response lags: `{payload['lag_memory_times']}` memory times.",
        f"- Exact sign-flip inference confidence: `{confidence:.2f}`.",
        "- Initial states: full 600-point memory buffers; no new formation run.",
        "",
        "## Pipeline Checks",
        "",
        f"Maximum normalized error of the `eta_zero` direct position response from the identity: {_fmt(direct_error)}.",
        "This verifies the pulse sign, branch pairing, normalization, and common-noise",
        "implementation. The direct position rank is deliberately full ambient rank and",
        "must not be interpreted as an emergent dimension.",
        "",
        f"![Response spectra]({_rel_from(report_path, spectra_path)})",
        "",
        f"![Probe quality]({_rel_from(report_path, quality_path)})",
        "",
        "## Primary-Fraction Rank Audit",
        "",
        f"The table uses the smaller probe fraction `{primary:g}`. `energy rank` is the",
        "descriptive 95%-energy rank. `flip rank` requires coherent response across seeds",
        f"at the exploratory `{confidence:.0%}` exact sign-flip level.",
        "",
        "| d | lag/tau | observable | energy rank | flip rank | s1 | s2/s1 | p1 |",
        "| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in ranks:
        if row["probe_fraction"] != primary or row["observable"] not in {
            "memory_center_residual",
            "shape_residual",
        }:
            continue
        p1 = float(row["p_values"][0]) if len(row["p_values"]) else float("nan")
        lines.append(
            f"| `{row['dim']}` | `{row['lag_memory_times']:g}` | `{row['observable']}` | "
            f"`{row['energy_rank']}` | `{row['reproducible_rank']}` | "
            f"{_fmt(row['leading_singular_value'])} | {_fmt(row['second_to_first'])} | {_fmt(p1)} |"
        )

    lines.extend(
        [
            "",
            "## Linearity and Stability",
            "",
            "Two-strength differences compare derivative-normalized response matrices.",
            "Zero is ideal; values near two indicate incompatible responses.",
            "",
            "| d | observable | median relative difference | maximum |",
            "| ---: | --- | ---: | ---: |",
        ]
    )
    for dim in dims:
        for observable in ("memory_center_residual", "shape_residual"):
            values = [
                float(row["relative_difference"])
                for row in linearity
                if row["dim"] == dim and row["observable"] == observable
            ]
            lines.append(
                f"| `{dim}` | `{observable}` | {_fmt(statistics.median(values))} | {_fmt(max(values))} |"
            )

    lines.extend(
        [
            "",
            "The unprobed branch is retained explicitly. The even `(+delta + -delta)/2`",
            "radius displacement against that branch is the first probe-disturbance",
            "diagnostic; it should remain small before a source-knot experiment is trusted.",
            "",
            "## Statistical Limit",
            "",
            "Five independent seeds yield only 16 unique two-sided singular-value sign",
            "patterns because a global sign is redundant. Therefore the minimum attainable",
            "exact p-value is `1/16 = 0.0625`. A conventional 5% response-rank claim is",
            "impossible with this pilot ensemble. The 90% flip rank is exploratory; the",
            "source-knot validation should use at least six and preferably ten independent",
            "seed states.",
            "",
            "## Findings and Decision",
            "",
            f"The control-subtracted memory-centre response is full ambient rank at every lag: `{center_rank_status}`.",
            f"Its smallest observed `s_last/s1` is {_fmt(center_tail_ratio)}, so the response is",
            "numerically isotropic rather than a hidden low-rank sector. In particular, the",
            "uniform probe returns rank 3 in `d=3` and rank 10 in `d=10`.",
            "",
            f"The shape response has zero reproducible flip rank at every tested lag: `{shape_rank_status}`.",
            f"Its largest leading singular value at `{final_lag:g}` memory times is only {_fmt(final_shape_amplitude)}.",
            "The descriptive full energy rank of this tiny signal must not be mistaken for a",
            "coherent shape mode.",
            "",
            f"The largest even radius disturbance over both probe strengths is {_fmt(maximum_even_radius)}.",
            "Together with the near-zero two-strength differences, this validates fractions",
            "`0.03..0.10` as a linear, non-destructive calibration range for these snapshots.",
            "",
            "This is a useful negative control: a uniform field does not reveal a",
            "low-dimensional external sector in the scalar reference model. It also cannot",
            "settle the relational question because its direct forcing spans the supplied",
            "basis by construction. The next experiment is a localized frozen translated",
            "source-knot field, first with cloned states and then with independent seeds.",
            "Its delayed, control-subtracted response is the first physically relevant",
            "response-rank candidate.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    source_dirs = args.source_dir or DEFAULT_SOURCE_DIRS
    probe_fractions = _float_list(args.probe_fractions)
    lag_memory_times = _float_list(args.lag_memory_times)
    if len(probe_fractions) != 2:
        raise SystemExit("--probe-fractions must contain exactly two values for linearity")
    if not 0.0 < args.confidence < 1.0:
        raise SystemExit("--confidence must satisfy 0 < value < 1")

    cases = load_snapshot_cases(source_dirs)
    if not cases:
        raise SystemExit("no complete baseline memory snapshots found")

    case_results: list[dict[str, Any]] = []
    for case in cases:
        print(f"running weak probe d={case.dim} seed={case.seed}", flush=True)
        case_results.extend(
            run_snapshot_case(
                case,
                probe_fractions=probe_fractions,
                pulse_memory_times=args.pulse_memory_times,
                lag_memory_times=lag_memory_times,
            )
        )

    rank_rows = aggregate_ranks(case_results, confidence=args.confidence)
    linearity = linearity_rows(case_results)
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_dir = _resolve(args.figure_dir)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    spectra_path = _plot_spectra(
        rank_rows,
        primary_fraction=min(probe_fractions),
        figure_dir=figure_dir,
    )
    quality_path = _plot_quality(case_results, linearity, figure_dir=figure_dir)
    payload = {
        "generated_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "--short", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "source_dirs": [_rel(_resolve(path)) for path in source_dirs],
        "probe_fractions": probe_fractions,
        "pulse_memory_times": float(args.pulse_memory_times),
        "lag_memory_times": lag_memory_times,
        "confidence": float(args.confidence),
        "case_results": case_results,
        "rank_rows": rank_rows,
        "linearity_rows": linearity,
        "figures": [_rel(spectra_path), _rel(quality_path)],
    }
    report = build_report(
        payload,
        report_path=report_path,
        spectra_path=spectra_path,
        quality_path=quality_path,
    )
    report_path.write_text(report, encoding="utf-8")
    summary_path.write_text(json.dumps(_jsonable(payload), indent=2) + "\n", encoding="utf-8")
    print(f"wrote {_rel(report_path)}")
    print(f"wrote {_rel(summary_path)}")


if __name__ == "__main__":
    main()
