from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT / "experiments" / "current" / "dynamics" / "dimension_over_n_reproduction.py"
)
SPEC = importlib.util.spec_from_file_location("dimension_over_n_reproduction", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_report_keeps_dimension_claims_bounded() -> None:
    payload = {
        "question": "test",
        "matched_seeds": [1, 2, 3],
        "summary": [
            {
                "steps": 1_000_000,
                "sample_count": 1_000,
                "sample_every": 1_000,
                "seed_count": 3,
                "D_win_valid_count": 2,
                "D_cov": {"median": 2.5},
                "D_occ": {"median": 1.0},
                "D_win": {"median": 1.8},
                "D_mem": {"median": 9.1},
            }
        ],
        "diagnostics": {
            "D_mem_median_min": 8.9,
            "D_mem_median_max": 9.3,
        },
        "git_revision": "abc",
        "git_status": "",
    }

    report = MODULE.render_report(
        payload,
        generated="2026-07-30T00:00:00Z",
        figure_link="figure.png",
    )

    assert "not evidence for selection of three dimensions" in report
    assert "sampling-cadence sensitivity" in report
    assert "No N-only law for occupancy dimension" in report


def test_quantiles_ignore_missing_values() -> None:
    result = MODULE._quantiles([None, 1.0, 2.0, 3.0])

    assert result["median"] == 2.0
    assert result["q1"] == 1.5
    assert result["q3"] == 2.5


def test_payload_summary_excludes_invalid_window_fit(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    original = MODULE.CHECKPOINTS
    MODULE.CHECKPOINTS = {100: "n100"}
    try:
        for seed, dimension, valid in [(1, 1.5, True), (2, 9.0, False)]:
            folder = data_root / "n100"
            folder.mkdir(parents=True, exist_ok=True)
            payload = {
                "condition": "baseline",
                "seed": seed,
                "config": {
                    "steps": 100,
                    "sample_every": 10,
                    **{key: 1 for key in MODULE.CONFIG_KEYS},
                },
                "diagnostics": {
                    "n_samples": 10,
                    "sample_shape": {"effective_dimension": 2.0},
                    "occupancy_dimension": 1.0,
                    "occupancy": {
                        "scaling_window": {
                            "dimension": dimension,
                            "valid_scaling": valid,
                        }
                    },
                    "memory_cloud": {"shape": {"effective_dimension": 3.0}},
                },
            }
            (folder / f"case_baseline_seed{seed}_steps100.json").write_text(
                __import__("json").dumps(payload),
                encoding="utf-8",
            )
        args = MODULE.parse_args(["--data-root", str(data_root), "--seeds", "1,2"])
        result = MODULE.build_payload(args)
    finally:
        MODULE.CHECKPOINTS = original

    assert result["summary"][0]["D_win"]["median"] == 1.5
    assert result["summary"][0]["D_win_valid_count"] == 1
    assert (
        result["measurement_convergence"]["D_occ"]["reason"]
        == "insufficient_checkpoints"
    )
    assert not result["measurement_convergence"]["D_occ"][
        "measurement_convergence_evaluable"
    ]
    report = MODULE.render_report(
        result,
        generated="2026-07-31T00:00:00Z",
        figure_link="figure.png",
    )
    assert "only 1 of 5 required checkpoints exist" in report
