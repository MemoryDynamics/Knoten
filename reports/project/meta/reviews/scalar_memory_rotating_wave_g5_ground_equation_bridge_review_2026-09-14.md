# Review: G5 direkt aus den Grundgleichungen

Datum: 2026-09-14.

Verdict:
**`g5-ground-equation-bridge-target-free-pass-component-unmeasured`**.

## 1. Ergebnis

G5 braucht keinen zusaetzlichen harmonischen Oszillator. Die vorhandene
Voll-FIFO-Map ist genau die deterministische Grundgleichung mit
$\varepsilon=0$. Der mitrotierende Rahmen multipliziert nach jedem nativen
Update alle Koordinaten mit $R_{-\theta}$; er veraendert die Dynamik nicht,
sondern macht den Kreis zu einem Fixpunkt.

Die Arnoldi-Rechnung verwendet den analytischen Jacobian dieser Map und ist
damit lokal linearisiert. Die radialen, tangentialen und vollhistorischen
Fortsetzungen iterieren dagegen die nichtlineare Grundgleichung selbst. Ein
G5-Befund darf deshalb nur aus der Uebereinstimmung beider Ebenen entstehen.

## 2. Implementierter Preflight

Der neue Standardbibliotheksrand erzeugt vor dem Eigensolver einen
persistierbaren Record. Er bindet die Papersprache $q$, $H$, $M_0$, $\eta$
und das Depositionsgewicht $\alpha M_0$ an die Codeparameter, prueft die
geometrische Gewichtssumme, native Kreiskovarianz, mitrotierenden Fixpunkt,
Jacobianform/-sparsitaet und analytische Symmetrieresiduen. Historie,
Jacobian und der kanonische JSON-Record erhalten getrennte SHA-256-Bindungen.

Der Horizontadapter verwendet diesen gemeinsamen Preflight nun auch fuer
seinen Arnoldi-Zustand. Der wissenschaftliche H=2400-Kandidat wurde dabei
nicht konstruiert oder ausgewertet; die Tests verwenden injizierte kleine
Zustaende und Mutationen.

## 3. Kritische Grenzen

Der Preflight ist persistierbar, aber noch nicht Bestandteil eines
eingefrorenen Ergebnisvertrags. Deshalb ist G5 weiterhin nicht zielbereit.
Die Historien- und Jacobianhashes sind wegen binary64-`sin`/`cos` nur auf
derselben Plattform reproduzierbar. Der LCG-Start bleibt dagegen portabel.

Ein kleiner Fixpunktfehler beweist weder Stabilitaet noch die Identitaet des
gesamten Horizontasts. Arnoldi ist keine Spektraleinschliessung, und der
Standardbibliothek-Auditor kann die gespeicherten Ritzresiduen nicht ohne
eigenen sparse Numerikbackend neu berechnen.

Native Kreiskovarianz und mitrotierender Fixpunkt sind zwei Darstellungen
desselben Ein-Schritt-Sachverhalts, keine unabhaengigen Replikationen. Der
Preflight wertet beide aus, um Vorzeichen- oder Rotationsrahmenfehler sichtbar
zu machen; er darf sie nicht als zwei statistisch unabhaengige Belege zaehlen.

## 4. Methodische Entscheidung

Vor dem vollstaendigen Horizontlauf wird ein isolierter G5-Komponentenpfad
vorbereitet. Er bestimmt und zertifiziert zuerst den festen H=2400-Root,
persistiert den Grundgleichungs-Preflight und fuehrt erst danach die zwei
Spektralpanels sowie vier direkten nichtlinearen Arme aus. Das zugehoerige
prospektive Protokoll friert Parameter, Schwellen, Entscheidungen und
Stopregeln outcome-blind ein.

Der naechste erlaubte Block ist dessen targetfreier Ergebnisvertrag,
Backendkomposition und unabhaengiger Auditor. Ein Zielzugriff ist nicht
autorisiert.

## 5. Lokale Verifikation

Vierzehn isolierte Modultests decken Positivzeuge, kanonischen Recordhash,
ungueltige Schwellen sowie Mutationen von Gewichtssumme, nativer
Kreisidentitaet, Fixpunkt, Jacobianstruktur und Symmetrien ab. Der gemeinsame
Grundgleichungs-/Jacobian-/G5-/Auditorblock besteht 128 Tests; die gesamte
Repositorysuite besteht 1093 Tests. Exakter CI-Lintumfang,
Informationsarchitektur und strikter Dokumentationsbau sind lokal gruen.

Diese Tests injizieren kleine Zustaende. Weder der H=2400-Root noch dessen
Jacobian, Spektrum oder Stoerungstrajektorien wurden ausgewertet.
