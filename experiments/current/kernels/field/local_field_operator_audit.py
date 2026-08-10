from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    LocalScalarFieldExpansion,
    gaussian_matched_local_expansion,
    gaussian_transfer,
    isotropic_ambient_transfer_matrix,
    local_scalar_operator_denominator,
    local_scalar_stationary_transfer,
    propagate_isotropic_ambient_covariance,
)


def _git_output(args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return completed.stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the minimal local scalar-field derivative expansion implied "
            "by the current symmetries, including Gaussian low-k matching, "
            "finite-wavenumber stability, and the ambient-rank null."
        )
    )
    parser.add_argument("--gaussian-length", type=float, default=3.0)
    parser.add_argument("--ambient-dimension", type=int, default=10)
    parser.add_argument("--max-dimensionless-wavenumber", type=float, default=3.0)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/kernels/field/local_field_operator_audit_2026-07-29.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/kernels/field/local_field_operator_audit_2026-07-29.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/kernels/field_2026-07-29/"
            "local_field_operator_audit.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative_link(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _validate_args(args: argparse.Namespace) -> None:
    if not math.isfinite(args.gaussian_length) or args.gaussian_length <= 0.0:
        raise SystemExit("--gaussian-length must be positive and finite")
    if args.ambient_dimension < 4:
        raise SystemExit("--ambient-dimension must be at least four for the rank null")
    if (
        not math.isfinite(args.max_dimensionless_wavenumber)
        or args.max_dimensionless_wavenumber <= 1.5
    ):
        raise SystemExit("--max-dimensionless-wavenumber must exceed 1.5")


def build_operator_cases(length: float) -> dict[str, LocalScalarFieldExpansion]:
    """Return the fixed analytic cases; this function performs no fitting."""

    gaussian_matched = gaussian_matched_local_expansion(gaussian_length=length)
    return {
        "relaxation_diffusion": LocalScalarFieldExpansion(
            mass_coefficient=1.0,
            gradient_coefficient=length**2 / 2.0,
        ),
        "gaussian_k4_match": gaussian_matched,
        "compensated_source": LocalScalarFieldExpansion(
            mass_coefficient=gaussian_matched.mass_coefficient,
            gradient_coefficient=gaussian_matched.gradient_coefficient,
            biharmonic_coefficient=gaussian_matched.biharmonic_coefficient,
            source_coefficient=0.0,
            source_laplacian_coefficient=length**2,
        ),
        "finite_k_stable": LocalScalarFieldExpansion(
            mass_coefficient=1.0,
            gradient_coefficient=-1.8 * length**2,
            biharmonic_coefficient=length**4,
        ),
        "finite_k_critical": LocalScalarFieldExpansion(
            mass_coefficient=1.0,
            gradient_coefficient=-2.0 * length**2,
            biharmonic_coefficient=length**4,
        ),
        "finite_k_unstable": LocalScalarFieldExpansion(
            mass_coefficient=1.0,
            gradient_coefficient=-2.2 * length**2,
            biharmonic_coefficient=length**4,
            cubic_saturation=1.0,
        ),
    }


def _max_error(u: np.ndarray, error: np.ndarray, upper: float) -> float:
    mask = u <= upper
    return float(np.max(error[mask]))


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    _validate_args(args)
    length = float(args.gaussian_length)
    cases = build_operator_cases(length)
    u = np.linspace(0.0, args.max_dimensionless_wavenumber, 3001)
    k = u / length
    exact = gaussian_transfer(k, length=length)
    rd = local_scalar_stationary_transfer(
        k,
        cases["relaxation_diffusion"],
        normalize_zero_mode=True,
    )
    matched = local_scalar_stationary_transfer(
        k,
        cases["gaussian_k4_match"],
        normalize_zero_mode=True,
    )
    rd_error = np.abs(rd - exact)
    matched_error = np.abs(matched - exact)

    stability = {
        name: asdict(field.linear_stability())
        for name, field in cases.items()
        if name.startswith("finite_k") or name == "gaussian_k4_match"
    }
    response = complex(
        local_scalar_stationary_transfer(
            1.0 / length,
            cases["gaussian_k4_match"],
            normalize_zero_mode=True,
        )
    )
    source_covariance = np.diag(
        np.linspace(1.0, 0.1, int(args.ambient_dimension))
    )
    transfer = isotropic_ambient_transfer_matrix(
        response,
        dimension=int(args.ambient_dimension),
    )
    output_covariance = propagate_isotropic_ambient_covariance(
        source_covariance,
        response,
    )
    return {
        "description": (
            "Fixed analytic audit of a restricted even-derivative local "
            "scalar field family compatible with the current assumptions."
        ),
        "inputs": {
            "gaussian_length": length,
            "ambient_dimension": int(args.ambient_dimension),
            "max_dimensionless_wavenumber": float(
                args.max_dimensionless_wavenumber
            ),
        },
        "operator_equation": (
            "tau d_t phi = -c0 phi + c2 Delta phi - c4 Delta^2 phi "
            "- v phi^2 - u phi^3 + s0 rho - s2 Delta rho"
        ),
        "stationary_transfer": "(s0+s2 k^2)/(c0+c2 k^2+c4 k^4)",
        "gaussian_matching": {
            "exact_series": "1 - u^2/2 + u^4/8 + O(u^6)",
            "rd_denominator": "1 + u^2/2",
            "k4_denominator": "1 + u^2/2 + u^4/8",
            "rd_max_abs_error_u_le_0p5": _max_error(u, rd_error, 0.5),
            "k4_max_abs_error_u_le_0p5": _max_error(u, matched_error, 0.5),
            "rd_max_abs_error_u_le_1": _max_error(u, rd_error, 1.0),
            "k4_max_abs_error_u_le_1": _max_error(u, matched_error, 1.0),
        },
        "stability": stability,
        "compensated_source": {
            "zero_mode_response": float(
                local_scalar_stationary_transfer(
                    0.0,
                    cases["compensated_source"],
                )
            ),
            "zero_mean": cases["compensated_source"].zero_mean_linear_response,
        },
        "ambient_rank_null": {
            "response_at_u_1": [response.real, response.imag],
            "transfer_shape": list(transfer.shape),
            "transfer_is_scalar_identity": bool(
                np.allclose(transfer, response * np.eye(args.ambient_dimension))
            ),
            "input_rank": int(np.linalg.matrix_rank(source_covariance)),
            "output_rank": int(np.linalg.matrix_rank(output_covariance)),
            "normalized_transfer_singular_values": (
                np.linalg.svd(transfer, compute_uv=False) / abs(response)
            ).real.tolist(),
        },
        "claims": {
            "random_walk_alone_selects_field_operator": False,
            "gaussian_fixes_low_k_coefficients_through_k4": True,
            "componentwise_isotropic_field_selects_rank_three": False,
            "finite_k_instability_is_already_derived": False,
            "finite_k_instability_is_minimal_open_mechanism": True,
            "inherited_symmetries_forbid_quadratic_field_term": False,
            "quantization_established": False,
        },
        "cases": {name: asdict(field) for name, field in cases.items()},
    }


def _plot(
    *,
    args: argparse.Namespace,
    payload: dict[str, Any],
    output: Path,
) -> None:
    length = float(args.gaussian_length)
    cases = build_operator_cases(length)
    u = np.linspace(0.0, args.max_dimensionless_wavenumber, 1801)
    k = u / length
    exact = gaussian_transfer(k, length=length)
    rd = local_scalar_stationary_transfer(
        k,
        cases["relaxation_diffusion"],
        normalize_zero_mode=True,
    )
    matched = local_scalar_stationary_transfer(
        k,
        cases["gaussian_k4_match"],
        normalize_zero_mode=True,
    )
    compensated = local_scalar_stationary_transfer(
        k,
        cases["compensated_source"],
    )
    if np.max(np.abs(compensated)) > 0.0:
        compensated = compensated / np.max(np.abs(compensated))

    fig, axes = plt.subplots(2, 2, figsize=(12.6, 8.4))
    colors = {
        "gaussian": "#202020",
        "rd": "#377eb8",
        "k4": "#147d64",
        "compensated": "#d06b25",
        "stable": "#147d64",
        "critical": "#8055a6",
        "unstable": "#c23b22",
    }

    axes[0, 0].plot(u, exact, color=colors["gaussian"], linewidth=2.2, label="exact Gaussian")
    axes[0, 0].plot(u, rd, color=colors["rd"], linewidth=1.9, linestyle="--", label="k^2 local field")
    axes[0, 0].plot(u, matched, color=colors["k4"], linewidth=1.9, linestyle="-.", label="k^4 local match")
    axes[0, 0].plot(u, compensated, color=colors["compensated"], linewidth=1.6, linestyle=":", label="derivative-source response")

    positive = u > 0.0
    axes[0, 1].plot(u[positive], np.abs(rd[positive] - exact[positive]), color=colors["rd"], linewidth=1.9, linestyle="--", label="k^2 error")
    axes[0, 1].plot(u[positive], np.abs(matched[positive] - exact[positive]), color=colors["k4"], linewidth=1.9, linestyle="-.", label="k^4 error")
    axes[0, 1].set_yscale("log")

    stability_labels = {
        "finite_k_stable": "stable finite-k minimum (a2=-1.8)",
        "finite_k_critical": "critical shell (a2=-2.0)",
        "finite_k_unstable": "unstable shell (a2=-2.2)",
    }
    stability_colors = {
        "finite_k_stable": colors["stable"],
        "finite_k_critical": colors["critical"],
        "finite_k_unstable": colors["unstable"],
    }
    for name in stability_labels:
        denominator = local_scalar_operator_denominator(k, cases[name])
        axes[1, 0].plot(
            u,
            denominator,
            color=stability_colors[name],
            linewidth=2.0,
            label=stability_labels[name],
        )

    singular_values = np.asarray(
        payload["ambient_rank_null"]["normalized_transfer_singular_values"]
    )
    components = np.arange(1, singular_values.size + 1)
    axes[1, 1].bar(
        components,
        singular_values,
        color="#377eb8",
        width=0.72,
        label=r"singular values of $H I_d$",
    )
    axes[1, 1].axvline(3.5, color="#c23b22", linestyle=":", linewidth=1.2, label="rank-3 gap would be here")

    axes[0, 0].set_title("Kernel as a local-field response")
    axes[0, 0].set_ylabel("normalized transfer H(u)")
    axes[0, 1].set_title("Low-wavenumber matching error")
    axes[0, 1].set_ylabel("absolute error")
    axes[1, 0].set_title("Finite-wavenumber stability gate")
    axes[1, 0].set_ylabel("P(u) = c0 + a2 u^2 + u^4")
    axes[1, 1].set_title("Ambient-rank null")
    axes[1, 1].set_ylabel("singular value / |H|")
    axes[1, 1].set_xlabel("ambient component")
    axes[1, 1].set_xticks(components)
    axes[1, 1].set_ylim(0.0, 1.15)
    for axis in axes.flat[:3]:
        axis.set_xlabel("u = L k")
    for axis in axes.flat:
        axis.axhline(0.0, color="#777777", linewidth=0.8)
        axis.grid(True, alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Local field operator audit: constrained response, open mechanism")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=190)
    plt.close(fig)


def _fmt(value: Any) -> str:
    number = float(value)
    if number == 0.0:
        return "0"
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.6e}"
    return f"{number:.6f}"


def write_outputs(args: argparse.Namespace) -> None:
    payload = build_payload(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    payload["generated_utc"] = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    payload["git_revision"] = _git_output(["rev-parse", "HEAD"])
    payload["git_status"] = _git_output(["status", "--short"])
    payload["outputs"] = {
        "report": str(args.report),
        "summary_json": str(args.summary_json),
        "figure": str(args.figure),
    }

    _plot(args=args, payload=payload, output=figure)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    matching = payload["gaussian_matching"]
    rank = payload["ambient_rank_null"]
    stability = payload["stability"]
    lines = [
        "# Local Field Operator Audit",
        "",
        f"Date: {payload['generated_utc']}.",
        "",
        "## Question",
        "",
        "Can the arbitrary radial kernel be replaced by a systematic local",
        "field expansion under the assumptions already used by the project,",
        "and which coefficient would constitute the first genuinely new",
        "pattern-forming mechanism?",
        "",
        "This is a fixed analytic audit. It performs no parameter fit, stochastic",
        "simulation, knot claim, or quantization step.",
        "",
        f"![Local field operator audit]({_relative_link(report, figure)})",
        "",
        "## Assumptions and restricted basis",
        "",
        "The inherited assumptions are translation invariance, O(d) isotropy,",
        "spatially parity-even scalar response, a local Markov field state, the",
        "existing memory source rho, and gradient readout by the visible",
        "trajectory. The restricted audit keeps the homogeneous linear operator",
        "through four spatial derivatives, the first derivative-source correction,",
        "and local powers through cubic order:",
        "",
        "```text",
        payload["operator_equation"],
        "H(k,0) = " + payload["stationary_transfer"],
        "```",
        "",
        "A Taylor expansion of a radial K(r) would only describe the near field.",
        "This derivative expansion instead defines a local field law whose Green",
        "response is the effective kernel.",
        "It is not the complete EFT operator basis: higher source derivatives,",
        "mixed field-gradient nonlinearities, and cross-component fields are",
        "deliberately omitted until an observable requires them.",
        "Spatial parity does not forbid v*phi^2. The symmetric subfamily v=0",
        "would be an explicit extra null assumption, not a result of the current",
        "model.",
        "",
        "## What the current Gaussian already fixes",
        "",
        "For u=Lk, the exact normalized Gaussian is",
        "`exp(-u^2/2)=1-u^2/2+u^4/8+O(u^6)`. The current relaxation-diffusion",
        "bridge matches only the quadratic term. Adding the lowest stabilizing",
        "fourth derivative gives the rational match",
        "`1/(1+u^2/2+u^4/8)`, which agrees through order u^4.",
        "",
        "| range | k^2 field max error | k^4 field max error |",
        "| --- | ---: | ---: |",
        f"| u<=0.5 | {_fmt(matching['rd_max_abs_error_u_le_0p5'])} | {_fmt(matching['k4_max_abs_error_u_le_0p5'])} |",
        f"| u<=1 | {_fmt(matching['rd_max_abs_error_u_le_1'])} | {_fmt(matching['k4_max_abs_error_u_le_1'])} |",
        "",
        "This fixes a low-k approximation, not the exact global kernel. A",
        "derivative-only source sets s0=0 and therefore H(0)=0 exactly, showing",
        "that zero mean is a source/operator constraint rather than an amplitude",
        "selected by the random walk.",
        "",
        "## First open mechanism",
        "",
        "Write the dimensionless linear denominator as",
        "`P(u)=1+a2 u^2+u^4`. For a2<0 its minimum occurs at",
        "`u_*=sqrt(-a2/2)` and has value `1-a2^2/4`.",
        "",
        "| case | u_* | minimum P | classification |",
        "| --- | ---: | ---: | --- |",
    ]
    for name, label in (
        ("finite_k_stable", "a2=-1.8"),
        ("finite_k_critical", "a2=-2.0"),
        ("finite_k_unstable", "a2=-2.2"),
    ):
        row = stability[name]
        lines.append(
            f"| {label} | {_fmt(row['preferred_wavenumber'] * args.gaussian_length)} | "
            f"{_fmt(row['minimum_denominator'])} | {row['classification']} |"
        )
    lines.extend(
        [
            "",
            "The sign change a2<0 is not implied by the Gaussian baseline. It is",
            "the first explicit new mechanism: anti-diffusive growth around a",
            "finite wave-number shell, stabilized in the ultraviolet by the",
            "fourth derivative. Beyond the critical value a positive cubic term",
            "can bound growth. A quadratic term is also allowed unless an internal",
            "sign symmetry is added; neither term guarantees localized knots,",
            "discrete branches, or quantized states.",
            "",
            "## Ambient-rank null",
            "",
            "Applying the same scalar transfer independently to every ambient",
            "component gives `T=H I_d` and `S_out=|H|^2 S_in`. In the fixed",
            f"d={args.ambient_dimension} audit the input/output ranks are",
            f"`{rank['input_rank']}/{rank['output_rank']}` and all normalized",
            "transfer singular values equal one. There is no eigengap after",
            "component three. Thus this operator family cannot select three",
            "directions without a cross-component order parameter or another",
            "symmetry-breaking mechanism.",
            "",
            "## Decision",
            "",
            "1. Treat K_eff as the response of a local augmented field rather than",
            "   as a freely scanned radial function.",
            "2. Retain the k^2 and k^4 Gaussian matches as linear null families.",
            "3. Do not infer the sign a2<0, either nonlinear coefficient, dimension",
            "   three, or quantization from the random walk or existing compact",
            "   branch.",
            "4. If a new dynamic pilot is opened, vary no kernel amplitudes. Test",
            "   exactly one finite-k field law with v=0 declared as a symmetric",
            "   null, against positive-a2, cubic-off, source-off, and eta-zero",
            "   controls with fixed coefficients across seeds. Primary observables",
            "   must be the field spectral peak and",
            "   width, branch/gap persistence, source-to-field closure, and knot",
            "   shape bounds.",
            "",
            "A positive pilot would establish classical pattern-forming branches,",
            "not QFT or quantization. Quantized language remains blocked until",
            "isolated seed-stable branches, spectral gaps, and controlled",
            "transition rules are demonstrated.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{payload['git_revision']}`",
            f"- Git status before generation: `{payload['git_status'] or 'clean'}`",
            "- Script: `experiments/current/kernels/field/local_field_operator_audit.py`",
        ]
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    write_outputs(parse_args())


if __name__ == "__main__":
    main()
