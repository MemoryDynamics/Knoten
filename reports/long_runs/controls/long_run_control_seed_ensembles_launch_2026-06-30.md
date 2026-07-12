# Long-Run Control Seed Ensembles Launch

Date: 2026-06-30.

## Purpose

This report records the matched five-seed control phase. The baseline condition
already has seeds `1..5`. The controls now receive the same seed coverage so
that condition effects can be read against seed-to-seed variation.

## Git Revision

- Commit immediately before launch: `2aed135`
- Branch: `main`
- Working tree at launch: clean

## Launched Processes

| Condition | Seeds | PID | Output directory |
| --- | --- | ---: | --- |
| `single_scale` | `2,3,4,5` | `10204` | `data/processed/long_run_metastability/2026-06-30_single_scale_seeds` |
| `eta_zero` | `2,3,4,5` | `31488` | `data/processed/long_run_metastability/2026-06-30_eta_zero_seeds` |

Both use the same base parameters as the baseline ensemble:

- `steps = 10,000,000`
- `dim = 3`
- `alpha = 0.01`
- `sample_every = 1000`
- `burn_in = 1,000,000`
- `max_memory = 800`

## One-Parameter Rule

Each control changes exactly one model component relative to baseline:

- `eta_zero`: sets `eta = 0`.
- `single_scale`: sets `amplitude_att = 0`.

The random seed is varied only inside each fixed condition. The existing seed
`1` controls are retained and will be combined with these new seeds.

## Initial Status

- `eta_zero` completed quickly and wrote `summary.json`.
- `single_scale` was running at the first status check.
- Initial error logs were empty.

## Next Review

After `single_scale` completes, combine:

- baseline seeds `1..5`;
- `eta_zero` seeds `1..5`;
- `single_scale` seeds `1..5`.

Only then compare condition means, spread, and overlap.
