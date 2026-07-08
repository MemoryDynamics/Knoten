# Long-Run Results: M0=0 and Alpha-One Controls

Date: 2026-07-08.

## Source

Output directory, intentionally ignored by Git:
`data/processed/long_run_metastability/m0_alpha_one_100M_seed1-10_2026-07-08`.

Launch report: `reports/long_run_m0_alpha_one_launch_2026-07-08.md`.

Run parameters:

| field | value |
| --- | --- |
| steps | `100,000,000` |
| seeds | `1..10` |
| dim | `3` |
| base alpha | `0.01` |
| base memory_mass | `1.0` |
| sample_every | `1000` |
| burn_in | `1,000,000` |
| max_memory | `800` |
| conditions | `m0_zero`, `alpha_one` |

The stderr log is empty and `summary.json` was written at the end of the run.

## Aggregate metrics

| condition | stored mass | horizon | median runtime | median steps/s | mean radius | mean `D_cov` | mean `D_occ` | median best residence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `m0_zero` | `0` | `600` | `2043.76 s` | `48,930` | `212.678` | `1.693` | `1.819` | `8000` updates / `80 alpha^{-1}` |
| `alpha_one` | `1` | `6` | `38.21 s` | `2,617,040` | `212.678` | `1.693` | `1.819` | `8000` updates / `8000 alpha^{-1}` |

Seed-matched trajectory metrics are identical between `m0_zero` and
`alpha_one` for all ten seeds: radius, increments, covariance dimension,
occupancy dimension, sample shape, and residence in updates agree seed by seed.

## Interpretation

`m0_zero` is the expected zero-field control: memory weights are zero and the
trajectory is a pure stochastic walk in the sampled coordinates.

`alpha_one` is not a confined one-step-memory knot regime. With `alpha=1`, the
only nonzero memory weight is the most recent deposited point. At the moment the
next force is evaluated, that point is exactly the current position. For a
symmetric Gaussian self-kernel, the self-gradient at the center is zero. The
visible update therefore reduces to the same stochastic walk as `m0_zero` for a
matched seed.

This is useful evidence: long exponential memory, not merely nonzero memory
mass, is necessary for the observed confinement in the active baseline and
single-scale long runs.

## Diagnostics caveats

- `alpha_one` reports `best residence` as `8000 alpha^{-1}` because
  `alpha^{-1}=1`; compare residence in raw updates across conditions.
- `alpha_one` memory-cloud dimension is mostly undefined because the active
  memory cloud degenerates to the current self-point.
- `m0_zero` was much slower than `alpha_one` in this run because the old
  long-run loop still evaluated the memory interaction even with zero weights.
  The code now skips the force loop when `memory_mass=0`.

## Consequence

Treat both `m0_zero` and `alpha_one` as negative controls for Paper I. The next
analysis step is not another blind scan, but a matched score/coarse-graining
comparison across `baseline`, `single_scale`, `eta_zero`, `m0_zero`, and
`alpha_one`, followed by the Block-Markov/AR mode test for real versus complex
slow modes.