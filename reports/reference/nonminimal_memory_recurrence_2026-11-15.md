# Nichtminimale Memory: native Regeneration vor Stabilitaet

Stand: 2026-11-15. Dynamische Fortsetzung des
[statischen Vorzeichennachweises](nonminimal_memory_defects_2026-11-15.md).
Eigene analytische Existenzpruefung und feste Codekontrollen;
keine Zieltrajektorie, kein Gain-Fit und keine Parametersuche.

## Befund

Die konstruierte negative Defektstruktur ist weiterhin ein gueltiger
gefuellter Memory-Zustand. Ihr Ringschluss macht sie aber nicht zu einem
nativen periodischen Orbit. Fuer die naheliegende Wiederholung der
zweischaligen Tetraederfolge gilt jetzt:

- Bei **gleichem skalarem und vektoriellem Vergessen**, rauschfreiem
  Alignment und Horizonten aus ganzen Achtperioden ist der Umlauf
  unmoeglich. Das gilt fuer beliebige innere/aeussere Radien, positive
  Gaussbreite und **jeden konstanten reellen Vektorgain**. Auch ein
  beliebiger glatter radialer skalarer Kernel kann ihn nicht herstellen.
- Fuer den festen Zeugen a=1, b=5, sigma_vector=1 und q=99/100 ist die
  groessere der beiden phasenspezifischen Ein-Schritt-Abweichungen strikt
  groesser als 7/3. Ein besserer Gain-Fit schliesst diese Luecke nicht.
- Getrenntes Vergessen ist nicht allgemein ausgeschlossen. Fuer
  denselben geometrischen Zeugen erzwingt bereits eine notwendige
  Tangentialbedingung jedoch skalare Retention s<1/4000, waehrend
  die vektorielle Retention q=99/100 betraegt. Das ist **kein**
  vollstaendiger Existenzbefund und keine gewaehlte Modellkalibrierung.

Die Huerde liegt vor jeder Floquet- oder Lebensdauerpruefung. Sie
widerlegt weder den statischen Defektbeweis noch alle nichtminimalen
Memory-Traeger, deformierte Orbits, nichtperiodische gebundene Zustaende
oder kollektive Dynamik. Insbesondere folgt daraus kein Bedarf an einem
externen QFT-Feld. Paper I und die Produktionsregeln bleiben unveraendert.

## 1. Genau gepruefte native Klasse

Die implementierte Bewegung ist bei epsilon=0

$$
x^+=x-\eta_s\nabla\Phi(x)+\eta_v V(x).
$$

Neue Einheitsrichtungen folgen aus dem tatsaechlichen Inkrement;
anschliessend werden Position und Richtung in die FIFO-Historien
eingeschoben. Der skalare Double-Gaussian-Kernel samt isotroper
Gaussdeposition ist radial. Fuer den Ausschluss darf er sogar durch
einen beliebigen glatten radialen Kernel ersetzt werden, ohne dadurch
eine neue native Regel einzufuehren: Die groessere Vergleichsklasse
erfuellt dieselbe hier benoetigte algebraische Identitaet.
Gemeint ist weiterhin der additive native Quellenreadout, also eine
Kraft der Form

$$
S(x)=c_s\sum_{j=0}^{H_s-1}s^j
f(|x-y_j|^2)(x-y_j),
$$

mit radialer Koeffizientenfunktion f und konstantem c_s; keine
beliebige nichtlineare Funktion der gesamten Historie.

Schreibe q=1-lambda_vector und s=1-alpha. Zunaechst gilt
0<q=s<1. Das entspricht auch der bestehenden Code-Voreinstellung
lambda_vector=None; unabhaengige Faktoren sind ebenfalls implementiert,
werden aber erst in Abschnitt 5 behandelt.

Seien v_i die vier Einheits-Tetraederecken des vorigen Berichts,
0<a<b und sigma=sigma_vector>0. Zwei Repraesentanten der durch
zyklische Tetraedersymmetrie verknuepften Historienphasen sind, neueste zuerst,

$$
Y_N=(av_0,bv_0,av_1,bv_1,av_2,bv_2,av_3,bv_3,av_0),
$$

$$
Y_F=(bv_0,av_1,bv_1,av_2,bv_2,av_3,bv_3,av_0,bv_0).
$$

Die zur **Wiederholung dieser Folge** erforderlichen Inkremente sind

$$
d_N=bv_3-av_0,\qquad d_F=(a-b)v_0.
$$

Die Tetraederpermutation ist hier eine orthogonale Symmetrie, keine
Behauptung eines kontinuierlichen Rotationsorbits oder eines Spins.

Die Radien a=1,b=5 gehoeren zum statischen Zeugen; der Ausschluss unten
gilt fuer die ganze angegebene Zweischalenfamilie. H_s=8m_s und
H_v=8m_v mit positiven ganzen m_s,m_v sind erlaubt. Eine weitere
vollstaendige Periode multipliziert jeweils alle acht
Phasengewichte mit demselben positiven Faktor. Fuer den Vektorkanal ist
der aggregierte Kopfkoeffizient

$$
\widehat w_0=\lambda_v M_v\sum_{k=0}^{m_v-1}q^{8k}.
$$

Kein gleicher skalarer/vektorieller Horizont oder gleicher Gain wird
vorausgesetzt. **Horizonte mit unvollstaendiger letzter Achtperiode
fallen nicht unter den Ausschluss.** Auch die tatsaechliche Berechnung
des Horizonts aus memory_factor und max_memory darf bei einem spaeteren
Modellvergleich nicht uebersprungen werden.

## 2. Eine Projektion entfernt den ganzen radialen Skalarbeitrag

Setze t=q^2 und

$$
h(q)=\frac{\sqrt3}{2}
\left(1,-\frac{1+t}{t},\frac1t\right).
$$

Direkte Tetraederalgebra ergibt

$$
h\cdot v_0=0,\quad h\cdot v_1=1,\quad
h\cdot v_2=-\frac{1+t}{t},\quad h\cdot v_3=\frac1t,
\qquad
|h|^2=\frac{3(1+t+t^2)}{2t^2}.
$$

Insbesondere annihiliert h auch

$$
T(q)=q^2v_1+q^4v_2+q^6v_3.
$$

Die drei nicht ausgerichteten Ecken jeder Schale haben zum aktuellen
Punkt jeweils denselben Abstand. In der nahen Phase sind ihre
Altersgewichte proportional zu q^(2i) beziehungsweise q^(2i+1),
in der fernen Phase zu q^(2i) beziehungsweise q^(2i-1).
Damit liegt **jede** radiale skalare Kraft beider Phasen in
span(v_0,T(q)); die ausgerichtete Gegenposition traegt nur radial bei.
Also unabhaengig von Kernelradien, Amplituden und skalarem Gain:

$$
h\cdot S_N=h\cdot S_F=0,\qquad S=-\eta_s\nabla\Phi.
$$

Dies ist kein Kraftgleichgewichts- oder Energiesatz, sondern eine
konkrete lineare Projektion der benoetigten Existenzgleichungen.

## 3. Zwei native Vektorprojektionen sind unvertraeglich

Definiere die Schrittnorm und Gaussfaktoren

$$
\ell=\sqrt{a^2+b^2+2ab/3},\quad
g_R=e^{-(b-a)^2/(2\sigma^2)},\quad
g_X=e^{-\ell^2/(2\sigma^2)},\quad
g_F=e^{-4b^2/(3\sigma^2)}.
$$

Die nahen gerichteten Depositionen sind -v_i, die fernen
(bv_i-av_(i+1))/ell. Mit den unveraenderten Altersgewichten folgt

$$
h\cdot V_N=-\widehat w_0\beta_N,\qquad
h\cdot V_F=-\widehat w_0\beta_F,
$$

$$
\beta_N=\frac{qa}{\ell}(g_R-g_X)>0,\qquad
\beta_F=\frac{a}{\ell}(1-g_F)>0.
$$

Zum Nachrechnen: Die alten gleichabstaendigen Gruppen verschwinden
unter h, weil h dot T(q)=0. Fuer die versetzt indizierten Richtungen
bleibt Summe von i=1 bis 3 q^(2i) h dot v_(i+1)=-1. Die aktuelle
fern gerichtete Deposition hat dagegen ihre eigene Gaussamplitude.
Genau deren Differenz erzeugt die beiden obigen nichtverschwindenden
Terme. Dies beruecksichtigt die aus der Bahn abgeleiteten Richtungen,
nicht ein eingefrorenes unabhaengiges Orientierungsfeld.

Setze $C=\eta_v\widehat w_0$. Notwendig waeren gleichzeitig

$$
-C\beta_N=\frac{b}{q^2},\qquad -C\beta_F=0.
$$

Da beide beta positiv sind, ist dies unmoeglich. Schon die nahe Phase
scheitert fuer eta_v>=0: Die erforderliche Projektion ist positiv,
die native nichtpositiv. Ein negativer Gain koennte diese einzelne
Projektion bedienen, scheitert aber an der fernen Phase.

**Somit existiert in dieser Klasse kein exakter Achtzyklus**, fuer
jeden endlichen konstanten reellen Gain. Seine hypothetische Stabilitaet
zu berechnen waere daher nicht zielfuehrend.

## 4. Endliche Residualschranke statt blossem Ungleichheitszeichen

Fuer die beiden nativen Inkrementfehler
r_N=S_N+eta_v V_N-d_N und r_F=S_F+eta_v V_F-d_F gilt exakt

$$
\beta_F h\cdot r_N-\beta_N h\cdot r_F
=-\frac{b\beta_F}{q^2}.
$$

Dreiecksungleichung und Cauchy-Schwarz liefern daher

$$
\max(|r_N|,|r_F|)
\ge\frac{b\beta_F}{q^2|h|(\beta_F+\beta_N)}>0.
$$

Hier wurde kein optimaler Gain gesucht. Die Identitaet eliminiert ihn
fuer alle Werte gleichzeitig. Fuer a=1,b=5,sigma=1,q=99/100 gilt
g_R=exp(-8), g_X=exp(-44/3) und g_F=exp(-100/3). Aus exp(4)>50 folgt

$$
\frac{\beta_N}{\beta_F}
=\frac{q(g_R-g_X)}{1-g_F}<\frac1{2499},\qquad
q^2|h|<\frac3{\sqrt2}.
$$

Somit

$$
\max(|r_N|,|r_F|)
>\frac{5\sqrt2}{3}\frac{2499}{2500}>\frac73.
$$

Die letzte Ungleichung reduziert sich nach Quadrieren auf
$50\cdot2499^2>49\cdot2500^2$. Die positive Taylor-Teilsumme von
exp(4) bis k=7 ist groesser als 50. Beides wird rational geprueft.

Die Schranke betrifft **die Inkremente an genau diesen beiden
Historienphasen**. Ohne kontrollierte Parameterschranken und einen
vollstaendigen History-Jacobian ist sie keine gainunabhaengige
Ausschlussumgebung fuer alle benachbarten deformierten Orbits.

## 5. Was getrenntes Vergessen wirklich aendert

Hier wieder der feste geometrische Zeuge a=1,b=5,sigma=1,q=99/100,
aber 0<s<1 im skalaren Kanal; weiterhin Horizonte aus ganzen Perioden.
Sei P=I-v_0v_0^T, e_i=P v_i und

$$
T_\perp(s)=\sum_{i=1}^3s^{2i}e_i
=s^2(1-s^2)\big[(1+s^2)e_1+s^2e_2\big].
$$

Jede skalare Tangentialkraft ist proportional zu T_perp(s). Der
Vektorkanal in der fernen Phase liefert dagegen

$$
\frac{PV_F}{\widehat w_0}
=A_F T_\perp(q)-\beta_F e_1,\qquad
A_F=\frac{g_F}{\ell}(5-q^{-2})-\frac{g_X}{q}<0.
$$

Das Vorzeichen folgt bereits aus 5/ell<1, g_F<g_X und 1/q>1.
Bei eta_v=0 scheitert die nahe Phase fuer jedes s: h(s) entfernt
ihre skalare Kraft, aber nicht die erforderliche Projektion b/s^2.
Ein Umlauf braucht daher einen nichtverschwindenden Vektorgain. Weil
der ferne Sollschritt radial ist, muss die obige Vektortangente dann
kollinear mit T_perp(s) sein.

Mit t=q^2, u=s^2 und A=-A_F>0 ist die Determinantenbedingung

$$
-A t(1-t)(t-u)+u\beta_F=0,
\qquad
u=\frac{A t^2(1-t)}{\beta_F+A t(1-t)}.
$$

Sie legt hoechstens einen skalaren Retentionsfaktor fest, ohne bereits
die radialen oder die andere tangentiale Bewegungsgleichung zu loesen.
Wegen 5-q^(-2)>0 gilt A<g_X/q. Zudem sind ell<6,
1-q^2<1/50, g_X<1/2000000 und g_F<1/2500. Daraus folgt

$$
s^2<\frac{\ell g_X q^3(1-q^2)}{1-g_F}
<\frac1{16660000}<\frac1{4000^2}.
$$

Die Schranke fuer g_X wird durch die positive Taylor-Teilsumme von
exp(44/3) bis k=24 abgesichert. Notwendig waere also
alpha=1-s>3999/4000, gegenueber lambda_vector=1/100.
Der Randfall s=0 hilft nicht: Dann wirkt die skalare aktuelle
Selbstdeposition nicht, waehrend die ferne Vektortangente ungleich null ist.

**Diese Bedingung ist keine Empfehlung fuer einen fast vollstaendig
vergessenden skalaren Kanal.** Es wurde weder dieser Wert als nativer
Parameter gewaehlt noch ein Gain, Kernel oder Orbit daran angepasst.
Volle Existenz, Defekterhaltung und Formstabilitaet bleiben ungeprueft.

## 6. Anschluss und Anspruchsgrenzen

Solange die Vektorhistorie aus ganzen Perioden besteht, laesst sich
die benoetigte skalare Querwirkung auch direkt bilanzieren. Mit
L_N=h(q) dot S_N und L_F=h(q) dot S_F verlangt ein Umlauf

$$
\beta_F L_N-\beta_N L_F=\frac{b\beta_F}{q^2}.
$$

Das ist eine notwendige Auswahlbedingung fuer einen vorhandenen
Mechanismus, nicht die Definition einer neuen Kraft. Bei gleichem
Vergessen und ganzen skalaren Perioden ist die linke Seite null.
Unterschiedliches Vergessen oder eine unvollstaendige letzte Periode
koennen diese spezielle Annullierung aufheben; die gesamte native
Existenzgleichung wird dadurch nicht automatisch erfuellt. Der vorhandene
statische Index liefert diesen fehlenden Bewegungsanteil nicht.

Die [aktive Arbeitsreihenfolge](../../docs/status/project_priorities.md)
bleibt massgeblich: keine Gain-/Breiten-Nachsuche in der ausgeschlossenen
Klasse. Getrenntes Vergessen nur als notwendige Bedingung weiterfuehren,
bevor eine Parameterentscheidung oder Stabilitaetsrechnung erwogen wird.
Auch ein spaeterer Orbit muesste Defektlokalisation, native Randbilanz,
volle Formstabilitaet und einen physikalischen Quellen-/Stromanschluss
bestehen. Der im vorigen Bericht gepruefte Literaturbezug betrifft
Defektindizes und statistische Abschirmung, nicht diesen FIFO-Umlauf;
hier wird daraus kein dynamischer Satz importiert.

## 7. Software- und Beweispruefung

`tests/test_nonminimal_memory_recurrence.py` kontrolliert feste
Kraftidentitaeten an beiden Phasen mit den nativen Gewichts-, Kernel-
und Vektorhelfern. Ganze Perioden mit verschiedenen Horizonten,
isotrope Gaussdeposition, eine zweite feste Geometrie und beide
Gainvorzeichen sind algebraische Kontrollen, keine Orbit-/Parametersuche.
Die rationale Absicherung benutzt Fraction-Arithmetik; die kontinuierlichen
Existenzsaetze folgen aus den Projektionen, nicht aus den Stichproben.

27 neue Kontrollen und insgesamt 203 Tests im betroffenen Memory-/
Dokumentationspanel bestanden; ebenso der konfigurierte Ruff-Lint
und der strikte MkDocs-Bau. Keine vollstaendige Repository-Testsuite.
Bei der ersten Testausfuehrung wies der
Validator eine unzulaessige positive Depositionsbreite im Delta-Testfall
zurueck; die Testkonfiguration wurde korrigiert, keine Produktionsregel.
Keine neue Zieltrajektorie, kein Eigenwertlauf und keine nachtraegliche
Teilchenzuordnung. Die Saetze gelten in exakter reeller Arithmetik;
Softwarechecks sind binary64-Kontrollen, kein maschinenverifizierter
Beweis oder unabhaengiger mathematischer Review.
