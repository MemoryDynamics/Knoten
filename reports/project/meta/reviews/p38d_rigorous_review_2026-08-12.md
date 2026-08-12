# P3.8d rigorous physics, code and result review

Date: 2026-08-12. Scope: the discrete longitudinal `(m,p,R)` candidate,
energy/work ledger, matched first-order control, convergence tests and the
fixed two-source pilot.

## Verdict

P3.8d is a conditional **dynamic existence pass** for a newly proposed
mediator. It is not a derivation from canonical scalar memory and does not
select second-order dynamics over a first-order relaxation with the same
static susceptibility.

The useful result is narrower: one adjoint source/readout energy admits a
stable discretization; two fixed collinear point sources from either side of
the barrier relax into the separated basin predicted in P3.8b/c. The result is
reproducible under timestep refinement and the basin location is stable under
the registered Fourier cutoffs.

## Findings and resolutions

| Severity | Finding | Resolution |
|---|---|---|
| high | A reversible field alone does not define source motion or a total energy balance. | Added overdamped relative coordinate `R_dot=nu B_R dot m` derived from the same energy. No centre inertia or mass was inserted. |
| high | A naive explicit source update need not reproduce source work. | Implemented a scalar discrete-gradient source step and solved it implicitly; maximum pilot work residual is below `1e-15`. |
| high | Static `reversible-off` cannot distinguish dynamic order because first- and second-order fields may share `A^-1`. | Added a matched first-order dynamic control with the same energy and equilibrium susceptibility. |
| medium | The first trial used `dt=1` outside the asymptotic convergence window. | The pilot uses `dt=0.5`; a separate `dt=0.25,0.125,0.0625` study against `0.03125` gives observed orders about `1.96` and `2.30`. Pilot endpoints are also repeated at `dt=0.25`. |
| medium | Subtracting nearly equal source cosines made tiny discrete-gradient steps lose precision. | Replaced the quotient by an analytic midpoint-`sinc` identity and added a tiny-motion regression test. |
| medium | Random UV modal initial data made a low-order damping quadrature underresolve frequencies up to order `k_max^3`. | Damping identity is tested independently on a deliberately resolved modal band; the production field step remains analytic for all retained modes. |
| medium | An abrupt point-source quench excites the UV tail. Early force extrema converge slower than the separation and static basin. | Added a `k_max=16,20,24,28` audit. Basin radii are gated; early force amplitudes are explicitly non-claim diagnostics. |
| medium | A zero-field start can make reversible ringing look like an intrinsic pair mode. | Added static-equilibrium initializations for both dynamic orders and both separations. They retain the basin but remove force reversal; ringing is classified as quench-dependent. |
| medium | The reversible and first-order separation curves are visually close. | Report states that the control reaches the same basin. The dynamic-order distinction is the selected-mode overshoot and short quench transient, not binding itself. |
| medium | Choosing `Gamma` as the first-order kinetic coefficient fixes one response timescale. | The report now treats this as one registered timing convention, not an exhaustive first-order null family. |
| low | Initial force sign-change counting mixed exact zero with nonzero signs. | Count now removes numerical zeros before comparing signs and is named `nonzero_force_sign_changes`. |
| low | The first regression test reran the full roughly 96-second evidence campaign in pytest. | Replaced it with a short deterministic experiment-glue/ledger/compaction test; the full fixed campaign remains an explicit report-generation command. |

## Independent checks

- The modal static force is compared against the exact Yukawa-residue Green
  derivative from P3.8b, rather than against the new time-stepper.
- Fixed-source damping loss is compared with independent Gauss-Legendre time
  integration of `Gamma |p(t)|^2`.
- The source substep reports the energy change and discrete work separately.
- Cross-off uses a zero common coupling and leaves field, force, energy and
  separation exactly zero.
- Equal and opposite source motion is imposed by the symmetric relative
  coordinate; this is an architectural property, not an independent
  action/reaction observation.
- First- and second-order controls are initialized at one common equilibrium
  to verify identical static force and energy.
- Timestep refinement compares the complete reduced state in its natural
  quadratic energy norm, not separation alone or an unweighted modal mean.
- Static basin radii and early dynamic observables are checked separately over
  Fourier cutoffs.

## Scientific limits

The following are still inputs rather than emergent outputs:

- the existence of the longitudinal mediator `(m,p)`;
- `delta=-1.9`, `mu=0.3`, equal decay rates and relative mobility `nu=1`;
- the identification of mediator length with the previous pair-law scale;
- the point-source and collinear reduction;
- the absence of noise and internal knot-shape dynamics.

Because the total energy is a strict Lyapunov function away from equilibrium,
this autonomous damped reduction cannot support a persistent limit cycle.
Its short complex-mode transient is not evidence for spin, an orbit, a photon
or quantum phase. No dimensional-selection claim follows.

## Decision

Keep P3.8d as a falsifiable candidate mechanism and software reference. Do not
promote it into the canonical model or a paper claim yet. The next gate must
ask whether canonical `(x,rho)` trajectories and independent response
holdouts identify this state and dispersion better than the matched
first-order null. Failure would classify P3.8 as a constructed extension,
not an emergent closure.

## Verification target

- focused P3.8d tests and full repository suite;
- Ruff on all changed Python files;
- `git diff --check`;
- MkDocs strict build;
- generated JSON parse and figure inspection.

Verification: `582` repository tests passed with a workspace-local
pytest temp directory; `11` focused P3.8d tests passed in `2.41 s`; Ruff passed on every
changed Python file; `git diff --check` and MkDocs strict passed. The generated
JSON was parsed after compaction and the figure was inspected at original
resolution. The reviewed code revision is `0214741`; the generated P3.8d
report records its full commit hash before the final documentation commit.
