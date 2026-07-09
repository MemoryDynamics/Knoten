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
| `baseline` | `1` | `0.857` | `12.389` | `13.393` | `0.061` | `1.797` | `7.800` | `3.984` | `1.508` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `baseline` | `2` | `0.786` | `0.431` | `13.607` | `0.585` | `1.934` | `4.856` | `1.570` | `1.344` | `0.0/1.0/1.0/1.0/1.0/1.0/0.5` |
| `baseline` | `3` | `0.857` | `0.661` | `13.745` | `0.656` | `1.778` | `7.443` | `3.359` | `1.849` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `4` | `0.643` | `0.245` | `13.826` | `0.751` | `1.812` | `6.077` | `1.410` | `1.142` | `0.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `baseline` | `5` | `0.857` | `0.164` | `13.002` | `0.856` | `1.769` | `6.391` | `2.101` | `1.564` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `matched_deposition_renormalized` | `1` | `0.857` | `12.389` | `13.514` | `0.063` | `1.804` | `7.854` | `3.990` | `1.509` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `matched_deposition_renormalized` | `2` | `0.786` | `0.438` | `13.716` | `0.609` | `1.930` | `4.874` | `1.570` | `1.344` | `0.0/1.0/1.0/1.0/1.0/1.0/0.5` |
| `matched_deposition_renormalized` | `3` | `0.857` | `0.647` | `13.866` | `0.709` | `1.773` | `7.484` | `3.366` | `1.852` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `matched_deposition_renormalized` | `4` | `0.643` | `0.245` | `13.947` | `0.758` | `1.811` | `6.107` | `1.411` | `1.142` | `0.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `matched_deposition_renormalized` | `5` | `0.857` | `0.163` | `13.117` | `0.841` | `1.901` | `6.416` | `2.103` | `1.564` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `zero_mean_two_scale` | `1` | `0.857` | `11.137` | `14.146` | `0.067` | `1.811` | `8.115` | `3.992` | `1.509` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `zero_mean_two_scale` | `2` | `0.786` | `0.426` | `14.381` | `0.631` | `1.943` | `4.989` | `1.562` | `1.340` | `0.0/1.0/1.0/1.0/1.0/1.0/0.5` |
| `zero_mean_two_scale` | `3` | `0.857` | `0.583` | `14.537` | `0.724` | `1.765` | `7.696` | `3.372` | `1.854` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `zero_mean_two_scale` | `4` | `0.643` | `0.224` | `14.626` | `0.774` | `1.810` | `6.259` | `1.425` | `1.146` | `0.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `zero_mean_two_scale` | `5` | `0.857` | `0.156` | `13.708` | `0.883` | `1.776` | `6.590` | `2.107` | `1.565` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.800` | `0.857` | `0.431` | `13.607` | `0.656` | `1.797` | `6.391` | `2.101` | `1.508` |
| `matched_deposition_renormalized` | `5` | `0.800` | `0.857` | `0.438` | `13.716` | `0.709` | `1.811` | `6.416` | `2.103` | `1.509` |
| `zero_mean_two_scale` | `5` | `0.800` | `0.857` | `0.426` | `14.381` | `0.724` | `1.810` | `6.590` | `2.107` | `1.509` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `2.172` | `0.465` | `0.380` | `2.847` | `0.760` | `0.100` |
| `eta_zero` | `2.051` | `0.419` | `5.167` | `1.903` | `0.380` | `0.622` |
| `matched_deposition_renormalized` | `2.174` | `0.466` | `0.377` | `2.848` | `0.760` | `0.099` |
| `zero_mean_two_scale` | `2.179` | `0.468` | `0.359` | `2.857` | `0.768` | `0.097` |

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
