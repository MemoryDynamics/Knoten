from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np

from emergenz_knoten import SimulationConfig, load_finite_memory_checkpoint
from emergenz_knoten.kernels import exponential_memory_weights


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "representations"
    / "curate_p38f_state_bundle.py"
)
SPEC = importlib.util.spec_from_file_location("curate_p38f_state_bundle", SCRIPT)
curation = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = curation
SPEC.loader.exec_module(curation)


def _write_source(path: Path, *, seed: int) -> None:
    config = SimulationConfig(
        steps=10,
        dim=2,
        epsilon=0.01,
        eta=0.15,
        alpha=0.2,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=5.0,
        memory_factor=5.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )
    memory = np.column_stack(
        (
            np.linspace(0.2, -0.2, 5) + seed,
            np.linspace(-0.1, 0.1, 5),
        )
    )
    payload = {
        "condition": "baseline",
        "config": config.__dict__,
        "diagnostics": {
            "memory_cloud": {
                "snapshot": {
                    "points": memory.tolist(),
                    "weights": exponential_memory_weights(0.2, 5).tolist(),
                }
            }
        },
        "elapsed_seconds": 2.5,
        "git_revision": "source-revision",
        "git_status": "",
        "seed": seed,
        "started_utc": "2026-08-15T00:00:00Z",
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_curated_bundle_round_trips_complete_states(tmp_path: Path) -> None:
    sources = []
    for seed in (1, 2):
        path = tmp_path / f"source_seed{seed}.json"
        _write_source(path, seed=seed)
        sources.append(path)
    output = tmp_path / "bundle"

    manifest = curation.curate_bundle(
        sources,
        output,
        expected_seeds=[1, 2],
        curation_revision="curation-revision",
        overwrite=False,
    )

    assert manifest["schema"] == curation.BUNDLE_SCHEMA
    assert manifest["expected_seeds"] == [1, 2]
    assert len(manifest["entries"]) == 2
    for entry in manifest["entries"]:
        checkpoint = load_finite_memory_checkpoint(output / entry["checkpoint"])
        assert checkpoint.formation_seed == entry["seed"]
        assert checkpoint.git_revision == "source-revision"
        assert checkpoint.created_utc == "2026-08-15T00:00:02Z"


def test_curated_bundle_rejects_missing_seed(tmp_path: Path) -> None:
    source = tmp_path / "source_seed1.json"
    _write_source(source, seed=1)

    with np.testing.assert_raises_regex(ValueError, "do not match expected"):
        curation.curate_bundle(
            [source],
            tmp_path / "bundle",
            expected_seeds=[1, 2],
            curation_revision="revision",
            overwrite=False,
        )
