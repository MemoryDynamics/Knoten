# Critical review: P1 L3 non-Anchor rotating-wave stability

Date: 2026-08-22.

Verdict: **uphold the registered `numerically-stable-source-pass` as local
numerical transverse-stability evidence for one prepared L3 relative
equilibrium.** Together with the Anchor this gives two tested matched scales.
It does not establish a complete spectral enclosure, stability of the six-cell
existence ladder, formation, an internal phase, mechanics, interactions or
mass.

## 1. Prospective integrity and immutable inputs

The selection audit began from main revision
`e10da5cad0ad85868b8c33ace9e3dd8c5baae9a6`, where no L3 Jacobian spectrum or
L3 perturbation continuation existed. The selection rule used only the
certified ladder direction and full-state cost: among the finer certified
cells L3--L5, choose the smallest state. This fixed

\[
(\alpha,H,\eta)=(0.005,2400,0.075),
\qquad H\alpha=12,
\qquad \eta/\alpha=15,
\]

before any stability proxy was opened.

The complete scientific protocol was published in freeze revision
`d10d5321754a67a0672f6fdda78f5b55a2527d44`, Git blob
`548ff395b21e16c894bc11e536023f19c0cc64cd`. The tested implementation was
then published separately as revision
`8719f70273c29f7dbb2bcbab56610a0a706982c3`. Before the first target run,
full repository linting, 742 tests and the strict documentation build passed
locally. Two decision-edge defects found during that pre-run review were
closed conservatively: instability now requires the matched Ritz pair, and a
missing, stopped or nonfinite exact arm can only yield an inconclusive result.
Neither change altered a candidate, panel, perturbation, threshold or stop.

The target run started from exactly that clean implementation revision under
Python 3.12.13, NumPy 2.3.5 and SciPy 1.17.1. All frozen dependency Git blobs
matched. The authoritative result JSON has SHA-256
`aeae8877670e4c63c2b67864236ac810cb35e4852e9428097eda2a61fe67bd90`
and Git blob `18821ed0235e5e915424f61c665be86d569d58cc`.

There is one immutable typesetting defect in the protocol: four display rows
contain the literal separator `quad` where `\quad` was intended. The prose,
candidate identifier, exact decimal center, dependency JSON and executable
registration all give the same unambiguous parameter tuple. The defect has no
numerical consequence and the executed protocol has not been silently edited.

## 2. Object under test

The 120-digit interval-certified balance center was converted to binary64 for
the full-FIFO stability calculation:

\[
R_3=0.9448058117057436564\ldots,
\qquad
\theta_3=0.0079066614624355237\ldots.
\]

The prepared circular history is a fixed point of the co-rotating map to
maximum component error (3.09\times10^{-15}), below the registered
(10^{-14}) bound. This is a one-step relative equilibrium in a
4800-dimensional finite-memory state. It is not a demonstrated integer-period
orbit: (2\pi/\theta_3\simeq794.67) updates.

The continuous family of globally rotated copies is the ambient (SO(2))
group orbit. It collapses to one point after the declared rotation quotient;
the calculation does not create a second internal (S^1).

## 3. Independent and analytic controls

Every control passed before Arnoldi was accepted:

| control | observed | registered bound |
| --- | ---: | ---: |
| unrelated (H=17) Jacobian finite difference | relative error (1.36\times10^{-10}) | (2\times10^{-9}) |
| production-kernel/FIFO replay | maximum error (0) | (2\times10^{-15}) |
| D0 translation/rotation quotient | distance (2.21\times10^{-15}) | (4\times10^{-15}) |
| candidate fixed point | (3.09\times10^{-15}) | (10^{-14}) |
| rotation-tangent residual | (6.17\times10^{-16}) | (10^{-10}) |
| translation-tangent residuals | (1.81,3.85\times10^{-17}) | (10^{-10}) |

The sparse Jacobian has the registered shape (4800\times4800) and exactly
19196 stored entries. The production replay is an implementation-independence
control for the update convention, not an independent derivation of the
spectrum.

## 4. Spectral evidence and symmetry separation

Both frozen largest-modulus panels converged and returned all 32 and 48
requested Ritz pairs. Their largest normalized residuals are
(6.82\times10^{-11}) and (1.56\times10^{-12}), both below (10^{-8}).
Each panel recovers exactly the expected two translation multipliers
(e^{\pm i\theta_3}) and the rotation multiplier 1. Their translation
overlaps are numerically 1; the rotation overlap is 0.999978.

The matched leading transverse pair is

\[
\lambda_{\perp,3}
=0.996442466747+0.010074827926i,
\qquad
|\lambda_{\perp,3}|=0.996493397718.
\]

The two panels differ by (7.85\times10^{-13}) in the complex plane and
(7.68\times10^{-13}) in modulus. The value lies 0.0034066 below the
registered pass boundary (1-10^{-4}=0.9999). Its maximum symmetry overlap is
only 0.234 with translations and 0.063 with rotation, so the transverse label
is not a threshold contact.

As a non-decision post-hoc check, every value in the 32-pair primary panel has
a partner in the 48-pair panel within (1.11\times10^{-9}). The smaller panel
does truncate one conjugate pair at its lowest-modulus boundary: the returned
(0.9943317+0.0297089i) value has no conjugate inside that 32-value table,
whereas the larger panel restores the pairing. This does not affect the
leading multiplier or the registered decision, but it is direct evidence that
the tables are truncated samples rather than a complete spectrum.

In memory time the leading rate is

\[
\gamma_3=-\frac{\log|\lambda_{\perp,3}|}{\alpha}
=0.702553,
\]

only 0.886% above the Anchor value 0.696384. This is encouraging two-scale
consistency, not a convergence theorem.

## 5. Nonlinear return and non-normality

All six nonzero arms complete 10000 updates, equal to 50 memory times and
about 12.58 rotations. The largest observed transient factor is only 1.002631
in a tangential arm; the other four radial/full-history arms never exceed
their initial D0 distance. Final-to-initial ratios range from
(2.02\times10^{-7}) to (5.47\times10^{-6}), far below the registered 0.1
bound.

The exact arm remains below (2.23\times10^{-14}) in absolute D0 distance,
comfortably below (10^{-10}). Its large ratio to its (1.97\times10^{-18})
initial numerical denominator is not a physical amplification; the gate
correctly uses the absolute exact-control bound.

Mirrored arms agree in their maximum distances to relative error at most
(1.01\times10^{-7}). Their final relative differences reach 9.94%, but all
final absolute distances are only (1.48\times10^{-14}) to
(2.13\times10^{-14}); that percentage is numerical-floor amplification,
not detectable chirality selection.

The nonlinear panel remains sparse: it samples three directions and their
signs at one amplitude. It neither bounds the induced transient-growth norm
of this non-normal delayed map nor measures a basin radius. The absence of
registered transient growth therefore supports only the declared local
return statement.

## 6. Strongest falsifiers that remain open

1. ARPACK uses two starts and panel sizes but one SciPy/ARPACK backend. It
   provides no theorem that an omitted eigenvalue has modulus below one. A
   validated characteristic-root method, full spectral enclosure or an
   independent high-precision backend could still overturn spectral
   completeness.
2. The two stable cells are Anchor and L3 only. L0, L1, L4 and L5 have local
   existence certificates but no stability result. Six stable cells or a
   stable family is unsupported.
3. Every trajectory starts at or (10^{-7}R_3) from a prepared circular
   history. No noncircular history has formed the loop; basin, chirality
   selection and noise robustness remain untested.
4. The interval existence certificates still share `mpmath.iv` 1.3.0. A
   second outward-rounded interval backend remains publication hardening.
5. The open write/forget ledger is unchanged. Local attraction supplies no
   microscopic actuator, conserved momentum, work balance or physical mass.

## 7. Reviewer decision and sequential consequence

No observed control, registered threshold or post-hoc diagnostic contradicts
the machine pass. The decision is therefore upheld with the exact claim:

> The unchanged native finite-memory map has local numerical transverse-
> stability evidence for the prepared L3 relative equilibrium in both
> registered largest-modulus Ritz panels and all six registered perturbation
> arms. Together with the Anchor, stability has been tested positively at two
> matched scales, not proved for the existence ladder.

P1 is complete at that scope. P2, a separately preregistered Loop--Center
compatibility test on this same frozen L3 candidate without retuning, may now
be designed. No P2 observable has yet been tested, and formation, topology,
mechanics, interactions and mass remain sealed by their own gates.
