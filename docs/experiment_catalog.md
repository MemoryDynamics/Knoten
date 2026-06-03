# Experiment-Katalog

Stand: 2026-05-22.

## Wichtigste Skripte

| Datei | Thema | Relevanz | Risiko |
| --- | --- | --- | --- |
| `Knoten.py` | 2D self-avoiding memory trajectory | frueher Modellkern, einfache Visualisierung | Top-level plotting, keine Parameterlogs |
| `Knoten3D.py` / `Knoten3D_prism.py` | 3D Trajektorien/Knotenfiguren | papernahe Knotenvisuals | noch keine reproduzierbare CLI |
| `DimensionsHeatmap*.py` | Spektral-/Kovarianzdimension ueber `alpha, eta` | zentrale Dimensionsdiagnostik | mehrere Versionen, teils schwere GPU/Numba-Laeufe |
| `DimensionsHeatmap4OptGPU.py` | CUDA Heatmap, `T=1_500_000` | groesster Scan fuer Dimension/Fitqualitaet | GPU-Abhaengigkeit, lange Laufzeit |
| `PaperII3D_*.py` | Retarded response, Time-of-flight, `c_eff`, Lichtkegel | zentrale Paper-II-Figuren | Threshold-/Glattungsrobustheit offen |
| `2SkalenKernel/emergent_3D_final.py` | Dimension plateau ueber `d=2..9`, `alpha`, `eta` | sehr wichtig fuer `d~3`-Claim | `N_MAX=2e8`, Checkpoint-Format ad hoc |
| `2SkalenKernel/SpecCovFrac.py` | Occupancy, covariance, spectral dimension im Double-Kernel | multi-diagnostic claim support | `N=150_000_000`, spektrale Diagnose O(n^2) im Fenster |
| `scripts/highN_regime.py` | Reproduzierbarer Pilot fuer das historischen 3D-High-N-Regime | Referenz-Entry-Point fuer Legacy-Parameter | ermoeglicht kleine Testlaeufe mit dem gleichen Kern |
| `scripts/highN_regime_validation.py` | Validierungs-Pilot fuer den historischen 7D-Regimepunkt | kleiner Einpunkttest mit Legacy-Parametern und Occupancy-Fit-Details | schneller Check ohne vollen 150M-Lauf |
| `scripts/highN_regime_ensemble.py` | Seed-Ensemble-Wrapper fuer das historische 7D-Regime | erlaubt Mittelwerte, Standardabweichungen und CI fuer D_cov/D_occ; unterstützt variable Regimeparameter | bevorzugt valide Fehlerbalken statt Einzelwerte |
| `knot_chi_scan.py` | Sweep ueber `chi = eta/(alpha sigma_att^2)` | Knotenanzahl/Residence/Dimension | schreibt nach `chi_scan`, lange Laeufe |
| `Fraktale/FD2.py` | Fraktaldimension, Parameter-Scan, finite-size scaling | wichtigste Occupancy-/Skalierungsbasis | CSV-Header passt nicht immer zum Row-Format |
| `Fraktale/fit_n_plot.py` | Fit von `D_inf`/Skalierung | Paper-Auswertung moeglich | Fitmodell muss preregistriert werden |
| `OU-Limit.py` | OU-Grenzfall | analytischer Kontrollfall | standalone plot |
| `EmergenzGravitation.py` / `emergenz_2regime.py` | Regime-/Anisotropiefiguren | konzeptionelle Karten | eher schematisch als beweisend |

## Ergebnisartefakte nach Claim

### Effektive Dimension

- `heatmap_spectral_dimension_gpu*.pdf`
- `heatmap_covariance_dimension_gpu*.pdf`
- `spectral_dimension_heatmap_optimized.pdf`
- `progress*.npy`, `progress*.npz`
- `2SkalenKernel/results*/D_vs_N.png`
- `2SkalenKernel/results*/D_vs_d.png`
- `Fraktale/results*.csv`
- `Fraktale/N_*.png`

### Endliche Propagation

- `diagram1_retarded_response.pdf`
- `diagram2_time_of_flight.pdf`
- `diagram3_ceff_scaling.pdf`
- `diagram4_light_cone.pdf`
- `front_delay_vs_L*.pdf`
- `front_lightcone.pdf`
- `diffusive_delay_vs_L*.pdf`
- `diffusive_lightcone.pdf`

### Knotenvisualisierung

- `fig1_knot_trajectory.pdf`
- `fig2_knot_scatter.pdf`
- `fig3_knot_trajectory.pdf`
- `Fraktale/N_*.png`

### Regime/Analytik

- `fig_alpha*.pdf`
- `fig_etaalpha.pdf`
- `fig_Gamma_alpha.pdf`
- `fig_OUlimit.pdf`

## Auffaellige technische Punkte

- Viele Skripte fuehren lange Simulationen direkt auf Top-Level aus.
- Mehrere Dateinamen enthalten historische Varianten statt semantischer
  Versionen (`*2`, `*3`, `Opt`, `GPU`, `cpy`, `copy`).
- Ergebnisdateien sind nicht eindeutig mit Parameterdateien verbunden.
- Einige CSV-Schreibfunktionen haben Header, die nicht zum tatsaechlichen
  Row-Format passen.
- Die Python-Umgebung ist beim Audit nicht lauffaehig; siehe
  `docs/reproducibility_status.md`.

## Priorisierte Reproduktionsziele

1. Kleiner Smoke-Test des kanonischen Kernels.
2. Reproduktion eines bekannten Heatmap-Punktes mit kurzer Laufzeit.
3. Reproduktion des staerksten `D_eff ~ 2.8/3`-Befunds mit 20 Seeds.
4. Reproduktion einer Time-of-flight-Grafik mit Fehlerbalken.
5. Negative-Control-Bundle fuer alle Hauptdiagnostiken.
