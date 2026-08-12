# Adjoint-gradient mediator Green-kernel gate

Date: 2026-08-11. Status: **structural pass, model candidate only**.

## Correction and question

An attractive near field and repulsive outer shell can preserve individual
nodes while preventing sufficiently separated identical nodes from merging.
It does not by itself guarantee one finite pair distance: a static two-scale
law commonly gives merger on one side of a force crossing and unbounded
separation on the other. The earlier compensated three-scale pilot already
constructed an outer repulsive shell at about `10.91 sigma_rep`, but did not
test reciprocal two-node dynamics.

Can the shell shape and its scale instead arise as the response of one
longitudinal vector mediator, with a common adjoint source/readout coupling?

## Review correction: state and source placement

The canonical memory remains the non-negative occupancy \(\rho\) in
\(z=(x,\rho)\). The following longitudinal vector mediator \(\mathbf m\) and
its conjugate velocity \(\mathbf p\) are a proposed Markov-state extension,
not a relabeling of \(\rho\):

\[
\partial_t\mathbf m=\mathbf p,
\qquad
\partial_t\mathbf p=-(\lambda_m+\gamma_p)\mathbf p
-\left[\lambda_m\gamma_p+(-\Delta)D(-\Delta)\right]\mathbf m
+g\nabla q.
\]

Here \(q\) is a scalar source density. A point witness uses \(q=G_x\); the
frozen-node follow-up uses its complete retained occupancy. The single
interaction energy is

\[
H_{\rm int}[\mathbf m,q]=-g\int\mathbf m(y)\cdot\nabla q(y)\,dy.
\]

It supplies both the vector source \(g\nabla q\) and its adjoint reciprocal
readout. This explicit source placement is required for the \(k^2\) numerator.
Additive deposition directly into canonical \(\rho\) does not produce that
numerator. The earlier wording that attached the response directly to the
canonical continuity-memory law was therefore too strong.

## Reciprocal response

Let the longitudinal constitutive stiffness be

\[
D(k)=a+b k^2+c k^4,
\qquad a,c>0.
\]

For reciprocal gradient coupling, eliminating the linear memory field gives

\[
\widehat K_{\rm eff}(k,\omega)
=\frac{g^2 k^2}
{(-i\omega+\lambda_m)(-i\omega+\gamma_p)+k^2D(k)}.
\]

The same `g` writes and reads the mediator, hence `g^2`; independent source and
readout amplitudes are absent. The adjoint gradient pair supplies
`K_eff(0,omega)=0`, so the spatial integral vanishes without balancing raw
Gaussian amplitudes.

With

\[
\ell=(c/a)^{1/4},\quad
u=k\ell,\quad
\delta=\frac b{\sqrt{ac}},\quad
\mu=\frac{\lambda_m\gamma_p\sqrt c}{a^{3/2}},\quad
r_\gamma=\frac{\max(\lambda_m,\gamma_p)}{\min(\lambda_m,\gamma_p)}\geq1,
\]

the static denominator is

\[
P(u)=\mu+u^2+\delta u^4+u^6.
\]

The two decay rates enter only through their sum and product, so exchanging
their labels leaves the response unchanged. `r_gamma` is therefore the
canonical larger-to-smaller ratio; the individual labels are not identifiable.

Thus five dimensional coefficients reduce to a length/rate normalization and
three dimensionless shape groups. The response-selected scale is not supplied:
for `y_*=u_*^2` it solves

\[
2y_*^3+\delta y_*^2-\mu=0.
\]

## Fixed existence witness

The fixed witness `delta=-1.9`, `mu=0.3`, `r_gamma=1` is an analytic existence
point, not a fit to knot data. Its constitutive minimum is
`0.0975>0`, so the fixed-source quadratic
mediator energy is positive.

- selected `u_*=1.03869`;
- selected wavelength `2 pi/u_*=6.04916`;
- first point-source pair barrier at `r/ell=3.9192`;
- first finite separated minimum of `U_pair=-K_eff` at
  `r/ell=6.99092`.

![Dynamic Green-kernel gate](../../../figures/draft/memory/dynamic_green_kernel_selection_gate_2026-08-11.png)

## Registered gates

| Gate | Result |
|---|---|
| `dimensionless_reduction_exact` | pass |
| `constitutive_operator_positive` | pass |
| `static_denominator_positive` | pass |
| `selected_mode_oscillatory` | pass |
| `analytic_peak_matches_grid` | pass |
| `gain_free_peak_inference_recovers_groups` | pass |
| `gradient_channel_zero_mode` | pass |
| `direct_channel_nonzero_mode_control` | pass |
| `common_gain_sign_invariant` | pass |
| `real_space_sign_changing_shells` | pass |
| `exact_residues_match_infinite_fourier_quadrature` | pass |
| `finite_separation_energy_minimum_exists` | pass |

## What is and is not self-selected

Selected conditional on the proposed field coefficients and source geometry:
effective response shape, zero integral, preferred wavelength, shell positions
and the linear point-source pair landscape.

Not selected: `delta`, `mu`, `r_gamma`, the absolute length/time units and the
overall coupling. A simulation cannot determine constants that do not have an
update law. Promoting them to arbitrary adaptive variables would only move the
kernel choice into an adaptation rule.

The defensible coarse-graining route is identification rather than tuning.
Let `kappa_y=-d_y^2 log H(y)|_* > 0` for `y=u^2`. Then the unknown overall
gain cancels and

\[
\delta
=\frac{y_*[6-\kappa_y(1+3y_*^2)]}{2(\kappa_y y_*^2-1)},
\qquad
\mu=2y_*^3+\delta y_*^2.
\]

Consequently:

1. peak position and local log curvature estimate `delta,mu` jointly;
2. temporal damping and frequency at the same peak estimate
   the unordered decay-rate ratio and test the dispersion relation;
3. a calibrated weak response fixes the remaining gain;
4. estimates must agree across seeds, blocks, resolutions and independent
   pair response before they are called effective parameters.

## Decision and next test

P3.8b passes after review as an analytic **adjoint-gradient mediator
candidate**. It gives
a common-energy route to a zero-mode-free, sign-changing quasistatic response,
a finite separated point-source basin and phase-bearing temporal modes. It is
not obtained from canonical scalar deposition alone. It does not establish
nonlinear knot formation, basin accessibility, stability under noise,
parameter universality, or `d=3`.

Next, and only next, run one matched two-node pilot using mature frozen states:

- arm A: the already fixed compensated static outer-shell kernel;
- arm B: this fixed dynamic Green field;
- controls: cross-off and direct non-gradient source in the static gate;
- fixed separations below the barrier, in the outward-force interval, at the
  predicted finite minimum and beyond it;
- primary static outcomes: signed full-memory centre force and agreement with
  independently predicted shell radii. Shape cannot change in this frozen gate.

Reversible/current-off is not a valid static null because first- and
second-order realizations share the same equilibrium susceptibility. Bounded
separation, shape evolution and energy/work balance require a later dynamic
mediator implementation with a separately preregistered time discretization
and gain/mobility; they are not inferred from this quasistatic response.

No kernel-amplitude sweep or adaptive coefficient law is authorized.

## Reproducibility

- Script: `experiments/current/memory/closure/dynamic_green_kernel_selection_gate.py`
- Package: `src/emergenz_knoten/gradient_mediator.py`
- Git revision before generated changes: `bd31965aeec8aa9ef04a8b78d1eef5bb8e794c59`
- Generated: `2026-08-12T03:50:27.388725+00:00`
