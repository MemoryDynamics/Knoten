# A sufficient domain for stationary weak-noise moments and transport

Date: 2026-10-21. Internal analytical continuation of
`5d3a7aeeaa4664f26c047e9a59ae114a1578dd94`. No new model rule, production
trajectory, parameter scan or independent referee review. The transport
extension below follows the moment-only version published at `eedd403`.

## Result and boundary

For the full Gaussian force with canonical exponential point-deposition
memory, a **global contraction condition** supplies a unique stationary
relative law and an expansion of its quadratic moments through order
$\varepsilon^4$, with an $O(\varepsilon^6)$ remainder. The argument covers
both untruncated memory and every fixed truncation, with uniform bounds
over the truncation length at fixed model coefficients.

This is a sufficient, not necessary, condition. **None of the active
frozen Paper-I cells satisfies it.** The result does not retroactively
justify their stationary weak-noise interpretation. A separate summable-
remainder argument below now also justifies the nonlinear long-time
diffusion correction in this same strict domain. A fixed-lag moment bound
alone would not justify that interchange.

The later positive-averaging extension in the
[finite-memory note](finite_memory_stationarity_2026-10-21.md) does cover
the archived model coefficients for fixed-$H$ stationary moments as noise
vanishes. It supplies neither a practical finite-noise tolerance there nor
the untruncated and transport conclusions established in this note's domain.

The contraction method is standard. The contribution here is an explicit
application and scope check for this model, not a claim of mathematical
priority or sufficient PRE novelty. It complements the broader
[finite-memory existence result](finite_memory_stationarity_2026-10-21.md),
whose minorization alone requires no small coupling but does not control
vanishing noise.

Scope update 2026-10-24: the
[response-theory audit](linear_response_scope_audit_2026-10-24.md) compares
this argument with two established frameworks. In particular, the
weighted-history contraction here is not total-variation mixing on the
full history. The explicit summable transport remainder, rather than
stationary differentiability alone, is the claim to assess for added value.

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
each fixed time lag. The additional estimates in the transport section
are needed to control the remainder summed over infinitely many time lags.

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

## Summable remainder and transport

The claim here concerns the per-coordinate stationary MSD slope, with one
update as the unit of time:

$$
D_H(\varepsilon)=\lim_{N\to\infty}\frac{1}{2N}
\mathbb E\left[\left(\sum_{n=1}^N v_n^a\right)^2\right].
$$

All parameters other than $\varepsilon$ remain fixed in $\theta<1$.
This is not a simultaneous continuous-time or $\alpha\to0$ limit.

### Derivative bounds and one-innovation coupling

For the same constants $c_3,c_5$ above, differentiating the Gaussian
remainders gives the global bounds

$$
\|\nabla^2K(u)-\kappa I\|_{\rm op}\leq3c_3|u|^2,
$$

$$
\|\nabla^2K(u)-\kappa I-
\lambda(|u|^2I+2uu^T)\|_{\rm op}\leq5c_5|u|^4.
$$

For a single Gaussian the second inequality follows by bounding the two
terms $(e^{-z}-1+z)I$ and
$-(e^{-z}-1)uu^T/s^2$ with $z=|u|^2/(2s^2)$. Their bounds sum to
$5|A||u|^4/(8s^6)$. Termwise differentiation on bounded subsets of $E_r$
is justified by the same summable third- and fifth-power history bounds.
Thus, for $N_H(V)=T_{H,0}(V)-A_HV$,

$$
\|DN_H(V)\|\leq3C_3\|V\|_r^2,\qquad
\|DR_H(V)\|\leq5C_5\|V\|_r^4.
$$

Replace only $\xi_0$ by an independent copy, keeping all other innovations
the same, and mark the coupled process with a star. For an $E_r$-valued
process $X$ set $\delta_p(X,k)=\|X_k-X_k^*\|_{L^p(E_r)}$. The contraction
and the linear propagator imply, for $k\geq0$,

$$
\delta_p(V^{\varepsilon,H},k)\leq C_p\varepsilon a^k,
\qquad \delta_p(W,k)\leq C_p a^k.
$$

Set $U^\varepsilon=V^{\varepsilon,H}-\varepsilon W$ and
$E^\varepsilon=V^{\varepsilon,H}-\varepsilon W-\varepsilon^3 Z$.
At time zero, $U^\varepsilon-U^{\varepsilon,*}$,
$Z-Z^*$ and $E^\varepsilon-E^{\varepsilon,*}$ vanish: the new innovation
enters $V$ and $\varepsilon W$ in exactly the same additive way, and $Z_0$
uses only earlier innovations. The recurrence

$$
U^\varepsilon_{n+1}=A_HU^\varepsilon_n+N_H(V^{\varepsilon,H}_n)
$$

and the derivative bound, combined with the stationary moment bounds and
Holder's inequality, give forcing differences
$O_{L^p}(\varepsilon^3 a^n)$. Convolution with $A_H^{k-1-n}$ therefore gives

$$
\delta_p(U^\varepsilon,k)\leq C_p\varepsilon^3(k+1)a^k,
\qquad \delta_p(Z,k)\leq C_p(k+1)a^k.
$$

For clarity, the cubic-difference estimate needed in the next subtraction
is stronger than bounding each cubic term separately. Write
$Q_H(V)=\mathcal B_H(V,V,V)$ with a bounded symmetric trilinear map.
Then $Q_H(V)-Q_H(Y)$ is a sum of three terms each containing $V-Y$.
Apply this with $Y=\varepsilon W$ and compare its starred version. Every
term contains either a coupled difference of $U^\varepsilon$ times two
$O_{L^p}(\varepsilon)$ factors, or an $O_{L^p}(\varepsilon^3)$ factor
times a coupled difference of $V$ or $\varepsilon W$ and one further
$O_{L^p}(\varepsilon)$ factor. Using higher moments where required gives
$O_{L^p}(\varepsilon^5(k+1)a^k)$. The coupled fifth-order remainder is
$O_{L^p}(\varepsilon^5a^k)$ by the derivative bound. A second stable
convolution establishes

$$
\boxed{\delta_p(E^\varepsilon,k)
\leq C_p\varepsilon^5(k+1)^2a^k.}
$$

Factors $a^{-1}$ or $a^{-2}$ from the convolution are absorbed into the
constant; $a>0$ is fixed. Constants can be uniform over $H$ and
$0<\varepsilon\leq\varepsilon_0$, not over approach to $\theta=1$ or
$\alpha=0$. This is the extra estimate absent from a fixed-lag expansion.

### From dependence to the covariance sum

Now use scalar coordinates of the processes and define
$\Delta_2(X)=\sum_{k\geq0}\|X_k-X_k^*\|_2$. For centered, jointly causal
stationary processes driven by the same iid innovations,

$$
\sum_{k\in\mathbb Z}|\operatorname{Cov}(X_0,Y_k)|
\leq\Delta_2(X)\Delta_2(Y).
$$

Here is the argument rather than an assumed mixing-rate interchange.
Let $\mathcal F_j=\sigma(\xi_i:i\leq j)$ and
$P_jX=\mathbb E[X\mid\mathcal F_j]-\mathbb E[X\mid\mathcal F_{j-1}]$.
Independent resampling and conditional Jensen give
$\|P_0X_n\|_2\leq\|X_n-X_n^*\|_2$. The iid remote-past tail is trivial,
so the centered causal variable has the orthogonal expansion
$X_n=\sum_{j\leq n}P_jX_n$. Consequently

$$
|\operatorname{Cov}(X_0,Y_k)|
\leq\sum_{m\geq\max(0,-k)}
\delta_2(X,m)\delta_2(Y,k+m).
$$

Summing this nonnegative double series gives the product bound. The
resampling/projection method is standard; see Wu,
[Nonlinear system theory: Another look at dependence (2005)](https://www.stat.uchicago.edu/~wbwu/papers/0506715102v1.pdf),
Definitions 1--3 and Theorem 1, inspected on 2026-10-21. The small-noise
orders and the Gaussian-memory derivative bounds here are our explicit
specialization, not results claimed from that source.

Let $w,z,e^\varepsilon$ be the first history coordinate and one spatial
component of $W,Z,E^\varepsilon$. The estimates above imply
$\Delta_2(w),\Delta_2(z)=O(1)$ and
$\Delta_2(e^\varepsilon)=O(\varepsilon^5)$. For
$\Gamma(X,Y)=\sum_{k\in\mathbb Z}\operatorname{Cov}(X_0,Y_k)$, expansion
of $v^a=\varepsilon w+\varepsilon^3z+e^\varepsilon$ now gives

$$
D_H(\varepsilon)=\frac{\varepsilon^2}{2}\Gamma(w,w)
+\frac{\varepsilon^4}{2}[\Gamma(w,z)+\Gamma(z,w)]
+O(\varepsilon^6).
$$

In particular the potentially problematic $w$--remainder covariance sum
is $O(\varepsilon^6)$ after its prefactor. The $z$--$z$ contribution is
also of that order. Absolute covariance summability justifies the MSD
slope limit by the usual triangular covariance sum. This proves a
stationary transport coefficient and its expansion, not a functional
central-limit theorem, a practical burn-in or a finite-noise accuracy bound.

### Identifying the coefficient

Write $C_{jj}^{(H)}$ for the per-coordinate unit-noise variance of the
linear lag $L_j(W)$. Its cubic force has first Gaussian-chaos projection
$(d+2)C_{jj}^{(H)}L_j(W)$. The remaining cubic chaos is orthogonal to every
linear Gaussian observable at every time. Hence the cross-covariance
coefficient equals the response to replacing the lag-force gains by

$$
\eta\gamma_j\kappa\longmapsto
\eta\gamma_j\kappa+\varepsilon^2\eta\gamma_j\lambda(d+2)C_{jj}^{(H)}.
$$

This is a coefficient calculation, not a finite-noise Gaussian closure.
The perturbed linear operator is still contractive for sufficiently small
perturbation because its added operator is bounded on $E_r$.
Its zero-frequency transfer is the reciprocal of one plus the first age
moment of the lag gains. Thus, with
$\mu_H=\sum_{1\leq j<H}j\gamma_j$ and
$S_H=\sum_{1\leq j<H}j\gamma_j C_{jj}^{(H)}$,

$$
\boxed{D_H(\varepsilon)=
\frac{\varepsilon^2}{2(1+\eta\kappa\mu_H)^2}
-\varepsilon^4\frac{\eta\lambda(d+2)S_H}
{(1+\eta\kappa\mu_H)^3}+O(\varepsilon^6).}
$$

Both age sums converge at $H=\infty$ by the weighted-history estimates.
The denominator is positive, since $|\eta\kappa\mu_H|\leq\theta<1$.
This also recovers the earlier finite-matrix response formula with
$g=\eta M_H\kappa$ and $\beta=\eta M_H\lambda$.

### Closed untruncated coefficient

For $H=\infty$, set $g_\infty=\eta\kappa$ and
$\rho=q(1-g_\infty)$. The unit-noise linear increments obey the exact
ARMA relation
$w_n=\rho w_{n-1}+\xi_n-q\xi_{n-1}$, with $|\rho|<1$ in the strict
domain. Their covariance is

$$
c_0=1+\frac{(\rho-q)^2}{1-\rho^2},\qquad
c_k=\frac{(\rho-q)(1-q\rho)}{1-\rho^2}\rho^{k-1},\quad k\geq1.
$$

Therefore $C_{jj}^{(\infty)}=jc_0+2\sum_{k=1}^{j-1}(j-k)c_k$.
Summing the geometric series and their first two age moments gives

$$
\mu_\infty=\frac q\alpha,\qquad
S_\infty=
\frac{q\{\alpha(1+4q+q^2)+q(q^2+2q-1)(1-\rho)\}}
{\alpha(1-\rho)(1+\rho)(1-q\rho)}.
$$

At $g_\infty=0$ this reduces to $q(1+q)/\alpha^2$, the weighted second
age of Brownian increments. The implementation checks linear stability
but does not itself certify the full nonlinear contraction hypothesis.

For the existing matched-curvature kernels $(A_r,A_a)=(0,26)$ and $(1,35)$
with $s_r=1,s_a=3$, $\kappa=26/9$ is identical while
$\lambda=-13/81$ and $23/81$. At the same $\eta>0$, memory and dimension
inside both contraction domains, $S_H>0$. Their leading transport
corrections are therefore respectively positive and negative, with ratio
$-23/13$. The comparison is to their common linear diffusion reference,
not to the Brownian control; this predicts neither superdiffusion nor a
new phase. These are asymptotic coefficients, not a finite-noise data test.

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

The [2026-10-22 external-review audit](external_review_audit_2026-10-22.md)
reproduces the closed coefficients but finds a fixed-lag/long-time
estimand mismatch in the suggested numerical panel. A Gaussian expected
force remainder does not replace the summable transport remainder proved
here. Explicit finite-noise constants and paired-estimator precision
remain required; no target run is authorized by that review.

The floating-point `exponential_contraction_diagnostic` in
[weak_nonlinearity.py](../scripts/weak_nonlinearity.py) reports the budget,
weighted-history decay and contraction rate. It is not an interval
certificate; unresolved near-boundary cases return no rate. Nineteen
additional synthetic checks cover the strict domain, weighted norms of
the existing lag matrix, production-kernel Hessians, archived-condition
exclusion, unresolved floating-point rates and invalid inputs. Together
with the earlier stationarity and weak-response checks, the moment-only
version passed 49 research tests and 18 baseline/documentation checks.
The transport extension adds 22 checks: production-Hessian remainder
bounds; comparison with a two-state covariance recurrence matching the
existing visible-MSD reference; a long finite-history Lyapunov calculation;
Brownian weighted-age controls; the matched-kernel sign and ratio; and
invalid domains. All 71 research tests and 18 baseline/documentation checks
pass locally (89 total), as do Ruff and the strict documentation build,
with NumPy 2.3.5, SciPy 1.16.3 and pytest 8.4.2. These are algebraic
and deterministic covariance calculations, not sampled trajectories or
tests of the general proof or physical validity of the model.

The next scientific decision is whether this restricted kernel-sensitive
moment/transport result adds enough beyond the closest literature to
support a revised Paper I, or whether a stronger/local-branch theorem is
essential.
The transport interchange is now supported only in the strict domain;
finite-noise accuracy, the archived active regime and the full-text aging-
paper comparison remain open. No parameter panel or new trajectory run is
authorized by this note. Frozen PDFs and data remain unchanged, and there is no new
bridge to gravity or quantum theory.
