# Emergenz Knoten Dokumentation

Stand: 2026-07-10.

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
soll weiterhin den belastbaren Minimalmechanismus tragen, aber die numerische
Evidenz wird nach der Kernelgradient-Korrektur neu aufgebaut.

Der v0.5-Knotenscore ist die aktuelle Scorecard, dokumentiert im Experiment-Katalog. Die alte matched-/zero-mean-/rep-zero-Evidenz vor der Kernelkorrektur ist `legacy-sign`-Auditmaterial.

Die korrigierte Amplitudenhierarchie findet kompakte Kurzlauf-Kandidaten im Fenster `A_att=9..35` bei `A_rep=1`; der Umschlag liegt bei `A_att ~= 7.9`. Der erste Vektormemory-Pilot ist ein Kontrollbefund: komplexe AR-Moden treten bereits im `eta_v=0`-Fallback auf und sind noch kein isolierter Vektoreffekt.

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
