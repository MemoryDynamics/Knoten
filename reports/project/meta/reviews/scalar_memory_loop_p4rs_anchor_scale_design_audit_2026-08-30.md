# P4-R-S design audit: Anchor-scale transfer of the discrete loop response

Date: 2026-08-30.

Decision: **select one paired Anchor-scale holdout with a dimensionless
memory-time map and an inherited, non-retuned cross-scale effect-size
boundary. Do not construct or advance an Anchor source/write target
trajectory in this audit.**

P4-R-S is the next allowed gate after the reviewed P4-R-phi pass and the
restricted publication-source verdict. It asks only whether the already
declared artificial source/write response is compatible with a second,
coarser prepared member of the same finite-memory ladder. It does not repair
the historical P4 failure, establish convergence, identify a physical
actuator or open a mass or spin interpretation.

The evidential statements are separated before the design:

- **evidence:** P4-R-phi resolved the local source/write metrology and found a
  positive chirality-odd response under one registered eight-node phase
  quadrature at L3;
- **inference to be tested:** the dimensionless response is not specific to
  the L3 discretization;
- **hypothesis:** the same port, evaluated on the already certified and
  numerically stable Anchor at matched memory time, remains in the frozen
  chiral region and agrees with the complete L3 response to within one
  inherited scalar-null effect-size unit;
- **not implied by a pass:** an all-alpha limit, first-order convergence,
  continuous phase averaging, independent replication, momentum, intrinsic
  spin, inertia or material mass.

## 1. Eligibility and immutable audit base

The audit begins from the green main revision

```text
ecdaa8522337880aa1504af8c66924be96e0a9db
```

after the following conditions were satisfied:

| prerequisite | immutable evidence | status |
| --- | --- | --- |
| P4-R result | `0beaf80f713851ab74bef85a24b8323f42f38108` | `p4r-phase-averaged-chiral-response-pass` |
| P4-R gate review | `b2e8fff8b779ac2b1b4ef6f40be8668fe0c4e5d5` | pass upheld |
| publication-source audit | `bb68d9bda94353edaa9a7b98dfdcc6669dc01b3b` plus CI closure `ecdaa8522337880aa1504af8c66924be96e0a9db` | restricted source-ready; compatible with P4-R-S protocol writing |
| mainline CI | [run 33320283789](https://github.com/MemoryDynamics/Knoten/actions/runs/33320283789) | success |

The relevant mainline Git blobs at audit start are:

| dependency | Git blob |
| --- | --- |
| immutable P4-R JSON | `2a668a4c70820bceb0ff84fa1932878d9130aabf` |
| P4-R critical review | `1d25e9db083d91fdfd521f44e0951a1ddd9e2c37` |
| P4-R protocol | `b81fa535c1921c2f11f83e5585bf38b05e0a08d5` |
| P4-R runner | `27a3a40dde60b797b58da576b5849ab10b47079f` |
| source/write implementation | `63d31bc47291f76c65a5633f14436ccd2105fe9a` |
| native nonlinear FIFO map | `9defb5a6876371202e1ba57cea030c997b9c6edd` |
| rotating-wave candidate definition | `630beb9952abefea823d91388dcbb2de8f1a2927` |
| rotating-wave formation/phase utilities | `38f16f11a790a64470bab3a34505825cf815e7f0` |
| Anchor interval result | `fc6e816c6895e408693fbde176afdaee963c20b9` |
| Anchor stability result | `1c9d5746c9553d9cb8031b58258e6d613f1633d9` |
| source-referee report | `273acc3a86a9f3757e853236ce386f064835194c` |
| source-referee findings | `9cf16689a3b8931842e6ef500f555212ac8f5b36` |

The canonical-LF SHA-256 of the P4-R JSON is

```text
807cf915d1602d87a779e7bf587387559b1b19d7de60dc43c6e1e220b73682c8
```

and the stored P4 decision remains
`p4-source-write-architecture-fail`. The P4-R JSON is the only numerical L3
reference. It may be read to form a paired comparison, but it may not be
rerun, filtered or used to choose a P4-R-S tolerance.

At audit time no P4-R-S runner or result artifact exists. The Anchor has
historical native-map stability trajectories and static coefficient tests,
but no registered P4-R-S source/write phase panel. The latter remains the
sealed target.

## 2. Why the Anchor is the discriminating next cell

The Anchor was selected and certified before P4-R and before its transverse
response was known. It is therefore not a response-selected parameter point.
It is also the only coarser ladder member with both:

1. a local finite-$H$ existence/uniqueness certificate, conditional on the
   declared `mpmath.iv` 1.3.0 trust base; and
2. a completed native-map numerical stability gate.

L3 and Anchor share

$$
H\alpha=12,\qquad {\eta\over\alpha}=15,
$$

the same kernel parameters and the same attractive amplitude. They differ in
finite step size, history length, finite-$H$ root, notch coefficients and
write gain. A paired port test therefore attacks the specific rival
explanation that the P4-R response is an L3-only discretization effect.

The Anchor is not an independent random replication: both cells belong to a
matched deterministic continuation ladder, share the same code and use the
same explicit port architecture. A pass supports two-scale compatibility,
not population generalization.

## 3. Frozen candidates and the scale map

The exact candidates are:

| quantity | Anchor target | L3 reference |
| --- | ---: | ---: |
| candidate id | `k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1` | `k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1` |
| $\alpha$ | `0.01` | `0.005` |
| $q=1-\alpha$ | `0.99` | `0.995` |
| $H$ | `1200` | `2400` |
| $H\alpha$ | `12` | `12` |
| $\eta$ | `0.15` | `0.075` |
| $\eta/\alpha$ | `15` | `15` |
| $R$ | `0.946517504804223960990626662735384935160072399313332184824852189820406142783597632634323623097735558253263801` | `0.944805811705743656419366118422595657454474452804188781825799206245348464567689511866917417017911971955244464` |
| $\theta$ | `0.0157703817171349919012689641413413231316321140980062507765923663663284306507309780740587352166842324150748019` | `0.00790666146243552374938496703030974246197803459527409259815696583141708245813094145986593003659167675765833059` |
| $\Omega=\theta/\alpha$ | `1.577038171713499` | `1.581332292487105` |

The exact Anchor decimals are the 120-decimal-digit refined root stored in
the interval result, not the shorter historical stability-run display value.
The executable representation is binary64 and must record both the decimal
source and the parsed value.

The comparison coordinate is memory time

$$
\tau=\alpha n.
$$

P4-R used 4000 L3 updates and stored every tenth update. P4-R-S therefore
uses exactly

| execution quantity | Anchor | L3 reference |
| --- | ---: | ---: |
| active updates | `2000` | `4000` |
| final memory time $\alpha N$ | `20` | `20` |
| storage stride | `5` | `10` |
| stored spacing $\Delta\tau$ | `0.05` | `0.05` |
| stored samples including zero | `401` | `401` |
| late window start | $\tau=18$, update `1800` | $\tau=18$, update `3600` |
| phase window start | $\tau=15$, update `1500` | $\tau=15$, update `3000` |
| high-precision checkpoints | updates `1,1000,2000` | updates `1,2000,4000` |

Copying 4000 updates to the Anchor would double the dimensionless exposure
and would not be a scale test. Copying the L3 storage stride would compare
different time grids. Both are prohibited.

## 4. Same equations, candidate-specific coefficients

For either cell define

$$
\bar w_j={\alpha q^j\over1-q^H},\qquad
B_H(z)=\sum_{j=0}^{H-1}\bar w_j z^{-j},
$$

$$
\beta_s=B_H(e^{is\theta}),\qquad
a_{s,0}={\bar w_0-\beta_s\over1-\beta_s},\qquad
a_{s,j}={\bar w_j\over1-\beta_s}\quad(j\ge1).
$$

The readout, adjoint write and matched mobility remain

$$
C_s(h)=\sum_j a_{s,j}h_j,\qquad
u_h=\alpha a_{s,0}^*F,\qquad
G_s=|a_{s,0}|^2,\qquad \nu_s=G_s.
$$

The rule $\nu=G$ is invariant across scale; the numerical gain is not. A
literal copy of the L3 gain into the Anchor would break the declared matched
center/actuator mobility and is prohibited. Static evaluation before any
target trajectory gives:

| static quantity for $s=+1$ | Anchor | L3 |
| --- | ---: | ---: |
| $\beta_s$ | `0.2923957083606503 - 0.45093731944942195 i` | `0.2884730031751183 - 0.4510795134912482 i` |
| $a_{s,0}$ | `0.004999787409710969 + 0.6340870653534046 i` | `0.0024995710921108883 + 0.632375173657427 i` |
| $G=\nu$ | `0.4020914043226352` | `0.39990460811390555` |

For $s=-1$ the values are their complex conjugates and the same positive
gain follows. The coupling strength remains $k=0.25$.

At each update the unchanged native map first produces $\widetilde h$, after
which the same midpoint discrete-gradient force is applied:

$$
F=-{k\over2+\alpha k(G+\nu)}
\left[(C_s(h)-Q)+(C_s(\widetilde h)-Q)\right],
$$

$$
h'_0=\operatorname{fl}(\widetilde h_0+\alpha a_{s,0}^*F),
\qquad
Q'=\operatorname{fl}(Q-\alpha\nu F).
$$

No second difference, velocity, momentum, mass, fitted transfer tensor,
co-rotating feedback or target tracking may enter the Anchor update.

## 5. Anchor holdout panel

The P4-R phase nodes are deliberately reused for a paired scale comparison:

$$
\varphi_m={(2m+1)\pi\over8},\qquad m=0,\ldots,7.
$$

They are known at L3 but unopened as Anchor port trajectories. No node may be
removed or shifted. The Anchor offset is fixed dimensionlessly:

$$
{\delta_A\over R_A}=1.5\times10^{-3},\qquad
\delta_A=0.0014197762572063359,
$$

$$
Q_0=\sigma\delta_A e_x,qquad \sigma\in\{-1,+1\}.
$$

The panel and serialization order remain:

- 16 Anchor channel-off arms: phase, then chirality $(+1,-1)$;
- 32 Anchor active arms: phase, then chirality $(+1,-1)$, then offset sign
  $(+1,-1)$.

Signs and chiralities are controls. The eight nodes form one deterministic
quadrature with four mirror-distinct pairs. The Anchor and L3 panels together
are two deterministic scale cells, not 64 replications.

Using the same phase nodes is necessary for a paired profile and trace
comparison. It does not address the known aliasing of harmonics $8,16,\ldots$
and does not upgrade the quadrature to a continuous phase integral.

## 6. Inherited Anchor validity and ledger gates

Every P4-R construction, channel-off, local-metrology, full-dot-envelope,
80-decimal-digit checkpoint, force, work, finite-history age, raw-center
rival, omitted-age rival, loop, phase, odd/even, mirror and half-turn rule is
inherited without scientific tolerance relaxation. Dimensional scales are
recomputed from $R_A$, $\delta_A$, $\alpha_A$, $H_A$, $G_A$ and the first
Anchor force.

In particular:

1. the local center, center/actuator and actuator-update residuals remain at
   most `5e-12` of the first prescribed coupling displacement;
2. all full-dot residuals must remain inside the same formula with
   $\gamma_{8H_A}$, not the L3 value of $H$;
3. per-step and cumulative ledger limits remain `5e-11` and `5e-9` of the
   Anchor initial interaction energy;
4. force and midpoint-force limits remain `5e-12` of the first Anchor force;
5. the complete finite-history age term remains mandatory and both mobility
   dissipations may not fall below `-1e-30`;
6. channel-off histories must be bitwise native, satisfy
   $D_0/R_A\le10^{-10}$ and $|C_s|/R_A\le10^{-10}$;
7. maximum and late own-chirality distances remain at most `0.01 R_A` and
   `0.002 R_A`; late opposite-chirality distance remains at least `0.5 R_A`;
8. final separation, signed longitudinal projections, interaction energy,
   phase increments and minimum center signal retain the P4-R dimensionless
   limits;
9. mirror and half-turn trace errors remain at most `1e-11 R_A`;
10. every arm must be finite, complete and valid at update 2000.

Failure of a local identity or complete ledger cannot be rescued by a
cross-scale response match. The full-dot envelope remains a conservative
binary64 model, not an interval proof.

## 7. Anchor response classifier

For each scale $r\in\{A,L3\}$, chirality $s$, phase $m$ and stored memory
time $\tau_k$, subtract the matching channel-off trace and form the sign-odd
dimensionless response for $X\in\{C,Q\}$:

$$
X^{\rm odd}_{r,s,m}(\tau_k)=
{X^{\rm resp}_{r,s,m,+}(\tau_k)-
X^{\rm resp}_{r,s,m,-}(\tau_k)\over2\delta_r}.
$$

Define chirality-aligned components

$$
A_{X,r,s,m}=\operatorname{Re}X^{\rm odd}_{r,s,m},\qquad
B_{X,r,s,m}=-s\operatorname{Im}X^{\rm odd}_{r,s,m}.
$$

The Anchor independently inherits the P4-R final-sample classifier:

$$
|\overline B_{C,A}|,|\overline B_{Q,A}|\le0.05
\quad\hbox{(scalar null)},
$$

or

$$
\overline B_{C,A},\overline B_{Q,A}\ge0.10
\quad\hbox{with at least six of eight positive paired nodes}
\quad\hbox{(positive chiral region)}.
$$

The same odd-signal resolution and even/odd RMS limit `0.02` apply. Values in
the gap, mixed classifications and insufficient sign support are
inconclusive. A component at or below `-0.10`, or resolved center/actuator
components of magnitude at least `0.10` with opposite signs, is a directional
falsification.

## 8. Frozen L3-to-Anchor scale comparison

The L3 reference is reconstructed directly from the immutable P4-R raw arm
traces. Its final phase-paired means, reported here only as the fixed
comparator, are:

| component | L3 value |
| --- | ---: |
| $\overline A_C$ | `0.24091330892887405` |
| $\overline B_C$ | `0.208421577193625` |
| $\overline A_Q$ | `0.303296080377988` |
| $\overline B_Q$ | `0.15375308546516817` |

These values do **not** set a new corridor. Every cross-scale effect-size
limit is the already frozen scalar-null boundary

```text
epsilon_scale = 0.05
```

which predates the Anchor target and was not selected from an Anchor preview
or from the observed L3-to-Anchor difference.

On the exactly matched 401-point $\tau$ grid require, for
$X\in\{C,Q\}$ and $Y\in\{A,B\}$,

$$
D_{X,Y}^{\rm trace}=
\left[{1\over16\cdot401}
\sum_{s,m,k}(Y_{X,A,s,m}(\tau_k)-
Y_{X,L3,s,m}(\tau_k))^2\right]^{1/2}\le0.05.
$$

Thus longitudinal and chirality-aligned transverse traces each have their
own scalar effect-size gate. A combined complex RMS may be stored as a
diagnostic, but it is not the registered decision quantity: applying the
scalar-null threshold to a Euclidean two-component norm would introduce an
unregistered stricter geometry.

At the final sample, first pair chiralities at each phase. For each of the
four components $Y\in\{A_C,B_C,A_Q,B_Q\}$ require the phase-profile RMS

$$
D_Y^{\rm profile}=
\left[{1\over8}\sum_{m=0}^7
(Y_{A,m}^{\rm pair}-Y_{L3,m}^{\rm pair})^2\right]^{1/2}
\le0.05.
$$

The four absolute mean differences are stored and must also be at most
`0.05`. This last condition is mathematically implied by the corresponding
profile RMS bound; it is retained as an explicit interpretive check, not
counted as independent evidence. Ratios and signed differences are reported
but cannot rescue or replace the absolute dimensionless limits.

The full-trace gate prevents agreement at one final sample from hiding a
different transient. The final profile gate prevents a local phase mismatch
from being diluted across 401 samples. Neither two-scale comparison
establishes an order of convergence; at least a third prospectively tested
scale and a separately frozen model would be required for that claim.

## 9. Decision precedence

The result labels and their exact order are:

1. provenance, registration, construction, completeness, finiteness,
   normal-number validity, reference-grid or channel-off failure returns
   **`p4rs-inconclusive`**;
2. local source/write, full-dot envelope, actuator update, force, midpoint
   force, split ledger, total ledger or mobility-sign failure returns
   **`p4rs-ledger-or-metrology-fail`**;
3. symmetry, odd-signal, loop, phase or inherited non-orthogonal response
   failure returns **`p4rs-inconclusive`**;
4. a valid Anchor panel in both scalar null regions returns
   **`p4rs-anchor-scalar-response`** and falsifies the registered chiral
   transfer route;
5. a valid resolved negative component at or below `-0.10`, or opposite-sign
   center/actuator components of magnitude at least `0.10`, returns
   **`p4rs-anchor-chiral-hypothesis-fail`**;
6. a valid Anchor chiral classification that violates any frozen trace,
   final-profile or mean scale limit returns
   **`p4rs-cross-scale-mismatch`**;
7. only a valid Anchor chiral classification with every inherited and
   cross-scale gate true returns **`p4rs-anchor-scale-transfer-pass`**;
8. every gap, mixed or insufficient-support case returns
   **`p4rs-inconclusive`**.

The historical P4 fail and P4-R pass are serialized unchanged in every
branch. `Inconclusive` never opens a new scientific gate.

## 10. Adversarial alternatives and falsifiers

P4-R-S must not pass if any of the following occurs:

1. an Anchor port trajectory is opened before protocol and implementation
   commits are separately frozen, pushed and reviewed;
2. the rounded stability candidate replaces the exact interval-refined
   Anchor decimals without explicit equality checks;
3. L3 numerical $G$ is copied rather than rebuilding $B_H$, $a_0$ and
   $G=\nu$ for the Anchor;
4. 4000 Anchor steps or storage stride 10 silently replace the matched
   memory-time map;
5. a phase, sign or chirality arm is removed because its target value is
   inconvenient;
6. the L3 raw reference is rerun, filtered or reconstructed from rounded
   report prose instead of the immutable JSON;
7. local metrology, the full finite-history age term, channel-off, raw-center
   or omitted-age rivals are weakened;
8. the Anchor is chiral but any full-trace or final-profile scale gate exceeds
   `0.05`;
9. symmetry-related arms are counted as independent replications;
10. the result is called first-order convergence, a continuous phase
    integral, spin, momentum, inertia, mass or two-loop evidence.

Important surviving alternatives even after a pass are:

- a response produced specifically by the explicitly chirality-conditioned
  notch/adjoint architecture;
- deterministic prepared chirality rather than spontaneous symmetry
  breaking;
- a two-cell matched-ladder effect with no theorem for other $\alpha$ or $H$;
- a numerical result sharing one implementation and no random ensemble;
- eight-node phase aliasing.

## 11. Required freeze sequence

The next actions are strictly ordered:

1. commit and push this target-free design audit;
2. write a separate P4-R-S protocol that pins this audit blob, every
   dependency blob, all paths, arm order, formulas, thresholds and decisions;
3. commit and push the protocol before creating the target runner;
4. implement the runner and synthetic/preflight tests without calling any
   registered Anchor arm;
5. commit, push and adversarially review the implementation; only that review
   may authorize one clean target execution;
6. write the complete result atomically, commit and push it unchanged before
   any outcome review or status promotion;
7. conduct a separate result review.

The planned paths, to be frozen by the later protocol, are:

```text
experiments/current/dynamics/rotation/scalar_memory_loop_p4rs_anchor_scale_gate.py
reports/dynamics/rotation/scalar_memory_loop_p4rs_anchor_scale_2026-08-30.json
reports/dynamics/rotation/scalar_memory_loop_p4rs_anchor_scale_2026-08-30.md
```

The runner must refuse to overwrite either default result artifact and may
not expose a partial target summary.

## 12. Claim boundary

A later reviewed full pass could support only:

> At the prepared L3 and Anchor members of one matched finite-memory ladder,
> the same explicitly declared reciprocal source/write rule closes its local
> and finite-history ledgers, preserves each loop and yields compatible
> dimensionless sign-odd responses under the registered eight-node phase
> quadrature and cross-scale effect-size gates.

It could then open **only prospective P5 protocol writing**. It would not be
P5 evidence and would not establish a physical force law, an independent
replication, all-scale convergence, continuous phase, internal topology,
spin, momentum, inertia, a center of mass or material mass. The three open
publication-source restrictions remain open independently of this gate.
