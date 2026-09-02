# P4-R-S allgemein erklaert

Stand: 2026-08-31.

## Kurz gesagt

Wir haben nicht einfach einen harmonischen Oszillator aufgeschrieben und
daraus nachtraeglich eine Masse abgelesen. Stattdessen wurde eine bereits
vorhandene, rauschfreie Schleife mit endlichem Gedaechtnis genommen. Fuer sie
wurde ein expliziter Rueckwirkungsport konstruiert, dessen Arbeit im Modell
vollstaendig bilanziert werden kann. Danach wurde vorab festgelegt, wie sich
die gemessene Antwort auf einer zweiten, schon vorher existierenden Skala
verhalten muss.

Der zweite Test ist bestanden. Die groesste registrierte Abweichung zwischen
den beiden Skalen ist etwa `0.00233`; erlaubt waren vor Einsicht in den neuen
Lauf `0.05`. Ein getrennt programmierter Auditor rekonstruiert dieselbe
Entscheidung aus den gespeicherten Rohtraces.

Das ist ein guter Befund fuer die diskrete Modellarchitektur. Es ist noch kein
Nachweis von physikalischer Masse, Spin oder einer Wechselwirkung zwischen
zwei Schleifen.

## Was wurde konkret getestet?

Zwei vorbereitete Kreisloesungen desselben finite-memory Modells wurden
verglichen:

- L3 mit `alpha=0.005`, `H=2400`, `eta=0.075`;
- Anchor mit `alpha=0.01`, `H=1200`, `eta=0.15`.

Beide besitzen dieselben dimensionslosen Kombinationen

$$
H\alpha=12,
\qquad {\eta\over\alpha}=15.
$$

Dadurch kann ihre Entwicklung auf derselben Gedaechtniszeit
$\tau=\alpha n$ verglichen werden. Beide Traces enthalten 401 Punkte von
$\tau=0$ bis $\tau=20$; es war keine Interpolation noetig.

Fuer den Anchor wurden 16 Kanal-aus-Kontrollen und 32 aktive Arme gerechnet.
Die aktiven Arme kombinieren acht Startphasen, zwei Drehrichtungen und zwei
Vorzeichen. Diese 32 Arme sind Kontrollen einer deterministischen Symmetrie,
keine 32 unabhaengigen Experimente.

## Warum ist der Test nicht trivial?

Der Kreis selbst garantiert den Pass nicht. Das Protokoll haette den Lauf aus
mehreren voneinander verschiedenen Gruenden stoppen oder falsifizieren
koennen:

- unvollstaendige oder nicht endliche Traces;
- falscher Anchor-Root oder kopierter L3-Gain;
- Verletzung der lokalen Source-/Write-Identitaet;
- Rundungsresiduen ausserhalb konservativer Envelopes;
- fehlerhafte Workbilanz oder negatives Mobilitaetsvorzeichen;
- Verlust der vorbereiteten Schleife;
- falsche Phasenantwort oder zu grosser even-Anteil;
- Verletzung von Spiegelung oder Halbdrehung;
- skalarer statt chiraler Antwort;
- falsches Chiralitaetsvorzeichen;
- abweichende Transienten, Phasenprofile oder Endmittel an der zweiten Skala.

Alle diese registrierten Zweige wurden durchlaufen. Die engste dynamische
Schwelle ist die finale Trennung von Center und Aktuator: beobachtet wurden
`0.0825` Offseteinheiten bei einer Grenze von `0.10`. Die groesste
Skalenabweichung nutzt dagegen nur etwa `4.65%` ihres erlaubten Budgets.

## Was ist dabei emergent, und was wurde konstruiert?

Konstruiert wurden:

- der chirality-konditionierte Center-Readout;
- der dazu adjungierte Source-/Write-Port;
- die Kopplungsstaerke und der kleine Testoffset;
- die Entscheidungsschwellen.

Nicht direkt einprogrammiert wurde der beobachtete zeitabhaengige
Antwortverlauf der vollen nichtlinearen FIFO-Dynamik. Insbesondere wurden die
Anchor-Werte nicht an die zuvor beobachtete L3-Antwort angepasst. Der Anchor
war schon vor dem P4-R-Antwortbefund als Kreisroot zertifiziert und numerisch
stabil getestet.

Die vorsichtige Lesart lautet daher: Die deklarierte Portarchitektur traegt
ihre diskrete, chirality-odd Antwort auf einen zweiten vorbereiteten
Skalenpunkt. Nicht zulaessig waere die staerkere Behauptung, die Natur habe
diesen Port oder seine Parameter selektiert.

## Warum ist das noch keine Masse?

Eine physikalische Masse verlangt mehr als eine endliche Antwort oder einen
positiven Filterkoeffizienten. Es fehlen weiterhin mindestens:

- ein mikroskopisch identifizierter Aktuator;
- ein physikalisch kalibrierter Impuls- und Arbeitsbegriff;
- ein konservierter oder kontrolliert gebrochener Gesamtimpuls;
- ein von der Portwahl unabhaengiger Traegheitsparameter;
- robuste Skalierung ueber mehr als zwei Zellen;
- eine experimentell oder numerisch unabhaengige Replikation.

Der bereits hergeleitete positive Koeffizient
$m_{\rm filter}=\tau/\mu_F$ bleibt deshalb **Filtertraegheit unter einem
gewaehlten Portvertrag**, keine Materialmasse. P4-R-S aendert diese Grenze
nicht.

## Warum ist das noch kein Spin?

Die Kreisbahn ist zunaechst eine raeumliche $SO(2)$-Gruppenbahn. Nach
Quotientieren der ambienten Rotation bleibt beim derzeitigen Nachweis ein
Punkt, keine zusaetzliche interne $S^1$-Phase. Die chirality-odd Antwort zeigt
eine orientierungsabhaengige diskrete Suszeptibilitaet, aber noch keinen
konservierten internen Drehimpuls.

Acht getestete Startphasen plus exakte Spiegel-/Halbdrehungssymmetrie ergeben
auch noch keinen kontinuierlichen Phasenkreis oder Torus. Dafuer waeren eigene
Topologie- und Dynamiktests noetig.

## Was bedeutet das fuer Paper I?

Paper I hat derzeit einen anderen, klareren Hauptclaim:

1. Der sichtbare Prozess ist im Allgemeinen nichtmarkovsch.
2. Position plus Memory bilden den natuerlichen Markov-Zustand.
3. Der bisherige stochastische kleine-Radius-Ast wird weitgehend durch eine
   lineare co-moving Relaxationswolke erklaert.

Der neue P4-R-S-Befund stammt dagegen aus einem rauschfreien
$d=2$-Rotating-wave-Ast mit vorbereitetem Orbit und explizit konstruiertem
Port. Ihn ohne klare Trennung in den Paper-I-Hauptclaim einzubauen, wuerde
zwei verschiedene Evidenzregime vermischen.

Die methodisch sauberste Einordnung ist vorerst:

- Paper I behaelt Markov-Einbettung und lineare Memory-Cloud als Kern;
- der Schleifen-/Portast erscheint als getrennte technische Notiz,
  Supplement-Option oder eng markierter Outlook;
- Paper I darf erwaehnen, dass eine vorbereitete deterministische Erweiterung
  einen zweiten Skalenholdout bestanden hat;
- Abstract und Hauptschluss von Paper I behaupten weiterhin weder
  nichtlineare Knotenmaterie noch Spin, Traegheit oder Masse.

## Was ist jetzt wirklich offen?

P5 darf nun **entworfen und prospektiv protokolliert** werden. Der naechste
Test soll fragen, ob zwei getrennt vorbereitete Schleifen ueber einen
gegenseitigen Port eine Antwort erzeugen, die nicht als Summe zweier
Single-Loop-Relaxationen erklaert werden kann.

Noch geschlossen sind:

- P5-Implementierung ohne vorherigen Design-/Protokoll-Freeze;
- jeder Interaktionsziellauf;
- Ladungs-, Kraftgesetz-, Spin-, Impuls-, Traegheits- oder Masseclaims.

Der naechste Fortschritt ist deshalb kein groesserer Parameterscan, sondern
ein harter Zwei-Loop-Falsifikationsentwurf mit Kanal-aus-, Einweg-, Swap-,
Vorzeichen-, Distanz- und vollstaendigen gegenseitigen Workkontrollen.

## Ein-Satz-Fazit

Die vorbereitete finite-memory Schleife traegt ihren expliziten
Source-/Write-Antworttyp auf einen zweiten, vorab festgelegten Skalenpunkt;
das macht die Modellarchitektur deutlich glaubwuerdiger, aber noch nicht zu
einem Teilchen mit Spin oder Masse.
