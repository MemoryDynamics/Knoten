from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments/current/memory/closure/eta_zero_raw_mode_null_audit.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "eta_zero_raw_mode_null_audit", SCRIPT
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_small_null_audit_classifies_complex_mode_as_unsupported() -> None:
    module = _load_module()
    args = argparse.Namespace(
        steps=3_000,
        burn_in=200,
        sample_every=10,
        seeds=[1, 2],
        segments=2,
        lags=[1, 2],
        epsilon=1e-3,
        lambda_value=0.02,
        box_length=40.0,
        n_low_modes=2,
        deposition_sigma=0.0,
        diffusion_length_ratio=0.3,
        sigma_att=3.0,
        ridge=1e-6,
        complex_tolerance=1e-6,
        identity_json=Path("reports/memory/closure/low_mode_identity_audit_2026-07-20.json"),
        closure_json=Path(
            "reports/memory/closure/low_mode_ar_feature_closure_long_N1M_2026-07-19.json"
        ),
        report=Path("unused.md"),
        summary_json=Path("unused.json"),
        figure=Path("unused.png"),
    )
    payload = module.build_payload(args)
    assert payload["gate"]["analytic_raw_operator_has_complex_modes"] is False
    assert payload["gate"]["physical_complex_mode_supported"] is False
    assert payload["gate"]["p2_null_classification_complete"] is True
    assert len(payload["analytic_rows"]) == 4
    assert {row["scope"] for row in payload["fit_summaries"]} == {
        "pooled",
        "seed",
        "segment",
    }
