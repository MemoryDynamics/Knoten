# Paper I - Minimal Point-Valued Stochastic Dynamics with Relaxing Memory

Stand: 2026-07-21.

## Rolle

Paper I ist die aktuelle eigenstaendige Minimalmodell-Fassung. Es definiert
einen exponentiell relaxierenden Speicherzustand, den sichtbaren
nichtmarkovschen Prozess `x_n`, die Markov-Einbettung
`z_n = (x_n, rho_n)`, interne Zeitskalen, metastabile Knoten und
Relaxationsproxies, ohne bereits Raumzeit, Quantenmechanik oder
Standardmodell-Claims vorauszusetzen.

Es gibt bewusst zwei Varianten:

- `main.tex`: rigorose Langfassung mit ausfuehrlicher Begriffsarbeit und
  defensiver Argumentation.
- `main_compact.tex`: kompakte Review-/Publikationsvariante mit gleicher
  Kernkonstruktion, weniger Absicherungstext und strafferem roten Faden.

## Aktueller Fokus

Die aktuelle Fassung ist auf folgende Lesart geschaerft:

- `x_n` als sichtbarer nichtmarkovscher Prozess;
- `z_n = (x_n, rho_n)` bzw. `z_n = (x_n, history_n)` als
  Markov-Einbettung;
- Markov-/Koopman-Operatoren und Vorwaerts-Halbgruppen als algebraische
  Beschreibung der augmentierten Dynamik;
- allgemeine Memory-Form `(1-lambda_m) rho_n + beta G_sigma` mit normierter Arbeitskonvention `lambda_m=beta=alpha`;
- `alpha^{-1}` als interne Speicherpersistenzskala in dieser normierten Konvention;
- Knoten als operational messbare metastabile Strukturen;
- aktueller numerischer Paper-I-Kern: co-moving kompakte Memory-Clouds im
  korrigierten scalar reference slice, deren Radius durch den linearen
  Finite-Memory-Relativmodus erklaert wird;
- `D_mem ~=2.94` im gewaehlten 3D-Embedding als erwartete isotrope
  Ambient-Shape-Diagnostik und nicht als Dimensionsselektion;
- Massenbezug nur als spaetere Kalibrierungsfrage; aktuell nur Relaxations-/Konfinierungsproxy;
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
- Private Begleitnotizen und Anschreiben werden nicht im oeffentlichen Repo
  getrackt. Fuer externe Sichtung nur sanitisierte Reports verwenden.
- `archiv/`: fruehere Versionen.
- `fig*.pdf`: lokal kopierte Figuren fuer reproduzierbare Builds.

Aktiv im Paper verwendet:

- `fig_markov_embedding.pdf`: sichtbarer nichtmarkovscher Prozess vs.
  Markov-Einbettung. Diese PDF ist auf die aktuelle `z_n`-Notation
  aktualisiert; der Generator selbst wurde in dieser Runde bewusst nicht
  angepasst.
- `fig_memory_weights.pdf`: Speichergewichte und Persistenzskala
  `alpha^{-1}`.
- `fig3_knot_trajectory.pdf`: historische illustrative Kompakttrajektorie; keine eigenstaendige Metastabilitaetsevidenz.
- `fig_relaxation_diagnostic.pdf`: operationaler Relaxationsfit fuer
  `Gamma_rel`.

Die kompakte Variante verwendet nur die Knotentrajektorie als Abbildung.
Markov-Einbettung und Relaxationsdiagnostik werden dort direkt ueber Gleichungen
und Text gefuehrt. Die Speichergewichte und die Markov-Embedding-Grafik bleiben
in der Langfassung als ergaenzende Anschauung.

Die frueheren Alpha/Gamma-Schemafiguren bleiben lokal erhalten, sind aber in
Paper I bewusst nicht mehr Teil der Hauptargumentation.

## Verwandte Projektstellen

- `docs/reference/THEORETICAL_CONTEXT.md`
- `docs/status/current_status.md`
- `docs/status/paper_claims.md`
- `reports/project/papers/paper1_source_audit_2026-06-01.md`
- `reports/long_runs/long_3e8/paper_i_evidence_table_N30M_eps1em4_2026-07-13.md`
- `reports/dimensions/memory_shape_boundary_2026-07-13.md`
- `reports/dimensions/dimension_claim_audit_2026-07-15.md`
- `reports/dimensions/reproduction/dimension_claim_seed_audit_2026-06-13.md`
- `experiments/current/reference/reference_experiment.py`
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

## Aktueller Reviewfokus

Fuer eine erste externe Sichtung sollte der Fokus nicht auf spaeteren
Weltmodell-Claims liegen, sondern auf:

1. Traegt die Minimalmodell-Definition?
2. Ist die Non-Markov/Markov-Embedding-Sprache mathematisch sauber?
3. Ist die neue `z_n`-/Operatornotation konsistent mit `G_sigma` als
   Kernelbreite?
4. Sind `t = alpha n`, Knoten und Relaxations-/Konfinierungsproxies defensiv genug
   formuliert?
5. Ist Paper 0 als separates mathematisches Einordnungspaper bzw. Supplement sinnvoll?
6. Ist die Long-Run-Evidenz defensiv genug als co-moving Memory-Cloud-Befund
   formuliert, ohne feste Zentren, Spin, Photon- oder Teilchenclaims?
7. Ist `D_mem ~=2.94` klar als erwartete Shape-Diagnostik des gewaehlten
   3D-Embeddings und nicht als Dimensionsselektion abgegrenzt?
