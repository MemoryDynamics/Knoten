# Critical result review: P4-R-S Anchor-scale transfer

Date: 2026-08-30.

Verdict: **`p4rs-result-review-upholds-scale-transfer`**.

The stored decision **`p4rs-anchor-scale-transfer-pass`** is upheld within
the exact boundary of the prospectively frozen P4-R-S protocol. The result
supports a deterministic second-cell transfer of the registered discrete
source/write response on one matched memory-time ladder. It opens **only
prospective P5 protocol writing**. It is not P5 evidence and does not establish
continuous phase invariance, convergence order, a physical actuator,
momentum, intrinsic spin, inertia, a material center of mass or physical mass.

The review finds no result-fatal critical or new major defect. It retains the
three open publication-source major restrictions and one explicit audit-
granularity limitation. Consequently the result is internally gate-ready and
restricted-source usable, not independently certified or unrestricted-source
ready.

## 1. Review question and disposition

The review asks:

> Does the first frozen P4-R-S output faithfully implement the preregistered
> decision, survive an independent raw-JSON reconstruction, and justify
> opening P5 protocol writing without exceeding the registered claim
> boundary?

The answer is **yes**, with the following strict separation:

- **evidence:** the frozen Anchor panel is complete, all inherited gates pass,
  the independently reconstructed decision agrees, and every registered
  cross-scale discrepancy is below `0.05`;
- **inference:** the L3 chiral response is not explained solely by failure at
  that one discretization, because a pre-existing second prepared cell gives
  a compatible response under the same declared rule;
- **hypothesis:** a continuum family, an $S^1$ field, toroidal dynamics,
  conserved interaction quantities, spin, inertia and mass remain untested.

## 2. Frozen object and execution chronology

### 2.1 Prospective chain

| object | immutable identifier | status |
| --- | --- | --- |
| green source-audit base | `ecdaa8522337880aa1504af8c66924be96e0a9db` | complete |
| P4-R-S design audit | commit `11cabd66d0ba086116b29b3ea3d8a8548560cea1`; blob `dec2f0c281f19fadc02412b04a78f78f0793422a` | CI 33320927753 green |
| P4-R-S protocol | commit `3797c98c83ed61fa02e939583782fd7213e0b961`; blob `e88557a77ed2937a0e65dc7880311a0804432f8b` | CI 33321607082 green |
| implementation | commit `d5cc87617a790c7b4be3664e36b261fc0c29ecc2` | CI 33331509204 green |
| target runner | blob `a3f1b2d4f9089d00f3786721ad1dcf13895377f7` | frozen before access |
| pre-target test module | blob `0dc1177d4cd1921c5dd1c6a3c26e1614221979c2` | frozen before access |
| implementation-readiness review | commit/execution revision `83185e00dc30575ad57cf7f0ec7c76f6ba7baa77`; review blob `64b771deff282a3c3bc2952f8f857d1c1d143383` | CI 33331842923 green |

The execution revision was clean, pushed and equal to its upstream. Both
default output paths were absent. The design and protocol commits were
ancestors, and every frozen source, native-map, historical-result and review
blob matched before target access.

### 2.2 Invocation record

One attempted direct file invocation stopped during Python import resolution
with `ModuleNotFoundError` before provenance verification, target construction
or any Anchor trajectory call. It created neither output nor partial result.
The first registered module invocation then ran from the clean pushed
execution revision, completed all arms in `81.7657 s`, and wrote the two
outputs atomically. No target rerun was performed.

This distinction is operational, not semantic: the failed direct invocation
did not access the registered target. It is recorded here so that “first run”
does not hide an earlier shell-level failure.

### 2.3 Raw result freeze

| artifact | frozen identifier |
| --- | --- |
| result commit | `6817d758c6287472c57c46780b938ab8fd7935a9` |
| result-commit parent | `83185e00dc30575ad57cf7f0ec7c76f6ba7baa77` |
| JSON blob | `e4eae06ada6860455e49a08691235b9f6e818f51` |
| JSON canonical-LF SHA-256 | `daf127a55adf0eaa60325725493781a94fad3601bf52e90c38ba8c5e13ff62a7` |
| report blob | `b5d085d665bc60d82279458072e775d0cf794ee8` |
| report canonical-LF SHA-256 | `f2a76ddbd79337b7a527fcd9951b6ab6b890b0fda7137d0791531cd8094132d0` |
| stored decision | `p4rs-anchor-scale-transfer-pass` |

The raw output was committed and pushed unchanged before scientific review.

## 3. Post-result CI lifecycle finding

The raw-freeze CI run 33332152479 failed with **829 passed, one failed**. The
only failure was the prospectively correct pre-target assertion that the
default result paths did not exist. Once the result was deliberately frozen,
that assertion became a stale lifecycle assumption.

The post-result correction changed no runner, model, threshold, trajectory,
result or report. It changed the test to require:

1. both frozen outputs exist;
2. both exact canonical hashes match;
3. the runner still refuses to overwrite them;
4. alternative output paths remain prohibited.

The independent-auditor commit
`07b8c15d3c028e7c478bae23c0c24572860dde82` closes this finding. CI run
33333066614 is green with 836 tests, the exact Ruff scope and strict MkDocs.
The historical red run remains part of the record and is not reclassified as
green.

Finding **P4RS-RES-MIN-001**: closed. This was a post-target test lifecycle
defect, not a scientific gate failure.

## 4. Exact Anchor root and static port

The independent standard-library reconstruction parses the full frozen
decimals, verifies membership in the stored interval intersection, and agrees
exactly with the stored 120-digit refined root. It rebuilds

$$
B_H(e^{i\theta})=
\sum_{j=0}^{H-1}{\alpha(1-\alpha)^j\over
1-(1-\alpha)^H}e^{-ij\theta},
$$

$$
a_0={\bar w_0-B_H(e^{i\theta})\over1-B_H(e^{i\theta})},
\qquad G=\nu=|a_0|^2.
$$

The maximum difference from the frozen static values is
`5.551115123125783e-16`, versus the `5e-13` tolerance. The reconstructed gain
is `0.4020914043226346`; the stored binary64 value is
`0.4020914043226352`. The L3 gain is not copied into the Anchor.

The exact scale relations also hold:

$$
H_A\alpha_A=1200\times0.01=12,
\qquad {\eta_A\over\alpha_A}=15.
$$

## 5. Panel registration and common memory time

The frozen JSON contains, in the registered order:

- 16 channel-off arms: eight phases and two chiralities;
- 32 active arms: eight phases, two chiralities and two offset signs;
- 401 stored samples per arm;
- Anchor steps `0,5,...,2000`;
- L3 steps `0,10,...,4000`;
- common memory times $\tau=0,0.05,\ldots,20$ without interpolation;
- 96 high-precision checkpoints: three per active arm.

Every stored trace is complete and finite. Phase, chirality, sign and arm
order agree exactly. Channel-off maxima are

$$
\max D_0/R_A=6.00\times10^{-15},
\qquad \max |C_s|/R_A=3.25\times10^{-15},
$$

well below `1e-10`.

## 6. Source/write metrology and exact work ledger

### 6.1 Decisive contacts

| diagnostic | worst observed | frozen limit |
| --- | ---: | ---: |
| step write/age split divided by $U_0$ | `2.242e-12` | `5e-11` |
| step total ledger divided by $U_0$ | `2.242e-12` | `5e-11` |
| cumulative split divided by $U_0$ | `1.088e-12` | `5e-9` |
| cumulative total ledger divided by $U_0$ | `1.090e-12` | `5e-9` |
| force balance divided by $|F_0|$ | `6.267e-17` | `5e-12` |
| midpoint force divided by $|F_0|$ | `1.098e-13` | `5e-12` |
| center local residual divided by $D_0$ | `2.976e-16` | `5e-12` |
| coupling local residual divided by $D_0$ | `2.976e-16` | `5e-12` |
| actuator full residual divided by $D_0$ | `7.605e-14` | `5e-12` |
| largest full-envelope ratio | `0.02488` | `1` |
| minimum mobility dissipation | `3.264e-12` | at least `-1e-30` |

The independent cumulative recombination differs from the stored ledgers by
at most `5.9165e-12` of $U_0$, within the audit tolerance `2e-11`.

All 96 high-precision records pass. Their largest high-precision residual
uses only `5.11e-6` of its full envelope, and the largest binary64-to-reference
distance uses `2.22e-5` of its evaluation envelope.

### 6.2 Nondecisional rivals

Omitting the finite-history age term yields a cumulative residual as large as
`720.0 U0`; substituting the raw memory center yields as much as `656.9 U0`.
These controls are strongly nonzero and cannot rescue or replace the declared
finite-history center ledger. The pass is therefore not obtained by silently
dropping the FIFO boundary contribution.

### 6.3 Audit granularity

The independent auditor can recompute every gate from serialized maxima,
envelopes, cumulative work terms, 96 reference records and stored stride-5
states. It cannot regenerate non-serialized per-update histories, raw ledger
operands, channel-off bitwise arrays or per-update normal/subnormal flags.
Those facts are covered by the frozen runner, pre-target tests and deterministic
full execution, not by a second independently stored arithmetic trace.

Finding **P4RS-RES-LIM-001**: open and accepted for this internal gate. It
prohibits “independently certified” or “formally verified” wording and is a
reproducibility limitation, but it does not contradict a frozen gate whose
protocol explicitly stores summaries rather than every update operand.

## 7. Nonlinear loop and phase gates

| diagnostic | worst observed | frozen requirement |
| --- | ---: | ---: |
| maximum own-chirality $D_0/R_A$ | `9.905e-5` | at most `0.01` |
| late own-chirality $D_0/R_A$ | `1.127e-5` | at most `0.002` |
| late opposite-chirality $D_0/R_A$ | `1.1095` | at least `0.5` |
| final separation divided by $\delta_A$ | `0.08248` | at most `0.10` |
| center longitudinal projection | `[0.2292,0.2549]` | `[0.20,0.80]` |
| actuator longitudinal projection | `[0.2906,0.3160]` | `[0.20,0.80]` |
| final interaction-energy ratio | `0.006803` | at most `0.01` |
| phase mean error divided by $\theta_A$ | `1.688e-6` | at most `0.01` |
| phase RMS error divided by $\theta_A$ | `7.349e-6` | at most `0.05` |
| minimum center signal divided by $\delta_A$ | `0.3011` | at least `0.25` |

The tightest inherited contact is final separation: `82.5%` of its allowed
maximum. The energy ratio uses `68.0%` of its allowance. These are genuine
passes, but they are not asymptotically small and should remain visible in any
paper-level sensitivity discussion.

## 8. Discrete chiral response and symmetries

The independently reconstructed final means are

| component | Anchor | L3 | absolute difference |
| --- | ---: | ---: | ---: |
| $A_C$ | `0.24204809` | `0.24091331` | `0.00113478` |
| $B_C$ | `0.20609447` | `0.20842158` | `0.00232710` |
| $A_Q$ | `0.30333072` | `0.30329608` | `0.00003464` |
| $B_Q$ | `0.15260066` | `0.15375309` | `0.00115243` |

Both Anchor chiral means exceed `0.10`; the smaller margin is
`0.05260066`. Center and actuator each have strictly positive paired support
at `8/8` phase nodes. The scalar and directional-failure regions are false.

The largest even-to-odd RMS ratio is `2.5424e-5`, versus `0.02`. The largest
mirror or half-turn covariance error is `1.8629e-15 R_A`, versus
`1e-11 R_A`. Thus the registered discrete symmetries and sign-odd response
close with large numerical margins.

These 32 arms are not 32 independent observations. Phase, chirality and sign
are deterministic symmetry/control factors. No p-value, binomial support
probability or replication count may be inferred from them.

## 9. Cross-scale estimands

### 9.1 Complete transient RMS

| component | RMS difference | limit |
| --- | ---: | ---: |
| $A_C$ | `0.00126192` | `0.05` |
| $B_C$ | `0.00157241` | `0.05` |
| $A_Q$ | `0.00083880` | `0.05` |
| $B_Q$ | `0.00055377` | `0.05` |

### 9.2 Final phase-profile RMS

| component | RMS difference | limit |
| --- | ---: | ---: |
| $A_C$ | `0.00115605` | `0.05` |
| $B_C$ | `0.00232715` | `0.05` |
| $A_Q$ | `0.00018370` | `0.05` |
| $B_Q$ | `0.00115389` | `0.05` |

### 9.3 Final means

The four absolute mean differences are `0.00113478`, `0.00232710`,
`0.00003464` and `0.00115243`. The largest registered discrepancy is the
$B_C$ phase-profile RMS, `0.00232715`. It consumes `4.65%` of the frozen
`0.05` allowance, leaving the smallest scale slack `0.04767285`.

The result demonstrates compatibility at the registered effect size. It does
not demonstrate exact scale invariance: the differences are nonzero. With only
two cells, it also cannot identify monotonicity, a convergence order or an
$\alpha\to0$, $H\to\infty$ limit.

## 10. Independent raw-JSON recomputation

The independent auditor is frozen as follows:

| object | identifier |
| --- | --- |
| auditor commit | `07b8c15d3c028e7c478bae23c0c24572860dde82` |
| auditor blob | `116f91c13f86b585c7c22d94d33d63b89d083aeb` |
| auditor test blob | `d2e3eee4c8b298d5492ed147c3cea75e2cd37336` |
| auditor CI | 33333066614, green |
| audit-output commit | `ab16a09f0f65f202bf4334f3d7a99bb0ab2224c3` |
| audit-output blob | `9a4da1e68c877ad4776f1ec81cfa4f99469e67b4` |
| audit-output canonical-LF SHA-256 | `b25dec2cdde88df004ce73b61f3b5246a25c6c1d20df97beb155e3622ebb9d0b` |
| audit-output CI | 33333262568, green |

The auditor imports neither the target runner nor NumPy, SciPy or mpmath. It
uses the standard library and three generic primitives from the older
independent P4-R auditor: finite-tree validation, phase unwrapping and
recursive stored/recomputed comparison. It independently rebuilds:

1. exact-root membership and the static $B_H$, $a_0$, $G=\nu$ values;
2. registration, completeness and common memory time;
3. local/full gate inequalities, cumulative ledgers and both rivals;
4. all 96 precision-record inequalities;
5. late loop and phase metrics from stored trajectories;
6. Anchor and raw-L3 sign-odd/even responses;
7. mirror and half-turn errors;
8. all transient, profile and mean scale arrays;
9. exact decision precedence.

It returns **`p4rs-independent-audit-agrees`**, with zero field differences
and the same recomputed P4-R-S decision. A mutation test changes a stored
scale summary while leaving the raw traces intact; the auditor then returns
disagreement. Fail-closed decision-table tests separately cover missing common
time, ledger failure and cross-scale mismatch.

This is independent analysis of shared stored trajectories, not an independent
experimental replication.

## 11. Decision precedence

The recomputed top-level gates are:

| gate | result |
| --- | --- |
| pipeline and registration | pass |
| active validity | pass |
| reciprocal ledger and metrology | pass |
| nonlinear loop dynamics | pass |
| response availability and symmetry | pass |
| finite response means | pass |
| scalar region | false |
| positive chiral region | true |
| positive phase support | true |
| directional-failure region | false |
| common memory-time grid | pass |
| cross-scale transfer | pass |

The preregistered precedence therefore reaches exactly
**`p4rs-anchor-scale-transfer-pass`**. No earlier inconclusive, ledger-failure,
scalar, directional-failure or cross-scale-mismatch branch applies.

## 12. External-validity and symmetry dependence

The result remains restricted by all of the following:

1. **Two prepared cells only.** Anchor and L3 share one matched ladder. No
   convergence order or open parameter neighbourhood follows.
2. **One deterministic implementation family.** The same code base and model
   construction generate both cells. This is a holdout, not independent
   replication by another implementation or group.
3. **Outcome-informed ancestry.** P4-R was designed after the P4 transverse
   discovery. The Anchor target panel was unopened and the Anchor candidate
   pre-existed, but the broader response class is not discovery-independent.
4. **Eight discrete phase nodes.** Exact mirror and half-turn covariance do
   not establish continuous $S^1$ equivariance or toroidal topology.
5. **One offset magnitude.** The sign-odd estimator controls parity at
   $\delta/R=1.5\times10^{-3}$; it does not establish an amplitude-independent
   linear-response tensor.
6. **Prepared-orbit conditionality.** The result begins from certified,
   constructed rotating waves. It does not show spontaneous formation,
   robustness to broad perturbations or interaction survival.
7. **No physical calibration.** The dimensionless reciprocal source/write
   ledger is exact for the declared model, but it is not yet a physical force,
   work, momentum or mass law.

## 13. Publication-source restrictions

The three previously audited major restrictions remain open and unchanged:

- **SRC-MAJ-001:** a single `mpmath.iv` interval trust base rather than an
  independent interval implementation or proof-assistant certificate;
- **SRC-MAJ-002:** no complete original environment wheel/hash lock;
- **SRC-MAJ-003:** no immutable citation/release archive.

P4-R-S does not resolve them. The permitted source verdict remains
**`referee-source-ready-with-major-claim-restrictions`**. An unrestricted
publication-source claim remains prohibited.

## 14. Allowed and prohibited claims

### 14.1 Allowed restricted claim

> The same explicit reciprocal source/write construction produces compatible
> dimensionless finite-history ledger and sign-odd response results at the
> prepared L3 and Anchor cells under the preregistered discrete phase and
> cross-scale gates. The maximum registered scale discrepancy is `0.00233`
> against the frozen `0.05` effect-size limit.

This wording must be accompanied by the two-cell, deterministic,
outcome-informed and restricted-source qualifiers.

### 14.2 Prohibited claims

The result may not be described as proof of:

- exact scale invariance or a continuum limit;
- continuous $S^1$ topology or a torus;
- independent replication or statistical significance;
- a physical actuator, force or work observable;
- conserved momentum, intrinsic spin, inertia or mass;
- two-loop interaction;
- P5 success or Paper-I mechanics closure;
- formal verification or independent certification.

## 15. Consequence for P5 and Paper I

P5 **protocol writing is now open** because the only registered prerequisite
was a separately reviewed P4-R-S full pass. P5 implementation, target access
and evidence remain closed until a new design audit and prospective protocol
are committed, pushed and CI-green.

A defensible P5 design must, before any interaction target is opened:

1. define two independently addressable prepared loops and the exact coupling
   channel;
2. distinguish self-response from mutual response with channel-off,
   one-sided and reciprocal controls;
3. freeze an interaction observable and complete mutual work/ledger identity;
4. include swap, reflection, chirality and separation controls without calling
   them replications;
5. register null, directional-failure and inconclusive branches;
6. prohibit retuning to a desired attraction, repulsion, locking or orbit;
7. retain the no-spin/no-inertia/no-mass claim boundary unless separately
   earned by later falsification tests.

For Paper I, the immediate task is not to add an interaction claim. It is to
consolidate the now reviewed P4/P4-R/P4-R-S evidence chain, state the finite
ledger and discrete-response result in restricted language, expose the
failure and limitation record, and keep P5 as prospective work.

## 16. Final referee disposition

**Internal scientific gate:** accept.

**Stored P4-R-S decision:** uphold.

**Independent raw-data reconstruction:** agrees, with zero stored-summary
differences and the explicit non-serialized-update limitation.

**P5 status:** protocol writing open; implementation, execution and evidence
closed.

**Publication status:** usable only under the existing major claim
restrictions; unrestricted source-ready wording remains blocked.

**Mechanics interpretation:** spin, inertia and mass remain hypotheses, not
results.
