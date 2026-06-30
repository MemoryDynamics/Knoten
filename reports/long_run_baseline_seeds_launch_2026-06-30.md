# Long-Run Baseline Seed Ensemble Launch

Date: 2026-06-30.

## Purpose

This report records the seed-variation phase of the long-run metastability
campaign. The rule for this phase is: vary only the random seed. All model
parameters remain identical to the completed baseline run for seed 1.

## Git Revision

- Commit at launch: `30619cb`
- Branch: `main`
- Working tree at launch: clean

## Process

- PID at launch: `35172`
- Started: 2026-06-30, Europe/Berlin
- Initial status: process started in the background

## Command

```powershell
python experiments/long_run_metastability.py `
  --steps 10000000 `
  --seeds 2,3,4,5 `
  --conditions baseline `
  --dim 3 `
  --alpha 0.01 `
  --sample-every 1000 `
  --burn-in 1000000 `
  --max-memory 800 `
  --output-dir data/processed/long_run_metastability/2026-06-30_baseline_seeds
```

Runtime dependencies were provided through `C:\tmp\knoten-longrun-deps`.

## Scope

Together with the completed baseline seed 1 run, this will give five baseline
long-run samples:

- baseline seed 1: completed in `2026-06-29_initial`;
- baseline seeds 2, 3, 4, 5: launched here.

The matched controls `single_scale` and `eta_zero` have already been run for
seed 1. Their interpretation is intentionally deferred until the seed ensemble
is reviewed, because the control comparison must be read against baseline
seed-to-seed variation.

## Expected Output

Generated files are intentionally kept under the ignored output tree:

- `data/processed/long_run_metastability/2026-06-30_baseline_seeds/case_baseline_seed2_steps10000000.json`
- `data/processed/long_run_metastability/2026-06-30_baseline_seeds/case_baseline_seed3_steps10000000.json`
- `data/processed/long_run_metastability/2026-06-30_baseline_seeds/case_baseline_seed4_steps10000000.json`
- `data/processed/long_run_metastability/2026-06-30_baseline_seeds/case_baseline_seed5_steps10000000.json`
- `data/processed/long_run_metastability/2026-06-30_baseline_seeds/summary.json`

After completion, combine these outputs with seed 1 and only then compare the
fixed-seed controls.
