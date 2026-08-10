from __future__ import annotations

from argparse import Namespace

import numpy as np

from experiments.current.memory.closure.balanced_full_memory_feature_gate import (
    _indices,
    evaluate_pair,
)


def _row(mode: np.ndarray) -> dict[str, object]:
    return {
        "rank": 1,
        "holdout_error": 0.05,
        "tail_energy_relative_se": 0.01,
        "_modes": mode,
    }


def test_indices_include_nondivisible_horizon() -> None:
    np.testing.assert_array_equal(_indices(7, 3), [0, 3, 6, 7])


def test_pair_gate_distinguishes_delay_equivalent_control() -> None:
    args = Namespace(
        max_rank=8,
        minimum_cosine=0.90,
        maximum_holdout_error=0.15,
        maximum_tail_relative_se=0.05,
    )
    actual_mode = np.array([[1.0], [0.0]])
    other_mode = np.array([[0.0], [1.0]])
    actual = [_row(actual_mode) for _ in range(12)]
    controls = {
        "flat": [_row(actual_mode), _row(actual_mode)],
        "shuffled": [_row(other_mode), _row(other_mode)],
    }
    result = evaluate_pair(actual, controls, args=args)
    assert result["pass"]
    assert result["controls"]["flat"]["equivalent"]
    assert not result["geometry_specific"]

    controls["flat"] = [_row(other_mode), _row(other_mode)]
    result = evaluate_pair(actual, controls, args=args)
    assert result["pass"]
    assert result["geometry_specific"]
