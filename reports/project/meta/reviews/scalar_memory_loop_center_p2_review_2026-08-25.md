# Critical review: P2 local Loop--Center response at L3

Date: 2026-08-25.

Verdict: **uphold the registered `loop-center-matrix-local-fail`, while
separating that formal decision from the strongly positive local-response
diagnostics.** The scalar-origin Center merger is analytically ineligible at
L3. The full matrix-valued tangent model predicts the nonlinear response with
large margin, but every nonzero arm violates the registered absolute tail-
slope threshold. P3 therefore remains closed.

The failure does not look like secular escape. A post-decision sign audit of
the immutable traces finds strictly negative late slopes and monotone decay at
every stored tail sample. The registered metric nevertheless used the
absolute slope and therefore rejects a trajectory that is still returning but
has not become sufficiently flat after ten recovery memory times. This is a
protocol-design limitation, not grounds to relabel the decision.

## 1. Prospective integrity

The linearization audit and complete P2 protocol were published in revision
`60aa3d12f891008eb579dcf56e96cf8fbb3fa54d`, before a forced L3 response was
opened. The implementation was then independently published in clean revision
`ba07277c64e25b5f51576827ad8d3727852ac592`. Before the target run:

- all 756 repository tests passed;
- the strict documentation build passed;
- focused state/input finite-difference and decision-semantic tests passed;
- NumPy 2.3.5 and SciPy 1.17.1 matched the P1 environment;
- the protocol, P1 result, P1 review and native map/Jacobian Git blobs matched
  their frozen values.

The target run began with an empty Git status. The immutable result was
committed separately in revision `30abc44`. Its JSON SHA-256 is
`697b9e9782fa5ba8cf694f8a84c6a931171cdec8a53b42605cb6b7971bc20656`.
No candidate parameter, waveform, amplitude, duration, threshold or decision
rule changed after target access.

## 2. The scalar Center merger fails analytically

At L3,

$$
\kappa_K=-0.611111111111\ldots,
\qquad
g_H=-0.045833060074\ldots,
$$

and the corresponding untruncated scalar pole is

$$
q(1-g_H)=1.040603894773\ldots>1.
$$

Thus the positive-$g_H$ scalar plants certified by A2 and B-star do not
include the finite-radius loop. This result was computed and published before
the P2 response. No effective positive gain was fitted afterward. The earlier
scalar filter-inertia result therefore cannot be transferred to L3.

This does not imply that every linear description fails. It selects the full
FIFO tangent operator around the finite-radius nonlinear state as the relevant
local linear theory.

## 3. Controls and implementation audit

All registered controls pass:

| control | observed | threshold |
| --- | ---: | ---: |
| co-rotating fixed point | $3.09\times10^{-15}$ | $10^{-14}$ |
| unrelated joint state/input Jacobian | $1.44\times10^{-10}$ relative | $2\times10^{-9}$ |
| direct versus retiring-sample Center recurrence | $5.22\times10^{-15}$ | $4.72\times10^{-13}$ |
| four-phase rotation covariance | $8.31\times10^{-17}$ normalized | $10^{-11}$ |
| final probe-off D0 distance | $1.77\times10^{-14}$ | $9.45\times10^{-11}$ |

Every registered branch completed all 2400 updates with finite values. The
phase control is an equivariance check and the Center recurrence is an exact
identity; neither is independent evidence for dynamics.

## 4. How linear is the tested response?

Within the frozen amplitude range, very strongly linear:

| diagnostic | worst primary value | registered limit |
| --- | ---: | ---: |
| odd full-state tangent error | $6.54\times10^{-9}$ | $5\times10^{-3}$ |
| odd Center-velocity tangent error | $7.46\times10^{-9}$ | $5\times10^{-3}$ |
| mirrored even leakage | $7.35\times10^{-5}$ | $2\times10^{-2}$ |
| single-sign first-order remainder | $7.35\times10^{-5}$ | $2\times10^{-2}$ |
| normalized amplitude-collapse error | $6.40\times10^{-9}$ | $5\times10^{-3}$ |

The single-sign absolute remainder has log--log secant slopes 1.99999 radial
and 1.99997 tangential between the two largest amplitudes. This is the
registered quadratic scaling. The independent Hann-doublet waveform also has
state and Center-velocity tangent errors below $5.3\times10^{-10}$.

The tiny odd errors should not be overinterpreted. Mirroring cancels the
leading even, quadratic term, so the odd response is expected to agree more
closely with the derivative than a single branch. The single-sign remainder
is the more direct finite-amplitude measure and is still only about
$7.4\times10^{-5}$ relative at $\epsilon=10^{-4}$.

This demonstrates that the chosen finite window is deeply local. It validates
the tangent implementation and its finite-amplitude adequacy; it is not an
independent discovery of a new inertial law or a test of a macroscopic basin.

## 5. Loop preservation and the formal failure

The largest quotient deformation is only

$$
\max D_0/R=5.07\times10^{-5},
$$

well below the registered $10^{-2}$ ceiling. After the 2000-update recovery,
the worst final-to-peak ratio is 0.005323, also below its 0.05 limit.

The failing diagnostic is the absolute slope over the last 400 updates:

| panel | direction | absolute slope per memory time | limit |
| --- | --- | ---: | ---: |
| sine amplitudes | radial | 0.0050913 | 0.001 |
| sine amplitudes | tangential | 0.0059465 | 0.001 |
| Hann holdout | radial | 0.0049456 | 0.001 |
| Hann holdout | tangential | 0.0057360 | 0.001 |

The values are amplitude independent to the displayed precision, as expected
in the measured linear regime. They exceed the threshold by factors 4.95 to
5.95, so this is not a rounding contact.

The protocol says **absolute** slope. Therefore all six primary rows and both
holdout rows fail, and the machine decision is correct.

## 6. Post-decision sign audit

The result JSON stores D0 every ten updates. A non-decisional audit of the last
400 updates gives:

- signed normalized slopes from $-0.00496$ to $-0.00595$ per memory time;
- zero increases in every one of the 40 stored tail intervals for every plus
  and minus branch;
- log-distance decay rates 0.541--0.545 radial and 0.647--0.657 tangential per
  memory time.

Thus the observed late motion is inward recovery, not outward secular drift.
The absolute-slope rule tests whether the trace is already nearly flat. It
does not distinguish a slowly decreasing tail from a slowly increasing one.
The rule is consequently conservative for the intended drift question and,
in retrospect, poorly targeted.

These sign and log-rate calculations use already published thinned traces.
They are post-decision diagnostics and cannot satisfy the failed criterion.
An extended recovery run would be a new, outcome-informed reconciliation,
not an independent replication and not a relabeling of P2.

## 7. Matrix versus scalar effective coupling

At the middle amplitude, the tangent Center-velocity RMS differs between the
two registered directions by a factor 1.562. This diagnostic is compatible
with the age-distributed anisotropic Hessian blocks of the finite-radius loop.
It is not a formal scalar-model likelihood comparison, but it reinforces why
a single isotropic $g_H$ would be an inadequate local replacement even apart
from its wrong sign at the origin.

The defensible hierarchy is therefore:

1. $B_H$ is an exact linear kinematic readout;
2. the full FIFO Jacobian is an excellent local effective coupling in the
   tested window;
3. the nonlinear Double-Gaussian law remains essential to select and support
   the finite-radius background about which that Jacobian is taken;
4. neither the additive visible-state probe nor the Center readout identifies
   a microscopic center-conjugate physical port.

## 8. Reviewer decision and downstream consequence

The machine fail is upheld exactly. It has two scientifically distinct parts:

- **analytic negative result:** the old scalar positive-$g_H$ Center merger
  does not apply to L3;
- **formal numerical fail:** the matrix-local panel misses only the absolute
  tail-flatness bound, despite strong tangent agreement and monotone recovery.

The strongest allowed statement is:

> The prepared L3 loop has a phase-covariant nonlinear weak response that is
> accurately predicted by the full matrix-valued FIFO tangent model over the
> registered amplitudes and both waveforms. The registered P2 gate nonetheless
> fails because the quotient recovery tail remains steeper in magnitude than
> the frozen flatness threshold after ten memory times.

P3 formation/Basin testing is not authorized by this result. A future
sign-sensitive long-recovery reconciliation may distinguish convergence from
late outward drift, but it must retain the P2 fail, disclose its
outcome-informed origin, use no parameter retuning and make no physical mass
or microscopic-port claim.
