# Corrected Scalar Candidate Hardening at 1M

Date: 2026-07-10.

## Scope

This is the first targeted hardening run after the KPI/Pareto decision. It
does not scan a broad parameter grid. It varies only the broad attractive
amplitude inside the corrected-sign scalar candidate window.

Axis: `A_att in {9, 20, 35}`.

Fixed parameters: `N=1,000,000`, seeds `1..5`, `d=3`, `alpha=lambda_m=0.01`,
`M0=1`, `epsilon=0.03`, `eta=0.15`, `sigma_rep=1`, `sigma_att=3`,
`A_rep=1`, `memory_factor=6`, `max_memory=600`, `burn_in=100,000`,
`sample_every=200`, deposition `delta`.

Each amplitude is scored seedwise against a matched `eta_zero` control with
the same nominal parameters. The score version is KnotScore `v0.5`.

## Median Summary

| A_att | score med | candidate seeds | residence gain med | sample compactness med | voxel stability med | D_occ med | memory compactness med | memory roundness gain med | memory dimension gain med | sample radius med | memory radius med | memory dim med |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `9` | `0.500` | `5/5` | `1.450` | `2.512` | `0.345` | `1.752` | `1.701` | `1.739` | `1.331` | `6.409` | `0.329` | `2.107` |
| `20` | `0.857` | `5/5` | `1.237` | `18.929` | `0.489` | `1.943` | `5.960` | `2.161` | `1.655` | `0.850` | `0.085` | `2.712` |
| `35` | `0.857` | `5/5` | `1.040` | `42.768` | `0.468` | `1.945` | `8.674` | `2.347` | `1.730` | `0.376` | `0.060` | `2.868` |

Score means are `0.543`, `0.857`, and `0.871` for `A_att=9`, `20`, and `35`.

## Reading

The corrected scalar model now has a genuine compact-candidate window.
`A_att=20` and `A_att=35` pass all v0.5 components except residence gain in
the median seed. Both amplitudes separate strongly from `eta_zero` in sample
compactness, memory compactness, memory roundness, and memory-shape dimension.

The bottleneck is not shape. The bottleneck is residence gain against the
matched random-walk control:

- `A_att=20`: median residence gain `1.237`, below the partial threshold `2`.
- `A_att=35`: median residence gain `1.040`, but with one high-residence seed
  and max seed-level gain `4.732`.

So the current honest statement is:

```text
The corrected scalar model produces seed-robust compact memory-cloud
confinement at A_att=20..35 in 1M-step pilots. The remaining Paper-I issue is
whether this compact confinement becomes long-residence metastability under
longer N, not whether the corrected model can form compact knots at all.
```

`A_att=9` remains useful as a transition/boundary control. It produces
long-lived candidate flags in all five seeds, but it does not reach the strong
compactness thresholds.

## Decision

Next scalar long-run should not broaden the amplitude scan. Use:

- `A_att=20` as the balanced compact candidate;
- `A_att=35` as the tight/round memory-cloud candidate;
- `A_att=9` only as a boundary control if runtime permits.

The next evidence question is residence scaling with `N`. A practical next
step is a longer run for `A_att=20` and `A_att=35`, same seeds and scorecard,
before adding more parameters.

## Source Reports

- `reports/knot_score_v0_5_scalar_hardening_q3_Aatt_9_1M_2026-07-10.md`
- `reports/knot_score_v0_5_scalar_hardening_q3_Aatt_20_1M_2026-07-10.md`
- `reports/knot_score_v0_5_scalar_hardening_q3_Aatt_35_1M_2026-07-10.md`
