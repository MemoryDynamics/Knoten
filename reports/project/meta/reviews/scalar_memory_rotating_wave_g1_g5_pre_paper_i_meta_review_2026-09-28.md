# Abschliessendes Meta-Review vor Paper I: finite Horizontleiter, G5 und G4

Datum: 2026-09-28.

Verdict: **`finite-branch-paper-i-ready-with-explicit-infinity-gap`**.

## 1. Reviewfrage und Umfang

Dieses Referee-Metareview fragt, welche gemeinsame Aussage aus den
Grundgleichungen, der positiven G5-Komponente, dem G1--G3-Attempt-2-Pass und
der positiven G4-Komponente tatsaechlich folgt. Geprueft wurden:

1. Protokoll, v2-Schema, Runner und One-shot-Governance der G1--G3-Bruecke;
2. Produktionsvalidator und getrennter Standardbibliotheksauditor;
3. Receipt, Ergebnis, Lesereport, Audit und Manifest von Attempt 2;
4. die versiegelten G5- und G4-Komponentenrecords;
5. Git-/CI-Provenienz und die Aenderungsgrenzen zwischen Implementierung,
   Autorisierung und Ergebnisaufnahme;
6. Status-, Katalog-, Prioritaeten- und Paper-Claim-Sprache.

Es wurde kein neuer numerischer Targetlauf ausgefuehrt. Das Review
rekonstruiert vorhandene Records und ihre logische Komposition.

## 2. Reproduzierbare Evidenzkette

### 2.1 Finite Rootfamilie

Attempt 2 enthaelt sieben lokal eindeutige 80-/120-dps-Rootpanels fuer
$H=(600,900,1200,1500,1800,2400,3600)$. Die sechs registrierten
Gleichungshomotopien bestehen 384/384 strikte Krawczyk-Scheiben und alle 378
erforderlichen Nachbarueberlappungen. Damit ist innerhalb der registrierten
Boxen eine zusammenhaengende **finite** lokale Rootfamilie belegt.

Die 120-dps-Koordinaten des Brueckenpanels bei $H=2400$ sind bytegenau die
Koordinaten des versiegelten G5-Finite-Roots. Entsprechendes gilt zwischen
dem Brueckenpanel bei $H=3600$ und dem versiegelten endlichen G4-Root. Die
Endpunktlinks beruhen zusaetzlich auf gegenseitigen Krawczyk-Inklusionen und
nicht nur auf Dezimalgleichheit.

### 2.2 Stabilitaet und Drift

G5 liefert am identischen $H=2400$-Root zwei uebereinstimmende
Largest-modulus-Arnoldi-Panels und drei kontrahierende nichtlineare
Voll-FIFO-Stoerungsarme. Das ist lokale direkte Stabilitaetsevidenz fuer
genau diesen Punkt der finiten Familie, kein Intervallspektralbeweis.

Die zertifizierte normierte Drift sinkt von
$4.5978984\times10^{-9}$ auf $2.5859006\times10^{-11}$; das Verhaeltnis
ist $0.0056241$ und die registrierte Kontraktionsschranke wird bestanden.
Dies ist starke Skalierungsevidenz, aber keine asymptotische Ordnung aus
mehreren unabhaengigen Skalenfolgen.

### 2.3 Separater unendlicher Root

G4 zertifiziert mit zwei strikten 120-/160-dps-Tailpanels einen lokalen Root
von $F_\infty$ unter den registrierten Tailbounds. Beide Tailpanels verwenden
den endlichen $H=3600$-Root als Mittelpunkt. G4s eigener eingefrorener
Claim lautet jedoch ausdruecklich: lokaler $F_\infty$-Root, **kein
Branchtransfer** und keine Stabilitaet.

Der G1--G3-Kompositionscode extrahiert aus G4 ausschliesslich den endlichen
`finite_root`. Er zertifiziert keine Homotopie
$F_{3600}\to F_\infty$. Naehe, gemeinsamer Mittelpunkt und fallende finite
Drift sind starke konsistente Evidenz, aber logisch kein Ersatz fuer diesen
letzten Gleichungstransfer.

## 3. Code-, Audit- und Provenienzreview

- Der geschuetzte Implementierungscommit
  `bdc033293b74ce2115a3006d13d1ba749bb3ef93` bestand 1199 Tests, den
  CI-genauen Ruff-Scope und strict Docs; die offizielle Linux-CI
  `36354118411` war erfolgreich.
- Der Autorisierungscommit
  `f9a6fcf45d1e3beeb81fe001be077076e429316b` veraenderte gegenueber seinem
  direkten Vorgaenger genau die Governance-Datei.
- Receipt und Payload binden Attempt `2`, UUID, Implementierungscommit,
  Ausfuehrungscommit, CI, Schema und Governancehash. Der exklusive Receipt
  entstand vor der Zielrechnung.
- Manifest-last-Publikation bindet Ergebnis, Lesereport und unabhaengigen
  Audit. Die erneute Publikationspruefung stimmt mit allen Hashes und der
  Entscheidung ueberein.
- Der Auditor importiert weder Produktionsgate noch NumPy, SciPy oder
  `mpmath`; er rekonstruiert Schema, Dezimalbeziehungen, Hashes und
  Klassifikation mit der Standardbibliothek. Er ist dennoch kein zweiter
  Intervallbackend und teilt die gespeicherten `mpmath.iv`-Zertifikate als
  Vertrauensbasis.
- Die nach Attempt 1 eingefuehrte outward-rounding Semantik akzeptiert nur
  praezisionsgebundene Aufweitung und verwirft Einwaertsschrumpfung sowie
  uebermaessige Aufweitung in Validator und Auditor.
- Nach Publikation ist Governance wieder geschlossen; ein weiterer
  Zielzugriff ist nicht autorisiert.

Es verbleibt kein Critical- oder Major-Implementierungsbefund in der
publizierten finite-branch Kette.

## 4. Claim-Mapping-Befund des Metareviews

**Major, Dokumentation/Schlussfolgerung; vor Paper I korrigiert:** Die erste
Ergebniszusammenfassung und mehrere aktive Statussaetze bezeichneten den
G4-Endpunkt zu weitgehend als direkten Link zum $F_\infty$-Root. Der
tatsaechlich gebundene Endpoint ist der endliche G4-Root bei $H=3600$.
Der separate $F_\infty$-Beleg liegt zwar in derselben kleinen Umgebung,
enthaelt aber keinen letzten Branchtransfer.

Der numerische Record, seine Klassifikation und der generierte Lesereport
waren bereits enger und korrekt: lokale fixed-$\alpha$-Rootast-Verbindung
mit direkter Stabilitaetsstuetzung bei genau $H=2400$, ausdruecklich keine
$H\to\infty$-Stabilitaet. Korrigiert wurden das kritische Ergebnisreview,
Status, Prioritaeten, Experimentkatalog, Horizontleitfaden und
Paper-Claim-Register. Es wurden keine Zahlen, Gates oder Ergebnisartefakte
umgedeutet.

## 5. Referee-Restpunkte

Die folgenden Punkte sind keine Blocker fuer einen eng formulierten
Paper-I-Abschnitt, begrenzen aber dessen Reichweite:

1. **Infinity gap:** Eine prospektive Homotopie oder andere zertifizierte
   Fortsetzung $F_{3600}\to F_\infty$ fehlt.
2. **Stability gap:** Stabilitaet ist direkt nur bei $H=2400$ numerisch
   geprueft und nicht bis $H=3600$ oder $\infty$ transferiert.
3. **Trust base:** Es existiert noch kein zweiter unabhaengiger
   Intervallbackend.
4. **Spectral scope:** G5 ist kein vollstaendiger Intervallspektralbeweis.
5. **Locality:** Alle Existenz- und Astclaims sind lokal; entfernte Roots und
   globale Eindeutigkeit bleiben offen.
6. **Formation:** Die Homotopie verbindet Gleichungsroots, nicht die
   Entstehung des Orbits aus einem offenen Anfangsdatengebiet.
7. **Physics boundary:** Interaktion, interne Phase, Spin, Impuls,
   Traegheit und physikalische Masse folgen nicht aus dieser Kette.

## 6. Zulaessige Paper-I-Sprache

Als Resultat oder computerassistierter Befund ist tragbar:

> Fuer die registrierten Parameter bei festem $\alpha=0.01$ existiert eine
> lokal Krawczyk-zertifizierte finite Rootfamilie ueber
> $H=600,900,1200,1500,1800,2400,3600$. Der identische Root bei
> $H=2400$ besitzt vorregistrierte direkte lokale Stabilitaetsevidenz; die
> zertifizierte finite Drift faellt auf der letzten Stufe deutlich. Separat
> existiert unter registrierten Tailbounds ein lokaler $F_\infty$-Root in
> derselben kleinen Umgebung wie der finite $H=3600$-Kopf.

Nicht tragbar ist:

> Die finite Familie sei bereits zertifiziert bis $H=\infty$ fortgesetzt
> oder dort stabil; sie sei global eindeutig, spontan gebildet oder ein
> Nachweis von Interaktion, Spin, Traegheit oder Masse.

Im Manuskript sollten finite Astverbindung, direkte H2400-Stabilitaet und
separater $F_\infty$-Existenzbeleg als drei logisch verschiedene Saetze oder
Propositionen erscheinen. Das verhindert, dass ein Leser ihre Komposition
staerker interpretiert als der Code beweist.

## 7. Abschlussurteil

Die finite G1--G5-Evidenzkette ist reproduzierbar, hashgebunden, adversarial
getestet und fuer eine enge Paper-I-Darstellung tragfaehig. Der im
Metareview gefundene Claim-Mapping-Fehler betraf die Dokumentation, nicht den
Resultatvertrag, und ist vor der Manuskriptarbeit korrigiert.

Paper I kann daher beginnen. Ein neuer numerischer Lauf ist fuer den engen
finite-branch Claim nicht erforderlich. Soll spaeter ein echter
$H\to\infty$-Ast- oder Stabilitaetsclaim erhoben werden, benoetigt er ein
neues prospektives Gate fuer die in Abschnitt 5 benannten Luecken.
