# Dimension Reproduction Pilot

Datum: 2026-07-01

Quelle:

- Skript: `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- JSON: `data/processed/fractal_analysis/kernel_scale_scan_d357_alpha001_beta1_sigmaatt010_N300k-1M_seed1-5.json`
- Git-Revision: `d4cfa09`

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
- beta values: `[0.01]`
- beta/alpha values: `[1.0]`
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

| dim | alpha | beta/alpha | sigma_att | condition | steps | runs | D_occ mean | D_occ 95% CI | D_win mean | valid win | D_cov mean | D_spec mean | horizon | mass |
| ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 0.01 | 1 | 0.1 | baseline | 300000 | 5 | 1.283 | 1.216..1.356 | 1.655 | 1.00 | 1.571 | 1.344 | 300 | 0.951 |
| 5 | 0.01 | 1 | 0.1 | baseline | 300000 | 5 | 0.813 | 0.793..0.834 | 0.674 | 1.00 | 1.975 | 1.323 | 300 | 0.951 |
| 7 | 0.01 | 1 | 0.1 | baseline | 300000 | 5 | 0.738 | 0.687..0.787 | 1.361 | 1.00 | 2.209 | 1.328 | 300 | 0.951 |
| 3 | 0.01 | 1 | 0.1 | baseline | 1000000 | 5 | 1.589 | 1.558..1.620 | 1.744 | 1.00 | 1.641 | 1.305 | 300 | 0.951 |
| 5 | 0.01 | 1 | 0.1 | baseline | 1000000 | 5 | 0.997 | 0.929..1.073 | 0.938 | 1.00 | 2.105 | 1.302 | 300 | 0.951 |
| 7 | 0.01 | 1 | 0.1 | baseline | 1000000 | 5 | 1.076 | 0.989..1.200 | 1.492 | 1.00 | 2.038 | 1.296 | 300 | 0.951 |

## Interpretation

Dieser Pilot ist ein Ressourcen-Test und ein Kontrollpfad. Ein belastbarer
Claim braucht weiterhin groessere `N`, mehr Seeds und stabilere Fitfenster.
Ein starkes Ergebnis waere hier nicht `D_occ` nahe 3 allein, sondern eine
konsistente Trennung des Baseline-Regimes von `eta_zero`, `single_scale` und
`shuffled_memory` ueber mehrere Diagnostiken.
