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

Der v0.5-Kontrollstand zeigt: Memory-Gradient-Feedback trennt sich deutlich
von `eta_zero`, `m0_zero` und `alpha_one` in Residence, Kompaktheit und
Memory-Cloud-Form. `single_scale` bleibt aber ebenfalls kompakt und langlebig.
Paper-I-Evidenz darf daher derzeit nur vorsichtig als
self-interaction-induced confinement formuliert werden, nicht als spezifisch
zweiskaliger Knotenmechanismus.

Die Kernel-Shape-Probe praezisiert die Ablationssprache: `A_att=0` entfernt
in der aktuellen Update-Konvention den breiten Gegenanteil, zerstoert aber
nicht die lokale Restaurierung. `A_rep=0` ist die haertere Dispersionskontrolle.
Der `matched_deposition`-Pilot zeigt ausserdem: normiertes Schreib-/Lese-
Matching bleibt zwar confined relativ zu `eta_zero`, ist ohne
Steifigkeitsrenormierung aber breiter als die Delta-Baseline.
Der neue `zero_mean_two_scale`-Track testet zusaetzlich, ob ein kompensierter
Kernel mit `int K=0` die Zweiskaligkeit sauberer isoliert. Die 100k-Piloten bei
`sigma_att/sigma_rep in {1.5,2,3}` isolieren diesen Mechanismus noch nicht; die
aktiven Bedingungen sind praktisch deckungsgleich. Der `rep_zero`-Pilot bei
`q=3` zeigt zugleich, dass die historischen Labels nicht literal gelesen werden
duerfen: `A_rep` ist in der aktuellen Update-Konvention der lokale
Confinement-Kanal, `A_att` ein breiter Gegenkanal.

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
| Knoten als metastabile Regime | numerisch gestuetzt gegen `eta_zero`, `m0_zero`, `alpha_one`; nicht kernel-spezifisch | v0.5 beibehalten, Kraftkomponenten/Vorzeichen messen, dann AR-/Transfermoden testen |
| Baseline/Single-scale zeigen langlebige Residence | robust gegen harte Negativkontrollen, aber Mechanismus nicht isoliert | Paper-I-Sprache auf Feedback-Confinement begrenzen |
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
