# 3e8 Long-Run Launch

Date: 2026-07-10.

## Runtime

The original repository-local `.venv` had been deleted. Recreating `.venv`
inside `C:\Users\Hauke\Documents\Emergenz_Knoten` failed because the local
System Python process could read the repository but could not create or write
files under the protected Documents path. The same interpreter could write to
`C:\tmp`.

Operational runtime for this launch:

- Python: `C:\tmp\knoten-runtime-py312-20260710\Scripts\python.exe`
- Base Python: Python 3.12.7
- NumPy: 2.3.5
- Numba: 0.63.1

The runtime was created under `C:\tmp` and installed from `requirements.txt`.

## Smoke Check

A Numba smoke run completed before launch:

- steps: `100000`
- conditions: `baseline,eta_zero`
- `A_att=35`
- output: `C:\tmp\knoten-longrun-smoke-center-residence-20260710`

Key smoke summary:

| condition | steps/s | best voxel residence memory-times | memory-center primary max run memory-times | memory-center inside fraction | memory shape dimension |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline | 20039.625 | 41.000 | 40.000 | 0.492 | 2.934 |
| eta_zero | 2979817.695 | 13.333 | 12.000 | 0.018 | 1.672 |

## Launched Runs

Both runs were launched as hidden background processes at about 18:12 Europe/Berlin.
The visible parent PIDs are the venv launchers; the child PIDs are the actual
Python compute processes.

Shared parameters:

- script: `experiments/current/dynamics/long_run_metastability.py`
- steps: `300000000`
- dim: `3`
- seeds: `1,2,3,4,5`
- conditions: `baseline,eta_zero`
- epsilon: `0.03`
- eta: `0.15`
- alpha: `0.01`
- memory_mass: `1.0`
- sigma_rep: `1.0`
- sigma_att: `3.0`
- amplitude_rep: `1.0`
- memory_factor: `6.0`
- max_memory: `600`
- burn_in: `0`
- sample_every: `200`
- deposition: default `delta`

| A_att | launcher PID | compute PID | output directory |
| ---: | ---: | ---: | --- |
| 20 | 6588 | 25996 | `C:\tmp\knoten-longrun-3e8-Aatt20-20260710` |
| 35 | 23156 | 16808 | `C:\tmp\knoten-longrun-3e8-Aatt35-20260710` |

Initial logs showed both processes entering `baseline seed=1`; stderr was empty.

## Monitoring

Useful local checks:

```powershell
Get-Process -Id 25996,16808 | Select-Object Id,CPU,WorkingSet64,StartTime
Get-Content -Tail 20 C:\tmp\knoten-longrun-3e8-Aatt20-20260710\stdout.log
Get-Content -Tail 20 C:\tmp\knoten-longrun-3e8-Aatt35-20260710\stdout.log
Get-Content -Tail 20 C:\tmp\knoten-longrun-3e8-Aatt20-20260710\stderr.log
Get-Content -Tail 20 C:\tmp\knoten-longrun-3e8-Aatt35-20260710\stderr.log
```

Expected final files per output directory:

- `summary.json`
- `case_baseline_seed*_steps300000000.json`
- `case_eta_zero_seed*_steps300000000.json`

## Follow-Up

After completion, copy or summarize the result into a committed report before
using it in ChatGPT/mobile/external references. The primary Paper-I diagnostic
for this run is the `memory_center_primary_max_run_memory_times` field added in
commit `24c35d9`.
