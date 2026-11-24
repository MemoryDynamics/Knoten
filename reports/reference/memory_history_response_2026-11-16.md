# Memory-Regeneration: volle Historienantwort statt isolierter Hoehenmode

Stand: 2026-11-16. Anschluss an die
[Zweiphasen-Kraftbilanz](memory_two_phase_balance_2026-11-16.md).
Keine neue Zielbahn, Parameterwahl, Regel oder Aenderung an Paper I.

## Ergebnis und Reichweite

Die notwendige skalare Rueckstellung ist noch kein Stabilitaetskriterium.
Jetzt liegt die vollstaendige lokale Ableitung der **vorhandenen**
deterministischen Alignment-Regel auf konsistenten gefuellten Historien vor.
Sie variiert Orte und daraus gewonnene Einheitsrichtungen gemeinsam.

Eine feste exakte Gegenkontrolle zeigt: Schon der Unterraum aus
Hoehenabstand und gemeinsamer axialer Translation ist unter der
Zweischritt-Rueckkehr nicht invariant. Zwei isolierte Hoehenableitungen
zu multiplizieren liefert deshalb keinen gerechtfertigten
Floquet-Multiplikator. Der bekannte negative-Gain-Vierzyklus bleibt
instabil; hier wird weder ein neuer Orbit noch ein neues allgemeines
Instabilitaetstheorem behauptet. Die vier Querbedingungen des
Zweiphasenansatzes sind weiterhin nicht geloest.

## 1. Ableitung der nativen Regel

Schreibe eine neueste-zuerst geordnete konsistente Historie als
Y=(y0,...,yN-1), mit N=max(H_s,H_v+1) bei aktivem Vektorkanal,
sonst N=H_s. Alle Koordinaten liegen in R^D. Definiere

$$
r_j=y_0-y_j,\qquad u_j=y_j-y_{j+1},\qquad
l_j=|u_j|,\qquad p_j=u_j/l_j.
$$

Fuer jeden aktiv gewichteten Vektoreintrag muss l_j>0 gelten. Am
Nullschritt ist die Einheitsdeposition nicht differenzierbar; ein
kleiner Nennerersatz waere eine andere Regel. Gewichtslose oder
vollstaendig deaktivierte Beitraege verlangen diese Voraussetzung nicht.

Mit nativen Vergessensgewichten v_j,w_j und G_sigma(r)=exp(-|r|^2/(2sigma^2)):

$$
\Psi(Y)=y_0-\eta_s\sum_{j<H_s}v_j\nabla K(r_j)
+\eta_v\sum_{j<H_v}w_jG_\sigma(r_j)p_j,
\qquad F(Y)=(\Psi(Y),y_0,\ldots,y_{N-2}).
$$

Die exakte erste Variation lautet

$$
\begin{aligned}
\delta\Psi={}&\delta y_0
-\eta_s\sum_{j=1}^{H_s-1}v_jD^2K(r_j)(\delta y_0-\delta y_j)\\
&+\eta_v\sum_{j<H_v}w_jG_\sigma(r_j)
\left[\frac{I-p_jp_j^T}{l_j}(\delta y_j-\delta y_{j+1})
-\frac{p_jr_j^T}{\sigma^2}(\delta y_0-\delta y_j)\right].
\end{aligned}
$$

Der skalare Selbstbeitrag j=0 verschwindet **vor** einer Hessian-
Auswertung. Bei Gaussdeposition gilt der bereits vorhandene effektiv
gefaltete Doppelgausskernel in der wirklichen Raumdimension D.
Orientierungs- und Kernelvariation sind beide notwendig.

`alignment_history_head_jacobian` speichert nur N Bloecke der Groesse
D mal D, nicht die gesamte ND-mal-ND-Matrix. Die restlichen
History-Zeilen verschieben die Variation unveraendert. Kosten und
Speicher der Kopfableitung sind O(N D^2). Es ist kein Solver und
kein automatischer Stabilitaetsentscheid. Die bestehende planare
Normalableitung bleibt unveraendert und wird als Projektion kontrolliert.

Translationsaequivarianz verlangt die Blocksumme I. Fuer jeden
antisymmetrischen Rotationsgenerator Omega gilt ausserdem
D Psi(Y)[Omega Y]=Omega Psi(Y). Beides wird unabhaengig von einer
Orbitannahme geprueft; gespeicherte Richtungen sind keine unabhaengigen
zusaetzlichen Freiheitsgrade.

## 2. Was die Hoehenableitung tatsaechlich misst

Verwende die Zweiphasenfamilie x_2k=Q^k a, x_2k+1=Q^k b mit
eigentlich rotierendem Q und fester Achse e. Variiere ausschliesslich
den Abstand d=e dot (b-a), bei festem axialem Mittelpunkt und festen
Querkoordinaten. Dann l_a^2=c_a^2+d^2, l_b^2=c_b^2+d^2 mit konstanten
transversalen Schrittlaengen c_a,c_b. Die Definitionen E_X,O_X,T_X,U_X
stammen aus dem vorherigen Bericht, sigma bezeichnet die Vektorbreite.

E_X ist unabhaengig von d; O_X enthaelt den Faktor exp(-d^2/(2sigma^2)).
Mit k'=dk/dD folgt

$$
T_X'=2d\sum_{\substack{j<H_s\\j\ {\rm ungerade}}}v_jk'(|x_X-y_{Xj}|^2),
$$

$$
U_a'=-\frac{dE_a}{l_a^3}
+dO_a\left(\frac1{\sigma^2l_b}+\frac1{l_b^3}\right),\qquad
U_b'=-\frac{dE_b}{l_b^3}
+dO_b\left(\frac1{\sigma^2l_a}+\frac1{l_a^3}\right).
$$

Setze A_X(d)=eta_s T_X(d)-eta_v w0 U_X(d). Die axialen Kopfwerte
sind, abgesehen vom konstanten Mittelpunkt, -d/2+d A_a beziehungsweise
d/2-d A_b. **An einem wirklichen Orbit**, also A_a=A_b=1 samt allen
Querbedingungen, sind ihre Ableitungen

$$
\frac12+dA_a',\qquad -\frac12-dA_b'.
$$

Dies sind Richtungsableitungen auf einer vorgegebenen Historienfamilie,
keine geschlossene Dynamik fuer d. Das Update veraendert nur den Kopf;
die alten Abstaende im FIFO werden nicht gleichzeitig reskaliert.
Zusaetzlich koennen Querantworten entstehen. Eine reduzierte
Hoehendynamik benoetigt einen separat bewiesenen invarianten Unterraum
oder eine kontrollierte Reduktion mit Fehlergrenze.

## 3. Exakte Nichtabgeschlossenheit am vorhandenen Kontrollorbit

Nutze unveraendert den
[negativen-Gain-Tetraederzyklus](memory_defect_recurrence_2026-11-14.md)
mit R uneigentlich, R^4=I und eigentlichem Q=R^2. Die Achse e=-e_y,
a=y0, b=R a und d=1 ergeben

$$
l_a=l_b=\sqrt2,\quad E_a=E_b=9/8,\quad O_a=O_b=5/16,
\quad\eta_sT_X=-37/2,\quad\eta_vw0U_X=-39/2.
$$

Insbesondere A_X=1. Fuer die Ableitungen gilt exakt

$$
\eta_sT_X'=37/4,\qquad
\eta_vw0U_X'=39/4-(15/2)\log2,\qquad
A_X'=-1/2+(15/2)\log2.
$$

Die reine Abstandstangente hat y-Koordinaten
(1/2,-1/2,1/2,-1/2,1/2), alle anderen Komponenten null. Der wirkliche
naechste Kopf besitzt in y die Antwort -(15/2)log2, nicht -1/2.

Nach zwei Schritten bleibt genau dieser erste neue Kopf als Alter 1
gespeichert. Q laesst die y-Achse unveraendert. Die alten Eintraege
an Alter 2 und 3 haben weiterhin Antworten +1/2,-1/2. Eine Darstellung
als Vielfaches der Abstandstangente plus gemeinsamer y-Translation
erzwingt dadurch den Faktor 1 und Translation 0. Alter 1 widerspricht
dem, mit Abweichung (15/2)log2-1/2>4. Die fruehere rationale Schranke
log2>69/100 reicht fuer diese strikte Ungleichung.

Dies beweist die Nichtinvarianz auch fuer die **Zweischritt-
Rueckkehr**, nicht bloss fuer einen Zwischenstand. Der Test bestimmt
die Koeffizienten von 1,log2,log^2(2) exakt mit rationaler Arithmetik.
Kein Eigenwertfit und kein allgemeiner Ausschluss anderer reduzierter
Unterraeume. Die volle Instabilitaet dieses Orbits war bereits separat
durch das Spurpolynom bewiesen.

## 4. Richtiger Rueckkehroperator und Literaturabgleich

Fuer einen nachgewiesenen Zweiphasenorbit mit Y_b=F(Y_a) und
F(Y_b)=Q Y_a lautet der volle Operator in Spaltenkonvention

$$
M_2=(I_N\otimes Q^{-1})\,DF(Y_b)\,DF(Y_a).
$$

Ohne Existenznachweis muss die zweite Ableitung bei **F(Y_a)**
ausgewertet werden, nicht bei einer gewuenschten Phase Y_b.
Auch ein Produkt an echten Zwischenzustaenden ist ausserhalb eines
relativen Orbits noch kein Floquet-Stabilitaetsbefund.
Am bekannten R-Kontrollorbit wird M_2=M_1^2 und das alte exakte
Spurpolynom unabhaengig mit den neuen allgemeinen Bloecken reproduziert.

Translationsrichtungen werden im Rueckkehrrahmen durch Q^-1
transportiert, Rotationsgeneratoren durch Q^-1 Omega Q. Ihre
Symmetriemultiplikatoren muessen nicht alle +1 sein. Eine diskrete
Zeitentwicklung besitzt zudem nicht automatisch die neutrale
Zeitphasenmode eines autonomen kontinuierlichen Flusses.

Der gelesene methodische Anschluss an Sidorenko/Thunberg,
[*Attracting Rotations Obstruct Almost-Global Consensus on Spheres
over Strongly Connected Graphs*, arXiv:2610.28341v1](https://arxiv.org/html/2610.28341v1),
ist eng begrenzt: Anhang B.3, Gleichungen (99)-(109), linearisiert
die volle tangentiale Agentendynamik im mitrotierenden Rahmen;
B.5, (207)-(220), trennt Form und Orientierung lokal am vollrangigen
Orbit. Erst die Formkontraktion begruendet dort Attraktion modulo
Rotation. Diese Abschnitte wurden im Volltext gelesen, kein eigener
Nachvollzug ihres Intervall-Stabilitaetszertifikats. Der Preprint
behandelt unabhaengige normierte Agenten, keinen seriellen FIFO.
Seine Kopplungen und Resultate werden nicht als native Memory-Regel
uebernommen; keine Stabilitaetsaussage in hoeheren Dimensionen importiert.

## 5. Verifikation und verbleibende Grenze

36 neue feste Kontrollen: 27 zur allgemeinen Kopfableitung, sechs
zur Hoehenformel mit unterschiedlichen Horizonten und allen drei
nativen Depositionskonventionen, drei zum bereits bekannten Orbit.
Die Ableitung wird in Dimension 2,3,5 an allen Koordinaten gegen
zentrale Differenzen geprueft, einschliesslich Symmetrien, langer
Skalarhistorie, inaktiver Kanaele und unzulaessiger Nullschritte.
Eine feste off-orbit Gegenprobe unterscheidet den richtigen
Zweischritt-Operator von der Ableitung an einer vorgeschriebenen Phase.
Dies sind lokale Methodenpruefungen, keine Zieltrajektorien.

336 Tests im betroffenen Panel einschliesslich Kernel-Audit bestehen,
ebenso Lint, strikter Dokumentationsbau und die nach der Berichtsergaenzung
erneut geprueften Markdown-Formeln; keine vollstaendige Repository-Testsuite.
Gleitkomma-Differenztests
ersetzen nicht den algebraischen Beweis; die exakte Nichtinvarianz
nutzt das unabhaengige rationale Kontrollpolynom.

Die Existenz eines geeigneten Memory-Traegers ist weiterhin offen.
Insbesondere sind notwendige Achsenrueckstellung, beide vollen
Kopfbilanzen, regulaerer gebundener Defekt und volle Formstabilitaet
nicht durch dieselbe neue Loesung erfuellt. Selbst ein solcher
Erfolg waere noch kein elektrischer Quellenport, Spin oder QFT.
Die einzige aktive Arbeitsreihenfolge bleibt in den
[Projektprioritaeten](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/docs/status/project_priorities.md).
