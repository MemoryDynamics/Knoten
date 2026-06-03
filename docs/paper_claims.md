# Paper-Claims und Status

Stand: 2026-05-22.

Quellen beim Audit:

- `C:\Users\Hauke\Downloads\1-3.pdf`
- `C:\Users\Hauke\Downloads\main-5.pdf`
- `C:\Users\Hauke\Documents\Hobby\Weltformel\EmergenteRaumzeit\PNGs\N_D29.pdf`

## Paper I: Minimal Point-Process Dynamics with Memory

Kernthese: Ein minimaler Punktprozess auf einem abstrakten Zustandsraum `Omega`
wird an eine explizite, endliche, relaxierende Speicherverteilung gekoppelt.
Das Speicherupdate ist nicht invertierbar und erzeugt eine intrinsische
Update-Richtung. Unter Grobkoernung `t = alpha n` kann eine SDE/Fokker-Planck
Beschreibung sinnvoll werden. Metastabile lokalisierte Strukturen ("Knoten")
werden ueber Relaxationsraten, Stabilitaetsmasse und Residence-Statistiken
diagnostiziert.

Wichtige bewusste Nicht-Claims im Draft:

- keine fundamentale Raumzeit
- keine Quantum-Postulate
- keine Felder oder Erhaltungsgroessen
- keine Kalibrierung zu SI-/Spacetime-Einheiten
- Standardmodell-/Relativitaets-Anbindung wird an Companion Works delegiert

Status: als konzeptionelles Fundament brauchbar, aber der technische Anspruch
haengt an operationalen Diagnostiken. Diese Diagnostiken muessen aus den
Skripten in testbare, versionierte Funktionen extrahiert werden.

## Paper II: Emergent Spacetime Kinematics from Irreversible Memory Dynamics

Kernthese: Effektiver Raum und relativistische Kinematik entstehen als
Konsistenzbedingungen metastabiler Knoten:

- effektive Dimension aus robusten, schwach gekoppelten Relaxationsmoden
- makroskopische Auswahl `d = 3` durch Kombination aus
  Wiederkehr-/Selbstblockade fuer `d <= 2` und Speicherverduennung fuer
  `d >= 4`
- endliche Signalgeschwindigkeit aus endlicher Speicherreichweite und
  Speicherrelaxation, grob `c_eff ~ l_mem / tau_mem`
- Lorentz-artige Kinematik aus universeller maximaler Propagationsgeschwindigkeit
  und Beobachter-/Knoten-Aequivalenz

Bewusst ausgeklammert:

- dynamische Gravitation/Kruemmung
- Quantenstruktur, Spinoren, Gauge-Wechselwirkungen
- konkrete physikalische Kalibrierung

Status: spannende These, aber mehrere Saetze sind derzeit eher
Konsistenzargumente als harte Ableitungen. Besonders die `d=3`-Selektion und
die Lorentz-Argumentation brauchen getrennte Schichten: mathematische Annahmen,
numerische Evidenz, und klar benannte Fail-Conditions.

## N_D29.pdf

Extrahierte Beschriftungen zeigen einen Plot `D_occ` gegen `N` fuer
Embedding-Dimensionen `d=2` bis `d=9`, mit `N` etwa im Bereich `10^5` bis
`10^7`. Das Artefakt gehoert wahrscheinlich zur Fraktal-/Occupancy-Dimension
und Dimension-Selection-Linie.

Status: als Ergebnisgrafik nuetzlich, aber fuer Paper-Haertung fehlen im
Repository unmittelbar daneben:

- genaue Parameter
- Seed-Strategie
- Anzahl der Runs
- Fehlerbalken oder Konfidenzintervalle
- Rohdatenzuordnung

## Claim-Register

| Claim | Aktueller Status | Noetige Haertung |
| --- | --- | --- |
| Nichtinvertierbarer Speicher erzeugt Update-Richtung | gut formulierbar | formale Minimalannahmen und Gegenbeispielgrenzen |
| Metastabile Knoten entstehen in bestimmten Parameterregimen | numerisch plausibel | Residence-Verteilungen, Lebensdauern, Seed-Ensembles |
| Effektive Dimension nahe 3 ist stabil bevorzugt | vielversprechend, aber kritisch | Reproduktion mit D_cov, D_occ, D_spec, finite-size scaling, CI |
| `d <= 2` wird durch Wiederkehr/Selbstblockade ausgeschlossen | heuristisch stark, formal offen | saubere finite-memory-Version der Wiederkehraussage |
| `d >= 4` verliert Stabilitaet durch Speicherverduennung | heuristisch, parameterabhaengig | Skalierung mit `sigma`, `epsilon`, `alpha`, Kernelklasse |
| Endliche Propagation folgt aus endlichem Speicher | plausibel | Kick/no-kick-Experimente, Threshold-Robustheit, Scaling von `c_eff` |
| Lorentz-Kinematik folgt aus universalem `c_eff` | derzeit Konsistenzargument | Annahmen explizit machen, lineare Transformationsklasse pruefen |
| Bezug zu Elektron/Standardmodell | spekulativ | erst nach dimensionsloser, robuster Kalibrierung anfassen |

## Paper-taugliche Sprachregel

Bis die Haertung steht, sollte der Text zwischen drei Kategorien trennen:

- "We define" fuer Modellannahmen und Diagnostiken.
- "We observe numerically" fuer Simulationsergebnisse.
- "We conjecture" fuer Weltmodell-/Standardmodell-/Lorentz-Bruecken, die noch
  nicht durch reproduzierbare Tests getragen sind.
