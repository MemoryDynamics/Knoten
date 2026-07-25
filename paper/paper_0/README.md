# Paper 0 - Mathematical Companion Note

Stand: 2026-07-26.

Working title:

**Self-Interacting Dynamics with Exponential Memory: Markovian Embedding,
Contractive Memory Fibres, and Metastability Diagnostics**

## Rolle

Paper 0 ist der mathematische Begleittext zu Paper I. Er ist als technischer
Anhang oder Companion Reference gedacht, nicht als eigenstaendiger
Neuheits- oder numerischer Phasenclaim.

Der Text:

- definiert die allgemeine Memory-Form
  `rho[n+1] = (1-lambda_m) rho[n] + beta G_sigma`;
- trennt sie von der normierten Konvention `lambda_m = beta = alpha`;
- leitet die exakte exponentielle Memory-Expansion her;
- beweist die Markov-Einbettung des augmentierten Zustands;
- beweist die pfadweise Kontraktion der Memory-Faser bei festem sichtbaren
  Pfad;
- trennt algebraische Ein-Schritt-Invertierbarkeit vom Verlust der geordneten
  Historie;
- formuliert eine formale Kontinuumsapproximation und kontrollbewusste
  Metastabilitaetsdiagnostik.

Nicht bewiesen werden globale Kontraktion, Ergodizitaet, spektrale Luecke,
nichtlineare Knotenexistenz oder ein Phasenuebergang.

## Literaturabgrenzung

Die revidierte Fassung unterscheidet explizit:

- kumulative normalisierte Occupation-Memory bei Benaim, Ledoux und Raimond;
- die symmetrische Free-Energy-Theorie von Benaim und Raimond (2005);
- die ungewichtete Vollhistorie bei Herrmann und Roynette (2003);
- den direkten Aging-/Exponential-Memory-Vergleich bei Milisic, Meunier und
  Roux (2026).

Die Arbeit beansprucht daher weder exponentielles Memory noch die
Markov-Zustandserweiterung als allgemeine Neuheit.

## Straffung

Die ungenutzte Skew-Product-Sektion und die redundante Beschreibung der
numerischen Pipeline wurden entfernt. Die Pipeline bleibt im Repository und
im Companion Paper dokumentiert. Die Regularitaetsannahmen wurden fuer
diskretes Modell, formalen Kontinuumsgrenzfall und Hessian-Linearisierung
getrennt praezisiert.

## Dateien

- `main.tex`: LaTeX-Quelle.
- `references.bib`: Bibliographie.
- `generate_figures.py`: reproduzierbare Abbildungen.
- `fig_memory_weights.pdf`: exponentielle Gewichte.
- `fig_transfer_spectrum.pdf`: illustrativer Transferdiagnostik-Check.

## Build

```powershell
cd paper/paper_0
latexmk -xelatex main.tex
```
