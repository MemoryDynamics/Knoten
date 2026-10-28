# Materie: Referenztheorie und Emergenz

Stand: 2026-10-28. Autorenentscheidung: **Referenztheorie und
Emergenznachweis strikt getrennt fuehren.** Bekannte QCD-/QFT-Gleichungen
und Teilchenparameter duerfen auf der Referenzseite vorausgesetzt werden.
Dadurch sind sie nicht im Memory-Modell hergeleitet. Das gehoert zum
Paper-III-Programm und erweitert keine Claims von Paper I.

## Gemeinsames Ziel, unterschiedliche Beweislast

| Referenzzweig | Memory-/Emergenzzweig |
| --- | --- |
| Quantenraum, Symmetrien, Kopplungen und Kalibrierungswerte ausdruecklich als Inputs deklarieren. | Dieselben Eigenschaften aus einer benannten Mikrodynamik und Beobachtungsabbildung herleiten oder als offene Luecke belassen. |
| Numerik an bekannten Identitaeten und unabhaengigen Vergleichsobservablen pruefen. | Eingesetzte Labels, Spinoren oder Potentiale nicht als emergierte Eigenschaften zaehlen. |
| Vollstaendige QCD, effektive Quarkmodelle und reine Zustandsalgebra getrennt bezeichnen. | Ein Dreiercluster ist noch kein Proton, eine FIFO-Schleife noch kein Elektron. |
| Identische Definitionen fuer Masse, Ladung, Spin, Formfaktoren und atomare Antwort verwenden. | Die Verbindung dieser Observablen muss aus demselben Kandidaten folgen, nicht aus separaten Nachfits. |

Die [Wasserstoff-Anforderungen](hydrogen_benchmark.md) bleiben gemeinsam.
Ein effektiver Protontraeger ist als atomarer Zwischenvergleich erlaubt,
ersetzt aber nicht mehr die ausdruecklich gewuenschte Untersuchung seiner
inneren Quarkstruktur. Innere Farbe/Flavor und aeussere Raumdimension sind
verschiedene Begriffe; drei Farben bedeuten keine drei Raumachsen.

## Proton und Elektron nicht gleich konstruieren

Der Valenzvergleich ist $p:uud$, $n:udd$, mit Quarkladungen
$q_u=2e/3$, $q_d=-e/3$. QCD umfasst darueber hinaus Gluon- und
Seequarkfreiheitsgrade. Ein Farbsingulett ist nicht bereits ein dynamischer
Confinement-Nachweis. Das einfache symmetrische Quarkmodell verwendet fuer
einen raeumlichen S-Zustand antisymmetrische Farbe und symmetrische
Spin-/Flavoranteile. Diese Modellannahmen sind nicht mit vollstaendiger
QCD gleichzusetzen:
[PDG 2025, Quark Model, Abschnitte 15.1, 15.5 und 15.6](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-quark-model.pdf).

Auch Constituent-Quarkmassen sind nicht die laufenden Massenparameter der
QCD-Lagrangefunktion; letztere brauchen Renormierungsschema und Skala.
Ein nach der Protonmasse eingestellter Constituent-Parameter sagt diese
Protonmasse nicht voraus:
[PDG 2025, Quark Masses, Abschnitte 60.1 und 60.2](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-quark-masses.pdf).

Auf der QFT-Referenzseite entsteht der Elektronbegriff aus dem quantisierten
Dirac-Materiefeld samt fermionischer Algebra. Ein extern vorgegebenes Feld
und das Elektronenfeld sind zu unterscheiden:
[Tong, Quantizing the Dirac Field, Abschnitt 5.2](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S5.html).
Die Hypothese des Autors lautet auf der Emergenzseite: Feld-/Memory-
Rueckwirkung koennte einen geeigneten Leptonzustand stabilisieren, eventuell
unter Beteiligung von FIFO. Nachzuweisen waeren sowohl der freie Zustand
als auch seine Antwort auf externe Felder. Die bisherigen FIFO-Befunde
liefern weder diese Quantisierung noch die Elektronenidentitaet.

## Ausgefuehrte Referenzkontrolle

Der neue
[Referenzrechner](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/experiments/current/reference/nucleon_spin_flavor_reference.py)
loest ein **endliches Zustandsalgebra-Problem**, keine raeumliche
Quarksimulation. Er verwendet NumPy fuer hermitesche Diagonalisierung;
die Rotationstests verwenden SciPy-Matrixexponentiation.

Die Einquarkbasis ist $(u\uparrow,u\downarrow,d\uparrow,d\downarrow)$.
Der dreifache Spin-/Flavorraum hat Dimension $4^3=64$. Im Sektor
$uud$, $S_z=\hbar/2$ spannen die normierten Symmetrisierungen von
$u\uparrow u\uparrow d\downarrow$ und
$u\uparrow u\downarrow d\uparrow$ einen zweidimensionalen Unterraum
auf. Der Rechner diagonalisiert dort $S^2$, statt das Gesamtergebnis
einfach als Zahl einzutragen. Fuer das Neutron werden $u,d$ vertauscht.

Beide Sektoren enthalten $S^2/\hbar^2=3/4$ **und** $15/4$.
Der Spin-$1/2$-Sektor wird als Referenz ausgewaehlt, nicht als energetischer
Grundzustand vorhergesagt. Der Spin-$3/2$-Gegencheck verhindert, dass
Quarkinhalt mit Teilchenidentifikation verwechselt wird.

Im separaten $3^3=27$-dimensionalen Farbraum wird der normierte
antisymmetrische Zustand $\epsilon_{abc}|abc\rangle/\sqrt6$ gegen alle
acht Gesamtgeneratoren geprueft. Ein unverschraenktes $|rgb\rangle$ dient
als negative Kontrolle: Drei verschiedene Farbetiketten sind fuer sich
noch kein Singulett. Spin-/Flavorsymmetrie, Farbasymmetrie und angenommene
symmetrische Raumwellenfunktion ergeben die eingesetzte Fermionsymmetrie;
sie sind kein aus klassischen Knoten entstandener Statistiknachweis.
Geprueft werden gemeinsame Farbrotationen, keine raumabhaengige
Eichfelddynamik oder deren Transport zwischen getrennten Quarkorten.

### Resultate und Nichtresultate

Die [archivierte Auswertung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/nucleon_spin_flavor_2026-10-28.json)
enthaelt Inputs, ausgelassene Physik und den Skript-Hash. Es bestehen acht
algebraische Checks und zwoelf
[Softwaretests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_nucleon_spin_flavor_reference.py).
Mit den bestehenden Paar- und Dokumentationsregressionen bestehen
insgesamt 96 Tests, ausserdem Lint und strikter Dokumentationsbau.

| Auswertung | Ergebnis | Interpretation |
| --- | --- | --- |
| Gesamtladung | $Q_p/e=1$, $Q_n/e=0$ | Addition vorausgesetzter Quarkladungen |
| Ausgewaehlter Spin | $S^2/\hbar^2=3/4$, $S_z/\hbar=1/2$ | Diagonalisierung und Sektorwahl, keine dynamische Selektion |
| Farbe | Alle acht Gesamtgeneratoren annihilieren den Singulettzustand | Farb-Algebra, kein Nachweis von Bindung oder Confinement |
| Negative Farbkontrolle | Maximale Generatornorm auf $|rgb\rangle$: $1/\sqrt2$ | Die Farbetiketten allein bestehen den Test nicht |
| Magnetische Spin-Gewichte | Proton $(4/3,-1/3)$, Neutron $(-1/3,4/3)$ fuer $(u,d)$ | Erwartungswerte desselben Spin-/Flavorzustands |
| Magnetisches Verhaeltnis | $\mu_n/\mu_p=-2/3$ bei gleichen Constituent-Massen und additiven Dirac-Momenten | Modellvorhersage ohne Fit des Vergleichswertes |

Die letzte Vorhersage stimmt mit den bekannten Quarkmodellformeln ueberein.
Vom in PDG 2025 zitierten Messvergleich $-0.6849793$ weicht der Modellwert
um etwa **2.67 Prozent relativ** ab. Das ist keine experimentelle Bestaetigung
dieses einfachen Modells. Die Abweichung bleibt ohne Nachfit stehen:
[PDG, Gleichungen (15.38)--(15.39)](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-quark-model.pdf).

**Nicht berechnet:** raeumliche Bindung, Confinement, Masse oder Radius
des Nukleons, Gluon-/Seequarkdynamik, schwacher Zerfall, Elektronenfeld,
Wasserstoffspektrum und irgendeine Emergenz aus Memory. Insbesondere ist
das Ergebnis kein Gitter-QCD-Lauf. Das Rechnen mit $udd$ erzeugt noch
keinen Prozess $n\to p+e^-+\bar\nu_e$.

Reproduktion des algebraischen Checks in eine neue Ausgabedatei:

```powershell
python experiments/current/reference/nucleon_spin_flavor_reference.py --output <neue-ausgabe.json>
python -m pytest tests/test_nucleon_spin_flavor_reference.py -q
```

Die Ausgabedatei wird nicht ueberschrieben. Keine Seeds, Zeitschritte,
Parametersuche oder Klassifikation eines Memory-Zielzustands sind Teil
dieses Rechners.

## Vertrag fuer die eigentliche Simulation

Die naechste **raeumlich-dynamische** Referenz braucht einen festgelegten
Hamiltonoperator bzw. eine Wirkung, Freiheitsgrade, Naeherung, Kalibrierung
und Konvergenzkontrollen. Bei einem Constituent-Modell sind insbesondere
Confinementpotential und effektive Quarkmassen Inputs; bei Gitter-QCD
kommen unter anderem Volumen-, Gitterabstands- und Ensemblekontrollen
hinzu. Diese Entscheidungen sind durch die bisherige Matrixrechnung
nicht erledigt. Es wurde noch keine solche Simulation gestartet.

Die Referenz soll Quarkstruktur ueber aeussere Nukleonobservablen an
denselben atomaren Benchmark anschliessen. Eine separat passend gemachte
Quarkanimation waere dafuer kein Ersatz. Auf der Memory-Seite bleiben die
[Paar-Grenzen](hydrogen_pair_audit.md) und die offene Kraft-/Arbeitsdeutung
bestehen. Neue Referenzphysik darf diese Luecken nicht unbemerkt verdecken.

Die neue Autorenentscheidung erlaubt den getrennten Referenzzweig, keine
Umdeklaration seiner Resultate zu Memory-Emergenz. Teure numerische Laeufe
benoetigen weiterhin einen geprueften begrenzten Ausfuehrungsvertrag;
verbrauchte FIFO-/P5-Genehmigungen bleiben geschlossen. Die einzige
Arbeitsreihenfolge steht in den
[Projektprioritaeten](../status/project_priorities.md).
