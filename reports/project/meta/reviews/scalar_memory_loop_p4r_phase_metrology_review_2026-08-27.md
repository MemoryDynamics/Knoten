# Critical review: P4-R-phi phase-averaged source/write response

Date: 2026-08-27.

Review verdict:
**`p4r-phase-averaged-chiral-response-pass-upheld`**.

The registered P4-R-phi result is internally consistent with its frozen
protocol and the narrow numerical claim encoded by
`p4r-phase-averaged-chiral-response-pass`. This review does not promote the
historical P4 result, does not infer mass or spin and does not yet authorize
P4-R-S. The separately preregistered publication-source referee audit remains
mandatory.

## 1. Immutable objects and review timing

| item | immutable identifier |
| --- | --- |
| P4-R design commit | `0bf9b3020f26acfaf5273c1efab5dcc52d596239` |
| P4-R protocol commit | `cb863d4a88c1072637116a0296ab9fc20356a675` |
| source-referee charter commit | `071c9d33c8611d0a1ef1cb3da620acb7dcdb5f7d` |
| initial implementation commit | `a5c7c6d5c0e2611e2ed523ce3da8416620b36d8e` |
| canonical-LF preflight fix | `59dc8875cf991e3d7472db1496c9ae8ffae16ca8` |
| execution revision | `59dc8875cf991e3d7472db1496c9ae8ffae16ca8` |
| runner blob | `27a3a40dde60b797b58da576b5849ab10b47079f` |
| source/write implementation blob | `63d31bc47291f76c65a5633f14436ccd2105fe9a` |
| immutable result commit | `0beaf80f713851ab74bef85a24b8323f42f38108` |
| result JSON blob | `2a668a4c70820bceb0ff84fa1932878d9130aabf` |
| result report blob | `d8435c36d4b83ee3574c84cf1cbcc36e27d8d03a` |
| canonical-LF JSON SHA-256 | `807cf915d1602d87a779e7bf587387559b1b19d7de60dc43c6e1e220b73682c8` |

The protocol and source-referee charter preceded implementation and target
access. The implementation was tested, committed and pushed before the
target runner was invoked. The first invocation stopped in provenance before
constructing or advancing a registered arm because checkout-native CRLF bytes
were compared with an explicitly canonical-LF historical hash. The narrow
canonicalization fix and a line-ending regression test were committed and
pushed before the successful invocation. The aborted preflight produced no
target JSON, report or partial trajectory.

The successful execution started from a clean revision exactly synchronized
with `origin/codex/loop-mechanics-p4r`. Its two atomically generated artifacts
were committed and pushed unchanged before this review began. The recomputed
canonical-LF digest agrees exactly with the digest stored in the report.

## 2. What was registered

The candidate and native map remain the historical L3 finite-memory loop:

```text
candidate = k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1
alpha     = 0.005
H         = 2400
eta       = 0.075
k         = 0.25
delta/R   = 0.0015
updates   = 4000 = 20 memory times
```

The eight new history phases are the odd eighth-turn nodes
`(2m+1) pi/8`. The exact serialized panel is:

- 16 channel-off arms in phase/chirality order;
- 32 active arms in phase/chirality/sign order;
- 401 samples per arm, including updates 0 and 4000;
- 96 exact-ratio, 80-decimal-digit arithmetic replays, at updates 1, 2000
  and 4000 of every active arm.

Direct enumeration of the raw JSON finds no missing, duplicate, truncated or
nonfinite arm. All expected implementation and frozen-dependency blobs in the
result match their registered values. The historical P4 JSON retains its
canonical hash and decision `p4-source-write-architecture-fail`.

## 3. Channel-off and construction controls

All 16 channel-off histories are bitwise equal to the native FIFO update.
Their largest own-orbit distance is

```text
max D0/R = 6.159014148355746e-15
```

and their largest orbit-center magnitude is

```text
max |C_s|/R = 2.966351390995749e-15.
```

Both are more than four orders of magnitude below the registered `1e-10`
limits. Every inherited construction gate passes: coefficient identities,
target notch, conjugacy, adjoint virtual work, translation, proper rotation,
reflection, wrong chirality, raw-center negative control and the static
omitted-age ledger control.

This confirms a prepared, numerically stationary loop and an exact
channel-off implementation. It does not show spontaneous loop formation;
that is a separate, finite-ensemble P3 statement.

## 4. Cancellation-safe metrology

All 32 active arms satisfy normal-or-exact-zero validity. The maximum local
identity residuals, normalized by the first forced center displacement, are

| diagnostic | observed maximum | registered limit |
| --- | ---: | ---: |
| center local identity | `4.486860872882369e-16` | `5e-12` |
| center/actuator local cancellation | `4.486860872882369e-16` | `5e-12` |
| actuator update | `1.531192520297914e-13` | `5e-12` |

The formerly decisive cancellation-dominated full-dot residuals lie inside
their forward envelopes in every update:

| envelope ratio | observed maximum | limit |
| --- | ---: | ---: |
| center full-dot | `2.155001635960272e-5` | `1` |
| center/actuator full-dot | `2.154940734978033e-5` | `1` |
| actuator update | `2.489260072426126e-2` | `1` |

All 96 high-precision checkpoints pass. Their largest residual/envelope ratio
is `2.522e-6`; their largest binary64-to-80-digit distance/evaluation-envelope
ratio is `8.566e-6`.

### Interpretation

**Evidence:** the local forced-increment identities are resolved far below
their registered tolerance, and the old full-dot differences are compatible
with the declared conservative binary64 model.

**Inference:** the two historical P4 metrology failures were caused by an
unresolvable absolute residual criterion rather than evidence of a broken
local source/write identity.

**Not established:** the full-dot envelope is not interval arithmetic and
does not validate an unknown BLAS implementation in general. The 80-digit
replay shares the stored target states and coefficients and is therefore an
independent arithmetic evaluation, not an independent trajectory.

## 5. Work and force ledger

The complete finite-history ledger passes in all arms with these worst
normalized residuals:

| diagnostic | observed maximum | registered limit |
| --- | ---: | ---: |
| per-step write/age split | `3.356032894404742e-12` | `5e-11` |
| per-step total ledger | `3.356217657907912e-12` | `5e-11` |
| cumulative write/age split | `1.241633532186298e-12` | `5e-9` |
| cumulative total ledger | `1.242202827350231e-12` | `5e-9` |
| force balance | `2.025956680032882e-16` | `5e-12` |
| midpoint-force identity | `1.111280397218436e-13` | `5e-12` |

The smallest recorded mobility dissipation is positive,
`1.683342140393484e-12`. Recombining the stored cumulative write, age,
center, actuator and endpoint interaction terms independently reproduces the
stored cumulative ledgers within `9.10e-12` of the initial interaction-energy
scale.

The two registered rivals remain decisively bad: omitting age work reaches a
maximum residual of `6.3868 U0`, while replacing the notched center by raw
memory center reaches `5.5514 U0`. Thus the full age term and declared
notched readout are operationally necessary for this ledger. This validates
the accounting of the declared port; it does not derive that port from a
unique microscopic physical actuator.

## 6. Loop preservation and response margins

All 32 active arms pass every non-orthogonal inherited dynamics gate:

| quantity | worst observed value | registered boundary |
| --- | ---: | ---: |
| maximum own-chirality D0/R | `9.900566357423817e-5` | at most `0.01` |
| late own-chirality D0/R | `1.151161226703699e-5` | at most `0.002` |
| late opposite-chirality D0/R | `1.113418550161328` | at least `0.5` |
| final separation/delta | `0.0840345455249696` | at most `0.10` |
| center longitudinal projection | `[0.2282585, 0.2535733]` | `[0.20, 0.80]` |
| actuator longitudinal projection | `[0.2908453, 0.3157516]` | `[0.20, 0.80]` |
| final interaction-energy ratio | `0.00706180484158819` | at most `0.01` |
| minimum resolved center signal/delta | `0.302067982383544` | at least `0.25` |

The largest phase-increment mean error is `1.3200e-8`, versus a
`7.9067e-5` limit; the largest RMS error is `5.8499e-8`, versus a
`3.9533e-4` limit. The closest ordinary dynamics contacts are final
separation, energy decay and the center projection/signal floors. None is a
roundoff-level pass.

## 7. Odd/even response and covariance

For each phase and chirality, sign-odd and sign-even responses were rebuilt
from the raw active trace minus its matching channel-off trace. The minimum
odd RMS is `0.221587` for the center and `0.548369` for the actuator. Hence no
ratio is rescued by an unresolved denominator.

| control | observed maximum | registered limit |
| --- | ---: | ---: |
| center even/odd RMS | `2.502580353013807e-5` | `0.02` |
| actuator even/odd RMS | `6.557624412978564e-6` | `0.02` |
| mirror center error/R | `2.135448425090927e-15` | `1e-11` |
| mirror actuator error/R | `9.062366711407076e-16` | `1e-11` |
| half-turn center error/R | `2.310161931077142e-15` | `1e-11` |
| half-turn actuator error/R | `8.429893127249514e-16` | `1e-11` |

The response is therefore resolved, almost sign-odd and covariant under both
registered algebraic maps. These controls rule out a simple sign-even offset
or an obvious broken reflection/half-turn implementation in this panel.

They are not replications. The 32 active arms are one deterministic response
construction with sign and chirality controls.

## 8. Frozen phase classifier

The final chirality-paired transverse coefficients are

| quantity | observed | scalar region | positive-chiral region |
| --- | ---: | ---: | ---: |
| center mean | `0.208421577193625` | `abs(B) <= 0.05` | `B >= 0.10` |
| actuator mean | `0.153753085465168` | `abs(B) <= 0.05` | `B >= 0.10` |

The margins above the chiral floor are `0.108422` and `0.0537531`.
Every registered phase node is positive for both observables:

```text
center phase range   = [0.207527662685586, 0.209315491701529]
actuator phase range = [0.152256627106049, 0.155249543824194]
support              = 8/8 and 8/8
```

The raw chirality-specific values also retain the sign, with center values in
`[0.195767, 0.221076]` and actuator values in `[0.141302, 0.166204]`.

### Dependence correction

The eight phase nodes contain only four mirror-distinct pairs. Moreover, the
reported phase averages occupy only two numerical levels: nodes
`0,3,4,7` share one level and nodes `1,2,5,6` share the other to displayed
precision. This is compatible with the registered covariance, but it makes
the dependence stronger rather than weaker. The `8/8` sign count must never
be described as eight independent confirmations or assigned a binomial
significance.

The eight-point rule can alias harmonics of order 8, 16 and above. The result
therefore supports the registered discrete average only; it neither evaluates
a continuous phase integral nor proves pointwise phase independence.

## 9. Independent decision-precedence check

Reapplying the frozen precedence to the raw records gives:

1. provenance, construction, registration, completeness, finiteness,
   normal-number and channel-off conditions pass;
2. every ledger and metrology condition passes;
3. every loop, phase, signal, odd/even and covariance condition passes;
4. neither scalar-null conjunction holds;
5. both positive-chiral means exceed `0.10` and both support counts exceed
   six;
6. no negative or opposite-sign directional-fail condition holds.

The unique registered branch is therefore
`p4r-phase-averaged-chiral-response-pass`, agreeing with the stored result.
No threshold or decision was changed during review.

## 10. Alternative explanations and falsifiers

The pass survives the alternatives that this gate was designed to separate:

- a cancellation-only explanation for the local source/write identity;
- a sign-even displacement offset;
- one of the eight new initial phases carrying the full mean;
- broken mirror or half-turn covariance;
- loss of the prepared L3 loop during coupling;
- omission of finite-history age work or substitution of raw memory center.

It does not separate the following explanations:

1. **Port construction.** The readout and adjoint write port are explicitly
   chirality-conditioned. The observed transverse susceptibility may be a
   dynamical consequence of that declared architecture; it is not evidence
   that a unique physical external port has been derived.
2. **Prepared chirality.** Chirality is selected in the initial loop. The
   result is not spontaneous symmetry breaking and does not establish an
   intrinsic internal `S1` degree of freedom.
3. **Finite memory and one scale.** Only `H=2400`, one L3 candidate and one
   new amplitude were tested. Continuous phase, amplitude collapse,
   finite-H scaling and the Anchor scale remain untested here.
4. **Deterministic environment.** No noise, randomized seed ensemble or
   second numerical stack enters this result.
5. **Kinematics versus ontology.** A chirality-odd transverse response can be
   described as gyroscopic-like only as an analogy. It does not define spin,
   angular momentum, inertial mass or a material center of mass.

The next discriminating scientific test, if source readiness permits, is the
already named P4-R-S Anchor-scale holdout. It must be separately
preregistered; the present L3 values may not be used to tune it.

## 11. Claim boundary and verdict

### Evidence supported

> For the frozen L3 candidate, one perturbation amplitude and eight-node
> deterministic phase quadrature, the explicitly declared reciprocal
> source/write port closes its finite-history work ledger, preserves the
> prepared loop and exhibits a resolved positive chirality-odd transverse
> center and actuator response. The registered discrete phase-averaged P4-R
> classifier passes.

### Evidence not supported

- a revision of the historical P4 formal fail;
- continuous or arbitrary-phase invariance;
- amplitude or finite-H scaling of the transverse response;
- a stable family of interacting loops;
- a physical actuator derivation or conserved total momentum;
- internal `S1`, spin, angular momentum, inertia or mass;
- P5 or a paper-level mechanics claim without the source audit.

Within that boundary, the P4-R decision is upheld. The result is stronger
than the P4 discovery observation because it uses new phases and resolved
metrology, but it remains an outcome-informed deterministic holdout of the
same candidate and architecture.

P4-R-S remains **closed at this review stage**. It can become eligible for
prospective protocol writing only after the frozen publication-source audit
returns a compatible verdict and every required claim restriction is
propagated consistently.
