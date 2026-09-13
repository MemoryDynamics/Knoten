# Readiness-Review: einmaliger G4-Komponenten-Retry

Datum: 2026-09-13.

Verdict:
**`g4-component-retry-ready-after-green-exact-ci`**.

## 1. Umfang

Geprueft ist ausschliesslich der nach dem invaliden Erstlauf neu autorisierte
Retry des isolierten G4-Komponentengates. Vollstaendiger Horizonttransfer,
LCG-Arnoldi/G5, P5-D und Zwei-Knoten-Transfer bleiben geschlossen.

## 2. Versuchstrennung

Der Erstlauf bleibt unveraendert als
`g4-experiment-invalid-outward-box-validation` dokumentiert. Das neue
Retry-Protokoll besitzt einen eigenen Hash und wird vom Runner sowie vom
unabhaengigen Auditor explizit gebunden. Es gibt keine Rekonstruktion oder
Uebernahme nicht publizierter In-memory-Ergebnisse des Erstlaufs.

## 3. Delta-Review

Start, Parameter, $H=3600$, Newtonschritte, Boxbreiten, Domain, Tailformeln
und 120/160-dps-Panels sind unveraendert. Die einzige numerische
Vertragsaenderung betrifft die Serialisierung: Die gespeicherte Box muss das
ideale Dezimalintervall enthalten, und ihr zusaetzlicher Außenrand ist durch
$\max(1,|c|)10^{4-p}$ begrenzt. Diese Grenze liegt viele Groessenordnungen
unter jeder registrierten wissenschaftlichen Boxbreite.

## 4. Falsifikatoren

Komponentenvalidator, Standardbibliothek-Auditor und gemeinsamer
Horizontvalidator akzeptieren gezielt einen backendtypischen
$10^{-121}$-Ueberschuss bei 120 dps. Sie verwerfen groessere Abweichungen,
nichtendliche Newtonwerte, disjunkte Bilder, unvollstaendige Panelfolgen,
mutierte Bounds, Reportdrift, Hashfehler, unbekannte Felder, vorhandene
Zielartefakte und einen unsauberen Arbeitsbaum.

## 5. Lokale Verifikation

- 94/94 gezielte G4- und Horizontvertragstests bestanden;
- 1063/1063 Repositorytests bestanden;
- der exakte CI-Lint-Scope bestand;
- Dokumentationsarchitektur und strikter Dokumentationsbau bestanden;
- seit der neuen Freigabe wurde kein Zielrunner gestartet;
- die reservierten Ergebnisartefakte sind nicht vorhanden.

## 6. Ausfuehrungsbedingung

Der Retry darf genau einmal starten, wenn Protokoll, Runner, Auditor, dieses
Review und die Tests gemeinsam in einem sauberen Commit liegen und die
exakte GitHub-CI dieses Commits gruen ist. Jeder technische Fehler,
regulaere Zertifikatsfehlschlag oder Publikationsabbruch stoppt ohne
Retuning und ohne weiteren Retry.

## 7. Claimgrenze

Ein Pass waere nur ein lokales, modell- und backendkonditionales
Existenzzertifikat fuer einen Root von $F_\infty$. Er waere kein Beleg fuer
Branchidentitaet, lokale Stabilitaet, Attraktion, Schleifenkopplung,
Interaktion, interne $S^1$-Phase, Traegheit oder Masse.
