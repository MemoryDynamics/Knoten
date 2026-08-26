# Critical review: P4 reciprocal orbit-center source/write mechanics

Date: 2026-08-26.

Reviewed machine decision: **`p4-source-write-architecture-fail`**.

Review disposition: **retain the registered failure, do not open P5, and do
not promote any mechanics or mass claim.** The result contains two distinct
findings that must not be conflated:

1. the exact write/age/interaction work ledger and generalized-force balance
   are numerically resolved and pass every registered work tolerance;
2. the composite architecture decision nevertheless fails because two
   algebraically redundant direct-displacement diagnostics are normalized
   below the binary64 cancellation floor in all 24 arms. Independently of
   that measurement defect, all 24 arms fail the registered straight-line
   response test through a large chirality-odd transverse displacement.

Thus the formal decision is not renamed or rescued. The direct residuals are
not evidence of physical nonreciprocity, while the transverse response is a
genuine falsifier of the frozen scalar straight-line response hypothesis.

## 1. Immutable record and timing

The protocol was committed before the implementation and before the target
run:

| stage | revision | commit time (Europe/Berlin) |
| --- | --- | --- |
| P4 protocol freeze | `15ccd714ba595c92ae5d0aff936977f78977f632` | `2026-08-26T06:42:14+02:00` |
| clean pushed implementation | `d339ee1924ab2a931c74803ee5a58213b73afbcd` | `2026-08-26T16:01:59+02:00` |
| unedited result record | `c4eff90dfe1fc63c2b605043a5334b3073f5bc4b` | `2026-08-26T16:07:21+02:00` |

The result records an empty pre-run worktree, the execution revision above,
the P3 decision `p3-formation-basin-pass`, and the frozen dependency blobs.
The execution blobs are

```text
runner  3e3aef0e48006f6ffb58948d1c4c30d22b020dd6
module  d8de95f4f46adc43c37d6d1affdc73be14f70ec3
```

The committed result JSON is Git blob
`41ddfb5ec2d4c907607995523775072ad12544f7`; its canonical LF byte stream has
SHA-256

```text
ea0651e206451e5f87ec08ab3f66ec68df2c04bee2d1b9d67219736058a275cc
```

which agrees with the report. The different hash of a Windows CRLF checkout
is an end-of-line representation effect, not a content or provenance failure.
Before target access, the clean pushed revision passed the exact CI lint
scope, strict documentation build and all 784 tests.

## 2. Coordinate construction and complex convention

For chirality (s\in\{+1,-1\}), the implementation evaluates the finite sum

\[
\beta_s=B_H(e^{is\theta_3}),\qquad
C_s=\sum_{j=0}^{H-1}a_{s,j}h_j
\]

directly from the normalized finite-memory weights. Complex multiplication by
(a) represents the real planar matrix (M(a)), so the Euclidean adjoint is
multiplication by (a^*). Consequently the slot force is

\[
f_j=a_{s,j}^*F,
\]

and the implementation's real inner product is
(u\cdot v=\operatorname{Re}(u^*v)). This convention is internally
consistent: the unrelated-history virtual-work error is
(2.08\times10^{-17}), while total generalized-force balance is below
(1.76\times10^{-16}) of the registered force scale in every target arm.

The coefficient sum, notch and chirality-conjugacy controls are at most
(9.16\times10^{-16}). Correct-chirality target centers are below
(9.49\times10^{-16}), whereas the wrong-chirality amplitude remains large.
Reflection maps the two chiralities exactly in the stored response panel.
There is no sign correction or post-result coefficient estimate.

The raw normalized memory center (c_H) was not substituted for (C_s).
Its rotating target amplitude is `0.5058810073761263`, while the notched
coordinate is zero to rounding precision. Treating (F\,dc_H) as work leaves
a per-step rival-ledger residual as large as `14.9784` initial interaction
energies; it cannot close the declared interaction ledger.

## 3. Source/write algebra and exact work ledger

The active transition first evaluates the unchanged nonlinear native L3 map
(\widetilde h=\mathcal T_{\rm L3}(h)), then modifies only the visible write
slot by

\[
h'_0=\widetilde h_0+\alpha a_0^*F.
\]

The external coordinate moves with the matched positive mobility
(\nu=|a_0|^2), and the force is the exact closed solution of the implicit
midpoint discrete-gradient equation. No second difference, velocity,
momentum or mass coefficient appears in either update.

The exact finite-history identity is

\[
F\cdot(C'-C)=W_{\rm write}+W_{\rm age},
\]

not (F\cdot\Delta h_0) or (F\cdot\Delta c_H) by definition. The target
results are:

| registered quantity | observed range or maximum | limit | result |
| --- | ---: | ---: | :---: |
| per-step write/age split / (U_0) | `1.997e-12 .. 9.595e-12` | `5e-11` | pass |
| per-step total interaction ledger / (U_0) | `1.997e-12 .. 9.596e-12` | `5e-11` | pass |
| cumulative write/age split / (U_0) | `3.730e-12` maximum | `5e-9` | pass |
| cumulative total ledger / (U_0) | `3.727e-12` maximum | `5e-9` | pass |
| force balance / initial force | `1.755e-16` maximum | `5e-12` | pass |
| midpoint-force residual / initial force | `2.922e-13` maximum | `5e-12` | pass |
| actuator update / initial coupling displacement | `1.149e-13` maximum | `5e-12` | pass |
| minimum mobility dissipation | nonnegative in every arm | nonnegative | pass |

Dropping the age term leaves as much as `19.99` initial energies in the
non-decisional truncated ledger. This is strong numerical evidence that the
source/sink boundary term was measured rather than silently discarded.

These facts establish an algebraically exact work decomposition for the
**declared artificial source/write port**. They do not establish that this
port is uniquely selected by the native model, that the open memory is
material, or that total material momentum exists.

## 4. Why the registered architecture label fails

All 24 arms fail exactly two entries grouped under `ledger_pass`:
`center_actuation` and `coupling_displacement`. Algebraically,

\[
C'-\widetilde C=\alpha |a_0|^2F
\]

holds identically because only slot zero is changed. With equal mobilities,
the corresponding coupling displacement also vanishes identically. The
runner checks these identities by subtracting two independently evaluated
2400-term dot products whose large rotating contributions cancel.

The observed absolute residuals are

```text
2.358e-16 .. 3.278e-16
```

but the amplitude-normalized registered limits are

```text
1.180e-18 .. 4.721e-18.
```

They are therefore 50--278 times too tight for the observed binary64
subtraction. For scale, the target weighted absolute sum is `1.71335`; a
conservative (\gamma_{4H}\sum_j|a_jh_j|) dot-product bound is
`3.65e-12`, far above both the observed residual and the registered absolute
limit. The failures are at ordinary machine-rounding magnitude and do not
contradict the exact single-slot algebra.

This is a protocol/measurement-design defect: a relative tolerance referenced
to the tiny forced increment was applied to a cancellation-dominated full
readout. A resolved audit should instead evaluate the local single-slot
increment directly or certify the full-dot result against a declared forward
error envelope. That correction was not preregistered, so it cannot be used
to change the current decision. Under the frozen decision map, two failed
entries make the immutable machine decision
`p4-source-write-architecture-fail`.

## 5. Independent nonlinear dynamic falsifier

Even if the two rounding-limited diagnostics were treated only as unresolved,
P4 would not pass. Every arm independently fails both registered orthogonal
response bounds:

| dynamic observable | observed range | limit | result |
| --- | ---: | ---: | :---: |
| center orthogonal displacement / (\delta) | `0.20716 .. 0.20969` | `0.05` | fail 24/24 |
| actuator orthogonal displacement / (\delta) | `0.15164 .. 0.15587` | `0.05` | fail 24/24 |
| final separation / (\delta) | `0.08153 .. 0.08437` | `0.10` | pass |
| final interaction energy / (U_0) | `0.006647 .. 0.007118` | `0.01` | pass |
| center longitudinal projection / (\delta) | `0.22428 .. 0.25755` | `[0.20,0.80]` | pass |
| actuator longitudinal projection / (\delta) | `0.28780 .. 0.31879` | `[0.20,0.80]` | pass |
| maximum own-chirality D0 / (R_3) | `2.46e-5 .. 1.373e-4` | `0.01` | pass |
| late own-chirality D0 / (R_3) | `3.19e-6 .. 1.489e-5` | `0.002` | pass |
| late opposite-chirality D0 / (R_3) | `1.113418 .. 1.113420` | at least `0.5` | pass |
| maximum center signal / (\delta) | `0.3053 .. 0.3321` | at least `0.25` | pass |

Phase, even/odd response, three-amplitude collapse and mirror equivariance all
pass. The maximum even/odd ratio is `2.97e-5`, the maximum amplitude-collapse
error is `1.49e-5`, and the stored mirror error is zero. The deflection changes
sign with chirality: for the positive-chirality (+x) arm at
(\delta/R_3=10^{-3}), the final normalized center is approximately
(0.2243-0.2072i); the negative-chirality mirror is
(0.2243+0.2072i). The (y) arms rotate covariantly.

This coherent sign change and amplitude collapse argue against random error,
large-amplitude nonlinearity or quotient-shape damage. They support only the
post-result hypothesis of a chirality-odd antisymmetric small-signal response,
schematically

\[
\chi_s(t)=\chi_{\parallel}(t)I+s\chi_{\perp}(t)J,
\qquad J^T=-J,
\]

not the preregistered nearly straight scalar response. Calling this a
Hall-like or gyroscopic susceptibility may be useful notation, but it is not
evidence for magnetic charge, intrinsic spin, angular-momentum conservation
or mass.

The ideal neutral-translation Cayley comparator predicts final separation
`0.018333`, versus `0.08153 .. 0.08437` on the full nonlinear target. It is a
useful positive reference but cannot rescue the failed target arms.

## 6. Role of linearization

The target simulation did **not** replace the native dynamics by a linearized
map. Every active step used the complete nonlinear L3 FIFO update, followed by
the exactly linear readout/adjoint source-write port. Linearization enters only
as an interpretation of weak-response scaling and in the non-decisional ideal
Cayley comparator.

The very small three-amplitude collapse error shows that the tested offsets
remain in a linear-response regime. Hence a linear coupling between memory
and trajectory is sufficient to expose the response tensor in this panel,
but it does not make the complete dynamics linear and does not justify a
scalar mobility or mass reduction.

## 7. Evidence, inference and hypothesis

**Evidence:** the frozen run is complete and informative. Construction,
channel-off, wrong-chirality, covariance, phase, loop-shape, response-collapse
and exact work-ledger controls pass. The registered composite decision is
`p4-source-write-architecture-fail`. All arms fail the two rounding-limited
direct diagnostics and the two substantive transverse-response gates.

**Inference:** the declared source/write architecture has a resolved exact
finite-H work ledger, but the frozen P4 contract does not establish the full
operational straight-line single-loop mechanics it asked for. The transverse
response is compatible with a chirality-conditioned matrix susceptibility
while the loop remains close to its quotient target.

**Hypothesis:** a full (2\times2) longitudinal/antisymmetric response model,
rather than a scalar center mobility, may describe the weak coupled loop.
This is outcome-informed and requires a new falsification contract and a
fresh holdout before it can become evidence.

## 8. Decision and permitted next work

1. The original P4 result remains `p4-source-write-architecture-fail`.
2. P5 two-loop interaction remains closed. No P4 mechanics, momentum or mass
   claim is released.
3. The result report's generic `established_if_full_pass` sentence is
   conditional boilerplate and is explicitly inapplicable to this failure.
4. No threshold, arm, duration, mobility, coupling strength or coefficient may
   be changed within the completed P4 record.
5. A separately named P4-R may be designed only as outcome-informed
   reconciliation. It must first separate numerical metrology from dynamics:
   certify the algebraic single-slot residual against an explicit rounding
   envelope, predeclare a matrix-valued chirality-odd response observable,
   and reserve genuinely new direction/scale data as holdout. Existing P4
   arms are discovery data for that tensor and cannot serve as its independent
   confirmation.

Until such a prospective holdout passes, the strongest accurate statement is:

> The explicit first-order source/write port closes its declared finite-H
> work ledger on the prepared nonlinear L3 loop, but the registered P4
> mechanics gate fails and reveals a large, reproducible chirality-odd
> transverse weak response. This is neither material mass nor spin.
