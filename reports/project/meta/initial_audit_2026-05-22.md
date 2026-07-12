# Initial Audit

Datum: 2026-05-22.

## Kurzdiagnose

Das Projekt hat bereits einen erstaunlich klaren inneren Bogen:

1. Minimaler irreversibler Speicherprozess.
2. Metastabile lokale Strukturen ("Knoten").
3. Effektive Dimension als Diagnose stabiler Freiheitsgrade.
4. Endliche Antwort/Propagation aus endlicher Speicherrelaxation.
5. Lorentz-artige Kinematik als makroskopische Konsistenzbedingung.

Die starke Seite ist nicht ein einzelner Plot, sondern die Wiederkehr derselben
Motive in mehreren numerischen Familien: Trajektorien, Dimension, Residence,
Retardierung und OU-/Regime-Grenzen.

## Hauptbefund

Das Modell ist als Weltmodell-Kandidat interessant genug, um systematisch
gehaertet zu werden. Es ist aber noch nicht in einem Zustand, in dem starke
Formulierungen zu Standardmodell, Elektron, Gravitation oder vollstaendiger
Lorentz-Invarianz paper-sicher waeren.

Die beste naechste Strategie ist daher:

- erst Reproduzierbarkeit,
- dann kanonischer Modellkern,
- dann die Dimension-nahe-3-Behauptung maximal hart pruefen,
- danach erst physikalische Identifikationen.

## Staerken

- Minimaler Generator ist knapp formulierbar.
- Endliche, relaxierende Erinnerung ist ein echter strukturgebender
  Mechanismus und nicht nur Dekoration.
- Mehrere unabhaengige Diagnoseideen existieren bereits:
  `D_cov`, `D_occ`, `D_spec`, Residence, Time-of-flight.
- Paper-Drafts trennen teilweise schon zwischen Modell, Diagnostik und
  spaeterer physikalischer Kalibrierung.

## Risiken

- Ein grosser Teil der Evidenz ist derzeit nicht reproduzierbar gekapselt.
- Viele Claims koennen von Fitfenstern, Downsampling, Voxelgroessen und Seeds
  abhaengen.
- Die `d=3`-Argumentation ist stark, aber mathematisch noch heuristisch.
- `c_eff`/Lorentz braucht mehr als plausible Lichtkegelplots: universelle
  Messbarkeit ueber verschiedene Knoten/Regime.
- Die Python-Umgebung ist aktuell kaputt, was jede Reproduktion blockiert.

## Erste Entscheidungen

- Historische Skripte werden zunaechst nicht verschoben.
- Neue Struktur startet mit Dokumentation, Claim-Register und Haertungsplan.
- `.gitignore` ignoriert Umgebungen/IDE/Cache, aber nicht pauschal Daten oder
  PDFs, weil diese fuer die historische Evidenz wichtig sind.
- `requirements.txt` enthaelt nur die aktuell sichtbaren Mindestabhaengigkeiten.

## Naechste konkrete Schritte

1. Python-Umgebung reparieren.
2. Baseline-Commit erstellen.
3. `src/emergenz_knoten/diagnostics.py` mit den drei Dimensionsdiagnostiken
   extrahieren.
4. Ein kleines Experimentprofil bauen, das in unter einer Minute laeuft.
5. Den besten vorhandenen `D_eff ~ 2.8/3`-Lauf identifizieren und als
   reproduzierbares Experiment neu aufsetzen.
