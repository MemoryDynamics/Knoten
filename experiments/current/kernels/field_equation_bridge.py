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
    gaussian_heat_time,
    gaussian_transfer,
    heat_transfer,
    low_wavenumber_matched_field,
    stationary_field_transfer,
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
            "Relate the current Gaussian convolution to an exact auxiliary "
            "heat flow and compare it with a local relaxation-diffusion "
            "mediator's stationary Green transfer."
        )
    )
    parser.add_argument("--gaussian-length", type=float, default=3.0)
    parser.add_argument("--diffusivity", type=float, default=1.0)
    parser.add_argument("--decay-rate", type=float, default=1.0)
    parser.add_argument("--coupling", type=float, default=1.0)
    parser.add_argument("--max-dimensionless-wavenumber", type=float, default=6.0)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/kernels/field/field_equation_bridge_2026-07-18.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/kernels/field/field_equation_bridge_2026-07-18.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/kernels/field_2026-07-18/field_equation_bridge.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _validate_args(args: argparse.Namespace) -> None:
    for name in (
        "gaussian_length",
        "diffusivity",
        "decay_rate",
        "max_dimensionless_wavenumber",
    ):
        value = float(getattr(args, name))
        if not math.isfinite(value) or value <= 0.0:
            raise SystemExit(f"--{name.replace('_', '-')} must be positive")
    if not math.isfinite(args.coupling):
        raise SystemExit("--coupling must be finite")


def bridge_payload(args: argparse.Namespace) -> dict[str, object]:
    _validate_args(args)
    length = float(args.gaussian_length)
    u = np.linspace(0.0, args.max_dimensionless_wavenumber, 2401)
    k = u / length
    diffusion_time = gaussian_heat_time(
        length=length,
        diffusivity=args.diffusivity,
    )
    gaussian = gaussian_transfer(k, length=length)
    heat = heat_transfer(
        k,
        diffusivity=args.diffusivity,
        diffusion_time=diffusion_time,
    )
    field = low_wavenumber_matched_field(
        gaussian_length=length,
        decay_rate=args.decay_rate,
        coupling=args.coupling,
    )
    stationary = stationary_field_transfer(
        k,
        field,
        normalize_zero_mode=True,
    )
    relative = np.abs(stationary - gaussian) / np.maximum(gaussian, 1.0e-15)

    def max_abs_below(limit: float) -> float:
        mask = u <= limit
        return float(np.max(np.abs(stationary[mask] - gaussian[mask])))

    return {
        "dimensionless_wavenumber": u,
        "gaussian_transfer": gaussian,
        "heat_transfer": heat,
        "stationary_field_transfer": stationary,
        "relative_difference": relative,
        "field": field,
        "diffusion_time": diffusion_time,
        "exact_heat_max_error": float(np.max(np.abs(gaussian - heat))),
        "stationary_max_abs_error_u_le_0p5": max_abs_below(0.5),
        "stationary_max_abs_error_u_le_1": max_abs_below(1.0),
        "stationary_max_abs_error_u_le_3": max_abs_below(3.0),
    }


def _plot(payload: dict[str, object], output: Path) -> None:
    u = np.asarray(payload["dimensionless_wavenumber"], dtype=float)
    gaussian = np.asarray(payload["gaussian_transfer"], dtype=float)
    heat = np.asarray(payload["heat_transfer"], dtype=float)
    stationary = np.asarray(payload["stationary_field_transfer"], dtype=float)
    relative = np.asarray(payload["relative_difference"], dtype=float)

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))
    axes[0].plot(u, gaussian, color="#202020", linewidth=2.2, label="Gaussian")
    axes[0].plot(
        u,
        heat,
        color="#147d64",
        linestyle="--",
        linewidth=1.8,
        label="auxiliary heat flow",
    )
    axes[0].set_title("Exact representation")

    axes[1].plot(u, gaussian, color="#202020", linewidth=2.2, label="Gaussian")
    axes[1].plot(
        u,
        stationary,
        color="#c23b22",
        linewidth=1.9,
        label="stationary local field",
    )
    axes[1].set_title("Low-k-matched field is a new model")

    axes[2].plot(u, relative, color="#7a4eab", linewidth=2.0)
    axes[2].set_yscale("log")
    axes[2].set_title("Relative transfer difference")
    axes[2].set_ylabel("|T_field-T_G| / T_G")

    for axis in axes:
        axis.set_xlabel("u = k L_G")
        axis.set_xlim(0.0, float(u[-1]))
        axis.grid(True, alpha=0.22)
        handles, labels = axis.get_legend_handles_labels()
        if handles:
            axis.legend(frameon=False, fontsize=8)
    axes[0].set_ylabel("zero-mode-normalized transfer")
    axes[1].set_ylabel("zero-mode-normalized transfer")
    fig.suptitle("From Gaussian kernel width to a local scalar mediator")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=190)
    plt.close(fig)


def write_outputs(args: argparse.Namespace) -> None:
    payload = bridge_payload(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    source_git_revision = _git_output(["rev-parse", "HEAD"])
    source_git_status = _git_output(["status", "--short"])
    _plot(payload, figure)
    field = payload["field"]
    assert hasattr(field, "correlation_length")
    generated = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    serializable = {
        "description": "Gaussian-to-local-field equation bridge.",
        "generated_utc": generated,
        "git_revision": source_git_revision,
        "git_status": source_git_status,
        "inputs": {
            "gaussian_length": args.gaussian_length,
            "diffusivity": args.diffusivity,
            "decay_rate": args.decay_rate,
            "coupling": args.coupling,
            "max_dimensionless_wavenumber": args.max_dimensionless_wavenumber,
        },
        "heat_diffusion_time": payload["diffusion_time"],
        "field": asdict(field),
        "field_correlation_length": field.correlation_length,
        "exact_heat_max_error": payload["exact_heat_max_error"],
        "stationary_max_abs_error_u_le_0p5": payload[
            "stationary_max_abs_error_u_le_0p5"
        ],
        "stationary_max_abs_error_u_le_1": payload["stationary_max_abs_error_u_le_1"],
        "stationary_max_abs_error_u_le_3": payload["stationary_max_abs_error_u_le_3"],
    }
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(serializable, indent=2, sort_keys=True), encoding="utf-8"
    )

    lines = [
        "# Field-Equation Bridge",
        "",
        f"Date: {generated}.",
        "",
        "## Exact statement for the current Gaussian",
        "",
        "A Gaussian convolution of width `L_G` is exactly the heat-semigroup",
        "snapshot",
        "",
        "```text",
        "partial_s u = D Delta u,    u(0)=rho,",
        "phi = u(s_G),               s_G=L_G^2/(2D).",
        "```",
        "",
        "This auxiliary coordinate `s` is a mathematical kernel construction,",
        "not yet physical update time or finite-speed propagation.",
        "",
        f"![Field equation bridge]({_rel_from(report, figure)})",
        "",
        "## Candidate local mediator",
        "",
        "```text",
        "tau_phi partial_t phi = D_phi Delta phi - mu_phi phi + g_phi rho.",
        "```",
        "",
        "Its stationary Fourier-space Green transfer is",
        "`g_phi/(mu_phi+D_phi k^2)` and its correlation length is",
        "`L_phi=sqrt(D_phi/mu_phi)`. Matching the Gaussian only through order",
        "`k^2` gives `L_phi=L_G/sqrt(2)`.",
        "",
        "| quantity | value |",
        "| --- | ---: |",
        f"| Gaussian width L_G | {args.gaussian_length:.8g} |",
        f"| exact heat time s_G | {float(payload['diffusion_time']):.8g} |",
        f"| matched field length L_phi | {field.correlation_length:.8g} |",
        f"| exact heat representation max error | {float(payload['exact_heat_max_error']):.3e} |",
        f"| field/Gaussian max abs error, kL<=0.5 | {float(payload['stationary_max_abs_error_u_le_0p5']):.3e} |",
        f"| field/Gaussian max abs error, kL<=1 | {float(payload['stationary_max_abs_error_u_le_1']):.3e} |",
        f"| field/Gaussian max abs error, kL<=3 | {float(payload['stationary_max_abs_error_u_le_3']):.3e} |",
        "",
        "## Decision",
        "",
        "The current Gaussian already has an exact local heat-flow generator",
        "in an auxiliary smoothing coordinate. Promoting the interaction to a",
        "physical relaxation-diffusion field is nevertheless a model change:",
        "the stationary Green transfer agrees only at long wavelengths. The",
        "field state must therefore be added to the Markov state and validated",
        "against knot and response controls before replacing the kernel.",
        "A hyperbolic/telegraph field is deferred until finite propagation is",
        "actually tested.",
        "",
        "## Provenance",
        "",
        f"- Git revision: `{serializable['git_revision']}`",
        f"- Git status: `{serializable['git_status'] or 'clean'}`",
        "- Script: `experiments/current/kernels/field_equation_bridge.py`",
        "",
    ]
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_outputs(parse_args())


if __name__ == "__main__":
    main()
