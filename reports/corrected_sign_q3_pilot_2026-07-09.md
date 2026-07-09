# Corrected-Sign q=3 Pilot

Date: 2026-07-09.

## Scope

This pilot reruns the q=3 kernel controls after correcting the Gaussian
potential-gradient sign. It is a short mechanism check, not a long-run knot
claim.

Source data:
`data/processed/long_run_metastability/corrected_sign_q3_100k_seed1-5_2026-07-09`.

Score report:
`reports/knot_score_v0_5_corrected_sign_q3_100k_2026-07-09.md`.

Parameters: `N=100,000`, seeds `1..5`, `d=3`, `alpha=0.01`, `M0=1`,
`sigma_rep=1`, `sigma_att=3`, `A_rep=1`, `A_att=0.35`, `sample_every=100`,
`burn_in=10,000`, `max_memory=600`, conditions `baseline`, `single_scale`,
`rep_zero`, `eta_zero`, with force-component diagnostics.

## Median Summary

| condition | score med | sample radius med | memory radius med | rep step med | att step med | rep/att med | net cos med | rep cos med | att cos med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `0.071` | `58.731` | `5.724` | `0.03387` | `0.00612` | `5.538` | `-0.921` | `-0.938` | `0.984` |
| `single_scale` | `0.000` | `84.460` | `6.534` | `0.03136` | `0` | `n/a` | `-0.954` | `-0.954` | `n/a` |
| `rep_zero` | `0.357` | `3.327` | `0.445` | `0` | `0.00149` | `0` | `0.991` | `n/a` | `0.991` |
| `eta_zero` | `n/a` | `5.167` | `0.622` | `0` | `0` | `n/a` | `n/a` | `n/a` | `n/a` |

Cosines are measured against the direction from the current point toward the
weighted memory center. Positive values move toward the memory center; negative
values move away.

## Reading

The sign correction is mechanically confirmed:

- `A_rep` now produces outward drift from the memory center.
- `A_att` now produces inward drift toward the memory center.
- At the historical q=3 baseline amplitude `A_att=0.35`, the repulsive channel
  dominates the attractive channel by a median factor of about `5.54`.
- The corrected `baseline` and `single_scale` cases disperse in this short
  pilot; the historical compact baseline was therefore legacy-sign evidence.
- `rep_zero` is the attraction-only control and is the only compact active
  condition in this pilot, but its score is still modest and not a full knot
  claim.

## Decision

Do not proceed to Block-Markov/AR mode tests on the historical q=3 baseline.
First run an attraction-amplitude hierarchy at fixed repulsive core, targeting
the transition from repulsion-dominated dispersion to attraction-dominated
confinement/collapse.
