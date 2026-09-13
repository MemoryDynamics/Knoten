# Ausfuehrungsreview: isolierter G4-Komponentenlauf

Datum: 2026-09-13.

Verdict:
**`g4-experiment-invalid-outward-box-validation`**.

## 1. Autorisierte Ausfuehrung

Der einzige durch das Komponentenprotokoll autorisierte Zielzugriff startete
vom sauberen Commit `4e813dbd35480c4ba3d0219d0574f03a8e57cd45`.
Die [exakte CI](https://github.com/MemoryDynamics/Knoten/actions/runs/34772024664)
hatte zuvor Lint, 1060 Tests und den strikten Dokumentationsbau bestanden.
Startwert, $H=3600$, Modellparameter und Praezisionen wurden nicht geaendert.

## 2. Beobachteter Abbruch

Die endliche Root- und Krawczyk-Rechnung wurde aufgerufen. Der implementierte
Ablauf ruft danach die Tailpanels auf und validiert erst den fertigen
Payload. Weil der endliche Record nicht `None` war, wurde mindestens das
erste Tailpanel aufgerufen; aus dem Trace ist nicht rekonstruierbar, ob ein
oder beide Panelaufrufe einen strikten Einschluss zurueckgaben. Anschliessend
brach die Ergebnisvalidierung bei
`$.finite_root.outer_certificate.box.radius: registered box mismatch` ab.
Ergebnis-JSON, Lesereport und Manifest wurden nicht geschrieben; der
unabhaengige Ergebnisauditor hatte somit kein publiziertes Ergebnis zu
pruefen. Nicht publizierte In-memory-Panelresultate werden weder als Pass
noch als Fail gewertet.

## 3. Ursache

Der Komponentenvalidator verlangte dezimal exakte Endpunkte
`center +/- half_width`. `mpmath.iv` repraesentiert aber bereits einen aus
einem Dezimalstring erzeugten Punkt als enges outward-gerundetes Intervall.
Nach Addition der registrierten Halbbreite umschliesst die serialisierte Box
die idealen Dezimalendpunkte minimal, ist ihnen jedoch nicht bitweise bzw.
dezimal gleich. Der strikte Gleichheitstest verwarf daher gerade die
garantierte outward-Rundung.

Eine targetfreie Reproduktion mit einer beliebigen Dezimalzahl zeigte
Endpunktueberschuesse in der Groessenordnung der 120-stelligen
Intervallpraezision. Das erklaert den Fehlerpfad, wertet aber weder den
$H=3600$-Root noch ein Tailpanel erneut aus.

## 4. Wissenschaftliche Einordnung

Dieser Ausgang ist **kein** Gegenbeispiel gegen einen Root von $F_\infty$.
Er ist auch kein G4-Pass. Da die Publikationshuelle eine gueltige
Intervallbox faelschlich abwies und keine vollstaendige Messung entstand,
bleibt G4 ungemessen. Aus dem Lauf folgen keine Branch-, Stabilitaets-,
Interaktions- oder Masseaussagen.

## 5. Targetfreie Remediation

Runner und Standardbibliothek-Auditor pruefen nun zwei getrennte Bedingungen:
Die serialisierte Box muss das ideale Intervall vollstaendig enthalten, und
ihr outward-Ueberschuss darf hoechstens eine von der registrierten
Dezimalpraezision abgeleitete kleine Toleranz betragen. Eine neue
Falsifikationskontrolle akzeptiert einen $10^{-121}$-Ueberschuss bei 120 dps
und verwirft einen $10^{-115}$-Ueberschuss. Damit wird outward-Rundung
zugelassen, eine unregistriert vergroesserte Box aber weiter fail-closed
abgelehnt. Die korrigierten Komponenten-, Auditor- und gemeinsamen
Horizontvalidatoren bestehen 1063/1063 lokale Repositorytests, den exakten
CI-Lint-Scope und den strikten Dokumentationsbau.

## 6. Lease- und Wiederholungsgrenze

Der Zielprozess wurde einmal gestartet; diese Einmalfreigabe ist damit
verbraucht. Es erfolgt kein stiller Retry und keine Ergebnisrekonstruktion
aus dem fehlgeschlagenen Prozess. Ein weiterer $H=3600$-Zugriff benoetigt
eine neue ausdrueckliche Nutzerfreigabe nach sauberem Remediation-Commit und
gruener exakter CI.

## 7. Naechster methodischer Haltepunkt

Die Remediation ist targetfrei fertig getestet und reviewed; sie wird mit
diesem Ausfuehrungsreview committed und gepusht. Nach gruener exakter CI
bleibt die Wahl offen: den isolierten G4-Lauf neu autorisieren oder G4
vorerst ungemessen lassen. LCG-Arnoldi/G5 und der gleichnamige historische
Zwei-Knoten-Transfer sind durch diesen Vorfall weder ausgefuehrt noch
freigegeben.
