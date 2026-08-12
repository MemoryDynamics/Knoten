# P3.8 Rigorous Physics and Code Review

Date: 2026-08-12. Scope: commits `902c7ad` and `0880253`, their generated
reports, and the P3.8c quasistatic two-knot follow-up.

## Verdict

The reviewed branch contains a valid analytic existence construction and a
valid frozen-state discriminator after correction. It does **not** yet contain
an emergent mediator, a dynamic two-knot solution, parameter self-selection,
or evidence for charge, spin, particles, QFT, or three-dimensional selection.

P3.8a and P3.8b must be treated as separate model candidates:

- P3.8a is a scalar density-current extension `(rho,j)` with a longitudinal
  propagation threshold.
- P3.8b is an independent vector mediator `(m,p)` whose adjoint gradient
  source/readout follows from one interaction energy.

They share a longitudinal pole polynomial, but that algebraic similarity does
not identify their states or source terms.

## Findings and corrections

| Severity | Finding | Resolution |
|---|---|---|
| high | The previous P3.8b text attached the `k^2` numerator to the P3.8a current without deriving its source placement. Canonical additive scalar deposition does not generate it. | Moved the response into `gradient_mediator.py`; introduced explicit `(m,p)` state and `H_int=-g integral m dot grad(q) dx`; documentation now separates P3.8a/b. |
| high | A common-energy claim was not supported by the former density-current equations. | Source and readout are now Hilbert adjoints. Their contraction supplies `g^2 k^2`; an independent energy-rate test checks homogeneous damping. |
| medium | Finite-cutoff Fourier inversion and a coarse derivative grid shifted reported radii to about `3.88` and `6.96`. | Replaced by exact Yukawa-residue inversion and analytic derivative. Infinite oscillatory quadrature agrees to `1.81e-15`; corrected radii are `3.919200371` and `6.990916303`. |
| medium | A partially neutral spectrum was classified unstable because marginality used maximum absolute real part. | Classification now uses the spectral abscissa; a one-zero/one-negative regression test reports `marginal_real`. |
| medium | Static `reversible-off` was proposed as a discriminator although first- and second-order dynamics can share one equilibrium susceptibility. | Removed as a static null. It is reserved for a later dynamic response test. |
| medium | Some checks repeated the implementation formula rather than using an independent numerical route. | Added independent Fourier quadrature, finite-difference energy gradient, point-limit convergence, covariance, zero-mode, and action/reaction tests. |
| low | Response sign was labelled attractive/repulsive without checking the derivative. | Figures now say sign-changing response shells; pair stability is classified from force changes. |
| low | Initial P3.8c numerical gates divided by near-zero force at stationary points and used an arbitrary compactness multiplier. | Force-gradient checks use registered nonstationary radii; root residuals, all-orientation force signs, full-memory stability, and empirical second-order point-limit convergence replace the arbitrary bound. |
| low | The two mediator decay rates were presented as an ordered ratio although the pole polynomial is invariant under their exchange. | `r_gamma` is now the canonical larger-to-smaller ratio (`>=1`); individual rate labels are explicitly non-identifiable from this response. |
| medium | The frozen pair pilot used a reciprocal memory-density/memory-density energy, whereas the canonical simulator reads foreign memory at a visible point. | The report now labels this as a new cross-channel choice and includes a separately energy-symmetrized visible-memory comparison. Both retain the discriminator signs because the checkpoint is pointlike; they are not declared equivalent. |

## P3.8c result

The test uses two rigid copies of the checksum-validated `d=3`, seed-1,
`N=100,000,000` complete finite-memory checkpoint. It advances no state and
fits no gain.

- At the fixed, model-derived `R/ell=5`, static compensated and
  gradient-mediator arms predict opposite force signs for all three tested
  orientations.
- The gradient arm has a full-memory unstable barrier near `3.91920 ell` and a
  stable quasistatic minimum near `6.99092 ell`.
- Force equals the negative energy derivative, action/reaction closes, and
  shrinking the internal cloud gives second-order point-limit convergence.
- The direct-source control also has shells but a nonzero Fourier zero mode;
  shells alone therefore do not establish neutrality.
- A symmetrized visible-memory comparison preserves the discriminator signs,
  but the primary memory-memory energy remains a distinct reciprocal
  cross-channel architecture. Its `0.2411%` common amplitude offset is the
  finite-tail mass factor: the point limits scale as `M_H` and `M_H^2`.

This is a conditional **mechanism-discriminability pass**. The stored cloud is
extremely compact (`R_mem/ell=2.12e-4`), so the result is effectively a
point-source validation. `ell=sigma_rep=1` is imposed, only one formation seed
is used, and the mediator has not been evolved.

This audit was not sealed by an earlier immutable preregistration commit. Its
physical arms, radii and discriminator were fixed before the final checkpoint
evaluation, while two flawed numerical validation gates were replaced during
review as recorded above. It should therefore be called a fixed-scope audit,
not a formally preregistered experiment.

## Remaining blockers

Before a dynamic two-knot claim, derive and test one discrete `(m,p)` update
with the same interaction energy. It must close source work plus damping,
converge with timestep, preserve action/reaction, and include cross-off and a
first-order dynamic control. Only then is one short pilot at the already fixed
radii justified. Coefficient, gain, kernel, and noise sweeps remain blocked.

## Verification

- focused P3.8 tests: `33 passed`;
- full repository suite: `571 passed` with a workspace-local `--basetemp`;
- Ruff on the reviewed P3.8 files: pass;
- `git diff --check`: pass;
- MkDocs strict build: pass.

A repository-wide Ruff audit additionally reports `24` findings in unchanged
legacy/archive and older paper scripts outside this review scope. They are not
regressions from P3.8, but the repository as a whole must therefore not be
described as globally Ruff-clean.

The first default-temp pytest attempt completed `535` tests but reported `35`
fixture setup errors because the global Windows directory
`%TEMP%/pytest-of-Hauke` was access-denied. Re-running the unchanged suite with
`--basetemp=data/processed/.pytest_tmp_p38_20260812` passed completely; this
was an environment-path failure, not a product-code failure.

Generated P3.8a/b/c reports record reviewed code revision `bd31965`.
