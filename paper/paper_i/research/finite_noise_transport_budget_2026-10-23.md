# An explicit finite-noise transport and estimator budget

Date: 2026-10-23. Continuation of `8e964db`. No new model rule, target
trajectory, parameter search or independent mathematical review. The
inequalities below concern real arithmetic and iid Gaussian innovations;
their numerical evaluation is floating point, not an interval certificate.

## Result and decision boundary

The strict-contraction argument can be made quantitative for both the
**random paired estimator** and the **nonlinear long-time transport**.
A coupling also controls a particular initialized process: a completely
prefilled memory of coincident points, with the canonical weights already
present. This is not the production runner's empty-memory startup.

For the already discussed kernel pair and counts, these conservative
bounds give a nonempty sufficient noise interval for an illustrative
10% relative radius at 95% coverage. Its upper endpoint is about
$4.46\,10^{-6}$, far below the proposed $0.007$. At that endpoint the
leading contrast is only about $9.54\,10^{-10}$ of the common linear
diffusion. Thus a useful mathematical bound does not establish a usable
floating-point experiment. The next gate is cancellation-safe paired
arithmetic and its numerical error/cost, alongside the unresolved novelty
comparison, not an authorized billion-update run. Failure of these
conservative bounds at $0.007$ does not falsify the expansion there.

## Positive filters and lag moments

Use the model, canonical unnormalized $\gamma_j=\alpha q^j$, $q=1-\alpha$,
and $\kappa,\lambda,G_2,c_3,c_5$ of the
[weak-noise validity note](weak_noise_validity_2026-10-21.md). Here $H$ is
fixed and finite. Let $s=|\eta|G_2$ and assume $\theta=sq/\alpha<1$.
The increment feedback Lipschitz coefficients are bounded by $sq^k$,
$k\geq1$, because $\sum_{j\geq k}\gamma_j=q^k$. The corresponding
nonnegative impulse envelope is

$$
h_0=1,\quad h_k=sq r_f^{k-1}\ (k\geq1),\qquad
r_f=q+sq<1,\quad T_f=\sum_kh_k=(1-\theta)^{-1}.
$$

The linear signed impulse has absolute sum at most
$T_l=(1-|\eta\kappa|q/\alpha)^{-1}$. These untruncated envelopes also
dominate every finite canonical truncation. The numerical covariance
helper additionally requires $0\leq \eta M_H\kappa<1$.

Write $m_p=(\mathbb E|N(0,I_d)|^p)^{1/p}$. A stationary increment has
$\|v\|_p\leq\varepsilon T_fm_p$ by the positive feedback inequality.
The map from all innovations to a block of $j$ increments summed as a
single vector has Euclidean Lipschitz constant at most
$\varepsilon\|\mathbf1_j*h\|_2\leq\varepsilon T_f\sqrt j$.
For a centered Gaussian-input vector map with Jacobian operator norm at
most $L$, Gaussian rotation gives $\|F\|_p\leq(\pi/2)Lm_p$.
Indeed rotate independent $G,G'$ through a quarter circle, integrate
$DF(G_t)\dot G_t$, and apply conditional Gaussian comparison and
Minkowski/Jensen. $G_t$ and $\dot G_t$ are independent standard Gaussians.
Backward finite-history maps are odd, hence centered; their $L^p$ limits
preserve the bound. This is the standard Gaussian Pisier inequality, not
a new concentration theorem; see
[Ivanisvili, van Handel and Volberg, arXiv v2, section 1.1, (1.2) and the rotation argument](https://arxiv.org/pdf/2003.06345),
inspected on 2026-10-23.

Consequently, with $C$ the exact unit-noise linear lag covariance, define

$$
R_j=T_f\min(j,\tfrac\pi2\sqrt j),\qquad S_j=\sqrt{C_{jj}}.
$$

Then $\|L_jv\|_p\leq\varepsilon m_pR_j$ and
$\|L_jW\|_p=m_pS_j$. Replacing one innovation by an independent copy
also gives

$$
\Delta_p(L_jv)\leq\varepsilon\sqrt2m_pjT_f,\qquad
\Delta_p(L_jW)\leq\sqrt2m_pjT_l,
$$

where $\Delta_p(X)=\sum_{k\geq0}\|X_k-X_k^*\|_p$ uses vector norms.

## Explicit increment remainders

On common innovations write $v=\varepsilon W+\varepsilon^3Z+E$ and
$U=v-\varepsilon W$. **Here $Z$ includes $\eta\lambda$**: it equals
$\beta Z_{\mathrm{unit}}$ for the unit-$\beta$ process in the
[paired-reference note](paired_transport_feasibility_2026-10-22.md), with
$\beta=\eta M_H\lambda$. All sums below run from $j=1$ to $H-1$.
Set $a_3=|\eta|c_3$, $a_5=|\eta|c_5$, $a_\lambda=|\eta\lambda|$ and

$$
u_p=T_la_3m_{3p}^3\sum_j\gamma_jR_j^3,\qquad
z_p=T_la_\lambda m_{3p}^3\sum_j\gamma_jS_j^3,
$$

$$
e_p=T_l\left[
a_\lambda u_{3p}m_{3p}^2\sum_j\gamma_jj(R_j^2+R_jS_j+S_j^2)
+a_5m_{5p}^5\sum_j\gamma_jR_j^5\right].
$$

Then $\|U\|_p\leq\varepsilon^3u_p$, $\|Z\|_p\leq z_p$ and
$\|E\|_p\leq\varepsilon^5e_p$. To see the last assertion, represent
$f(x)=|x|^2x$ by its symmetric trilinear form
$B(a,b,c)=((a\cdot b)c+(a\cdot c)b+(b\cdot c)a)/3$, of norm at most
$|a||b||c|$. Expand $f(X)-f(Y)$ into the three terms containing
$X-Y$, take $X=L_jv$, $Y=\varepsilon L_jW$, use
$\|L_jU\|_{3p}\leq j\varepsilon^3u_{3p}$ and Holder, then convolve
with the linear impulse. The fifth-order global force remainder supplies
the second term. No bounded-support noise or cubic surrogate is used.

For dependence define

$$
dU_p=3\sqrt2a_3T_lT_fm_{3p}^3\sum_j\gamma_jjR_j^2,
\qquad
dZ_p=3\sqrt2a_\lambda T_l^2m_{3p}^3\sum_j\gamma_jjS_j^2,
$$

$$
\begin{aligned}
dE_p=T_l\bigg\{a_\lambda m_{3p}^2\bigg[&
dU_{3p}\sum_j\gamma_jj(R_j^2+R_jS_j+S_j^2)\\
&+\sqrt2u_{3p}\sum_j\gamma_jj^2
\{(2R_j+S_j)T_f+(R_j+2S_j)T_l\}\bigg]\\
&+5\sqrt2a_5T_fm_{5p}^5\sum_j\gamma_jjR_j^4\bigg\}.
\end{aligned}
$$

These bound $\Delta_p(U)/\varepsilon^3$, $\Delta_p(Z)$ and
$\Delta_p(E)/\varepsilon^5$. The derivative bounds $3c_3|x|^2$ and
$5c_5|x|^4$ are global. Integrating the derivative between two coupled
lags uses the same moment bound for each convex interpolation, so does
not require independence between the lag and its difference. For $dE$,
the three cubic difference terms each yield three coupled product terms.
Those with $\delta U$ give the first sum; those with $\delta X$ or
$\delta Y$ give respectively $2R+S$ and $R+2S$. The fifth-order force
gives the last sum. Absolute summation and the linear filter contribute
$T_l$. This specifies the constants in the previous summable-rest proof.

## Transport and random estimator

The scalar-coordinate linear dependence sum is bounded by
$dW=\sqrt2T_l$. Vector bounds $dZ=dZ_2$, $dE=dE_2$ also bound each
coordinate. The causal covariance-product inequality in the validity
note gives the explicit transport remainder

$$
|D(\varepsilon)-\varepsilon^2D_2-\varepsilon^4D_4|
\leq\varepsilon^6(\tfrac12dZ^2+dW\,dE)
+\varepsilon^8dZ\,dE+\tfrac12\varepsilon^{10}dE^2.
$$

For a raw block-MSD estimator of length $m$, put
$w_m=m_4T_l\sqrt m$, $z=z_4$, $e=e_4$. Its expansion through order
$\varepsilon^4$ has **random $L^2$ remainder** bounded by

$$
\varepsilon^6 A_m+\varepsilon^8B_m+\varepsilon^{10}C_m,\qquad
A_m=\frac{w_me}{d}+\frac{mz^2}{2d},\quad
B_m=\frac{mze}{d},\quad C_m=\frac{me^2}{2d}.
$$

Expand $|\varepsilon W_m+\varepsilon^3Z_m+E_m|^2/(2dm)$ and
apply Holder with $\|Z_m\|_4\leq mz$ and
$\|E_m\|_4\leq\varepsilon^5me$. Block/seed averaging cannot increase
this bound by Minkowski; **no independence or variance reduction for the
remainder is assumed**. The two-length estimator
$\widehat D_T=2\widehat D_{2L}-\widehat D_L$ therefore has coefficients
$2(A_{2L},B_{2L},C_{2L})+(A_L,B_L,C_L)$.

For two kernels driven by the same innovations and with matched $\kappa$,
the linear statistic cancels pathwise. Add the two remainder bounds,
divide by $|\Delta D_4|$, and set $t=\varepsilon^2$. This defines the
relative estimator and transport polynomials
$e_{\rm est}(t)=a_et+b_et^2+c_et^3$ and
$e_D(t)=a_Dt+b_Dt^2+c_Dt^3$. The leading normalized statistic is the
common $\overline Q/m_\infty$ of the
[finite-sample reference](finite_block_transport_bound_2026-10-22.md).

## Fully prefilled flat initialization

Set every increment $v_n=0$ for $n\leq0$ and give every age its canonical
weight from the first update. Couple future innovations to the stationary
process. The initial stationary increment norm is at most
$\varepsilon T_fm_p$. The positive Volterra recursion then implies

$$
\|v_n^{\rm flat}-v_n^{\rm stat}\|_p
\leq\varepsilon T_fm_p\theta r_f^{n-1},\qquad n\geq1.
$$

For example, the infinite prehistory contributes $\theta q^{n-1}$ after
normalization; adding the intervening positive convolution solves to
$\theta r_f^{n-1}$. Finite memory is dominated by the same envelope.
After discarding $B$ updates, define

$$
I_m=T_fm_4\theta r_f^B\frac{1-r_f^m}{1-r_f},\qquad
V_m=T_fm_4\min(m,\tfrac\pi2\sqrt m),\qquad
G_M(z)=\frac{1-z^M}{M(1-z)}.
$$

For $M$ successive blocks of length $m$, the raw initialized-stationary
estimator difference has $L^2$ norm at most $\varepsilon^2J(m,M,B)$,
where

$$
J(m,M,B)=\frac{2V_mI_mG_M(r_f^m)+I_m^2G_M(r_f^{2m})}{2dm}.
$$

Use $|Y+\delta Y|^2-|Y|^2=2Y\cdot\delta Y+|\delta Y|^2$ and sum
the decaying block bounds. For $P$ superblocks, the two-length bound is
$2J(2L,P,B)+J(L,2P,B)$. Add kernels and divide by $|\Delta D_4|$ to
obtain $I$, so the normalized initialization error is $I/t$. Averaging
seeds gives no assumed improvement. This contract must be implemented
and checked before any experimental use; no current startup is certified.

## Combined radius and fixed diagnostic

Let $b_Q$ and $s_Q$ be the preceding relative coefficient-bias and
sampling-standard-deviation bounds. For failure probability $\delta$,
triangle inequalities and Markov on the squared random remainder give
a radius relative to $|\varepsilon^4\Delta D_4|$ of

$$
\mathcal R(t)=b_Q+e_D(t)
+\frac{s_Q+e_{\rm est}(t)+I/t}{\sqrt\delta}.
$$

Precisely, the initialized paired statistic differs from the stationary
nonlinear $\Delta D(\varepsilon)$ by at most
$|\varepsilon^4\Delta D_4|\mathcal R(t)$ with probability at least
$1-\delta$. For a radius around the leading prediction instead, omit
$e_D$. This transfers the sampling result without claiming a Gaussian
law, an effective independent-block count, or a finite-noise CLT.

Use the unchanged comparison $(A_r,A_a)=(0,26),(1,35)$, scales $(1,3)$,
$\alpha=0.01$, $H=600$, $d=3$, $\eta=0.5\alpha/[q(1+35/9)]$,
$L=1000$, $P=200000$ and five independent seeds. Declare $B=10000$
for this initialization calculation, not as an approved production choice.

| Quantity | Floating-point evaluation |
| --- | --- |
| Common $D_2$ | 0.300259021399 |
| $\Delta D_4$ (second minus first) | -14.4185159350 |
| $e_{\rm est}$ coefficients $(a_e,b_e,c_e)$ | $(6.284915\,10^7,\ 6.093551\,10^9,\ 3.653161\,10^{15})$ |
| $e_D$ coefficients $(a_D,b_D,c_D)$ | $(2.522565\,10^7,\ 4.335457\,10^9,\ 1.113033\,10^{15})$ |
| $I$ | $2.897020\,10^{-27}$ |
| $b_Q+s_Q/\sqrt{0.05}$ | 0.0878265072 |

For a **diagnostic, not protocol-selected**, total margin $0.10$, let
$h=0.10-b_Q-s_Q/\sqrt{0.05}>0$. Write the added terms as
$at+bt^2+ct^3+i/t$, with $(a,b,c)=(a_D,b_D,c_D)+(a_e,b_e,c_e)/\sqrt\delta$
and $i=I/\sqrt\delta$. A sufficient interval, without scanning, is

$$
t_{\min}=2i/h,\qquad t_0=h/(2a),\qquad
t_{\max}=\frac{h/2}{a+bt_0+ct_0^2}.
$$

For $t\in[t_{\min},t_{\max}]$, each of the initialization and nonlinear
terms consumes at most $h/2$. Here it is nonempty and yields
$\varepsilon_{\min}\simeq1.459\,10^{-12}$ and
$\varepsilon_{\max}\simeq4.458\,10^{-6}$. The total computed radius
at either endpoint is about 0.0939133. At the upper endpoint the random
estimator remainder is 0.00124895 in $L^2$ and the transport remainder
is 0.000501288, both relative to the leading contrast. At $0.007$ the
radius bound exceeds $17000$ and provides no useful validation.

The very small lower endpoint comes from dividing the residual
initialization error by $\varepsilon^4$; it is not a physical lower
noise cutoff. Nor is the upper endpoint a necessary validity boundary.
The signal-to-linear-background ratio at the upper endpoint is about
$9.54\,10^{-10}$, not an impossibility theorem for coupled arithmetic.
This analysis assumes exact innovations, force evaluations, summation and
updates. Subtracting independently rounded trajectories is not justified
by these bounds. Stable residual/difference recurrences, high-precision
counterchecks and accumulation/cost checks remain required before a
bounded prospective test. The existing eight-billion-update proposal
remains unauthorized; no simulation has been performed here.

## Verification and scope

[finite_noise_transport.py](../scripts/finite_noise_transport.py) evaluates
the displayed constants. The
[tests](../scripts/test_finite_noise_transport.py) check Gaussian moments
against chi-square products, zero-feedback limits, matrix versus explicit
transport coefficients, exact scalar $H=2$ cubic moments/resampling by
Gauss--Hermite quadrature, independent positive-Volterra recurrences,
literal increment/block startup sums, square-expansion factors, the
sufficient interval and invalid domains. These controls do not constitute
an independent review of the general proof or a machine-rounding bound.

The full-text aging comparison and independent mathematical review remain
open. No publication novelty, archived-regime transport validity, FIFO
formation/transfer, interaction, quantum or gravity claim follows. The
scientific role of this calculation is to expose what a genuine test of
the proposed nonlinear contrast would need, not to replace that test.

Local verification on 2026-10-23: 46 new checks pass; the combined suite
passes 243 research checks and 18 frozen-reference/documentation/claim
checks, 261 total. Ruff, formatting and the strict documentation build
pass. The target-free research CI job includes the new test file. Frozen
manuscripts, production code and archived data are unchanged.
