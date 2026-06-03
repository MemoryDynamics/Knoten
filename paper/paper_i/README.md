# Paper I - Emergente Raumzeit

## Übersicht

Dieses Verzeichnis enthält **Paper I** der Emergenz_Knoten-Forschung:
- **Fokus**: Frühe Knoten-Modelle, Trajektorien-Dynamik, Raumzeitstrukturen
- **Status**: Aktiv (Rohversion in progress)

## Dateien

- `main.tex` — LaTeX-Hauptdatei (kopiert aus docs/EmergenteRaumzeit/1.tex)
- `references.bib` — Bibliographie
- `main.pdf` — Kompiliertes PDF
- `archiv/` — Alte Versionen (für Reproduzierbarkeit)
- `fig*.pdf` — 5 referenzierte Figures:
  - `fig1_knot_trajectory.pdf`
  - `fig2_knot_scatter.pdf`
  - `fig3_knot_trajectory.pdf`
  - `fig_alpha.pdf`
  - `fig_Gamma_alpha.pdf`

## Workflow

1. Bearbeite `main.tex`
2. Kompiliere mit `pdflatex main.tex`
3. Aktualisiere `references.bib` bei Bedarf
4. Commit mit `git add -A && git commit -m "paper_i: ..."`

## Verwandtheit

- **Experiment**: `experiments/knot_stability/` — Knoten-Modell-Skripte
- **Figures**: `figures/paper/` — Production Figures
- **Dokumentation**: `docs/EmergenteRaumzeit/` — Rohversion & Archiv

## Hinweise

- Figures sind lokal kopiert, um Unabhängigkeit zu gewährleisten
- `docs/EmergenteRaumzeit/archiv/` enthält frühere Versionen
- Hauptarbeit erfolgt hier; docs/ dient als Backup
