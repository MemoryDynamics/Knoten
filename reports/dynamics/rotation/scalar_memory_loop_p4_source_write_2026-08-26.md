# P4 reciprocal orbit-center source/write mechanics

Date: 2026-08-26.

Decision: **`p4-source-write-architecture-fail`**.

The gate uses an exact linear orbit-center notch and adjoint port on
the full nonlinear native L3 FIFO map. No mass, momentum state or
second-order equation is inserted.

## Gate summary

| gate | status |
| --- | :---: |
| `pipeline` | pass |
| `registration` | pass |
| `complete` | pass |
| `informative_signal` | pass |
| `response_available` | pass |
| `reciprocal_ledger` | fail |
| `nonlinear_loop_mechanics` | fail |

## Static architecture controls

| control | maximum/observed | status |
| --- | ---: | :---: |
| coefficient identities | 9.15513e-16 | pass |
| target-center error | 9.48575e-16 | pass |
| adjoint virtual-work error | 2.08167e-17 | pass |
| truncated-ledger omitted fraction | 0.0948561 | pass |

## Active arms

| arm | dynamic | ledger | max D0/R | final separation/delta | C projection | Q projection | energy ratio | max ledger/U0 |
| --- | :---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `splus_x_offsetplus_d0.0005` | fail | fail | 2.46038e-05 | 0.0843668 | 0.224281 | 0.287804 | 0.00711776 | 9.59552e-12 |
| `splus_x_offsetplus_d0.0010` | fail | fail | 4.92069e-05 | 0.0843668 | 0.22428 | 0.287804 | 0.00711776 | 3.39876e-12 |
| `splus_x_offsetplus_d0.0020` | fail | fail | 9.84106e-05 | 0.0843668 | 0.22428 | 0.287803 | 0.00711776 | 2.01872e-12 |
| `splus_x_offsetminus_d0.0005` | fail | fail | 2.46046e-05 | 0.0843668 | 0.224281 | 0.287805 | 0.00711776 | 8.60217e-12 |
| `splus_x_offsetminus_d0.0010` | fail | fail | 4.921e-05 | 0.0843668 | 0.224281 | 0.287805 | 0.00711776 | 4.01552e-12 |
| `splus_x_offsetminus_d0.0020` | fail | fail | 9.84231e-05 | 0.0843668 | 0.224282 | 0.287805 | 0.00711776 | 2.27499e-12 |
| `splus_y_offsetplus_d0.0005` | fail | fail | 3.43214e-05 | 0.0815277 | 0.257547 | 0.318789 | 0.00664677 | 7.3834e-12 |
| `splus_y_offsetplus_d0.0010` | fail | fail | 6.86451e-05 | 0.0815275 | 0.257549 | 0.318791 | 0.00664673 | 3.94983e-12 |
| `splus_y_offsetplus_d0.0020` | fail | fail | 0.000137299 | 0.081527 | 0.257553 | 0.318794 | 0.00664666 | 2.07822e-12 |
| `splus_y_offsetminus_d0.0005` | fail | fail | 3.43192e-05 | 0.0815281 | 0.257544 | 0.318786 | 0.00664684 | 8.88013e-12 |
| `splus_y_offsetminus_d0.0010` | fail | fail | 6.86362e-05 | 0.0815284 | 0.257542 | 0.318785 | 0.00664688 | 3.7794e-12 |
| `splus_y_offsetminus_d0.0020` | fail | fail | 0.000137263 | 0.0815288 | 0.257539 | 0.318782 | 0.00664695 | 1.99739e-12 |
| `sminus_x_offsetplus_d0.0005` | fail | fail | 2.46038e-05 | 0.0843668 | 0.224281 | 0.287804 | 0.00711776 | 9.59552e-12 |
| `sminus_x_offsetplus_d0.0010` | fail | fail | 4.92069e-05 | 0.0843668 | 0.22428 | 0.287804 | 0.00711776 | 3.39876e-12 |
| `sminus_x_offsetplus_d0.0020` | fail | fail | 9.84106e-05 | 0.0843668 | 0.22428 | 0.287803 | 0.00711776 | 2.01872e-12 |
| `sminus_x_offsetminus_d0.0005` | fail | fail | 2.46046e-05 | 0.0843668 | 0.224281 | 0.287805 | 0.00711776 | 8.60217e-12 |
| `sminus_x_offsetminus_d0.0010` | fail | fail | 4.921e-05 | 0.0843668 | 0.224281 | 0.287805 | 0.00711776 | 4.01552e-12 |
| `sminus_x_offsetminus_d0.0020` | fail | fail | 9.84231e-05 | 0.0843668 | 0.224282 | 0.287805 | 0.00711776 | 2.27499e-12 |
| `sminus_y_offsetplus_d0.0005` | fail | fail | 3.43192e-05 | 0.0815281 | 0.257544 | 0.318786 | 0.00664684 | 8.88013e-12 |
| `sminus_y_offsetplus_d0.0010` | fail | fail | 6.86362e-05 | 0.0815284 | 0.257542 | 0.318785 | 0.00664688 | 3.7794e-12 |
| `sminus_y_offsetplus_d0.0020` | fail | fail | 0.000137263 | 0.0815288 | 0.257539 | 0.318782 | 0.00664695 | 1.99739e-12 |
| `sminus_y_offsetminus_d0.0005` | fail | fail | 3.43214e-05 | 0.0815277 | 0.257547 | 0.318789 | 0.00664677 | 7.3834e-12 |
| `sminus_y_offsetminus_d0.0010` | fail | fail | 6.86451e-05 | 0.0815275 | 0.257549 | 0.318791 | 0.00664673 | 3.94983e-12 |
| `sminus_y_offsetminus_d0.0020` | fail | fail | 0.000137299 | 0.081527 | 0.257553 | 0.318794 | 0.00664666 | 2.07822e-12 |

## Response and symmetry controls

- Response panel available: `True`.
- Maximum even/odd response ratio: `2.97315e-05`.
- Maximum normalized amplitude-collapse error: `1.48732e-05`.
- Maximum mirror center/actuator error fraction: `0`.

## Non-decisional rivals

- Ideal Cayley factor per update: `0.999001`; final separation ratio: `0.0183331`.
- Maximum raw-memory-center ledger residual / initial interaction energy: `14.9784`.
- Maximum age-truncated ledger residual / initial interaction energy: `19.99`.
- These comparisons are recorded but are not used by any gate.

## Interpretation boundary

an explicit first-order reciprocal source/write actuator, exact finite-H age ledger and weak nonlinear L3 orbit-center response for the registered panel.

Not established: material center of mass, unique microscopic ontology, conserved total momentum, physical mass, SI calibration, noise robustness, internal S1 or two-loop interaction.

## Provenance

- Freeze revision: `15ccd714ba595c92ae5d0aff936977f78977f632`.
- Execution revision: `d339ee1924ab2a931c74803ee5a58213b73afbcd`.
- Runtime: `3.12.13` / NumPy `2.4.6` / SciPy `1.18.0`.
- Machine-readable JSON SHA-256: `ea0651e206451e5f87ec08ab3f66ec68df2c04bee2d1b9d67219736058a275cc`.
