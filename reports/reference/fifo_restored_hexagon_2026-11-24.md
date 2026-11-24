# Das FIFO-Sechseck nach Bindung der freien Speichermode

Stand: 2026-11-24. Fortsetzung des
[exakten Sechsecks mit zwei Kraftprofilen](fifo_two_center_hexagon_2026-11-24.md).
Die reversible Schreibkarte und der autonome Rotor bleiben gleich.
Keine native Zieltrajektorie und kein Scan.

**Ergebnis.** Eine zusaetzliche konservative Kraft kann die
letzte freie interne Koordinate binden, ohne das treue
FIFO-Sechseck an den Schnitten zu aendern. Bei alleiniger
Aenderung dieser Mode muss sie dafuer ganze Perioden je
Write vollenden. Das eliminiert den grossen Driftbeitrag
in der Querableitung, laesst aber eine reelle wachsende
Kopierfehlermode mit Betrag zwischen $6/5$ und $5/4$
pro Write bestehen. Eine analytische Kompensationsbedingung
zeigt, wie mehrere nichtganzzahlige Speicherphasen
das alte Rueckkehrproblem anders schliessen koennten.

## 1. Bindung ohne festen externen Anker

In Registerordnung $(x,y_0,y_1,y_2,b)$ sei
$R=\operatorname{diag}(1/m,1/\mu,1/\mu,1/\mu,1/m)$
die inverse Massenmatrix und $\nu=\mu/m$.
Der Kovektor

$$
g=(-1/2,\ 1+\nu,\ -1-2\nu,\ 1+\nu,\ -1/2)^T
$$

ist translationsinvariant und in der Massenmetrik
orthogonal zu den drei bisherigen Oszillatormoden.
Der Zusatz

$$
U_g=\frac{\Omega_g^2}{2\,g^TRg}\,|g^Tq|^2
$$

ist positiv und rotationsinvariant. Er gibt der
alten freien internen Richtung die Frequenz $\Omega_g$,
ohne die gemeinsame Translation festzuhalten.
Die beiden bisherigen Speichermoden machen weiterhin
bei $T=\pi/(3\omega)$ einen bzw. zwei volle Umlaeufe.
Ist $\Omega_g T=2\pi k$ mit ganzzahligem $k\ge1$,
kehrt auch die neue Mode nach dem Flug exakt zum
Startzustand zurueck. Die Translation driftet auf
dem vorbereiteten Sechseck nicht, weil der
Gesamtimpuls null ist. Der interne Flug schliesst
daher dieselbe Registerbahn wie bisher. Die Energie
vor und nach dem Write ist gleich, weil der
ankommende Zustand nur gedreht wurde und der Flug
die neue interne Energie erhaelt. Der Rotor behielt
seinen Anfangsimpuls; die Zeiten wurden nicht von
aussen nachgestellt.

## 2. Wann ein anderer Phasenabgleich ueberhaupt moeglich ist

Behalte das starre, treue Sechseck mit dem Drehfaktor
$\lambda=e^{i\pi/3}$ je Write und dem relativen Flug
$\omega T=\pi/3$ bei. Setze $D=P_x-P_b$.
Der relative Ortsabstand $d$ und sein ankommender
Impuls muessen von Schnitt zu Schnitt ebenfalls um
$\lambda$ drehen. Aus dem Flug folgt
$D^+=D=i m\omega d$. Die Impulskarte erzwingt daher
$P_{y_2}=-P_b$.

Sei $\Delta_j=P_{y_j,n+1}-P_{y_j,n}^+$ der
Impulsgewinn des $j$-ten Registers in einem Flug.
Rotation und Shift liefern
$\lambda P_{y_0}=P_b+\Delta_0$,
$\lambda P_{y_1}=P_{y_0}+\Delta_1$ und
$\lambda P_{y_2}=P_{y_1}+\Delta_2$.
Mit $\lambda^3=-1$ bleibt als notwendige Bedingung

$$
\Delta_0+\lambda\Delta_1+\lambda^2\Delta_2=0.
$$

Bleiben die beiden alten Speichermoden auf ganzen
Perioden, kann nur die neue Mode netto Impuls
abgeben. Ihre Registerkomponente in dieser Gleichung
hat den Koeffizienten
$(1+\nu)(1+\lambda^2)+(-1-2\nu)\lambda=-\nu\lambda$,
der bei endlichen Massen nicht verschwindet. Also
muss auch sie ihren Anfangsimpuls exakt behalten.
Ihr Ortsanteil unmittelbar nach dem Write ist
$-\nu\lambda^{-1}x\ne0$ bei Mittelpunkt null und
muss wegen der treuen Historie ebenfalls zurueckkehren.
Eine angeregte harmonische Mode kann beides nur
bei einer ganzen Periodenzahl tun. Diese Aussage
erlaubt sogar andere vorbereitete Impulse, solange
die Schnittorte, Drehung und alten Phasen gleich bleiben.

Allgemeiner lasse einen Satz massenorthogonaler
Speichermoden in $(c,y_0,y_1,y_2)$ zu, wobei das
relative $d$ unveraendert entkoppelt bleibt.
Eine Mode mit reellem Kovektor $a_\ell$ und
Registerteil $(a_{\ell 0},a_{\ell 1},a_{\ell 2})$
hat $\kappa_\ell=a_{\ell 0}+\lambda a_{\ell 1}+
\lambda^2 a_{\ell 2}$. Ihr Koordinatenwert direkt
nach dem Write ist $x\overline{\kappa_\ell}$.
Bezeichne mit $N_\ell=a_\ell^T R_z a_\ell$ ihre
inverse modale Masse, mit $R_z$ der inversen
Massenmatrix im Schwerpunkt-Speicher-Teil.
Ist $\sin(\Omega_\ell T)\ne0$, verlangt identische
Position an beiden Flugenden einen modalen
Startimpuls $(\Omega_\ell/N_\ell)\tan(\Omega_\ell
T/2)x\overline{\kappa_\ell}$. Der Endimpuls ist
das Negative davon. Eine ganze Periode gibt keinen
Nettoimpuls; eine ungerade Halbperiode setzt
$\kappa_\ell=0$ voraus und traegt daher nichts zur
obigen Shift-Bedingung bei. Sie reduziert sich somit zu

$$
\sum_{\ell:\,\sin(\Omega_\ell T)\ne0}
\frac{\Omega_\ell}{N_\ell}\,
|\kappa_\ell|^2\,\tan(\Omega_\ell T/2)=0.
$$

Sofern angeregte Moden ausserhalb ganzer Perioden
mitwirken, muessen mindestens zwei Beitraege
entgegengesetztes Vorzeichen haben. Das ist ein
notwendiger Phasenausgleich, noch kein ausreichender
Existenz- oder Stabilitaetsnachweis.

## 3. Was von der Querinstabilitaet uebrig bleibt

Am planaren Sechseck hat eine senkrechte Stoerung
weiterhin in erster Ordnung keine Wirkung auf die
Rotorzeit. Bei den vollen Perioden sind alle
Speichermoden im Flug an den Schnitt zurueckgekehrt.
Ausser dem relativen Oszillator bleibt nur die
freie gemeinsame Translation. Deren Drift aendert
die Eigenwerte nicht: Gemeinsamer Impuls ist
erhalten, und die Positionsdrift zeigt nur in die
Translationsrichtung. Auf dem Unterraum mit
Gesamtimpuls null ist sie ohnehin null.

In Einheiten $m=\omega=1$ sei $P$ der
orthogonale Projektor auf $(1,0,0,0,-1)^T$,
$U=I-P/2$, und $(C,G)$ der Orts- und Impulsblock
des Writes mit $G=C^{-T}$. Ohne den
Translationsdrift ist der Querblock aehnlich zu

$$
\begin{pmatrix}
UC & \tfrac34 PG\\
-PC & UG
\end{pmatrix}.
$$

Hier wurden die Impulse durch $\sin(\pi/3)$ geteilt.
Mit $u=\xi+\xi^{-1}$ fuer einen Eigenwert $\xi$ hat sein
charakteristisches Polynom die reziproke Form

$$
\xi^5(u-2)(u-1)(u^3+u^2-2u+1/4).
$$

Reziproke reduzierte Polynome sind ein bekanntes
Werkzeug fuer die
[lineare Hamilton-Stabilitaet](https://www.sciencedirect.com/science/article/pii/037596018790836X).
Hier entsteht der konkrete rationale Ausdruck
aus Write und relativem Flug. Die kubische Klammer
ist bei $u=-41/20$ negativ und bei $u=-61/30$
positiv. Damit besitzt der volle Return einen
reellen negativen Einzelschritt-Multiplikator
$-5/4<\xi<-6/5$. Das Ergebnis ist fuer
jede zugelassene ganze Periode der Zusatzmode gleich.
Nach sechs Writes waechst dieser Modus um mehr
als $(6/5)^6$.

Die Mode beeinflusst die Kopie selbst: Hielte ein
Eigenvektor mit $|\xi|>1$ den Kopierfehler
null, bliebe der Mittelpunkt beim Write und
Flug unveraendert, also muesste er im Eigenvektor
null sein. Die alten Registerpositionen wuerden
nur verschoben, sodass $b=y_2=\xi^{-3}x=-x$.
Damit verschwinden alle Ortskomponenten.
Wegen $\sin(\pi/3)\ne0$ muss dann auch der
relative Impuls vor und nach dem Write null sein.
Aus $P_{y_2}=\xi^{-3}P_b$ folgt
$(1+\xi^{-3})P_b=0$, also verschwinden
auch alle Impulse. Ein nichttrivialer wachsender
Eigenvektor kann den Kopierfehler daher nicht meiden.

## 4. Kontrolle und naechster Vergleich

[Referenzcode](../../experiments/current/reference/fifo_carrier_clock_cycle.py)
und [Kontrollen](../../tests/test_fifo_restored_hexagon.py)
pruefen zwei volle Wiederkehrfaelle, die Verletzung
der treuen Historie bei einer festen Halbperiodenwahl,
das Polynom mit exakten Bruechen und die volle
autonome Querableitung. Das Sechseck ist erhalten,
aber nicht querstabil. Offen bleibt, ob zwei
gezielt entgegengesetzte Speicherphasen den
Kopierfehler unterdruecken, ohne Rotor und
Historie von aussen zu steuern.

Die [Halbperioden-Konstruktion](fifo_half_turn_hexagon_2026-11-24.md)
aendert die Kraftprofile und laesst eine Mode bei Ortswert
null netto Impuls umkehren. Sie erhaelt die Historie, ist
aber fuer jedes positive Massenverhaeltnis quer instabil.
