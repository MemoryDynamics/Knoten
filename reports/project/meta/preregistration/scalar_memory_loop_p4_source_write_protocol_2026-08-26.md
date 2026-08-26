# Prospective P4 gate: reciprocal orbit-center source/write mechanics

Date: 2026-08-26.

Status: **frozen before any P4-coupled L3 trajectory is advanced.** The exact
finite-sum coefficients, their static notch/adjoint identities and the ideal
two-coordinate reference rate were evaluated while writing this contract. No
active source/write continuation, center-transfer trace, loop-preservation
trace or work-ledger output at the registered L3 target has been opened.

## 1. Question and claim boundary

P3 established finite-ensemble attraction to the unchanged L3 rotating wave.
It did not supply a mechanical port. P4 asks:

> Does one explicitly declared, first-order source/write architecture couple
> reciprocally to a phase-cleaned orbit-center coordinate, move that center
> on the full nonlinear L3 map, preserve the quotient loop and close every
> finite-history work term?

The selected architecture is fixed by the preceding
`scalar_memory_loop_p4_actuator_architecture_audit_2026-08-26.md`. It is not a
parameter competition. Dynamic memory carriers, raw-$c_H$ coupling, a direct
$x$-work port and every second-order or explicit-mass alternative are excluded
from this gate.

A full pass establishes only an operational reciprocal single-loop actuator
and its exact source/write/age ledger in the tested weak panel. It does not
establish a material center of mass, unique microscopic ontology, conserved
momentum of the native open memory system, physical mass, SI calibration,
generic formation, noise robustness, internal $S^1$ or two-loop interaction.

## 2. Frozen provenance

The selection base is the reviewed P3 main merge

```text
ce1aa31e15c96e4023ef537a0c612432187e1c54
```

and the separately published architecture audit revision

```text
cfdb059162d42129252906dd85e9dc1ffb038169
```

The runner must verify these Git blobs:

| dependency | frozen Git blob |
| --- | --- |
| architecture audit | `91620a60f7af84fb9eeeb5c8a5ce0036b9e04906` |
| P3 result JSON | `35b46192c2c4dc7ace3751d321a4e25bd3a80096` |
| P3 critical review | `5897be4ba6c4011eb7afbd32f6f3cacf538600ca` |
| native nonlinear FIFO map | `9defb5a6876371202e1ba57cea030c997b9c6edd` |
| existing Loop--Center utilities | `a8b8a002be3a3e4d75f8bd6b00989f1dafe61e0b` |
| rotating-wave candidate definition | `630beb9952abefea823d91388dcbb2de8f1a2927` |

The P3 JSON SHA-256 must remain

```text
42469985488ee73e2bd8bb1c6dc4cd339b58684b85f2743fa1b2df340e82fc2b
```

and its decision must remain `p3-formation-basin-pass`. The protocol freeze
revision, clean implementation revision, dependency and implementation blobs,
runtime versions and empty pre-run worktree must be recorded. A provenance,
dirty-tree or missing-control error is `p4-inconclusive`, never a mechanics
result.

## 3. Unchanged L3 loop and exact finite-memory readout

No native parameter is changed:

$$
d=2,\quad \varepsilon=0,\quad M_0=1,
$$

$$
(\alpha,H,\eta)=(0.005,2400,0.075),
$$

$$
(\sigma_{\rm rep},\sigma_{\rm att})=(1,3),\qquad
(A_{\rm rep},A_{\rm att})=(1,3.5),
$$

with the reviewed decimal $R_3$ and $\theta_3$ from P1--P3. Let

$$
q=1-\alpha,\qquad
\bar w_j={\alpha q^j\over1-q^H},\qquad
B_H(z)=\sum_{j=0}^{H-1}\bar w_jz^{-j}.
$$

For chirality $s\in\{+1,-1\}$, freeze

$$
\beta_s=B_H(e^{is\theta_3}),
$$

$$
C_s(h)={c_H(h)-\beta_sh_0\over1-\beta_s}
=\sum_{j=0}^{H-1}a_{s,j}h_j,
$$

$$
a_{s,0}={\bar w_0-\beta_s\over1-\beta_s},\qquad
a_{s,j}={\bar w_j\over1-\beta_s}\quad(j\ge1).
$$

Complex coefficients act as real planar rotation-scale matrices $M(a)$. The
positive branch construction values are frozen as

| quantity | binary64 construction value |
| --- | ---: |
| $q^H$ | `5.9620249581892009e-06` |
| $\bar w_0$ | `0.0050000298103025208` |
| $\Re\beta_+$ | `0.28847300317511804` |
| $\Im\beta_+$ | `-0.45107951349124853` |
| $|\beta_+|$ | `0.53543384376818492` |
| $\Re a_{+,0}$ | `0.0024995710921114429` |
| $\Im a_{+,0}$ | `0.63237517365742668` |
| $G=|a_{+,0}|^2$ | `0.39990460811390499` |

The negative branch must be the complex conjugate. No coefficient may be
estimated from an active P4 response.

## 4. Frozen source/write and reciprocal actuator update

For each update, first compute the exact unforced native provisional history

$$
\widetilde h_{n+1}=\mathcal T_{\rm L3}(h_n)
$$

and its orbit center $\widetilde C_{n+1}=C_s(\widetilde h_{n+1})$.

The external coordinate has harmonic interaction

$$
U_n={k\over2}|C_{s,n}-Q_n|^2.
$$

For center force $F_n$ define the write-slot adjoint force

$$
f_{0,n}=M(a_{s,0})^TF_n.
$$

The only active history modification is first order:

$$
h_{0,n+1}=\widetilde h_{0,n+1}+\alpha f_{0,n},
\qquad
h_{j,n+1}=h_{j-1,n}\quad(j\ge1).
$$

The external coordinate uses the equal mobility

$$
\nu=G=|a_{s,0}|^2,
\qquad
F_{Q,n}=-F_n,
\qquad
Q_{n+1}=Q_n+\alpha\nu F_{Q,n}.
$$

The midpoint discrete-gradient force is evaluated by the exact closed form

$$
F_n=-{k\over2+\alpha k(G+\nu)}
\left[(C_{s,n}-Q_n)+(\widetilde C_{s,n+1}-Q_n)\right].
$$

This must satisfy the implicit midpoint equation when recomputed from the
final $(C_{s,n+1},Q_{n+1})$. No iterative tolerance, response fit, mass term
or second difference is permitted.

## 5. Exact force and work ledger

For every slot, define the adjoint generalized force

$$
f_{j,n}=M(a_{s,j})^TF_n.
$$

The registered per-step quantities are

$$
W_{{\rm write},n}
=f_{0,n}\cdot(h_{0,n+1}-h_{0,n}),
$$

$$
W_{{\rm age},n}
=\sum_{j=1}^{H-1}
f_{j,n}\cdot(h_{j-1,n}-h_{j,n}),
$$

$$
W_{Q,n}=F_{Q,n}\cdot(Q_{n+1}-Q_n).
$$

The following are independent mandatory identities:

$$
\sum_j f_{j,n}+F_{Q,n}=0,
$$

$$
W_{{\rm write},n}+W_{{\rm age},n}
=F_n\cdot(C_{s,n+1}-C_{s,n}),
$$

$$
U_{n+1}-U_n+W_{{\rm write},n}+W_{{\rm age},n}+W_{Q,n}=0.
$$

Also record the input-induced nonnegative mobility terms

$$
D_{{\rm write},n}
=f_{0,n}\cdot(\alpha f_{0,n})\ge0,
\qquad
D_{Q,n}=F_{Q,n}\cdot(\alpha\nu F_{Q,n})\ge0.
$$

$W_{\rm age}$ is signed reservoir work, not dissipation and not a fitted
residual. A deliberately truncated ledger that drops this term is a negative
control; it may not be used as the physical ledger even if it happens to
nearly cancel on one trajectory.

## 6. Frozen coupling panel

The coupling strength is

$$
k=0.25.
$$

This value is chosen before target access from the ideal neutral-translation
Cayley factor

$$
\rho_{\rm ideal}={1-\alpha Gk\over1+\alpha Gk}.
$$

Over 20 memory times it predicts a separation ratio about $e^{-4}\simeq
0.0183$, leaving a factor-five margin to the registered final threshold. It
is not fitted to the nonlinear L3 response.

Every active arm runs

$$
N=4000,\qquad \alpha N=20,
$$

with stored output every 10 updates and ledger accumulation at every update.
The initial loop is the exact prepared circle at chirality $s$. Its orbit
center is zero. The external coordinate is initialized as

$$
Q_0=\sigma\delta d,
$$

for

$$
{\delta\over R_3}\in\{5\times10^{-4},10^{-3},2\times10^{-3}\},
$$

$\sigma\in\{+1,-1\}$ and $d\in\{e_x,e_y\}$. Both chiralities are run, for
24 active arms. Offset signs are linearity pairs; chiralities and rotated
copies are symmetry controls, not statistical replications.

The largest initial center force is $5\times10^{-4}R_3$ and the largest
write-slot force is about $3.16\times10^{-4}R_3$. These values follow from the
frozen construction and are not adjusted after a trajectory is opened.

Channel-off $k=0$ controls are run for both chiralities. No noise, force pulse,
target tracking, co-rotating feedback, parameter sweep or P3 formation history
is introduced.

## 7. Structural and falsification controls

All controls are mandatory:

1. coefficient construction, conjugacy, $\sum_ja_{s,j}=1$ and the notch
   $\sum_ja_{s,j}e^{-isj\theta_3}=0$ agree within $5\times10^{-13}$;
2. the exact target and translated/phase-rotated copies return their known
   orbit centers within $10^{-12}R_3$;
3. raw $c_H$ retains the frozen rotating amplitude
   $0.5058810073761263$, while the correct orbit center remains below
   $10^{-12}R_3$;
4. the wrong-chirality readout on the positive target retains amplitude at
   least $0.5R_3$;
5. random unrelated finite-history variations satisfy adjoint virtual work
   and total generalized-force balance within $5\times10^{-13}$ relative;
6. an unrelated deterministic $H=17$ shift satisfies the full write/age
   identity, while dropping $W_{\rm age}$ leaves at least one percent of the
   full center-work scale;
7. $k=0$ is bitwise identical to the native FIFO step and the channel-off
   prepared orbit remains within $10^{-10}R_3$ in D0;
8. translation and common proper-rotation covariance are accurate to
   $10^{-11}R_3$; reflection maps $s=+1$ to $s=-1$ at the same tolerance;
9. every stored state and scalar is finite and every registered arm is
   complete.

Failure of controls 1--8 invalidates the architecture measurement and yields
`p4-inconclusive`. A nonfinite or scientifically stopped active arm with an
otherwise valid pipeline is a dynamic failure.

## 8. Decisional active-arm gates

For every active arm, with $\delta=|Q_0|$ and signed unit direction
$d_\sigma=Q_0/\delta$:

1. the maximum quotient distance from the own-chirality target is at most
   $0.01R_3$;
2. every stored sample over memory times 18--20 and the final sample have D0
   at most $0.002R_3$;
3. the opposite-chirality D0 over the same late window is at least $0.5R_3$;
4. the final separation satisfies $|C_s-Q|/\delta\le0.10$;
5. the final projected center and actuator positions each lie in
   $[0.20,0.80]\delta$ along $d_\sigma$;
6. the final orthogonal magnitudes of $C_s$ and $Q$ are each at most
   $0.05\delta$;
7. the final interaction energy is at most one percent of its initial value;
8. the late mean phase-increment error is at most $0.01\theta_3$ and its RMS
   error at most $0.05\theta_3$ over memory times 15--20;
9. maximum per-step write/age work-split and total interaction-ledger residuals
   are each at most $5\times10^{-11}$ of initial interaction energy, and each
   cumulative residual is at most $5\times10^{-9}$ of that energy;
10. force-balance and direct coupling-displacement residuals are at most
    $5\times10^{-12}$ of their registered force/displacement scales, and no
    mobility dissipation is negative beyond binary64 tolerance.

For every chirality/direction/amplitude sign pair, the even center-response
RMS must be at most 0.02 of the odd RMS. For every chirality/direction/sign,
the three center traces divided by $\delta$ must collapse within 0.02 relative
RMS. Signal is informative only if the maximum center displacement is at
least $0.25\delta$; otherwise the dynamic port is `inconclusive`, not pass.

The ideal Cayley trace and raw-$c_H$ work ledger are reported as
non-decisional rivals. They cannot rescue a failed nonlinear target arm.
The wider registered position interval deliberately does not assume midpoint
partition or conserved total momentum in the open source/sink system; it
requires both coordinates to move materially toward one another.

## 9. Layered decision semantics

- **`p4-source-write-mechanics-pass`:** provenance and every structural,
  ledger, response, linearity, symmetry, phase and loop-preservation gate
  pass for all registered arms.
- **`p4-source-write-ledger-only`:** the pipeline and exact reciprocal ledger
  pass, but at least one valid dynamic center-response, amplitude-collapse,
  phase or loop-preservation gate fails. This does not open P5.
- **`p4-source-write-architecture-fail`:** a valid execution falsifies the
  registered force/work identities or reciprocal implementation.
- **`p4-inconclusive`:** provenance, construction, registration, numerical
  validity, control or signal-floor failure prevents a scientific decision.

Only a separately reviewed full pass may open P5. No failed arm may be
removed, no duration extended and no threshold, $k$, mobility, amplitude,
direction or readout coefficient changed under this protocol.

## 10. Required artifacts and review

The planned executable is

```text
experiments/current/dynamics/rotation/scalar_memory_loop_p4_source_write_gate.py
```

and it must write

```text
reports/dynamics/rotation/scalar_memory_loop_p4_source_write_2026-08-26.json
reports/dynamics/rotation/scalar_memory_loop_p4_source_write_2026-08-26.md
```

The reusable implementation is planned as

```text
src/emergenz_knoten/orbit_center_actuator.py
```

The implementation commit may add tests and static controls but may not alter
the formulas, panel, thresholds or decision map. Full tests, focused tests,
Ruff and strict documentation must pass at a clean pushed implementation
revision before the active P4 continuation is opened.

The separate critical review must audit at least:

1. protocol timing and immutable dependency/implementation blobs;
2. complex-to-real conventions, signed chirality and exact $B_H$ evaluation;
3. whether raw $c_H$ was accidentally substituted for $C_s$;
4. adjoint force balance and every source/write/age work term;
5. discrete-gradient force solution and absence of inserted second order;
6. channel-off, wrong-chirality, covariance and truncated-ledger controls;
7. threshold contacts, numerical floors and mirror-pair non-independence;
8. whether center motion is separated from phase or quotient-shape damage;
9. the distinction between an operational actuator, filter inertia, material
   mass, additive momentum and two-loop interaction.

No project status, Paper claim or P5 priority change is permitted before that
review.
