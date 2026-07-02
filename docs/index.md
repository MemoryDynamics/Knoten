# Emergenz Knoten Dokumentation

Stand: 2026-07-02.

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

Paper 0 wird als mathematischer Anker bzw. moegliches Supplement gefuehrt. Es
muss nur Modell, Markov-Einbettung, kontraktive Memory-Faser und
Metastabilitaetsdiagnostik sauber machen. Paper I traegt die numerische
Knoten-Evidenz erst nach Long-Run-Kontrollen.

Der Kontrollreport vom 2026-07-01 zeigt: Memory-Gradient-Feedback trennt
sich klar von `eta_zero`, aber `single_scale` ist ebenfalls kompakt und
langlebig. Die naechste Prioritaet ist daher kein neuer Blindscan, sondern ein
strengeres Knotenkriterium aus Residence, Kompaktheit, Voxel-Stabilitaet und
Kontrolltrennung.

Die Kernel-Shape-Probe zeigt ausserdem: `A_att=0` ist in der aktuellen
Euler-Konvention keine Zerfallskontrolle; `A_rep=0` ist die passendere
Dispersionsablation. Der Seedvergleich zeigt verschiedene konkrete Pfade,
aber aehnliche lokale Schritt- und Turn-Metriken im Baseline-Regime.

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
