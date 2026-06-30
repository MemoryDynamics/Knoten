# Paper-Claims und Status

Stand: 2026-06-30.

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

Status: mathematisch mit Paper 0 synchronisiert; numerische Evidenz wird jetzt
gehaertet.

Aktuell tragbar:

- Minimalmodell mit relaxierendem Memory;
- sichtbarer Prozess nichtmarkovsch, augmentierter Zustand markovsch;
- interne Speicherskala `alpha^{-1}` in der normierten Konvention;
- Knoten als metastabile Kandidaten;
- Relaxationsraten nur als Stabilitaets- oder mass-like proxies.

Noch nicht tragbar:

- robuste Knotenexistenz aus einem einzelnen Baseline-Long-Run;
- physikalische Masse;
- starke Dimensions- oder Raumzeitclaims.

Der erste Baseline-Long-Run mit `n=10^7` zeigt ein starkes Residence-Signal,
aber Paper-I-Evidenz braucht jetzt `eta_zero`, `single_scale`, Seeds und
Sensitivitaeten.

## Paper II: Propagation and Spacetime Kinematics

Status: Folgeprogramm.

Nur als Future Work formulieren:

- effektive Dimension;
- Zwei-Knoten-Propagation;
- `c_eff` und Antwortkegel;
- Lorentz-artige Kinematik.

Kritische Bedingung: exponentielles Memory allein erzeugt keine harte kausale
Schranke, solange direkte Fernkopplung ueber `K` moeglich ist.

## Paper III: Quantum / Standard-Model Programme

Status: geparkt.

Erst wieder anfassen, wenn metastabile Regime, Relaxationsskalen,
Mehrknoten-Wechselwirkungen und Propagation reproduzierbar sind.

## Claim-Register

| Claim | Aktueller Status | Naechste Haertung |
| --- | --- | --- |
| Sichtbarer Prozess ist nichtmarkovsch | strukturell gut | in Paper 0/I konsistent halten |
| Augmentierter Zustand ist markovsch | strukturell gut | Markov-Kern/Operator sauber zitieren |
| Memory-Faser kontrahiert pfadweise | beweisbar | Normannahmen klar nennen |
| Knoten als metastabile Regime | Definition/Diagnostik | Long-Run-Kontrollen und Seeds |
| Baseline `n=10^7` zeigt langlebige Residence | numerische Beobachtung | `eta_zero`, `single_scale`, weitere Seeds |
| `D_occ ~ 2.8` im Archiv | numerische Beobachtung | Seed- und Fitfenster-Reproduktion |
| Eindeutige `d=3`-Selektion | conjecture/offen | nicht behaupten |
| Endliche Propagation | conjecture/offen | lokale Kopplung und Response-Tests |
| Lorentz-Kinematik | conjecture/offen | erst nach Propagation |
| Relaxationsrate als Masse | conjecture/offen | nur mass-like proxy sagen |
| Standardmodellbezug | spekulativ | Paper III, spaeter |

## Paper-taugliche Sprachregel

- `We define` fuer Modellannahmen und Diagnostiken.
- `We prove` fuer direkte Strukturresultate.
- `We observe numerically` fuer reproduzierbare Simulationsergebnisse.
- `We conjecture` fuer Weltmodell-, Lorentz-, Quanten- oder
  Standardmodell-Bruecken.
