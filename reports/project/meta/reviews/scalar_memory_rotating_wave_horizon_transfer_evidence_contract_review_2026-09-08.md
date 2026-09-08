# Negativreview: wissenschaftliche Vollstaendigkeit des Horizontvertrags v2

Datum: 2026-09-08.

Gepruefte Implementierungsrevision:
`b7b75be328de766de73fed61407b13dd67315060`.

Vorausgehendes v2-Review:
`a9d67b68c5c4439dfacaa35984c080659d7d58a4`.

Verdict:
**`rotating-wave-horizon-transfer-contract-v2-evidence-incomplete-v3-required-target-closed`**.

Der v2-Vertrag schliesst die Null- und Abbruchsemantik korrekt, bildet aber
nicht alle im Protokoll geforderten wissenschaftlichen Nachweiselemente ab.
Er reicht deshalb nicht fuer die Implementierung eines publishbaren Runners.
Dieser Befund entstand bei der targetfreien Abbildung vorhandener
Standardbibliotheken auf die Runnerstufen. Es wurden keine registrierten
Roots, Homotopien, Spektren oder Trajektorien ausgewertet.

## 1. Blockierende Befunde

### HT-EC01: Aeusseres und inneres Rootzertifikat sind kollabiert

Das Protokoll verlangt fuer jedes 80-/120-dps-Panel getrennte
Krawczyk-Zertifikate mit Halbbreiten `1e-8` und `1e-30`. Die vorhandene
Bibliothek rechnet diese ebenfalls getrennt. v2 besitzt jedoch nur
`certificate_80` und `certificate_120`, also insgesamt zwei statt vier
Zertifikate. Der Runner muesste das aeussere oder das innere Zertifikat
unterschlagen; `inner_intersection` waere dann keiner gespeicherten
eindeutigen Quelle zugeordnet.

### HT-EC02: Branch-Ausschlussblaetter enthalten keinen Beweisrecord

Ein Exclusion-Leaf speichert nur Box, Tiefe und die behauptete Klassifikation
`residual-excluded`, `krawczyk-root` oder `unresolved`. Fuer
`residual-excluded` fehlen die beiden ausgewerteten Residualintervalle; fuer
`krawczyk-root` fehlen Krawczyk-Bild und strikte Inklusion. Runner und Auditor
koennen daher nicht unterscheiden, ob ein Label durch Intervallrechnung
getragen oder lediglich gesetzt wurde. `local_branch_excluded=true` waere
damit nicht auditierbar.

### HT-EC03: Mehrere Intervall-Summaries werden nur vertraut

v2 rekonstruiert noch nicht aus den gespeicherten Dezimalendpunkten:

- die Mittelpunktdifferenz der 80-/120-dps-Newtonpfade gegen `1e-50`;
- den Schnitt der beiden inneren Root-Krawczyk-Bilder;
- die exakten Homotopieintervalle `[i/64,(i+1)/64]`;
- die tatsächliche Ueberlappung benachbarter Homotopieeinschluesse;
- Schnitt und Ueberlapp der beiden Tail-Krawczyk-Panels.

Die zugehoerigen Booleschen Felder koennen deshalb derzeit nicht als
fail-closed Nachweis gelten.

### HT-EC04: Arnoldi-Start ist nur als ungebundener Hash gespeichert

Das Protokoll friert zwei konkrete 4800-dimensionale Startvektoren ein. Der
Vertrag speichert zwar `start_sha256`, besitzt aber keine erwarteten
Hashkonstanten und rekonstruiert sie im unabhaengigen Auditor nicht. Zudem
weicht der bestehende allgemeine `S2`-Start in Vorzeichen und Phasenoffset
vom neuen Protokoll ab. Der neue Runner darf ihn daher nicht ungeprueft
erben.

### HT-EC05: Stoerungsregistrierung ist im Ergebnis nicht gebunden

Die drei Trajektorienarme speichern Namen und Abstandsreihen, aber weder
Amplitude noch Hash des tatsaechlich eingesetzten 4800-dimensionalen
Stoerungsvektors. Ein falscher radialer, tangentialer oder projizierter
Voll-FIFO-Stoss koennte denselben Resultvertrag fuellen.

## 2. Erforderliche v3-Remediation

Vor Runnercode muss ein expliziter v3-Vertrag:

1. je Praezision aeusseres und inneres Rootzertifikat speichern;
2. `inner_intersection` ausschliesslich aus den beiden inneren
   Krawczyk-Bildern rekonstruieren;
3. je Exclusion-Leaf die fuer seine Klassifikation erforderlichen
   Residualintervalle oder das Krawczyk-Bild und die strikte Inklusion
   speichern;
4. Homotopie-s-Intervalle, Einschluesse und Tail-Panelueberlapp aus
   Dezimalendpunkten neu berechnen;
5. die beiden exakten Arnoldi-Starthashes als Vertragskonstanten binden und
   unabhaengig aus der Formel rekonstruieren;
6. fuer jeden Stoerungsarm Name, Amplitude und SHA-256 des gerundeten
   Eingangsvektors speichern und aus der eingefrorenen Konstruktion
   rekonstruieren;
7. Mutationen fuer jedes dieser Summaryfelder und jeden fehlenden
   Nachweisrecord vor dem Runner bestehen.

## 3. Abgrenzung zum v2-Pass

Das v2-Review bleibt als Nachweis gueltig, dass fruehe Abbrueche und
partielle Ausgaben ohne erfundene Werte serialisierbar sind. Sein Verdict
oeffnete nur Runner-RED, nicht Runner-Readiness oder einen Zielzugriff. Der
vorliegende tiefere Mappingtest falsifiziert nun diese Oeffnung und ersetzt
sie durch v3-Bedarf.

Bis v3 separat prospektiv registriert, implementiert, getestet und reviewed
ist, bleiben wissenschaftlicher Runner, Horizontlauf und P5-D geschlossen.
