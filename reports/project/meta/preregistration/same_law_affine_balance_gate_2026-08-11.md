# Preregistration: same-law affine-balance gate

Date: 2026-08-11.

## Trigger

The registered common-scale follow-up identified local stable-complex Jacobian
windows at four fixed separations. A Jacobian spectrum alone is not a normal-
mode result unless the expansion point is stationary. This gate was added
after that result and before any nonlinear pilot.

## Question and fixed law

For every distance that passed the common-scale full-matrix gate, place two
identical mature scalar-memory states at the same separation and orientation
used by the Jacobian audit. Use the fixed geometric-midpoint coupling from the
common-scale report for both self and cross readout.

Let \(F_1^{\rm cross}\) and \(F_2^{\rm cross}\) denote the two visible cross
gradients before multiplication by \(-\eta\). The deterministic affine drift
of the relative visible coordinate is

\[
b_{x,-}
=
-\frac{\eta}{2}
\left(F_1^{\rm cross}-F_2^{\rm cross}\right).
\]

The identical translated self states have identical self gradients, so their
contribution cancels from this relative residual at the initial geometry.

## Diagnostics and gate

For every direction and both available dimensions, report

\[
B_R=\frac{\lVert b_{x,-}\rVert}{R},
\qquad
B_{\rm mem}
=
\frac{\lVert b_{x,-}\rVert}{\lambda R_{\rm mem}}.
\]

The second number is the frozen-drift displacement over one memory time in
units of the mature memory radius. It is a screening diagnostic, not a
trajectory prediction.

- **affine-balance eligible:** one previously eligible distance has
  \(B_{\rm mem}\le 0.01\) for every direction in both dimensions;
- **affine-balance negative:** all previously eligible distances exceed this
  bound in at least one direction, and the point-deposit two-Gaussian law has
  no positive force-zero radius;
- **inconclusive:** a complete-state force zero is indicated despite the
  point-deposit result, or numerical/asymmetry effects prevent classification.

No distance, gain or threshold may be retuned after evaluation. A negative
result blocks the nonlinear same-law oscillation pilot: the earlier complex
windows then describe transient local curvature along a drifting geometry,
not an equilibrium normal mode.
