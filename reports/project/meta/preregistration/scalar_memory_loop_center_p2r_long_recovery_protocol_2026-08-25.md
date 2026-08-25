# Prospective P2-R gate: sign-sensitive L3 long recovery

Date: 2026-08-25.

Status: **frozen before any L3 response is advanced beyond the original P2
endpoint at update 2400.**

This is an explicitly outcome-informed reconciliation. The original
`loop-center-matrix-local-fail` remains immutable. P2-R asks a narrower new
question: whether the negative, monotonically decreasing tail visible after
the P2 decision continues to converge or reverses into plateau, oscillation or
outward drift under longer observation.

## 1. Why this follow-up exists

The original P2 gate passed every control, tangent-response, mirrored-
linearity, quadratic-remainder, waveform and maximum/final D0 bound. Every
response row failed only the registered absolute tail-slope ceiling. The
post-decision review showed that all stored late slopes had negative sign.

The absolute value was appropriate as a conservative flatness criterion but
did not answer the intended drift question. P2-R therefore changes no model
parameter and does not reinterpret that decision. It prospectively measures
the sign and log rate of a longer recovery.

## 2. Frozen provenance and scope

The selection base is revision
`384cc0dca6a2dccfa407e27462b6774784ee5a7e`. The authoritative P2 JSON, its
review, the P2 protocol, the candidate, the native map and the response
implementation must match their Git blobs. The runner requires a clean
worktree and the P2 decision
`loop-center-matrix-local-fail` with JSON SHA-256
`697b9e9782fa5ba8cf694f8a84c6a931171cdec8a53b42605cb6b7971bc20656`.

The unchanged candidate is

$$
(\alpha,H,\eta)=(0.005,2400,0.075),
\quad
(A_{\rm rep},A_{\rm att})=(1,3.5),
\quad
(\sigma_{\rm rep},\sigma_{\rm att})=(1,3).
$$

No kernel, gain, radius, angle, port, amplitude, direction, waveform or
response normalization may change. No fit is allowed.

## 3. Complete frozen replay panel

All original nonzero rows are rerun from the prepared circular history:

- primary sine-cycle waveform at amplitude fractions
  $10^{-5},3\times10^{-5},10^{-4}$;
- Hann-doublet holdout at $3\times10^{-5}$;
- radial and tangential laboratory directions;
- independent plus and minus branches;
- an exact probe-off clone.

This gives eight response rows and sixteen signed branches. Each has the same
400 driven updates as P2. Recovery is extended from 2000 to 4000 probe-off
updates, so the new endpoint is update 4400, or 20 recovery memory times.

Before the extension is evaluated, the unchanged P2 runner is executed in
memory and must reproduce the authoritative 2400-update result. Every scalar
decision metric and control must agree within

$$
|x_{\rm replay}-x_{\rm old}|
\le 5\times10^{-15}+5\times10^{-12}|x_{\rm old}|.
$$

The decision and every row's pass flag must agree exactly. The independently
advanced long-recovery path must additionally reproduce maximum D0, final D0
ratio and absolute tail slope at update 2400 under the same tolerance. A
replay mismatch makes P2-R `inconclusive`; it may not be repaired by changing
tolerances after inspection.

## 4. Frozen late windows and observables

Let $D_n^\pm$ be the established D0 proper-rotation/translation quotient
distance of each forced branch from its simultaneous probe-off clone. For each
branch define its full-run peak $D_{\max}^\pm$ and evaluate three disjoint
400-update windows:

$$
W_1=3201{:}3600,
\qquad
W_2=3601{:}4000,
\qquad
W_3=4001{:}4400.
$$

For each branch and window the runner records:

1. the signed least-squares slope of $D_n/D_{\max}$ per memory time;
2. the log-distance decay rate
   $-d\log D/dt_{\rm memory}$;
3. the largest ten-update sampled increase
   $D_{n+10}/D_n-1$;
4. the minimum distance relative to the peak, as a numerical signal check.

The D0 trace is evaluated every update for regression and every tenth update
for the monotonic-envelope diagnostic. No response-dependent window shift is
allowed.

## 5. Frozen recovery gates

Every plus and minus branch must satisfy all of the following:

- signed normalized slope strictly below zero in $W_1,W_2,W_3$;
- log-distance decay rate in $[0.2,1.5]$ per memory time in every window;
- maximum sampled ten-update increase at most `0.01` in every window;
- final distance at update 4400 at most $5\times10^{-4}$ of the branch peak;
- every distance in $W_3$ at least $10^{-8}$ of the branch peak, otherwise
  the sign/rate test is numerically `inconclusive`;
- no point after the drive exceeds `1.25` times the branch peak.

The log-rate interval is centered broadly around the pre-P2 P1 transverse
rate 0.702553 and is not fitted to the P2 tail. The final-ratio ceiling demands
at least another order of magnitude beyond the observed P2 endpoint and
remains ten times tighter than the old 0.0053 value. These choices are
outcome-informed and must be reported as such.

The extended probe-off clone must remain below $10^{-10}R$ in final D0.

## 6. Decision semantics

- **`p2r-sign-sensitive-long-recovery-pass`:** provenance and both replay
  controls pass, every branch/window passes the sign, log-rate, envelope,
  final-ratio and signal gates, and probe-off passes.
- **`p2r-sign-sensitive-long-recovery-fail`:** all traces and replays are
  valid, but at least one scientific recovery gate fails.
- **`p2r-sign-sensitive-long-recovery-inconclusive`:** provenance, replay,
  finite-trace, signal-floor or numerical-control failure prevents a
  scientific decision.

The old P2 decision remains `loop-center-matrix-local-fail` under every P2-R
outcome. A reviewed P2-R pass would support continued local recovery of the
prepared loop and may open P3 under the updated project priorities. It would
not be an independent replication, would not make the scalar-origin Center
model eligible, and would not establish formation, a finite basin, a
microscopic center-conjugate actuator, work or physical mass.
