# G5-Komponentenlauf: Execution-Incident Attempt 2

Datum: 2026-09-16.

Verdikt: **Attempt 2 verbraucht; `experiment-invalid`; kein G5-Ergebnis;
kein Attempt 3 autorisiert**.

## Ablauf und Provenienz

Der autorisierte Einmalversuch lief auf Governance-Commit
`3c3fe7d8003f13498be5f423eccbb34abc5b2c5e`. Die atomare Attempt-2-Receipt
wurde am 2026-09-16 um 20:54:01 UTC vor der Zielnumerik erzeugt. Sie bindet
den reviewed Implementierungscommit
`7e7610e9e5baa928d4855b269081ec67beb8b25d`, die erfolgreiche CI
`35137838583` und die Autorisierung
`a620c161-0a46-49d7-a26a-81d0eac85d54`. Ihr SHA-256 ist
`298584842752efebafee63152a652082ff84ddb1a02675d0ad112b5e50dff041`.

Finite Root, Grundgleichungs-Preflight und beide Arnoldi-Panels oeffneten die
nichtlinearen Fortsetzungen. Nach ihrer Berechnung brach die abschliessende
Payloadvalidierung ab:

```text
ValueError: $.trajectories.perturbation_arms[1]: trajectory summary mismatch
```

Index 1 ist der registrierte tangentiale Arm. Ergebnis-JSON, Lesereport und
Publikationsmanifest existieren nicht. Die berechneten Zielwerte wurden nicht
persistiert und duerfen nicht durch einen unangemeldeten Wiederholungslauf
rekonstruiert werden.

## Reproduzierbare Source-Diagnose

`run_continuation()` aktualisiert `maximum_distance` bei **jedem**
Integrationsschritt, schreibt in `trace` aber nur jeden zehnten Schritt sowie
gegebenenfalls den letzten Abbruchschritt. Daraus berechnet der Backendrecord

$$
g_{\rm raw}=\frac{\max_{0\leq n\leq N} d_n}{d_0}.
$$

Der Komponentenvalidator sieht nur die ausgeduennte Samplefolge und fordert
dagegen bitweise exakt

$$
g_{\rm record}=\frac{\max_{n\in\{0,10,20,\ldots,N\}} d_n}{d_0}.
$$

Liegt das Laufmaximum zwischen zwei Samples, sind beide wohldefinierten
Groessen verschieden. Genau diese Vertragsverletzung ist fuer Arm 1
beobachtet worden. Der konkrete Abstand und die Differenz wurden wegen des
fail-closed Abbruchs nicht persistiert. Die semantische Ursache ist dennoch
direkt aus den beiden gegensaetzlichen Codepfaden ableitbar; eine Aussage
ueber Vorzeichen oder Groesse der wissenschaftlichen Stabilitaetsmetrik ist
daraus nicht zulaessig.

## Reviewbefund

Der Vorfall falsifiziert die End-to-End-Abdeckung des Readinessreviews. Die
Mocks hatten Zusammenfassungen, deren Maxima auf dem publizierten Raster
lagen; ein off-grid Maximum wurde nicht als Gegenbeispiel getestet. Der
Fail-closed Validator hat dagegen korrekt verhindert, dass ein intern
widerspruechlicher Record publiziert wird.

Eine Remediation muss vor jedem weiteren Zielzugriff prospektiv entscheiden,
welche Groesse der wissenschaftliche Vertrag meint. Belastbar waeren
insbesondere eine voll rekonstruierbare dichte Trajektorie oder ein eigener,
explizit definierter und gepruefter Maximumsrecord. Ein blosses Lockern der
Gleichheitstoleranz waere sachlich falsch, weil es sich nicht um Rundungsrauschen,
sondern um unterschiedliche Stichprobenmengen handelt.

Attempt 2 bleibt dauerhaft verbraucht. Jede Remediation braucht RED-Test,
Code- und Vertragsreview, neue exakte CI, ein eigenes outcome-blindes
Attempt-3-Protokoll und eine neue ausdrueckliche Nutzerfreigabe.
