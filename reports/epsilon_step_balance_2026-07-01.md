# Epsilon Step-Balance Report

Date: 2026-07-01T20:20:44Z.

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

| epsilon | median noise | median repulsive step | median net drift | median total step | median noise/repulsive | median noise/drift | mean turn cosine | mean radius |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.03` | `0.04624` | `0.01281` | `0.01231` | `0.04779` | `3.615` | `3.763` | `-0.070` | `0.717` |
| `0.015` | `0.02312` | `0.00643` | `0.00618` | `0.02391` | `3.598` | `3.744` | `-0.071` | `0.354` |
| `0.01` | `0.01541` | `0.00429` | `0.00412` | `0.01594` | `3.594` | `3.740` | `-0.071` | `0.235` |
| `0.005` | `0.00771` | `0.00215` | `0.00206` | `0.00797` | `3.593` | `3.738` | `-0.071` | `0.118` |

## Observed Result

In this slice, lowering `epsilon` scales down the whole local motion
rather than changing the balance between stochastic and memory-induced
updates. The median `noise_to_repulsive` ratio remains near
`3.60`, and median `noise_to_net_drift`
remains near `3.75` across the tested
epsilon values.

The mean `turn_cosine` also remains essentially unchanged
(`-0.071` on average). This indicates that
smaller `epsilon` alone makes a smaller trajectory, not a smoother
or more drift-dominated one.

In the current Euler update, the repulsive potential does not define
a hard minimum step length. It defines a deterministic force contribution
that competes with the independent stochastic displacement `epsilon xi_n`.

## Reading

- `epsilon=0.03` is fluctuation-dominated if its median noise step is
  larger than the median net memory drift and comparable to or larger
  than the repulsive contribution.
- Lower `epsilon` values are interesting only if they reduce noise/drift
  ratios without merely freezing the trajectory.
- `turn_cosine` close to zero means jagged random-walk-like directions;
  larger positive values indicate smoother directional persistence.
