# P3.8e identification reconciliation review

Date: 2026-08-13. Reviewed revision: `e4f56b8`. Reviewed scope: canonical
finite-`k` continuation, temporal-identification library, regression tests,
fixed correction protocol, machine-readable output, response archive, report,
and figure.

## Referee verdict

The historical P3.8e temporal-order result is
`superseded-methodologically-inconclusive`. Its paired finite-`k` simulation
was not shown to be wrong, but two result-changing identification defects were
present. The corrected analysis again selects no second-order state (`0/5`
channels), now without complex active poles. Scientifically this is
`null-not-rejected-memory-holdout-limited`, not a scalar-memory no-go theorem.

## Findings

| Severity | Finding | Consequence |
|---|---|---|
| critical | The historical free AR(2) and "damped AR(2)" were the same model on every reported stable conjugate-pole solution. A stable complex real AR(2) already has an exact damped continuous-time representation. | Their identical coefficients and errors were mathematically expected. The old comparison supplied no independent evidence for damping, passivity, or a physical oscillator. |
| critical | The historical block-Hankel matrix created separate column families for seeds and directions. Different panel residue vectors could increase rank even when all panels shared one temporal pole. | The old full-rank/entropy-rank evidence cannot be used. The corrected operator stacks all panel readouts into one output vector and uses only chronological shifts as columns. |
| high | The historical primary signal was `active - eta_zero`. A difference of two first-order responses can itself have order two. Visible and memory readouts also contributed jointly to fitted coefficients. | The old complex roots did not identify the active canonical system. The corrected fit uses active and `eta=0` separately, learns poles only from memory readouts, and withholds the visible coordinate. |
| high | The original AR orders used different first targets and the original holdout started after signal extinction. | The correction uses common target 8 and a 600-update analysis horizon. Even then, memory holdout contains only `0.2%..0.8%` of scale-balanced energy, so the negative result remains holdout-limited. |
| high | The five nominal input profiles are not independent for these localized states: weighted Gram condition number min/median/max is `28.2/15867.1/165244.7`, with maximum off-diagonal `0.9964`. | The five responses cannot support a five-point dispersion fit. Input-basis orthogonalization or a lower effective input rank is required before spatial coefficient identification. |
| medium | Corrected pooled AR(2) poles are real for all five channels. AR(2) visible rollout ratios are `1.069..1.138`, no better than zero and not 20% better than AR(1). The genuinely undamped reference is much worse (`3.814..29.756`). | No corrected channel supplies a predictive oscillatory temporal state. This is independent of the removed damped/free redundancy. |
| medium | Corrected Hankel first-two energy is high (`0.875..0.988`), but `s3/s2=0.557..0.695`; all matrices retain numerical rank 30 at `1e-3`. | The responses look like one dominant relaxation plus a distributed tail, not a clean rank-two realization. |
| medium | The `N=3M` to `N=100M` seed-1 shift lies within the five-seed spread for `5/5` channels, but maximum seed pole spread is already `0.368..0.470`. | The age comparison no longer has a common-noise confound, but its pass only says formation age is not the dominant variation. Pole identity is not established. |
| medium | The intervention is still a complete memory-state deformation rather than a pulse written through the canonical trajectory-deposition map. | It measures state/read susceptibility, not canonical controllability, an adjoint write/read pair, or a power-conjugate port. |
| low | Uniform identity, complete `eta=0` extinction, diagonal and full-mode strength linearity, and shape boundedness all pass. Cross-`k` diagonal fractions are `0.904` active and `0.929` after control subtraction. | No sign, central-difference scaling, obvious nonlinearity, branch-noise, or shape-destruction defect explains the null result. |

## Code verification

- The Numba continuation uses the same effective kernel parameters and sign as
  the public canonical gradient.
- A new one-step regression test compares the complete paired finite-`k`
  response against a direct public-kernel central difference.
- Paired signs, active/control arms, and formation-age pairs use the intended
  common random numbers.
- All recurrence orders use 65 common training targets and 48 common holdout
  targets per pooled channel.
- Changing the withheld visible readout cannot change fitted memory poles; a
  regression test enforces this independence.
- A synthetic common one-pole response remains Hankel rank one even with quiet
  panel channels; this test catches the historical matrix-layout defect.
- The complete cross-wavenumber response, not only its diagonal, is retained
  in the committed NPZ archive.
- `597` repository tests pass. Ruff passes `src`, `tests`, and
  `experiments/current`; repository-wide Ruff still reports pre-existing
  issues in explicitly archived legacy scripts and old standalone paper
  generators.

## Review-findings status

Implemented: independent active/control fits, common target windows,
signal-bearing-window diagnostics, withheld visible readout, corrected Hankel
layout and rank gate, seed-level replication, common-noise age comparison,
input-profile Gram gate, full cross-`k` archival, full-mode extinction, and a
genuinely distinct undamped reference.

Intentionally unresolved: canonical trajectory write port, balanced
controllability/observability, positive storage metric, power-conjugate ports,
cross-node mediation, and microscopic interpretation of a second state.

## Scientific decision

1. Do not tune kernel amplitudes, noise, damping, or P3.8d parameters to force
   complex poles in this data set.
2. Do not cite the historical damped/free equality or historical Hankel ranks
   as evidence.
3. P3.8d remains a constructed, internally consistent comparison model, not a
   reduction derived from canonical `z=(x,rho)`.
4. If the scalar route receives its final P3.8f test, it must write through a
   zero-net canonical trajectory pulse, use a weighted-orthogonalized or
   explicitly rank-reduced input basis, and fix blocked signal-window
   validation before data generation.
5. Failure of that source-port test would justify ending the scalar `(m,p)`
   route. An oriented/current memory or shared multi-source field would then be
   a declared model extension, not a discovered reparameterization.

## Claim boundary

Evidence: controlled finite-`k` state susceptibility, exact controls, corrected
real-pole temporal fits, corrected Hankel spectra, input-profile collinearity,
and broad formation-seed variation.

Inference: the tested projection does not select a shared underdamped
second-order state.

Not established: a universal scalar-memory no-go theorem, emergent momentum,
passivity, spin, quantization, particle identity, physical mass, dimension
selection, or a field shared by multiple knots.
