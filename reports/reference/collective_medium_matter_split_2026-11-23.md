# Frei bewegliche Materie und verankerte Antwort im FIFO-Wellenmedium

Stand: 2026-11-23. Lineare Vergleichsmodelle nach dem
[Selbstkopplungstest](collective_accumulated_feedback_2026-11-23.md).
Der Feld-/Materie-Port und die Verankerung werden als getrennte
Referenzen gesetzt, nicht aus dem nativen Mehrknotensystem
abgeleitet. Keine neue Zieltrajektorie.

**Ergebnis.** Eine eigene frei bewegliche Materiepopulation
beseitigt die Langwelleninstabilitaet nicht. Wird sie ueber
den vorhandenen diffusionsartigen Dichte-Update gekoppelt,
entsteht eine andere Wachstumsrate, proportional zu
$k^{2/3}$ statt einem konstanten Grenzwert. Verankerte
Materie kann dagegen bei endlicher Rueckwirkung einen
statischen $1/k^2$-Pol und gedaempfte Wellen behalten.
Innere Bindung eines frei beweglichen, massenproportional
gekoppelten Knotens liefert diese Verankerung nicht.

## 1. Zwei Populationen, keine direkte Selbstanziehung

Uebernehme aus dem
[Dichte-/Richtungsabschluss](collective_directional_current_2026-11-22.md)
den kritischen Richtungsport $g_0\chi=1$, den skalaren
Koeffizienten $b_s<0$, $C=\epsilon^2+b_s>0$ und
$A=1+\bar j_v$. Fuer $k>0$ ist die Feld-Auslese
$\Phi=u/k^2$. Die Traeger der Dichte u werden nicht
unmittelbar durch $\Phi$ angetrieben. Stattdessen schreibt
eine getrennte Materievariation w ueber den bisherigen
skalaren Quellport $s=s_{\rm ext}+q w$, mit $q>0$.
Nur diese Materie liest den rekonstruierten Gradienten
mit Mobilitaet $\mu>0$. Transport und Quelle sind damit
rueckgekoppelt, aber kein aus einem Hamiltonian gewonnener
gemeinsamer Kraftport.

Mit dem alten Determinanten $D(k,z)$ liefert der
[exakte Quelltransfer](collective_accumulated_current_2026-11-22.md)

$$
D(k,z)u=-p(k) k^2 b_s(k)z(s_{\rm ext}+q w).
$$

Fuer den Materieblock schreibe
$ (z-r(k))w=\mu M(k)u $.
Dabei kommt der Faktor u aus dem Dichtefaktor
$k^2\Phi$, nicht aus nichtkonservativer Quelleninjektion.
Die gemeinsame Determinante ist dann

$$
D_{\rm mix}(k,z)=(z-r(k))D(k,z)
                 +q\mu M(k)p(k)b_s(k)zk^2 .
$$

Im Folgenden gilt $M(0)=1$. Bezeichne
$\nu=-q\mu b_s>0$. Die Ergebnisse unterscheiden sich
danach, ob $r(k)$ bei $k=0$ gegen eins geht oder nicht.

## 2. Frei verschiebbare Materie: wachsende Mode

Fuer einen diffusionsartigen, rauschglatteten Materialschritt
$+\mu ik\Phi$ ist $r(k)=M(k)=p_m(k)=e^{-D_m k^2}$ mit
$D_m>0$. Das folgt aus derselben ersten Variation des
Dichtetransports wie beim nativen skalar getriebenen Kopf.
Es ist keine zweite mechanische Impulsgleichung. Der
gesamte Material-Nullmodus wird festgehalten; die
Aussagen verwenden kleine Nichtnullmoden.

Am kritischen Richtungsport gilt fuer $z\to1$
$D(k,z)=A(z-1)^2+Ck^2+
O(|z-1|^3+k^2|z-1|+k^4)$.
Setze $z=1+k^{2/3}\lambda$. Da
$z-p_m=k^{2/3}\lambda+O(k^2)$, erhaelt man

$$
k^{-2}D_{\rm mix}(k,1+k^{2/3}\lambda)
= A\lambda^3-\nu+O(k^{2/3}).
$$

Die positive Nullstelle $(\nu/A)^{1/3}$ ist einfach.
Die reelle Fortsetzung fuer kleine positive k liefert
einen wachsenden Zweig
$z=1+(\nu/A)^{1/3}k^{2/3}+O(k^{4/3})$.
Das Wachstum verschwindet gegen kleine k, ueberwiegt
auf der Langwellenskala aber die akustische Frequenz $O(k)$.
Zwei getrennte Populationen allein ergeben damit
kein stabiles homogenes Wellenmedium. Der Exponent
gehoert zu diesem diffusionsartigen Materialport und
ist keine Vorhersage fuer Newtonsche Materie.

## 3. Verankerte Materie: konstruktiver Gegenfall

Betrachte stattdessen ein Material, dessen Verschiebung
P relativ zu einem festgelegten Bezugsprofil relaxiert:
$P_{n+1}=rP_n+\mu ik\Phi_n$ mit $0<r<1$.
Seine lineare Dichtestoerung ist $w=-ikP$. Daraus folgt
der blockweise Ansatz $r(k)=r$, $M(k)=1$.
Der exakte Nullmodus der physischen Dichte wird
nicht abgesenkt; $w=-ikP$ beschreibt nur Verschiebungen
mit null Aenderung der Gesamtmasse. Der Bezugspunkt
ist extern vorgegeben, nicht von beweglichen Knoten
im Modell erzeugt.

Nach Elimination von w ist der Feldnenner
$D_{\rm eff}=D+q\mu p b_s(k)zk^2/(z-r)$.
Damit gilt im akustischen Grenzwert

$$
\frac{D_{\rm eff}(k,e^{k\lambda})}{k^2}
\longrightarrow A\lambda^2+C_{\rm eff},
\qquad C_{\rm eff}=C-\frac{\nu}{1-r}.
$$

Fuer $C_{\rm eff}>0$ bleibt eine von null
verschiedene Wellengeschwindigkeit $v_{\rm eff}^2=
C_{\rm eff}/A$ und der statische Transfer
$\Phi/s_{\rm ext}\sim -b_s/(C_{\rm eff}k^2)$.
Die statische Materieauslese ist proportional zu u,
also zu $k^2\Phi$, nicht zu $\Phi$:
Sie veraendert die Steifigkeit, ohne dem Feld eine
statische Reichweitengrenze zu geben.

Fuer die bereits feste Positivkontrolle mit einem
Skalaralter, Vektoraltern $(2/3,1/3)$ und
$b_s=-\epsilon^2/2$ gilt $A=4/3$. Schreibe
$D_v=\sigma_v^2/2+(6/5)\epsilon^2$ wie im
Richtungsabschluss und $\zeta=\log z$. Der
Koeffizient von $\zeta k^2$ aendert sich von
$D_v-\epsilon^2/6$ auf
$D_v-\epsilon^2/6+\nu r/(1-r)^2$:
$z/(z-r)=(1-r)^{-1}-r\zeta/(1-r)^2+O(\zeta^2)$.
Die reale $k^2$-Korrektur der beiden Log-Multiplikatoren
ist somit

$$
\frac{v_{\rm eff}^2-D_v+\epsilon^2/6-\nu r/(1-r)^2}{2 A},
$$

und ist negativ, da schon der ungekoppelte Wert
negativ war, $v_{\rm eff}^2$ sinkt und r positiv ist.
Die restlichen longitudinalen Nullwellenzahl-Wurzeln
$r$ und $-1/3$ liegen strikt im Einheitskreis. Das
ist eine tatsaechliche Positivkontrolle fuer
hinreichend lange Wellen, kein all-k-Stabilitaetssatz.
Die Trennung gebundener Polarisation von propagierenden
Moden hat bekannte Parallelen, etwa bei
[Hopfield (1958)](https://doi.org/10.1103/PhysRev.112.1555).
Hier geht es um den anderen, konkreten skalaren
FIFO-Transfer und nicht um ein optisches Modell.

## 4. Innere Bindung ist keine Verankerung des Massenzentrums

Der stabilisierende Parameter r relaxiert eine
Verschiebung relativ zu einem fixierten Bezug.
Bei einem isolierten intern gebundenen Knoten
schreibe die Bestandteilspositionen als $R+r_a$ mit
$\sum_a m_a r_a=0$. Sind die Quellenkopplungen
alle proportional zu ihren mechanischen Massen,
ist die Quellenform bei kleiner Wellenzahl

$$
\sum_a m_a e^{-i\mathbf k\cdot(R+r_a)}
=e^{-i\mathbf k\cdot R}
\left(\sum_a m_a+O(k^2)\right).
$$

Bei festem Schwerpunkt R veraendert eine interne
Formmode die Quelle erst in Ordnung $k^2$.
Der Monopol bleibt am frei verschiebbaren Schwerpunkt.
Damit ist eine interne Rueckstellung allein
kein Ersatz fuer das gesetzte r der Positivkontrolle.
Andere, nicht massenproportionale Ladungen koennen
ein internes Dipolmoment besitzen; das waere aber
nicht dieselbe universelle Massenkopplung.

Der Befund schliesst keine inhomogenen gravitierenden
Hintergruende aus. Er macht die offene Aufgabe
konkret: Entweder den Bezugs-/Rueckstellungsmechanismus
aus einem erweiterten kollektiven Zustand herleiten
oder die volle Dynamik des frei beweglichen,
inhomogenen Mediums behandeln. Ein Positivtest mit
verankerten Quellpunkten darf freie Materietraeger
nicht ersetzen. Eine gemeinsame mechanische und
quantenmechanische Phasenkopplung bleibt unabgeleitet.

Der [neutrale Verbundvergleich](collective_neutral_material_response_2026-11-23.md)
realisiert die interne Polarisation ohne fixierten Anker. Er zeigt,
warum die frei bewegliche Mode nur bei Neutralitaet jedes
gebundenen Verbunds aus dem Quellenkanal verschwindet.

[Feste Matrix- und Formfaktorkontrollen](../../tests/test_collective_directional_current.py)
pruefen beide dynamischen Vergleichsfaelle und die
fehlende universelle Dipolkopplung einer internen
Formmode. Keine Parametersuche.
