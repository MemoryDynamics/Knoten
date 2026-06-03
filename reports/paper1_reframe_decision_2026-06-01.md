# Paper I Reframe Decision

Datum: 2026-06-01.

Quelle: `docs/EmergenteRaumzeit/1.tex`

## Ausgangslage

Paper I ist aktuell als Weltmodell-Grundlegung formuliert:

- Minimaler irreversibler Punktprozess
- endliche, relaxierende Memory-Dynamik
- emergente Update-Zeit
- metastabile Knoten
- mass-like Relaxationsskalen

Das ist inhaltlich konsistent, aber breit. Der riskante Teil ist nicht der
Modellkern, sondern die implizite Erwartung, dass ein Leser schon in Paper I
den Weg zu Raumzeit, 3D, Lorentz, Standardmodell und Gravitation mitgeht.

## Empfehlung

Paper I sollte nicht komplett auf 3D umgebaut werden. Besser ist ein engerer
technischer Fokus:

> Define the finite-memory point-process model, derive its operational
> coarse-grained time and metastability diagnostics, and establish the
> numerical/analytical toolkit used later for dimension selection.

Die 3D-Selektion gehoert als Hauptclaim in Paper II oder in ein eigenes,
deutlich fokussierteres Paper:

> Finite-memory self-interaction selects low-dimensional metastable regimes,
> with evidence for an effective dimension near three.

## Warum diese Trennung sinnvoll ist

- Paper I hat bereits einen sauberen Kern: Grundgleichungen, Irreversibilitaet,
  Zeitparameter, Knoten, Relaxation.
- Die 3D-Selektion braucht andere Evidenz: lange finite-size scaling runs,
  Seed-Ensembles, negative Controls, mehrere Dimensionsdiagnostiken.
- Ein Paper, das gleichzeitig Modellaxiome, Zeit, Masse, Raumdimension und
  Weltmodell-Vision tragen soll, wird schwer zu verteidigen.
- Ein enger Paper-I-Scope macht spaetere starke Claims glaubwuerdiger, weil die
  Begriffe vorher operational definiert sind.

## Konkreter Zielzuschnitt fuer Paper I

### Behalten

- Definition von `sigma_n = (x_n, rho_n)`
- Update-Gleichungen fuer `x_n` und `rho_n`
- Nicht-Invertierbarkeit als Update-Pfeil
- `t = alpha n` als coarse-grained Parameter
- finite-memory mixture interpretation
- OU-Linearisierung als frozen-memory Approximation
- `Gamma_rel`, `D`, `widehat{Gamma}` als Diagnostiken
- Knoten als metastabile dynamische Muster

### Straffen

- Weltmodell-Sprache in Introduction und Outlook reduzieren.
- "Mass" konsequent als relaxation/stability proxy kennzeichnen.
- Lorentz-/Standardmodell-/Gravitationsbruecken nur als Companion-Work
  erwaehnen, nicht ausargumentieren.
- Figuren nur behalten, wenn sie direkt eine Definition oder Diagnose stützen.

### Auslagern

- 3D-Selektion
- endliche Signalgeschwindigkeit und `c_eff`
- Lorentz-Kinematik
- Standardmodell-/Elektron-Spekulation
- Gravitation/Kosmologie

## Alternative: 3D-Fokus als neues Paper I

Moeglich, aber riskanter. Dann muesste das Paper neu aufgebaut werden:

1. Modellgleichungen nur kurz.
2. Dimension diagnostics als Hauptmethodik.
3. finite-size scaling und negative Controls als Hauptresultat.
4. 3D-Selektionsargument formal und numerisch.
5. Weltmodell-Vision nur in einem kurzen Outlook.

Dafuer fehlt aktuell noch die reproduzierbare Datenkette. Daher ist diese
Variante erst nach der Haertung des `D_occ ~ 2.8/3`-Befunds sinnvoll.

## Naechster sinnvoller Schritt

Paper I technisch sauber bauen und minimal ueberarbeiten. Parallel dazu die
3D-Dimension-Story in einem separaten `paper_3d_outline.md` vorbereiten, sobald
die Reproduktionspipeline steht.
