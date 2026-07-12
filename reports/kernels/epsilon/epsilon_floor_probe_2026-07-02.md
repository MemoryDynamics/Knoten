# Epsilon Step-Balance Report

Date: 2026-07-02T02:41:39Z.

## Scope

This targeted run compares stochastic and memory-induced update scales
while varying only `epsilon`. It is a scale diagnostic, not a new
parameter sweep for Paper-I evidence.

For each sampled update the script records:

- `noise_norm = ||epsilon xi_n||`;
- `repulsive_step_norm = ||eta grad_rep||`;
- `attractive_step_norm = ||eta grad_att||`;
- `net_drift_norm = ||-eta(grad_rep-grad_att)||`;
- `total_step_norm = ||x_{n+1}-x_n||`;
- `turn_cosine` between consecutive update vectors.

## Configuration

- condition: `baseline`
- seed: `1`
- steps: `500000`
- burn-in: `50000`
- sample every: `10` updates
- alpha: `0.01`
- eta: `0.15`
- sigma_rep / sigma_att: `1.0` / `3.0`
- amplitude_rep / amplitude_att: `1.0` / `0.35`

## Results

| epsilon | median noise | median repulsive step | median net drift | median total step | median noise/repulsive | median noise/drift | mean turn cosine | zero-step fraction | mean radius |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0` | `0` | `0` | `0` | `0` | `n/a` | `n/a` | `n/a` | `1.000` | `0` |
| `1e-05` | `1.541e-05` | `4.293e-06` | `4.126e-06` | `1.594e-05` | `3.592` | `3.738` | `-0.071` | `0` | `2.351e-04` |
| `1e-10` | `1.541e-10` | `4.293e-11` | `4.126e-11` | `1.594e-10` | `3.592` | `3.738` | `-0.071` | `0` | `2.351e-09` |
| `1e-20` | `1.541e-20` | `4.293e-21` | `4.126e-21` | `1.594e-20` | `3.592` | `3.738` | `-0.071` | `0` | `2.351e-19` |
| `1e-34` | `1.541e-34` | `4.293e-35` | `4.126e-35` | `1.594e-34` | `3.592` | `3.738` | `-0.071` | `0` | `2.351e-33` |

## Observed Result

For positive `epsilon` values in this slice, lowering `epsilon`
scales down the whole local motion rather than changing the balance
between stochastic and memory-induced updates. The median
`noise_to_repulsive` ratio remains near
`3.59`, and median `noise_to_net_drift`
remains near `3.74` across the tested
positive epsilon values.

The exact `epsilon=0` case is different: with the zero initial
state used here it remains at the deterministic fixed point, so no
memory gradient is seeded.

The mean `turn_cosine` for positive epsilon values also remains
essentially unchanged
(`-0.071` on average). This indicates that
smaller positive `epsilon` alone makes a smaller trajectory, not a
smoother or more drift-dominated one.

In the current Euler update, the repulsive potential does not define
a hard minimum step length. It defines a deterministic force contribution
that competes with the independent stochastic displacement `epsilon xi_n`.

## Reading

- `epsilon=0` is a fixed-point control for the zero-start baseline:
  without stochastic novelty, no displacement and no memory gradient
  are generated.
- Positive `epsilon` values remain scale-equivalent in this slice:
  noise, drift, radius, and total step shrink together.
- Lower positive `epsilon` values are interesting only if they reduce
  noise/drift ratios without merely shrinking the trajectory.
- `turn_cosine` close to zero means jagged random-walk-like directions;
  larger positive values indicate smoother directional persistence.
