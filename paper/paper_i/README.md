# Paper I - Minimal Point-Process Dynamics with Finite Memory

Stand: 2026-06-14.

## Rolle

Paper I ist die aktuelle eigenstaendige Minimalmodell-Fassung. Es definiert
einen endlichen, exponentiell relaxierenden Speicherprozess, den sichtbaren
nichtmarkovschen Prozess `x_n`, die Markov-Einbettung `(x_n, rho_n)`, interne
Zeitskalen, metastabile Knoten und Relaxationsproxies, ohne bereits Raumzeit,
Quantenmechanik oder Standardmodell-Claims vorauszusetzen.

## Aktueller Fokus

Die aktuelle Fassung ist auf folgende Lesart geschaerft:

- `x_n` als sichtbarer nichtmarkovscher Prozess;
- `(x_n, rho_n)` bzw. `(x_n, history_n)` als Markov-Einbettung;
- `alpha^{-1}` als interne Speicherpersistenzskala;
- Knoten als operational messbare metastabile Strukturen;
- Masse nur als Relaxations-/Konfinierungsproxy;
- klare Trennung von Definition, numerical observation und conjecture.

## Dateien

- `main.tex`: LaTeX-Hauptdatei.
- `references.bib`: Bibliographie.
- `main.pdf`: kompilierte Fassung.
- `../../reports/paper1_olaf_note_2026-06-14.md`: kurze Begleitnotiz fuer
  Sichtung/Diskussion.
- `archiv/`: fruehere Versionen.
- `fig*.pdf`: lokal kopierte Figuren fuer reproduzierbare Builds.

## Verwandte Projektstellen

- `docs/non_markovian_basis.md`
- `docs/current_status.md`
- `docs/paper_claims.md`
- `reports/paper1_source_audit_2026-06-01.md`
- `reports/dimension_claim_seed_audit_2026-06-13.md`
- `experiments/reference_experiment.py`
- `src/emergenz_knoten/`

## Build

Bevorzugt mit LaTeX-Toolchain im Paper-Ordner:

```powershell
latexmk -xelatex main.tex
```

Wenn `latexmk` nicht verfuegbar ist, kann direkt mit `xelatex` und `bibtex`
gebaut werden.

## Aktueller Versandfokus

Fuer eine erste Sichtung durch Olaf sollte der Fokus nicht auf spaeteren
Weltmodell-Claims liegen, sondern auf:

1. Traegt die Minimalmodell-Definition?
2. Ist die Non-Markov/Markov-Embedding-Sprache mathematisch sauber?
3. Sind `t = alpha n`, Knoten und Mass-/Relaxationsproxies defensiv genug
   formuliert?
4. Ist Paper 0 als separates mathematisches Einordnungspaper sinnvoll?
