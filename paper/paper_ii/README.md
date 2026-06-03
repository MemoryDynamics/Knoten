# Paper II - Propagation Speed & Light-Cone Dynamics

## Übersicht

Dieses Verzeichnis enthält **Paper II** der Emergenz_Knoten-Forschung:
- **Fokus**: Propagation Speed, retardierte Effekte, effektive Light-Cone-Struktur
- **Status**: In Entwicklung (Main-Struktur vorbereitet)

## Dateien

- `main.tex` — LaTeX-Hauptdatei
- `references2.bib` — Bibliographie

## Verwandte Experimente & Daten

### Skripte
- `experiments/propagation_speed/` — Light-cone Analyse Skripte:
  - `PaperII3D_*.py` (4 Visualisierungs-Skripte)

### Figures (Draft)
- `figures/draft/` — Analysis Plots (noch nicht in Paper integriert):
  - `diagram*.pdf` — Retardierte Response, Time-of-Flight
  - `front_*`, `diffusive_*` — Light-Cone Diagramme

### Daten
- `data/processed/` — JSON/NPY Simulationsergebnisse

## Workflow

1. Bearbeite `main.tex`
2. Referenziere Figures aus `figures/draft/` oder generiere neue
3. Kompiliere mit `pdflatex main.tex`
4. Aktualisiere `references2.bib`
5. Commit mit `git add -A && git commit -m "paper_ii: ..."`

## Nächste Schritte

- [ ] Main-Struktur finalisieren
- [ ] Figures selektion & Beschreibung
- [ ] References compilieren
- [ ] Erste Draft-Version

## Hinweise

- Unterscheide zwischen Rohfiguren (figures/draft/) und Production-Figures
- Simulationsergebnisse in data/processed/ referenzierbar
- Skripte in experiments/propagation_speed/ sind reproduzierbare Datenquellen
