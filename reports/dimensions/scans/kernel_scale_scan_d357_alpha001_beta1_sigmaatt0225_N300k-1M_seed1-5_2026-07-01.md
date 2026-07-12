# Dimension Reproduction Pilot

Datum: 2026-07-01

Quelle:

- Skript: `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- JSON: `data/processed/fractal_analysis/kernel_scale_scan_d357_alpha001_beta1_sigmaatt0225_N300k-1M_seed1-5.json`
- Git-Revision: `d4cfa09`

## Ziel

Ressourcenschonender Seed-Pilot fuer den archivierten Dimensionsbefund aus
`experiments/fractal_analysis/archive_source/data/n_scaling/resultsN.csv`. Der Lauf nutzt den
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
| 3 | 0.01 | 1 | 0.225 | baseline | 300000 | 5 | 1.072 | 0.999..1.159 | 1.970 | 1.00 | 1.808 | 1.381 | 300 | 0.951 |
| 5 | 0.01 | 1 | 0.225 | baseline | 300000 | 5 | 0.543 | 0.468..0.665 | 2.097 | 0.40 | 2.390 | 1.417 | 300 | 0.951 |
| 7 | 0.01 | 1 | 0.225 | baseline | 300000 | 5 | 0.287 | 0.262..0.310 | nan | 0.00 | 2.569 | 1.407 | 300 | 0.951 |
| 3 | 0.01 | 1 | 0.225 | baseline | 1000000 | 5 | 1.434 | 1.384..1.484 | 2.088 | 1.00 | 1.960 | 1.361 | 300 | 0.951 |
| 5 | 0.01 | 1 | 0.225 | baseline | 1000000 | 5 | 0.865 | 0.796..0.920 | 2.382 | 1.00 | 2.246 | 1.367 | 300 | 0.951 |
| 7 | 0.01 | 1 | 0.225 | baseline | 1000000 | 5 | 0.647 | 0.529..0.809 | 2.311 | 0.60 | 2.211 | 1.316 | 300 | 0.951 |

## Interpretation

Dieser Pilot ist ein Ressourcen-Test und ein Kontrollpfad. Ein belastbarer
Claim braucht weiterhin groessere `N`, mehr Seeds und stabilere Fitfenster.
Ein starkes Ergebnis waere hier nicht `D_occ` nahe 3 allein, sondern eine
konsistente Trennung des Baseline-Regimes von `eta_zero`, `single_scale` und
`shuffled_memory` ueber mehrere Diagnostiken.
