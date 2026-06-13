# Dimension Reproduction Pilot

Datum: 2026-06-13

Quelle:

- Skript: `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- JSON: `data/processed/fractal_analysis/dimension_reproduction_pilot.json`
- Git-Revision: `9e498f9`

## Ziel

Ressourcenschonender Seed-Pilot fuer den archivierten Dimensionsbefund aus
`experiments/fractal_analysis/Fraktale/resultsN.csv`. Der Lauf nutzt den
historischen Fraktal-Parametersatz und den historischen Box-Counting-Schaetzer.
Er ersetzt nicht den `N=60,000,000`-Befund, sondern prueft, ob bei kleineren
`N` bereits eine trennbare Signatur gegen einfache Negativkontrollen sichtbar
wird.

## Parameter

- embedding dimension: `5`
- seeds: `[1, 2, 3]`
- steps ladder: `[10000, 30000, 60000]`
- conditions: `['baseline', 'eta_zero', 'single_scale', 'shuffled_memory']`
- engine request: `auto`
- sample_every: `10`
- max_memory: `300`
- burn-in fraction: `0.2`
- estimator: `archive_fraktale_box_counting`

## Ergebnis

| condition | steps | runs | D_occ mean | D_occ 95% CI | D_cov mean | D_spec mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 10000 | 3 | 0.186 | 0.167..0.203 | 4.700 | 1.999 |
| eta_zero | 10000 | 3 | 0.739 | 0.570..0.923 | 1.606 | 1.240 |
| shuffled_memory | 10000 | 3 | 0.434 | 0.140..1.019 | 3.805 | 2.582 |
| single_scale | 10000 | 3 | 0.806 | 0.651..1.010 | 1.617 | 1.236 |
| baseline | 30000 | 3 | 0.325 | 0.296..0.366 | 4.496 | 1.915 |
| eta_zero | 30000 | 3 | 0.906 | 0.767..0.992 | 2.377 | 1.313 |
| shuffled_memory | 30000 | 3 | 0.313 | 0.272..0.346 | 4.828 | 2.120 |
| single_scale | 30000 | 3 | 0.959 | 0.859..1.026 | 2.363 | 1.305 |
| baseline | 60000 | 3 | 0.450 | 0.435..0.462 | 4.387 | 1.871 |
| eta_zero | 60000 | 3 | 1.063 | 1.045..1.093 | 2.583 | 1.334 |
| shuffled_memory | 60000 | 3 | 0.467 | 0.441..0.501 | 4.630 | 2.007 |
| single_scale | 60000 | 3 | 1.122 | 1.094..1.138 | 2.601 | 1.357 |

## Interpretation

Dieser Pilot ist ein Ressourcen-Test und ein Kontrollpfad. Ein belastbarer
Claim braucht weiterhin groessere `N`, mehr Seeds und stabilere Fitfenster.
Ein starkes Ergebnis waere hier nicht `D_occ` nahe 3 allein, sondern eine
konsistente Trennung des Baseline-Regimes von `eta_zero`, `single_scale` und
`shuffled_memory` ueber mehrere Diagnostiken.
