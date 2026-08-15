# P3.8f canonical write-port review

Date: 2026-08-15.

## Verdict

The implementation is suitable for the registered G0/G1 decision after one
material readout correction. G0 passes in all five formation seeds. G1 is
inconclusive in all five seeds; G2 and G3 remain blocked. The result does not
identify or reject a second state.

## Findings resolved

1. **Critical: laboratory translation contaminated the first G1 draft.** The
   absolute branch position retains a small global translation-neutral mode.
   It produced nearly seed-identical holdout ratios just above `1e-3` and
   would have caused a false `5/5` G1 pass. Revision `f32733d` replaces it by
   the co-moving response

   \[
   \delta(x-m_\rho)
   \]

   together with the independent self-force response. A regression test adds
   an arbitrary common translation to `x` and `m_rho` and verifies that the
   G1 envelope is unchanged. The contaminated draft was never committed as
   evidence.

2. **High: the P3.8e profile Gramian was assigned to the wrong side of the
   port.** Direct finite-`k` memory deformations in P3.8e are not independent
   canonical P3.8f inputs. P3.8f has one known trajectory pulse per ambient
   axis; memory centre and `kR` modes are outputs. The preregistration was
   corrected before simulation.

3. **Medium: simulation and analysis provenance were conflated.** Shards now
   retain simulation revision `31e11e7`, while the aggregate separately
   records the readout-analysis revision. Bundle, checkpoint, shard-manifest
   and NPZ hashes are validated before aggregation.

4. **Medium: missing signals and degenerate shapes could crash or silently
   corrupt aggregation.** Empty channels now produce explicit failed fold
   rows, and a collapsed no-kick radius fails G0 before relative shape ratios
   are interpreted.

## Evidence review

The paired pulse is weak and perturbative: maximum normalized strength
nonlinearity is below `9.43e-4`, mirrored even leakage below `5.20e-2`, and
maximum relative radius change below `1.77e-4`. The zero-net, `eta=0`,
extinction and defined-control-shape checks pass in every seed.

Memory outputs remain above the registered signal requirement in all three
holdouts for every seed. The co-moving position/self-force response falls
below `1e-3` of its peak by about `0.12 tau_mem`; its holdout RMS is only about
`8e-8` of its early reference. Thus G1 is not a near-threshold failure.

At `6 tau_mem`, the plots show a small deterministic discontinuity when the
two perturbed deposits leave the explicitly truncated 600-point memory
buffer. The preregistered `(6,8] tau_mem` interval is extinction-only, so this
finite-horizon artifact does not enter G1 or a model fit.

## Remaining limits

* The adjacent return kick writes a memory perturbation but does not sustain
  an independently visible relative response into the registered holdouts.
* No AR order, Hankel rank, pole, damping, frequency, momentum or phase is
  estimable under the split-gate dependency rule.
* A single follow-up may repair excitation without tuning microscopic
  parameters: return the zero-net kick after exactly one intrinsic memory
  time and retain the adjacent pulse as the negative control. Its protocol
  must be fixed before execution.
* If that follow-up also leaves G1 inconclusive, the canonical scalar route to
  an emergent `(m,p)` closure should be closed rather than rescued by shorter
  post-hoc windows, stronger gains or a second knot.

## Verification

The canonical response, bundle curation, shard hashing, out-of-order
aggregation, translation invariance and gate dependency behavior are covered
by tests. The full repository suite passed before the result run; scoped Ruff
and strict MkDocs checks pass after the documentation update.
