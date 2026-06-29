# Emergenz Knoten Dokumentation

Stand: 2026-06-29.

Diese Dokumentation ist die kuratierte Frontdoor fuer das Projekt. Rohnotizen,
Chatverlaeufe und historische Skripte bleiben erhalten, aber der belastbare
Arbeitsstand wird hier und in den datierten Reports zusammengefuehrt.

## Projekt in einem Satz

`Emergenz Knoten` untersucht, ob aus einem irreversiblen stochastischen
Punktprozess mit endlichem, relaxierendem Gedaechtnis metastabile Strukturen,
effektive Dimensionen, interne Zeitskalen und spaeter physikalische
Grobstrukturen operational entstehen koennen.

## Wichtigste Lesereihenfolge

1. [Aktueller Stand](current_status.md)
2. [Projektprioritaeten](project_priorities.md)
3. [Repository Map](repository_map.md)
4. [Non-Markovian Basis](non_markovian_basis.md)
5. [Markov-Architektur](markov_architecture.md)
6. [Markov-Anforderungen](markov_requirements.md)
7. [Architekturuebersicht](architecture_overview.md)
8. [Experiment-Katalog](experiment_catalog.md)
9. [Long-Run Metastability Plan](long_run_metastability_plan.md)
10. [Reproduzierbarkeitsstatus](reproducibility_status.md)
11. [Haertungsplan](hardening_plan.md)
12. [Paper-Claims](paper_claims.md)

## Aktuelle Arbeitsentscheidung

Die naechste inhaltliche Klammer ist nicht "direkt neue Physik behaupten",
sondern das Modell als endlich-gedaechtnisbehafteten, selbstinteragierenden
Prozess sauber zu verankern:

- Der sichtbare Prozess `x_n` ist nichtmarkovsch.
- Der augmentierte Zustand `z_n = (x_n, rho_n)` bzw.
  `z_n = (x_n, history_n)` ist die natuerliche Markov-Einbettung.
- Metastabile Knoten sollen nicht nur visuell oder geometrisch, sondern ueber
  Operator-/Uebergangsdynamik messbar werden.
- Algebraisch ist die Grundstruktur damit ein positiver Markov-/Koopman-
  Operator auf Observablen des augmentierten Zustandsraums; seine Iterierten
  bilden eine vorwaertsgerichtete Halbgruppe, keine reversible Gruppe.

Die aktuelle Arbeitsentscheidung nach Paper 0 ist zweigeteilt: Paper 0 wird
als mathematischer Anker bzw. moegliches Supplement eingefroren, waehrend Paper
I gegen diesen Anker synchronisiert und empirisch durch echte Long-Run-Laeufe
gehaertet wird. Die Markov-/Transferoperator-Schicht steht initial als
Paketstruktur; sie wird in [Markov-Architektur](markov_architecture.md)
erklaert, die Akzeptanzkriterien stehen in
[Markov-Anforderungen](markov_requirements.md).

Damit ergeben sich drei aktive Schreib- und Evidenzpfade, aber nicht mit
gleicher Prioritaet:

- **Paper 0:** technischer Anker fuer finite-memory self-interacting processes,
  Markovian embeddings und Transferoperator-Diagnostik; keine robuste
  Knotenexistenzbehauptung.
- **Paper I:** Minimalmodell mit konsistenter Speicherform, Markov-Sprache und
  spaeter Long-Run-Evidenztabelle fuer metastabile Knoten.
- **Long-Run-Kampagne:** Hintergrundlaeufe mit `n >= 10^7`, Residence-Zeiten,
  Negativkontrollen und Voxel-Sensitivitaet; siehe
  [Long-Run Metastability Plan](long_run_metastability_plan.md).

## Nicht ueberclaimen

Der archivierte Dimensionsbefund ist vielversprechend, aber noch nicht
abschliessend:

- In `experiments/fractal_analysis/Fraktale/resultsN.csv` liegt bei
  `embedding dim = 5`, `N = 60,000,000` ein Gruppenmittel
  `D_occ = 2.810559` ueber fuenf Runs vor.
- Neue Kurzlaeufe koppeln bei kleineren `N` plausibel an den Archivpfad an.
- Die getesteten Kurzlauf-Kontrollen zeigen noch keinen robusten Near-3-Claim.

Die belastbare Sprache bleibt deshalb: reproduzierbarer Archivanschluss und
klarer Haertungsplan, noch kein Nachweis eindeutiger 3D-Selektion.

## Build

Lokal:

```bash
python -m pip install -r docs/requirements.txt
python -m mkdocs serve
python -m mkdocs build
```

ReadTheDocs nutzt `.readthedocs.yaml` und `mkdocs.yml`.
