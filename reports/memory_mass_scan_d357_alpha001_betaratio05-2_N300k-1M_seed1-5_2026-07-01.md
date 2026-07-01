# Dimension Reproduction Pilot

Datum: 2026-07-01

Quelle:

- Skript: `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- JSON: `data/processed/fractal_analysis/memory_mass_scan_d357_alpha001_betaratio05-2_N300k-1M_seed1-5.json`
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
- alpha/lambda_m values: `[0.01]`
- beta values: `[0.005, 0.01, 0.02]`
- beta/alpha values: `[0.5, 1.0, 2.0]`
- seeds: `[1, 2, 3, 4, 5]`
- steps ladder: `[300000, 1000000]`
- conditions: `['baseline']`
- engine request: `auto`
- coupling mode: `historical`
- eta-alpha target: `None`
- memory mode: `capped`
- memory tail mass: `0.95`
- sample_every: `100`
- configured max_memory: `300`
- burn-in fraction: `0.2`
- estimator: `archive_fraktale_box_counting`

## Ergebnis

| dim | alpha | beta/alpha | sigma_att | condition | steps | runs | D_occ mean | D_occ 95% CI | D_cov mean | D_spec mean | horizon | mass |
| ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 0.01 | 0.5 | 0.15 | baseline | 300000 | 5 | 1.100 | 1.023..1.191 | 1.766 | 1.365 | 300 | 0.475 |
| 3 | 0.01 | 1 | 0.15 | baseline | 300000 | 5 | 0.981 | 0.909..1.044 | 2.015 | 1.468 | 300 | 0.951 |
| 3 | 0.01 | 2 | 0.15 | baseline | 300000 | 5 | 0.932 | 0.875..0.988 | 2.318 | 1.576 | 300 | 1.902 |
| 5 | 0.01 | 0.5 | 0.15 | baseline | 300000 | 5 | 0.815 | 0.769..0.857 | 1.959 | 1.280 | 300 | 0.475 |
| 5 | 0.01 | 1 | 0.15 | baseline | 300000 | 5 | 0.463 | 0.405..0.558 | 2.673 | 1.490 | 300 | 0.951 |
| 5 | 0.01 | 2 | 0.15 | baseline | 300000 | 5 | 0.362 | 0.315..0.432 | 3.316 | 1.628 | 300 | 1.902 |
| 7 | 0.01 | 0.5 | 0.15 | baseline | 300000 | 5 | 0.729 | 0.679..0.778 | 2.249 | 1.337 | 300 | 0.475 |
| 7 | 0.01 | 1 | 0.15 | baseline | 300000 | 5 | 0.517 | 0.201..0.928 | 2.356 | 1.470 | 300 | 0.951 |
| 7 | 0.01 | 2 | 0.15 | baseline | 300000 | 5 | 0.307 | 0.141..0.601 | 3.021 | 1.588 | 300 | 1.902 |
| 3 | 0.01 | 0.5 | 0.15 | baseline | 1000000 | 5 | 1.535 | 1.470..1.603 | 1.567 | 1.352 | 300 | 0.475 |
| 3 | 0.01 | 1 | 0.15 | baseline | 1000000 | 5 | 1.373 | 1.313..1.426 | 2.078 | 1.408 | 300 | 0.951 |
| 3 | 0.01 | 2 | 0.15 | baseline | 1000000 | 5 | 1.325 | 1.282..1.358 | 2.330 | 1.460 | 300 | 1.902 |
| 5 | 0.01 | 0.5 | 0.15 | baseline | 1000000 | 5 | 1.026 | 0.957..1.107 | 1.870 | 1.306 | 300 | 0.475 |
| 5 | 0.01 | 1 | 0.15 | baseline | 1000000 | 5 | 0.779 | 0.718..0.828 | 2.365 | 1.394 | 300 | 0.951 |
| 5 | 0.01 | 2 | 0.15 | baseline | 1000000 | 5 | 0.776 | 0.679..0.939 | 2.325 | 1.438 | 300 | 1.902 |
| 7 | 0.01 | 0.5 | 0.15 | baseline | 1000000 | 5 | 1.072 | 0.970..1.212 | 2.063 | 1.297 | 300 | 0.475 |
| 7 | 0.01 | 1 | 0.15 | baseline | 1000000 | 5 | 1.229 | 1.058..1.401 | 1.947 | 1.319 | 300 | 0.951 |
| 7 | 0.01 | 2 | 0.15 | baseline | 1000000 | 5 | 0.616 | 0.426..0.806 | 2.135 | 1.357 | 300 | 1.902 |

## Interpretation

Dieser Pilot ist ein Ressourcen-Test und ein Kontrollpfad. Ein belastbarer
Claim braucht weiterhin groessere `N`, mehr Seeds und stabilere Fitfenster.
Ein starkes Ergebnis waere hier nicht `D_occ` nahe 3 allein, sondern eine
konsistente Trennung des Baseline-Regimes von `eta_zero`, `single_scale` und
`shuffled_memory` ueber mehrere Diagnostiken.
