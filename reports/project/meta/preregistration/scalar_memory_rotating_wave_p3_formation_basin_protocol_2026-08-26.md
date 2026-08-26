# Prospective P3 gate: L3 formation and sampled finite basin

Date: 2026-08-26.

Status: **frozen before any P3 history is advanced by the native map.** Only
the analytic initial histories and their static D0 separations were evaluated
while writing this contract. No continuation, entrance time, late distance or
phase-rate output from any registered P3 arm has been opened.

## 1. Question and layered claim boundary

P3 asks two deliberately separate questions:

1. **sampled finite basin:** do finite, target-informed but noncircular
   deformations return to the already reviewed L3 relative equilibrium?
2. **formation from target-blind histories:** do chiral noncircular histories
   built only from the model scales $\alpha$ and $\sigma_{\rm rep}$ approach
   the same relative equilibrium without using $R_3$ or $\theta_3$ in their
   construction?

A full pass supports attraction for exactly the registered finite ensemble.
It does not prove an open basin ball, basin volume, generic or spontaneous
formation, noise robustness, chirality selection from an exactly symmetric
state, an internal $S^1$, mechanics, interaction or mass.

The model is deterministic and reflection equivariant. Exact achiral initial
data lie in an invariant subspace and cannot choose a handed loop. Therefore
the active formation histories occur in mirror pairs with a declared seed
chirality. The mirror pairs are symmetry controls, not independent
replications. An exact collinear history is retained as a negative control.

Only a critically reviewed full P3 pass may open P4. A basin-only result does
not.

## 2. Frozen provenance

The selection base is the clean main merge

```text
a956f1343af5566d309634b8a3e02e0e32d10b9c
```

which contains the reviewed P1 pass, the immutable P2 fail and the reviewed
P2-R pass. The runner must verify these Git blobs:

| dependency | frozen Git blob |
| --- | --- |
| P1 L3 result JSON | `18821ed0235e5e915424f61c665be86d569d58cc` |
| P1 L3 critical review | `8fa25608f165789662ca1fb92d2507791dc143ea` |
| P2 result JSON | `69cca249c5fb919f9c95b8e24cc230646f6a49c8` |
| P2 critical review | `7404931c683ff740a0bce8bcd85d6a49b0acd91e` |
| P2-R result JSON | `d6ac2d4bb522e73e69af03a0d1548e7c893c2e84` |
| P2-R critical review | `240fbebe3419547670fce40a871387e6674e378a` |
| native FIFO/D0 implementation | `9defb5a6876371202e1ba57cea030c997b9c6edd` |
| rotating-wave gate implementation | `630beb9952abefea823d91388dcbb2de8f1a2927` |

The P2-R JSON SHA-256 must be

```text
484d0c614471980f81a242e3656ccea7793bd4c832f6138621cee575c36c1423
```

and the decisions must be, respectively,
`numerically-stable-source-pass`, `loop-center-matrix-local-fail` and
`p2r-sign-sensitive-long-recovery-pass`. The protocol freeze revision, clean
implementation revision, dependency blobs, Python/NumPy/SciPy versions and
clean pre-run worktree must be recorded. A provenance or dirty-tree failure is
`p3-inconclusive`, never a scientific formation result.

## 3. Unchanged candidate and two target chiralities

No model parameter is retuned:

$$
d=2,\qquad \varepsilon=0,\qquad M_0=1,
$$

$$
(\alpha,H,\eta)=(0.005,2400,0.075),
$$

$$
(\sigma_{\rm rep},\sigma_{\rm att})=(1,3),\qquad
(A_{\rm rep},A_{\rm att})=(1,3.5).
$$

The frozen binary64 construction uses the published decimal center

$$
R_3=0.944805811705743656419366118422595657454474452804188781825799206245348464567689511866917417017911971955244464,
$$

$$
\theta_3=0.00790666146243552374938496703030974246197803459527409259815696583141708245813094145986593003659167675765833059.
$$

For age $j=0,\ldots,H-1$ and chirality $s\in\{+1,-1\}$, define

$$
C_s(j)=R_3
\begin{pmatrix}
\cos(j\theta_3)\\
-s\sin(j\theta_3)
\end{pmatrix}.
$$

$C_{+}$ is the published P1/P2 history and $C_-$ its reflection. The proper-
rotation/translation quotient does not identify them. Their frozen static
separation is

$$
\frac{D_0(C_-,C_+)}{R_3}
=1.1134199709942472.
$$

At every native update an arm is compared with both fixed target histories.
Because D0 already quotients the common spatial phase, no target-assisted
time alignment or fitted angular frequency is used.

## 4. Frozen active initial-history ensemble

All active arms use the unchanged native map with no external port and no
noise. Every noncircular family is run at both $s=+1$ and $s=-1$.

### 4.1 Prepared positive controls

The exact $C_+$ and $C_-$ histories are advanced for the full horizon. They
test the native-map convention and both target orientations; they are not
formation evidence.

### 4.2 Target-informed sampled-basin panel

The ellipse family is

$$
E_{s,e}(j)=R_3
\begin{pmatrix}
(1+e)\cos(j\theta_3)\\
-s(1-e)\sin(j\theta_3)
\end{pmatrix},
\qquad e\in\{0.03,0.10\}.
$$

The separate geometry holdout combines radial and phase modulation:

$$
\rho_j=R_3\left[1+0.08\cos\left(2j\theta_3+\frac{\pi}{5}\right)\right],
$$

$$
\phi_{s,j}=-s\left[j\theta_3+0.08\sin(j\theta_3)\right],
\qquad
W_s(j)=\rho_j(\cos\phi_{s,j},\sin\phi_{s,j}).
$$

The static plus-branch D0 fractions, frozen only as construction controls,
are

| family | initial $D_0/R_3$ |
| --- | ---: |
| $E_{+,0.03}$ | 0.03229444319841298 |
| $E_{+,0.10}$ | 0.1079491520241994 |
| $W_+$ | 0.1082191303711561 |

The mirrored values must agree within $5\times10^{-13}$. These finite
directions bridge the $10^{-7}R_3$ P1 panel but do not certify every history
inside their distance.

### 4.3 Target-blind formation panel

Let $u_j=\alpha j$. Neither target-blind family contains $R_3$ or
$\theta_3$.

The primary wrong-rate ellipse is

$$
F_s(j)=\sigma_{\rm rep}
\begin{pmatrix}
\cos u_j\\
-0.6s\sin u_j
\end{pmatrix}.
$$

Its angular age increment is $\alpha$, whereas the target increment is not
used in construction. The nonperiodic formation holdout is the damped hook

$$
G_s(j)=\sigma_{\rm rep}
\begin{pmatrix}
e^{-u_j}\\
-s u_j e^{-u_j}
\end{pmatrix}.
$$

Their frozen static plus-branch D0 fractions are 0.6318738063717837 and
0.6787314983982393. Thus neither is a disguised small perturbation or a
prepared circular history. They are nevertheless analytic delay histories,
not histories generated by a prior autonomous run; that limitation survives
every outcome.

For every noncircular seed, the intended target must already be closer than
the reflected target by at least $0.1R_3$. The smallest frozen construction
margin is $0.1511509872450275R_3$ for $G_+$. This is only a seed-chirality
registration check; it is not evidence that the dynamics preserves or forms
that chirality.

## 5. Negative controls

Two controls are mandatory and non-decisional for formation in the positive
sense.

1. **FIFO-only control:** advance $G_+$ with $\eta=0$ for exactly $H=2400$
   updates. The visible point then remains fixed and the FIFO must become a
   collapsed constant history. Its final translation-reduced norm must be at
   most $10^{-12}R_3$, while its final distance to either chiral target must
   exceed $0.5R_3$. This prevents finite-memory replacement alone from being
   labeled formation.
2. **Achiral invariant-subspace control:** with the active L3 parameters,
   advance

   $$
   A(j)=\sigma_{\rm rep}(e^{-\alpha j},0)
   $$

   for 2400 updates. Every $y$ coordinate must remain below
   $10^{-13}\sigma_{\rm rep}$ in absolute value, and neither target distance
   may fall below $0.1R_3$ at a stored sample. This records the deterministic
   no-selection fact: an exactly reflection-symmetric seed cannot choose
   chirality.

Failure of a negative control invalidates the measurement pipeline and yields
`p3-inconclusive`; it cannot be counted as positive formation.

## 6. Native execution, sampling and scientific stops

Every active arm runs

$$
N=12000,\qquad \alpha N=60
$$

native updates, sampled every 10 updates including step zero. This is about
15.1 target rotations and leaves 15 memory times after the registered entrance
deadline. No co-rotating force, phase feedback or input is applied.

An active arm stops scientifically if its state becomes nonfinite, if its
translation-reduced norm exceeds $10\sigma_{\rm rep}$, or if the absolute
memory centroid exceeds $10^6\sigma_{\rm rep}$. Such a completed registered
stop is a failure of that arm, not a numerical inconclusive result. An
external interruption may be rerun only from the same clean revision and does
not change the decision semantics.

The D0 distance, optimal proper-rotation alignment, translation-reduced norm
and memory centroid are computed from the unchanged production routines. No
trajectory-dependent threshold, rescaling, rephasing or extension is allowed.

## 7. Entrance, dwell, phase and chirality gates

For an active noncircular arm of seed chirality $s$, let $D_s(n)$ denote D0
distance to $C_s$, $D_{-s}(n)$ distance to the reflected target, and
$a_s(n)$ the D0 alignment angle. The arm passes only if all conditions hold:

1. it starts at $D_s(0)/R_3\ge0.02$ and completes all 12000 updates;
2. it enters $D_s/R_3\le0.01$ no later than update 9000;
3. every stored sample from update 9000 through 12000 remains at
   $D_s/R_3\le0.01$;
4. its final distance is at most $0.002R_3$;
5. every stored sample from update 9000 onward has
   $D_{-s}/R_3\ge0.5$;
6. over updates 10000--12000, unwrap $a_s$ and define the inferred native
   angular increment per update as minus its sampled difference divided by
   10. Its mean differs from $s\theta_3$ by at most $0.01\theta_3$, and its
   RMS deviation from $s\theta_3$ is at most $0.05\theta_3$.

The tube gate measures attraction to the symmetry-reduced target history;
the phase gate independently rejects a static or wrong-handed shape match.
No entrance time or late rate is fitted.

For every mirrored family, let $S=\operatorname{diag}(1,-1)$ and define the
unfitted raw mirror error

$$
M^2(n)=\lVert h^-_0(n)-S h^+_0(n)\rVert^2
+\sum_{j=1}^{H-1}\bar w_j
\lVert h^-_j(n)-S h^+_j(n)\rVert^2.
$$

It must satisfy $M(n)\le10^{-11}R_3$ at every stored sample. No translation,
rotation or phase is optimized in this control. It is an implementation/
equivariance check and supplies no additional replication count.

The two exact prepared controls must complete with maximum own-target D0 at
most $10^{-10}R_3$, remain at least $0.5R_3$ from the opposite target after
step zero, and meet the same late phase-increment tolerances.

## 8. Layered decision semantics

`pipeline-controls` means provenance, clean execution, exact initial geometry,
both prepared controls, mirror equivariance, both negative controls, complete
registration and finite metric evaluation all pass.

- **`p3-formation-basin-pass`:** `pipeline-controls` passes, all six sampled-
  basin arms pass and all four target-blind formation arms pass.
- **`p3-basin-only`:** `pipeline-controls` passes, all six sampled-basin arms
  pass, but at least one valid target-blind formation arm fails.
- **`p3-finite-basin-fail`:** `pipeline-controls` passes, but at least one
  sampled-basin arm fails.
- **`p3-inconclusive`:** provenance, initial construction, prepared control,
  mirror, negative control, registration or numerical metric failure prevents
  a scientific classification.

The ordering is fixed: a basin failure cannot be rescued by a target-blind
arm that happens to pass. A stopped/diverged active arm is a valid arm failure.
No partial family count may be promoted to the full-pass language.

Only a separately reviewed `p3-formation-basin-pass` opens P4. A
`p3-basin-only` result supports a finite sampled return ensemble and nothing
more. All other outcomes stop the sequential loop programme pending a new
scientifically distinct protocol.

## 9. Registered diagnostics, not decision replacements

The report must include all stored D0 traces, opposite-target distances,
alignment phases, first entrance times, final and dwell maxima, phase means
and RMS errors, translation-reduced norms, centroids and mirror errors. It may
also report:

- monotone or nonmonotone approach and maximum transient D0;
- late log-distance rates where the signal is above a declared numerical
  floor;
- which target-blind geometry fails first;
- the relation of late rates to the P1 value 0.702553 per memory time.

These diagnostics cannot retune the tube, deadline, horizon, phase tolerance
or decision. In particular, fitting a new radius, angular increment or moving
target to a failed arm is forbidden under P3.

## 10. Artifacts, validation and mandatory review

The planned executable is

```text
experiments/current/dynamics/rotation/scalar_memory_rotating_wave_p3_formation_basin.py
```

and must write

```text
reports/dynamics/rotation/scalar_memory_rotating_wave_p3_formation_basin_2026-08-26.json
reports/dynamics/rotation/scalar_memory_rotating_wave_p3_formation_basin_2026-08-26.md
```

The implementation commit may add code and tests but may not alter a family,
horizon, sample cadence, threshold, stop or decision. Before target access,
the full repository tests, lint and strict documentation build must pass.

A separate critical review must audit at least:

1. absence of P3 dynamic target access before the freeze;
2. exact source blobs, constructors and native-map equivalence;
3. whether any seed encodes the target radius or rate;
4. entrance versus transient crossing and the full dwell interval;
5. reflection covariance, opposite-target separation and phase unwrapping;
6. negative controls and deterministic chirality non-selection;
7. scientific stops, numerical floors and any threshold contacts;
8. the finite-ensemble limitation and the distinction between sampled basin,
   target-blind formation, generic formation and physical mechanics.

No status, Paper claim or downstream priority changes before that review.
