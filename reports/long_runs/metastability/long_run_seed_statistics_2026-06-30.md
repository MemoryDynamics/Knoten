# Long-Run Seed Statistics

Date: 2026-06-30.

## Scope

This report summarizes the current long-run metastability statistics before
expanding the matched controls. The scientific rule for the current phase is:
vary only the random seed inside a fixed condition.

## Baseline Seeds

All baseline runs use:

- `steps = 10,000,000`
- `dim = 3`
- `alpha = 0.01`
- `eta = 0.15`
- `amplitude_rep = 1.0`
- `amplitude_att = 0.35`
- `sample_every = 1000`
- `burn_in = 1,000,000`
- `max_memory = 800`

| Seed | Best residence in `alpha^{-1}` | `D_cov` | `D_occ` | Candidate |
| ---: | ---: | ---: | ---: | --- |
| `1` | `256.0` | `1.699` | `1.792` | true |
| `2` | `406.7` | `2.061` | `1.859` | true |
| `3` | `207.5` | `2.519` | `1.849` | true |
| `4` | `318.0` | `1.422` | `1.815` | true |
| `5` | `1000.0` | `1.516` | `1.791` | true |

Baseline summary:

| Metric | Mean | SD | Min | Max |
| --- | ---: | ---: | ---: | ---: |
| best residence in `alpha^{-1}` | `437.6` | `323.1` | `207.5` | `1000.0` |
| `D_cov` | `1.843` | `0.450` | `1.422` | `2.519` |
| `D_occ` | `1.821` | `0.032` | `1.791` | `1.859` |

## Fixed-Seed Controls Already Available

For seed `1`, the matched controls are:

| Condition | Changed parameter | Best residence in `alpha^{-1}` | `D_cov` | `D_occ` |
| --- | --- | ---: | ---: | ---: |
| `baseline` | none | `256.0` | `1.699` | `1.792` |
| `eta_zero` | `eta = 0` | `80.0` | `1.699` | `1.727` |
| `single_scale` | `amplitude_att = 0` | `780.0` | `1.699` | `1.794` |

## Interpretation

The baseline ensemble shows long-lived residence for all five seeds, but the
residence strength varies strongly across seeds. A single fixed-seed control is
therefore not sufficient for a robust statement.

The seed-1 controls are useful as a first sanity check:

- `eta_zero` is lower than baseline seed 1.
- `single_scale` is higher than baseline seed 1 and lies within the broad
  baseline seed-to-seed range.

This means the current evidence does not yet isolate the attractive-repulsive
two-scale mechanism as the unique cause of long residence. The next scientific
step is to run the same five-seed ensemble for `eta_zero` and `single_scale`.

## Decision

Proceed with matched control ensembles:

1. `single_scale`, seeds `2,3,4,5`.
2. `eta_zero`, seeds `2,3,4,5`.
3. Combine each with the existing seed `1` control.
4. Compare condition means and seed variance before building any Paper-I
   evidence table.
