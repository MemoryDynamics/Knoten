from __future__ import annotations

from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np

from emergenz_knoten import (
    FiniteMemoryCheckpoint,
    FiniteMemoryState,
    SimulationConfig,
    save_finite_memory_checkpoint,
)
from emergenz_knoten.kernels import exponential_memory_weights


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "closure"
    / "p38f_canonical_write_gate.py"
)
SPEC = importlib.util.spec_from_file_location("p38f_canonical_write_gate", SCRIPT)
p38f = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = p38f
SPEC.loader.exec_module(p38f)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_bundle(root: Path) -> Path:
    config = SimulationConfig(
        steps=20,
        dim=2,
        epsilon=0.05,
        eta=0.15,
        alpha=0.2,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=5.0,
        memory_factor=1.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )
    entries = []
    weights = exponential_memory_weights(config.alpha, 5)
    for seed in p38f.REGISTERED_SEEDS:
        angle = 0.17 * seed
        memory = np.column_stack(
            (
                np.linspace(0.0, -0.4, 5),
                0.08 * np.sin(np.arange(5) + angle),
            )
        )
        state = FiniteMemoryState(
            x=memory[0],
            memory=memory,
            weights=weights,
        )
        checkpoint = FiniteMemoryCheckpoint(
            state=state,
            config=config,
            update_index=20,
            formation_seed=seed,
            created_utc="2026-08-15T00:00:00+00:00",
            git_revision="formation-revision",
            generator="test_p38f_canonical_write_gate",
        )
        filename = f"state_seed{seed}.npz"
        path = save_finite_memory_checkpoint(checkpoint, root / filename)
        entries.append(
            {
                "seed": seed,
                "checkpoint": filename,
                "checkpoint_sha256": _sha256(path),
                "config": asdict(config),
            }
        )
    manifest = {
        "schema": "emergenz-knoten.p38f-state-bundle",
        "schema_version": 1,
        "expected_seeds": p38f.REGISTERED_SEEDS,
        "entries": entries,
    }
    path = root / "bundle_manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def test_seed_shards_round_trip_and_aggregate_out_of_order(tmp_path: Path) -> None:
    bundle = _write_bundle(tmp_path / "bundle")
    shard_dir = tmp_path / "shards"
    paths = [
        p38f.simulate_seed(
            bundle,
            seed,
            shard_dir,
            simulation_revision="simulation-revision",
            overwrite=False,
        )
        for seed in p38f.REGISTERED_SEEDS
    ]

    payload = p38f.aggregate_shards(list(reversed(paths)))

    assert payload["schema"] == p38f.AGGREGATE_SCHEMA
    assert [row["seed"] for row in payload["seed_rows"]] == p38f.REGISTERED_SEEDS
    assert [row["seed"] for row in payload["shards"]] == p38f.REGISTERED_SEEDS
    assert [Path(row["manifest"]).name for row in payload["shards"]] == [
        f"p38f_seed{seed}.json" for seed in p38f.REGISTERED_SEEDS
    ]
    assert payload["g0_seed_passes"] == 5
    assert payload["gate_hierarchy"]["experimental-validity"].passed
    assert payload["gate_hierarchy"]["second-state-selection"].status.value in {
        "not-run",
        "blocked",
    }


def test_seed_shard_rejects_tampered_archive(tmp_path: Path) -> None:
    bundle = _write_bundle(tmp_path / "bundle")
    manifest_path = p38f.simulate_seed(
        bundle,
        1,
        tmp_path / "shards",
        simulation_revision="simulation-revision",
        overwrite=False,
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    archive = Path(manifest["archive"])
    archive.write_bytes(archive.read_bytes() + b"tampered")

    with np.testing.assert_raises_regex(ValueError, "archive hash mismatch"):
        p38f._load_shard(manifest_path)
