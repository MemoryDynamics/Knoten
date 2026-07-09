# Kernel Scale-Ratio and Rep-Zero Controls

Date: 2026-07-09.

## Scope

This report consolidates the short 100k seed-matched controls after adding the
`zero_mean_two_scale`, `matched_deposition_renormalized`, and `rep_zero`
conditions. The purpose is not to establish a long-run knot theorem. It is a
method check: do current diagnostics isolate a specific two-scale or zero-mean
kernel mechanism, or only feedback confinement relative to no-feedback controls?

All pilots used `d=3`, `alpha=0.01`, `M0=1`, seeds `1..5`, `N=100,000`,
`sample_every=100`, `burn_in=10,000`, `sigma_rep=1`, `amplitude_rep=1`, and
baseline `amplitude_att=0.35` unless the condition overrides it.

## Scale-ratio pilots

Score reports:

- `reports/knot_score_v0_5_zero_mean_matched_100k_2026-07-09.md` for
  `sigma_att/sigma_rep=1.5`.
- `reports/knot_score_v0_5_zero_mean_scale_ratio2_100k_2026-07-09.md` for
  `sigma_att/sigma_rep=2`.
- `reports/knot_score_v0_5_zero_mean_scale_ratio3_100k_2026-07-09.md` for
  `sigma_att/sigma_rep=3`.

| ratio `q=sigma_att/sigma_rep` | condition | zero-mean `A_att` | score median | sample radius median | memory radius median | memory roundness median | `D_occ` median |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `1.5` | `baseline` | n/a | `0.857` | `0.408` | `0.103` | `0.766` | `1.902` |
| `1.5` | `matched_deposition_renormalized` | n/a | `0.857` | `0.404` | `0.103` | `0.765` | `1.823` |
| `1.5` | `zero_mean_two_scale` | `0.296296` | `0.857` | `0.397` | `0.102` | `0.764` | `1.816` |
| `2.0` | `baseline` | n/a | `0.857` | `0.380` | `0.100` | `0.760` | `1.797` |
| `2.0` | `matched_deposition_renormalized` | n/a | `0.857` | `0.377` | `0.099` | `0.760` | `1.811` |
| `2.0` | `zero_mean_two_scale` | `0.125000` | `0.857` | `0.359` | `0.097` | `0.768` | `1.810` |
| `3.0` | `baseline` | n/a | `0.857` | `0.362` | `0.097` | `0.767` | `1.805` |
| `3.0` | `matched_deposition_renormalized` | n/a | `0.857` | `0.359` | `0.097` | `0.767` | `1.808` |
| `3.0` | `zero_mean_two_scale` | `0.037037` | `0.857` | `0.350` | `0.095` | `0.772` | `1.811` |

The active conditions remain nearly indistinguishable in the v0.5 scorecard
across the tested scale ratios. Increasing the scale separation makes
`zero_mean_two_scale` slightly more compact, but it does not produce a distinct
mechanism-level signature in these short pilots.

Reading: the current evidence supports feedback confinement relative to
`eta_zero`. It does not yet support the stronger claim that the baseline needs a
specific two-scale or zero-integral kernel.

## Rep-zero control at `q=3`

Score report: `reports/knot_score_v0_5_rep_zero_q3_100k_2026-07-09.md`.

| condition | score median | sample radius median | memory radius median | memory roundness median | `D_occ` median |
| --- | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `0.857` | `0.362` | `0.097` | `0.767` | `1.805` |
| `single_scale` (`A_att=0`) | `0.857` | `0.349` | `0.095` | `0.772` | `1.812` |
| `rep_zero` (`A_rep=0`) | `0.214` | `10.742` | `1.156` | `0.230` | `1.351` |
| `eta_zero` | n/a | `5.167` | `0.622` | `0.380` | n/a |

This is a strong diagnostic result. `single_scale` behaves like baseline;
`rep_zero` disperses and has a much lower score. Therefore, in the current
simulation convention, `A_rep` is the locally restoring channel and `A_att`
partly counters it. The names `rep` and `att` are historical labels and should
not be used as literal force-direction claims without specifying the update
sign convention.

## Sign-convention audit

In the package kernel code, `gaussian_gradient` returns a vector pointing away
from the memory cloud. The canonical update is

```text
x[n+1] = x[n] + epsilon*noise - eta*grad
```

so a positive one-scale `grad` contribution confines the trajectory toward the
memory cloud. Equivalently, the current implementation is consistent as an
update rule, but the parameter labels can be misleading:

- `amplitude_rep` currently denotes the short-scale positive gradient channel;
  under `-eta*grad` it acts as a restoring/confining channel.
- `amplitude_att` currently denotes the broad positive gradient channel that is
  subtracted inside `double_gaussian_gradient`; under `-eta*grad` it can reduce
  or reverse the local restoration.
- `single_scale` is therefore not a no-knot control. It is the short-scale
  confinement channel alone.
- `rep_zero` is the sharper dispersion control for this code path.

## Decision

Do not scale zero-mean ratio pilots to 1M/100M yet. The short pilots do not show
a mechanism-level separation. First harden the force diagnostics and language:

1. Document Paper-I claims as feedback confinement, not as a necessary two-scale
   or zero-mean mechanism.
2. Add force-component observables: median `||eta grad_rep||`,
   `||eta grad_att||`, net drift, and projection onto the memory-center vector.
3. Use `single_scale` as a positive ablation and `rep_zero`, `eta_zero`,
   `m0_zero`, `alpha_one` as controls with clearly stated semantics.
4. Only after the sign/force-component diagnostics are stable, run
   Block-Markov/AR mode tests on the surviving compact regimes.
