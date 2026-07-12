# N30M Hybrid Trace Launch: eps=1e-4

Date: 2026-07-12.

## Decision

The N=1M confirmation slice keeps the corrected-sign scalar candidates inside the same v0.5 score plateau for `epsilon in {1.65e-6, 1e-4, 0.015}`. Because the smallest value lies directly on the lower plateau edge and can be read as nearly deterministic scaling, the overnight long run uses the smaller-but-not-edge value:

- `epsilon = 1e-4`
- `A_att in {20, 35}`
- `A_rep = 1`, corrected-sign convention
- `seeds = 1..5`
- `conditions = baseline, eta_zero`
- `N = 30,000,000`
- `burn_in = 0`
- hybrid trace: `trace_points=100`, `trace_spacing=log`, `trace_every=1`, `trace_window_memory_times=100`

## Confirmation Slice

Reports:

- `reports/long_runs/epsilon/epsilon_confirm_q3_Aatt20_N1M_2026-07-12.md`
- `reports/long_runs/epsilon/epsilon_confirm_q3_Aatt35_N1M_2026-07-12.md`

Key reading: all three tested epsilons give median score `0.857`; active runs remain compact and separate from `eta_zero` in radius, normalized drift, memory dimension, and roundness. Raw spin dephasing remains an upper bound at the first resolved lag and is not used as a positive spin claim.

## Local Raw Output

The N30M jobs were launched via per-run Python supervisors under ignored `data/processed/` paths:

- `data/processed/long_run_metastability/dynamic_center_trace_q3_Aatt_20_N30M_seed1-5_eps1em4_hybrid_2026-07-12`
- `data/processed/long_run_metastability/dynamic_center_trace_q3_Aatt_35_N30M_seed1-5_eps1em4_hybrid_2026-07-12`

Each folder contains `run.stdout.log`, `run.stderr.log`, `run.supervisor.pid`, `run.child.pid`, and eventually `run.exitcode` when finished.

First observed stdout line for both jobs:

```text
running condition=baseline seed=1 steps=30000000 alpha=0.01 memory_mass=1 deposition=delta dim=3
```

## Next Action After Completion

Aggregate with `dynamic_center_trace_report.py` using the source glob:

```text
data/processed/long_run_metastability/dynamic_center_trace_q3_Aatt_*_N30M_seed1-5_eps1em4_hybrid_2026-07-12
```

Recommended output targets:

```text
reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N30M_eps1em4_2026-07-12.md
reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N30M_eps1em4_summary_2026-07-12.json
figures/draft/dynamic_center_spin_N30M_eps1em4/
```
