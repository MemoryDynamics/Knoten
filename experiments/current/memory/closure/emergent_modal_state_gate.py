"""P3.8e: identify temporal order from canonical finite-k memory responses."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
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
    fit_damped_second_order_recurrence,
    fit_shared_recurrence,
    impulse_hankel_spectrum,
    load_finite_memory_checkpoint,
    paired_finite_k_memory_response,
    paired_uniform_probe_response,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_CASE_GLOB = (
    "data/processed/long_run_metastability/"
    "raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/"
    "case_baseline_seed*.json"
)
DEFAULT_AGE_CHECKPOINT = (
    "data/processed/reference_states/"
    "scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/"
    "scalar_Aatt35_d3_seed1_N100000000.npz"
)


@dataclass(frozen=True)
class CanonicalCase:
    label: str
    seed: int
    update_index: int
    path: Path
    sha256: str
    state: FiniteMemoryState
    config: SimulationConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-glob", default=DEFAULT_CASE_GLOB)
    parser.add_argument("--age-checkpoint", type=Path, default=Path(DEFAULT_AGE_CHECKPOINT))
    parser.add_argument("--seeds", default="1,2,3,4,5")
    parser.add_argument("--kr-values", default="0.5,1,2,4,8")
    parser.add_argument("--dispersion-holdout-kr", type=float, default=2.0)
    parser.add_argument("--perturbation-fractions", default="0.005,0.01")
    parser.add_argument("--memory-times", type=float, default=20.0)
    parser.add_argument("--sample-every", type=int, default=5)
    parser.add_argument("--train-fraction", type=float, default=0.6)
    parser.add_argument("--delay-order", type=int, default=8)
    parser.add_argument("--noise-seed", type=int, default=20_260_813)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/memory/closure/emergent_modal_state_gate_2026-08-13.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/memory/closure/emergent_modal_state_gate_2026-08-13.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/emergent_modal_state_gate_2026-08-13.png"
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


def _jsonable(value: Any) -> Any:
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, np.ndarray):
        return _jsonable(value.tolist())
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if np.isfinite(number) else None
    if isinstance(value, Path):
        return _relative(value)
    if hasattr(value, "__dataclass_fields__"):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _csv_floats(text: str, *, positive: bool = False) -> np.ndarray:
    values = np.asarray(
        [float(item.strip()) for item in text.split(",") if item.strip()],
        dtype=float,
    )
    if values.size < 1 or not np.isfinite(values).all():
        raise ValueError("list must contain finite values")
    if positive and np.any(values <= 0.0):
        raise ValueError("list values must be positive")
    if not np.array_equal(values, np.unique(values)):
        raise ValueError("list values must be unique and increasing")
    return values


def _csv_seeds(text: str) -> list[int]:
    seeds = [int(item.strip()) for item in text.split(",") if item.strip()]
    if not seeds or len(seeds) != len(set(seeds)) or any(seed < 0 for seed in seeds):
        raise ValueError("seeds must be unique non-negative integers")
    return seeds


def _load_snapshot(path: Path) -> CanonicalCase:
    raw = path.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    snapshot = payload["diagnostics"]["memory_cloud"]["snapshot"]
    points = np.asarray(snapshot["points"], dtype=float)
    weights = np.asarray(snapshot["weights"], dtype=float)
    seed = int(payload["seed"])
    update_index = int(payload["config"]["steps"])
    return CanonicalCase(
        label=f"N{update_index}_seed{seed}",
        seed=seed,
        update_index=update_index,
        path=path,
        sha256=hashlib.sha256(raw).hexdigest(),
        state=FiniteMemoryState(x=points[0], memory=points, weights=weights),
        config=SimulationConfig(**payload["config"]),
    )


def _load_checkpoint(path: Path) -> CanonicalCase:
    checkpoint = load_finite_memory_checkpoint(path)
    return CanonicalCase(
        label=f"N{checkpoint.update_index}_seed{checkpoint.formation_seed}",
        seed=checkpoint.formation_seed,
        update_index=checkpoint.update_index,
        path=path,
        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        state=checkpoint.state,
        config=checkpoint.config,
    )


def discover_cases(args: argparse.Namespace) -> tuple[list[CanonicalCase], CanonicalCase]:
    seeds = _csv_seeds(args.seeds)
    paths = [Path(item).resolve() for item in glob.glob(str(_resolve(Path(args.case_glob))))]
    loaded = [_load_snapshot(path) for path in paths]
    cases_by_seed = {case.seed: case for case in loaded}
    missing = sorted(set(seeds) - set(cases_by_seed))
    if missing:
        raise ValueError(f"missing mature snapshot cases for seeds {missing}")
    cases = [cases_by_seed[seed] for seed in seeds]
    age_case = _load_checkpoint(_resolve(args.age_checkpoint))
    if age_case.seed != seeds[0] or age_case.config.dim != cases[0].config.dim:
        raise ValueError("age checkpoint must match the first seed and ambient dimension")
    return cases, age_case


def _sample_steps(config: SimulationConfig, args: argparse.Namespace) -> np.ndarray:
    n_steps = int(round(args.memory_times / config.alpha))
    if n_steps < 20 or args.sample_every < 1:
        raise ValueError("response horizon and sample cadence are too short")
    steps = np.arange(0, n_steps + 1, args.sample_every, dtype=int)
    if steps[-1] != n_steps:
        steps = np.append(steps, n_steps)
    if not np.all(np.diff(steps) == args.sample_every):
        raise ValueError("response horizon must be divisible by sample cadence")
    return steps


def _response_features(response: Any) -> tuple[np.ndarray, np.ndarray]:
    relative = response.position_matrices - response.memory_center_matrices
    longitudinal = np.einsum("tdi,d->ti", relative, response.direction)
    dimensionless_modes = response.memory_radius * response.centered_mode_matrices
    diagonal = np.diagonal(dimensionless_modes, axis1=1, axis2=2)
    features = np.stack(
        (longitudinal, diagonal.real, diagonal.imag),
        axis=2,
    )
    return features, dimensionless_modes


def run_responses(
    cases: list[CanonicalCase],
    age_case: CanonicalCase,
    args: argparse.Namespace,
    kr_values: np.ndarray,
    fractions: np.ndarray,
) -> tuple[dict[tuple[Any, ...], dict[str, Any]], list[dict[str, Any]]]:
    records: dict[tuple[Any, ...], dict[str, Any]] = {}
    case_rows = []
    for case in [*cases, age_case]:
        steps = _sample_steps(case.config, args)
        rng = np.random.default_rng(args.noise_seed + 1009 * case.seed + case.update_index)
        noise = rng.normal(size=(int(steps[-1]), case.config.dim))
        radius = float(
            np.sqrt(
                np.average(
                    np.sum(
                        (
                            case.state.memory
                            - np.average(
                                case.state.memory,
                                axis=0,
                                weights=case.state.weights,
                            )
                        )
                        ** 2,
                        axis=1,
                    ),
                    weights=case.state.weights,
                )
            )
        )
        uniform = paired_uniform_probe_response(
            case.state,
            case.config,
            directions=np.eye(case.config.dim),
            noise=noise[:1],
            sample_steps=[0, 1],
            per_step_strength=float(fractions[0] * radius),
            pulse_steps=1,
        )
        uniform_error = float(
            np.max(np.abs(uniform.position_matrices[-1] - np.eye(case.config.dim)))
        )
        for condition in ("active", "eta_zero"):
            config = case.config if condition == "active" else replace(case.config, eta=0.0)
            for fraction in fractions:
                for axis_index in range(case.config.dim):
                    direction = np.eye(case.config.dim)[axis_index]
                    response = paired_finite_k_memory_response(
                        case.state,
                        config,
                        direction=direction,
                        kr_values=kr_values,
                        perturbation_fraction=float(fraction),
                        noise=noise,
                        sample_steps=steps,
                    )
                    features, modes = _response_features(response)
                    radius_ratio = response.radius_ratios / response.control_radius_ratios[
                        :, None, None
                    ]
                    key = (case.label, condition, float(fraction), axis_index)
                    records[key] = {
                        "features": features,
                        "modes": modes,
                        "sample_steps": response.sample_steps,
                        "radius_max_change": float(np.max(np.abs(radius_ratio - 1.0))),
                        "eta_zero_final_mode": float(np.max(np.abs(modes[-1]))),
                    }
        case_rows.append(
            {
                "label": case.label,
                "seed": case.seed,
                "update_index": case.update_index,
                "path": _relative(case.path),
                "sha256": case.sha256,
                "memory_radius": radius,
                "memory_horizon": case.state.n_memory,
                "sample_steps": steps,
                "uniform_identity_error": uniform_error,
                "config": asdict(case.config),
            }
        )
    return records, case_rows


def _feedback_records(
    records: dict[tuple[Any, ...], dict[str, Any]],
    *,
    case_label: str,
    fraction: float,
    dim: int,
) -> list[dict[str, Any]]:
    rows = []
    for axis in range(dim):
        active = records[(case_label, "active", fraction, axis)]
        control = records[(case_label, "eta_zero", fraction, axis)]
        rows.append(
            {
                "features": active["features"] - control["features"],
                "modes": active["modes"] - control["modes"],
                "sample_steps": active["sample_steps"],
            }
        )
    return rows


def _aggregate_panels(
    records: dict[tuple[Any, ...], dict[str, Any]],
    cases: list[CanonicalCase],
    *,
    fraction: float,
    k_index: int,
) -> np.ndarray:
    panels = []
    for case in cases:
        for row in _feedback_records(
            records,
            case_label=case.label,
            fraction=fraction,
            dim=case.config.dim,
        ):
            panels.append(row["features"][:, k_index, :])
    return np.stack(panels, axis=1)


def analyze_gate(
    records: dict[tuple[Any, ...], dict[str, Any]],
    cases: list[CanonicalCase],
    age_case: CanonicalCase,
    case_rows: list[dict[str, Any]],
    args: argparse.Namespace,
    kr_values: np.ndarray,
    fractions: np.ndarray,
) -> dict[str, Any]:
    primary_fraction = float(fractions[0])
    secondary_fraction = float(fractions[1])
    interval = float(args.sample_every)
    temporal_rows = []
    aggregate_responses = {}
    for k_index, kr in enumerate(kr_values):
        panels = _aggregate_panels(
            records,
            cases,
            fraction=primary_fraction,
            k_index=k_index,
        )
        aggregate_responses[str(float(kr))] = panels
        first = fit_shared_recurrence(
            panels,
            order=1,
            train_fraction=args.train_fraction,
            start_index=2,
        )
        second = fit_shared_recurrence(
            panels,
            order=2,
            train_fraction=args.train_fraction,
            start_index=2,
        )
        delay = fit_shared_recurrence(
            panels,
            order=args.delay_order,
            train_fraction=args.train_fraction,
            start_index=args.delay_order,
        )
        damped = fit_damped_second_order_recurrence(
            panels,
            sample_interval=interval,
            train_fraction=args.train_fraction,
            start_index=2,
        )
        hankel = impulse_hankel_spectrum(
            panels,
            block_rows=30,
            block_columns=30,
            start_index=1,
        )
        second_advantage = second.test_rollout_rmse <= 0.8 * first.test_rollout_rmse
        damped_close = damped.test_rollout_rmse <= 1.1 * second.test_rollout_rmse
        delay_closed = second.test_rollout_rmse <= 1.1 * delay.test_rollout_rmse
        temporal_pass = bool(
            second_advantage
            and damped_close
            and delay_closed
            and second.stable
            and damped.stable
            and damped.underdamped
        )
        temporal_rows.append(
            {
                "kr": float(kr),
                "first_order": first,
                "second_order": second,
                "damped_second_order": damped,
                "delay_order": delay,
                "hankel": hankel,
                "second_order_advantage": second_advantage,
                "damped_close_to_unconstrained": damped_close,
                "second_order_closes_delay": delay_closed,
                "temporal_pass": temporal_pass,
            }
        )

    linearity_errors = []
    active_specificity = []
    diagonal_fractions = []
    for case in cases:
        small = _feedback_records(
            records,
            case_label=case.label,
            fraction=primary_fraction,
            dim=case.config.dim,
        )
        large = _feedback_records(
            records,
            case_label=case.label,
            fraction=secondary_fraction,
            dim=case.config.dim,
        )
        for axis, (small_row, large_row) in enumerate(zip(small, large, strict=True)):
            small_values = small_row["features"]
            large_values = large_row["features"]
            denominator = max(
                float(np.linalg.norm(small_values)),
                float(np.linalg.norm(large_values)),
                np.finfo(float).tiny,
            )
            linearity_errors.append(float(np.linalg.norm(small_values - large_values)) / denominator)
            active = records[(case.label, "active", primary_fraction, axis)]["features"]
            active_specificity.append(
                float(np.linalg.norm(small_values))
                / max(float(np.linalg.norm(active)), np.finfo(float).tiny)
            )
            mode_values = small_row["modes"]
            diagonal = np.zeros_like(mode_values)
            indices = np.arange(kr_values.size)
            diagonal[:, indices, indices] = mode_values[:, indices, indices]
            diagonal_fractions.append(
                float(np.linalg.norm(diagonal))
                / max(float(np.linalg.norm(mode_values)), np.finfo(float).tiny)
            )

    maximum_radius_change = max(
        row["radius_max_change"]
        for key, row in records.items()
        if key[0].startswith("N3000000")
    )
    eta_zero_extinction = max(
        row["eta_zero_final_mode"]
        for key, row in records.items()
        if key[0].startswith("N3000000") and key[1] == "eta_zero"
    )
    uniform_error = max(
        row["uniform_identity_error"]
        for row in case_rows
        if row["update_index"] == cases[0].update_index
    )

    age_rows = []
    for case in (cases[0], age_case):
        for k_index, kr in enumerate(kr_values):
            panels = np.stack(
                [
                    row["features"][:, k_index]
                    for row in _feedback_records(
                        records,
                        case_label=case.label,
                        fraction=primary_fraction,
                        dim=case.config.dim,
                    )
                ],
                axis=1,
            )
            fit = fit_shared_recurrence(
                panels,
                order=2,
                train_fraction=args.train_fraction,
                start_index=2,
            )
            age_rows.append(
                {
                    "case": case.label,
                    "kr": float(kr),
                    "response_norm": float(np.linalg.norm(panels)),
                    "second_order": fit,
                }
            )

    controls = {
        "uniform_identity_max_error": uniform_error,
        "eta_zero_final_dimensionless_mode": eta_zero_extinction,
        "linearity_error_median": float(np.median(linearity_errors)),
        "linearity_error_max": float(np.max(linearity_errors)),
        "active_specificity_median": float(np.median(active_specificity)),
        "active_specificity_min": float(np.min(active_specificity)),
        "cross_wavenumber_diagonal_fraction_median": float(
            np.median(diagonal_fractions)
        ),
        "maximum_radius_ratio_change": maximum_radius_change,
    }
    control_gates = {
        "uniform_pipeline": uniform_error <= 1e-10,
        "eta_zero_extinction": eta_zero_extinction <= 1e-8,
        "paired_linearity": controls["linearity_error_median"] <= 0.1
        and controls["linearity_error_max"] <= 0.25,
        "shape_bounded": maximum_radius_change <= 0.1,
        "feedback_specific_signal": controls["active_specificity_median"] >= 0.05,
    }
    temporal_pass_count = sum(row["temporal_pass"] for row in temporal_rows)
    temporal_gate = temporal_pass_count >= 4
    decision = (
        "second-order-candidate"
        if all(control_gates.values()) and temporal_gate
        else "canonical-null-not-rejected"
    )
    return {
        "controls": controls,
        "control_gates": control_gates,
        "temporal_rows": temporal_rows,
        "temporal_pass_count": temporal_pass_count,
        "temporal_gate": temporal_gate,
        "age_rows": age_rows,
        "linearity_errors": linearity_errors,
        "active_specificity": active_specificity,
        "diagonal_fractions": diagonal_fractions,
        "decision": decision,
        "aggregate_responses": aggregate_responses,
    }


def plot_results(payload: dict[str, Any], path: Path) -> None:
    analysis = payload["analysis"]
    sample_steps = np.asarray(payload["sample_steps"], dtype=float)
    kr_values = np.asarray(payload["registration"]["kr_values"], dtype=float)
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.0))
    colors = plt.cm.viridis(np.linspace(0.08, 0.92, kr_values.size))
    for color, kr in zip(colors, kr_values, strict=True):
        response = np.asarray(analysis["aggregate_responses"][str(float(kr))])
        mean = np.mean(response, axis=1)
        axes[0, 0].plot(sample_steps + 1.0, mean[:, 0], color=color, label=f"kR={kr:g}")
        axes[0, 1].plot(sample_steps + 1.0, mean[:, 1], color=color, label=f"kR={kr:g}")
    axes[0, 0].set_xscale("log")
    axes[0, 1].set_xscale("log")
    axes[0, 0].set_title("Feedback-specific visible readout")
    axes[0, 1].set_title("Feedback-specific centered memory mode")
    axes[0, 0].set_ylabel(r"$\partial[(x-\bar x_\rho)\cdot e]/\partial\delta$")
    axes[0, 1].set_ylabel(r"$R\,\partial\Re\hat\rho_k/\partial\delta$")
    axes[0, 0].legend(fontsize=8, ncol=2)

    labels = ["AR(1)", "AR(2)", "damped AR(2)", f"AR({payload['registration']['delay_order']})"]
    x = np.arange(kr_values.size)
    width = 0.19
    for offset, key, label in zip(
        (-1.5, -0.5, 0.5, 1.5),
        ("first_order", "second_order", "damped_second_order", "delay_order"),
        labels,
        strict=True,
    ):
        ratios = [
            row[key]["test_rollout_rmse"]
            / max(row[key]["test_zero_rmse"], np.finfo(float).tiny)
            for row in analysis["temporal_rows"]
        ]
        axes[1, 0].bar(x + offset * width, ratios, width=width, label=label)
    axes[1, 0].axhline(1.0, color="black", linewidth=1.0, linestyle="--")
    axes[1, 0].set_xticks(x, [f"{value:g}" for value in kr_values])
    axes[1, 0].set_xlabel(r"$kR_{mem}$")
    axes[1, 0].set_ylabel("holdout rollout RMSE / zero")
    axes[1, 0].set_title("Temporal-order holdout")
    axes[1, 0].legend(fontsize=7, ncol=2)

    for color, row in zip(colors, analysis["temporal_rows"], strict=True):
        singular = np.asarray(row["hankel"]["singular_values"], dtype=float)
        axes[1, 1].semilogy(
            np.arange(1, min(12, singular.size) + 1),
            singular[:12] / singular[0],
            "o-",
            color=color,
            label=f"kR={row['kr']:g}",
        )
    axes[1, 1].set_xlabel("Hankel singular-value index")
    axes[1, 1].set_ylabel(r"$s_j/s_1$")
    axes[1, 1].set_title("Nonparametric response rank")
    axes[1, 1].legend(fontsize=8, ncol=2)
    for axis in axes.flat:
        axis.grid(alpha=0.22)
    fig.suptitle(
        "P3.8e canonical finite-k mechanism closure\n"
        f"decision: {analysis['decision']}",
        fontsize=13,
    )
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _pole_text(values: list[dict[str, float]]) -> str:
    return ", ".join(
        f"{item['real']:.3g}{item['imag']:+.3g}i" for item in values
    )


def build_report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    analysis = payload["analysis"]
    controls = analysis["controls"]
    lines = [
        "# P3.8e canonical finite-k mechanism-closure gate",
        "",
        f"Date: {payload['generated_utc'][:10]}.",
        "",
        "## Verdict",
        "",
    ]
    if analysis["decision"] == "second-order-candidate":
        lines.extend(
            [
                "The registered temporal gate passes. This admits a second predictive",
                "state as a candidate for the next storage/passivity and dispersion",
                "tests; it does not yet identify that state with physical momentum.",
            ]
        )
    else:
        lines.extend(
            [
                "The canonical null is not rejected. The feedback-specific finite-`k`",
                "responses do not yet require a stable underdamped second temporal state",
                "on held-out times. P3.8d therefore remains a constructed extension, not",
                "an emergent reduction of the tested scalar `(x,rho)` dynamics.",
            ]
        )
    lines.extend(
        [
            "",
            "## Registered intervention and readout",
            "",
            "For a mature retained path `r_j`, fixed direction `e` and registered",
            "wavenumber `kR_mem`, the paired initial states use",
            "",
            r"\[r_j^{\pm}=r_j\pm\delta\,e\,f_k(r_j),\qquad \sum_jw_jf_k(r_j)=0,\qquad f_k(r_0)=0.\]",
            "",
            "Thus mass, memory weights, visible state `x=r_0`, and the weighted memory",
            "centroid are unchanged at intervention. The branches then follow the",
            "unchanged canonical simulator with common random numbers. The fixed",
            "projection contains `(x-xbar_rho).e` and the real and imaginary parts of",
            "the centered scalar-memory Fourier coefficient at the same `k`. No target",
            "frequency, P3.8d pole, inertia, or cross-node law enters the experiment.",
            "",
            "The primary response is `active - eta_zero`. Five `kR_mem` values are",
            "measured; `kR=2` is withheld from any later dispersion fit. The two paired",
            "strengths test central-difference linearity. `k=0` remains only the uniform",
            "identity-pipeline control.",
            "",
            "## Controls",
            "",
            "| diagnostic | value | registered gate | pass |",
            "|---|---:|---:|:---:|",
            f"| uniform immediate identity error | {controls['uniform_identity_max_error']:.3e} | <=1e-10 | {'yes' if analysis['control_gates']['uniform_pipeline'] else 'no'} |",
            f"| eta-zero final modal response | {controls['eta_zero_final_dimensionless_mode']:.3e} | <=1e-8 | {'yes' if analysis['control_gates']['eta_zero_extinction'] else 'no'} |",
            f"| strength-linearity error, median / max | {controls['linearity_error_median']:.3f} / {controls['linearity_error_max']:.3f} | <=0.10 / <=0.25 | {'yes' if analysis['control_gates']['paired_linearity'] else 'no'} |",
            f"| feedback-specific norm / active norm, median | {controls['active_specificity_median']:.3f} | >=0.05 | {'yes' if analysis['control_gates']['feedback_specific_signal'] else 'no'} |",
            f"| maximum branch radius-ratio change | {controls['maximum_radius_ratio_change']:.3f} | <=0.10 | {'yes' if analysis['control_gates']['shape_bounded'] else 'no'} |",
            f"| cross-k diagonal response fraction, median | {controls['cross_wavenumber_diagonal_fraction_median']:.3f} | diagnostic | -- |",
            "",
            "## Temporal-order holdout",
            "",
            "Every recurrence is fitted to the same standardized panel of five formation",
            "seeds, three fixed coordinate directions and three predeclared readouts.",
            "The score below is recursive chronological holdout RMSE divided by the",
            "zero-response null; it is not a teacher-forced one-step score.",
            "",
            "| kR | AR(1) | AR(2) | damped AR(2) | delay | AR(2) poles | gate |",
            "|---:|---:|---:|---:|---:|---|:---:|",
        ]
    )
    for row in analysis["temporal_rows"]:
        ratios = []
        for key in ("first_order", "second_order", "damped_second_order", "delay_order"):
            fit = row[key]
            ratios.append(
                fit["test_rollout_rmse"]
                / max(fit["test_zero_rmse"], np.finfo(float).tiny)
            )
        lines.append(
            f"| {row['kr']:g} | {ratios[0]:.3f} | {ratios[1]:.3f} | "
            f"{ratios[2]:.3f} | {ratios[3]:.3f} | "
            f"{_pole_text(row['second_order']['poles'])} | "
            f"{'pass' if row['temporal_pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            f"Temporal channels passing all necessary conditions: **{analysis['temporal_pass_count']}/5**; registered requirement: at least 4/5.",
            "",
            "The damped AR(2) restriction is only a necessary temporal condition for a",
            "passive reciprocal realization. A positive storage metric and collocated",
            "power-conjugate write/read ports would still have to be established after",
            "a temporal pass.",
            "",
            "## Formation-age check",
            "",
            "The same seed is evaluated at `N=3e6` and `N=1e8`. These rows are an",
            "age-stationarity diagnostic, not independent seed replication.",
            "",
            "| case | kR | response norm | AR(2) rollout / zero | poles |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for row in analysis["age_rows"]:
        fit = row["second_order"]
        lines.append(
            f"| {row['case']} | {row['kr']:g} | {row['response_norm']:.3e} | "
            f"{fit['test_rollout_rmse'] / max(fit['test_zero_rmse'], np.finfo(float).tiny):.3f} | "
            f"{_pole_text(fit['poles'])} |"
        )
    lines.extend(
        [
            "",
            "## Figure",
            "",
            f"![P3.8e finite-k mechanism closure]({_relative_from(report, figure)})",
            "",
            "## Interpretation boundary",
            "",
            "- **Evidence:** paired responses, exact passive-memory extinction, strength",
            "  linearity, recursive holdout errors and Hankel spectra from the canonical",
            "  scalar simulator.",
            "- **Inference allowed only after a pass:** a second predictive effective",
            "  state may be useful up to similarity transformation.",
            "- **Not established here:** microscopic momentum, an `(m,p)` field, a",
            "  cross-node mediator, passivity, quantization, spin, particle identity or",
            "  dimension selection.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{payload['git_revision']}`.",
            f"- Git status at execution: `{payload['git_status'] or 'clean'}`.",
            f"- Command: `{payload['command']}`.",
            f"- Machine-readable summary: [{Path(payload['summary_json']).name}]({_relative_from(report, _resolve(Path(payload['summary_json'])))})",
            "- Source checkpoints and SHA-256 digests are recorded in the JSON summary.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    git_status = _git_output(["status", "--porcelain"])
    if git_status not in ("", "unavailable") and not args.allow_dirty:
        raise RuntimeError("refusing to run on a dirty worktree; use --allow-dirty explicitly")
    kr_values = _csv_floats(args.kr_values, positive=True)
    fractions = _csv_floats(args.perturbation_fractions, positive=True)
    if fractions.size != 2:
        raise ValueError("exactly two perturbation fractions are registered")
    if args.dispersion_holdout_kr not in kr_values:
        raise ValueError("dispersion holdout must be one of the registered kr values")
    cases, age_case = discover_cases(args)
    records, case_rows = run_responses(
        cases,
        age_case,
        args,
        kr_values,
        fractions,
    )
    analysis = analyze_gate(
        records,
        cases,
        age_case,
        case_rows,
        args,
        kr_values,
        fractions,
    )
    sample_steps = records[
        (cases[0].label, "active", float(fractions[0]), 0)
    ]["sample_steps"]
    payload = {
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": git_status,
        "command": "python experiments/current/memory/closure/emergent_modal_state_gate.py",
        "registration": {
            "kr_values": kr_values,
            "dispersion_holdout_kr": args.dispersion_holdout_kr,
            "perturbation_fractions": fractions,
            "memory_times": args.memory_times,
            "sample_every": args.sample_every,
            "train_fraction": args.train_fraction,
            "delay_order": args.delay_order,
            "noise_seed": args.noise_seed,
            "primary_null": (
                "canonical responses do not require a stable reversible "
                "second-order modal realization"
            ),
        },
        "sample_steps": sample_steps,
        "cases": case_rows,
        "analysis": analysis,
        "summary_json": _relative(args.summary_json),
    }
    serializable = _jsonable(payload)
    figure = _resolve(args.figure)
    summary = _resolve(args.summary_json)
    report = _resolve(args.report)
    plot_results(serializable, figure)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(serializable, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(build_report(serializable, report, figure), encoding="utf-8")
    print(json.dumps({"decision": analysis["decision"], "report": _relative(report)}, indent=2))


if __name__ == "__main__":
    main()
