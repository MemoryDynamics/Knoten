# Second referee review: S1-phase and mass-falsification program

Date: 2026-08-16.

Reviewed artifact:
[S1-phase and mass-falsification program](../../decisions/s1_phase_mass_falsification_program_2026-08-16.md).

## Verdict

The revised charter is suitable as a scientific program charter and as the
boundary for candidate-independent method development. It is not yet an
executable preregistration. Candidate runs remain blocked because P0 lacks the
complete parameter tuple, discovery provenance, initial-state hashes,
candidate observable, target metric and confirmatory seed rule.

This distinction is substantive. Starting A--F against an incompletely frozen
candidate would convert confirmatory gates into post-selection diagnostics.
The authorized start is therefore limited to dependency-pinned generic code
and synthetic controls that contain no candidate-shaped observable, delay,
metric, threshold or decision rule.

## Findings and resolutions

| severity | finding | resolution in the revised charter |
|---|---|---|
| critical | A period-p orbit of the native discrete map is a finite set, not a space homeomorphic to S1. Linear interpolation can manufacture a visual loop. | The claimed topological object must now be named. A discrete S1 claim requires an invariant circle with degree-one dynamics; a finite cycle is classified separately. |
| high | A raw point-cloud time permutation was incorrectly proposed as a topology-negative control even though it leaves all pairwise distances unchanged. | It is now an invariance test. Shuffling becomes a negative control only before a registered delay embedding or in temporal D3/D4 tests. |
| high | Candidate-derived whitening, delay selection or best-looking projection could leak the target label into D2. | Metric, component weights, whitening, delay family and projection are part of D0 and must be fixed from units, model structure or controls before target labels are opened. |
| high | Segments, cadence variants and densely oversampled points could be counted as independent evidence. | Formation seed is the replication unit; segment and cadence variants are repeated measures. Seedwise block resampling handles serial dependence. |
| high | A two-knot momentum test that ignored damping and memory/bath impulse could falsely diagnose nonreciprocity. | C now balances knot plus declared mediator/field momentum against registered bath impulse and includes a common-noise cross-off arm. |
| high | Varying tau, mobility or stored memory mass can destroy the knot or oscillator and induce survivorship bias in a mass regression. | B now separates state-matched weak response from independently re-formed states. Loss of formation or phase is a regime change, not censoring. |
| medium | Recomputing a circular coordinate separately on every holdout was compatible with the earlier wording but is not out-of-sample prediction. | D3 now requires one fitted extension rule applied unchanged to withheld times, seeds, cadences and the sealed parameter cell. |
| medium | C was shown as depending on D4 even though translational composition and momentum are meaningful without a phase. | B, not D4, is the prerequisite for C. D4 enters only an optional phase-exchange subarm. |
| medium | Intrinsic dimension of a noisy tube is scale-dependent; an unqualified one-dimensionality test is ill posed. | D2 now names a preregistered mesoscale between sampling noise and loop diameter and requires boundary diagnostics as a separate condition. |
| medium | F was represented as a terminal mechanical gate, which obscured topology symmetries that do not need a force port. | F is split conceptually into cross-cutting F0 coordinate/topology checks and F1 mechanical/open-system checks. |

No unresolved contradiction was found among the revised dependency graph,
stop rules and publication claim ladder.

## Executed method-only start

The generic
[synthetic topology control record](../../../topology/s1_control_pipeline_2026-08-16.md)
implements full-cloud Vietoris--Rips H0/H1 persistence with a pinned software
dependency and no candidate cutoff. Its method-training split contains:

- a noisy circle and a deterministic stable Hopf limit cycle;
- a flat torus with two long H1 generators;
- a filled disk and a noisy interval with boundary;
- a damped transient spiral;
- a noisy finite 12-cycle as a semantic counterexample.

The full-cloud point-order permutation changes the H1 lifetimes by zero in the
recorded run. The noisy circle has top H1 lifetime 1.5841, while the finite
12-cycle has 1.2068. The latter is intentionally a failure of interpretation:
strong one-hole persistence does not identify an invariant circle or an
autonomous phase. The torus has two comparable leading lifetimes, 0.9851 and
0.9732, so a longest-bar-only classifier is also rejected.

These observations are evidence that the adapter and semantic controls expose
two known failure modes. They are not evidence for an S1 in the knot model and
must not be used as a candidate decision threshold. The distinct
method-validation seed remains unrun. Unit tests verify translation/scale
normalization, prime-field validation, raw-cloud permutation invariance,
finite JSON output and the intended one- versus two-generator control cases.

Software verification after CLI integration:

- focused topology plus experiment-catalog tests: 17 passed;
- complete repository suite with an isolated test temp directory: 641 passed;
- Ruff lint and format checks on changed Python files: passed;
- strict MkDocs build: passed.

## Residual blockers and falsification order

Before any candidate D1/D2 run:

1. complete and commit P0, including all discovery material and the exact
   candidate architecture;
2. choose the primary object: continuous-time orbit, discrete invariant
   circle, stochastic ridge, delay reconstruction or collective orbit;
3. freeze D0, including the physically defensible component metric and all
   symmetry actions;
4. add training-only temporal null families: matched OU/real-pole AR,
   stationary complex focus, phase-randomized surrogate, metastable switching
   and all architecture-specific drive/mechanism-off arms;
5. freeze estimator family, multiplicity treatment and threshold-selection
   rule on method-training controls;
6. run the untouched method-validation split exactly once; only a validation
   pass authorizes candidate topology analysis.

The first candidate result can therefore be a failure without ambiguity. D1
failure means measurement-inconclusive; D2 failure ends the S1/phase language;
D2/D3 pass with D4 failure supports at most recurrent or driven circular
output geometry. None of those outcomes bears on physical mass unless the
independent A--C and E/F1 program also passes.
