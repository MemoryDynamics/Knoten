# Prospective P4-R-phi gate: discrete phase response and resolved metrology

Date: 2026-08-26.

Status: **frozen prospectively after the P4-R design audit and before any
registered P4-R-phi target trajectory is advanced.** At protocol writing, the
planned runner and both planned result files do not exist. Static formulas,
historical P4 output and dependency blobs may be inspected; no arm at the new
phase grid or amplitude may be evaluated before the clean implementation
freeze described below.

## 1. Question, historical decision and claim boundary

The immutable P4 decision is

```text
p4-source-write-architecture-fail
```

P4-R-phi does not rerun, rename or rescue that gate. It asks two narrower,
outcome-informed questions:

1. Do the exact source/write identities pass when the decisive residual is
   formed on the forced-increment scale, while the original full-dot residual
   remains inside a predeclared binary64 forward-error envelope?
2. Does the discovery sign of the chirality-odd transverse response survive
   a new discrete average over eight prepared-history phases?

The hypotheses are separated from the evidence:

- historical evidence is limited to the P4 finite panel, exact ledger and
  observed transverse coefficients;
- the binary64 explanation of the two failed direct residuals is an inference
  tested here;
- the phase-averaged chirality-odd response is a new hypothesis tested here.

Even a reviewed chiral pass establishes only that the declared artificial
source/write port closes locally and that its weak response survives this
registered eight-point phase quadrature on the prepared L3 loop. It does not
establish a continuous phase integral, phase-independent mobility, material
mass, a center of mass, conserved momentum, intrinsic spin, internal $S^1$,
a torus, two-loop interaction or P5. A reviewed chiral pass may open only a
separately preregistered P4-R-S anchor-scale holdout.

## 2. Frozen provenance

The design base is revision

```text
0bf9b3020f26acfaf5273c1efab5dcc52d596239
```

and the runner must verify these Git objects before target access:

| dependency | frozen Git blob |
| --- | --- |
| P4-R-phi design audit | `45920014d5b98087ecadca832b216818b4d6d18a` |
| corrected P4 critical review | `4412f6050896a33a275ad10e1d1c0e524bcfba3f` |
| immutable P4 result JSON | `41ddfb5ec2d4c907607995523775072ad12544f7` |
| P4 protocol | `fb1f41c66fad0e6df9c7dc8a226517940deab939` |
| historical P4 runner | `c44b186bfb56567b300903e846540e5a21231ff0` |
| source/write implementation before reconciliation | `d8de95f4f46adc43c37d6d1affdc73be14f70ec3` |
| native nonlinear FIFO map | `9defb5a6876371202e1ba57cea030c997b9c6edd` |
| rotating-wave formation/phase utilities | `38f16f11a790a64470bab3a34505825cf815e7f0` |
| rotating-wave candidate definition | `630beb9952abefea823d91388dcbb2de8f1a2927` |
| raw finite-memory center utility | `a8b8a002be3a3e4d75f8bd6b00989f1dafe61e0b` |

The canonical-LF SHA-256 of the P4 JSON remains

```text
ea0651e206451e5f87ec08ab3f66ec68df2c04bee2d1b9d67219736058a275cc
```

and its stored decision must remain the historical fail above. The commit
containing this protocol becomes the protocol freeze revision. The later
runner must record that revision, the clean pushed implementation revision,
all dependency and implementation blobs, Python/NumPy/platform versions and
an initially clean worktree. Missing provenance, a dirty tree, an altered
dependency or pre-existing target output is `p4r-inconclusive`, never a
scientific response result.

## 3. Unchanged L3 candidate and port equations

The candidate remains exactly

```text
k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1
```

with the frozen decimal values

```text
R3 = 0.944805811705743656419366118422595657454474452804188781825799206245348464567689511866917417017911971955244464
theta3 = 0.00790666146243552374938496703030974246197803459527409259815696583141708245813094145986593003659167675765833059
```

and

$$
d=2,\quad \varepsilon=0,\quad M_0=1,
$$

$$
(\alpha,H,\eta)=(0.005,2400,0.075),
$$

$$
(\sigma_{\rm rep},\sigma_{\rm att})=(1,3),\qquad
(A_{\rm rep},A_{\rm att})=(1,3.5).
$$

For chirality $s\in\{-1,+1\}$, the readout is unchanged:

$$
C_s(h)=\sum_{j=0}^{H-1}a_{s,j}h_j,\qquad
\beta_s=B_H(e^{is\theta_3}),
$$

$$
B_H(z)=\sum_{j=0}^{H-1}{\alpha(1-\alpha)^j\over
1-(1-\alpha)^H}z^{-j},
$$

$$
a_{s,0}={\bar w_0-\beta_s\over1-\beta_s},\qquad
a_{s,j}={\bar w_j\over1-\beta_s}\quad(j\ge1).
$$

The complex coefficients act as real planar rotation-scale matrices. The
write gain and matched actuator mobility remain

$$
G=|a_{s,0}|^2=0.39990460811390499,\qquad \nu=G,
$$

and the coupling strength remains $k=0.25$. No coefficient, gain, mobility,
stiffness or candidate parameter may be estimated from P4-R output.

Each transition is exactly the P4 transition. First advance the unchanged
nonlinear native map to $\widetilde h$, then solve the same midpoint
discrete-gradient force $F$, add the sole history input

$$
u_h=\alpha a_{s,0}^*F,\qquad h'_0=\operatorname{fl}(\widetilde h_0+u_h),
$$

and update the external coordinate with $F_Q=-F$,

$$
v_Q=\alpha\nu F_Q,\qquad Q'=\operatorname{fl}(Q+v_Q).
$$

All older slots are the native FIFO shift. The force remains

$$
F=-{k\over2+\alpha k(G+\nu)}
\left[(C_s(h)-Q)+(C_s(\widetilde h)-Q)\right].
$$

No second difference, velocity, momentum variable, fitted tensor, explicit
mass, co-rotating feedback or target tracking may enter the update.

## 4. New holdout panel and deterministic execution order

Only the initial prepared-history phase and the single interpolation
amplitude are new:

$$
\varphi_m={(2m+1)\pi\over8},\qquad m=0,\ldots,7,
$$

$$
h^{(s,m)}_j=e^{i\varphi_m}h^{(s)}_j,\qquad
{\delta\over R_3}=1.5\times10^{-3},\qquad
Q_0=\sigma\delta e_x,\quad \sigma\in\{+1,-1\}.
$$

The amplitude is the unopened arithmetic midpoint between the old
$10^{-3}R_3$ and $2\times10^{-3}R_3$ arms. All eight phases are unopened as
dynamic target trajectories. Earlier static covariance evaluations do not
count as target access.

Every trajectory runs

$$
N=4000,\qquad \alpha N=20,
$$

stores a sample every 10 updates and accumulates all work and metrology terms
at every update. The complete panel is:

- 16 channel-off arms: $m=0,\ldots,7$, then
  $s=(+1,-1)$, with $Q_0=0$ and $k=0$;
- 32 active arms: $m=0,\ldots,7$, then $s=(+1,-1)$, then
  $\sigma=(+1,-1)$.

That nesting is the frozen execution and serialization order. The runner may
not print, serialize or expose partial target summaries. It writes the
complete result atomically only after all arms and the decision have been
evaluated.

The 32 arms are not 32 replications. Signs and chiralities are algebraic
controls. The eight phase nodes form one deterministic quadrature and contain
four mirror-related phase pairs. A half-turn also maps
$(m,\sigma)$ to $(m+4\bmod8,-\sigma)$. These relations are tested rather than
counted as independent evidence.

## 5. Cancellation-safe local identities

At each active update define the prescribed center increment before it is
added to the order-one state,

$$
d_C=\alpha G F,\qquad
\Delta C_{\rm local}=\operatorname{fl}(a_{s,0}u_h),
$$

and evaluate

$$
r_{C,\rm local}=\operatorname{fl}(\Delta C_{\rm local}-d_C),
$$

$$
r_{CQ,\rm local}=\operatorname{fl}(\Delta C_{\rm local}+v_Q).
$$

Here $v_Q$ is the prescribed small increment before its addition to $Q$, not
the cancellation-dominated difference $Q'-Q$. For each arm, freeze the
normalization at its first active update,

$$
D_0=\alpha G|F_0|>0.
$$

Both maxima must satisfy

$$
{\max_n|r_{C,\rm local,n}|\over D_0}\le5\times10^{-12},\qquad
{\max_n|r_{CQ,\rm local,n}|\over D_0}\le5\times10^{-12}.
$$

This retains the original scientific tolerance while evaluating the identity
on its resolvable scale.

## 6. Frozen full-dot forward-error envelope

The original residuals remain mandatory stored diagnostics:

$$
r_{C,\rm full}=\operatorname{fl}
\left(C_s(h')-C_s(\widetilde h)-d_C\right),
$$

$$
r_{CQ,\rm full}=\operatorname{fl}
\left(C_s(h')-C_s(\widetilde h)+(Q'-Q)\right).
$$

They are no longer divided by a sub-binary64 absolute limit. Instead set

$$
\epsilon_{64}=2^{-52},\qquad
\gamma_n={n\epsilon_{64}\over1-n\epsilon_{64}},
$$

and use $\gamma_{8H}$ for each complex dot product. For any stored history,
the implementation computes

$$
S^\uparrow(h)=\operatorname{nextafter}\!\left[
(1+\gamma_{8H})\operatorname{fsum}_{j=0}^{H-1}
\left(|a_{s,j}|\,|h_j|\right),+\infty\right].
$$

The factor and outward final step guard the nonnegative-sum evaluation; this
is a conservative IEEE-754 forward model, not an interval certificate for an
unknown vendor BLAS.

Here $\epsilon_{64}$ is deliberately NumPy's machine epsilon, twice the
usual round-to-nearest unit roundoff, so the $\gamma_n$ factors err on the
conservative side. The relative-error model is used only for normal operands
and exact zero. Any nonzero subnormal operand or result entering these
expressions invalidates the envelope and makes the run `p4r-inconclusive`.

Let $p=\widetilde h_0$ and define insertion bounds

$$
E_h=\gamma_4(|p|+|u_h|),\qquad
E_Q=\gamma_4(|Q|+|v_Q|).
$$

With the actually computed local residuals, define

$$
L_C=|r_{C,\rm local}|+
\gamma_8\left(|a_{s,0}|\,|u_h|+|d_C|\right),
$$

$$
L_{CQ}=|r_{CQ,\rm local}|+
\gamma_8\left(|a_{s,0}|\,|u_h|+|v_Q|\right).
$$

The per-step envelopes are

$$
E_C=\gamma_{8H}\left[S^\uparrow(h')+S^\uparrow(\widetilde h)\right]
+|a_{s,0}|E_h+L_C
+\gamma_8\left(|C_s(h')|+|C_s(\widetilde h)|+|d_C|\right),
$$

$$
\begin{aligned}
E_{CQ}={}&\gamma_{8H}\left[S^\uparrow(h')+S^\uparrow(\widetilde h)\right]
+|a_{s,0}|E_h+E_Q+L_{CQ}\\
&+\gamma_8\left(|C_s(h')|+|C_s(\widetilde h)|+|Q'|+|Q|\right).
\end{aligned}
$$

The implementation applies one final `nextafter(..., +inf)` to each positive
envelope. Every step must satisfy

$$
|r_{C,\rm full}|\le E_C,\qquad |r_{CQ,\rm full}|\le E_{CQ}.
$$

It stores every maximum residual, maximum envelope ratio and minimum absolute
margin. Passing this envelope means only that the old full-dot residual is
compatible with the declared rounding model. The local identities, not the
loose full-dot envelope, carry the $5\times10^{-12}$ coupling-accuracy gate.

The actuator update remains separately checked. With

$$
r_{Q,\rm full}=\operatorname{fl}(Q'-Q-v_Q),
$$

require both

$$
{\max_n|r_{Q,\rm full,n}|\over D_0}\le5\times10^{-12}
$$

and

$$
|r_{Q,\rm full}|\le
\operatorname{nextafter}\!\left[
E_Q+\gamma_8(|Q'|+|Q|+|v_Q|),+\infty\right]
$$

at every step.

At updates 1, 2000 and 4000 of every active arm, the runner also recomputes
both full residuals independently with `mpmath` at 80 decimal digits.
Every binary64 real and imaginary operand is transferred exactly through its
`float.as_integer_ratio()`; decimal string conversion is forbidden. The
high-precision calculation uses the stored $h'$, $\widetilde h$, $Q'$, $Q$,
$d_C$ and coefficients, so insertion rounding remains part of the quantity
rather than being silently removed.

At those checkpoints the high-precision residual must lie inside the same
$E_C$ or $E_{CQ}$ envelope. In addition, its distance from the binary64
residual must not exceed the corresponding dot-and-final-evaluation portion

$$
E_C^{\rm eval}=\gamma_{8H}\left[S^\uparrow(h')+
S^\uparrow(\widetilde h)\right]
+\gamma_8\left(|C_s(h')|+|C_s(\widetilde h)|+|d_C|\right),
$$

$$
E_{CQ}^{\rm eval}=\gamma_{8H}\left[S^\uparrow(h')+
S^\uparrow(\widetilde h)\right]
+\gamma_8\left(|C_s(h')|+|C_s(\widetilde h)|+|Q'|+|Q|\right).
$$

All reference residuals, margins, precision and `mpmath` version are
stored. This is an independent arithmetic replay of selected target states,
not a second trajectory and not an interval proof.

## 7. Exact ledger and inherited per-arm gates

The P4 work definitions and every non-orthogonal loop/ledger threshold are
unchanged. With initial interaction energy $U_0=k\delta^2/2$ and first-step
force scale $|F_0|$, every active arm must satisfy:

1. maximum per-step write/age split and total interaction-ledger residual,
   each divided by $U_0$, at most $5\times10^{-11}$;
2. absolute cumulative split and total residual, each divided by $U_0$, at
   most $5\times10^{-9}$;
3. force-balance and midpoint-force residual, each divided by $|F_0|$, at
   most $5\times10^{-12}$;
4. both local identities, both full-dot envelopes and the actuator-update
   gates in Sections 5--6 pass at every update;
5. neither write nor actuator mobility dissipation falls below `-1e-30`;
6. maximum own-chirality quotient distance at most $0.01R_3$;
7. every stored sample over memory times 18--20, including the final sample,
   has own-chirality D0 at most $0.002R_3$ and opposite-chirality D0 at least
   $0.5R_3$;
8. final separation $|C_s-Q|/\delta\le0.10$;
9. final baseline-corrected center and actuator projections along the signed
   laboratory input each lie in $[0.20,0.80]$ after division by $\delta$;
10. final interaction energy is at most `0.01` of $U_0$;
11. late mean phase-increment error at most $0.01\theta_3$ and RMS error at
    most $0.05\theta_3$ over memory times 15--20;
12. maximum baseline-corrected center response at least $0.25\delta$;
13. every stored value is finite and the arm reaches update 4000.

Raw-$c_H$ work and a ledger with the finite-history age term removed remain
reported rivals and cannot rescue a gate. The deterministic $H=17$ static
control must still show at least a one-percent error when age work is dropped.
Coefficient, notch, conjugacy, virtual-work, wrong-chirality, translation,
proper-rotation and reflection construction controls retain their P4
thresholds. Every phase-specific channel-off arm must be bitwise native, stay
within $10^{-10}R_3$ in D0 and keep $|C_s|/R_3\le10^{-10}$.

The old per-arm orthogonal bound of `0.05` is deliberately not reused as a
pass condition: it is the P4 criterion that the discovery panel falsified.
It is replaced prospectively by the scalar/chiral classifier below. P4-R-phi
uses only one new amplitude, so it makes no new amplitude-collapse or scaling
claim. The old three-amplitude collapse remains historical P4 discovery
evidence, not a P4-R holdout gate.

## 8. Response construction and symmetry controls

For each phase and chirality, subtract the matching channel-off trace:

$$
C^{\rm resp}_{s,m,\sigma}(t)
=C_{s,m,\sigma}(t)-C^{\rm off}_{s,m}(t),
$$

$$
Q^{\rm resp}_{s,m,\sigma}(t)
=Q_{s,m,\sigma}(t)-Q^{\rm off}_{s,m}(t).
$$

Define sign-odd and sign-even traces

$$
C^{\rm odd}_{s,m}={C^{\rm resp}_{s,m,+}-C^{\rm resp}_{s,m,-}
\over2\delta},\qquad
C^{\rm even}_{s,m}={C^{\rm resp}_{s,m,+}+C^{\rm resp}_{s,m,-}
\over2\delta},
$$

and analogously for $Q$. For both center and actuator and for every $(s,m)$,
the full-trace even-to-odd RMS ratio must not exceed `0.02`. An unresolved odd
RMS makes the panel inconclusive rather than allowing division by a numerical
floor.

The active mirror map is

$$
(s,m,\sigma)\longleftrightarrow(-s,7-m,\sigma),
$$

with complex conjugation of center and actuator traces. The half-turn map is

$$
(s,m,\sigma)\longleftrightarrow
(s,m+4\bmod8,-\sigma),
$$

with multiplication of both traces by $-1$. Every stored center and actuator
sample in both controls must agree within $10^{-11}R_3$. These are covariance
checks and do not add replications.

At the final registered sample define

$$
A_{C,s,m}=\operatorname{Re}C^{\rm odd}_{s,m},\qquad
B_{C,s,m}=-s\operatorname{Im}C^{\rm odd}_{s,m},
$$

and analogously $A_Q,B_Q$. Then

$$
B^{\rm pair}_{C,m}={1\over2}\sum_{s\in\{-1,+1\}}B_{C,s,m},\qquad
B^{\rm pair}_{Q,m}={1\over2}\sum_{s\in\{-1,+1\}}B_{Q,s,m},
$$

$$
\overline B_C={1\over8}\sum_{m=0}^7B^{\rm pair}_{C,m},\qquad
\overline B_Q={1\over8}\sum_{m=0}^7B^{\rm pair}_{Q,m}.
$$

The phase nodes are quadrature nodes, not statistical replications. Because
of reflection, they form four symmetry-related pairs. The sign-support gate
requires $B^{\rm pair}_{C,m}>0$ in at least six of eight nodes and separately
$B^{\rm pair}_{Q,m}>0$ in at least six of eight nodes. Subject to the mirror
gate this is at least three of four distinct phase pairs. No binomial
significance or confidence interval is claimed.

This eight-point rule can alias phase harmonics of order $8,16,\ldots$. A
positive result therefore supports only the registered discrete phase
average, not a continuous phase integral or pointwise phase independence.

## 9. Frozen response regions and decision precedence

The scalar null region inherits the old straight-response boundary:

$$
|\overline B_C|\le0.05,\qquad |\overline B_Q|\le0.05.
$$

The discovery-informed chiral alternative is

$$
\overline B_C\ge0.10,\qquad \overline B_Q\ge0.10,
$$

together with both six-of-eight sign-support gates. The `0.10` floor was
frozen before target access near the midpoint between the old `0.05` null
boundary and the smallest historical P4 transverse coefficient `0.151637`.

Decision precedence is exact:

1. provenance, registration, construction, completeness, finiteness,
   normal-number validity or channel-off failure yields
   **`p4r-inconclusive`**;
2. failure of a local identity, full-dot envelope, actuator update, force
   balance, midpoint force, work split, total ledger or mobility sign yields
   **`p4r-ledger-or-metrology-fail`**;
3. if ledger and metrology pass, symmetry, odd-signal, loop, phase or
   non-orthogonal response failure yields **`p4r-inconclusive`**;
4. if the valid panel lies in both scalar null regions, return
   **`p4r-phase-averaged-scalar-response`**; this falsifies the registered
   chiral route;
5. if the valid panel lies in both positive chiral regions and both support
   gates pass, return **`p4r-phase-averaged-chiral-response-pass`**;
6. if either resolved mean is at most `-0.10`, or if both means have magnitude
   at least `0.10` with opposite signs, return
   **`p4r-phase-averaged-chiral-hypothesis-fail`**;
7. every mixed scalar/chiral case, every value with
   $0.05<|\overline B|<0.10$, or a failed sign-support count with otherwise
   valid dynamics yields **`p4r-inconclusive`**.

No branch changes the historical P4 decision. Only a separately reviewed
`p4r-phase-averaged-chiral-response-pass` may authorize writing a new P4-R-S
protocol. No result authorizes P5, mass, spin, momentum or interaction.

## 10. Required implementation, artifacts and pre-target tests

The planned executable is

```text
experiments/current/dynamics/rotation/scalar_memory_loop_p4r_phase_metrology_gate.py
```

and the only default target outputs are

```text
reports/dynamics/rotation/scalar_memory_loop_p4r_phase_metrology_2026-08-26.json
reports/dynamics/rotation/scalar_memory_loop_p4r_phase_metrology_2026-08-26.md
```

The reusable source/write implementation may be extended only to expose the
pre-addition increments, local residuals, weighted sums and forward envelopes
defined here. The native map, state update, force, coefficients and port
parameters may not change.

Before any registered arm is advanced, a separate clean pushed implementation
commit must pass:

1. exact protocol and dependency-blob verification;
2. exact 16-control/32-active registration and arm-order tests;
3. phase-grid, conjugate-pair and half-turn mapping tests;
4. decision-table tests covering every named outcome and precedence branch;
5. synthetic small-$H$ tests for local identities, insertion bounds, full-dot
   envelopes, exact-ratio 80-digit checkpoint replay and deliberately
   corrupted residual rejection;
6. existing source/write, rotating-wave and Markdown-math tests;
7. the full test suite, exact CI Ruff scope and strict MkDocs build.

Pre-target tests may use static construction values and synthetic histories,
but they may not call a registered P4-R active or channel-off trajectory. The
implementation revision, test count and clean tree must be pushed before the
target runner is invoked. The runner must refuse to overwrite an existing
default target artifact.

The first result is committed and pushed unchanged before any critical review
or status edit. A separate gate-specific review must audit at least protocol
timing, dependency and implementation blobs, arm completeness, phase
redundancy, local versus full-dot metrology, envelope assumptions, every
ledger term, threshold contacts, decision precedence, eight-point aliasing
and all claim boundaries.

## 11. Publication-source referee audit

Because this repository may itself be cited as a scientific source, the
gate-specific P4-R review is necessary but not sufficient. Before P4-R-S or
any paper-level promotion, a separately scoped referee/source-readiness audit
must examine the full P0--P4-R evidence chain rather than only the latest
result. Its charter must be frozen before the P4-R target is opened and must
require at least:

1. claim-to-protocol-to-JSON-to-code traceability with immutable Git links;
2. reproduction from a clean checkout using a recorded environment;
3. independent recomputation of decisive summaries from raw JSON;
4. algebraic review of the finite-$H$ readout, adjoint port and complete work
   ledger;
5. adversarial review of numerical conditioning, binary64 envelopes and the
   conditional interval/Krawczyk trust base;
6. an explicit ledger of discovery, preregistered holdout, post hoc inference
   and negative result for every promoted statement;
7. alternative explanations, dependence among symmetry-related arms,
   eight-point phase aliasing and remaining external-validity gaps;
8. repository citation stability, licenses, environment files and permanent
   artifact hashes.

That audit is not allowed to retune P4-R or convert a fail into a pass. It may
return source-ready, source-ready-with-major-claim-restrictions or
not-source-ready. Only its first two outcomes, together with a reviewed P4-R
chiral pass, may leave P4-R-S prospectively open. P5 remains closed in every
case until the later scientific gates themselves pass.
