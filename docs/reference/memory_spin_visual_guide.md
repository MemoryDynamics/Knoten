# Memory-Struktur und Spin: zwei getrennte Bilder

Stand: 2026-11-19. Leserabbildungen, keine neue Simulation und keine
freigegebenen Paperfiguren. Die erste zeigt unsere analytische Konstruktion;
die zweite zeigt den quantenmechanischen Zielmassstab, **nicht** ein bereits
erreichtes Memory-Ergebnis.

## 1. Welche Struktur haben wir tatsaechlich?

![Nichtplanarer Memory-Vierzyklus mit vier Speicherorten, aktueller Position und einer innenliegenden Feldnullstelle; darunter vier Draufsichten mit farbcodierter Hoehe.](https://raw.githubusercontent.com/MemoryDynamics/Knoten/codex/paper-i-finalization/figures/draft/memory_charge_2026-11-19/memory_structure.png)

**Eine Bahn, vier Erinnerungen.** Die Punkte sind vier aufeinanderfolgende
Speicherorte desselben bewegten Objekts, nicht vier Teilchen. Der schwarze
Ring bezeichnet seinen aktuellen Ort. Die gerichteten Kanten geben die
zeitliche Reihenfolge an; die geraden Verbindungen sind nur eine Zeichenhilfe,
keine berechnete kontinuierliche Flugbahn. Nach vier diskreten Schritten
wiederholt sich die konfigurierte Historie.

**Eine raeumliche, aber noch keine verknotete Struktur.** Zwei Orte liegen
oberhalb, zwei unterhalb der Mittelebene. Rot und Blau erhalten diese Hoehe
auch in den vier Draufsichten. Die blasse Huelle umschliesst die vier Orte;
sie ist weder eine materielle Oberflaeche noch ein zusaetzliches Feld.
Ein topologisch nichttrivialer Bahnknoten ist hier nicht nachgewiesen.

**Ein Feldmerkmal im Inneren.** An der violetten Raute heben sich die
gewichteten gespeicherten Richtungen im nativen Vektorreadout auf. Rund um
diese regulaere Nullstelle besitzt das Richtungsfeld den lokalen Index +1.
Dieser Index ist eine topologische Orientierungszahl, nicht die Ladung +e.
Die Nullstelle bewegt sich mit der exakten Historie; ihre kleine Bewegung
wird in den Draufsichten nicht kuenstlich vergroessert.

Die inverse Konstruktion liefert eine exakte Vierperiode bei den analytisch
zugehoerigen Kopplungen. Ob kleine Stoerungen abklingen, ist weiterhin offen.
Das Bild ist deshalb **kein Stabilitaetsnachweis**. Auch die drei
Raumdimensionen sind hier Modellinput, nicht emergiert.
Grundlage: [Existenzkonstruktion, Abschnitte 1 und 3-5](https://github.com/MemoryDynamics/Knoten/blob/4a43713/reports/reference/flat_memory_cycle_2026-11-16.md).

## 2. Warum Spin 1/2 keine vierte Raumdimension braucht

![Spinor-Referenz fuer Drehungen von null bis 720 Grad: raeumliche Spinrichtung, getrennte komplexe Phasen und unterschiedliche Perioden von Spinmessung und Referenzarm-Interferenz.](https://raw.githubusercontent.com/MemoryDynamics/Knoten/codex/paper-i-finalization/figures/draft/memory_charge_2026-11-19/spinor_reference.png)

Ein Spinor hat zwei komplexe Amplituden a und b, also vier reelle
Komponenten. Das sind **Zustandskomponenten, keine Raumrichtungen**.
Normierung und die fuer einen isolierten Zustand unbeobachtbare gemeinsame
Phase reduzieren diese Beschreibung auf die zwei Winkel der Bloch-Kugel.
Die Kugel beschreibt Spinorientierungen, nicht die Oberflaeche eines Teilchens.
Eine vierte raeumliche Achse ist dafuer nicht erforderlich.

In der obersten Bildzeile wird eine Spinrichtung um die z-Achse gedreht;
gezeigt ist ihre xy-Projektion. Die roten und blauen Zeiger darunter leben
dagegen jeweils in einer komplexen Zahlenebene. Nach 360 Grad ist die
Spinrichtung wieder gleich, aber beide Amplituden haben das Vorzeichen
gewechselt. Erst nach 720 Grad kehrt auch dieser Spinorrepraesentant zurueck.
Mathematisch beschreibt das die doppelte Ueberlagerung der 3D-Rotationen
SO(3) durch SU(2). Das ist bekannte Quantenmechanik, keine neue
Memory-Herleitung. [MIT-Kursnotizen, Abschnitte 4.1 und 4.2.4-4.2.5](https://live.ocw.mit.edu/courses/22-51-quantum-theory-of-radiation-interactions-fall-2012/fb8b6e60579e7a4e1584e44e597c7c05_MIT22_51F12_Ch4.pdf).

**Das Minus ist nicht allein messbar.** Die gestrichelte Kurve zeigt eine
Spinmessung am gedrehten Zustand. Die violette Kurve gehoert zu einem
anderen Aufbau: Zwei kohaerente Wegarme werden wieder vereinigt, und nur
in einem Arm wird der Spin gedreht. Dann wird aus dem gemeinsamen Minus
der Spinamplituden eine relative Phase zwischen den Armen. Es aendert das
Interferenzsignal, obwohl eine isolierte Spinmessung unveraendert ist.

### Rechenbasis der dargestellten Referenz

Wir setzen den bekannten Spin-1/2-Rotationsoperator voraus und waehlen
einen anfangs entlang +x polarisierten Zustand. Fuer einen Winkel theta
in Radiant ist

$$
\psi(\theta)=\frac{1}{\sqrt{2}}
\begin{pmatrix}e^{-i\theta/2}\\e^{+i\theta/2}\end{pmatrix},
\qquad
\frac{2\langle\mathbf S\rangle}{\hbar}
=(\cos\theta,\sin\theta,0).
$$

Die Zeiger zeigen nur die Phasen; beide Amplitudenbetraege sind konstant
1/sqrt(2). Die beiden Kurven folgen durch direkte Projektion bzw.
Ueberlagerung der Arme:

$$
P_{+x}=\frac{1+\cos\theta}{2},\qquad
P_{\mathrm{out}}=
\frac{\|\psi(0)+\psi(\theta)\|^2}{4}
=\frac{1+\cos(\theta/2)}{2}.
$$

Die zweite Formel gilt fuer ideal balancierte kohaerente Arme, keinen
zusaetzlichen Wegphasenunterschied und einen spinunabhaengigen Detektor
am ausgewaehlten Ausgang. Sie ist hier eine analytische Referenzkurve,
keine Messung oder Simulation unseres Modells.

## 3. Was zwischen beiden Bildern noch fehlt

Der Vierzyklus aus Bild 1 ist **kein Spinor**. Vier Schritte, wechselnde
Hoehen oder eine Rueckkehr erst nach mehreren Schritten erzeugen fuer
sich genommen keinen halbzahligen Spin. Seine Ein-Schritt-Symmetrie
enthaelt sogar eine Spiegelung; sie ist keine reine Raumrotation.

Aus Memory muessten erst geeignete interne Zustaende und ihre
Transformation unter beliebigen Raumrotationen hergeleitet werden.
Ein Spin-1/2-Claim muesste dann auch die Observablen und eine physikalisch
definierte relative Phasenmessung tragen. Ein einzelnes 720-Grad-Muster
waere dafuer nicht genug. Ein Bindungs-, Ladungs- oder Elektronenclaim
wird durch diese Abbildungen nicht hinzugefuegt.

## Dateien und Reproduktion

Fortsetzung: [FIFO in 4D und die 720-Grad-Wiederkehr](fifo_4d_spin_projection.md)
zeigt dieselbe Spinorkinematik rein reell mit einer ganzen vierplaetzigen
Historie und grenzt sie von einer nativen raeumlichen 4D-Einbettung ab.

- Struktur: [PNG](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/figures/draft/memory_charge_2026-11-19/memory_structure.png), [SVG](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/figures/draft/memory_charge_2026-11-19/memory_structure.svg), [PDF](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/figures/draft/memory_charge_2026-11-19/memory_structure.pdf).
- Spinreferenz: [PNG](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/figures/draft/memory_charge_2026-11-19/spinor_reference.png), [SVG](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/figures/draft/memory_charge_2026-11-19/spinor_reference.svg), [PDF](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/figures/draft/memory_charge_2026-11-19/spinor_reference.pdf).
- [Erzeugendes Skript](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/experiments/current/reference/memory_spin_illustrations.py), [Kontrollen](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_memory_spin_illustrations.py), [Provenienz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/figures/draft/memory_charge_2026-11-19/provenance.json).

```bash
python -m experiments.current.reference.memory_spin_illustrations
pytest -q tests/test_memory_spin_illustrations.py
```

Plotgeometrie: f=1/2, g=2/3, q=99/100, sigma=1. Kein Kraftlauf,
keine Eigenwertauswertung, keine Parametersuche. Die Kontrollen pruefen
die gezeichneten Nullstellen, Innenlage, Phasenabbildung und Spinformeln;
sie ersetzen weder den Existenzbeweis noch eine Stabilitaetspruefung.

Validiert: 13 neue Abbildungskontrollen sowie die vorhandenen festen
Vierzyklus- und Markdown-Kontrollen, insgesamt 36 bestandene Tests;
Lint im konfigurierten Bereich und strikter Dokumentationsbau. PNGs
und die erneut gerenderten PDF-Seiten wurden visuell geprueft.
Keine vollstaendige Repository-Testsuite.
