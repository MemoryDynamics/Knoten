# AR Mode Probe on Corrected Candidates

Date: 2026-07-09T19:13:11Z.

## Scope

This report fits linear autoregressive maps on PCA-reduced augmented-state
features for the corrected-sign compact candidates. It is a coarse-grained
mode diagnostic, not evidence that the selected variables are closed.

A complex conjugate pair would be an empirical reason to pursue a phase- or
wave-like effective model. Purely real modes support a relaxation-only
reading for the scalar memory model.

## Parameters

- `steps`: `50000`
- `burn_in`: `5000`
- `sample_every`: `100`
- `seeds`: `[1, 2, 3]`
- `amplitude_att`: `[0.35, 9.0, 35.0]`
- `alpha`: `0.01`
- `memory_mass`: `1.0`
- `sigma_rep`: `1.0`
- `sigma_att`: `3.0`
- `amplitude_rep`: `1.0`
- `lags`: `[1, 2, 5, 10]`
- `pca_components`: `6`
- `ridge`: `1e-06`
- `slow_abs_min`: `0.2`

## Mode Summary

| A_att | lag samples | lag updates | class | leading | |leading| | residual rms | n pairs | top eigenvalues |
| ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| `0.35` | `1` | `100` | `real` | `1.0000` | `1.0000` | `0.5260` | `1350` | `1.0000 ; 0.9999 ; 0.9932 ; 0.8594 ; 0.8485 ; 0.6026` |
| `0.35` | `2` | `200` | `real` | `1.0000` | `1.0000` | `0.6957` | `1347` | `1.0000 ; 0.9994 ; 0.9900 ; 0.6237 ; 0.5948 ; 0.2621` |
| `0.35` | `5` | `500` | `real` | `1.0000` | `1.0000` | `0.7935` | `1338` | `1.0000 ; 0.9983 ; 0.9812 ; 0.1895 ; 0.0293+0.0367i ; 0.0293-0.0367i` |
| `0.35` | `10` | `1000` | `real` | `1.0000` | `1.0000` | `0.8067` | `1323` | `1.0000 ; 0.9983 ; 0.9699 ; -0.0897 ; -0.0361 ; 0.0229` |
| `9` | `1` | `100` | `real` | `1.0000` | `1.0000` | `0.7725` | `1350` | `1.0000 ; 0.9982 ; 0.9882 ; 0.2602 ; 0.1537 ; -0.0007` |
| `9` | `2` | `200` | `real` | `1.0000` | `1.0000` | `0.7881` | `1347` | `1.0000 ; 0.9974 ; 0.9824 ; 0.0909 ; 0.0790 ; -0.0417` |
| `9` | `5` | `500` | `real` | `1.0000` | `1.0000` | `0.7997` | `1338` | `1.0000 ; 0.9951 ; 0.9635 ; 0.0645 ; 0.0151+0.0262i ; 0.0151-0.0262i` |
| `9` | `10` | `1000` | `real` | `1.0000` | `1.0000` | `0.8175` | `1323` | `1.0000 ; 0.9913 ; 0.9321 ; 0.0389 ; -0.0289 ; -0.0241` |
| `35` | `1` | `100` | `real` | `1.0000` | `1.0000` | `0.7973` | `1350` | `1.0000 ; 0.9980 ; 0.9229 ; 0.2288 ; -0.0389 ; -0.0065` |
| `35` | `2` | `200` | `real` | `1.0000` | `1.0000` | `0.8055` | `1347` | `1.0000 ; 0.9964 ; 0.9191 ; 0.0648+0.0153i ; 0.0648-0.0153i ; -0.0515` |
| `35` | `5` | `500` | `real` | `1.0000` | `1.0000` | `0.8106` | `1338` | `1.0000 ; 0.9911 ; 0.9154 ; 0.1031 ; 0.0125+0.0320i ; 0.0125-0.0320i` |
| `35` | `10` | `1000` | `real` | `1.0000` | `1.0000` | `0.8198` | `1323` | `1.0000 ; 0.9827 ; 0.9069 ; -0.0329 ; -0.0299 ; 0.0144` |

## PCA Coverage

| A_att | raw dim | projected dim | explained ratio first components |
| ---: | ---: | ---: | --- |
| `0.35` | `12` | `6` | `0.287, 0.195, 0.142, 0.088, 0.083, 0.083` |
| `9` | `12` | `6` | `0.253, 0.191, 0.131, 0.086, 0.085, 0.083` |
| `35` | `12` | `6` | `0.284, 0.181, 0.106, 0.094, 0.089, 0.083` |

## Reading

- Treat classifications as lag- and feature-dependent diagnostics.
- A classification is meaningful only if it is stable across several lags.
- Fast complex residues below `slow_abs_min` are reported in the eigenvalue
  list but do not make the slow-mode classification complex.
- If the corrected scalar candidates show only real modes, the current
  scalar memory model supports relaxation/confinement more directly than
  oscillator or photon analogies.

## Result

All tested slow-mode classifications are real for `A_att=0.35`, `9`, and `35`
across lags `1,2,5,10`. Small complex conjugate pairs appear only as fast
residual modes with `|mu| < 0.2`, and are not stable slow oscillatory modes.

This supports the current interpretation: the corrected scalar-memory model can
produce relaxation and compact memory clouds, but this pilot does not provide an
oscillatory or photon-like effective mode. A vector-, phase-, velocity-, or
otherwise oriented memory channel remains the plausible next extension if the
project needs persistent internal phase dynamics.