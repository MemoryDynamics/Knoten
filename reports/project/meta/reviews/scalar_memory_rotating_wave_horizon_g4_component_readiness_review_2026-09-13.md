# Readiness-Review: isolierter G4-Komponentenlauf

Datum: 2026-09-13.

Verdict:
**`g4-component-ready-after-green-exact-ci`**.

## 1. Gepruefter Anspruch

Der Runner darf genau einmal den vorregistrierten $H=3600$-Root aus dem
festen Start berechnen und danach zwei tail-augmentierte Krawczyk-Panels mit
120 und 160 Dezimalstellen auswerten. Ein Pass belegt nur lokale Existenz
eines Roots von $F_\infty$ in der registrierten Box. Er belegt weder den
vollstaendigen Horizontast noch Stabilitaet, Formation, Zwei-Knoten-Transfer,
Interaktion oder Masse.

## 2. Ablauf in einfacher Sprache

1. Der Runner akzeptiert nur einen sauberen, festgeschriebenen Git-Stand und
   `mpmath==1.3.0`.
2. Er berechnet den endlichen Root ohne Parametersuche aus dem eingefrorenen
   Start.
3. Nur wenn beide endlichen Krawczyk-Boxen strikt einschliessen, werden die
   zwei unendlichen Tailpanels nacheinander berechnet.
4. Nur zwei strikt einschliessende und ueberlappende Tailbilder ergeben
   `g4-local-infinite-root-pass`; jeder andere gueltige Ausgang bleibt
   `g4-inconclusive`.
5. Ergebnis und Lesereport werden zuerst geschrieben, das Hashmanifest
   zuletzt. Ein Standardbibliothek-Auditor rekonstruiert die Entscheidung.

## 3. Code-Review und behobener Fund

Der numerische Tailkern war bereits algebraisch und targetfrei reviewed. Im
neuen Publikationsrahmen fand der erste Regressionstest dennoch einen echten
Praezisionsfehler: Die Kontrolle der registrierten $10^{-30}$-Innenbox
verwendete implizit die 28-stellige Standardpraezision von `Decimal`. Dadurch
waere ein korrektes hochpraezises Zertifikat faelschlich abgelehnt worden.
Runner und unabhaengiger Auditor rechnen diese Boxrelation nun explizit mit
200 Dezimalstellen. Der Fehler betraf die Validierung, nicht die
Krawczyk-Auswertung; vor seiner Behebung wurde kein Zielwert berechnet.

Newton-Residual, Punktjacobian, Root, Zertifikatsboxen, Intervalljacobians,
Panelreihenfolge, Panelueberlappung, Klassifikation, Lesereport und Manifest
werden nun auf Typ, Dimension, Endlichkeit und registrierte Bindungen
geprueft. Unbekannte Felder und nicht zusammenhaengend abgeschlossene Panels
schliessen fail-closed.

## 4. Falsifikation statt Bestaetigungssuche

Die Tests injizieren absichtlich fehlende Panels, disjunkte Krawczyk-Bilder,
nichtendliche Newton-Daten, veraenderte Tailbounds, Hashabweichungen,
Reportdrift, unbekannte Felder, vorhandene Zielartefakte und einen unsauberen
Git-Stand. Weder Parameter, Boxbreiten, Startwert noch Praezision duerfen nach
einem negativen Ausgang angepasst werden. Der Lauf darf nicht wiederholt
werden, um ein anderes Ergebnis zu erhalten.

## 5. Unabhaengigkeit und verbleibende Trust Base

Der Ergebnisauditor importiert weder Runner noch Horizontgate und benutzt fuer
Hashes, JSON-Vertrag, Dezimalbounds und Entscheidungslogik nur die
Python-Standardbibliothek. Er ist damit ein unabhaengiger Record- und
Publikationsaudit, aber **kein zweiter Intervallbackend**. Die eigentliche
outward-rounded Einschliessung bleibt konditional auf `mpmath.iv` 1.3.0.

## 6. Lokale Verifikation vor Freigabe

- 8/8 gezielte G4-Komponenten-, Mutations- und Audit-Tests bestanden;
- 1060/1060 Repositorytests bestanden;
- Ruff fuer Runner, Auditor und neue Tests bestanden;
- es wurde kein $H=3600$-Zielroot und kein Tailpanel ausgewertet;
- die drei reservierten Ergebnisartefakte sind noch nicht vorhanden.

## 7. Bedingte Freigabe

Genau ein isolierter G4-Komponentenlauf ist freigegeben, **wenn** dieser
Review, Runner, Auditor und Tests gemeinsam in einem sauberen Commit liegen
und die exakte GitHub-CI dieses Commits gruen ist. Die Freigabe umfasst weder
den vollstaendigen Fixed-$\alpha$-Horizontlauf noch LCG-Arnoldi/G5 noch einen
neuen P5-D- oder Zwei-Knoten-Interaktionslauf.
