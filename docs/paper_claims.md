# Paper-Claims und Status

Stand: 2026-07-09.

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

Der bisherige v0.5-Kontrollstand ist nach dem Vorzeichenfund nur noch
`legacy-sign`-Evidenz. Nach der Korrektur des Kernelgradienten muss Paper-I-
Evidenz neu aufgebaut werden: zuerst korrigierte Kurz-Kontrollen, dann
Amplitudenhierarchie, dann erst Knotenscore und Modentests.

Die Kernel-Shape-Probe und der Force-Komponenten-Pilot identifizierten den
Vorzeichenfehler. Korrigiert wurde der Gradient: `A_rep` ist jetzt lokal
repulsiv, `A_att` breit attraktiv im Potentialmodell.
Matched-, Zero-Mean-, Scale-Ratio- und Rep-Zero-Piloten vor diesem Report
bleiben als Diagnose der alten Implementierung nuetzlich. Fuer Paper I muessen
sie unter korrigierter Sign-Konvention neu gerechnet werden, bevor daraus ein
Confinement- oder Mechanismusclaim abgeleitet wird.

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
| Knoten als metastabile Regime | nach Sign-Korrektur neu zu testen | korrigierte Kontrollen, Amplitudenhierarchie, dann AR-/Transfermoden |
| Baseline/Single-scale zeigen langlebige Residence | nur `legacy-sign`-Befund | mit korrigiertem Kernel neu rechnen |
| `D_occ ~ 2.8` im Archiv | numerische Beobachtung | Seed- und Fitfenster-Reproduktion |
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
