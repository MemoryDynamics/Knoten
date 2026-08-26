# P2 local Loop--Center response at L3

Date: 2026-08-25.

Decision: **`loop-center-matrix-local-fail`**.

The full nonlinear finite-memory loop was compared with the frozen
full-FIFO tangent recurrence. No response pole, gain, damping, phase
or normalization was fitted.

## Analytic scalar comparator

| quantity | value |
| --- | ---: |
| origin curvature | -0.611111 |
| finite-H $g_H$ | -0.0458331 |
| scalar pole $q(1-g_H)$ | 1.0406 |
| decision | `scalar-origin-ineligible` |

This analytic result is separate from the matrix-local decision and
was not repaired by fitting an effective scalar gain.

## Controls

| control | observed | threshold | pass |
| --- | ---: | ---: | :---: |
| fixed point | 3.08781e-15 | 1e-14 | True |
| unrelated joint Jacobian | 1.43709e-10 | 2e-09 | True |
| center recurrence | 5.2237e-15 | 4.72403e-13 | True |
| rotation covariance | 8.30907e-17 | 1e-11 | True |
| probe off final D0 | 1.7709e-14 | 9.44806e-11 | True |

## Primary amplitude ladder

| direction | amplitude | state tangent error | center-velocity error | even leakage | first-order remainder | amplitude collapse | max D0/R | final/peak | tail slope | pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| radial | 1e-05 | 2.93194e-10 | 2.94293e-10 | 7.355e-06 | 7.35485e-06 | 0 | 3.94374e-06 | 0.00532288 | 0.0050913 | False |
| radial | 3e-05 | 2.6736e-10 | 3.80197e-10 | 2.20639e-05 | 2.20639e-05 | 2.86522e-10 | 1.18312e-05 | 0.00532288 | 0.0050913 | False |
| radial | 0.0001 | 2.83417e-09 | 3.87611e-09 | 7.3546e-05 | 7.35452e-05 | 2.6291e-09 | 3.94379e-05 | 0.00532289 | 0.00509132 | False |
| tangential | 1e-05 | 1.82595e-10 | 1.79454e-10 | 7.05137e-06 | 7.05123e-06 | 0 | 5.06886e-06 | 0.00438781 | 0.00594649 | False |
| tangential | 3e-05 | 6.20882e-10 | 6.94526e-10 | 2.11582e-05 | 2.11576e-05 | 4.9547e-10 | 1.52067e-05 | 0.00438781 | 0.0059465 | False |
| tangential | 0.0001 | 6.54184e-09 | 7.46257e-09 | 7.05288e-05 | 7.05225e-05 | 6.40343e-09 | 5.06908e-05 | 0.00438782 | 0.00594654 | False |

## Quadratic remainder and waveform holdout

| panel | direction | diagnostic | value | pass |
| --- | --- | --- | ---: | :---: |
| primary | radial | remainder secant slope | 1.99999 | True |
| primary | tangential | remainder secant slope | 1.99997 | True |
| holdout | radial | state / center tangent error | 2.05706e-10 / 2.75221e-10 | False |
| holdout | tangential | state / center tangent error | 4.5643e-10 / 5.25798e-10 | False |

## Decision and limits

Gate components: `{"complete_traces": true, "controls": true, "primary_response": false, "quadratic_remainder_slopes": true, "signals_above_floor": true, "waveform_holdout": false}`.

A pass supports only the local matrix-valued response of this one
prepared L3 loop. The exact center readout and covariance controls
are structural. The finite amplitude ladder, quadratic remainder,
waveform holdout and D0 recovery are the discriminating numerical
content.

The result does not transfer the former scalar B-star filter mass
to L3 and does not identify a microscopic center-conjugate port.
Formation, a finite basin, physical work or mass, internal topology
and interactions remain outside P2.

## Provenance

- freeze revision: `60aa3d12f891008eb579dcf56e96cf8fbb3fa54d`;
- execution revision: `ba07277c64e25b5f51576827ad8d3727852ac592`;
- JSON SHA-256: `697b9e9782fa5ba8cf694f8a84c6a931171cdec8a53b42605cb6b7971bc20656`;
- elapsed seconds: `39.5142`;
- Python / NumPy / SciPy: `3.12.13` / `2.3.5` / `1.17.1`.
