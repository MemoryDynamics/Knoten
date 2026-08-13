"""Reconcile P3.8e after auditing temporal-model and holdout semantics."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
import glob
import hashlib
import json
import math
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
    fit_conservative_recurrence_with_held_out_readout,
    fit_conservative_second_order_recurrence,
    fit_recurrence_with_held_out_readout,
    fit_shared_recurrence,
    impulse_hankel_spectrum,
    interpret_continuous_second_order,
    load_finite_memory_checkpoint,
    longitudinal_memory_mode_profiles,
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
    parser.add_argument("--perturbation-fractions", default="0.005,0.01")
    parser.add_argument("--analysis-updates", type=int, default=600)
    parser.add_argument("--extinction-updates", type=int, default=800)
    parser.add_argument("--sample-every", type=int, default=5)
    parser.add_argument("--train-fraction", type=float, default=0.6)
    parser.add_argument("--common-start-index", type=int, default=8)
    parser.add_argument("--delay-order", type=int, default=8)
    parser.add_argument("--noise-seed", type=int, default=20_260_813)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/memory/closure/"
            "emergent_modal_state_reconciliation_2026-08-13.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/memory/closure/"
            "emergent_modal_state_reconciliation_2026-08-13.json"
        ),
    )
    parser.add_argument(
        "--responses-npz",
        type=Path,
        default=Path(
            "reports/memory/closure/"
            "emergent_modal_state_reconciliation_2026-08-13.responses.npz"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/"
            "emergent_modal_state_reconciliation_2026-08-13.png"
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
    if isinstance(value, (float, np.floating)):
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


def _csv_floats(text: str) -> np.ndarray:
    values = np.asarray(
        [float(item.strip()) for item in text.split(",") if item.strip()],
        dtype=float,
    )
    if (
        values.size < 1
        or not np.isfinite(values).all()
        or np.any(values <= 0.0)
        or not np.array_equal(values, np.unique(values))
    ):
        raise ValueError("values must be unique increasing positive numbers")
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
    paths = sorted(Path(path).resolve() for path in glob.glob(str(_resolve(Path(args.case_glob)))))
    loaded = [_load_snapshot(path) for path in paths]
    by_seed: dict[int, CanonicalCase] = {}
    for case in loaded:
        if case.seed in by_seed:
            raise ValueError(f"multiple mature snapshots found for seed {case.seed}")
        by_seed[case.seed] = case
    missing = sorted(set(seeds) - set(by_seed))
    if missing:
        raise ValueError(f"missing mature snapshots for seeds {missing}")
    cases = [by_seed[seed] for seed in seeds]
    if len({case.update_index for case in cases}) != 1:
        raise ValueError("mature snapshots must share one formation age")
    reference_config = asdict(cases[0].config)
    for ignored in ("steps", "burn_in", "sample_every"):
        reference_config.pop(ignored)
    for case in cases[1:]:
        candidate = asdict(case.config)
        for ignored in ("steps", "burn_in", "sample_every"):
            candidate.pop(ignored)
        if candidate != reference_config:
            raise ValueError("mature snapshots must share one dynamical configuration")
    age_case = _load_checkpoint(_resolve(args.age_checkpoint))
    if age_case.seed != seeds[0] or age_case.config.dim != cases[0].config.dim:
        raise ValueError("age checkpoint must match first formation seed and dimension")
    age_config = asdict(age_case.config)
    for ignored in ("steps", "burn_in", "sample_every"):
        age_config.pop(ignored)
    if age_config != reference_config:
        raise ValueError("age checkpoint must share the registered dynamics")
    return cases, age_case


def response_features(response: Any) -> np.ndarray:
    """Return visible holdout followed by two memory-only fit readouts."""

    relative = response.position_matrices - response.memory_center_matrices
    visible = np.einsum("tdi,d->ti", relative, response.direction)
    modes = response.memory_radius * response.centered_mode_matrices
    diagonal = np.diagonal(modes, axis1=1, axis2=2)
    return np.stack((visible, diagonal.real, diagonal.imag), axis=2)


def response_modes(response: Any) -> np.ndarray:
    """Return the complete dimensionless cross-wavenumber memory response."""

    return response.memory_radius * response.centered_mode_matrices


def mode_profile_gram(
    state: FiniteMemoryState,
    direction: np.ndarray,
    kr_values: np.ndarray,
) -> np.ndarray:
    profiles, _, _ = longitudinal_memory_mode_profiles(
        state,
        direction=direction,
        kr_values=kr_values,
    )
    return (profiles * state.weights[None, :]) @ profiles.T / np.sum(state.weights)


def run_responses(
    cases: list[CanonicalCase],
    age_case: CanonicalCase,
    args: argparse.Namespace,
    kr_values: np.ndarray,
    fractions: np.ndarray,
) -> tuple[dict[tuple[str, str, float, int], dict[str, Any]], list[dict[str, Any]]]:
    if args.extinction_updates < args.analysis_updates:
        raise ValueError("extinction horizon must not precede analysis horizon")
    if (
        args.analysis_updates % args.sample_every
        or args.extinction_updates % args.sample_every
    ):
        raise ValueError("analysis and extinction horizons must match sample cadence")
    sample_steps = np.arange(
        0,
        args.extinction_updates + 1,
        args.sample_every,
        dtype=int,
    )
    records: dict[tuple[str, str, float, int], dict[str, Any]] = {}
    case_rows = []
    for case in [*cases, age_case]:
        rng = np.random.default_rng(args.noise_seed + 1009 * case.seed)
        noise = rng.normal(size=(args.extinction_updates, case.config.dim))
        grams = np.stack(
            [
                mode_profile_gram(case.state, direction, kr_values)
                for direction in np.eye(case.config.dim)
            ]
        )
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
                for axis, direction in enumerate(np.eye(case.config.dim)):
                    response = paired_finite_k_memory_response(
                        case.state,
                        config,
                        direction=direction,
                        kr_values=kr_values,
                        perturbation_fraction=float(fraction),
                        noise=noise,
                        sample_steps=sample_steps,
                    )
                    modes = response_modes(response)
                    radius_ratio = response.radius_ratios / response.control_radius_ratios[
                        :, None, None
                    ]
                    records[(case.label, condition, float(fraction), axis)] = {
                        "features": response_features(response),
                        "modes": modes,
                        "radius_max_change": float(np.max(np.abs(radius_ratio - 1.0))),
                    }
        case_rows.append(
            {
                "label": case.label,
                "seed": case.seed,
                "update_index": case.update_index,
                "path": _relative(case.path),
                "sha256": case.sha256,
                "config": asdict(case.config),
                "memory_radius": radius,
                "memory_horizon": case.state.n_memory,
                "uniform_identity_error": uniform_error,
                "profile_grams": grams,
                "profile_conditions": np.asarray(
                    [np.linalg.cond(gram) for gram in grams]
                ),
            }
        )
    return records, case_rows


def response_panel(
    records: dict[tuple[str, str, float, int], dict[str, Any]],
    cases: list[CanonicalCase],
    *,
    condition: str,
    fraction: float,
) -> np.ndarray:
    panels = []
    for case in cases:
        for axis in range(case.config.dim):
            panels.append(records[(case.label, condition, fraction, axis)]["features"])
    return np.stack(panels, axis=1)


def _ratio(numerator: float, denominator: float) -> float:
    return float(numerator / max(denominator, np.finfo(float).tiny))


def _rank_two_diagnostics(spectrum: Any) -> dict[str, float | bool]:
    singular = np.asarray(spectrum.singular_values, dtype=float)
    energy = float(np.sum(singular[:2] ** 2) / np.sum(singular**2))
    if singular.size <= 2 or singular[1] <= np.finfo(float).eps * singular[0]:
        gap = 0.0
    else:
        gap = float(singular[2] / singular[1])
    return {
        "rank_two_energy": energy,
        "third_to_second_ratio": gap,
        "rank_two_pass": bool(energy >= 0.9 and gap <= 0.5),
    }


def _fit_active_models(
    values: np.ndarray,
    args: argparse.Namespace,
) -> dict[str, Any]:
    memory = values[:, :, 1:]
    visible = values[:, :, :1]
    shared = {
        str(order): fit_recurrence_with_held_out_readout(
            memory,
            visible,
            order=order,
            train_fraction=args.train_fraction,
            start_index=args.common_start_index,
        )
        for order in (1, 2, args.delay_order)
    }
    conservative = fit_conservative_recurrence_with_held_out_readout(
        memory,
        visible,
        train_fraction=args.train_fraction,
        start_index=args.common_start_index,
    )
    interpretation = interpret_continuous_second_order(
        shared["2"].coefficients,
        sample_interval=float(args.sample_every),
    )
    spectrum = impulse_hankel_spectrum(
        memory,
        block_rows=30,
        block_columns=30,
        start_index=1,
    )
    return {
        "models": shared,
        "conservative": conservative,
        "continuous_interpretation": interpretation,
        "hankel": spectrum,
        **_rank_two_diagnostics(spectrum),
    }


def _fit_control_models(values: np.ndarray, args: argparse.Namespace) -> dict[str, Any]:
    memory = values[:, :, 1:]
    shared = {
        str(order): fit_shared_recurrence(
            memory,
            order=order,
            train_fraction=args.train_fraction,
            start_index=args.common_start_index,
        )
        for order in (1, 2, args.delay_order)
    }
    conservative = fit_conservative_second_order_recurrence(
        memory,
        sample_interval=float(args.sample_every),
        train_fraction=args.train_fraction,
        start_index=args.common_start_index,
    )
    return {"models": shared, "conservative": conservative}


def _seed_rows(
    records: dict[tuple[str, str, float, int], dict[str, Any]],
    cases: list[CanonicalCase],
    *,
    fraction: float,
    k_index: int,
    analysis_mask: np.ndarray,
    sample_steps: np.ndarray,
    args: argparse.Namespace,
) -> list[dict[str, Any]]:
    rows = []
    for case in cases:
        values = np.stack(
            [
                records[(case.label, "active", fraction, axis)]["features"]
                for axis in range(case.config.dim)
            ],
            axis=1,
        )[analysis_mask, :, k_index]
        fits = _fit_active_models(values, args)
        first = fits["models"]["1"]
        second = fits["models"]["2"]
        delay = fits["models"][str(args.delay_order)]
        interpretation = fits["continuous_interpretation"]
        memory_signal = _balanced_signal_diagnostics(
            values[:, :, 1:], sample_steps, args
        )
        visible_signal = _balanced_signal_diagnostics(
            values[:, :, :1], sample_steps, args
        )
        fit_advantage = second.fit_test_rollout_rmse <= 0.8 * first.fit_test_rollout_rmse
        readout_advantage = (
            second.readout_test_rollout_rmse
            <= 0.8 * first.readout_test_rollout_rmse
        )
        passed = bool(
            fit_advantage
            and readout_advantage
            and second.fit_test_rollout_rmse <= 1.1 * delay.fit_test_rollout_rmse
            and second.readout_test_rollout_rmse
            <= 1.1 * delay.readout_test_rollout_rmse
            and second.stable
            and interpretation.underdamped
            and fits["rank_two_pass"]
            and memory_signal["pass"]
            and visible_signal["pass"]
        )
        rows.append(
            {
                "seed": case.seed,
                "first_order": first,
                "second_order": second,
                "continuous_interpretation": interpretation,
                "fit_advantage": fit_advantage,
                "readout_advantage": readout_advantage,
                "memory_signal": memory_signal,
                "visible_signal": visible_signal,
                "pass": passed,
            }
        )
    return rows


def _balanced_signal_diagnostics(
    values: np.ndarray,
    sample_steps: np.ndarray,
    args: argparse.Namespace,
) -> dict[str, float | int | bool]:
    """Check that a scale-balanced response remains measurable on holdout."""

    training_end = int(math.floor(args.train_fraction * (values.shape[0] - 1)))
    training = values[: training_end + 1]
    scales = np.sqrt(np.mean(training * training, axis=0))
    maximum = float(np.max(scales))
    floor = max(
        1e-6 * maximum,
        np.finfo(float).eps * max(1.0, float(np.max(np.abs(training)))),
    )
    active = scales > floor
    if not np.any(active):
        return {
            "support_updates": 0,
            "holdout_start_update": int(sample_steps[training_end + 1]),
            "holdout_energy_fraction": 0.0,
            "pass": False,
        }
    flattened = values.reshape(values.shape[0], -1)[:, active.reshape(-1)]
    standardized = flattened / scales.reshape(-1)[active.reshape(-1)][None, :]
    envelope = np.sqrt(np.mean(standardized * standardized, axis=1))
    threshold = 0.01 * float(np.max(envelope))
    indices = np.flatnonzero(envelope >= threshold)
    support = int(sample_steps[indices[-1]]) if indices.size else 0
    holdout_start = training_end + 1
    total_energy = float(
        np.sum(standardized[args.common_start_index :] ** 2)
    )
    holdout_energy = float(np.sum(standardized[holdout_start:] ** 2))
    fraction = holdout_energy / max(total_energy, np.finfo(float).tiny)
    return {
        "support_updates": support,
        "holdout_start_update": int(sample_steps[holdout_start]),
        "holdout_energy_fraction": fraction,
        "pass": bool(
            support >= int(sample_steps[holdout_start]) and fraction >= 0.05
        ),
    }


def analyze(
    records: dict[tuple[str, str, float, int], dict[str, Any]],
    cases: list[CanonicalCase],
    age_case: CanonicalCase,
    case_rows: list[dict[str, Any]],
    args: argparse.Namespace,
    kr_values: np.ndarray,
    fractions: np.ndarray,
) -> dict[str, Any]:
    sample_steps = np.arange(0, args.extinction_updates + 1, args.sample_every)
    analysis_mask = sample_steps <= args.analysis_updates
    primary = float(fractions[0])
    active = response_panel(records, cases, condition="active", fraction=primary)
    control = response_panel(records, cases, condition="eta_zero", fraction=primary)
    rows = []
    for k_index, kr in enumerate(kr_values):
        active_values = active[analysis_mask, :, k_index]
        control_values = control[analysis_mask, :, k_index]
        active_fit = _fit_active_models(active_values, args)
        control_fit = _fit_control_models(control_values, args)
        first = active_fit["models"]["1"]
        second = active_fit["models"]["2"]
        delay = active_fit["models"][str(args.delay_order)]
        control_first = control_fit["models"]["1"]
        control_second = control_fit["models"]["2"]
        interpretation = active_fit["continuous_interpretation"]
        memory_signal = _balanced_signal_diagnostics(
            active_values[:, :, 1:], sample_steps[analysis_mask], args
        )
        visible_signal = _balanced_signal_diagnostics(
            active_values[:, :, :1], sample_steps[analysis_mask], args
        )
        seed_rows = _seed_rows(
            records,
            cases,
            fraction=primary,
            k_index=k_index,
            analysis_mask=analysis_mask,
            sample_steps=sample_steps[analysis_mask],
            args=args,
        )
        seed_passes = sum(row["pass"] for row in seed_rows)
        gates = {
            "memory_ar2_advantage": (
                second.fit_test_rollout_rmse <= 0.8 * first.fit_test_rollout_rmse
            ),
            "heldout_visible_ar2_advantage": (
                second.readout_test_rollout_rmse
                <= 0.8 * first.readout_test_rollout_rmse
            ),
            "closes_delay_memory": (
                second.fit_test_rollout_rmse <= 1.1 * delay.fit_test_rollout_rmse
            ),
            "closes_delay_visible": (
                second.readout_test_rollout_rmse
                <= 1.1 * delay.readout_test_rollout_rmse
            ),
            "stable_underdamped": bool(
                second.stable and interpretation.embeddable and interpretation.underdamped
            ),
            "rank_two_hankel": bool(active_fit["rank_two_pass"]),
            "memory_signal_in_holdout": bool(memory_signal["pass"]),
            "visible_signal_in_holdout": bool(visible_signal["pass"]),
            "seed_reproducibility": seed_passes >= 4,
        }
        rows.append(
            {
                "kr": float(kr),
                "active": active_fit,
                "eta_zero": control_fit,
                "seed_rows": seed_rows,
                "seed_passes": seed_passes,
                "memory_signal": memory_signal,
                "visible_signal": visible_signal,
                "eta_zero_ar2_over_ar1": _ratio(
                    control_second.test_rollout_rmse,
                    control_first.test_rollout_rmse,
                ),
                "gates": gates,
                "pass": all(gates.values()),
            }
        )

    linearity = {"active": [], "eta_zero": []}
    mode_linearity = {"active": [], "eta_zero": []}
    radius_changes = []
    for case in cases:
        for condition in ("active", "eta_zero"):
            for axis in range(case.config.dim):
                small = records[(case.label, condition, float(fractions[0]), axis)]
                large = records[(case.label, condition, float(fractions[1]), axis)]
                denominator = max(
                    float(np.linalg.norm(small["features"])),
                    float(np.linalg.norm(large["features"])),
                    np.finfo(float).tiny,
                )
                linearity[condition].append(
                    float(np.linalg.norm(small["features"] - large["features"]))
                    / denominator
                )
                mode_denominator = max(
                    float(np.linalg.norm(small["modes"])),
                    float(np.linalg.norm(large["modes"])),
                    np.finfo(float).tiny,
                )
                mode_linearity[condition].append(
                    float(np.linalg.norm(small["modes"] - large["modes"]))
                    / mode_denominator
                )
                radius_changes.extend(
                    [small["radius_max_change"], large["radius_max_change"]]
                )

    grams = np.concatenate(
        [row["profile_grams"] for row in case_rows if row["update_index"] == cases[0].update_index],
        axis=0,
    )
    conditions = np.asarray(
        [value for row in case_rows if row["update_index"] == cases[0].update_index for value in row["profile_conditions"]]
    )
    off_diagonal = grams - np.eye(kr_values.size)[None, :, :]
    spatial_input = {
        "median_gram": np.median(grams, axis=0),
        "condition_min": float(np.min(conditions)),
        "condition_median": float(np.median(conditions)),
        "condition_max": float(np.max(conditions)),
        "max_abs_off_diagonal": float(np.max(np.abs(off_diagonal))),
        "independent_mode_gate": bool(
            np.median(conditions) <= 100.0
            and np.max(np.abs(off_diagonal)) <= 0.95
        ),
    }

    cross_mode_fractions = {"active": [], "feedback_difference": []}
    diagonal_indices = np.arange(kr_values.size)
    for case in cases:
        for axis in range(case.config.dim):
            active_modes = records[(case.label, "active", primary, axis)]["modes"]
            control_modes = records[(case.label, "eta_zero", primary, axis)]["modes"]
            for name, mode_values in (
                ("active", active_modes),
                ("feedback_difference", active_modes - control_modes),
            ):
                diagonal = np.zeros_like(mode_values)
                diagonal[:, diagonal_indices, diagonal_indices] = mode_values[
                    :, diagonal_indices, diagonal_indices
                ]
                cross_mode_fractions[name].append(
                    _ratio(float(np.linalg.norm(diagonal)), float(np.linalg.norm(mode_values)))
                )

    eta_final = []
    for case in cases:
        for axis in range(case.config.dim):
            eta_final.append(
                np.max(
                    np.abs(
                        records[(case.label, "eta_zero", primary, axis)]["features"][-1]
                    )
                )
            )
    controls = {
        "uniform_identity_error": max(
            row["uniform_identity_error"]
            for row in case_rows
            if row["update_index"] == cases[0].update_index
        ),
        "eta_zero_extinction": float(np.max(eta_final)),
        "active_linearity_median": float(np.median(linearity["active"])),
        "active_linearity_max": float(np.max(linearity["active"])),
        "active_full_mode_linearity_median": float(
            np.median(mode_linearity["active"])
        ),
        "active_full_mode_linearity_max": float(np.max(mode_linearity["active"])),
        "eta_zero_linearity_median": float(np.median(linearity["eta_zero"])),
        "eta_zero_linearity_max": float(np.max(linearity["eta_zero"])),
        "eta_zero_full_mode_linearity_median": float(
            np.median(mode_linearity["eta_zero"])
        ),
        "eta_zero_full_mode_linearity_max": float(
            np.max(mode_linearity["eta_zero"])
        ),
        "active_cross_k_diagonal_fraction_median": float(
            np.median(cross_mode_fractions["active"])
        ),
        "feedback_cross_k_diagonal_fraction_median": float(
            np.median(cross_mode_fractions["feedback_difference"])
        ),
        "radius_change_max": float(np.max(radius_changes)),
    }
    control_gates = {
        "uniform_identity": controls["uniform_identity_error"] <= 1e-10,
        "eta_zero_extinction": controls["eta_zero_extinction"] <= 1e-8,
        "active_linearity": controls["active_linearity_median"] <= 0.1
        and controls["active_linearity_max"] <= 0.25
        and controls["active_full_mode_linearity_median"] <= 0.1
        and controls["active_full_mode_linearity_max"] <= 0.25,
        "eta_zero_linearity": controls["eta_zero_linearity_median"] <= 0.1
        and controls["eta_zero_linearity_max"] <= 0.25
        and controls["eta_zero_full_mode_linearity_median"] <= 0.1
        and controls["eta_zero_full_mode_linearity_max"] <= 0.25,
        "shape_bounded": controls["radius_change_max"] <= 0.1,
    }

    age_rows = []
    for case in (cases[0], age_case):
        values = response_panel(
            records,
            [case],
            condition="active",
            fraction=primary,
        )[analysis_mask]
        for k_index, kr in enumerate(kr_values):
            fit = _fit_active_models(values[:, :, k_index], args)
            age_rows.append(
                {
                    "case": case.label,
                    "kr": float(kr),
                    "second_order": fit["models"]["2"],
                    "continuous_interpretation": fit["continuous_interpretation"],
                    "response_norm": float(np.linalg.norm(values[:, :, k_index])),
                }
            )
    age_comparisons = []
    for k_index, kr in enumerate(kr_values):
        pair = [row for row in age_rows if row["kr"] == float(kr)]
        first_poles = np.sort_complex(np.asarray(pair[0]["second_order"].poles))
        second_poles = np.sort_complex(np.asarray(pair[1]["second_order"].poles))
        formation_rows = []
        for case in cases:
            values = response_panel(
                records,
                [case],
                condition="active",
                fraction=primary,
            )[analysis_mask, :, k_index]
            fit = _fit_active_models(values, args)["models"]["2"]
            formation_rows.append(
                {
                    "seed": case.seed,
                    "poles": np.sort_complex(np.asarray(fit.poles)),
                    "response_norm": float(np.linalg.norm(values)),
                }
            )
        reference = formation_rows[0]
        seed_pole_distances = [
            float(np.max(np.abs(row["poles"] - reference["poles"])))
            for row in formation_rows[1:]
        ]
        seed_norm_ratios = [
            _ratio(row["response_norm"], reference["response_norm"])
            for row in formation_rows
        ]
        pole_distance = float(np.max(np.abs(first_poles - second_poles)))
        norm_ratio = _ratio(pair[1]["response_norm"], pair[0]["response_norm"])
        pole_within_seed_spread = pole_distance <= max(seed_pole_distances) + 1e-12
        norm_within_seed_spread = (
            min(seed_norm_ratios) <= norm_ratio <= max(seed_norm_ratios)
        )
        age_comparisons.append(
            {
                "kr": float(kr),
                "pole_distance": pole_distance,
                "max_formation_seed_pole_distance": max(seed_pole_distances),
                "response_norm_ratio": norm_ratio,
                "formation_seed_norm_ratio_min": min(seed_norm_ratios),
                "formation_seed_norm_ratio_max": max(seed_norm_ratios),
                "pole_within_seed_spread": pole_within_seed_spread,
                "norm_within_seed_spread": norm_within_seed_spread,
                "pass": bool(pole_within_seed_spread and norm_within_seed_spread),
            }
        )

    temporal_passes = sum(row["pass"] for row in rows)
    controls_pass = all(control_gates.values())
    temporal_candidate = controls_pass and temporal_passes >= 4
    age_passes = sum(row["pass"] for row in age_comparisons)
    age_reconciliation = age_passes >= 4
    if not temporal_candidate:
        decision = "second-order-not-selected"
    elif not age_reconciliation and not spatial_input["independent_mode_gate"]:
        decision = "second-order-candidate-age-and-spatial-unresolved"
    elif not age_reconciliation:
        decision = "second-order-candidate-age-unresolved"
    elif not spatial_input["independent_mode_gate"]:
        decision = "second-order-candidate-spatial-modes-unresolved"
    else:
        decision = "second-order-candidate"
    return {
        "rows": rows,
        "controls": controls,
        "control_gates": control_gates,
        "spatial_input": spatial_input,
        "age_rows": age_rows,
        "age_comparisons": age_comparisons,
        "age_passes": age_passes,
        "age_reconciliation": age_reconciliation,
        "temporal_passes": temporal_passes,
        "temporal_candidate": temporal_candidate,
        "decision": decision,
        "historical_p38e_status": "superseded-methodologically-inconclusive",
        "review_findings_addressed": {
            "damped_ar2_redundancy": True,
            "active_and_eta_zero_fitted_separately": True,
            "common_target_windows": True,
            "signal_bearing_holdout": True,
            "visible_readout_withheld_from_fit": True,
            "hankel_rank_is_a_gate": True,
            "common_noise_for_age_pair": True,
            "age_shift_compared_with_seed_spread": True,
            "seed_level_reproducibility": True,
            "input_profile_gram_gate": True,
            "cross_wavenumber_leakage_retained": True,
            "canonical_trajectory_write_port": False,
        },
    }


def write_archive(
    records: dict[tuple[str, str, float, int], dict[str, Any]],
    case_rows: list[dict[str, Any]],
    path: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    arrays: dict[str, np.ndarray] = {
        "sample_steps": np.arange(
            0,
            args.extinction_updates + 1,
            args.sample_every,
            dtype=np.int64,
        ),
        "kr_values": _csv_floats(args.kr_values),
        "perturbation_fractions": _csv_floats(args.perturbation_fractions),
    }
    keys = {}
    for index, (record_key, record) in enumerate(sorted(records.items())):
        name = f"features_{index}"
        mode_name = f"modes_{index}"
        arrays[name] = np.asarray(record["features"], dtype=float)
        arrays[mode_name] = np.asarray(record["modes"], dtype=np.complex128)
        keys["|".join(map(str, record_key))] = {
            "features": name,
            "modes": mode_name,
        }
    arrays["profile_grams"] = np.concatenate(
        [np.asarray(row["profile_grams"], dtype=float) for row in case_rows],
        axis=0,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **arrays)
    return {
        "path": _relative(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "record_keys": keys,
        "array_shapes": {name: list(value.shape) for name, value in arrays.items()},
    }


def plot_results(payload: dict[str, Any], path: Path) -> None:
    rows = payload["analysis"]["rows"]
    kr = np.asarray([row["kr"] for row in rows], dtype=float)
    fig, axes = plt.subplots(2, 2, figsize=(11.3, 8.1))
    x = np.arange(kr.size)
    width = 0.2
    model_specs = (
        ("1", "AR(1)"),
        ("2", "AR(2)"),
        ("conservative", "undamped"),
        (str(payload["registration"]["delay_order"]), "AR(8)"),
    )
    for offset, (key, label) in zip((-1.5, -0.5, 0.5, 1.5), model_specs, strict=True):
        values = []
        for row in rows:
            fit = row["active"][key] if key == "conservative" else row["active"]["models"][key]
            values.append(
                _ratio(
                    fit["readout_test_rollout_rmse"],
                    fit["readout_test_zero_rmse"],
                )
            )
        axes[0, 0].bar(x + offset * width, values, width=width, label=label)
    axes[0, 0].axhline(1.0, color="black", linestyle="--", linewidth=1)
    axes[0, 0].set_title("Held-out visible readout")
    axes[0, 0].set_ylabel("recursive RMSE / zero")
    axes[0, 0].legend(fontsize=8, ncol=2)

    for offset, order in zip((-0.18, 0.18), ("1", "2"), strict=True):
        values = [
            _ratio(
                row["eta_zero"]["models"][order]["test_rollout_rmse"],
                row["eta_zero"]["models"][order]["test_zero_rmse"],
            )
            for row in rows
        ]
        axes[0, 1].bar(x + offset, values, width=0.36, label=f"AR({order})")
    axes[0, 1].axhline(1.0, color="black", linestyle="--", linewidth=1)
    axes[0, 1].set_title("eta=0 memory control")
    axes[0, 1].set_ylabel("recursive RMSE / zero")
    axes[0, 1].legend(fontsize=8)

    rank_energy = [row["active"]["rank_two_energy"] for row in rows]
    gaps = [row["active"]["third_to_second_ratio"] for row in rows]
    axes[1, 0].plot(x, rank_energy, "o-", label="rank-2 energy")
    axes[1, 0].plot(x, gaps, "s-", label=r"$s_3/s_2$")
    axes[1, 0].axhline(0.9, color="C0", linestyle="--", linewidth=1)
    axes[1, 0].axhline(0.5, color="C1", linestyle="--", linewidth=1)
    axes[1, 0].set_ylim(0.0, 1.05)
    axes[1, 0].set_title("Hankel order gate")
    axes[1, 0].legend(fontsize=8)

    gram = np.asarray(payload["analysis"]["spatial_input"]["median_gram"])
    image = axes[1, 1].imshow(gram, vmin=-1.0, vmax=1.0, cmap="coolwarm")
    axes[1, 1].set_xticks(x, [f"{value:g}" for value in kr])
    axes[1, 1].set_yticks(x, [f"{value:g}" for value in kr])
    axes[1, 1].set_xlabel(r"input $kR_{mem}$")
    axes[1, 1].set_ylabel(r"input $kR_{mem}$")
    axes[1, 1].set_title("Weighted input-profile Gram matrix")
    fig.colorbar(image, ax=axes[1, 1], fraction=0.046, pad=0.04)
    for axis in axes[:1].flat:
        axis.set_xticks(x, [f"{value:g}" for value in kr])
        axis.set_xlabel(r"$kR_{mem}$")
        axis.grid(alpha=0.2)
    axes[1, 0].set_xticks(x, [f"{value:g}" for value in kr])
    axes[1, 0].set_xlabel(r"$kR_{mem}$")
    axes[1, 0].grid(alpha=0.2)
    fig.suptitle(
        "P3.8e technical reconciliation\n"
        f"decision: {payload['analysis']['decision']}",
        fontsize=13,
    )
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _pole_text(values: list[dict[str, float]]) -> str:
    return ", ".join(
        f"{value['real']:.3g}{value['imag']:+.3g}i" for value in values
    )


def build_report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    analysis = payload["analysis"]
    controls = analysis["controls"]
    spatial = analysis["spatial_input"]
    lines = [
        "# P3.8e technical reconciliation",
        "",
        f"Date: {payload['generated_utc'][:10]}.",
        "",
        "## Verdict",
        "",
        f"Decision: **`{analysis['decision']}`**.",
        "",
        "The historical P3.8e decision is superseded as",
        "`superseded-methodologically-inconclusive`. Its raw simulation was not",
        "shown to be wrong; its temporal identification did not implement all review",
        "requirements consistently. This reconciliation does not select an emergent",
        "`(m,p)` state unless at least four of five channels pass every corrected gate.",
        "",
        "## Why AR(2) and 'damped AR(2)' were identical",
        "",
        "For an underdamped continuous equation sampled every `Delta`,",
        "",
        r"\[a_1=2e^{-\gamma\Delta}\cos(\omega_d\Delta),\qquad a_2=-e^{-2\gamma\Delta}.\]",
        "",
        "Every stable conjugate-pole real AR(2) has this representation. The old",
        "'damped' fit therefore reparameterized the same two free coefficients and",
        "was not an independent model. The corrected table compares free AR(2) with",
        "the genuinely different undamped constraint `a2=-1`; damping/frequency are",
        "now labels inferred from free poles, not a second fit or pass criterion.",
        "",
        "## Review corrections executed",
        "",
        "- active and `eta=0` responses are fitted separately; their difference is",
        "  not treated as a transfer function;",
        "- every order uses targets starting at sample 8 and the same 60/40 split;",
        "- the analysis ends at the known 600-update memory horizon, placing held-out",
        "  targets inside the signal-bearing transient; update 800 is extinction-only;",
        "- coefficients are learned from real/imaginary memory Fourier readouts; the",
        "  visible relative coordinate is scored without contributing to the fit;",
        "- rank-two Hankel energy/gap and 4/5 seed replication are decision gates;",
        "- the `N=3M` and `N=100M` age pair uses the same future-noise realization;",
        "- the weighted Gram matrix tests whether nominal `kR` inputs are independent.",
        "- full cross-`k` responses remain archived; diagonal leakage is a separate",
        "  diagnostic rather than being silently discarded.",
        "",
        "## Numerical controls",
        "",
        "| diagnostic | value | pass |",
        "|---|---:|:---:|",
        f"| uniform identity error | {controls['uniform_identity_error']:.3e} | {'yes' if analysis['control_gates']['uniform_identity'] else 'no'} |",
        f"| eta-zero extinction at update 800 | {controls['eta_zero_extinction']:.3e} | {'yes' if analysis['control_gates']['eta_zero_extinction'] else 'no'} |",
        f"| active strength linearity, median / max | {controls['active_linearity_median']:.3f} / {controls['active_linearity_max']:.3f} | {'yes' if analysis['control_gates']['active_linearity'] else 'no'} |",
        f"| active full-mode linearity, median / max | {controls['active_full_mode_linearity_median']:.3f} / {controls['active_full_mode_linearity_max']:.3f} | {'yes' if analysis['control_gates']['active_linearity'] else 'no'} |",
        f"| eta-zero strength linearity, median / max | {controls['eta_zero_linearity_median']:.3f} / {controls['eta_zero_linearity_max']:.3f} | {'yes' if analysis['control_gates']['eta_zero_linearity'] else 'no'} |",
        f"| eta-zero full-mode linearity, median / max | {controls['eta_zero_full_mode_linearity_median']:.3f} / {controls['eta_zero_full_mode_linearity_max']:.3f} | {'yes' if analysis['control_gates']['eta_zero_linearity'] else 'no'} |",
        f"| maximum radius-ratio disturbance | {controls['radius_change_max']:.3f} | {'yes' if analysis['control_gates']['shape_bounded'] else 'no'} |",
        f"| active / feedback cross-k diagonal fraction | {controls['active_cross_k_diagonal_fraction_median']:.3f} / {controls['feedback_cross_k_diagonal_fraction_median']:.3f} | diagnostic |",
        "",
        "## Corrected temporal comparison",
        "",
        "Ratios are recursive held-out visible RMSE divided by its zero null. AR(2)",
        "coefficients are fitted only on memory readouts. `eta0 AR2/AR1` uses the",
        "memory-fit rollout because its visible response is exactly zero.",
        "",
        "| kR | AR(1) | AR(2) | undamped | AR(8) | eta0 AR2/AR1 | mem holdout E | vis holdout E | rank-2 energy | s3/s2 | seed pass | poles | gate |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|:---:|",
    ]
    for row in analysis["rows"]:
        active = row["active"]
        first = active["models"]["1"]
        second = active["models"]["2"]
        delay = active["models"][str(payload["registration"]["delay_order"])]
        conservative = active["conservative"]
        eta_first = row["eta_zero"]["models"]["1"]
        eta_second = row["eta_zero"]["models"]["2"]
        lines.append(
            f"| {row['kr']:g} | "
            f"{_ratio(first['readout_test_rollout_rmse'], first['readout_test_zero_rmse']):.3f} | "
            f"{_ratio(second['readout_test_rollout_rmse'], second['readout_test_zero_rmse']):.3f} | "
            f"{_ratio(conservative['readout_test_rollout_rmse'], conservative['readout_test_zero_rmse']):.3f} | "
            f"{_ratio(delay['readout_test_rollout_rmse'], delay['readout_test_zero_rmse']):.3f} | "
            f"{_ratio(eta_second['test_rollout_rmse'], eta_first['test_rollout_rmse']):.3f} | "
            f"{row['memory_signal']['holdout_energy_fraction']:.3f} | "
            f"{row['visible_signal']['holdout_energy_fraction']:.3f} | "
            f"{active['rank_two_energy']:.3f} | {active['third_to_second_ratio']:.3f} | "
            f"{row['seed_passes']}/5 | {_pole_text(second['poles'])} | "
            f"{'pass' if row['pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            f"Complete temporal channels: **{analysis['temporal_passes']}/5**; required: at least 4/5.",
            "The eta-zero AR(2)/AR(1) ratio is diagnostic only. The passive finite",
            "memory shift can itself have multi-lag structure; feedback specificity",
            "instead requires a predictive visible response, which is identically zero",
            "in the eta-zero arm.",
            "",
            "## Spatial-input audit",
            "",
            f"Weighted profile condition number min/median/max: `{spatial['condition_min']:.1f}` / `{spatial['condition_median']:.1f}` / `{spatial['condition_max']:.1f}`.",
            f"Maximum absolute off-diagonal Gram entry: `{spatial['max_abs_off_diagonal']:.4f}`.",
            f"Independent-mode gate: **{'pass' if spatial['independent_mode_gate'] else 'fail'}**.",
            "",
            "A failed Gram gate does not invalidate each state perturbation, but it",
            "blocks treating the five responses as independent spatial modes or fitting",
            "the P3.8d dispersion polynomial from them.",
            "",
            "## Formation-age comparison",
            "",
            "Seed 1 at `N=3M` and `N=100M` now shares the identical future-noise",
            "array. This remains one paired seed, not population evidence.",
            f"Age-consistent channels relative to the five-seed formation spread: **{analysis['age_passes']}/5**.",
            "",
            "| kR | age pole distance | max seed pole distance | N100M/N3M norm | seed norm range | pass |",
            "|---:|---:|---:|---:|---:|:---:|",
        ]
    )
    for row in analysis["age_comparisons"]:
        lines.append(
            f"| {row['kr']:g} | {row['pole_distance']:.3f} | "
            f"{row['max_formation_seed_pole_distance']:.3f} | "
            f"{row['response_norm_ratio']:.3f} | "
            f"{row['formation_seed_norm_ratio_min']:.3f}--"
            f"{row['formation_seed_norm_ratio_max']:.3f} | "
            f"{'pass' if row['pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "## Figure",
            "",
            f"![P3.8e reconciliation]({_relative_from(report, figure)})",
            "",
            "## Scientific boundary",
            "",
            "This reconciliation can reject or retain a two-pole *effective temporal",
            "closure* for the tested state intervention. It still does not establish",
            "power-conjugate ports, a positive storage metric, a canonical deposition",
            "write channel, cross-node mediation or microscopic momentum. P3.8f remains",
            "the separate write-port test if the corrected temporal result warrants it.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{payload['git_revision']}`.",
            f"- Git status: `{payload['git_status'] or 'clean'}`.",
            f"- Protocol revision: `{payload['protocol_revision']}`.",
            f"- Summary: [{Path(payload['summary_json']).name}]({_relative_from(report, _resolve(Path(payload['summary_json'])))})",
            f"- Response archive: [{Path(payload['response_archive']['path']).name}]({_relative_from(report, _resolve(Path(payload['response_archive']['path'])))}) (`{payload['response_archive']['sha256']}`).",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    status = _git_output(["status", "--porcelain"])
    if status not in ("", "unavailable") and not args.allow_dirty:
        raise RuntimeError("refusing dirty worktree; use --allow-dirty explicitly")
    kr_values = _csv_floats(args.kr_values)
    fractions = _csv_floats(args.perturbation_fractions)
    if not np.array_equal(kr_values, np.asarray([0.5, 1.0, 2.0, 4.0, 8.0])):
        raise ValueError("reconciliation fixes kR={0.5,1,2,4,8}")
    if not np.array_equal(fractions, np.asarray([0.005, 0.01])):
        raise ValueError("reconciliation fixes perturbation fractions {0.005,0.01}")
    if _csv_seeds(args.seeds) != [1, 2, 3, 4, 5]:
        raise ValueError("reconciliation fixes formation seeds 1--5")
    registered_scalars = {
        "analysis_updates": (args.analysis_updates, 600),
        "extinction_updates": (args.extinction_updates, 800),
        "sample_every": (args.sample_every, 5),
        "train_fraction": (args.train_fraction, 0.6),
        "common_start_index": (args.common_start_index, 8),
        "delay_order": (args.delay_order, 8),
        "noise_seed": (args.noise_seed, 20_260_813),
    }
    changed = [name for name, (actual, expected) in registered_scalars.items() if actual != expected]
    if changed:
        raise ValueError(f"registered reconciliation arguments changed: {changed}")
    cases, age_case = discover_cases(args)
    records, case_rows = run_responses(
        cases,
        age_case,
        args,
        kr_values,
        fractions,
    )
    analysis = analyze(
        records,
        cases,
        age_case,
        case_rows,
        args,
        kr_values,
        fractions,
    )
    archive_path = _resolve(args.responses_npz)
    response_archive = write_archive(records, case_rows, archive_path, args)
    payload = {
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": status,
        "protocol_revision": _git_output(["rev-parse", "HEAD"]),
        "command": (
            "python experiments/current/memory/closure/"
            "emergent_modal_state_reconciliation.py"
        ),
        "registration": {
            "kr_values": kr_values,
            "perturbation_fractions": fractions,
            "analysis_updates": args.analysis_updates,
            "extinction_updates": args.extinction_updates,
            "sample_every": args.sample_every,
            "train_fraction": args.train_fraction,
            "common_start_index": args.common_start_index,
            "delay_order": args.delay_order,
            "noise_seed": args.noise_seed,
            "required_channel_passes": 4,
            "rank_two_energy_threshold": 0.9,
            "third_to_second_singular_threshold": 0.5,
            "holdout_energy_fraction_threshold": 0.05,
            "support_fraction_of_peak": 0.01,
            "profile_condition_threshold": 100.0,
            "required_age_passes": 4,
        },
        "cases": case_rows,
        "analysis": analysis,
        "response_archive": response_archive,
        "summary_json": _relative(args.summary_json),
    }
    serializable = _jsonable(payload)
    figure = _resolve(args.figure)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    plot_results(serializable, figure)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(serializable, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(build_report(serializable, report, figure), encoding="utf-8")
    print(
        json.dumps(
            {
                "decision": analysis["decision"],
                "temporal_passes": analysis["temporal_passes"],
                "report": _relative(report),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
