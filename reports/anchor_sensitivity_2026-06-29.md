# Anchor Markov Sensitivity Analysis

Date: 2026-06-29

Scope: small diagnostic sensitivity run for the Paper-0 Markov layer. This is not a broad robustness claim.

## Parameters

```json
{
  "alpha": [
    0.02,
    0.05
  ],
  "amplitude_att": 0.35,
  "amplitude_rep": 1.0,
  "base_feature_voxel_size": 1.0,
  "base_lag": 3,
  "burn_in": 300,
  "controls": [
    "baseline",
    "eta_zero",
    "shuffled_memory_features"
  ],
  "dim": 3,
  "epsilon": 0.03,
  "eta": 0.15,
  "feature_voxel_size": [
    0.75,
    1.0,
    1.25
  ],
  "lag": [
    1,
    3,
    5
  ],
  "max_memory": 800,
  "memory_factor": 6.0,
  "sample_every": 10,
  "seeds": [
    1,
    2,
    3
  ],
  "sigma_att": 3.0,
  "sigma_rep": 1.0,
  "steps": 3000,
  "voxel_size": 0.75
}
```

## Aggregate Table

| category | control | alpha | sample_lag | feature_voxel_size | n | slow_abs | rate | gap | n_states | empty_rows | residence_mean | ac_lag1 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lag_sensitivity | baseline | 0.02 | 1 | 1 | 3 | 0.9595 | 0.004236 | 0.04048 | 59 | 0 | 2.233 | 0.7728 |
| lag_sensitivity | baseline | 0.02 | 3 | 1 | 3 | 0.9227 | 0.002799 | 0.07726 | 59 | 0 | 2.233 | 0.7728 |
| lag_sensitivity | baseline | 0.02 | 5 | 1 | 3 | 0.907 | 0.002036 | 0.09298 | 59 | 0 | 2.233 | 0.7728 |
| lag_sensitivity | baseline | 0.05 | 1 | 1 | 3 | 0.9597 | 0.00421 | 0.04027 | 48.67 | 0 | 4.697 | 0.932 |
| lag_sensitivity | baseline | 0.05 | 3 | 1 | 3 | 0.9333 | 0.00236 | 0.06668 | 48.67 | 0 | 4.697 | 0.932 |
| lag_sensitivity | baseline | 0.05 | 5 | 1 | 3 | 0.9198 | 0.001713 | 0.08019 | 48.67 | 0 | 4.697 | 0.932 |
| negative_control | baseline | 0.02 | 3 | 1 | 3 | 0.9227 | 0.002799 | 0.07726 | 59 | 0 | 2.233 | 0.7728 |
| negative_control | baseline | 0.05 | 3 | 1 | 3 | 0.9333 | 0.00236 | 0.06668 | 48.67 | 0 | 4.697 | 0.932 |
| negative_control | eta_zero | 0.02 | 3 | 1 | 3 | 0.9683 | 0.001079 | 0.03173 | 85.67 | 1 | 3.667 | 0.9843 |
| negative_control | eta_zero | 0.05 | 3 | 1 | 3 | 0.972 | 0.0009503 | 0.02802 | 100 | 1 | 3.667 | 0.9843 |
| negative_control | shuffled_memory_features | 0.02 | 3 | 1 | 3 | 0.8164 | 0.008046 | 0.1836 | 104 | 0.3333 | 2.233 | 0.7728 |
| negative_control | shuffled_memory_features | 0.05 | 3 | 1 | 3 | 0.9231 | 0.002827 | 0.07687 | 101.7 | 0.6667 | 4.697 | 0.932 |
| voxel_sensitivity | baseline | 0.02 | 3 | 0.75 | 3 | 0.9227 | 0.002799 | 0.07726 | 59 | 0 | 2.233 | 0.7728 |
| voxel_sensitivity | baseline | 0.02 | 3 | 1 | 3 | 0.9227 | 0.002799 | 0.07726 | 59 | 0 | 2.233 | 0.7728 |
| voxel_sensitivity | baseline | 0.02 | 3 | 1.25 | 3 | 0.9227 | 0.002799 | 0.07726 | 59 | 0 | 2.233 | 0.7728 |
| voxel_sensitivity | baseline | 0.05 | 3 | 0.75 | 3 | 0.9405 | 0.002082 | 0.05945 | 59.67 | 0.3333 | 4.697 | 0.932 |
| voxel_sensitivity | baseline | 0.05 | 3 | 1 | 3 | 0.9333 | 0.00236 | 0.06668 | 48.67 | 0 | 4.697 | 0.932 |
| voxel_sensitivity | baseline | 0.05 | 3 | 1.25 | 3 | 0.9333 | 0.00236 | 0.06668 | 48.67 | 0 | 4.697 | 0.932 |

## Reading Notes

- `sample_lag` is a lag in stored samples, not physical time.
- `lag_updates` is recorded per raw case in the JSON output.
- `shuffled_memory_features` keeps visible samples but permutes memory-summary columns; it is a feature-control, not a new dynamics run.
- `eta_zero` is a dynamics control with the memory-gradient coupling removed.
- Voxel results are baseline diagnostics; they are not a final PCCA or HMM decomposition.

## Git

- revision: `6f9be65f2c4e6105377569fcb43c4b918b4c87fb`
- status at run:

```text
M README.md
 M docs/experiment_catalog.md
 M docs/index.md
 M experiments/README.md
 M mkdocs.yml
?? docs/repository_map.md
?? experiments/anchor_sensitivity_analysis.py
?? reports/anchor_sensitivity_2026-06-29.md
```
