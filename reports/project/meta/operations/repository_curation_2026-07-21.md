# Repository-Kuration 2026-07-21

## Ziel

Die aktive Projektoberflaeche wurde nach dem Miller-Prinzip neu geordnet:
wenige gleichzeitig sichtbare Entscheidungen, klare Evidenzstufen und eine
separate historische Auditspur. Wissenschaftliche Negativbefunde bleiben
erhalten; geloescht werden nur reproduzierbare Buildartefakte oder exakte,
unreferenzierte Kopien.

## Ausgangslage

Bestandsaufnahme auf Revision `b9f5477`:

- sauberer `main`-Arbeitsbaum und Synchronitaet mit `origin/main`;
- 627 sichtbare Dateien, davon 168 unter `reports/`, 128 unter `figures/` und
  135 unter `experiments/`;
- 129 Markdown-Reports, davon 83 aus der aktiven Doku referenziert;
- 49.29 MiB getrackte Dateien;
- 739 lose Git-Objekte mit 8.88 MiB, aber keine gemeldete Garbage-Struktur;
- aktive Statusseite mit 774 Zeilen und aktive Prioritaetenliste mit 606
  Zeilen;
- mehrere lokale Testcaches, ein gebautes `site/` und rund 9.9 MiB Scratch-
  Material unter dem ignorierten `tmp/`.

## Befund

### Evidenz

- Der Arbeitsbaum war vor der Kuration sauber.
- Die neuesten Interaction-Age-Reports waren bereits in Status, Katalog und
  Theorie eingeordnet.
- Alle neueren datierten Reports ab 2026-07-18 waren aus der aktiven Doku
  erreichbar.
- Eine CSV (`results_copy.csv`) war byteidentisch, unreferenziert und nur eine
  Kopie.
- Vier getrackte LaTeX-Dateien (`*.out`, `*.synctex.gz`) waren generierte
  Buildprodukte.

### Inferenz

Die Hauptlast entstand nicht durch fehlende Dokumentation, sondern durch zu
viel aktive Chronologie: abgeschlossene Einzelschritte standen neben aktuellen
Entscheidungen und machten die Frontdoor schwer lesbar. Das Risiko war weniger
Datenverlust als Claim-Verwechslung zwischen aktuellem Befund, historischem
Zwischenstand und Future Work.

### Nicht behauptet

- Die Kuration bewertet nicht jeden historischen Report erneut.
- Ein unreferenzierter alter Report ist nicht automatisch falsch.
- Inhaltlich identische Paperfiguren koennen fuer selbstenthaltene LaTeX-Builds
  absichtlich mehrfach vorliegen.
- Lokales Scratch-Material ist keine wissenschaftliche Evidenz, solange es
  nicht reviewed und committed wurde.

## Umgesetzte Ordnung

1. Die langen Status- und Prioritaetenchronologien wurden unter
   `docs/archive/status/` eingefroren.
2. `docs/status/current_status.md` wurde als kurze Sieben-Punkte-Frontdoor mit
   expliziter Trennung von Evidenz, Inferenz und Hypothese neu aufgebaut.
3. `docs/status/project_priorities.md` enthaelt nur noch fuenf aktive Gates,
   Stopregeln und bewusst zurueckgestellte Programme.
4. `reports/README.md` indexiert die aktuelle Evidenzschiene und fuehrt ein
   Statusvokabular (`structural`, `supported`, `negative`, `inconclusive`,
   `pipeline-only`, `legacy-sign`, `superseded`) ein.
5. `figures/README.md` trennt Draft-, Paper- und Kommunikationsabbildungen.
6. Frontdoor-Daten und aktuelle Source-/Interaction-Age-Einordnung wurden auf
   den Stand 2026-07-21 gebracht.
7. Exakte Kopie und getrackte Buildprodukte wurden entfernt; `.gitignore`
   schuetzt kuenftige LaTeX-Nebenprodukte.
8. Lokale Caches, `site/`, `results/` und `tmp/` wurden entfernt; reviewed
   Daten unter `data/processed/` blieben unangetastet.

## Wissenschaftliche Entscheidung nach der Kuration

- Der skalare Ast bleibt lineare kontrollierte Baseline.
- Das Interaction-Age-Gate zeigt Translation ohne kontrollgetrennte
  Formmodifikation; eine reine Laufzeitverlaengerung ist kein priorisierter
  Mechanismustest.
- Genau eine neue Hypothese darf als Naechstes geoeffnet werden: lokaler bzw.
  retardierter Mediator oder orientiertes Vektormemory.
- Reziproke Kopplung, Dimensions-, Lorentz-, Quanten- und Standardmodellclaims
  bleiben gesperrt, bis die jeweils vorgelagerten diskriminierenden Gates
  bestehen.

## Verifikation

- Ruff: bestanden.
- Vollstaendige Testsuite: `265 passed`.
- MkDocs strict: bestanden.
- Lokale Links in den 13 aktiven bzw. neuen Markdown-Frontdoor-Dateien:
  `0` gebrochene Ziele.
- Git-Integritaet: keine fehlenden oder korrupten Objekte; `fsck` meldete nur
  nicht referenzierte Zwischenobjekte aus den Arbeitsvorgaengen.
- Kuratierter Index: 650 getrackte Pfade mit 49.24 MiB. Die verbleibenden 13
  exakten Duplikatgruppen sind leere `.gitkeep`-Dateien oder beabsichtigte
  selbstenthaltene Paper-/Archivkopien.
- Getrackte LaTeX-Nebenprodukte: `0`.
- Standard-GC: `0` lose Objekte, `0` Garbage, zwei Packs mit 40.64 MiB.
- Prozesshygiene: 47 verwaiste `git.exe`-Abfragen beendet.
- GitHub Actions wird nach dem Push bis zum Endstatus beobachtet.
