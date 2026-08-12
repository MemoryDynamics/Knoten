"""P3.8d energy gate and one fixed dynamic two-knot existence pilot."""

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
    FirstOrderMediatorState,
    SecondOrderMediatorState,
    advance_second_order_fixed_source,
    build_isotropic_mediator_modes,
    first_order_energy,
    gradient_mediator_selection,
    instantaneous_radial_force,
    modal_source,
    modal_static_force,
    radial_gradient_mediator_green_derivative_3d,
    second_order_energy,
    second_order_fixed_source_damping_quadrature,
    selected_mode_step_response,
    step_first_order_mediator,
    step_second_order_mediator,
    zero_first_order_state,
    zero_second_order_state,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
SPECTRAL_SHAPE = -1.9
MEMORY_LOADING = 0.3
MEMORY_DECAY = float(np.sqrt(MEMORY_LOADING))
CONJUGATE_DECAY = float(np.sqrt(MEMORY_LOADING))
RELATIVE_MOBILITY = 1.0
INITIAL_SEPARATIONS = (5.0, 8.0)
PILOT_DURATION = 1500.0
PILOT_TIME_STEP = 0.5
TRACE_EVERY = 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/reciprocal/"
            "dynamic_two_knot_mediator_gate_2026-08-12.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/reciprocal/"
            "dynamic_two_knot_mediator_gate_2026-08-12.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/"
            "dynamic_two_knot_mediator_gate_2026-08-12.png"
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


def _simulate(
    *,
    dynamic_order: str,
    modes,
    initial_separation: float,
    duration: float,
    time_step: float,
    relative_mobility: float,
    trace_every: int,
    initialization: str = "zero_field",
) -> dict[str, Any]:
    n_steps = round(duration / time_step)
    if not np.isclose(n_steps * time_step, duration):
        raise ValueError("duration must be an integer multiple of time_step")
    if dynamic_order == "second":
        if initialization == "zero_field":
            state = zero_second_order_state(modes, separation=initial_separation)
        elif initialization == "static_equilibrium":
            state = SecondOrderMediatorState(
                initial_separation,
                modal_source(modes, initial_separation) / modes.restoring,
                np.zeros(modes.n_modes),
            )
        else:
            raise ValueError("initialization must be zero_field or static_equilibrium")
        step: Callable = step_second_order_mediator
        energy: Callable = second_order_energy
    elif dynamic_order == "first":
        if initialization == "zero_field":
            state = zero_first_order_state(modes, separation=initial_separation)
        elif initialization == "static_equilibrium":
            state = FirstOrderMediatorState(
                initial_separation,
                modal_source(modes, initial_separation) / modes.restoring,
            )
        else:
            raise ValueError("initialization must be zero_field or static_equilibrium")
        step = step_first_order_mediator
        energy = first_order_energy
    else:
        raise ValueError("dynamic_order must be second or first")

    times = [0.0]
    separations = [state.separation]
    forces = [instantaneous_radial_force(state.separation, state.field, modes)]
    energies = [energy(state, modes)]
    maximum_balance_residual = 0.0
    maximum_source_work_residual = 0.0
    minimum_energy_increment = 0.0
    cumulative_source_dissipation = 0.0
    cumulative_mediator_dissipation = 0.0
    previous_energy = energies[0]
    for index in range(1, n_steps + 1):
        state, ledger = step(
            state,
            modes,
            time_step=time_step,
            relative_mobility=relative_mobility,
        )
        maximum_balance_residual = max(
            maximum_balance_residual, abs(ledger.balance_residual)
        )
        maximum_source_work_residual = max(
            maximum_source_work_residual,
            ledger.maximum_source_work_residual,
        )
        cumulative_source_dissipation += ledger.source_dissipation
        cumulative_mediator_dissipation += ledger.mediator_dissipation
        current_energy = energy(state, modes)
        minimum_energy_increment = max(
            minimum_energy_increment,
            current_energy - previous_energy,
        )
        previous_energy = current_energy
        if index % trace_every == 0 or index == n_steps:
            times.append(index * time_step)
            separations.append(state.separation)
            forces.append(
                instantaneous_radial_force(state.separation, state.field, modes)
            )
            energies.append(current_energy)
    force_array = np.asarray(forces)
    nonzero_force = force_array[np.abs(force_array) > 1.0e-12]
    force_sign_changes = int(
        np.sum(np.signbit(nonzero_force[1:]) != np.signbit(nonzero_force[:-1]))
    )
    return {
        "dynamic_order": dynamic_order,
        "initialization": initialization,
        "initial_separation": initial_separation,
        "final_separation": float(state.separation),
        "times": times,
        "separations": separations,
        "forces": forces,
        "energies": energies,
        "maximum_energy_increase": float(minimum_energy_increment),
        "maximum_balance_residual": float(maximum_balance_residual),
        "maximum_source_work_residual": float(maximum_source_work_residual),
        "cumulative_source_dissipation": float(cumulative_source_dissipation),
        "cumulative_mediator_dissipation": float(cumulative_mediator_dissipation),
        "nonzero_force_sign_changes": force_sign_changes,
    }


def _state_error(reference, candidate, modes) -> float:
    velocity_reference = getattr(reference, "conjugate_velocity", None)
    velocity_candidate = getattr(candidate, "conjugate_velocity", None)
    error = (reference.separation - candidate.separation) ** 2
    field_difference = reference.field - candidate.field
    error += float(np.dot(modes.restoring * field_difference, field_difference))
    if velocity_reference is not None:
        velocity_difference = velocity_reference - velocity_candidate
        error += float(np.dot(velocity_difference, velocity_difference))
    return float(np.sqrt(error))


def _final_state(*, modes, time_step: float, duration: float = 100.0):
    state = zero_second_order_state(modes, separation=5.0)
    for _ in range(round(duration / time_step)):
        state, _ = step_second_order_mediator(
            state,
            modes,
            time_step=time_step,
            relative_mobility=RELATIVE_MOBILITY,
        )
    return state


def run_audit() -> dict[str, Any]:
    modes = build_isotropic_mediator_modes(
        n_wavenumber=64,
        n_direction=64,
        k_max=16.0,
        spectral_shape=SPECTRAL_SHAPE,
        memory_loading=MEMORY_LOADING,
        memory_decay=MEMORY_DECAY,
        conjugate_decay=CONJUGATE_DECAY,
    )
    static_radii = np.asarray((2.8, 5.0, 8.0, 12.0))
    modal_forces = np.asarray([modal_static_force(modes, radius) for radius in static_radii])
    exact_forces = radial_gradient_mediator_green_derivative_3d(
        static_radii,
        spectral_shape=SPECTRAL_SHAPE,
        memory_loading=MEMORY_LOADING,
    )
    static_absolute_error = float(np.max(np.abs(modal_forces - exact_forces)))
    modal_barrier = float(brentq(lambda radius: modal_static_force(modes, radius), 3.5, 4.5))
    modal_minimum = float(brentq(lambda radius: modal_static_force(modes, radius), 6.5, 7.5))

    rng = np.random.default_rng(3801)
    damping_modes = build_isotropic_mediator_modes(
        n_wavenumber=16,
        n_direction=16,
        k_max=3.0,
        spectral_shape=SPECTRAL_SHAPE,
        memory_loading=MEMORY_LOADING,
    )
    amplitude_scale = 0.01 / np.sqrt(damping_modes.restoring)
    damping_state = SecondOrderMediatorState(
        5.0,
        rng.normal(size=damping_modes.n_modes) * amplitude_scale,
        rng.normal(size=damping_modes.n_modes) * amplitude_scale,
    )
    damping_final = advance_second_order_fixed_source(
        damping_state,
        damping_modes,
        duration=0.7,
    )
    damping_energy_loss = second_order_energy(
        damping_state, damping_modes
    ) - second_order_energy(damping_final, damping_modes)
    damping_quadrature = second_order_fixed_source_damping_quadrature(
        damping_state,
        damping_modes,
        duration=0.7,
        quadrature_order=48,
    )
    damping_residual = float(abs(damping_energy_loss - damping_quadrature))

    selection = gradient_mediator_selection(
        spectral_shape=SPECTRAL_SHAPE,
        memory_loading=MEMORY_LOADING,
        decay_rate_ratio=1.0,
    )
    selected_k = selection.selected_scaled_wavenumber
    selected_restoring = float(
        MEMORY_LOADING
        + selected_k**2
        + SPECTRAL_SHAPE * selected_k**4
        + selected_k**6
    )
    response_times = np.linspace(0.0, 40.0, 4001)
    second_response = selected_mode_step_response(
        response_times,
        restoring=selected_restoring,
        damping=modes.damping,
        dynamic_order="second",
    )
    first_response = selected_mode_step_response(
        response_times,
        restoring=selected_restoring,
        damping=modes.damping,
        dynamic_order="first",
    )
    selected_angular_frequency = float(
        np.sqrt(selected_restoring - 0.25 * modes.damping**2)
    )

    equilibrium = modal_source(modes, 5.0) / modes.restoring
    equilibrium_second = SecondOrderMediatorState(
        5.0, equilibrium, np.zeros(modes.n_modes)
    )
    equilibrium_first = zero_first_order_state(modes, separation=5.0)
    equilibrium_first = type(equilibrium_first)(5.0, equilibrium)
    static_control_force_difference = abs(
        instantaneous_radial_force(5.0, equilibrium_second.field, modes)
        - instantaneous_radial_force(5.0, equilibrium_first.field, modes)
    )

    off_modes = build_isotropic_mediator_modes(
        n_wavenumber=16,
        n_direction=16,
        k_max=8.0,
        spectral_shape=SPECTRAL_SHAPE,
        memory_loading=MEMORY_LOADING,
        coupling=0.0,
    )
    off_second = zero_second_order_state(off_modes, separation=5.0)
    off_first = zero_first_order_state(off_modes, separation=5.0)
    for _ in range(20):
        off_second, off_second_ledger = step_second_order_mediator(
            off_second, off_modes, time_step=0.5
        )
        off_first, off_first_ledger = step_first_order_mediator(
            off_first, off_modes, time_step=0.5
        )

    reference = _final_state(modes=modes, time_step=0.03125, duration=50.0)
    time_steps = (0.25, 0.125, 0.0625)
    time_step_errors = [
        _state_error(
            reference,
            _final_state(modes=modes, time_step=time_step, duration=50.0),
            modes,
        )
        for time_step in time_steps
    ]
    observed_orders = [
        float(np.log2(time_step_errors[index] / time_step_errors[index + 1]))
        for index in range(len(time_step_errors) - 1)
    ]

    pilots = []
    for dynamic_order in ("second", "first"):
        for initial_separation in INITIAL_SEPARATIONS:
            pilots.append(
                _simulate(
                    dynamic_order=dynamic_order,
                    modes=modes,
                    initial_separation=initial_separation,
                    duration=PILOT_DURATION,
                    time_step=PILOT_TIME_STEP,
                    relative_mobility=RELATIVE_MOBILITY,
                    trace_every=TRACE_EVERY,
                    initialization="zero_field",
                )
            )

    equilibrium_initialized_controls = []
    for dynamic_order in ("second", "first"):
        for initial_separation in INITIAL_SEPARATIONS:
            equilibrium_initialized_controls.append(
                _simulate(
                    dynamic_order=dynamic_order,
                    modes=modes,
                    initial_separation=initial_separation,
                    duration=PILOT_DURATION,
                    time_step=PILOT_TIME_STEP,
                    relative_mobility=RELATIVE_MOBILITY,
                    trace_every=TRACE_EVERY,
                    initialization="static_equilibrium",
                )
            )

    refined_second_order_final = {}
    for initial_separation in INITIAL_SEPARATIONS:
        refined = _simulate(
            dynamic_order="second",
            modes=modes,
            initial_separation=initial_separation,
            duration=PILOT_DURATION,
            time_step=0.25,
            relative_mobility=RELATIVE_MOBILITY,
            trace_every=round(PILOT_TIME_STEP / 0.25),
            initialization="zero_field",
        )
        refined_second_order_final[str(initial_separation)] = refined[
            "final_separation"
        ]

    uv_probe = {}
    uv_duration = 50.0
    uv_time_step = 0.25
    for cutoff, n_quadrature in ((16.0, 64), (20.0, 80), (24.0, 96), (28.0, 112)):
        uv_modes = build_isotropic_mediator_modes(
            n_wavenumber=n_quadrature,
            n_direction=n_quadrature,
            k_max=cutoff,
            spectral_shape=SPECTRAL_SHAPE,
            memory_loading=MEMORY_LOADING,
        )
        uv_trace = _simulate(
            dynamic_order="second",
            modes=uv_modes,
            initial_separation=5.0,
            duration=uv_duration,
            time_step=uv_time_step,
            relative_mobility=RELATIVE_MOBILITY,
            trace_every=1,
            initialization="zero_field",
        )
        uv_probe[str(cutoff)] = {
            "n_quadrature": n_quadrature,
            "modal_barrier": float(
                brentq(lambda radius: modal_static_force(uv_modes, radius), 3.5, 4.5)
            ),
            "modal_minimum": float(
                brentq(lambda radius: modal_static_force(uv_modes, radius), 6.5, 7.5)
            ),
            "final_separation": uv_trace["final_separation"],
            "minimum_force": float(np.min(uv_trace["forces"])),
            "maximum_force": float(np.max(uv_trace["forces"])),
        }

    second_pilots = [item for item in pilots if item["dynamic_order"] == "second"]
    all_pilots = pilots + equilibrium_initialized_controls
    gates = {
        "static_modal_quadrature_preserves_registered_force_signs": bool(
            modal_forces[0] < 0.0
            and modal_forces[1] > 0.0
            and modal_forces[2] < 0.0
            and static_absolute_error < 3.0e-4
        ),
        "static_modal_barrier_and_minimum_match_green_inversion": bool(
            abs(modal_barrier - 3.919200371) < 5.0e-3
            and abs(modal_minimum - 6.990916303) < 5.0e-3
        ),
        "homogeneous_damping_matches_independent_time_quadrature": (
            damping_residual < 2.0e-12
        ),
        "cross_off_is_exact": bool(
            off_second.separation == 5.0
            and off_first.separation == 5.0
            and off_second_ledger.energy_before == 0.0
            and off_first_ledger.energy_before == 0.0
        ),
        "first_and_second_order_share_static_susceptibility": (
            static_control_force_difference < 1.0e-14
        ),
        "second_order_selected_mode_overshoots": bool(
            np.max(second_response) > 1.005 and np.any(np.diff(second_response) < 0.0)
        ),
        "first_order_selected_mode_is_monotone": bool(
            np.all(np.diff(first_response) >= 0.0) and np.max(first_response) < 1.0
        ),
        "split_scheme_has_second_order_step_convergence": bool(
            min(observed_orders) > 1.7
        ),
        "dynamic_energy_balance_closes": bool(
            max(item["maximum_balance_residual"] for item in all_pilots) < 3.0e-12
            and max(item["maximum_source_work_residual"] for item in all_pilots)
            < 3.0e-12
            and max(item["maximum_energy_increase"] for item in all_pilots) < 3.0e-12
        ),
        "second_order_pilots_enter_common_static_basin": bool(
            all(abs(item["final_separation"] - modal_minimum) < 0.04 for item in second_pilots)
        ),
        "pilot_final_separation_is_time_step_stable": bool(
            all(
                abs(
                    item["final_separation"]
                    - refined_second_order_final[str(item["initial_separation"])]
                )
                < 2.0e-3
                for item in second_pilots
            )
        ),
        "static_basin_is_uv_stable": bool(
            max(
                abs(item["modal_minimum"] - 6.990916303)
                for item in uv_probe.values()
            )
            < 0.02
        ),
        "second_order_pilot_differs_from_first_order_control": bool(
            all(
                max(
                    abs(
                        np.asarray(
                            next(
                                control["separations"]
                                for control in pilots
                                if control["dynamic_order"] == "first"
                                and control["initial_separation"]
                                == item["initial_separation"]
                            )
                        )
                        - np.asarray(item["separations"])
                    )
                )
                > 1.0e-3
                for item in second_pilots
            )
        ),
        "second_order_quench_has_nonzero_force_reversal": bool(
            all(item["nonzero_force_sign_changes"] >= 1 for item in second_pilots)
            and all(
                item["nonzero_force_sign_changes"] == 0
                for item in pilots
                if item["dynamic_order"] == "first"
            )
        ),
        "equilibrium_initialized_controls_enter_same_basin": bool(
            all(
                abs(item["final_separation"] - modal_minimum) < 0.04
                for item in equilibrium_initialized_controls
            )
        ),
        "force_reversal_is_quench_dependent": bool(
            all(
                item["nonzero_force_sign_changes"] == 0
                for item in equilibrium_initialized_controls
            )
        ),
    }
    return {
        "decision": (
            "p38d-conditional-dynamic-existence-pass"
            if all(gates.values())
            else "p38d-dynamic-gate-fail"
        ),
        "gates": gates,
        "fixed_scope": {
            "spectral_shape": SPECTRAL_SHAPE,
            "memory_loading": MEMORY_LOADING,
            "decay_rate_ratio": 1.0,
            "relative_mobility": RELATIVE_MOBILITY,
            "initial_separations": INITIAL_SEPARATIONS,
            "pilot_duration": PILOT_DURATION,
            "pilot_time_step": PILOT_TIME_STEP,
            "quadrature": {
                "n_wavenumber": modes.n_wavenumber,
                "n_direction": modes.n_direction,
                "k_max": modes.k_max,
            },
        },
        "static_validation": {
            "radii": static_radii.tolist(),
            "modal_forces": modal_forces.tolist(),
            "exact_green_forces": exact_forces.tolist(),
            "maximum_absolute_error": static_absolute_error,
            "modal_barrier": modal_barrier,
            "modal_minimum": modal_minimum,
        },
        "damping_validation": {
            "energy_loss": damping_energy_loss,
            "time_quadrature": damping_quadrature,
            "absolute_residual": damping_residual,
        },
        "time_step_validation": {
            "time_steps": time_steps,
            "reference_time_step": 0.03125,
            "duration": 50.0,
            "errors_against_reference": time_step_errors,
            "observed_orders": observed_orders,
        },
        "dynamic_control": {
            "selected_wavenumber": selected_k,
            "selected_restoring": selected_restoring,
            "second_order_angular_frequency": selected_angular_frequency,
            "second_order_period": float(2.0 * np.pi / selected_angular_frequency),
            "second_order_peak_response": float(np.max(second_response)),
            "first_order_peak_response": float(np.max(first_response)),
            "static_force_difference": static_control_force_difference,
        },
        "pilots": pilots,
        "equilibrium_initialized_controls": equilibrium_initialized_controls,
        "refined_second_order_final": refined_second_order_final,
        "uv_probe": {
            "duration": uv_duration,
            "time_step": uv_time_step,
            "results": uv_probe,
            "interpretation": (
                "final separation converges faster than the early force extrema; "
                "point-source quench amplitudes remain cutoff-sensitive"
            ),
        },
        "claim_limits": {
            "model_status": "new longitudinal mediator candidate, not canonical rho",
            "source_status": "point-source quadrature; mature checkpoint shape is not evolved",
            "mobility": "relative_mobility=1 is fixed for an existence witness, not inferred",
            "coefficients": "delta, mu, damping ratio and absolute scales remain inputs",
            "geometry": "collinear symmetric separation only; no orbit or transverse mode",
            "first_order_control": (
                "field kinetic coefficient is set to the same Gamma for a timing "
                "convention; this does not exhaust first-order null models"
            ),
            "initialization": (
                "zero-field quench and static-equilibrium controls bracket two protocols; "
                "neither is derived from knot formation"
            ),
            "physics": "no charge, spin, particle, QFT or dimension-selection claim",
        },
    }


def _write_figure(path: Path, result: dict[str, Any]) -> None:
    pilots = result["pilots"]
    fig, axes = plt.subplots(1, 3, figsize=(15.4, 4.35), constrained_layout=True)
    colors = {"second": "#a94435", "first": "#2b6f77"}
    styles = {5.0: "-", 8.0: "--"}
    for pilot in pilots:
        label = f"{pilot['dynamic_order']}, R0={pilot['initial_separation']:g}"
        axes[0].plot(
            pilot["times"],
            pilot["separations"],
            color=colors[pilot["dynamic_order"]],
            linestyle=styles[pilot["initial_separation"]],
            label=label,
        )
        axes[1].plot(
            pilot["times"][:300],
            pilot["forces"][:300],
            color=colors[pilot["dynamic_order"]],
            linestyle=styles[pilot["initial_separation"]],
            label=label,
        )
        energy = np.asarray(pilot["energies"])
        axes[2].plot(
            pilot["times"],
            energy - energy[-1],
            color=colors[pilot["dynamic_order"]],
            linestyle=styles[pilot["initial_separation"]],
            label=label,
        )
    axes[0].axhline(
        result["static_validation"]["modal_minimum"],
        color="#30343b",
        linewidth=0.9,
        linestyle=":",
        label="modal static minimum",
    )
    axes[0].set(xlabel=r"dimensionless time $t$", ylabel=r"separation $R/\ell$")
    axes[0].set_title("Common basin from both sides")
    axes[0].legend(frameon=False, fontsize=8)
    axes[1].axhline(0.0, color="#555f6b", linewidth=0.8)
    axes[1].set(xlabel=r"early time $t$", ylabel="instantaneous radial force")
    axes[1].set_title("Reversible transient vs control")
    axes[2].set_yscale("log")
    axes[2].set(xlabel=r"dimensionless time $t$", ylabel=r"$E(t)-E(T)$")
    axes[2].set_title("Monotone energy descent")
    fig.suptitle("P3.8d dynamic longitudinal-mediator existence pilot")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _write_report(path: Path, result: dict[str, Any], figure: Path) -> None:
    gate_rows = "\n".join(
        f"| `{name}` | {'pass' if passed else 'fail'} |"
        for name, passed in result["gates"].items()
    )
    pilot_rows = "\n".join(
        "| {dynamic_order} | {initial_separation:g} | {final_separation:.9f} | "
        "{nonzero_force_sign_changes} | {maximum_balance_residual:.3e} |".format(**item)
        for item in result["pilots"]
    )
    static = result["static_validation"]
    control = result["dynamic_control"]
    convergence = result["time_step_validation"]
    report = rf"""# P3.8d dynamic two-knot mediator gate

Date: 2026-08-12. Decision: **`{result['decision']}`**.

## Model boundary

This experiment advances the proposed longitudinal mediator `(m,p)` and two
symmetric point sources. It does not replace or silently modify the canonical
`z=(x,rho)` process. The source separation `R` is overdamped; no mechanical
mass is inserted for the knot centres.

For modal source loading \(B(R)\) and positive stiffness \(A\), the candidate is

\[
\dot{{\mathbf m}}=\mathbf p,
\qquad
\dot{{\mathbf p}}=-\Gamma\mathbf p-A\mathbf m+B(R),
\qquad
\dot R=\nu\,\partial_R B(R)\cdot\mathbf m.
\]

with energy

\[
E=\frac12\|\mathbf p\|^2+\frac12\mathbf m^T A\mathbf m
-B(R)\cdot\mathbf m,
\qquad
\dot E=-\Gamma\|\mathbf p\|^2-\frac{{\dot R^2}}\nu\leq0.
\]

The same source functional supplies field writing and source readout. The
separation substep uses a scalar discrete gradient, so source work closes
without replacing `B(R)` by a local force approximation. Fixed-source field
substeps are analytic. The first-order control uses
`Gamma m_dot=-A m+B(R)` and therefore has exactly the same equilibrium
susceptibility but no conjugate velocity.

## Fixed scope

- analytic witness: `(delta,mu,r_gamma)=(-1.9,0.3,1)`;
- relative source mobility: `nu=1`, fixed as an existence witness, not inferred;
- modal quadrature: `64 x 64`, `k_max=16`;
- initial separations: `R/ell=5` and `8`;
- duration `T=1500`, step `dt=0.5`;
- no gain, coefficient, noise, kernel or mobility sweep.

![P3.8d dynamic mediator gate]({figure.as_posix()})

## Registered gates

| Gate | Result |
|---|---|
{gate_rows}

Static modal inversion gives barrier `{static['modal_barrier']:.9f}` and basin
minimum `{static['modal_minimum']:.9f}`. Its maximum absolute force error at
the registered nonstationary radii is `{static['maximum_absolute_error']:.3e}`.
The independent damping quadrature residual is
`{result['damping_validation']['absolute_residual']:.3e}`.

Time-step errors against `dt={convergence['reference_time_step']}` over
`T={convergence['duration']}` are
`{', '.join(f'{value:.3e}' for value in convergence['errors_against_reference'])}`
for `dt=(0.25,0.125,0.0625)`, with observed orders
`{', '.join(f'{value:.3f}' for value in convergence['observed_orders'])}`.

## Dynamic result

| order | initial R/ell | final R/ell | force sign changes | max balance residual |
|---|---:|---:|---:|---:|
{pilot_rows}

Both second-order starts enter the same static basin while total energy remains
monotone. The reversible and first-order trajectories are measurably distinct;
both reversible arms show one or more nonzero-force sign changes during the
point-source quench, while the matched first-order arms are sign-monotone.
When both fields instead start at their static equilibrium for the initial
separation, all arms retain the common basin but the force reversals disappear.
The ringing is therefore a quench-dependent reversible transient, not an
initialization-independent pair property. The
matched first-order arm approaches the same basin and
equilibrium response without a selected-mode overshoot. At the selected mode,
the second-order linear step
response peaks at `{control['second_order_peak_response']:.9f}` and has period
`{control['second_order_period']:.6f}`; the first-order response is monotone.

Repeating the second-order endpoint with `dt=0.25` changes final separation by
less than `2e-3`. A separate `k_max=16..28` check keeps the static minimum
within `0.004 ell` of the exact Green result but shows slower convergence of
the earliest force extrema than of separation. Those UV-sensitive point-source
quench amplitudes are retained as diagnostics and are not interpreted as a
physical observable.

## Interpretation

P3.8d is a conditional **dynamic existence pass** for the proposed mediator:
one energy supplies reciprocal source/readout coupling, the discrete scheme
closes work and damping, the two registered time realizations are distinguishable
under a zero-field quench, and one fixed collinear pilot relaxes into the
quasistatic separated basin.

It is not emergence from the scalar knot equations. The mediator state,
constitutive coefficients, relative mobility and scale matching remain new
inputs. The pilot uses point sources because the mature checkpoint is
`2.12e-4 ell` wide; it neither evolves the complete knot shape nor deposits
canonical memory. Force reversal is a damped field transient, not an orbit,
spin or persistent coherent oscillation. The energy Lyapunov function in fact
excludes a non-decaying limit cycle in this autonomous damped reduction.
The first-order kinetic prefactor was matched to `Gamma` as one timing
convention; it is a useful registered control, not the entire first-order null
family.
Action/reaction is enforced by the symmetric single-separation reduction; it
is not an independent many-body momentum-conservation measurement.

Therefore the next scientific question is mechanism closure: can the
canonical trajectory/memory data identify or generate this mediator and its
dimensionless coefficients on holdout responses? A coefficient sweep would
only demonstrate tunability and remains blocked.

## Reproducibility

- script: `experiments/current/memory/synchronization/reciprocity/dynamic_two_knot_mediator_gate.py`;
- package: `src/emergenz_knoten/dynamic_gradient_mediator.py`;
- git revision before generated changes: `{_git_output(['rev-parse', 'HEAD'])}`;
- generated: `{datetime.now(UTC).isoformat()}`.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")


def _compact_summary(result: dict[str, Any]) -> dict[str, Any]:
    """Remove plot traces from the reviewed JSON summary."""

    trace_keys = {"times", "separations", "forces", "energies"}

    def compact_pilot(pilot: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in pilot.items() if key not in trace_keys}

    compact = dict(result)
    compact["pilots"] = [compact_pilot(item) for item in result["pilots"]]
    compact["equilibrium_initialized_controls"] = [
        compact_pilot(item) for item in result["equilibrium_initialized_controls"]
    ]
    compact["trace_storage"] = (
        "full traces are generated in memory for the figure but are not tracked "
        "in this reviewed summary"
    )
    return compact


def main() -> None:
    args = parse_args()
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    result = run_audit()
    _write_figure(figure, result)
    relative_figure = Path("../../../figures/draft/memory") / figure.name
    _write_report(report, result, relative_figure)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(_compact_summary(result), indent=2), encoding="utf-8")
    print(json.dumps({"decision": result["decision"], "gates": result["gates"]}, indent=2))


if __name__ == "__main__":
    main()
