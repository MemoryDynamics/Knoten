# Dimension Reproduction Pilot

Datum: 2026-06-30

Quelle:

- Skript: `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- JSON: `data/processed/fractal_analysis/d_alpha_n_pilot_seed1_30k_100k.json`
- Git-Revision: `9bf671f`

## Ziel

Ressourcenschonender Seed-Pilot fuer den archivierten Dimensionsbefund aus
`experiments/fractal_analysis/archive_source/data/n_scaling/resultsN.csv`. Der Lauf nutzt den
historischen Fraktal-Parametersatz und den historischen Box-Counting-Schaetzer.
Er ersetzt nicht den `N=60,000,000`-Befund, sondern prueft, ob bei kleineren
`N` bereits eine trennbare Signatur gegen einfache Negativkontrollen sichtbar
wird.

## Parameter

- embedding dimensions: `[2, 3, 4, 5, 6]`
- alpha values: `[0.005, 0.01, 0.02]`
- seeds: `[1]`
- steps ladder: `[30000, 100000]`
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
| 2 | 0.005 | baseline | 30000 | 1 | 1.299 | 1.299..1.299 | 1.840 | 1.602 | 300 | 0.778 |
| 2 | 0.01 | baseline | 30000 | 1 | 1.271 | 1.271..1.271 | 1.980 | 1.719 | 300 | 0.951 |
| 2 | 0.02 | baseline | 30000 | 1 | 1.301 | 1.301..1.301 | 1.952 | 1.626 | 251 | 0.994 |
| 3 | 0.005 | baseline | 30000 | 1 | 1.216 | 1.216..1.216 | 2.900 | 1.895 | 300 | 0.778 |
| 3 | 0.01 | baseline | 30000 | 1 | 0.907 | 0.907..0.907 | 2.988 | 1.977 | 300 | 0.951 |
| 3 | 0.02 | baseline | 30000 | 1 | 0.842 | 0.842..0.842 | 2.988 | 1.840 | 251 | 0.994 |
| 4 | 0.005 | baseline | 30000 | 1 | 1.220 | 1.220..1.220 | 1.641 | 4.311 | 300 | 0.778 |
| 4 | 0.01 | baseline | 30000 | 1 | 0.510 | 0.510..0.510 | 3.935 | 1.981 | 300 | 0.951 |
| 4 | 0.02 | baseline | 30000 | 1 | 0.470 | 0.470..0.470 | 3.921 | 1.974 | 251 | 0.994 |
| 5 | 0.005 | baseline | 30000 | 1 | 0.812 | 0.812..0.812 | 2.731 | 1.321 | 300 | 0.778 |
| 5 | 0.01 | baseline | 30000 | 1 | 0.314 | 0.314..0.314 | 4.795 | 2.072 | 300 | 0.951 |
| 5 | 0.02 | baseline | 30000 | 1 | 0.322 | 0.322..0.322 | 4.757 | 2.082 | 251 | 0.994 |
| 6 | 0.005 | baseline | 30000 | 1 | 0.667 | 0.667..0.667 | 3.699 | 1.552 | 300 | 0.778 |
| 6 | 0.01 | baseline | 30000 | 1 | 0.188 | 0.188..0.188 | 5.854 | 2.280 | 300 | 0.951 |
| 6 | 0.02 | baseline | 30000 | 1 | 0.159 | 0.159..0.159 | 5.808 | 2.205 | 251 | 0.994 |
| 2 | 0.005 | baseline | 100000 | 1 | 1.547 | 1.547..1.547 | 1.572 | 1.511 | 300 | 0.778 |
| 2 | 0.01 | baseline | 100000 | 1 | 1.516 | 1.516..1.516 | 1.840 | 1.579 | 300 | 0.951 |
| 2 | 0.02 | baseline | 100000 | 1 | 1.552 | 1.552..1.552 | 1.818 | 1.527 | 251 | 0.994 |
| 3 | 0.005 | baseline | 100000 | 1 | 1.623 | 1.623..1.623 | 1.061 | 1.038 | 300 | 0.778 |
| 3 | 0.01 | baseline | 100000 | 1 | 1.283 | 1.283..1.283 | 2.914 | 1.872 | 300 | 0.951 |
| 3 | 0.02 | baseline | 100000 | 1 | 1.239 | 1.239..1.239 | 2.937 | 1.819 | 251 | 0.994 |
| 4 | 0.005 | baseline | 100000 | 1 | 1.113 | 1.113..1.113 | 2.980 | 1.356 | 300 | 0.778 |
| 4 | 0.01 | baseline | 100000 | 1 | 0.952 | 0.952..0.952 | 2.958 | 1.616 | 300 | 0.951 |
| 4 | 0.02 | baseline | 100000 | 1 | 0.876 | 0.876..0.876 | 3.088 | 1.657 | 251 | 0.994 |
| 5 | 0.005 | baseline | 100000 | 1 | 1.356 | 1.356..1.356 | 2.102 | 1.307 | 300 | 0.778 |
| 5 | 0.01 | baseline | 100000 | 1 | 0.775 | 0.775..0.775 | 3.794 | 1.671 | 300 | 0.951 |
| 5 | 0.02 | baseline | 100000 | 1 | 0.745 | 0.745..0.745 | 3.717 | 1.679 | 251 | 0.994 |
| 6 | 0.005 | baseline | 100000 | 1 | 1.251 | 1.251..1.251 | 1.984 | 1.316 | 300 | 0.778 |
| 6 | 0.01 | baseline | 100000 | 1 | 0.479 | 0.479..0.479 | 3.338 | 1.610 | 300 | 0.951 |
| 6 | 0.02 | baseline | 100000 | 1 | 0.467 | 0.467..0.467 | 3.237 | 1.565 | 251 | 0.994 |

## Interpretation

Dieser Pilot ist ein Ressourcen-Test und ein Kontrollpfad. Ein belastbarer
Claim braucht weiterhin groessere `N`, mehr Seeds und stabilere Fitfenster.
Ein starkes Ergebnis waere hier nicht `D_occ` nahe 3 allein, sondern eine
konsistente Trennung des Baseline-Regimes von `eta_zero`, `single_scale` und
`shuffled_memory` ueber mehrere Diagnostiken.

## d-alpha-N-Lesart

Ergaenzende Heatmaps:

- `figures/draft/dimensions/d_alpha_n/seed1/d_alpha_n_intensity_seed1_30k_100k_D_occ.png`
- `figures/draft/dimensions/d_alpha_n/seed1/d_alpha_n_intensity_seed1_30k_100k_D_cov.png`
- `figures/draft/dimensions/d_alpha_n/seed1/d_alpha_n_intensity_seed1_30k_100k_D_spec.png`

Der staerkste vorlaeufige Hinweis liegt in `D_cov`: Bei `d=3` und
`alpha=0.01/0.02` bleibt der Wert von `N=30,000` zu `N=100,000` nahe bei 3
(`2.988 -> 2.914` beziehungsweise `2.988 -> 2.937`). Das ist ein plausibler
Kandidatenbereich fuer laengere Laeufe.

Der Befund ist aber nicht exklusiv: Bei `N=100,000` liegen auch mehrere
`d=4`-Zellen nahe 3 (`2.980`, `2.958`, `3.088`). Damit traegt der Pilot noch
keinen `d=3`-Claim. Er priorisiert den naechsten Sweep: mindestens fuenf Seeds
und eine laengere N-Leiter fuer `d=3` und `d=4`, insbesondere bei
`alpha=0.01/0.02`, plus die bereits geplanten Negativkontrollen.
