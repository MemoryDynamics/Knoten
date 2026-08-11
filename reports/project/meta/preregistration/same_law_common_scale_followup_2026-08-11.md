# Preregistration: same-law common-scale follow-up

Date: 2026-08-11.

## Trigger and question

The preregistered same-law Jacobian audit was inconclusive: the current
coupling produced only real modes, while the same-law cross/self ordering was
larger than one at some fixed separations. This follow-up is explicitly
post-audit and does not alter that decision.

The question is narrower: does one common rescaling of the canonical self and
cross law place all tested orientations, in both available mature states, in a
stable complex local regime at the same normalized separation?

## Fixed quantities

For every existing audit row, write the directional gains at the checkpoint
coupling \(\eta_0\) as \(g_0,c_0\). A common positive scale \(s\) gives

\[
g=s g_0,
\qquad
c=s c_0,
\qquad
\eta=s\eta_0.
\]

Self and cross gains may not be scaled separately. The memory relaxation
\(\lambda\), kernels, deposition rule, mature states, distances and
eigendirections remain those of the original audit.

For the scalar directional block, define

\[
T(s)=2-\lambda-s\left[(1-\lambda)g_0+(1+\lambda)c_0\right],
\]

\[
D(s)=(1-\lambda)\left[1-s(g_0+c_0)\right].
\]

The exact complex interval is the positive set on which

\[
\Delta(s)=T(s)^2-4D(s)<0,
\qquad
0<D(s)<1.
\]

## Fixed aggregation rule

For each preregistered normalized distance label:

1. compute the exact stable-complex scale interval for every direction in
   both checkpoints;
2. intersect all intervals across directions and dimensions;
3. if the intersection is non-empty, choose its geometric midpoint, with no
   numerical optimization;
4. at that one scale, recompute every full matrix
   \(A_-(sG,sC,\lambda)\).

The geometric midpoint is undefined when the common interval is empty. No new
distance may be introduced after inspecting the results.

## Decision rule

- **common-scale eligible:** at least one preregistered distance has a
  non-empty interval shared by every direction in both checkpoints, and every
  full matrix at its fixed midpoint is stable and contains a complex pair;
- **common-scale negative:** no preregistered distance has a non-empty common
  scalar interval;
- **matrix-inconclusive:** a common scalar interval exists, but at least one
  full matrix at its fixed midpoint is unstable or has no complex pair.

The report must list every common interval, not only the best one. Any eligible
distance and coupling authorize only a five-formation-seed \(N=500\,000\)
pilot under the unchanged same-law rule. They do not establish a persistent
oscillation, parameter self-selection, quantum dynamics or a physical
interaction law.
