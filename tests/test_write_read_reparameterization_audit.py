from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "kernels"
    / "write_read_reparameterization_audit.py"
)
SPEC = importlib.util.spec_from_file_location("write_read_audit", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_short_audit_passes_fixed_equivalence_gate() -> None:
    args = MODULE.parse_args([])
    args.steps = 200
    args.sample_every = 10
    args.seeds = [1, 2]

    payload = MODULE.build_payload(args)

    assert payload["passed"]
    assert payload["status"] == "structural"
    assert payload["constant_kernel_gradient"] == 0.0
    assert payload["maximum_errors"]["path"] <= args.tolerance
    assert not payload["claims"]["constant_kernel_is_identity"]
    assert payload["claims"]["dirac_readout_is_identity"]
