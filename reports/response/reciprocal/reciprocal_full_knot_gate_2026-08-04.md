# P3.1 reciprocal full-knot reconciliation gate

Date: 2026-08-04T14:01:18+00:00.

## Question

Does synchronous instantaneous reciprocal scalar readout create a stable,
control-separated complex relative mode in the complete finite-memory knot,
despite the registered local reduction predicting a real mode?

## Meaning of complex

A coordinate-fixed-effects real 2 x 2 relative-state matrix has a complex mode when its
eigenvalues are a non-real conjugate pair. Such a matrix is real-similar
to `a E + b J`, with `J=[[0,-1],[1,0]]`; it need not have that literal
entry pattern in the measured `(x_-, m_-)` coordinates. This rotation is
in relative state space, not evidence for spatial rotation or d=3.

## Fixed design

- complete d=3 checkpoint at N=100,000,000, formation seed 1;
- two copies are rigidly placed and the second is cyclically rotated;
- initial centre distance `2.5 R_pair`;
- lambda=0.01, eta=0.15, epsilon=0.0001;
- registered finite-horizon cross gain c=0.02, giving cross_eta=0.006939767;
- 5 node-specific future-noise seed pairs, each shared across channel-off, one-way, and reciprocal conditions;
- 50,000 updates = 500.0 memory times; the first 100.0 memory times are excluded from four segment fits.

- runtime 137.56 s, or 1817.4 continuation updates/s.

The future-noise seeds are repeated continuations of one formation basin.
They test pathwise robustness but are not independent knot formations.

## Analytic preregistration

The retained-memory self gain is `0.432291`.
At c=0.02, the local relative discriminant is `0.208318` and the multipliers are `[{'real': 0.9991252883200965, 'imag': 0.0}, {'real': 0.5427064606658762, 'imag': 0.0}]`. The local mode is therefore complex=False, stable=True.

A segment counts only if the fitted pair is stable and non-real, its
frequency is at least 0.05 per memory time, phase coherence is at least 0.5, normalized residual at most 0.8, and design condition at most 1e+08. A seed needs 3/4 segments with frequency and damping ranges each at most 0.25. The reciprocal candidate needs 4/5 seeds and at most 1 candidate seed in either control.

## Result

Classification: **registered real-mode null confirmed**.

- exact cross-zero identity: True (max error 0.000e+00);
- candidate seeds off / one-way / reciprocal: 0 / 0 / 0;
- reciprocal response detected: 5/5;
- reciprocal shape bounded/coherent: 5/5;
- nonlinear complex candidate: False.

![P3.1 reciprocal full-knot gate](../../figures/draft/response/reciprocal_full_knot_gate_2026-08-04.png)

## Seed rows

| future seed | off complex seg | one-way complex seg | reciprocal complex seg | reciprocal response/R | reciprocal shape | final separation/R | candidate |
| ---: | ---: | ---: | ---: | ---: | :---: | ---: | :---: |
| 1 | 0 | 0 | 0 | 1.218 | True | 0.8797 | False |
| 2 | 0 | 0 | 0 | 3.138 | True | 0.3158 | False |
| 3 | 0 | 0 | 0 | 1.88 | True | 0.3921 | False |
| 4 | 0 | 0 | 0 | 1.516 | True | 0.3145 | False |
| 5 | 0 | 0 | 0 | 3.544 | True | 0.8414 | False |

## Interpretation boundary

- A null confirms only the registered direct instantaneous scalar arm at
  this fixed gain and mature checkpoint. It is not a no-oscillator theorem
  for nonlinear fields, delayed mediators, or oriented memory.
- A positive result would remain a candidate until reproduced across
  independently formed mature states without retuning.
- Shape-bounded/coherent permits bounded breathing and rigid rotation; it
  does not require pointwise shape preservation.
- No charge, spin, particle, QFT, or dimensional-selection claim follows.

## Reproduction

    python experiments/current/memory/synchronization/reciprocity/reciprocal_full_knot_gate.py

Checkpoint: `data/processed/reference_states/scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/scalar_Aatt35_d3_seed1_N100000000.npz`.
Git revision: `3a68e582fbf800ed9e620249c6da3fb22027ca68`.
Machine-readable summary: [reciprocal_full_knot_gate_2026-08-04.json](reciprocal_full_knot_gate_2026-08-04.json)
Git status at generation: `clean`.
