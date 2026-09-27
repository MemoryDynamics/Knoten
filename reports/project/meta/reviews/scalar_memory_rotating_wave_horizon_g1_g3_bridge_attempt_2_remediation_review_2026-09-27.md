# Kritisches Review: G1--G3 Attempt-2-Remediation

Datum: 2026-09-27.

Verdict: **`g1-g3-attempt-2-remediation-code-reviewed-target-closed`**.

## Gegenstand

Dieses Review bewertet ausschliesslich die outcome-blinde Korrektur nach dem
verbrauchten ersten G1--G3-Zielversuch. Es bewertet kein numerisches
Leiterergebnis. Versuch 2 ist nicht autorisiert.

Geprueft wurden das vierfach amendierte Protokoll, das v2-Ergebnisschema, der
One-shot-Guard, Produktionsvalidator, unabhaengiger
Standardbibliotheksauditor und die zugehoerigen targetfreien Tests. Die
numerischen Grundgleichungen, Parameter, Newtonschritte, Homotopie, Boxbreiten,
Gatefolge und Entscheidungsschwellen wurden nicht geaendert.

## Rekonstruktion des Fehlers

Versuch 1 erreichte die erste Homotopiescheibe und stoppte bei
`box.radius: center mismatch`. Der Backendkasten wird durch `mpmath.iv`
auswaerts gerundet. Der alte Validator forderte dagegen zugleich exakt
$u-l=2w$ und $(l+u)/2=c$. Diese Forderung ist fuer korrekt auswaerts
gerundete Endpunkte nicht invariant und war strenger als die bereits fuer
Rootzertifikate verwendete Recordsemantik.

Der unabhaengige Auditor duplizierte dieselbe exakte Homotopiepruefung. Sein
Rootzertifikatspfad enthielt ausserdem noch die entsprechende verdeckte
Exaktheitsforderung. Eine Reparatur nur an der zuerst ausgeloesten Zeile
haette den naechsten Validierungsschritt daher voraussichtlich erneut
blockiert.

## Bewertete Korrektur

Fuer Zentrum $c$, Halbbreite $w$ und Praezision $p$ muss der gespeicherte
Kasten den beabsichtigten Kasten $[c-w,c+w]$ enthalten. Die zusaetzliche
Aufweitung jeder Seite darf hoechstens

$$
\tau_p(c)=\max(|c|,1)10^{4-p}
$$

betragen. Einwaertsrundung und groessere Aufweitung bleiben Fehler. Die
Homotopie verwendet unveraendert $p=120$, also fuer die registrierten
Koordinatenskalen eine Schranke von $10^{-116}$. Rootpanels verwenden ihre
jeweilige 80-/120-dps-Praezision. Produktionsvalidator und Auditor
rekonstruieren die Ungleichungen getrennt aus Dezimalstrings.

Versuch 2 ist durch `attempt=2` in Governance-Autorisierung, Receipt und
Payload gebunden. Receipt, Ergebnis, Report, Audit, Manifest und
Readinessreview besitzen neue `attempt_2`-Pfade. Der vorhandene
Attempt-1-Receipt wird weder gelesen noch ueberschrieben.

## Falsifikation

Die targetfreien Tests pruefen:

1. asymmetrische Auswaertsrundung um $10^{-121}$ beziehungsweise
   $2\times10^{-121}$ wird akzeptiert;
2. Einwaertsschieben einer Grenze um $10^{-121}$ wird verworfen;
3. Auswaertsaufweitung um $10^{-110}$ wird als zu gross verworfen;
4. Produktionsvalidator und unabhaengiger Auditor treffen dieselben
   Akzeptanzentscheidungen;
5. der reale Homotopieadapter verarbeitet asymmetrisch outward-gerundete
   Fake-Backendrecords;
6. falsche Versuchsnummern und Pfadaliasing werden vor Receipt/Target
   verworfen.

Der fokussierte Lauf bestand 133 Tests; Ruff bestand fuer alle geaenderten
Pythondateien. Der vollstaendige lokale Lauf und die exakte offizielle CI
sind bewusst Voraussetzungen des nachfolgenden Readinessreviews und noch
kein Befund dieses Reviews.

## Befunde

- **Kein Critical/Major-Codebefund:** Die neue Ungleichungssemantik ist eine
  eng beschraenkte Serialisierungsgrenze, keine wissenschaftliche
  Schwellenlockerung.
- **Geschlossene Flanke beseitigt:** Der unabhaengige Rootpfad wurde zusammen
  mit dem Homotopiepfad korrigiert; die Reparatur endet nicht an der ersten
  sichtbaren Ausnahme.
- **Versionierung nachvollziehbar:** Der geaenderte Payloadvertrag ist v2;
  Versuch 1 bleibt als gescheiterter Pipeline-Incident unveraendert erhalten.
- **Keine positive Evidenz:** Aus dem erfolgreichen Fake-/Vertragstest folgt
  weder Rootexistenz noch Branchverbindung, Driftpass oder
  $H\to\infty$-Stabilitaet.

## Restrisiken und Stopregel

`mpmath.iv` bleibt der gemeinsame Intervall-Vertrauenskern; der Auditor ist
kein zweiter numerischer Backendbeweis. Die Remediation verhindert eine
falsche Ablehnung korrekt outward-gerundeter Records, kann aber keinen
fehlerhaften Krawczyk-Backendwert erkennen, der innerhalb desselben
Vertrauenskerns entsteht.

Vor einer neuen Nutzerfreigabe muessen der exakte Implementierungscommit,
der vollstaendige lokale Testlauf, Ruff, strikter Docs-Bau und eine
erfolgreiche offizielle CI in einem separaten Readinessreview gebunden sein.
Bis dahin bleibt Governance geschlossen. Dieses Review autorisiert keinen
zweiten Zielzugriff.
