# Long-Run Baseline Review

Date: 2026-06-30.

## Source

- Script: `experiments/current/dynamics/long_run_metastability.py`
- Local output: `data/processed/long_run_metastability/2026-06-29_initial`
- Git revision recorded by run: `c36816e`
- Condition: `baseline`
- Seed: `1`

## Parameters

| Parameter | Value |
| --- | ---: |
| updates | `10,000,000` |
| dimension | `3` |
| alpha | `0.01` |
| epsilon | `0.03` |
| eta | `0.15` |
| amplitude_rep | `1.0` |
| amplitude_att | `0.35` |
| sigma_rep | `1.0` |
| sigma_att | `3.0` |
| burn_in | `1,000,000` |
| sample_every | `1000` |
| max_memory | `800` |

## Result

| Metric | Value |
| --- | ---: |
| samples | `9001` |
| elapsed_seconds | `337.997` |
| steps_per_second | `29,586` |
| memory_horizon | `600` |
| stored_weight_mass | `0.997595` |
| covariance_dimension | `1.699` |
| occupancy_dimension | `1.792` |
| best max residence in memory times | `256` |

Residence by voxel size:

| Voxel | visited_voxels | knot_count | max_residence_updates | max_residence_memory_times |
| ---: | ---: | ---: | ---: | ---: |
| `0.5` | `674` | `529` | `14,000` | `140` |
| `1.0` | `180` | `168` | `20,400` | `204` |
| `2.0` | `56` | `54` | `25,600` | `256` |

## Interpretation

This is a strong baseline signal for long-lived residence in this parameter
set, but it is not yet a robust Paper-I result. The next required checks are
the matched controls `eta_zero` and `single_scale`, followed by additional
seeds or voxel/sampling sensitivity if the controls separate cleanly.

## Decision

- Keep Paper 0 independent of this result; Paper 0 remains a structural anchor.
- Do not promote this single baseline run into a knot-existence claim.
- Start the matched controls before building a Paper-I evidence table.
