# Ein autonom wiederkehrender FIFO-Traeger und seine Querinstabilitaet

Stand: 2026-11-24. Fortsetzung des
[reversiblen einzelnen Schreibereignisses](fifo_reversible_carrier_2026-11-24.md).
Analytischer klassischer Vergleich mit idealer Taktschnittflaeche.
Keine Aenderung der nativen FIFO-Regel, keine Zieltrajektorie,
kein selbstgebundener Memory-Knoten.

**Ergebnis.** Ein Rotor und derselbe Traeger koennen ein
vorbereitetes FIFO wiederholt exakt schreiben, ohne Reset
oder neue Energiezufuhr. Der Rotor muss hier synchron zur
halben Periode einer deklarierten Relativfeder laufen.
Die so gebildete Zweiperiode ist in mindestens zwei
Raumdimensionen fuer jede ungerade FIFO-Laenge $H\ge3$
linear instabil: Ein Querimpuls des Kopfs wird durch
die volle Schreib- und Rueckkehrkarte verstaerkt.
Der instabile Multiplikator bleibt gleich, wenn eine
dynamische skalare Kernel-Amplitude die zentrale Kraft
moduliert, solange dieselbe kollineare Schreibbahn
erhalten bleibt und die Speichereintraege passiv sind.

## 1. Takt und Traeger im selben autonomen Vergleich

Der Takt ist ein Rotor mit Umfang $L$ und Masse $M_s$.
Die bekannte kanonische Registerkarte $C$ wird am
Schnitt des Kreises angewandt. Im aufgeschnittenen
Bereich ist das Register-Hamiltonian zeitunabhaengig:

$$
E_{\rm int}=\frac{|P_x|^2+|P_b|^2}{2m}
              +\frac{k}{2}|x-b|^2 .
$$

Der Kopf $x$ und der Traeger $b$ haben Masse $m$
und eine translationsinvariante Relativfeder.
Die alten $y_j$ und ihre konjugierten Impulse
stehen zwischen den Writes still, da $E_{\rm int}$
von ihnen unabhaengig ist. Das ist ein gewaehlter
degenerierter Aufzeichnungsspeicher, keine
hergeleitete Massentraegheit seiner Eintraege.
Insbesondere sitzt die Bindung in der Feder,
nicht in einer aus den Eintraegen erzeugten Kraft.

Am Schnitt sind die Registercharts durch $C$ und
den zugehoerigen Impulslift verklebt. Der
Energiesprung wird aus dem Taktimpuls $\pi_s$
wie im vorigen Bericht bezahlt; bei Mangel
reflektiert der Takt. Zwischen den Schnitten
laeuft der Rotor frei. Nach erfolgreichem Write
betragt die Flugzeit $\tau=M_sL/|\pi_s|$ mit
dem **ausgehenden** Impuls. Eine neue Zeit oder
ein neuer Traeger wird danach nicht gesetzt.
Die Konstruktion ist ein idealer autonomer
Schnitt-Hamiltonian, keine glatte Mikrodynamik
des Schreibmechanismus.

## 2. Exakte Zweiperiode

Sei $H$ ungerade, $A\ne0$ ein fester Ortsvektor
und vor einem Vorwaertsschreiben

$$
x=A,\qquad b=-A,\qquad
y_j=(-1)^{j+1}A,\quad 0\le j<H,\qquad P=0.
$$

Der alte letzte Eintrag ist $-A=b$. Der Write
kopiert daher $x$ exakt, speichert den alten
Eintrag im selben Traeger und aendert die
internen Impulse nicht. Das interne Hamiltonian
haengt nur von $x,b,P_x,P_b$ ab und bleibt beim
Schreiben exakt gleich. Der Rotor zahlt auf
dieser speziellen Bahn keine Nettoarbeit pro
Write. Waehle seinen Anfangsimpuls so, dass

$$
\omega=\sqrt{2k/m},\qquad
\tau=\pi/\omega,\qquad
\pi_s=M_sL\omega/\pi .
$$

Nach einem Rotorumlauf hat die Relativfeder
eine halbe Periode absolviert. Kopf und Traeger
haben die beiden Positionen getauscht und stehen
wieder am Umkehrpunkt. Die geschriebenen Register
ergeben beim naechsten Eintreffen genau die
vorzeichenumgekehrte urspruengliche Historie;
insbesondere ist der Traeger erneut bereit.
Nach zwei Writes sind alle Koordinaten und
Impulse zurueck. Die Gesamtenergie
$2k|A|^2+\pi_s^2/(2M_s)$ ist endlich.
Die Anfangsphase und das Frequenzverhaeltnis
sind vorbereitet, nicht spontan ausgewaehlt.

Wenn nur die Anfangsflugzeit um $\delta/\omega$
abweicht, bleibt der erste Write exakt und
kostenlos. Beim zweiten Eintreffen ist dagegen
$b-y_{H-1}=A(\cos\delta-1)$: Der Traeger verfehlt
den richtigen Eintrag, obwohl er weiterlaeuft.
Der Fehler ist an diesem Umkehrpunkt quadratisch
klein, aber nicht identisch null.

## 3. Der volle Querimpuls hat einen wachsenden Zweig

Betrachte eine Raumrichtung senkrecht zu $A$.
Die Ableitung des Grenzflaechen-Energiesprungs
in diesen Querkoordinaten verschwindet: Die
Grundauslenkung ist parallel zu $A$, und die
Grundimpulse sind null. Also bleibt die
Flugzeit in erster Ordnung unveraendert.
Die folgende Rechnung ist deshalb die
Querableitung des gekoppelten Rotors, nicht
diejenige einer nachtraeglich festgehaltenen Zeit.

Bei einer halben Federperiode werden
in der Impulszeile Kopf und Traeger
vertauscht. Das Positionsblocksymbol $B$
des Halbschritts mit vorherigem Write
setzt, ohne die Positionsbeitraege der
Impulse, die drei ersten bzw. letzten
Beziehungen

$$
x_{\rm neu}=y_{H-1},\qquad
b_{\rm neu}=x,\qquad
(y_0)_{\rm neu}=x+b-y_{H-1},
\qquad (y_j)_{\rm neu}=y_{j-1}\quad(j\ge1).
$$

Der Quer-Jacobian ist blockdreieckig mit
Diagonalbloecken $B$ und $B^{-T}$.
Der freie Schwerpunktweg traegt nur
zum oberen rechten Block bei.
Aus $b=x/\lambda$ und
$y_{H-1}=\lambda x$ in einem Eigenvektor
von $B$ folgt

$$
\lambda^{H+2}+\lambda^2-\lambda-1=0.
$$

Fuer ungerades $H$ faktorisiert dies als

$$
(\lambda^2-1)
\left(1+\lambda\sum_{j=0}^{(H-1)/2}\lambda^{2j}\right).
$$

Fuer $H\ge3$ ist die zweite Klammer bei
$-3/4$ negativ und bei null positiv.
Sie liefert eine reelle Wurzel
$-3/4<\lambda_*<0$ und damit in
$B^{-T}$ einen Faktor mit Betrag
$|1/\lambda_*|>4/3$ pro Write.
Der Eigenvektor kann nicht nur unsichtbare
Speicherimpulse tragen: Aus
$P_b^{\rm neu}=P_x-P_b$ und
$P_x^{\rm neu}=P_{H-1}+P_b$ wuerde
$P_x=0$ auf diesem Zweig $P_b=0$,
dann $P_{H-1}=0$ und durch den Shift
alle uebrigen Impulse null erzwingen.
Die Verstaerkung erreicht also die
Kopfgeschwindigkeit. Beide Halbzyklen
haben denselben Querblock, sodass
die volle Periode einen Faktor
groesser als $16/9$ besitzt, nicht
bloss einen neutralen Symmetriemodus.
Fuer $H=1$ liefert dieser Beweis
keine exponentielle Instabilitaet und
auch keinen Stabilitaetspass.

## 4. Grenze einer schwingenden Kernel-Amplitude

Ersetze die Feder durch ein glattes Zentralpotential
$V(u,a)$ mit $u=|x-b|^2/2$ und einer internen skalaren
Amplitude $a$ mit eigener Hamilton-Dynamik und
Rueckwirkung durch $V$. Die Amplitude kann am zweiten
Schnitt eine andere Phase haben. Die Schreibkarte
laesst sie und ihren Impuls unveraendert. Die Massen,
der autonome Rotor und die passiven Register bleiben.
Die Aussage ist bedingt: Es muss bereits eine
kollineare Austauschbahn mit $x-b=\ell(t)\hat A$,
$\ell(T)=-\ell(0)\ne0$ und
$\dot\ell(0)=\dot\ell(T)=0$ je Flug geben.
Es wird keine solche Bahn fuer ein beliebiges $V$ behauptet.

Eine Querauslenkung $z$ der Relativkoordinate aendert
$u$ und den Antrieb von $a$ in erster Ordnung nicht.
Auch der Schreib-Energiesprung ist quer gerade.
Deshalb aendern sich weder die innere Phase noch die
Rotorflugzeit in erster Ordnung quer. Entlang der
Grundbahn gilt

$$
\ddot z+\frac{2}{m}\partial_u V(u(t),a(t))z=0.
$$

Die Auslenkung $\ell(t)$ selbst erfuellt genau diese
lineare Gleichung mit dem Koeffizienten der Grundbahn.
Sie ist die Quervariation einer infinitesimal gedrehten
Bahn. In Koordinaten $(z,p_z)$ mit $p_z=m\dot z/2$
hat die Flugmatrix daher die erste Spalte $(-1,0)^T$.
Die Wronski-Determinante ist eins, weil die Gleichung
keine erste Ableitung enthaelt. Damit hat der Flug die Form

$$
\begin{pmatrix}-1&\beta\\0&-1\end{pmatrix}.
$$

Die Wirkung der zeitlichen Modulation auf den Querflug
sitzt damit in der Scherung $\beta$. Die Querimpulse
von Kopf und Traeger werden mit unveraendertem
Schwerpunktimpuls weiter vertauscht. Der volle
Schreibschritt hat daher dieselben Diagonalbloecke
$B$ und $B^{-T}$ wie vorher. Auch bei verschiedenen
Scherungen in beiden Fluegen behaelt das Produkt
$B^2$ und $(B^{-T})^2$. Die Verstaerkung groesser als
$16/9$ pro Paar von Writes bleibt unveraendert.
Bei einer periodisch wiederkehrenden Grundbahn ist
dies ein Floquet-Multiplikator im Sinn der
[Variationsmethode von Floquet](https://numdam.org/articles/10.24033/asens.220/).

Die Rechnung schliesst keine nichtkollineare Bahn aus
und sagt nichts ueber Phasenaenderungen, die den
Austausch selbst veraendern. Sie zeigt aber, dass
eine Suche nur in Frequenz, Phase und Modulationstiefe
diesen Zweig nicht stabilisieren kann, solange sie in
derselben Austauschklasse bleibt. Der naechste Test
ist daher eine konservative Memory-Kraft, bei der
mindestens ein gespeicherter Abstand im Querblock
mitwirkt. Ob sie die Rueckkehr erhaelt und die
wachsende Mode verschiebt, bleibt offen.

## 5. Reichweite und Kontrollen

Der Vergleich trennt drei Fragen, die ein
rein energetischer Test nicht trennt:
exakte Wiederkehr, fortlaufende Praeparation
und Stabilitaet gegen Rueckstoesse. Dieselbe
konservative Regel kann die ersten zwei auf
einer vorbereiteten Bahn erfuellen und am
dritten scheitern. Andere Rueckfuehrungen
oder eine wirkliche Memory-Kraft sind
davon nicht ausgeschlossen. Der naechste
Test muss die Querimpulsantwort aendern,
ohne die Taetigkeit des Takts wieder von
aussen vorzugeben.

[Woods, Silva und Oppenheim](https://arxiv.org/abs/1607.04591)
verwenden einen dynamischen Takt in einem
anderen, bereits quantisierten Hamiltonmodell.
Das ist ein methodischer Vergleich zur
internen Uhr, kein Beleg fuer die klassische
FIFO-Grenzflaeche oder eine Quantenentstehung.

[Code](../../experiments/current/reference/fifo_carrier_clock_cycle.py)
und [feste Kontrollen](../../tests/test_fifo_carrier_clock_cycle.py)
pruefen zwei exakte vorbereitete Writes,
einen fest verstimmten Takt und die
transverse Ableitung der vollen Rueckkehr.
Der Ausschluss fuer alle ungeraden
$H\ge3$ folgt aus dem Polynom, nicht
aus einem Horizontscan oder einem
numerischen Ziellauf.

Eine [reziproke Kraft aus dem FIFO-Zentrum](fifo_memory_center_cycle_2026-11-24.md)
laesst die Speichereintraege im Querblock mitwirken. Sie erhaelt
die vorbereitete Zweiperiode, zeigt aber einen neuen instabilen
Ortsmodus fuer alle kompatiblen konvexen Zentren mit positivem
Gewicht des juengsten Eintrags.
