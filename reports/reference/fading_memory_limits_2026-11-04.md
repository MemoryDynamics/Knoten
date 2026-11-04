# Unendliche Memory: stetige Invarianten und singulaere Grenzfaelle

Stand: 2026-11-04. Analytische Entscheidungsvorbereitung nach der
[endlichen FIFO-Invariantengrenze](memory_current_invariants_2026-11-04.md).
Keine Auswahl einer neuen Modellstruktur, keine Zielsimulation. Die
offene Richtungsfrage an den Autor wird dadurch nicht als beantwortet
behandelt. Paper I bleibt unveraendert.

## Ergebnis

**H nach unendlich bei festem positivem Vergessen reicht fuer eine
nichttriviale stetige exakte Zustandsinvariante nicht aus**, sofern die
unten angegebenen Volltraeger-, Zustandsraum- und Stetigkeitsannahmen
gelten. Die untrunkierte Memory kann zwar exakte Informationen im
verschwindenden Rest behalten. Diese Tatsache allein liefert aber noch
keine robuste Ladungsobservable und keinen Wechselwirkungsmechanismus.

Der neue Satz ist enger als der endliche: Er betrifft **stetige**
Zustandsfunktionen. Ein explizites unstetiges Gegenbeispiel zeigt, warum
wir ihn nicht auf alle messbaren Funktionen erweitern duerfen. Das ist
kein Ausschluss aller topologischen Ladungen auf eingeschraenkten
physikalischen Zustandsraeumen. Die Wahl des Zustandsraums und seiner
Topologie ist Teil der Annahmen, keine nachtraegliche Nebensache.

## 1. Modell und kontrollierte Schreibfolge

Verwendet wird die untrunkierte Punktdeposition aus
[Paper I, Deposited-Trace Model](../../paper/paper_i/manuscript/content.tex),
mit normierter Memory und endlichem zweitem Moment:

$$
Z=(x,\mu)\in\mathbb R^d\times\mathcal P_2(\mathbb R^d),\qquad
x^+=b(x,\mu)+\varepsilon\xi,\qquad
\mu^+=q\mu+\alpha\delta_{x^+},\qquad q=1-\alpha\in(0,1).
$$

Die Innovationen sind ideal, unabhaengig und standardnormalverteilt,
$\varepsilon>0$, und b ist messbar und endlich. Bei Gausskerneln ist
die erforderliche Gradientenintegration gegen eine endliche Memory
endlich. Der Zustand umfasst keine weiteren unveraenderlichen Labels.
Wir verwenden den euklidischen Abstand fuer x und die
Wasserstein-2-Topologie fuer die Memory:

$$
W_2(\mu,\nu)^2=\inf_{\pi\in\Pi(\mu,\nu)}
\int |y-z|^2\,\pi(dy,dz).
$$

$\Pi(\mu,\nu)$ bezeichnet die Kopplungen mit den angegebenen Marginalen.
Dies ist eine festgelegte Regularitaetsanforderung an Q, keine Behauptung,
dass jede denkbare physikalische Ladung auf diesem ganzen Raum stetig ist.

Fuer eine beliebige **vorgegebene** Folge von Schreiborten $u_1,\ldots,u_N$
gilt durch Ausrollen der affinen Rekursion

$$
\mu_N=q^N\mu_0+\alpha\sum_{r=1}^Nq^{N-r}\delta_{u_r}.
$$

Zwei solche Memory-Zustaende mit derselben vorgegebenen Folge erfuellen
$\mu_N-\nu_N=q^N(\mu_0-\nu_0)$. Das ist keine Synchronisation zweier
ungezwungener stochastischer Trajektorien: Die zum Erreichen derselben
Orte benoetigten Innovationen haengen von der jeweiligen Drift ab.

Waehlt man ausschliesslich $u_r=a$, so gilt fuer $N\geq1$

$$
x_N=a,\qquad\mu_N=q^N\mu_0+(1-q^N)\delta_a,\qquad
W_2(\mu_N,\delta_a)^2=q^N\int|y-a|^2\,\mu_0(dy).
$$

Die letzte Gleichheit folgt aus der einzigen moeglichen Kopplung mit
einer Dirac-Masse: jeder Punkt muss nach a transportiert werden. Daher
konvergiert dieser kontrollierte Zustand nach $(a,\delta_a)$.

## 2. Ausschluss stetiger exakter Invarianten

**Satz.** Ist $Q:\mathbb R^d\times\mathcal P_2(\mathbb R^d)\to\mathbb R$
stetig und gilt $Q(Z^+)=Q(Z)$ fast sicher fuer jeden Startzustand, dann
ist Q konstant.

**Beweis.** Fixiere Z. Die Abbildung

$$
u\longmapsto Q(u,q\mu+\alpha\delta_u)-Q(Z)
$$

ist stetig: Durch gemeinsames Koppeln des alten Memory-Anteils und
Transport der neuen Dirac-Masse gilt
$W_2(q\mu+\alpha\delta_u,q\mu+\alpha\delta_v)\leq\sqrt\alpha|u-v|$.
Die bedingte Dichte von $x^+$ ist auf ganz $\mathbb R^d$ positiv.
Wegen der fast sicheren Erhaltung verschwindet die Abbildung fast
ueberall. Eine stetige Funktion, die irgendwo ungleich null ist, waere
auf einer offenen Umgebung ungleich null; diese Umgebung hat positive
Wahrscheinlichkeit. Also verschwindet die Abbildung fuer **alle** u.

Damit darf man in jedem Schritt denselben Ort a als Kontrollwert
einsetzen. Die Erhaltung gilt entlang dieser Folge algebraisch. Mit
der Konvergenz aus Abschnitt 1 und der Stetigkeit von Q folgt

$$
Q(x,\mu)=Q(a,\mu_N)\longrightarrow Q(a,\delta_a).
$$

Ein festes a kann fuer alle Starts gewaehlt werden. Deshalb ist Q
konstant. Es wird weder eine positive Wahrscheinlichkeit der exakt
konstanten Bahn noch eine stationaere Verteilung vorausgesetzt.

Eine gleichartige Aussage gilt fuer normierte, endlich-zweitmomentige
verschobene Depositionsprofile G: gemeinsames Koppeln gibt Konvergenz
nach $(a,G_a)$. Fuer den hier geprueften kanonischen Fall genuegt die
Punktdeposition; keine neue Feldvariable wurde eingefuehrt.

### Was der Satz nicht sagt

Er liefert keine Aufenthalts-, Austritts- oder Mischzeit. Kontrollierte
Orte sind keine wahrscheinlichen physikalischen Bahnen. Er behandelt
keine Grobkornladung, die nur in einem Grenzmodell definiert ist, keine
singulaeren oder nur auf einem eingeschraenkten Sektor definierten
Readouts und keine Ladungsbilanz eines zusaetzlichen Mediums. Auch eine
konstante Gesamtladung und lokale Gegenladungen bleiben moeglich.
Ein topologisches Label kann etwa an Defektkonfigurationen unstetig
sein; ob solche Konfigurationen physikalisch ausgeschlossen sind, muss
ein gesonderter Modellvertrag entscheiden.

## 3. Gegenbeispiel: exakte Information ohne stetige Observable

Auf demselben Massraum betrachte

$$
Q_{\rm supp}(\mu)=\mathbf1_{\{\operatorname{supp}\mu\text{ ist unendlich}\}}.
$$

Da $q>0$, ist der neue Traeger der alte Traeger vereinigt mit hoechstens
einem Punkt. Endlicher Traeger bleibt nach jedem endlichen Update
endlich, unendlicher Traeger bleibt unendlich. Also ist dieses Label
exakt invariant fuer beliebige Schreiborte, auch mit positivem Rauschen.
Es ist messbar: Die Menge der Masse mit Traegerumfang hoechstens k
ist schwach abgeschlossen. Haette ein Grenzmass k+1 Traegerstellen,
gaebe es k+1 disjunkte offene Umgebungen mit positiver Masse; schwache
Konvergenz erzwingt positive Masse in allen diesen Umgebungen auch bei
hinreichend spaeten Folgengliedern, ein Widerspruch. Die Vereinigung
ueber endliches k ist daher Borel-messbar.

Das Label ist jedoch nicht stetig. Starte beispielsweise mit einer
normierten Gaussverteilung und schreibe wiederholt a. Jedes endliche
$\mu_N$ besitzt weiterhin unendlichen Traeger und damit $Q_{\rm supp}=1$,
waehrend $\mu_N\to\delta_a$ in $W_2$ und $Q_{\rm supp}(\delta_a)=0$.
Ein beliebig kleines, niemals exakt geloeschtes Gewicht traegt das Label.
Es unterscheidet hier Praeparationen, erzeugt aber keine Teilchenladung.
Auf einer engeren Klasse von Historien, deren Traeger stets unendlich
ist, waere dieses konkrete Label ohnehin konstant.

Bei einer beschraenkten Testfunktion $\varphi$ und zwei Memories mit
gemeinsamer vorgegebener Schreibfolge gilt hingegen exakt

$$
\int\varphi\,d(\mu_N-\nu_N)
=q^N\int\varphi\,d(\mu_0-\nu_0).
$$

Dies umfasst das direkte Gausskraft-Readout bei **festgehaltenem**
Probeort. Es ist kein Fehlergesetz fuer selbstkonsistent bewegte Proben.
Die strukturelle Unterscheidung zwischen erhaltener Information und
regularer Auslesbarkeit stimmt mit der bestehenden vorsichtigen
Formulierung in Paper I ueberein; keine thermodynamische Irreversibilitaet
wird aus dem Vergessen gefolgert. Auch Gleitkomma-Unterlauf ist keine
mathematische Loeschung eines positiven exakten Restgewichts.

## 4. Grenzfaelle sind verschiedene Fragen

| Grenzgang | Gesicherte Aussage | Was dadurch nicht gewonnen wird |
| --- | --- | --- |
| H nach unendlich, festes $\alpha>0$, $\varepsilon>0$ | Die endliche Dichteaequivalenz entfaellt. Der neue stetige Invariantensatz bleibt auf dem angegebenen untrunkierten Zustandsraum gueltig. | Keine robuste Ladung allein durch mehr Speicher. Unstetige oder auf anderen Raeumen definierte Sektoren sind gesondert zu untersuchen. |
| $\varepsilon\to0$ bei festem positivem Wert vor dem Grenzuebergang | Fuer jeden positiven Wert gelten die jeweiligen Saetze. Keine uniforme Uebergangszeitschranke folgt daraus. | Lange Stabilitaet ist nicht exakte Erhaltung; die rauschfreie Grenzdynamik braucht eigene Invarianten- und Stabilitaetsbeweise. |
| Genau $\varepsilon=0$ | Das Volltraegerargument ist nicht anwendbar. Schon $\eta=0$ liefert den trivial konstanten Ort x. | Dieses triviale Gegenbeispiel liefert weder Bindung, Ladung noch Quantisierung und waehlt keinen physikalischen Ast. |
| $\alpha\to0$ bei festem endlichem H und unveraenderten nativen Gewichten | $W_H=M_0[1-(1-\alpha)^H]\leq M_0\alpha H\to0$. | Das ist keine Memory gleicher Masse mit immer laengerer Lebensdauer. Nachnormierung waere eine geaenderte Konvention. |
| $\alpha\to0$ in der untrunkierten normierten Rekursion bei fester Schrittzahl | $\mu^+-\mu=\alpha(\delta_{x^+}-\mu)$ verschwindet in schwachen beschraenkten Readouts; bei genau null friert die Memory ein. | Ein eingefrorener Anfangszustand ist keine dynamische Erzeugung von Teilchentypen. Ein reskalierter Zeitgrenzfall ist gesondert zu definieren. |
| $H(\alpha)\alpha\to C\in(0,\infty)$, $\alpha\to0$ | Der Tail $q^H\to e^{-C}$ bleibt positiv. Fuer verschwindenden Tail braucht man $\alpha H\to\infty$. | Eine feste Anzahl von Memory-Zeitskalen im Buffer ist kein exakter unendlicher Horizont. |

Insbesondere vertauschen die Massengrenzen nicht:

$$
\lim_{\alpha\to0}\lim_{H\to\infty} W_H=M_0,\qquad
\lim_{H\to\infty}\lim_{\alpha\to0} W_H=0.
$$

Ein Kontinuumsgrenzfall muss zusaetzlich Schrittzeit, Drift und Rauschen
skalieren und die Konvergenz der Observablen beweisen. Er ist nicht durch
die Wahl eines kleinen numerischen alpha bereits hergestellt. Die
bisherigen Fixed-alpha-Rootzertifikate pruefen eine andere Frage,
naemlich Existenz eines vorbereiteten Orbits; sie belegen weder eine
stochastische Invariante noch deren physikalische Ladung.

## 5. Verifikation, Literatur und Entscheidung

Die [konstruierten Kontrollen](../../tests/test_fading_memory_limits.py)
pruefen die ausgerollte Massengleichung und Transportkosten mit exakten
Bruechen, gemeinsame Praefixe, das vorhandene Gausskraft-Readout und
die endlichen Massenskalierungen. Ein Unterlaufbeispiel verhindert die
Verwechslung von exakt positiv mit numerisch null. Diese Tests beweisen
keinen unendlichen Grenzwert und ersetzen nicht die Argumente oben.
Die bereits vorhandenen Spektraltests kontrollieren die affine Rekursion
ebenfalls fuer vorgegebene Orte; sie werden nicht als neue Entdeckung
oder als ungezwungene Bahnkontraktion umgedeutet.

Verifikation am 2026-11-04: **52 gezielte Tests bestanden in 2.32 s**,
darunter zehn neue algebraische Kontrollen. Die konfigurierte Ruff-
Pruefung, der strikte MkDocs-Bau und die Whitespacepruefung bestehen.
Keine vollstaendige Repository-Testsuite, kein Beweisassistenten-Zertifikat,
keine neue Zielbahn und keine stochastische Stichprobe.

Gezielter Literaturabgleich, kein systematischer Review:
[Grigoryeva und Ortega, Differentiable reservoir computing,
JMLR 20(179), 1-62 (2019)](https://www.jmlr.org/papers/v20/19-150.html).
Gelesen wurden Abstract, die begriffliche Einleitung und die Definitionen
gewichteter Normen und stetiger Fading-Memory-Abbildungen in Abschnitten
2.1/2.2 der [publizierten Fassung](https://jmlr.org/papers/volume20/19-150/19-150.pdf).
Der Beitrag dient der begrifflichen Trennung von Informationen,
Vergessen und Kontinuitaet. Seine Reservoir-, Universalisierungs- und
Differenzierbarkeitssaetze werden nicht auf unsere selbstgekoppelte
Dynamik uebertragen. Der hier benoetigte Invariantensatz ist oben
direkt bewiesen; eine Neuheitsbehauptung wird nicht erhoben.

Die offene Richtungsfrage wird damit praeziser: Ein Grenzfall braucht
einen benannten Mechanismus, der ueber laengeres Speichern hinausgeht,
etwa einen hergeleiteten eingeschraenkten physikalischen Zustandsraum.
Eine explizite Modellerweiterung bleibt die andere, getrennt zu
kennzeichnende Option. Fuer beide fehlen weiter die physikalische
Quellenkopplung, Energiebilanz und der gemeinsame Quanten-/Gravitations-
Anschluss. Die Arbeitsreihenfolge steht ausschliesslich in den
[Projektprioritaeten](../../docs/status/project_priorities.md).
