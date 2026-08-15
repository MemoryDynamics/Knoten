"""Curate the five mature P3.8f scalar states into validated checkpoints."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timedelta
import glob
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

import numpy as np

from emergenz_knoten import (
    FiniteMemoryCheckpoint,
    FiniteMemoryState,
    SimulationConfig,
    finite_memory_checkpoint_manifest,
    load_finite_memory_checkpoint,
    save_finite_memory_checkpoint,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
GENERATOR = (
    "experiments/current/memory/representations/curate_p38f_state_bundle.py"
)
BUNDLE_SCHEMA = "emergenz-knoten.p38f-state-bundle"
BUNDLE_SCHEMA_VERSION = 1
DEFAULT_SOURCE_GLOB = (
    "data/processed/long_run_metastability/"
    "raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/"
    "case_baseline_seed*_steps3000000.json"
)
DEFAULT_OUTPUT_DIR = (
    "data/processed/reference_states/"
    "p38f_scalar_Aatt35_N3M_d3_seed1-5_2026-08-15"
)


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


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _completed_utc(payload: dict[str, Any]) -> str:
    started = datetime.fromisoformat(str(payload["started_utc"]).replace("Z", "+00:00"))
    completed = started + timedelta(seconds=float(payload["elapsed_seconds"]))
    return completed.isoformat(timespec="seconds").replace("+00:00", "Z")


def checkpoint_from_snapshot(
    path: Path,
) -> tuple[FiniteMemoryCheckpoint, dict[str, Any]]:
    """Convert one complete long-run memory snapshot without resimulation."""

    source = path.resolve()
    payload = json.loads(source.read_text(encoding="utf-8"))
    if payload.get("condition") != "baseline":
        raise ValueError("P3.8f bundle accepts baseline snapshots only")
    config = SimulationConfig(**payload["config"])
    snapshot = payload["diagnostics"]["memory_cloud"]["snapshot"]
    memory = np.asarray(snapshot["points"], dtype=float)
    weights = np.asarray(snapshot["weights"], dtype=float)
    state = FiniteMemoryState(x=memory[0], memory=memory, weights=weights)
    checkpoint = FiniteMemoryCheckpoint(
        state=state,
        config=config,
        update_index=int(payload["config"]["steps"]),
        formation_seed=int(payload["seed"]),
        created_utc=_completed_utc(payload),
        git_revision=str(payload["git_revision"]),
        generator=GENERATOR,
    )
    return checkpoint, {
        "source_path": _relative(source),
        "source_sha256": _sha256(source),
        "source_git_status": str(payload.get("git_status", "unavailable")),
        "source_started_utc": str(payload["started_utc"]),
        "source_elapsed_seconds": float(payload["elapsed_seconds"]),
    }


def curate_bundle(
    source_paths: list[Path],
    output_dir: Path,
    *,
    expected_seeds: list[int],
    curation_revision: str,
    overwrite: bool,
) -> dict[str, Any]:
    """Write validated checkpoints and one hash-complete bundle manifest."""

    if not source_paths:
        raise ValueError("at least one source snapshot is required")
    if len(expected_seeds) != len(set(expected_seeds)) or not expected_seeds:
        raise ValueError("expected_seeds must be non-empty and unique")
    destination = output_dir.resolve()
    destination.mkdir(parents=True, exist_ok=True)

    converted = [checkpoint_from_snapshot(path) for path in source_paths]
    by_seed: dict[int, tuple[FiniteMemoryCheckpoint, dict[str, Any]]] = {}
    for checkpoint, provenance in converted:
        if checkpoint.formation_seed in by_seed:
            raise ValueError(f"duplicate source seed {checkpoint.formation_seed}")
        by_seed[checkpoint.formation_seed] = checkpoint, provenance
    if sorted(by_seed) != sorted(expected_seeds):
        raise ValueError(
            f"source seeds {sorted(by_seed)} do not match expected {sorted(expected_seeds)}"
        )

    reference_config = asdict(by_seed[expected_seeds[0]][0].config)
    entries = []
    for seed in expected_seeds:
        checkpoint, provenance = by_seed[seed]
        if asdict(checkpoint.config) != reference_config:
            raise ValueError("bundle checkpoints must share one simulation config")
        filename = (
            f"scalar_Aatt{checkpoint.config.amplitude_att:g}_"
            f"d{checkpoint.config.dim}_seed{seed}_N{checkpoint.update_index}.npz"
        )
        checkpoint_path = destination / filename
        if checkpoint_path.exists() and not overwrite:
            raise FileExistsError(f"checkpoint already exists: {checkpoint_path}")
        save_finite_memory_checkpoint(checkpoint, checkpoint_path)
        reloaded = load_finite_memory_checkpoint(checkpoint_path)
        if finite_memory_checkpoint_manifest(reloaded) != finite_memory_checkpoint_manifest(
            checkpoint
        ):
            raise RuntimeError("checkpoint reload changed its canonical manifest")
        entries.append(
            {
                "seed": seed,
                "checkpoint": filename,
                "checkpoint_sha256": _sha256(checkpoint_path),
                "checkpoint_bytes": checkpoint_path.stat().st_size,
                "checkpoint_manifest": finite_memory_checkpoint_manifest(reloaded),
                **provenance,
            }
        )

    manifest = {
        "schema": BUNDLE_SCHEMA,
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "curation_revision": curation_revision,
        "generator": GENERATOR,
        "expected_seeds": expected_seeds,
        "shared_config": reference_config,
        "entries": entries,
    }
    manifest_path = destination / "bundle_manifest.json"
    temporary = manifest_path.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(manifest_path)
    return {**manifest, "manifest": _relative(manifest_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-glob", default=DEFAULT_SOURCE_GLOB)
    parser.add_argument("--output-dir", type=Path, default=Path(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--seeds", default="1,2,3,4,5")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    status = _git_output(["status", "--porcelain"])
    if status not in ("", "unavailable") and not args.allow_dirty:
        raise RuntimeError("refusing dirty worktree; use --allow-dirty explicitly")
    seeds = [int(value.strip()) for value in args.seeds.split(",") if value.strip()]
    paths = sorted(Path(path).resolve() for path in glob.glob(str(_resolve(Path(args.source_glob)))))
    payload = curate_bundle(
        paths,
        _resolve(args.output_dir),
        expected_seeds=seeds,
        curation_revision=_git_output(["rev-parse", "HEAD"]),
        overwrite=args.overwrite,
    )
    print(
        json.dumps(
            {
                "manifest": payload["manifest"],
                "seeds": payload["expected_seeds"],
                "checkpoints": len(payload["entries"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
