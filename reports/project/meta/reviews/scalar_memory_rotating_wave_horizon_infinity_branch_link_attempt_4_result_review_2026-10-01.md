# Unendlichkeits-Astlink Attempt 4: kritisches Ergebnisreview

Datum: 2026-10-01.

Verdict: **`g-infinity-branch-link-attempt-4-valid-inconclusive-u4-box-representation-overconstraint`**.

## Ergebnisintegritaet

Der einmalig autorisierte Attempt 4 lief ohne Execution- oder
Publikationsfehler durch. Receipt, Resultat, lesbarer Report, unabhaengiger
Audit und zuletzt geschriebenes Manifest existieren exklusiv. Eine separate
Nachpruefung bestaetigt alle drei Manifest-SHA-256-Werte und den
Standardbibliotheksaudit. Das Receipt hat SHA-256
`8460c1fe55bc44d7f288f6f7049760cabfc3a3ff08a605e3b0f8de90cb8d2c78`.

Die registrierte Entscheidung
`g-infinity-branch-link-inconclusive` ist fuer den eingefrorenen v4-Vertrag
korrekt und wird nicht rueckwirkend umbenannt.

## Beobachtete Gates

| Gate | Befund | Lesart |
| --- | --- | --- |
| U0 | pass | versiegelte Inputs und Provenienz stimmen |
| U1 | pass | Homotopieendpunkte und Tailbound-Replay stimmen |
| U2 | pass | beide 120-/160-dps-Krawczyk-Panels sind strikt |
| U3 | pass | uniforme Regularitaet mit etwa $5.9582\,10^{-6}<1$ |
| U4 | inconclusive | einzig `g4_tail_boxes_match_uniform` ist falsch |
| U5 | pass | beide Krawczyk-Bilder ueberlappen |
| Audit | agrees | Entscheidung, Relationen, Hashes und Report rekonstruiert |

Beide Panels verwenden denselben registrierten Mittelpunkt und dieselbe
Halbbreite $10^{-10}$, sind strikt, regulaer und besitzen einen nichtleeren
gemeinsamen Bildschnitt. Die finite Rootkoordinate liegt in beiden uniformen
Boxen. Die versiegelten G4-Krawczyk-Bilder liegen ebenfalls in beiden
uniformen Boxen.

## Warum U4 scheitert

Der Produktionsklassifikator verlangt zusaetzlich bytegenaue Gleichheit der
outward serialisierten G4-Boxendpunkte und der neu serialisierten uniformen
Boxendpunkte. Diese Bedingung steht staerker im Code als im prospektiven
U4-Text. Das Protokoll verlangt, dass die finite und unendliche
G4-Zertifikatswurzel in der gemeinsamen Box liegen und dort ueber
Eindeutigkeit gebunden sind; es verlangt keine Textgleichheit zweier
unabhaengiger outward Darstellungen derselben Eingabebox.

Die Abweichungen liegen ausschliesslich an den letzten outward Stellen:

- 120 dps: Endpunktdifferenzen von rund $4\,10^{-130}$ bis
  $2.34\,10^{-129}$;
- 160 dps: Endpunktdifferenzen von rund $4.9\,10^{-171}$ bis
  $2.97\,10^{-169}$.

Diese Groessen sind ungefaehr 119 beziehungsweise 159 Dekaden kleiner als
die registrierte Halbbreite. Sie zeigen keine geometrisch verschiedenen
Boxen oder disjunkten Zertifikate. Gleichwohl war die exakte Equality Teil
des eingefrorenen Produktionsentscheids; deshalb bleibt Attempt 4 formal
inconclusive.

## Referee-Befund

Das Ergebnis falsifiziert nicht die uniforme Homotopie: alle unmittelbar
mathematischen Einschluss-, Regularitaets- und Reproduktionsgates bestehen.
Es belegt den Paper-Claim aber ebenfalls noch nicht prospektiv, weil das
registrierte Gesamtgate U4 nicht bestand.

Der Befund ist ein **Major protocol-to-code operationalization defect**:

1. `g4_tail_boxes_match_uniform` prueft exakte Repräsentationsgleichheit statt
   die fuer das Endpunktlemma entscheidende Zertifikatsinklusion.
2. `g4_tail_images_in_uniform_box=True` ist bereits die relevante
   hinreichende Bruecke: Jede vom G4-Krawczyk-Operator eingeschlossene
   $F_\infty$-Wurzel liegt damit in der uniformen Box; deren dortige
   Eindeutigkeit identifiziert beide Wurzeln.
3. Diese logische Schlusskette muss jedoch nach Ergebnissichtung als
   outcome-informierte Reconciliation behandelt werden, nicht als
   nachtraeglicher Attempt-4-Pass.

## Naechster falsifizierbarer Schritt

Kein weiterer Target-Retry ist gerechtfertigt. Zunaechst ist ein strikt
targetfreier Endpoint-Lemma-Audit erforderlich, der nur den publizierten
Attempt-4-Record und die versiegelten G4-/G1--G3-Artefakte liest und getrennt
prueft:

1. Root- und Modellidentitaet;
2. strikten uniformen Einschluss und Regularitaet an $s=0,1$;
3. G4-Krawczyk-Bild als Teilmenge jeder uniformen Box;
4. die daraus folgende Rootidentitaet ohne Boxtextgleichheit;
5. Gegenbeispiele, bei denen Boxueberlappung ohne Bildinklusion nicht reicht.

Ein positives Reconciliation-Urteil waere explizit post hoc und
methodenkorrigierend. Es darf Attempt 4 nicht umetikettieren und ersetzt
weder einen zweiten Intervallbackend noch einen dynamischen
$H\to\infty$-Stabilitaetsbeweis.
