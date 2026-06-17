# Paper I - Minimal Point-Valued Stochastic Dynamics with Relaxing Memory

Stand: 2026-06-16.

## Rolle

Paper I ist die aktuelle eigenstaendige Minimalmodell-Fassung. Es definiert
einen exponentiell relaxierenden Speicherzustand, den sichtbaren
nichtmarkovschen Prozess `x_n`, die Markov-Einbettung `(x_n, rho_n)`, interne
Zeitskalen, metastabile Knoten und Relaxationsproxies, ohne bereits Raumzeit,
Quantenmechanik oder Standardmodell-Claims vorauszusetzen.

Es gibt bewusst zwei Varianten:

- `main.tex`: rigorose Langfassung mit ausfuehrlicher Begriffsarbeit und
  defensiver Argumentation.
- `main_compact.tex`: komprimierte Olaf-/Publikationsvariante mit gleicher
  Kernkonstruktion, weniger Absicherungstext und strafferem roten Faden.

## Aktueller Fokus

Die aktuelle Fassung ist auf folgende Lesart geschaerft:

- `x_n` als sichtbarer nichtmarkovscher Prozess;
- `(x_n, rho_n)` bzw. `(x_n, history_n)` als Markov-Einbettung;
- `alpha^{-1}` als interne Speicherpersistenzskala;
- Knoten als operational messbare metastabile Strukturen;
- Masse nur als Relaxations-/Konfinierungsproxy;
- klare Trennung von Definition, numerical observation und conjecture.

## Dateien

- `main.tex`: LaTeX-Hauptdatei der rigorosen Langfassung.
- `main_compact.tex`: kompakte Variante fuer schnelle Sichtung und moegliche
  Publikationsfassung.
- `references.bib`: Bibliographie.
- `main.pdf`: kompilierte Langfassung.
- `main_compact.pdf`: kompilierte Kurzfassung, falls gebaut.
- `generate_figures.py`: erzeugt die Paper-I-spezifischen Modell- und
  Diagnostikfiguren.
- `../../reports/paper1_olaf_note_2026-06-14.md`: kurze Begleitnotiz fuer
  Sichtung/Diskussion.
- `../../reports/paper1_olaf_note_2026-06-16.md`: aktuelles Anschreiben fuer
  Olaf mit Verweis auf `https://memorydynamics.org`.
- `archiv/`: fruehere Versionen.
- `fig*.pdf`: lokal kopierte Figuren fuer reproduzierbare Builds.

Aktiv im Paper verwendet:

- `fig_markov_embedding.pdf`: sichtbarer nichtmarkovscher Prozess vs.
  Markov-Einbettung.
- `fig_memory_weights.pdf`: Speichergewichte und Persistenzskala
  `alpha^{-1}`.
- `fig3_knot_trajectory.pdf`: representative metastabile Knotenbildung.
- `fig_relaxation_diagnostic.pdf`: operationaler Relaxationsfit fuer
  `Gamma_rel`.

Die kompakte Variante verwendet nur die Knotentrajektorie als Abbildung.
Markov-Einbettung und Relaxationsdiagnostik werden dort direkt ueber Gleichungen
und Text gefuehrt. Die Speichergewichte und die Markov-Embedding-Grafik bleiben
in der Langfassung als ergaenzende Anschauung.

Die frueheren Alpha/Gamma-Schemafiguren bleiben lokal erhalten, sind aber in
Paper I bewusst nicht mehr Teil der Hauptargumentation.

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

Kompakte Variante:

```powershell
latexmk -xelatex main_compact.tex
```

## Aktueller Versandfokus

Fuer eine erste Sichtung durch Olaf sollte der Fokus nicht auf spaeteren
Weltmodell-Claims liegen, sondern auf:

1. Traegt die Minimalmodell-Definition?
2. Ist die Non-Markov/Markov-Embedding-Sprache mathematisch sauber?
3. Sind `t = alpha n`, Knoten und Mass-/Relaxationsproxies defensiv genug
   formuliert?
4. Ist Paper 0 als separates mathematisches Einordnungspaper sinnvoll?
