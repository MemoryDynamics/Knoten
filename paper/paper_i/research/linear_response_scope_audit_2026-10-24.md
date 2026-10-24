# Scope of existing response theory for the transport claim

Date: 2026-10-24. Bounded analytical audit of the candidate at `9ce8f3c`.
No new model, target simulation, independent referee report or novelty
certificate. The [Gaussian-projection audit](gaussian_projection_audit_2026-10-24.md)
already identifies the coefficient with a standard approximation. This
note checks whether two established rigorous response frameworks directly
supply the remaining validity claim.

**Conclusion:** rigorous stationary response is not a new method here.
One inspected framework is incompatible with the full-history state in
its stated metric; the other is a plausible route but still needs a
function-space and transport-response verification. Neither observation
establishes sufficient novelty. The candidate remains a model-specific
controlled application of established methods, not a new general theory.

## The precise claim being compared

Use the full Gaussian force, canonical weights $\gamma_j=\alpha q^j$,
$q=1-\alpha$, and definitions of $G_2,\kappa,\lambda,\mu_H,S_H$ in the
[validity note](weak_noise_validity_2026-10-21.md). At fixed coefficients
with $\theta=|\eta|G_2q/\alpha<1$, that internal argument gives a unique
stationary relative process and

$$
D_H(\varepsilon)=
\frac{\varepsilon^2}{2(1+\eta\kappa\mu_H)^2}
-\varepsilon^4\frac{\eta\lambda(d+2)S_H}
{(1+\eta\kappa\mu_H)^3}+O(\varepsilon^6).
$$

Here $D_H$ is the infinite-time MSD slope per coordinate, not a finite-lag
variance. The argument includes $H=\infty$ and finite $H$ with constants
uniform in $H$ at these fixed coefficients. It does not assert uniformity
as $\alpha\to0$ or $\theta\to1$, a functional central-limit theorem, or
validity in the archived active cells. No extra simultaneous-limit claim
is inferred merely from uniform constants. The proof remains internal.

## Primary-source check

The following portions of the author PDFs were read on 2026-10-24.

| Primary source and inspected result | Relevant hypotheses and scope |
| --- | --- |
| [Hairer and Majda, *A simple framework to justify linear response theory*, author version dated 17 February 2010](https://www.hairer.org/papers/FDT.pdf), Section 2, Assumptions 1--3, Theorem 2.3 and Remarks 2.4--2.7 | Differentiability of invariant expectations on a separable Banach space follows from a centered spectral gap in a weighted $C^1$ observable norm, an operator derivative into a weaker weighted continuous norm, and a uniform invariant integrability bound. A transition density is not required. The statement concerns a first derivative and is formulated for Markov semigroups. |
| [Ferre, Herve and Ledoux, *Regular perturbation of V-geometrically ergodic Markov chains*, author version dated 5 June 2012](https://herve.perso.math.cnrs.fr/Stab-FHL.pdf), (VG), Theorem 1 and Proposition 1 | The starting gap is in a weighted supremum norm over measurable observables. Theorem 1 adds a uniform drift bound and two-norm continuity. Proposition 1 treats higher regularity for an AR(1) family under explicit noise-density conditions, including bounded derivative-to-density ratios. |

The Bernard--Wu full-theorem comparison and the aging-paper full text
remain unresolved as recorded in the
[source ledger](pre_reassessment_2026-10-19.md). These two inspected PDFs
do not close the entire literature search.

## An exact obstruction to the total-variation route

This is our elementary state-space check, not a result attributed to the
two papers. On the existing weighted history space

$$
E_r=\{y:r^iy_i\to0\},\qquad
T(y,\xi)=(F_H(y)+\varepsilon\xi,y_0,y_1,\ldots),
$$

start from a fixed history $y$. After $n$ updates its coordinate with
zero-based index $n$ is still exactly $y_0$. The Borel set
$A_n=\{z:z_n=y_0\}$ therefore satisfies $P^n(y,A_n)=1$.

For $\varepsilon>0$, the current increment conditional on its past is a
translated nondegenerate Gaussian. Its stationary marginal has no atoms;
stationarity gives the same fact for every history coordinate. Hence the
stationary full-history law $\nu$ satisfies $\nu(A_n)=0$, and

$$
d_{\rm TV}(P^n(y,\cdot),\nu)
\equiv\sup_A|P^n(y,A)-\nu(A)|=1
\quad\hbox{for every finite }n.
$$

With the alternative supremum over $|f|\leq1$, the value is 2. In
particular, for any finite weight $V(y)\geq1$, the indicators of $A_n$
contradict a bound $c\rho^n V(y)$ with $\rho<1$ over all $|f|\leq V$.
The (VG) route therefore fails on this full-history representation.

This holds even for a finite force horizon if passive older coordinates
are retained. It does **not** rule out total-variation convergence after
projecting to the finite active state, and it does not contradict our
common-innovation contraction in the weighted history distance. Old
coordinates become metrically small without becoming randomly refreshed.
The normalized linear reference below also has nondegenerate noise, so
the same obstruction applies to its full-history kernel at the expansion
point. It is not a new dynamical mechanism or a novelty argument.
A different Markov representation could remove this obstruction; its
closure for the full nonlinear family would have to be established.

## Mapping the small-noise problem to response

For $\varepsilon>0$, put $Y=V/\varepsilon$ and
$\tau=\varepsilon^2$. The normalized one-step chain has unit Gaussian
noise and first-coordinate drift

$$
\widetilde F_{\tau,H}(y)=-\eta\sum_{1\leq j<H}\gamma_j
\left[\frac{A_a}{s_a^2}e^{-\tau|L_j(y)|^2/(2s_a^2)}
-\frac{A_r}{s_r^2}e^{-\tau|L_j(y)|^2/(2s_r^2)}\right]L_j(y).
$$

This defines its linear reference at $\tau=0$ by continuity, not by
dividing the zero-noise trajectory by zero. With $A_H,Q_H$ as in the
validity note, the full noise-free history map obeys

$$
\widetilde T_{\tau,H}(y)
=A_Hy+\tau Q_H(y)+\mathcal E_{\tau,H}(y),\qquad
\|\mathcal E_{\tau,H}(y)\|_r
\leq C_5\tau^2\|y\|_r^5.
$$

The existing global bounds give contraction and all stationary moments
uniformly for $\tau\geq0$ and $H$ at the fixed coefficients. For smooth
cylindrical observables with polynomially bounded derivatives, the
pointwise right derivative of the one-step operator is consequently

$$
P'_0\varphi(y)
=\mathbb E\left[D\varphi(A_Hy+e\xi)[Q_H(y)]\right],
$$

where $e$ inserts the innovation in the first coordinate. This formula
does not itself verify a derivative in an operator norm.

| Requirement for a response-based proof | Status for our model |
| --- | --- |
| State space and invariant laws | The separable $E_r$, invariant construction and polynomial moments are supplied in the strict contraction domain. |
| Weighted observable gap and closure | Common-noise contraction is available. The particular weighted differentiable function space, its closure, and a centered operator estimate have not been verified. A metric contraction cannot simply be renamed the required norm estimate. |
| Parameter derivative and integrability | The displayed cubic direction and moment bounds are ingredients; compatible weights and norm differentiability still need checking. |
| Boundary and discrete time | $\tau=0$ is a one-sided boundary. A discrete-time/right-derivative adaptation must be stated. Extending the exponentials to negative $\tau$ without growth control is not a justification. A first derivative in signed $\varepsilon$ would not identify its even-order correction. |
| Transport and remainder order | The changing correlation resolvent must also be differentiated, with a quantitative remainder and constants uniform over the intended horizons. |

For the specific AR(1) proposition in the second source, even the Gaussian
density fails its bounded-ratio assumption as written, since
$\nu'(x)/\nu(x)=-x$. This excludes that direct substitution, not other
Gaussian perturbation theorems or an adaptation of its proof.

## Why invariant-law response alone is insufficient

Here is a conditional operator calculation to identify the extra work;
we do not assert that all its norm hypotheses have already been checked.
Let $g(y)=y_0^{(1)}$ be one coordinate of the normalized increment. Oddness
and uniqueness make $\nu_\tau g=0$ for every parameter. On a suitable
odd-observable space, suppose the series
$R_\tau g=\sum_{k\geq0}P_\tau^kg$ converges and the following products,
resolvents and derivatives are controlled. Then

$$
\mathcal D_H(\tau)
=\nu_\tau[gR_\tau g]-\frac12\nu_\tau[g^2],\qquad
D_H(\varepsilon)=\varepsilon^2\mathcal D_H(\varepsilon^2),
$$

and differentiating gives

$$
\mathcal D'_H(0)
=\nu'_0\left[gR_0g-\frac12g^2\right]
+\nu_0[gR_0P'_0R_0g].
$$

The first term changes the stationary law. The second changes temporal
propagation; it follows from $R'_0=R_0P'_0R_0$ on that odd space. A theorem
for a fixed stationary observable supplies neither this second term nor
its bounds automatically. Moreover, differentiability alone gives a
remainder $o(\varepsilon^4)$ in $D_H$, not the claimed
$O(\varepsilon^6)$. The latter requires the stronger normalized
$O(\tau^2)$ control.

An exact scalar check makes the distinction visible. For
$y_{n+1}=b y_n+\xi_{n+1}$, $|b|<1$, unit innovation variance,

$$
\nu_b(y^2)=\frac1{1-b^2},\qquad
R_bg=\frac{y}{1-b},\qquad
\mathcal D(b)=\frac1{2(1-b)^2}.
$$

At $b=0$, the stationary-variance derivative is zero while
$\mathcal D'(0)=1$. The entire first-order transport response comes from
the propagation term. This is an algebraic control example, not a target
simulation or proposed replacement dynamics.

Our existing one-innovation resampling proof addresses the needed
transport control directly: its stationary residual has both
$O_{L^p}(\varepsilon^5)$ size and summable dependence bounds
$C_p\varepsilon^5(k+1)^2a^k$. Those are the model-specific estimates to
assess, rather than claiming that invariant differentiability by itself
settles the MSD limit.

## Consequence for the manuscript decision

The limited comparison is complete; a blanket claim that existing theory
already proves everything, or that infinite memory makes our method new,
would both exceed it. The review question is now narrower: **does the
explicit, horizon-uniform control of this model's transport remainder
provide useful additional content beyond routine applications of known
response and coupling techniques?**

The [decision brief](paper_i_decision_brief_2026-10-23.md) carries that
question forward. A failure of one theorem's assumptions is not evidence
of publishable novelty. No automatic higher-order calculation, runner
optimization or large panel follows. The missing full texts and human
mathematical assessment remain explicit gaps. Nothing here supplies a
physical multisystem law or a bridge to quantum mechanics or gravity.

Validation scope: the support argument, normalized derivative and AR(1)
identity are displayed for analytical inspection. An exact-rational
check of the AR(1) response decomposition passes at
$b=-3/4,-1/2,0,1/3,3/4$, including the zero law-response at $b=0$.
The 18 existing Paper-I/documentation checks and the strict documentation
build pass. These finite checks do not validate the general proofs or
the conditional operator assumptions. Production code, frozen PDFs and
target data are unchanged.
