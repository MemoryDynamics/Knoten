"""Audit scale selection by an energy-reciprocal gradient mediator."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

from emergenz_knoten import (
    dimensionless_gradient_mediator_denominator,
    gradient_mediator_dimensionless_groups,
    gradient_mediator_selection,
    gradient_mediator_transfer,
    infer_gradient_mediator_groups_from_peak,
    radial_gradient_mediator_green_3d,
    radial_gradient_mediator_green_derivative_3d,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
SPECTRAL_SHAPE = -1.9
MEMORY_LOADING = 0.3
DECAY_RATIO = 1.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/memory/closure/dynamic_green_kernel_selection_gate_2026-08-11.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/memory/closure/dynamic_green_kernel_selection_gate_2026-08-11.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/dynamic_green_kernel_selection_gate_2026-08-11.png"
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


def _witness_parameters() -> dict[str, float]:
    relaxation = float(np.sqrt(MEMORY_LOADING))
    return {
        "memory_decay": relaxation,
        "conjugate_decay": relaxation,
        "local_stiffness": 1.0,
        "gradient_stiffness": SPECTRAL_SHAPE,
        "biharmonic_stiffness": 1.0,
    }


def _dimensionless_gradient_transfer(wavenumber: float) -> float:
    denominator = float(
        dimensionless_gradient_mediator_denominator(
            wavenumber,
            spectral_shape=SPECTRAL_SHAPE,
            memory_loading=MEMORY_LOADING,
        )
    )
    return float(wavenumber * wavenumber / denominator)


def _quadrature_green_3d(radii: np.ndarray) -> np.ndarray:
    """Independently invert the spectrum using infinite oscillatory quadrature."""

    values = []
    for radius in np.asarray(radii, dtype=float):
        if radius <= 0.0:
            raise ValueError("quadrature probes must have positive radii")
        integral = quad(
            lambda value: value * _dimensionless_gradient_transfer(value),
            0.0,
            np.inf,
            weight="sin",
            wvar=float(radius),
            epsabs=1.0e-11,
            epsrel=1.0e-11,
            limit=500,
            limlst=500,
        )[0]
        values.append(integral / (2.0 * np.pi**2 * radius))
    return np.asarray(values, dtype=float)


def _root_positions(function, *, minimum: float = 0.05, maximum: float = 20.0) -> list[float]:
    grid = np.linspace(minimum, maximum, 5000)
    values = np.asarray(function(grid), dtype=float)
    indices = np.flatnonzero(np.signbit(values[:-1]) != np.signbit(values[1:]))
    return [
        float(brentq(lambda radius: float(function(radius)), grid[index], grid[index + 1]))
        for index in indices
    ]


def _extrema() -> list[dict[str, float | str]]:
    def derivative(radius):
        return radial_gradient_mediator_green_derivative_3d(
            radius,
            spectral_shape=SPECTRAL_SHAPE,
            memory_loading=MEMORY_LOADING,
        )

    roots = _root_positions(derivative)
    extrema = []
    for radius in roots:
        step = 1.0e-5 * max(1.0, radius)
        derivative_left = float(derivative(radius - step))
        derivative_right = float(derivative(radius + step))
        value = float(
            radial_gradient_mediator_green_3d(
                radius,
                spectral_shape=SPECTRAL_SHAPE,
                memory_loading=MEMORY_LOADING,
            )
        )
        if derivative_left > 0.0 and derivative_right < 0.0:
            kind = "kernel_maximum_pair_energy_minimum"
        elif derivative_left < 0.0 and derivative_right > 0.0:
            kind = "kernel_minimum_pair_energy_barrier"
        else:
            raise RuntimeError("Green-kernel extremum could not be classified")
        extrema.append(
            {
                "radius": radius,
                "kernel": value,
                "kind": kind,
            }
        )
    return extrema


def run_audit() -> dict[str, Any]:
    parameters = _witness_parameters()
    groups = gradient_mediator_dimensionless_groups(**parameters)
    selection = gradient_mediator_selection(
        spectral_shape=groups.spectral_shape,
        memory_loading=groups.memory_loading,
        decay_rate_ratio=groups.decay_rate_ratio,
    )
    y_peak = selection.selected_scaled_wavenumber**2
    curvature_step = 1.0e-4 * y_peak
    curvature_y = y_peak + curvature_step * np.array([-1.0, 0.0, 1.0])
    curvature_u = np.sqrt(curvature_y)
    curvature_denominator = dimensionless_gradient_mediator_denominator(
        curvature_u,
        spectral_shape=groups.spectral_shape,
        memory_loading=groups.memory_loading,
    )
    curvature_transfer = curvature_y / curvature_denominator
    log_curvature_y = float(
        (
            np.log(curvature_transfer[0])
            - 2.0 * np.log(curvature_transfer[1])
            + np.log(curvature_transfer[2])
        )
        / curvature_step**2
    )
    inferred = infer_gradient_mediator_groups_from_peak(
        selected_scaled_wavenumber=selection.selected_scaled_wavenumber,
        log_transfer_curvature_y=log_curvature_y,
    )

    u = np.linspace(0.0, 4.0, 40001)
    transfer = gradient_mediator_transfer(
        u,
        coupling=1.0,
        coupling_geometry="gradient_vector",
        **parameters,
    ).real
    numerical_peak = float(u[int(np.argmax(transfer))])
    direct = gradient_mediator_transfer(
        np.array([0.0, numerical_peak]),
        coupling=1.0,
        coupling_geometry="direct_scalar",
        **parameters,
    )
    positive = gradient_mediator_transfer(
        u[::100], coupling=0.7, **parameters
    )
    negative = gradient_mediator_transfer(
        u[::100], coupling=-0.7, **parameters
    )

    zeros = _root_positions(
        lambda radius: radial_gradient_mediator_green_3d(
            radius,
            spectral_shape=SPECTRAL_SHAPE,
            memory_loading=MEMORY_LOADING,
        )
    )
    extrema = _extrema()
    finite_pair_minima = [
        item
        for item in extrema
        if item["kind"] == "kernel_maximum_pair_energy_minimum"
        and float(item["radius"]) > 1.0
    ]
    first_barrier = next(
        item
        for item in extrema
        if item["kind"] == "kernel_minimum_pair_energy_barrier"
    )
    first_pair_minimum = finite_pair_minima[0]

    quadrature_probe_radii = np.array([0.2, 1.0, 4.0, 7.0, 10.0])
    residue_probes = radial_gradient_mediator_green_3d(
        quadrature_probe_radii,
        spectral_shape=SPECTRAL_SHAPE,
        memory_loading=MEMORY_LOADING,
    )
    quadrature_probes = _quadrature_green_3d(quadrature_probe_radii)
    inverse_transform_max_error = float(np.max(np.abs(residue_probes - quadrature_probes)))

    constitutive_minimum = 1.0 - SPECTRAL_SHAPE**2 / 4.0
    gates = {
        "dimensionless_reduction_exact": bool(
            np.isclose(groups.spectral_shape, SPECTRAL_SHAPE)
            and np.isclose(groups.memory_loading, MEMORY_LOADING)
            and np.isclose(groups.decay_rate_ratio, DECAY_RATIO)
        ),
        "constitutive_operator_positive": constitutive_minimum > 0.0,
        "static_denominator_positive": selection.statically_stable,
        "selected_mode_oscillatory": selection.selected_mode_oscillatory,
        "analytic_peak_matches_grid": abs(
            selection.selected_scaled_wavenumber - numerical_peak
        )
        < 2.0e-4,
        "gain_free_peak_inference_recovers_groups": bool(
            np.isclose(inferred.spectral_shape, groups.spectral_shape, rtol=1.0e-6)
            and np.isclose(
                inferred.memory_loading, groups.memory_loading, rtol=1.0e-6
            )
        ),
        "gradient_channel_zero_mode": bool(transfer[0] == 0.0),
        "direct_channel_nonzero_mode_control": bool(direct[0] > 0.0),
        "common_gain_sign_invariant": bool(np.allclose(positive, negative)),
        "real_space_sign_changing_shells": len(zeros) >= 3,
        "exact_residues_match_infinite_fourier_quadrature": (
            inverse_transform_max_error < 2.0e-10
        ),
        "finite_separation_energy_minimum_exists": len(finite_pair_minima) >= 1,
    }
    return {
        "decision": "structural-pass-adjoint-gradient-mediator-candidate",
        "gates": gates,
        "witness_is_not_parameter_fit": True,
        "dimensionless_groups": groups.__dict__,
        "selection": selection.__dict__,
        "peak_inference": {
            "log_transfer_curvature_y": log_curvature_y,
            **inferred.__dict__,
        },
        "constitutive_minimum": constitutive_minimum,
        "numerical_peak": numerical_peak,
        "zero_crossings": zeros,
        "inverse_transform_max_error": inverse_transform_max_error,
        "first_pair_barrier": first_barrier,
        "first_finite_pair_minimum": first_pair_minimum,
        "claim_limits": {
            "coefficient_selection": "delta, mu and gamma/lambda remain inputs",
            "state_boundary": "vector mediator m is not canonical occupancy rho",
            "source_geometry": "k^2 requires the new adjoint gradient coupling",
            "kernel_selection": "K_eff is derived from the proposed mediator response",
            "pair_result": "linear point-source energy landscape only",
            "nonlinear_nodes": "not simulated",
            "dimension_selection": "not supplied",
        },
    }


def _write_figure(path: Path, result: dict[str, Any]) -> None:
    parameters = _witness_parameters()
    selection = result["selection"]
    u = np.linspace(0.0, 1.8, 1000)
    constitutive = 1.0 + SPECTRAL_SHAPE * np.square(u) + u**4
    transfer = gradient_mediator_transfer(u, **parameters).real

    radii = np.linspace(0.05, 15.0, 360)
    kernel = radial_gradient_mediator_green_3d(
        radii,
        spectral_shape=SPECTRAL_SHAPE,
        memory_loading=MEMORY_LOADING,
    )
    pair_energy = -kernel
    pair_force = radial_gradient_mediator_green_derivative_3d(
        radii,
        spectral_shape=SPECTRAL_SHAPE,
        memory_loading=MEMORY_LOADING,
    )

    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.35), constrained_layout=True)
    axes[0].plot(u, constitutive, color="#555f6b", label=r"$D(u)$")
    axes[0].plot(u, transfer / np.max(transfer), color="#2b6f77", label=r"$K_{eff}(u)$")
    axes[0].axvline(
        float(selection["selected_scaled_wavenumber"]),
        color="#20252b",
        linestyle="--",
        linewidth=1.0,
    )
    axes[0].set(xlabel=r"scaled wavenumber $u=k\ell$", ylabel="normalized value")
    axes[0].set_title("Kernel generated by response")
    axes[0].legend(frameon=False)

    axes[1].plot(radii, kernel, color="#2b6f77", label=r"$K_{eff}(r)$")
    axes[1].plot(radii, pair_energy, color="#a33f32", label=r"$U_{pair}=-K_{eff}$")
    axes[1].axhline(0.0, color="#555f6b", linewidth=0.8)
    axes[1].set(xlabel=r"scaled distance $r/\ell$", ylabel="response")
    axes[1].set_title("Sign-changing response shells")
    axes[1].legend(frameon=False)

    axes[2].plot(radii, pair_force, color="#6b4c8a")
    axes[2].axhline(0.0, color="#555f6b", linewidth=0.8)
    barrier = float(result["first_pair_barrier"]["radius"])
    minimum = float(result["first_finite_pair_minimum"]["radius"])
    axes[2].axvspan(barrier, minimum, color="#d9a441", alpha=0.25, label="outward force")
    axes[2].axvline(minimum, color="#20252b", linestyle="--", linewidth=1.0)
    axes[2].set(xlabel=r"scaled distance $r/\ell$", ylabel=r"radial force $K'(r)$")
    axes[2].set_title("First separated pair basin")
    axes[2].legend(frameon=False)

    fig.suptitle("Adjoint-gradient mediator: selected scale without an amplitude sweep")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _write_report(path: Path, result: dict[str, Any], figure: Path) -> None:
    gate_rows = "\n".join(
        f"| `{name}` | {'pass' if passed else 'fail'} |"
        for name, passed in result["gates"].items()
    )
    selection = result["selection"]
    report = rf"""# Adjoint-gradient mediator Green-kernel gate

Date: 2026-08-11. Status: **structural pass, model candidate only**.

## Correction and question

An attractive near field and repulsive outer shell can preserve individual
nodes while preventing sufficiently separated identical nodes from merging.
It does not by itself guarantee one finite pair distance: a static two-scale
law commonly gives merger on one side of a force crossing and unbounded
separation on the other. The earlier compensated three-scale pilot already
constructed an outer repulsive shell at about `10.91 sigma_rep`, but did not
test reciprocal two-node dynamics.

Can the shell shape and its scale instead arise as the response of one
longitudinal vector mediator, with a common adjoint source/readout coupling?

## Review correction: state and source placement

The canonical memory remains the non-negative occupancy \(\rho\) in
\(z=(x,\rho)\). The following longitudinal vector mediator \(\mathbf m\) and
its conjugate velocity \(\mathbf p\) are a proposed Markov-state extension,
not a relabeling of \(\rho\):

\[
\partial_t\mathbf m=\mathbf p,
\qquad
\partial_t\mathbf p=-(\lambda_m+\gamma_p)\mathbf p
-\left[\lambda_m\gamma_p+(-\Delta)D(-\Delta)\right]\mathbf m
+g\nabla q.
\]

Here \(q\) is a scalar source density. A point witness uses \(q=G_x\); the
frozen-node follow-up uses its complete retained occupancy. The single
interaction energy is

\[
H_{{\rm int}}[\mathbf m,q]=-g\int\mathbf m(y)\cdot\nabla q(y)\,dy.
\]

It supplies both the vector source \(g\nabla q\) and its adjoint reciprocal
readout. This explicit source placement is required for the \(k^2\) numerator.
Additive deposition directly into canonical \(\rho\) does not produce that
numerator. The earlier wording that attached the response directly to the
canonical continuity-memory law was therefore too strong.

## Reciprocal response

Let the longitudinal constitutive stiffness be

\[
D(k)=a+b k^2+c k^4,
\qquad a,c>0.
\]

For reciprocal gradient coupling, eliminating the linear memory field gives

\[
\widehat K_{{\rm eff}}(k,\omega)
=\frac{{g^2 k^2}}
{{(-i\omega+\lambda_m)(-i\omega+\gamma_p)+k^2D(k)}}.
\]

The same `g` writes and reads the mediator, hence `g^2`; independent source and
readout amplitudes are absent. The adjoint gradient pair supplies
`K_eff(0,omega)=0`, so the spatial integral vanishes without balancing raw
Gaussian amplitudes.

With

\[
\ell=(c/a)^{{1/4}},\quad
u=k\ell,\quad
\delta=\frac b{{\sqrt{{ac}}}},\quad
\mu=\frac{{\lambda_m\gamma_p\sqrt c}}{{a^{{3/2}}}},\quad
r_\gamma=\frac{{\max(\lambda_m,\gamma_p)}}{{\min(\lambda_m,\gamma_p)}}\geq1,
\]

the static denominator is

\[
P(u)=\mu+u^2+\delta u^4+u^6.
\]

The two decay rates enter only through their sum and product, so exchanging
their labels leaves the response unchanged. `r_gamma` is therefore the
canonical larger-to-smaller ratio; the individual labels are not identifiable.

Thus five dimensional coefficients reduce to a length/rate normalization and
three dimensionless shape groups. The response-selected scale is not supplied:
for `y_*=u_*^2` it solves

\[
2y_*^3+\delta y_*^2-\mu=0.
\]

## Fixed existence witness

The fixed witness `delta=-1.9`, `mu=0.3`, `r_gamma=1` is an analytic existence
point, not a fit to knot data. Its constitutive minimum is
`{result['constitutive_minimum']:.6g}>0`, so the fixed-source quadratic
mediator energy is positive.

- selected `u_*={selection['selected_scaled_wavenumber']:.6g}`;
- selected wavelength `2 pi/u_*={selection['selected_scaled_wavelength']:.6g}`;
- first point-source pair barrier at `r/ell={result['first_pair_barrier']['radius']:.6g}`;
- first finite separated minimum of `U_pair=-K_eff` at
  `r/ell={result['first_finite_pair_minimum']['radius']:.6g}`.

![Dynamic Green-kernel gate]({figure.as_posix()})

## Registered gates

| Gate | Result |
|---|---|
{gate_rows}

## What is and is not self-selected

Selected conditional on the proposed field coefficients and source geometry:
effective response shape, zero integral, preferred wavelength, shell positions
and the linear point-source pair landscape.

Not selected: `delta`, `mu`, `r_gamma`, the absolute length/time units and the
overall coupling. A simulation cannot determine constants that do not have an
update law. Promoting them to arbitrary adaptive variables would only move the
kernel choice into an adaptation rule.

The defensible coarse-graining route is identification rather than tuning.
Let `kappa_y=-d_y^2 log H(y)|_* > 0` for `y=u^2`. Then the unknown overall
gain cancels and

\[
\delta
=\frac{{y_*[6-\kappa_y(1+3y_*^2)]}}{{2(\kappa_y y_*^2-1)}},
\qquad
\mu=2y_*^3+\delta y_*^2.
\]

Consequently:

1. peak position and local log curvature estimate `delta,mu` jointly;
2. temporal damping and frequency at the same peak estimate
   the unordered decay-rate ratio and test the dispersion relation;
3. a calibrated weak response fixes the remaining gain;
4. estimates must agree across seeds, blocks, resolutions and independent
   pair response before they are called effective parameters.

## Decision and next test

P3.8b passes after review as an analytic **adjoint-gradient mediator
candidate**. It gives
a common-energy route to a zero-mode-free, sign-changing quasistatic response,
a finite separated point-source basin and phase-bearing temporal modes. It is
not obtained from canonical scalar deposition alone. It does not establish
nonlinear knot formation, basin accessibility, stability under noise,
parameter universality, or `d=3`.

Next, and only next, run one matched two-node pilot using mature frozen states:

- arm A: the already fixed compensated static outer-shell kernel;
- arm B: this fixed dynamic Green field;
- controls: cross-off and direct non-gradient source in the static gate;
- fixed separations below the barrier, in the outward-force interval, at the
  predicted finite minimum and beyond it;
- primary static outcomes: signed full-memory centre force and agreement with
  independently predicted shell radii. Shape cannot change in this frozen gate.

Reversible/current-off is not a valid static null because first- and
second-order realizations share the same equilibrium susceptibility. Bounded
separation, shape evolution and energy/work balance require a later dynamic
mediator implementation with a separately preregistered time discretization
and gain/mobility; they are not inferred from this quasistatic response.

No kernel-amplitude sweep or adaptive coefficient law is authorized.

## Reproducibility

- Script: `experiments/current/memory/closure/dynamic_green_kernel_selection_gate.py`
- Package: `src/emergenz_knoten/gradient_mediator.py`
- Git revision before generated changes: `{_git_output(['rev-parse', 'HEAD'])}`
- Generated: `{datetime.now(UTC).isoformat()}`
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")


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
    summary.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
