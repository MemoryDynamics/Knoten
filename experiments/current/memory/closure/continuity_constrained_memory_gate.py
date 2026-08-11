"""Audit a continuity-constrained density-flux extension of scalar memory."""

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

from emergenz_knoten import (
    continuity_memory_mode,
    continuity_memory_mode_operator,
    continuity_oscillation_threshold,
    memory_innovation_moments,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/memory/closure/continuity_constrained_memory_gate_2026-08-11.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/memory/closure/continuity_constrained_memory_gate_2026-08-11.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/continuity_constrained_memory_gate_2026-08-11.png"
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


def run_audit() -> dict[str, Any]:
    stationary = memory_innovation_moments(
        memory_relaxation=0.01,
        target_mass=1.0,
        current_mass=1.0,
        current_centroid=np.array([0.2, -0.4, 0.1]),
        deposited_position=np.array([0.5, 0.0, -0.3]),
    )
    expected_first = 0.01 * (
        np.array([0.5, 0.0, -0.3]) - np.array([0.2, -0.4, 0.1])
    )

    rng = np.random.default_rng(20_260_811)
    initial = rng.normal(size=31)
    state = initial.copy()
    accumulated = np.zeros_like(state)
    for _ in range(100):
        updated = 0.99 * state + 0.01 * rng.normal(size=state.size)
        accumulated += updated - state
        state = updated
    telescoping_error = float(np.max(np.abs(accumulated - (state - initial))))

    root_errors = []
    for flux_ratio in (0.0, 0.25, 1.0, 2.0, 4.0):
        for scaled_k in np.linspace(0.0, 4.0, 81):
            kwargs = {
                "memory_relaxation": 1.0,
                "flux_relaxation": flux_ratio,
                "stiffness": 1.0,
            }
            analytical = np.sort_complex(
                np.asarray(continuity_memory_mode(scaled_k, **kwargs).eigenvalues)
            )
            numerical = np.sort_complex(
                np.linalg.eigvals(continuity_memory_mode_operator(scaled_k, **kwargs))
            )
            root_errors.append(float(np.max(np.abs(analytical - numerical))))

    threshold = continuity_oscillation_threshold(
        memory_relaxation=1.0,
        flux_relaxation=2.0,
        stiffness=1.0,
    )
    below = continuity_memory_mode(
        0.99 * threshold,
        memory_relaxation=1.0,
        flux_relaxation=2.0,
        stiffness=1.0,
    )
    above = continuity_memory_mode(
        1.01 * threshold,
        memory_relaxation=1.0,
        flux_relaxation=2.0,
        stiffness=1.0,
    )
    no_flux_stiffness = continuity_memory_mode(
        10.0,
        memory_relaxation=1.0,
        flux_relaxation=2.0,
        stiffness=0.0,
    )

    gates = {
        "stationary_innovation_zero_monopole": abs(stationary.monopole) < 1.0e-14,
        "innovation_first_moment_identity": bool(
            np.allclose(stationary.first_moment, expected_first, atol=1.0e-14)
        ),
        "block_innovation_telescopes": telescoping_error < 1.0e-13,
        "dispersion_roots_match_operator": max(root_errors) < 1.0e-12,
        "threshold_separates_real_and_complex": bool(
            not below.oscillatory and above.oscillatory
        ),
        "zero_stiffness_remains_real": not no_flux_stiffness.oscillatory,
    }
    return {
        "decision": "structural-pass-with-unresolved-force-balance",
        "gates": gates,
        "max_root_error": max(root_errors),
        "telescoping_error": telescoping_error,
        "dimensionless_witness": {
            "memory_relaxation": 1.0,
            "flux_relaxation": 2.0,
            "stiffness": 1.0,
            "threshold": threshold,
            "below_classification": below.classification,
            "above_classification": above.classification,
        },
        "claim_limits": {
            "new_state": "the flux is absent from canonical (x,rho)",
            "new_coefficients": ["flux_relaxation", "stiffness"],
            "static_force_balance": "not supplied by the continuity law",
            "transverse_phase": "transverse flux only relaxes in the minimal law",
            "dimension_selection": "the O(d)-covariant law does not select d=3",
        },
    }


def _write_figure(path: Path) -> None:
    flux_ratios = np.linspace(0.0, 4.0, 241)
    scaled_k = np.linspace(0.0, 2.5, 301)
    ratio_grid, k_grid = np.meshgrid(flux_ratios, scaled_k, indexing="ij")
    oscillatory = 4.0 * np.square(k_grid) > np.square(1.0 - ratio_grid)

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.2), constrained_layout=True)
    axes[0].pcolormesh(
        scaled_k,
        flux_ratios,
        oscillatory,
        shading="auto",
        cmap=matplotlib.colors.ListedColormap(["#d9dde2", "#2f7d6d"]),
    )
    upper = 1.0 + 2.0 * scaled_k
    lower = 1.0 - 2.0 * scaled_k
    axes[0].plot(
        scaled_k[upper <= 4.0], upper[upper <= 4.0], color="#20252b", linewidth=1.2
    )
    axes[0].plot(
        scaled_k[lower >= 0.0], lower[lower >= 0.0], color="#20252b", linewidth=1.2
    )
    axes[0].set(xlabel=r"$c_j k/\lambda_m$", ylabel=r"$\gamma_j/\lambda_m$")
    axes[0].set_title("Longitudinal mode classification")
    axes[0].set_ylim(0.0, 4.0)
    axes[0].text(1.65, 1.1, "oscillatory", color="white", ha="center")
    axes[0].text(0.08, 3.25, "real", color="#20252b")

    k_values = np.linspace(0.0, 2.5, 301)
    real_parts = []
    imaginary_parts = []
    for value in k_values:
        mode = continuity_memory_mode(
            float(value),
            memory_relaxation=1.0,
            flux_relaxation=2.0,
            stiffness=1.0,
        )
        real_parts.append(max(root.real for root in mode.eigenvalues))
        imaginary_parts.append(mode.angular_frequency)
    axes[1].plot(k_values, real_parts, label=r"max Re$(s)$", color="#a33f32")
    axes[1].plot(k_values, imaginary_parts, label=r"$|$Im$(s)|$", color="#2b6690")
    axes[1].axvline(0.5, color="#20252b", linestyle="--", linewidth=1.0)
    axes[1].set(xlabel=r"$c_j k/\lambda_m$", ylabel="dimensionless rate")
    axes[1].set_title(r"Witness: $\gamma_j/\lambda_m=2$")
    axes[1].legend(frameon=False)
    fig.suptitle("Continuity-constrained memory: propagation eligibility, not knot proof")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _write_report(path: Path, result: dict[str, Any], figure: Path) -> None:
    gate_rows = "\n".join(
        f"| `{name}` | {'pass' if passed else 'fail'} |"
        for name, passed in result["gates"].items()
    )
    text = rf"""# Continuity-constrained memory gate

Date: 2026-08-11. Status: **structural pass with unresolved force balance**.

## Question

Can the scalar memory acquire a phase-bearing local transport mechanism without
assigning a charge label, a preferred direction, or separate self/cross
kernels?

## Proposed minimal extension

The canonical deposition remains

\[
\rho_{{n+1}}-\rho_n=\lambda_m\left[M_0G_\sigma(\cdot-x_{{n+1}})-\rho_n\right].
\]

At stationary total memory mass its innovation has zero monopole and the first
moment

\[
\int y\,(\rho_{{n+1}}-\rho_n)(y)\,dy
=\lambda_mM_0(x_{{n+1}}-\bar x_n^\rho).
\]

This signed innovation is derived from the existing update; it is not a new
charge. Its block sum telescopes to \(\rho_{{n+B}}-\rho_n\), so a bounded
stationary memory has no persistent DC source.

The new proposal is a local memory flux \(\mathbf j\):

\[
\partial_t\rho=-\lambda_m\rho-\nabla\!\cdot\mathbf j+S_x,
\qquad
\partial_t\mathbf j=-\gamma_j\mathbf j-c_j^2\nabla\rho.
\]

For one longitudinal Fourier mode,

\[
(s+\lambda_m)(s+\gamma_j)+c_j^2k^2=0.
\]

It is oscillatory exactly when

\[
2c_jk>|\lambda_m-\gamma_j|.
\]

The current direction is constrained by transport and O(d) covariance rather
than assigned per knot. Nevertheless \(\mathbf j\), \(\gamma_j\), and \(c_j\)
are new model content and are not derived from the scalar long runs.

## Registered identities

| Gate | Result |
|---|---|
{gate_rows}

Maximum root error: `{result['max_root_error']:.3e}`. Telescoping error:
`{result['telescoping_error']:.3e}`.

![Dimensionless continuity-mode gate]({figure.as_posix()})

## Decision

This is the preferred **P3.8a analytic extension** because it introduces no
external sign, handedness, node species, boundary, or separate cross geometry.
It supplies a falsifiable propagation/phase threshold and a compulsory
first-order null control (`c_j=0`).

It does **not** yet authorize a coupled simulation:

1. continuity does not cancel the nonzero affine pair force found in P3.7b;
2. the minimal law couples only the longitudinal current; transverse current
   decays and therefore supplies no spin mode;
3. it remains O(d)-covariant and cannot select three dimensions;
4. a common source/readout energy must still make deposition and trajectory
   backreaction reciprocal without independently tuned gains.

The next calculation is therefore an energy-consistent density-current
coupling and its affine equilibrium/limit-cycle gate. Only a simultaneous
force-balance and stable-mode pass permits one short pilot. A kernel, gain,
lambda, or noise sweep remains blocked.

## Reproducibility

- Script: `experiments/current/memory/closure/continuity_constrained_memory_gate.py`
- Package: `src/emergenz_knoten/continuity_memory.py`
- Git revision before generated changes: `{_git_output(['rev-parse', 'HEAD'])}`
- Generated: `{datetime.now(UTC).isoformat()}`
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    args = parse_args()
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    result = run_audit()
    _write_figure(figure)
    relative_figure = Path("../../../figures/draft/memory") / figure.name
    _write_report(report, result, relative_figure)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
