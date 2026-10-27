# Wasserstoff als gemeinsamer Zielbenchmark

Stand: 2026-10-27. Ziel- und Hypothesenvertrag auf Autorenwunsch, kein
Ergebnis, keine neue Modellregel und keine Ausfuehrungsfreigabe. Die einzige
Arbeitsreihenfolge bleibt in den [Projektprioritaeten](../status/project_priorities.md).

## Ein System, gemeinsam pruefbare Eigenschaften

Ziel ist ein zusammenhaengender Nachweis vom Memory-Zustand zu zwei
wechselwirkenden Strukturen und ihren atomaren Observablen. Eine passende
Bahn, ein diskretes klassisches Modenspektrum oder ein einzelner Zahlenfit
genuegt nicht. Der volle Zielumfang wird jetzt festgehalten; nicht jede
Zeile der folgenden Tabelle wird dadurch zum sofortigen Simulationsauftrag.

| Eigenschaft | Physikalischer Zielvergleich | Zu pruefender Ansatz, kein Befund |
| --- | --- | --- |
| Zwei unterscheidbare Strukturen | Lokalisierte, langlebige Komponenten mit eigener Antwort; bei Trennung sinnvoll identifizierbar | Gemeinsame Memory/Feld-Dynamik kann stabilisieren. Einzel- und Paarzustand vergleichen, keine aeussere Falle oder vorgeschriebene Bahn. |
| Traegheit und Massenverhaeltnis | $m_p/m_e=1836.152673426(32)$, CODATA 2022 | Knotengroesse, innere Bewegung, Memory-Gewichte oder Relaxation koennten Traegheit beeinflussen. Masse muss unabhaengig dynamisch bestimmt werden. |
| Ladung und Fernantwort | $q_p=+e$, $q_e=-e$, neutrale Gesamtladung; Coulomb-Grenzfall auf deklarierter Skala | Vorzeichen, additive Bilanz und Kopplung pruefen. Attraktion allein oder ein gesetztes Vorzeichenlabel ist keine Ladungsherleitung. |
| Spin und Statistik | Beide Komponenten haben Spin $1/2$; identische Elektronen bzw. identische Protonen sind Fermionen | FIFO-Rahmen und Konfigurationsraumwege untersuchen. Altersordnung, Umlauf oder Quaternionenvorzeichen ersetzen keine Quantenamplitude und keine Austauschregel. |
| Magnetische Momente | Unterschiedliche freie $g$-Faktoren trotz gleichen Spins: $g_e\simeq-2.00231930436$, $g_p\simeq5.5856946893$ in CODATA-Konvention | Magnetische Antwort aus derselben Ladungs-, Massen- und Spinbeschreibung ableiten; keine separaten Fits pro Zustand. |
| Atomare Bindung und Raumverteilung | Endlicher Grundzustand ohne Kollaps, $1s$-Form mit $\ell=0$, Ionisationsschwelle; im Coulomb-Grenzfall $E_n\propto-1/n^2$ | Effektive Relativdynamik und Energiebilanz herleiten. Eine klassische Kreisbahn ist kein $1s$-Zustand. |
| Rueckstoss und Spektroskopie | Reduzierte Masse, Uebergaenge, Auswahlregeln; spaeter Fein- und Hyperfeinstruktur | Bereits bestimmte Einzelkomponenten muessen gemeinsam diese Observablen vorhersagen. Fuer $1s$ koppeln die Spins zu $F=0,1$ (21-cm-Uebergang). |
| Groesse und innere Struktur | Formfaktoren und getrennte atomare/interne Laengenskalen | Memory-Radius, Ladungsradius, Compton-Laenge und Ausdehnung der relativen Wahrscheinlichkeitsverteilung nicht gleichsetzen. Proton zunaechst effektiv, nicht als elementar behaupten. |

Zahlen und Konventionen: [NIST/CODATA 2022, vollstaendige Tabelle](https://physics.nist.gov/cuu/pdf/all.pdf).
Atomarer Vergleich: [Tong, Atoms, Abschnitte 7.1.1 und 7.1.6](https://www.damtp.cam.ac.uk/user/tong/aqm/aqmseven.pdf).
Die Referenzunsicherheit ist keine bereits beschlossene Simulationsgenauigkeit.
Magnetische Momente freier und gebundener Teilchen sind zu unterscheiden.
In der hier verwendeten Konvention gilt
$\boldsymbol\mu_i=g_i e\mathbf S_i/(2m_i)$ mit $e>0$; ein negatives
Elektronen-$g$ darf nicht nochmals mit einem negativen $q_e$ multipliziert werden.

## Masse aus Groesse: pruefbare Hypothese

Ein geometrischer Readout waere beispielsweise

$$
R_\rho^2=\frac{\sum_j w_j|y_j-\bar y|^2}{\sum_j w_j},
\qquad \bar y=\frac{\sum_j w_jy_j}{\sum_j w_j}.
$$

Dieser Memory-Radius ist weder eine Masse noch bereits ein physikalischer
Ladungsradius. Auch die Modellparameter `memory_mass`, $M_0$, $H$ und eine
inverse OU-Relaxationsrate sind keine nachgewiesenen Teilchenmassen.
Ohne begruendete Energiedichte folgt weder $m\propto R_\rho$ noch
$m\propto R_\rho^3$; eine Compton-Laenge ist ihrerseits keine geometrische
Ausmessung des Knotens.

Zuerst braucht es einen physikalisch definierten schwachen Kraft-Eingriff
und eine gemeinsame Zeit-/Kraftkalibrierung fuer beide Strukturen. Eine
moegliche effektive Antwort auf einem nachgewiesenen Frequenzband waere,
mit Zeitkonvention $e^{-i\omega t}$,

$$
\chi_i(\omega)^{-1}
=k_i-m_i\omega^2-i\gamma_i\omega+\Delta_i(\omega).
$$

Dies ist ein zu pruefender Ansatz, keine angenommene Newton-Dynamik des
FIFO. Ein belastbares $m_i$ verlangt Kontrolle von Rest $\Delta_i$,
Richtungsabhaengigkeit, Fitfenster und Trennung von Reibung/Memory-Effekten.
Eine rein ueberdaempfte Mobilitaet darf nicht als Masse umbenannt werden.
Ein Bewegungsanteil, der nur im Paar existiert, ist zunaechst eine
kollektive effektive Masse, nicht die freie Elektronen-/Protonenmasse.

Erst danach laesst sich ein Zusammenhang mit $R_\rho$, innerer Struktur
oder Memory-Zeitskala testen. Ein an beiden Zielwerten angepasster
Groessen-Massen-Zusammenhang erklaert das Verhaeltnis nicht. Eine
Abweichung in weiteren Praeparationen oder unabhaengigen Antwortmessungen
widerlegt die beanspruchte universelle Zuordnung im getesteten Bereich.

## Spin aus FIFO: die konkrete offene Verbindung

Die [vorhandene Rahmenanalyse](fifo_structure_candidate.md) zeigt fuer
nichtentartete altersmarkierte 3D-Historien eine $SO(3)$-Struktur mit
bedingter $\mathbb Z_2$-Wegtopologie. Im vollen nativen FIFO-Zustandsraum
sind Entartungen erlaubt; dort ist diese Schleife kontrahierbar. Zudem ist
der konkrete H=1200-Kreis [normal instabil](fifo_rigid_structure_limits.md).
Er ist kein nachgewiesener stabiler Spintraeger.

Fuer Spin $1/2$ waeren eine physikalische Quantenbeschreibung mit
$S^2=3\hbar^2/4$, Projektionen $S_a=\pm\hbar/2$, der entsprechenden
Rotationsdarstellung und konsistenter Statistik erforderlich. Ein
$2\pi$-Vorzeichenwechsel muss die Quantenamplitude betreffen, nicht nur
die gewaehlt doppelte Quaternionenbeschreibung desselben klassischen
Rahmens. Sein globales Vorzeichen allein ist keine direkt verschiedene
klassische Messkonfiguration. Austausch zweier identischer Komponenten
ist ein eigener Test; Elektron und Proton sind nicht identisch.

Hopf-Solitonen liefern einen Vergleich, in dem fermionische Quantisierung
unter passenden topologischen Bedingungen moeglich ist. Sie setzt dort
eine Quantisierung voraus, die wir nicht aus FIFO hergeleitet haben:
[Krusch und Speight, Abschnitte 2 und 4](https://arxiv.org/abs/hep-th/0503067).
FIFO bleibt ein Ansatz fuer innere Struktur, kein Ersatz fuer diese Luecke.

## Verknuepfte Vorhersagen statt separater Treffer

Im nichtrelativistischen punktfoermigen Coulomb-Vergleich gelten

$$
\mu_{\rm red}=\frac{m_em_p}{m_e+m_p},\qquad
\kappa=\frac{e^2}{4\pi\epsilon_0},\qquad
a=\frac{\hbar^2}{\mu_{\rm red}\kappa},\qquad
E_n=-\frac{\mu_{\rm red}\kappa^2}{2\hbar^2n^2}.
$$

Diese Referenzgleichungen werden nicht als neue Mikrodynamik eingesetzt.
Mit unabhaengig bestimmten Massen und Kopplung verbindet die gemeinsame
Wirkungsskala $\hbar$ Laenge und Energie. Die reine Coulomb-Vorhersage
$E_2/E_1=1/4$, $E_3/E_1=1/9$ bleibt ein eigener Test. Ein vorgegebenes
Massenverhaeltnis ist ein legitimer Input eines effektiven Atommodells,
aber keine emergierte Teilcheneigenschaft. Unterschiedliche Wirkungsskalen
fuer Masse-, Spin- und Spektralfit waeren keine gemeinsame Quantentheorie.

Die unabhaengig bestimmten magnetischen Momente und die raeumliche
Grundzustandsstruktur muessen anschliessend dieselbe Hyperfeinkopplung
tragen. Ein einfach eingesetzter Spin-Spin-Term reproduziert deren Form
nur als Input. Ein spaeterer Isotopenvergleich erfordert einen separat
definierten Kern; dessen Masse/Radius duerfen nicht rueckwirkend aus den
zu testenden Linien bestimmt werden. Fein-/Hyperfeinstruktur, Kernstruktur
und Strahlungskorrekturen begrenzen die Genauigkeit der Coulomb-Naeherung.

Eine Absorptionskurve verlangt einen definierten Eingriff und Readout;
FFT-Peaks einer klassischen Bahn sind nicht automatisch atomare
Uebergangsenergien. Praeparation, gespeicherte Energie, Dissipation und
gegebenenfalls abgefuehrte Bindungsenergie muessen bilanziert werden.
Ein konservatives Zweikoerpersystem faengt zwei anfangs ungebundene
Komponenten nicht ohne Energietransfer ein. Existenz eines gebundenen
Zustands und seine Formation sind deshalb getrennte Aussagen.

## Vorhandene Bausteine und offene Entscheidungen

Die [B1-Bestandsaufnahme](operational_contract.md) beschreibt vorhandene
Frozen-Source- und direkte reziproke Kopplungen. Die Einzelprozessregel
bestimmt dieses Mehrsystemgesetz nicht. Eine feste Quelle besitzt keine
Rueckwirkung; sie ist nur ein erklaerter Schwerquellen-Grenzfall, kein
Nachweis des endlichen Massenverhaeltnisses. Ein gemeinsames Feld und seine
moegliche stabilisierende Rueckwirkung sind konkret zu spezifizieren.

Skalare, Vektor- und Kernelvarianten gehen als vorhandene Kandidaten in
den Vergleich ein, nicht als gleichzeitig freigegebene Parameterachsen.
Die [Vektormemory-Nullkontrolle](https://github.com/MemoryDynamics/Knoten/blob/4b0a5687ea72afa7fbd1598d85280d67a78461bd/reports/vector_memory/vector_memory_eta_s_zero_control_2026-07-10.md)
warnt bereits davor, komplexe projizierte AR-Moden als isolierten
Vektoreffekt oder Quantisierung zu lesen.

Fuer jeden Kandidaten ist ein gemeinsames Register zu fuellen:

| Eintrag | Vor einer Zielauswertung festzulegen |
| --- | --- |
| Dynamik | Exakte Regel, vollstaendiger Zustand, gemeinsame/artspezifische Parameter und ihre Herkunft. |
| Kalibrierung | Welche Groessen sind gesetzt, unabhaengig gemessen oder aus welchen Daten gefittet? |
| Vorhersage | Welche anderen Observablen bleiben ohne Nachfit als Test zurueck? |
| Fehler | Gueltigkeitsbereich, numerischer und statistischer Fehler, vorab festgelegte Toleranz. |
| Gegenkontrolle | Kopplung aus, Einzel- gegen Paarzustand, Richtungen/Praeparationen sowie geeignete Nullkontrollen. |
| Entscheidung | Was widerlegt den beanspruchten Zusammenhang, was bleibt lediglich unaufgeloest? |

Bewertungsstufen, keine zweite Arbeitsliste: **gebundenes klassisches
Knotenpaar**, **quantenmechanischer Wasserstoff-Benchmark** und
**Identifikation der Komponenten**. Ein Pass der ersten Stufe impliziert
keinen Pass der anderen. Eine vorausgesetzte Schroedinger-/Pauli-Dynamik
kann eine Referenzimplementierung sein, aber keine Herleitung aus Memory.
Eine volle Identifikation verlangt mehr als das endliche Benchmarkpanel,
insbesondere weitere Streu-/Wechselwirkungstests und die zusammengesetzte
Natur des Protons.

3D und ein effektiver Protontraeger duerfen fuer den begrenzten Vergleich
als deklarierte Inputs behandelt werden. Dimensionsemergenz, Gravitation
und die gesamte Flavorstruktur bleiben separate Ziele der
[Forschungsroadmap](../status/research_roadmap.md).
Neue Modellregeln erfordern eine Richtungsentscheidung; konkrete
Ziellaeufe eine separat gepruefte, begrenzte Freigabe. Bestehende
FIFO-/P5-Sperren und verbrauchte Versuchsgenehmigungen bleiben bestehen.
