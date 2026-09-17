# G5 Attempt 3: kritisches Ergebnisreview

Stand: 2026-09-17.

Verdict: **`g5-attempt-3-result-reviewed-local-direct-stability-pass`**

Der vorregistrierte Attempt 3 wurde genau einmal auf Execution-Commit
`9007564d4420e357fbef733fe05c7b58d8d1a81d` ausgefuehrt. Receipt, Ergebnis,
Lesereport und zuletzt geschriebenes Manifest liegen vor. Der getrennte
Standardbibliothek-Auditor akzeptierte Payload und Publikation waehrend des
Laufs und in einer anschliessenden rein lesenden Wiederholung.

## 1. Evidenz

- Der 120-dps-Newtonlauf konvergiert in acht Schritten zu
  \(R=0.946516919482980\ldots\) und
  \(\theta=0.0157704507232456\ldots\). Innere und aeussere
  `mpmath.iv`-Krawczykbox schliessen strikt ein.
- Der direkte Grundgleichungs-Preflight besteht. Der FIFO-Jacobian besitzt
  Form \(4800\times4800\) und 19196 gespeicherte Eintraege. Gewichtssummen-,
  Kreis-, Fixpunkt- und Symmetriefehler liegen innerhalb der registrierten
  Grenzen.
- Beide Arnoldi-Panels sind vollstaendig. Das fuehrende gematchte
  transversale Paar hat Betrag `0.9930442043708534` im Primaerpanel und
  `0.9930442042250666` im Konvergenzpanel, jeweils klar unter der
  Stabilitaetsgrenze `0.9999`. Ihr Abstand ist
  `1.6755588669714317e-10` gegen die Grenze `1e-5`.
- Die groessten normalisierten Ritzresiduen betragen im Primaerpanel
  `6.019194433653485e-11` und im Konvergenzpanel
  `1.889035586918184e-12`, jeweils unter `1e-8`.
- Alle drei nichtlinearen Stoerungsarme laufen 5000 Schritte ohne Stop. Die
  groesste transiente Verstaerkung ist `1.0026125744010914` gegen die Grenze
  `10`; der groesste Endquotient ist `1.3822191392182151e-6` gegen `0.1`.
- Die ungestoerte Kontrolle bleibt mit maximal
  `6.7353968168882186e-15` unter `1e-10`. Das zwischen Samples liegende
  Vollschrittmaximum wird aus der dichten Spur exakt rekonstruiert.

Damit werden alle vorregistrierten Gates erfuellt und die Recordentscheidung
`g5-local-direct-stability-pass` ist korrekt rekonstruiert.

## 2. Inferenz

Belastbar ist starke numerische Evidenz fuer lokale direkte Stabilitaet des
vorbereiteten, translations- und rotationsquotientierten FIFO-Orbits bei
exakt

\[
\alpha=0.01,\quad q=0.99,\quad H=2400,\quad \eta=0.15,
\quad \varepsilon=0.
\]

Die nahe Eins liegenden Translations- und Rotationsmoden sind die erwarteten
Symmetriemoden; der transversale Abstand zur Einheitskreisgrenze ist nicht nur
ein Rundungseffekt. Spektrum und direkte nichtlineare Stoerungen stuetzen
denselben lokalen Befund.

## 3. Nicht belegt

Der Arnoldilauf ist ein numerischer Largest-modulus-Ausschnitt, keine
Intervallschranke fuer das volle 4800-dimensionale Spektrum. Der Auditor
rekonstruiert Recordrelationen und Entscheidung, fuehrt aber keinen zweiten
Sparse-Eigenloeser aus. Drei vorbereitete Stoerungsrichtungen und 5000
Schritte beweisen weder einen offenen Basin-Ball noch globale oder
asymptotische Stabilitaet.

Insbesondere folgen daraus weder die Verbindung des isolierten
\(F_\infty\)-Roots ueber G1--G3, noch Stabilitaet fuer \(H\to\infty\),
Formation, Interaktion zwischen Schleifen, internes \(S^1\), Spin, Traegheit
oder physikalische Masse. Diese Aussagen bleiben Hypothesen beziehungsweise
separate Gates.

## 4. Provenienz

- Implementationsrevision: `059ff8e18630bfe1c64e533f17832a8bb3b25b3c`
- offizielle Implementations-CI:
  [35166339027](https://github.com/MemoryDynamics/Knoten/actions/runs/35166339027)
- Authorization UUID: `0277d0ba-3d81-4bda-84a1-e41adf441596`
- Receipt SHA-256:
  `c681904f9fc9e7766410493d59693d6124265ae425c8b13ff0a4d52da95039a4`
- Ergebnis SHA-256:
  `3321ee6392a6eb2a3c5098fa437cb41bb57b9da7e1c0ada521bdd1e894f4ec39`
- Lesereport SHA-256:
  `1fa82e7c9dd27080566bd3c29c40e08299bd088bba651646d8567292547418ab`
- Publikationsmanifest SHA-256:
  `62ed914737028678be360633f4c97b8cb28cd0ef9fae6e7077684fa272a9df8e`

Attempt 3 ist verbraucht. Es ist kein Retry und kein Attempt 4 autorisiert.
