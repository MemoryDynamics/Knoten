# P4-R design audit: phase averaging and resolved source/write metrology

Date: 2026-08-26.

Decision: **select a same-L3 phase-holdout reconciliation before any
cross-scale or two-loop continuation. Do not open a new target trajectory in
this audit.**

P4-R is outcome-informed. It cannot rename the completed P4 decision
`p4-source-write-architecture-fail`, remove a failed arm or retroactively
change a threshold. Its two questions are narrower:

1. Does a cancellation-safe evaluation confirm the source/write identities
   that are algebraically exact but unresolved by the original full-dot
   subtraction?
2. Does the chirality-odd transverse response survive averaging over genuinely
   new force-to-orbit start phases, or was it a phase-conditioned artifact of
   the original two laboratory directions?

A pass would establish neither material mass nor intrinsic spin. It would
only resolve the declared artificial port metrology and identify a
weak response that survives the registered discrete eight-phase average of
the prepared L3 loop.

The evidential boundary is fixed before the design:

- **evidence:** P4 closed its exact write/age ledger and observed a
  chirality-odd transverse response in its registered finite panel;
- **inference to be tested:** ordinary binary64 cancellation, rather than a
  broken source/write identity, caused the two full-dot residual failures;
- **hypothesis to be tested:** a nonzero chirality-odd component survives a
  new discrete average over force-to-orbit start phase.

## 1. Frozen evidence base

The audit starts from main revision

```text
8f215e88e6f6344a33dcc765ee11a904644a1ab5
```

with these canonical Git blobs:

| dependency | Git blob |
| --- | --- |
| P4 result JSON | `41ddfb5ec2d4c907607995523775072ad12544f7` |
| P4 critical review | `46f5417efe34343368fb0c0694fa5928b9dea4e0` |
| P4 protocol | `fb1f41c66fad0e6df9c7dc8a226517940deab939` |
| P4 target runner | `c44b186dc3b0d22cf6434df5532a60d3bb22eb07` |
| orbit-center source/write module | `d8de95f4f46adc43c37d6d1affdc73be14f70ec3` |
| native nonlinear FIFO map | `9defb5a6876371202e1ba57cea030c997b9c6edd` |
| anchor interval result | `fc6e816c6895e408693fbde176afdaee963c20b9` |
| anchor stability result | `1c9d5746c9553d9cb8031b58258e6d613f1633d9` |

The canonical LF SHA-256 values are

```text
P4 JSON          ea0651e206451e5f87ec08ab3f66ec68df2c04bee2d1b9d67219736058a275cc
anchor interval  63dc4158c0d8a9543230b656b7602feef76a48a2a75fbe6a6e001cb81082a840
anchor stability 43b0d7f5e5ba81dc35d4a2e9d138d3663a3d98b67bcb09ed2d4572d5a01eb86f
```

The P4 result remains authoritative. Any reconciliation output must quote it
as a historical fail and use its arms only as discovery data.

The P4-review blob above is the historical main-line object at audit start.
The present audit change also repairs its inline math delimiters and narrows
one overstatement about the old $x/y$ comparison. Those editorial and
interpretive corrections do not alter the P4 result, protocol, source or
decision. The later P4-R-phi protocol must pin the corrected review blob.

## 2. What P4 actually resolved

The exact work quantities passed in every P4 arm. The maximum per-step full
interaction-ledger residual was `9.596e-12` of initial energy, below the
registered `5e-11`; the maximum cumulative residual was `3.727e-12`, far
below `5e-9`. Force balance, midpoint force, actuator update, channel-off,
loop D0, late phase, even/odd response, three-amplitude collapse and mirror
equivariance also passed.

The formal architecture label failed because the full-readout expressions

$$
r_C=C(h')-C(\widetilde h)-\alpha G F,
$$

$$
r_{CQ}=C(h')-C(\widetilde h)+(Q'-Q)
$$

were computed as differences of cancellation-dominated 2400-term dot
products. Their absolute residuals were only
`2.358e-16 .. 3.278e-16`, but the registered normalization demanded
`1.180e-18 .. 4.721e-18`.

The same run contained a substantive dynamic result. At final time, after
aligning signs and chirality, the discovery coefficients were:

| original lab direction | center longitudinal | center chiral transverse | actuator longitudinal | actuator chiral transverse |
| --- | ---: | ---: | ---: | ---: |
| $x$ | `0.224281` | `0.207157` | `0.287804` | `0.151637` |
| $y$ | `0.257546` | `0.209686` | `0.318788` | `0.155869` |

The transverse terms are close and keep the same chirality-registered sign;
the longitudinal terms differ by about 10--15 percent.

## 3. The phase confound missed by the first interpretation

For a prepared history $h^{(s)}$, a common proper rotation

$$
h^{(s,\varphi)}_j=e^{i\varphi}h^{(s)}_j,
\qquad Q^{(\varphi)}=e^{i\varphi}Q
$$

is an exact covariance of the native map and source/write port. P4 checked
this construction statically.

The dynamic $x$ and $y$ arms did something different: they retained the same
history phase and changed only the initial actuator direction. They therefore
sampled two relative angles between the forcing direction and the prepared
orbit phase. The resulting response is more honestly written

$$
\chi_s(t;\varphi_0),
$$

not yet as a phase-independent tensor $\chi_s(t)$. A new oblique direction at
the same start phase would add another relative angle but would not determine
the phase average. Rotating history and actuator together would be almost a
tautological covariance replay.

The discriminating follow-up is instead to hold the laboratory actuator along
$e_x$ and rotate only the prepared history through a uniform, previously
unopened phase grid.

## 4. Selected first reconciliation: P4-R-phi

The first reconciliation retains the exact L3 candidate, native map,
source/write equations, $k=0.25$, matched mobility, 20 memory times and every
non-orthogonal P4 loop/ledger threshold. It changes no physical or dynamic
parameter.

The only new target design is:

$$
\varphi_m={ (2m+1)\pi\over8},\qquad m=0,\ldots,7,
$$

$$
{\delta\over R_3}=1.5\times10^{-3},
\qquad Q_0=\sigma\delta e_x,
\qquad \sigma\in\{+1,-1\}.
$$

All eight phases and the amplitude are new relative to the P4 dynamic target
panel; the earlier static covariance checks are not target trajectories.
Both registered chiralities are used, producing 32 active arms. The signs and
chiralities are symmetry/oddness controls, not independent replications.
Channel-off baselines are evaluated at every phase and chirality so that
phase-dependent binary64 drift cannot enter the response comparison.

The offset `1.5e-3` is the arithmetic midpoint of two old amplitudes and was
not previously simulated. It is fixed to test interpolation within the
already demonstrated weak regime, not selected by opening a new trace.

## 5. Cancellation-safe metrology

The decisive local slot identity will be evaluated before adding the input to
the order-one state:

$$
\Delta C_{\rm local}=a_0(\alpha a_0^*F),
$$

$$
r_{C,\rm local}=\Delta C_{\rm local}-\alpha |a_0|^2F,
$$

$$
r_{CQ,\rm local}=\Delta C_{\rm local}+\Delta Q.
$$

These expressions use only quantities on the forced-increment scale. Their
registered relative threshold remains `5e-12` of the first-step coupling
displacement; no scientific tolerance is relaxed.

The original full-dot residuals remain stored. They are not silently removed.
For each complex dot product, define

$$
\gamma_{8H}={8H\epsilon_{64}\over1-8H\epsilon_{64}},
$$

and a conservative forward envelope from the absolute weighted sums of the
provisional and final histories, plus the final subtraction terms. The full
residual must lie inside that envelope. Failure of the small-scale identity
or of the full-dot envelope is an architecture/metrology failure. Passing it
does not rename P4; it only resolves why the old diagnostic was unmeasurable.

The exact write/age/interaction ledger, force balance and mobility
dissipation remain independently decisive with their original thresholds.

## 6. Phase-averaged response observable

For each phase and chirality, first subtract its matching channel-off trace,

$$
\widehat C_{s,m,\sigma}(t)
=C_{s,m,\sigma}(t)-C^{\rm off}_{s,m}(t),
$$

and analogously for $Q$. Then use the sign-odd response

$$
C^{\rm odd}_{s,m}(t)
={\widehat C_{s,m,+}(t)-\widehat C_{s,m,-}(t)\over2\delta},
$$

and analogously $Q^{\rm odd}_{s,m}$. With the laboratory input along $e_x$,
define chirality-aligned components

$$
A_C=\operatorname{Re}C^{\rm odd},
\qquad
B_C=-s\operatorname{Im}C^{\rm odd},
$$

and $A_Q,B_Q$ in the same way. Average first over mirrored chiralities and
then over the eight new phases. Classification uses the registered final
sample after 20 memory times; the full traces remain subject to the inherited
transient, phase and loop-preservation controls. The phase is the effective
deterministic sampling unit; duplicated signs and chiralities may not inflate
a sample count.

This is an eight-point discrete quadrature, not a proof of a continuous phase
integral or pointwise phase independence. It can alias phase harmonics whose
order is a multiple of eight. Any positive claim must therefore be worded as
"survives the registered eight-phase average" unless a separately
preregistered refinement resolves the continuous-phase question.

For the sign-consistency count, define the chirality-paired phase values

$$
B_{C,m}^{\rm pair}={1\over2}\sum_{s\in\{-1,+1\}}B_{C,s,m},
\qquad
B_{Q,m}^{\rm pair}={1\over2}\sum_{s\in\{-1,+1\}}B_{Q,s,m}.
$$

A chiral pass requires strictly positive paired values in at least six of
eight phases separately for center and actuator. This is a deterministic
sign-support gate, not a binomial significance claim.

The old straight-response boundary supplies the scalar null region

$$
|\overline B_C|,|\overline B_Q|\le0.05.
$$

The smallest P4 discovery transverse coefficient was `0.151637`. The
outcome-informed chiral alternative floor is frozen at `0.10`, approximately
the midpoint between the old null boundary and that smallest discovery value:

$$
\overline B_C,\overline B_Q\ge0.10.
$$

Values with $0.05<|\overline B|<0.10$, a mixed scalar/chiral classification,
insufficient signal or fewer than six of eight phasewise positive
coefficients are inconclusive. A resolved
component at or below `-0.10`, or center and actuator components of magnitude
at least `0.10` with opposite signs, is a directional falsification rather
than an inconclusive chiral pass. This gap prevents a marginal trace from
being labelled either scalar or chiral.

## 7. Layered decisions

- **`p4r-phase-averaged-chiral-response-pass`:** provenance, local metrology,
  full-dot envelope, exact ledger, channel-off, completeness, oddness,
  quotient-loop, phase and all chiral-alternative gates pass. This does not
  alter P4 and opens only a separately preregistered cross-scale anchor
  holdout.
- **`p4r-phase-averaged-scalar-response`:** the valid complete panel lies in
  the scalar null region for both center and actuator. This falsifies the
  phase-averaged chiral hypothesis and closes its route.
- **`p4r-phase-averaged-chiral-hypothesis-fail`:** a valid, resolved panel
  has a component at or below `-0.10`, or center and actuator have magnitudes
  of at least `0.10` with opposite signs. This falsifies the registered
  direction of the discovery hypothesis and closes its route.
- **`p4r-ledger-or-metrology-fail`:** a valid run fails the resolved
  source/write, forward-envelope or exact work identities.
- **`p4r-inconclusive`:** provenance, numerical validity, completeness,
  signal, loop preservation, oddness or the predeclared response gap prevents
  a decision.

No outcome opens P5 directly. Only a reviewed chiral phase pass may open the
anchor scale holdout. Mass, momentum, internal $S^1$, torus, spin and two-loop
interaction remain outside this gate.

## 8. Falsifiers retained

P4-R-phi must fail or remain inconclusive if any of the following occurs:

1. after this audit commit, the P4 JSON, corrected review, native map or
   source/write module changes before the protocol freeze;
2. any new phase or amplitude is removed after target access;
3. the local single-slot identity fails on the input scale;
4. the full-dot residual exceeds its forward rounding envelope;
5. the write/age term is omitted or raw $c_H$ replaces $C_s$;
6. the channel-off phase grid leaves the prepared quotient orbit;
7. the sign-odd phase response is unresolved or dominated by even response;
8. the phase average enters neither registered scalar nor chiral region;
9. loop D0, opposite chirality or native phase gates fail;
10. a result is interpreted as mass, spin, conserved momentum or P5
    authorization.

The next action after this audit is to freeze the exact runner paths,
provenance blobs, forward-error formula, arm order and thresholds in a
separate protocol commit. No P4-R target output may be opened before that
commit is clean, pushed and fully tested.
