"""Inspect a fixed archive selection without importing or executing a simulator.

This is an inventory, not an automatic verdict about statistical sufficiency.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
PAIR_REPORTS = (
    "reciprocal_full_knot_gate_2026-08-04",
    "retarded_reciprocal_full_knot_gate_2026-08-04",
    "p32_accumulation_control_N500k_2026-08-06",
)
FILES = tuple(f"reports/response/reciprocal/{name}.json" for name in PAIR_REPORTS) + (
    "data/processed/reference_states/scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/"
    "scalar_Aatt35_d3_seed1_N100000000.npz",
    "reports/memory/closure/emergent_modal_state_reconciliation_2026-08-13.responses.npz",
    "data/processed/p38f_canonical_write_2026-08-15/shards/p38f_seed1.npz",
    "experiments/current/memory/synchronization/reciprocity/reciprocal_full_knot_gate.py",
    "experiments/current/memory/synchronization/reciprocity/retarded_reciprocal_full_knot_gate.py",
    "experiments/current/memory/synchronization/reciprocity/p32_accumulation_control.py",
    "experiments/current/memory/closure/p38f_canonical_write_gate.py",
    "src/emergenz_knoten/canonical_write_port.py",
    "src/emergenz_knoten/reciprocal_nodes.py",
)


def list_lengths(value: object, path: str = "$") -> list[dict]:
    """Visit all JSON lists, not just the first row of a putative schema."""
    result = []
    if isinstance(value, dict):
        for key, child in value.items():
            result.extend(list_lengths(child, f"{path}.{key}"))
    elif isinstance(value, list):
        result.append({"path": path, "length": len(value)})
        for index, child in enumerate(value):
            result.extend(list_lengths(child, f"{path}[{index}]"))
    return result


def describe(path: Path) -> dict:
    with path.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    result = {"bytes": path.stat().st_size, "sha256": digest}
    if path.suffix in {".json", ".py"}:
        source_text = path.read_text(encoding="utf-8")
        result["sha256_utf8_lf"] = hashlib.sha256(
            source_text.encode("utf-8")
        ).hexdigest()
    if path.suffix == ".json":
        payload = json.loads(source_text)
        lengths = list_lengths(payload)
        base = payload.get("base_gate", payload)
        rows = base.get("rows", [])
        result.update(
            schema=payload.get("schema"),
            declared_revision=payload.get("git_revision"),
            declared_git_status=payload.get("git_status"),
            root_keys=sorted(payload),
            parameters={
                key: base.get("parameters", {}).get(key)
                for key in ("updates", "sample_every", "future_seeds")
            },
            row_count=len(rows),
            condition_keys=sorted(
                {key for row in rows for key in row.get("conditions", {})}
            ),
            condition_record_keys=sorted(
                {
                    key
                    for row in rows
                    for condition in row.get("conditions", {}).values()
                    for key in condition
                }
            ),
            list_count=len(lengths),
            longest_lists=sorted(
                lengths, key=lambda item: (-item["length"], item["path"])
            )[:5],
        )
    elif path.suffix == ".npz":
        groups = {}
        with np.load(path, allow_pickle=False) as arrays:
            for key in sorted(arrays.files):
                array = arrays[key]
                group = groups.setdefault((array.shape, str(array.dtype)), [])
                group.append(key)
            result["array_count"] = len(arrays.files)
        result["array_groups"] = [
            {
                "shape": list(shape),
                "dtype": dtype,
                "count": len(keys),
                "example_keys": keys[:3],
            }
            for (shape, dtype), keys in sorted(groups.items())
        ]
    return result


def inventory(root: Path) -> dict:
    return {
        "schema": "emergenz-knoten.memory-pair-archive-inventory.v1",
        "scope": "explicit file selection; not an exhaustive filesystem search",
        "operation": "read bytes, JSON layouts and NPZ arrays only; no trajectory replay",
        "hash_convention": "sha256: working-tree bytes; sha256_utf8_lf: UTF-8 text with universal newlines normalized to LF",
        "files": {name: describe(root / name) for name in FILES},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()
    output = json.dumps(inventory(args.root), indent=2, sort_keys=True) + "\n"
    if args.output_json is None:
        print(output, end="")
    else:
        args.output_json.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
