# Emergenz Knoten Dokumentation

Stand: 2026-07-09.

Diese Dokumentation ist die kuratierte Frontdoor fuer das Projekt. Sie ist
bewusst klein gehalten: aktive Orientierung laeuft ueber sieben Dokumente.
Historische Chatverlaeufe, alte Paper-Artefakte und Rohnotizen bleiben im
Repository, gelten aber nicht als kuratierte Quelle.

## Projekt in einem Satz

`Emergenz Knoten` untersucht einen selbstinteragierenden stochastischen
Prozess mit relaxierendem Gedaechtnis. Der sichtbare Prozess `x_n` ist im
Allgemeinen nichtmarkovsch; der augmentierte Zustand `z_n=(x_n,rho_n)` bzw.
eine explizite Memory-Reprasentation ist die Markov-Einbettung. Metastabile
Knoten sollen ueber Residence-Zeiten, Operator-Moden und Kontrollen messbar
werden, nicht ueber Einzelbilder.

## Die sieben aktiven Dokumente

1. [Aktueller Stand](current_status.md) - Was ist jetzt wahr, was laeuft, was ist offen?
2. [Prioritaeten](project_priorities.md) - Was als Naechstes zu tun ist.
3. [Theoretical Context](THEORETICAL_CONTEXT.md) - Modellkern, Markov-Schicht, Claim-Grenzen.
4. [Repository Map](repository_map.md) - Mermaid-Uebersicht ueber Code, Daten, Paper und Doku.
5. [Experiment-Katalog](experiment_catalog.md) - Entry-Points, Ergebnisse, Kontrollen, Reproduzierbarkeit.
6. [Paper-Claims](paper_claims.md) - Claim-Register fuer Paper 0/I/II/III.
7. Diese Startseite.

Damit ersetzt diese Struktur die alten Parallelseiten `action_matrix`,
`hardening_plan`, `markov_architecture`, `markov_requirements`,
`non_markovian_basis`, `project_map`, `architecture_overview`,
`reproducibility_status` und `long_run_metastability_plan`.

## Aktuelle Entscheidung

Paper 0 bleibt der mathematische Anker bzw. ein moegliches Supplement. Paper I
soll aktuell nicht die gesamte Emergenzphysik tragen, sondern den belastbaren
Befund formulieren: aktives Memory-Feedback erzeugt confinement-artige,
metastabile Regime relativ zu `eta_zero`, `m0_zero` und `alpha_one`.

Der v0.5-Knotenscore trennt `baseline` und `single_scale` klar von den harten
Negativkontrollen. Er isoliert aber keinen notwendigen zweiskaligen
Baseline-Mechanismus. Auch der neue `matched_deposition`-Pilot bleibt zwar
confined relativ zu `eta_zero`, ist ohne Steifigkeitsrenormierung aber breiter
als die Delta-Baseline.

Naechster gezielter Schritt: eine curvature-renormalized matched-deposition
Condition testen, bevor weitere 100M-Laeufe gestartet werden.

## Nicht ueberclaimen

- Keine eindeutige `d=3`-Selektion aus den bisherigen Daten.
- Keine harte endliche Signalgeschwindigkeit aus exponentiellem Gedaechtnis
  allein.
- Keine Identifikation von Relaxationsraten mit physikalischer Masse.
- Keine Lorentz-, Quanten- oder Standardmodell-Claims in Paper 0/I ausser als
  Future Work.

## Build

```bash
python -m pip install -r docs/requirements.txt
python -m mkdocs serve
python -m mkdocs build --strict
```

ReadTheDocs nutzt `.readthedocs.yaml` und `mkdocs.yml`.
