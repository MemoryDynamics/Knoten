# G5-Komponentenlauf: Execution-Incident

Datum: 2026-09-16.

Verdikt: **Attempt 1 verbraucht; kein G5-Ergebnis; Retry nicht autorisiert**.

## Ablauf

Der autorisierte Einmalversuch lief auf Commit
`0e6250338397f5f9940b58f5413d11b0d4423ff9`. Die atomare Receipt wurde am
2026-09-15 um 21:01:44 UTC erzeugt. Finite-Root- und
Grundgleichungs-Preflight oeffneten den Arnoldi-Schritt; beide registrierten
Panels wurden aufgerufen. Vor jeder Publikation brach die abschliessende
Recordvalidierung ab:

```text
ValueError: $.arnoldi.primary: overlap outside [0,1]
```

Ergebnis-JSON, Lesereport und Manifest existieren nicht. Die in-memory
Arnoldiwerte wurden vom eingefrorenen Pfad nicht persistiert und duerfen nicht
rekonstruiert oder durch einen unangemeldeten Wiederholungslauf ersetzt
werden.

## Kritische Einordnung

Translations- und Rotationsoverlap sind normierte Projektionen und daher
mathematisch auf $[0,1]$ beschraenkt. Der Runner speichert die direkte
binary64-Auswertung, waehrend der Vertrag die exakte Grenze ohne
Rundungstoleranz verlangt. Ein targetfreier Test der analytischen
$H=2400$-Basis ergab eine Gram-Abweichung von `7.77e-16`; damit ist ein
wenige-ulp-Ueberschwingen technisch plausibel. Der konkrete verworfene Wert
wurde jedoch nicht persistiert. Die Rundungsursache ist daher eine stark
gestuetzte Diagnose, kein aus dem Zielrecord rekonstruierter Messwert.

Der Vorfall falsifiziert die targetfreie Abdeckung der numerischen
Recordgrenze. Er entscheidet weder Stabilitaet noch Instabilitaet. Eine
Remediation muesste Overlaps vor Serialisierung mathematisch auf $[0,1]$
kanonisieren und durch Grenztests absichern. Jeder Retry benoetigt ein eigenes
prospektives Amendement, neues Review, neue Governance und ausdrueckliche
Autorisierung.
