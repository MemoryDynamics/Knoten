# Dimension Reproduction Pilot

Datum: 2026-06-30

Quelle:

- Skript: `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- JSON: `data/processed/fractal_analysis/d_alpha_n_seed_scan_d3-8_alpha0102_n30k-300k_seed1-5.json`
- Git-Revision: `9142cfc`

## Ziel

Ressourcenschonender Seed-Pilot fuer den archivierten Dimensionsbefund aus
`experiments/fractal_analysis/Fraktale/resultsN.csv`. Der Lauf nutzt den
historischen Fraktal-Parametersatz und den historischen Box-Counting-Schaetzer.
Er ersetzt nicht den `N=60,000,000`-Befund, sondern prueft, ob bei kleineren
`N` bereits eine trennbare Signatur gegen einfache Negativkontrollen sichtbar
wird.

## Parameter

- embedding dimensions: `[3, 4, 5, 6, 7, 8]`
- alpha values: `[0.01, 0.02]`
- seeds: `[1, 2, 3, 4, 5]`
- steps ladder: `[30000, 100000, 300000]`
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
| 3 | 0.01 | baseline | 30000 | 5 | 0.896 | 0.881..0.912 | 2.891 | 1.856 | 300 | 0.951 |
| 3 | 0.02 | baseline | 30000 | 5 | 0.914 | 0.892..0.938 | 2.865 | 1.766 | 251 | 0.994 |
| 4 | 0.01 | baseline | 30000 | 5 | 0.587 | 0.537..0.641 | 3.682 | 1.890 | 300 | 0.951 |
| 4 | 0.02 | baseline | 30000 | 5 | 0.553 | 0.506..0.597 | 3.636 | 1.762 | 251 | 0.994 |
| 5 | 0.01 | baseline | 30000 | 5 | 0.341 | 0.314..0.372 | 4.440 | 1.776 | 300 | 0.951 |
| 5 | 0.02 | baseline | 30000 | 5 | 0.341 | 0.315..0.376 | 4.344 | 1.750 | 251 | 0.994 |
| 6 | 0.01 | baseline | 30000 | 5 | 0.214 | 0.193..0.237 | 4.834 | 1.861 | 300 | 0.951 |
| 6 | 0.02 | baseline | 30000 | 5 | 0.210 | 0.179..0.241 | 4.766 | 1.629 | 251 | 0.994 |
| 7 | 0.01 | baseline | 30000 | 5 | 0.129 | 0.111..0.147 | 5.131 | 1.828 | 300 | 0.951 |
| 7 | 0.02 | baseline | 30000 | 5 | 0.124 | 0.101..0.147 | 5.040 | 1.794 | 251 | 0.994 |
| 8 | 0.01 | baseline | 30000 | 5 | 0.609 | 0.342..0.755 | 2.617 | 1.469 | 300 | 0.951 |
| 8 | 0.02 | baseline | 30000 | 5 | 0.080 | 0.072..0.088 | 5.198 | 1.737 | 251 | 0.994 |
| 3 | 0.01 | baseline | 100000 | 5 | 1.300 | 1.264..1.327 | 2.402 | 1.586 | 300 | 0.951 |
| 3 | 0.02 | baseline | 100000 | 5 | 1.294 | 1.272..1.310 | 2.406 | 1.629 | 251 | 0.994 |
| 4 | 0.01 | baseline | 100000 | 5 | 0.978 | 0.917..1.045 | 2.625 | 1.514 | 300 | 0.951 |
| 4 | 0.02 | baseline | 100000 | 5 | 0.966 | 0.916..1.025 | 2.568 | 1.487 | 251 | 0.994 |
| 5 | 0.01 | baseline | 100000 | 5 | 0.642 | 0.618..0.663 | 2.994 | 1.599 | 300 | 0.951 |
| 5 | 0.02 | baseline | 100000 | 5 | 0.650 | 0.588..0.714 | 2.971 | 1.595 | 251 | 0.994 |
| 6 | 0.01 | baseline | 100000 | 5 | 0.470 | 0.399..0.551 | 3.948 | 1.668 | 300 | 0.951 |
| 6 | 0.02 | baseline | 100000 | 5 | 0.481 | 0.411..0.568 | 3.947 | 1.665 | 251 | 0.994 |
| 7 | 0.01 | baseline | 100000 | 5 | 0.506 | 0.331..0.790 | 2.875 | 1.558 | 300 | 0.951 |
| 7 | 0.02 | baseline | 100000 | 5 | 0.366 | 0.319..0.413 | 3.221 | 1.504 | 251 | 0.994 |
| 8 | 0.01 | baseline | 100000 | 5 | 1.022 | 0.955..1.076 | 1.842 | 2.057 | 300 | 0.951 |
| 8 | 0.02 | baseline | 100000 | 5 | 0.279 | 0.245..0.314 | 3.234 | 1.461 | 251 | 0.994 |
| 3 | 0.01 | baseline | 300000 | 5 | 1.699 | 1.658..1.742 | 2.020 | 1.452 | 300 | 0.951 |
| 3 | 0.02 | baseline | 300000 | 5 | 1.722 | 1.674..1.786 | 1.955 | 1.434 | 251 | 0.994 |
| 4 | 0.01 | baseline | 300000 | 5 | 1.378 | 1.316..1.465 | 2.078 | 1.433 | 300 | 0.951 |
| 4 | 0.02 | baseline | 300000 | 5 | 1.377 | 1.323..1.454 | 2.074 | 1.434 | 251 | 0.994 |
| 5 | 0.01 | baseline | 300000 | 5 | 1.022 | 0.939..1.149 | 2.687 | 1.493 | 300 | 0.951 |
| 5 | 0.02 | baseline | 300000 | 5 | 1.022 | 0.930..1.157 | 2.618 | 1.474 | 251 | 0.994 |
| 6 | 0.01 | baseline | 300000 | 5 | 0.800 | 0.758..0.853 | 2.793 | 1.443 | 300 | 0.951 |
| 6 | 0.02 | baseline | 300000 | 5 | 0.819 | 0.770..0.864 | 2.821 | 1.444 | 251 | 0.994 |
| 7 | 0.01 | baseline | 300000 | 5 | 0.967 | 0.586..1.442 | 2.361 | 1.445 | 300 | 0.951 |
| 7 | 0.02 | baseline | 300000 | 5 | 0.625 | 0.577..0.671 | 2.824 | 1.456 | 251 | 0.994 |
| 8 | 0.01 | baseline | 300000 | 5 | 1.202 | 1.152..1.235 | 2.104 | 1.329 | 300 | 0.951 |
| 8 | 0.02 | baseline | 300000 | 5 | 0.589 | 0.472..0.663 | 2.185 | 1.344 | 251 | 0.994 |

## Interpretation

Dieser Pilot ist ein Ressourcen-Test und ein Kontrollpfad. Ein belastbarer
Claim braucht weiterhin groessere `N`, mehr Seeds und stabilere Fitfenster.
Ein starkes Ergebnis waere hier nicht `D_occ` nahe 3 allein, sondern eine
konsistente Trennung des Baseline-Regimes von `eta_zero`, `single_scale` und
`shuffled_memory` ueber mehrere Diagnostiken.

## Seeded d-alpha-N-Lesart

Ergaenzende Heatmaps:

- `figures/draft/d_alpha_n_intensity_seedscan_d3-8_alpha0102_n30k-300k_D_cov.png`
- `figures/draft/d_alpha_n_intensity_seedscan_d3-8_alpha0102_n30k-300k_D_occ.png`
- `figures/draft/d_alpha_n_intensity_seedscan_d3-8_alpha0102_n30k-300k_D_spec.png`

Die Seedmittel stuetzen keinen stabilen `d=3`-Plateau-Claim in diesem
ressourcenschonenden N-Bereich:

- Bei `N=30,000` liegt `D_cov` fuer `d=3` nahe bei 3 (`2.891`, `2.865`).
- Bei `N=100,000` liegen die naechsten Werte bei `d=5` (`2.994`, `2.971`).
- Bei `N=300,000` liegen die naechsten Werte bei `d=6/7` (`2.821`, `2.824`).

Damit wandert die Naehe zu 3 mit der N-Leiter. Das ist eher ein Hinweis auf
endliche-N-, Fitfenster- oder Schaetzerabhaengigkeit als auf ein robustes
emergentes 3D-Plateau. Fuer Paper I sollte dieser Befund defensiv als offene
Dimensionsdiagnostik gefuehrt werden, nicht als Evidenz fuer eine Auswahl von
`d=3`.
