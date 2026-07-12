# Knot Score v0.5 Report

Date: 2026-07-10T12:02:06Z.

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
| `baseline` | `1` | `0.857` | `1.572` | `18.929` | `0.333` | `1.983` | `7.846` | `4.461` | `1.893` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `2` | `0.857` | `0.823` | `18.875` | `0.373` | `1.943` | `10.177` | `1.878` | `1.483` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `3` | `0.857` | `1.237` | `18.929` | `0.566` | `1.969` | `5.960` | `2.161` | `1.549` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `4` | `0.857` | `1.457` | `18.951` | `0.528` | `1.839` | `5.626` | `1.988` | `1.655` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `5` | `0.857` | `0.839` | `18.914` | `0.489` | `1.908` | `5.165` | `2.804` | `1.841` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.857` | `0.857` | `1.237` | `18.929` | `0.489` | `1.943` | `5.960` | `2.161` | `1.655` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `2.017` | `0.325` | `0.850` | `2.712` | `0.673` | `0.085` |
| `eta_zero` | `2.001` | `0.318` | `16.098` | `1.639` | `0.331` | `0.508` |

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
