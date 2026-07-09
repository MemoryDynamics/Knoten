# Knot Score v0.5 Report

Date: 2026-07-09T05:15:24Z.

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
| `baseline` | `1` | `0.857` | `13.953` | `12.482` | `0.058` | `1.791` | `7.408` | `3.950` | `1.505` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `baseline` | `2` | `0.786` | `0.467` | `12.672` | `0.444` | `2.020` | `4.690` | `1.583` | `1.349` | `0.0/1.0/1.0/1.0/1.0/1.0/0.5` |
| `baseline` | `3` | `0.857` | `0.692` | `12.790` | `0.621` | `1.925` | `7.126` | `3.344` | `1.843` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `4` | `0.643` | `0.222` | `12.861` | `0.759` | `1.824` | `5.850` | `1.390` | `1.136` | `0.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `baseline` | `5` | `0.857` | `0.172` | `12.145` | `0.792` | `1.902` | `6.140` | `2.095` | `1.563` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `matched_deposition_renormalized` | `1` | `0.857` | `13.953` | `12.607` | `0.057` | `1.791` | `7.466` | `3.959` | `1.506` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `matched_deposition_renormalized` | `2` | `0.786` | `0.460` | `12.784` | `0.453` | `2.028` | `4.709` | `1.582` | `1.348` | `0.0/1.0/1.0/1.0/1.0/1.0/0.5` |
| `matched_deposition_renormalized` | `3` | `0.857` | `0.677` | `12.914` | `0.602` | `1.785` | `7.169` | `3.351` | `1.846` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `matched_deposition_renormalized` | `4` | `0.643` | `0.222` | `12.985` | `0.760` | `1.823` | `5.883` | `1.391` | `1.137` | `0.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `matched_deposition_renormalized` | `5` | `0.857` | `0.169` | `12.265` | `0.808` | `1.911` | `6.167` | `2.096` | `1.563` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `zero_mean_two_scale` | `1` | `0.857` | `12.389` | `12.804` | `0.063` | `1.794` | `7.548` | `3.965` | `1.506` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `zero_mean_two_scale` | `2` | `0.786` | `0.463` | `13.002` | `0.489` | `2.023` | `4.749` | `1.578` | `1.347` | `0.0/1.0/1.0/1.0/1.0/1.0/0.5` |
| `zero_mean_two_scale` | `3` | `0.857` | `0.677` | `13.127` | `0.605` | `1.789` | `7.239` | `3.350` | `1.845` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `zero_mean_two_scale` | `4` | `0.643` | `0.238` | `13.201` | `0.808` | `1.816` | `5.931` | `1.397` | `1.138` | `0.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `zero_mean_two_scale` | `5` | `0.857` | `0.169` | `12.449` | `0.801` | `1.900` | `6.230` | `2.097` | `1.563` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.800` | `0.857` | `0.467` | `12.672` | `0.621` | `1.902` | `6.140` | `2.095` | `1.505` |
| `matched_deposition_renormalized` | `5` | `0.800` | `0.857` | `0.460` | `12.784` | `0.602` | `1.823` | `6.167` | `2.096` | `1.506` |
| `zero_mean_two_scale` | `5` | `0.800` | `0.857` | `0.463` | `13.002` | `0.605` | `1.816` | `6.230` | `2.097` | `1.506` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `2.163` | `0.461` | `0.408` | `2.847` | `0.766` | `0.103` |
| `eta_zero` | `2.051` | `0.419` | `5.167` | `1.903` | `0.380` | `0.622` |
| `matched_deposition_renormalized` | `2.165` | `0.462` | `0.404` | `2.846` | `0.765` | `0.103` |
| `zero_mean_two_scale` | `2.166` | `0.462` | `0.397` | `2.843` | `0.764` | `0.102` |

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
