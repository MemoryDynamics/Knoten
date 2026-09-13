# Code-Review: G4-Tailkern vor Komponentenlauf

Datum: 2026-09-13.

Verdict:
**`g4-numerical-core-reviewed-component-runner-required`**.

## 1. Gepruefter Umfang

Geprueft wurden finite Rotating-wave-Balance und analytischer Jacobian, die
Tailbounds, die outward-rounded Tailaugmentation, der generische
zweidimensionale Krawczyk-Operator und der v3-Tailadapter. Es wurde noch kein
$H=3600$-Root oder Tailpanel ausgewertet.

## 2. Algebraaudit

Die endliche Summe verwendet die Alter $j=1,\ldots,H-1$; der ausgelassene
Tail beginnt daher korrekt bei $j=H$. Aus
$\alpha\sum_{j=H}^{\infty}q^j=q^H$ folgen Residual- und Radiusbound. Die
gewichtete Alterssumme ist

$$
\alpha\sum_{j=H}^{\infty}j q^j
=q^H\left(H+\frac q\alpha\right),
$$

und stimmt mit dem Winkelbound ueberein. Die Ableitungen im Code entsprechen
$r_j=2R|\sin(j\theta/2)|$ ausser an den fuer die globale Normabschaetzung
unerheblichen Nullstellen der Betragsfunktion. Die symmetrische
Komponentenbox ist konservativer als der euklidische Ball, aber eine gueltige
Einschliessung.

## 3. Numerik- und Domainaudit

Finite Funktion, Funktion am Mittelpunkt und beide Jacobi-Spalten werden mit
`mpmath.iv` outward-rounded ausgewertet. Die Inverse des endlichen
Punktjacobians dient nur als Praekonditionierer; die eigentliche
Krawczyk-Matrix enthaelt den tail-augmentierten Intervalljacobian. Der Adapter
bindet die gesamte $10^{-10}$-Box an die registrierte Domain und stoppt bei
Singularitaet oder Nichtinklusion.

Die Tailbounds werden als nach oben gerundete binary64-Dezimalstrings
transportiert. Bestehende Tests vergleichen sie gegen die konservativen
Dezimalformeln und den unmittelbar kleineren Float. Die verbleibende Trust
Base ist `mpmath.iv` 1.3.0; eine unabhaengige Intervallimplementierung fehlt.

## 4. Falsifikation

Null-Tail reproduziert das endliche Krawczyk-Bild. Positive Testbounds
erweitern beide Residualkomponenten und jeweils die richtige Jacobi-Spalte.
Negative/nichtendliche Bounds, Nullbreite, falsche Praezision, Rootboxen
ausserhalb der Domain und gemeldete Nichtinklusion schliessen fail-closed.
Die vorhandene v3-Validierung rekonstruiert Boxen, strikten Einschluss und
Panelschnitt aus den gespeicherten Endpunkten.

## 5. Befund

Es wurde kein algebraischer oder numerischer Major/Critical-Fehler im G4-Kern
gefunden. Der Kern ist fuer einen festen, bereits vorregistrierten lokalen
Test geeignet. Nicht ausfuehrungsreif war dagegen die Huelle: Das bisherige
Modul besitzt absichtlich keinen Top-level-Zielstart, keinen isolierten
G4-Ergebnisrecord und kein eigenstaendiges Manifest. Ein manueller
Funktionsaufruf wuerde die etablierte Provenienz- und Publikationsgrenze
unterschreiten.

## 6. Remediation und Grenze

Vor Ausfuehrung ist deshalb der separat preregistrierte G4-Komponentenrunner
mit Standardbibliothek-Auditor, Mutationskontrollen, sauberem Commit und
gruener CI erforderlich. Dieses Review genehmigt keine Parametersuche und
keinen vollstaendigen Horizont- oder P5-D-Lauf.

