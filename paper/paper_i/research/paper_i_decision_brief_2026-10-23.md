# Paper I: Entscheidungsvorlage zum wissenschaftlichen Kern

Stand: 2026-10-25. Interne Bewertung fuer die Diskussion mit Olaf, kein
Fachgutachten und keine Einreichungs- oder Simulationsfreigabe. Die
[Projektprioritaeten](../../../docs/status/project_priorities.md) bleiben
die einzige aktive Arbeitsliste. Die Baseline vom 2026-10-09 bleibt erhalten.

## Empfehlung

**Zuerst den analytischen Beitrag fachlich bewerten, dann ueber einen
Transporttest entscheiden.** Die Frage ist inzwischen praezise genug
fuer eine Diskussion; ihre Publikationsneuheit ist noch nicht belegt.
Weitere Runneroptimierung vor dieser Bewertung ist nicht priorisiert.

Der neue [Vergleich mit statistischer Linearisierung](gaussian_projection_audit_2026-10-24.md)
verschaerft die Frage: Die bekannte Gaussprojektion reproduziert den
vollstaendigen ersten Transportkorrekturterm. Der moegliche Mehrwert liegt
damit im kontrollierten Gueltigkeitsnachweis, nicht in einem von dieser
Naeherung unterscheidbaren $D_4$-Koeffizienten. Der anschliessende
[Satzvergleich](linear_response_scope_audit_2026-10-24.md) grenzt zwei
rigorose Antworttheorien ab: Die Totalvariationsroute scheitert am vollen
Historienzustand. Eine anschliessende direkte Poisson-/Resolventrechnung
kontrolliert nun intern die konkret benoetigten Observablen, zeitlichen
Korrelationen und die Restordnung uniform im Horizont. Ein allgemeiner
Satzimport wird damit nicht behauptet. Beide Herleitungswege nutzen
bekannte Methoden; die offene Frage ist der Wert des kontrollierten
Modellbeispiels, nicht eine neue allgemeine Antworttheorie.

Der nun moegliche [Aging-Volltextabgleich](aging_full_text_comparison_2026-10-25.md)
zeigt zudem eine exakte Zuordnung unserer ungekuerzten linearen Regel zum
Euler-Schema des Preprints, einschliesslich der Startkonventionen. Der
kontinuierliche Diffusionskoeffizient folgt erst im passend skalierten
Zeitschrittgrenzwert. Die lineare Grundlage ist damit konkret abgedeckt;
die Quelle behandelt keine nichtlineare Schwachrauschkorrektur. Das ist
keine Entwarnung zur Neuheit des verbleibenden Gueltigkeitsbeitrags.

Die Leitfrage lautet: **Wann reicht gleiche lokale Kernelkruemmung nicht
mehr aus, um den Langzeittransport vorherzusagen, und laesst sich die
Abweichung ohne Fit an nichtlineare Simulationsdaten berechnen?**

Ein moeglicher Arbeitstitel ist *Controlled weak-noise transport with
exponential memory*. Gemeint ist klassische stochastische Dynamik in einem
vorgegebenen Raum, keine bereits emergente Raumzeit oder Quantentheorie.

## Der konkrete Resultatkandidat

Die volle Dynamik ist

$$
x_{n+1}-x_n=\varepsilon\xi_{n+1}
-\eta\sum_{1\leq j<H}\gamma_j\nabla K(x_n-x_{n-j}),
\qquad \xi_n\overset{\mathrm{iid}}{\sim}\mathcal N(0,I_d).
$$

Fuer ihre stationaeren relativen Inkremente ergibt die
[interne Herleitung](weak_noise_validity_2026-10-21.md) bei festen
Modellparametern und $\varepsilon\to0$ im hinreichenden Bereich
$|\eta|G_2q/\alpha<1$:

$$
D_H(\varepsilon)=\lim_{m\to\infty}
\frac{\mathbb E|x_{n+m}-x_n|^2}{2dm}
=\frac{\varepsilon^2}{2(1+\eta\kappa\mu_H)^2}
-\varepsilon^4\frac{\eta\lambda(d+2)S_H}
{(1+\eta\kappa\mu_H)^3}+O(\varepsilon^6).
$$

Hier sind $0<\alpha<1$, $q=1-\alpha$, $\gamma_j=\alpha q^j$,
$\mu_H=\sum_{1\leq j<H}j\gamma_j$ und
$S_H=\sum_{1\leq j<H}j\gamma_j C_{jj}^{(H)}$. Dabei ist
$C_{jj}^{(H)}$ die pro Koordinate berechnete Varianz des linearen
Einheitsrausch-Lags. Fuer
$K(u)=A_r e^{-|u|^2/(2s_r^2)}-A_a e^{-|u|^2/(2s_a^2)}$ mit
$s_r,s_a>0$ gelten
$\kappa=A_a/s_a^2-A_r/s_r^2$,
$\lambda=A_r/(2s_r^4)-A_a/(2s_a^4)$ und
$G_2=|A_r|/s_r^2+|A_a|/s_a^2$.

Die Rechnung umfasst festes endliches $H$ sowie $H=\infty$ und
kontrolliert den Rest in der unendlichen Kovarianzsumme. Sie ist mehr als
eine Taylorentwicklung der Kraft an einem einzelnen Punkt. Sie liegt
aber noch nicht als unabhaengig fachlich begutachteter Satz vor.
Die Gewichte werden bei endlichem $H$ nicht renormalisiert. Stationaer
ist der relative Zustand, nicht die absolute Position.

Bei $s_r=1,s_a=3$ haben die Kernel $(A_r,A_a)=(0,26)$ und $(1,35)$
dieselbe Kruemmung $26/9$, aber $\lambda=-13/81$ bzw. $23/81$.
Bei gleichem positivem $\eta$ im gemeinsamen Gueltigkeitsbereich haben
ihre ersten Transportkorrekturen daher entgegengesetzte Vorzeichen und
das Verhaeltnis $-23/13$. Bezugswert ist der gemeinsame lineare Transport,
nicht die freie Brownsche Diffusion. Das ist weder Superdiffusion noch
ein Phasenuebergang. **Der Vorzeichenwechsel allein ist kein starker
Neuheitsanspruch:** Er folgt unmittelbar aus der linearen Abhaengigkeit
des ersten Korrekturterms von $\lambda$.

## Was daran noch zu bewerten ist

| Aspekt | Stand und entscheidende Frage |
| --- | --- |
| Physikalischer Mehrwert | Gleiche lineare Antwort verdeckt unterschiedliche nichtlineare Transportantwort. Ist die kontrollierte Aufloesung dieser Entartung interessant genug oder lediglich eine erwartbare Perturbationskorrektur? |
| Naechste Literatur | Der [Neuheitsaudit](pre_reassessment_2026-10-19.md) dokumentiert bereits Memory-Transport, Gaussian-Feedback und perturbative Diffusionskorrekturen. Ein anderes Expansionsargument allein begruendet keine ausreichende Neuheit. |
| Konkrete Vergleichsgrenze | [Kopp--Klapp, Abschnitt IV, Gl. (19)--(22)](https://arxiv.org/pdf/2210.03182v3) verwenden fuer ihre Transportnaeherung kleinen Delay und die Hesse-Matrix am Ursprung. Unser Kandidat entwickelt bei festem Gedaechtnis in kleiner Rauschamplitude. Das unterscheidet diese Rechnungen, beweist aber keine Literaturprioritaet; am 2026-10-23 erneut am Volltext geprueft. |
| Rigorose Methoden | Der [Satzvergleich mit direkter Poissonrechnung](linear_response_scope_audit_2026-10-24.md) liefert intern die konkrete Transportantwort samt Rest $O(\varepsilon^6)$ auf einem zweiten Weg. Das ist keine unabhaengige Begutachtung. Die Einordnung als modellspezifische Anwendung bekannter Methoden wird dadurch staerker. |
| Aging-Vergleich und offene Literatur | Der gelieferte Volltext ist auf Modellebene abgeglichen: exakte lineare Euler-Zuordnung, keine nichtlineare Transportentwicklung. Vorzeichen-/Koeffizientenfehler der gelieferten Fassung sind dokumentiert. Bernard--Wu und die breitere Neuheit des kontrollierten Resultats bleiben auf Satzebene zu pruefen. |
| Vorhandene Daten | Die archivierten Radien pruefen eine lineare Referenz, nicht diesen Transportkoeffizienten. Keine aktive archivierte Zelle liegt im obigen hinreichenden Kontraktionsbereich. |
| Praktische Nachweisbarkeit | Ein analytisches endliches Fehlerbudget existiert, aber nur mit sehr konservativem Rauschbereich. Die Maschinenarithmetik des vollstaendigen Tests ist noch nicht abgesichert. |

## Begrenzter numerischer Aufwand statt offener Optimierung

Das [externe Modellreview](external_review_audit_2026-10-22.md) wurde
nachgerechnet: Seine Koeffizienten tragen, sein urspruengliches
Block-MSD-/Nachweisstaerke-Argument nicht. Der korrigierte gepaarte
Zweilaengen-Schaetzer hat inzwischen ein analytisches
[Gesamtfehlerbudget](finite_noise_transport_budget_2026-10-23.md).
Die illustrative 10%-Grenze ist noch keine registrierte Testtoleranz.

Die [exakte Restdarstellung](paired_residual_precision_2026-10-23.md)
verhindert die problematische Subtraktion des linearen Hintergrunds.
Die neue [Fehlerfortpflanzungspruefung](paired_error_propagation_2026-10-23.md)
liefert eine bedingte zeituniforme Zustandsschranke und einen separat
begrenzten Summationsbaum. Noch fehlen lokale Fehlergrenzen der
tatsaechlichen Updates, kontrollierte Laggrenzen und die vollstaendige
Statistik-/Innovationsschnittstelle. Das ist kein Langlaufzertifikat.
Der zuvor gemessene unoptimierte Referenz-Mikrobenchmark ergibt bei
naiver Hochrechnung rund 145 serielle Stunden fuer zwei Milliarden Paarupdates,
ohne RNG, Statistik und I/O; eine optimierte Laufzeit ist nicht bekannt.

**Entscheidungskriterium:** Nur wenn der Resultatkandidat wissenschaftlich
traegt und ein begrenzter Test mit vorab festgelegtem Fehler- und
Kostenbudget realistisch ist, einen solchen Test entwerfen und freigeben.
Ein aufgeloester Gegenbefund muss die Vorhersage verwerfen koennen;
ungueltige Voraussetzungen oder unzureichende Genauigkeit ergeben dagegen
keinen Test der Theorie. Ein korrektes asymptotisches Resultat kann auch
ohne Milliardenlauf bewertet werden. Ein erfolgreicher Lauf wuerde
umgekehrt eine fehlende Neuheit nicht ersetzen.

## Drei Fragen fuer die fachliche Diskussion

1. Liefert die explizite, horizontuniforme Restkontrolle des bereits durch
   statistische Linearisierung reproduzierbaren Koeffizienten einen
   substanziellen Beitrag, oder ist sie eine routinemaessige Anwendung
   bekannter Antwort- und Kopplungsmethoden? Die direkte Poissonrechnung
   liefert inzwischen auch den konkreten Antwortbeweis, keine neue Methode.
2. Welche Luecke sieht der Leser in der stationaeren Herleitung und
   ihrer Gueltigkeitsdomain? Besonders kritisch: schwaches Rauschen,
   langer Beobachtungszeitraum und unendliches Gedaechtnis.
3. Welche Evidenz wuerde die Beurteilung wirklich aendern: ein eng
   spezifizierter Vollkrafttest, ein staerkerer analytischer Satz oder
   eine andere physikalische Fragestellung?

Bei positivem Urteil kann die Manuskriptfolge Modell und lineare
Entartung, kontrollierter nichtlinearer Transport, gezielter Test sowie
Gueltigkeitsgrenzen lauten. Bei fehlendem Mehrwert bleibt die bestehende
Fassung ein technischer Anker; ein Journalwechsel allein behebt das nicht.
FIFO-Orbits gehoeren weiterhin in die getrennte Arbeit. Das hier notwendige
finite-$H$-/Trunkationsargument ist lediglich die Kontrolle derselben
Transportaussage, kein Import des FIFO-Stabilitaetsprogramms.

Fuer das Fernziel bleibt die [R0/B1-Architekturentscheidung](../../../docs/status/architecture_decision.md)
getrennt: Ein klassischer Transportkoeffizient liefert kein physikalisches
Mehrsystem-/Messgesetz und keinen Anschluss an Gravitation oder das
Standardmodell. Die bestehende Regel wird bis zur Autorenentscheidung
nicht erweitert. Diese Vorlage ist vorbereitet, nicht an Olaf versendet.
