"""Discriminate fixed quasistatic pair laws on one mature full-memory state."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
from typing import Any, Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

from emergenz_knoten import (
    centered_finite_difference_pair_force,
    gradient_mediator_transfer,
    load_finite_memory_checkpoint,
    FiniteMemoryState,
    memory_centroid,
    memory_shape_tensor,
    radial_gradient_mediator_green_3d,
    radial_gradient_mediator_green_derivative_3d,
    reciprocal_visible_memory_pair_interaction,
    rigid_full_memory_pair_interaction,
    three_scale_radial_derivative,
    three_scale_radial_potential,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
CHECKPOINT = Path(
    "data/processed/reference_states/"
    "scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/"
    "scalar_Aatt35_d3_seed1_N100000000.npz"
)
STATIC_PARAMETERS = {
    "sigma_rep": 1.0,
    "sigma_att": 3.0,
    "sigma_comp": 10.0,
    "amplitude_rep": 1.0,
    "amplitude_att": 35.0,
    "amplitude_comp": 0.944,
}
SPECTRAL_SHAPE = -1.9
MEMORY_LOADING = 0.3
DISCRIMINATION_RADIUS = 5.0
ROOT_BRACKETS = {
    "static_compensated": ((10.0, 12.0),),
    "gradient_mediator": ((3.5, 4.5), (6.5, 7.5)),
    "direct_source_control": ((4.0, 5.0), (7.0, 8.0)),
}
FIXED_RADII = (2.8, 5.0, 6.990916302867424, 8.0, 10.913073624192032, 12.0)
NONSTATIONARY_FORCE_RADII = (2.8, 5.0, 8.0, 12.0)
POINT_LIMIT_SCALES = (1.0, 0.5, 0.25)


RadialLaw = Callable[[np.ndarray], np.ndarray]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, default=CHECKPOINT)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/reciprocal/"
            "quasistatic_two_knot_discrimination_2026-08-12.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/reciprocal/"
            "quasistatic_two_knot_discrimination_2026-08-12.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/"
            "quasistatic_two_knot_discrimination_2026-08-12.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


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


def _laws() -> dict[str, tuple[RadialLaw, RadialLaw]]:
    def static_energy(radius: np.ndarray) -> np.ndarray:
        return three_scale_radial_potential(radius, **STATIC_PARAMETERS)

    def static_derivative(radius: np.ndarray) -> np.ndarray:
        return three_scale_radial_derivative(radius, **STATIC_PARAMETERS)

    def gradient_energy(radius: np.ndarray) -> np.ndarray:
        return -radial_gradient_mediator_green_3d(
            radius,
            spectral_shape=SPECTRAL_SHAPE,
            memory_loading=MEMORY_LOADING,
            coupling_geometry="gradient_vector",
        )

    def gradient_derivative(radius: np.ndarray) -> np.ndarray:
        return -radial_gradient_mediator_green_derivative_3d(
            radius,
            spectral_shape=SPECTRAL_SHAPE,
            memory_loading=MEMORY_LOADING,
            coupling_geometry="gradient_vector",
        )

    def direct_energy(radius: np.ndarray) -> np.ndarray:
        return -radial_gradient_mediator_green_3d(
            radius,
            spectral_shape=SPECTRAL_SHAPE,
            memory_loading=MEMORY_LOADING,
            coupling_geometry="direct_scalar",
        )

    def direct_derivative(radius: np.ndarray) -> np.ndarray:
        return -radial_gradient_mediator_green_derivative_3d(
            radius,
            spectral_shape=SPECTRAL_SHAPE,
            memory_loading=MEMORY_LOADING,
            coupling_geometry="direct_scalar",
        )

    return {
        "static_compensated": (static_energy, static_derivative),
        "gradient_mediator": (gradient_energy, gradient_derivative),
        "direct_source_control": (direct_energy, direct_derivative),
    }


def _orientations() -> dict[str, np.ndarray]:
    return {
        "identity": np.eye(3),
        "cyclic_rotation": np.array(
            [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]]
        ),
        "reflection_control": np.diag([-1.0, 1.0, 1.0]),
    }


def _point_roots(
    derivative: RadialLaw,
    brackets: tuple[tuple[float, float], ...],
) -> list[float]:
    return [
        float(brentq(lambda radius: float(derivative(np.asarray(radius))), low, high))
        for low, high in brackets
    ]


def _full_root(
    state,
    derivative: RadialLaw,
    energy: RadialLaw,
    bracket: tuple[float, float],
    rotation: np.ndarray,
) -> tuple[float, float, str]:
    axis = np.array([1.0, 0.0, 0.0])

    def force(radius: float) -> float:
        return rigid_full_memory_pair_interaction(
            state,
            state,
            radius * axis,
            radial_pair_energy=energy,
            radial_pair_energy_derivative=derivative,
            second_rotation=rotation,
        ).radial_force_on_second

    point_root = float(
        brentq(
            lambda radius: float(derivative(np.asarray(radius))),
            *bracket,
            xtol=1.0e-12,
            rtol=1.0e-14,
        )
    )
    step = 1.0e-5 * point_root
    force_at_root = force(point_root)
    slope = (force(point_root + step) - force(point_root - step)) / (2.0 * step)
    if not np.isfinite(slope) or slope == 0.0:
        raise RuntimeError("full-memory stationary-point slope is not identifiable")
    corrected = point_root - force_at_root / slope
    if not bracket[0] < corrected < bracket[1]:
        raise RuntimeError("full-memory root correction left registered bracket")
    residual = abs(force(corrected))
    scale = max(abs(force(point_root - step)), abs(force(point_root + step)))
    stability_step = 1.0e-4 * corrected
    force_left = force(corrected - stability_step)
    force_right = force(corrected + stability_step)
    if force_left > 0.0 and force_right < 0.0:
        stability = "stable"
    elif force_left < 0.0 and force_right > 0.0:
        stability = "unstable"
    else:
        stability = "unclassified"
    return (
        float(corrected),
        float(residual / max(scale, np.finfo(float).tiny)),
        stability,
    )


def _root_stability(derivative: RadialLaw, radius: float) -> str:
    step = 1.0e-4 * radius
    force_left = -float(derivative(np.asarray(radius - step)))
    force_right = -float(derivative(np.asarray(radius + step)))
    if force_left > 0.0 and force_right < 0.0:
        return "stable"
    if force_left < 0.0 and force_right > 0.0:
        return "unstable"
    return "unclassified"


def run_audit(checkpoint_path: Path | None = None) -> dict[str, Any]:
    source = _resolve(CHECKPOINT if checkpoint_path is None else checkpoint_path)
    checkpoint = load_finite_memory_checkpoint(source)
    state = checkpoint.state
    if state.dim != 3:
        raise ValueError("the registered Green inversion and checkpoint must both be d=3")
    axis = np.array([1.0, 0.0, 0.0])
    laws = _laws()
    orientations = _orientations()
    mass_product = float(np.sum(state.weights) ** 2)
    rms_radius = float(np.sqrt(np.trace(memory_shape_tensor(state))))

    roots: dict[str, dict[str, Any]] = {}
    maximum_root_shift_ratio = 0.0
    maximum_orientation_spread_ratio = 0.0
    maximum_root_residual_ratio = 0.0
    for name, (energy, derivative) in laws.items():
        point_roots = _point_roots(derivative, ROOT_BRACKETS[name])
        full_root_results = {
            orientation_name: [
                _full_root(state, derivative, energy, bracket, rotation)
                for bracket in ROOT_BRACKETS[name]
            ]
            for orientation_name, rotation in orientations.items()
        }
        full_roots_by_orientation = {
            orientation_name: [item[0] for item in values]
            for orientation_name, values in full_root_results.items()
        }
        full_stabilities_by_orientation = {
            orientation_name: [item[2] for item in values]
            for orientation_name, values in full_root_results.items()
        }
        root_rows = []
        for index, point_root in enumerate(point_roots):
            full_values = [
                values[index] for values in full_roots_by_orientation.values()
            ]
            shift_ratio = max(
                abs(value - point_root) / point_root for value in full_values
            )
            spread_ratio = (max(full_values) - min(full_values)) / point_root
            maximum_root_shift_ratio = max(maximum_root_shift_ratio, shift_ratio)
            maximum_orientation_spread_ratio = max(
                maximum_orientation_spread_ratio, spread_ratio
            )
            residual_ratio = max(
                values[index][1] for values in full_root_results.values()
            )
            maximum_root_residual_ratio = max(
                maximum_root_residual_ratio, residual_ratio
            )
            root_rows.append(
                {
                    "point_radius": point_root,
                    "full_memory_radii": {
                        key: values[index]
                        for key, values in full_roots_by_orientation.items()
                    },
                    "point_stability": _root_stability(derivative, point_root),
                    "full_memory_stabilities": {
                        key: values[index]
                        for key, values in full_stabilities_by_orientation.items()
                    },
                    "maximum_relative_shift": shift_ratio,
                    "orientation_relative_spread": spread_ratio,
                    "maximum_root_residual_ratio": residual_ratio,
                }
            )
        roots[name] = {"stationary_points": root_rows}

    fixed_rows = []
    maximum_force_energy_error = 0.0
    maximum_action_reaction_error = 0.0
    for name, (energy, derivative) in laws.items():
        for radius in FIXED_RADII:
            point_force = -mass_product * float(derivative(np.asarray(radius)))
            for orientation_name, rotation in orientations.items():
                interaction = rigid_full_memory_pair_interaction(
                    state,
                    state,
                    radius * axis,
                    radial_pair_energy=energy,
                    radial_pair_energy_derivative=derivative,
                    second_rotation=rotation,
                )
                if radius in NONSTATIONARY_FORCE_RADII:
                    finite_difference = centered_finite_difference_pair_force(
                        state,
                        state,
                        radius * axis,
                        radial_pair_energy=energy,
                        radial_pair_energy_derivative=derivative,
                        second_rotation=rotation,
                        step=1.0e-5,
                    )
                    force_scale = max(
                        abs(interaction.radial_force_on_second),
                        abs(finite_difference),
                        1.0e-14,
                    )
                    force_energy_error = abs(
                        interaction.radial_force_on_second - finite_difference
                    ) / force_scale
                    maximum_force_energy_error = max(
                        maximum_force_energy_error, force_energy_error
                    )
                else:
                    finite_difference = None
                    force_energy_error = None
                action_reaction_error = float(
                    np.linalg.norm(
                        interaction.force_on_first + interaction.force_on_second
                    )
                )
                if abs(point_force) > 1.0e-8:
                    point_error = abs(
                        interaction.radial_force_on_second - point_force
                    ) / abs(point_force)
                else:
                    point_error = None
                maximum_action_reaction_error = max(
                    maximum_action_reaction_error, action_reaction_error
                )
                fixed_rows.append(
                    {
                        "model": name,
                        "radius": radius,
                        "orientation": orientation_name,
                        "full_memory_force": interaction.radial_force_on_second,
                        "point_force": point_force,
                        "point_relative_error": point_error,
                        "energy_gradient_force": finite_difference,
                        "force_energy_relative_error": force_energy_error,
                        "action_reaction_absolute_error": action_reaction_error,
                    }
                )

    center = memory_centroid(state)
    point_limit_rows = []
    point_limit_orders = []
    for name, (energy, derivative) in laws.items():
        for radius in NONSTATIONARY_FORCE_RADII:
            point_force = -mass_product * float(derivative(np.asarray(radius)))
            relative_errors = []
            for scale in POINT_LIMIT_SCALES:
                scaled_state = FiniteMemoryState(
                    x=center + scale * (state.x - center),
                    memory=center[None, :] + scale * (state.memory - center[None, :]),
                    weights=state.weights,
                )
                interaction = rigid_full_memory_pair_interaction(
                    scaled_state,
                    scaled_state,
                    radius * axis,
                    radial_pair_energy=energy,
                    radial_pair_energy_derivative=derivative,
                )
                relative_errors.append(
                    abs(interaction.radial_force_on_second - point_force)
                    / abs(point_force)
                )
            orders = [
                float(
                    np.log(relative_errors[index] / relative_errors[index + 1])
                    / np.log(POINT_LIMIT_SCALES[index] / POINT_LIMIT_SCALES[index + 1])
                )
                for index in range(len(POINT_LIMIT_SCALES) - 1)
            ]
            point_limit_orders.extend(orders)
            point_limit_rows.append(
                {
                    "model": name,
                    "radius": radius,
                    "scales": list(POINT_LIMIT_SCALES),
                    "relative_errors": relative_errors,
                    "observed_orders": orders,
                }
            )

    identity_at_discriminator = {
        row["model"]: row["full_memory_force"]
        for row in fixed_rows
        if row["radius"] == DISCRIMINATION_RADIUS
        and row["orientation"] == "identity"
    }
    canonical_readout_comparison = {}
    for name, (energy, derivative) in laws.items():
        full = next(
            row["full_memory_force"]
            for row in fixed_rows
            if row["model"] == name
            and row["radius"] == DISCRIMINATION_RADIUS
            and row["orientation"] == "identity"
        )
        visible_memory = reciprocal_visible_memory_pair_interaction(
            state,
            state,
            DISCRIMINATION_RADIUS * axis,
            radial_pair_energy=energy,
            radial_pair_energy_derivative=derivative,
        )
        relative_difference = abs(
            visible_memory.radial_force_on_second - full
        ) / max(abs(full), np.finfo(float).tiny)
        canonical_readout_comparison[name] = {
            "memory_memory_force": full,
            "reciprocal_visible_memory_force": visible_memory.radial_force_on_second,
            "relative_difference": relative_difference,
        }
    finite_tail_mass_difference = abs(1.0 / float(np.sum(state.weights)) - 1.0)
    maximum_readout_mass_residual = max(
        abs(row["relative_difference"] - finite_tail_mass_difference)
        for row in canonical_readout_comparison.values()
    )
    static_integral = (
        STATIC_PARAMETERS["amplitude_rep"] * STATIC_PARAMETERS["sigma_rep"] ** 3
        - STATIC_PARAMETERS["amplitude_att"] * STATIC_PARAMETERS["sigma_att"] ** 3
        + STATIC_PARAMETERS["amplitude_comp"] * STATIC_PARAMETERS["sigma_comp"] ** 3
    )
    relaxation = float(np.sqrt(MEMORY_LOADING))
    transfer_parameters = {
        "memory_decay": relaxation,
        "conjugate_decay": relaxation,
        "local_stiffness": 1.0,
        "gradient_stiffness": SPECTRAL_SHAPE,
        "biharmonic_stiffness": 1.0,
    }
    gradient_zero = complex(
        gradient_mediator_transfer(0.0, **transfer_parameters).item()
    )
    direct_zero = complex(
        gradient_mediator_transfer(
            0.0,
            coupling_geometry="direct_scalar",
            **transfer_parameters,
        ).item()
    )
    def zero_law(radii: np.ndarray) -> np.ndarray:
        return np.zeros_like(np.asarray(radii, dtype=float))

    cross_off = rigid_full_memory_pair_interaction(
        state,
        state,
        DISCRIMINATION_RADIUS * axis,
        radial_pair_energy=zero_law,
        radial_pair_energy_derivative=zero_law,
    )
    compactness_ratio = max(
        (rms_radius / row["point_radius"]) ** 2
        for model in roots.values()
        for row in model["stationary_points"]
    )
    discriminator_rows = [
        row for row in fixed_rows if row["radius"] == DISCRIMINATION_RADIUS
    ]
    gates = {
        "checkpoint_schema_and_checksum_valid": checkpoint.update_index == 100_000_000,
        "static_compensated_integral_zero": abs(static_integral) < 1.0e-12,
        "gradient_mediator_zero_mode_zero": abs(gradient_zero) < 1.0e-14,
        "direct_source_zero_mode_nonzero_control": direct_zero.real > 0.0,
        "cross_off_energy_and_force_exactly_zero": bool(
            cross_off.energy == 0.0
            and np.array_equal(cross_off.force_on_first, np.zeros(state.dim))
            and np.array_equal(cross_off.force_on_second, np.zeros(state.dim))
        ),
        "common_radius_force_sign_discriminates_for_all_orientations": bool(
            all(
                row["full_memory_force"] < 0.0
                for row in discriminator_rows
                if row["model"] == "static_compensated"
            )
            and all(
                row["full_memory_force"] > 0.0
                for row in discriminator_rows
                if row["model"] == "gradient_mediator"
            )
        ),
        "canonical_readout_symmetrization_preserves_discriminator_signs": bool(
            canonical_readout_comparison["static_compensated"][
                "reciprocal_visible_memory_force"
            ]
            < 0.0
            and canonical_readout_comparison["gradient_mediator"][
                "reciprocal_visible_memory_force"
            ]
            > 0.0
        ),
        "readout_amplitude_offset_matches_finite_tail_mass": (
            maximum_readout_mass_residual < 2.0e-8
        ),
        "static_arm_has_one_full_memory_unstable_radius": (
            len(roots["static_compensated"]["stationary_points"]) == 1
            and set(
                roots["static_compensated"]["stationary_points"][0][
                    "full_memory_stabilities"
                ].values()
            )
            == {"unstable"}
        ),
        "gradient_arm_has_full_memory_barrier_then_stable_minimum": (
            all(
                [
                    row["full_memory_stabilities"][orientation]
                    for row in roots["gradient_mediator"]["stationary_points"]
                ]
                == ["unstable", "stable"]
                for orientation in orientations
            )
        ),
        "force_is_negative_pair_energy_gradient": maximum_force_energy_error < 2.0e-8,
        "action_reaction_exact": maximum_action_reaction_error < 1.0e-13,
        "full_memory_root_residuals_resolved": maximum_root_residual_ratio < 1.0e-6,
        "point_limit_converges_at_second_order": (
            min(point_limit_orders) > 1.95 and max(point_limit_orders) < 2.05
        ),
    }
    return {
        "schema": "emergenz-knoten.quasistatic-two-knot-discrimination.v1",
        "decision": (
            "quasistatic-discrimination-pass-pointlike-full-memory"
            if all(gates.values())
            else "quasistatic-discrimination-fail"
        ),
        "gates": gates,
        "checkpoint": source.relative_to(ROOT).as_posix(),
        "checkpoint_update_index": checkpoint.update_index,
        "formation_seed": checkpoint.formation_seed,
        "memory_weight_mass": float(np.sum(state.weights)),
        "memory_rms_radius": rms_radius,
        "fixed_discrimination_radius": DISCRIMINATION_RADIUS,
        "fixed_radii": list(FIXED_RADII),
        "static_parameters": STATIC_PARAMETERS,
        "gradient_mediator_parameters": {
            "spectral_shape": SPECTRAL_SHAPE,
            "memory_loading": MEMORY_LOADING,
            "decay_rate_ratio": 1.0,
        },
        "zero_modes": {
            "static_integral_coefficient": static_integral,
            "gradient_mediator": [gradient_zero.real, gradient_zero.imag],
            "direct_source_control": [direct_zero.real, direct_zero.imag],
        },
        "cross_off": {
            "energy": cross_off.energy,
            "force_on_first": cross_off.force_on_first.tolist(),
            "force_on_second": cross_off.force_on_second.tolist(),
        },
        "force_at_discrimination_radius": identity_at_discriminator,
        "canonical_readout_comparison_at_discrimination_radius": (
            canonical_readout_comparison
        ),
        "finite_tail_mass_relative_difference": finite_tail_mass_difference,
        "maximum_readout_mass_residual": maximum_readout_mass_residual,
        "roots": roots,
        "fixed_force_rows": fixed_rows,
        "maximum_force_energy_relative_error": maximum_force_energy_error,
        "maximum_action_reaction_absolute_error": maximum_action_reaction_error,
        "maximum_root_shift_ratio": maximum_root_shift_ratio,
        "maximum_orientation_spread_ratio": maximum_orientation_spread_ratio,
        "maximum_root_residual_ratio": maximum_root_residual_ratio,
        "squared_compactness_ratio": compactness_ratio,
        "point_limit_rows": point_limit_rows,
        "minimum_point_limit_order": min(point_limit_orders),
        "maximum_point_limit_order": max(point_limit_orders),
        "claim_limits": {
            "dynamics": "no state is advanced; mediator equilibration is not simulated",
            "shape": "rigid frozen clouds cannot test shape evolution",
            "gain": "force amplitudes are not compared across model families",
            "selection": "no observed target response selects either law",
            "generality": "one tracked d=3 formation seed; point-limit validation only",
            "dimension": "the 3D inverse transform is supplied, not selected",
            "scale_matching": "ell=sigma_rep=1 is imposed, not inferred",
            "cross_readout": (
                "memory-memory energy is the primary reciprocal source-density law; "
                "a symmetrized visible-memory readout is a separate comparison"
            ),
        },
    }


def _write_figure(path: Path, result: dict[str, Any]) -> None:
    laws = _laws()
    radii = np.linspace(2.0, 13.0, 1000)
    colors = {
        "static_compensated": "#2b6f77",
        "gradient_mediator": "#a33f32",
        "direct_source_control": "#6b4c8a",
    }
    labels = {
        "static_compensated": "static compensated",
        "gradient_mediator": "gradient mediator",
        "direct_source_control": "direct-source control",
    }
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.35), constrained_layout=True)
    for name, (energy, derivative) in laws.items():
        energy_values = np.asarray(energy(radii), dtype=float)
        force_values = -np.asarray(derivative(radii), dtype=float)
        axes[0].plot(
            radii,
            energy_values / np.max(np.abs(energy_values)),
            color=colors[name],
            label=labels[name],
        )
        axes[1].plot(
            radii,
            force_values / np.max(np.abs(force_values)),
            color=colors[name],
            label=labels[name],
        )
    for axis in axes[:2]:
        axis.axhline(0.0, color="#555f6b", linewidth=0.8)
        axis.axvline(
            DISCRIMINATION_RADIUS,
            color="#20252b",
            linestyle="--",
            linewidth=1.0,
        )
        axis.set_xlabel(r"separation $R/\ell$")
    axes[0].set_ylabel("pair energy, normalized per arm")
    axes[0].set_title("Fixed pair-energy geometries")
    axes[1].set_ylabel("radial force, normalized per arm")
    axes[1].set_title("Opposite prediction at R = 5")
    axes[1].legend(frameon=False, fontsize=8)

    identity_rows = [
        row
        for row in result["fixed_force_rows"]
        if row["orientation"] == "identity"
        and row["radius"] in (2.8, 5.0, 8.0, 12.0)
    ]
    plot_radii = [2.8, 5.0, 8.0, 12.0]
    x = np.arange(len(plot_radii), dtype=float)
    width = 0.25
    for offset, name in zip((-width, 0.0, width), laws, strict=True):
        values = [
            next(
                row["full_memory_force"]
                for row in identity_rows
                if row["model"] == name and row["radius"] == radius
            )
            for radius in plot_radii
        ]
        signs = np.sign(values)
        axes[2].bar(
            x + offset,
            signs,
            width=width,
            color=colors[name],
            label=labels[name],
        )
    axes[2].axhline(0.0, color="#555f6b", linewidth=0.8)
    axes[2].set_xticks(x, [f"{radius:g}" for radius in plot_radii])
    axes[2].set_ylim(-1.25, 1.25)
    axes[2].set_yticks([-1, 0, 1], ["inward", "zero", "outward"])
    axes[2].set_xlabel(r"separation $R/\ell$")
    axes[2].set_title("Full-memory force signs")
    fig.suptitle("Quasistatic two-knot discrimination on the N=100M checkpoint")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=190)
    plt.close(fig)


def _write_report(path: Path, result: dict[str, Any], figure: Path) -> None:
    gate_rows = "\n".join(
        f"| `{name}` | {'pass' if passed else 'fail'} |"
        for name, passed in result["gates"].items()
    )
    root_rows = []
    for model, payload in result["roots"].items():
        for index, row in enumerate(payload["stationary_points"], start=1):
            values = list(row["full_memory_radii"].values())
            root_rows.append(
                "| {} | {} | {:.9g} | {:.9g}..{:.9g} | {} | {:.3e} |".format(
                    model,
                    index,
                    row["point_radius"],
                    min(values),
                    max(values),
                    "/".join(sorted(set(row["full_memory_stabilities"].values()))),
                    row["maximum_relative_shift"],
                )
            )
    force_rows = []
    for radius in (2.8, 5.0, 8.0, 12.0):
        values = {
            row["model"]: row["full_memory_force"]
            for row in result["fixed_force_rows"]
            if row["orientation"] == "identity" and row["radius"] == radius
        }
        force_rows.append(
            "| {:.6g} | {:+.6e} | {:+.6e} | {:+.6e} |".format(
                radius,
                values["static_compensated"],
                values["gradient_mediator"],
                values["direct_source_control"],
            )
        )
    text = f"""# Quasistatic Two-Knot Discrimination

Date: 2026-08-12. Decision: **`{result['decision']}`**.

## Fixed review scope

This is the first P3.8c stage after the rigorous P3.8a/b review. It uses the
checksum-validated `d=3`, seed-1 scalar checkpoint at `N=100,000,000`. Both
complete retained memory clouds are translated rigidly. No trajectory or
mediator state is advanced, no coupling gain is calibrated and no parameter is
swept.

The test compares three fixed source-source pair laws:

1. the existing exact-zero-integral static compensated Gaussian kernel;
2. the reviewed adjoint-gradient mediator susceptibility with
   `(delta,mu)=(-1.9,0.3)` and pair energy `U=-K_eff`;
3. the direct-source susceptibility as a nonzero-zero-mode architecture control.

The a priori model-derived common discriminator is `R/ell=5`: the static arm
predicts inward force and the gradient mediator predicts outward force. Raw
amplitudes between model families are not compared.

![Quasistatic two-knot discrimination]({figure.as_posix()})

## Force signs

Positive means increasing separation (outward); negative means inward.

| R/ell | static compensated | gradient mediator | direct-source control |
|---:|---:|---:|---:|
{chr(10).join(force_rows)}

At the fixed `R/ell=5`, the full-memory forces are
`{result['force_at_discrimination_radius']['static_compensated']:+.6e}` and
`{result['force_at_discrimination_radius']['gradient_mediator']:+.6e}`. Their
opposite signs make a future observed two-node response discriminating without
gain matching.

The primary reciprocal energy couples the two retained source densities. That
is a new cross-channel choice, not the canonical one-visible-point readout. A
separate reciprocal symmetrization of the canonical visible-to-foreign-memory
readout preserves the same discriminator signs; its relative force differences
from the source-density law are
`{result['canonical_readout_comparison_at_discrimination_radius']['static_compensated']['relative_difference']:.3e}`
(static) and
`{result['canonical_readout_comparison_at_discrimination_radius']['gradient_mediator']['relative_difference']:.3e}`
(gradient mediator). The common amplitude offset is explained to within
`{result['maximum_readout_mass_residual']:.3e}` by the finite retained mass
`M_H={result['memory_weight_mass']:.9f}`: the point limit scales as `M_H^2`
for memory-memory and as `M_H` for visible-memory coupling. Compactness
preserves the radial profiles and signs; it does not make the two cross-channel
definitions identical.

## Stationary radii

| model | root | point prediction | full-memory range over 3 orientations | full-memory type | max relative shift |
|---|---:|---:|---:|---|---:|
{chr(10).join(root_rows)}

The static compensated arm has only an unstable separation in the fixed
range. The gradient mediator has a full-memory unstable barrier followed by a
stable quasistatic pair-energy minimum. The direct-source control also has shells,
showing that shells alone do not establish neutrality; unlike the gradient
arm, its Fourier zero mode is nonzero.

## Final review gates

| gate | result |
|---|---|
{gate_rows}

Maximum force-versus-energy-gradient error:
`{result['maximum_force_energy_relative_error']:.3e}`. Maximum action/reaction
residual: `{result['maximum_action_reaction_absolute_error']:.3e}`. Maximum
full-memory root shift from the point prediction:
`{result['maximum_root_shift_ratio']:.3e}`; maximum normalized root residual:
`{result['maximum_root_residual_ratio']:.3e}`. Point-limit convergence order over
internally scaled copies of the same stored cloud:
`{result['minimum_point_limit_order']:.6f}..{result['maximum_point_limit_order']:.6f}`.

## Interpretation

This is a **mechanism-discriminability and implementation pass**, not a
mechanism-selection pass. The complete knot is so compact
(`R_mem={result['memory_rms_radius']:.6g}` in units where `ell=1`) that its
finite-memory force differs from the point-source prediction only at the
expected quadratic multipole scale. The result therefore validates the
source-density convolution and proves that the two fixed architectures make
opposite predictions at one fixed, model-derived separation. It does not show
that the dynamic gradient mediator exists, equilibrates, or stabilizes a
moving two-knot state.

The comparison also imposes `ell=sigma_rep=1`; no observation identifies that
cross-family scale matching. It is therefore a conditional discriminator, not
evidence that either physical scale is selected.

A dynamic continuation now requires an explicit time discretization of the
new `(m,p)` field, one shared interaction energy, and source-work plus damping
balance. `reversible-off` becomes a useful control only there: in static
equilibrium a first-order relaxation and a reversible second-order field share
the same susceptibility. No dynamic gain, mobility or timestep is inferred by
this frozen test.

No claim about charge, spin, particles, quantum dynamics or selection of three
dimensions follows.

## Reproducibility

- checkpoint: `{result['checkpoint']}`;
- script: `experiments/current/memory/synchronization/reciprocity/quasistatic_two_knot_discrimination.py`;
- packages: `src/emergenz_knoten/gradient_mediator.py`,
  `src/emergenz_knoten/quasistatic_pair.py`;
- git revision before generated changes: `{_git_output(['rev-parse', 'HEAD'])}`;
- generated: `{datetime.now(UTC).isoformat()}`.

This audit was not sealed in a separate immutable preregistration commit. The
physical arms, radii and `R/ell=5` discriminator were fixed before the final
checkpoint evaluation; numerical validation gates were corrected during code
review and are documented in the P3.8 review report.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    args = parse_args()
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    result = run_audit(args.checkpoint)
    _write_figure(figure, result)
    relative_figure = Path("../../../figures/draft/memory") / figure.name
    _write_report(report, result, relative_figure)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
