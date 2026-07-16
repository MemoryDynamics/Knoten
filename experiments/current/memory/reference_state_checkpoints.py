"""Build complete long-N scalar-memory reference-state checkpoints."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, replace
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

import numpy as np

from emergenz_knoten import (
    FiniteMemoryCheckpoint,
    SimulationConfig,
    finite_memory_checkpoint_manifest,
    load_finite_memory_checkpoint,
    memory_centroid,
    memory_shape_tensor,
    save_finite_memory_checkpoint,
    shape_statistics,
    simulate_final_finite_memory_state,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
GENERATOR = "experiments/current/memory/reference_state_checkpoints.py"


@dataclass(frozen=True)
class FormationJob:
    config: SimulationConfig
    seed: int
    output_dir: Path
    git_revision: str
    overwrite: bool


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


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
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, Path):
        try:
            return value.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            return value.as_posix()
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _parse_positive_ints(text: str, *, name: str) -> list[int]:
    values = [int(part.strip()) for part in text.split(",") if part.strip()]
    if not values or any(value < 1 for value in values):
        raise ValueError(f"{name} must contain positive integers")
    if len(set(values)) != len(values):
        raise ValueError(f"{name} must not contain duplicates")
    return values


def _checkpoint_name(config: SimulationConfig, seed: int) -> str:
    return (
        f"scalar_Aatt{config.amplitude_att:g}_d{config.dim}_seed{seed}_"
        f"N{config.steps}.npz"
    )


def _run_job(job: FormationJob) -> dict[str, Any]:
    destination = job.output_dir / _checkpoint_name(job.config, job.seed)
    if destination.exists() and not job.overwrite:
        raise FileExistsError(f"checkpoint already exists: {destination}")

    started = time.perf_counter()
    state = simulate_final_finite_memory_state(job.config, seed=job.seed)
    elapsed = time.perf_counter() - started
    checkpoint = FiniteMemoryCheckpoint(
        state=state,
        config=job.config,
        update_index=job.config.steps,
        formation_seed=job.seed,
        created_utc=_utc_now(),
        git_revision=job.git_revision,
        generator=GENERATOR,
    )
    save_finite_memory_checkpoint(checkpoint, destination)
    reloaded = load_finite_memory_checkpoint(destination)
    if not (
        np.array_equal(reloaded.state.x, state.x)
        and np.array_equal(reloaded.state.memory, state.memory)
        and np.array_equal(reloaded.state.weights, state.weights)
    ):
        raise RuntimeError("checkpoint reload did not reproduce the formed state")
    checkpoint = reloaded
    state = reloaded.state

    shape = shape_statistics(state.memory, weights=state.weights)
    tensor = memory_shape_tensor(state)
    center = memory_centroid(state)
    return {
        "checkpoint": destination,
        "checkpoint_bytes": destination.stat().st_size,
        "elapsed_seconds": elapsed,
        "steps_per_second": job.config.steps / elapsed,
        "post_save_validation": {
            "schema_checksum_reload": True,
            "exact_array_reload": True,
        },
        "manifest": finite_memory_checkpoint_manifest(checkpoint),
        "state_geometry": {
            "memory_points": state.n_memory,
            "stored_weight_mass": float(np.sum(state.weights)),
            "memory_center": center,
            "visible_to_center_distance": float(np.linalg.norm(state.x - center)),
            "rms_radius": float(np.sqrt(max(np.trace(tensor), 0.0))),
            "mean_radius": shape["mean_radius"],
            "shape_effective_dimension": shape["effective_dimension"],
            "axis_ratio_min_max": shape["axis_ratio_min_max"],
            "axis_ratio_intrinsic_min_max": shape["axis_ratio_intrinsic_min_max"],
            "shape_eigenvalues": shape["covariance_eigenvalues"],
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Form complete scalar z_N=(x_N,rho_N) checkpoints without storing "
            "the preceding trajectory."
        )
    )
    parser.add_argument("--steps", type=int, default=100_000_000)
    parser.add_argument("--dims", default="3,10")
    parser.add_argument("--seeds", default="1")
    parser.add_argument("--epsilon", type=float, default=1e-4)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--deposition-kernel", default="delta")
    parser.add_argument("--deposition-sigma", type=float, default=0.0)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=35.0)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--max-memory", type=int, default=800)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "data/processed/reference_states/"
            "scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        dims = _parse_positive_ints(args.dims, name="--dims")
        seeds = _parse_positive_ints(args.seeds, name="--seeds")
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if args.steps < 1:
        raise SystemExit("--steps must be positive")
    if args.workers < 1:
        raise SystemExit("--workers must be positive")
    if args.memory_mass <= 0.0:
        raise SystemExit("reference-state checkpoints require --memory-mass > 0")

    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    if git_status:
        raise SystemExit(
            "reference-state formation requires a clean worktree; commit or stash changes first"
        )

    jobs: list[FormationJob] = []
    for dim in dims:
        for seed in seeds:
            config = SimulationConfig(
                steps=args.steps,
                dim=dim,
                epsilon=args.epsilon,
                eta=args.eta,
                alpha=args.alpha,
                memory_mass=args.memory_mass,
                deposition_kernel=args.deposition_kernel,
                deposition_sigma=args.deposition_sigma,
                sigma_rep=args.sigma_rep,
                sigma_att=args.sigma_att,
                amplitude_rep=args.amplitude_rep,
                amplitude_att=args.amplitude_att,
                memory_factor=args.memory_factor,
                max_memory=args.max_memory,
                burn_in=0,
                sample_every=args.steps,
            )
            jobs.append(
                FormationJob(
                    config=config,
                    seed=seed,
                    output_dir=output_dir,
                    git_revision=git_revision,
                    overwrite=args.overwrite,
                )
            )

    results: list[dict[str, Any]] = []
    worker_count = min(args.workers, len(jobs))
    if worker_count == 1:
        for job in jobs:
            print(
                f"forming d={job.config.dim} seed={job.seed} N={job.config.steps}",
                flush=True,
            )
            results.append(_run_job(job))
    else:
        warmup = replace(jobs[0].config, steps=1, burn_in=0, sample_every=1)
        simulate_final_finite_memory_state(warmup, seed=0)
        print(f"forming {len(jobs)} checkpoints with {worker_count} workers", flush=True)
        with ProcessPoolExecutor(max_workers=worker_count) as executor:
            future_jobs = {executor.submit(_run_job, job): job for job in jobs}
            for future in as_completed(future_jobs):
                job = future_jobs[future]
                result = future.result()
                results.append(result)
                print(
                    f"completed d={job.config.dim} seed={job.seed} "
                    f"at {result['steps_per_second']:.0f} steps/s",
                    flush=True,
                )

    results.sort(
        key=lambda result: (
            int(result["manifest"]["config"]["dim"]),
            int(result["manifest"]["formation_seed"]),
        )
    )
    payload = {
        "schema": "emergenz-knoten.reference-state-index",
        "schema_version": 1,
        "generated_utc": _utc_now(),
        "git_revision": git_revision,
        "git_status": git_status,
        "command": [sys.executable, *sys.argv],
        "purpose": (
            "canonical branch points for paired free, weak-probe, frozen-source, "
            "and later multi-knot continuations"
        ),
        "continuation_design": (
            "all compared arms load the same z_N and receive the same explicit "
            "fresh future-noise array"
        ),
        "entries": results,
    }
    summary_path = output_dir / "reference_state_index.json"
    summary_path.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {summary_path.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
