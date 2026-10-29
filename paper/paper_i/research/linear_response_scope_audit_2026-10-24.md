# Scope of existing response theory for the transport claim

Date: 2026-10-24; concrete-observable proof updated 2026-10-25.
Bounded analytical audit of the candidate at `9ce8f3c`, extended after
the initial scope audit at `467ebe8`.
No new model, target simulation, independent referee report or novelty
certificate. The [Gaussian-projection audit](gaussian_projection_audit_2026-10-24.md)
already identifies the coefficient with a standard approximation. This
note checks whether two established rigorous response frameworks directly
supply the remaining validity claim.

**Conclusion:** rigorous stationary response is not a new method here.
One inspected framework is incompatible with the full-history state in
its stated metric. A general import of the other has not been verified,
but the concrete observables now admit the direct Poisson/resolvent proof
below, including the transport remainder uniformly in the horizon.
This reinforces the interpretation as a model-specific controlled
application of established methods, not a new general theory. The proof
is internal, not an independent mathematical review or a novelty verdict.

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

The following portions of the primary sources were read on 2026-10-24.

| Primary source and inspected result | Relevant hypotheses and scope |
| --- | --- |
| [Hairer and Majda, *A simple framework to justify linear response theory*, author version dated 17 February 2010](https://www.hairer.org/papers/FDT.pdf), Section 2, Assumptions 1--3, Theorem 2.3 and Remarks 2.4--2.7 | Differentiability of invariant expectations on a separable Banach space follows from a centered spectral gap in a weighted $C^1$ observable norm, an operator derivative into a weaker weighted continuous norm, and a uniform invariant integrability bound. A transition density is not required. The statement concerns a first derivative and is formulated for Markov semigroups. |
| [Ferre, Herve and Ledoux, *Regular perturbation of V-geometrically ergodic Markov chains*, author version dated 5 June 2012](https://herve.perso.math.cnrs.fr/Stab-FHL.pdf), (VG), Theorem 1 and Proposition 1 | The starting gap is in a weighted supremum norm over measurable observables. Theorem 1 adds a uniform drift bound and two-norm continuity. Proposition 1 treats higher regularity for an AR(1) family under explicit noise-density conditions, including bounded derivative-to-density ratios. |
| [Duncan, Nusken and Pavliotis, *Using Perturbed Underdamped Langevin Dynamics to Efficiently Sample from Probability Distributions*, J. Stat. Phys. 169 (2017), 1098--1131](https://pmc.ncbi.nlm.nih.gov/articles/PMC6959385/), Section 2.3, Lemma 2, Eqs. (22)--(25) | Poisson solutions and inverse operators represent asymptotic variance in their continuous-time diffusion setting. Their hypoellipticity and $L^2$-decay hypotheses are not imported into our history chain. This is a methodological precedent, not a theorem for our model. |

The Bernard--Wu full-theorem comparison and the aging-paper full text
remain unresolved as recorded in the
[source ledger](pre_reassessment_2026-10-19.md). These inspected sources
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
| Weighted observable gap and closure | The direct proof below controls odd polynomial-growth $C^1$ observables and a centered quadratic Poisson solution. It does not identify this space with the source's closure of cylindrical functions. |
| Parameter derivative and integrability | The needed polynomial operator differences and stationary expectations are bounded below; differentiability on the entire source space is not claimed. |
| Boundary and discrete time | The proof below works directly with discrete updates and $\tau\downarrow0$. No negative-variance extension or continuous-time embedding is used. |
| Transport and remainder order | The concrete resolvent expansion below gives an $O(\tau^2)$ remainder with constants uniform in $H$ in the original strict domain. |

For the specific AR(1) proposition in the second source, even the Gaussian
density fails its bounded-ratio assumption as written, since
$\nu'(x)/\nu(x)=-x$. This excludes that direct substitution, not other
Gaussian perturbation theorems or an adaptation of its proof.

## Why invariant-law response alone is insufficient

Here is the operator calculation motivating the extra work. Its concrete
observable version is established in the next section; we do not claim
differentiability of the whole resolvent in the source's operator norm.
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

## Direct proof for the needed observables

All norms in this section use the same $E_r$ and fixed contraction rate
$a<1$ as the validity note. Suppress $H$ in operators. Constants may
depend on the fixed kernel, memory, dimension and contraction margin,
but not on $H$ or $0\leq\tau\leq\tau_0$. The normalized deterministic
map $T_\tau$ is odd, $T_\tau(0)=0$ and $\|DT_\tau\|\leq a$.
The existing global Gaussian bounds give

$$
T_\tau(y)=Ay+\tau Q(y)+E_\tau(y),\qquad
\|T_\tau(y)-Ay\|\leq C_3\tau\|y\|^3,
$$

$$
\|D(T_\tau-A)(y)\|\leq3C_3\tau\|y\|^2,\qquad
\|E_\tau(y)\|\leq C_5\tau^2\|y\|^5,\qquad
\|DE_\tau(y)\|\leq5C_5\tau^2\|y\|^4.
$$

The history sums and their derivatives converge since $q<r^5$. These
are global bounds, not restrictions to bounded Gaussian trajectories.
The stationary common-innovation coupling also yields
$\|Y^\tau-W\|_{L^p(E_r)}=O(\tau)$ for every finite $p$: subtract the
linear recursion and sum the forcing bounded by
$C_3\tau\|Y^\tau\|^3$. Uniform stationary moments control its norm.
Consequently expectations of any fixed bounded multilinear polynomial
change by $O(\tau)$, using its polynomial difference estimate and Holder.

### Odd-observable resolvents

For $m=1,3,5$, let $\mathcal B_m$ be the space of odd, continuously
Frechet-differentiable scalar functions with finite norm

$$
\|f\|_m=\sup_y\left\{
\frac{|f(y)|}{1+\|y\|^m}
+\frac{\|Df(y)\|}{1+\|y\|^{m-1}}\right\}.
$$

This is a complete weighted $C^1$ space; convergence in this norm gives
locally uniform convergence of functions and derivatives. It is defined
directly, not as the cylindrical closure in the cited theorem. No
differentiation of the weight $\|y\|^m$ is needed.

For the chain started at $y$, contraction gives
$\|Y_n^y-Y_n^0\|\leq a^n\|y\|$ and
$\|D_yY_n^y\|\leq a^n$. Its zero-start moments are uniformly bounded
in $n,\tau,H$. Differentiating under the expectation, justified by these
moment bounds on bounded sets of initial states, therefore gives

$$
\|D(P_\tau^nf)(y)\|
\leq C_m a^n\|f\|_m(1+\|y\|^{m-1}).
$$

Symmetry gives $P_\tau^nf(0)=0$. Integrating this derivative along the
segment from zero to $y$ controls the value part of the norm. Thus

$$
\|P_\tau^nf\|_m\leq C_m a^n\|f\|_m,\qquad
R_\tau=\sum_{n\geq0}P_\tau^n:\mathcal B_m\to\mathcal B_m,
\qquad \|R_\tau\|\leq\frac{C_m}{1-a}.
$$

The series is a two-sided inverse of $I-P_\tau$ on this odd space.
For $g(y)=y_0^{(1)}$, the same estimate and stationary second moments
give absolute covariance summability. This establishes the MSD slope
and its resolvent representation without total-variation mixing.

### Quantitative resolvent expansion

Define $Jf(y)=\mathbb E[Df(Ay+e\xi)[Q(y)]]$ for the polynomials below.
Set $\ell=R_0g$, $s=J\ell$ and $r_3=R_0s$. The function $\ell$ is
linear and $s$ is cubic. The function $r_3$ is cubic plus linear: writing
$Y_n^y=A^ny+\zeta_n$ at $\tau=0$, Gaussian averaging of a cubic leaves
only a cubic term in $A^ny$ and a linear term containing the covariance
of $\zeta_n$. Their coefficients are summable, bounded respectively by
constants times $a^{3n}$ and $a^n$.

The displayed map bounds imply

$$
\|(P_\tau-P_0)\ell-\tau s\|_5\leq C\tau^2,
\qquad
\|(P_\tau-P_0)r_3\|_5\leq C\tau.
$$

For the second bound, integrate the derivative of the cubic polynomial
between $Ay+e\xi$ and $T_\tau(y)+e\xi$. Both deterministic endpoints
are bounded by $a\|y\|$; their difference is $O(\tau\|y\|^3)$.
This bounds values by $C\tau(1+\|y\|^5)$. Differentiating the difference
uses the quadratic first and linear second derivatives of $r_3$, and
$\|DT_\tau-A\|\leq3C_3\tau\|y\|^2$, giving
$C\tau(1+\|y\|^4)$. Gaussian moments control the innovation factors.
The first bound follows directly from $\ell(E_\tau)$ and its derivative.

Applying $I-P_\tau$ to $\ell+\tau r_3$ gives the exact residual identity

$$
R_\tau g-\ell-\tau r_3
=R_\tau\left[(P_\tau-P_0)\ell-\tau s
+\tau(P_\tau-P_0)r_3\right].
$$

All terms lie in $\mathcal B_5$, so the preceding resolvent bound proves
$\|R_\tau g-\ell-\tau r_3\|_5=O(\tau^2)$ uniformly in $H$.

### The stationary-law term

Let $h=g\ell-g^2/2=B(y,y)$ with its continuous symmetric bilinear form
$B$. The quadratic Poisson solution for the linear reference is explicit:

$$
u_h(y)=\sum_{n\geq0}
\left[B(A^ny,A^ny)-\mathbb E B(A^nW,A^nW)\right].
$$

Its bilinear coefficients and constant converge at rate $a^{2n}$, and
$(I-P_0)u_h=h-\nu_0h$. Expanding the quadratic polynomial using the
global map bounds gives

$$
|(P_\tau-P_0)u_h(y)-\tau Ju_h(y)|
\leq C\tau^2(1+\|y\|^6).
$$

Invariant integration, justified by the stationary moments, yields the
exact identity $\nu_\tau h-\nu_0h=\nu_\tau[(P_\tau-P_0)u_h]$.
The function $Ju_h$ is quartic. The common-innovation $O(\tau)$ estimate
therefore permits replacement of $\nu_\tau Ju_h$ by $\nu_0Ju_h$ with
error $O(\tau)$. Consequently

$$
\nu_\tau h=\nu_0h+\tau\nu_0Ju_h+O(\tau^2).
$$

Combining the two expansions, and using the same moment argument for
the degree-at-most-four polynomial $g r_3$, proves

$$
\boxed{\mathcal D_H(\tau)=\nu_0h
+\tau\{\nu_0Ju_h+\nu_0[g r_3]\}+O(\tau^2).}
$$

This supplies both response terms and the claimed $O(\varepsilon^6)$
transport remainder after multiplication by $\varepsilon^2$. It holds
also at $H=\infty$, with the same fixed-parameter uniformity as before.
There is no use of a negative $\tau$ or a functional central-limit theorem.

Both coefficient terms pair a cubic Gaussian observable with a linear
one. In the second term the pair is at different times, still jointly
Gaussian. Replacing $Q$ by its first Gaussian-chaos projection therefore
leaves both unchanged. That projection has first-coordinate gains
$-\eta\lambda(d+2)\gamma_j C_{jj}^{(H)}$ multiplying $L_j$.
The linear transfer derivative then recovers exactly the displayed
$D_4$ from the earlier projection audit, including the untruncated case.
No new transport coefficient is introduced.

This is a second analytical route using the same model assumptions and
Taylor/contraction bounds. It does not rely on the previous summable
residual-dependence estimate, but it is not an independent expert review.

### Finite-matrix controls

For the test implementation, use the finite lag matrix $A$, per-coordinate
covariance $C$, readout $e_1$, and projected cubic derivative matrix $J_c$.
Set $l=(I-A^T)^{-1}e_1$,
$B=(e_1l^T+le_1^T-e_1e_1^T)/2$, and solve
$M-A^TMA=B$. The two scalar contributions are

$$
L=2\operatorname{tr}(MACJ_c^T),\qquad
P=e_1^TC(I-A^T)^{-1}J_c^Tl.
$$

The tests use the existing helper's parameter $t=\beta\varepsilon^2$,
with $\beta=\eta M_H\lambda$: $L+P$ is per unit cubic gain, and
$\beta(L+P)$ is the physical $D_4$. Twelve cases cover $H=2,5,9$,
linear gains 0 and 0.2, and dimensions 1 and 3. They compare the sum to
the transfer derivative, the law term to the covariance derivative, and
the dual Lyapunov residual to zero. At zero gain the law term vanishes
but propagation does not. Two polynomial-exact Gaussian quadratures at
$(H,d)=(2,1),(3,2)$ check both terms directly with the cubic force and
reversed Gaussian regression, without using its projected force matrix.
These are synthetic coefficient checks, not a validation of a noise range.

## Consequence for the manuscript decision

The concrete response route is now supplied internally. This removes the
earlier need to leave its observable and transport estimates hypothetical;
it does not establish a verbatim import of either general theorem. The
review question is now sharper: **is this explicit controlled benchmark
scientifically useful enough for a paper, given that both its coefficient
and a rigorous proof route use established methods?** A generic method-
novelty claim is not supported. Neither is a claim that no useful
model-specific publication is possible.

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
The extended version passes 392 focused research/documentation tests,
including fourteen new matrix/quadrature cases, plus Ruff and the strict
documentation build. The matrix checks split the law and propagation
terms using a dual Lyapunov equation and compare
their sum with the existing transfer derivative. Small Gaussian quadrature
checks both terms directly against the cubic force. These checks audit
algebra, not the infinite-dimensional proof or physical interpretation.
Production code, frozen PDFs and target data are unchanged.
