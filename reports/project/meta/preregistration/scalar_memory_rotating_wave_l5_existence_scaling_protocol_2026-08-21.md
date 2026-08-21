# Prospective L5 existence and scaling gate: scalar-memory rotating wave

Date: 2026-08-21.

Status: frozen prospective protocol. This document is committed before the L5
cell is evaluated. The L5 numerical result, the amplitude holdout, non-anchor
stability, formation, topology and interactions are all sealed at freeze time.

## 1. Question and claim boundary

The gate asks one deliberately narrow question: does the already certified
finite-memory branch continue, without retuning, to

$$
(\alpha,H,\eta)=(0.00125,9600,0.01875),
$$

and does the appended L0--L5 sequence remain quantitatively compatible with
first-order approach to the independently reconciled continuum root?

A pass establishes local existence and local uniqueness inside the declared
L5 interval boxes, conditional on the interval-arithmetic trust base, plus
finite-sequence numerical scaling evidence. It does not prove existence for
all smaller $\alpha$, global uniqueness, non-anchor stability, formation from
generic histories, an internal $S^1$, a torus, intrinsic spin, work, inertia,
mass or an interaction law.

## 2. Frozen native model and L5 cell

The native deterministic update remains

$$
x_{n+1}=x_n-\eta\nabla(K*\rho_n)(x_n),
\qquad
\rho_{n+1}=q\rho_n+\alpha M_0\delta_{x_{n+1}},
\qquad q=1-\alpha.
$$

The L5 cell uses

$$
d=2,\quad\varepsilon=0,\quad M_0=1,\quad
\sigma_{\rm rep}=1,\quad\sigma_{\rm att}=3,\quad
A_{\rm rep}=1,\quad A_{\rm att}=3.5,
$$

with delta deposition and the exact finite-age sum over $j=1,\ldots,H-1$.
Decimal arithmetic must verify exactly

$$
H\alpha=12,
\qquad
\eta/\alpha=15.
$$

No amplitude, kernel width, memory extent, deposition rule, gain, start,
precision, iteration count, interval box or gate threshold may be retuned.
The $A_{\rm att}=7$ discovery holdout remains sealed.

For a prepared circular history $x_n=R e^{in\theta}$ define

$$
w_j=\alpha M_0q^j,\qquad
u_j=1-\cos(j\theta),\qquad
\chi_j=R^2u_j,
$$

$$
\phi(\chi)=
-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
 e^{-\chi/\sigma_{\rm rep}^2}
+\frac{A_{\rm att}}{\sigma_{\rm att}^2}
 e^{-\chi/\sigma_{\rm att}^2},
$$

$$
A_H=\sum_{j=1}^{H-1}w_j\phi(\chi_j)u_j,
\qquad
S_H=\sum_{j=1}^{H-1}w_j\phi(\chi_j)\sin(j\theta).
$$

The frozen reduced balance is

$$
F_R=\cos\theta-1+\eta A_H=0,
\qquad
F_T=\sin\theta+\eta S_H=0.
$$

Where their denominators have the required signs, the two independently
reconstructed gains are

$$
\eta_R=\frac{1-\cos\theta}{A_H},
\qquad
\eta_T=-\frac{\sin\theta}{S_H}.
$$

## 3. Immutable inputs and branch transfer

The immutable source objects are exact versioned Git blobs at `HEAD:path`:

| source | canonical Git-blob SHA-256 |
| --- | --- |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_refinement_ladder_2026-08-21.json` | `1ba774daf0bf3395c1d0a356a31c8f5aab17eca76de7b32029f49b456cefb279` |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_foundation_audit_2026-08-21.json` | `8ebc71a2e1f74a859e7aff4acc04bddade55617976ed13f8865826a1f2ad12ce` |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_continuum_reconciliation_2026-08-21.json` | `8008f3846678e8920c1193468e1cacd078ff2c45b2903fbc4ac130431bd68658` |

The recorded ladder execution revision
`b03ff433776ced084f8bf3d56b54b8fe7b1e5ef2` and foundation-audit execution
revision `0bc74acf432f6a2f24cf5e78411441fc8dfa2555` must exist and be ancestors of
the L5 execution revision. The run must begin from a clean, fully committed
worktree with complete Git history. Its protocol revision and execution
revision must be recorded separately.

The L5 continuation start is frozen from the L4 120-digit center:

$$
R_{\rm start}=
0.943957188362017621962796728889665465955595255173674745698318322703201904120534919460310738324071442073390305,
$$

$$
\Omega_{\rm start}=
1.58345817054227476011136633656328035603531524285000037859953328942975445582475455451996353123520752489026474.
$$

In each precision panel independently, initialize

$$
(R,\theta)=(R_{\rm start},\alpha_{\rm L5}\Omega_{\rm start})
$$

and perform exactly eight undamped analytic Newton iterations. Every iterate
must remain in the predeclared branch corridor

$$
|R-R_{\rm start}|<0.01,
\qquad
|\theta/\alpha_{\rm L5}-\Omega_{\rm start}|<0.01.
$$

Leaving the corridor is a failure; changing the start or following a
different root is not an authorized repair.

## 4. L5 interval existence gate

Evaluate independent 80- and 120-decimal-digit panels. Around each final
panel center certify both

$$
X_{\rm outer}:\quad
|\Delta R|\le10^{-6},
\qquad
|\Delta\theta|\le\alpha_{\rm L5}10^{-6},
$$

and

$$
X_{\rm inner}:\quad
|\Delta R|\le10^{-35},
\qquad
|\Delta\theta|\le\alpha_{\rm L5}10^{-35}.
$$

Every box must pass the existing physical-domain, nonsingular-preconditioner,
force-balance containment, sign, required-gain and strict Krawczyk interior
inclusion controls. The panel centers must agree within $10^{-55}$ in both
$R$ and $\Omega=\theta/\alpha$. Each point residual must be no larger than
$10^{-(p-20)}$ at precision $p$. Inner Krawczyk-image widths must be below
$10^{-33}$ in $R$ and $\alpha_{\rm L5}10^{-33}$ in $\theta$.

Strict $K(X)\subset\operatorname{int}(X)$ certifies one root in the declared
box and uniqueness there, subject to the implemented formula, analytic
Jacobian, binary-endpoint serialization and `mpmath.iv` interval operations.
The two precision panels are convergence controls, not independent interval
libraries or a proof-assistant verification.

## 5. Independent finite-sum replay

At the 120-digit center, a separate 70-decimal-digit implementation must
evaluate the displayed finite sums directly without importing either
rotating-wave evaluator. Require

- $\max(|F_R|,|F_T|)\le10^{-45}$;
- $A_H>0$ and $S_H<0$;
- both independently inferred gains differ from $\eta=0.01875$ by at most
  $10^{-40}$; and
- the exact decimal scaling identities in Section 2.

This is a sign, indexing and implementation replay. It is not a second
interval proof.

## 6. Frozen continuum target and scaling tests

Use the independently reconciled continuum root, without refitting it:

$$
R_\infty=
0.9431133067695436321754560922340476968548404654598893868057171376405795,
$$

$$
\Omega_\infty=
1.585570077717788706778975148699744358665285143773149240644121542575246.
$$

Append L5 to the immutable certified L0--L4 centers. For
$y\in\{R,\Omega\}$ define the signed error $d_{y,k}=y_k-y_\infty$ and
$e_{y,k}=|d_{y,k}|$. Recompute every observable rather than importing stored
diagnostics. All of the following must pass for both $R$ and $\Omega$:

1. $e_{y,k}$ decreases strictly from L0 through L5.
2. The least-squares log-log slope on L1--L5 lies in $[0.8,1.2]$.
3. The same-side first-order contraction satisfies

   $$
   0.4\le \frac{d_{y,5}}{d_{y,4}}\le0.6.
   $$

4. The target-independent successive-difference contraction satisfies

   $$
   0.4\le
   \frac{y_5-y_4}{y_4-y_3}
   \le0.6.
   $$

5. The last-pair Richardson estimate $y_{\rm Rich}=2y_5-y_4$ obeys

   $$
   \frac{|y_{\rm Rich}-y_\infty|}{e_{y,5}}\le0.1.
   $$

The signed ratios deliberately reject a branch crossing or oscillatory
approach that an absolute-error-only test could conceal. These thresholds
discriminate first-order behavior on this finite ladder; they do not prove
an asymptotic theorem.

## 7. Decisions and sequential consequence

Decision is `l5-existence-scaling-pass` only if provenance, exact parameter
scaling, both interval panels and boxes, the independent finite-sum replay
and every scaling test pass.

Decision is `l5-existence-pass-scaling-fail` if every L5 existence and replay
gate passes but at least one scaling test fails. This preserves the local
root while falsifying the registered first-order continuation claim at L5.

Any missing interval certificate, provenance failure, arithmetic exception,
corridor exit or replay failure is `l5-existence-inconclusive`. Failure of a
Krawczyk inclusion with these frozen boxes does not prove nonexistence.

Only `l5-existence-scaling-pass` permits preregistration of exactly one
non-anchor stability cell. Formation, topology, toroidal architecture,
mechanics and interactions remain later and separately falsifiable stages.
