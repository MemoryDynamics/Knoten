# Corrected-Sign Transition Boundary near A_att < 9

Date: 2026-07-09.

## Scope

This pilot refines the corrected-sign amplitude transition below `A_att=9` with
more seeds. It is a boundary-finding scan, not a long-run knot claim.

Fixed parameters: `N=50,000`, seeds `1..10`, `d=3`, `alpha=0.01`, `M0=1`,
`sigma_rep=1`, `sigma_att=3`, `A_rep=1`, `epsilon=0.03`, `eta=0.15`,
`sample_every=100`, `burn_in=5,000`, `max_memory=600`, delta deposition, and
force-component diagnostics.

The dimensionless local force-balance coordinate is

```text
chi = (A_att/sigma_att^2) / (A_rep/sigma_rep^2).
```

For this scan, `chi=A_att/9`.

## Median Summary

| A_att | chi | score med | candidate seeds | best residence med | sample radius med | memory radius med | memory roundness med | rep/att med | net cos med | net cos IQR |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `3.5` | `0.389` | `0.286` | `0/10` | `2.5` | `3.605` | `1.058` | `0.234` | `1.210` | `-0.530` | `-0.542..-0.522` |
| `4.5` | `0.500` | `0.286` | `0/10` | `3` | `3.263` | `0.882` | `0.268` | `1.143` | `-0.557` | `-0.570..-0.547` |
| `5.5` | `0.611` | `0.286` | `0/10` | `4` | `3.511` | `0.758` | `0.342` | `1.095` | `-0.579` | `-0.584..-0.564` |
| `6.5` | `0.722` | `0.286` | `1/10` | `5.85` | `2.578` | `0.630` | `0.422` | `1.061` | `-0.595` | `-0.599..-0.593` |
| `7.5` | `0.833` | `0.286` | `3/10` | `8.667` | `2.012` | `0.434` | `0.387` | `1.026` | `-0.400` | `-0.437..-0.369` |
| `7.75` | `0.861` | `0.286` | `4/10` | `7.9` | `1.910` | `0.408` | `0.399` | `1.012` | `-0.177` | `-0.198..-0.139` |
| `8.0` | `0.889` | `0.286` | `5/10` | `9.444` | `1.788` | `0.380` | `0.410` | `0.996` | `0.249` | `0.204..0.313` |
| `8.25` | `0.917` | `0.286` | `3/10` | `8.104` | `1.678` | `0.353` | `0.422` | `0.982` | `0.693` | `0.670..0.704` |
| `8.5` | `0.944` | `0.286` | `3/10` | `8.212` | `1.577` | `0.320` | `0.435` | `0.964` | `0.889` | `0.884..0.897` |
| `9.0` | `1.000` | `0.321` | `3/10` | `8.304` | `1.359` | `0.267` | `0.424` | `0.933` | `0.975` | `0.973..0.977` |

`net cos` is measured relative to the direction from the current point toward
the weighted memory center. Positive values mean inward drift; negative values
mean outward drift.

## Boundary Estimate

Linear interpolation gives two close boundary estimates:

```text
rep/att = 1   at A_att ~= 7.93, chi ~= 0.881
net cos = 0   at A_att ~= 7.85, chi ~= 0.873
```

The empirical transition is therefore around

```text
A_att ~= 7.9, chi ~= 0.88.
```

## Reading

- The transition begins below the naive local-curvature balance `chi=1`.
- Candidate residence appears weakly already around `A_att=6.5..7.5`, but the
  force direction remains outward there.
- The sign of the net drift flips between `A_att=7.75` and `8.0`.
- The score median remains low in this short scan; this identifies a boundary,
  not a robust metastable knot.
- The refined scalar boundary is useful for Paper I hardening, but it still
  does not produce slow complex modes by itself.

## Consequence

The next scalar-memory long-run candidate should not be the old `A_att=0.35` or
a broad blind sweep. If scalar hardening is needed, use the narrow corrected
window `A_att in [7.75, 9.0]` for transition physics and `A_att in [9, 35]` for
compactness. For oscillator, photon, or bosonic interpretations, move to a
vector or phase memory channel instead of further overfitting the scalar kernel.
