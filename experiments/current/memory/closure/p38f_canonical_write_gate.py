"""Run and aggregate the P3.8f canonical trajectory write-port gate."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, replace
from datetime import UTC, datetime
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
    GateStatus,
    evaluate_evidence_gate,
    load_finite_memory_checkpoint,
    paired_canonical_write_response,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
SHARD_SCHEMA = "emergenz-knoten.p38f-canonical-write-shard"
SHARD_SCHEMA_VERSION = 1
AGGREGATE_SCHEMA = "emergenz-knoten.p38f-canonical-write-aggregate"
AGGREGATE_SCHEMA_VERSION = 1
DEFAULT_BUNDLE = Path(
    "data/processed/reference_states/"
    "p38f_scalar_Aatt35_N3M_d3_seed1-5_2026-08-15/"
    "bundle_manifest.json"
)
DEFAULT_SHARD_DIR = Path(
    "data/processed/p38f_canonical_write_2026-08-15/shards"
)
DEFAULT_SUMMARY = Path(
    "reports/memory/closure/p38f_canonical_write_gate_2026-08-15.json"
)
DEFAULT_REPORT = Path(
    "reports/memory/closure/p38f_canonical_write_gate_2026-08-15.md"
)
DEFAULT_FIGURE = Path(
    "figures/draft/memory/p38f_canonical_write_gate_2026-08-15.png"
)
REGISTERED_KR = np.asarray([0.5, 1.0, 2.0, 4.0, 8.0], dtype=float)
REGISTERED_FRACTIONS = np.asarray([0.005, 0.01], dtype=float)
REGISTERED_SEEDS = [1, 2, 3, 4, 5]
NOISE_SEED = 20_260_815


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


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True, allow_nan=False)
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _load_bundle(path: Path) -> dict[str, Any]:
    source = path.resolve()
    payload = json.loads(source.read_text(encoding="utf-8"))
    if payload.get("schema") != "emergenz-knoten.p38f-state-bundle":
        raise ValueError("unsupported P3.8f state-bundle schema")
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported P3.8f state-bundle schema version")
    if payload.get("expected_seeds") != REGISTERED_SEEDS:
        raise ValueError("state bundle does not contain registered seeds 1--5")
    return payload


def _registration(alpha: float, dim: int) -> dict[str, Any]:
    tau_updates = 1.0 / float(alpha)
    rounded_tau = int(round(tau_updates))
    if not np.isclose(tau_updates, rounded_tau, rtol=0.0, atol=1e-12):
        raise ValueError("P3.8f requires an integer update memory time")
    return {
        "kr_values": REGISTERED_KR,
        "perturbation_fractions": REGISTERED_FRACTIONS,
        "formation_seeds": REGISTERED_SEEDS,
        "dim": int(dim),
        "tau_updates": rounded_tau,
        "analysis_updates": 8 * rounded_tau,
        "sample_every": 1,
        "pulse_updates": 2,
        "noise_seed": NOISE_SEED,
        "absolute_response_floor": 1e-8,
        "signal_relative_floor": 1e-3,
        "required_informative_folds": 2,
        "required_seed_passes": 4,
        "folds_memory_times": {
            "A": {"fit": [0.1, 2.0], "holdout": [2.0, 3.0]},
            "B": {"fit": [0.1, 3.0], "holdout": [3.0, 4.0]},
            "C": {"fit": [0.1, 4.0], "holdout": [4.0, 5.0]},
        },
    }


def _response_arrays(response: Any) -> dict[str, np.ndarray]:
    return {
        "position_response": response.position_response,
        "memory_center_response": response.memory_center_response,
        "centered_mode_response": response.centered_mode_response,
        "self_drift_response": response.self_drift_response,
        "position_even_leakage": response.position_even_leakage,
        "memory_center_even_leakage": response.memory_center_even_leakage,
        "centered_mode_even_leakage": response.centered_mode_even_leakage,
        "branch_positions": response.branch_positions,
        "branch_radius_ratios": response.branch_radius_ratios,
        "control_positions": response.control_positions,
        "control_radius_ratios": response.control_radius_ratios,
        "plus_kicks": response.plus_kicks,
    }


def simulate_seed(
    bundle_manifest: Path,
    seed: int,
    output_dir: Path,
    *,
    simulation_revision: str,
    overwrite: bool,
) -> Path:
    """Generate one immutable seed shard from a curated mature state."""

    bundle_path = bundle_manifest.resolve()
    bundle = _load_bundle(bundle_path)
    entries = {int(entry["seed"]): entry for entry in bundle["entries"]}
    if seed not in entries:
        raise ValueError(f"seed {seed} is absent from state bundle")
    entry = entries[seed]
    checkpoint_path = bundle_path.parent / entry["checkpoint"]
    if _sha256(checkpoint_path) != entry["checkpoint_sha256"]:
        raise ValueError("checkpoint file hash does not match bundle manifest")
    checkpoint = load_finite_memory_checkpoint(checkpoint_path)
    registration = _registration(checkpoint.config.alpha, checkpoint.config.dim)
    steps = np.arange(0, registration["analysis_updates"] + 1, dtype=int)

    destination = output_dir.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    npz_path = destination / f"p38f_seed{seed}.npz"
    json_path = destination / f"p38f_seed{seed}.json"
    if (npz_path.exists() or json_path.exists()) and not overwrite:
        raise FileExistsError(f"P3.8f seed shard already exists for seed {seed}")

    arrays: dict[str, np.ndarray] = {
        "sample_steps": steps,
        "kr_values": REGISTERED_KR,
        "perturbation_fractions": REGISTERED_FRACTIONS,
    }
    records = []
    for axis_index, direction in enumerate(np.eye(checkpoint.config.dim)):
        noise = np.random.default_rng(
            NOISE_SEED + 1009 * seed + 53 * axis_index
        ).normal(size=(registration["analysis_updates"], checkpoint.config.dim))
        for condition in ("active", "eta_zero"):
            config = (
                checkpoint.config
                if condition == "active"
                else replace(checkpoint.config, eta=0.0)
            )
            for fraction_index, fraction in enumerate(REGISTERED_FRACTIONS):
                response = paired_canonical_write_response(
                    checkpoint.state,
                    config,
                    direction=direction,
                    kr_values=REGISTERED_KR,
                    perturbation_fraction=float(fraction),
                    noise=noise,
                    sample_steps=steps,
                )
                prefix = f"{condition}_f{fraction_index}_a{axis_index}"
                fields = _response_arrays(response)
                for name, values in fields.items():
                    arrays[f"{prefix}__{name}"] = np.asarray(values)
                records.append(
                    {
                        "condition": condition,
                        "fraction": float(fraction),
                        "fraction_index": fraction_index,
                        "axis": axis_index,
                        "prefix": prefix,
                        "memory_radius": response.memory_radius,
                        "perturbation_amplitude": response.perturbation_amplitude,
                    }
                )

    temporary = npz_path.with_suffix(".npz.tmp")
    with temporary.open("wb") as handle:
        np.savez_compressed(handle, **arrays)
    temporary.replace(npz_path)
    payload = {
        "schema": SHARD_SCHEMA,
        "schema_version": SHARD_SCHEMA_VERSION,
        "generated_utc": datetime.now(UTC).isoformat(),
        "simulation_revision": simulation_revision,
        "bundle_manifest": _relative(bundle_path),
        "bundle_manifest_sha256": _sha256(bundle_path),
        "checkpoint": _relative(checkpoint_path),
        "checkpoint_sha256": entry["checkpoint_sha256"],
        "formation_seed": seed,
        "formation_update_index": checkpoint.update_index,
        "formation_revision": checkpoint.git_revision,
        "config": asdict(checkpoint.config),
        "registration": registration,
        "records": records,
        "archive": _relative(npz_path),
        "archive_sha256": _sha256(npz_path),
        "array_shapes": {name: list(values.shape) for name, values in arrays.items()},
    }
    _atomic_json(json_path, payload)
    return json_path


def _load_shard(path: Path) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != SHARD_SCHEMA:
        raise ValueError("unsupported P3.8f shard schema")
    if payload.get("schema_version") != SHARD_SCHEMA_VERSION:
        raise ValueError("unsupported P3.8f shard schema version")
    archive = _resolve(Path(payload["archive"]))
    if _sha256(archive) != payload["archive_sha256"]:
        raise ValueError("P3.8f shard archive hash mismatch")
    with np.load(archive, allow_pickle=False) as data:
        arrays = {name: np.asarray(data[name]) for name in data.files}
    expected = {name: list(values.shape) for name, values in arrays.items()}
    if expected != payload["array_shapes"]:
        raise ValueError("P3.8f shard array shapes do not match manifest")
    return payload, arrays


def _record_arrays(
    shard: dict[str, Any],
    arrays: dict[str, np.ndarray],
    *,
    condition: str,
    fraction_index: int,
    axis: int,
) -> dict[str, np.ndarray]:
    match = [
        record
        for record in shard["records"]
        if record["condition"] == condition
        and int(record["fraction_index"]) == fraction_index
        and int(record["axis"]) == axis
    ]
    if len(match) != 1:
        raise ValueError("P3.8f shard record index is incomplete or duplicated")
    prefix = match[0]["prefix"]
    return {
        name.split("__", 1)[1]: values
        for name, values in arrays.items()
        if name.startswith(prefix + "__")
    }


def _norm_ratio(numerator: np.ndarray, denominator: np.ndarray) -> float:
    return float(
        np.linalg.norm(numerator)
        / max(float(np.linalg.norm(denominator)), np.finfo(float).tiny)
    )


def _signal_folds(
    values: np.ndarray,
    sample_steps: np.ndarray,
    registration: dict[str, Any],
) -> dict[str, Any]:
    matrix = np.asarray(values)
    if np.iscomplexobj(matrix):
        matrix = np.concatenate((matrix.real, matrix.imag), axis=1)
    matrix = np.asarray(matrix, dtype=float).reshape(matrix.shape[0], -1)
    tau = int(registration["tau_updates"])
    reference = (sample_steps >= math.ceil(0.1 * tau)) & (sample_steps <= 2 * tau)
    scales = np.sqrt(np.mean(matrix[reference] ** 2, axis=0))
    maximum = float(np.max(scales)) if scales.size else 0.0
    absolute_floor = float(registration["absolute_response_floor"])
    active = scales > max(1e-6 * maximum, absolute_floor)
    if not np.any(active):
        empty_folds = {
            name: {"rms": 0.0, "relative_to_reference": 0.0, "pass": False}
            for name in registration["folds_memory_times"]
        }
        return {
            "active_channels": 0,
            "reference_rms": maximum,
            "active_scale_min": 0.0,
            "active_scale_max": maximum,
            "folds": empty_folds,
            "passes": 0,
        }
    standardized = matrix[:, active] / scales[active][None, :]
    reference_rms = float(np.sqrt(np.mean(standardized[reference] ** 2)))
    floor = float(registration["signal_relative_floor"])
    fold_rows = {}
    passes = 0
    for name, windows in registration["folds_memory_times"].items():
        lower, upper = windows["holdout"]
        mask = (sample_steps > lower * tau) & (sample_steps <= upper * tau)
        rms = float(np.sqrt(np.mean(standardized[mask] ** 2)))
        ratio = rms / max(reference_rms, np.finfo(float).tiny)
        passed = ratio >= floor
        passes += passed
        fold_rows[name] = {"rms": rms, "relative_to_reference": ratio, "pass": passed}
    return {
        "active_channels": int(np.count_nonzero(active)),
        "reference_rms": reference_rms,
        "active_scale_min": float(np.min(scales[active])),
        "active_scale_max": float(np.max(scales[active])),
        "folds": fold_rows,
        "passes": int(passes),
    }


def _relative_lifetime(
    envelope: np.ndarray,
    sample_steps: np.ndarray,
    registration: dict[str, Any],
) -> float:
    values = np.asarray(envelope, dtype=float)
    peak = float(np.max(values))
    if not np.isfinite(peak) or peak <= 0.0:
        return 0.0
    pulse_end = int(registration["pulse_updates"])
    supported = (sample_steps >= pulse_end) & (
        values >= float(registration["signal_relative_floor"]) * peak
    )
    if not np.any(supported):
        return 0.0
    return float(
        np.max(sample_steps[supported]) / int(registration["tau_updates"])
    )


def _seed_diagnostics(
    shard: dict[str, Any],
    arrays: dict[str, np.ndarray],
) -> dict[str, Any]:
    registration = shard["registration"]
    steps = np.asarray(arrays["sample_steps"], dtype=int)
    dim = int(registration["dim"])
    linearity = []
    even_leakage = []
    shape_changes = []
    net_kicks = []
    eta_return = []
    eta_extinction = []
    control_radius_minima = []
    memory_values = []
    visible_values = []
    for axis in range(dim):
        for condition in ("active", "eta_zero"):
            small = _record_arrays(
                shard, arrays, condition=condition, fraction_index=0, axis=axis
            )
            large = _record_arrays(
                shard, arrays, condition=condition, fraction_index=1, axis=axis
            )
            small_stack = np.concatenate(
                (
                    small["position_response"].reshape(steps.size, -1),
                    small["memory_center_response"].reshape(steps.size, -1),
                    small["centered_mode_response"].real.reshape(steps.size, -1),
                    small["centered_mode_response"].imag.reshape(steps.size, -1),
                    small["self_drift_response"].reshape(steps.size, -1),
                ),
                axis=1,
            )
            large_stack = np.concatenate(
                (
                    large["position_response"].reshape(steps.size, -1),
                    large["memory_center_response"].reshape(steps.size, -1),
                    large["centered_mode_response"].real.reshape(steps.size, -1),
                    large["centered_mode_response"].imag.reshape(steps.size, -1),
                    large["self_drift_response"].reshape(steps.size, -1),
                ),
                axis=1,
            )
            linearity.append(_norm_ratio(small_stack - large_stack, small_stack))
            for record in (small, large):
                odd = np.concatenate(
                    (
                        record["position_response"].reshape(steps.size, -1),
                        record["memory_center_response"].reshape(steps.size, -1),
                        record["centered_mode_response"].real.reshape(steps.size, -1),
                        record["centered_mode_response"].imag.reshape(steps.size, -1),
                    ),
                    axis=1,
                )
                even = np.concatenate(
                    (
                        record["position_even_leakage"].reshape(steps.size, -1),
                        record["memory_center_even_leakage"].reshape(steps.size, -1),
                        record["centered_mode_even_leakage"].real.reshape(steps.size, -1),
                        record["centered_mode_even_leakage"].imag.reshape(steps.size, -1),
                    ),
                    axis=1,
                )
                even_leakage.append(_norm_ratio(even, odd))
                control_radius = record["control_radius_ratios"][:, None]
                control_radius_minima.append(float(np.min(control_radius)))
                shape_changes.append(
                    float(
                        np.max(
                            np.abs(
                                record["branch_radius_ratios"]
                                / np.maximum(control_radius, 1e-12)
                                - 1.0
                            )
                        )
                    )
                )
                net_kicks.append(float(np.linalg.norm(np.sum(record["plus_kicks"], axis=0))))
            if condition == "eta_zero":
                post = steps >= 2
                for record in (small, large):
                    difference = record["branch_positions"][post] - record[
                        "control_positions"
                    ][post, None, :]
                    eta_return.append(float(np.max(np.abs(difference))))
                    mode = record["centered_mode_response"]
                    eta_extinction.append(
                        _norm_ratio(mode[-1:], mode)
                    )
            else:
                memory_values.extend(
                    (
                        small["memory_center_response"],
                        small["centered_mode_response"],
                    )
                )
                visible_values.extend(
                    (
                        small["position_response"]
                        - small["memory_center_response"],
                        small["self_drift_response"],
                    )
                )

    memory = np.concatenate(memory_values, axis=1)
    visible = np.concatenate(visible_values, axis=1)
    memory_signal = _signal_folds(memory, steps, registration)
    visible_signal = _signal_folds(visible, steps, registration)
    memory_envelope = np.sqrt(np.mean(np.abs(memory) ** 2, axis=1))
    visible_envelope = np.sqrt(np.mean(visible**2, axis=1))
    required_folds = int(registration["required_informative_folds"])
    g0_checks = {
        "zero_net_kick": max(net_kicks) <= 1e-14,
        "eta_zero_visible_return": max(eta_return) <= 1e-10,
        "eta_zero_extinction": max(eta_extinction) <= 1e-8,
        "strength_linearity": float(np.median(linearity)) <= 0.1
        and max(linearity) <= 0.25,
        "mirror_even_leakage": float(np.median(even_leakage)) <= 0.1
        and max(even_leakage) <= 0.25,
        "control_shape_defined": min(control_radius_minima) > 1e-12,
        "shape_bounded": max(shape_changes) <= 0.1,
    }
    g1_checks = {
        "memory_signal_in_two_folds": memory_signal["passes"] >= required_folds,
        "visible_or_force_signal_in_two_folds": visible_signal["passes"]
        >= required_folds,
    }
    return {
        "seed": int(shard["formation_seed"]),
        "g0_checks": g0_checks,
        "g0_pass": all(g0_checks.values()),
        "g1_checks": g1_checks,
        "g1_pass": all(g1_checks.values()),
        "memory_signal": memory_signal,
        "visible_signal": visible_signal,
        "metrics": {
            "linearity_median": float(np.median(linearity)),
            "linearity_max": max(linearity),
            "even_leakage_median": float(np.median(even_leakage)),
            "even_leakage_max": max(even_leakage),
            "shape_change_max": max(shape_changes),
            "control_radius_ratio_min": min(control_radius_minima),
            "net_kick_max": max(net_kicks),
            "eta_zero_return_max": max(eta_return),
            "eta_zero_extinction_max": max(eta_extinction),
            "relative_force_lifetime_memory_times": _relative_lifetime(
                visible_envelope,
                steps,
                registration,
            ),
        },
        "plot_memory_envelope": memory_envelope,
        "plot_visible_envelope": visible_envelope,
    }


def aggregate_shards(
    shard_paths: list[Path],
    *,
    analysis_revision: str = "unavailable",
) -> dict[str, Any]:
    """Validate all registered shards and evaluate only G0 and G1."""

    loaded = [
        (path.resolve(), *_load_shard(path.resolve()))
        for path in shard_paths
    ]
    by_seed = {
        int(payload["formation_seed"]): (path, payload, arrays)
        for path, payload, arrays in loaded
    }
    if sorted(by_seed) != REGISTERED_SEEDS or len(by_seed) != len(loaded):
        raise ValueError("aggregate requires exactly one shard for each seed 1--5")
    first = by_seed[REGISTERED_SEEDS[0]][1]
    for _, payload, _ in by_seed.values():
        if payload["simulation_revision"] != first["simulation_revision"]:
            raise ValueError("shards use different simulation revisions")
        if payload["bundle_manifest_sha256"] != first["bundle_manifest_sha256"]:
            raise ValueError("shards use different state bundles")
        if payload["registration"] != first["registration"]:
            raise ValueError("shards use different P3.8f registrations")
    bundle_path = _resolve(Path(first["bundle_manifest"]))
    if _sha256(bundle_path) != first["bundle_manifest_sha256"]:
        raise ValueError("P3.8f state-bundle hash changed after simulation")

    seed_rows = [
        _seed_diagnostics(*by_seed[seed][1:])
        for seed in REGISTERED_SEEDS
    ]
    g0_seed_passes = sum(row["g0_pass"] for row in seed_rows)
    g1_seed_passes = sum(row["g1_pass"] for row in seed_rows)
    validity = evaluate_evidence_gate(
        "experimental-validity",
        {"all_five_seed_controls": g0_seed_passes == 5},
    )
    identifiability = evaluate_evidence_gate(
        "input-output-identifiability",
        {
            "four_of_five_informative_seeds": g1_seed_passes
            >= int(first["registration"]["required_seed_passes"]),
        },
        prerequisites=(validity,),
        failed_status=GateStatus.INCONCLUSIVE,
    )
    second_state = evaluate_evidence_gate(
        "second-state-selection",
        None,
        prerequisites=(identifiability,),
    )
    oscillation = evaluate_evidence_gate(
        "oscillatory-phase-mode",
        None,
        prerequisites=(second_state,),
    )
    hierarchy = {
        gate.name: gate
        for gate in (validity, identifiability, second_state, oscillation)
    }
    return {
        "schema": AGGREGATE_SCHEMA,
        "schema_version": AGGREGATE_SCHEMA_VERSION,
        "generated_utc": datetime.now(UTC).isoformat(),
        "simulation_revision": first["simulation_revision"],
        "analysis_revision": analysis_revision,
        "bundle_manifest": first["bundle_manifest"],
        "bundle_manifest_sha256": first["bundle_manifest_sha256"],
        "registration": first["registration"],
        "shards": [
            {
                "seed": seed,
                "manifest": _relative(by_seed[seed][0]),
                "manifest_sha256": _sha256(by_seed[seed][0]),
                "archive": by_seed[seed][1]["archive"],
                "archive_sha256": by_seed[seed][1]["archive_sha256"],
            }
            for seed in REGISTERED_SEEDS
        ],
        "seed_rows": seed_rows,
        "g0_seed_passes": g0_seed_passes,
        "g1_seed_passes": g1_seed_passes,
        "gate_hierarchy": hierarchy,
        "decision": (
            "ready-for-second-state-identification"
            if identifiability.passed
            else "write-port-invalid"
            if not validity.passed
            else "write-port-identifiability-inconclusive"
        ),
    }


def _plot(payload: dict[str, Any], path: Path) -> None:
    rows = payload["seed_rows"]
    tau = int(payload["registration"]["tau_updates"])
    steps = np.arange(0, int(payload["registration"]["analysis_updates"]) + 1)
    time = steps / tau
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.0))
    for row in rows:
        memory = np.asarray(row["plot_memory_envelope"], dtype=float)
        visible = np.asarray(row["plot_visible_envelope"], dtype=float)
        axes[0, 0].plot(time, memory / max(float(np.max(memory)), 1e-300), label=f"seed {row['seed']}")
        axes[0, 1].plot(time, visible / max(float(np.max(visible)), 1e-300), label=f"seed {row['seed']}")
    for axis, title in zip(
        axes[0],
        ("Memory response envelope", "Relative-position/force response envelope"),
        strict=True,
    ):
        axis.set_yscale("log")
        axis.set_ylim(1e-12, 2.0)
        axis.set_xlabel(r"updates / $\tau_{mem}$")
        axis.set_ylabel("normalized RMS")
        axis.set_title(title)
        axis.grid(alpha=0.2)
    axes[0, 0].legend(fontsize=8, ncol=2)

    metric_names = ("linearity_max", "even_leakage_max", "shape_change_max")
    x = np.arange(len(rows))
    width = 0.25
    for offset, name in zip((-1, 0, 1), metric_names, strict=True):
        axes[1, 0].bar(
            x + offset * width,
            [row["metrics"][name] for row in rows],
            width=width,
            label=name.replace("_", " "),
        )
    axes[1, 0].axhline(0.1, color="black", linestyle="--", linewidth=1)
    axes[1, 0].set_xticks(x, [str(row["seed"]) for row in rows])
    axes[1, 0].set_xlabel("formation seed")
    axes[1, 0].set_title("G0 perturbation controls")
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].grid(axis="y", alpha=0.2)

    fold_names = ("A", "B", "C")
    image = np.asarray(
        [
            [
                min(
                    row["memory_signal"]["folds"][fold]["relative_to_reference"],
                    row["visible_signal"]["folds"][fold]["relative_to_reference"],
                )
                for fold in fold_names
            ]
            for row in rows
        ]
    )
    display = axes[1, 1].imshow(np.log10(np.maximum(image, 1e-12)), cmap="viridis", aspect="auto")
    axes[1, 1].set_xticks(np.arange(3), fold_names)
    axes[1, 1].set_yticks(np.arange(5), [str(row["seed"]) for row in rows])
    axes[1, 1].set_xlabel("blocked holdout fold")
    axes[1, 1].set_ylabel("formation seed")
    axes[1, 1].set_title("min(memory, relative/force) log10 signal ratio")
    fig.colorbar(display, ax=axes[1, 1], fraction=0.046, pad=0.04)
    fig.suptitle(f"P3.8f canonical write port: {payload['decision']}", fontsize=13)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _build_report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    hierarchy = payload["gate_hierarchy"]
    lines = [
        "# P3.8f canonical trajectory write port",
        "",
        f"Date: {payload['generated_utc'][:10]}.",
        "",
        "## Verdict",
        "",
        f"Decision: **`{payload['decision']}`**.",
        "",
        "The intervention is written by mirrored visible kicks `(+delta,-delta)`",
        "and `(-delta,+delta)`. Both arms have zero direct net kick; every visited",
        "point enters the unchanged scalar-memory deposition update.",
        "",
        "| gate | status | failed checks | blocked by |",
        "|---|---|---|---|",
    ]
    for gate in hierarchy.values():
        lines.append(
            f"| `{gate['name']}` | **`{gate['status']}`** | "
            f"{', '.join(gate['failed_checks']) or '-'} | "
            f"{', '.join(gate['blocked_by']) or '-'} |"
        )
    lines.extend(
        [
            "",
            f"G0 seed passes: **{payload['g0_seed_passes']}/5**.",
            f"G1 seed passes: **{payload['g1_seed_passes']}/5**.",
            "G2 is intentionally not evaluated here. A G1 pass only licenses the",
            "blocked model-order comparison; it does not select a second state.",
            "",
            "## Seed controls and signal support",
            "",
            "| seed | G0 | G1 | linearity max | even max | shape max | response lifetime / tau | memory folds | relative/force folds | max relative/force holdout |",
            "|---:|:---:|:---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in payload["seed_rows"]:
        metrics = row["metrics"]
        visible_ratios = [
            fold["relative_to_reference"]
            for fold in row["visible_signal"]["folds"].values()
        ]
        lines.append(
            f"| {row['seed']} | {'pass' if row['g0_pass'] else 'fail'} | "
            f"{'pass' if row['g1_pass'] else 'inconclusive'} | "
            f"{metrics['linearity_max']:.3e} | {metrics['even_leakage_max']:.3e} | "
            f"{metrics['shape_change_max']:.3e} | "
            f"{metrics['relative_force_lifetime_memory_times']:.3f} | "
            f"{row['memory_signal']['passes']}/3 | "
            f"{row['visible_signal']['passes']}/3 | {max(visible_ratios):.3e} |"
        )
    lines.extend(
        [
            "",
            "The response lifetime is descriptive, not an extra gate: it is the last",
            "sample at or above the registered `1e-3` fraction of the full",
            "relative-position/force envelope peak.",
            "",
            "## Readout audit",
            "",
            "The laboratory position contains a global translation-neutral mode.",
            "It is excluded from G1. The independent readout is the co-moving",
            "coordinate `x-m_rho` together with the self-force. An uncommitted draft",
            "that used absolute position was discarded before this evidence artifact",
            "was generated.",
            "",
            "## Figure",
            "",
            f"![P3.8f canonical write gate]({_relative_from(report, figure)})",
            "",
            "## Interpretation boundary",
            "",
            "G0 establishes only a valid weak canonical intervention. G1 establishes",
            "only whether memory and an independent relative-position/force readout remain",
            "measurable in fixed chronological holdouts. Neither gate identifies",
            "`(m,p)`, complex poles, momentum, phase, energy, a second knot or a",
            "field law.",
            "",
            "## Provenance",
            "",
            f"- Simulation revision: `{payload['simulation_revision']}`.",
            f"- Analysis revision: `{payload['analysis_revision']}`.",
            f"- State bundle: `{payload['bundle_manifest']}` (`{payload['bundle_manifest_sha256']}`).",
        ]
    )
    return "\n".join(lines) + "\n"


def _simulate_job(arguments: tuple[str, int, str, str, bool]) -> str:
    bundle, seed, output, revision, overwrite = arguments
    return str(
        simulate_seed(
            Path(bundle),
            seed,
            Path(output),
            simulation_revision=revision,
            overwrite=overwrite,
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-dirty", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate = subparsers.add_parser("simulate")
    simulate.add_argument("--bundle-manifest", type=Path, default=DEFAULT_BUNDLE)
    simulate.add_argument("--seed", type=int, required=True)
    simulate.add_argument("--output-dir", type=Path, default=DEFAULT_SHARD_DIR)
    simulate.add_argument("--overwrite", action="store_true")

    batch = subparsers.add_parser("simulate-all")
    batch.add_argument("--bundle-manifest", type=Path, default=DEFAULT_BUNDLE)
    batch.add_argument("--output-dir", type=Path, default=DEFAULT_SHARD_DIR)
    batch.add_argument("--workers", type=int, default=5)
    batch.add_argument("--overwrite", action="store_true")

    aggregate = subparsers.add_parser("aggregate")
    aggregate.add_argument("--shard-dir", type=Path, default=DEFAULT_SHARD_DIR)
    aggregate.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    aggregate.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    aggregate.add_argument("--figure", type=Path, default=DEFAULT_FIGURE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    status = _git_output(["status", "--porcelain"])
    if status not in ("", "unavailable") and not args.allow_dirty:
        raise RuntimeError("refusing dirty worktree; use --allow-dirty explicitly")
    revision = _git_output(["rev-parse", "HEAD"])
    if args.command == "simulate":
        path = simulate_seed(
            _resolve(args.bundle_manifest),
            args.seed,
            _resolve(args.output_dir),
            simulation_revision=revision,
            overwrite=args.overwrite,
        )
        print(json.dumps({"shard": _relative(path), "seed": args.seed}, indent=2))
        return
    if args.command == "simulate-all":
        if args.workers < 1:
            raise ValueError("workers must be positive")
        jobs = [
            (
                str(_resolve(args.bundle_manifest)),
                seed,
                str(_resolve(args.output_dir)),
                revision,
                args.overwrite,
            )
            for seed in REGISTERED_SEEDS
        ]
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            paths = list(executor.map(_simulate_job, jobs))
        print(json.dumps({"shards": [_relative(Path(path)) for path in paths]}, indent=2))
        return

    shard_dir = _resolve(args.shard_dir)
    paths = [shard_dir / f"p38f_seed{seed}.json" for seed in REGISTERED_SEEDS]
    payload = aggregate_shards(paths, analysis_revision=revision)
    serializable = _jsonable(payload)
    summary = _resolve(args.summary)
    report = _resolve(args.report)
    figure = _resolve(args.figure)
    _atomic_json(summary, serializable)
    _plot(serializable, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_build_report(serializable, report, figure), encoding="utf-8")
    print(
        json.dumps(
            {
                "decision": payload["decision"],
                "g0_seed_passes": payload["g0_seed_passes"],
                "g1_seed_passes": payload["g1_seed_passes"],
                "report": _relative(report),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
