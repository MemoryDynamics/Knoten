# Prospective P4-R-S gate: Anchor-scale transfer of the discrete loop response

Date: 2026-08-30.

Status: **frozen prospectively after the separately committed and CI-green
P4-R-S design audit, and before any registered Anchor source/write trajectory
is constructed or advanced.** At protocol writing, the planned runner,
target test module, result JSON and result report do not exist. Static
Anchor formulas and immutable historical L3 output may be inspected; no
registered Anchor arm may be evaluated before the implementation freeze and
review defined below.

## 1. Question, historical decisions and claim boundary

The immutable historical decisions are

```text
P4   = p4-source-write-architecture-fail
P4-R = p4r-phase-averaged-chiral-response-pass
```

P4-R-S changes neither decision. It asks one new question:

> Does the same explicitly declared source/write rule, evaluated on the
> already certified and numerically stable Anchor at matched dimensionless
> memory time, close all inherited gates, remain in the registered chiral
> response region and agree with the complete L3 response within the frozen
> cross-scale effect-size limits?

The L3 response is evidence and a fixed comparator. Scale transfer is the
hypothesis. A successful Anchor result would be a deterministic second-cell
holdout on one matched ladder, not an independent replication or a theorem
for a continuum family.

Even a later reviewed full pass would establish neither a physical actuator
nor continuous phase invariance, all-$\alpha$ convergence, momentum,
intrinsic spin, inertia, a material center of mass or physical mass. It could
open only prospective P5 protocol writing. It is not P5 evidence.

## 2. Frozen timing and provenance

The design audit was committed and pushed as

```text
11cabd66d0ba086116b29b3ea3d8a8548560cea1
```

with Git blob

```text
dec2f0c281f19fadc02412b04a78f78f0793422a
```

and passed
[GitHub Actions run 33320927753](https://github.com/MemoryDynamics/Knoten/actions/runs/33320927753).
The green source-audit mainline base is

```text
ecdaa8522337880aa1504af8c66924be96e0a9db
```

The later runner must verify these exact Git objects before target access:

| dependency | frozen Git blob |
| --- | --- |
| P4-R-S design audit | `dec2f0c281f19fadc02412b04a78f78f0793422a` |
| immutable P4-R JSON | `2a668a4c70820bceb0ff84fa1932878d9130aabf` |
| P4-R critical review | `1d25e9db083d91fdfd521f44e0951a1ddd9e2c37` |
| P4-R protocol | `b81fa535c1921c2f11f83e5585bf38b05e0a08d5` |
| historical P4-R runner | `27a3a40dde60b797b58da576b5849ab10b47079f` |
| source/write implementation | `63d31bc47291f76c65a5633f14436ccd2105fe9a` |
| native nonlinear FIFO map | `9defb5a6876371202e1ba57cea030c997b9c6edd` |
| rotating-wave candidate definition | `630beb9952abefea823d91388dcbb2de8f1a2927` |
| rotating-wave formation/phase utilities | `38f16f11a790a64470bab3a34505825cf815e7f0` |
| Anchor interval result | `fc6e816c6895e408693fbde176afdaee963c20b9` |
| Anchor native stability result | `1c9d5746c9553d9cb8031b58258e6d613f1633d9` |
| historical P4 JSON | `41ddfb5ec2d4c907607995523775072ad12544f7` |
| publication-source report | `273acc3a86a9f3757e853236ce386f064835194c` |
| publication-source findings | `9cf16689a3b8931842e6ef500f555212ac8f5b36` |

The canonical-LF SHA-256 values are

```text
P4-R JSON          807cf915d1602d87a779e7bf587387559b1b19d7de60dc43c6e1e220b73682c8
P4 JSON            ea0651e206451e5f87ec08ab3f66ec68df2c04bee2d1b9d67219736058a275cc
Anchor interval    63dc4158c0d8a9543230b656b7602feef76a48a2a75fbe6a6e001cb81082a840
Anchor stability   43b0d7f5e5ba81dc35d4a2e9d138d3663a3d98b67bcb09ed2d4572d5a01eb86f
```

The commit containing this protocol becomes the protocol-freeze revision.
The future result must record that revision, the later clean pushed
implementation revision, every dependency and implementation blob,
Python/NumPy/mpmath/platform/BLAS versions and an initially clean worktree.

Before advancing an arm, the runner must additionally require:

1. the design commit and protocol commit are ancestors of the execution
   revision;
2. the execution revision is exactly synchronized with its remote branch;
3. the default target JSON and report do not exist;
4. the P4-R JSON has the frozen hash, complete raw panel and stored decision;
5. the P4 JSON still stores its historical fail;
6. the Anchor interval and stability files retain their frozen decisions;
7. the source verdict remains
   `referee-source-ready-with-major-claim-restrictions` and explicitly keeps
   P5 closed before a reviewed P4-R-S full pass.

Missing provenance, a dirty or unpushed tree, pre-existing target output or a
changed dependency is **`p4rs-inconclusive`**, never a response result.

## 3. Frozen Anchor target and L3 reference

The Anchor target is exactly

```text
candidate_id = k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1
R_A = 0.946517504804223960990626662735384935160072399313332184824852189820406142783597632634323623097735558253263801
theta_A = 0.0157703817171349919012689641413413231316321140980062507765923663663284306507309780740587352166842324150748019
alpha_A = 0.01
H_A = 1200
eta_A = 0.15
```

and the L3 reference remains

```text
candidate_id = k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1
R_L3 = 0.944805811705743656419366118422595657454474452804188781825799206245348464567689511866917417017911971955244464
theta_L3 = 0.00790666146243552374938496703030974246197803459527409259815696583141708245813094145986593003659167675765833059
alpha_L3 = 0.005
H_L3 = 2400
eta_L3 = 0.075
```

Both have

$$
d=2,\quad\varepsilon=0,\quad M_0=1,
$$

$$
(\sigma_{\rm rep},\sigma_{\rm att})=(1,3),\qquad
(A_{\rm rep},A_{\rm att})=(1,3.5),
$$

$$
H\alpha=12,\qquad\eta/\alpha=15.
$$

The exact decimals are parsed once to binary64 and both forms are serialized.
The runner must verify that the exact Anchor decimals lie in the stored
certified intersection and agree with the 120-digit refined root. It must not
silently substitute the shorter stability-file display values.

## 4. Frozen notch, adjoint and first-order port

For each candidate let $q=1-\alpha$ and

$$
\bar w_j={\alpha q^j\over1-q^H},\qquad
B_H(z)=\sum_{j=0}^{H-1}\bar w_jz^{-j}.
$$

For chirality $s\in\{-1,+1\}$,

$$
\beta_s=B_H(e^{is\theta}),\qquad
C_s(h)=\sum_{j=0}^{H-1}a_{s,j}h_j,
$$

$$
a_{s,0}={\bar w_0-\beta_s\over1-\beta_s},\qquad
a_{s,j}={\bar w_j\over1-\beta_s}\quad(j\ge1).
$$

The coefficients act as real planar rotation-scale matrices and their real
adjoint is represented by complex conjugation. The write gain and actuator
mobility are rebuilt from the target candidate:

$$
G_s=|a_{s,0}|^2,\qquad\nu_s=G_s>0.
$$

Static pre-target values for the Anchor are frozen as

```text
beta_(s=+1) = 0.2923957083606503 - 0.45093731944942195 i
a0_(s=+1)   = 0.004999787409710969 + 0.6340870653534046 i
G = nu       = 0.4020914043226352
```

with complex conjugates for $s=-1$. The L3 value
`0.39990460811390555` may not be copied into the Anchor.

The coupling remains $k=0.25$. Each transition first advances the unchanged
native map to $\widetilde h$, then uses

$$
F=-{k\over2+\alpha k(G+\nu)}
\left[(C_s(h)-Q)+(C_s(\widetilde h)-Q)\right],
$$

$$
u_h=\alpha a_{s,0}^*F,\qquad
h'_0=\operatorname{fl}(\widetilde h_0+u_h),
$$

$$
v_Q=-\alpha\nu F,\qquad
Q'=\operatorname{fl}(Q+v_Q).
$$

All older history slots are the native FIFO shift. No velocity, momentum,
mass, second difference, fitted response tensor, co-rotating controller or
target tracking may enter the update.

## 5. Matched memory-time panel and arm order

The only Anchor target panel is

$$
\varphi_m={(2m+1)\pi\over8},\qquad m=0,\ldots,7,
$$

$$
h_j^{(s,m)}=e^{i\varphi_m}h_j^{(s)},\qquad
{\delta_A\over R_A}=1.5\times10^{-3},
$$

$$
Q_0=\sigma\delta_Ae_x,\qquad\sigma\in\{+1,-1\}.
$$

The executable binary64 offset is `0.0014197762572063359`. It must be
computed from the frozen fraction and parsed Anchor radius, not inserted as a
free parameter.

Every active trajectory runs

$$
N_A=2000,\qquad\alpha_A N_A=20,
$$

stores updates `0,5,10,...,2000`, and accumulates all work and metrology at
every update. This yields the same 401-point memory-time grid
$\tau=0,0.05,\ldots,20$ as the immutable L3 traces at updates
`0,10,20,...,4000`.

The exact execution and serialization order is:

1. 16 channel-off arms, nested by `phase_index=0..7`,
   `chirality=(+1,-1)`, with $Q_0=0$ and $k=0$;
2. 32 active arms, nested by `phase_index=0..7`,
   `chirality=(+1,-1)`, `offset_sign=(+1,-1)`.

The runner may not print, serialize or expose partial target summaries. It
writes the complete JSON atomically only after all arms and the decision are
known. Signs, chiralities and phase symmetries are controls, not replications.

## 6. Cancellation-safe local metrology

At each active update define

$$
d_C=\alpha GF,\qquad
\Delta C_{\rm local}=\operatorname{fl}(a_{s,0}u_h),
$$

$$
r_{C,{\rm local}}=\operatorname{fl}(\Delta C_{\rm local}-d_C),
\qquad
r_{CQ,{\rm local}}=\operatorname{fl}(\Delta C_{\rm local}+v_Q).
$$

Freeze the arm normalization at its first active update,

$$
D_0=\alpha G|F_0|>0.
$$

Require

$$
{\max_n|r_{C,{\rm local},n}|\over D_0}\le5\times10^{-12},
\qquad
{\max_n|r_{CQ,{\rm local},n}|\over D_0}\le5\times10^{-12}.
$$

The actuator full residual

$$
r_{Q,{\rm full}}=\operatorname{fl}(Q'-Q-v_Q)
$$

must obey the same `5e-12` relative displacement threshold and the forward
envelope below.

## 7. Full-dot binary64 envelopes and high precision

The cancellation-dominated diagnostics remain stored:

$$
r_{C,{\rm full}}=\operatorname{fl}
\left(C_s(h')-C_s(\widetilde h)-d_C\right),
$$

$$
r_{CQ,{\rm full}}=\operatorname{fl}
\left(C_s(h')-C_s(\widetilde h)+(Q'-Q)\right).
$$

Set

$$
\epsilon_{64}=2^{-52},\qquad
\gamma_n={n\epsilon_{64}\over1-n\epsilon_{64}},
$$

and use the Anchor value $\gamma_{8H_A}$. For a stored history define

$$
S^\uparrow(h)=\operatorname{nextafter}\!\left[
(1+\gamma_{8H_A})\operatorname{fsum}_j(|a_{s,j}|\,|h_j|),
+\infty\right].
$$

With $p=\widetilde h_0$,

$$
E_h=\gamma_4(|p|+|u_h|),\qquad
E_Q=\gamma_4(|Q|+|v_Q|),
$$

$$
L_C=|r_{C,{\rm local}}|
+\gamma_8(|a_{s,0}|\,|u_h|+|d_C|),
$$

$$
L_{CQ}=|r_{CQ,{\rm local}}|
+\gamma_8(|a_{s,0}|\,|u_h|+|v_Q|).
$$

The per-step envelopes are

$$
\begin{aligned}
E_C={}&\gamma_{8H_A}[S^\uparrow(h')+S^\uparrow(\widetilde h)]
+|a_{s,0}|E_h+L_C\\
&+\gamma_8(|C_s(h')|+|C_s(\widetilde h)|+|d_C|),
\end{aligned}
$$

$$
\begin{aligned}
E_{CQ}={}&\gamma_{8H_A}[S^\uparrow(h')+S^\uparrow(\widetilde h)]
+|a_{s,0}|E_h+E_Q+L_{CQ}\\
&+\gamma_8(|C_s(h')|+|C_s(\widetilde h)|+|Q'|+|Q|),
\end{aligned}
$$

and

$$
E_Q^{\rm full}=E_Q+\gamma_8(|Q'|+|Q|+|v_Q|).
$$

One final `nextafter(...,+inf)` is applied to each positive envelope. Every
step must satisfy

$$
|r_{C,{\rm full}}|\le E_C,\qquad
|r_{CQ,{\rm full}}|\le E_{CQ},\qquad
|r_{Q,{\rm full}}|\le E_Q^{\rm full}.
$$

Nonzero subnormal operands or results invalidate this relative-error model
and make the panel `p4rs-inconclusive`.

At Anchor updates `1,1000,2000` of every active arm, both center full
residuals are recomputed with `mpmath` at 80 decimal digits. Every binary64
operand is transferred through `float.as_integer_ratio()`; decimal string
conversion is forbidden. The high-precision residuals must lie inside the
same envelopes, and their distances from the binary64 residuals must lie
inside

$$
E_C^{\rm eval}=\gamma_{8H_A}[S^\uparrow(h')+S^\uparrow(\widetilde h)]
+\gamma_8(|C_s(h')|+|C_s(\widetilde h)|+|d_C|),
$$

$$
E_{CQ}^{\rm eval}=\gamma_{8H_A}[S^\uparrow(h')+S^\uparrow(\widetilde h)]
+\gamma_8(|C_s(h')|+|C_s(\widetilde h)|+|Q'|+|Q|).
$$

All 96 references,
margins, precision and `mpmath` version are stored.

This is an arithmetic replay of stored states, not a second trajectory or an
interval certificate.

## 8. Exact work ledger and inherited per-arm gates

Let

$$
U_0={k\delta_A^2\over2}.
$$

Every active Anchor arm must satisfy:

| gate | frozen limit |
| --- | ---: |
| maximum per-step write/age split residual divided by $U_0$ | `5e-11` |
| maximum per-step total interaction-ledger residual divided by $U_0$ | `5e-11` |
| absolute cumulative split residual divided by $U_0$ | `5e-9` |
| absolute cumulative total residual divided by $U_0$ | `5e-9` |
| force-balance and midpoint-force residual divided by $|F_0|$ | `5e-12` |
| minimum write or actuator mobility dissipation | `-1e-30` |
| maximum own-chirality quotient distance | `0.01 R_A` |
| late own-chirality D0, every stored sample at $18\le\tau\le20$ | `0.002 R_A` |
| late opposite-chirality D0 | at least `0.5 R_A` |
| final separation divided by $\delta_A$ | `0.10` |
| final signed longitudinal center and actuator projection divided by $\delta_A$ | each in `[0.20,0.80]` |
| final interaction-energy ratio | `0.01` |
| late mean phase-increment error, $15\le\tau\le20$ | `0.01 theta_A` |
| late RMS phase-increment error | `0.05 theta_A` |
| maximum baseline-corrected center response | at least `0.25 delta_A` |
| active-arm completion | update `2000` |

The exact finite-history write/age/interaction ledger, force balance,
midpoint force and both positive first-order mobility dissipations are
decisive. The raw-memory-center ledger and the ledger with age work removed
remain nondecisional rivals and cannot rescue a gate. The deterministic
$H=17$ static control must still show at least one-percent error when age
work is omitted.

All coefficient, notch, conjugacy, virtual-work, wrong-chirality,
translation, proper-rotation and reflection controls inherit their P4-R
limits. Every channel-off arm must be bitwise native, satisfy
$D_0/R_A\le10^{-10}$ and $|C_s|/R_A\le10^{-10}$.

## 9. Anchor response and symmetry controls

For each phase and chirality subtract the matching channel-off trace and form

$$
X^{\rm odd}_{A,s,m}(\tau)=
{X^{\rm resp}_{A,s,m,+}(\tau)-X^{\rm resp}_{A,s,m,-}(\tau)
\over2\delta_A},
$$

$$
X^{\rm even}_{A,s,m}(\tau)=
{X^{\rm resp}_{A,s,m,+}(\tau)+X^{\rm resp}_{A,s,m,-}(\tau)
\over2\delta_A},
$$

for $X\in\{C,Q\}$. Every full-trace even-to-odd RMS ratio must be at most
`0.02`; unresolved odd RMS is inconclusive.

The exact covariance maps remain

$$
(s,m,\sigma)\leftrightarrow(-s,7-m,\sigma)
$$

with complex conjugation and

$$
(s,m,\sigma)\leftrightarrow(s,m+4\bmod8,-\sigma)
$$

with multiplication by $-1$. Every stored center and actuator sample must
agree within `1e-11 R_A`.

At the final sample define

$$
A_{X,A,s,m}=\operatorname{Re}X^{\rm odd}_{A,s,m},\qquad
B_{X,A,s,m}=-s\operatorname{Im}X^{\rm odd}_{A,s,m}.
$$

Pair chiralities at each phase and then average the eight phases. The Anchor
scalar region is

$$
|\overline B_{C,A}|,|\overline B_{Q,A}|\le0.05.
$$

The positive chiral region is

$$
\overline B_{C,A},\overline B_{Q,A}\ge0.10
$$

with strictly positive paired values in at least six of eight nodes for each
observable. The support count is deterministic, not a binomial statistic.

Values in the gap, mixed scalar/chiral classifications or insufficient
support are inconclusive. A resolved mean at or below `-0.10`, or two resolved
center/actuator means of magnitude at least `0.10` with opposite signs, is a
directional falsification.

## 10. Immutable L3 reconstruction and time matching

The runner must reconstruct the L3 reference from all 16 channel-off and 32
active raw P4-R arm records. It may not use rounded Markdown values or rerun
the L3 trajectory. It must verify:

1. exact arm keys, order, count and 401 samples per trace;
2. steps `0,10,...,4000` and complete finite records;
3. the same phase, chirality and sign registration;
4. the P4-R stored result and gate-review decisions;
5. raw reconstruction of phase values and means agrees with stored P4-R
   summaries within `5e-15` absolute, a numerical consistency check rather
   than a scientific tolerance.

The L3 final comparator means are frozen as

```text
A_C = 0.24091330892887405
B_C = 0.208421577193625
A_Q = 0.303296080377988
B_Q = 0.15375308546516817
```

For stored index $k=0,\ldots,400$, match

$$
n_A=5k,\qquad n_{L3}=10k,\qquad
\tau_k=0.05k.
$$

No interpolation is permitted or needed.

## 11. Frozen cross-scale response estimands

For both scales form chirality-aligned time-dependent components

$$
A_{X,r,s,m}(\tau_k)=\operatorname{Re}X^{\rm odd}_{r,s,m}(\tau_k),
\qquad
B_{X,r,s,m}(\tau_k)=-s\operatorname{Im}X^{\rm odd}_{r,s,m}(\tau_k).
$$

The sole scientific scale tolerance is

```text
epsilon_scale = 0.05
```

inherited from the pre-Anchor scalar-null effect-size boundary. It was not
chosen from an Anchor preview or from an observed L3-to-Anchor difference.

### 11.1 Complete transient

For $X\in\{C,Q\}$ and $Y\in\{A,B\}$ require

$$
D_{X,Y}^{\rm trace}=
\left[{1\over16\cdot401}\sum_{s,m,k}
(Y_{X,A,s,m}(\tau_k)-Y_{X,L3,s,m}(\tau_k))^2
\right]^{1/2}\le0.05.
$$

These are four componentwise gates. A combined complex RMS is reported only
as a diagnostic and cannot replace them.

### 11.2 Final phase profile

At $\tau=20$, pair the two chiralities at each phase. For
$Y\in\{A_C,B_C,A_Q,B_Q\}$ require

$$
D_Y^{\rm profile}=
\left[{1\over8}\sum_{m=0}^7
(Y_{A,m}^{\rm pair}-Y_{L3,m}^{\rm pair})^2
\right]^{1/2}\le0.05.
$$

### 11.3 Final means

Require

$$
|\overline Y_A-\overline Y_{L3}|\le0.05
$$

for the same four components. These mean limits are implied by the profile
RMS limits and are retained as explicit interpretive checks, not counted as
independent evidence. Signed differences and ratios are stored but are
nondecisional.

The transient gate prevents one final match from hiding a different response
history. The profile gate prevents a phase-local mismatch from being diluted
across time. The two tested scales cannot identify a convergence order.

## 12. Exact decision precedence

The result labels are applied in this order:

1. provenance, registration, construction, completeness, finiteness,
   normal-number validity, L3 reconstruction, common-grid or channel-off
   failure returns **`p4rs-inconclusive`**;
2. local source/write, full-dot envelope, actuator update, force, midpoint
   force, work split, total ledger or mobility-sign failure returns
   **`p4rs-ledger-or-metrology-fail`**;
3. symmetry, odd-signal, loop, phase or inherited non-orthogonal response
   failure returns **`p4rs-inconclusive`**;
4. a valid Anchor panel in both scalar regions returns
   **`p4rs-anchor-scalar-response`**;
5. a valid resolved Anchor panel with a mean at or below `-0.10`, or with
   resolved center/actuator means of magnitude at least `0.10` and opposite
   signs, returns **`p4rs-anchor-chiral-hypothesis-fail`**;
6. a valid positive-chiral Anchor panel that fails any trace, profile or mean
   scale limit returns **`p4rs-cross-scale-mismatch`**;
7. only a valid positive-chiral Anchor panel with every inherited and
   cross-scale gate true returns
   **`p4rs-anchor-scale-transfer-pass`**;
8. every gap, mixed or insufficient-support case returns
   **`p4rs-inconclusive`**.

The scalar, directional and cross-scale-mismatch labels falsify different
parts of the registered transfer hypothesis. None opens P5. Only a later
separately reviewed full pass may open P5 **protocol writing**.

## 13. Planned implementation and pre-target tests

The only planned new implementation paths are

```text
experiments/current/dynamics/rotation/scalar_memory_loop_p4rs_anchor_scale_gate.py
tests/test_rotating_wave_p4rs_anchor_scale.py
```

The immutable P4-R runner, native map and source/write module may not change
during implementation. The new runner may call their pure functions and
locally orchestrate the frozen equations, metrology and reconstruction. It
may not mutate imported P4-R module globals, add a target-dependent
coefficient or introduce an alternative update.

The only default target outputs are

```text
reports/dynamics/rotation/scalar_memory_loop_p4rs_anchor_scale_2026-08-30.json
reports/dynamics/rotation/scalar_memory_loop_p4rs_anchor_scale_2026-08-30.md
```

Before any registered Anchor arm is advanced, a clean pushed implementation
commit must pass:

1. exact protocol, design, historical result and dependency-blob checks;
2. proof that the default target outputs are absent and overwrite refusal is
   active;
3. exact Anchor decimal, interval-membership, $H\alpha$, $\eta/\alpha$,
   $B_H$, $a_0$, conjugacy and $G=\nu$ tests;
4. exact 16-control/32-active registration and serialization order;
5. the 2000-step, stride-5, 401-sample memory-time map and exact pairing with
   L3 steps;
6. raw L3 reconstruction of all four frozen final means;
7. synthetic identical-scale pass, transient-only mismatch,
   final-phase-local mismatch and mean-mismatch tests;
8. decision-table tests covering every named result and precedence branch;
9. synthetic small-$H$ local identities, full-dot envelopes,
   exact-ratio 80-digit replay and deliberately corrupted rejection;
10. monkeypatched guards proving no pre-target test calls a registered
    Anchor active or channel-off trajectory;
11. existing P4/P4-R/source-write/rotating-wave and Markdown-math tests;
12. the full test suite, exact CI Ruff scope and strict MkDocs build.

The implementation revision, exact test count, lint/docs results, all new
blobs and clean remote synchronization must be documented in a separate

```text
reports/project/meta/reviews/scalar_memory_loop_p4rs_anchor_scale_implementation_readiness_2026-08-30.md
```

and pushed before target execution. That review may authorize exactly one
first clean invocation or reject the implementation. It may not inspect a
target result.

## 14. Result freeze and critical review

If implementation readiness is upheld, the runner is invoked once from its
clean pushed revision. It must write both complete outputs atomically and
refuse overwrites. The first result artifacts are committed and pushed
unchanged before any status edit or scientific review.

A later result review must independently audit at least:

- protocol timing, all blobs and canonical hashes;
- Anchor exact-root selection and static gain;
- arm completeness and common-memory-time pairing;
- local versus full-dot metrology and all 96 precision checkpoints;
- every finite-history ledger term and both rivals;
- loop, phase, odd/even, mirror and half-turn margins;
- raw L3 reconstruction without rounded summaries;
- all trace, profile and mean cross-scale arrays;
- decision precedence and closest threshold contacts;
- symmetry dependence, two-cell external-validity limits and every prohibited
  interpretation.

No result may be described as reviewed until that separate commit exists and
passes CI.

## 15. Frozen falsifiers and publication boundary

P4-R-S cannot pass if:

1. target access precedes the protocol/implementation freeze and review;
2. any frozen dependency changes without a new protocol;
3. the rounded Anchor replaces the exact interval-refined root;
4. L3 gain, step count or storage stride is copied into the Anchor;
5. any phase, sign, chirality or target trace is removed after access;
6. local metrology, finite-history age work, full-dot envelopes, raw-center
   or omitted-age controls are weakened;
7. the L3 reference is rerun, rounded, filtered or interpolated;
8. the Anchor chiral classifier passes but a transient, phase-profile or mean
   scale gate fails;
9. deterministic symmetry arms are called replications;
10. a pass is interpreted as continuous phase, convergence order, physical
    work, momentum, spin, inertia, mass or P5 evidence.

A later reviewed `p4rs-anchor-scale-transfer-pass` could support only:

> The same explicit reciprocal source/write construction produces compatible
> dimensionless finite-history ledger and sign-odd response results at the
> prepared L3 and Anchor cells under the registered discrete phase and
> cross-scale gates.

The three publication-source restrictions remain: a single `mpmath.iv`
interval trust base, no complete original wheel/hash lock and no citation/
release archive. P5 remains closed until the complete P4-R-S result is both a
full pass and separately reviewed.
