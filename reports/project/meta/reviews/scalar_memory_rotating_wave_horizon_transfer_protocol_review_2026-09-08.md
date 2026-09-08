# Review: Protokoll zum Rotating-wave-Horizonttransfer

Datum: 2026-09-08.

Gepruefte Protokollrevision:
`c936fa584ae45657fb8f3e8628e797564ee75329`.

Gepruefter Protokollblob:
`bb66dae815c30d1e35971d8cb06e9c37e9892d8f`.

Gepruefte CI:
[GitHub Actions run 34185742741](https://github.com/MemoryDynamics/Knoten/actions/runs/34185742741),
erfolgreich fuer die exakte Protokollrevision.

Verdict:
**`rotating-wave-horizon-transfer-protocol-needs-amendment`**.

Das Protokoll stellt die richtige wissenschaftliche Frage und seine
analytischen Tailbounds sind konservativ korrekt. Es darf dennoch noch nicht
implementiert werden. Ein deterministisch falsches binary64-Kontrollgate und
fuenf weitere Spezifikationsluecken koennten einen korrekten Lauf als invalid
klassifizieren oder die Staerke eines spaeteren Ergebnisses ueberzeichnen.
Dieses Review ist targetfrei und autorisiert weder Horizonttrajektorien noch
P5-D-Versuch 4.

## 1. Positive Befunde

1. Das Protokoll haelt `alpha=0.01`, `eta=0.15`, `M0=1`, Kernel und
   `epsilon=0` fest. Es testet damit erstmals den Kreisroot entlang $H$ und
   wiederholt nicht den frueheren retunten linearen Center-Grenztest.
2. Vorwaertsleiter, untere Belastung und unendlicher Tail sind getrennt. Ein
   Fehler bei `H<1200` kann den Grenzuebergang nach oben nicht logisch
   widerlegen.
3. Die Homotopie ist outcome-blind festgelegt. Ein fehlgeschlagenes
   Krawczykbild gilt korrekt als inconclusive und nicht als Rootverlust.
4. Der lokale Ausschlussfalsifikator erlaubt `branch-loss` nur nach
   vollstaendigem Intervall-Ausschluss einer registrierten Domain.
5. Arnoldi, direkte Stoerungsarme und die Speicherkontrollen werden nicht als
   unendlicher Stabilitaetsbeweis bezeichnet.
6. Publikationsmanifest, unabhaengiger Auditor und P5-D-Schliessung sind vor
   Implementierung registriert.

## 2. Analytische Pruefung der Tailbounds

Mit
$v_j=(1-\cos(j\theta),\sin(j\theta))$ gilt
$\lVert v_j\rVert_2\le2$ und
$\lVert\partial_\theta v_j\rVert_2=j$. Ferner sind
$|\partial_R r_j|\le2$ und
$|\partial_\theta r_j|\le Rj$. Daher folgen aus den registrierten
$\Phi_0$- und $\Phi_1$-Schranken

$$
\|T_H\|_2\le2\eta M_0\Phi_0q^H,
\qquad
\|\partial_RT_H\|_2\le4\eta M_0\Phi_1q^H,
$$

und wegen

$$
\sum_{j=H}^{\infty}\alpha jq^j
=q^H\left(H+\frac q\alpha\right)
$$

auch die registrierte $\theta$-Ableitungsschranke. Die Verwendung dieser
euklidischen Bounds als symmetrische komponentenweise Intervallzugaben ist
konservativ. An diesen Formeln wurde kein Vorzeichen- oder Indexfehler
gefunden.

Die Bounds allein beweisen noch keinen Root. Der geplante strikt innere
Krawczyk-Einschluss muss weiterhin die Nichtentartung und Existenz in der
registrierten lokalen Box liefern; seine Aussage bleibt auf den getrackten
Intervallbackend bedingt.

## 3. Blockierende Findings

### HT-P01 -- kritisch: das binary64-Tail-Kontrollgate ist konstruktiv falsch

Das Protokoll verlangt fuer `q**H` und `exp(H*log1p(-alpha))` relative
Uebereinstimmung unter `2e-15`. Diese Ausdruecke berechnen nicht denselben
binary64-Input: `q=1.0-alpha` ist bereits gerundet, waehrend `log1p(-alpha)`
die Subtraktion umgeht. Bei den sieben registrierten Horizonten betraegt die
relative Differenz bereits etwa `5.23e-15` bis `2.85e-14`; G0 wuerde daher
ohne wissenschaftlichen Fehler sicher scheitern.

Die Amendierung muss drei Ebenen unterscheiden: exaktes dezimales
`q=0.99` fuer Multipraezision/Intervalle, explizites `q64=1.0-alpha64` fuer
den Produktionspfad und einen ULP-Vergleich von `q64**H` mit
`exp(H*log(q64))`. Fuer die registrierten Werte genuegen zwei ULP. Der
Unterschied zur exakten Dezimalpotenz ist als Repraesentationsfehler zu
protokollieren, nicht als Physikgate zu verwenden.

### HT-P02 -- hoch: die Driftgates ignorieren Zertifikatsunsicherheit

$d_{a,b}$ wird nur aus 120-dps-Mittelpunkten gebildet. Ein Roottransferclaim
muss jedoch aus den zertifizierten Rootintervallen folgen. Die Amendierung
muss fuer beide Driftbedingungen outward-rounded obere Schranken ueber alle
Endpunkte der beiden Einschlussboxen verwenden. Mittelpunktwerte duerfen nur
Diagnostik sein. Eine Mutation, die die Intervallbreite vergroessert, muss
den Driftpass schliessen.

### HT-P03 -- hoch: die Circular-FIFO-Kontrolle kann tautologisch werden

Die Formulierung verlangt dieselbe Altersfolge nach Materialisierung, legt
aber nicht fest, dass Kraftsumme, Indexfortschaltung und Ueberschreiben in
einem unabhaengigen zyklischen Backend erfolgen. Eine Implementierung koennte
den Ring zuerst in die Shift-Reihenfolge kopieren und danach dieselbe
Produktionsfunktion aufrufen. Das testet nur Kopieren.

Die Amendierung muss einen unabhaengigen Indexweg mit `head`, modularer
Altersadressierung, eigener gewichteter Kraftakkumulation und
Overwrite-after-read verlangen. Zu vergleichen sind materialisierter
Alters-Hash, neuer Punkt und kompletter Folgezustand. Der relative Fehler ist
als `||a-b||_2/max(1,||a||_2,||b||_2)` zu definieren. Mutationen von
Modulo-Richtung, Read/write-Reihenfolge und aeltestem Slot muessen scheitern.

### HT-P04 -- hoch: der Auditorvertrag ist zu unscharf

Der Auditor soll Parameter, Tailbounds, Drift und Entscheidung
rekonstruieren, doch Schema, Pflichtfelder, Manifestpruefung und die Grenze
seiner wissenschaftlichen Unabhaengigkeit sind nicht festgelegt. Ein
Standardbibliothek-Auditor kann gespeicherte Arnoldi- oder Krawczykresultate
nicht unabhaengig beweisen, ohne die jeweilige Numerik neu zu implementieren.

Die Amendierung muss einen getrackten Ergebnisvertrag oder eine exakte
Feldtabelle verlangen. Der Auditor muss Manifest und Hashes zuerst pruefen,
Kardinalitaeten und Endlichkeit fail-closed behandeln sowie Tail-, Drift- und
Entscheidungslogik unabhaengig rekonstruieren. Krawczyk-Inklusionen,
Ritzresiduen und Trajektorien bleiben verifizierte Runnerrecords, sofern kein
separater numerischer Rebuild registriert wird; diese Vertrauensgrenze muss
im Ergebnis stehen.

### HT-P05 -- mittel: partielle Arnoldi-Ausgaben sind nicht entschieden

Die Tabelle nennt 24 und 36 angeforderte Ritzpaare, fordert aber nicht
ausdruecklich exakt diese gespeicherten Kardinalitaeten. ARPACK kann bei
Nichtkonvergenz partielle Eigenpaare liefern. Ein kleineres, zufaellig
guenstiges Panel darf weder Stabilitaet noch Instabilitaet stuetzen.

Beide Panels muessen exakt 24 beziehungsweise 36 endliche Paare mit Vektoren
und Residuen liefern. `ArpackNoConvergence`, falsche Kardinalitaet, fehlende
Vektoren oder ein Residuum ueber der Grenze ergeben G5-inconclusive. Die
Instabilitaetsentscheidung muss dieselben vollstaendigen Panel- und
Symmetriekontrollen voraussetzen wie der Stabilitaetspass.

### HT-P06 -- mittel: lokale und Governance-Claims brauchen eine harte Grenze

Der Ausschlussfalsifikator prueft nur eine lokale Domain um den vorherigen
Root. Sein Ergebnis darf deshalb nur
`registered-local-horizon-branch-loss` heissen; ein globaler Rootverlust ist
nicht gezeigt. Ausserdem bleibt offen, welcher Horizontentscheid spaeter
ueberhaupt eine neue P5-D-Designentscheidung erlauben koennte.

Die Amendierung muss festlegen: Nur
`rotating-wave-horizon-root-transfer-pass-with-large-h-stability-support`
darf ein separates P5-D-Governancereview oeffnen. Auch dann bleiben explizite
Nutzerentscheidung, neue UUID, neuer Receiptpfad und Governance-only-Commit
obligatorisch. Alle sechs anderen Horizontausgaenge halten P5-D geschlossen.

## 4. Erforderliche Amendierung und Stopgrenze

Vor Implementierung sind alle sechs Findings im Protokoll selbst zu
schliessen. Danach muessen Amendierungscommit und CI gruen sein und ein
separates Suffizienzreview die exakten neuen Blobs binden.

Insbesondere darf HT-P01 nicht durch Lockern einer relativen Toleranz behoben
werden; die verglichenen Repraesentationen muessen zuerst semantisch gleich
sein. Ebenso darf HT-P03 nicht durch einen Vergleich zweier Aufrufe derselben
materialisierten Kraftfunktion geschlossen werden.

Bis dahin lautet der einzige belastbare Befund:
**`rotating-wave-horizon-transfer-protocol-needs-amendment`**.
