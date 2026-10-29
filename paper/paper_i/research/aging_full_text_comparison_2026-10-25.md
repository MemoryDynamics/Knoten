# Aging diffusion: full-text comparison with the linear reference

Date: 2026-10-25. Internal model comparison, not an independent referee
report or a novelty certificate. The
[project priorities](../../../docs/status/project_priorities.md) remain
the only execution list. No target simulations or new model rules.

## Source and conclusion

The user supplied the 22-page PDF of Nicolas Meunier, Vuk Milisic and
Raphael Roux, *Self-Interacting Diffusions with Aging*,
[SSRN 6659876](https://doi.org/10.2139/ssrn.6659876).
Its metadata date is 2026-04-27 and it is marked not peer reviewed.
SHA-256 of the supplied file:
`5aaf229daa78b87517c36e5663e7e3a6838039a12b3a3660e8da9207ae790c31`.
All pages were read as extracted text; PDF pages 2, 4, 8, 15 and 20 were
also rendered and visually checked for the equations used below. Printed
manuscript page numbers are one less than PDF page numbers because of the
highlights page. The supplied PDF is not redistributed in this repository.
The title page gives this author order and first name Raphael; SSRN's
listing uses a different order and the first name Rafael.

**The missing model-level comparison is now resolved.** For untruncated
exponential memory, our linear update is exactly the authors'
Euler--Maruyama scheme after matching parameters, noise and initialization.
Their continuous-time diffusion coefficient is the scaled small-step limit
of our discrete coefficient, not generally the same number at finite step.
This is stronger overlap than an analogy. It does not identify their
linear model with our nonlinear Gaussian-mixture force.

The supplied work has no nonlinear weak-noise transport expansion of the
kind considered here. That narrow absence does not establish priority:
the [Gaussian-projection audit](gaussian_projection_audit_2026-10-24.md)
already reproduces our first nonlinear coefficient by a known method.
The remaining candidate is a useful controlled application, including its
remainder and memory/long-time limits. Its scientific significance remains
to be assessed independently.

## What the source establishes and what it does not

| Inspected location | Source-reported content | Consequence for our comparison |
| --- | --- | --- |
| Eq. (1.1), Proposition 2.1; printed pp. 1, 4--5 | Additive Brownian noise and a force linear in past displacements, weighted by a deterministic age kernel; Gaussianity for deterministic initial position. | The temporal kernel is general, the spatial interaction is linear. A general age kernel does not supply our nonlinear spatial response. |
| Theorems 1.1--1.3, Eq. (3.3), Sections 3.1--3.3 | Resolvent decomposition and subcritical, critical and supercritical long-time regimes for the auxiliary full-past process. | The linear memory/transport story is prior work. Critical prefactors need the correction identified below; no wholesale theorem import is made. |
| Theorems 1.4--1.5 and Section 4 | Comparison of a process started with an empty past and a zero-extended full-past process. | Initialization is part of their analysis, not a detail that can be erased in an exact model match. |
| Sections 5.1--5.3, Lemma 5.1 and Corollary 5.2; printed pp. 14--16 | Explicit exponential-memory resolvents and a subcritical Brownian contribution plus bounded corrections. | Directly covers renormalized diffusion coexisting with bounded relative fluctuations in the linear example. The corrections need not be independent of the Brownian term. |
| Section 6; printed p. 19 | Euler--Maruyama schemes with sampled age weights and unit Brownian amplitude. | Gives the exact discrete linear correspondence below. It does not prove a nonlinear discrete weak-noise theorem or uniform nonlinear truncation bounds. |

This is a scope comparison and a reproduction of the relevant exponential
linear formulas, not a verification of every general-kernel proof. The
source's broad supercritical conjecture is not used to support our result.

## Explicit parameter dictionary

Rename the source's interaction coefficient to $a$ and its exponential
decay rate to $b>0$. Neither is our memory parameter $\alpha$ or our
cubic force coefficient. With Brownian amplitude $\sigma$ restored, its
empty-past equation is

$$
dx_t=a\int_0^t (x_t-x_{t-s})e^{-bs}\,ds\,dt+\sigma\,dW_t.
$$

The source sets $\sigma=1$; its generalization here follows directly by
linearity, not from a new model fit. Negative $a$ is attractive in this
equation. For step $h>0$, Section 6 gives

$$
x_{n+1}-x_n
=a h^2\sum_{j=0}^{n}e^{-bjh}(x_n-x_{n-j})
+\sigma\sqrt h\,\xi_{n+1}.
$$

Our corresponding linear equation, before a hard horizon cutoff, is

$$
x_{n+1}-x_n
=-g\sum_{j\geq1}\alpha q^j(x_n-x_{n-j})
+\varepsilon\xi_{n+1},\qquad
q=1-\alpha,\quad g=\eta\kappa.
$$

The exact coefficient dictionary is

$$
q=e^{-bh},\qquad \alpha=1-e^{-bh},\qquad
a h^2=-g\alpha,\qquad \varepsilon=\sigma\sqrt h.
$$

The $j=0$ force vanishes. No normalization of the retained weights is
performed. A normalized finite-memory implementation must retain its
separate total mass in the effective gain before this dictionary is used.
The coordinatewise mapping extends the source's scalar linear equation to
independent coordinates; it is not a nonlinear dimensional extension.

Initialization must match as well:

- Empty history: retain only $1\leq j\leq n$. This is the source's
  non-convolution Euler scheme.
- Flat prehistory $x_k=x_0$ for $k<0$: add the tail
  $-g q^{n+1}(x_n-x_0)$ to the empty-history drift. After translating
  $x_0$ to zero, this is the source's full-past convolution scheme.
- Stationary relative increments: this is our transport theorem's initial
  law, not either of the two starts above. A long-time identification needs
  a stability/coupling argument; one-step equality is not that argument.

A hard finite $H$ also changes the age kernel. This comparison does not
replace our separate horizon estimates or the FIFO orbit program.

## Continuous and discrete transport

For the full-past linear exponential model, introduce
$m_t=\int_0^\infty e^{-bs}X_{t-s}\,ds$ and
$r_t=X_t/b-m_t$, with zero prehistory. Then

$$
dm_t=(X_t-bm_t)\,dt,\qquad
dr_t=(a/b-b)r_t\,dt+(\sigma/b)\,dW_t.
$$

Thus the relative mode is stable for $a<b^2$, while the absolute position
need not be stationary. In this subcritical regime, setting $z=a/b-b$,
Section 5.1's resolvent is

$$
R(t)=c+d e^{zt},\qquad
c=\frac{b^2}{b^2-a},\qquad d=-\frac{a}{b^2-a},\qquad c+d=1.
$$

For $a=0$ this is $R=1$. The stochastic convolution gives directly

$$
\operatorname{Var}X_t
=\sigma^2\left[c^2t+
2cd\frac{e^{zt}-1}{z}+
d^2\frac{e^{2zt}-1}{2z}\right],\qquad
D_{\rm cont}=\lim_{t\to\infty}\frac{\operatorname{Var}X_t}{2t}
=\frac{\sigma^2}{2(1-a/b^2)^2}.
$$

The source sometimes calls $c$ a diffusion coefficient; in our MSD
convention it is a Brownian amplitude and the diffusion coefficient is
$\sigma^2c^2/2$. The bounded relative OU mode and the diffusive absolute
position are not evidence for absolute localization.

In the untruncated discrete equation let
$s_n=\alpha\sum_{j\geq0}q^j x_{n-j}$ and $u_n=x_n-s_n$. The exact recursion
is

$$
u_{n+1}=q(1-g)u_n+q\varepsilon\xi_{n+1}.
$$

For $|q(1-g)|<1$, the increment filter has zero-frequency gain
$\alpha/(\alpha+gq)$. Consequently the per-coordinate diffusion on the
chosen time scale with step $h$ is

$$
\frac{D_{\rm step}}{h}
=\frac{\varepsilon^2}{2h(1+gq/\alpha)^2}
=\frac{\sigma^2}{2(1-a\mu_{1,h})^2},\qquad
\mu_{1,h}=h^2\sum_{j\geq1}j e^{-bjh}
=\frac{h^2q}{(1-q)^2}.
$$

This reproduces the repository's linear coefficient, using the sampled
first age moment. It is our derivation for the source's scheme, not a
discrete theorem attributed to that paper. Since

$$
\mu_{1,h}=\frac{h^2}{4\sinh^2(bh/2)}
=\frac1{b^2}-\frac{h^2}{12}+O(h^4),
$$

the coefficient tends to $D_{\rm cont}$ when $a,b,\sigma$ are held fixed
and $g=-a h^2/(1-e^{-bh})$. The stable discrete pole satisfies
$q(1-g)=1+(a/b-b)h+O(h^2)$. At finite step, continuous stability alone is
not enough to ensure $|q(1-g)|<1$. This coefficient limit is not a theorem
about convergence of the full nonlinear process and does not assign a
physical clock to the model's update index.

## Source inconsistencies checked before reuse

These are version-specific checks, not a reason to dismiss the overlap.

1. **Attraction sign.** Printed p. 1 after Eq. (1.1) labels positive
   source $\alpha$ attractive. The displayed drift points away from past
   positions for that sign. Section 4.1 correctly uses negative $\alpha$
   for attraction. The dictionary above follows the equations and Section
   4.1, not the erroneous introductory sentence.
2. **Critical Brownian prefactor.** Eq. (1.5) gives
   $4\mu_1\mu_3/\mu_2^2$, whereas Eq. (3.5) gives
   $2\mu_1\mu_3/(3\mu_2^2)$ for the constant resolvent coefficient.
   For $P(s)=e^{-bs}$ and $a=b^2$, the exact resolvent is $R(t)=1+bt$.
   Thus $X_t=\sigma W_t+\sigma b\int_0^tW_s\,ds$.
   The two printed coefficients evaluate to $6$ and $1$, respectively.
   The discrepancy cannot be absorbed into an $L^1\cap L^2$ convolution
   remainder: it would require the constant kernel $-5$. Eq. (1.5), as
   printed, fails this explicit special-case check. The exact special
   case agrees with Eq. (3.5).
3. **Numerical caption.** Figure 1 states $P(s)=s e^{-s}$ and
   $\mu_1=1/4$. The moment is actually
   $\int_0^\infty s^2e^{-s}\,ds=2$. We do not infer the kernel used by
   their unavailable code from this caption or reproduce its numerical
   regime labels as evidence.

The supplied version also has unresolved citation placeholders. We have
not independently audited or repaired its complete general-kernel proofs.
In particular, reading every page does not make it an independent theorem
validation. Our exponential comparison uses explicit algebra instead.

## Reproducible checks and publication consequence

The aging-prefixed tests in
`paper/paper_i/scripts/test_weak_nonlinearity.py` check the parameter map
with both starts, the discrete diffusion coefficient against the existing
reference helper, the scaled continuous limit, the explicit continuous
resolvent and variance, the critical prefactor discrepancy, and the caption
moment. They use deterministic vectors, small quadratures and exact
formulas. They are not new trajectory data or proof of publication novelty.

For the next manuscript revision, cite the aging work as a direct linear
predecessor and explain the parameter map briefly. Do not sell exponential
memory, reduced diffusion, an OU-like relative mode, or an Euler
implementation as the new mechanism. The candidate main result remains
the controlled nonlinear transport statement in its strict domain, as
specified in the [decision brief](paper_i_decision_brief_2026-10-23.md).
The supplied aging work does not settle that statement's overlap with
rigorous statistical linearization or response theory. Bernard--Wu's
theorem-level comparison and independent assessment remain open.
Nothing in this comparison supplies a physical multisystem measurement
law, quantum mechanics or gravity.
