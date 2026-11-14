# Memory-Defekt: Rekurrenz, Vorzeichen und volle Formstabilitaet

Stand: 2026-11-14. Fortsetzung des
[Defekt-/FIFO-Audits](memory_defect_charge_2026-11-14.md).
Analytische Resultate und endliche konstruierte Rechenkontrollen,
keine Parameter- oder Orbitsuche und keine neue Zieltrajektorie.

## Ergebnis

Die Ein-Schritt-Konstruktion laesst sich jetzt klarer einordnen:

- **Minimaler Vorzeichenbefund:** Bei d+1 gerichteten Depositionen in
  R^d hat jede regulaere Nullstelle dieses bahnkonsistenten
  Gaussreadouts Index +1. Das gilt auch fuer offene Historien, nicht
  nur fuer das vorherige geschlossene Simplex. In 3D liefern vier
  Depositionen mit derselben Definition also keine beiden Ladungsvorzeichen.
- **Positive Alignment-Kopplung:** Ein rauschfreier periodischer Umlauf durch die
  vier Ecken eines regulaeren Tetraeders ist fuer native
  Vergessensfaktoren 0 < q,s < 1 und nichtnegativen Vektorgain unmoeglich, auch mit
  verschiedenem skalarem und vektoriellem Vergessen. Der Satz betrifft
  Horizonte aus ganzen Vierperioden, nicht beliebige Geometrien.
- **Nicht pauschal ausschliessen:** Der bestehende Code erlaubt auch
  negativen Vektorgain. Dafuer existiert ein exakt konstruierter,
  rauschfreier Vierzyklus mit periodisch gebundenem +1-Defekt. Seine
  **volle History-Dynamik ist jedoch instabil**. Eine exakte
  Spurschranke beweist einen Vier-Schritt-Floquet-Multiplikator mit
  Betrag groesser als 3; kein gerundeter Eigenwert wird als Beweis benutzt.

Damit ist zeitlich wiederkehrende Defektstruktur im vorhandenen Modell
nicht allgemein ausgeschlossen, aber auch kein stabiler Memory-
Ladungstraeger gewonnen. Der negative Gain ist eine algebraische
Gegenkontrolle, keine neue physikalische Parameterwahl oder Freigabe
fuer einen Ziellauf. Paper I und die Simulationsregeln bleiben unveraendert.

## 1. Alle minimalen regulaeren Defekte haben dasselbe Vorzeichen

Seien H=d+1 gerichtete Depositionen aus einer beliebigen Historie
y_0,...,y_{d+1} gegeben, mit u_j=y_j-y_{j+1}. Ein Ringschluss wird
**nicht** vorausgesetzt. Wie im vorherigen Bericht gilt

$$
V(z)=\sum_{j=0}^{d}w_j\frac{u_j}{s_j}
e^{-|z-y_j|^2/(2\sigma^2)},\qquad w_j>0,\quad \sigma>0,
$$

mit s_j=1 fuer Displacement und s_j=|u_j| fuer Einheitsrichtungen.
Bei einer regulaeren Nullstelle hat die Matrix der u_j vollen Rang d.
Die positiven Gausskoeffizienten liefern eine positive Nullrelation

$$
\sum_{j=0}^{d}r_j u_j=0,\qquad r_j>0.
$$

Ihr Kern ist eindimensional. Weil jede Komponente r_j positiv ist,
sind insbesondere u_0,...,u_{d-1} linear unabhaengig; ebenso sind
y_0,...,y_d affin unabhaengig. Umgekehrt reichen voller Rang und eine
positive Nullrelation fuer genau eine endliche Nullstelle: Ihre
Koeffizienten muessen w_j G_j/s_j=c r_j mit c>0 erfuellen. Nach
Logarithmieren ergibt sich das eindeutig loesbare lineare System

$$
(y_j-y_0)\cdot z_*=
\frac{|y_j|^2-|y_0|^2}{2}
-\sigma^2\log\frac{w_j/(s_jr_j)}{w_0/(s_0r_0)},
\qquad j=1,\ldots,d.
$$

Nach Translation y_0=0 setze U=(u_0,...,u_{d-1}). Dann sind
y_j=-sum_{k<j}u_k und u_d=-sum_{j<d}(r_j/r_d)u_j. Im Jacobian
verschwinden die z_*-Terme durch die Nullrelation. Ausschreiben liefert

$$
D V(z_*)=\frac{c}{\sigma^2}UTU^{\mathsf T},\qquad
T_{ik}=\begin{cases}r_i,& k\geq i,\\0,&k<i,\end{cases}
\quad 0\leq i,k<d.
$$

Damit gilt

$$
\det D V(z_*)=
\left(\frac{c}{\sigma^2}\right)^d
(\det U)^2\prod_{i=0}^{d-1}r_i>0.
$$

Der Satz schliesst jede **regulaere** negative Indexquelle in dieser
minimalen Klasse aus. Eine rangdefiziente Richtungsmenge bildet das
gesamte Feld in einen echten linearen Unterraum ab und kann auch bei
isolierten Nullstellen keinen von null verschiedenen lokalen Grad
tragen. Diese Ausnahme erzeugt daher keine versteckte negative Ladung.
Fuer weniger als d+1 aktive Richtungen ist eine regulaere Nullstelle
bereits durch den Rang ausgeschlossen.

Falls ein gemeinsamer physikalischer Ladungsreadout proportional zu
diesem Index sein soll, braucht ein Paar entgegengesetzter Vorzeichen
folglich mehr als d+1 aktive Depositionen oder eine andere, eigenstaendig
hergeleitete Definition. **H>=5 in 3D ist nur eine notwendige Huerde,
keine hinreichende Konstruktion.** Depositionen sind Speicherbeitraege
einer Bahn, nicht Quarks oder Teilchen. Die Aussage legt weder eine
physikalische Dimension noch die Elementarladung fest.

## 2. Regulaerer Tetraeder-Umlauf: Existenz vor Stabilitaet

Betrachte eine vorgeschriebene rauschfreie Vierperiode durch regulaere
Tetraederecken, mit gemeinsamer Kantenlaenge ell und unit-orientierter
Deposition. Seien q und s die vektoriellen bzw. skalaren
Vergessensfaktoren in (0,1), zunaechst H_v=H_s=4. Definiere

$$
g=e^{-\ell^2/(2\sigma_v^2)}\in(0,1),\qquad
B=\frac{\eta_v w_0}{\ell},\qquad
C=\eta_s a(\ell)v_0,
$$

mit grad K(r)=a(|r|)r. C darf ein beliebiges reelles Vorzeichen haben;
es wird kein attraktiver skalarer Kern vorausgesetzt. In der Basis
(u_0,u_1,u_2) lauten die drei Koeffizienten des aktuellen Schritts

$$
\begin{aligned}
d_0&=B(1-gq^3)-C(s+s^2+s^3),\\
d_1&=Bg(q-q^3)-C(s^2+s^3),\\
d_2&=Bg(q^2-q^3)-Cs^3.
\end{aligned}
$$

Fuer den exakten Umlauf muss der neue Ort y_3 sein, also
d_0=d_1=d_2=-1. Die Differenzen erzwingen bei B ungleich null

$$
Cs=B(1-gq),\qquad Cs^2=Bgq(1-q),\qquad
s=\frac{gq(1-q)}{1-gq}<q.
$$

Setzt man dies in den letzten Koeffizienten ein, folgt

$$
d_2=Bgq(1-q)(q-s).
$$

Fuer B>0 ist dieser Wert positiv statt -1. Bei B=0 erzwingt bereits
die erste Differenz C=0, ebenfalls ohne Umlauf. Damit ist die
regulaere Vierperiode fuer eta_v>=0 ausgeschlossen. Das ist ein
Existenzhindernis, kein durch kleine Stoerungen beobachteter Zerfall.

Der Befund gilt auch fuer H_v=4m_v und H_s=4m_s mit positiven ganzen
m_v,m_s: Auf einer exakten Vierperiode summieren sich die Gewichte
einer Phase zu

$$
\sum_{k=0}^{m-1}w_0q^{j+4k}
=w_0\frac{1-q^{4m}}{1-q^4}q^j,\qquad j=0,1,2,3.
$$

Dies reskaliert lediglich B bzw. C positiv. Langes Memory aus ganzen
Wiederholungen beseitigt dieses Hindernis nicht. Bei nicht durch vier
teilbaren Horizonten aendern sich die Phasengewichte; der Satz behauptet
dort nichts. Ebenso bleiben nichtregulaere und laengerperiodische
Historien offen. Ein Tetraeder ist hier ein Bahnansatz, kein Protonmodell.

## 3. Exakter Gegenfall mit vorhandenem negativem Gain

Die Validierung von `VectorMemoryConfig` fordert fuer eta_vector nur
Endlichkeit, nicht Positivitaet. Eine Aussage ueber die gesamte
implementierte Familie darf diesen Zweig daher nicht unterschlagen.
Waehle ausschliesslich als algebraische Kontrolle

$$
q=g=\frac12,\qquad s=\frac16,\qquad B=-24,\qquad C=-108.
$$

Die obigen drei Koeffizienten sind dann exakt -1. Eine konkrete
Realisierung in willkuerlichen Laengeneinheiten ist

$$
\begin{aligned}
y_0&=(1,1,1)/2,& y_1&=(1,-1,-1)/2,\\
y_2&=(-1,1,-1)/2,& y_3&=(-1,-1,1)/2,\qquad y_4=y_0.
\end{aligned}
$$

Hier ist ell=sqrt(2). Beide Memory-Massennormierungen sind 1,
beide Horizonte 4, epsilon=0 und die skalare Deposition ist delta.
Fuer den bestehenden Doppelgauss-Kernel waehle A_rep=1,
sigma_rep=sqrt(2), A_att=0; die dann wirkungslose positive
sigma_att wird im Test auf 2 gesetzt. Damit ist a(ell)=-exp(-1/2)/2.
Die Parameter lauten vollstaendig

$$
\alpha_s=5/6,\quad\lambda_v=1/2,\quad
\sigma_v=1/\sqrt{\log2},\quad
\eta_v=-48\sqrt2,\quad
\eta_s=\frac{108}{(5/6)(1/2)e^{-1/2}}.
$$

`force_mode=alignment`, `memory_factor=vector_memory_factor=4` und die jeweiligen Maximalhorizonte
4 erzeugen diese Speichertiefen. Das sind keine gemessenen Teilchen-
parameter, kein Kontinuumsgrenzfall und kein Genauigkeitsfit. Die
Gains sind gross und stammen aus der Existenzidentitaet; kein
physikalisch akzeptierter Kopplungswert wird daraus abgeleitet.

Mit

$$
R=\begin{pmatrix}0&0&-1\\0&-1&0\\1&0&0\end{pmatrix},
\qquad R^4=I,\quad\det R=-1,
$$

gilt fuer den gesamten Fuenfpunkt-Historienzustand Y genau
F(Y)=R Y. R wirkt auf jeden gespeicherten Punkt. Die Schreibweise
meint diese gemeinsame Raumtransformation, nicht Matrixmultiplikation
mit einer zeilenweise gespeicherten History. R ist **keine eigentliche
Rotation**; insbesondere folgt daraus kein Spin- oder 2-pi-Befund.

Die O(3)-Aequivarianz der vorhandenen rauschfreien Regel und R^4=I
liefern F^4(Y)=Y. Die +1-Nullstelle beginnt bei z_*=(-2,-1,0) und
nimmt an den folgenden Phasen die Orte R^k z_* an. Ihr Radius um den
festen Bahnmittelpunkt ist stets sqrt(5), der Radius der Speicherorte
sqrt(3)/2. Das ist ein exakt wiederkehrender, endlich gebundener
Defekt an diesem Orbit, nicht bereits ein anziehender oder stoerungs-
resistenter Kern. Die Aussage betrifft die diskreten Updatezeitpunkte;
ein physikalischer Zwischenzeit-Strom ist dadurch nicht hergeleitet.
Die Historie wird vorgegeben, nicht aus leerem
Speicher als spontaner Attraktor erzeugt.

## 4. Volle History-Variation widerlegt Stabilitaet der Kontrolle

Die Zustandsdimension ist 15: vier gerichtete Depositionen brauchen
fuenf dreidimensionale Positionen zur konsistenten Rekonstruktion der
letzten Orientierung. Keine Orientierung darf bei der Variation
eingefroren werden. Mit r_j=y_0-y_j, p_j=u_j/ell_j und G_j=G(r_j)
lauten die Beitraege zur ersten Blockzeile des History-Jacobians

$$
\begin{aligned}
\delta y_+={}&\delta y_0
-\eta_s\sum_{j=1}^{3}v_j D^2K(r_j)(\delta y_0-\delta y_j)\\
&+\eta_v\sum_{j=0}^{3}w_jG_j\left[
\frac{I-p_jp_j^{\mathsf T}}{\ell_j}(\delta y_j-\delta y_{j+1})
-\frac{p_jr_j^{\mathsf T}}{\sigma_v^2}(\delta y_0-\delta y_j)
\right].
\end{aligned}
$$

Die uebrigen Blockzeilen sind der native History-Shift. Die skalare
Selbstdeposition hat keine Differenzvariation. Saemtliche Schritte
des konstruierten Orbits sind ungleich null, sodass die Normierungs-
ableitung existiert.

Diese Positions-History parametrisiert die bahnkonsistenten nativen
Zustaende mit einer redundanten Koordinate: Eine Laengenaenderung
des aeltesten Schritts bei fester Richtung aendert keine noch gelesene
Deposition. Ihr Jacobian-Bild ist null, wie separat kontrolliert wird.
Sie kann daher keinen wachsenden Multiplikator erzeugen. Fuer den
Instabilitaetsnachweis reicht eine wachsende Richtung in dieser
invarianten bahnkonsistenten Zustandsklasse; unabhaengig erfundene
Orientierungen oder zusaetzliche innere Freiheitsgrade werden nicht benutzt.

Definiere G=R^{-1}F auf dem gesamten Historienzustand. Wegen
Aequivarianz kommutiert F mit R, G(Y)=Y und F^4=G^4. Deshalb ist
der volle Vier-Schritt-Floquet-Operator am Orbit M^4 mit M=DG(Y).
Fuer die oben festgelegten Parameter laesst er sich exakt schreiben als

$$
M=M_0+(\log2)M_1,\qquad M_0,M_1\in\mathbb Q^{15\times15}.
$$

Die [Kontrollen](../../tests/test_memory_defect_recurrence.py) bauen
diese Matrizen aus der angegebenen Variation mit rationaler Arithmetik
auf, getrennt von der Differenzenquotientenpruefung der nativen
Kraftfunktionen. Exakte Multiplikation ergibt

$$
\operatorname{tr}(M^2)=\frac{97}{16}
-\frac{63}{4}\log2+\frac{261}{4}(\log2)^2.
$$

Eine rein rationale Schranke reicht aus. Aus
log2=2 atanh(1/3)=2 sum_{k>=0}(1/3)^{2k+1}/(2k+1) folgt

$$
\frac{69}{100}<\frac{56}{81}<\log2
<\frac{56}{81}+\frac1{540}<\frac7{10}.
$$

Der Rest wurde durch die geometrische Reihe mit Nenner mindestens
5 majorisiert. Damit gilt

$$
\operatorname{tr}(M^2)>
\frac{97}{16}-\frac{63}{4}\frac7{10}
+\frac{261}{4}\left(\frac{69}{100}\right)^2>26>15.
$$

Fuer jede 15-dimensionale Matrix, auch mit komplexen Eigenwerten und
Jordanbloecken, ist |tr(M^2)| <= 15 rho(M)^2. Also

$$
\rho(D F^4)=\rho(M)^4>
\left(\frac{26}{15}\right)^2>3.
$$

Die Instabilitaet folgt somit weder aus transienter Normverstaerkung
noch aus numerischer Eigenwert-Rundung. Translationen und starre
Raumrotationen werden im reduzierten Schritt durch R^{-1} bzw. dessen
Konjugationswirkung transportiert und haben Multiplikatoren vom
Betrag 1. Die wachsende Richtung ist deshalb keine solche Symmetrie-
verschiebung. Dies beweist Instabilitaet **dieser Kontrolle**, nicht
aller negativen Gains oder aller nichtplanaren Defekte.

## 5. Literaturabgleich und Bedeutung fuer das Teilchenziel

[Siminos und Cvitanovic, Physica D 240, 187-198 (2011)](https://doi.org/10.1016/j.physd.2010.07.010)
behandeln Aequivarianz, relative periodische Orbits und Symmetriereduktion
an dissipativen kontinuierlichen Flows. Geprueft wurden im
[Primaerpreprint](https://arxiv.org/pdf/1006.2362v1) insbesondere
Abschnitt 3, Gl. (21), und die Einleitung zu Abschnitt 4. Das begruendet
die methodische Trennung zwischen Bewegung entlang einer Symmetrie und
Formvariation. Unsere diskrete Identitaet F^4=G^4 und der Spurtest sind
oben eigenstaendig abgeleitet; der Artikel beweist keinen FIFO-Orbit
oder Memory-Ladungsschutz.

Der bereits im [Strukturabgleich](../../docs/reference/fifo_rigid_structure_limits.md)
erfasste Vergleich von Kopp und Klapp,
[PRE 107, 024611 (2023)](https://doi.org/10.1103/PhysRevE.107.024611),
wurde nochmals am [Autorenstand v3](https://arxiv.org/pdf/2210.03182v3)
mit Abschnitt II und dem deterministischen Modellansatz abgeglichen.
Dort kann repulsives Gaussfeedback mit einem einzelnen Zeitverzug
persistente Translation erzeugen. Das ist weder gebundene 3D-Defekt-
struktur noch ein Transfer unserer Stabilitaet. APS weist auf eine
Korrektur von Gl. (6) am 12.06.2023 hin; diese Gleichung wird hier
nicht verwendet. Keine eigene Reproduktion der Literaturmodelle.

Der entscheidende Zugewinn gegenueber einem Formbild ist jetzt die
getrennte Kette: zulaessige Historie, Index, exakte native Rekurrenz,
endlicher Defektabstand und volle Formvariation. Die Kontrolle erfuellt
die ersten vier Eigenschaften, scheitert an der fuenften. Zusaetzlich
fehlt in der gesamten minimalen Klasse das entgegengesetzte Index-
vorzeichen. Ein weiteres Optimieren dieser Kontrolle waere daher
kein Ersatz fuer den gesuchten robusten Ladungstraeger mit Wechselwirkung.

Es bleiben andere, nichtminimale und nichtregulaere Memory-Strukturen
offen. Ein positiver Befund dort muesste im selben Zustandsvertrag
beide benoetigten Vorzeichen, lokale Bindung und den dynamischen Schutz
pruefen. Selbst dies waere noch keine elektrische Quellenkopplung,
Quantenstatistik, Massenherleitung oder Gravitation. Die aktive
Arbeitsreihenfolge steht nur in den
[Projektprioritaeten](../../docs/status/project_priorities.md).

## 6. Ausfuehrungs- und Pruefumfang

Die neuen Tests pruefen die minimale Vorzeichenformel an offenen
Historien in 2D/3D/5D, beide Depositionskonventionen, die notwendigen
Vierzyklus-Gleichungen, Phasengewichte ganzer Perioden, den exakt
festgelegten negativen Gain-Kontrollfall an vier vorgeschriebenen
Phasen, alle 15 History-Ableitungen, Symmetrierichtungen und das
rationale Instabilitaetszertifikat. Die Native-Regel wird nicht geaendert.
Die vier Phasen sind algebraische Kontrollen, keine gesuchte oder lange
integrierte Zielbahn. Kein Anker-Replay, keine automatische Gain-/H-
Suche und kein neuer ausfuehrbarer Ziellauf.

Ein separater kleiner Matrixaufruf in der eingeschraenkten Umgebung
blieb ohne Ausgabe und wurde kontrolliert abgebrochen; sein Prozessende
wurde geprueft. Dieselbe endliche Algebra lief danach in der bereits
funktionierenden Testumgebung mit fester 10-s-Abbruchgrenze in etwa
1.5 s durch. Dies war keine wiederholte Zielsimulation. SymPy war nicht
installiert und wurde nicht nachinstalliert; das Zertifikat verwendet
die Standardbibliothek `fractions.Fraction`.

Die Beweise beziehen sich auf exakte reelle Arithmetik; die native
Kraft- und Differenzenquotienten-Gegenpruefung arbeitet mit binary64.
Sie ersetzt weder eine unabhaengige Begutachtung noch eine allgemeine
Klassifikation aller Memory-Defekte. Die Literatursuche war gezielt,
nicht systematisch; kein Neuheitsanspruch aus fehlenden Suchtreffern.

Verifikation: **23 neue konstruierte Kontrollen und 153 Tests im
betroffenen Panel bestanden**. Das Panel umfasst Rekurrenz, Defekt-
Readout, aktive Vektormemory und Normalantwort, topologischen
Zustandsvertrag, Memory-Strom, kollektive Ladung, Kernphase, Zustands-
und Markdown-Mathematiktests. Keine vollstaendige Repository-Suite
und keine unabhaengige Reproduktion eines Literaturmodells.
Ruff, strikter MkDocs-Bau und Whitespacepruefung bestanden.
