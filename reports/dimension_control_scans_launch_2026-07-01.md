# Dimension Control Scans Launch - 2026-07-01

This launch report records the long-running dimension-control scans started after
decoupling memory decay (`alpha`, interpreted as `lambda_m`) from deposited
memory weight (`beta`).

## Code State

- repository: <https://github.com/MemoryDynamics/Knoten>
- launch commit: [`66d04172bfd94336bb0003664a25aa27345b3537`](https://github.com/MemoryDynamics/Knoten/commit/66d04172bfd94336bb0003664a25aa27345b3537)
- key change: `experiments/fractal_analysis/reproduce_dimension_pilot.py` now supports `--beta`, `--beta-list`, and `--beta-over-alpha-list`
- legacy convention preserved: omitted `beta` gives `beta=alpha`
- validation before launch:
  - `py_compile`: passed
  - `pytest tests -q`: `23 passed`
  - Numba smoke run with `beta/alpha=0.5,1`: passed

## Runtime

- Python runtime: bundled Codex Python 3.12
- dependency target: `C:\tmp\d-alpha-numba-deps`
- `numpy`: 2.4.6
- `numba`: 0.65.1
- engine argument: `--engine auto`
- observed at launch: all six processes were running as `python`, responding, and accumulating CPU time
- stderr logs at launch check: all zero bytes

Runtime logs are intentionally local under ignored `tmp/` paths. Finished JSON
and Markdown reports are written to versioned repository paths under
`data/processed/fractal_analysis/` and `reports/`.

## Started Scans

| scan | PID | purpose | main settings | output |
| --- | ---: | --- | --- | --- |
| `highN_d5_alpha001_beta1_N100M_seed1` | 30664 | Compare with earlier high-N sweeps at a much longer horizon. | `d=5`, `alpha=0.01`, `beta/alpha=1`, `N=100000000`, `seed=1`, `sample_every=1000` | `data/processed/fractal_analysis/highN_d5_alpha001_beta1_N100M_seed1.json` |
| `memory_time_scan_d357_alpha005-02_beta1_N300k-1M_seed1-5` | 31248 | Test memory-time dependence while holding `eta*alpha` fixed. | `d=3,5,7`, `alpha=0.005,0.01,0.02`, `beta/alpha=1`, `N=300000,1000000`, `seeds=1..5`, `eta*alpha=0.02`, `sample_every=100` | `data/processed/fractal_analysis/memory_time_scan_d357_alpha005-02_beta1_N300k-1M_seed1-5.json` |
| `memory_mass_scan_d357_alpha001_betaratio05-2_N300k-1M_seed1-5` | 5148 | Test deposited memory mass at fixed memory decay. | `d=3,5,7`, `alpha=0.01`, `beta/alpha=0.5,1,2`, `N=300000,1000000`, `seeds=1..5`, `sample_every=100` | `data/processed/fractal_analysis/memory_mass_scan_d357_alpha001_betaratio05-2_N300k-1M_seed1-5.json` |
| `kernel_scale_scan_d357_alpha001_beta1_sigmaatt010_N300k-1M_seed1-5` | 24584 | Test shorter attractive scale. | `d=3,5,7`, `alpha=0.01`, `beta/alpha=1`, `sigma_att=0.10`, `N=300000,1000000`, `seeds=1..5`, `sample_every=100` | `data/processed/fractal_analysis/kernel_scale_scan_d357_alpha001_beta1_sigmaatt010_N300k-1M_seed1-5.json` |
| `kernel_scale_scan_d357_alpha001_beta1_sigmaatt015_N300k-1M_seed1-5` | 15200 | Re-run default attractive scale under the new beta-aware schema. | `d=3,5,7`, `alpha=0.01`, `beta/alpha=1`, `sigma_att=0.15`, `N=300000,1000000`, `seeds=1..5`, `sample_every=100` | `data/processed/fractal_analysis/kernel_scale_scan_d357_alpha001_beta1_sigmaatt015_N300k-1M_seed1-5.json` |
| `kernel_scale_scan_d357_alpha001_beta1_sigmaatt0225_N300k-1M_seed1-5` | 34680 | Test broader attractive scale. | `d=3,5,7`, `alpha=0.01`, `beta/alpha=1`, `sigma_att=0.225`, `N=300000,1000000`, `seeds=1..5`, `sample_every=100` | `data/processed/fractal_analysis/kernel_scale_scan_d357_alpha001_beta1_sigmaatt0225_N300k-1M_seed1-5.json` |

## Interpretation Guardrails

- These runs vary one scientific axis per scan family, not all parameters at once.
- The `memory_time` scan keeps `eta*alpha` fixed to reduce trivial coupling-strength drift.
- The `memory_mass` scan changes `beta/alpha`, so it probes stored memory mass separately from memory lifetime.
- The kernel-scale scans vary `sigma_att` while holding `alpha` and `beta/alpha` fixed.
- `N=100000000` is a reference stress run, not a full replicated result.
- These scans are still baseline-only; negative controls and lag/voxel sensitivity remain separate follow-up steps.

