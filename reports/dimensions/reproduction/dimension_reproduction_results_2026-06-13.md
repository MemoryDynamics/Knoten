# Dimension Reproduction Results

Datum: 2026-06-13

## Scope

Dieser Lauf prueft den archivierten `D_occ ~ 2.8`-Befund aus
`experiments/fractal_analysis/archive_source/data/n_scaling/resultsN.csv` unter lokalen
Ressourcenbeschraenkungen.

Neu hinzugefuegter Entry-Point:

- `experiments/fractal_analysis/reproduce_dimension_pilot.py`

Er nutzt den historischen Fraktal-Parametersatz:

- `dim = 5`
- `epsilon = 0.05`
- `eta = 2.0`
- `alpha = 0.01`
- `A = 1.0`
- `B = 3.0`
- `sigma_rep = 1.0`
- `sigma_att = 0.15`
- `max_memory = 300`
- historischer Box-Counting-Schaetzer aus `archive_source/scripts/FD2.py`

Die lokale Codex-Python-Runtime hatte kein `numba`; die Laeufe wurden daher
mit der vektorisierten NumPy-Implementierung ausgefuehrt.

## Implementation Check Against Archive

Baseline-only, 3 Seeds, neuer reproduzierbarer Pfad:

| N | archived dim=5 mean D_occ | new mean D_occ | new 95% CI |
| ---: | ---: | ---: | ---: |
| 50,000 | 0.421737 | 0.421893 | 0.401013..0.453854 |
| 100,000 | 0.630021 | 0.645965 | 0.581214..0.775108 |
| 300,000 | 1.099995 | 1.008439 | 0.954117..1.062546 |
| 60,000,000 | 2.810559 | not run locally | n/a |

Interpretation: Der neue Reproduktionspfad trifft die archivierte
Finite-Size-Skala bei `50k` und `100k` sehr gut und bleibt bei `300k` in der
gleichen Groessenordnung. Damit ist die Implementierung fuer kleine bis
mittlere `N` plausibel an den Archivpfad gekoppelt.

## Negative-Control Pilot

Kleiner Kontrolllauf, 3 Seeds, `N = 10k, 30k, 60k`:

| condition | N | mean D_occ | mean D_cov | mean D_spec |
| --- | ---: | ---: | ---: | ---: |
| baseline | 60,000 | 0.449562 | 4.386536 | 1.871364 |
| eta_zero | 60,000 | 1.062666 | 2.583211 | 1.333678 |
| shuffled_memory | 60,000 | 0.467421 | 4.629946 | 2.007148 |
| single_scale | 60,000 | 1.121828 | 2.600773 | 1.356632 |

Interpretation: Bei `N <= 60k` ist kein Near-3-`D_occ` sichtbar. Das ist
konsistent mit dem Archiv, wo `dim=5` erst bei Millionen-Schrittzahlen in den
Bereich `D_occ > 2` steigt.

Die Kontrollen liefern bei dieser kleinen Skala kein starkes positives Signal
fuer den Claim:

- `baseline` und `shuffled_memory` liegen bei `D_occ` fast gleich.
- `eta_zero` und `single_scale` liegen bei `D_occ` hoeher als die Baseline.
- `D_cov` trennt dagegen Baseline/shuffled von eta_zero/single_scale deutlich,
  ist aber kein direkter Ersatz fuer den archivierten Box-Counting-Claim.

## Current Claim Status

Belastbar:

> Der archivierte `dim=5`-Finite-Size-Trend ist mit einem neuen
> seed-kontrollierten Skript bei kleinen und mittleren `N` reproduzierbar.

Nicht belastbar aus den neuen Kurzlaeufen:

> Der Near-3-Befund ist bereits unter lokalen Kurzlaeufen oder unter den
> getesteten Negativkontrollen stabil sichtbar.

Weiterhin gueltig aus dem Archiv:

> In `resultsN.csv` erreicht `dim=5` bei `N=60,000,000` ueber fuenf Runs
> `mean D_occ = 2.810559`.

## Next Run Under Realistic Resources

Naechster sinnvoller Schritt nach Reparatur einer `numba`-faehigen Umgebung:

1. Baseline `dim=5` bei `N = 1,000,000`, `2,500,000`, `6,000,000`, je 3 Seeds.
2. Danach `shuffled_memory` bei denselben `N`, weil diese Kontrolle den
   Speichermechanismus direkt trifft.
3. Erst wenn Baseline und shuffled auseinanderlaufen, `eta_zero` und
   `single_scale` im gleichen Bereich nachziehen.

Ohne `numba` ist `N >= 1,000,000` lokal moeglich, aber wenig effizient. Mit
`numba` ist der Millionenbereich der richtige naechste Haertungsschritt.
