# Haertungsplan

Stand: 2026-05-22.

Ziel: Aus einem stark gewachsenen Explorationsprojekt ein reproduzierbares,
falsifizierbares Modellprogramm machen. Die Grundhaltung ist nicht, das Modell
zu schuetzen, sondern es so fair wie moeglich scheitern zu lassen.

## Phase 0: Reproduzierbarkeit herstellen

Definition of done:

- Python-Umgebung funktioniert lokal.
- `requirements.txt` oder Lockfile ist installierbar.
- Es gibt einen Baseline-Commit des historischen Stands.
- Jedes neue Experiment schreibt Parameter, Seed, Git-Revision und Outputs in
  ein Manifest.
- Lange Laeufe koennen fortgesetzt werden und erzeugen keine stillen
  Ueberschreibungen.

Soforttests:

- Import-Test: `numpy`, `matplotlib`, `numba`, `scipy`, `pandas`.
- Smoke-Test mit kleinem `N`, der in Sekunden laeuft.
- Determinismus-Test: gleicher Seed, gleiche Messwerte innerhalb Toleranz.

## Phase 1: Kanonischen Modellkern extrahieren

Zu kapseln:

- Speicherupdate `rho_{n+1} = (1-alpha) rho_n + alpha G_sigma(...)`
- Punktupdate `x_{n+1} = x_n + epsilon xi_n - eta grad Phi_n(x_n)`
- Kernelklassen: single Gaussian, double Gaussian, finite window, recursive
  memory approximation
- Diagnostiken: `D_cov`, `D_occ`, `D_spec`, Knot count, Residence, Relaxation

Minimaltests:

- Translation und Rotation aendern Diagnostiken nicht wesentlich.
- `eta = 0` reproduziert Random-Walk/Brownian-Kontrollen.
- `alpha -> 1` und sehr kleine Memory-Horizons zerstoeren Langzeitknoten.
- Speichergewichte bleiben normiert oder die Abweichung wird explizit
  dokumentiert.
- Diagnosefunktionen liefern auf synthetischen Punktwolken bekannte Werte
  (Linie ca. 1, Flaeche ca. 2, isotrope Wolke in 3D ca. 3 fuer passende
  Schaetzer).

## Phase 2: Hauptclaims reproduzieren

### A. Effektive Dimension nahe 3

Experimentdesign:

- Parameterregion aus den bisherigen besten Laeufen fixieren.
- Fuer jeden Punkt mindestens 20 Seeds laufen lassen.
- Drei unabhaengige Diagnostiken berichten: `D_cov`, `D_occ`, `D_spec`.
- Finite-size scaling ueber mehrere `N`.
- Bootstrap-Konfidenzintervalle und Sensitivitaet gegen Burn-in/Downsampling.
- Negative Controls: `eta=0`, shuffled memory, sign-flipped attraction,
  single-scale kernel.

Erfolgskriterium:

- Ein stabiler Plateauwert nahe 3 bleibt unter Seed-, N- und Diagnosewechseln
  erhalten.

Red flags:

- 2.8/3 tritt nur bei einer Diagnose oder nur bei einem engen Fitfenster auf.
- Plateau wandert monoton mit `N`.
- Ergebnis haengt stark an Downsampling, Voxelgroesse oder Threshold.

### B. Metastabile Knoten

Experimentdesign:

- Residence-Time-Verteilungen statt nur Mittelwerte.
- Knotenanzahl, mittlere Residence, Lebensdauer, Rueckkehrzeiten.
- Lokale Relaxationsspektren/Hessian-Approximationen in stabilen Regionen.
- Vergleich mit Brownian/TSAW/SRBP-aehnlichen Baselines.

Erfolgskriterium:

- Knoten sind nicht nur visuell erkennbar, sondern statistisch von Kontrollen
  unterscheidbar.

### C. Endliche Propagation / `c_eff`

Experimentdesign:

- Kick/no-kick-Ensemble mit gleicher Seed-Struktur.
- Response-Observable vorab definieren.
- Onset-Detection gegen Threshold, Glattung und Fenster testen.
- `L` variieren und `t_onset(L)` fitten.
- Scaling von `c_eff` gegen `alpha`, `sigma`, Memory-Horizon und Kernelklasse.

Erfolgskriterium:

- `t_onset` waechst robust linear mit Distanz, und die Steigung folgt den
  Modellparametern in erwarteter Richtung.

Red flags:

- Onset entsteht aus Threshold-Artefakten.
- Response ist bei randomisiertem Speicher gleich stark.
- Keine klare Trennung von diffusive spreading und front-like propagation.

### D. Lorentz-artige Kinematik

Experimentdesign:

- Zuerst nur als effektive Kinematik testen, nicht als vollstaendige Physik.
- Operationalen Lichtkegel aus Propagationsexperimenten definieren.
- Pruefen, ob verschiedene metastabile Knoten denselben `c_eff` messen.
- Verletzungen gegen Memory-Laenge, Coarse-Graining und anisotrope Kernel
  quantifizieren.

Erfolgskriterium:

- Ein gemeinsamer effektiver Cone existiert ueber mehrere Knoten/Regime hinweg.

Red flags:

- `c_eff` ist knotenspezifisch ohne universelles Plateau.
- Anisotropie bleibt makroskopisch gross.

## Phase 3: Theorie schaerfen

Zu trennen:

- Theorem: folgt aus expliziten Annahmen.
- Lemma: plausibel, aber annahmensensitiv.
- Numerical observation: reproduzierbarer Simulationsbefund.
- Conjecture: tragende Idee ohne ausreichende Haertung.

Kritische offene Stellen:

- Die Wiederkehrargumentation fuer `d <= 2` muss auf den finite-memory,
  selbstinteragierenden Prozess zugeschnitten werden.
- Die Speicherverduennung fuer `d >= 4` muss die Skalierung von `sigma`,
  `epsilon`, `alpha`, Kernelamplituden und Beobachtungsfenster explizit machen.
- Die Lorentz-Ableitung braucht eine klare Liste der Symmetrie-/Linearitaets-
  und Homogenitaetsannahmen.

## Phase 4: Paper-Readiness

Ein Claim darf in die starke Formulierung, wenn:

- Code und Daten reproduzierbar sind.
- Negative Controls dokumentiert sind.
- Fehlerbalken/CI vorhanden sind.
- Parameter- und Seed-Sensitivitaet gezeigt ist.
- Der Claim ohne Standardmodell-/Gravitationsueberdehnung formulierbar bleibt.

Bis dahin ist die robuste Formulierung:

> The model exhibits regimes in which memory-driven metastable structures show
> effective low-dimensional, finite-response behavior compatible with an
> emergent-geometry interpretation.
