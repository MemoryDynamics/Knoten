from __future__ import annotations

import argparse
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

from emergenz_knoten.spectral_memory_field import (  # noqa: E402
    SpectralMemoryConfig,
    advance_collapsed_potential_state,
    advance_state,
    collapse_memory_to_potential,
    collapsed_potential_gradient,
    initialize_collapsed_potential_state,
    initialize_state,
    kernel_transfer,
    periodic_displacement,
    potential_gradient,
    wavenumbers,
    zero_mean_attractive_kernel,
)


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(item < 0 for item in values):
        raise argparse.ArgumentTypeError("expected non-negative comma-separated integers")
    return values


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the exact reparameterization from separate write/read kernels "
            "to a signed potential-memory write with identity readout."
        )
    )
    parser.add_argument("--steps", type=int, default=10_000)
    parser.add_argument("--sample-every", type=int, default=20)
    parser.add_argument("--seeds", type=_parse_int_list, default=_parse_int_list("1,2,3"))
    parser.add_argument("--epsilon", type=float, default=1e-4)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--lambda-value", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--box-length", type=float, default=80.0)
    parser.add_argument("--n-modes", type=int, default=64)
    parser.add_argument("--deposition-sigma", type=float, default=0.0)
    parser.add_argument("--amplitude-att", type=float, default=26.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--sigma-comp", type=float, default=10.0)
    parser.add_argument("--tolerance", type=float, default=1e-10)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/kernels/field/write_read_reparameterization_audit_2026-07-30.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/kernels/field/write_read_reparameterization_audit_2026-07-30.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/kernels/field_2026-07-30/"
            "write_read_reparameterization_audit.png"
        ),
    )
    return parser.parse_args(argv)


def _validate_args(args: argparse.Namespace) -> None:
    if args.steps < 1 or args.sample_every < 1:
        raise SystemExit("--steps and --sample-every must be positive")
    if args.n_modes < 1:
        raise SystemExit("--n-modes must be positive")
    for name in (
        "epsilon",
        "eta",
        "memory_mass",
        "deposition_sigma",
    ):
        value = float(getattr(args, name))
        if not math.isfinite(value) or value < 0.0:
            raise SystemExit(f"--{name.replace('_', '-')} must be non-negative")
    for name in (
        "lambda_value",
        "box_length",
        "amplitude_att",
        "sigma_att",
        "sigma_comp",
        "tolerance",
    ):
        value = float(getattr(args, name))
        if not math.isfinite(value) or value <= 0.0:
            raise SystemExit(f"--{name.replace('_', '-')} must be positive")
    if args.lambda_value > 1.0:
        raise SystemExit("--lambda-value must not exceed one")


def _config(args: argparse.Namespace) -> SpectralMemoryConfig:
    return SpectralMemoryConfig(
        box_length=float(args.box_length),
        n_modes=int(args.n_modes),
        lambda_value=float(args.lambda_value),
        memory_mass=float(args.memory_mass),
        deposition_sigma=float(args.deposition_sigma),
        kernel=zero_mean_attractive_kernel(
            amplitude_att=float(args.amplitude_att),
            sigma_att=float(args.sigma_att),
            sigma_comp=float(args.sigma_comp),
        ),
    )


def run_pair(
    config: SpectralMemoryConfig,
    *,
    seed: int,
    steps: int,
    sample_every: int,
    epsilon: float,
    eta: float,
) -> dict[str, Any]:
    initial_x = 0.37 * config.box_length
    memory = initialize_state(config, x=initial_x)
    collapsed = initialize_collapsed_potential_state(config, x=initial_x)
    noise = np.random.default_rng(seed).normal(size=steps)

    sample_steps: list[int] = []
    memory_x: list[float] = []
    collapsed_x: list[float] = []
    path_error: list[float] = []
    field_error: list[float] = []
    gradient_error: list[float] = []

    for step, value in enumerate(noise, start=1):
        memory = advance_state(
            memory,
            config,
            epsilon=epsilon,
            eta=eta,
            noise=float(value),
        )
        collapsed = advance_collapsed_potential_state(
            collapsed,
            config,
            epsilon=epsilon,
            eta=eta,
            noise=float(value),
        )
        if step % sample_every != 0 and step != steps:
            continue

        expected_phi = collapse_memory_to_potential(
            config,
            memory.rho_coefficients,
        )
        denominator = max(float(np.linalg.norm(expected_phi)), np.finfo(float).tiny)
        old_gradient = potential_gradient(
            config,
            memory.rho_coefficients,
            x=memory.x,
        )
        new_gradient = collapsed_potential_gradient(
            config,
            collapsed.phi_coefficients,
            x=collapsed.x,
        )
        sample_steps.append(step)
        memory_x.append(memory.x)
        collapsed_x.append(collapsed.x)
        path_error.append(
            abs(
                periodic_displacement(
                    collapsed.x,
                    memory.x,
                    config.box_length,
                )
            )
        )
        field_error.append(
            float(np.linalg.norm(collapsed.phi_coefficients - expected_phi))
            / denominator
        )
        gradient_error.append(abs(new_gradient - old_gradient))

    return {
        "seed": int(seed),
        "sample_steps": sample_steps,
        "memory_x": memory_x,
        "collapsed_x": collapsed_x,
        "path_error": path_error,
        "relative_field_error": field_error,
        "gradient_error": gradient_error,
        "max_path_error": max(path_error, default=0.0),
        "max_relative_field_error": max(field_error, default=0.0),
        "max_gradient_error": max(gradient_error, default=0.0),
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    _validate_args(args)
    config = _config(args)
    runs = [
        run_pair(
            config,
            seed=seed,
            steps=int(args.steps),
            sample_every=int(args.sample_every),
            epsilon=float(args.epsilon),
            eta=float(args.eta),
        )
        for seed in args.seeds
    ]
    constant_field = np.zeros(config.n_modes + 1, dtype=np.complex128)
    constant_field[0] = 1.0
    constant_gradient = collapsed_potential_gradient(config, constant_field, x=17.0)
    maxima = {
        "path": max(run["max_path_error"] for run in runs),
        "relative_field": max(run["max_relative_field_error"] for run in runs),
        "gradient": max(run["max_gradient_error"] for run in runs),
    }
    passed = bool(
        all(value <= args.tolerance for value in maxima.values())
        and constant_gradient == 0.0
    )
    return {
        "question": (
            "Does moving the linear read kernel into deposition preserve the "
            "visible path and stored potential field under common noise?"
        ),
        "status": "structural" if passed else "failed_numerical_audit",
        "passed": passed,
        "equations": {
            "separate": "rho'=q rho+beta G_x; phi=K*rho",
            "collapsed": "phi'=q phi+beta (K*G)_x; read=delta",
            "induction": "phi_n=K*rho_n",
        },
        "parameters": {
            "steps": int(args.steps),
            "sample_every": int(args.sample_every),
            "seeds": list(args.seeds),
            "epsilon": float(args.epsilon),
            "eta": float(args.eta),
            "lambda_value": config.lambda_value,
            "memory_mass": config.memory_mass,
            "box_length": config.box_length,
            "n_modes": config.n_modes,
            "deposition_sigma": config.deposition_sigma,
            "amplitude_att": float(args.amplitude_att),
            "sigma_att": float(args.sigma_att),
            "sigma_comp": float(args.sigma_comp),
            "tolerance": float(args.tolerance),
        },
        "maximum_errors": maxima,
        "constant_kernel_gradient": constant_gradient,
        "claims": {
            "constant_kernel_is_identity": False,
            "dirac_readout_is_identity": True,
            "collapse_changes_visible_dynamics": False,
            "collapsed_field_is_nonnegative_density": False,
            "collapse_adds_field_self_dynamics": False,
        },
        "runs": runs,
    }


def _plot(args: argparse.Namespace, payload: dict[str, Any], output: Path) -> None:
    config = _config(args)
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 8.4))
    colors = plt.get_cmap("tab10")
    floor = 1e-18
    initial_x = 0.37 * config.box_length

    for index, run in enumerate(payload["runs"]):
        color = colors(index)
        steps = np.asarray(run["sample_steps"])
        axes[0, 0].plot(
            steps,
            np.asarray(run["memory_x"]) - initial_x,
            color=color,
            linewidth=1.7,
            label=f"seed {run['seed']}: separate",
        )
        axes[0, 0].plot(
            steps,
            np.asarray(run["collapsed_x"]) - initial_x,
            color=color,
            linewidth=1.0,
            linestyle="--",
            label=f"seed {run['seed']}: collapsed",
        )
        axes[0, 1].semilogy(
            steps,
            np.maximum(run["path_error"], floor),
            color=color,
            label=f"seed {run['seed']}",
        )
        axes[1, 0].semilogy(
            steps,
            np.maximum(run["relative_field_error"], floor),
            color=color,
            label=f"seed {run['seed']}",
        )

    k = wavenumbers(config)
    write = np.exp(-0.5 * config.deposition_sigma**2 * k**2)
    read = kernel_transfer(config)
    effective = write * read
    scale = max(float(np.max(np.abs(effective))), np.finfo(float).tiny)
    axes[1, 1].plot(k, write, color="#377eb8", label="old write |G_hat|")
    axes[1, 1].plot(k, np.abs(read) / scale, color="#c23b22", label="old read |K_hat| / max")
    axes[1, 1].plot(
        k,
        np.abs(effective) / scale,
        color="#147d64",
        linestyle="--",
        label="new write |K_hat G_hat| / max",
    )

    axes[0, 0].set(title="Visible path overlay", xlabel="update n", ylabel="periodic x - x0")
    axes[0, 1].set(title="Path disagreement", xlabel="update n", ylabel="periodic |delta x|")
    axes[1, 0].set(title="Stored-field identity", xlabel="update n", ylabel="relative ||phi-K rho||")
    axes[1, 1].set(title="Write/read factorization", xlabel="wavenumber k", ylabel="transfer magnitude")
    for axis in axes.flat:
        axis.grid(True, alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Write/read reparameterization: same dynamics, different state meaning")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=190)
    plt.close(fig)


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


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative_link(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def write_outputs(args: argparse.Namespace) -> None:
    payload = build_payload(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    generated = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    payload["generated_utc"] = generated
    payload["git_revision"] = _git_output(["rev-parse", "HEAD"])
    payload["git_status"] = _git_output(["status", "--porcelain"])
    payload["outputs"] = {
        "report": str(args.report),
        "summary_json": str(args.summary_json),
        "figure": str(args.figure),
    }

    _plot(args, payload, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    compact_payload = {key: value for key, value in payload.items() if key != "runs"}
    compact_payload["runs"] = [
        {
            "seed": run["seed"],
            "max_path_error": run["max_path_error"],
            "max_relative_field_error": run["max_relative_field_error"],
            "max_gradient_error": run["max_gradient_error"],
        }
        for run in payload["runs"]
    ]
    summary.write_text(
        json.dumps(compact_payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    errors = payload["maximum_errors"]
    lines = [
        "# Write/Read Reparameterization Audit",
        "",
        f"Date: {generated}.",
        "",
        "## Question",
        "",
        "Can the separate linear interaction kernel be moved into the write",
        "operation without changing the visible stochastic dynamics?",
        "",
        f"![Audit figure]({_relative_link(report, figure)})",
        "",
        "## Structural identity",
        "",
        "For a translation-invariant linear write G and read K,",
        "",
        "```text",
        "rho_(n+1) = q rho_n + beta G_(x_(n+1)),",
        "phi_n = K*rho_n.",
        "```",
        "",
        "Defining the signed stored field `phi=K*rho` gives",
        "",
        "```text",
        "phi_(n+1) = q phi_n + beta (K*G)_(x_(n+1)).",
        "```",
        "",
        "The read operation is then convolution with the Dirac delta, not with",
        "the spatially constant function one. A constant kernel retains only the",
        "zero Fourier mode and therefore has exactly zero spatial gradient.",
        "",
        "## Fixed numerical audit",
        "",
        f"- status: **{payload['status']}**",
        f"- seeds: `{args.seeds}`; updates per seed: `{args.steps}`",
        f"- maximum periodic path error: `{errors['path']:.6e}`",
        f"- maximum relative stored-field error: `{errors['relative_field']:.6e}`",
        f"- maximum gradient error: `{errors['gradient']:.6e}`",
        f"- constant-kernel gradient: `{payload['constant_kernel_gradient']:.6e}`",
        f"- preregistered numerical tolerance: `{args.tolerance:.1e}`",
        "",
        "## Interpretation",
        "",
        "The collapse is an exact linear reparameterization. It simplifies the",
        "state semantics from a non-negative occupancy memory plus read kernel to",
        "a generally signed potential memory with identity readout. It does not",
        "make the field self-dynamic and does not create a new knot mechanism.",
        "",
        "A genuinely active field is the next separate model extension: its",
        "update must include a local field operator and, if tested, nonlinear",
        "saturation. The deposition should begin as a delta source so that the",
        "resolved field scale is selected by the field law rather than written in",
        "by a broad source mollifier.",
        "",
        "## Claim boundary",
        "",
        "This audit proves factorization non-identifiability for the current",
        "linear translation-invariant scalar model. It establishes neither",
        "field self-organization, vector memory, chirality, strings, quantization,",
        "nor dimension selection.",
        "",
        "## Provenance",
        "",
        f"- Git revision: `{payload['git_revision']}`",
        f"- Git status before generation: `{payload['git_status'] or 'clean'}`",
        "- Script: `experiments/current/kernels/write_read_reparameterization_audit.py`",
    ]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    write_outputs(parse_args())


if __name__ == "__main__":
    main()
