# Dimension Reproduction Pilot

Datum: 2026-07-01

Quelle:

- Skript: `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- JSON: `data/processed/fractal_analysis/memory_time_scan_d357_alpha005-02_beta1_N300k-1M_seed1-5.json`
- Git-Revision: `e824f80`

## Ziel

Ressourcenschonender Seed-Pilot fuer den archivierten Dimensionsbefund aus
`experiments/fractal_analysis/Fraktale/resultsN.csv`. Der Lauf nutzt den
historischen Fraktal-Parametersatz und den historischen Box-Counting-Schaetzer.
Er ersetzt nicht den `N=60,000,000`-Befund, sondern prueft, ob bei kleineren
`N` bereits eine trennbare Signatur gegen einfache Negativkontrollen sichtbar
wird.

## Parameter

- embedding dimensions: `[3, 5, 7]`
- alpha/lambda_m values: `[0.005, 0.01, 0.02]`
- beta values: `[0.005, 0.01, 0.02]`
- beta/alpha values: `[1.0]`
- seeds: `[1, 2, 3, 4, 5]`
- steps ladder: `[300000, 1000000]`
- conditions: `['baseline']`
- engine request: `auto`
- coupling mode: `fixed-eta-alpha`
- eta-alpha target: `0.02`
- memory mode: `capped`
- memory tail mass: `0.95`
- sample_every: `100`
- configured max_memory: `300`
- burn-in fraction: `0.2`
- estimator: `archive_fraktale_box_counting`

## Ergebnis

| dim | alpha | beta/alpha | sigma_att | condition | steps | runs | D_occ mean | D_occ 95% CI | D_win mean | valid win | D_cov mean | D_spec mean | horizon | mass |
| ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 0.005 | 1 | 0.15 | baseline | 300000 | 5 | 0.974 | 0.917..1.029 | 1.945 | 1.00 | 2.089 | 1.498 | 300 | 0.778 |
| 3 | 0.01 | 1 | 0.15 | baseline | 300000 | 5 | 0.981 | 0.909..1.044 | 1.953 | 1.00 | 2.015 | 1.468 | 300 | 0.951 |
| 3 | 0.02 | 1 | 0.15 | baseline | 300000 | 5 | 1.059 | 0.988..1.139 | 2.003 | 1.00 | 1.777 | 1.364 | 251 | 0.994 |
| 5 | 0.005 | 1 | 0.15 | baseline | 300000 | 5 | 0.444 | 0.392..0.528 | 2.267 | 0.20 | 2.800 | 1.518 | 300 | 0.778 |
| 5 | 0.01 | 1 | 0.15 | baseline | 300000 | 5 | 0.463 | 0.405..0.558 | 2.136 | 0.20 | 2.673 | 1.490 | 300 | 0.951 |
| 5 | 0.02 | 1 | 0.15 | baseline | 300000 | 5 | 0.562 | 0.475..0.689 | 2.107 | 0.40 | 2.321 | 1.402 | 251 | 0.994 |
| 7 | 0.005 | 1 | 0.15 | baseline | 300000 | 5 | 0.645 | 0.566..0.725 | 1.353 | 1.00 | 2.505 | 1.407 | 300 | 0.778 |
| 7 | 0.01 | 1 | 0.15 | baseline | 300000 | 5 | 0.517 | 0.201..0.928 | 2.298 | 0.40 | 2.356 | 1.470 | 300 | 0.951 |
| 7 | 0.02 | 1 | 0.15 | baseline | 300000 | 5 | 0.331 | 0.296..0.366 | nan | 0.00 | 2.473 | 1.393 | 251 | 0.994 |
| 3 | 0.005 | 1 | 0.15 | baseline | 1000000 | 5 | 1.352 | 1.299..1.396 | 2.104 | 1.00 | 2.113 | 1.415 | 300 | 0.778 |
| 3 | 0.01 | 1 | 0.15 | baseline | 1000000 | 5 | 1.373 | 1.313..1.426 | 2.125 | 1.00 | 2.078 | 1.408 | 300 | 0.951 |
| 3 | 0.02 | 1 | 0.15 | baseline | 1000000 | 5 | 1.433 | 1.363..1.487 | 2.078 | 1.00 | 1.963 | 1.376 | 251 | 0.994 |
| 5 | 0.005 | 1 | 0.15 | baseline | 1000000 | 5 | 0.863 | 0.695..1.125 | 2.531 | 0.80 | 2.181 | 1.453 | 300 | 0.778 |
| 5 | 0.01 | 1 | 0.15 | baseline | 1000000 | 5 | 0.779 | 0.718..0.828 | 2.508 | 1.00 | 2.365 | 1.394 | 300 | 0.951 |
| 5 | 0.02 | 1 | 0.15 | baseline | 1000000 | 5 | 0.905 | 0.828..0.958 | 2.377 | 1.00 | 2.200 | 1.356 | 251 | 0.994 |
| 7 | 0.005 | 1 | 0.15 | baseline | 1000000 | 5 | 1.060 | 0.962..1.185 | 1.481 | 1.00 | 2.099 | 1.318 | 300 | 0.778 |
| 7 | 0.01 | 1 | 0.15 | baseline | 1000000 | 5 | 1.229 | 1.058..1.401 | 2.326 | 1.00 | 1.947 | 1.319 | 300 | 0.951 |
| 7 | 0.02 | 1 | 0.15 | baseline | 1000000 | 5 | 0.863 | 0.706..1.020 | 2.273 | 0.60 | 2.015 | 1.291 | 251 | 0.994 |

## Interpretation

Dieser Pilot ist ein Ressourcen-Test und ein Kontrollpfad. Ein belastbarer
Claim braucht weiterhin groessere `N`, mehr Seeds und stabilere Fitfenster.
Ein starkes Ergebnis waere hier nicht `D_occ` nahe 3 allein, sondern eine
konsistente Trennung des Baseline-Regimes von `eta_zero`, `single_scale` und
`shuffled_memory` ueber mehrere Diagnostiken.
