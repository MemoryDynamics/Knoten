# Internal adversarial publication-source audit through P4-R-phi

Date: 2026-08-27.

Verdict: **`referee-source-ready-with-major-claim-restrictions`**.

This is an **internal adversarial source-readiness audit**, not independent
peer review. It finds no open critical defect and reproduces every decisive
P4-R scientific field exactly in two numerical environments. It also finds
three open major source restrictions:

1. all promoted Krawczyk inclusions depend on `mpmath.iv` 1.3.0;
2. no complete wheel/hash lock reconstructs the original execution stack,
   whose installation directory contains stale duplicate package metadata;
3. the repository has no `CITATION.cff`, release tag or archival release
   manifest.

These restrictions prevent an unrestricted source-ready verdict. They do not
alter the narrow P4-R decision, and none undermines the tested port equations,
finite-history ledger or discrete phase-response result. The claim-language
commit is now pushed and green, so P4-R-S may be *prospectively specified*.
P5 remains closed. No current result establishes spin, momentum,
inertia, a material center of mass or physical mass.

## 1. Immutable scope and review timing

The audit followed the prospectively frozen
[source-referee charter](https://github.com/MemoryDynamics/Knoten/blob/071c9d33c8611d0a1ef1cb3da620acb7dcdb5f7d/reports/project/meta/preregistration/p4_publication_source_referee_audit_charter_2026-08-26.md).
It began only after the unedited
[P4-R result](https://github.com/MemoryDynamics/Knoten/blob/0beaf80f713851ab74bef85a24b8323f42f38108/reports/dynamics/rotation/scalar_memory_loop_p4r_phase_metrology_2026-08-26.json)
and its separate
[gate review](https://github.com/MemoryDynamics/Knoten/blob/b2e8fff8b779ac2b1b4ef6f40be8668fe0c4e5d5/reports/project/meta/reviews/scalar_memory_loop_p4r_phase_metrology_review_2026-08-27.md)
were committed and pushed.

| object | immutable identifier |
| --- | --- |
| P4-R design | commit `0bf9b3020f26acfaf5273c1efab5dcc52d596239` |
| P4-R protocol | commit `cb863d4a88c1072637116a0296ab9fc20356a675`, blob `b81fa535c1921c2f11f83e5585bf38b05e0a08d5` |
| source-referee charter | commit `071c9d33c8611d0a1ef1cb3da620acb7dcdb5f7d`, blob `2bc9bba4c2c5f9184201987f2f97faac2c91aec5` |
| P4-R execution | revision `59dc8875cf991e3d7472db1496c9ae8ffae16ca8` |
| P4-R runner | blob `27a3a40dde60b797b58da576b5849ab10b47079f` |
| source/write implementation | blob `63d31bc47291f76c65a5633f14436ccd2105fe9a` |
| P4-R raw result | commit `0beaf80f713851ab74bef85a24b8323f42f38108`, blob `2a668a4c70820bceb0ff84fa1932878d9130aabf` |
| P4-R canonical-LF JSON SHA-256 | `807cf915d1602d87a779e7bf587387559b1b19d7de60dc43c6e1e220b73682c8` |
| P4-R gate review | commit `b2e8fff8b779ac2b1b4ef6f40be8668fe0c4e5d5`, blob `1d25e9db083d91fdfd521f44e0951a1ddd9e2c37` |
| independent auditor | commit `d60f6eec93c8cb05c4ea104b76d652a1471b6bab`, blob `3419412799e3ea29dfb5eae42e4f5e6d12e8a2ab` |

The first P4-R invocation stopped during provenance preflight: Windows CRLF
bytes were compared with a canonical-LF P4 digest. It generated no target arm,
JSON, report or partial summary. Commit
`59dc8875cf991e3d7472db1496c9ae8ffae16ca8` fixed only the line-ending
canonicalization and added a regression test before the successful target
invocation. The holdout timing is therefore intact.

The machine-readable audit companions are:

- `p4_publication_source_claim_trace_2026-08-27.json`;
- `p4_publication_source_referee_findings_2026-08-27.json`;
- `p4_publication_source_reproduction_2026-08-27.json`;
- `p4r_independent_result_recompute_2026-08-27.json`.

Historical protocols, raw results and decisions were not edited.

The final pre-commit verification passed the exact CI Ruff scope, the strict
MkDocs build and all **814** repository tests.

## 2. Verdict logic and finding counts

The frozen verdict rule allows the restricted verdict when every decision
reproduces, no critical finding remains, and declared limitations are
propagated into public wording. That condition is met.

| severity/status | count | effect |
| --- | ---: | --- |
| open critical | 0 | no decision mismatch, broken provenance or algebraic contradiction found |
| open major | 3 | blocks unrestricted source-ready wording |
| resolved/closed minor | 3 | hash convention, stale status and preflight incident documented or repaired |
| notes | 5 | scoped limitations retained |

The exact finding objects, evidence paths, commands and remediation are in the
findings JSON. Absence of a critical finding is not proof that no defect
exists.

## 3. Pass A — claim traceability

The claim trace contains 11 complete rows spanning the required chain:

1. exact finite-H circle reduction plus the numerical Anchor witness;
2. six local conditional finite-H root certificates;
3. numerical fixed-gain First-order scaling;
4. local Anchor numerical stability;
5. local L3 numerical stability;
6. ambient `SO(2)` topology and the negative internal-`S1` conclusion;
7. the strong local P2 matrix response together with its formal fail;
8. the outcome-informed P2-R long-recovery pass;
9. P3 finite-ensemble attraction;
10. P4 exact ledger together with its formal architecture fail;
11. the upheld, discrete P4-R chiral-response pass.

Every row gives allowed wording, evidence class, immutable protocol/result/
review/code links, Git blobs, a canonical-LF raw-result digest, exact scope,
excluded nearby claims and status consistency. No promoted claim contradicts
its stored decision. In particular:

- `loop-center-matrix-local-fail` remains the P2 decision;
- `p4-source-write-architecture-fail` remains the P4 decision;
- P2-R is labelled outcome-informed rather than independent;
- P3 is a finite deterministic ensemble, not an open basin;
- P4-R is one discrete quadrature, not 32 replications or a continuous phase
  integral;
- every Krawczyk existence statement is conditional on `mpmath.iv` 1.3.0.

The current README, status, priorities, report ledger, repository map and
experiment catalog are updated by the same audit change. This resolves the
otherwise minor stale-status defect without rewriting history.

## 4. Pass B — independent algebra and model semantics

### 4.1 The finite-memory transfer is a normalized geometric polynomial

Let

$$
q=1-\alpha,
\qquad
\bar w_j={\alpha q^j\over1-q^H},
\qquad j=0,\ldots,H-1.
$$

Then the finite-memory transfer is

$$
B_H(z)=\sum_{j=0}^{H-1}\bar w_jz^{-j}
={\alpha\over1-q^H}
{1-(qz^{-1})^H\over1-qz^{-1}}
$$

when $qz^{-1}\ne1$. At the removable special case $z=q$, the finite sum is
$\alpha H/(1-q^H)$. Since $1-q=\alpha$,

$$
B_H(1)=1.
$$

Thus this is indeed a finite normalized geometric series, not a fitted
transfer function. The closed form is useful analytically; the registered
code evaluates the finite sum where rounding provenance matters.

For the signed rotating history

$$
h_{j,n}=C+R\exp[i(\phi_n-sj\theta)],
\qquad s\in\{-1,+1\},
$$

define

$$
\beta_s=B_H(e^{is\theta}).
$$

Direct substitution gives

$$
c_H=C+\beta_s(x-C).
$$

This identity is decisive semantically: raw $c_H$ contains a rotating term
and is not a pure orbit center. At L3, $|\beta_s|R=0.5058810073761263$, so
discarding that term is not a small-error approximation.

### 4.2 Exact chirality-conditioned notch

Solving the preceding identity for $C$ gives

$$
C_s={c_H-\beta_sx\over1-\beta_s}
=\sum_{j=0}^{H-1}a_{s,j}h_j,
$$

with

$$
a_{s,0}={\bar w_0-\beta_s\over1-\beta_s},
\qquad
a_{s,j}={\bar w_j\over1-\beta_s}\quad(j\ge1).
$$

Equivalently,

$$
A_s(z)={B_H(z)-\beta_s\over1-\beta_s}.
$$

Therefore

$$
A_s(1)=\sum_ja_{s,j}=1,
\qquad
A_s(e^{is\theta})=0.
$$

Because the weights are real,

$$
\beta_{-s}=\beta_s^*,
\qquad
a_{-s,j}=a_{s,j}^*.
$$

The wrong-chirality notch does not remove the target rotation; its registered
remaining amplitude is `1.0117541055435313`. Chirality is consequently an
explicit model input and a falsifying construction control, not a quantity
selected from the target response.

### 4.3 Complex-to-real adjoint

For $a=a_R+ia_I$, complex multiplication corresponds to

$$
M(a)=
\begin{pmatrix}
a_R&-a_I\\
a_I&a_R
\end{pmatrix},
\qquad
M(a)^T=M(a^*).
$$

A variation of the readout obeys

$$
\delta C_s=\sum_jM(a_{s,j})\delta h_j.
$$

Hence the slot force adjoint to a generalized center force $F$ is

$$
f_j=M(a_{s,j})^TF=a_{s,j}^*F
$$

in complex notation. It satisfies both

$$
\sum_j f_j\mathbin{\cdot}\delta h_j=F\mathbin{\cdot}\delta C_s
$$

and, because $\sum_ja_{s,j}=1$,

$$
\sum_jf_j=F.
$$

These are exact linear-algebra identities. They do not establish that the
slots are autonomous material carriers.

### 4.4 First-order source/write step and midpoint force

After the unchanged nonlinear native map produces $\widetilde h$, the only
active history input is

$$
u_h=\alpha a_{s,0}^*F,
\qquad
h'_0=\operatorname{fl}(\widetilde h_0+u_h).
$$

The actuator increment is

$$
v_Q=\alpha\nu F_Q,
\qquad
F_Q=-F,
\qquad
\nu=G=|a_{s,0}|^2>0.
$$

With

$$
U(C_s,Q)={k\over2}|C_s-Q|^2,
$$

the midpoint discrete-gradient force obeys

$$
F=-{k\over2}\left[(C'_s-Q')+(C_s-Q)\right].
$$

Since $C'_s=\widetilde C'_s+\alpha GF$ and
$Q'=Q-\alpha\nu F$, rearrangement gives the unique closed form

$$
F=-{k\over2+\alpha k(G+\nu)}
\left[(C_s-Q)+(\widetilde C'_s-Q)\right].
$$

There is no nonlinear solve, velocity, second difference, momentum state or
mass coefficient in this update. Positive $G$ and $\nu$ are first-order
mobilities. Calling either sign a positive or negative *mass* would be a
category error; no inertial constitutive law has been identified here.

### 4.5 Complete finite-history work ledger

FIFO ageing gives $h'_j=h_{j-1}$ for $j\ge1$. Therefore

$$
F\mathbin{\cdot}(C'_s-C_s)
=f_0\mathbin{\cdot}(h'_0-h_0)
+\sum_{j=1}^{H-1}f_j\mathbin{\cdot}(h_{j-1}-h_j).
$$

Define

$$
W_{\rm write}=f_0\mathbin{\cdot}(h'_0-h_0),
$$

$$
W_{\rm age}=\sum_{j=1}^{H-1}
f_j\mathbin{\cdot}(h_{j-1}-h_j),
$$

and

$$
W_Q=F_Q\mathbin{\cdot}(Q'-Q).
$$

For $r=C_s-Q$,

$$
\Delta U={k\over2}(r'+r)\mathbin{\cdot}(r'-r)
=-F\mathbin{\cdot}\Delta C_s-F_Q\mathbin{\cdot}\Delta Q.
$$

Combining the two identities yields

$$
\Delta U+W_{\rm write}+W_{\rm age}+W_Q=0.
$$

The sign is fixed by the declared force convention. $W_{\rm age}$ is signed
reservoir/source/sink work, not positive dissipation. The separately recorded
input-induced terms

$$
D_{\rm write}=f_0\mathbin{\cdot}(\alpha f_0)\ge0,
\qquad
D_Q=F_Q\mathbin{\cdot}(\alpha\nu F_Q)\ge0
$$

are the nonnegative mobility dissipations. This is operational accounting for
the chosen port, not a derivation of physical work or a closed Hamiltonian for
the native memory substrate.

### 4.6 Cancellation-safe local identities and the full-dot envelope

On the forced-increment scale,

$$
d_C=\alpha GF,
\qquad
\Delta C_{\rm local}=a_{s,0}u_h=\alpha|a_{s,0}|^2F=d_C.
$$

Matched mobility also gives

$$
\Delta C_{\rm local}+v_Q=0.
$$

The implemented residuals evaluate these identities before subtracting two
order-one full readouts. The old full-dot differences remain stored, but are
tested against a prospective forward-error envelope.

With $\epsilon_{64}=2^{-52}$ and

$$
\gamma_n={n\epsilon_{64}\over1-n\epsilon_{64}},
$$

the weighted-sum guard is

$$
S^\uparrow(h)=\operatorname{nextafter}\!\left[
(1+\gamma_{8H})\operatorname{fsum}_j|a_{s,j}|\,|h_j|,+\infty
\right].
$$

Let

$$
E_h=\gamma_4(|\widetilde h_0|+|u_h|),
\qquad
E_Q=\gamma_4(|Q|+|v_Q|),
$$

$$
L_C=|r_{C,\rm local}|+
\gamma_8(|a_{s,0}|\,|u_h|+|d_C|),
$$

$$
L_{CQ}=|r_{CQ,\rm local}|+
\gamma_8(|a_{s,0}|\,|u_h|+|v_Q|).
$$

Repeated application of the dot-product, insertion and final-subtraction
triangle bounds gives

$$
\begin{aligned}
E_C={}&\gamma_{8H}[S^\uparrow(h')+S^\uparrow(\widetilde h)]
+|a_{s,0}|E_h+L_C\\
&+\gamma_8(|C_s(h')|+|C_s(\widetilde h)|+|d_C|),
\end{aligned}
$$

and

$$
\begin{aligned}
E_{CQ}={}&\gamma_{8H}[S^\uparrow(h')+S^\uparrow(\widetilde h)]
+|a_{s,0}|E_h+E_Q+L_{CQ}\\
&+\gamma_8(|C_s(h')|+|C_s(\widetilde h)|+|Q'|+|Q|).
\end{aligned}
$$

One final `nextafter(...,+inf)` is applied. Nonzero subnormal operands make the
run inconclusive. This is deliberately conservative binary64 forward-error
accounting; it is not interval arithmetic and does not validate an unknown
BLAS implementation in general.

### 4.7 Rejected rivals

| rival | rejection type | discriminating result |
| --- | --- | --- |
| omit $W_{\rm age}$ | algebraic and numerical | removes a required FIFO boundary term; P4-R reaches `6.3868 U0` residual |
| replace $C_s$ by raw $c_H$ | algebraic, semantic and numerical | raw $c_H$ retains the rotating mode; rival ledger reaches `5.5514 U0` |
| conjugate the wrong chirality | algebraic and numerical | target notch no longer vanishes; registered wrong-chirality amplitude is `1.011754...` |
| read $F\,dx$ as the interaction work | semantic/algebraic | $U$ is defined on $(C_s,Q)$ and no identity maps $F\cdot\Delta x$ to the complete finite-history ledger |
| insert $m\Delta^2x$ or a momentum state | ontological/model change | creates a new second-order model and cannot explain the current first-order data without a new prospective protocol |

The first three are automated or stored negative controls. The last two cannot
be automated as corruptions of the registered model: they require inventing a
different port or state equation. Their non-selection is therefore documented
as an algebraic/ontological boundary, not presented as empirical falsification
of every possible inertial extension.

## 5. Pass C — numerical trust base

### 5.1 P4-R margins

All 16 channel-off and 32 active arms are complete and valid; all 96
80-decimal exact-ratio checkpoints pass. The closest and most diagnostic
margins are:

| quantity | observed worst case | gate | fraction of limit |
| --- | ---: | ---: | ---: |
| local center/coupling residual | `4.48686e-16` | `5e-12` | `8.97e-5` |
| actuator update residual | `1.53119e-13` | `5e-12` | `3.06e-2` |
| center full-dot envelope ratio | `2.15500e-5` | `1` | `2.16e-5` |
| coupling full-dot envelope ratio | `2.15494e-5` | `1` | `2.15e-5` |
| actuator envelope ratio | `0.0248926` | `1` | `0.0249` |
| per-step total ledger / $U_0$ | `3.35622e-12` | `5e-11` | `0.0671` |
| cumulative total ledger / $U_0$ | `1.24220e-12` | `5e-9` | `2.48e-4` |
| midpoint-force residual | `1.11128e-13` | `5e-12` | `0.0222` |
| final separation / $\delta$ | `0.0840345` | `0.10` | `0.840` |
| final energy / $U_0$ | `0.0070618` | `0.01` | `0.706` |
| minimum signal / $\delta$ | `0.3021` | `0.25` minimum | `1.208` of minimum |

The dynamic separation and energy gates are the closest positive margins;
they pass but are not asymptotic statements.

The phase-averaged transverse coefficients are

$$
\overline B_C=0.208421577193625,
\qquad
\overline B_Q=0.15375308546516817.
$$

Both exceed the registered `0.10` chiral floor with 8/8 positive phase-node
support. The independent standard-library recomputation gives the actuator
mean as `0.1537530854651682`; the last displayed-bit difference is far inside
the predeclared absolute `5e-13` comparison tolerance and does not affect any
classification.

The maximum center and actuator sign-even/sign-odd ratios are respectively
`2.50258e-5` and `6.55762e-6`, versus `0.02`. Mirror and half-turn deviations
are at most about `2.4e-15 R`, versus `1e-11 R`. These are covariance checks,
not replication counts.

### 5.2 Cancellation, summation and high precision

The target calculation uses NumPy dot products for the stored full readouts,
`math.fsum` for nonnegative envelope sums and exact binary-to-rational transfer
for the 80-decimal checkpoint replay. The high-precision calculation retains
the already rounded stored state, so it independently evaluates arithmetic at
selected states without pretending to generate a second trajectory. Its
largest residual/envelope ratio is `2.522e-6`.

A synthetic test reorders the full-dot accumulation and verifies that both
orders remain inside the declared envelope while the local identity is
unchanged. Deliberate `1e-8 D0` local corruption, `1e-8 U0` work corruption,
subnormal injection and high-precision residual corruption are rejected.

### 5.3 Krawczyk trust base

For a box $X$, center $x_0$ and numerical inverse $Y$ of the point Jacobian,
the implementation evaluates the standard operator

$$
K(X)=x_0-YF(x_0)+[I-YJ(X)](X-x_0).
$$

Strict componentwise inclusion $K(X)\subset\operatorname{int}(X)$ gives the
registered local existence/uniqueness conclusion under the interval
arithmetic assumptions. The audit inspected the analytic Jacobian and endpoint
serialization, reran the Anchor at 80 and 120 dps in both environments, and
reran the unrelated known-root inclusion and point-in-interval regression
controls. Both target panels again returned
`interval-certified-unique-root-pass`.

This does **not** supply a second interval trust base: both precision panels
and both environments call `mpmath.iv` 1.3.0. Precision diversity is not
backend independence. All existence wording therefore remains conditional;
“formally verified” and “independently certified” are prohibited.

## 6. Pass D — design, dependence and falsification

| stage | design status | allowed interpretation |
| --- | --- | --- |
| discovery | prospectively frozen search, then selected numerical candidate | one finite-H numerical witness |
| interval/L5 | prospective local boxes and L5 holdout | conditional local certificates and numerical scaling |
| P2 | prospective local response gate | strong tangent evidence but formal composite fail |
| P2-R | outcome-informed, prospectively frozen extension | continued signed return; not a P2 relabel or independent replication |
| P3 | prospective finite set, partly target-blind | finite-ensemble attraction; not an open basin or spontaneous formation |
| P4 | prospective architecture and scalar-response gate | exact ledger plus formal fail; transverse response is discovery evidence for P4-R |
| P4-R | outcome-informed model class, new unopened phase/amplitude holdout | one discrete eight-node chiral-response pass |

The 32 P4-R active arms factor into eight phase nodes, two prescribed
chiralities and two input signs. Sign oddness, reflection and half-turn
symmetry deliberately create dependence. Only four phase pairs are
mirror-distinct. Treating 32 arms as 32 replications would be
pseudoreplication and is explicitly rejected.

The preferred narrow interpretation survived these registered falsifiers:

- channel-off histories remained bitwise native;
- both sign-even contamination ratios stayed far below `0.02`;
- mirror and half-turn maps held for every stored sample;
- local identities, full-dot envelopes, force balance and the complete ledger
  passed every update;
- the raw-center and omitted-age rivals failed by order-one energy scales;
- all phase nodes had the same positive chirality-conditioned transverse
  orientation.

It does **not** separate the following live alternatives:

1. response conditioned on the prepared rotating orbit rather than autonomous
   formation;
2. a finite-$H$ source/write effect rather than a continuum law;
3. a port property created by the explicit chirality-conditioned notch and
   matched actuator mobility;
4. eight-node aliasing of harmonics $8,16,\ldots$;
5. a scale-specific L3 response rather than a transferable Anchor law;
6. a gyroscopic-looking antisymmetric susceptibility without any conserved
   angular momentum or intrinsic spin.

P4-R-S is the registered discriminating next step for item 5 only. It must not
be used to retune P4-R or convert the finite phase quadrature into a continuous
claim.

## 7. Pass E — clean-checkout reproduction

A fresh checkout at
[`b2e8fff8b779ac2b1b4ef6f40be8668fe0c4e5d5`](https://github.com/MemoryDynamics/Knoten/commit/b2e8fff8b779ac2b1b4ef6f40be8668fe0c4e5d5)
was clean and synchronized with its upstream. The exact CI Ruff scope, all
797 pre-auditor tests and strict MkDocs build passed in both obtainable
scientific environments:

| environment | NumPy | SciPy | mpmath | BLAS | P4-R replay |
| --- | --- | --- | --- | --- | --- |
| execution-stack match | 2.4.6 | 1.18.0 | 1.3.0 | OpenBLAS 0.3.31.188.0, Haswell, 8 threads at inventory | 215.39 s, exact scientific equality |
| fresh repository pins | 2.3.5 | 1.17.1 | 1.3.0 | OpenBLAS 0.3.30, Haswell, 8 threads at inventory | 228.50 s, exact scientific equality |

For both replays, every nonvolatile scientific top-level block is exactly
equal after JSON parsing:

```text
active_arms, candidate, candidate_id, channel_off_arms, claim_boundary,
construction_controls, decision, gate, gates, historical_p4, protocol,
registration_controls, response_controls, schema_version
```

There is therefore no merely tolerated scientific last-bit drift between the
two trajectory replays: the observed maximum scientific difference is zero.
The full files are not byte-identical because timestamps, elapsed time and
replay revision are regenerated; the pinned replay also records different
runtime versions. Their canonical-LF hashes are retained in the reproduction
JSON rather than hidden.

The original execution-stack directory is not a clean reconstructible lock:
its metadata lists both NumPy 2.4.6 and 2.5.2 and two `packaging` versions,
although imported code reports NumPy 2.4.6. The separately installed pinned
environment is consistent. This is a major environment-readiness defect,
mitigated but not erased by exact scientific equality.

The full installed-package manifests, OS, architecture, Python, BLAS,
commands, hashes and realistic runtimes are machine-readable in the
reproduction JSON. CI from P4-R design through gate review is green; the
review-stage run is
[GitHub Actions run 33018391498](https://github.com/MemoryDynamics/Knoten/actions/runs/33018391498).
The later audit-artifact commit
[`bb68d9bda94353edaa9a7b98dfdcc6669dc01b3b`](https://github.com/MemoryDynamics/Knoten/commit/bb68d9bda94353edaa9a7b98dfdcc6669dc01b3b)
also passed
[GitHub Actions run 33106952847](https://github.com/MemoryDynamics/Knoten/actions/runs/33106952847).

## 8. Pass F — independent result recomputation

The separately committed
[standard-library auditor](https://github.com/MemoryDynamics/Knoten/blob/d60f6eec93c8cb05c4ea104b76d652a1471b6bab/experiments/current/dynamics/rotation/scalar_memory_loop_p4r_result_audit.py)
imports neither the P4-R runner nor NumPy, SciPy or mpmath. It independently
transcribes the thresholds and reconstructs:

- arm registration and ordering;
- trace completeness and finiteness;
- channel-off stored metrics;
- high-precision decimal magnitude consistency;
- every available ledger/metrology threshold contact;
- cumulative write/age/external ledger recombination;
- D0, phase, projection, separation, signal and energy metrics;
- sign-odd and sign-even traces;
- mirror and half-turn pairing;
- the final $A/B$ response table, means and support;
- decision precedence and Markdown-summary agreement.

Its result is **`p4r-independent-audit-agrees`**, with zero stored-summary
differences. Ten mutation tests reject a duplicate arm, a changed protocol
threshold/blob, a `1e-8 D0` local residual, a `1e-8 U0` cumulative work term
and a reversed stored response sign. The independent output has canonical-LF
SHA-256
`28d7e6d624c0234aeb3d5b730c566389abfc0b49fea45ec0771fc528230ea7e5`.

Independence has a strict boundary. The raw JSON does not serialize every
per-update full history, raw ledger term, bitwise channel-off history or
subnormal operand. Those facts are checked by deterministic full replay, not
reconstructed from the result JSON alone. Agreement of two decision code
paths sharing one simulation is internal reproducibility, not external or
mathematical independence.

## 9. Pass G — repository and citation readiness

### Passed

- all claim inputs have public immutable commit URLs and Git blobs;
- all raw result entries have canonical-LF SHA-256 digests;
- the 15.9 MB P4-R JSON is ordinary Git data with no broken LFS indirection;
- code and data/documentation are covered by the repository MIT license;
- failed and superseded gates remain visible in the report ledger;
- clean reproduction commands and realistic runtimes are recorded;
- public citation paths need no private machine path or credential.

### Open restrictions

- no `CITATION.cff` or equivalent citation metadata;
- no release tag, archival snapshot or DOI;
- no complete cross-platform wheel/hash lock;
- no second validated interval backend;
- no external reproduction.

Immutable commit links make the present evidence citable at source level, but
they do not turn a mutable development branch into an archival release. Author
metadata must be confirmed rather than invented before adding citation files.

## 10. Adversarial attack matrix

| attack | executed discriminator | outcome |
| --- | --- | --- |
| omit $W_{\rm age}$ | stored rival plus `test_registered_age_and_raw_center_rivals_remain_discriminating` | fails, maximum `6.3868 U0` |
| replace $C_s$ by raw $c_H$ | stored rival plus the same test | fails, maximum `5.5514 U0` |
| conjugate wrong chirality | static construction controls and `test_readout_recovers_translation_and_rejects_registered_rotation` | notch/shape control rejects it |
| perturb one protocol blob | `test_target_provenance_rejects_a_protocol_blob_mutation` | provenance raises before target access |
| delete or duplicate one arm | independent-auditor registration mutation test | returns disagreement/inconclusive |
| corrupt local increment by $10^{-8}D_0$ | parameterized independent-auditor mutation test | ledger/metrology failure |
| corrupt work term by $10^{-8}U_0$ | cumulative-work mutation test | ledger/metrology failure |
| reverse one response sign | response-sign mutation test | response recomputation disagrees and classifier changes |
| treat 32 arms as replications | protocol, gate review, claim trace and documentation consistency test | flagged as pseudoreplication; four mirror-distinct pairs retained |
| replay declared and execution NumPy versions | two clean-checkout replays | all scientific JSON blocks exactly equal |
| reorder full-dot accumulation | synthetic forward/reverse accumulation test | both remain in envelope; local identity unchanged |
| remove conditional Krawczyk wording | source-audit consistency test across claim trace and public status surfaces | test fails if conditional trust-base wording disappears |
| read direct $x$ work | independent algebra above | no work identity for the declared $(C_s,Q)$ potential; would define another model |
| insert second-order/mass term | source inspection and protocol prohibition | impossible as a data corruption; it adds a new state equation and requires a new protocol |

All attacks required by the charter are automated unless the attack changes
the model ontology rather than corrupting the registered calculation. Those
two cases are explicitly identified rather than simulated under an invented
alternative.

## 11. Evidence, inference and hypotheses after audit

### Evidence supported

1. The finite-$H$ readout, notch, adjoint force and complete age ledger obey
   the derived algebra.
2. The historical P4 full gate failed while its declared finite-history
   ledger passed.
3. The prospective P4-R panel passed local metrology, full-dot forward
   envelopes, all ledger gates, nonlinear loop-preservation gates and the
   registered discrete chiral classifier.
4. The P4-R decision and every scientific JSON field reproduce exactly in the
   two audited numerical stacks.
5. A separately implemented standard-library auditor recovers the stored
   decision from the available raw JSON.

### Inference permitted

The explicit source/write architecture exhibits a reproducible
chirality-conditioned antisymmetric component in its *discrete phase-averaged
weak response* on the prepared L3 loop. “Gyroscopic-like” may be used only as
an analogy to the antisymmetric response matrix, with the exclusions stated in
the same context.

### Hypotheses still open

- whether the response transfers to the Anchor scale;
- whether a denser or continuous phase average has the same sign and size;
- whether an autonomous microscopic rule selects this port;
- whether two independently formed loops interact reciprocally;
- whether any reduced transfer law contains an identifiable inertial pole.

### Prohibited interpretations

- P4 passed;
- 32 independent replications or statistical significance;
- continuous phase invariance;
- internal `S1`, torus or topological spin;
- conserved angular or linear momentum;
- intrinsic spin, inertia or material mass;
- physical center of mass or uniquely derived physical work;
- P5/two-loop interaction.

## 12. P4-R-S and the paper boundary

The four frozen P4-R-S prerequisites evaluate as follows:

| prerequisite | result |
| --- | --- |
| P4-R chiral decision | pass |
| separate gate review | upheld |
| compatible source verdict | restricted pass; no restriction undermines port/ledger/response |
| required claim language committed and pushed | satisfied only when this audit/status change is on the remote |

Consequently the next scientific task may be **writing a fresh P4-R-S
Anchor-scale holdout protocol** after the audit commit is pushed. This is not
authorization to inspect an Anchor target before that new protocol and its
implementation are separately frozen. P4-R-S must inherit the same port,
ledger and no-mass boundary and predeclare how L3-to-Anchor scaling is judged.

P5 remains closed until P4-R-S itself returns a reviewed full pass. Even then,
P5 would test only the registered two-loop interaction, not charge, intrinsic
spin, a universal force law, field theory or quantization.

## 13. Final referee disposition

The narrow computational chain is sufficiently traceable and reproducible to
serve as a **restricted internal source** for carefully scoped paper claims.
The strongest defensible new sentence is:

> On one prepared L3 finite-memory rotating loop, the explicitly constructed
> chirality-conditioned source/write port closes its complete finite-history
> work ledger and exhibits a positive chirality-odd transverse response under
> the preregistered discrete eight-phase quadrature; the result reproduces
> exactly across the two audited NumPy/SciPy stacks.

It must be followed by the restrictions that the quadrature has four
mirror-distinct phase pairs, the port is an explicit model construction, P4
remains a formal failure, the root certificates are conditional on one
interval backend, and no spin, momentum, inertia or mass has been derived.

Verdict: **`referee-source-ready-with-major-claim-restrictions`**.
