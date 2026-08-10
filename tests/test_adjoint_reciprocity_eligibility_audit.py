from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from experiments.current.memory.closure.adjoint_reciprocity_eligibility_audit import (
    analyze_case,
)


def test_analyze_case_separates_normalized_source_from_raw_control(
    tmp_path: Path,
) -> None:
    path = tmp_path / "case.json"
    points = [[index * 2e-4, 0.0, 0.0] for index in range(20)]
    path.write_text(
        json.dumps(
            {
                "seed": 7,
                "diagnostics": {
                    "memory_cloud": {"snapshot": {"points": points}}
                },
            }
        ),
        encoding="utf-8",
    )

    row = analyze_case(
        path,
        relaxation=0.01,
        coupling=5e-6,
        forgetting_factor=0.99,
        metric_scales=[0.001, 1.0, 1000.0],
    )

    assert row["baseline_complex_fraction"] == 1.0
    assert not row["raw_direction_control"]["complex"]
    assert row["ambient_dimension"] == 3
    assert row["step_count"] == 19
    np.testing.assert_allclose(row["step_norm"]["median"], 2e-4)
    scales = row["metric_scale_sensitivity"]
    assert scales[0]["complex_fraction"] == 0.0
    assert scales[1]["complex_fraction"] == 1.0
    assert scales[2]["complex_fraction"] == 0.0
