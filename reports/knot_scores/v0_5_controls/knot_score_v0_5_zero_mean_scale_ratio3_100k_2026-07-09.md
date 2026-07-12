# Knot Score v0.5 Report

Date: 2026-07-09T05:27:22Z.

## Scope

This report applies a scorecard-style knot criterion to matched long-run
JSON files. It does not rerun simulations and it does not claim a final
scalar knot definition.

The v0.5 score is the control-safe variant for mixed-alpha comparisons.
It keeps the seven v0.4 components but changes two conventions:

- residence gain is compared in raw update counts, not in `alpha^{-1}` units;
- memory-cloud compactness only scores when the case has nondegenerate
  memory roundness and memory dimension diagnostics.

This prevents the `alpha=1` one-point memory limit from looking
artificially long-lived or compact merely because its memory time is one
update and its active memory cloud is degenerate.

## Seed Scorecard

| condition | seed | score | residence gain | sample compactness | voxel stability | D_occ | memory compactness | memory roundness gain | memory dimension gain | components R/C/V/D/MC/MR/MD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `baseline` | `1` | `0.857` | `11.137` | `14.043` | `0.069` | `1.806` | `8.072` | `3.992` | `1.509` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `baseline` | `2` | `0.786` | `0.425` | `14.275` | `0.639` | `1.943` | `4.971` | `1.563` | `1.341` | `0.0/1.0/1.0/1.0/1.0/1.0/0.5` |
| `baseline` | `3` | `0.857` | `0.595` | `14.429` | `0.735` | `1.761` | `7.662` | `3.370` | `1.854` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `4` | `0.643` | `0.224` | `14.517` | `0.775` | `1.805` | `6.234` | `1.423` | `1.146` | `0.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `baseline` | `5` | `0.857` | `0.157` | `13.611` | `0.882` | `1.775` | `6.564` | `2.106` | `1.565` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `matched_deposition_renormalized` | `1` | `0.857` | `11.137` | `14.159` | `0.067` | `1.808` | `8.124` | `3.996` | `1.510` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `matched_deposition_renormalized` | `2` | `0.786` | `0.426` | `14.381` | `0.632` | `1.940` | `4.988` | `1.563` | `1.341` | `0.0/1.0/1.0/1.0/1.0/1.0/0.5` |
| `matched_deposition_renormalized` | `3` | `0.857` | `0.583` | `14.545` | `0.727` | `1.764` | `7.700` | `3.376` | `1.856` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `matched_deposition_renormalized` | `4` | `0.643` | `0.224` | `14.633` | `0.779` | `1.811` | `6.262` | `1.425` | `1.146` | `0.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `matched_deposition_renormalized` | `5` | `0.857` | `0.157` | `13.721` | `0.883` | `1.780` | `6.588` | `2.108` | `1.565` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `zero_mean_two_scale` | `1` | `0.857` | `11.137` | `14.507` | `0.065` | `1.929` | `8.264` | `3.991` | `1.509` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `zero_mean_two_scale` | `2` | `0.786` | `0.439` | `14.753` | `0.671` | `1.943` | `5.051` | `1.559` | `1.339` | `0.0/1.0/1.0/1.0/1.0/1.0/0.5` |
| `zero_mean_two_scale` | `3` | `0.857` | `0.545` | `14.918` | `0.711` | `1.767` | `7.814` | `3.377` | `1.857` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `zero_mean_two_scale` | `4` | `0.643` | `0.224` | `15.011` | `0.724` | `1.811` | `6.344` | `1.433` | `1.148` | `0.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `zero_mean_two_scale` | `5` | `0.857` | `0.157` | `14.045` | `0.920` | `1.773` | `6.684` | `2.110` | `1.566` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.800` | `0.857` | `0.425` | `14.275` | `0.735` | `1.805` | `6.564` | `2.106` | `1.509` |
| `matched_deposition_renormalized` | `5` | `0.800` | `0.857` | `0.426` | `14.381` | `0.727` | `1.808` | `6.588` | `2.108` | `1.510` |
| `zero_mean_two_scale` | `5` | `0.800` | `0.857` | `0.439` | `14.753` | `0.711` | `1.811` | `6.684` | `2.110` | `1.509` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `2.178` | `0.467` | `0.362` | `2.856` | `0.767` | `0.097` |
| `eta_zero` | `2.051` | `0.419` | `5.167` | `1.903` | `0.380` | `0.622` |
| `matched_deposition_renormalized` | `2.180` | `0.468` | `0.359` | `2.857` | `0.767` | `0.097` |
| `zero_mean_two_scale` | `2.182` | `0.469` | `0.350` | `2.862` | `0.772` | `0.095` |

## Reading

- High score means the condition separates from the no-feedback
  `eta_zero` control for that seed under the selected score version.
- The score is an evidence scorecard, not a proof of a specific
  two-scale knot mechanism.
- Baseline minus `single_scale` score difference has median `n/a`;
  therefore this score still does not isolate the baseline two-scale
  kernel as necessary.
- Memory-cloud shape is explicit in v0.5, and residence is compared in raw updates.
  The raw sample path remains a reported diagnostic rather than the knot-shape criterion.
