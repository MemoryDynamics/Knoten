# Dimension Reproduction Pilot

Datum: 2026-06-13

Quelle:

- Skript: `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- JSON: `data/processed/fractal_analysis/fractal_alpha_sweep_pilot_historical_30k.json`
- Git-Revision: Arbeitsbaum, der mit diesem Report committed wird

## Ziel

Ressourcenschonender Seed-Pilot fuer den archivierten Dimensionsbefund aus
`experiments/fractal_analysis/archive_source/data/n_scaling/resultsN.csv`. Der Lauf nutzt den
historischen Fraktal-Parametersatz und den historischen Box-Counting-Schaetzer.
Er ersetzt nicht den `N=60,000,000`-Befund, sondern prueft, ob bei kleineren
`N` bereits eine trennbare Signatur gegen einfache Negativkontrollen sichtbar
wird.

## Parameter

- embedding dimensions: `[3, 4, 5, 6]`
- alpha values: `[0.005, 0.01, 0.02]`
- seeds: `[1, 2, 3]`
- steps ladder: `[30000]`
- conditions: `['baseline']`
- engine request: `auto`
- coupling mode: `historical`
- eta-alpha target: `None`
- memory mode: `capped`
- memory tail mass: `0.95`
- sample_every: `10`
- configured max_memory: `300`
- burn-in fraction: `0.2`
- estimator: `archive_fraktale_box_counting`

## Ergebnis

| dim | alpha | condition | steps | runs | D_occ mean | D_occ 95% CI | D_cov mean | D_spec mean | horizon | mass |
| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 0.005 | baseline | 30000 | 3 | 1.023 | 0.897..1.216 | 2.649 | 1.786 | 300 | 0.778 |
| 3 | 0.01 | baseline | 30000 | 3 | 0.910 | 0.892..0.933 | 2.886 | 1.873 | 300 | 0.951 |
| 3 | 0.02 | baseline | 30000 | 3 | 0.904 | 0.842..0.961 | 2.880 | 1.633 | 251 | 0.994 |
| 4 | 0.005 | baseline | 30000 | 3 | 1.081 | 0.968..1.220 | 1.801 | 1.692 | 300 | 0.778 |
| 4 | 0.01 | baseline | 30000 | 3 | 0.548 | 0.510..0.594 | 3.901 | 1.951 | 300 | 0.951 |
| 4 | 0.02 | baseline | 30000 | 3 | 0.527 | 0.470..0.578 | 3.883 | 1.763 | 251 | 0.994 |
| 5 | 0.005 | baseline | 30000 | 3 | 0.953 | 0.812..1.053 | 2.309 | 1.305 | 300 | 0.778 |
| 5 | 0.01 | baseline | 30000 | 3 | 0.325 | 0.296..0.366 | 4.496 | 1.934 | 300 | 0.951 |
| 5 | 0.02 | baseline | 30000 | 3 | 0.303 | 0.276..0.322 | 4.479 | 1.887 | 251 | 0.994 |
| 6 | 0.005 | baseline | 30000 | 3 | 0.777 | 0.667..0.976 | 2.778 | 1.428 | 300 | 0.778 |
| 6 | 0.01 | baseline | 30000 | 3 | 0.253 | 0.188..0.300 | 5.207 | 1.966 | 300 | 0.951 |
| 6 | 0.02 | baseline | 30000 | 3 | 0.189 | 0.159..0.226 | 5.220 | 1.967 | 251 | 0.994 |

## Interpretation

Dieser Pilot ist ein Ressourcen-Test und ein Kontrollpfad. Ein belastbarer
Claim braucht weiterhin groessere `N`, mehr Seeds und stabilere Fitfenster.
Ein starkes Ergebnis waere hier nicht `D_occ` nahe 3 allein, sondern eine
konsistente Trennung des Baseline-Regimes von `eta_zero`, `single_scale` und
`shuffled_memory` ueber mehrere Diagnostiken.

## Spezifische Lesart dieses Laufs

Bei `N = 30,000` gewinnt in jeder getesteten Einbettungsdimension
`alpha = 0.005`.

| dim | best alpha | mean D_occ | 95% CI | stored mass |
| ---: | ---: | ---: | ---: | ---: |
| 3 | 0.005 | 1.022946 | 0.897275..1.216352 | 0.777708 |
| 4 | 0.005 | 1.081128 | 0.968371..1.219960 | 0.777708 |
| 5 | 0.005 | 0.952796 | 0.811642..1.053123 | 0.777708 |
| 6 | 0.005 | 0.777262 | 0.666965..0.976093 | 0.777708 |

Das ist kein Near-3-Befund. Es ist aber ein klarer Hinweis, dass `alpha` im
historisch gekappten Regime schon bei kleinem `N` die fraktale Occupancy
sichtbar verschiebt.

Vorsicht: Bei `alpha=0.005` ist wegen `max_memory=300` nur etwa `77.8%` der
exponentiellen Gewichtsmasse enthalten. Bei `alpha=0.01` sind es etwa `95.1%`,
bei `alpha=0.02` etwa `99.4%`. Der beobachtete Alpha-Trend ist deshalb noch
eine Mischung aus Zerfallsrate, Speicher-Cap und effektiver Kopplung
`eta*alpha`.
