"""Versioned checkpoints for complete finite-memory Markov states."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path

import numpy as np

from .core import SimulationConfig, memory_horizon, validate_simulation_config
from .kernels import exponential_memory_weights
from .state import FiniteMemoryState

CHECKPOINT_SCHEMA = "emergenz-knoten.finite-memory-state"
CHECKPOINT_SCHEMA_VERSION = 1
FRESH_COMMON_NOISE_POLICY = (
    "fresh explicit common-noise stream per paired continuation experiment"
)


def _array_manifest(array: np.ndarray) -> dict[str, object]:
    contiguous = np.ascontiguousarray(array)
    digest = hashlib.sha256()
    digest.update(contiguous.dtype.str.encode("ascii"))
    digest.update(b"\0")
    digest.update(json.dumps(list(contiguous.shape), separators=(",", ":")).encode("ascii"))
    digest.update(b"\0")
    digest.update(contiguous.tobytes(order="C"))
    return {
        "dtype": contiguous.dtype.str,
        "shape": list(contiguous.shape),
        "sha256": digest.hexdigest(),
    }


@dataclass(frozen=True)
class FiniteMemoryCheckpoint:
    """Complete scalar Markov state plus formation provenance."""

    state: FiniteMemoryState
    config: SimulationConfig
    update_index: int
    formation_seed: int
    created_utc: str
    git_revision: str
    generator: str
    continuation_noise_policy: str = FRESH_COMMON_NOISE_POLICY

    def __post_init__(self) -> None:
        validate_simulation_config(self.config)
        if self.state.dim != self.config.dim:
            raise ValueError("checkpoint state dimension must match config")
        if isinstance(self.update_index, bool) or not isinstance(
            self.update_index, (int, np.integer)
        ):
            raise ValueError("update_index must be an integer")
        if self.update_index < 1:
            raise ValueError("update_index must be positive")
        if isinstance(self.formation_seed, bool) or not isinstance(
            self.formation_seed, (int, np.integer)
        ):
            raise ValueError("formation_seed must be an integer")
        for name in (
            "created_utc",
            "git_revision",
            "generator",
            "continuation_noise_policy",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        expected_length = min(self.update_index, memory_horizon(self.config))
        if self.state.n_memory != expected_length:
            raise ValueError(
                "checkpoint does not contain the complete retained memory horizon"
            )
        expected_weights = exponential_memory_weights(
            self.config.alpha,
            expected_length,
            memory_mass=self.config.memory_mass,
        )
        if not np.allclose(
            self.state.weights,
            expected_weights,
            rtol=1e-13,
            atol=1e-15,
        ):
            raise ValueError("checkpoint weights do not match the formation config")
        if not np.allclose(
            self.state.x,
            self.state.memory[0],
            rtol=1e-13,
            atol=1e-15,
        ):
            raise ValueError("visible state must equal the youngest deposited point")


def finite_memory_checkpoint_manifest(
    checkpoint: FiniteMemoryCheckpoint,
) -> dict[str, object]:
    """Return canonical human-readable checkpoint metadata and array digests."""

    return {
        "schema": CHECKPOINT_SCHEMA,
        "schema_version": CHECKPOINT_SCHEMA_VERSION,
        "model": "scalar_finite_memory",
        "memory_order": "youngest_first",
        "update_index": int(checkpoint.update_index),
        "formation_seed": int(checkpoint.formation_seed),
        "created_utc": checkpoint.created_utc,
        "git_revision": checkpoint.git_revision,
        "generator": checkpoint.generator,
        "continuation_noise_policy": checkpoint.continuation_noise_policy,
        "config": asdict(checkpoint.config),
        "arrays": {
            "x": _array_manifest(checkpoint.state.x),
            "memory": _array_manifest(checkpoint.state.memory),
            "weights": _array_manifest(checkpoint.state.weights),
        },
    }


def save_finite_memory_checkpoint(
    checkpoint: FiniteMemoryCheckpoint,
    path: Path,
) -> Path:
    """Atomically write a compressed checkpoint without pickle payloads."""

    destination = path.expanduser().resolve()
    if destination.suffix.lower() != ".npz":
        raise ValueError("checkpoint path must use the .npz suffix")
    destination.parent.mkdir(parents=True, exist_ok=True)
    manifest = json.dumps(
        finite_memory_checkpoint_manifest(checkpoint),
        sort_keys=True,
        separators=(",", ":"),
    )
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    try:
        with temporary.open("wb") as handle:
            np.savez_compressed(
                handle,
                x=checkpoint.state.x,
                memory=checkpoint.state.memory,
                weights=checkpoint.state.weights,
                manifest=np.asarray(manifest),
            )
        temporary.replace(destination)
    finally:
        if temporary.exists():
            temporary.unlink()
    return destination


def load_finite_memory_checkpoint(path: Path) -> FiniteMemoryCheckpoint:
    """Load and fully validate a finite-memory checkpoint."""

    source = path.expanduser().resolve()
    with np.load(source, allow_pickle=False) as data:
        required = {"x", "memory", "weights", "manifest"}
        if set(data.files) != required:
            raise ValueError("checkpoint members do not match the schema")
        x = np.asarray(data["x"], dtype=float)
        memory = np.asarray(data["memory"], dtype=float)
        weights = np.asarray(data["weights"], dtype=float)
        manifest_array = data["manifest"]
        if manifest_array.shape != ():
            raise ValueError("checkpoint manifest must be a scalar JSON string")
        manifest_text = manifest_array.item()

    if not isinstance(manifest_text, str):
        raise ValueError("checkpoint manifest must be text")
    try:
        manifest = json.loads(manifest_text)
    except json.JSONDecodeError as exc:
        raise ValueError("checkpoint manifest is invalid JSON") from exc
    if manifest.get("schema") != CHECKPOINT_SCHEMA:
        raise ValueError("unsupported checkpoint schema")
    if manifest.get("schema_version") != CHECKPOINT_SCHEMA_VERSION:
        raise ValueError("unsupported checkpoint schema version")

    state = FiniteMemoryState(x=x, memory=memory, weights=weights)
    try:
        config = SimulationConfig(**manifest["config"])
        checkpoint = FiniteMemoryCheckpoint(
            state=state,
            config=config,
            update_index=manifest["update_index"],
            formation_seed=manifest["formation_seed"],
            created_utc=manifest["created_utc"],
            git_revision=manifest["git_revision"],
            generator=manifest["generator"],
            continuation_noise_policy=manifest["continuation_noise_policy"],
        )
    except (KeyError, TypeError) as exc:
        raise ValueError("checkpoint manifest fields are incomplete") from exc

    expected_manifest = finite_memory_checkpoint_manifest(checkpoint)
    if manifest != expected_manifest:
        raise ValueError("checkpoint metadata or array checksum mismatch")
    return checkpoint
