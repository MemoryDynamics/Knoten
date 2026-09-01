# P5-D-Protokoll: deterministische gegenseitige Centerantwort zweier Schleifen

Datum: 2026-09-01

Status: **prospektiv eingefroren vor Implementierung und vor jeder
registrierten P5-D-Trajektorie**.

Dieser Freeze autorisiert nur die nachgelagerte Implementierung mit
synthetischen und statischen Preflight-Tests. Der registrierte Targetpfad
bleibt bis zu einem separaten Implementierungsreadinessreview gesperrt.

### Preimplementation-Korrektur der Phasenabbildung

Beim ersten algebraischen Implementierungsreview, vor dem ersten Codecommit
und vor jeder P5-D-Trajektorie, wurde ein Closure-Fehler in der urspruenglich
notierten halbierten Phase gefunden. Das Panel
`phi_A=phi_m/2`, `phi_B=-phi_m/2` ist mit acht `phi_m`-Knoten nicht unter
Reflexion geschlossen, weil die Halbwinkel effektiv einen $4\pi$-Index
benoetigen.

Das Protokoll wird deshalb prospektiv und ohne Zielzugriff auf die unten
verwendete direkte Abbildung

$$
\phi_A=\phi_m,\qquad\phi_B=-\phi_m
$$

korrigiert. Distanzen, Staerken, Schwellen, Armzahl und Serialisierungsordnung
bleiben unveraendert. Das korrigierte Acht-Knoten-Panel enthaelt vier
verschiedene Relativphasen und deren Halbdrehungs-Mates. Reflexion und der
wegen der festen Centerpositionen verwendete Swap-plus-Halbdrehung schliessen
nun innerhalb desselben Panels. Der Korrekturcommit und sein CI muessen wie
der urspruengliche Freeze vor dem Implementierungscommit liegen.

## 1. Registrierte Frage und Claim-Grenze

Die einzige primaere Frage lautet:

> Tragen zwei getrennt fortgeschriebene, vorbereitete Anchor-Schleifen die im
> Designaudit deklarierte lineare notched-Center-/adjungierte Write-Kopplung
> als schleifenerhaltenden, reziproken Closed-loop-Port mit vollstaendigem
> finite-$H$-Paarledger und einer aufgeloesten Abweichung von der Summe der
> beiden getrennten Einwegantworten?

Das Protokoll testet eine **explizit eingefuegte** Paararchitektur. Selbst ein
Vollpass waere kein Nachweis, dass die ungekoppelten Paper-I-Gleichungen diese
Wechselwirkung spontan erzeugen. Nicht freigeschaltet werden Ladung,
universelles Kraftgesetz, Reichweite, materieller Impuls, interner Spin,
Traegheit oder Masse.

## 2. Freeze-Basis und Provenienz

Der verpflichtende Design-Freeze ist

```text
commit f68c8f89f4d62fcfc7f440d78e4e2a6011ce6344
blob   0f02d86bcbfacd2154d21df4a40f853174085d0b
path   reports/project/meta/reviews/
       scalar_memory_loop_p5d_mutual_center_design_audit_2026-09-01.md
```

Sein CI-Lauf
[33507408346](https://github.com/MemoryDynamics/Knoten/actions/runs/33507408346)
ist erfolgreich. Der vorgelagerte Main-Stand ist
`b91d258056bc6e99426ab38aefdb1968b6bd7457`; der N0-Status bleibt
`n0-noise-stability-window-bracketed-reviewed-pass`.

Die Implementierung muss beim spaeteren Targetlauf mindestens die folgenden
Design-Eingangsblobs exakt pruefen:

| Objekt | Git-Blob am Design-Freeze |
| --- | --- |
| Designaudit | `0f02d86bcbfacd2154d21df4a40f853174085d0b` |
| `src/emergenz_knoten/orbit_center_actuator.py` | `63d31bc47291f76c65a5633f14436ccd2105fe9a` |
| `src/emergenz_knoten/rotating_wave_stability.py` | `9defb5a6876371202e1ba57cea030c997b9c6edd` |
| `src/emergenz_knoten/rotating_wave_stability_gate.py` | `630beb9952abefea823d91388dcbb2de8f1a2927` |
| `src/emergenz_knoten/rotating_wave_formation.py` | `38f16f11a790a64470bab3a34505825cf815e7f0` |
| P4-R-S Ergebnis-JSON | `e4eae06ada6860455e49a08691235b9f6e818f51` |
| P4-R-S Ergebnisreview | `4d3297c2bfb0fd191bd73e8e9cad7f7d85a86b87` |
| N0 Ergebnis-JSON | `0bcf489068fc0c7004f0c65b973f7be49dfe1621` |
| N0 Ergebnisreview | `5f5e374aa554eb795172110c2ddccb32dcb48de0` |
| P4 Source-Referee-Audit | `273acc3a86a9f3757e853236ce386f064835194c` |

Der spaetere Runner muss zusaetzlich den Protokollcommit, den Protokollblob,
alle Implementierungsblobs, einen sauberen gepushten Stand und die exakte
Upstream-Synchronisation speichern. Ein Targetlauf aus einem Dirty Worktree,
vor dem Protokollcommit oder mit abweichenden Eingangsblobs muss vor dem
Erzeugen eines Paarzustands abbrechen.

## 3. Eingefrorener Einzel-Loop-Zustand

Beide Rollen A und B verwenden getrennte Arrays desselben bereits
zugelassenen Anchor-Kandidaten:

| Groesse | Wert |
| --- | --- |
| candidate id | `k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1` |
| $\alpha$ | `0.01` |
| $q=1-\alpha$ | `0.99` |
| $H$ | `1200` |
| $\alpha H$ | `12` |
| $\eta$ | `0.15` |
| $\eta/\alpha$ | `15` |
| memory mass | `1` |
| $\sigma_{\rm rep},\sigma_{\rm att}$ | `1, 3` |
| $A_{\rm rep},A_{\rm att}$ | `1, 3.5` |
| $R$ | `0.946517504804223960990626662735384935160072399313332184824852189820406142783597632634323623097735558253263801` |
| $\theta$ | `0.0157703817171349919012689641413413231316321140980062507765923663663284306507309780740587352166842324150748019` |
| $G=|a_{s,0}|^2$ | `0.4020914043226352` |
| $\mu=\alpha G$ | `0.004020914043226352` |

`R` und `theta` muessen aus den gespeicherten Dezimalstrings nach binary64
geparst werden. Der Readout wird fuer jede Chiralitaet aus $q,H,\theta$ und
den normierten finite-$H$-Gewichten neu konstruiert. Der gespeicherte
$G$-Wert ist eine exakte Preflight-Erwartung, kein Laufparameter.

Die beiden Ausgangshistorien werden mit der bestehenden
`target_history(candidate, chirality=s)`-Konstruktion erzeugt, getrennt
rotiert und anschliessend slotweise um ihre jeweiligen Centerpositionen
verschoben. A und B duerfen kein Array teilen.

## 4. Phasen- und Chiralitaetspanel

Die acht registrierten Winkel sind

$$
\phi_m={(2m+1)\pi\over8},\qquad m=0,\ldots,7.
$$

Fuer jede Zelle gilt

$$
\phi_A=\phi_m,\qquad
\phi_B=-\phi_m.
$$

Damit bilden die relativen Phasen $2\phi_m$ vier verschiedene
odd-quarter-turn-Knoten. Die jeweils um $\pi$ verschobenen History-Paare sind
Halbdrehungs-Mates. Reflexion an der reellen Achse bildet
$m\mapsto7-m$ und $(s_A,s_B)\mapsto(-s_A,-s_B)$ ab. Weil A im Standardpanel
immer links und B immer rechts startet, wird der A/B-Swap mit einer
anschliessenden Halbdrehung verglichen; diese Abbildung ist

$$
m\mapsto(3-m)\bmod8,
\qquad(s_A,s_B)\mapsto(s_B,s_A).
$$

Beide Abbildungen bleiben im Panel. Die Chiralitaetspaare werden in dieser
Reihenfolge serialisiert:

```text
(+1,+1), (+1,-1), (-1,+1), (-1,-1)
```

Die acht Winkel enthalten vier verschiedene Relativphasen und vier
Halbdrehungs-Mates. Zusammen mit den vier Chiralitaetspaaren sind sie
algebraische Kontrollen, keine 32 Replikationen. Es wird kein kontinuierliches
Phasenintegral behauptet.

## 5. Distanzen und Initialisierung

Die beiden initialen notched Center liegen auf der reellen Achse bei

$$
C_A(0)=-{d\over2},\qquad C_B(0)=+{d\over2}.
$$

Die registrierten Distanzen sind

| $d/R$ | $d$ | $d/2$ |
| ---: | ---: | ---: |
| `3` | `2.839552514412671882971879988206154805480217197939996554474556569461218428350792897902970869293206674759791403` | `1.4197762572063359414859399941030774027401085989699982772372782847306092141753964489514854346466033373798957015` |
| `6` | `5.679105028825343765943759976412309610960434395879993108949113138922436856701585795805941738586413349519582806` | `2.839552514412671882971879988206154805480217197939996554474556569461218428350792897902970869293206674759791403` |

Im Runner werden die Center aus den tatsaechlich gerundeten verschobenen
Historien erneut gemessen. Die Updategleichung darf weder $d$ noch einen
anderen Anfangsabstand als Sollwert verwenden.

Die harte Kollisions-/Ueberlappungsgrenze ist

$$
|C_A-C_B|\ge2.25R
$$

zu jedem gespeicherten und jedem intern geprueften Schritt. Ihr Unterschreiten
stoppt den betreffenden Arm und klassifiziert das Panel als
`p5d-loop-integrity-fail`; es autorisiert keine Staerkereduktion nach dem
Target.

## 6. Kopplungsstaerken und targetfreie Referenz

Die zwei registrierten Betraege sind

```text
kappa_low  = 0.000625
kappa_high = 0.00125
```

und beide Vorzeichen werden ausgefuehrt:

$$
\lambda=\varsigma\kappa,qquad \varsigma\in\{+1,-1\}.
$$

Diese Werte wurden vor Implementierung aus der bereits bekannten
Anchor-Newest-slot-Mobilitaet gewaehlt. Fuer einen reinen Center-only-
Midpoint-Schritt mit konstantem nativen Center lauten die exakten Faktoren

$$
q_{\rm rec}={1-\lambda\mu\over1+\lambda\mu},
\qquad
q_{\rm one}={1-\lambda\mu/2\over1+\lambda\mu/2}.
$$

Nach $N=2000$ Updates ergeben sich targetfrei:

| $\kappa$ | Vorzeichen | $q_{\rm rec}^N$ | $q_{\rm one}^N$ | vorzeichenbereinigter rec. Response | vorzeichenbereinigter Einwegresponse | $\mathcal X/d$ |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.000625` | `+` | `0.9899980702398411` | `0.9949864673651882` | `0.01000192976015895` | `0.005013532634811779` | `0.00002513550946461011` |
| `0.000625` | `-` | `1.010102979046955` | `1.005038794796966` | `0.01010297904695495` | `0.00503879479696649` | `0.00002538945302196829` |
| `0.00125` | `+` | `0.9800961790784848` | `0.9899980702398411` | `0.01990382092151518` | `0.01000192976015895` | `0.0001000385988027095` |
| `0.00125` | `-` | `1.020308028279663` | `1.010102979046955` | `0.02030802827966266` | `0.01010297904695495` | `0.0001020701857527602` |

Fuer das positive Vorzeichen ist das targetfreie Verhaeltnis

```text
X_low / X_high = 0.2512581120231498
```

Diese Tabelle ist eine Preflight- und Skalierungsreferenz, keine
vorweggenommene P5-Trajektorie. Die volle nichtlineare FIFO-Schleife darf von
den Center-only-Amplituden abweichen. Die Referenz legt jedoch Signalordnung,
Vorzeichen, Staerkestufe und die erwartete quadratische Closed-loop-Skalierung
fest.

## 7. Zeitgitter

Alle Arme verwenden exakt:

| Groesse | Wert |
| --- | ---: |
| aktive Updates | `2000` |
| End-Memory-Zeit $\alpha N$ | `20` |
| interner Gate-Stride | `1` |
| gespeicherter Trace-Stride | `20` |
| gespeicherte $\Delta\tau$ | `0.2` |
| gespeicherte Samples einschliesslich Null | `101` |
| Late-window-Start | Update `1800`, $\tau=18$ |
| Phase-window-Start | Update `1500`, $\tau=15$ |
| 80-digit-Referenzschritte | `1, 1000, 2000` |

Ledger-, Finitheits-, Kollisions-, D0- und Schleifenerhaltgates werden in
jedem Update geprueft; der groebere Speicherstride reduziert nur die
Ergebnisgroesse.

## 8. Paarupdates

Fuer beide Rollen wird zuerst der unveraenderte native nichtlineare
FIFO-Schritt berechnet. Mit $d=C_A-C_B$ und
$\widetilde d=\widetilde C_A-\widetilde C_B$ gelten danach exakt die im
Designaudit hergeleiteten Stufen.

### 8.1 Beide Kanaele aus

Beide vorlaeufigen Historien werden unveraendert uebernommen. Keine Kraft und
keine Write-Inkremente duerfen berechnet oder addiert werden. Die Histories
muessen bitweise mit zwei separat ausgefuehrten nativen Referenzen
uebereinstimmen.

### 8.2 Nur A auf B

$$
F_B={\lambda(d+\widetilde d)\over2+\lambda\mu_B},
\qquad F_A=0.
$$

Nur $h_{B,0}$ erhaelt $\alpha a_{B,0}^*F_B$. A bleibt bitweise nativ.

### 8.3 Nur B auf A

$$
F_A=-{\lambda(d+\widetilde d)\over2+\lambda\mu_A},
\qquad F_B=0.
$$

Nur $h_{A,0}$ erhaelt $\alpha a_{A,0}^*F_A$. B bleibt bitweise nativ.

### 8.4 Reziprok

$$
F_A=-F_B=-{\lambda(d+\widetilde d)\over
2+\lambda(\mu_A+\mu_B)}.
$$

Beide Newest slots erhalten den jeweiligen adjungierten Write. Eine
sequentielle Auswertung, bei der der zweite Force den bereits geschriebenen
ersten Zustand sieht, ist verboten; beide Writes muessen aus demselben
Pre-write-Paarzustand folgen.

Kein Arm darf Geschwindigkeit, zweite Differenz, Impuls, Sollphase,
co-rotating Target oder fitted transfer tensor verwenden.

## 9. Serialisierte Kontrollmatrix

Die Basisschluessel werden geordnet nach

```text
distance_fraction: 3, 6
phase_index:        0, 1, 2, 3, 4, 5, 6, 7
chirality_pair:     (++), (+-), (-+), (--)
```

erzeugt. Das sind `64` Basiskonfigurationen.

Zuerst werden `64` Doppel-Channel-off-Arme gespeichert. Danach folgen fuer
jeden Basisschluessel in der Reihenfolge

```text
kappa:     low, high
sign:      +1, -1
direction: A_to_B, B_to_A, reciprocal
```

genau `12` aktive Paararme. Damit umfasst die registrierte Matrix

```text
64 channel-off pair arms
768 active pair arms
832 total pair arms
```

Kein Schluessel darf wegen Laufzeit, Shape, Signalstaerke oder Ergebnis
entfernt werden. Ein frueh gestoppter Arm bleibt mit Stopgrund und letzter
gueltiger Stufe im internen Transaktionsobjekt, aber der Runner darf kein
partielles Standardergebnis veroeffentlichen.

Die 80-digit-Replays werden fuer alle `64` reziproken
`kappa_high`, `sign=+1`-Arme an den drei registrierten Schritten erzeugt,
also fuer `192` Checkpoints. Sie evaluieren gespeicherte Pre-step-Zustaende
und Koeffizienten neu; sie sind keine unabhaengigen Trajektorien.

## 10. Lokale Metrologie und Workledger

Fuer jeden aktiven Write werden lokal gespeichert:

- Force, Write-Force und History-Inkrement;
- Center vor, nach nativem Schritt und nach Write;
- raw memory center vor und nach dem Schritt;
- lokale Center-/Write-Identitaet;
- binary64 full-dot-Huelle mit dem jeweiligen $\gamma_{8H}$;
- Newest-slot-Mobilitaetsdissipation;
- Write- und vollstaendige Age-Arbeit.

Fuer den reziproken Arm gelten primaer

$$
F_A+F_B=0,
$$

$$
F_A+{\lambda\over2}(d+d')=0,
$$

$$
W_i^{\rm write}+W_i^{\rm age}-W_i^C=0
\quad(i=A,B),
$$

$$
U_\lambda'-U_\lambda
+W_A^{\rm write}+W_A^{\rm age}
+W_B^{\rm write}+W_B^{\rm age}=0.
$$

Mit $U_0=|\lambda|d^2/2$ sind die eingefrorenen Grenzen:

| Gate | Grenze |
| --- | ---: |
| lokaler Center-/Write-Rest relativ zur ersten vorgeschriebenen Centerbewegung | `5e-12` |
| full-dot-Rest / berechnete Huelle | `1` |
| Kraftbilanz relativ zur ersten Kraft | `5e-12` |
| Midpoint-Kraftrest relativ zur ersten Kraft | `5e-12` |
| per-step Write-/Age-Split relativ $U_0$ | `5e-11` |
| per-step Paarledger relativ $U_0$ | `5e-11` |
| kumulativer Split relativ $U_0$ | `5e-9` |
| kumulativer Paarledger relativ $U_0$ | `5e-9` |
| minimale Mobilitaetsdissipation | `-1e-30` |

Der negative Wert ist nur eine Rundungstoleranz; eine klar negative
Mobilitaetsdissipation ist ein Fail.

Die Einwegledger enthalten den ausgelassenen Gegenport explizit als
Reservoirterm. Sie duerfen nicht gegen den reziproken Nullrest getestet
werden.

Die folgenden Recompute-Rivalen sind verpflichtend:

1. Age A ausgelassen;
2. Age B ausgelassen;
3. beide Age-Terme ausgelassen;
4. raw Center statt notched Center;
5. Einwegarm ohne Reservoirterm als angeblich geschlossenes Paar;
6. Forcezeichen genau eines reziproken Loops gekippt.

Mindestens die strukturellen Korruptionsfixtures muessen die jeweils
vorgesehene Gatefamilie sicher ausloesen. Ein realer Rivale, dessen Rest im
Targetpanel numerisch unaufgeloest bleibt, wird als solcher berichtet und
darf den primaeren Ledger nicht bestaetigen.

## 11. Schleifen- und Channel-off-Gates

Fuer beide Loops getrennt gelten:

| Gate | Grenze |
| --- | ---: |
| Channel-off bitwise native | exakt |
| Channel-off $D_0/R$ | `1e-10` |
| Channel-off $|C-Z|/R$ | `1e-10` |
| aktives maximales own-chirality $D_0/R$ | `0.01` |
| aktives spaetes own-chirality $D_0/R$ | `0.002` |
| aktives spaetes opposite-chirality $D_0/R$ | mindestens `0.5` |
| mittlerer Phaseninkrementfehler / $\theta$ | `0.01` |
| RMS-Phaseninkrementfehler / $\theta$ | `0.05` |
| minimaler Paarcenterabstand | `2.25 R` |
| maximale einzelne Centerantwort / initialer Abstand | `0.10` |

Jeder Arm muss 2000 finite Updates vollstaendig erreichen. Shapezerstoerung,
Chiralitaetsverlust oder Kollision ist ein P5-D-Fail, nicht ein
Interaktionssignal.

## 12. Responsekonstruktion

Fuer jeden aktiven Arm wird der gematchte Doppel-Channel-off-Trace mit
demselben Distanz-, Phasen- und Chiralitaetsschluessel subtrahiert:

$$
D^X=C_A^X-C_B^X,
\qquad \delta D^X=D^X-D^{\rm off}.
$$

Mit der initialen Einheitsachse

$$
e_0={D^{\rm off}(0)\over|D^{\rm off}(0)|}
$$

ist der vorzeichenbereinigte longitudinale Response

$$
L_X=-\operatorname{sgn}(\lambda)
{\operatorname{Re}(\delta D^X\overline e_0)\over d}.
$$

Der transversale Response ist

$$
T_X={\operatorname{Im}(\delta D^X\overline e_0)\over d}.
$$

Fuer Einweg-Kausalitaet werden ausserdem die beiden einzelnen
baseline-subtrahierten Centertraces gespeichert. Im $A\to B$-Arm muss A
bitweise Channel-off bleiben; im $B\to A$-Arm muss B bitweise Channel-off
bleiben.

Der additive Rivale und Closed-loop-Ueberschuss sind

$$
\delta D^{\rm add}
=\delta D^{A\to B}+\delta D^{B\to A},
$$

$$
\mathcal X
=\delta D^{\rm rec}-\delta D^{\rm add},
\qquad
X_L={\operatorname{Re}(\mathcal X\overline e_0)\over d}.
$$

Alle finalen Klassifikatoren werden zusaetzlich als Late-window-Mittel und
RMS ueber $\tau\ge18$ gespeichert. Ein einzelner finaler Sample darf keinen
anderen fehlgeschlagenen Trace-Gate retten.

## 13. Registrierte Response- und Skalierungsgates

Nach Paarung der simultanen Reflexions-/Chiralitaetsarme gelten fuer jede
Distanz und jedes Kopplungsvorzeichen:

| Gate | Grenze |
| --- | ---: |
| finaler reziproker $L$ bei `kappa_low` | mindestens `0.0025` |
| finaler reziproker $L$ bei `kappa_high` | mindestens `0.005` |
| finaler Einweg-$L$ je Richtung bei `kappa_low` | mindestens `0.00125` |
| finaler Einweg-$L$ je Richtung bei `kappa_high` | mindestens `0.0025` |
| positive Phasensupport-Knoten | mindestens `6/8` je Chiralitaetspaar |
| low/high-Verhaeltnis von reziprokem und Einweg-$L$ | `0.35..0.65` |
| sign-even/sign-odd-RMS der primaeren Response | hoechstens `0.05` |
| normalisierte Responseabweichung zwischen `d/R=3` und `6` | hoechstens `10%` |
| rohe grosse/kleine Distanzantwort | `1.8..2.2` |
| Swap-Trace-RMS / $R$ | hoechstens `1e-11` |
| Reflexions-Trace-RMS / $R$ | hoechstens `1e-11` |

Der Response muss in beiden Einwegrichtungen und im reziproken Arm
aufgeloest sein. Ein richtiges Abstandsvorzeichen bei fehlender
Einwegkausalitaet reicht nicht.

Fuer den Closed-loop-Ueberschuss gelten nach demselben Pairing:

| Gate | Grenze |
| --- | ---: |
| $X_L$ bei `kappa_low` | mindestens `2e-6` |
| $X_L$ bei `kappa_high` | mindestens `1e-5` |
| positiver $X_L$-Phasensupport | mindestens `6/8` je Chiralitaetspaar |
| $X_{L,\rm low}/X_{L,\rm high}$ | `0.10..0.40` |
| $X_L/L_{\rm rec}$ | `5e-4..0.02` |
| normalisiertes $X_L$ zwischen beiden Distanzen | hoechstens `20%` Abweichung |

Die Center-only-Referenz `0.2512581120` liegt innerhalb des registrierten
Staerkekorridors. Die breiteren Grenzen erlauben finite-memory Transienten,
ohne einen exakt additiven oder gross nichtlinearen Befund als Closed-loop-
Pass zu etikettieren.

Transversale Response wird vollstaendig gespeichert und auf Swap,
Reflexion, Vorzeichen und Chiralitaetspairing geprueft. Ein transversaler
Kreiseffekt, Phasenlock oder Paarorbit ist weder notwendig noch hinreichend
fuer den P5-D-Pass.

## 14. Entscheidungsordnung

Die Entscheidung wird genau in dieser Reihenfolge getroffen:

1. falsche Provenienz, Dirty/ungepushter Stand, abweichender Blob,
   unvollstaendiges Panel, nichtfinite Zahl, fehlender Trace oder
   unaufgeloeste primaere Antwort:
   **`p5d-inconclusive`**;
2. lokale Port-, full-dot-, Midpoint-, Gegenkraft-, Split-, Paarledger- oder
   Mobilitaetsverletzung:
   **`p5d-ledger-or-reciprocity-fail`**;
3. Channel-off-, D0-, Radius-, Phase-, Chiralitaets-, Kollisions-,
   Einzelresponse- oder Schleifenerhaltverletzung:
   **`p5d-loop-integrity-fail`**;
4. Source-History im Einwegarm nicht bitweise nativ, fehlende Zielantwort
   oder vertauschte Einwegrichtung:
   **`p5d-directional-causality-fail`**;
5. falsches Kopplungsvorzeichen, Swap-/Reflexionsfail oder aufgeloeste
   gegenseitige Antwort in der falschen Richtung:
   **`p5d-mutual-hypothesis-fail`**;
6. $X_L$ bei einer Staerke unaufgeloest, nicht positiv oder mit dem exakt
   additiven Rivalen kompatibel:
   **`p5d-independent-superposition`**;
7. alle lokalen und kausalen Gates bestehen, aber ein Staerke-, Distanz-,
   Phase-, Ratio- oder Closed-loop-Korridor wird verfehlt:
   **`p5d-inconclusive`**;
8. nur wenn jede vorherige Gatefamilie und jeder Response-/Skalierungsgate
   besteht:
   **`p5d-mutual-center-response-pass`**.

Eine fruehere Entscheidung in dieser Liste kann nicht durch einen spaeteren
Plot oder Gesamtmittelwert gerettet werden.

## 15. Verbotene Anpassungen und Stopregeln

Nach diesem Protokoll-Freeze sind verboten:

- Aendern oder Entfernen von Distanz, Phase, Chiralitaet, Staerke,
  Vorzeichen oder Richtung;
- Verwenden einer P5-Vorschau zur Wahl von Signal- oder Ledgergrenzen;
- Ersetzen des notched Centers durch einen besser reagierenden Readout;
- nachtraegliches Staerken der Kopplung bei unaufgeloestem $\mathcal X$;
- Einfuehren einer Sollphase, eines Sollabstands, einer Zielbahn oder eines
  co-rotating Controllers;
- Einfuehren von Impuls, Geschwindigkeit, zweiter Differenz oder Masse in den
  Pair-step;
- Umdeuten von `inconclusive` oder `independent-superposition` als Pass;
- Zaehlung der 832 Symmetrie-/Kontrollarme als Replikationen;
- noisige P5-C- oder P5-I-Arme vor einem reviewed P5-D-Ergebnis.

Bei nichtfiniten Daten, Kollisionsgrenze, Shape-/Chiralitaetsverlust oder
fehlgeschlagenem Ledger wird der Arm intern gestoppt. Das Standardresultat
wird nur atomar geschrieben, wenn das gesamte registrierte Panel als
vollstaendiges Entscheidungsobjekt vorliegt; andernfalls endet der Runner mit
Fehler und ohne partielle Standardartefakte.

## 16. Implementierung und synthetische Falsifikatoren

Die vorgesehenen spaeteren Pfade sind:

```text
src/emergenz_knoten/mutual_center_coupling.py
experiments/current/dynamics/rotation/
    scalar_memory_loop_p5d_mutual_center_gate.py
experiments/current/dynamics/rotation/
    scalar_memory_loop_p5d_mutual_center_result_audit.py
tests/test_mutual_center_coupling.py
tests/test_rotating_wave_p5d_mutual_center.py
tests/test_rotating_wave_p5d_result_audit.py
```

Vor Targetzugriff muessen synthetische oder statische Tests mindestens
nachweisen:

1. exakte Loesung der reziproken und beiden Einweg-Midpoint-Gleichungen;
2. Translation, Rotation, Reflexion und A/B-Swap;
3. exakte Channel-off-Nativitaet;
4. Source-Bitgleichheit in beiden Einwegarmen;
5. geschlossenen Paarledger fuer synthetische finite Histories;
6. Fail bei vertauschtem Gegenkraftzeichen;
7. Fail bei ausgelassenem A- oder B-Age-Term;
8. Fail beim raw-Center-Rivalen;
9. Fail, wenn der reziproke Trace durch die Einwegsumme ersetzt wird;
10. Fail bei unvollstaendiger Kontrollmatrix;
11. Entscheidungspraezedenz fuer jeden registrierten Zweig;
12. dass normale Tests und Imports den Targetrunner nicht aufrufen.

Der Ergebnis-Auditor darf keine Entscheidungshelper des Runners importieren.
Er muss aus dem gespeicherten JSON Panelordnung, lokale Gates,
Paarledger, Symmetrien, Einwegkausalitaet, Response, Distanz-, Staerke- und
Closed-loop-Entscheidung eigenstaendig rekonstruieren.

## 17. Ergebnisartefakte und Einmaligkeit

Die spaeteren Standardpfade sind:

```text
reports/dynamics/rotation/
    scalar_memory_loop_p5d_mutual_center_2026-09-01.json
reports/dynamics/rotation/
    scalar_memory_loop_p5d_mutual_center_2026-09-01.md
```

Der Targetrunner muss das Ueberschreiben existierender Standardartefakte
verweigern. JSON und Markdown werden in temporaere Dateien geschrieben,
vollstaendig validiert und erst dann atomar an beide Standardpfade
verschoben. Der rohe Ergebniscommit wird vor Auditorcode, Figuren,
Ergebnisreview oder Statuspromotion gepusht.

Ein spaeteres Darstellungsdiagramm darf nur aus dem unveraenderten JSON
erzeugt werden. Es ist kein primaeres Entscheidungsartefakt.

## 18. Erforderliche weitere Freeze-Folge

1. dieses Protokoll separat committen und pushen;
2. Protokollblob und erfolgreichen CI-Lauf festhalten;
3. Implementierung und synthetische Tests ohne Targetzugriff erstellen;
4. Vollsuite, Ruff und strikten MkDocs-Build ausfuehren;
5. Implementierung separat committen und pushen;
6. ein kritisches Readinessreview schreiben, das jeden Falsifikator und die
   Targetversiegelung prueft;
7. Readinessreview committen, pushen und CI abwarten;
8. erst danach einen einzigen sauberen Standardziellauf ausfuehren;
9. Rohresultat unveraendert committen und pushen;
10. unabhaengigen Auditor ausfuehren und das Ergebnis aus Referee-Sicht
    reviewen.

## 19. Engste Pass-Sprache

Ein reviewed `p5d-mutual-center-response-pass` duerfte ausschliesslich so
zusammengefasst werden:

> Im registrierten deterministischen Anchor--Anchor-Panel schliesst die
> explizit deklarierte lineare notched-Center-/adjungierte Write-Kopplung
> ihren gemeinsamen finite-$H$-Ledger, erhaelt beide vorbereiteten Schleifen,
> besteht die getrennten Einweg-, Swap-, Reflexions-, Vorzeichen-, Distanz-
> und Staerkekontrollen und zeigt einen aufgeloesten reziproken Closed-loop-
> Ueberschuss gegenueber der Summe der beiden Einwegantworten.

Diese Sprache bezeichnet eine operational kompatible Mutual-Port-
Architektur. Sie behauptet weder spontane Wechselwirkungsentstehung noch
Ladung, ein universelles Kraftgesetz, konservierten materiellen Impuls,
Spin, Traegheit oder Masse.
