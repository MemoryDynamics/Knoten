# Suffizienzreview: amendiertes G1--G3-Brueckenprotokoll

Datum: 2026-09-27.

Gepruefte Amendierungsrevision:
`65f142e9dfb351bda2615fd2aae12689394abb84`.

Gepruefter Protokollblob:
`6dbb768d2fba1ee86c0ef38978125e6b9c6d6969`.

SHA-256 des Protokollinhalts:
`c00cbeddbc0469d58ea6dd3d1b1df584f3571509c477eb5ed7e564f6181f68fb`.

Geprueftes negatives Review: Revision `5f3ea0b`, Pfad
`reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_g1_g3_bridge_protocol_review_2026-09-27.md`.

Verdict:
**`g1-g3-bridge-protocol-sufficient-contract-red-open-target-closed`**.

Die Amendierung schliesst HGB-P01--P06 und definiert eine falsifizierbare
lokale Verbindung zwischen der endlichen Fixed-$\alpha$-Leiter und den
bereits versiegelten G4-/G5-Komponenten. Das Urteil oeffnet ausschliesslich
Ergebnisvertrag und zunaechst rote targetfreie Tests. Es autorisiert weder
einen Leiterroot noch einen Homotopieschlauch, Ergebnisartefakte oder einen
weiteren G4-, G5- oder P5-D-Lauf.

## 1. Schliessung der Reviewbefunde

### HGB-P01/P03 -- geschlossen

Rootidentitaet wird nicht mehr aus einem blossen Intervallschnitt abgeleitet.
Innerhalb jedes 80-/120-dps-Paars und an beiden versiegelten Endpunkten
muessen die inneren Krawczyk-Bilder wechselseitig in den fremden aeusseren
Eindeutigkeitsboxen liegen. Aus $K(X)\subset\operatorname{int}(X)$ folgt,
dass der eingeschlossene Root im Krawczyk-Bild liegt; die Kreuzinklusion legt
ihn deshalb in die Eindeutigkeitsbox des anderen Zertifikats. Die Pruefung
benoetigt keine neue numerische Toleranz.

### HGB-P02 -- geschlossen

Die Amendierung trennt bytegenaue Komposition von numerischer Replikation.
Der Brueckenlauf hasht die fuenf versiegelten Laufzeitinputs und extrahiert
nur Parameter, Schema-ID, Entscheidung und Rootzertifikate. Er berechnet
keine G5-Eigenwertbetraege, Trajektorien oder Transzendentalwerte neu und
ueberschreitet damit nicht die dokumentierte
`same-platform-binary64-transcendentals`-Grenze.

### HGB-P04 -- geschlossen

G6 bindet nun wieder die nichtkreisfoermigen Horizonte 17 und 257, alle
sieben Kreishorizonte, den Fehler $<5\times10^{-14}$, genau $H+1$
Nullkopplungsschritte und die Abweichung $<10^{-14}$. Die drei registrierten
Circular-FIFO-Mutationen bleiben obligatorisch.

### HGB-P05 -- geschlossen

Fuenf Laufzeitinputs sind von drei reinen Governance-Reviews getrennt. Das
Protokoll behauptet keinen nicht vorhandenen G5-Auditoutput. Eine
Inhaltsaenderung kann wegen des vorab gebundenen SHA-256 nicht durch ein frei
gesetztes Entscheidungsfeld kaschiert werden.

### HGB-P06 -- geschlossen

Der nicht registrierte lower-tail-loss-Ausgang ist entfernt. Der Stressast
kennt nur `pass` oder `inconclusive`; der lokale Ausschlussbaum bleibt auf
die vier Vorwaertskanten beschraenkt.

## 2. Wissenschaftliche Suffizienz

Die Bruecke trennt vier logisch verschiedene Aussagen:

1. G1 zertifiziert lokale Roots an den diskreten endlichen Leiterzellen.
2. G2 zertifiziert denselben lokalen Ast ueber feste affine
   Homotopieschlaeuche; es behauptet keinen physikalisch kontinuierlichen
   Horizont.
3. G3 verlangt schrumpfende outward-rounded Rootdrift.
4. Kreuzinklusion verbindet die neuen $H=2400$- und $H=3600$-Roots mit den
   bereits versiegelten Komponenten.

Damit kann ein positiver Lauf die bisherige logische Luecke schliessen, ohne
G4 oder G5 erneut auszufuehren. Ein Homotopie- oder Krawczykfehler bleibt
`inconclusive`; nur die vollstaendige lokale Residualausschlusspartition darf
Branchverlust melden. Die Entscheidungsrangfolge verhindert, dass fehlende
Evidenz als positiver oder negativer Astclaim erscheint.

## 3. Verbleibende Vertrauens- und Claimgrenzen

- Alle Root-, Homotopie- und Tailzertifikate vertrauen weiterhin demselben
  `mpmath.iv`-Backend; Kreuzinklusion ist keine zweite Intervallreplikation.
- Die festen Boxen und 64 Scheiben koennen fuer einen existierenden Ast zu
  eng sein. Ein solcher Fehlschlag ist numerisch unentschieden.
- G4- und G5-Ausgaenge waren vor diesem Protokoll bekannt. Outcome-blind ist
  nur der neue G1--G3-Zugriff; die Evidenzkomposition selbst ist bewusst
  retrospektiv hashgebunden.
- Lokale Stabilitaet bei $H=2400$ plus Rootast-Verbindung impliziert keine
  Stabilitaet des $H=\infty$-Systems und keine stabile offene Parameterfamilie.
- Formation, Interaktion, Spin, Traegheit und Masse bleiben ausserhalb des
  Gates.

Diese Grenzen sind im Protokoll entscheidungswirksam oder explizit
claimbeschraenkend und blockieren den targetfreien Vertragsschritt nicht.

## 4. Autorisierte naechste Grenze

Der naechste Commit darf ausschliesslich einen fail-closed Komponentenvertrag
und zunaechst scheiternde Tests einfuehren. Die Tests muessen mindestens
verwerfen:

- fehlende, falsch geordnete oder nur teilweise Rootpanels;
- blossen Innenbildschnitt ohne Kreuzinklusion;
- falsche oder unvollstaendige Homotopiescheiben;
- unbewiesene oder unvollstaendige Ausschlusspartitionen;
- falsche Driftrekonstruktion;
- geaenderte G4-/G5-Datei- oder Manifesthashes;
- falsche Endpunktinklusionen und frei gesetzte Komponentenentscheidungen;
- abgeschwaechte G0-/G6-Kontrollen;
- positive Klassifikation nach einem abgebrochenen Praefix;
- Publikation vor vollstaendigem, validiertem Record.

Alle wissenschaftlichen Backends sind in dieser Stufe durch Traps oder
synthetische primitive Records geschlossen. Erst ein dokumentierter
RED-Zustand oeffnet die kleinste targetfreie Implementierung. Danach bleiben
separates Code-/Readinessreview, sauberer Commit, gruene exakte CI und neue
Nutzerfreigabe zwingend.
