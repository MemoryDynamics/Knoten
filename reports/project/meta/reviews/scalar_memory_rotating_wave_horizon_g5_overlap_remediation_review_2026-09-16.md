# G5-Overlap-Remediation: targetfreies Review

Datum: 2026-09-16.

Verdikt: **targetfreier Remediation-Pass; Retry weiterhin nicht autorisiert**.

## Anlass und Regel

Attempt 1 scheiterte vor der Publikation, weil ein mathematisch auf $[0,1]$
beschraenkter Arnoldi-Symmetrieoverlap in binary64 geringfuegig ueber die
exakte Recordgrenze lief. Der konkrete verworfene Wert wurde nicht
persistiert; die Rundungsdiagnose bleibt deshalb stark gestuetzt, aber nicht
direkt gemessen.

Die Standardbibliothek kanonisiert nun einen rohen Projektionsoverlap $o$ nur
innerhalb

$$
-\tau_d \le o \le 1+\tau_d,
\qquad
\tau_d = 8\,\frac{d u}{1-d u},
$$

mit Zustandsdimension $d$ und binary64-Maschinenepsilon $u$. Fuer den
registrierten Zustand $d=4800$ ist $\tau_d\approx 8.53\times10^{-12}$.
Innerhalb dieses Budgets wird auf das abgeschlossene Intervall $[0,1]$
abgebildet. Groessere Verletzungen, nichtendliche Werte und ungueltige
Dimensionen brechen weiterhin ab.

## Kritisches Review

- Die Korrektur liegt vor Klassifikation und Serialisierung in der
  wiederverwendbaren Horizon-Stabilitaetsbibliothek; Resultatvertrag und
  unabhaengiger Auditor bleiben strikt auf $[0,1]$.
- Die Klassifikationsgrenze $0.99$ wird nicht aufgeweicht. Nur Werte in einer
  rund $10^{-11}$ breiten Umgebung der mathematischen Endpunkte werden
  kanonisiert.
- Ein Integrationstest erzwingt ein Ein-ulp-Ueberschwingen und verlangt den
  serialisierten Wert `1.0`. Separate Falsifikationstests verwerfen
  $\pm10^{-8}$-Verletzungen, `NaN` und Unendlich.
- 45 fokussierte Horizon-, G5-Vertrags- und Governance-Tests sowie die
  vollstaendige Suite mit 1124 Tests, der CI-Lint und der strikte Doku-Build
  bestanden.

Damit ist die identifizierte Recordgrenze abgedeckt. Nicht gezeigt sind ein
erfolgreicher Wiederholungslauf, Stabilitaet, Instabilitaet oder die
Vollstaendigkeit anderer numerischer Fehlerpfade. Ein Retry erfordert weiter
ein prospektives Protokoll, unabhaengiges Readinessreview, geschlossene
Governance bis zur ausdruecklichen Autorisierung und einen neuen Einmalversuch.
