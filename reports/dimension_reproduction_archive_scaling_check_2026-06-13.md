# Dimension Reproduction Pilot

Datum: 2026-06-13

Quelle:

- Skript: `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- JSON: `data/processed/fractal_analysis/dimension_reproduction_archive_scaling_check.json`
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
- steps ladder: `[50000, 100000, 300000]`
- conditions: `['baseline']`
- engine request: `auto`
- sample_every: `10`
- max_memory: `300`
- burn-in fraction: `0.2`
- estimator: `archive_fraktale_box_counting`

## Ergebnis

| condition | steps | runs | D_occ mean | D_occ 95% CI | D_cov mean | D_spec mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 50000 | 3 | 0.422 | 0.401..0.454 | 4.239 | 1.727 |
| baseline | 100000 | 3 | 0.646 | 0.581..0.775 | 3.582 | 1.659 |
| baseline | 300000 | 3 | 1.008 | 0.954..1.063 | 2.026 | 1.407 |

## Interpretation

Dieser Pilot ist ein Ressourcen-Test und ein Kontrollpfad. Ein belastbarer
Claim braucht weiterhin groessere `N`, mehr Seeds und stabilere Fitfenster.
Ein starkes Ergebnis waere hier nicht `D_occ` nahe 3 allein, sondern eine
konsistente Trennung des Baseline-Regimes von `eta_zero`, `single_scale` und
`shuffled_memory` ueber mehrere Diagnostiken.
