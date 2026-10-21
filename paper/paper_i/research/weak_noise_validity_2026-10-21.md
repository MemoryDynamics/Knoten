# A sufficient domain for stationary weak-noise moments

Date: 2026-10-21. Internal analytical continuation of
`5d3a7aeeaa4664f26c047e9a59ae114a1578dd94`. No new model rule, production
trajectory, parameter scan or independent referee review.

## Result and boundary

For the full Gaussian force with canonical exponential point-deposition
memory, a **global contraction condition** supplies a unique stationary
relative law and an expansion of its quadratic moments through order
$\varepsilon^4$, with an $O(\varepsilon^6)$ remainder. The argument covers
both untruncated memory and every fixed truncation, with uniform bounds
over the truncation length at fixed model coefficients.

This is a sufficient, not necessary, condition. **None of the active
frozen Paper-I cells satisfies it.** The result does not retroactively
justify their stationary weak-noise interpretation. It also does not
justify the nonlinear long-time diffusion correction: an infinite-lag
transport interchange still needs a separate argument.

The contraction method is standard. The contribution here is an explicit
application and scope check for this model, not a claim of mathematical
priority or sufficient PRE novelty. It complements the broader
[finite-memory existence result](finite_memory_stationarity_2026-10-21.md),
which requires no small coupling but does not control vanishing noise.

## Model and sufficient condition

Use $q=1-\alpha$, $0<\alpha<1$, $\gamma_j=\alpha q^j$ and

$$
K(u)=A_r e^{-|u|^2/(2s_r^2)}-A_a e^{-|u|^2/(2s_a^2)},
\qquad s_r,s_a>0.
$$

Let $v_n=x_n-x_{n-1}$ and $V_n=(v_n,v_{n-1},\ldots)$. For
$L_j(V)=\sum_{i=0}^{j-1}v_i$, define

$$
F_H(V)=-\eta\sum_{1\leq j<H}\gamma_j\nabla K(L_j(V)),\qquad
V_{n+1}=\bigl(F_H(V_n)+\varepsilon\xi_{n+1},v_n,v_{n-1},\ldots\bigr).
$$

Here $H\in\{2,3,\ldots\}\cup\{\infty\}$ and
$\xi_n\sim\mathcal N(0,I_d)$ are independent innovations, independent of
the initial history. For finite $H$, the extra old increments are passive
coordinates; projecting onto the first $H-1$ gives the finite relative
state. The weights in the force are **not renormalized** after truncation;
the retained total mass, including age zero, is $M_H=1-q^H$, and
$M_\infty=1$. The age-zero force is zero. Startup with an unfilled memory
is not the stationary process treated here.

A global Hessian bound is

$$
G_2=\frac{|A_r|}{s_r^2}+\frac{|A_a|}{s_a^2},\qquad
\sup_u\|\nabla^2K(u)\|_{\rm op}\leq G_2.
$$

For one Gaussian its tangential eigenvalue has magnitude at most
$|A|/s^2$, and its radial eigenvalue is
$(A/s^2)(t-1)e^{-t/2}$, $t=|u|^2/s^2$. The inequality
$|(t-1)e^{-t/2}|\leq1$ proves the bound. Set $s=|\eta|G_2$ and require

$$
\boxed{\theta=s\frac{q}{\alpha}<1.}
$$

This uses the global Hessian, not just the signed local curvature
$\kappa=A_a/s_a^2-A_r/s_r^2$ or the local gain $g=\eta M_H\kappa$.
A different overall deposited mass must also multiply $s$.

## Weighted-history contraction

Choose a number $r$ satisfying

$$
\max\left(q^{1/5},\frac{q}{1-sq}\right)<r<1.
$$

Such a choice exists when $\theta<1$: $sq<\alpha$ implies
$1-sq>q$. Work on the complete separable space

$$
E_r=\{V:r^i v_i\longrightarrow0\},\qquad
\|V\|_r=\sup_{i\geq0}r^i|v_i|.
$$

This is a weighted copy of $c_0(\mathbb N;\mathbb R^d)$. Write
$S_j(r)=\sum_{i=0}^{j-1}r^{-i}$. Then
$|L_j(V)-L_j(W)|\leq S_j(r)\|V-W\|_r$ and

$$
\sum_{j\geq1}\alpha q^j S_j(r)=\frac{q}{1-q/r}.
$$

The sum follows by exchanging positive series and summing over
$j\geq i+1$. Therefore, uniformly in $H$,

$$
|F_H(V)-F_H(W)|\leq L_r\|V-W\|_r,\qquad
L_r=\frac{sq}{1-q/r}<1.
$$

The history shift has norm $r$. With a common innovation, the full update
$T_{H,\varepsilon}$ satisfies

$$
\|T_{H,\varepsilon}(V,\xi)-T_{H,\varepsilon}(W,\xi)\|_r
\leq a\|V-W\|_r,\qquad a=\max(r,L_r)<1.
$$

The infinite force is well defined: its bounded summands have summable
weights. The Lipschitz estimate also gives continuity; shifting and adding
one finite coordinate preserves $E_r$.

### Stationary construction and moments

Construct backward iterates from zero using a two-sided iid innovation
sequence. Adding one earlier update changes the result by at most
$a^m\varepsilon|\xi_{-m}|$ after $m$ contractions. The sum of these bounds
converges almost surely and in every $L^p$, $1\leq p<\infty$. Its limit is
a stationary causal process $V^{\varepsilon,H}$, and Minkowski's inequality
gives

$$
\|V^{\varepsilon,H}\|_{L^p(E_r)}
\leq\frac{\varepsilon\|\xi\|_{L^p(\mathbb R^d)}}{1-a}.
$$

Any two initial histories coupled to the same future innovations approach
each other at rate $a^n$. Coupling two invariant laws and testing bounded
Lipschitz functions then proves uniqueness without assuming a moment of
an arbitrary second invariant law. The constructed invariant law already
has all finite moments by the displayed estimate. At $\varepsilon=0$ it
is concentrated on the zero-increment history. Thus competing nonzero
deterministic recurrent relative states are excluded in this domain.

This is the uniformly contractive specialization of the iterated-random-
functions framework. See Diaconis and Freedman,
[Theorem 1 and Proposition 1, author report dated 3 May 1998](https://statistics.berkeley.edu/sites/default/files/tech-reports/511.pdf),
Section 1 inspected on 2026-10-21. The model-specific norm, constants and
moment/Taylor argument here are given explicitly rather than attributed
to that source. This is a real-valued stochastic-law result, not a theorem
about a finite-state PRNG implementation or absolute-position stationarity.

## Controlled moment expansion

Fix $\alpha$, the kernel and $\eta$ in the strict domain above. Define

$$
\kappa=\frac{A_a}{s_a^2}-\frac{A_r}{s_r^2},\qquad
\lambda=\frac{A_r}{2s_r^4}-\frac{A_a}{2s_a^4}.
$$

Let $A_H$ be the derivative at zero of the noise-free increment-history
map, including the shift, so $\|A_H\|\leq a$. The cubic term is the vector
whose first coordinate is

$$
Q_H(V)_0=-\eta\lambda\sum_{1\leq j<H}
\gamma_j |L_j(V)|^2 L_j(V),
$$

and whose other coordinates vanish. The full noise-free map is
$T_{H,0}(V)=A_HV+Q_H(V)+R_H(V)$. For all $u$,

$$
|\nabla K(u)-\kappa u|
\leq c_3|u|^3,\qquad
c_3=\frac{|A_r|}{2s_r^4}+\frac{|A_a|}{2s_a^4},
$$

$$
|\nabla K(u)-\kappa u-\lambda|u|^2u|
\leq c_5|u|^5,\qquad
c_5=\frac{|A_r|}{8s_r^6}+\frac{|A_a|}{8s_a^6}.
$$

These follow from $1-e^{-z}\leq z$ and
$|e^{-z}-1+z|\leq z^2/2$ for $z\geq0$, not from restricting the noise to
a bounded neighborhood. Since $q<r^5$,
$\sum_j\gamma_j S_j(r)^m<\infty$ for $m=3,5$. Consequently there are
constants independent of $H$ with

$$
\|T_{H,0}(V)-A_HV\|_r\leq C_3\|V\|_r^3,\qquad
\|R_H(V)\|_r\leq C_5\|V\|_r^5,
$$

$$
\|Q_H(V)-Q_H(W)\|_r
\leq C_Q(\|V\|_r^2+\|W\|_r^2)\|V-W\|_r.
$$

For example $C_m=|\eta|c_m\sum_{j\geq1}\gamma_j S_j(r)^m$ works
in the first two bounds. These constants may be very large near the
contraction boundary; no practical finite-noise accuracy is asserted.

On the same innovations define the stationary linear process and its
cubic response by

$$
W_{n+1}=A_HW_n+e\xi_{n+1},\qquad
Z_{n+1}=A_HZ_n+Q_H(W_n),
$$

where $e$ inserts a $d$-vector in the first history coordinate. Their
convergent backward series have every finite moment. Subtracting the
recursions and summing the stable linear propagator gives, for every
fixed $p\geq1$,

$$
\|V^{\varepsilon,H}-\varepsilon W\|_{L^p(E_r)}
=O(\varepsilon^3).
$$

Indeed the forcing is bounded by $C_3\|V^{\varepsilon,H}\|_r^3$,
whose $L^p$ norm is $O(\varepsilon^3)$ by the $3p$ moment bound. In the
next subtraction the forcing is
$Q_H(V^{\varepsilon,H})-Q_H(\varepsilon W)+R_H(V^{\varepsilon,H})$.
The cubic difference estimate, Holder's inequality and the preceding
bound at higher moments make it $O_{L^p}(\varepsilon^5)$. Thus

$$
\boxed{V^{\varepsilon,H}
=\varepsilon W+\varepsilon^3Z+O_{L^p(E_r)}(\varepsilon^5).}
$$

All constants can be chosen independently of $H$ at the fixed parameters.
The full Gaussian dynamics, not an iterated cubic surrogate, is being
expanded. For every continuous bilinear form $B$ on $E_r$ this
implies

$$
\mathbb E B(V^{\varepsilon,H},V^{\varepsilon,H})
=\varepsilon^2\mathbb E B(W,W)
+\varepsilon^4\mathbb E[B(W,Z)+B(Z,W)]
+O(\varepsilon^6).
$$

Oddness of the force and symmetry of the innovations give zero means,
so quadratic lag moments are covariances. The same expansion holds at
each fixed time lag. It does not, by itself, bound the remainder summed
over infinitely many time lags.

### Connection to the finite covariance helper

For finite $H$, the invertible cumulative-sum map from increments to lags
puts the linear covariance and first correction into the Lyapunov
equations of the [nonlinear calculation](pre_reassessment_2026-10-19.md).
With $w_j=\gamma_j/M_H$ and $\beta=\eta M_H\lambda$, the Wick calculation
there identifies

$$
\operatorname{Cov}(L^a)
=\varepsilon^2 C+\beta\varepsilon^4 C_1+O(\varepsilon^6).
$$

This now has a stationary justification **in the contraction domain**.
The numerical helper also restricts $0\leq g<1$; that additional software
domain is unchanged and is not equivalent to $\theta<1$.

For untruncated memory the relative-position and cloud quadratic
functionals are continuous on $E_r$ because
$\sum_j\gamma_j S_j(r)^2<\infty$. Their moment expansions therefore
also follow. This is not a numerical evaluation or independent validation
of an infinite-dimensional correction coefficient. Finite normalized
radius weights are uniformly bounded by $\gamma_j/M_2$, so the analogous
quadratic error bounds can be uniform over $H\geq2$.

## A restricted truncation bound

For comparison on the same infinite-history space, set
$G_1=e^{-1/2}(|A_r|/s_r+|A_a|/s_a)$. The omitted force satisfies
$|F_\infty(V)-F_H(V)|\leq|\eta|G_1q^H$. Coupling stationary backward
constructions with the same innovations yields

$$
\|V^{\varepsilon,\infty}-V^{\varepsilon,H}\|_{L^p(E_r)}
\leq\frac{|\eta|G_1 q^H}{1-a}.
$$

This is a weak-coupling horizon statement at fixed $\alpha$, with the
canonical unnormalized force weights. It does not solve the separate
FIFO rotating-branch horizon problem. Here the zero-noise relative state
is globally contracting; a nonzero rotating recurrent state cannot be
covered by this certificate. No G1--G5 or P5 status changes follow.

## Archived-condition audit

The frozen [trace manifest](../evidence/trace_manifest.json) has
$\alpha=0.01$, $H=600$, $\eta=0.15$, $A_r=1$, $s_r=1$, $s_a=3$ in its
active cells. Its gain and retained mass recover this $\eta$. The
metadata give:

| $A_a$ | $\theta=\lvert\eta\rvert G_2q/\alpha$ | Threshold $\alpha/(qG_2)$ for $\lvert\eta\rvert$ (rounded) | Covered? |
| --- | --- | --- | --- |
| 20 | 47.85 | 0.0031347962 | No |
| 35 | 72.60 | 0.0020661157 | No |

The $\eta=0$ controls satisfy the condition trivially. Failing a sufficient
bound proves neither actual instability nor failure of the formal
expansion. Conversely, local $g<1$ and agreement of terminal radii do not
supply the missing global argument. These figures come from existing
metadata, not new trajectory outcomes or a search for a favorable regime.

## Verification and next decision

The floating-point `exponential_contraction_diagnostic` in
[weak_nonlinearity.py](../scripts/weak_nonlinearity.py) reports the budget,
weighted-history decay and contraction rate. It is not an interval
certificate; unresolved near-boundary cases return no rate. Nineteen
additional synthetic checks cover the strict domain, weighted norms of
the existing lag matrix, production-kernel Hessians, archived-condition
exclusion, unresolved floating-point rates and invalid inputs. Together
with the earlier stationarity and weak-response checks, 49 research tests
pass locally. Eight baseline and ten documentation/claim/evidence checks
also pass (67 total), as do Ruff and the strict documentation build, using
NumPy 2.3.5, SciPy 1.16.3 and pytest 8.4.2. These checks audit implementation
and algebra, not the general proof or physical validity of the model.

The next scientific decision is whether this restricted kernel-sensitive
moment result adds enough beyond the closest literature to support a
revised Paper I, or whether a stronger/local-branch theorem is essential.
Transport, finite-noise accuracy and the full-text aging-paper comparison
remain open. No parameter panel or new trajectory run is authorized by
this note. Frozen PDFs and data remain unchanged, and there is no new
bridge to gravity or quantum theory.
