# Force-Component Pilot at `sigma_att/sigma_rep=3`

Date: 2026-07-09.

## Scope

This pilot adds direct force-component diagnostics to the q=3 kernel controls.
It is a short 100k method check, not a long-run evidence campaign. It tests
whether the observed `single_scale`/`rep_zero` behavior follows from the actual
update sign convention.

Run source:
`data/processed/long_run_metastability/force_components_q3_100k_seed1-5_2026-07-09`.

Provenance: `git_revision=8178346`, `git_status=""`.

Parameters: `d=3`, `alpha=0.01`, `M0=1`, `N=100,000`, seeds `1..5`,
`sigma_rep=1`, `sigma_att=3`, `A_rep=1`, `A_att=0.35`, `sample_every=100`,
`burn_in=10,000`, conditions `baseline`, `single_scale`, `rep_zero`, `eta_zero`.

## Component medians over seeds

All step norms include the factor `eta`. The cosine columns are projections of
the component step onto the vector from the current point toward the weighted
memory center. Positive means toward the memory center; negative means away.

| condition | rep step | att step | net drift | noise | rep/att | noise/net | rep center cos | att center cos | net center cos |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `0.0129327` | `0.000508458` | `0.0124242` | `0.046033` | `25.4429` | `3.7264` | `0.906270` | `-0.905914` | `0.906284` |
| `single_scale` | `0.0127501` | `0` | `0.0127501` | `0.046033` | n/a | `3.64401` | `0.904503` | n/a | `0.904503` |
| `rep_zero` | `0` | `0.00257358` | `0.00257358` | `0.046033` | `0` | `17.8868` | n/a | `-0.996941` | `-0.996941` |
| `eta_zero` | `0` | `0` | `0` | `0.046033` | n/a | n/a | n/a | n/a | n/a |

## Reading

The force-component diagnosis explains the earlier scorecard results.

- `baseline` is dominated by the local `rep` channel: its median step is about
  25 times the broad `att` channel, and it points toward the memory center.
- `single_scale` removes the broad counter-channel and therefore remains as
  compact as, or slightly more compact than, baseline.
- `rep_zero` removes the local restoring channel. The remaining broad channel
  points away from the memory center and the run disperses.
- `eta_zero` is the no-feedback control: only stochastic novelty remains.

This confirms that the current labels `rep` and `att` are historical channel
names. Under the canonical update `x <- x - eta*grad`, `A_rep` is the local
confinement channel and `A_att` is a broad counter-channel in this parameter
slice.

## Decision

This closes the immediate kernel-sign ambiguity. Do not scale additional
zero-mean or two-scale kernel sweeps until a specific mechanism-level observable
is proposed. The next useful scientific step is the Block-Markov/AR mode test on
compact regimes, using the new force-component diagnostics as auxiliary
features or sanity checks.
