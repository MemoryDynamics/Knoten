# Long-Run Metastability Launch

Date: 2026-06-29.

## Purpose

This report records the first real background run for Paper-I metastability
evidence. It follows the updated priority decision: Paper 0 is frozen as a
technical anchor or possible supplement, while robust knot evidence for Paper I
must come from long runs and controls.

## Git Revision

- Commit: `a9ea908`
- Branch: `main`
- Remote: `https://github.com/MemoryDynamics/Knoten`

## Process

- PID at launch: `35600`
- Started: 2026-06-29 22:09 Europe/Berlin
- Initial status check: process running, `stderr` empty

## Command

```powershell
python experiments/long_run_metastability.py `
  --steps 10000000 `
  --seeds 1 `
  --conditions baseline `
  --dim 3 `
  --alpha 0.01 `
  --sample-every 1000 `
  --burn-in 1000000 `
  --max-memory 800 `
  --output-dir data/processed/long_run_metastability/2026-06-29_initial
```

Runtime dependencies were provided through `C:\tmp\knoten-longrun-deps`.

## Scope

This is the first baseline run only:

- one seed;
- `n = 10^7`;
- normalized memory convention `lambda_m = beta = alpha`;
- Residence diagnostics in update units and in units of `alpha^{-1}`;
- no claim of robust knot existence until controls and additional seeds are
  available.

## Expected Output

Generated files are intentionally kept under the ignored output tree:

- `data/processed/long_run_metastability/2026-06-29_initial/case_baseline_seed1_steps10000000.json`
- `data/processed/long_run_metastability/2026-06-29_initial/summary.json`
- `data/processed/long_run_metastability/2026-06-29_initial/long_run_stdout.log`
- `data/processed/long_run_metastability/2026-06-29_initial/long_run_stderr.log`

After completion, the JSON outputs should be reviewed before any result report
is committed.

## Next Checks

1. Confirm completion and inspect `summary.json`.
2. Read residence ratios across voxel sizes.
3. Decide whether to run `eta_zero` first or repeat baseline with additional
   seeds.
4. Only after controls: construct the Paper-I evidence table.
