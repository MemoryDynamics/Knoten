from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

from emergenz_knoten import SimulationConfig, load_finite_memory_checkpoint


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "current" / "memory" / "reference_state_checkpoints.py"


def load_module():
    spec = importlib.util.spec_from_file_location("reference_state_checkpoints", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_reference_state_job_writes_reloadable_complete_checkpoint(
    tmp_path: Path,
) -> None:
    module = load_module()
    config = SimulationConfig(
        steps=80,
        dim=2,
        epsilon=1e-4,
        eta=0.15,
        alpha=0.1,
        memory_mass=1.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=2.0,
        memory_factor=2.0,
        max_memory=50,
        burn_in=0,
        sample_every=80,
    )
    job = module.FormationJob(
        config=config,
        seed=3,
        output_dir=tmp_path,
        git_revision="abc1234",
        overwrite=False,
    )

    result = module._run_job(job)
    checkpoint = load_finite_memory_checkpoint(Path(result["checkpoint"]))

    assert checkpoint.config == config
    assert checkpoint.update_index == 80
    assert checkpoint.formation_seed == 3
    assert checkpoint.state.n_memory == 20
    assert result["state_geometry"]["memory_points"] == 20
    assert result["checkpoint_bytes"] > 0
    assert result["post_save_validation"]["schema_checksum_reload"] is True
    assert result["post_save_validation"]["exact_array_reload"] is True


def test_reference_state_cli_list_validation() -> None:
    module = load_module()

    assert module._parse_positive_ints("3,10", name="--dims") == [3, 10]
