# Kann gemeinsames weisses Rauschen die FIFO Zeitrichtung aufheben?

Stand: 2026-11-21. Fortsetzung des [Paar-Zeitumkehrtests](memory_pair_time_reversal_2026-11-21.md).
Analytischer Vergleich, keine neue Rauschregel im Modell und kein Ziellauf.

**Befund.** Bei verschiedenen geometrischen Retentionen kann keine
konstante Kopf-Rauschkovarianz die gemeinsamen Center-Inkremente
zeitumkehrsymmetrisch machen, sobald beide FIFO-Horizonte gleich
und mindestens drei sind. Bei genau zwei Speicherplaetzen gibt es
eine explizite Ausnahme. Sie erfordert eine bestimmte Driftbeziehung
und eine passende positive Kreuzkovarianz. Das ist eine Grenze eines
augenblicklichen weissen Bades, kein Ausschluss zeitlich strukturierter
Anstoesse oder einer physikalisch hergeleiteten Umgebung.

## 1. Einzige neue Annahme im Referenzvergleich

Behalte den attraktiven stationaeren linearen Paarblock mit
$g_i,h_i>0$, $s_i=1-g_i-h_i\ge0$ und gemeinsamem endlichem H bei.
Setze $0<q_A,q_B<1$, $q_A\ne q_B$ und
$P_i(z)=\sum_{\ell=0}^{H-1}q_i^\ell z^{-\ell}/S_i$,
$S_i=\sum_{\ell=0}^{H-1}q_i^\ell$.
Wie zuvor sei $A_i(z)=(z-s_i)/P_i(z)-g_i$.
Jetzt duerfen die beiden zeitlich weiterhin unabhaengigen, zentrierten
Gauss-Kopfinnovationen im selben Update korreliert sein:

$$
\Sigma=\begin{pmatrix}v_A&t\\t&v_B\end{pmatrix},
\qquad v_A,v_B>0,\quad t^2\le v_Av_B.
$$

Der vom gemeinsamen Translationsmodus befreite Center-Inkrementtransfer
bleibt unveraendert. Mit $A_i^\#(z)=A_i(z^{-1})$ und Weglassen des
nichtverschwindenden gemeinsamen Spektralfaktors ist die
Zeitumkehrbedingung dieselbe rationale Identitaet wie das
Verschwinden des Imaginaerteils der Kreuzkovarianz:

$$
0=F(z):=v_A h_B(A_B-A_B^\#)-v_B h_A(A_A-A_A^\#)
+t(A_B A_A^\#-A_B^\# A_A).
$$

Der reelle Term $t h_A h_B$ hebt sich dabei heraus. Die
Identitaet folgt aus Gleichheit auf dem Einheitskreis und
reell-rationaler Fortsetzung. Sie betrifft denselben
stationaeren Gaussprozess der Center-Inkremente wie zuvor,
nicht die vollen Speicherpfade oder einen angenommenen Kraftport.

## 2. Warum mindestens drei Speicherplaetze entscheidend sind

An einem inneren Pol $p=q_Be^{2\pi i m/H}$, $m=1,\ldots,H-1$,
von $A_B$ sind alle anderen Faktoren regulaer. Wegen
$q_A\ne q_B$, $s_B\ge0$ und $0<q_i<1$ ist der Pol einfach
und wird im Zaehlterm nicht aufgehoben. Seine Aufhebung in F
verlangt daher

$$
v_A h_B+t A_A(1/p)=0
$$

an **jedem** der H-1 Pole des B-Filters. Insbesondere ist t
nicht null. Mit $p^H=q_B^H$ ergibt die geometrische Summe

$$
A_A(1/p)=
\frac{S_A}{1-(q_Aq_B)^H}
\left[\frac1p+s_A q_A p-(s_A+q_A)\right]-g_A .
$$

Fuer zwei verschiedene solche Pole p und p' koennte der Wert
nur gleich sein, wenn $s_A q_A=1/(pp')$. Das ist unmoeglich:
Links ist der Betrag kleiner eins, rechts gleich $q_B^{-2}>1$.
Damit sind ab H=3 schon zwei notwendige Polbedingungen
unvereinbar. Der Beweis benoetigt nicht einmal die
Positivsemidefinitheit von Sigma. Bei $t=0$ verhindern bereits
die disjunkten inneren Pole eine Aufhebung, sofern ein
Rauschvarianzterm nicht null ist. Also verschwindet F fuer
$H\ge3$ in der gesamten reellen symmetrischen Kovarianzklasse
nur fuer die Nullmatrix.

Dies verschaerft den [endlichen Lag-Test](memory_pair_time_reversal_2026-11-21.md#3-endlicher-lag-test-und-bedeutung):
Die lineare Abbildung von den drei Kovarianzeintraegen zu den ersten
$2H-1$ antisymmetrischen Kreuzlags ist injektiv. An einem festen
Paar hat sie daher eine positive kleinste Singulaerzahl. Diese
kann beim Uebergang auf gleiche q und gleiche s gegen null gehen,
da der Grenzfall einen reversiblen Rauschvektor besitzt. Bei endlichen
Daten bleibt ein Fehler- und Aufloesungstest noetig.

## 3. Exakte Ausnahme bei H=2

Bei $H=2$ gibt es nur den Pol $-q_i$ pro Filter. Definiere
$L_A=-A_A(-1/q_B)$ und $L_B=-A_B(-1/q_A)$. Die beiden
inneren Polbedingungen lauten

$$
v_Ah_B=tL_A,\qquad v_Bh_A=tL_B.
$$

Sie heben durch $F(z^{-1})=-F(z)$ auch die reziproken Pole auf.
Beide L sind positiv, z.B.
$L_A=g_A+(1+q_A)(1/q_B+s_A)/(1-q_Aq_B)>1$, analog $L_B$.
Wegen $A_i(0)=-g_i$ und $A_i(z)\sim(1+q_i)z$ bei Unendlich
bleibt zusaetzlich die lineare Wachstumsbedingung

$$
(1+q_B)(v_Ah_B-tg_A)=(1+q_A)(v_Bh_A-tg_B).
$$

Nach Einsetzen der Polenbedingungen ist dies genau
$s_A-s_B=1/q_A-1/q_B$. Sind alle Bedingungen erfuellt, hat F
keine endlichen Pole mehr und ist bei Unendlich beschraenkt.
Die rational-ungerade Konstante ist null. Die Bedingungen sind
also notwendig und hinreichend. Die so bestimmte Kovarianz
ist fuer jedes $t>0$ positiv definit, denn $L_A L_B>h_A h_B$.

**Fester Zeuge.** Waehle
$q_A=1/2$, $q_B=3/5$, $s_A=1/2$, $s_B=1/6$,
$h_A=1/4$, $h_B=3/20$. Daraus folgen
$g_A=1/4$, $g_B=41/60$, beide positiv. Fuer $t=1$ ergeben
sich $L_A=137/28$, $L_B=789/140$ und

$$
v_A=685/21,\qquad v_B=789/35 .
$$

Die gemeinsame Kovarianz ist positiv definit und die
Center-Inkremente sind exakt zeitumkehrsymmetrisch. Mit
denselben Diagonalen, aber $t=0$, gilt der fruehere
Irreversibilitaetsbefund. Hier wird nichts an der Dynamik
nachgefittet; der Zeuge ist aus den algebraischen Bedingungen
konstruiert. Weder seine Parameter noch das gemeinsame
weisse Rauschen sind aus Memory abgeleitet.

## 4. Bedeutung und Verifikation

Eine physikalische Umgebung darf eigene Antwortzeiten und
Korrelationen tragen. Der Ausschluss ab H=3 bezieht sich nur
auf zeitlich weisse Kopfinnovationen mit konstanter 2x2-Matrix
und auf diesen attraktiven linearen Paarblock mit ungleichen
geometrischen Retentionen. Er fordert keinen bestimmten
Ersatz. Ein hergeleiteter Gleichgewichtsanschluss muesste
die zeitliche Rauschstruktur und die dissipative Antwort
gemeinsam begruenden; ein ad hoc angepasstes Spektrum
waere nur eine Referenz. Zeitumkehrsymmetrie des Readouts
allein bleibt kein physikalischer FDT-, Energie- oder Quantennachweis.

[Godreche und Luck, J. Phys. A 52, 035002 (2019), Abschnitt 2.3](https://arxiv.org/pdf/1807.00694)
vergleichen Drift und Diffusionsmatrix fuer Reversibilitaet in
kontinuierlichen mehrdimensionalen OU-Prozessen; das wird hier
nicht auf einen projizierten FIFO als Satz uebertragen.
[Maes, Safaverdi, Visco und van Wijland, Phys. Rev. E 87, 022125 (2013), Abschnitt II B](https://arxiv.org/pdf/1211.2181)
unterscheiden in ihrer generalisierten Langevinbeschreibung
eine durch lokale detaillierte Balance motivierte Beziehung
zwischen Reibungsgedaechtnis und Rauschkorrelation von frei
eingestelltem Rauschen. Gezielter Volltextabgleich, keine
Reproduktion und keine thermodynamische Zusatzannahme hier.

Die [festen Kontrollen](../../tests/test_memory_pair_time_reversal.py)
pruefen den rational konstruierten H=2-Zeugen mit der vollen
History-Resolvente und dem unabhaengigen Lag-Quotienten,
die separate Wirkung der Kreuzkovarianz und die Rangaussage
an festen H=2-, H=3- und H=4-Kontrollen. Kein Ziellauf und
keine Auswertung der offenen 3D-Traegerstabilitaet.

Der [anschliessende Portvergleich](memory_pair_port_spectrum_2026-11-21.md)
bestimmt am deklarierten Center-Arbeitsport ein zeitlich korreliertes
Nyquist-Referenzspektrum. Bei grossen Retentionen und H>=3 kann
harmonische Aktivitaet auch dieses passive Vergleichsbad ausschliessen.

Verifikation: 57 Tests im gezielten Panel bestanden, davon fuenf
neue Kontrollen. Das Panel umfasst ferner Paartransfer, Paarreduktion,
endlichen Abstand, Potentialbilanz und Markdown-Formeln.
Keine vollstaendige Repository-Testsuite.
