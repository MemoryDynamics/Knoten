# P5-D targetfreier Designaudit: gegenseitiger Center-Port zweier Schleifen

Datum: 2026-09-01

Auditurteil: **`p5d-mutual-center-design-identifiable`**

Freigabe: Ein prospektives P5-D-Protokoll darf geschrieben werden.

Weiterhin gesperrt: Implementierung, registrierte P5-Trajektorie und jeder
Interaktions-, Ladungs-, Spin-, Impuls-, Traegheits- oder Masseclaim.

## 0. Kurzurteil

Eine minimale falsifizierbare Zwei-Schleifen-Frage ist mit dem vorhandenen
P4-R-S-Port formulierbar. Zwei getrennte, vorbereitete Anchor-Historien
werden nicht ueber eine Zielbahn oder einen vorgegebenen Sollabstand
gesteuert. Stattdessen liest jede Schleife ihren momentanen notched Center
aus; die beiden Center liefern eine einzige translations- und
rotationskovariante Paarenergie. Die daraus folgende Gegenkraft wird ueber
den bereits auditierten adjungierten Newest-slot-Port in beide Historien
zurueckgeschrieben.

Der wissenschaftlich diskriminierende Test ist nicht, ob der Abstand unter
einer einprogrammierten attraktiven Kopplung abnimmt. Primaer sind:

1. richtungsgetrennte kausale Einwegantworten bei identischen
   Channel-off-Ausgangszustaenden;
2. exakte Gegenkraft und ein gemeinsamer, beide finite-$H$-Age-Terme
   enthaltender Paarledger;
3. Swap-, Reflexions- und Vorzeichenkontrollen;
4. ein aufgeloester Closed-loop-Kontrast gegen die Summe der beiden
   unabhaengigen Einwegantworten;
5. Erhalt beider vorbereiteten Schleifen.

Damit ist eine lineare Centerkopplung fuer P5-D ausreichend und sogar die
sauberste Nullarchitektur. Ein nichtlinearer Kopplungsterm, ein harmonischer
Phasenlock oder eine zusaetzliche Impulsvariable wuerden die erste
Kausalfrage nur mit neuen Annahmen belasten.

Ein spaeterer Pass wuerde dennoch keine Wechselwirkung aus den ungekoppelten
Grundgleichungen emergieren lassen: Der gegenseitige Port wird explizit
hinzugefuegt. Geprueft wuerde, ob die bereits zugelassenen endlichen
Memory-Schleifen diesen Port als geschlossenes dynamisches Paar tragen.

## 1. Evidenz, Inferenz und Hypothese vor dem Target

- **Evidenz:** P4-R-S traegt denselben expliziten Source-/Write-Antworttyp am
  vorbereiteten L3- und Anchor-Kreis; der Anchor ist lokal
  existenzzertifiziert und hat seinen nativen Stabilitaetstest bestanden.
- **Evidenz:** N0 klammert fuer beide vorbereiteten Zellen ein aufgeloestes
  endliches Rauschfenster ein. P5-D verwendet zunaechst trotzdem exakt
  $\varepsilon=0$, damit Paarantwort und Innovationsantwort nicht vermischt
  werden.
- **Inferenz:** Der notched Center und sein adjungierter Newest-slot-Write
  koennen als zwei Enden eines gegenseitigen diskreten Ports verwendet
  werden, ohne einen neuen mechanischen Zustand einzufuehren.
- **Zu testende Hypothese:** Zwei getrennte Anchor-Schleifen koennen unter
  einer schwachen expliziten Center-Center-Kopplung beide Schleifen erhalten,
  einen vollstaendigen reziproken Paarledger schliessen und eine
  Closed-loop-Antwort erzeugen, die nicht mit dem blossen nachtraeglichen
  Addieren zweier Einwegtraces identisch ist.
- **Nicht aus einem Pass ableitbar:** spontane Kopplungsentstehung, ein
  physisches Kraftgesetz, Reichweite, Ladung, konservierter materieller
  Impuls, interner Spin, Traegheit oder Masse.

## 2. Unveraenderliche Auditbasis

Der Audit baut auf dem gruenen Main-Stand

```text
b91d258056bc6e99426ab38aefdb1968b6bd7457
```

und dem rein redaktionellen Paper-I-Abgrenzungscommit

```text
5be5cb61b950f5c783860bbca7d58825e8de39b1
```

auf. Der CI-Lauf fuer diesen Branch ist
[33506427098](https://github.com/MemoryDynamics/Knoten/actions/runs/33506427098)
und erfolgreich.

Die fuer das spaetere Protokoll relevanten Git-Bloecke am Auditstart sind:

| Objekt | Git-Blob |
| --- | --- |
| `src/emergenz_knoten/orbit_center_actuator.py` | `63d31bc47291f76c65a5633f14436ccd2105fe9a` |
| `src/emergenz_knoten/rotating_wave_stability.py` | `9defb5a6876371202e1ba57cea030c997b9c6edd` |
| `src/emergenz_knoten/rotating_wave_stability_gate.py` | `630beb9952abefea823d91388dcbb2de8f1a2927` |
| `src/emergenz_knoten/rotating_wave_formation.py` | `38f16f11a790a64470bab3a34505825cf815e7f0` |
| P4-R-S Ergebnis-JSON | `e4eae06ada6860455e49a08691235b9f6e818f51` |
| P4-R-S Ergebnisreview | `4d3297c2bfb0fd191bd73e8e9cad7f7d85a86b87` |
| N0 Ergebnis-JSON | `0bcf489068fc0c7004f0c65b973f7be49dfe1621` |
| N0 Ergebnisreview | `5f5e374aa554eb795172110c2ddccb32dcb48de0` |
| P4 Source-Referee-Audit | `273acc3a86a9f3757e853236ce386f064835194c` |

Kein P5-Runner, kein P5-Paarzustand und kein Zielergebnis existiert bei
Abschluss dieses Audits.

## 3. Warum Anchor--Anchor der erste Paarversuch ist

Der primaere P5-D-Versuch verwendet zwei getrennt gespeicherte, verschobene
Kopien des zugelassenen Anchor-Zustands

```text
candidate = k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1
alpha     = 0.01
q         = 0.99
H         = 1200
eta       = 0.15
R         = 0.94651750480422396099...
theta     = 0.01577038171713499190...
```

Beide Arrays werden unabhaengig fortgeschrieben; es wird keine gemeinsame
History und kein gemeinsames Memory-Feld angelegt. Sie sind operationell zwei
Zustaende, aber keine zwei unabhaengig formierten oder statistisch
replizierten Objekte.

Die identische Zelle ist fuer den ersten Kausaltest strenger als ein
Anchor--L3-Mischpaar: gleiche Schrittweite, gleicher Write-Gain und gleiche
Memory-Zeit entfernen eine unnoetige Mobilitaetsasymmetrie. L3--L3 bleibt ein
spaeterer, separat zu registrierender Skalenholdout und darf einen negativen
Anchor--Anchor-Befund nicht retten.

## 4. Lesbarer finite-$H$-Center und Write-Port

Mit $q=1-\alpha$ lauten die normierten endlichen Memory-Gewichte

$$
\bar w_j={\alpha q^j\over1-q^H},\qquad j=0,\ldots,H-1.
$$

Der bisher oft nur symbolisch verwendete Filter ist die endliche geometrische
Reihe

$$
B_H(z)=\sum_{j=0}^{H-1}\bar w_jz^{-j}
={\alpha\,[1-(q/z)^H]\over(1-q^H)(1-q/z)}.
$$

Fuer Chiralitaet $s\in\{-1,+1\}$ setze

$$
\beta_s=B_H(e^{is\theta}),
$$

$$
a_{s,0}={\bar w_0-\beta_s\over1-\beta_s},\qquad
a_{s,j}={\bar w_j\over1-\beta_s}\quad(j\ge1).
$$

Dann ist

$$
C_s(h)=\sum_{j=0}^{H-1}a_{s,j}h_j
$$

der translationskovariante und fuer die vorbereitete Rotationsmode genotchte
Center. Es gelten $\sum_j a_{s,j}=1$ und die entsprechende Notch-Identitaet.
Der rohe finite-memory Center

$$
c_H(h)=\sum_j\bar w_jh_j
$$

bleibt ein registrierter falscher-Center-Rivale.

Eine Centerkraft $F$ wird wie in P4-R-S nur in den neuesten History-Slot
geschrieben:

$$
h'_0=\widetilde h_0+\alpha a_{s,0}^*F,
\qquad G_s=|a_{s,0}|^2>0,
$$

wobei $\widetilde h$ der vollstaendige native nichtlineare FIFO-Schritt ist.
Damit folgt lokal und ohne gefittete Mobilitaet

$$
C_s(h')=C_s(\widetilde h)+\mu_sF,
\qquad \mu_s=\alpha G_s.
$$

Fuer den Anchor ist der bereits gespeicherte statische Wert
$G_s=0.4020914043226352$ fuer beide Chiralitaeten. Das spaetere Protokoll
muss ihn aus $q,H,\theta$ neu aufbauen und gegen diesen Wert pruefen; es darf
ihn nicht als frei zu fittenden Paarparameter behandeln.

## 5. Gewaehlte gegenseitige Architektur

Seien $C_A,C_B$ die beiden notched Center und

$$
d=C_A-C_B.
$$

Die einzige P5-D-Paarenergie ist

$$
U_\lambda(C_A,C_B)={\lambda\over2}|C_A-C_B|^2,
\qquad \lambda=\varsigma\kappa,
$$

mit registriertem Betrag $\kappa>0$ und Vorzeichenkontrolle
$\varsigma\in\{-1,+1\}$. Das positive Vorzeichen programmiert eine
attraktive Centerkopplung, das negative eine endliche repulsive
Richtungskontrolle. Das Vorzeichen wird nicht aus dem Lauf gelernt.

Nach den beiden nativen Schritten seien $\widetilde C_A,\widetilde C_B$ und
$\widetilde d=\widetilde C_A-\widetilde C_B$. Fuer die reziproke
Midpoint-Discrete-gradient-Stufe gilt

$$
F_A=-F_B=F,
$$

$$
F=-{\lambda(d+\widetilde d)\over
2+\lambda(\mu_A+\mu_B)}.
$$

Danach werden $F_A$ und $F_B$ ueber die jeweiligen adjungierten Newest-slot-
Writes eingetragen. Diese geschlossene Formel ist genau aequivalent zu

$$
F=-{\lambda\over2}(d+d'),
$$

wobei $d'=C'_A-C'_B$ der tatsaechliche neue Paarabstand ist.

Die Architektur besitzt damit:

- keine Solltrajektorie;
- keinen Sollabstand und keinen Bindungsradius;
- keine Phasen- oder Chiralitaetsregel im Kraftgesetz;
- keinen separat eingefuehrten Impuls- oder Geschwindigkeitszustand;
- keinen Fit an eine registrierte P5-Antwort;
- exakte Translation, eigentliche Rotation, Reflexion mit
  Chiralitaetswechsel und $A\leftrightarrow B$-Kovarianz.

Die Anfangsdistanz ist nur eine Panelbedingung. Sie erscheint nicht als
Referenzwert in der Updategleichung.

## 6. Einwegablationen

Die Einwegkontrollen verwenden dieselbe momentane Centergeometrie, schreiben
aber absichtlich nur in den Empfaenger.

Fuer $A\to B$ bleibt A exakt im nativen Channel-off-Arm und

$$
F_B={\lambda(d+\widetilde d)\over2+\lambda\mu_B},
\qquad F_A=0\quad\hbox{im Update}.
$$

Fuer $B\to A$ bleibt B nativ und

$$
F_A=-{\lambda(d+\widetilde d)\over2+\lambda\mu_A},
\qquad F_B=0\quad\hbox{im Update}.
$$

Diese Arme sind absichtlich nicht reziprok. Der ausgelassene Gegenport wird
als externes Reservoir bilanziert und darf nicht als geschlossener
Paarledger ausgegeben werden. In jedem Einwegarm muss die Source-History
bitweise mit ihrem gematchten Channel-off-Arm uebereinstimmen. Eine Bewegung
der Source durch den angeblich abgeschalteten Rueckkanal ist ein harter
Richtungsfail.

## 7. Vollstaendiger gegenseitiger Work-/Ledger-Vertrag

Fuer jede Schleife $i\in\{A,B\}$ wird der bereits gepruefte finite-$H$-Split
verwendet:

$$
W_i^{\rm write}
=\left\langle a_{i,0}^*F_i,h'_{i,0}-h_{i,0}\right\rangle,
$$

$$
W_i^{\rm age}
=\left\langle F_i,
\sum_{j=1}^{H-1}a_{i,j}(h_{i,j-1}-h_{i,j})\right\rangle,
$$

$$
W_i^{C}=W_i^{\rm write}+W_i^{\rm age}
=\langle F_i,C'_i-C_i\rangle.
$$

Der primaere Paarledger lautet

$$
\Delta U_\lambda+W_A^{\rm write}+W_A^{\rm age}
+W_B^{\rm write}+W_B^{\rm age}=0
$$

bis zur vorab modellierten binary64-Huelle. Gleichzeitig muessen

$$
F_A+F_B=0
$$

und die beiden lokalen Center-/Write-Identitaeten schliessen. Positive
Newest-slot-Mobilitaetsdissipation bleibt eine Portdiagnose; sie ist kein
physischer Waerme- oder Energiebegriff.

Mindestens folgende Rivalen werden aus denselben gespeicherten Schritten neu
berechnet und muessen den primaeren Ledger nicht bestehen:

1. Age-Arbeit von A ausgelassen;
2. Age-Arbeit von B ausgelassen;
3. beide Age-Terme ausgelassen;
4. $C_i$ durch den rohen Center $c_{H,i}$ ersetzt;
5. ein Einwegarm faelschlich als geschlossener reziproker Paararm bilanziert;
6. ein gespeichertes Kraftvorzeichen in genau einem Loop vertauscht.

Ein Ledgerpass validiert nur den deklarierten diskreten Portvertrag. Weil
$U_\lambda$ und der Write-Port konstruiert sind, ist er kein unabhaengiger
Nachweis physischer Energie oder Impulserhaltung.

## 8. Observablen, die Selbstantwort und Mutualantwort trennen

Fuer jede aktive Paarzelle existiert ein gematchter Doppel-Channel-off-Arm.
Mit

$$
D^X=C_A^X-C_B^X,\qquad
\delta D^X=D^X-D^{\rm off}
$$

fuer $X\in\{A\to B,B\to A,\mathrm{rec}\}$ werden nur
baseline-subtrahierte Antworten klassifiziert. Ein gemeinsamer Drift oder
zwei unabhaengige native Relaxationen verschwinden in dieser Differenz.

Die Einweg-Kausalitaet wird getrennt geprueft:

- im $A\to B$-Arm ist die Source A bitweise nativ und nur B darf eine
  aufgeloeste richtungskorrekte Antwort tragen;
- im $B\to A$-Arm gilt die spiegelbildliche Bedingung;
- die Antwort muss mit dem Kopplungsvorzeichen und unter Swap konsistent
  wechseln.

Der entscheidende Rivale ist die nachtraegliche Summe der unabhaengigen
Einwegantworten

$$
\delta D^{\rm add}
=\delta D^{A\to B}+\delta D^{B\to A}.
$$

Der Closed-loop-Ueberschuss ist

$$
\mathcal X
=\delta D^{\rm rec}-\delta D^{\rm add}.
$$

Bei schwacher linearer Kopplung ist $\mathcal X=O(\kappa^2)$, nicht
$O(\kappa)$. Er darf deshalb nicht durch einen beliebigen grossen
Nichtlinearitaetsfloor erzwungen werden. Das Protokoll muss zwei vorab
gewaehlte Kopplungsbetraege verwenden, eine targetfrei berechnete
Center-only-Midpoint-Referenz einfrieren und verlangen, dass der
longitudinale Anteil von $\mathcal X$ aufgeloest, vorzeichenrichtig und mit
der quadratischen Staerkenskalierung kompatibel ist. Ein exakt additiver oder
unaufgeloester Befund ist ein gueltiger negativer Zweig
`p5d-independent-superposition`, kein nachtraeglicher Anlass fuer staerkere
Kopplung.

Zusaetzlich werden gespeichert:

- longitudinaler und transversaler Paarresponse relativ zur initialen
  Trennachse;
- paarweiser Centerdrift und relative Centerantwort;
- jede einzelne Loop-Translation relativ zum eigenen Channel-off;
- eigener D0-, Radius-, Phasen- und Chiralitaetserhalt;
- linear normierter Distanzkontrast zwischen mindestens zwei vorab
  gewaehlten Separationen;
- odd/even-Anteile unter $\lambda\mapsto-\lambda$;
- komplette zeitaufgeloeste und kumulative Ledgers.

Die absolute Abstandsabnahme allein ist keine primaere P5-Observable.

## 9. Phasen-, Chiralitaets-, Distanz- und Staerkepanel

Der spaetere Protokoll-Freeze muss vor Implementierung festlegen:

1. eine endliche relative Phasenquadratur, die unter Swap und Reflexion
   geschlossen ist;
2. alle vier Chiralitaetspaare $(s_A,s_B)$;
3. mindestens zwei nicht kollidierende initiale Distanzen in Einheiten von
   $R$;
4. exakt zwei schwache positive Kopplungsbetraege fuer den
   $O(\kappa^2)$-Kontrast;
5. beide Vorzeichen $\varsigma$;
6. gemeinsame Memory-Zeit, Speicherstride, Late-window und
   Abbruchdistanz;
7. alle numerischen Huelle-, Signal-, Shape-, Ledger-, Richtungs- und
   Skalierungsschwellen.

Die Werte duerfen aus Anchor-Konstanten, P4-R-S-Margen und der analytischen
Center-only-Referenz bestimmt werden, aber aus keiner P5-Trajektorie. Nach dem
Freeze ist kein Entfernen einer Phase, Chiralitaet, Distanz, Staerke oder
Richtung erlaubt.

Phasenarme, Vorzeichen und Chiralitaeten sind algebraische Kontrollen, keine
unabhaengigen Replikationen. Das primaere Panel bleibt deterministisch.

## 10. N0-Dekomposition

P5 wird in drei getrennte Evidenzstufen zerlegt:

1. **P5-D:** der hier entworfene deterministische Paarversuch mit exakt
   $\varepsilon=0$;
2. **P5-C:** nur nach einem reviewed P5-D-Ergebnis eine gemeinsame
   Innovationsfolge, um Paar- und Common-mode-Anteile zu trennen;
3. **P5-I:** erst danach unabhaengige Innovationen fuer A und B.

N0 autorisiert keine direkte noisy-P5-Suche. Insbesondere ist weder ein
physischer Rauschwert noch ein Wert aus Plancks Konstante ableitbar.

## 11. Vorlaeufige Entscheidungsordnung

Das spaetere Protokoll muss mindestens folgende disjunkte Zweige in dieser
Reihenfolge praezisieren:

1. Provenienz-, Registrierungs-, Vollstaendigkeits-, Endlichkeits- oder
   Aufloesungsfehler: **`p5d-inconclusive`**;
2. lokale Port-, Midpoint-, Gegenkraft- oder gemeinsamer Ledgerfehler:
   **`p5d-ledger-or-reciprocity-fail`**;
3. Channel-off-, D0-, Shape-, Phase-, Chiralitaets-, Kollisions- oder
   Schleifenerhaltfehler: **`p5d-loop-integrity-fail`**;
4. Source-Kontamination im Einwegarm oder falsche kausale Richtung:
   **`p5d-directional-causality-fail`**;
5. aufgeloeste Antwort mit falschem Vorzeichen oder verletzter Swap-/
   Reflexionskovarianz: **`p5d-mutual-hypothesis-fail`**;
6. reziproke Antwort, die mit der unabhaengigen Einwegsumme identisch oder
   deren Closed-loop-Ueberschuss unaufgeloest ist:
   **`p5d-independent-superposition`**;
7. aufgeloeste, richtungskorrekte Paarantwort, aber ein vorab festgelegter
   Distanz-, Staerke- oder Closed-loop-Skalierungskorridor wird verfehlt:
   **`p5d-inconclusive`**;
8. nur wenn alle Konstruktion-, Ledger-, Schleifen-, Kausal-, Symmetrie-,
   Distanz- und Closed-loop-Gates bestehen:
   **`p5d-mutual-center-response-pass`**.

Kein Inconclusive-Zweig darf unter demselben Gate durch Retuning fortgesetzt
werden.

## 12. Adversarielle Falsifikatoren

Die Implementierung muss spaeter synthetisch nachweisen, dass der Pass
verhindert wird durch:

1. vertauschte Gegenkraft in einem Loop;
2. ausgelassenen A- oder B-Age-Term;
3. rohen statt notched Center im Workledger;
4. einen Source-Write im angeblichen Einweg-off-Kanal;
5. Ersetzen der reziproken Trace durch die Summe zweier Einwegtraces;
6. unvollstaendige Phase-, Chiralitaets-, Distanz- oder Staerkepanels;
7. Verletzung der A/B-Swapabbildung;
8. einprogrammierte Sollposition, Sollphase oder Anfangsdistanz im Update;
9. nachtraeglich geaenderte Kopplungsstaerke wegen unaufgeloestem
   Closed-loop-Ueberschuss;
10. Kollision, Schleifenverlust oder nur durch Shapezerstoerung erzeugte
    Centerbewegung.

Tests duerfen dafuer nur synthetische Traces oder Preflight-Zustaende nutzen.
Sie duerfen vor dem Readinessreview keine registrierte P5-Trajektorie
erzeugen.

## 13. Referee-Grenzen der Architektur

### Warum der Test nicht trivial ist

Das Vorzeichen der longitudinalen Kraft wird programmiert. Nicht programmiert
sind der tatsaechliche nichtlineare finite-$H$-Response, der Erhalt beider
Schleifen, die lokale und kumulative Workaufteilung, die Closed-loop-
Abweichung von den getrennten Einwegarmen sowie die Symmetrie- und
Skalierungsfehler. Jeder dieser Punkte kann den Gatezweig unabhaengig
falsifizieren.

### Warum eine lineare Kopplung zulaessig ist

P5-D fragt zuerst nach identifizierbarer gegenseitiger Kausalitaet und
reziproker Closure. Linearitaet ist dafuer kein Defekt. Im Gegenteil:
Nichtlinearitaet, Phasenlocking oder ein gebundener Paarorbit waeren staerkere
und schlechter kontrollierte Zusatzhypothesen. Der $O(\kappa^2)$-
Closed-loop-Kontrast prueft Rueckkopplung, obwohl das momentane Kraftgesetz
linear ist.

### Was selbst ein Pass offen laesst

- Der notched Center und sein Adjungierter sind explizit konstruiert.
- Die harmonische Paarenergie besitzt keine abgeleitete Reichweite und ist
  kein universelles Kraftgesetz.
- Ein Anchor-Paar ist eine deterministische Klonarchitektur, keine
  Replikation oder Population.
- Gegenkraft im Port ist konstruiert; materieller Gesamtimpuls wird nicht
  gemessen.
- Die interne Arbeitszahl besitzt keine SI-Kalibration.
- Eine ambient kreisende oder transversale Paarantwort beweist weder internes
  $S^1$ noch Spin.
- Es wird keine Masse abgeleitet; beide Center bleiben first-order
  finite-memory Koordinaten.

## 14. Verbindliche Freeze-Sequenz

1. diesen targetfreien Designaudit committen, pushen und durch CI pruefen;
2. ein getrenntes P5-D-Protokoll mit exakten Panelwerten, Formeln,
   Schwellen, Serialisierungsordnung und Entscheidungslogik schreiben;
3. das Protokoll separat committen, pushen und reviewen;
4. erst danach Pair-step, Runner, unabhaengigen Auditor und synthetische
   Falsifikatoren implementieren;
5. Implementierung committen und pushen, ohne den registrierten Targetpfad
   aufzurufen;
6. ein separates Readinessreview mit Vollsuite und gruenem CI erstellen;
7. erst dann genau einen sauberen P5-D-Ziellauf erlauben;
8. Ergebnis unveraendert committen und erst danach kritisch reviewen.

## 15. Engste spaeter moegliche Aussage

Ein reviewed Vollpass duerfte hoechstens stuetzen:

> Zwei getrennt fortgeschriebene, vorbereitete Anchor-Schleifen erhalten
> unter der explizit deklarierten linearen notched-Center-/adjungierten
> Write-Kopplung ihre Einzelschleifen, schliessen einen gemeinsamen
> finite-$H$-Paarledger und zeigen unter den registrierten Richtungs-, Swap-,
> Vorzeichen-, Phasen-, Chiralitaets-, Distanz- und Staerkekontrollen eine
> aufgeloeste reziproke Closed-loop-Antwort jenseits der nachtraeglichen
> Summe beider Einwegantworten.

Das waere ein operationaler Mutual-Port-Befund. Es waere nicht die Emergenz
einer Wechselwirkung aus dem ungekoppelten Paper-I-Modell und kein Nachweis
von Ladung, Spin, Impuls, Traegheit oder Masse.
