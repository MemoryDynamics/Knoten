# Wenn das akkumulierte Feld auf seine eigene Quelle zurueckwirkt

Stand: 2026-11-23. Analytische Gegenprobe im bestehenden linearen
[Dichte-/Richtungsabschluss](collective_directional_current_2026-11-22.md).
Der Rueckwirkungsport wird fuer den Vergleich gesetzt, nicht als
nativer Knotenbestandteil eingefuehrt. Keine Zielsimulation.

**Ergebnis.** Ein rueckwirkungsfreier Probe-Reader kann die
rekonstruierte $1/r$-Antwort lesen. Gibt man denselben Gradient
mit anziehendem Vorzeichen an die Dichte zurueck, die ihn
erzeugt, folgt fuer jede feste positive Kopplungsstaerke
eine reell wachsende Langwellenmode. Eine Verzoegerung mit
gleicher statischer Lesestaerke verhindert das nicht.
Die zuvor stabilen akustischen Moden koennen daher nicht
unveraendert als stabiles homogenes Medium mit dieser
Selbstkopplung interpretiert werden.

## 1. Probe kontra geschlossener Rueckkanal

Im [vorherigen Vergleich](collective_accumulated_current_2026-11-22.md)
war fuer die Nichtnullmode k
$\Phi=u/k^2$ und $E=ik\Phi=i u/k$.
Das ist die seit der Anfangsreferenz akkumulierte
longitudinale Transportgroesse. Die native Driftregel
liest sie nicht. Ein *gesetzter*, rueckwirkungsfreier
Probeknoten mit $d_{\rm probe}=\mu E$ liest den Betrag
des statischen Gradienten und im akustischen Grenzsymbol
die frueher hergeleitete Wellenausbreitung.
$\mu>0$ ist anziehend fuer positive Quellen, denn
der Gradient des positiven $1/r$-Kerns zeigt nach innen.
Die Probe ist keine Quelle fuer u; sie hat also nichts
ueber die Konsistenz desselben Gesetzes auf beiden Seiten
gezeigt. $d_{\rm probe}$ ist ein Modellschritt, keine
mechanische Beschleunigung aus abgeleiteter Traegheit.

Fuer den selbstkonsistenten Vergleich addiere zum Schritt
der dichtebildenden Traeger $+\alpha E$. Allgemeiner
erlaube einen reellen, bei null stetigen raeumlichen
Profilmultiplikator $F(k)$ mit $F(0)>0$ und einen zeitlichen Lesefilter
$Q(z)=\sum_j q_jz^{-j}$ mit $\sum_j q_j=1$ und
$\sum_j |q_j|<\infty$. Sofortkopplung ist $F=Q=1$.
Der Nullmodus bleibt aus der Poisson-Auslese entfernt;
geprueft werden beliebig kleine **nichtverschwindende**
k. Dies setzt keine Hamiltonsche Reziprozitaet oder
Erhaltung von Impuls und Energie voraus.

## 2. Die Determinante hat eine exakte Rueckwirkungsform

Sei $D_0(k,z)$ die Determinante des ungekoppelten
laengsgerichteten Dichte-/Richtungsblocks. Der
laengsgerichtete Schritt hat nun den skalaren
Koeffizienten

$$
b_s(k)P_s(z)-\frac{\alpha F(k)Q(z)}{k^2}
$$

statt $b_s(k)P_s(z)$. In der Determinante
kommt dieser Koeffizient ausschliesslich als
$p k^2 z$ mal dem Koeffizienten vor: Die
beiden Vektorrueckwirkungsterme kuerzen sich.
Damit gilt exakt

$$
D_\alpha(k,z)=D_0(k,z)-\alpha p(k)z F(k)Q(z).
$$

Das beruecksichtigt, dass die Rueckwirkung den
realisierten Schritt und damit **auch** den am neuen
Ort abgelegten Richtungsvektor aendert. Nur die erste
Zeile der Dynamik zu aendern waere ein anderer Ansatz.

Bezeichne mit $\mathcal C(k)$ den statischen Nenner der
vorherigen Dichteauslese. Aus $D_0(k,1)=p k^2\mathcal C(k)$
folgt

$$
D_\alpha(k,1)=p\big[k^2\mathcal C(k)-\alpha F(k)\big].
$$

Am kritischen Richtungswert $g_0\chi=1$ war
$\mathcal C(k)\to C=\epsilon^2+b_s>0$ fuer die
Wellenroute. Jede feste $\alpha>0$ macht den
Ausdruck daher fuer hinreichend kleine k strikt
negativ. Entlang reeller $z\ge1$ bleibt die
Determinante stetig und geht fuer $z\to\infty$
gegen $+\infty$. Es gibt mindestens eine Wurzel
$z>1$ und damit eine exponentiell wachsende
Mode. Die Vorzeichenprobe haengt nur von $Q(1)=1$
ab. Ein endlicher Delay oder ein absolut summierbarer
Filter gleicher statischer Staerke kann sie nicht
aufheben. Bei unendlichem Filter hat die wachsende
Mode eine wohlbestimmte, nach hinten abklingende
Vorgeschichte; die Formel ist kein frei eingesetztes
Polynom fuer den ganzen Historienraum.

Die exakte hinreichende Bedingung an einer beliebigen
Wellenzahl ist $\alpha F(k)>k^2\mathcal C(k)$.
Das Gegenzeichen beweist keine Stabilitaet aller
Moden. In einer endlichen Box muss eine entsprechend
kleine Nichtnullmode ueberhaupt vorhanden sein.

Bleibt die externe Testquelle s allein am bisherigen
skalaren Eingang, erhaelt die rekonstruierte Auslese
den formalen statischen Transfer
$\Phi/s=-b_s(k)/(k^2\mathcal C(k)-\alpha F(k))$.
Er ist bei $k\to0$ beschraenkt. Wegen des wachsenden
Eigenmodus ist dies ein algebraischer statischer Loesungswert,
kein erreichter stationaerer Screening-Grenzwert.

## 3. Wachstumsrate und Gegenproben

Ohne Verzoegerung und mit $F(0)=1$ hat der
langwellige Grenzmultiplikator $z_*>1$ am
Richtungsschwellenwert die Gleichung

$$
(z_*-1)\left(1-\frac{P_v(z_*)}{z_*}\right)=\alpha .
$$

Fuer nichtnegative normierte Altersgewichte steigt
die linke Seite fuer $z_*>1$ streng von null
ins Unendliche. Die Wurzel ist einfach und wird bei
$k\to0$ von einer reell wachsenden Wurzel des vollen
Blocks erreicht. Fuer schwache Kopplung folgt
$z_*-1=\sqrt{\alpha/(1+\bar j_v)}+O(\alpha)$;
das folgt aus $1-P_v(z)/z=(1+\bar j_v)(z-1)+O((z-1)^2)$.
Die Wachstumsrate geht bei festem $\alpha$ also nicht
mit k gegen null. Der exakt erhaltene Dichtemittelwert
ist kein Gegenargument: Er ist nicht die hier
verwendete Folge von Nichtnullmoden.

Im kontrollierten schwachen Skalengrenzfall
$\alpha=\tilde\alpha k^2$ und $z=e^{k\lambda}$
(mit $F(0)=1$, $Q(1)=1$) lautet das fuehrende Symbol

$$
(1+\bar j_v)\lambda^2+C-\tilde\alpha .
$$

Dies ergibt in der Naehe der Schwelle die Balance
zwischen konstantem anziehendem Gewicht und
$k^2$-Rueckstellung der akustischen Mode. Das ist
die diskrete Analogie zur klassischen
[Jeans-Instabilitaet](https://doi.org/10.1098/rsta.1902.0012);
kein neuer allgemeiner Gravitationsmechanismus.
Ein abgeschirmter Reader $\Phi=u/(k^2+\kappa^2)$
liefert denselben Skalierungsfall mit
$\tilde\alpha\to\alpha/\kappa^2$. Er kann diese
Langwellen-Gegenprobe bei hinreichender Abschirmung
bestehen, verliert aber gerade den ungeschirmten
$1/r$-Anteil. Ein Vorzeichenwechsel aendert das
Argument ebenso, ist aber keine Aussage ueber die
Stabilitaet des so geaenderten diskreten Systems.

## 4. Was dadurch entschieden ist

Die Einweg-Probe zeigt einen lesbaren Gradienten,
nicht die unveraenderte Dynamik nach Rueckwirkung.
Der einfachste anziehende Selbstanschluss besteht
den Test als **stabiles homogenes Wellenmedium** nicht.
Das ist kein Ausschluss attraktiver Physik,
inhomogener stabilisierter Traeger oder anderer
Quellen- und Feldgleichungen. Auch Gravitation kann
homogene Materiezustaende destabilisieren. Der Befund
verhindert aber, dass die zuvor ungekoppelte
Wellengeschwindigkeit und die Rueckwirkung
unabhaengig als gleichzeitig nachgewiesen gelten.
Die Rekonstruktion leitet weiterhin weder den
Kraftport noch die Phasenkopplung des
[gemeinsamen Benchmarks](retarded_scalar_interferometer_2026-11-22.md) her.

[Feste Kontrollen](../../tests/test_collective_directional_current.py)
pruefen die Determinantenverschiebung, den Grenzmultiplikator,
eine verzoegerte Rueckwirkung sowie beide Seiten der
akustischen Schwelle. Keine Suche nach nativen Parametern.
