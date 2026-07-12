# Long-Run Controls Launch

Date: 2026-06-30.

## Purpose

This report records the matched control run required after the first baseline
long-run signal. The goal is to test whether the residence signal separates
from simple controls before any Paper-I evidence table is built.

## Git Revision

- Commit at launch: `8f45894`
- Branch: `main`
- Working tree at launch: clean

## Process

- PID at launch: `33532`
- Started: 2026-06-30 13:24 Europe/Berlin
- Initial status check: process running, `stderr` empty
- First logged case: `single_scale`

## Command

```powershell
python experiments/current/dynamics/long_run_metastability.py `
  --steps 10000000 `
  --seeds 1 `
  --conditions single_scale,eta_zero `
  --dim 3 `
  --alpha 0.01 `
  --sample-every 1000 `
  --burn-in 1000000 `
  --max-memory 800 `
  --output-dir data/processed/long_run_metastability/2026-06-30_controls
```

Runtime dependencies were provided through `C:\tmp\knoten-longrun-deps`.

## Scope

The controls use the same baseline parameters as the completed baseline run:

- `single_scale`: disables the attractive component by setting
  `amplitude_att = 0`.
- `eta_zero`: disables memory-induced drift by setting `eta = 0`.

The case order intentionally starts with `single_scale`, because it has the
same full-gradient runtime profile as baseline and gives enough time to commit
this launch report before the first case finishes.

## Expected Output

Generated files are intentionally kept under the ignored output tree:

- `data/processed/long_run_metastability/2026-06-30_controls/case_single_scale_seed1_steps10000000.json`
- `data/processed/long_run_metastability/2026-06-30_controls/case_eta_zero_seed1_steps10000000.json`
- `data/processed/long_run_metastability/2026-06-30_controls/summary.json`
- `data/processed/long_run_metastability/2026-06-30_controls/controls_stdout.log`
- `data/processed/long_run_metastability/2026-06-30_controls/controls_stderr.log`

After completion, compare these controls against the baseline report before
promoting any metastability claim.
