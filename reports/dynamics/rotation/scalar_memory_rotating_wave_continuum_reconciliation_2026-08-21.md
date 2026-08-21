# Fixed-gain continuum reconciliation for the rotating-wave ladder

Generated: 2026-08-21T03:20:06.692392+00:00.

Decision: **fixed-gain-continuum-reconciliation-pass**.

The historical ladder verdict remains **certified-roots-nonconvergent**; this result does not relabel it.

## Fixed equations

The target solves `I_R(R, Omega) = 0` and `Omega + 15 I_T(R, Omega) = 0` at `C = 12`, using the unchanged native two-Gaussian kernel. No ladder value or extrapolation seeds the solve.

## Independent quadrature panels

| panel | order | R | Omega | max residual | required gain | pass |
| --- | ---: | ---: | ---: | ---: | ---: | :---: |
| numpy-256 | 256 | 0.94311330677 | 1.58557007772 | 2.22044604925e-16 | 15 | True |
| numpy-512 | 512 | 0.94311330677 | 1.58557007772 | 2.22044604925e-16 | 15 | True |
| scipy-1024 | 1024 | 0.94311330677 | 1.58557007772 | 1.16280682999e-17 | 15 | True |

Panel ranges: R = 4.77395900589e-15, Omega = 4.1522341121e-14.

The registered target is the highest-order panel:

- R = 0.94311330677
- Omega = 1.58557007772
- required eta/alpha = 15

## Audited source mismatch

The old discovery initializer is reproduced directly from its JSON:

- old R = 0.943010829278
- old Omega = 1.58681662724
- old required eta/alpha = 15.0163451872

It therefore belongs to a different gain than the ladder's exact eta/alpha = 15.

## Original scaling gates against the corrected target

- radius slope: 1.00944375819
- Omega slope: 1.01102361966
- radius finest/anchor error ratio: 0.247894389186
- Omega finest/anchor error ratio: 0.247530525355
- radius Richardson relative error: 0.00561897698817
- Omega Richardson relative error: 0.00661529057861
- all original scaling gates: True

## Claim boundary

a numerically quadrature-converged fixed-gain continuum root and consistency of the frozen five-cell ladder with the original first-order scaling gates against that corrected target.

This does not establish an interval theorem for the continuum integral, an all-alpha convergence theorem, non-anchor stability, formation, noise robustness, internal S1, work, inertia, or mass.
