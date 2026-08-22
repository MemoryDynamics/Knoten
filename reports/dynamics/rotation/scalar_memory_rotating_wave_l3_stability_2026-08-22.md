# P1 L3 non-Anchor rotating-wave stability

Generated: 2026-08-22T07:09:58.093406+00:00.

Decision: **numerically-stable-source-pass**.

The run used the unchanged protocol frozen at
d10d5321754a67a0672f6fdda78f5b55a2527d44 and clean execution
revision 8719f70273c29f7dbb2bcbab56610a0a706982c3.

## Prospective and full-map controls

- Frozen provenance pass: True
- Input replay pass: True
- Implementation controls: True
- Fixed-point max error: 3.08780779e-15
- Jacobian shape: [4800, 4800]
- Sparse nonzeros: 19196
- Analytic symmetry pass: True
- Full-map controls: True
- Runtime: 166.719 s

## Leading transverse multipliers

| panel | lambda | modulus | residual | decay rate | panel pass |
| --- | ---: | ---: | ---: | ---: | :---: |
| primary | 0.996442467 +0.0100748279i | 0.996493398 | 1.19825e-12 | 0.702552965 | True |
| convergence | 0.996442467 +0.0100748279i | 0.996493398 | 5.66606391e-13 | 0.702552965 | True |

- Panel agreement: True
- Complex difference: 7.85039858e-13
- Modulus difference: 7.67719222e-13
- Anchor decay rate per memory time: 0.696384366

## Registered perturbations

| perturbation | initial | maximum | final | max/initial | final/initial | stop |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| exact | 1.96623028e-18 | 2.22247919e-14 | 1.85921999e-14 | 11303.2497 | 9455.75912 | completed |
| visible_radial_plus | 8.70110205e-08 | 8.70110205e-08 | 1.75927237e-14 | 1 | 2.02189603e-07 | completed |
| visible_radial_minus | 8.70110198e-08 | 8.70110198e-08 | 1.83711149e-14 | 1 | 2.11135497e-07 | completed |
| visible_tangential_plus | 7.5403366e-08 | 7.56017329e-08 | 2.12659772e-14 | 1.00263074 | 2.82029547e-07 | completed |
| visible_tangential_minus | 7.54033645e-08 | 7.56017331e-08 | 1.91528874e-14 | 1.00263077 | 2.5400574e-07 | completed |
| full_history_transverse_plus | 2.93148136e-09 | 2.93148136e-09 | 1.47766745e-14 | 1 | 5.04068514e-06 | completed |
| full_history_transverse_minus | 2.93148165e-09 | 2.93148165e-09 | 1.60425162e-14 | 1 | 5.47249416e-06 | completed |

## Claim boundary

A pass concerns one prepared L3 spatial relative equilibrium in
the registered numerical panels. It is not a complete spectral
enclosure, stable-family, formation, topology, Loop--Center, work,
mass or interaction result. The critical review is mandatory before
P2 or any Paper claim is opened.
