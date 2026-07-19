# Paper-Claims und Status

Stand: 2026-07-19.

Diese Datei ist das aktive Claim-Register. Sie trennt Modelldefinition,
strukturelle Resultate, numerische Beobachtungen und Future Work.

## Paper 0: Mathematical Anchor

Status: traegt als technischer Anker oder Supplement.

Robuste Aufgabe:

- self-interacting stochastic dynamics with exponential memory definieren;
- allgemeine Memory-Form `(1-lambda_m)rho_n + beta G_sigma` fuehren;
- normierte `alpha`-Konvention als Spezialfall erklaeren;
- explizite exponentielle Memory-Expansion ableiten;
- Markov-Einbettung des augmentierten Zustands formulieren;
- pfadweise Kontraktion der Memory-Faser beweisen;
- Metastabilitaet als messbare Diagnostik rahmen.

Nicht Aufgabe von Paper 0:

- robuste Knotenexistenz ueber Parameterbereiche;
- eindeutige `d=3`-Selektion;
- endliche Signalgeschwindigkeit;
- Lorentz-, Quanten- oder Standardmodell-Ableitung;
- physikalische Massen.

## Paper I: Minimal Dynamical Foundation

Status: mathematisch mit Paper 0 synchronisiert; der aktuelle kleine-Radius-Ast traegt als co-moving linearer skalarer Relaxationsbefund, noch nicht als nichtlineare Metastabilitaetsevidenz.

Aktuell tragbar:

- Minimalmodell mit relaxierendem Memory;
- sichtbarer Prozess nichtmarkovsch, augmentierter Zustand markovsch;
- interne Speicherskala `alpha^{-1}` in der normierten Konvention;
- Knotenbegriff als diagnostischer Kandidat, nicht beobachtete Metastabilitaet;
- Relaxationsraten nur als Stabilitaets- oder mass-like proxies.

Noch nicht tragbar:

- fixed absolute spatial knots;
- stabiler skalarer Spin-/Phasen-/Photonmodus;
- physikalische Masse;
- starke Dimensions- oder Raumzeitclaims.

Der fruehere Driftumschlag bei A_att ungefaehr 7.9 gehoert ausschliesslich
zum historischen Slice mit festem A_rep=1. Ohne A_rep besitzt jeder positive
A_att-Wert lokale Rueckstellung; der neue A_att=0..40-Screening-Scan zeigt
keinen endlichen Phasenuebergang.

Der enge Kernel-Core-Audit und die seed-gematchte Ablation zeigen, dass die
bisherige (1,35)-Referenz im gesampelten Taylor-Regime bis etwa 1e-8 relativ
durch den attraktiven Ein-Kernel-Punkt (0,26) reproduziert wird. Fuer
A_att>=5 folgt der dynamische Radius der exakten linearen
Memory-Center-Vorhersage mit 0.94 Prozent medianem und 3.44 Prozent maximalem
relativen Fehler. Die erweiterte Reconciliation ueber neun aktive
`N=30M/300M`-Slices reduziert den maximalen finite-memory Radiusfehler auf
`1.16%`. Der direkte Familienvergleich zeigt bei q=3 die exakte
Reparametrisierung `A_eff=A_att-9`; auf dieser Achse kollabieren Ein- und
Zweiskalen-KPIs numerisch.

Das feste-g-Gate bis `R_linear/L=0.3` findet eine seed-stabile `6.2%`-
Superlinearitaet, aber keine relevante D_mem- oder Roundness-Aenderung. Seine
vorregistrierte Composite-Regel bleibt formal `inconclusive`. Die nachgelagerte
Skalenpruefung zeigt, dass feste Voxel Residence und KnotScore ueber die
veraenderte Radiusachse verzerren; co-moving Residence ist fuer aktive und
eta-zero-Pfade gesaettigt und deshalb nicht diskriminierend.

Damit ist fuer Paper I derzeit tragbar: Das skalare Feedback erzeugt eine
reproduzierbar kompaktere, mitbewegte Relaxationswolke als eta=0. Nicht
tragbar ist die staerkere Aussage, dass die Daten einen nichtlinearen
metastabilen Knoten oder einen Phasenuebergang isolieren. D_mem nahe drei im
d=3-Embedding ist im linearen isotropen Regime erwartete Gaussgeometrie und
keine Dimensionsselektion. Long-Run-Trace-AR, Feature-Closure und der negative
Spinbefund sind mit diesem reellen Relativmodus konsistent.

Ein dynamisches Relaxations-Diffusionsfeld bleibt eine kontrollierte
Modellerweiterung: Sein stationaerer Greenkernel ist nicht global
gaussfoermig, der Feldzustand muss in die Markov-Einbettung, und Diffusion
allein liefert keine harte endliche Ausbreitungsgeschwindigkeit.

The static field audit and calibrated distance ladder sharpen the interaction
interpretation: with `A_att=35`, the scalar point-source field is attractive at
all tested radii, and the stored d3/d10 clouds are unresolved by the much broader
cross-kernel. The full Ambient-Rang response is therefore expected. The current
`rho>=0` channel has no knot-specific sign and cannot support charge or
neutrality claims. Moreover, the compact q=3 kernel is strongly non-neutral:
for `q>1`, two-scale zero integral (`a=q^-d`) and local restoring curvature
(`a>q^2`) are structurally incompatible. A broad third scale now provides
exact integral cancellation while preserving the local compact branch. The
minimal signed scalar cross-channel also passes its bitwise null, product and
label-flip architecture gates on one d3 and one d10 checkpoint. This is not
charge evidence: the labels are assigned, only the target is dynamic, and
independent-seed validation is still missing. Vector memory remains reserved
for oriented observables.

## Paper II: Propagation and Spacetime Kinematics

Status: Folgeprogramm.

Nur als Future Work formulieren:

- effektive Dimension;
- externe/macroskopische `d=3`-Selektion aus lokalen Memory-Shape-Befunden;
- Innen/Aussen-Reconciliation aus Center-Trace-, Memory-Shape- und Response-Dimensionen;
- Zwei-Knoten-Propagation;
- `c_eff` und Antwortkegel;
- Lorentz-artige Kinematik.

Kritische Bedingung: exponentielles Memory allein erzeugt keine harte kausale
Schranke, solange direkte Fernkopplung ueber `K` moeglich ist.

## Paper III: Quantum / Standard-Model Programme

Status: offene Future-Work-Tuer, aber ohne Claim-Status.

Der Weg ueber QFT-artige kollektive Moden und spaeter moegliche
Standardmodellstrukturen bleibt ausdruecklich offen. Er wird erst belastbar,
wenn metastabile Regime, Relaxationsskalen, Mehrknoten-Wechselwirkungen,
Synchronisation und Propagation reproduzierbar sind.

## Claim-Register

| Claim | Aktueller Status | Naechste Haertung |
| --- | --- | --- |
| Sichtbarer Prozess ist nichtmarkovsch | strukturell gut | in Paper 0/I konsistent halten |
| Augmentierter Zustand ist markovsch | strukturell gut | Markov-Kern/Operator sauber zitieren |
| Memory-Faser kontrahiert pfadweise | beweisbar | Normannahmen klar nennen |
| Knoten als metastabile Regime | nicht isoliert: Long-Run-Radien folgen dem finite-memory linearen Modus; das feste-g-Gate zeigt nur eine glatte 6.2%-Korrektur ohne Shape-Umschlag. Die vorregistrierte Regel ist formal inconclusive, ihre Residence-/Score-Stuetzen sind aber skalenverzerrt bzw. nicht diskriminierend | skalares Modell als Kontrollbaseline behalten; dynamisches Feld mit eigenem Zustand, Greenkernel-, Vorzeichen- und eta=0-Kontrollen testen |
| Baseline/Single-scale zeigen langlebige Residence | nur Legacy-Sign-Befund; der korrigierte attraktive Ast ist stattdessen linear erklaert | nicht als aktuellen Metastabilitaetsclaim verwenden |
| `D_occ ~ 2.8` im Archiv | numerische Beobachtung | Seed- und Fitfenster-Reproduktion |
| D_mem nahe 2.94 im aktuellen kleinen-Radius-Slice | seed-stabile Shape-Beobachtung, aber durch den isotropen linearen Relativmodus erklaert; in d=3 ist D_mem nahe drei erwartete Ambient-Gaussgeometrie, nicht 3D-Emergenz | nur als lineare Shape-Diagnostik berichten; Paper II braucht relationale oder ambient-unabhaengige Evidenz |
| `d=10`-A_att-Transition zeigt `D_cov ~=2.52` bei hoher `D_mem` | numerische Beobachtung; spricht fuer getrennte sichtbare Sample-Geometrie und interne Memory-Shape, aber nicht fuer einen makroskopischen `d=3`-Satz | Center-Trace-Dimensionen, `D_p90`/`D_p95`, D_spec-Skalenempfindlichkeit und Response-/Zwei-Knoten-Tests |
| `D_spec memory` naehrt sich bei hohen `d` etwa 3 | Legacy-Beobachtung und Hypothesenhinweis; Sensitivitaets- und `N=3M`-Rohsnapshot-Retest zeigen keine robuste externe Dimension | nicht isoliert claimen; nur gemeinsam mit lokalisierter relationaler Response weiterverfolgen |
| Uniformer externer Weak Probe liefert niedrigen Response-Rang | widerlegt fuer den aktuellen Skalarslice: Memory-Zentrumantwort ist isotrop vollrangig (`3` in `d=3`, `10` in `d=10`); Formantwort nicht seed-reproduzierbar | als Vollrang-Negativkontrolle berichten |
| Zweiskaliger q=3-Kernel ist zugleich lokal konfinierend und global neutral | analytisch widerlegt fuer `q>1`: `int K=0` verlangt `a=q^-d`, lokale Rueckstellung `a>q^2`; Fixed-chi-q-Pilot zeigt zusaetzlich, dass der kompakte Ast bei `R_mem/sigma_rep<=2e-4` nur lokale Steifigkeit identifiziert | breiter Drei-Skalen-Kompensator erfuellt Nullintegral und lokale Kruemmung im `N=1M`-Pilot; als Modellvariante, nicht als Neutralitaetsnachweis berichten |
| Signierter skalarer Cross-Kanal besitzt exakte Null- und Vorzeichenarme | als Architekturtest gestuetzt: auf je einem `N=100M`-Checkpoint in `d=3/10` sind Null- und Produktarme bitgenau, der Produkt-Flip kehrt die Antwort um und Radiusstoerungen bleiben klein; Labels sind extern vergeben | mindestens 6, bevorzugt 10 unabhaengige Zustaende ohne Retuning und feste Distanzpruefung unter/ueber dem Kraftwechsel |
| Geklonte Knoten ziehen sich wegen Neutralitaet oder Ladung an | weiterhin nicht gestuetzt: der alte `rho>=0`-Cross-Kanal war vorzeichenlos; der neue signierte Kanal zeigt nur kontrollierte Labelmechanik an einer eingefrorenen Quelle | erst unabhaengige Seeds, dann einseitig dynamische Quelle und zuletzt Reziprozitaet; keine Ladungssprache |
| Eindeutige `d=3`-Selektion | conjecture/offen; seeded d-alpha-N-Scan stuetzt kein stabiles Plateau | nicht behaupten |
| Endliche Propagation | conjecture/offen | lokale Kopplung und Response-Tests |
| Lorentz-Kinematik | conjecture/offen | erst nach Propagation |
| Relaxationsrate als Masse | conjecture/offen | nur mass-like proxy sagen |
| Standardmodellbezug | offene Paper-III-Tuer, spekulativ | erst nach stabilen Knoten, QFT-artigen kollektiven Moden und Mehrknoten-Tests |

## Paper-taugliche Sprachregel

- `We define` fuer Modellannahmen und Diagnostiken.
- `We prove` fuer direkte Strukturresultate.
- `We observe numerically` fuer reproduzierbare Simulationsergebnisse.
- `We conjecture` fuer Weltmodell-, Lorentz-, Quanten- oder
  Standardmodell-Bruecken.
