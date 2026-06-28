# Paper 0 Validation and Review

Date: 2026-06-26

Scope: second-pass validation of Paper 0,
`Self-Interacting Dynamics with Exponential Memory: Markovian Embedding,
Contractive Memory Fibres, and Metastability`.

## Validation Summary

- The mathematical core is coherent: the discrete model, exponential memory
  expansion, pathwise memory-fibre contraction, Markov kernel, observable
  operator, non-Markovian projection, and formal continuum approximation are
  correctly separated.
- Strong physics claims remain outside the main result. Dimension selection,
  finite signal speed, Lorentz invariance, quantum structure, physical masses,
  and Standard-Model claims are explicitly listed as future work, not results.
- The reproducible code path now exposes reduced augmented-state features,
  residence statistics, autocorrelation, and a finite transfer-operator
  estimate.
- The transfer estimate now reports finite-sample terminal rows and treats
  them explicitly, avoiding silent substochastic zero rows.

## Corrections Made In This Review Pass

1. Added state-space and boundary conventions to the baseline assumptions:
   either `Omega = R^d`, or boundary/extension rules must keep `x_{n+1}` in
   `Omega` and preserve the stated kernel mass.
2. Replaced the ambiguous random-cocycle notation with an explicit augmented
   one-step map `F_xi(x,rho)`.
3. Clarified finite-sample terminal-row handling in transfer-matrix estimates.
4. Updated the transfer-operator helper so empty empirical rows are handled
   explicitly and reported by the pipeline.
5. Updated tests for empty-row handling in finite transition matrices.

## Olaf-Style Review

### Main Impression

This is now a useful mathematical anchor. It does not try to sell the whole
world model. It defines one process, proves the immediate structural facts,
and turns "Knoten" into a measurable metastability question. That is the right
level for Paper 0.

### What Works

- The paper now has a clear limited claim:
  visible dynamics is generally non-Markovian, augmented dynamics is Markovian,
  and the memory fibre contracts along a common visible path.
- The mass language is controlled. Relaxation rates are treated as stability or
  mass-like proxies, not as physical masses.
- The dangerous later topics are parked explicitly: 3D, finite propagation,
  Lorentz, quantum, constants, particles.
- The literature placement is credible: self-interacting diffusions,
  reinforced processes, Brownian polymer/self-repelling motion, GLE embeddings,
  random dynamical systems, and transfer operators.

### What Should Still Be Improved Before Wider Circulation

- The introduction is mathematically clear but still a little dry. For an
  external reader, one paragraph explaining why exponential forgetting is the
  new modelling choice would help.
- The kernel classes should become more explicit in a future revision:
  purely attractive, purely repulsive, and two-scale attractive-repulsive.
- The numerical section is only a pipeline sketch. It is good enough for an
  anchor note, but not yet enough for a results paper.
- The open-problem section should eventually include a concrete theorem target:
  compact `Omega`, smooth bounded kernels, nondegenerate noise, Feller kernel,
  existence of invariant measure.

## Referee-Style Review

### Summary

The manuscript introduces a discrete self-interacting stochastic process with
an exponentially relaxing memory field. It proves elementary but important
structural facts: exact memory expansion, contraction of the memory fibre along
a fixed visible path, and Markovianity of the augmented state. It also proposes
metastability diagnostics based on residence times and transfer operators.

### Strengths

- The paper is conservative and avoids overclaiming.
- The mathematical definitions are mostly precise.
- The proof obligations match the actual claims.
- The distinction between structural results, formal continuum approximations,
  numerical diagnostics, and future conjectures is explicit.
- The note correctly avoids saying that the affine memory update is
  noninvertible when the deposited kernel is known.

### Major Concerns

1. Well-posedness is not yet a theorem. The paper states baseline assumptions
   but does not prove existence, uniqueness, Feller continuity, or invariant
   measures.
2. The continuum approximation is formal. This is acknowledged, but a referee
   would ask for either a precise scaling theorem or a clearer statement that
   it is heuristic.
3. The transfer-operator diagnostics are preliminary. Reduced memory features
   are lossy, and the bias introduced by feature choice, lag, discretization,
   and finite-sample terminal rows is not quantified.
4. No numerical phase diagram is provided. The figure is illustrative, not
   evidentiary.

### Minor Concerns

- "Knots" is project terminology and may sound physically loaded. The paper
  mitigates this by defining it operationally, but a more neutral alias such as
  "metastable memory-localized regimes" may help for submission.
- The bibliography is adequate for an anchor note but should be expanded if
  submitted as a standalone mathematical paper.
- The OU local approximation depends on a stable Hessian and slow memory
  variation; this should remain explicitly conditional.

### Referee Verdict

As an internal anchor paper or mathematical companion note: acceptable after
minor revision.

As a standalone journal submission: promising, but requires additional theorem
statements, stronger numerical validation, and a more detailed comparison with
self-interacting diffusion literature.

## Recommended Next Actions

1. Add a compact theorem-proposition structure for a bounded/compact-state
   special case.
2. Create a small kernel-class subsection with three canonical kernel families.
3. Run a small reproducible sweep and add a table, not just an illustrative
   spectrum.
4. Add lag/discretization sensitivity checks for transfer spectra.
5. Decide whether "knots" remains in the title/abstract or is reserved for
   project-internal language.
## Addendum: 2026-06-27 Micro-Review

A third pass found and corrected smaller consistency issues:

- The transfer-operator rate formula now distinguishes the sample lag `ell`
  from the actual lag time `tau_ell` used for relaxation rates.
- Unit-modulus eigenvalues are now described as reported spectral information,
  not automatically as relaxation rates.
- The pipeline reports both `empty_rows_handled` and
  `unit_eigenvalues_reported`, making finite-sample transfer-matrix conventions
  visible in machine-readable output.
- The figure caption now says non-unit modes near the unit circle are candidate
  slow modes, avoiding accidental interpretation of terminal-row artifacts as
  metastability.

## Addendum: 2026-06-28 Final Review

### Incorporation Check

The accumulated review findings have been checked against the current Paper 0
source, README, pipeline, and report artifacts.

Addressed items:

- The scope boundary is explicit: Paper 0 does not claim spacetime, Lorentz
  kinematics, quantum mechanics, Standard-Model structure, physical masses, or
  constants.
- The Markov embedding claim is correctly formulated for the augmented state
  and not for the visible coordinate alone.
- The memory update is no longer described as algebraically noninvertible when
  the deposited kernel and next visible point are known; the text now states
  the weaker and correct loss of ordered full history.
- Relaxation rates are described as stability or mass-like proxies, not as
  calibrated physical masses.
- Dimension selection, finite propagation speed, Lorentz kinematics, and
  quantum/Standard-Model topics are confined to future-work language.
- Transfer-operator diagnostics now distinguish sample lag from physical or
  scaled lag time, make terminal-row handling visible, and avoid converting
  unit-modulus eigenvalues into relaxation rates.
- Concrete repository links now point to Paper II and a planned Paper III
  roadmap, while making clear that these companion tracks are not evidence for
  the claims of Paper 0.

Remaining submission blockers:

- There is still no rigorous well-posedness, Feller, invariant-measure, or
  ergodicity theorem for a named kernel/state-space class.
- The continuum approximation remains formal rather than a proved scaling
  limit.
- The numerical evidence is still a smoke-test and diagnostic scaffold, not a
  systematic parameter sweep with seed statistics and lag/discretization
  sensitivity.
- The novelty claim relative to self-interacting diffusions and reinforced
  processes is plausible but would need a sharper theorem-level comparison for
  a mathematical journal.

### Final Referee Verdict

Do not submit the paper to a journal as a standalone peer-review manuscript in
its present form. It is suitable as an internal mathematical anchor and close
to a technical preprint or discussion draft. For journal review, it should first
be upgraded with either a compact rigorous theorem package for a bounded or
compact setting, or a substantially stronger reproducible numerical section
with systematic sweeps and validation tables.

A realistic next target is: circulate to one or two trusted expert readers, add
one clean theorem block and one small evidence table, then reassess journal fit.

## Addendum: 2026-06-28 Memory Normalization Correction

A late notation review found that the mathematically natural memory update is

```text
rho_{n+1} = (1-lambda_m) rho_n + beta G_sigma(. - x_{n+1}).
```

The previous `alpha` formulation is the normalized special case
`lambda_m=beta=alpha`. Paper 0 has been updated accordingly:

- `lambda_m` controls exponential forgetting and the memory time scale.
- `beta` controls deposited memory strength.
- The expansion is now `beta sum_j (1-lambda_m)^j G_sigma`.
- Pathwise fibre contraction is `(1-lambda_m)^n`.
- Unit mass is preserved only when the kernel and initial memory have unit mass
  and `beta=lambda_m`.
- The formal continuum scaling now assumes `beta/lambda_m -> kappa`, with the
  normalized convention corresponding to `kappa=1`.

This correction improves the paper. It does not remove the journal-submission
blockers listed above: the continuum approximation is still formal, and the
numerical evidence remains preliminary.
