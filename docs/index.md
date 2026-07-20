# Emergenz Knoten Dokumentation

Stand: 2026-07-19.

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

1. [Aktueller Stand](status/current_status.md) - Was ist jetzt wahr, was laeuft, was ist offen?
2. [Prioritaeten](status/project_priorities.md) - Was als Naechstes zu tun ist.
3. [Theoretical Context](reference/THEORETICAL_CONTEXT.md) - Modellkern, Markov-Schicht, Claim-Grenzen.
4. [Repository Map](reference/repository_map.md) - Mermaid-Uebersicht ueber Code, Daten, Paper und Doku.
5. [Experiment-Katalog](reference/experiment_catalog.md) - Entry-Points, Ergebnisse, Kontrollen, Reproduzierbarkeit.
6. [Paper-Claims](status/paper_claims.md) - Claim-Register fuer Paper 0/I/II/III.
7. Diese Startseite.

Damit ersetzt diese Struktur die alten Parallelseiten `action_matrix`,
`hardening_plan`, `markov_architecture`, `markov_requirements`,
`non_markovian_basis`, `project_map`, `architecture_overview`,
`reproducibility_status` und `long_run_metastability_plan`.

## Aktuelle Entscheidung

Paper 0 bleibt der mathematische Anker bzw. ein moegliches Supplement. Paper I
soll weiterhin den belastbaren Minimalmechanismus tragen, aber die numerische
Evidenz wird nach der Kernelgradient-Korrektur neu aufgebaut.

Historische Long-Run-Evidenz bleibt mit KnotScore v0.5 ausgewiesen. Fuer neue interaktionsfaehige Checkpoints ergaenzt v0.6 ein explizites Stationaritaets-Zulassungsgate; Details stehen im Experiment-Katalog. Alte matched-/zero-mean-/rep-zero-Evidenz vor der Kernelkorrektur ist `legacy-sign`-Auditmaterial.

Der Kernel-Familienvergleich macht die Reduktion explizit: fuer den q=3-
Zweiskalenkernel gilt bei gleicher lokaler Kruemmung exakt
`A_eff=A_att-9`. Auf dieser Achse kollabieren Ein- und Zweiskalen-Kurven bis
auf numerisches Rauschen. Die alte Grenze bei `A_att~=7.9` gehoert zum
rauschstaerkeren historischen Zweiskalen-Slice und darf nicht als neue
Ein-Kernel-Schwelle um sechs gelesen werden.

Die vorhandenen `N=30M/300M`-Radien und das vorregistrierte feste-`g`-Gate
bestaetigen den linearen Kern mit einer kleinen glatten Korrektur: bei
`R_linear/L=0.3` liegt der Radius seed-stabil etwa `6.2%` ueber der linearen
Skalierung, ohne relevante Aenderung von `D_mem` oder Roundness. Residence
und KnotScore sind ueber diese Radiusachse skalenempfindlich; die co-moving
Alternative ist auch fuer `eta=0` gesaettigt und daher nicht diskriminierend.

Die aktuelle Paper-I-Lesart bleibt deshalb eng: kontrollierte co-moving
skalare Relaxationswolke, keine isolierte nichtlineare Metastabilitaet und
kein Dimensionsclaim. Weitere skalare Amplituden- oder kleinere-Epsilon-
Sweeps sind nicht priorisiert.

Die Spektralfeldschicht stellt dasselbe exponentielle rho mit 64 Moden und
rund 1 KB Zustandspeicher dar; eine endliche Realraumhistorie validiert die
Kraft bis zum erwarteten Memory-Tail. Low-Mode-/AR-Closure, Box-/Modenzahlgate
und ein N=1M-Lauf stuetzen eine reduzierte Vorhersagebeschreibung. Der
Eigenvektor-/Zeitsegmentaudit isoliert jedoch keinen stabilen einzelnen
reellen Modus; komplexe aktive und `eta=0`-Subraeume sind praktisch
identisch. Damit kein Oszillator-, Photon-, Metastabilitaets- oder
Propagationsbefund.

Der erste One-Way-Quelltest bleibt ebenfalls negativ, ist nun aber methodisch
schaerfer: Der N100M-Checkpoint besteht ein explizites Vorlauf-
Stationaritaetsgate. Ein externer Punkt-Drive bewegt die Source
radiusbeschraenkt, aber nicht in allen Seeds durchgehend spektral
formkohaerent, und erzeugt nur eine sub-threshold Targetantwort. Naechster
Mechanismusschritt ist deshalb shape-bounded/coherent Source-Transport oder
ein lokaler/retardierter Feldkanal. Reziproke Kopplung bleibt bis dahin
gesperrt.

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
