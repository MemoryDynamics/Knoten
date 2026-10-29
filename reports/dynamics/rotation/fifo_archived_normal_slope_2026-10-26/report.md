# FIFO-Anker: wachsende Normalmode aus archivierten Koeffizienten

Stand: 2026-10-26. **Ergebnis: `positive-real-normal-mode-certified`.**
Am unveraenderten, rauschfreien H=1200-Kreis besitzt der lineare Normalblock
mindestens einen reellen Formmultiplikator groesser als eins. Das ist ein
rechnergestuetzter Instabilitaetsbeleg auf der Vertrauensbasis der bereits
gespeicherten Root- und Koeffizientenintervalle, keine neue Simulation.

## Befund

Ausgewertet wurde ausschliesslich

$$
S=p_H'(1)=1+\sum_{j=1}^{1199}j c_j.
$$

| Archivdatensatz | Ergebnis fuer S, gerundet zur Anzeige | Obere Intervallgrenze | Laufzeit |
| --- | ---: | --- | ---: |
| 80 dps | -0.3276456990433840337505836 | strikt negativ | 1.531 s |
| 120 dps | -0.3276456990433840337505836 | strikt negativ | 1.516 s |

Beide exakten rationalen Intervalle ueberlappen und liegen vollstaendig
innerhalb `(-0.327646, -0.327645)`. Die Anzeige ist gerundet; entscheidend
sind die gespeicherten Brueche fuer beide Endpunkte. Es wurde nicht der
Mittelpunkt und nicht eine float64-Naeherung fuer die Entscheidung verwendet.
Die zwei Praezisionsstufen sind keine unabhaengigen physikalischen Versuche.

## Warum dies eine wachsende Formmode belegt

Die Translationssymmetrie erzwingt exakt

$$
f(x)=\frac{p_H(x)}{x^{H-1}}
=x-1+\sum_jc_j(1-x^{-j}),\qquad f(1)=0.
$$

Aus $f'(1)=S<0$ folgt $f(x)<0$ unmittelbar rechts von eins.
Weil $f(x)\to+\infty$ fuer $x\to+\infty$, existiert eine Nullstelle
$\lambda>1$. Sie ist keine der normalen Symmetriemoden
$1,e^{\pm i\theta}$ am zertifizierten Kreisroot, sondern eine wachsende
Formmode. Die vollstaendige Herleitung steht im
[Methodenvertrag, Abschnitt 6](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/docs/reference/fifo_normal_stability_contract.md).

Die gespeicherten Polynomkoeffizienten lauten ab Index 2 `-c_j`. Der
Archiv-Runner kehrt deshalb beim Einlesen das Vorzeichen und die
Intervallgrenzen um und summiert dann mit den Altersgewichten `j`.
Binaere Endpunkte werden als exakte Brueche gelesen. Die neue Summe
erzeugt keine weitere Rundungsunsicherheit. Das ersetzt keine unabhaengige
Pruefung der urspruenglichen `mpmath.iv`-Einschliessungen.

## Bedeutung und Grenzen

- **Belegt:** lokale lineare Instabilitaet dieses vorbereiteten Kreises
  gegen eine echte Auslenkungs-Formmode ausserhalb der Kreisebene.
- **Damit ausgeschlossen:** die Interpretation genau dieses Kreises als
  linear stabiler 3D-Baustein unter der unveraenderten Regel. Eine rein
  rueckstellende Beschreibung aller Formmoden um diesen Kreis ist nicht gerechtfertigt.
- **Nicht bestimmt:** genauer Multiplikator, Wachstumsrate, Zahl weiterer
  instabiler Moden, spaeterer nichtlinearer Zustand, Rauschlebensdauer oder
  Stabilitaet anderer Kreise und nichtkreisfoermiger FIFO-Strukturen.
- **Nicht abgeleitet:** Teilcheneigenschaften, Quantisierung, Gravitation
  oder eine Identifikation mit der schwachen Wechselwirkung.

Der fruehere Intervall-Schur-Test bleibt unveraendert `inconclusive`.
Seine Polynomdivision war zu weit eingeschlossen. Der neue hinreichende
Beleg benoetigt diese Division nicht und widerspricht dem alten
Nicht-Ergebnis daher nicht. Das beobachtete endliche Wachstum war fuer
sich allein kein Spektralbeweis; der vorliegende Befund schliesst nun die
Luecke zur Existenz einer echten wachsenden Mode, ohne den genauen Verlauf
der frueheren Stoerungsarme zu erklaeren.

## Provenienz und Ausfuehrung

- Kandidat: `k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1`.
- [Vorab festgelegter Vertrag](https://github.com/MemoryDynamics/Knoten/blob/a155b7b5daad3c31f2c4c8b84bdf6699a946f70b/reports/project/meta/preregistration/fifo_archived_normal_slope_2026-10-26.md).
- Ausfuehrungsrevision: `a155b7b5daad3c31f2c4c8b84bdf6699a946f70b`, sauberer Worktree.
- Quelldatenrevision: `fdbd24fd437187a4db185d413f4c3bd022104b3b`,
  urspruengliche Ausfuehrung `16f60f5a12281628a55eb5e591fe027418d21a3a`.
- Ein Aufruf pro Datensatz, 80 vor 120 dps; beide unter 30 Sekunden.
  Keine neuen Trajektorien, Root- oder Kernelrechnungen, Suche oder Wiederholung.
- Vorab: 198 lokale synthetische/Regressions-/Dokumentationstests,
  Quelltext-Lint und strikter Dokumentationsbau bestanden.

Die Freigabe ist damit verbraucht. Die rohe
[Zusammenfassung mit exakten Bruechen und Quellhashes](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_archived_normal_slope_2026-10-26/summary.json)
und das
[Ausfuehrungsreceipt](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_archived_normal_slope_2026-10-26/receipt.json)
sind unveraenderte Runnerausgaben. Nachtraegliche Evidenztests lesen nur
diese Ergebnisse und starten keine erneute Koeffizientenauswertung.

Abschliessende lokale Verifikation: 304 betroffene Tests bestanden,
einschliesslich der reinen Ergebnis-Lesepruefungen; Quelltext-Lint und
strikter Dokumentationsbau ebenfalls bestanden. Dies ist keine Aussage
ueber den Abschluss der nach dem Push gestarteten GitHub-CI.
