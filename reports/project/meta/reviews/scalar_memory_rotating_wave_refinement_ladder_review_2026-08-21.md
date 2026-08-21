# Critical review: scalar-memory rotating-wave refinement ladder

Date: 2026-08-21.

Formal verdict: **certified-roots-nonconvergent**, exactly as required by the
preregistered decision rule.

Scientific verdict: **all five matched cells possess locally unique exact
finite-\(H\) roots and form a striking first-order Cauchy sequence, but the
ladder fails two Richardson comparisons to a mismatched pre-existing
continuum guide.** The formal decision must not be rewritten. The failure is
more informative about the guide definition than about the existence of a
continuum root family.

## 1. Prospective integrity

The five cells, common initial geometry, independent cell starts, two
precision panels, Newton count, branch corridor, interval boxes, continuum
guide and scaling thresholds were committed and pushed at clean revision
b03ff433776ced084f8bf3d56b54b8fe7b1e5ef2 before any non-anchor cell was
evaluated. The run began from that clean revision.

Every cell kept

\[
H\alpha=12,\qquad \eta/\alpha=15,
\]

with \(A_{\rm att}=3.5\) and every other native kernel parameter fixed. The
\(A_{\rm att}=7\) holdout remained sealed.

## 2. Strong positive cellwise result

All five cells passed both 80- and 120-digit Krawczyk panels, every
sign/gain control, the common branch corridor and cross-precision agreement.
The anchor enclosure overlaps the earlier unique-root certificate.

| \(\alpha\) | \(H\) | \(\eta\) | certified \(R\) center | certified \(\Omega=\theta/\alpha\) center |
| ---: | ---: | ---: | ---: | ---: |
| 0.04 | 300 | 0.60 | 0.9572176121167313 | 1.5500365078147323 |
| 0.02 | 600 | 0.30 | 0.9500002957808805 | 1.5682772012588133 |
| 0.01 | 1200 | 0.15 | 0.9465175048042240 | 1.5770381717134992 |
| 0.005 | 2400 | 0.075 | 0.9448058117057437 | 1.5813322924871047 |
| 0.0025 | 4800 | 0.0375 | 0.9439571883620176 | 1.5834581705422748 |

Thus the anchor is not an isolated finite-grid accident. At five fixed
native parameter cells, the exact balance possesses a locally unique root
on the same registered branch corridor.

## 3. Registered scaling decision

Six of eight scaling gates passed:

- both radius and frequency errors relative to the frozen guide decrease
  monotonically;
- the L1--L4 log-log slopes are \(0.9620\) for \(R\) and \(0.8228\) for
  \(\Omega\), inside the registered \([0.8,1.2]\) interval;
- the L4-to-anchor error ratios are \(0.2699\) and \(0.3435\), below \(0.35\).

The two Richardson-to-guide gates failed:

\[
\frac{|R_{\rm Rich}-R_\infty^{\rm guide}|}{e_R(0.0025)}
=0.1033>0.1,
\]

\[
\frac{|\Omega_{\rm Rich}-\Omega_\infty^{\rm guide}|}
{e_\Omega(0.0025)}
=0.3670>0.1.
\]

The radius miss is marginal; the frequency miss is decisive. Under the
frozen rule, the composite gate therefore cannot pass.

## 4. The target mismatch

The pre-existing discovery record itself states that its continuum
initializer has

\[
R_\infty^{\rm guide}=0.9430108292781663,\qquad
\Omega_\infty^{\rm guide}=1.5868166272376472,
\]

but requires

\[
\widehat\eta_{\rm guide}=15.016345187237246.
\]

It was selected because this gain was closest on the registered continuum
grid to the desired value 15. The finite-\(H\) ladder, however, fixes
\(\eta/\alpha=15\) exactly in every cell. The protocol therefore compared a
fixed-gain discrete sequence to a continuum point belonging to a different
gain.

This is not amplitude retuning and does not invalidate any certified cell.
It is a target-definition error in the refinement protocol. Because it was
visible in the already committed discovery JSON, it should have been caught
before the ladder was frozen.

## 5. Post-result diagnostic, not a gate

Successive cell differences contract as follows:

| halving step | \(dR_{\rm next}/dR_{\rm previous}\) | \(d\Omega_{\rm next}/d\Omega_{\rm previous}\) |
| --- | ---: | ---: |
| 0.04 to 0.02 to 0.01 | 0.4826 | 0.4803 |
| 0.02 to 0.01 to 0.005 | 0.4915 | 0.4901 |
| 0.01 to 0.005 to 0.0025 | 0.4958 | 0.4951 |

Ratios tending to \(1/2\) are the expected signature of first-order
convergence under \(\alpha\)-halving. A quadratic extrapolation of the three
finest cells gives approximately

\[
R_0=0.9431133805,\qquad \Omega_0=1.5855699270,
\]

not the frozen guide. These are post-result diagnostics and must not replace
the registered decision or become unregistered confirmation targets.

## 6. Correct sequential response

The result justifies one explicitly post-result reconciliation, not a
threshold relaxation:

1. freeze the continuum equations at exactly
   \(\widehat\eta=15\), \(C=12\) and the existing kernel;
2. start from the old pre-ladder guide, not from the ladder extrapolation;
3. solve with fixed independent quadrature orders and root tolerances;
4. compare the already frozen ladder to that corrected target using the
   original scaling thresholds;
5. preserve the historical label certified-roots-nonconvergent regardless
   of the reconciliation outcome.

Non-anchor stability, formation, noise, topology, the amplitude holdout,
work and mass remain unopened.
