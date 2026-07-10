# Corrected Scalar N-Scaling Pilot

Date: 2026-07-10.

## Scope

This report measures how the corrected scalar candidates settle as the
run length `N` increases. It uses `burn_in=0` deliberately, because the
formation transient is part of the question.

Fixed parameters: `d=3`, seeds `1..5`, `alpha=lambda_m=0.01`, `M0=1`,
`epsilon=0.03`, `eta=0.15`, `A_rep=1`, `sigma_rep=1`, `sigma_att=3`,
`memory_factor=6`, `max_memory=600`, `sample_every=200`, deposition
`delta`.

Axis: `A_att in {20,35}` and `N in {100k,300k,1M,3M}`.

Each point is scored seedwise against a matched `eta_zero` control.

## Median Summary

| A_att | N | score med | residence gain med | best residence med | sample radius med | memory radius med | raw D_occ med | D_win med | memory dim med | score pass | residence pass |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `20` | `100,000` | `0.857` | `1.429` | `2285.714` | `0.317` | `0.087` | `1.110` | `1.675` | `2.787` | `5/5` | `0/5` |
| `20` | `300,000` | `0.857` | `1.560` | `4054.839` | `0.736` | `0.092` | `1.568` | `1.803` | `2.919` | `5/5` | `2/5` |
| `20` | `1,000,000` | `0.857` | `1.237` | `3067.797` | `0.964` | `0.085` | `1.877` | `1.897` | `2.712` | `5/5` | `0/5` |
| `20` | `3,000,000` | `0.857` | `1.584` | `4286.667` | `1.419` | `0.092` | `2.002` | `2.016` | `2.723` | `5/5` | `1/5` |
| `35` | `100,000` | `0.857` | `0.911` | `1639.130` | `0.146` | `0.060` | `1.042` | `1.650` | `2.936` | `5/5` | `1/5` |
| `35` | `300,000` | `0.857` | `1.423` | `3700.000` | `0.327` | `0.060` | `1.552` | `1.865` | `2.953` | `5/5` | `0/5` |
| `35` | `1,000,000` | `0.857` | `1.091` | `2837.168` | `0.426` | `0.060` | `1.887` | `1.953` | `2.868` | `5/5` | `1/5` |
| `35` | `3,000,000` | `0.857` | `1.684` | `5223.467` | `0.626` | `0.060` | `2.078` | `2.084` | `2.885` | `5/5` | `1/5` |

## Reading

The compact-memory-cloud signal is already present at `N=100k` and
stays stable through `N=3M`. The memory radius is nearly stationary
over this N-range. The sample radius grows slowly with `N`, but remains
small compared with the matched `eta_zero` controls, which is why the
compactness component stays saturated.

The residence signal is not monotone and is still below the v0.5
partial threshold in the median seed. At `N=3M`, median residence gain
is `1.584` for `A_att=20` and `1.684` for `A_att=35`; both remain below
the partial threshold `2`. Residence pass counts therefore remain too
low for a final Paper-I metastability claim.

Interpretation: the corrected scalar candidates appear to form compact
memory clouds quickly. The unresolved question is not formation speed
but whether residence statistics converge slowly, fluctuate by seed,
or require a sharper residence observable than the current voxel
maximum.

## Figures

- `figures/draft/scalar_n_scaling_q3_score_residence_2026-07-10.png`
- `figures/draft/scalar_n_scaling_q3_compactness_2026-07-10.png`
- `figures/draft/scalar_n_scaling_q3_dimensions_2026-07-10.png`

## Raw Rows

- Seed score rows: `40`.
- Machine-readable aggregate: `reports/scalar_n_scaling_q3_summary_2026-07-10.json`.
