# Paper I - Self-Interacting Stochastic Dynamics with Exponential Memory

Stand: 2026-09-01.

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

## Abgrenzung zum deterministischen Schleifenast

Der reviewed P4-R-S-Befund stammt aus einem getrennten rauschfreien
`d=2`-Rotating-wave-Ast mit vorbereitetem Kreisorbit und explizit
konstruiertem Source-/Write-Port. Dort uebertraegt sich derselbe registrierte
diskrete Antworttyp von L3 auf den schon zuvor existenzzertifizierten Anchor;
die groesste Anchor--L3-Abweichung ist `0.00232715` gegen die prospektive
Grenze `0.05`. Ein separat implementierter Auditor rekonstruiert die
gespeicherte Entscheidung ohne Feldabweichung.

Dieser Zwei-Zellen-Pass ist weder eine unabhaengige Replikation noch eine
Konvergenzordnung und identifiziert keine physische Interaktion, keinen Spin,
keine Traegheit und keine Masse. Er wird deshalb nicht in den Paper-I-
Hauptclaim eingemischt. Eine spaetere Einordnung ist nur als getrennte
technische Notiz, Supplement-Option oder eng markierter Outlook vorgesehen;
`main.tex` und `main_compact.tex` bleiben in ihrer zentralen Evidenzlinie
unveraendert.

| Ebene | Eng tragbare Aussage | Nicht daraus ableitbar |
| --- | --- | --- |
| Evidenz | P4 schliesst den konstruierten Write-/Age-Ledger, scheitert aber formal am registrierten Gesamtgate. | operationaler Single-Loop-Mechanikpass |
| Evidenz | P4-R traegt am vorbereiteten L3-Kreis eine diskrete chirality-odd Portantwort mit 8/8 Phasensupport. | kontinuierliche Phase, interne Topologie oder unabhaengige Replikation |
| Evidenz | P4-R-S uebertraegt denselben registrierten Antworttyp auf den Anchor; maximaler Zwei-Zellen-Unterschied `0.00232715` gegen `0.05`. | Konvergenzordnung, stabile Familie oder natuerliche Portselektion |
| Inferenz | Die explizite diskrete Portarchitektur ist an zwei vorbereiteten Skalen intern kompatibel. | mechanisches Objekt, materieller Schwerpunkt oder physische Arbeit |
| Hypothese | Zwei getrennte Schleifen koennten ueber einen gegenseitigen Port eine nichtadditive Mutualantwort zeigen. | Interaktion, Ladung, Spin, Impuls, Traegheit oder Masse vor einem reviewed P5-Lauf |

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

Getrennte Schleifen-/Port-Einordnung:

- `docs/status/p4rs_plain_language_summary.md`
- `reports/project/meta/reviews/scalar_memory_loop_p4rs_anchor_scale_result_review_2026-08-30.md`

## Reviewte N0-Bruecke zum Schleifenarm

Die Paper-I-Uebergangssprache bleibt der gemeinsame Modellkern:

\[
x_{n+1}=x_n+\varepsilon\xi_n-\eta\nabla\Phi_n(x_n),\qquad
\rho_{n+1}=(1-\lambda_{\rm m})\rho_n
+\beta_\rho G_\sigma(\cdot-x_{n+1}).
\]

Der Schleifenarm verwendet davon zunaechst die deterministische
`epsilon=0`-Spezialisierung mit endlichem geordnetem Gedächtnis. Der vor P5
eingeschobene N0-Stresstest hebt diese Spezialisierung kontrolliert auf. Er
vergleicht Skalen ueber
`chi = epsilon / (R sqrt(alpha))`, entsprechend
`D/R^2 = chi^2/2` unter der Paper-I-Konvention
`D = epsilon^2/(2 alpha)`.

Der prospektive Lauf und sein unabhaengiges Recompute sind nun reviewed. Bis
`chi=1e-16` bleibt die Innovation numerisch unaufgeloest; `1e-15..1e-4`
bestehen, `1e-3` und `1e-2` scheitern am lokalen Phasen-/Chiralitaetsgate.
Dies ist eine finite-time Robustheitsklammer zweier vorbereiteter Zellen, kein
physikalischer Rauschpegel. Diese enge Abgrenzung steht jetzt in den
Diskussionsabschnitten der Lang- und Kurzfassung; sie erweitert nicht den
Paper-I-Hauptclaim. Rohes `epsilon` ist wegen der Normierung mit `R` und
`alpha` weder zell- noch konventionsuebergreifend vergleichbar.

Ergebnis und enges Review:

- `reports/dynamics/rotation/scalar_memory_rotating_wave_noise_stress_2026-08-31.md`
- `reports/project/meta/reviews/scalar_memory_rotating_wave_noise_stress_result_review_2026-09-01.md`

## Build

```powershell
cd paper/paper_i/manuscript
latexmk -xelatex main.tex
latexmk -xelatex main_compact.tex
```
