# Paper I - Self-Interacting Stochastic Dynamics with Exponential Memory

Stand: 2026-07-26.

## Rolle

Paper I ist die eigenstaendige Modell- und Evidenzfassung. Es definiert den
sichtbaren nichtmarkovschen Prozess `x_n`, die Markov-Einbettung
`z_n = (x_n, rho_n)` und die exponentielle Memory-Dynamik. Der aktuelle
publikationsrelevante Befund ist eine lineare co-moving Relaxationswolke, nicht
ein isolierter nichtlinearer Knoten.

Es gibt zwei synchronisierte Varianten:

- `main.tex`: ausfuehrliche Fassung mit Regularitaets-, Operator-, Skalierungs-
  und Diagnostikdiskussion.
- `main_compact.tex`: kompakte Publikationsfassung mit derselben Modell- und
  Evidenzlinie.

## Hauptresultat

Aus der exakten Memory-Center-Rekursion

```text
m[n+1] = (1-alpha) m[n] + alpha x[n+1]
```

folgt im lokal linearen Skalarregime fuer `r_n = x_n - m_n` ein reeller
AR(1)-Relativmodus. Seine stationaere RMS-Radiusvorhersage wird mit der
tatsaechlich gespeicherten finite-memory Masse ausgewertet.

Ueber neun aktive Long-Run-Slices mit je fuenf Seeds, `d=3..20` und
Lauflaengen bis `N=300M` betraegt der mediane relative Radiusfehler `0.76%`,
der maximale `1.15%`. Gematchte Ein- und Zweiskalenkernel kollabieren auf der
lokalen Kruemmungsachse. Ein feste-g-Nichtlinearitaetsgate zeigt bei
`R_linear/L=0.3` eine glatte `6.2%`-Radiuskorrektur, aber keinen Shape- oder
Residence-Umschlag; seine vorregistrierte Gesamtentscheidung bleibt
`inconclusive`.

Daraus folgt:

- gestuetzt: reproduzierbare kompakte, mitbewegte skalare Relaxationswolke;
- nicht isoliert: nichtlinearer metastabiler Zustand oder Phasenuebergang;
- nicht informativ fuer Dimensionsselektion: `D_mem` nahe drei im
  dreidimensionalen isotropen Embedding.

`Dynamical knot` bleibt als Projektbegriff fuer einen kuenftigen Befund
reserviert, der die lineare Nullhypothese, `eta=0`-Kontrollen und skalenbewusste
Metastabilitaetsdiagnostik uebersteht.

## Literaturpositionierung

Die Einleitung grenzt die Arbeit jetzt konkret ab gegen:

- Benaim, Ledoux und Raimond: normalisierte kumulative Besetzungsmasse;
- Benaim und Raimond (2005): symmetrische Wechselwirkung und
  Free-Energy-Konvergenz;
- Herrmann und Roynette (2003): ungewichtete Vollhistorie, nicht
  exponentielles Memory;
- Milisic, Meunier und Roux (2026): Aging-Kernel mit linearen
  Wechselwirkungen und explizitem Exponentialfall.

Die Neuheit wird nicht mehr mit exponentiellem Memory oder Zustandserweiterung
allein begruendet, sondern mit dem konkreten diskreten Feldmodell und dem
kontrollierten linearen Nulltest.

## Abbildungen

Aktiv verwendet:

- `fig_markov_embedding.pdf` in der Langfassung;
- `fig_memory_weights.pdf` in der Langfassung;
- `figures/draft/scalar_hardening/linear_reconciliation_2026-07-19/linear_long_run_reconciliation.png`
  in beiden Fassungen.

Die historische `fig3_knot_trajectory.pdf` bleibt im Ordner erhalten, wird aber
nicht mehr als Paper-Evidenz verwendet. Die schematische
`fig_relaxation_diagnostic.pdf` ist ebenfalls nicht mehr Teil der zentralen
Argumentation.

## Zentrale Evidenz

- `reports/long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.md`
- `reports/kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.md`
- `reports/kernels/nonlinearity/fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.md`
- `docs/status/paper_claims.md`

## Build

```powershell
cd paper/paper_i
latexmk -xelatex main.tex
latexmk -xelatex main_compact.tex
```
