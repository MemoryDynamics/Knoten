# Review: Homotopie- und Intervalladapter des Horizonttransfers

Datum: 2026-09-09.

Gepruefte Implementierungsrevision:
`59e137968673b88e4cf3d93b2a814d260b67718f`.

Verdict:
**`horizon-homotopy-adapter-pass-no-branch-result-target-closed`**.

## Befund

Die Homotopie erweitert den bestehenden outward-rounded Intervallkern; sie
fuehrt keinen zweiten Residual-, Jacobian- oder Krawczyk-Solver ein. Fuer jede
der exakt 64 registrierten Scheiben wird das volle geschlossene
$s$-Intervall ausgewertet. Residuum und Jacobian umschliessen damit nicht nur
den Scheibenmittelpunkt, sondern alle affinen Zwischensysteme
$F_a+s(F_b-F_a)$ und Zustandsboxen der Scheibe. Die
Krawczyk-Praekonditionierung verwendet den
Punktjacobian am Scheibenmittelpunkt. Benachbarte Krawczyk-Bilder muessen sich
schneiden; der Adapter bricht beim ersten fehlenden strikten Einschluss, bei
fehlender Ueberlappung oder singulaerem Punktjacobian fail-closed ab.

Die Tests wurden in Revision `2a80ade` vor den neuen oeffentlichen Symbolen
committed. Der RED-Zustand bestand aus genau fuenf Fehlschlaegen wegen der
fehlenden Symbole; vier bereits vorhandene Vertragstests blieben gruen. Die
Implementierung besteht danach folgende diskriminierende Tests:

1. direkte Punktstichproben von Residuum und Jacobian muessen in den
   outward-rounded Intervallen liegen;
2. eine Homotopiescheibe muss Stichproben ueber die gesamte
   Parameterinterpolation einschliessen;
3. jede Parameteraenderung ausser $H$ wird verworfen;
4. der Adapter erzeugt genau 64 nichtadaptive Scheiben;
5. Zertifikatsfehler und fehlende Bildueberlappung stoppen am ersten
   fehlerhaften Praefix;
6. ein singulaerer Punktjacobian wird als `inconclusive` mit leerem
   Erfolgspraefix abgebildet;
7. der unabhaengige v3-Validator rekonstruiert einen synthetischen
   Adapterrecord aus dessen Geometrie.

Nach der Implementierung wurde die gemeinsame 2x2-Punktinversion in genau
eine Bibliotheksfunktion gezogen. Protokollkonstanten fuer Rootreihenfolge und
Homotopiekanten stehen nun bei den Modellkonstanten. Dieser kleine
Kuratierungsschritt aendert keine numerische Semantik; 90 fokussierte Tests
und Ruff sind nach dem Refactoring lokal gruen.

Gebundene Implementierungsblobs vor dieser Kuratierung:

- Intervallbibliothek: `462362b2b6c716a882e1427e4d8bc242bd21f3fd`;
- Horizontgate: `899a2e502c7186e2ec190973debe6edb8ff00cd4`.

Die offizielle Linux-CI
[34407208385](https://github.com/MemoryDynamics/Knoten/actions/runs/34407208385)
bestand 1029 Tests, Lint und Dokumentationsbau.

## Evidenzgrenze

Die Tests belegen Intervallschluss, Adaptersemantik und Stopregeln an
synthetischen oder kleinen kontrollierten Faellen. Die Homotopie ist eine
vorregistrierte affine Deformation zwischen zwei diskreten finite-$H$-
Gleichungen; sie behauptet weder einen physikalisch kontinuierlichen Horizont
noch, dass nichtganzzahlige $H$ zum Modell gehoeren. Es wurde keine der sechs
registrierten Horizontkanten numerisch zertifiziert und damit weder ein
zusammenhaengender Rootast noch ein Fixed-alpha-Grenztransfer nachgewiesen.
Der lokale Ausschlussbaum, das tail-augmentierte Zertifikat, LCG-Arnoldi,
Trajektorienabbildung und Backendkomposition bleiben offen. Alle reservierten
Ergebnis-, Manifest-, Audit- und Ergebnisreviewpfade bleiben geschlossen;
weder ein Horizontlauf noch P5-D-Versuch 4 ist autorisiert.

## Naechste Stopregel

Als naechstes darf nur der targetfreie lokale Ausschlussadapter implementiert
werden. Er muss fuer Residualausschluss und Krawczyk-Einschluss denselben hier
geprueften Intervallauswerter verwenden und die bereits im v3-Vertrag
rekonstruierte dyadische Vollpartition liefern. Erst nach dessen Review folgt
das unendliche Tailzertifikat.
