# Topologischer Schutz: Zustandsraum vor Knotennamen

Stand: 2026-11-05; begonnen am 2026-11-04. Analytische Entscheidungsvorbereitung nach den
[Invariantengrenzen](fading_memory_limits_2026-11-04.md), ohne neue
Modellregel oder Zielsimulation. Die Richtungsfrage an den Autor bleibt
offen. Dieser Bericht ergaenzt den bestehenden
[FIFO-Rahmenaudit](../../docs/reference/fifo_structure_candidate.md),
statt dessen SO(3)-Befund erneut als neue Entdeckung zu zaehlen.

## Befund

Die vorhandenen skalaren und vektoriellen Readouts definieren noch
keinen globalen topologischen Ladungssektor. Insbesondere machen
normierte einzelne Orientierungen das summierte Memory-Feld nicht
zu einem ueberall definierten Einheitsvektorfeld. Eine konkrete
alterskonsistente Hin-und-zurueck-Historie liefert unten eine exakte
Nullebene und unterschiedliche normierte Richtungen im Fernfeld.

Bekannte Hopf-Solitonen zeigen eine moegliche **Referenzarchitektur**,
aber keine schon erfolgte Memory-Herleitung. Ihre Voraussetzungen
muessen getrennt geprueft werden: Zielraum und Rand, Erhaltung unter
der Dynamik, Stabilitaet sowie physikalische Kopplung/Quantisierung.
Eine interessante Kurvenform allein ersetzt keinen dieser Schritte.

## 1. Was im Bestand bereits bekannt ist

Der vollstaendige endliche skalare Historienraum ist bei festen Gewichten
$\mathbb R^{dH}$. Er erlaubt Kollisionen, Kollinearitaet und Kollaps.
Die untrunkierte Klasse positiver normierter Masse ist ebenfalls
kontrahierbar, etwa durch $\mu_s=(1-s)\mu+s\delta_a$. Ein geometrischer
Ring oder die Topologie einer ausgewaehlten Dichte-Niveaumenge ist
daher keine automatisch erhaltene Komponente des ganzen Zustandsraums.
Dieser geometrische Befund behauptet weder eine reale Zerfallsbahn
noch eine kleine Uebergangsbarriere.

Der [FIFO-Rahmenaudit](../../docs/reference/fifo_structure_candidate.md)
trennt bereits die Wegklassen $\pi_1(SO(3))=\mathbb Z_2$ von getrennten
Knotentypen. Der Rahmen ist bei Entartung undefiniert, waehrend die
native Gausskraft regulaer bleibt. Die FIFO-Alterslinie ist ausserdem
offen: Der aelteste Eintrag wird entfernt; keine materielle geschlossene
Kurve und kein Kreuzungsverbot sind vorgegeben.

Der neue Punkt ist die Pruefung der bereits vorhandenen Feldvarianten,
nicht ein weiterer Kreis- oder Stabilitaetslauf.

## 2. Explizites Gegenbeispiel fuer das Vektorgedaechtnis

Die Implementierung
[`vector_gaussian_field`](../../src/emergenz_knoten/vector_memory.py)
liest

$$
V(z)=\sum_j w_j u_j\exp\left[-\frac{|z-y_j|^2}{2\sigma^2}\right].
$$

Betrachte in gewaehlten drei Dimensionen die neueste-zuerst-Historie
$y_0=a e_1$, $y_1=-a e_1$, $y_2=a e_1$, $a>0$.
`oriented_history_from_state(mode="unit")` leitet daraus genau zwei
Richtungsdeposits ab: $u_0=e_1$, $u_1=-e_1$ an $y_0,y_1$ mit
$w_0=\alpha M_0$, $w_1=q w_0$, $q=1-\alpha\in(0,1)$.
Das entspricht der Bewegungsfolge $a\to-a\to a$; die Richtungen
werden nicht unabhaengig von den Positionen passend gewaehlt.

Mit $z=(z_1,z_\perp)$ gilt

$$
V(z)=w_0 e_1 e^{-|z_\perp|^2/(2\sigma^2)}
\left[e^{-(z_1-a)^2/(2\sigma^2)}
      -q e^{-(z_1+a)^2/(2\sigma^2)}\right].
$$

Auf der ganzen Ebene

$$
z_1=\frac{\sigma^2}{2a}\log q
$$

ist V exakt null. Die Einzelrichtungen sind trotzdem Einheitsvektoren.
Links und rechts der Ebene zeigt V in entgegengesetzte Richtungen.
Das postprozessierte Feld $n=V/|V|$ ist auf der Ebene undefiniert und
kann nicht stetig ueber sie fortgesetzt werden. Insbesondere sind
die Richtungsgrenzen entlang der positiven/negativen $e_1$-Achse
$+e_1$ und $-e_1$. Dass $V\to0$ fuer grosse Abstaende gilt, ersetzt
keinen festen richtungsunabhaengigen Randwert von n.

Dies ist eine zulaessige konstruierte Historie, keine gemessene
typische Bahn, kein Attraktor und kein Nachweis haeufiger Nulldurchgaenge.
Es widerlegt nur die allgemeine Behauptung, die aktuelle Konstruktion
liefere automatisch ein globales $S^2$-Feld samt konstantem Rand.

Zwei weitere direkte Codebefunde passen dazu: `normalize_orientation`
liefert bei ruhendem Punkt den Nullvektor. Der
[persistente Orientierungsfilter](../../src/emergenz_knoten/oriented_source.py)
fixiert die Laenge nicht; etwa alte Richtung $e_1$, Antrieb $-e_1$
und Relaxation $1/2$ ergeben exakt null. Ein Weglassen solcher Faelle
oder Erzwingen von $|n|=1$ waere eine neue Zustands-/Updatekonvention.

## 3. Weiche Feldenergie ist kein hartes Kreuzungsverbot

Die [kovariante Vektorfeld-Erweiterung](../../src/emergenz_knoten/covariant_vector_field.py)
ist bereits als Zusatzmodell, nicht als native Memory-Ableitung
markiert. Ihre Variablen sind unbeschraenkte Vektoren; ihre lokale
Energie enthaelt quadratische Terme in Feld und Ableitungen sowie
eine quartische Amplitudensaettigung. Es gibt keinen implementierten
Zwang $|m|=1$ und keine Singularitaet bei $m=0$.

Fuer ein glattes, kompakt getragenes Profil m ohne externe Quelle
hat die zulaessige Amplitudenfamilie $m_s=(1-s)m$ bei den dortigen
polynomiellen Termen die Form

$$
F[m_s]=(1-s)^2F_{\rm quadratisch}[m]
       +(1-s)^4F_{\rm quartisch}[m].
$$

Sie bleibt endlich bis zum Nullfeld. Die quadratischen Beitraege
muessen dabei nicht alle positiv sein; hier wird keine monotone
physikalische Relaxation behauptet. Ein geordneter Hintergrund,
andere Randbedingungen oder ein kontrollierter steifer Grenzfall
brauchen eine eigene Analyse. Das Beispiel ist kein No-go fuer
metastabile Texturen oder alle Phasen dieser Zusatzmodelle.

## 4. Was eine Hopf-Referenz zusaetzlich voraussetzt

[Battye und Sutcliffe, To be or knot to be?](https://arxiv.org/pdf/hep-th/9808129)
setzen ein Feld $n:\mathbb R^3\to S^2$, einen festen Randwert
$n_\infty$ und eine Energie mit quadratischem Gradienten- und
quartischem Skyrme-Term voraus. Der Rand erlaubt die raeumliche
Kompaktifizierung zu $S^3$; die Sektoren sind durch die Hopf-Klasse
$\pi_3(S^2)=\mathbb Z$ charakterisiert. Eine als Kurve dargestellte
Feldstruktur ist nicht mit der gesamten Feldabbildung gleichzusetzen;
die Arbeit diskutiert auch Rekonnexionen bei ihrer Relaxation.

Die elementare Skalierungspruefung macht den Energiebedarf sichtbar.
Fuer $n_L(x)=n(x/L)$ in drei Dimensionen gilt

$$
E[n_L]=L E_2[n]+L^{-1}E_4[n].
$$

Volumen bringt $L^3$, jede Ableitung $L^{-1}$. Ohne $E_4$ sinkt
die reine positive Gradientenenergie beim Schrumpfen. Mit positiven
$E_2,E_4$ besitzt die Skalierungsfamilie ein Minimum bei
$L_*^2=E_4/E_2$. Das ist nur ein notwendiger Skalierungscheck, kein
vollstaendiger Existenz-, Formstabilitaets- oder globaler Minimierungsbeweis.
Er darf nicht auf unsere dissipative Memory ohne diese Energie
uebertragen werden. Ein beliebiger vierter Ableitungsterm oder eine
quartische Amplitude ist auch nicht automatisch derselbe Skyrme-Term.

[Krusch und Speight](https://arxiv.org/pdf/hep-th/0503067v2) behandeln
die fermionische Quantisierung von Hopf-Solitonen ueber
Finkelstein-Rubinstein-Bedingungen. Wellenfunktionen auf einer
Ueberlagerung des Konfigurationsraums und ihre Vorzeichenbedingung
werden dabei als Quantenbeschreibung eingefuehrt. Dies zeigt einen
moeglichen Anschluss in einem definierten Referenzmodell, aber keine
Entstehung von Quantenmechanik oder Elektronenspin aus FIFO. Auch die
Hopf-Zahl allein ist noch keine identifizierte elektrische Ladung.

## 5. Kriterien fuer einen wirklichen Anschluss

| Erforderlicher Baustein | Vorhandener Befund | Noch fehlender Nachweis |
| --- | --- | --- |
| Abbildung vom vollstaendigen Memory-Zustand auf das physikalische Objekt | Scalar-Memory, altersabgeleitete Rahmen und gerichtete Feldreadouts vorhanden. | Zielraum, Regularitaet, aeussere Dimension und Rand festlegen; Nullstellen/Defekte nicht stillschweigend ausschliessen. |
| Erhaltung eines definierten Labels | Bedingte Wegtopologie; keine native globale Ladungsidentifikation. | Dynamik muss den relevanten Zustandsraum erhalten. Bei nur effektivem Schutz Fehler- und Zeitbereich angeben. |
| Endliche stabile Ausdehnung | Lokale Rotationsbefunde und getrennte Feldprototypen. | Eine zu genau derselben Struktur gehoerende Energie-/Arbeitsbilanz oder andere kontrollierte Stabilitaetsanalyse; kein Nachfit der Knotengroesse. |
| Physikalische Bedeutung der Zahl | Referenzmodelle besitzen geometrische/topologische Labels. | Kopplung an messbare Quellen, Paarvorzeichen und Erhaltung; keine Gleichsetzung von Hopf-Zahl, elektrischer Ladung, Flavor oder Spin per Benennung. |
| Quanten- und Gravitationsanschluss | Noch offen. | Quantenzustaende, Statistik, Kausalitaet und universelle Energie-/Geometriekopplung aus kompatiblen Annahmen. Ein Soliton allein erledigt diese Aufgaben nicht. |

Das sind Kriterien fuer die offene Richtungsentscheidung, keine Freigabe
eines Hopf-/Skyrme-Simulators. Ohne hergeleitete Zielraumrestriktion
waere ein solcher Simulator ein explizites Referenz-/Erweiterungsmodell.
Die Arbeitsreihenfolge steht nur in den
[Projektprioritaeten](../../docs/status/project_priorities.md).

## 6. Verifikation und Quellenumfang

Die [sechs neuen konstruierten Tests](../../tests/test_topological_state_contract.py)
nutzen die vorhandenen Historien-, Orientierungs- und Feldfunktionen.
Sie pruefen die Nullebene fuer drei feste Geometrien, den Richtungswechsel,
zwei endliche Fernproben ohne Unterlauf sowie die beiden Nullorientierungen.
Die Aussagen ueber die ganze Ebene und den unendlichen Rand folgen aus
der Formel, nicht aus endlich vielen Proben. Keine neue Zielsimulation.

Verifikation am 2026-11-05: **104 betroffene Tests bestanden in 10.71 s**,
einschliesslich der sechs neuen Gegenkontrollen. Die konfigurierte Ruff-
Pruefung, der strikte MkDocs-Bau und die Whitespacepruefung bestehen.
Die am Vortag unterbrochene Freigabepruefung hatte Formatter und Tests
nicht gestartet; beide wurden nach Wiederaufnahme regulaer ausgefuehrt.
Keine vollstaendige Repository-Testsuite, keine unabhaengige Reproduktion
von Hopf-Solitonen und kein formales Beweiszertifikat. Die bekannten
genehmigungspflichtigen Zielpanels bleiben geschlossen.

Quellenumfang: Codefunktionen und bestehender FIFO-Rahmenbericht direkt
gelesen. Von Battye--Sutcliffe wurde die arXiv-v1-Fassung vom 20.08.1998
geprueft: Einleitung/Modell, Gl. (1)-(3), Diskussionspassagen zu
Rekonnexionen und Grenzen der numerischen Minimierung. Keine eigene
Reproduktion und kein kompletter numerischer Methodenaudit. Von
Krusch--Speight wurde v2 vom 09.11.2005 verwendet: Abstract/Einleitung,
Definition des Konfigurationsraums in Abschnitt 2, Modellbeginn in
Abschnitt 3 und Beginn von Abschnitt 4 bis zu den FR-Bedingungen.
Eine anschliessende konkrete Massenskalenanwendung wird hier weder
uebernommen noch aktualisiert. Dies ist ein gezielter Vergleich,
kein systematischer Literaturreview und keine Neuheitsbehauptung.
