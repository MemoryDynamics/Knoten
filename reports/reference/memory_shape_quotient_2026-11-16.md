# Memory-Vierzyklus: acht Formmoden und notwendige Stabilitaetsbedingungen

Stand: 2026-11-16. Analytischer Anschluss an die
[positive abgeflachte Vierphasenfamilie](flat_memory_cycle_2026-11-16.md).
Der angefragte feste positive Stabilitaetskandidat wird hier **nicht**
ausgewertet. Keine neue Zieltrajektorie oder Parametersuche; Paper I bleibt
unveraendert.

## Ergebnis

Die vollen 15 konsistenten Historienkoordinaten lassen sich am exakten
Vierzyklus begruendet zerlegen: sechs euklidische Symmetrierichtungen,
ein redundanter Nullanteil und acht verbleibende Formmoden. Ein expliziter
konstanter Koeffizient ihres charakteristischen Polynoms liefert einen
notwendigen Produkttest, ohne numerische Eigenwertberechnung. Dazu kommt
eine unabhaengige notwendige Spurbedingung.

Eine gemeinsame Laengenreskalierung mit entsprechend angepassten
nativen Gains laesst die volle lokale Ableitung unveraendert. Ebenso
koennen kompensierte Memory-Massennormierungen oder Skalaramplituden die
Stabilitaet nicht retten. Die unabhaengigen dimensionslosen Parameter
bleiben f,g,q. Das ist keine zusaetzliche neutrale Mode eines festen
Modells, sondern eine Beziehung zwischen reskalierten Modellen.

Keine Stabilitaetsentscheidung fuer den ausstehenden festen Vertreter.
Analytisch ausgeschlossen wird nur hinreichend rasches Vergessen bei
fester Geometrie, nicht der angefragte hohe-q-Fall. Der bekannte
negative-Gain-Kontrollorbit dient der unabhaengigen Methodenpruefung;
die neue Zielauswertung bleibt bis zur konkreten Freigabe geschlossen.

## 1. Richtiger voller Operator

Alle Parameter werden bei einer Stoerung **festgehalten**. Insbesondere
duerfen die abgeleiteten Gains nicht nach jeder veraenderten Geometrie
neu eingestellt werden. Sei J_j=d Psi/d y_j die vorhandene volle
Kopfableitung und S die uneigentliche Viertelrotation aus dem
Existenzbericht. Am nachgewiesenen Orbit F(Y)=S Y gilt

$$
M=(I_5\otimes S^{-1})DF(Y),\qquad D(F^4)(Y)=M^4.
$$

Die obere Blockzeile besteht aus S^-1 J_j, die vier Shiftbloecke
sind S^-1. Fuer einen Eigenvektor mit nichtverschwindendem lambda
folgt delta y_j=lambda^-j S^-j delta y_0. Der Schur-Komplement-
Ausdruck liefert daher das monische Polynom vom Grad 15:

$$
\chi(\lambda)=\det(S^{-1})\det P(\lambda),\qquad
P(\lambda)=\lambda^5S-\sum_{j=0}^4\lambda^{4-j}J_jS^{-j}.
$$

Die Identitaet gilt durch polynomiale Fortsetzung auch bei lambda=0.
Als reine Blockmatrixidentitaet gilt sie auch ohne Orbitannahme;
**erst** ein exakter relativer Orbit erlaubt ihre Floquet-Deutung.

## 2. Welche Faktoren entfernt werden duerfen

Translationsstoerungen werden durch S^-1 transportiert. Ihre drei
Multiplikatoren sind -1,+i,-i. Rotationsgeneratoren transformieren
als Omega nach S^-1 Omega S. Da det S=-1, entspricht das fuer ihren
axialen Vektor der Matrix -S^-1, mit +1,+i,-i. Es folgen genau die
nachgewiesenen Symmetriefaktoren

$$
D_{\rm sym}(\lambda)=(\lambda^2-1)(\lambda^2+1)^2.
$$

Die vier nichtkoplanaren Orte garantieren die Unabhaengigkeit dieser
sechs Tangenten. Es wird nicht behauptet, dass es keine weiteren
Einheitskreiswurzeln gibt: Weitere solche Wurzeln bleiben Formmoden.
Eine kontinuierliche Zeitphasenmode ist bei der diskreten Regel nicht
zusaetzlich abzuziehen.

Die siebte Richtung veraendert nur y_4 entlang p_3. Solange die
Schrittlaenge positiv bleibt, aendert dies weder p_3 noch irgendeinen
gelesenen Ort; y_4 wird beim naechsten Shift verworfen. Die ganze
Abbildung ist entlang dieses lokalen Laengenfreiheitsgrads konstant.
Seine Ableitung ist null. Weil J_4=-Bq^3g(I-p_3p_3^T) Rang zwei hat,
besitzt DF Rang 14. Die redundante Richtung ist unabhaengig von den
sechs Symmetrietangenten. Damit

$$
\chi(\lambda)=\lambda(\lambda^2-1)(\lambda^2+1)^2Q_8(\lambda),
\qquad Q_8(\lambda)=\lambda^8+a_1\lambda^7+\cdots+a_8.
$$

Auch Q_8 darf weitere Nullwurzeln besitzen; es wird kein einfacher
algebraischer Nullmultiplikator vorausgesetzt. Ein orthogonales
Komplement ist nicht automatisch invariant. Die korrekte Konstruktion
ist eine Basis mit dem **invarianten** siebendimensionalen Raum zuerst;
die untere rechte Acht-mal-acht-Matrix der blockoberen Dreiecksform
repraesentiert den Quotienten. Nur eine Hoehen- oder Radialprojektion
liefert diesen Quotienten im Allgemeinen nicht.

## 3. Produkt aller acht Formmultiplikatoren

Benutze die Parameter des Existenzberichts, gleiche Skalar- und
Vektorbreite sigma und rein attraktiven Skalar-Gausskernel. Setze

$$
R=r^2/\sigma^2,\quad Z=h^2/\sigma^2,\quad
\gamma=4h^2/L^2=\frac{4Z}{2R+4Z},\quad t_3=q^3g.
$$

Aus J_4=-B t_3(I-p_3p_3^T) folgt
P(0)=B t_3(I-p_3p_3^T) und
adj P(0)=(B t_3)^2 p_3p_3^T. Da P'(0)=-J_3 S und
S p_3=p_2, ist

$$
\chi'(0)=(Bt_3)^2p_3^TJ_3p_2,\qquad a_8=-\chi'(0).
$$

Der skalare Anteil von J_3 ist
C_1s^3(I-r_3r_3^T/sigma^2), mit r_3=y_0-y_3=-L p_3.
Der Orientierungsanteil A_3 verschwindet links an p_3, der Anteil
-A_2 rechts an p_2. Die verbleibende Kernelvariation ergibt

$$
p_3^TJ_3p_2=C_1s^3(4Z-\gamma)+4Bq^3gZ.
$$

Damit explizit

$$
\boxed{a_8=B^2q^6g^2\left[C_1s^3(\gamma-4Z)-4Bq^3gZ\right].}
$$

Mit C_1=B(1-gq)/s kann derselbe Ausdruck allein aus B,s,f,g,q und
der daraus bestimmten dimensionslosen Geometrie berechnet werden.
Es ist das Produkt der **acht Formmultiplikatoren**, nicht der
gesamten 15 Eigenwerte: Deren Produkt waere wegen der redundanten
Nullrichtung immer null und damit uninformativ.

Sind alle Formmultiplikatoren strikt im Einheitskreis, muss
|a_8|<1 gelten. Eine rigorose untere Schranke |a_8|>1 beweist eine
wachsende Formmode und liefert

$$
\rho_{\rm form}(M)\ge |a_8|^{1/8}>1,\qquad
\rho_{\rm form}(D(F^4))\ge |a_8|^{1/2}>1.
$$

|a_8|=1 verhindert strikte Schur-Stabilitaet, beweist aber nicht
allein Wachstum. |a_8|<1 ist **nicht hinreichend**: Ein wachsender
Multiplikator kann durch kleine andere Faktoren kompensiert werden.
Intervallgrenzen, die 1 schneiden, bleiben unentschieden.

## 4. Unabhaengige notwendige Spurbedingung

Die Symmetriemultiplikatoren summieren sich zu null; der redundante
Anteil traegt ebenfalls null bei. Somit ist die Summe der acht
Formmultiplikatoren gleich tr M. Die volle Kopfableitung und die
nativen Existenzgleichungen vereinfachen sie zu

$$
T:=\operatorname{tr}M=-4Z+B\left[
\gamma-gq^3+2Rgq+(2R-4Z)fq^2-4Z\right].
$$

Strikte Schur-Stabilitaet verlangt |T|<8. Fuer |T|>8 existiert eine
wachsende Formmode mit rho_form(M)>=|T|/8. Auch dieser Test ist nur
notwendig, nicht hinreichend. Beispielsweise haben die acht formal
vorgegebenen Zahlen 6/5,1/5,...,1/5 sowohl |Summe|<8 als auch
|Produkt|<1 und trotzdem eine Zahl groesser als 1. Diese Gegenkontrolle
ist kein nativer Orbit.

Fuer festes f,g der positiven Existenzklasse gilt bei q gegen 0
B asymptotisch f^2/[q^2(g^4-f^3)]. Wenn gamma-4Z ungleich null ist,
divergiert T wie q^-2; im Ausnahmefall gamma=4Z bleibt ein positiver
q^-1-Leitterm. Daher ist fuer jede feste solche Geometrie hinreichend
rasches Vergessen instabil. Dieser Grenzfall verletzt bei festem r,h
auch die Innenlagebedingung des Defekts; er entscheidet **nicht**
den angefragten hohen-q-Kandidaten.

Der [spaetere Gebietstest](four_cycle_stability_exclusions_2026-11-21.md)
verwendet dieselbe Spur, um sehr kleine Radien mit Innenlage
und sehr grosse Hoehen analytisch auszuschliessen.
Das ist keine Auswertung des angefragten 3D-Kandidaten.

## 5. Welche Reskalierungen nichts an der Stabilitaet aendern

Fuer a,b_s,b_v,c>0 reskaliere gleichzeitig

$$
Y'=cY,\quad\sigma'=c\sigma,\quad A'=aA,\quad
M_s'=b_sM_s,\quad M_v'=b_vM_v,
$$

$$
\eta_s'=\frac{c^2}{a b_s}\eta_s,\qquad
\eta_v'=\frac{c}{b_v}\eta_v.
$$

Bei gleichen Retentionen und Horizonten gilt fuer den hier verwendeten
Kernel exakt F'(cY)=cF(Y), daher DF'(cY)=DF(Y). Einheitsrichtungen
bleiben gleich; die Skalargradienten liefern den Faktor a b_s/c,
der Vektorreadout den Faktor b_v. Die Gains kompensieren diese
Faktoren. Auch der mitbewegte volle Operator ist unveraendert.

Dies gilt sogar an nichtperiodischen Historien im glatten Bereich.
Fuer die analytische Familie haengt das Formpolynom damit nur von
f,g,q ab. Ein groesserer Knoten oder eine andere Memory-Masseneinheit
kann bei dieser gemeinsamen Reskalierung einen instabilen Orbit
nicht stabil machen. Eine Gain- oder Massenveraenderung **ohne** die
angegebene Kompensation ist hingegen ein anderes Problem und erhaelt
die nachgewiesene Bahn nicht automatisch. Es wird kein physikalischer
Massenbegriff aus M_s oder M_v abgeleitet.

## 6. Unabhaengige Kontrollen und Literatur

Die Ableitung des konstanten Koeffizienten wird zusaetzlich fuer
einen einzelnen skalaren Gausskernel beliebigen Vorzeichens und
anderer Breite tau kontrolliert. Dann lautet die verallgemeinerte
Formel fuer -chi'(0)

$$
(Bq^3g)^2\left[
C_1s^3\left(\gamma-\frac{4h^2}{\tau^2}\right)
-\frac{4Bq^3gh^2}{\sigma^2}\right].
$$

An festen Nicht-Orbits wird sie mit der Summe aller Diagonalkofaktoren
der vollen 15-mal-15-Matrix verglichen; dort werden **keine**
Symmetriefaktoren entfernt und kein Formpolynom behauptet.
Die Drei-mal-drei-Determinantenidentitaet wird separat an reellen
und komplexen Argumenten geprueft, die Skalenidentitaet direkt an
Kopfwert und allen Ableitungsbloecken.

Am bereits bekannten negativen-Gain-Tetraeder gilt
B=-24,q=g=1/2,C_1=-108,s=1/6,gamma=1/2 und 4h^2/tau^2=1/2,
waehrend 4h^2/sigma^2=log2. Daher exakt a_8=(27/8)log2>1.
Der unabhaengig aus den alten rational-logarithmischen Bloecken
gebildete Acht-dimensional-Quotient reproduziert diesen Wert.
Das ist ein zusaetzlicher Kontrollbeweis seiner **bereits bekannten**
Instabilitaet, kein Test des neuen positiven Kandidaten.

[Sidorenko/Thunberg, arXiv:2610.28341v1](https://arxiv.org/html/2610.28341v1),
Anhang B.3, Gleichungen (154)-(158), wurde im Volltext als methodischer
Vergleich gelesen: Die Autoren identifizieren Symmetriemultiplikatoren
vor der Schur-Cohn-Rekursion; deren erster Schritt testet den Betrag
des konstanten Koeffizienten. Unsere acht Formmoden und die obigen
Koeffizienten sind eigenstaendig fuer den FIFO hergeleitet. Ihre
Mehragentendynamik und ihre Stabilitaetsresultate werden nicht
uebernommen. Kein eigener Nachvollzug ihres Intervallzertifikats.

Die vorhandene `interval_schur_test`-Routine ist fuer einen spaeteren
vollstaendigen Koeffiziententest verfuegbar; sie wird hier nicht auf
den ausstehenden Kandidaten angewandt. Ein erstes bestandenes
Produktkriterium darf die weiteren Schur-Schritte nicht ersetzen.

15 neue feste algebraische Kontrollen sind hinzugefuegt. Sie pruefen
Nicht-Orbits, formale Polynome und den alten negativen Kontrollorbit,
keine Spektren oder Wachstumsgrenzen des neuen positiven Vertreters.
372 Tests im betroffenen Panel bestehen, ebenso Lint im konfigurierten
Bereich und strikter Dokumentationsbau. Keine vollstaendige
Repository-Testsuite. Die endlichen Kontrollen pruefen die Umsetzung;
die allgemeinen Aussagen beruhen auf den angegebenen Herleitungen.
Die einzige aktive Arbeitsreihenfolge bleibt in den
[Projektprioritaeten](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/docs/status/project_priorities.md).
