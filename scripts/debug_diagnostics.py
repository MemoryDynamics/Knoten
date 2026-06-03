#!/usr/bin/env python3
from __future__ import annotations

import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (
    SimulationConfig,
    covariance_dimension,
    occupancy_dimension,
    simulate_finite_memory,
    simulate_finite_memory_numba,
    spectral_dimension,
)


def run_debug(use_numba: bool = False):
    cfg = SimulationConfig(
        steps=20000,
        dim=7,
        epsilon=0.03,
        eta=0.15,
        alpha=0.002,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=0.35,
        memory_factor=6.0,
        max_memory=3000,
        burn_in=0,
        sample_every=10,
    )
    print("Config:", cfg)
    simulate = simulate_finite_memory_numba if use_numba else simulate_finite_memory
    t0 = time.perf_counter()
    res = simulate(cfg, seed=42)
    t1 = time.perf_counter()
    samples = res["samples"]
    steps = res["sample_steps"]
    print(f"Simulation done: {samples.shape[0]} samples, elapsed={t1-t0:.3f}s")
    if samples.shape[0] == 0:
        print("No samples produced; check sample_every/steps/burn_in")
        return
    print("Samples min/max per-dim:", samples.min(axis=0), samples.max(axis=0))
    try:
        d_cov = covariance_dimension(samples)
    except Exception as e:
        d_cov = f"ERROR: {e}"
    try:
        occ_res = occupancy_dimension(samples, return_details=True)
    except Exception as e:
        occ_res = f"ERROR: {e}"
    try:
        d_spec = spectral_dimension(samples)
    except Exception as e:
        d_spec = f"ERROR: {e}"
    print("D_cov:", d_cov)
    print("D_occ result:", occ_res)
    print("D_spec:", d_spec)


if __name__ == "__main__":
    print("Debug run sequential (numba=False)")
    run_debug(use_numba=False)
    print("\nDebug run with numba (if available)")
    try:
        run_debug(use_numba=True)
    except Exception as e:
        print("Numba run failed:", e)
