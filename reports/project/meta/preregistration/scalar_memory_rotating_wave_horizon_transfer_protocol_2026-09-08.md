# Protokoll: Horizonttransfer der skalaren Rotating Wave

Datum: 2026-09-08.

Status: **prospektiv zum dritten Mal amendiert nach negativem
Evidenzvertragsreview, vor wissenschaftlichem Runnercode und vor jeder neuen
Horizont-Trajektorie; P5-D-Target geschlossen**.

Die Amendierung schliesst HT-P01--HT-P06 aus dem separat committed Review an
Revision `c1ee529d969ebafed7a557e3db47eba95a38af17`, Reviewblob
`11b3f86320d976cb9d77f50d79cc69c5c48cd971`. Die zugehoerige CI muss vor
einem Suffizienzreview erfolgreich abgeschlossen sein. Kein numerischer
Root, keine Horizonttrajektorie und kein P5-D-Target wurde fuer die
Amendierung ausgewertet.

Die zweite Amendierung schliesst ausschliesslich die Null- und
Abbruchsemantik aus dem spaeteren Negativreview an Revision
`adb5c2445a63265b96c28eee1c1cfd98a1f7017c`, Reviewblob
`dfafe31604d24d36ce0fa8eecf7d2ceaa3902bb7`. Sie aendert keine Gleichung,
keinen Parameter, keine numerische Schwelle, keine Gatepraezedenz und keinen
registrierten Pfad. Auch fuer diese Amendierung wurde kein numerischer Root,
keine Homotopie, kein Arnoldi-Panel und keine Horizonttrajektorie
ausgewertet.

Die dritte Amendierung schliesst die Nachweisvollstaendigkeit aus Revision
`ef7707514468754837ef6a5c5648b73024be82b0`, Reviewblob
`6963de5eef5906fd9db45754110ecf3a18d25395`. Sie fuegt keine numerische
Methode, Schwelle oder Suchfreiheit hinzu, sondern verlangt, dass bereits
registrierte aeussere/innere Zertifikate, Ausschlusswitnesses, Startvektoren
und Stoerungen im Ergebnis nachpruefbar gespeichert werden. Auch fuer diese
Amendierung wurde kein registrierter numerischer Wert ausgewertet.

Dieses Protokoll operationalisiert den Befund
`finite-h-loop-nontautological-horizon-transfer-open`. Es darf erst nach
einem separat committed und gruen getesteten Suffizienzreview implementiert
werden. Es autorisiert weder P5-D-Versuch 4 noch eine Wechselwirkungs-,
Oszillator-, Traegheits- oder Masseaussage.

## 1. Frage und Abgrenzung

Geprueft wird, ob der bereits zertifizierte deterministische Anchor-Root bei
festem Vergessen und festem Updategesetz entlang wachsender
Gedachtnishorizonte zu einem lokal nichtentarteten Root der unendlichen
exponentiellen Erinnerung fortgesetzt werden kann. Zusaetzlich wird an einem
vorab gewaehlten groesseren Horizont numerisch geprueft, ob die bekannte
lokale Voll-FIFO-Stabilitaetsevidenz erhalten bleibt.

Der fruehere Kontinuumsgrenztest bei `C in {6,9,12}` ist kein Ersatz: Er
untersuchte einen lokal linearisierten dreidimensionalen Center-Relaxationsmodus
bei `A_att=35`, konstruiertem `chi`, Rauschen und retuntem `eta`. Das neue
Gate untersucht den nichtlinearen zweidimensionalen Kreisroot bei
`A_att=3.5`, `epsilon=0` und unveraendertem `eta`.

Ein Pass darf deshalb nur als lokaler Roottransfer mit numerischer
Large-H-Stabilitaetsstuetzung bezeichnet werden. Er waere kein Beweis
globaler Eindeutigkeit, generischer Kreisformation oder Stabilitaet des
unendlichdimensionalen Feldzustands.

## 2. Eingefrorenes Modell und Evidenz

Die Grundgleichung bleibt

$$
x_{n+1}=x_n-\eta\nabla(K*\rho_n)(x_n),
\qquad
\rho_{n+1}=q\rho_n+\alpha M_0
\delta(\mathord\cdot-x_{n+1}),
\qquad q=1-\alpha .
$$

Fuer einen Kreis $x_n=R e^{in\theta}$ lautet der finite Residual

$$
F_H(R,\theta)=
\binom{\cos\theta-1}{\sin\theta}
+\eta\sum_{j=1}^{H-1}\alpha M_0q^j\phi(r_j)
\binom{1-\cos(j\theta)}{\sin(j\theta)},
$$

mit $r_j=2R|\sin(j\theta/2)|$ und

$$
\phi(r)=-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
e^{-r^2/(2\sigma_{\rm rep}^2)}
+\frac{A_{\rm att}}{\sigma_{\rm att}^2}
e^{-r^2/(2\sigma_{\rm att}^2)}.
$$

Alle wissenschaftlichen Parameter bleiben exakt:

| Groesse | Wert |
| --- | ---: |
| $\alpha$ | `0.01` |
| $q$ | `0.99` |
| $M_0$ | `1.0` |
| $\eta$ | `0.15` |
| $(A_{\rm rep},A_{\rm att})$ | `(1.0,3.5)` |
| $(\sigma_{\rm rep},\sigma_{\rm att})$ | `(1.0,3.0)` |
| $\varepsilon$ | `0.0` |

Ausgangspunkt ist ausschliesslich der bereits publizierte Anchor
`R=0.946517504804225`, `theta=0.015770381717135`, `H=1200`. Kein Radius,
Winkel, Kernel-, Memory- oder Integrationsparameter darf anhand neuer
Ergebnisse gewaehlt oder retunt werden.

Die prospektive Evidenzbasis ist an Revision
`bf038d758f2dd8a367699832f194621756c39696` und folgende Blobs gebunden:

- `src/emergenz_knoten/rotating_wave.py`:
  `3b70f408ab8bb24e7cc6df4b9c61f54f17a65a4d`;
- `src/emergenz_knoten/rotating_wave_interval.py`:
  `58ce9b0862f980c17c691c4555557e8e363468a4`;
- `src/emergenz_knoten/rotating_wave_stability.py`:
  `9defb5a6876371202e1ba57cea030c997b9c6edd`;
- Discovery-JSON:
  `4d2cbd50bd61b050747af5d51752f684b42adb56`;
- Anchor-Stabilitaets-JSON:
  `1c9d5746c9553d9cb8031b58258e6d613f1633d9`;
- Anchor-Intervallzertifikat:
  `fc6e816c6895e408693fbde176afdaee963c20b9`;
- Finite-H-Audit:
  `02da3a71aded2f68f55a4babbdb96aa07d693780`.

## 3. Horizontleiter und Branch-Identitaet

Die einzige neue Achse ist

```text
H = (600, 900, 1200, 1500, 1800, 2400, 3600)
C = alpha H = (6, 9, 12, 15, 18, 24, 36)
```

Die primaere Vorwaertsleiter ist
`1200 -> 1500 -> 1800 -> 2400 -> 3600`. Die getrennte Rueckwaertsbelastung
ist `1200 -> 900 -> 600`. Ein Fehler unterhalb `H=1200` widerlegt nicht den
Grenzuebergang nach oben, muss aber als lower-tail branch loss oder
Inconclusiveness berichtet werden.

Jeder neue Mittelpunkt entsteht deterministisch durch acht Newtonschritte
bei 80 und 120 Dezimalstellen, jeweils nur vom Mittelpunkt des unmittelbar
vorherigen Leiterschritts. Eine globale Suche, ein alternativer Startwert oder
eine Parameteranpassung nach Einsicht in Ergebnisse ist verboten.
Jedes Praezisionspanel verwendet dabei durchgehend seine eigene vorherige
Panelmitte; Homotopie, Drift und spaetere Dynamik verwenden die 120-dps-Mitte.

Zwischen benachbarten Leiterschritten wird die Rootidentitaet zusaetzlich
ueber die vorab definierte Homotopie

$$
F_{a,b}(R,\theta;s)=F_a(R,\theta)
+s\,[F_b(R,\theta)-F_a(R,\theta)],
\qquad 0\le s\le1,
$$

geprueft. Der Bereich wird in 64 geschlossene, gleich breite $s$-Intervalle
geteilt. In jedem Intervall muss ein Krawczyk-Schlauch mit streng innerem Bild
den vorherigen eindeutigen Root fortsetzen. Weder adaptive Unterteilung noch
das Ueberspringen eines fehlgeschlagenen Abschnitts ist erlaubt. Ein
Krawczyk-Fehler allein beweist keinen Branchverlust; er ist numerisch
inconclusive.

Fuer jede $s$-Scheibe ist das Boxzentrum die lineare Interpolation der beiden
vorab durch das feste Newtonverfahren erzeugten Endpunktzentren am
Scheibenmittelpunkt. Die festen Halbbreiten sind `1e-4` fuer $R$ und `1e-6`
fuer $\theta$. Das Krawczyk-Bild muss fuer das gesamte geschlossene
$s$-Intervall strikt in dieser Box liegen; benachbarte Root-Einschluesse
muessen ueberlappen. Diese Konstruktion darf nach einem Fehlschlag weder
verbreitert noch verfeinert werden.

Fuer jeden der sieben Horizonte muessen beide Praezisionspanels einen lokalen
Krawczyk-Einschluss um den deterministisch verfeinerten Root liefern. Die
aeussere Halbbreite ist `1e-8` je Koordinate, die innere Halbbreite `1e-30`.
Beide Panelzentren muessen je Koordinate innerhalb `1e-50` uebereinstimmen,
und ihre inneren Einschlussintervalle muessen sich schneiden.

Als Driftmetrik gilt

$$
d_{a,b}^{\rm up}=\max\!\left(
\frac{\sup|I_R^{(b)}-I_R^{(a)}|}{R_\star},
\frac{\sup|I_\theta^{(b)}-I_\theta^{(a)}|}{\theta_\star}
\right),
$$

mit den festen positiven Normierungen
$R_\star=0.946517504804225$ und
$\theta_\star=0.015770381717135$. Alle Differenzen werden outward-rounded
ueber die geschnittenen inneren 80-/120-dps-Rootintervalle ausgewertet.
Mittelpunktwerte werden getrennt als Diagnostik gespeichert und entscheiden
kein Gate. Fuer den Vorwaertspass sind
$d_{2400,3600}^{\rm up}\le10^{-8}$ und
$d_{2400,3600}^{\rm up}\le
0.01d_{1800,2400}^{\rm up}+10^{-14}$ erforderlich. Eine Testmutation, die
eine der beteiligten Intervallbreiten ueber die Grenze vergroessert, muss den
Driftpass schliessen. Diese empirischen Driftgates ersetzen nicht das
folgende Intervallargument.
Jeder Mittelpunkt und jede Zertifikatsbox muss vollstaendig in der festen
Domain $D$ aus Abschnitt 4 liegen; ein Verlassen von $D$ ist Branchdrift.

Nur wenn eine Vorwaertsfortsetzung scheitert, darf ein automatischer
Ausschlussfalsifikator die lokale Branchdomain
$[R_{\rm prev}-0.02,R_{\rm prev}+0.02]\times
[\theta_{\rm prev}-0.002,\theta_{\rm prev}+0.002]$, geschnitten mit $D$,
pruefen. Eine feste FIFO-Warteschlange halbiert jeweils die laengere
normalisierte Boxkante bis Tiefe 20. Eine Box wird nur bei intervallbewiesenem
Residualausschluss oder einem regulaeren Krawczykresultat abgeschlossen. Nur
wenn alle Blaetter Residualausschluesse sind, ist `branch-loss` zulaessig;
jedes ungeloeste Blatt oder ein anderer eingeschlossener Root macht den
Fortsetzungsbefund inconclusive. Dieser Falsifikator darf keinen neuen
Startpunkt fuer die primaere Leiter liefern.

## 4. Unendlicher Tail und Existenztransfer

Das unendliche Residual ist $F_\infty=F_H+T_H$. Fuer die registrierten
Kernelparameter gelten global

$$
\Phi_0=sup_{r\ge0}|\phi(r)|
\le \frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
+\frac{A_{\rm att}}{\sigma_{\rm att}^2},
$$

$$
\Phi_1=sup_{r\ge0}|\phi'(r)|
\le e^{-1/2}\left(
\frac{A_{\rm rep}}{\sigma_{\rm rep}^3}
+\frac{A_{\rm att}}{\sigma_{\rm att}^3}
\right).
$$

Auf der festen Domain
$D=[0.8,1.1]\times[0.01,0.022]$ muessen outward-rounded Intervalle die
folgenden euklidischen Tailbounds verwenden:

$$
\|T_H\|_2\le2\eta M_0\Phi_0q^H,
$$

$$
\|\partial_R T_H\|_2\le4\eta M_0\Phi_1q^H,
$$

$$
\|\partial_\theta T_H\|_2
\le\eta M_0(\Phi_0+2R_{\max}\Phi_1)
q^H\left(H+\frac q\alpha\right),
\qquad R_{\max}=1.1.
$$

Diese Schranken werden bei `H=3600` als symmetrische Intervallunsicherheit
zum finite Summenresidual und seinem analytischen Jacobian addiert. Auf einer
Box mit Halbbreite `1e-10` um den 120-dps-Root bei `H=3600` muss das daraus
berechnete Krawczyk-Bild strikt im Inneren liegen. Ein zweites 160-dps-Panel
muss einen ueberlappenden Einschluss liefern. Damit wird lokal mindestens ein
Root von $F_\infty$ und, bei streng innerem Krawczyk-Bild, genau ein Root in
der registrierten Box zertifiziert. Die Aussage bleibt konditional auf den
getrackten Intervallbackend.

Die Taildarstellung trennt drei Repraesentationen. Multipraezision und
Intervalle verwenden exakt dezimal `q_dec=mp.mpf("0.99")`. Der
Produktionspfad speichert explizit `alpha64=float("0.01")` und
`q64=1.0-alpha64`. Fuer alle sieben Horizonte werden `q64**H` und
`exp(H*log(q64))` verglichen; ihre Differenz darf hoechstens zwei ULP des
direkten Ergebnisses betragen. `exp(H*log1p(-alpha64))` wird nur als
Repraesentationsdiagnostik gespeichert. Seine Differenz zur direkten Potenz
ist kein Physik- oder Validitaetsgate. Die exakte Dezimalpotenz, beide
binary64-Pfade und ihre Abweichungen werden vollstaendig protokolliert; fuer
`H=3600` darf keiner der Pfade unterlaufen oder nichtendlich werden.

Ein getrackter, fail-closed Ergebnisvertrag registriert jeden Root-,
Homotopie-, Tail-, Arnoldi-, Trajektorien-, Kontroll- und Publikationswert
mit exaktem nativen Typ, Kardinalitaet und `null`-Semantik. Der unabhaengige
Standardbibliothek-Auditor liest das Manifest zuerst, prueft alle
Dateihashes, Schemafelder, Kardinalitaeten und Endlichkeiten und rekonstruiert
Parameter, alle drei $q$-Repraesentationen, Tailbounds,
Intervall-Driftobergrenzen
und Entscheidungsrangfolge ohne Import des Runners.

Der Vertrag besitzt exakt sieben Rootobjekte: `identity` fuer
Schema/Version/Zeit/Revision/Protokoll/Provenienz/Parameter,
`finite_branch` fuer Horizonte/Rootpanels/Homotopien/Drift/Lower-tail/Replay,
`infinite_tail` fuer Konstanten/q-Repraesentationen/Bounds/Zertifikatpanels/
Panelvergleich, `stability` fuer Rootrundung/Arnoldi/Continuation/Symmetrie/
Gates, `controls` fuer Shift/Circular/eta-null/Mutationen, `classification`
fuer Gates/Entscheidung/Claimgrenze und `publication` fuer Pfad und Rolle der
beiden vor dem Manifest erzeugten Inhaltsartefakte JSON und Markdown. Der
Resultrecord enthaelt keinen selbstreferenziellen Hash; die beiden
Inhaltshashes stehen ausschliesslich im spaeter publizierten Manifest.
Unbekannte oder fehlende Felder schliessen fail-closed;
der konkrete JSON-Vertrag und seine zunaechst roten Tests muessen vor dem
Runnercode committed werden.

Der Auditor prueft gespeicherte Krawczyk-Inklusionen, Ritzresiduen und
Trajektorien nur gegen den Vertrag und ihre registrierten Summary-/Hash-
Beziehungen. Er ist kein zweiter Intervallbackend und keine unabhaengige
Arnoldi- oder Trajektorienreproduktion. Diese Vertrauensgrenze muss im
Ergebnisbericht und Ergebnisreview stehen.

## 5. Voll-FIFO-Stabilitaet und Speicherfalsifikatoren

Der einzige neue Stabilitaetsholdout ist der vorab festgelegte Root bei
`H=2400`. Der exakte sparse Jacobian der mitrotierenden 4800-dimensionalen
Voll-FIFO-Map wird in zwei Arnoldi-Panels ausgewertet:

| Panel | Ritzpaare | `ncv` | Toleranz | Max. Iterationen |
| --- | ---: | ---: | ---: | ---: |
| primaer | 24 | 96 | `1e-10` | 20000 |
| Konvergenz | 36 | 144 | `1e-12` | 40000 |

Mit Komponentenindex $k=0,\ldots,4799$ ist der normalisierte Start des
primaeren Panels
`sin(sqrt(2)*(k+1))+cos(sqrt(3)*(k+0.5))`; das Konvergenzpanel verwendet
getrennt
`sin(sqrt(5)*(k+1))+cos(sqrt(7)*(k+0.5))`. Der 120-dps-Root wird fuer die
Voll-FIFO-Rechnung genau einmal in binary64 gerundet und dieser Wert
vollstaendig protokolliert.

Alle gespeicherten Ritzresiduen muessen kleiner `1e-8` sein. Symmetriemoden,
Paneluebereinstimmung und Schwellen werden unveraendert vom Anchor geerbt:
Symmetrieueberlappung mindestens `0.99`, Eigenwertabstand hoechstens `1e-7`,
fuehrender transversaler Panelabstand hoechstens `1e-5`, stabiler Modul
kleiner `1-1e-4`, instabiler Modul groesser `1+1e-6`. Unkonvergierte oder
widerspruechliche Arnoldi-Panels sind inconclusive, nicht stabil.

Das primaere Panel muss exakt 24, das Konvergenzpanel exakt 36 endliche
Eigenwerte, zugehoerige Vektoren und normalisierte Residuen speichern.
`ArpackNoConvergence`, falsche Kardinalitaet, fehlende Vektoren oder ein
Residuum ueber `1e-8` ergeben G5-inconclusive. Auch eine
Instabilitaetsentscheidung setzt vollstaendige Panels, bestandene
Symmetriepruefung und Paneluebereinstimmung voraus.

Die drei geerbten transversalen Stoerungen verwenden Amplitude `1e-7 R`,
5000 Updates, Sampling alle 10 Schritte und den rotations-/translations-
reduzierten D0-Abstand. Sie sind exakt: ein Offset des neuesten Punkts in
radialer Richtung, derselbe Offset in tangentialer Richtung und der Vektor
`sin(0.37 k)+cos(0.11 k)` ueber alle FIFO-Komponenten nach orthogonaler
Projektion gegen beide Translationen und die Rotation. Jeder Arm muss ohne
Stop abschliessen und auf hoechstens `0.1` seines initialen Abstands
kontrahieren; der exakte Arm muss unter `1e-10` bleiben. Ein konvergiertes
transversales Ritzpaar oberhalb `1+1e-6` gilt erst zusammen mit einem
Stoerungswachstum um mindestens Faktor 100 als numerische Instabilitaet. Das
ist lokale numerische Evidenz, keine vollstaendige Spektraleinschliessung.

Zwei Speicherfalsifikatoren sind obligatorisch:

1. Ein explizites Shift-FIFO und eine zyklisch adressierte Implementierung
   muessen fuer nichtkreisfoermige deterministische Historien mit `H=17` und
   `H=257` sowie fuer die mit dem publizierten Anchor-$(R,\theta)$ erzeugten
   Kreisgeschichten aller sieben Horizonte nach Materialisierung dieselbe
   Altersfolge und einen relativen Ein-Schritt-Fehler unter `5e-14` liefern.
2. Bei `eta=0` muss eine gespeicherte Kreisgeschichte nach `H+1` reinen
   FIFO-Shifts zu einer konstanten Historie kollabieren; ihre maximale
   Abweichung vom neuesten Punkt muss unter `1e-14` liegen.

Beide Kontrollen testen Speichersemantik. Sie duerfen nicht als Root- oder
Stabilitaetsevidenz gezaehlt werden.

Die zyklische Kontrolle muss von der Shift-Produktion unabhaengig rechnen:
Sie speichert einen `head`, adressiert jedes Alter modular, akkumuliert die
gewichtete Kraft ueber diesen Indexweg und ueberschreibt den aeltesten Slot
erst nach vollstaendigem Lesen. Vor der Kraftakkumulation darf sie keine
Shift-Reihenfolge materialisieren und nicht `native_fifo_step` aufrufen.
Verglichen werden SHA-256 der materialisierten Altersfolge, der neue Punkt
und der vollstaendige Folgezustand mit
$\|a-b\|_2/\max(1,\|a\|_2,\|b\|_2)$. Mutationen der Modulo-Richtung, der
Read/write-Reihenfolge und des zu ueberschreibenden Slots muessen scheitern.

## 6. Gates und Entscheidungslogik

Die Gates werden in dieser Reihenfolge ausgewertet:

1. **G0 Provenienz/Numerik:** exakte Blobs, Parameter, zwei Praezisionspfade,
   endliche Werte, direkte Summenreplays und Tail-Identitaeten bestehen.
2. **G1 finite Roots:** `G1F` verlangt die fuenf lokalen Zertifikate der
   Vorwaertsleiter; `G1R` berichtet die zwei tieferen Horizonte getrennt.
3. **G2 Branch-Identitaet:** `G2F` verlangt alle vier
   Vorwaertshomotopien; `G2R` berichtet die zwei Rueckwaertshomotopien als
   getrenntes Stressgate.
4. **G3 Drift:** beide vorregistrierten Vorwaerts-Driftbedingungen bestehen.
5. **G4 unendlicher Root:** beide Tail-Krawczyk-Panels und ihr Ueberlapp
   bestehen.
6. **G5 Large-H-Stabilitaet:** beide Arnoldi-Panels, Symmetriekontrollen,
   Stoerungsarme und exakter Arm bestehen.
7. **G6 Speicherkontrollen:** Shift/Circular-Aequivalenz und `eta=0`-Kollaps
   bestehen.

Die finale Entscheidung wird in dieser Praezedenz vergeben:

1. G0 oder G6 scheitert:
   `rotating-wave-horizon-experiment-invalid`.
2. Ein Intervall-Ausschluss beweist, dass die registrierte lokale
   Branchdomain an einem Vorwaertshorizont keinen admissiblen Root enthaelt:
   `registered-local-horizon-branch-loss`.
3. G1F und G2F bestehen, aber G3 zeigt nichtkontrahierende Drift:
   `rotating-wave-horizon-branch-drift`.
4. G0, G1F, G2F, G3, G4 und G6 bestehen und die vorregistrierte
   Spektrum-plus-Wachstumsbedingung in G5 zeigt Instabilitaet:
   `rotating-wave-infinite-root-certified-large-h-instability`.
5. G0, G1F, G2F, G3, G4, G5 und G6 bestehen:
   `rotating-wave-horizon-root-transfer-pass-with-large-h-stability-support`.
6. G0, G1F, G2F, G3, G4 und G6 bestehen, aber G5 bleibt unentschieden oder
   stuetzt weder Kontraktion noch Instabilitaet:
   `infinite-memory-local-root-certified-stability-open`.
7. Jeder andere numerisch unentschiedene Fall:
   `rotating-wave-horizon-transfer-inconclusive`.

Ein Rueckwaertsfehler erhaelt zusaetzlich
`lower-tail-stress-loss` oder `lower-tail-stress-inconclusive`, aendert aber
allein keinen bestandenen Vorwaerts-/Unendlichkeitsbefund. G5 ohne G4 bleibt
`finite-large-h-stability-only` und darf nicht als Horizonttransfer gelten.

Nur der vollstaendige Ausgang
`rotating-wave-horizon-root-transfer-pass-with-large-h-stability-support`
darf ein spaeteres, getrenntes P5-D-Governancereview oeffnen. Auch dann sind
eine neue ausdrueckliche Nutzerentscheidung, eine frische UUID, ein exklusiver
Receiptpfad und ein Governance-only-Commit erforderlich. Alle sechs anderen
Horizontausgaenge halten P5-D geschlossen.

## 7. Implementierung, Publikation und Stopbedingungen

Eine spaetere Implementierung darf die vorhandenen wissenschaftlichen
Bibliotheken erweitern, wenn neue Funktionen allgemeine finite-/infinite-
Tail- oder FIFO-Semantik besitzen. Gateparameter, Entscheidung und
Publikationsvertrag bleiben im Experimentmodul. NumPy/SciPy tragen
Vektorrechnung und Arnoldi, `mpmath.iv` die Intervallrechnung; eine neue
Abhaengigkeit ist nicht autorisiert.

Die registrierten Pfade sind:

- Runner und Ergebnisvertrag:
  `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_gate.py`
  sowie
  `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_result_schema_v3.json`;
- unabhaengiger Auditor:
  `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_result_audit.py`
  mit Auditoutput
  `reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_independent_audit_2026-09-08.json`;
- Tests: `tests/test_rotating_wave_horizon_transfer.py` und
  `tests/test_rotating_wave_horizon_transfer_result_audit.py`;
- Ergebnis:
  `reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_2026-09-08.json`;
- lesbarer Bericht: gleicher Basispfad mit Suffix `.md`;
- Publikationsmanifest: gleicher Basispfad mit Suffix `.publication.json`;
- spaeteres Ergebnisreview:
  `reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_result_review_2026-09-08.md`.

JSON und Markdown werden zuerst in temporaere Dateien geschrieben und
gehasht; das Manifest wird zuletzt atomar publiziert. Der Auditor liest das
Manifest zuerst. Ein unvollstaendiger Satz ist kein Ergebnis.

Vor einem Lauf sind mindestens targetfreie Tests fuer Formeln/analytischen
Jacobian, die drei $q$-Repraesentationen und Tailbounds, intervallbewertete
Drift und Krawczyk-/Homotopieunterbrechung, partielle Arnoldi-Ausgaben,
unabhaengige Shift/Circular-Mutationen und `eta=0`-Kollaps sowie Schema,
Auditor, Entscheidungspraezedenz und Manifestfehler erforderlich. Danach
folgen ein separates Implementierungs-Readinessreview, sauberer Commit,
gruenes CI und erst dann genau ein registrierter Horizontlauf. P5-D bleibt
waehrenddessen geschlossen.

Die Arbeit stoppt fuer eine Protokollamendierung, wenn eine Formel oder
Tailnorm korrigiert werden muss, eine neue Suchbox oder adaptive Fortsetzung
gewuenscht wird, ein wissenschaftlicher Inputblob driftet, der Auditor
Runnerlogik importiert oder ein Ergebnis vor Manifestpublikation sichtbar
wuerde. Weder ein positiver noch ein negativer Horizontbefund autorisiert
automatisch P5-D-Versuch 4.

## 8. Zweite Amendierung: ehrliche Null- und Abbruchsemantik

Der konkrete Ergebnisvertrag muss neben einem vollstaendigen Pass jeden in
den Abschnitten 3--7 registrierten fail-closed Pfad ohne erfundene Werte
abbilden. Deshalb bleiben alle positionsgebundenen Arrays in ihrer festen
Laenge erhalten, noch nicht oder nicht vollstaendig ausgewertete Slots sind
jedoch exakt `null`.

Es gelten folgende unveraenderliche Regeln:

1. `root_panels` hat sieben Slots in der Reihenfolge der registrierten
   Horizonte. Nach einem abhaengigen Leiterabbruch sind alle nicht mehr
   zulaessig erreichbaren Slots `null`. Bereits unabhaengig vorhandene
   Anchor-Evidenz darf nur als gebundener Input, nicht als neu berechnetes
   Panel ausgegeben werden.
2. `homotopies` hat sechs Slots in der registrierten Kantenreihenfolge. Eine
   begonnene Homotopie hat 64 Scheibenslots. Ausgewertete Scheiben bilden ein
   zusammenhaengendes nicht-null Praefix; nach der ersten fehlgeschlagenen
   Scheibe sind alle spaeteren Slots `null`. Eine vollstaendige
   `status=pass`-Homotopie besitzt genau 64 nicht-null Scheiben.
3. Die beiden Driftzeilen und die zwei Tail-Zertifikatpanels behalten ihre
   feste Slotzahl. Ein Slot ist `null`, wenn seine vorausgesetzten
   Rootintervalle fehlen. Ein Drift- oder Tailpass ist dann unmoeglich.
4. Jedes Arnoldi-Panel behaelt exakt 24 beziehungsweise 36 Eigenpaarslots.
   Nicht zurueckgegebene Eigenpaare sind `null`; ein zurueckgegebener
   Eigenwert ohne Vektor speichert das Eigenpaar mit `vector=null`. Nur
   `status=complete` erlaubt ausschliesslich vollstaendige, endliche
   Eigenpaare und kann G5 stuetzen. Nicht-null Eigenpaare muessen ein
   zusammenhaengendes Praefix bilden.
5. Die drei Stoerungsarme bleiben positionsgebunden; ein nicht gestarteter
   Arm ist `null`. Jeder gestartete Arm und der exakte Arm behalten 501
   Sampleslots fuer Schritte `0,10,...,5000`. Nach einem fruehen Stopp sind
   alle Slots ausserhalb des berechneten Praefixes `null`; es duerfen keine
   Werte fortgeschrieben oder erfunden werden. Ein `completed=true`-Arm
   besitzt genau 501 nicht-null Samples und `stopped=false`.
6. In jedem nullable Array bilden nicht-null Werte ein Praefix, ausser bei
   den sieben Root- und sechs Homotopie-Slots: Dort darf die getrennte
   Rueckwaertsbelastung unabhaengig von einem Vorwaertsabbruch ausgewertet
   werden. Die erlaubten Slotabhaengigkeiten werden im Validator explizit
   rekonstruiert; beliebige innere Null-Locher bleiben unzulaessig.
7. Gatewerte muessen mit den vorhandenen und fehlenden Slots konsistent
   sein. Ein fehlender vorausgesetzter Slot ergibt `inconclusive`, niemals
   `pass` oder einen positiven Claim. Ein vollstaendiger numerischer
   Ausschlussfalsifikator bleibt die einzige Grundlage fuer
   `local_branch_excluded=true`.

Vor wissenschaftlichem Runnercode muessen targetfreie Negativ-Witnesses
mindestens einen Leiterabbruch, einen Homotopieabbruch, partielle
Arnoldi-Ausgabe, fehlenden Arnoldi-Vektor und fruehen Trajektorienstopp
validieren. Mutationen von `null` zu erfundenen Werten nach einem Stopp,
innere Null-Locher und positive Gates trotz fehlender Voraussetzung muessen
von Runner-Validator und unabhaengigem Auditor verworfen werden.

## 9. Dritte Amendierung: vollstaendiger Nachweisrecord

Die Nullsemantik aus Abschnitt 8 bleibt unveraendert. Der v3-Vertrag muss
zusaetzlich jeden fuer einen positiven oder negativen Claim verwendeten
Nachweis aus den gespeicherten primitiven Intervall- und Vektordaten
rekonstruierbar machen.

1. Jedes 80-/120-dps-Rootpanel speichert getrennt das aeussere
   Krawczyk-Zertifikat mit Halbbreite `1e-8` und das innere mit Halbbreite
   `1e-30`. `inner_intersection` ist exakt der outward gerundete Schnitt der
   beiden inneren Krawczyk-Bilder. `centers_agree` wird aus den beiden
   Newtonmittelpunkten je Koordinate gegen `1e-50` rekonstruiert.
2. Ein `residual-excluded`-Leaf speichert beide Intervallkomponenten von
   $F_H$ auf seiner Box; mindestens eine Komponente muss Null ausschliessen.
   Ein `krawczyk-root`-Leaf speichert sein Krawczyk-Bild und die strikte
   Inklusion in die Leafbox. Nicht zur Klassifikation passende oder fehlende
   Witnessfelder sind unzulaessig.
3. Fuer jede Homotopiescheibe werden $s$-Intervall, Box und Krawczyk-Bild als
   Dezimalendpunkte gespeichert. Der Auditor rekonstruiert exakt
   $[i/64,(i+1)/64]$, strikte Inklusion und die Ueberlappung aufeinander
   folgender Krawczyk-Bilder. Das gespeicherte Boolfeld allein entscheidet
   nichts.
4. Der Schnitt und die Ueberlappung der beiden 120-/160-dps-
   Tail-Krawczyk-Bilder werden ebenfalls ausschliesslich aus den gespeicherten
   Endpunkten rekonstruiert.
5. Der primaere Arnoldi-Start ist die normierte binary64-Auswertung
   `sin(sqrt(2)*(k+1))+cos(sqrt(3)*(k+0.5))`. Der Konvergenzstart ist die
   normierte binary64-Auswertung
   `sin(sqrt(5)*(k+1))+cos(sqrt(7)*(k+0.5))`, jeweils fuer
   `k=0,...,4799`. Die Norm ist deterministisch
   `sqrt(fsum(v_k*v_k))`; Division und trigonometrische Werte sind native
   binary64. Ihre SHA-256 ueber contiguous little-endian float64-Bytes werden
   als Vertragskonstanten gebunden und im
   Standardbibliothek-Auditor ohne NumPy rekonstruiert. Der abweichende
   allgemeine `S2`-Start aus der bestehenden Bibliothek ist fuer dieses Gate
   unzulaessig.
6. Jeder der drei Stoerungsarme speichert `amplitude=1e-7 R_2400`, den
   tatsaechlich verwendeten 4800-Komponenten-float64-Vektor und dessen
   SHA-256 ueber contiguous little-endian Bytes. Runner-Validator und
   Standardbibliothek-Auditor rekonstruieren radialen, tangentialen und den
   gegen drei Symmetrietangenten projizierten Voll-FIFO-Stoss aus der
   gerundeten Kreisgeschichte. Fuer den Voll-FIFO-Stoss werden zusaetzlich
   Norm und drei Skalarprodukte gegen die Symmetrietangenten geprueft. Alle
   Normen und Skalarprodukte dieser Konstruktion verwenden ebenfalls
   `sqrt(fsum(v_k*v_k))` beziehungsweise `fsum(a_k*b_k)` in aufsteigender
   Komponentenreihenfolge.
7. `rounded_root` wird exakt durch binary64-Rundung des gespeicherten
   120-dps-H=2400-Newtonroots rekonstruiert. Ein abweichender Root darf weder
   Jacobian noch Arnoldi noch Stoerungen speisen.

Vor Runnercode muessen Mutationen fuer fehlendes aeusseres Zertifikat,
falschen inneren Schnitt, unbelegten Residualausschluss, falsches
Homotopie-s-Intervall, falsche Einschluesse, falschen Arnoldi-Starthash,
falschen Stoerungshash und abweichenden gerundeten Root scheitern.
