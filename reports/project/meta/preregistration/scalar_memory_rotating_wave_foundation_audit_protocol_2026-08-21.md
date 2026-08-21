# Prospective foundation audit: native scalar-memory rotating waves

Date: 2026-08-21.

Status: frozen retrospective falsification protocol. It is written after the
discovery, stability, interval, refinement and fixed-gain continuum results,
but before running the independent checks below. It cannot make those earlier
analyses prospective. Its purpose is to decide whether their immutable
evidence chain is internally consistent enough to serve as a scoped
foundation for later loop cells.

The proposed next cell

$$
(\alpha,H,\eta)=(0.00125,9600,0.01875)
$$

and the amplitude holdout $A_{\rm att}=7$ remain sealed throughout this
audit.

## 1. Frozen object and notation

The native deterministic update is

$$
x_{n+1}=x_n-\eta\nabla(K*\rho_n)(x_n),
\qquad
\rho_{n+1}=q\rho_n+\alpha M_0\delta_{x_{n+1}},
\qquad q=1-\alpha.
$$

For a prepared circular history $x_n=R e^{in\theta}$ and ages
$j=1,\ldots,H-1$, define

$$
w_j=\alpha M_0q^j,
\quad u_j=1-\cos(j\theta),
\quad \chi_j=R^2u_j,
$$

$$
\phi(\chi)
=-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
 e^{-\chi/\sigma_{\rm rep}^2}
 +\frac{A_{\rm att}}{\sigma_{\rm att}^2}
 e^{-\chi/\sigma_{\rm att}^2}.
$$

The symbol $q$ is reserved for forgetting. The auxiliary squared half-chord
used as $q(t)$ in the historical continuum protocol is renamed $\chi(t)$ in
this audit; this is a notation correction, not a changed equation.

The exact reduced finite-$H$ equations are

$$
F_R=\cos\theta-1+\eta\sum_{j=1}^{H-1}w_j\phi(\chi_j)u_j=0,
$$

$$
F_T=\sin\theta+\eta\sum_{j=1}^{H-1}
w_j\phi(\chi_j)\sin(j\theta)=0.
$$

No oscillator, momentum, centripetal-force or mass term is introduced.

## 2. Immutable input ledger

The audit must reject any byte change in the following sources. SHA-256 is
lowercase hexadecimal.

| source | SHA-256 |
| --- | --- |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_discovery_2026-08-20.json` | `ab47cb3168561e4d9d9535981bda598bfa9815c3c593f65b6fd28d1874c561cb` |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_initial_state_spec_2026-08-20.json` | `4ab3f657cfa68bcd38d73c0722cd718a94e413b33fc46c17bb995b3637808dd2` |
| `reports/project/meta/preregistration/scalar_memory_rotating_wave_p0_manifest_2026-08-20.json` | `3d89d2fe390c24765b23a834ad682b626f5ce3025b44f508afb1509b7fd6efb1` |
| `reports/project/meta/preregistration/scalar_memory_rotating_wave_p0_audit_2026-08-20.json` | `5ddde8005dd261bbd2aa8bd72906a7395f53d8bb666fb1ce5e9bb5686cdcde4c` |
| `reports/project/meta/preregistration/scalar_memory_rotating_wave_d0_contract_2026-08-20.md` | `4ad70cd38efb87e97509fe253987a6ac0a6dce9555cc37457eaba54a5f822bb2` |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_stability_2026-08-20.json` | `8b168d702d335dc5833f63c44cd2aa9b7c762a7ad6ac3ce36b87553a62114930` |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_interval_certificate_2026-08-21.json` | `77558d09f5114a549384916fc15c2dc6113b1c6eb4a2f77f6a3646d6ff2df20c` |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_refinement_ladder_2026-08-21.json` | `9e76e34911261b263278004281822e2b4d36025181e1b9b9daf899aa28770301` |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_continuum_reconciliation_2026-08-21.json` | `8457536836b3fe1f4dc6d83fc74f57b39447978bd62574e5eedbb40294f4cd10` |

Every recorded execution revision must exist and be an ancestor of the audit
revision. The run must begin from a clean worktree.

## 3. Gate A: provenance and parameter closure

Require all source hashes and revisions to pass. The candidate identifier
must agree across P0, stability and interval artifacts. P0 must be frozen,
clean and defect-free. Discovery, P0, stability and interval parameters must
agree with

$$
d=2,\ \varepsilon=0,\ \alpha=0.01,\ H=1200,\ M_0=1,
\ \eta=0.15,
$$

$$
\sigma_{\rm rep}=A_{\rm rep}=1,
\quad \sigma_{\rm att}=3,
\quad A_{\rm att}=3.5
$$

to absolute tolerance $5\times10^{-13}$ where historical decimal rounding
prevents exact string identity.

The historical ladder decision must remain
`certified-roots-nonconvergent`; the later reconciliation must explicitly
preserve that label.

## 4. Gate B: independent finite-sum replay

Without importing either rotating-wave implementation, evaluate the two
displayed finite sums with `mpmath` at 70 decimal digits at the 120-digit
centers of all five certified cells. Require in every cell:

- $\max(|F_R|,|F_T|)\leq10^{-45}$;
- $A_H>0$ and $S_H<0$;
- both independently inferred gains differ from the registered $\eta$ by at
  most $10^{-40}$;
- $H\alpha=12$ and $\eta/\alpha=15$ exactly in decimal arithmetic.

This is an implementation/sign/indexing replay, not a second interval proof.

## 5. Gate C: certificate and stability semantics

Require both interval panels, their cross-panel overlap, all five ladder
cells and anchor overlap to retain their recorded passes. Require the
stability artifact to retain both frozen Arnoldi controls, its matched
transverse pair inside the unit circle, exact-control bound and all three
registered contractions.

The audit must nevertheless label stability `anchor-local-numerical`, because
24/36 Ritz pairs are not a complete spectral enclosure. It must label the
continuous circle `ambient-SO2-group-orbit`, because D0 collapses it to a
point after ambient rotation is quotiented. Neither limitation is a failed
consistency gate; overstating either claim is.

## 6. Gate D: independent multiprecision continuum solve

Use the same native limiting equations but a new `mpmath` implementation.
For $t\in[0,12]$ set

$$
u(t)=1-\cos(\Omega t),\qquad \chi(t)=R^2u(t),
$$

$$
I_R=\int_0^{12}e^{-t}\phi(\chi(t))u(t)\,dt,
\qquad
I_T=\int_0^{12}e^{-t}\phi(\chi(t))\sin(\Omega t)\,dt,
$$

and solve $I_R=0$, $\Omega+15I_T=0$ with the displayed analytic Jacobian.
Both frozen panels start independently from the old discovery guide

$$
(R,\Omega)=(0.9430108292781663,1.5868166272376472)
$$

and perform exactly six undamped Newton steps at 70 decimal digits on the
fixed partition $[0,2,4,6,8,10,12]$:

| panel | `mpmath` method | maximum degree |
| --- | --- | ---: |
| mp-ts-70 | tanh-sinh | 10 |
| mp-gl-70 | Gauss--Legendre | 10 |

Every iterate must remain within $0.05$ of the start in each coordinate.
Each final residual must be at most $10^{-45}$, $I_T<0$, the inferred gain
must differ from 15 by at most $10^{-40}$ and the absolute Jacobian
determinant must exceed $0.1$. Panel roots must agree within $10^{-40}$.
Each root must agree with the published SciPy-1024 target within
$5\times10^{-13}$. These are independent multiprecision quadrature controls,
not interval enclosures of the continuum integrals.

## 7. Gate E: scaling replay

Using the mp-gl-70 root as the target, recompute rather than import the old
scaling diagnostics. Preserve the original thresholds:

- strictly decreasing positive errors across L0--L4;
- L1--L4 log-log slopes in $[0.8,1.2]$;
- L4/anchor error ratios at most $0.35$;
- first-order Richardson relative errors at most $0.1$.

Also require the stored fixed-gain reconciliation decision and all its gates
to remain positive. This finite ladder supports first-order numerical
consistency; it is not an all-$\alpha$ convergence theorem.

## 8. Decision and claim boundary

Decision is `foundation-audit-pass-scoped` only if Gates A--E all pass and
the report retains every boundary below. Any hash, provenance, parameter,
finite-sum, certificate, continuum or scaling failure yields
`foundation-audit-fail`. An execution exception yields
`foundation-audit-inconclusive`.

A scoped pass establishes:

1. an exact algebraic reduction of a prepared native circular history;
2. five locally unique finite-$H$ balance roots on one registered branch;
3. independent numerical support for their matched fixed-gain continuum
   target and first-order approach;
4. anchor-local numerical stability in the registered panels.

It does **not** establish global root uniqueness, a complete stability
theorem, formation from generic history, a basin size, noise robustness,
chirality selection, an internal $S^1$ after symmetry reduction, a work
ledger, inertia, mass or a material knot. Those require separate prospective
gates.
