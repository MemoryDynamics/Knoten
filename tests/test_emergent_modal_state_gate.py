from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "closure"
    / "emergent_modal_state_gate.py"
)
SPEC = importlib.util.spec_from_file_location("emergent_modal_state_gate", SCRIPT)
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


def test_response_archive_separates_lossless_panels_from_summary(tmp_path: Path) -> None:
    first = np.arange(24, dtype=float).reshape(4, 2, 3)
    second = -0.25 * first
    payload = {
        "sample_steps": np.array([0, 5, 10, 15]),
        "registration": {"kr_values": np.array([0.5, 2.0])},
        "analysis": {
            "aggregate_responses": {
                "0.5": first,
                "2.0": second,
            }
        },
    }
    path = tmp_path / "responses.npz"

    metadata = gate.write_response_archive(payload, path)

    assert metadata["path"].endswith("responses.npz")
    assert len(metadata["sha256"]) == 64
    with np.load(path, allow_pickle=False) as archive:
        np.testing.assert_array_equal(archive["sample_steps"], payload["sample_steps"])
        np.testing.assert_allclose(
            archive[metadata["response_keys"]["0.5"]],
            first,
        )
        np.testing.assert_allclose(
            archive[metadata["response_keys"]["2.0"]],
            second,
        )
