# Nichtminimale Memory: beide lokale Defektvorzeichen

Stand: 2026-11-15. Analytische Fortsetzung der
[minimalen Vorzeichenklassifikation](memory_defect_recurrence_2026-11-14.md).
Feste konstruierte Historien und Softwarekontrollen, keine Zielbahn,
Nullstellen- oder Parametersuche. Paper I und die native Dynamik bleiben
unveraendert.

Die anschliessende [native Regenerationspruefung](nonminimal_memory_recurrence_2026-11-15.md)
schliesst den starren Zweischalenumlauf bei gleichem skalarem/vektoriellem
Vergessen und Horizonten aus ganzen Achtperioden aus. Der statische
Existenzsatz unten bleibt davon unberuehrt; getrenntes Vergessen liefert
zunaechst nur eine notwendige, keine hinreichende Umlaufbedingung.

## Ergebnis und Reichweite

**Die Vorzeichenhuerde ist fuer den bestehenden Readout nicht allgemein:**
Eine explizite bahnkonsistente Historie mit acht gerichteten Depositionen
traegt genau einen regulaeren Defekt mit Index -1 innerhalb eines Balls
vom Radius 1/6. Dieser Ball liegt im Inneren der nahen Memory-Geometrie.
Eine andere Historie mit demselben H, denselben nativen Gewichten,
derselben Gaussbreite und derselben Richtungsdefinition traegt dort
einen regulaeren +1-Defekt. Es werden weder unabhaengige interne
Orientierungen noch ein zusaetzliches Materiefeld eingefuehrt.

Im negativen Kontrollfeld ist zusaetzlich ein positiver Gesamtindex
ausserhalb des kleinen Balls erzwungen: aussen +1, innen -1, dazwischen
also +2. Das ist **kein neutraler Zweiteilchenzustand**. Die Rechnung
bestimmt dort weder die Zahl noch die Regularitaet einzelner Nullstellen.

Dies schliesst einen statischen Existenzschritt, keinen Ladungstraeger-
Nachweis. Die Historien sind erlaubte gefuellte Zustaende, aber keine
nachgewiesenen Orbits oder Attraktoren. Dynamische Regeneration,
physikalischer Strom, elektrische Wirkung und Quantendynamik bleiben offen.
H=8 ist damit konstruktiv ausreichend fuer beide statischen Vorzeichen;
der kleinste moegliche Horizont ist nicht bestimmt. 3D ist hier ein
Input, kein Ergebnis der Konstruktion.

## 1. Unveraenderter nativer Readout

Wir verwenden in vorgegebenen drei Raumdimensionen

$$
V(z)=\sum_{j=0}^{7}w_jp_j e^{-|z-y_j|^2/2},\qquad
p_j=\frac{y_j-y_{j+1}}{|y_j-y_{j+1}|},\qquad
w_j=(1-q)q^j,\quad q=\frac{99}{100}.
$$

Damit sind sigma_vector=1, vector_mass=1 und lambda_vector=1/100.
Die acht Depositionen benoetigen neun Historienpositionen. Die
Orientierungen werden ausschliesslich aus ihren Differenzen gewonnen;
alle Differenzen sind ungleich null. Die abgeschnittenen Gewichte
summieren sich zu 1-q^8, nicht zu eins. Es gibt keine nachtraegliche
Massen-, Feld- oder Kraftnormierung. Ein Gain wird nicht ausgewaehlt.

Fuer einen regulaeren Nullpunkt z_* ist der hier untersuchte Index

$$
Q_{\rm top}(z_*)=\operatorname{sgn}\det DV(z_*).
$$

Das ist der lokale Abbildungsgrad eines Vektorfelds, nicht die
Verschlingungszahl der Historienkurve und nicht bereits elektrische Ladung.
Insbesondere sind acht Speicherbeitraege keine acht Teilchen.

Die Tetraederecken

$$
v_0=\frac{(1,1,1)}{\sqrt3},\quad
v_1=\frac{(1,-1,-1)}{\sqrt3},\quad
v_2=\frac{(-1,1,-1)}{\sqrt3},\quad
v_3=\frac{(-1,-1,1)}{\sqrt3}
$$

erfuellen Summe v_i=0, Summe v_i v_i^T=(4/3)I und
v_i dot v_j=-1/3 fuer i ungleich j. Ihr Umkugelradius ist 1,
ihr Inkugelradius 1/3.

## 2. Konkrete Historie mit negativem Index

Die neueste-zuerst geordnete Historie ist

$$
y_{2i}=v_i,\quad y_{2i+1}=5v_i\quad(i=0,1,2,3),
\qquad y_8=v_0.
$$

Sie ist geschlossen. Mit zyklischem Index i+1 folgen ohne freie Wahl

$$
p_{2i}=-v_i,\qquad
p_{2i+1}=\frac{5v_i-v_{i+1}}{\ell},\qquad
\ell=\sqrt{\frac{88}{3}}<6.
$$

Die nahen Depositionen zeigen nach innen. Die verbindenden
Depositionen liegen weiter aussen und sind im Zentrum gaussschwach.
Dies begruendet die Konstruktion; die Zahlen 5 und 99/100 sind feste
analytische Zeugen, keine aus Teilchendaten hergeleiteten Parameter.

Fuer den Beweis allein teilen wir durch den positiven Faktor w_0:

$$
F(z)=\frac{V(z)}{w_0}
=-\sum_{i=0}^3q^{2i}v_i e^{-|z-v_i|^2/2}
+\sum_{i=0}^3q^{2i+1}p_{2i+1}e^{-|z-5v_i|^2/2}.
$$

Diese Schreibweise aendert weder Nullstellen noch Index, ersetzt aber
nicht die native Amplitude in einer Bewegungsgleichung.

### 2.1 Referenzfeld und kontrollierter Rest

Als rein analytischen Vergleich nehmen wir

$$
F_0(z)=-\sum_{i=0}^3v_i e^{-|z-v_i|^2/2},\qquad
F_0(0)=0,\qquad DF_0(0)=-\kappa I,
\quad \kappa=\frac43e^{-1/2}>\frac45.
$$

Das ist keine Umstellung der nativen Altersgewichte auf Gleichgewichtung.
Setze r=1/6 und bezeichne mit B_r den offenen Ball um den Ursprung.
Auf seinem Abschluss sind die Abstaende zu
jedem v_i zwischen 5/6 und 7/6. Fuer G(z)=exp(-|z-v_i|^2/2) sind die
Eigenwerte der Hesse-Matrix -exp(-t/2) und (t-1)exp(-t/2), mit
t=|z-v_i|^2. Hier gilt |t-1|<1, also

$$
\|D^2G\|\le e^{-25/72}<\frac{18}{25},\qquad
\|D^2F_0\|\le L_0=\frac{72}{25}.
$$

Die zweite Norm ist die bilineare Operatornorm. Auf |z|=r folgt

$$
|F_0(z)|\ge\kappa r-\frac{L_0r^2}{2}>\frac7{75}.
$$

Der Taylorrest ist kleiner als |(-kappa I)z|. Die geradlinige Homotopie
zwischen F_0 und -kappa z ist daher auf dem Rand nullstellenfrei:
deg(F_0,B_r,0)=-1.

Schreibe E=F-F_0 als Vergessenskorrektur plus aeussere Depositionen.
Bernoullis Ungleichung ergibt

$$
\sum_{i=0}^3(1-q^{2i})
\le (0+2+4+6)(1-q)=\frac3{25}.
$$

Die aeusseren Punkte haben Abstand mindestens 29/6. Deshalb gilt
auf ganz B_r

$$
|E(z)|<\frac3{25}\frac{18}{25}+4e^{-841/72}
<\frac{54}{625}+\frac1{10000}<\frac7{75}.
$$

Die Homotopie F_0+sE bleibt auf dem Rand nullstellenfrei. Insbesondere

$$
\deg(F,B_r,0)=-1,\qquad
\inf_{\partial B_r}|F|>\frac{41}{6000}.
$$

### 2.2 Eindeutigkeit, Regularitaet und Lokalisation

Global gilt |grad G|<=exp(-1/2)<2/3. Fuer die aeusseren Punkte ist
d exp(-d^2/2) bei d>=29/6 fallend. Daraus folgt auf ganz B_r

$$
\|DF(z)+\kappa I\|
< L_0r+\frac3{25}\frac23
+4\frac{29}{6}e^{-841/72}
<\frac{12}{25}+\frac2{25}+\frac1{2000}<\kappa.
$$

Der symmetrische Jacobiananteil ist strikt negativ, mit Reserve
groesser als 479/2000. Entlang einer Verbindungsstrecke in B_r folgt
fuer verschiedene x,y

$$
(F(x)-F(y))\cdot(x-y)
<-\frac{479}{2000}|x-y|^2.
$$

Es gibt also hoechstens eine Nullstelle. Der Grad beweist deren
Existenz; die Jacobianschranke beweist Regularitaet und negatives
Determinantenvorzeichen durch Homotopie zu -kappa I.

**Genau ein regulaerer -1-Defekt liegt im Ball mit Radius 1/6.** Dieser Ball liegt
streng innerhalb des nahen Tetraeders: Fuer |z|<=1/6 sind

$$
\beta_i=\frac{1+3v_i\cdot z}{4}>0,\qquad
\sum_i\beta_i=1,\qquad \sum_i\beta_i v_i=z.
$$

Es handelt sich somit nicht um die zuvor beobachtete weit entfernte
Simplex-Nullstelle. Kleine C^1-Stoerungen erhalten diesen lokalen
Befund. Im nativen V betragen die obigen Reserven w_0 mal 41/6000
am Rand und w_0 mal 479/2000 fuer den negativen symmetrischen
Jacobiananteil. Eine solche Stoerungsreserve ist noch keine Schranke
fuer die vom eigenen Update erzeugte Zustandsaenderung.
Der negative symmetrische **Ortsjacobian des eingefrorenen Readouts**
ist insbesondere kein Stabilitaetsnachweis der vollen Memory-Dynamik.

### 2.3 Rationale Absicherung der Konstanten

Die Beweise benoetigen keine gerundeten Exponentialwerte:

- exp(1/2)<=1+1/2+(1/8)/(1-1/6)=33/20<5/3; fuer den
  Rest wird $k!\ge2\cdot3^{k-2}$ fuer k>=2 verwendet.
- exp(1)>1+1+1/2>9/4 liefert exp(-1/2)<2/3.
- exp(25/72)>1+25/72+(25/72)^2/2>25/18.
- 841/72>11 und die positive Taylor-Teilsumme von exp(11) bis
  einschliesslich k=16 ist groesser als 40000.
- Die positive Taylor-Teilsumme von exp(4) bis k=7 ist groesser als 50.

Die Tests pruefen diese endlichen Vergleiche mit Fraction-Arithmetik.
Die analytischen Taylor-/Monotonieargumente, nicht eine Abtastung der
Kugel, tragen die Aussagen fuer alle Punkte.

## 3. Positiver Kontrollfall bei denselben Parametern

Setze stattdessen y_j=v_(j mod 4), j=0,...,8. Dies ist eine doppelt
durchlaufene Tetraeder-Historie mit acht aktiven Depositionen.
Gleiche Positionen und Richtungen aggregieren die nativen Gewichte zu

$$
\widetilde w_i=w_0(1+q^4)q^i,\qquad i=0,1,2,3.
$$

Der bereits bewiesene geschlossene Simplexsatz liefert genau eine
regulaere Nullstelle mit Index +1. Explizit ist sie

$$
z_+=\sqrt3\log(q)\,(1,1/2,0),\qquad
|z_+|=\frac{\sqrt{15}}2|\log q|
\le\frac{\sqrt{15}}{198}<\frac16.
$$

Die letzte Schranke verwendet -log q<=(1-q)/q. Damit sind beide
Indexvorzeichen in derselben nativen Readout-Klasse lokal realisierbar,
ohne den Gain oder die Definition fuer das zweite Vorzeichen umzudrehen.
Das sind zunaechst **zwei verschiedene Zustaende**, keine nachgewiesene
Umwandlung, Paarerzeugung oder Wechselwirkung.

Die [gemeinsame Fernindexpruefung](memory_defect_far_degree_2026-11-23.md)
zeigt inzwischen: Die beiden lokalen Grade koennen im gemeinsamen
Feld gleichzeitig bestehen, ohne eine global neutrale Quelle zu liefern.
Jede geschlossene voll affine Spur dieser Klasse hat global Grad $+1$.

## 4. Was das negative Kontrollfeld aussen erzwingt

Auch im einzelnen negativen Kontrollfeld ist der kleine Defekt nicht
die ganze Topologie. Sei n ein Einheitsvektor, a_i=n dot v_i und
m=max a_i. Weil n/3 im Tetraeder liegt, gilt m>=1/3. Das folgt zum
Beispiel aus den nichtnegativen baryzentrischen Gewichten (1+a_i)/4.

An einem maximierenden Index ist

$$
n\cdot p_{2i+1}=\frac{5m-a_{i+1}}{\ell}\ge\frac{4m}{\ell}.
$$

Eine aeussere Deposition mit negativer radialer Projektion erfuellt
5a_i<a_(i+1)<=m, also a_i<m/5. Auf z=Rn faktorisieren wir die
positive gemeinsame Gaussamplitude

$$
K_R=\exp(-R^2/2-25/2+5Rm).
$$

Die maximal projizierte aeussere Quelle liefert mindestens
$q^7\cdot4m/\ell$. Hoechstens drei negative aeussere Beitraege sind
relativ dazu jeweils durch exp(-4Rm) beschraenkt. Jeder negative
innere Beitrag ist durch exp(12-4Rm) beschraenkt. Folglich

$$
\frac{n\cdot F(Rn)}{K_R}
\ge q^7\frac{4m}{\ell}-3e^{-4Rm}-4e^{12-4Rm}
>\frac{31}{150}-\frac1{10000}-\frac2{25}
=\frac{3797}{30000}>0\qquad(R\ge12).
$$

Verwendet wurden q^7>=93/100, ell<6, m>=1/3, exp(4)>50 und
3/50^4<1/10000. Alle Radien R>=12 sind erfasst, nicht nur Stichproben.

F zeigt auf jeder dieser Kugeln strikt nach aussen. Die Homotopie
zum radialen Identitaetsfeld gibt deg(F,B_12,0)=+1; ausserhalb B_12
liegen keine Nullstellen. Die Additivitaet des Grads liefert

$$
\deg(F,B_{12}\setminus\overline{B_{1/6}},0)=+2.
$$

Dieser positive Gesamtgrad ist ein gleichzeitiger Befund im selben
Memory-Feld. Er garantiert jedoch **nicht** genau zwei isolierte
+1-Nullstellen; dazu fehlt eine Regularitaets-/Zerlegungspruefung des
aeusseren Nullstellensatzes. Insbesondere ist der gesamte Kontrollfall
nicht neutral und kein Wasserstoffanalogon. Der Index ist zudem kein
Fluss des glatten, im Fernfeld abklingenden Rohfelds V.

## 5. Literaturabgleich: Topologie ist nicht elektrische Abschirmung

Gezielte Pruefung vom 2026-11-15, keine systematische Literaturreview:
Gesucht wurden Vorzeichen und Abschirmung von Vektorfeldnullstellen.
Gelesen wurden die nachstehenden Primaertexte; die Konstruktion oben
ist eine eigene Ableitung fuer die bahngebundene Memory-Klasse.

| Quelle und gelesener Bereich | Beleg | Transfergrenze |
| --- | --- | --- |
| M. R. Dennis, *Correlations and screening of topological charges in Gaussian random fields*, J. Phys. A 36, 6611-6628 (2003), [DOI](https://doi.org/10.1088/0305-4470/36/24/301), [arXiv v2](https://arxiv.org/pdf/math-ph/0302024v2), Abschnitte 1, 4 und 7 | Lokaler Index regulaerer Vektornullstellen ueber das Jacobianvorzeichen; Ladungskorrelationen und eine Abschirm-Summenregel fuer die untersuchten Zufallsfeld-Ensembles. | Der Vektorfall setzt unabhaengige identisch verteilte gausssche Komponenten voraus. Unser deterministisches altersgewichtetes Feld mit bahngebundenen Richtungen erfuellt diesen Vertrag nicht automatisch. |
| M. Wilkinson, *Screening of charged singularities of random fields* (2004), [Journal-DOI](https://doi.org/10.1088/0305-4470/37/26/012), [arXiv v1](https://arxiv.org/pdf/cond-mat/0402120v1), Abschnitte 1-2 und 4 | Abschirmargument ueber Rand-/Volumenkorrelationen bei stationaeren, ladungsneutralen Statistiken und geeigneter Korrelationsabnahme; explizites Gegenbeispiel zu universeller perfekter Abschirmung. | Ein topologischer Index allein liefert weder eine solche Statistik noch eine Coulomb-Kraft. Diese Voraussetzungen muessen fuer eine native Ensemble-Dynamik gesondert geprueft werden. |

Gaussfoermige **Kernel** sind nicht gleichbedeutend mit einem
gaussschen **Zufallsfeld-Ensemble**. Der Grad +2 in einem bestimmten
Ringgebiet ist auch keine statistische Abschirm-Summenregel. Insbesondere
leitet dieser Befund weder ein anziehendes Gegenladungs-Potential noch
eine Energie, elektrische Neutralitaet oder QFT ab.

Die arXiv-Metadaten ordnen beide Texte den angegebenen Journal-DOIs zu.
Die DOI-spezifische Korrektur-/Erratum-Suche ergab keinen eindeutig
zugeordneten Korrekturhinweis; das ist kein vollstaendiger Crossmark-Audit.
Die gelesenen Fassungen sind Dennis v2 und Wilkinson v1, nicht eine
zeilenweise gepruefte Identitaet mit den Verlagsfassungen.

## 6. Kontrollen und verbleibender Anschluss

Die neue Testdatei `tests/test_nonminimal_memory_defects.py` kontrolliert
die echten History-/Gewichtshelfer, die Orientierungsableitung, beide
Feldformeln, den expliziten positiven Nullpunkt, die Jacobianableitung,
raumstarre Kovarianz und die rationalen Beweisreserven. Feste Punktchecks
sichern die Implementierung, **nicht** die kontinuierlichen Randbeweise.
Keine negative Nullstelle wurde numerisch gesucht; ihre Existenz,
Eindeutigkeit, Regularitaet und Lokalisation folgen aus Abschnitt 2.

Die 23 neuen Kontrollen und insgesamt 176 Tests im betroffenen
Regressionspanel bestanden: Defekt/Rekurrenz, Vektormemory/Normalantwort,
topologischer Zustand, Memory-Strom, kollektive Quellen, Kernphase,
Zustandsvertrag und Markdown-Mathematik. Der konfigurierte Ruff-Lint
und der strikte MkDocs-Bau bestanden ebenfalls. Keine vollstaendige
Repository-Testsuite. Ein unabhaengiger mathematischer Review oder
maschinenverifizierter Beweis liegt nicht vor.
Die Saetze gelten in exakter reeller Arithmetik; die binary64-Kontrollen
sind kein Intervallzertifikat fuer den Simulator.

Die Arbeitsreihenfolge bleibt ausschliesslich in den
[Projektprioritaeten](../../docs/status/project_priorities.md).
Der jetzt konkretisierte offene Anschluss ist ein **unter nativen
Updates regenerierter, raeumlich kontrollierter Zustandsbereich**, nicht
noch ein statisches Vorzeichenbeispiel. Die vorhandene Quellen-/Tail-
Identitaet und das Randkriterium bleiben anwendbar, sind aber fuer diese
Historie noch nicht ueber die Zeit geschlossen. Vollstaendige
Formstabilitaet und eine physikalische Quellen-/Stromkopplung sind davon
weitere getrennte Anforderungen. Kein Gain-Fit, H-Scan, neuer Ziellauf
oder Import eines Referenzfeldes folgt aus dem statischen Satz.
