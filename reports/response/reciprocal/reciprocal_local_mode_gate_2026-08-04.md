# Reciprocal local-mode gate

Status: structural analytic gate. Date: 2026-08-04.

## Question

Can a synchronous reciprocal return channel between two scalar-memory knots
produce a stable complex relative mode without adding inertia or an explicit
wave equation?

## Result

For the local reduction, stable complex modes require both a negative mode
discriminant and multipliers inside the unit circle. A positive cross-gain
window exists only when

$$
g < \frac{\lambda}{1+\lambda}.
$$

At $\lambda=0.01$ the threshold is `0.0099009901`. The
current compact-knot baseline has local curvature `2.8888889` and
$g=0.43333333$, so it has no stable complex cross-gain interval.

For the weak-self witness $g=0$, the stable complex interval is
`(0.0017228756, 0.056898828)`. At $c=0.02$ the
frequency is `0.013314774` per update and the
damping rate is `0.015126522` per update.

The condition $c>g$ is necessary inside the stable complex region. In contrast,
$g+c>1$ makes the determinant negative and therefore gives two real
opposite-sign multipliers. Those multipliers can still both lie inside the unit
circle; this is an alternating real mode, not a harmonic oscillator.

## Interpretation

- **Evidence:** the common/relative formulas match the full four-state matrix;
  the regime boundaries are analytic and unit-tested.
- **Inference:** an instantaneous reciprocal continuation of the current
  compact checkpoints should be treated as a real-mode null and nonlinear
  reconciliation test.
- **Hypothesis:** a retarded reciprocal mediator may create sufficient phase lag
  for a complex mode at compact-knot self gain.
- **Not supported:** charge, flavor, particle identity, spatial rotation, or
  ambient-independent three-dimensional selection.

The complex rotation here is in the state-space plane $(x_-,m_-)$ and already
exists in a one-dimensional spatial model. It cannot by itself explain $d=3$.

## Registered next gate

Use mature stored knot states and common noise in four paired arms:

1. channel off;
2. one-way cross-readout;
3. synchronous instantaneous reciprocal cross-readout;
4. reciprocal readout through one fixed local mediator.

Primary observables are relative-center multipliers, damping, frequency, phase
continuity, radius and shape bounds, and separation from the paired controls.
No cross-gain retuning follows a failed instantaneous arm.

![Reciprocal mode regime map](../../figures/draft/response/reciprocal_mode_regime_lambda001_2026-08-04.png)

Machine-readable summary: [reciprocal_local_mode_gate_2026-08-04.json](reciprocal_local_mode_gate_2026-08-04.json).
