# Zweischalen-Zeuge: auch getrenntes Vergessen reicht nicht

Stand: 2026-11-16, begonnen am 2026-11-15. Fortsetzung der
[nativen Regenerationspruefung](nonminimal_memory_recurrence_2026-11-15.md).
Geschlossene notwendige Kraftgleichungen und ein endliches rationales
Intervallzertifikat, keine Parameteranpassung oder neue Zieltrajektorie.

## Ergebnis

Der feste nichtminimale Defektzeuge mit a=1, b=5, sigma_vector=1,
q=99/100 und der angegebenen starren Tetraeder-Achtfolge ist **auch
bei getrenntem skalarem Vergessen kein nativer periodischer Orbit**
des vorhandenen rauschfreien Double-Gaussian-/Alignment-Modells, wenn beide
Horizonte ganze Achtperioden enthalten.

Bei getrenntem Vergessen hatte der vorherige Test nur die ferne
Tangentialbewegung geprueft.
Jetzt erzwingt die volle Bilanz beider Phasen eine eindeutige Tabelle
skalarer Kraftkoeffizienten. Diese Tabelle kann **keine reelle Summe
aus zwei Gaussfunktionen** annehmen. Das gilt auch fuer vertauschte
Breiten, beliebige reelle Amplituden, beliebige konstante reelle Gains
und die vorhandene isotrope Gaussdeposition. Es wird also nicht nur
eine bevorzugte attraktive/repulsive Parameterwahl ausgeschlossen.

Der statische -1-Defekt bleibt mathematisch gueltig. Aus seiner
Existenz folgt aber nicht, dass sich die konstruierte Historie
regeneriert. Keine Stabilitaetsrechnung, Kernel-Nachsuche oder
Teilcheninterpretation an diesem Zeugen anschliessen. Der Satz
betrifft **nicht** alle nichtminimalen Memory-Zustaende, andere
Geometrien, andere Vektorbreiten/Retentionsfaktoren, unvollstaendige
Speicherperioden oder nichtperiodische gebundene Strukturen.

## 1. Gemeinsamer Kernel statt unabhaengiger Phasenkraefte

Es gelten die beiden Historienphasen Y_N,Y_F und die erforderlichen
Inkremente d_N=5v_3-v_0, d_F=-4v_0 aus dem vorherigen Bericht.
Die skalaren und vektoriellen Horizonte duerfen unabhaengig H_s=8m_s und H_v=8m_v
sein, mit positiven ganzen m_s,m_v. Die vollstaendigen Perioden
aggregieren nur die jeweiligen Kopfgewichte. Der Vektorreadout
verwendet weiterhin die aus den Positionsdifferenzen abgeleiteten
Einheitsrichtungen, keine unabhaengigen Orientierungsfreiheitsgrade.

Mit s=1-alpha und u=s^2 sind die vier relevanten quadrierten
Abstaende

$$
D_N=\frac83,\qquad D_R=16,\qquad
D_X=\frac{88}3,\qquad D_F=\frac{200}3.
$$

Die ersten drei sind aequidistant, mit Schritt Delta_D=40/3.
N bezeichnet den Abstand verschiedener naher Ecken, R den radialen
Schritt, X den schraeg verbindenden Schritt und F verschiedene ferne
Ecken. Dies sind keine Teilchenlabels oder physikalischen Massen.

Schreibe den nativen skalaren Inkrementanteil nach Aggregation als

$$
S(x)=\sum_{j=0}^7s^j k(|x-y_j|^2)(x-y_j).
$$

Der gemeinsame skalare Gain und das Kopfgewicht sind hier in k
enthalten. Fuer den implementierten Double-Gaussian-Gradienten samt
isotroper Gaussdeposition hat er immer die Form

$$
k(D)=P e^{-rD}+Q e^{-hD},\qquad r,h>0,\quad P,Q\in\mathbb R.
$$

Die Faltung aendert Breiten und Amplituden, nicht die Zahl der zwei
Exponentialterme in D. Auch negative oder verschwindende Amplituden
und gleiche Breiten sind in dieser groesseren Klasse enthalten.
Wir muessen deshalb dieselben Werte k_N,k_R,k_X,k_F in **beiden**
Phasen verwenden; unabhaengig eingestellte Phasenkraefte waeren keine
Loesung des nativen Modells.

## 2. Vollstaendige Vektor- und Skalarbilanzen

Verwende wie zuvor t=q^2, ell=sqrt(88/3),
g_N=exp(-4/3), g_R=exp(-8), g_X=exp(-44/3), g_F=exp(-100/3) und

$$
T(q)=q^2v_1+q^4v_2+q^6v_3,\qquad
W_q=t+t^2+t^3,\qquad W_s=u+u^2+u^3.
$$

Die vollen Vektorfelder, nicht nur ihre Tangentialprojektionen, sind

$$
\frac{V_N}{\widehat w_0}=\rho_Nv_0+A_NT(q)-\beta_Nv_1,
\qquad
\frac{V_F}{\widehat w_0}=\rho_Fv_0+A_FT(q)-\beta_Fv_1,
$$

mit

$$
\begin{aligned}
\beta_N&=\frac q\ell(g_R-g_X),&
\beta_F&=\frac{1-g_F}{\ell},\\
A_N&=-g_N+\frac{qg_X}{\ell}(5-q^{-2}),&
A_F&=\frac{g_F}{\ell}(5-q^{-2})-\frac{g_X}{q},\\
\rho_N&=-1+\frac q\ell(5g_R-q^6g_X),&
\rho_F&=\frac{5-q^6g_F}{\ell}-q^7g_R.
\end{aligned}
$$

Die gemeinsame effektive Vektorkopplung ist $C=\eta_v\widehat w_0$.
Fuer die Skalarbeitraege definiere

$$
K_N=k_N+5s k_X,\qquad K_F=5k_F+k_X/s.
$$

Direkte Summation aller acht Altersbeitraege liefert

$$
S_N=[(k_N+s k_X)W_s-4s k_R]v_0-K_NT(s),
$$

$$
S_F=[5(k_F+k_X/s)W_s+4s^7 k_R]v_0-K_FT(s).
$$

Die zu erfuellenden Gleichungen sind S_N+C V_N/widehat(w_0)=d_N
und S_F+C V_F/widehat(w_0)=d_F. Das folgende Eliminieren ist eine
**notwendige Bedingung im Widerspruchsbeweis**, kein Fit eines
Simulators oder eine Auswahl physikalischer Parameter.

### 2.1 Tangentiale Bedingungen

Die vorherige ferne Tangentialbedingung setzt A=-A_F>0 und erzwingt

$$
u=\frac{A t^2(1-t)}{\beta_F+A t(1-t)},\qquad s=\sqrt u.
$$

Die Faelle C=0 (reiner Skalarfall) und s=0 waren bereits ausgeschlossen.
Setze nun

$$
\delta=A_N-\frac{\beta_N}{\beta_F}A_F,\qquad
J=\frac{\beta_F+A t(1-t)}{u(1-u)}.
$$

Die nahe Tangentialbewegung und die ferne Kollinearitaet bestimmen

$$
C=-\frac{5[\beta_F+A t(1-t)]}
{\beta_F\delta t^2(1-t)},\qquad K_F=-CJ,
$$

$$
K_N=\frac{5A[\beta_N-A_Nt(1-t)]}
{\beta_F\delta u^2(1-u)}.
$$

Das Zertifikat unten schliesst delta=0 aus und bestaetigt alle
Divisionen; es wird kein kleiner Nenner stillschweigend verworfen.

### 2.2 Radiale Bedingungen und gemeinsame Krafttabelle

Die radialen Vektorkomponenten sind

$$
R_N^v=\rho_N-A_NW_q/3+\beta_N/3,\qquad
R_F^v=\rho_F-A_FW_q/3+\beta_F/3.
$$

Aus v_0 dot d_N=-8/3 und v_0 dot d_F=-4 folgen

$$
L=\frac{(4/3)K_NW_s+C R_N^v+8/3}{4s}
=k_R+W_s k_X,
$$

$$
M=\frac{-4-(4/3)K_FW_s-C R_F^v}{4}
=\frac{W_s}{s}k_X+s^7k_R.
$$

Damit sind die vier notwendigen Kraftwerte eindeutig:

$$
k_X=\frac{M-s^7L}{W_s/s-s^7W_s},\quad
k_R=L-W_sk_X,\quad
k_N=K_N-5sk_X,\quad
k_F=(K_F-k_X/s)/5.
$$

Der erste Nenner ist W_s(1-s^8)/s>0. Auch hier sind keine
unabhaengigen Nah-/Fernkernel erlaubt; k_R und k_X werden jeweils
in beiden Phasen benutzt.

## 3. Rational abgesicherte notwendige Werte

Das feste Zertifikat ergibt folgende **strikten** Einschliessungen:

| Groesse | Untergrenze | Obergrenze |
| --- | ---: | ---: |
| s | 211/1000000 | 212/1000000 |
| C | 992 | 993 |
| k_N | -116000000 | -115000000 |
| k_R | -882000 | -881000 |
| k_X | -872000 | -871000 |
| k_F | 4130000 | 4140000 |

Die Werte sind aus den notwendigen Gleichungen erzwungen, **keine
vorgeschlagenen Kopplungen oder Kraftparameter**. Der entscheidende
Inkompatibilitaetstest benoetigt weder ihre langen Dezimaldarstellungen
noch einen Eigenwertlauf. Schon die groben ganzzahligen Schranken geben

$$
k_N<0<k_F,\qquad
k_R^2-k_Nk_X
<882000^2-115000000\cdot871000<0.
$$

Verfahren und Vertrauensbasis:

- Fuer exp(-x), x in {4/3,8,44/3,100/3}, wird die positive Taylor-
  Teilsumme S_160 fuer exp(x) rational gebildet. Der Rest ist durch
  den Term x^161/161! geteilt durch 1-x/162 nach oben beschraenkt. Invertieren liefert eine
  Einschliessung fuer exp(-x).
- Quadratwurzeln werden mit ganzzahligem isqrt und rationalen Unter-/
  Obergrenzen eingeschlossen. Nach jeder elementaren Operation werden
  die Grenzen **nach aussen** auf das Gitter 10^(-40) gerundet, mit
  exakter Fraction-/Ganzzahlarithmetik. Keine binary64-Rundung traegt
  das Zertifikat.
- Jede Division prueft den Ausschluss von null im Nennerintervall.
  Die Arithmetik hat eigene Endpunkt-, Rundungs- und Fehlerkontrollen.
  Keine automatische Praezisionssteigerung oder Wiederholung.

Eine vorbereitende Decimal-Auswertung diente nur der Algebra-Kontrolle.
Der erste Versuch mit optionalem mpmath scheiterte vor der Rechnung am
Import; es wurde nichts installiert. Die bewiesenen Vorzeichen folgen
aus dem anschliessenden rationalen Zertifikat, nicht aus dieser Vorschau.

## 4. Warum keine zwei Gaussfunktionen diese Tabelle liefern

Sei k(D)=P exp(-rD)+Q exp(-hD). Absorbiere die positiven
Exponentialfaktoren bei D_N in a_0 und b_0 und setze
z=exp(-r Delta_D), w=exp(-h Delta_D). An den drei aequidistanten
Abstaenden gilt dann exakt

$$
k_N=a_0+b_0,\quad k_R=a_0z+b_0w,\quad
k_X=a_0z^2+b_0w^2,
$$

$$
k_R^2-k_Nk_X=-a_0b_0(z-w)^2.
$$

Die strikt negative linke Seite erzwingt a_0 b_0>0 und z ungleich w.
Weil k_N<0, muessen **beide** Koeffizienten negativ sein. Dann ist
k(D)<0 fuer jeden endlichen Abstand, im Widerspruch zu k_F>0.
Gleiche Breiten oder ein verschwindender Term liefern stattdessen
Determinante null und sind ebenfalls ausgeschlossen.

Dies ist eine elementare exakte Zwei-Term-Identitaet, keine
heuristische Aussage ueber einen ungluecklich gewaehlten Kernel.
Ein anderer konstanter Gain, eine andere Double-Gaussian-Breite oder
Gaussdeposition kann den Widerspruch nicht beheben. Fuer mehr als
zwei Exponentialterme gilt dieses Argument nicht; daraus folgt aber
kein nachgewiesener Orbit und keine Freigabe fuer einen dritten Term.

## 5. Kontrollen, Konsequenz und offene Zielsetzung

`tests/test_nonminimal_kernel_obstruction.py` umfasst das rationale
Zertifikat, die exakte Zwei-Term-Identitaet und unabhaengige Kontrollen
an **allen acht Historienphasen**. Dort wird der vorhandene native
Vektorreadout benutzt; nur zum Gegenpruefen der notwendigen Gleichungen
wird die formale Vierwerttabelle eingesetzt. Sie wird weder als neuer
Kernel gespeichert noch in eine Simulationsregel uebernommen. Ihr
Bestehen der algebraischen Bewegungsbilanz ist gerade **kein nativer
Existenzpass**, weil Abschnitt 4 ihre Kernelrealisierung ausschliesst.

20 neue Kontrollen und insgesamt 223 Tests im betroffenen Memory-/
Dokumentationspanel bestanden, ebenso der konfigurierte Ruff-Lint
und der strikte MkDocs-Bau. Keine vollstaendige Repository-Testsuite. Kein
maschinenverifizierter Beweis oder unabhaengiger mathematischer Review.
Die Ergebnisse gelten in exakter reeller Arithmetik; die zusaetzlichen
binary64-Kraftchecks sind nicht die Quelle des Ausschlusszertifikats.

Die [Projektprioritaeten](../../docs/status/project_priorities.md) bleiben
die einzige aktive Arbeitsreihenfolge. Dieser feste Zweischalen-Zeuge
ist damit als **statisches Existenzbeispiel, nicht als nativer
Ladungstraeger** abgeschlossen. Ihn nicht durch neue Parameter,
periodenweise geschaltete Gains oder einen weiteren Kernelterm retten.
Fuer den offenen Memory-Anschluss bleibt ein nativ regenerierter,
raeumlich kontrollierter nichtminimaler Zustandsbereich erforderlich;
statische Indexexistenz, volle Dynamik und physikalische Quellenwirkung
sind weiterhin gemeinsam zu pruefen. Der Ausschluss begruendet weder
elektrische Ladung noch die Notwendigkeit zusaetzlicher QFT-Felder.
