# Review: lokaler Ausschlussadapter des Horizonttransfers

Datum: 2026-09-09.

Gepruefte Implementierungsrevisionen:
`84fa8a9472e9ec3ad6ed8e160e142ef61e7a05b9` und
`54bb211b5578c88c828114e22ca65797d9301e33`.

Verdict:
**`horizon-local-exclusion-adapter-pass-no-branch-result-target-closed`**.

## Befund

Der Adapter implementiert den vorregistrierten lokalen Falsifikator, nicht
eine neue Rootsuche fuer die primaere Leiter. Nach einem extern festgestellten
Fortsetzungsfehler schneidet er die Box
$[R_{\rm prev}-0.02,R_{\rm prev}+0.02]\times
[\theta_{\rm prev}-0.002,\theta_{\rm prev}+0.002]$ mit der festen Domain
$[0.8,1.1]\times[0.01,0.022]$. Eine FIFO-Warteschlange halbiert bis maximal
Tiefe 20 jeweils die laengere auf die Domainbreiten $0.3$ und $0.012$
normalisierte Kante.

Jede Box wird zuerst durch den gemeinsamen outward-rounded
`interval_balance_and_jacobian_box`-Kern ausgewertet. Schliesst mindestens
eine Residualkomponente Null aus, entsteht ein `residual-excluded`-Leaf.
Andernfalls wird die bestehende Krawczyk-Bibliotheksfunktion auf derselben Box
aufgerufen. Nur die aus den gespeicherten Intervallendpunkten rekonstruierte
strikte Inklusion erzeugt ein `krawczyk-root`-Leaf. Singulaere oder nicht
einschliessende Boxen werden weiter geteilt; auf Tiefe 20 bleiben sie
`unresolved`. `all-residual-excluded` ist daher nur bei einer vollstaendigen
Residualausschlusspartition moeglich. Ein Root oder ein ungeloestes Leaf
verhindert den Branch-loss-Claim.

Die FIFO wurde nach dem ersten gruenen Stand von einer fortlaufend behaltenen
Liste auf `collections.deque` umgestellt. Damit bleiben abgearbeitete innere
Knoten nicht bis zum Ende im Speicher. Die protokollbedingt moeglichen bis zu
$2^{20}$ Blaetter bleiben dennoch eine reale Laufzeit- und Speicherschranke.

## RED- und Falsifikationshistorie

Revision `1e0ad62` committed sieben Tests vor dem Adaptersymbol; alle sieben
scheiterten ausschliesslich am fehlenden
`local_branch_exclusion_backend_record`. Beim ersten GREEN-Lauf falsifizierte
ein Test seine eigene Teilungsannahme: Fuer die registrierte lokale Box ist
$0.004/0.012$ groesser als $0.04/0.3$, also muss zuerst $\theta$ und nicht
$R$ halbiert werden. Die Erwartung wurde auf die bereits vorregistrierte
Normierungsregel korrigiert, nicht die Regel an den Test angepasst.

Die schliesslich neun gezielten Faelle pruefen:

1. ausschliessliche Nutzung des gemeinsamen Residualauswerters bei direktem
   Ausschluss;
2. Zielhorizont, 120 Dezimalstellen, geschnittene Domain und nativen
   v3-Record;
3. einen strikten Krawczyk-Root trotz eines fuer diese Leafsemantik
   irrelevanten anderen Bibliotheksgates;
4. FIFO-Reihenfolge und die laengere normalisierte Kante;
5. ein einzelnes bis Tiefe 20 verfolgtes ungeloestes Blatt;
6. Rekonstruktion statt Vertrauen in ein widerspruechliches
   Krawczyk-Boolfeld;
7. Ablehnung nicht registrierter Kanten, Float-Horizonte, Listenroots und
   nichtendlicher Dezimalwerte;
8. Akzeptanz eines synthetischen Adapterrecords durch den vollstaendigen
   v3-Ausschlussvalidator;
9. die bereits vorhandenen unabhaengigen Auditor-Counterexamples gegen
   unbewiesene Residualausschluesse, unvollstaendige Partitionen und den
   Widerspruch zu einem zertifizierten Zielroot.

Gebundene Blobs:

- Horizontgate nach FIFO-Kuratierung:
  `c4f519b68001dd6c7c99f228e18210ce25b7b3f8`;
- fokussierte Tests einschliesslich v3-Integration:
  `1cc32e29f55a46b57573cb1808a8a3550511b1c0`.

Die lokale Regression besteht 99 relevante Tests und Ruff. Die offizielle
Linux-CI
[34409772851](https://github.com/MemoryDynamics/Knoten/actions/runs/34409772851)
fuer den FIFO-kuratierten Implementierungsstand bestand 1038 Tests, Lint und
Dokumentationsbau.

## Evidenzgrenze und Stopregel

Die Tests verwenden kontrollierte synthetische Intervallantworten. Keine
registrierte lokale Domain wurde durchsucht; insbesondere liegt weder ein
vollstaendiger Residualausschluss noch ein anderer Root noch ein
Tiefe-20-Fehler fuer eine Zielkante vor. `mpmath.iv` bleibt derselbe getrackte
Intervallbackend und ist kein unabhaengiger zweiter Beweiskern. Intervall-
Overestimation kann den Baum bis Tiefe 20 treiben; dieses Resultat waere
`inconclusive`, kein Branchverlust.

Als naechstes darf targetfrei nur das tail-augmentierte Krawczyk-Zertifikat
implementiert werden. LCG-Arnoldi, Trajektorienabbildung,
Backendkomposition, Readinessreview und ein registrierter Horizontlauf
bleiben geschlossen; P5-D-Versuch 4 ist nicht autorisiert.
