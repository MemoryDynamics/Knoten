# P3.8e review: can `(m,p)` be an emergent effective state?

Date: 2026-08-13.

## Verdict

Not yet. The canonical state `z=(x,rho)` can in principle generate a
non-Markovian projected response whose minimal realization contains a second
predictive state. Existing data do not identify that state or select the
P3.8d gradient mediator against first-order and nonparametric-delay nulls.

The rigorous admissible claim, after a future pass, would be an **emergent
effective closure**, not a new microscopic momentum. State coordinates are
unique only up to similarity; the invariant evidence is the input-output map,
poles, zeros, residues, minimal order and storage relation.

## Findings

| Severity | Finding | Consequence |
|---|---|---|
| high | A longer autonomous P3.8d run cannot select dynamic order. Its Lyapunov balance makes first- and second-order arms approach the same stationary equations. | Use long canonical histories to test response stationarity with formation age. Do not extend the constructed pilot as a mechanism test. |
| high | Projection cannot create a causal cross-channel absent from the canonical transition kernel. | Single-knot data can select only an internal effective mode. A cross-mediator needs a registered common-field/multi-source microscopic law or remains an explicit extension. |
| high | The previous uniform weak probe excites `k=0`, while the P3.8d gradient response has an exact `k^2` zero. | Replace it for identification by paired localized or zero-mean finite-`k` probes; retain the uniform probe only as a pipeline control. |
| high | P3.8d is a field with two temporal states per spatial mode, not one global two-state system. | Compare first versus second order per registered mode. For `r` resolved modes the generic order comparison is at least `r` versus `2r`. |
| medium | The spatial polynomial has three unknown coefficients `a,b,c`. Three `k` values merely interpolate it. | Require at least three training channels and one untouched dispersion holdout; add another if the decay-rate product is not independently fixed. |
| medium | A rank-two fit or two real poles can be rewritten in companion form without physical inertia. | Call `p` only a second predictive state until passivity, reciprocal power-conjugate ports and a storage-metric-robust reversible part are established. |
| medium | A similar knot and kernel potential is expected in the current point limit `R_mem/ell=2.12e-4`. | Treat curve similarity as a coarse-graining hypothesis, not mechanism evidence. Probe `k R_mem=O(1)` or at least two resolved knot sizes. |
| medium | Stochastic projected paths retain an orthogonal fluctuating-force term; it is not generically a martingale difference. | Compare conditional-mean response plus residual statistics; do not claim an exact finite deterministic AR law for individual paths. |

## Registered next gate

1. Fix `Y=Psi(x,rho)`, finite-`k` inputs and a separate readout without using
   a target frequency.
2. Measure paired `+/-` impulse responses with common random numbers on mature
   checkpoints and multiple formation-age windows.
3. On common holdouts compare first order, unconstrained second order,
   passive-reciprocal second order and a nonparametric delay kernel per mode.
4. Reconcile continuous poles and residues across seeds, cadences, horizons,
   resolutions and knot age.
5. Use power-conjugate ports for the storage/passivity test and withhold
   displacement, force, phase and one finite-`k` channel for prediction.
6. Only a pass authorizes mapping the second state to `p` and testing the
   P3.8c/d pair response without retuning.

Primary null: canonical responses do not require a stable reversible
second-order modal realization. Failure keeps P3.8d as a constructed model
extension.

## Review checks

- Mori-Zwanzig block elimination was qualified as a local conditional-mean
  identity with an orthogonal stochastic term; martingale structure requires
  an additional conditional-expectation construction.
- Minimal-realization coordinate gauge and parameter non-identifiability were
  stated explicitly.
- Passivity was restricted to power-conjugate ports.
- Global rank-two and uniform-probe shortcuts were rejected.
- No particle, spin, quantization, dimension-selection or physical-mass claim
  was introduced.

## Method anchors

- Mori, *Transport, Collective Motion, and Brownian Motion*:
  <https://doi.org/10.1143/PTP.33.423>.
- Lin et al., *Data-driven learning for the Mori-Zwanzig formalism*:
  <https://arxiv.org/abs/2101.05873>.
- Juang and Pappa, *An Eigensystem Realization Algorithm*:
  <https://ntrs.nasa.gov/citations/19850064186>.
- Lewkowicz, continuous/discrete positive-real state-space systems:
  <https://arxiv.org/abs/2008.04635>.

## Verification

- `582` repository tests passed using a workspace-local pytest base directory;
- Ruff passed on `src`, `experiments/current` and `tests`;
- MkDocs strict and `git diff --check` passed;
- a repository-wide Ruff invocation additionally reported 20 pre-existing
  findings confined to archived/legacy and historical dimension scripts.
