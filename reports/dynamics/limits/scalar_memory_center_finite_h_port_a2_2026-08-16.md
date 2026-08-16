# Finite-H center-port Gate A2

Generated: 2026-08-16T10:07:42.311542+00:00.

Decision: **`finite-h-effective-center-port-pass`**.

This deterministic certificate was run from the clean preregistered
revision `2792ca17d076f2e00f628092790e78b188dfa18c`. No stochastic target
trace, new seed, or sealed transfer cell was opened.

## Registered finite-memory certificate

For the normalized finite geometric memory,

\[
B_H(z)={\alpha\over1-q^H}{1-q^Hz^{-H}\over1-qz^{-1}},
\qquad
G_H(z)={(z-1)B_H(z)\over z-(1-g)-gB_H(z)}.
\]

The report uses a global analytic perturbation bound from
\(G_\infty(z)=\alpha z/[z-q(1-g)]\). The dense frequency grid is
only a sanity check and cannot decide the gate.

| alpha | H | q^H | small-gain bound | certified min Re G_H | safety | grid min Re G_H | decision |
|---:|---:|---:|---:|---:|---:|---:|:---:|
| 0.04 | 300 | 4.8014224e-06 | 4.7617641e-05 | 0.022131667 | 1872.9184 | 0.02214349 | pass |
| 0.02 | 600 | 5.4405827e-06 | 5.3079144e-05 | 0.010504458 | 808.9877 | 0.010517459 | pass |
| 0.01 | 1200 | 5.7840697e-06 | 5.5975192e-05 | 0.005113535 | 376.48768 | 0.0051271534 | pass |
| 0.005 | 2400 | 5.962025e-06 | 5.7465643e-05 | 0.0025175829 | 181.67279 | 0.0025315174 | pass |
| 0.0025 | 4800 | 6.0525853e-06 | 5.8221614e-05 | 0.0012437514 | 89.244498 | 0.0012578458 | pass |

## Decision boundary

A pass establishes an exact passive finite-H input/output
realization for the registered local linear plant and permits a
reciprocal discrete-gradient wrapper. It does not identify the
memory centroid as material mass or derive a microscopic natural
actuator. Consequently only the separately labelled B-star filter
scaling study is authorized; physical B remains blocked.

The S1 branch remains sealed because this real-pole center plant is
not an S1 candidate.
