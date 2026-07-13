# Ambient-Dimension Memory-Shape Sweep Launch

Date: 2026-07-13.

## Purpose

This is the direct follow-up to the `D_mem ~= 2.94` boundary note. The goal is to test whether the current local memory-shape finding is tied to the chosen 3D embedding or persists when the same scalar reference candidate is placed in higher ambient dimensions.

This is still a Paper-II bridge test, not a dimension-selection theorem.

## Fixed Slice

- `A_att = 35`
- `A_rep = 1`
- `epsilon = 1e-4`
- `eta = 0.15`
- `alpha = lambda_m = 0.01`
- `M0 = 1`
- deposition kernel: `delta`
- corrected q=3 scalar kernel
- `N = 30,000,000`
- `burn_in = 0`
- seeds `1..5`
- conditions `baseline,eta_zero`
- trace: `trace_points=100`, `trace_spacing=log`, `trace_every=1`, `trace_window_memory_times=100`
- spectral geometry: `spectral_points=1000` for both sampled path and memory cloud `D_spec`

## Ambient Dimensions

Primary overnight dimensions:

```text
d in {4,5,7,10,13,20}
```

The existing `d=3` `A_att=35`, `N=30M`, `epsilon=1e-4` rerun is the reference:

```text
data/processed/long_run_metastability/dynamic_center_trace_q3_Aatt_35_N30M_seed1-5_eps1em4_rerun_2026-07-13
```

## Raw Output Pattern

Each new dimension writes to ignored local data directories:

```text
data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d{dim}_seed1-5_eps1em4_2026-07-13
```

Each directory should contain `case_*.json`, `summary.json`, `run.stdout.log`, `run.stderr.log`, and `run.exitcode`.

## Long-Run Command Template

Run once per ambient dimension, replacing `{dim}` in both places:

```text
python experiments/current/dynamics/long_run_metastability.py \
  --steps 30000000 \
  --dim {dim} \
  --seeds 1,2,3,4,5 \
  --conditions baseline,eta_zero \
  --epsilon 1e-4 \
  --eta 0.15 \
  --alpha 0.01 \
  --memory-mass 1 \
  --deposition-kernel delta \
  --deposition-sigma 0 \
  --sigma-rep 1 \
  --sigma-att 3 \
  --amplitude-rep 1 \
  --amplitude-att 35 \
  --memory-factor 6 \
  --max-memory 800 \
  --burn-in 0 \
  --sample-every 1000 \
  --trace-every 1 \
  --trace-points 100 \
  --trace-spacing log \
  --trace-window-memory-times 100 \
  --spectral-points 1000 \
  --voxel-sizes 0.5,1.0,2.0 \
  --max-ac-lag 50 \
  --min-memory-times 10 \
  --output-dir data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d{dim}_seed1-5_eps1em4_2026-07-13
```

## Post-Run Aggregation

After completion, aggregate with:

```text
python experiments/current/dynamics/ambient_dimension_memory_shape_report.py \
  --source-dir data/processed/long_run_metastability/dynamic_center_trace_q3_Aatt_35_N30M_seed1-5_eps1em4_rerun_2026-07-13 \
  --source-dir data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d4_seed1-5_eps1em4_2026-07-13 \
  --source-dir data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d5_seed1-5_eps1em4_2026-07-13 \
  --source-dir data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d7_seed1-5_eps1em4_2026-07-13 \
  --source-dir data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d10_seed1-5_eps1em4_2026-07-13 \
  --source-dir data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d13_seed1-5_eps1em4_2026-07-13 \
  --source-dir data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d20_seed1-5_eps1em4_2026-07-13 \
  --report reports/dimensions/ambient_memory_shape_N30M_eps1em4_2026-07-14.md \
  --summary-json reports/dimensions/ambient_memory_shape_N30M_eps1em4_summary_2026-07-14.json
```

## Decision Rule

- If active `D_mem` remains near three, active roundness remains high, and radius/drift separation survives across ambient dimensions, then the phrase "chosen 3D embedding" can be weakened to "local 3D memory-shape phenomenon".
- `D_spec` is an unweighted point-cloud reconciliation metric, not the primary acceptance criterion. Agreement between memory `D_spec` and `D_mem` near three strengthens the Paper-II geometry reading; disagreement flags estimator or scale sensitivity that must be reviewed before any stronger claim.
- If `D_mem` increases with ambient dimension or loses control separation, keep the current conservative wording and treat macroscopic 3D as Paper-II open work.
