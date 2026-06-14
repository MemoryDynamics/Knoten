# Paper-Claims und Status

Stand: 2026-06-14.

Quellen beim Audit:

- `C:\Users\Hauke\Downloads\1-3.pdf`
- `C:\Users\Hauke\Downloads\main-5.pdf`
- `C:\Users\Hauke\Documents\Hobby\Weltformel\EmergenteRaumzeit\PNGs\N_D29.pdf`

Neuere Projektquellen:

- `reports/dimension_claim_seed_audit_2026-06-13.md`
- `reports/dimension_reproduction_results_2026-06-13.md`
- `reports/fractal_parameter_landscape_reading_2026-06-13.md`
- `docs/non_markovian_basis.md`

## Paper 0: Non-Markovian Basis und Markov-Einbettung

Kernthese: Das Knotenmodell ist ein endlich-gedaechtnisbehafteter,
selbstinteragierender stochastischer Prozess. Der sichtbare Prozess `x_n` ist
nichtmarkovsch; der augmentierte Zustand `(x_n, rho_n)` bzw.
`(x_n, history_n)` ist eine natuerliche Markov-Einbettung.

Paper-0-Aufgabe:

- Literaturumgebung klaeren: self-interacting diffusions, reinforced/random
  walks, self-repelling Brownian polymer, exponentielle Memory-Kerne,
  generalized Langevin equations, Markovian embeddings, Transferoperatoren.
- Zeigen, welche Teile des Modells Standard sind und wo die spezifische
  Neuheit liegt.
- Operational definieren, wie metastabile Knoten ueber Uebergangsdynamik,
  Residence, Relaxationsspektren und negative Controls getestet werden.

Status: strategisch wahrscheinlich der robusteste naechste Schreibpfad, weil
er die existierende Mathematik andockt, bevor Paper I staerkere Physikclaims
traegt.

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

Status: als konzeptionelles Fundament brauchbar. Die naechste Ueberarbeitung
sollte `x_n` als sichtbaren nichtmarkovschen Prozess und `rho_n` als
Markov-Embedding-Variable explizit trennen. Diagnostiken muessen als
Definition, numerical observation oder conjecture markiert werden.

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
Konsistenzargumente als harte Ableitungen. Besonders die `d=3`-Selektion,
Propagation und Lorentz-Argumentation brauchen getrennte Schichten:
mathematische Annahmen, numerische Evidenz, und klar benannte Fail-Conditions.
Diese Arbeit sollte nach Paper 0 oder nach einer Paper-I-Haertung priorisiert
werden.

## N_D29.pdf

Extrahierte Beschriftungen zeigen einen Plot `D_occ` gegen `N` fuer
Embedding-Dimensionen `d=2` bis `d=9`, mit `N` etwa im Bereich `10^5` bis
`10^7`. Das Artefakt gehoert wahrscheinlich zur Fraktal-/Occupancy-Dimension
und Dimension-Selection-Linie.

Status: als Ergebnisgrafik nuetzlich. Die neueren Reports zeigen, dass die
staerkste archivierte Long-N-Spur in `resultsN.csv` liegt:

- `embedding dim = 5`
- `N = 60,000,000`
- fuenf Runs
- `mean D_occ = 2.810559`
- population std etwa `0.029533`

Fuer Paper-Haertung fehlen weiterhin:

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
| Sichtbarer Prozess `x_n` ist nichtmarkovsch, augmentierter Speicherzustand ist markovsch | gut formulierbar | formale Definition und erste Trace-/Lagged-Dataset-API |
| Effektive Dimension nahe 3 ist stabil bevorzugt | archiviert vielversprechend, neu noch nicht gehaertet | Reproduktion mit D_cov, D_occ, D_spec, finite-size scaling, CI, Negativkontrollen |
| `d <= 2` wird durch Wiederkehr/Selbstblockade ausgeschlossen | heuristisch stark, formal offen | saubere finite-memory-Version der Wiederkehraussage |
| `d >= 4` verliert Stabilitaet durch Speicherverduennung | heuristisch, parameterabhaengig | Skalierung mit `sigma`, `epsilon`, `alpha`, Kernelklasse |
| Endliche Propagation folgt aus endlichem Speicher | plausibel | Kick/no-kick-Experimente, Threshold-Robustheit, Scaling von `c_eff` |
| Lorentz-Kinematik folgt aus universalem `c_eff` | derzeit Konsistenzargument | Annahmen explizit machen, lineare Transformationsklasse pruefen |
| Bezug zu Elektron/Standardmodell | spekulativ | erst nach dimensionsloser, robuster Kalibrierung anfassen |
| Masse als Funktion der Speicherlaenge | Arbeitshypothese | Relaxationsraten gegen `alpha`, Memory-Horizon und Kernelklasse testen |

## Paper-taugliche Sprachregel

Bis die Haertung steht, sollte der Text zwischen drei Kategorien trennen:

- "We define" fuer Modellannahmen und Diagnostiken.
- "We observe numerically" fuer Simulationsergebnisse.
- "We conjecture" fuer Weltmodell-/Standardmodell-/Lorentz-Bruecken, die noch
  nicht durch reproduzierbare Tests getragen sind.

Aktuelle robuste Dimensionssprache:

> In archived finite-size occupancy data, the strongest near-3 signal appears
> in a higher embedding space, most clearly for embedding dimension 5 at
> `N = 60,000,000`, where five runs cluster around `D_occ = 2.81`. New
> short-to-mid-scale reproductions are consistent with the archived finite-size
> trend but do not yet establish robust 3D selection.
