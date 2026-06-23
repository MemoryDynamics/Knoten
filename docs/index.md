# Emergenz Knoten Dokumentation

Stand: 2026-06-24.

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
2. [Non-Markovian Basis](non_markovian_basis.md)
3. [Architekturuebersicht](architecture_overview.md)
4. [Experiment-Katalog](experiment_catalog.md)
5. [Reproduzierbarkeitsstatus](reproducibility_status.md)
6. [Haertungsplan](hardening_plan.md)
7. [Paper-Claims](paper_claims.md)

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

Damit ergeben sich zwei moegliche naechste Schreibpfade:

- **Paper 0:** Literatur- und Methodenbasis fuer finite-memory
  self-interacting processes, Markovian embeddings und Transferoperatoren.
- **Paper I:** Ueberarbeitung des Minimalmodells mit klarer Trennung von
  Definition, numerical observation und conjecture.
- **Paper II:** Kinematik als Konsistenzstruktur metastabiler Operator-
  Regime formulieren; Lorentz-Symmetrie erscheint dann als effektiver
  Stabilisator des makroskopischen Propagationskegels.

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
