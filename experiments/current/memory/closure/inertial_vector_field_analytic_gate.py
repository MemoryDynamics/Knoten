"""Audit the minimal inertial reversible extension of the local vector field."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import subprocess
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np
from scipy.linalg import expm

from emergenz_knoten import (
    InertialVectorFieldDynamics,
    LocalVectorFieldExpansion,
    inertial_mode_energy_rate,
    inertial_vector_dimensionless_groups,
    inertial_vector_fourier_operator,
    inertial_vector_mode,
    inertial_vector_mode_operator,
    isotropic_vector_energy_hessian,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
TOLERANCE = 1e-12


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/memory/closure/inertial_vector_field_analytic_gate_2026-08-11.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/memory/closure/inertial_vector_field_analytic_gate_2026-08-11.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/inertial_vector_field_analytic_gate_2026-08-11.png"
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


def _energy_metric(
    wavevector: np.ndarray, dynamics: InertialVectorFieldDynamics
) -> np.ndarray:
    hessian = isotropic_vector_energy_hessian(wavevector, dynamics.energy)
    dim = wavevector.size
    return np.block(
        [
            [hessian, np.zeros((dim, dim))],
            [np.zeros((dim, dim)), np.eye(dim) / dynamics.inertia],
        ]
    )


def run_audit() -> dict[str, Any]:
    energy = LocalVectorFieldExpansion(
        mass_coefficient=1.0,
        longitudinal_gradient_coefficient=0.4,
        transverse_gradient_coefficient=1.1,
        biharmonic_coefficient=0.3,
        cubic_saturation=1.0,
        mobility=0.7,
    )
    dynamics = InertialVectorFieldDynamics(energy=energy, inertia=1.7, damping=0.4)
    conservative = InertialVectorFieldDynamics(
        energy=energy, inertia=dynamics.inertia, damping=0.0
    )
    rng = np.random.default_rng(20_260_811)
    root_errors = []
    covariance_errors = []
    reversible_errors = []
    energy_rate_errors = []
    for dim in (1, 2, 3, 5):
        wavevector = rng.normal(size=dim)
        rotation, _ = np.linalg.qr(rng.normal(size=(dim, dim)))
        transform = np.block(
            [
                [rotation, np.zeros_like(rotation)],
                [np.zeros_like(rotation), rotation],
            ]
        )
        operator = inertial_vector_fourier_operator(wavevector, dynamics)
        rotated = inertial_vector_fourier_operator(rotation @ wavevector, dynamics)
        covariance_errors.append(
            float(np.linalg.norm(rotated - transform @ operator @ transform.T))
        )

        reversible_operator = inertial_vector_fourier_operator(wavevector, conservative)
        metric = _energy_metric(wavevector, conservative)
        reversible_errors.append(
            float(
                np.linalg.norm(
                    reversible_operator.T @ metric + metric @ reversible_operator
                )
            )
        )
        state = rng.normal(size=2 * dim)
        momentum = state[dim:]
        measured_rate = float(state @ metric @ operator @ state)
        expected_rate = float(np.sum(inertial_mode_energy_rate(momentum, dynamics)))
        energy_rate_errors.append(abs(measured_rate - expected_rate))

    for channel in ("longitudinal", "transverse"):
        for wavenumber in np.linspace(0.0, 3.0, 31):
            operator = inertial_vector_mode_operator(
                float(wavenumber), dynamics, channel=channel
            )
            mode = inertial_vector_mode(float(wavenumber), dynamics, channel=channel)
            numerical = np.sort_complex(np.linalg.eigvals(operator))
            analytical = np.sort_complex(np.asarray(mode.eigenvalues))
            root_errors.append(float(np.max(np.abs(numerical - analytical))))

    unstable_energy = LocalVectorFieldExpansion(
        mass_coefficient=-0.2,
        longitudinal_gradient_coefficient=0.4,
        transverse_gradient_coefficient=0.4,
        biharmonic_coefficient=0.3,
        cubic_saturation=1.0,
    )
    unstable = inertial_vector_mode(
        0.0,
        InertialVectorFieldDynamics(energy=unstable_energy, inertia=1.0, damping=2.0),
        channel="longitudinal",
    )
    negative_control_pass = bool(
        unstable.classification == "restoring_instability"
        and max(value.real for value in unstable.eigenvalues) > 0.0
    )

    witnesses = []
    witness_energy = LocalVectorFieldExpansion(
        mass_coefficient=1.0,
        longitudinal_gradient_coefficient=0.0,
        transverse_gradient_coefficient=0.0,
        biharmonic_coefficient=1.0,
        cubic_saturation=1.0,
    )
    for damping_ratio in (0.0, 0.05, 1.0, 1.5):
        witness = InertialVectorFieldDynamics(
            energy=witness_energy,
            inertia=1.0,
            damping=2.0 * damping_ratio,
        )
        mode = inertial_vector_mode(0.0, witness, channel="transverse")
        witnesses.append(
            {
                "damping_ratio": damping_ratio,
                "classification": mode.classification,
                "eigenvalues": mode.eigenvalues,
                "angular_frequency": mode.angular_frequency,
                "decay_rate": mode.decay_rate,
                "quality_factor": mode.quality_factor,
                "cycles_per_e_folding": mode.cycles_per_e_folding,
            }
        )

    maxima = {
        "root_error": max(root_errors),
        "covariance_error": max(covariance_errors),
        "reversible_energy_error": max(reversible_errors),
        "dissipative_energy_rate_error": max(energy_rate_errors),
    }
    gates = {name: value <= TOLERANCE for name, value in maxima.items()}
    gates["negative_curvature_control"] = negative_control_pass
    gates["classification_boundaries"] = [
        row["classification"] for row in witnesses
    ] == [
        "conservative_oscillation",
        "damped_oscillation",
        "critical_damping",
        "overdamped_relaxation",
    ]
    return {
        "tolerance": TOLERANCE,
        "maxima": maxima,
        "negative_control": {
            "classification": unstable.classification,
            "eigenvalues": unstable.eigenvalues,
        },
        "witnesses": witnesses,
        "dimensionless_groups": inertial_vector_dimensionless_groups(dynamics),
        "gates": gates,
        "decision": "structural-pass" if all(gates.values()) else "fail",
    }


def _jsonable(value: Any) -> Any:
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, (float, np.floating)):
        number = float(value)
        if not np.isfinite(number):
            return "Infinity" if number > 0.0 else "-Infinity"
        return number
    if isinstance(value, np.integer):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if hasattr(value, "__dataclass_fields__"):
        return {
            name: _jsonable(getattr(value, name)) for name in value.__dataclass_fields__
        }
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def write_figure(path: Path) -> None:
    denominator = np.linspace(-1.0, 4.0, 500)
    damping_ratio = np.linspace(0.0, 2.0, 400)
    d_grid, z_grid = np.meshgrid(denominator, damping_ratio)
    regime = np.zeros_like(d_grid, dtype=int)
    regime[d_grid > 0.0] = 1
    regime[(d_grid > 0.0) & (d_grid > np.square(z_grid))] = 2

    figure, axes = plt.subplots(1, 3, figsize=(14.0, 4.2), constrained_layout=True)
    cmap = ListedColormap(["#b24a4a", "#55707f", "#2f8f83"])
    axes[0].pcolormesh(denominator, damping_ratio, regime, cmap=cmap, shading="auto")
    axes[0].plot(
        denominator[denominator >= 0],
        np.sqrt(denominator[denominator >= 0]),
        color="black",
        linewidth=1.2,
    )
    axes[0].axvline(0.0, color="black", linewidth=1.2)
    axes[0].set(
        title="Universal linear regimes",
        xlabel="dimensionless D",
        ylabel="damping ratio zeta",
    )
    axes[0].legend(
        handles=[
            Patch(color="#b24a4a", label="unstable D < 0"),
            Patch(color="#2f8f83", label="damped oscillation"),
            Patch(color="#55707f", label="overdamped"),
            plt.Line2D([], [], color="black", label="critical damping"),
        ],
        fontsize=7,
        loc="upper left",
    )

    time = np.linspace(0.0, 20.0, 1000)
    for zeta in (0.0, 0.05, 1.0, 1.5):
        energy = LocalVectorFieldExpansion(1.0, 0.0, 0.0, 1.0, 1.0)
        dynamics = InertialVectorFieldDynamics(
            energy=energy, inertia=1.0, damping=2.0 * zeta
        )
        operator = inertial_vector_mode_operator(0.0, dynamics, channel="transverse")
        trace = np.asarray([(expm(operator * value) @ [1.0, 0.0])[0] for value in time])
        axes[1].plot(time, trace, label=f"zeta={zeta:g}")
    axes[1].axhline(0.0, color="black", linewidth=0.8)
    axes[1].set(title="Exact dimensionless return", xlabel=r"$t/t_I$", ylabel="m(t)")
    axes[1].legend(fontsize=8)

    zeta = np.linspace(0.005, 0.999, 500)
    cycles = np.sqrt(1.0 - np.square(zeta)) / (2.0 * np.pi * zeta)
    axes[2].semilogy(zeta, cycles, color="#2f8f83", linewidth=2)
    axes[2].axhline(1.0, color="black", linestyle="--", linewidth=1)
    axes[2].set(
        title="Persistence of underdamped modes",
        xlabel="damping ratio zeta",
        ylabel="cycles per e-fold",
    )
    for axis in axes:
        axis.grid(alpha=0.2)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(figure)


def write_report(
    payload: dict[str, Any], path: Path, figure_path: Path, json_path: Path
) -> None:
    result = payload["result"]
    lines = [
        "# Inertial reversible vector-field analytic gate",
        "",
        f"Date: {payload['generated_utc'][:10]}.",
        "",
        f"**Decision: `{result['decision']}`.**",
        "",
        "The existing reactive pair placeholder is now reconciled with the spatial vector-field energy through a conjugate momentum field.",
        "",
        f"![Inertial vector-field audit]({_relative_from(path, figure_path)})",
        "",
        "## Linear result",
        "",
        r"For each longitudinal or transverse mode,",
        "",
        r"\[ I s^2+\gamma s+D_q(k)=0. \]",
        "",
        r"A damped oscillation is asymptotically stable exactly when \(D_q(k)>0\), \(\gamma>0\), and \(4ID_q(k)>\gamma^2\). The reversible term does not stabilize negative curvature.",
        "",
        "## Audit",
        "",
        "| gate | maximum/error | pass |",
        "|---|---:|---|",
    ]
    for name, value in result["maxima"].items():
        lines.append(f"| {name} | {value:.3g} | {result['gates'][name]} |")
    lines.extend(
        [
            f"| negative_curvature_control | positive root retained | {result['gates']['negative_curvature_control']} |",
            f"| classification_boundaries | exact | {result['gates']['classification_boundaries']} |",
            "",
            "## Dimensionless witnesses",
            "",
            "| zeta | classification | decay | omega | Q | cycles/e-fold |",
            "|---:|---|---:|---:|---:|---:|",
        ]
    )
    for row in result["witnesses"]:
        lines.append(
            f"| {row['damping_ratio']:.3g} | {row['classification']} | "
            f"{row['decay_rate']:.3g} | {row['angular_frequency']:.3g} | "
            f"{row['quality_factor']:.3g} | {row['cycles_per_e_folding']:.3g} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "The pass is structural and partly constructive: adding a conjugate momentum was designed to permit oscillation. It establishes mathematical consistency, not emergence or empirical support.",
            "",
            "Positive field curvature and damping provide stability; the reversible exchange provides phase. Long-lived oscillation additionally requires small damping ratio. None of these coefficients is selected by the current passive memory.",
            "",
            "The operator is O(d)-covariant and acts identically on ambient components. It does not select d=3. No knot, spin, charge, photon, quantum or particle claim follows.",
            "",
            "## Next gate",
            "",
            "Specify one trajectory source J[x], derive the reciprocal trajectory force from the same coupling energy, and preregister discrete energy accounting plus source-off, reversible-off and first-order controls. Only then is one model-conditional knot pilot admissible.",
            "",
            "## Reproducibility",
            "",
            f"- revision: `{payload['git_revision']}`;",
            f"- schema: `{payload['schema']}`;",
            f"- JSON: `{_relative(json_path)}`.",
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
    result = run_audit()
    report_path = _resolve(args.report)
    json_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    payload = {
        "schema": "emergenz-knoten.inertial-vector-field-analytic-gate.v1",
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "result": result,
    }
    serializable = _jsonable(payload)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(serializable, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    write_figure(figure_path)
    write_report(payload, report_path, figure_path, json_path)
    print(json.dumps(serializable["result"]["gates"], indent=2))
    print(f"decision={serializable['result']['decision']}")


if __name__ == "__main__":
    main()
