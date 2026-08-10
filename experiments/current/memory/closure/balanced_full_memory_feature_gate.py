"""Preregistered balanced closure gate for the passive full oriented memory."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import glob
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from emergenz_knoten import (
    FiniteMemoryState,
    SimulationConfig,
    advance_oriented_memory_state,
    balanced_hankel_spectrum,
    initialize_oriented_memory_state,
    memory_shape_tensor,
    minimum_principal_cosine,
    passive_delay_observability,
    passive_delay_reachability,
    place_oriented_memory_state,
    randomized_holdout_error,
    select_balanced_rank,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_CASE_GLOBS = (
    "data/processed/long_run_metastability/"
    "raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/"
    "case_baseline_seed*.json",
    "data/processed/long_run_metastability/"
    "raw_memory_snapshot_retest_Aatt35_N3M_d3_seed6_2026-07-22/"
    "case_baseline_seed*.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-glob", action="append", default=None)
    parser.add_argument("--seeds", default="1,2,3,4,5,6")
    parser.add_argument("--lambda-vector", type=float, default=0.01)
    parser.add_argument("--orientation-relaxation", type=float, default=0.01)
    parser.add_argument("--vector-mass", type=float, default=1.0)
    parser.add_argument("--distance-ratio", type=float, default=2.5)
    parser.add_argument("--far-distance-ratio", type=float, default=5.0)
    parser.add_argument("--sigma-ratio", type=float, default=2.5)
    parser.add_argument("--horizons-memory-times", default="5,10")
    parser.add_argument("--cadences", default="1,5,10")
    parser.add_argument("--max-modes", type=int, default=12)
    parser.add_argument("--max-rank", type=int, default=8)
    parser.add_argument("--minimum-gap", type=float, default=3.0)
    parser.add_argument("--minimum-energy", type=float, default=0.90)
    parser.add_argument("--minimum-cosine", type=float, default=0.90)
    parser.add_argument("--maximum-holdout-error", type=float, default=0.15)
    parser.add_argument("--maximum-tail-relative-se", type=float, default=0.05)
    parser.add_argument("--energy-probes", type=int, default=64)
    parser.add_argument("--holdout-probes", type=int, default=64)
    parser.add_argument("--required-pairs", type=int, default=5)
    parser.add_argument("--noise-seed", type=int, default=20_260_810)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/memory/closure/balanced_full_memory_feature_gate_2026-08-10.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/memory/closure/balanced_full_memory_feature_gate_2026-08-10.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/balanced_full_memory_feature_gate_2026-08-10.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _relative_from(source: Path, target: Path) -> str:
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


def _parse_ints(text: str) -> list[int]:
    values = [int(item.strip()) for item in text.split(",") if item.strip()]
    if not values or any(value < 1 for value in values):
        raise ValueError("expected positive comma-separated integers")
    return values


def _parse_floats(text: str) -> list[float]:
    values = [float(item.strip()) for item in text.split(",") if item.strip()]
    if not values or not np.isfinite(values).all():
        raise ValueError("expected finite comma-separated values")
    return values


def _load_case(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    if payload.get("condition") != "baseline":
        raise ValueError(f"{path} is not a baseline case")
    config = SimulationConfig(**payload["config"])
    snapshot = payload["diagnostics"]["memory_cloud"]["snapshot"]
    points = np.asarray(snapshot["points"], dtype=float)
    weights = np.asarray(snapshot["weights"], dtype=float)
    if points.ndim != 2 or points.shape[1] != config.dim:
        raise ValueError(f"invalid snapshot shape in {path}")
    return {
        "path": path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "seed": int(payload["seed"]),
        "config": config,
        "state": FiniteMemoryState(x=points[0], memory=points, weights=weights),
    }


def _discover_cases(patterns: list[str], seeds: list[int]) -> dict[int, dict[str, Any]]:
    paths = {
        Path(value).resolve()
        for pattern in patterns
        for value in glob.glob(str(_resolve(Path(pattern))))
    }
    cases: dict[int, dict[str, Any]] = {}
    for path in sorted(paths):
        case = _load_case(path)
        if case["seed"] in seeds:
            if case["seed"] in cases:
                raise ValueError(f"duplicate case for seed {case['seed']}")
            cases[case["seed"]] = case
    missing = sorted(set(seeds) - set(cases))
    if missing:
        raise FileNotFoundError(f"missing cases for seeds {missing}")
    return cases


def _indices(horizon: int, cadence: int) -> np.ndarray:
    values = np.arange(0, horizon + 1, cadence, dtype=int)
    if values[-1] != horizon:
        values = np.append(values, horizon)
    return values


def _readout_factors(probe: np.ndarray, state: Any, sigma: float) -> np.ndarray:
    differences = probe[None, :] - state.scalar_state.memory
    radius2 = np.einsum("ij,ij->i", differences, differences)
    return np.exp(-0.5 * radius2 / sigma**2)


def generate_segment_rows(
    state: Any,
    config: SimulationConfig,
    *,
    near_probe: np.ndarray,
    far_probe: np.ndarray,
    vector_sigma: float,
    n_steps: int,
    random_seed: int,
) -> tuple[dict[str, np.ndarray], Any]:
    """Advance one passive segment and collect actual and control readouts."""

    near = np.empty((n_steps + 1, state.weights.size))
    far = np.empty_like(near)
    shuffled = np.empty_like(near)
    flat = np.broadcast_to(state.weights, near.shape).copy()
    rng = np.random.default_rng(random_seed)
    shuffle_rng = np.random.default_rng(random_seed + 1)
    age_permutation = shuffle_rng.permutation(state.weights.size)
    noise = rng.normal(size=(n_steps, config.dim))
    for step in range(n_steps + 1):
        near_factors = _readout_factors(near_probe, state, vector_sigma)
        far_factors = _readout_factors(far_probe, state, vector_sigma)
        near[step] = state.weights * near_factors
        far[step] = state.weights * far_factors
        shuffled[step] = state.weights * near_factors[age_permutation]
        if step < n_steps:
            state = advance_oriented_memory_state(
                state, config, noise_increment=noise[step]
            )
    return {"actual": near, "far": far, "flat": flat, "shuffled": shuffled}, state


def analyze_readout(
    rows: np.ndarray,
    *,
    holdout_rows: np.ndarray | None,
    horizon: int,
    cadence: int,
    carrier_decay: float,
    deposition_gain: float,
    args: argparse.Namespace,
    random_seed: int,
) -> dict[str, Any]:
    selected = _indices(horizon, cadence)
    reachability = passive_delay_reachability(
        rows.shape[1],
        horizon + 1,
        carrier_decay=carrier_decay,
        deposition_gain=deposition_gain,
    )
    observability = passive_delay_observability(
        rows[selected], selected, carrier_decay=carrier_decay
    )
    spectrum = balanced_hankel_spectrum(
        observability,
        reachability,
        max_modes=args.max_modes,
        random_seed=random_seed,
        energy_probe_count=args.energy_probes,
    )
    rank = select_balanced_rank(
        spectrum,
        max_rank=args.max_rank,
        minimum_gap=args.minimum_gap,
        minimum_energy=args.minimum_energy,
    )
    holdout_error = None
    if rank is not None and holdout_rows is not None:
        holdout = passive_delay_observability(
            holdout_rows[selected], selected, carrier_decay=carrier_decay
        )
        holdout_error = randomized_holdout_error(
            holdout,
            reachability,
            spectrum.state_modes[:, :rank],
            probe_count=args.holdout_probes,
            random_seed=random_seed + 2,
        )
    selected_energy = (
        None if rank is None else float(spectrum.energy_fractions[rank - 1])
    )
    selected_gap = None if rank is None else float(spectrum.gap_ratios[rank - 1])
    return {
        "horizon_updates": horizon,
        "cadence": cadence,
        "rank": rank,
        "selected_energy_fraction": selected_energy,
        "selected_gap_ratio": selected_gap,
        "holdout_error": holdout_error,
        "tail_energy_relative_se": spectrum.tail_energy_relative_se,
        "singular_values": spectrum.singular_values,
        "energy_fractions": spectrum.energy_fractions,
        "_modes": spectrum.state_modes,
    }


def evaluate_pair(
    actual: list[dict[str, Any]],
    controls: dict[str, list[dict[str, Any]]],
    *,
    args: argparse.Namespace,
) -> dict[str, Any]:
    reference = actual[0]
    ranks = [row["rank"] for row in actual]
    common_rank = (
        ranks[0] if ranks and all(rank == ranks[0] for rank in ranks) else None
    )
    overlaps: list[float] = []
    if common_rank is not None:
        reference_modes = reference["_modes"][:, :common_rank]
        overlaps = [
            minimum_principal_cosine(reference_modes, row["_modes"][:, :common_rank])
            for row in actual
        ]
    holdouts = [row["holdout_error"] for row in actual]
    pair_pass = bool(
        common_rank is not None
        and common_rank <= args.max_rank
        and min(overlaps, default=0.0) >= args.minimum_cosine
        and all(
            value is not None and value <= args.maximum_holdout_error
            for value in holdouts
        )
        and all(
            row["tail_energy_relative_se"] <= args.maximum_tail_relative_se
            for row in actual
        )
    )

    control_summaries = {}
    for name, rows in controls.items():
        control_ranks = [row["rank"] for row in rows]
        equivalent = False
        control_overlap = 0.0
        actual_overlap = 0.0
        if (
            common_rank is not None
            and len(rows) == 2
            and control_ranks == [common_rank, common_rank]
        ):
            control_overlap = minimum_principal_cosine(
                rows[0]["_modes"][:, :common_rank],
                rows[1]["_modes"][:, :common_rank],
            )
            actual_overlap = minimum_principal_cosine(
                reference["_modes"][:, :common_rank],
                rows[0]["_modes"][:, :common_rank],
            )
            equivalent = bool(
                control_overlap >= args.minimum_cosine
                and actual_overlap >= args.minimum_cosine
            )
        control_summaries[name] = {
            "ranks": control_ranks,
            "segment_cosine": control_overlap,
            "actual_cosine": actual_overlap,
            "equivalent": equivalent,
        }
    geometry_specific = bool(
        pair_pass
        and not control_summaries["flat"]["equivalent"]
        and not control_summaries["shuffled"]["equivalent"]
    )
    return {
        "pass": pair_pass,
        "common_rank": common_rank,
        "minimum_internal_cosine": min(overlaps, default=0.0),
        "maximum_holdout_error": max(
            (value for value in holdouts if value is not None), default=None
        ),
        "maximum_tail_energy_relative_se": max(
            row["tail_energy_relative_se"] for row in actual
        ),
        "controls": control_summaries,
        "geometry_specific": geometry_specific,
    }


def evaluate_ensemble(
    pairs: list[dict[str, Any]], args: argparse.Namespace
) -> dict[str, Any]:
    passing = [pair for pair in pairs if pair["gate"]["pass"]]
    ranks = [pair["gate"]["common_rank"] for pair in passing]
    common_rank = (
        ranks[0] if ranks and all(rank == ranks[0] for rank in ranks) else None
    )
    cross_cosines: list[float] = []
    if common_rank is not None:
        reference = passing[0]["reference_modes"][:, :common_rank]
        cross_cosines = [
            minimum_principal_cosine(
                reference, pair["reference_modes"][:, :common_rank]
            )
            for pair in passing
        ]
    effective = bool(
        len(passing) >= args.required_pairs
        and common_rank is not None
        and min(cross_cosines, default=0.0) >= args.minimum_cosine
    )
    geometry_count = sum(pair["gate"]["geometry_specific"] for pair in pairs)
    geometry_specific = bool(effective and geometry_count >= args.required_pairs)
    descriptive_ranks = [pair["gate"]["common_rank"] for pair in pairs]
    descriptive_rank = (
        descriptive_ranks[0]
        if descriptive_ranks
        and descriptive_ranks[0] is not None
        and all(rank == descriptive_ranks[0] for rank in descriptive_ranks)
        else None
    )
    descriptive_cosines: list[float] = []
    if descriptive_rank is not None:
        reference = pairs[0]["reference_modes"][:, :descriptive_rank]
        descriptive_cosines = [
            minimum_principal_cosine(
                reference, pair["reference_modes"][:, :descriptive_rank]
            )
            for pair in pairs
        ]
    actual_rows = [row for pair in pairs for row in pair["actual"]]
    holdout_values = [
        row["holdout_error"] for row in actual_rows if row["holdout_error"] is not None
    ]
    control_cosines = [
        pair["gate"]["controls"][name]["actual_cosine"]
        for pair in pairs
        for name in ("flat", "shuffled")
    ]
    decision = (
        "geometry-specific-pass"
        if geometry_specific
        else "constitutive-only"
        if effective
        else "fail"
    )
    return {
        "decision": decision,
        "effective_closure": effective,
        "geometry_specific_closure": geometry_specific,
        "passing_pairs": len(passing),
        "geometry_specific_pairs": geometry_count,
        "common_rank": common_rank,
        "minimum_cross_pair_cosine": min(cross_cosines, default=0.0),
        "descriptive_common_rank": descriptive_rank,
        "descriptive_minimum_cross_pair_cosine": min(descriptive_cosines, default=0.0),
        "actual_energy_fraction_range": [
            min(row["selected_energy_fraction"] for row in actual_rows),
            max(row["selected_energy_fraction"] for row in actual_rows),
        ],
        "actual_gap_ratio_range": [
            min(row["selected_gap_ratio"] for row in actual_rows),
            max(row["selected_gap_ratio"] for row in actual_rows),
        ],
        "far_holdout_error_range": [min(holdout_values), max(holdout_values)],
        "minimum_control_actual_cosine": min(control_cosines),
    }


def _without_modes(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "_modes"}


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def write_figure(payload: dict[str, Any], path: Path) -> None:
    figure, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))
    for pair in payload["pairs"]:
        reference = pair["actual"][0]
        singular = np.asarray(reference["singular_values"])
        energy = np.asarray(reference["energy_fractions"])
        label = f"{pair['target_seed']}<-{pair['source_seed']}"
        axes[0].semilogy(
            np.arange(1, singular.size + 1),
            singular / singular[0],
            marker="o",
            label=label,
        )
        axes[1].plot(np.arange(1, energy.size + 1), energy, marker="o", label=label)
    axes[0].set(title="Reference Hankel spectrum", xlabel="mode", ylabel="s / s1")
    axes[1].axhline(0.90, color="black", linestyle="--", linewidth=1)
    axes[1].set(
        title="Full-energy capture",
        xlabel="mode",
        ylabel="cumulative fraction",
        ylim=(0, 1.03),
    )

    labels = [
        f"{pair['target_seed']}<-{pair['source_seed']}" for pair in payload["pairs"]
    ]
    holdout = [
        np.nan
        if pair["gate"]["maximum_holdout_error"] is None
        else pair["gate"]["maximum_holdout_error"]
        for pair in payload["pairs"]
    ]
    axes[2].bar(np.arange(len(labels)), holdout, color="#3b7a78")
    axes[2].axhline(
        payload["thresholds"]["maximum_holdout_error"],
        color="black",
        linestyle="--",
        linewidth=1,
    )
    axes[2].set(
        title="Worst far-probe error",
        ylabel="relative error",
        xticks=np.arange(len(labels)),
        xticklabels=labels,
    )
    axes[2].tick_params(axis="x", rotation=45)
    for axis in axes[:2]:
        axis.grid(alpha=0.25)
    axes[0].legend(fontsize=7)
    figure.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180)
    plt.close(figure)


def write_report(payload: dict[str, Any], path: Path, figure_path: Path) -> None:
    result = payload["decision"]
    lines = [
        "# Balanced full-memory feature gate",
        "",
        f"Date: {payload['generated_utc'][:10]}.",
        "",
        f"**Decision: `{result['decision']}`.**",
        "",
        "This is a balanced reduction test of the passive deposited oriented memory, not an oscillation search.",
        "",
        f"![Balanced full-memory gate]({_relative_from(path, figure_path)})",
        "",
        "## Pair gates",
        "",
        "| target<-source | rank | internal cosine | far error | tail SE | flat equivalent | shuffled equivalent | geometry-specific | pass |",
        "|---|---:|---:|---:|---:|---|---|---|---|",
    ]
    for pair in payload["pairs"]:
        gate = pair["gate"]
        rank = "-" if gate["common_rank"] is None else str(gate["common_rank"])
        holdout = (
            "-"
            if gate["maximum_holdout_error"] is None
            else f"{gate['maximum_holdout_error']:.3g}"
        )
        lines.append(
            f"| {pair['target_seed']}<-{pair['source_seed']} | {rank} | "
            f"{gate['minimum_internal_cosine']:.3f} | {holdout} | "
            f"{gate['maximum_tail_energy_relative_se']:.3g} | "
            f"{gate['controls']['flat']['equivalent']} | "
            f"{gate['controls']['shuffled']['equivalent']} | "
            f"{gate['geometry_specific']} | {gate['pass']} |"
        )
    lines.extend(
        [
            "",
            "## Ensemble",
            "",
            f"- passing pairs: `{result['passing_pairs']}/6`;",
            f"- geometry-specific pairs: `{result['geometry_specific_pairs']}/6`;",
            f"- common rank: `{result['common_rank']}`;",
            f"- minimum cross-pair principal cosine: `{result['minimum_cross_pair_cosine']:.4g}`;",
            f"- descriptive actual-geometry rank across all pairs: `{result['descriptive_common_rank']}`;",
            f"- descriptive minimum cross-pair cosine: `{result['descriptive_minimum_cross_pair_cosine']:.4g}`;",
            f"- actual energy-fraction range: `{result['actual_energy_fraction_range'][0]:.4g}..{result['actual_energy_fraction_range'][1]:.4g}`;",
            f"- actual gap-ratio range: `{result['actual_gap_ratio_range'][0]:.4g}..{result['actual_gap_ratio_range'][1]:.4g}`;",
            f"- far-holdout error range: `{result['far_holdout_error_range'][0]:.4g}..{result['far_holdout_error_range'][1]:.4g}`;",
            f"- minimum actual/control cosine: `{result['minimum_control_actual_cosine']:.4g}`.",
            "",
            "## Interpretation boundary",
            "",
        ]
    )
    if result["decision"] == "fail":
        lines.append(
            "The near readout has a highly reproducible rank-one mode, but the same mode is reproduced by both controls and fails the independent far readout. It is generic exponential delay/readout compression, not a spatially transferable knot mode. Gain, lambda and oscillation optimization remain blocked."
        )
    elif result["decision"] == "constitutive-only":
        lines.append(
            "A low-rank representation is reproducible, but the controls reproduce it. It is delay/readout compression rather than knot-specific mode evidence."
        )
    else:
        lines.append(
            "The geometry-specific closure gate passes. This authorizes a reduced-state metric comparison and time-domain holdout, not yet a nonlinear reciprocal run."
        )
    lines.extend(
        [
            "",
            "Complex values in the earlier eligibility calculation remain algebraic pole classifications under a chosen metric. This report does not call them observed temporal oscillations.",
            "",
            "## Reproducibility",
            "",
            f"- revision: `{payload['git_revision']}`;",
            f"- schema: `{payload['schema']}`;",
            f"- JSON: `{payload['summary_json']}`.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    git_status = _git_output(["status", "--short"])
    if git_status and not args.allow_dirty:
        raise SystemExit(
            "refusing dirty worktree; commit protocol or use --allow-dirty"
        )
    seeds = _parse_ints(args.seeds)
    if len(seeds) != 6 or len(set(seeds)) != 6:
        raise ValueError("the preregistered gate requires six unique seeds")
    horizons_memory = _parse_floats(args.horizons_memory_times)
    cadences = sorted(set(_parse_ints(args.cadences)))
    if horizons_memory != [5.0, 10.0] or cadences != [1, 5, 10]:
        raise ValueError("accepted gate fixes horizons 5,10 and cadences 1,5,10")
    if not 0.0 < args.lambda_vector < 1.0:
        raise ValueError("lambda-vector must lie in (0,1)")
    horizons = [int(round(value / args.lambda_vector)) for value in horizons_memory]
    cases = _discover_cases(args.case_glob or list(DEFAULT_CASE_GLOBS), seeds)
    pairs: list[dict[str, Any]] = []
    for pair_index, (target_seed, source_seed) in enumerate(
        zip(seeds, seeds[1:] + seeds[:1])
    ):
        target_case = cases[target_seed]
        source_case = cases[source_seed]
        if target_case["config"] != source_case["config"]:
            raise ValueError("paired configurations must match")
        source = initialize_oriented_memory_state(
            source_case["state"],
            lambda_vector=args.lambda_vector,
            vector_mass=args.vector_mass,
            orientation_relaxation=args.orientation_relaxation,
        )
        source_radius = float(
            np.sqrt(np.trace(memory_shape_tensor(source.scalar_state)))
        )
        target_radius = float(
            np.sqrt(np.trace(memory_shape_tensor(target_case["state"])))
        )
        pair_radius = 0.5 * (source_radius + target_radius)
        source_center = np.zeros(source.dim)
        source_center[0] = args.distance_ratio * pair_radius
        source = place_oriented_memory_state(source, source_center)
        near_probe = np.zeros(source.dim)
        far_probe = source_center.copy()
        far_probe[0] -= args.far_distance_ratio * pair_radius
        vector_sigma = args.sigma_ratio * source_radius

        actual_rows: list[dict[str, Any]] = []
        control_rows: dict[str, list[dict[str, Any]]] = {"flat": [], "shuffled": []}
        for segment in range(2):
            random_seed = args.noise_seed + pair_index * 100_003 + segment * 1_000_003
            row_sets, source = generate_segment_rows(
                source,
                source_case["config"],
                near_probe=near_probe,
                far_probe=far_probe,
                vector_sigma=vector_sigma,
                n_steps=max(horizons),
                random_seed=random_seed,
            )
            for horizon in horizons:
                for cadence in cadences:
                    row = analyze_readout(
                        row_sets["actual"],
                        holdout_rows=row_sets["far"],
                        horizon=horizon,
                        cadence=cadence,
                        carrier_decay=1.0 - args.orientation_relaxation,
                        deposition_gain=args.orientation_relaxation,
                        args=args,
                        random_seed=random_seed + horizon + cadence,
                    )
                    row["segment"] = segment
                    actual_rows.append(row)
            for name in control_rows:
                row = analyze_readout(
                    row_sets[name],
                    holdout_rows=None,
                    horizon=max(horizons),
                    cadence=min(cadences),
                    carrier_decay=1.0 - args.orientation_relaxation,
                    deposition_gain=args.orientation_relaxation,
                    args=args,
                    random_seed=random_seed + (11 if name == "flat" else 13),
                )
                row["segment"] = segment
                control_rows[name].append(row)

        actual_rows.sort(
            key=lambda row: (
                row["segment"],
                -row["horizon_updates"],
                row["cadence"],
            )
        )
        gate = evaluate_pair(actual_rows, control_rows, args=args)
        reference_modes = actual_rows[0]["_modes"]
        pairs.append(
            {
                "target_seed": target_seed,
                "source_seed": source_seed,
                "target_case": _relative(target_case["path"]),
                "source_case": _relative(source_case["path"]),
                "target_sha256": target_case["sha256"],
                "source_sha256": source_case["sha256"],
                "geometry": {
                    "source_radius": source_radius,
                    "target_radius": target_radius,
                    "pair_radius": pair_radius,
                    "vector_sigma": vector_sigma,
                },
                "actual": [_without_modes(row) for row in actual_rows],
                "controls": {
                    name: [_without_modes(row) for row in rows]
                    for name, rows in control_rows.items()
                },
                "reference_modes": reference_modes,
                "gate": gate,
            }
        )

    decision = evaluate_ensemble(pairs, args)
    for pair in pairs:
        retained_rank = pair["gate"]["common_rank"] or 0
        pair["reference_modes"] = pair["reference_modes"][:, :retained_rank]
    report_path = _resolve(args.report)
    json_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    payload = {
        "schema": "emergenz-knoten.balanced-full-memory-feature-gate.v1",
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "summary_json": _relative(json_path),
        "parameters": {
            "seeds": seeds,
            "lambda_vector": args.lambda_vector,
            "orientation_relaxation": args.orientation_relaxation,
            "vector_mass": args.vector_mass,
            "distance_ratio": args.distance_ratio,
            "far_distance_ratio": args.far_distance_ratio,
            "sigma_ratio": args.sigma_ratio,
            "horizons_memory_times": horizons_memory,
            "cadences": cadences,
            "max_modes": args.max_modes,
        },
        "thresholds": {
            "max_rank": args.max_rank,
            "minimum_gap": args.minimum_gap,
            "minimum_energy": args.minimum_energy,
            "minimum_cosine": args.minimum_cosine,
            "maximum_holdout_error": args.maximum_holdout_error,
            "maximum_tail_relative_se": args.maximum_tail_relative_se,
            "required_pairs": args.required_pairs,
        },
        "pairs": pairs,
        "decision": decision,
    }
    serializable = _jsonable(payload)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(serializable, indent=2) + "\n", encoding="utf-8")
    write_figure(serializable, figure_path)
    write_report(serializable, report_path, figure_path)
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
