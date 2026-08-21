# Scalar-memory rotating-wave matched-refinement ladder

Generated: 2026-08-21T03:01:10.291533+00:00.

Decision: **certified-roots-nonconvergent**.

The ladder was evaluated from clean prospective revision
b03ff433776ced084f8bf3d56b54b8fe7b1e5ef2.

## Certified cells

| cell | alpha | H | eta | R | Omega | R error | Omega error | certified |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| L0 | 0.04 | 300 | 0.60 | 0.957217612 | 1.55003651 | 0.0142067828 | 0.0367801194 | True |
| L1 | 0.02 | 600 | 0.30 | 0.950000296 | 1.5682772 | 0.0069894665 | 0.018539426 | True |
| L2 | 0.01 | 1200 | 0.15 | 0.946517505 | 1.57703817 | 0.00350667553 | 0.00977845552 | True |
| L3 | 0.005 | 2400 | 0.075 | 0.944805812 | 1.58133229 | 0.00179498243 | 0.00548433475 | True |
| L4 | 0.0025 | 4800 | 0.0375 | 0.943957188 | 1.58345817 | 0.000946359084 | 0.0033584567 | True |

## Scaling diagnostics

- anchor enclosure overlap: True
- radius log-log slope: 0.962030243
- Omega log-log slope: 0.822846871
- radius finest/anchor error: 0.269873582
- Omega finest/anchor error: 0.343454719
- radius Richardson relative error: 0.103275534
- Omega Richardson relative error: 0.367007454

## Claim boundary

A pass establishes five locally unique exact finite-H roots and
numerical first-order approach to the pre-existing continuum guide.
It is not an all-alpha convergence theorem and does not establish
non-anchor stability, formation, noise robustness, internal phase,
physical work or mass.
