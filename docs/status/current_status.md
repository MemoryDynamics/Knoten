# Aktueller Stand

Stand: 2026-11-22 (raeumlich gemeinsames Rauschen bindet getrennte Knoten nicht stationaer; positiver 3D-Formkandidat weiter ungeprueft).

Diese Seite berichtet nur den gegenwaertigen Befund. Die Arbeitsreihenfolge
steht ausschliesslich in den [Projektprioritaeten](project_priorities.md); der
vollstaendige vorherige Stand liegt im
[Repository-Archiv](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/docs/archive/status/current_status_through_2026-09-02.md).

## Evidenz

Der [raeumliche Feldrauschvergleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_spatial_noise_2026-11-22.md)
kontrolliert kurzreichweitig korrelierte, pro Schritt frische
Gaussinnovationen. Bei festem unabhaengigem Rauschanteil bleibt
in d>=3 fast sichere Trennung. Bei rein gemeinsamem Feld ist die
exakte Diagonale identischer Historien invariant, aber keine
stationaere Verteilung getrennter Orte moeglich. Ein isotropes
Skalarfeld erlaubt keine perfekte Korrelationsschale bei r>0.
Getrennter Rauschvertrag, keine emergente Felddynamik.

Die [Besetzungs- und Budgetabschaetzung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_summable_cross_drift_2026-11-22.md)
liefert in d>=3 fast sichere Trennung und aequivalente freie
und gekoppelte Pfadmasse fuer endliche direkte Paare mit
beschraenktem Kraftschwanz O(r^-p), p>1, und unabhaengigem
positivem Gaussrauschen. Das umfasst feste Gausskerne und
den regulaeren 1/r^2-Vergleich. Bei festen Kerneln stimmt
der Brown-Grenzprozess mit dem freien Paar ueberein.
Keine Aussage ueber Verweilzeiten, singulaere Kerne
oder vermittelte Wechselwirkung.

Der [Fluchtbeweis bei fester Breite](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_fixed_range_escape_2026-11-22.md)
schliesst in d>=3 eine stationaere Abstandsverteilung
fuer endliche direkte Gauss-FIFOs bei unabhaengigem
positivem Rauschen aus. Aus jedem Start bleibt eine
positive Fluchtwahrscheinlichkeit; alte Quelldeposits
werden auf den Vergleichspfaden mit kontrolliert.
Keine Weitbereichsgrenze, keine sichere Flucht oder
Angabe einer metastabilen Lebensdauer.

Der [breite Paargrenzfall](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_diffusive_limit_2026-11-22.md)
kontrolliert direkte Gauss-Kreuzkopplung auf einer gemeinsamen
Weitbereichs- und Diffusionsskala. Im Kreuzterm bleibt die
Quellenmasse; die Selbsthistorie bestimmt getrennt Mobilitaet
und Diffusion. Gleiche Quellen erzwingen keinen
driftfreien einfachen Mittelpunkt. Der relative Grenzprozess
besitzt bei beschraenktem Gauss-Potential keine stationaere
Abstandsverteilung auf freiem Raum. Kein Paar-Ziellauf und
keine Aussage zum festbreiten nativen Langzeitprozess.

Die [stationaere Kopfantwort](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fading_memory_stationary_mobility_2026-11-22.md)
leitet Mobilitaet bei festem Gaussrauschen als absolut summierbare
Innovationskorrelation her, auch fuer unendliches geometrisches Memory.
Diffusion ist eine andere Korrelation. Die am freien Lauf kalibrierte
Einstein-Proportionalitaet scheitert schon im schwach attraktiven nativen
Zwei-Orte-Skalar-FIFO; dessen Inkremente verletzen detaillierte Balance.
Kein physikalischer Kraftport, keine Entropie- oder Zielauswertung.

Der [diffusive Langzeitgrenzsatz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fading_memory_diffusive_transport_2026-11-21.md)
liefert bei festem positivem Gaussrauschen und geometrischen
Altersgewichten eine isotrope Brownsche Ortsgrenze mit strikt
positiver Kovarianz, ohne Annahme kleiner Gains. Der
Koeffizient ist durch eine konvergente Korrelationssumme
bestimmt und konvergiert beim Trunkieren ohne Nachnormierung.
Kein Zahlenwert fuer den nativen Kandidaten, kein gemeinsamer
Rausch-/Retentionsgrenzwert und keine aus Memory abgeleitete Traegheit.

Die [stochastische Zukunftskopplung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fading_memory_future_mixing_2026-11-21.md)
beweist exponentielles Vergessen in der kuenftigen Inkrementfolge
bei festem positiven Gaussrauschen und geometrischer Retention,
auch fuer unendliches relatives Skalar-/Alignment-Gedaechtnis.
Das stationaere Gesetz ist eindeutig; der volle unendliche Tail
mischt nicht in Totalvariation. Der Fehler fester stationaerer
Fenster beim Trunkieren ist durch die verworfenen Gewichte beschraenkt.
Kein Transportkoeffizient, Kleinrauschlimes oder Ziellauf.

Die [720-Grad-Pfadgegenprobe](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_spin_path_memory_2026-11-21.md)
konstruiert alterskonsistente Folgen mit Liftzeichen +,-,+,
aber identischem aktiven FIFO nach einer gemeinsamen Endfolge.
Ein idealisierter unendlicher exponentieller Speicher laesst
die Pfadunterschiede exakt geometrisch abklingen; ein stetiges
diskretes Label kann sie dort nicht dauerhaft tragen.
Keine native Zielbahn oder hergeleitete Spinor-Dynamik.

Die [Gebietsausschluesse](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/four_cycle_stability_exclusions_2026-11-21.md)
schliessen im gleichbreiten attraktiven FIFO sehr kleine Radien mit
innenliegendem Defekt und sehr grosse Hoehen in 3D aus. Eine weitere
Ortsdimension ist bei innenliegendem Defekt und f>=1/2 transversal
instabil. Bei festem Seitenverhaeltnis und normierter Retention
gibt es genau eine Grenze der zusaetzlichen Formmode; nahe der
oberen Seitenverhaeltnisgrenze ueberlappen 3D- und 4D-Ausschluss.
Keine Dimensionsauswahl, Spin- oder Kandidatenauswertung.

Die [Vierphasen-Poseantwort](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/four_cycle_pose_response_2026-11-21.md)
trennt unter Nichtresonanz eine moegliche spiegelungerade Querdrift
von der linearen Kippantwort. Ein axialer Input erkennt keine der
beiden Raten. Bei strikter Formstabilitaet stimmen Schwerpunktdrift
und ueber vier Phasen gemittelte Nullpunktdrift linear ueberein,
nicht notwendig fuer eine einzelne Phase. Keine nativen
Koeffizienten, keine physikalische Kraft oder Masse bestimmt.

Die [axiale Fortsetzung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/four_cycle_axial_response_2026-11-21.md)
liefert bei fehlenden Formmultiplikatoren +1 und -1 im mitgedrehten
Einschrittblock eine deformierte relative Zweiperiode unter kleinem
konstantem Kopfinput. Axialer Versatz ist ungerade, die zusaetzliche
Drehung gerade. Eine 3-mal-3-Gleichung liefert axiale Antwort und
Formstoerung; ein strikt innenliegender regulaerer Defekt bleibt
auf der fortgesetzten Bahn innen. Kein Ergebnis fuer Betrag,
Vorzeichen oder Stabilitaet am nativen Zielkandidaten; kein
physikalischer Kraftport.

Der [aktive Formabschluss](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/four_cycle_active_form_2026-11-21.md)
reduziert die native nichtlineare Regel auf vier Orte und die
aelteste Einheitsrichtung, ohne die aelteste Schrittlaenge.
In 3D bleiben acht lokale Formkoordinaten. Drei geteilte Orte
schliessen eine zusaetzliche exakt starre Poseaenderung aus.
In 4D schliesst erst die gespeicherte Richtung die verbleibende
Drehfreiheit fuer den eingebetteten tetraedrischen Vierzyklus.
Die Fehlerschranken trennen Poseaenderung und Formabweichung;
keine Aussage ueber Stabilitaet oder Mobilitaet deformierter Zustaende.

Der [Paar-Zeitumkehrtest](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_time_reversal_2026-11-21.md)
trennt den reziproken Center-Transfer von den gemeinsamen stationaeren
Fluktuationen der Center-Inkremente. Verschiedene geometrische
Altersfilter verhindern im attraktiven linearen Gauss-Vergleich
Zeitumkehrsymmetrie fuer alle positiven unabhaengigen Rauschvarianzen.
Theoretisch genuegen endlich viele positive Kreuzlags; keine
physikalische Entropie-, Kraft- oder Quantenidentifikation.

Der [Abgleich korrelierter weisser Anstoesse](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_white_noise_2026-11-21.md)
erhaelt diese Zeitumkehrgrenze fuer gleiche H>=3 und verschiedene
geometrische Retentionen bei beliebiger konstanter Kovarianz.
Der explizite H=2-Gegenfall begrenzt den Satz. Zeitlich strukturierte
Umgebungsantwort und physikalische FDT bleiben offen.

Der [passive Rauschvergleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_port_spectrum_2026-11-21.md)
liefert am deklarierten Center-Arbeitsanschluss ein eindeutig
bestimmtes farbiges Referenzspektrum bis auf eine gemeinsame Skala.
Bei H=2 ist es positiv und kausal realisierbar. Laengerer Speicher
mit langsamem Vergessen kann trotz linearer Stabilitaet harmonisch
aktiv sein; dann ist dieses passive Bad nicht moeglich. Keine
physikalische Portselektion oder Modell-Implementierung.

Die [stationaere Schalenbilanz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/critical_fifo_stationary_tail_2026-11-21.md)
schliesst das linear vorhergesagte isotrope 1/r-Dichteprofil in der
exakten nichtlinearen deterministischen Mittelfeldregel aus. Der
quadratische Transport hinterlaesst einen Schalenrest festen Vorzeichens.
Auch ein entsprechendes Potential bei u=O(1/r) ist ausgeschlossen.
Der lineare Transferpol bleibt korrekt; keine Aussage zum stochastischen
Vielteilchenlimit oder zur Existenz anderer stationaerer Profile.

Der [kritische FIFO-Mittelfeldvergleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/collective_fifo_screening_2026-11-21.md)
liefert aus attraktiver kollektiver Gauss-Rueckkopplung eine statische
1/r-Antwort an einer genau gesetzten Schwelle. Die Langwellenrate ist
quartisch statt ballistisch. Bei gleicher Gesamtstaerke liefert H=1
denselben Pol; der Altersfilter aendert die Rate erst in Ordnung k^6.
Kein Nachweis eines kontrollierten kritischen Vielteilchen-Grenzfalls,
einer universellen Kopplung oder von Gravitation.

Die [Fluktuationspruefung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/critical_fifo_fluctuations_2026-11-21.md)
liefert die exakte Ein-Schritt-Kovarianz der empirischen Dichtemoden.
Die lineare kritische Referenz hat Varianz der Ordnung 1/(N k^2).
Das relative Zweitharmonische Signal waechst in zwei begrenzten
Vergleichen bei fester 3D-Dichte wie L^(3/2). Das markiert die fehlende
nichtlineare Kontrolle, beweist aber keinen Verlust des Fernfelds.

Der [endliche Paartransfer](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_dynamic_reciprocity_2026-11-21.md)
trennt um stationaere konstante Historien exakt Center- und Ortsantwort.
Der Centertransfer wird mit passend normiertem additivem Punktantrieb
symmetrisch; der Ortstransfer braucht zusaetzlich gleiche Altersfilter.
Diese Differenz kann beim ersten Kreuzsignal verborgen bleiben, zeigt
sich bei ungleicher geometrischer Retention aber beim naechsten Schritt.
Kein physikalischer Kraftport und kein Transferbeleg fuer rotierende Knoten.

Die [4D-FIFO-/Spinprojektion](../reference/fifo_4d_spin_projection.md)
realisiert die angefragte 720-Grad-Wiederkehr als rein reelle Referenz:
vier Speicherplaetze, acht innere Umlaufphasen und vier Phasen des
gewaehlten quadratischen 3D-Readouts. Kopfrotation und Readout sind
Inputs, keine Memory-Emergenz. 20 feste Algebra-/Einbettungskontrollen
bestehen. Die unveraenderte rauschfreie native Regel mit Delta-Deposition
ist dagegen mit isometrischer 3D-/4D-Einbettung vertraeglich: keine
Periodenverdopplung. Ihr eingebetteter Gauss-Vektorfeldnullpunkt wird
zur Nullstellenlinie, nicht zum regulaeren 4D-Punktdefekt.
Keine neue Zieltrajektorie, Stabilitaetsentscheidung oder Aenderung an Paper I.

Die [aktive 4D-FIFO-Variante](../reference/fifo_4d_spin_projection.md#aktiver-fifo-der-speicher-liefert-den-naechsten-schritt)
liest den neuen Kopf aus dem negierten aeltesten Eintrag. Damit gilt
exakt $F^4=-I$, $F^8=I$. Ein passend phasenversetztes Fenster dreht
einen ganzen ausgelesenen 3D-Rahmen; das Gegenbeispiel mit vier anfangs
gleichen Eintraegen hat dieselbe interne Periode bei festem Rahmen.
Diese gesetzte Speicherregel ist neutral und keine native Spinableitung.

Die [relative 4D-FIFO-Auslese](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_4d_relative_phase_2026-11-22.md)
liefert einen exakten Gegenvergleich: Nur Rahmenzugriff bleibt blind.
Im gemeinsamen internen 4D-Koordinatensystem ist der Gauss-Kernel
fuer alle Phasen genau bei antipodal gleichen Altersgewichten blind.
Eine ruhende Abfrage mittelt anders als ein mitlaufender Referenz-FIFO.
Die gemeinsame interne Referenz ist eingesetzt, nicht hergeleitet;
keine native Rueckkopplung, Synchronisation oder Bindung nachgewiesen.
Fuer tatsaechlich antiparallele 3D-Richtungen werden beide
Kernelvorzeichen getrennt kontrolliert; das Driftvorzeichen folgt
aus dem Kernel, nicht aus dem Spinlabel. Ein anschliessender
begrenzter Referenztest mit Rueckkopplung ueber acht Schritte
bestaetigt: Der interne Abstand waechst bzw. schrumpft, obwohl
die 3D-Pfeile in beiden Faellen die Antiparallelitaet verlieren.
Nullkopplung kehrt exakt zurueck. Das Kernelvorzeichen bleibt
offen; eine 3D-Ortskraft oder Bindung wurde nicht getestet.

Das [orientierte Vierplatzvolumen](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_oriented_volume_2026-11-23.md)
liefert ein aus den Speichervektoren bestimmtes relatives Vorzeichen,
das die 3D-Rahmen nicht verraten; auf dem planaren Referenzumlauf ist
es null. Fuer den freien FIFO ist es exakt erhalten. Bei jeder
nichtkonstanten glatten radialen Kernelform gibt es Fenster, fuer
die das einzelne Kopfschreiben die Volumensumme schon bei
beliebig schwacher Kreuzkopplung verletzt. Ein anderer radialer
Kernel allein schliesst die Quellenbilanz also nicht.

Der [bilanzierte Volumentransfer](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_balanced_volume_2026-11-23.md)
korrigiert als Referenz den rohen Kopfdrift minimal bei festem
Gesamtvolumen. Der endliche Transfer ist nicht null. Die Bilanz
ist eingesetzt, nicht nativ hergeleitet. Eine allgemeine Sperre
bleibt: Stetige Ein-Kopf-Updates mit exakter Volumenerhaltung
koennen rein planare Fenster nicht aus ihren alten Ebenen heben.

Die [native 4D-Wiederkehrpruefung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/native_fifo_four_volume_rotation_2026-11-23.md)
schliesst starre gebundene Ein-Schritt-Wiederkehr mit vollem
Vierervolumen bei positivem Alignment aus; negativer Gain
braucht einen abstossenden Skalarbeitrag. Ein exakter nativer
Fuenfzyklus mit dieser Gegenkopplung existiert, ist aber
analytisch instabil und besitzt mit vier unabhaengigen
Deposits keine Nullstelle des nativen Vektorreadouts.

Die [native Fuenf-Deposit-Familie](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/native_fifo_five_deposit_defect_2026-11-23.md)
liefert mit positivem Alignment und rein attraktivem Gauss-Kernel
einen bei jedem Schritt regenerierten, in einem ganzen Teilbereich
strikt innenliegenden $+1$-Defekt. Die volle Historienableitung
erzwingt ueber die Spur auf dem gesamten konstruierten Zweig
eine wachsende Mode. Kein robuster Traeger und keine Gegenladung.

Die [Sechsphasen-Grenze](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_defect_phase_threshold_2026-11-23.md)
beweist fuer geschlossene vollrangige Sechs-Deposit-Spuren
in 4D genau eine regulaere Nullstelle mit Index $+1$.
Laengere Fenster mit denselben Phasen aendern das nicht.
Zehn vorgegebene Deposits mit nativen Gewichten erlauben
beide lokalen Vorzeichen, aber noch keine native Rekurrenz
des Minusdefekts oder eine isolierte Gegenladung.

Die [Phasen- und Kraftpruefung des Zehn-Deposit-Zeugen](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_negative_phase_recurrence_2026-11-23.md)
bestaetigt den Minusindex in jedem vorbereiteten Fenster.
Die native Kraftbilanz scheitert aber fuer diese Geometrie
an zwei tangentialen Bedingungen, auch bei getrenntem
Vergessen und beliebigem radialem Skalarprofil. Periodische
Orbits aus derselben affinen Ein-Schritt-Abbildung koennen
unabhaengig von ihrer Phasenzahl keinen Minusindex tragen.

Der [inverse radiale Referenzbenchmark](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_inverse_radial_pair_2026-11-23.md)
konstruiert zwei deformierte Zehn-Phasen-Orbits beider
Vorzeichen mit demselben freien Skalarprofil und nativem
Vektorport. Er erfuellt exakt die Kopfgleichungen, aber
die Interpolationswerte erzwingen keine Stabilitaet.
Keine Herleitung des Doppel-Gauss-Kernels, keine
spontane Bildung und kein interagierendes Paar.

Die [radiale Vorzeichenobstruktion](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_radial_sign_obstruction_2026-11-23.md)
erzwingt bei den beiden inversen Referenzbahnen mindestens
drei bzw. zwei skalare Kraftvorzeichenwechsel fuer jeden
Vektorgain. Das schliesst den nativen Doppel-Gauss-Kernel auf
beiden Geometrien und eine Dreifach-Gauss-Summe auf der
Plusgeometrie aus, ohne Parameterfit oder Zieltrajektorie.

Der [relative Vergleich zweier gespeicherter Rahmenwege](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_relative_frame_lift_2026-11-22.md)
benoetigt bei gegenlaeufigen Halbdrehungen minimal drei Proben je
Arm, aber keine gemeinsame interne 4D-Basis. Der einzelne
Richtungspfeil bleibt dabei konstant. Der Lift ist fuer die
Vierteldrehungsprobe bei Rahmenfehlern unter 45 Grad garantiert
stabil und verschwindet aus der Auslese nach dem Altern der
unterschiedlichen Proben. Dieses Bit ist kein stetiger
gravitativer Aktionsphasenbeitrag.

Der [skalare Bahnphasentest](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_gravity_action_phase_2026-11-22.md)
schliesst eine zur Haltezeit proportionale Hoehenphase fuer die
additive translationsinvariante Eigenmemory-Auslese mit summierbaren
Altersgewichten aus. Fuer den gemeinsamen linearen kritischen Kanal
betragt der kumulierte Anteil nach einer Relaxationszeit etwa 37
Prozent der stationaeren Referenz; die Zeit skaliert mit $k^{-4}$
auch ohne FIFO-Verzoegerung. Phasenregel, mechanische Masse und
universeller Kraftport bleiben unabgeleitet.

Der [Zwei-Zeiten-Wirkungstest](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_single_path_action_2026-11-22.md)
schliesst fuer den unveraenderten retardierten Eigenmemory-Drift
eine Darstellung als Wirkungsgradient auf einer einzelnen Bahn aus: Die spaetere
Kraft haengt vom frueheren Ort ab, nicht umgekehrt. Die summierten
Lesepotentiale liefern beim Variieren einen zusaetzlichen Term aus
spaeteren Zeiten. Die exakte Fourier-Darstellung der Gauss-Pfaddichte
behaelt die Kausalitaet bei, liefert aber nur klassische Statistik.
Ein erweiterter Wirkungsabschluss bleibt offen.

Der [lineare Zwei-Bahn-Vergleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_gaussian_influence_2026-11-22.md)
liefert dafuer einen exakten Test: Eine kausale Verzoegerung im
Gaussschen Einflussfaktor legt eine Mindest-Dephasierung fest.
Unterhalb koennen drei Historien trotz unauffaelliger Paarbetraege
keine gemeinsame Quantenumgebung haben. An der Grenze existiert
eine kontrollierte Vakuum-Moden-Referenz; ihre Zuordnung zum
nativen Rauschen, Lokalitaet und Massenkopplung bleiben offen.

Der [thermische Abtasttest](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_thermal_sampling_2026-11-22.md)
trennt jetzt einen aufgeloesten Gleichgewichtskanal von diskreter
Positivitaet: Eine endliche Verzoegerungsantwort und exakt weisse
Dephasierung passen dort nicht zusammen. Oberhalb der diskreten
Grenze lassen sich dieselben FIFO-Daten mit hochfrequenten
thermischen Baedern reproduzieren, die zwischen den Proben
unterschiedlich sind. Bandbreite und Messintervall werden damit
Teil des physikalischen Vergleichs, keine freien Fits.

Der [retardierte Skalarfeld-Benchmark](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/retarded_scalar_interferometer_2026-11-22.md)
liefert getrennt davon eine gemeinsame raeumliche Referenz fuer
Kraft, relative Phase und Kontrast. Fuer kompakte Quellen setzt
die Antwort erst nach Signallaufzeit ein; der Phasenunterschied
waechst spaet exakt linear, waehrend die Vakuum-Dephasierung
bei festem Armabstand einen endlichen Grenzwert hat. Wellengleichung,
Massenkopplung und Quantisierung sind nicht aus Knoten hergeleitet.

Der [Horizontvergleich des Dichtekanals](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/collective_fifo_horizon_response_2026-11-22.md)
zeigt: Kein nichtnegatives Altersprofil baut den kollektiven Anteil
schneller auf als H=1, selbst bei mit der Wellenlaenge wachsendem
Horizont. Endlich beschraenkte signierte Altersfilter aendern
den Ausschluss einer starken akustischen Antwort nicht. Fuer einen
nativen Wellenkandidaten ist ein eigenstaendiger langsamer Strom
im Vektorkanal zu pruefen, nicht eine laengere skalare Liste.

Der [gemeinsame Dichte-/Richtungsabschluss](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/collective_directional_current_2026-11-22.md)
findet diesen zusaetzlichen linearen Modus bei kritischer
Alignment-Staerke; ein fester Zweialter-Block hat gedaempfte
Langwellen. Am selben skalaren Quellport kontrolliert jedoch
derselbe Koeffizient den statischen Nenner und die quadratische
Wellengeschwindigkeit. Ein Pol und eine endliche nichtverschwindende
Wellengeschwindigkeit kommen dort nicht gleichzeitig vor.
Kein nativer Vielteilchen-Grenzwert oder Impulsnachweis.

Die [akkumulierte longitudinale Stromauslese](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/collective_accumulated_current_2026-11-22.md)
rekonstruiert im selben linearen Abschluss einen akustischen
Wellenresolventen mit statischem $1/k^2$-Pol. Das ist eine
neue Auslese, keine Kraft: Der vorhandene stationaere Schritt
ist gegenueber ihrem Gradienten um $O(k^2)$ unterdrueckt.
Auch eine kompakte Richtungsquelle liefert am alten skalaren
Lesekanal keinen Monopolpol. Retention und physikalische
Kopplung der akkumulierten Groesse bleiben offen.

Der [geschlossene Rueckwirkungstest](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/collective_accumulated_feedback_2026-11-23.md)
findet beim eingesetzten anziehenden Kraftport eine Jeans-artige
wachsende Langwellenmode fuer jede feste positive Selbstkopplung.
Zeitverzoegerung mit gleicher statischer Lesestaerke verhindert
das nicht. Eine rueckwirkungsfreie Probe darf deshalb nicht als
stabile Eigendynamik desselben Mediums ausgegeben werden.
Keine neue native Regel und kein allgemeiner Ausschluss von Gravitation.

Der [getrennte Feld-/Materievergleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/collective_medium_matter_split_2026-11-23.md)
findet bei frei diffundierender Materie weiterhin eine wachsende
Langwellenmode, hier mit Rate $k^{2/3}$. Ein gesetzter verankerter
Materialkanal erlaubt gedaempfte Wellen plus statischen $1/k^2$-Pol.
Die Verankerung folgt nicht aus einer inneren Knotenbindung:
Bei massenproportionaler Kopplung bleibt der Monopol am frei
beweglichen Schwerpunkt, waehrend interne Formvariationen erst
in Ordnung $k^2$ sichtbar werden.

Der [neutrale Verbundvergleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/collective_neutral_material_response_2026-11-23.md)
haelt den Schwerpunkt frei und laesst innere Federmoden den
Rueckkanal tragen. Bei Neutralitaet jedes verbundenen Verbunds
koennen gedaempfte Langwellen und ein statischer Fremdquellenpol
ohne aeusseren Anker koexistieren. Ungebundene Gegenladungen
oder ein Netto-Monopol behalten ein positives Translationsresiduum
und damit den wachsenden Zweig. Es ist eine gesetzte
vorzeichenbehaftete Referenz, kein universeller Massenport.

Der [Fernindex geschlossener FIFO-Spuren](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_defect_far_degree_2026-11-23.md)
ist fuer endliche voll affine Spuren mit positiven Gewichten
immer $+1$, auch nach positiver Ueberlagerung mehrerer Spuren.
Ein gemeinsames Feld kann die lokalen Grade $+1/-1$ behalten,
muss aber ausserhalb beider Kerne Restgrad $+1$ tragen.
Diese lokalen Vorzeichen liefern daher nicht die neutrale
Gesamtquelle des Materialvergleichs. Der unnormierte
Gaussfeldfluss verschwindet am Fernrand.

Der [polarisierte Richtungsabschluss](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/collective_polarized_background_2026-11-23.md)
hat oberhalb der Alignment-Schwelle einen homogenen Zweig mit
freier Richtung und kontinuierlich einsetzender Amplitude.
Als eingefrorener Rand kann er die lokalen Grade $+1/-1$ bei
Fernindex null erhalten. Nahe der Schwelle ist der Zweig
jedoch gegen longitudinale Dichtestoerungen instabil, obwohl
die uniforme radiale Mode relaxiert. Kein stabiler nativer Rand.

Der [Langwellenbefund fuer den gesamten polaren Zweig](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/collective_polarized_full_branch_2026-11-23.md)
schliesst den homogenen attraktiven Hintergrund bei jeder
Amplitude aus. In einem Winkelbereich um die Querrichtung
waechst die Dichtemode sogar linear mit dem Wellenbetrag.
Repulsive Achsendaempfung ist nur unter Bedingungen moeglich;
zu grosse skalare Verzoegerung schliesst sie nahe der
Schwelle auf beiden Achsen gleichzeitig aus.

Der [Memory-Generatorabgleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_spin_generator_2026-11-20.md)
zeigt eine exakte Nichtidentifizierbarkeit: Unterschiedliche komplementaere
Rotationen erzeugen dieselbe gesamte Referenzhistorie. Ihr vorhandener
antisymmetrischer Stromtensor hat Rang zwei; eine Hodge-Vervollstaendigung
liefert algebraisch den Referenzgenerator, ist aber keine hergeleitete
dynamische Antwort. Deshalb kein Spinnachweis aus einem einzelnen
720-Grad-Umlauf, auch nicht mit beliebig genauer Bahnmessung.

Der [zusaetzliche Raumnormalblock](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/four_cycle_extra_dimensions_2026-11-20.md)
ist fuer den exakten raeumlichen Vierzyklus analytisch bestimmt:
Pro weiterer Ortsdimension kommen vier Symmetrierichtungen und genau
eine Formmode mit Faktor Bq^3g hinzu. Der Quotient ist die normale
Abweichung zwischen aktuellem und vier Schritte altem Ort. Keine
Periodenverdopplung, Spin- oder Dimensionsselektion; kein positiver
Parametersatz wurde auf dieses neue Stabilitaetskriterium ausgewertet.
Abseits des Orbits skaliert der Koeffizient des aeltesten Vorgaengers
das orientierte Vierervolumen exakt. Nichtentartetes Rauschen treibt
dieses Volumen bei regulaerer 3D-Basis bereits im naechsten Update an.

Der [bedingte orbitale Bindungssatz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_orbital_binding_2026-11-16.md)
verbindet einen kuenftigen strikten Schur-Nachweis mit einer kleinen
vorwaertsinvarianten Umgebung, orbitaler Konvergenz und einem innen
gebundenen regulaeren +1-Defekt. Die Voraussetzung ist fuer keinen
positiven Vertreter belegt. Im vollstaendigen Positionslift behalten
neun Formkoordinaten die aelteste Schrittlaenge; der aktive Abschluss
braucht sie nicht. Acht nichttriviale Multiplikatoren bleiben das
lineare Kriterium. Explizite Feld-/Huellenreserven ergaenzen
den Beweis, ohne einen konkreten dynamischen Radius auszuwerten.
16 neue statische Kontrollen und 469 Tests im betroffenen Panel bestehen,
ebenso Lint und strikter Dokumentationsbau; keine volle Repository-Suite.
Der Literaturabgleich grenzt Fluss- und Diffeomorphismussaetze vom
singulaeren FIFO ab. Kein neuer Ziellauf, stabiler Traegernachweis,
elektrischer Quellenport oder physikalischer Energiebegriff.

Die [begrenzte Stabilitaetspruefung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/flat_memory_stability_preflight_2026-11-16.md)
ist nun mit Quellenbindung, hartem 30-Sekunden-Workerlimit und
verweigertem Zweitstart vorbereitet. 49 neue Kontrollen und 453 Tests
im betroffenen Panel bestehen, ebenso Lint und strikter Dokumentationsbau;
keine vollstaendige Repository-Testsuite. Die neue positive Zielhistorie
wurde nicht ausgewertet und ihr Versuchsordner nicht angelegt.
Nur der alte negative Kontrollorbit, eine Off-Orbit-Abweisung und
synthetische Daten dienen der Methodenpruefung. Ein rigoroser
Produktbetrag ueber eins kann Wachstum belegen; kleinere Werte und
Gleitkomma-Eigenwerte liefern keinen Stabilitaetsnachweis. Freigabe
weiter offen, keine neue Ladungs- oder Teilchenbehauptung.

Der [volle Formquotient](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_shape_quotient_2026-11-16.md)
trennt sechs euklidische Symmetrierichtungen und einen redundanten
Nullanteil von acht verbleibenden Formmoden. Die Produkt- und
Spurbedingungen folgen aus der vollen Historienableitung, nicht
aus einer isolierten Hoehenmode. Gleichzeitige Laengen- und
kompensierte Massennormierungs-Reskalierungen lassen die lokalen
Multiplikatoren unveraendert. Bei fester Geometrie ist hinreichend
rasches Vergessen analytisch instabil; dieser Grenzfall entscheidet
nicht den angefragten innenliegenden hohen-q-Kandidaten. Dessen
Auswertung bleibt geschlossen. Die neuen Methoden werden nur an
Nicht-Orbits, formalen Koeffizienten und dem alten negativen
Kontrollorbit geprueft; kein neuer positiver Stabilitaetsbefund.
15 neue feste Kontrollen und 372 Tests im betroffenen Panel bestehen,
ebenso Lint und strikter Dokumentationsbau; keine vollstaendige
Repository-Testsuite.

Die [abgeflachte Vierphasenfamilie](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/flat_memory_cycle_2026-11-16.md)
erfuellt nun alle nativen Kraftkomponenten mit positivem Alignment
und dem vorhandenen rein attraktiven skalaren Memory. Fuer 0<h<r/2,
H_s=H_v=4 und gleichbreite Gausslesekerne folgen Retention und Gains
analytisch aus den Gleichungen. Es ist eine inverse Existenzkonstruktion,
keine Parameterprognose oder Simulation. Der eindeutige regulaere
+1-Felddefekt bewegt sich exakt mit und liegt fuer ein angegebenes
offenes q-Intervall strikt innerhalb der Memory-Huelle.
21 neue feste Algebra-/Kraft-/Feldkontrollen und 357 Tests im betroffenen
Panel bestehen, ebenso Lint und strikter Dokumentationsbau; keine
vollstaendige Repository-Testsuite. Der regulaere
Tetraeder bleibt vom frueheren Ausschluss betroffen; die neue
abgeflachte Klasse liegt ausserhalb seiner Voraussetzungen.
Volle Formstabilitaet und ein robuster Ladungstraeger sind nicht
nachgewiesen. Ein einmaliger begrenzter Stabilitaetstest ist angefragt,
noch nicht ausgefuehrt. Keine elektrische Quellenwirkung, Gegenladung,
Spin- oder Dimensionsherleitung und keine Aenderung an Paper I.

Die [volle Historienantwort](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_history_response_2026-11-16.md)
variiert jetzt alle Orte und daraus abgeleiteten Einheitsrichtungen
der bestehenden Regel gemeinsam. 36 neue feste Kontrollen und
336 betroffene Tests bestehen, einschliesslich Kernel-Audit; ebenso
Lint und strikter Dokumentationsbau, keine vollstaendige Repository-Testsuite.
Die Achsen-Rueckstellung erlaubt noch keinen skalaren Stabilitaetstest:
Am bekannten negativen-Gain-Vierzyklus ist der Hoehenunterraum selbst
mit axialer Translation unter zwei Schritten nicht invariant, exakt
rational-logarithmisch nachgewiesen. Die allgemeine Ableitung
reproduziert den frueheren vollen Rueckkehroperator; der Kontrollorbit
bleibt instabil. Dieser Ableitungsbericht enthielt keinen neuen Orbit,
Gain-Fit oder Ziellauf. Die Querbilanzen sind nun fuer die oben
genannte Sonderfamilie geloest; ein stabiler gebundener Memory-Traeger
bleibt offen.
Keine elektrische Ladung oder Aenderung an Paper I.

Die [native Zweiphasenbilanz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_two_phase_balance_2026-11-16.md)
liefert jetzt beide Kopfkraefte und einen gemeinsamen axialen
Existenzfilter. Ganze Vektorspeicher-Umlaufperioden besitzen eine
strikt positive Zweimal-zwei-Determinante; der Beweis nutzt die
Gausskernel-Positivitaet und den symmetrisierten Altersoperator.
Positives Alignment allein oder mit ausschliesslich repulsiver
Skalarwirkung kann diese beschraenkte Zweiphasenklasse daher nicht
regenerieren. Die erforderliche gewichtete skalare Rueckstellung hat
eine explizite Untergrenze. Fuer andere endliche Horizonte sind Tail
und Positivitaet separat zu pruefen; ein formales Gegenbeispiel
verhindert den ungeprueften Transfer vom unendlichen Speicher.
21 neue feste Kontrollen und 298 Tests im betroffenen Panel bestehen,
einschliesslich des bekannten negativen-Gain-Vierzyklus; ebenso Lint
und strikter Dokumentationsbau, keine vollstaendige Repository-Testsuite.
Dieser Bilanzbericht enthielt keinen neuen Orbit, Gain-Fit,
Stabilitaetspass oder Zwang zu externen Feldern. Seine notwendige
Achsenhuerde bleibt gueltig; die oben genannte Sonderfamilie erfuellt
nun auch die Querbilanzen, nicht bereits die volle History-Stabilitaet.

Der [FIFO-/Rotationsabgleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_rigid_regeneration_2026-11-16.md)
liefert eine von Gains und Gaussbreite unabhaengige notwendige Huerde: Ein
einzelner gefuellter FIFO mit pro Schritt gemeinsam eigentlich
rotierenden Richtungen traegt in ungerader Dimension keinen regulaeren
Punktdefekt dieses Readouts. Der Alters-Shift erzwingt gleiche
Fixraumprojektionen. Mehrphasige Wiederkehr verlangt mindestens
dim ker(I-Q)+1 zeitliche Klassen; dies sind keine neuen Freiheitsgrade.
Eine quantitative Grenze verbindet beinahe starre Regeneration mit
der Jacobian-Reserve. Fuer zwei Phasen sind nun die beiden nativen
Kopfgleichungen und die Achsenbilanz in jenem Bericht formuliert,
noch ohne Loesung. Der bekannte negative-Gain-Vierzyklus ist eine passende,
weiterhin instabile Gegenkontrolle. Neue Literatur zu stabilen
gerichteten Agentenrotationen ist kein direkter FIFO-Transfer und
verbietet pauschale Alignment-Zerfallsbehauptungen. 27 neue feste
Kontrollen und 277 Tests im betroffenen Panel bestehen, ebenso Lint
und strikter Dokumentationsbau; keine vollstaendige Repository-Testsuite.
Kein stabiler Traeger oder elektrische Ladung.

Der [Defekttransport-/Zeitskalierungsabgleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_defect_transport_2026-11-16.md)
ergaenzt den bisherigen Gesamtgradschutz um ein hinreichendes endliches
Kriterium fuer lokal genau einen regulaeren Defekt nach dem wirklichen Update,
gleichen Index und einen Ortsfehler relativ zum geometrischen
Memory-Schwerpunkt. Noch kein invarianter Historienbereich. Kleine
Bewegungs-Gains allein regularisieren die Einheitsdeposition nicht:
bei festem Gewicht bleibt ein endlicher Sprung am Nullinkrement.
Unter expliziter diffusiver Zeitverfeinerung mit festem Memory-Massstab,
festen Breiten und beschraenktem adaptivem Drift verschwindet der neu
erzeugte Vektorreadout punktweise im L2 mit O(sqrt(h)). Eine beliebige
Anfangshistorie und bewegte Abfrageorte sind gesondert behandelt.
Kein allgemeines Defekt-No-go oder gewaehlter physikalischer Grenzfall;
kleine Amplitude loescht Indizes nicht automatisch. 27 neue feste
Kontrollen und 250 Tests im betroffenen Panel bestehen, ebenso Lint
und strikter Dokumentationsbau; keine vollstaendige Repository-Testsuite.
Keine Zielbahn, neue Regel oder Gain-Anpassung.

Die [volle Kernelpruefung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/nonminimal_kernel_obstruction_2026-11-16.md)
schliesst jetzt auch den festen Zweischalen-Zeugen mit getrenntem
Vergessen aus, fuer a=1,b=5,sigma_vector=1,q=99/100 und Horizonte aus
ganzen Achtperioden. Die beiden vollen Bewegungsbilanzen erzwingen
vier gemeinsame skalare Kraftwerte, die keine reelle Summe aus zwei
Gaussfunktionen annehmen kann. Ein rationales Intervallzertifikat
sichert den Widerspruch; die formale Tabelle wird unabhaengig an
allen acht Phasen gegen den nativen Vektorreadout geprueft, aber
nicht als Kernel installiert. 20 neue Kontrollen und 223 Tests im
betroffenen Panel bestanden, ebenso Lint und strikter Dokumentationsbau;
keine vollstaendige Repository-Testsuite.
Kein Fit, kein Ziellauf und kein pauschales No-go fuer andere
Memory-Strukturen. Der feste Zeuge bleibt ein statisches Beispiel,
kein nativer Orbit; die folgende Retentionsbedingung ist nur notwendig.

Die [native Zweischalenpruefung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/nonminimal_memory_recurrence_2026-11-15.md)
zeigt jetzt eine konkrete dynamische Huerde: Gleiche skalare und
vektorielle Retention und Horizonte aus ganzen Achtperioden erlauben
die starre zweischalige Tetraederfolge nicht, unabhaengig vom konstanten
Vektorgain und radialen skalaren Kernel. Eine Tangentialprojektion
beweist den Ausschluss fuer alle inneren/aeusseren Radien und positiven
Gaussbreiten. Beim festen H=8-Zeugen bleibt in mindestens einer von
zwei Phasen ein Inkrementfehler groesser als 7/3. Getrenntes Vergessen
ist nicht generell ausgeschlossen; fuer denselben geometrischen
Zeugen verlangt bereits die ferne Tangentialbilanz s<1/4000 bei
q=99/100. Kein Existenzpass oder ausgewaehlter Parameter. 27 neue
Kraft-/Algebrakontrollen und 203 Tests im betroffenen Panel bestanden,
ebenso Lint und strikter Dokumentationsbau. Keine vollstaendige
Repository-Testsuite. Keine Zielbahn, kein Gain-Fit,
keine neue Regel; der statische Vorzeichenbeweis bleibt gueltig.

Der [nichtminimale Defektbefund](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/nonminimal_memory_defects_2026-11-15.md)
schliesst die statische Vorzeichenhuerde: Eine feste H=8-Historie aus
nahen und aeusseren Tetraederpositionen hat genau einen regulaeren
-1-Defekt im Radius 1/6, innerhalb der nahen konvexen Memory-Huelle.
Die Richtungen sind aus der Historie abgeleitet, die positiven
Vergessensgewichte unveraendert. Bei gleichen Parametern besitzt eine
andere Historie einen lokalisierten +1-Defekt. Im negativen Kontrollfeld
erzwingt der Aussenrand ausserdem den Gesamtindex +2 im Ringgebiet;
kein neutraler Zweiteilchenzustand und keine bestimmte Zahl aeusserer
Einzeldefekte. Die Beweise nutzen uniforme analytische Schranken samt
rationalen Reserven; 23 neue feste Kontrollen und 176 Tests im
betroffenen Panel bestanden, ebenso Lint und strikter Dokumentationsbau.
Keine vollstaendige Repository-Testsuite. Kein
Nullstellensucher, Ziellauf oder neue Feldregel. Native Regeneration,
volle Formstabilitaet und elektrische Quellenwirkung sind noch offen.

Die [Rekurrenz- und Vorzeichenpruefung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_defect_recurrence_2026-11-14.md)
klassifiziert jetzt den minimalen Readout: d+1 aktive gerichtete
Depositionen in d Dimensionen koennen nur regulaere Defekte mit Index
+1 tragen, auch bei offenen Historien. Der regulaere Tetraeder-Umlauf
scheitert bei nichtnegativem Alignment-Gain an den Existenzgleichungen,
fuer Horizonte aus ganzen Vierperioden. Der vorhandene negative
Vektorgain erlaubt dagegen eine exakte rauschfreie Vierperiode mit
gebundenem Defekt. Ein rational abgesicherter Spurtest beweist jedoch
einen Vier-Schritt-Floquet-Multiplikator vom Betrag groesser als 3.
Die volle History-Variation trennt ihn von Translation und Raumrotation.
23 neue Kontrollen und 153 betroffene Tests bestanden. Keine
Parametersuche, neue Simulationsregel, Zieltrajektorie oder Teilchenidentifikation.

Der [Memory-Defektanschluss](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_defect_charge_2026-11-14.md)
liefert einen lokalen ganzzahligen Index ohne zusaetzliches Materiefeld:
Eine geschlossene Simplex-Historie hat genau eine regulaere +1-Nullstelle
des bestehenden Gauss-Vektorfelds, auch mit positiven nativen
Vergessensgewichten und Einheitsrichtungen. Ein aktiver Alignment-Schritt
kann bei der regulaeren Vierpunkt-Historie jedoch alle Feldnullstellen
entfernen; ein globaler Halbraumbeweis ersetzt die Nullstellensuche.
Notwendige Richtungsumfassung und ein hinreichendes Quellen-/Tail-
Randkriterium sind abgeleitet. Lokale strukturelle Robustheit ist nicht
zeitlicher Schutz; weder elektrische Ladung noch ein Teilchen gewonnen.
Der vorhandene skalare Kanal kann oberhalb einer expliziten Schwelle
nach einem Schritt wieder einen +1-Defekt liefern. Die feste positive
Kontrolle liegt jedoch weit ausserhalb der Memory-Wolke; daraus folgt
keine raeumliche Bindung oder weitergehende Erhaltung.
Keine Simulationsregel geaendert und keine Zieltrajektorie ausgefuehrt.
29 neue konstruierte Kontrollen, 130 betroffene Tests, Lint und strikter
Dokumentationsbau bestanden; keine vollstaendige Repository-Testsuite.

Die [dynamische Fortsetzung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_core_phase_bridge_2026-11-11.md#6-dynamischer-anschluss-normalantwort-und-ladung)
leitet die volle Normalvariation der vorhandenen aktiven Vektormemory
her. Der neue Pruefer veraendert keine Simulationsregel; Ein-Schritt-
Gegenkontrollen erfassen auch die beweglichen gespeicherten Richtungen.
Translations-/Kippmoden werden von Formmoden unterschieden. Die normale
Instabilitaetshuerde ist um den Alignment-Beitrag erweitert, aber kein
neuer Orbit oder Stabilitaetsbefund erzeugt. Die separate Modenintensitaet
hat eine explizite Quellen-/Verlustbilanz und ist nicht allgemein erhalten;
ein exakt auswertbarer aktiver Update aendert sie von 1 auf 1/2.
28 neue Kontrollen, 170 betroffene Tests, Lint und strikter Dokumentationsbau
bestanden. Noch keine Ladung, kein Teilchen und keine neue Zielsimulation.

Auf Autorenentscheidung sind im [Memory-/Kernphasenanschluss](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_core_phase_bridge_2026-11-11.md)
beide Straenge getrennt konkretisiert. Ein komplexer Vektorreadout folgt
aus vorhandenen Displacement-Historien, einschliesslich exakter
FIFO-Randbilanz und bedingter Phasenfehlerkontrolle. Ein expliziter
Historienpfad loest die projizierte Wicklung bei nichtverschwindendem
Gesamtreadout auf; dynamischer Schutz folgt nicht aus mehr Dimensionen.
Der Referenzzweig besitzt nun einen Witten-Wirkungsvertrag mit explizitem
geladenem Kernfeld, globaler Vakuumkontrolle und Kondensationsoperator.
Keine Memory-Herleitung dieser Felder, keine quantisierte Ladung oder
Elektronenidentifikation. 19 neue konstruierte Kontrollen, 103 Tests im
betroffenen Panel bestanden; keine Zieltrajektorien oder Parametersuche.

Die [Fortsetzung zur Mischkopplung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/field_stabilization_channels_2026-11-10.md#6-konkreter-anschluss-mischkopplung-mit-kernstrom)
benennt jetzt einen nichtminimalen Quellenansatz und seinen fehlenden
Kernstrom. Dessen kinematische Vervollstaendigung erhaelt den Gesamtstrom;
unter den angegebenen Rand-/Defektannahmen haengt die Gesamtladung
vom eigenen Kernzustand statt allein von der Verknuepfung ab. Ein glatter
Regulator zeigt, dass Abschneiden der Singularitaet das Problem nicht
loest. Keine gekoppelte Feldloesung oder native Emergenz. Die jetzt
freigegebene Referenzausarbeitung bleibt davon und von Memory getrennt.

Der [Feld-/Quellenabgleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/field_stabilization_channels_2026-11-10.md)
vertieft zwei Literaturvergleiche und liefert einen bedingten analytischen
Test: Ein masseloser Kanal nutzt nur bei nichtverschwindender Kernquellen-
Projektion. Minimale Stroeme ausschliesslich kondensierter Spezies haben
im deklarierten abelschen Higgs-Vergleich keine solche Projektion.
Ein eingefrorenes Selbstfeld kann ausserdem ein falsches Energieminimum
anzeigen. Keine neue Feldregel, Teilchenidentifikation oder Zielsimulation;
der native Kern-/Quellenmechanismus bleibt offen. Die Mischkopplungs-
Fortsetzung ergaenzte 15 Kontrollen auf insgesamt 37 in dieser Testdatei;
70 Tests im damaligen Panel, Lint und strikter Dokumentationsbau bestanden.
Keine Solitonreproduktion und kein neuer Produktionssolver.

Auf Autorenanregung trennt der [datengebundene Benchmark](../reference/hydrogen_benchmark.md#datengebundener-einstieg-statt-freier-parametersuche)
jetzt reale Vergleichswerte, gemeinsame Einheiten und freie Memory-
Zuordnungen. CODATA-Werte und die betreffenden PDG-2026-Abschnitte sind
nachgelesen; wenige Referenzverhaeltnisse wurden arithmetisch umgerechnet.
Keine Teilchenmasse, Feldgleichung oder Schrittzahl daraus hergeleitet.
N als moeglicher Massentraeger ist begrifflich noch offen. Der Vorschlag
eines einzelnen Knotens mit dynamischem Feld ist eine Empfehlung fuer
die naechste Modellentscheidung, kein Elektronenbefund. Die bestehende
AL1-Referenz bleibt getrennt. Der folgende Paarlauf ist vorerst
zurueckgestellt, nicht automatisch freigegeben.

Der [antipodale Methodenauswerter](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/antipodal_pair_method_2026-11-08.md)
trennt jetzt feste Newton-Schritte, einen Krawczyk-Existenznachweis und
den hinreichenden gemeinsamen Normal-Instabilitaetstest. Ein algebraisch
konstruiertes natives H=2-Beispiel besteht die Existenzpruefung, ist aber
normal instabil. 37 neue Methodenchecks bestehen, 166 im betroffenen
Regressionspanel. Keine Stabilitaetsklassifikation, kein neuer Ankerlauf
oder Gain-Scan. Der [konkrete Vorschlag](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/antipodal_pair_attempt_proposal_2026-11-08.md)
enthaelt jetzt einen separat getesteten Einmal-Runner und das explizit
vorgeschlagene additive Gain-Paar 0.15/0.15. 40 neue Runner-Kontrollen
bestehen, einschliesslich echtem kleinen H=2-Worker und gepruefter
Zeitlimit-Prozessbeendigung. Keine Freigabe oder Ausfuehrung; seit dem
2026-11-09 zugunsten der physikalischen Benchmark-Zuordnung zurueckgestellt.

Der [kollektive Stabilitaetsabgleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/collective_memory_stability_2026-11-07.md)
liefert einen exakten bedingten Befund: Deckungsgleiche identische
Historien bei gleicher Zeilensumme behalten die Einzelgleichung samt
gemeinsamer Instabilitaet. Additive Kreuzkopplung veraendert bereits
deren Gesamtstaerke. Phasenversetzte Historien veraendern hingegen die
Kruemmungsgewichte; fuer einen Polygonansatz sind Existenzgleichung,
voller Normalblock und hinreichender Instabilitaetstest hergeleitet.
Die antipodale Spezialisierung trennt zusaetzlich Summen-/Differenzantwort
und vollstaendige mitrotierende ebene Bloecke. Ein hinreichendes
Abklingkriterium fuer den gemeinsamen Normalblock ist bewiesen.
Die anschliessende Kompatibilitaetspruefung zeigt jedoch: Beim identischen
Ankerkernel, $r\theta<6/13$ und hinreichender Historie bis zur naechsten
Halbwendung ist mindestens ein gemeinsamer Koeffizient negativ, fuer
jedes nichtnegative nichttriviale Selbst-/Kreuz-Gain-Paar. Die gespeicherte
Geometrie wurde nur anhand ihrer Parameter zugeordnet. Der einfache
Positivitaetssatz hilft dort nicht; ein signiertes stabiles Gegenpolynom
verhindert den Fehlschluss auf allgemeine Paarinstabilitaet. Rein repulsive
Chordbereiche scheitern bereits an der radialen Existenzgleichung.
54 kleine Kontrollen bestehen, einschliesslich nativer Paarregel fuer
einen konstruierten Schritt, nichtsynchronem Jacobian-Abgleich und
korrekt mitrotierender kompletter Historie.
Keine neue Zielsimulation, keine Stabilitaets-, Teilchen- oder QFT-
Herleitung. Der erweiterte Literaturvergleich mit orbitierenden
Walking-Droplet-Paaren trennt vorgegebene Traegheit, 2D-Untergrund,
Antrieb und semiempirische Auftreffphasenanpassung von nativer
FIFO-Dynamik. Modell-/
Normierungsentscheidung ist beim Autor angefragt, nicht vorweggenommen.

Der [mitlaufende lineare Memory-Vergleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/linear_memory_quantum_closure_2026-11-06.md)
liefert einen exakten Kontrast: Gleiche Gauss-Ortsdichte und gleicher
Strom koennen wegen verschiedener Memory-Varianz verschieden evolvieren.
Die Zuordnung zu derselben reinen skalaren Wellenfunktion schliesst
deshalb nicht auf der ganzen geprueften Praeparationsklasse. Ein anfangs
passender Quanten-Breitenwert ist nicht dynamisch invariant. Alle festen
translationskovarianten linearen Ortsauslesen im stabilen Vergleich
bleiben langfristig diffusiv, auch das Memory-Zentrum. Das ist keine
geschlossene freie Teilchendynamik bei fester Zeit-/Laengenkalibrierung.
18 neue algebraische Kontrollen, kein nichtlinearer FIFO-No-go und keine
neue Zielsimulation. Ein bestandener klassischer Gauss-Schervergleich
zeigt umgekehrt, dass auch passende Breiten allein nicht genuegen.

Der [stochastische Quantenabgleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/stochastic_quantum_bridge_2026-11-06.md)
grenzt den Anschluss an Wasserstoff ab: Native Memory-Spur und
Ensemble-Ortsdichte sind nicht identisch. Die OU-Grundzustandstransformation
liefert Imaginarzeit, nicht von selbst unitaere Echtzeitdynamik. Ein
stationaerer Nelson-Oszillatorvergleich bleibt moeglich; beliebige
OU-Transienten tragen nicht dasselbe Kraftgesetz. Die Ringkontrolle
trennt lokale Gleichung und globalen Phasensektor. 16 neue konstruierte
Kontrollen bestehen; keine neue Zielsimulation oder Quantenherleitung.
Die abgeschlossenen AL1-Archive bestehen erneut ihre elf lesenden
Kontrollen; die bereits verbrauchte Freigabe wurde nicht erneut genutzt.

Die [Umlauf-/Kollektivpruefung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/loop_flux_limits_2026-11-05.md)
liefert einen bedingten positiven Grenzfall: Vorgegebene periodische
Historien werden bei ausreichend langer Memory und kleinem Vergessen
im Linienreadout gleichgewichtet. Kein Nachweis nativer periodischer
Bahnen. Unabhaengige lokalisierte Loops mit dem angegebenen endlichen
Moment haben dagegen eine mit k^2 verschwindende spektrale Amplitude,
nicht die klassische Coulomb-Referenz. Spurnormierung kann diesen
Unterschied verbergen. Keine Aussage gegen kollektive Phasen und
keine neue Modelldynamik oder Zielsimulation.
91 betroffene Tests einschliesslich 12 neuer konstruierter Kontrollen,
Lint und strikter Dokumentationsbau bestehen.

Der [kollektive Ladungsabgleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/collective_charge_constraints_2026-11-05.md)
grenzt eine Alternative zu topologischen Knotenlabels ab: Defekte
lokaler Flussbedingungen. Klassische freie Energie, energetische
Wechselwirkung und quantenmechanische Eichdynamik werden getrennt.
Ein konkreter FIFO-Gegenbefund ist analytisch bestimmt: Auch ein
geschlossener altersgewichteter Linienfluss besitzt im Allgemeinen
innere Quellenreste. Die native Punkt-Vektormemory ist zudem kein
exaktes Linienintegral. Die bedingte Graphminimierung liefert eine
inverse Laplace-Matrix, aber weder automatisch 3D noch Coulomb-Physik
aus Memory. Keine neue Regel, kein Ziellauf oder Quanten-/Ladungsclaim.
79 betroffene Tests einschliesslich 13 neuer algebraischer Kontrollen,
Lint und strikter Dokumentationsbau bestehen.

Der [topologische Zustandsraumabgleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/topological_state_contract_2026-11-04.md)
zeigt an einer alterskonsistenten Hin-und-zurueck-Historie eine exakte
Nullebene des gerichteten Gaussfelds trotz normierter Einzelrichtungen.
Die normierte Feldrichtung besitzt zudem keinen gemeinsamen Fernrand.
Ein globales Hopf-Feld folgt daher nicht automatisch aus diesem Readout.
Der Vergleich mit Hopf-Referenzen trennt Zielraum/Rand, topologisches
Label, Stabilitaet und Quantisierung. Keine Aussage gegen alle moeglichen
Vektormemory-Zustaende und keine neue Feld- oder Normierungsregel.
104 betroffene Tests einschliesslich sechs neuer Gegenkontrollen,
Lint und strikter Dokumentationsbau bestehen.

Die [analytische Grenzfallpruefung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fading_memory_limits_2026-11-04.md)
erweitert den Befund bedingt auf untrunkierte exponentielle Memory:
Bei festem positivem Vergessen und idealem vollrangigem Gaussrauschen
gibt es auf dem angegebenen ganzen Zustandsraum keine nichtkonstante
Wasserstein-2-stetige exakte Invariante fuer alle Starts. Ein unstetiges
Traegerlabel ist ein explizites Gegenbeispiel gegen eine Erweiterung
auf alle messbaren Funktionen. Gemeinsame vorgegebene Schreiborte
sind keine ungezwungene stochastische Synchronisation. Die Grenzen
alpha nach null und H nach unendlich vertauschen fuer die native
Gesamtmasse nicht. Keine Aussage gegen Sektoren auf anderen Raeumen,
keine Richtungswahl und keine Aenderung der Dynamik.

Die [FIFO-Strom-/Invariantenpruefung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_current_invariants_2026-11-04.md)
liefert eine exakte lokale Kontinuitaetsidentitaet einschliesslich des
aeltesten Eintrags. Die volle Memory-Masse ist konstant; der Strom
bleibt um divergenzfreie Anteile unbestimmt. Bei endlichem H, idealem
unabhaengigem vollrangigem Gaussrauschen, endlichem Drift und
uneingeschraenktem Zustandsraum schliesst die positive H-Schritt-Dichte
nichtkonstante, fuer jeden Start fast sicher exakt erhaltene
Zustandsfunktionen aus. Kein Stationaritaets- oder Mischzeitbeweis;
keine Aussage gegen lokale Gegenladungen bei festem Gesamtwert,
Metastabilitaet, unendliche Memory oder andere Grenzfaelle. 19 kleine
Kontrollen sind Softwaretests, nicht der Beweis und keine Zielsimulation.
Ein physikalischer Ladungsmechanismus ist damit nicht gewonnen.

Die [Energie-/Fernfeld-Bestandspruefung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/interaction_structure_inventory_2026-11-02.md)
findet keinen bereits gemeinsamen nativen Ladungsabschluss in den
geprueften Varianten. Sie trennt kurzreichweitige Gaussreadouts,
normierte Relaxations-Diffusionsmemory, Zusatzfelder mit moeglicher
gaploser Antwort und den energiegeschlossenen Gradientenmediator.
Ein Feldpol wird durch Source-/Readout-Gradienten unter Umstaenden
aufgehoben; das Vorzeichen einer eliminierten skalaren Feldenergie
ist nicht automatisch das elektromagnetische. 15 neue kleine
Kontrollen bestehen. Die optional bereits vorhandene Vektormemory-
Rueckkopplung ist in der Theorieuebersicht nun korrekt abgegrenzt.
Keine Dynamik geaendert, kein neues Feld oder Ziellauf eingefuehrt.

Der [Gaussvergleich des nichtlinearen Readouts](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_gaussian_readout_2026-11-02.md)
liefert jetzt den Erwartungswert ueber das ganze feste Fenster mit
Anfangstransient und allen 600 Quellaltern, ohne neue Zielbahn. 17 kleine
Kontrollen bestehen. Der Kontrast liegt bei etwa 1.36e-14, die bisherige
obere Transfer-Fehlerschranke zur nativen Dynamik bei 3.48e-7. Das ist
keine Messung eines grossen Fehlers, erlaubt aber keine native
Vorzeichen-/Amplitudenvorhersage. Nullmittel macht den ungeraden
Gauss-Readout trotz Korrelation exakt blind. Die Vorbereitung eines
kleinen Nachweispanels an diesem Anker wird vorerst geschlossen; kein
Negativbeweis gegen alle anderen Observablen oder Schaetzmethoden.

Die [endliche Bahnschranke](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_path_envelope_2026-11-01.md)
behaelt Nichtlinearitaet und FIFO-Rand im symmetrischen nativen Paar bei.
Fuer die feste Auswertung N=50000, S=0.01, z=10 schliesst die
Nichtaustrittsbedingung numerisch bei 0.008173; 18 neue kleine Tests
bestehen. Die Fehlerwahrscheinlichkeit von etwa 3.5e-14 gilt unter den
Annahmen exakter Arithmetik und idealer unabhaengiger Gaussinnovationen,
nicht als Zertifikat der binary64-/PRNG-Ausfuehrung. Eine korrekt
trunkierte Replikationsstatistik hat ein viel engeres Betragsbudget
von 7.60e-7, aber bei nur zwei disjunkten Paaren weiterhin eine zu breite
Hoeffding-Halbbreite von 1.78e-6. Keine Power oder neue Zielbahn; kein
asymptotischer Stabilitaets-, Bindungs- oder Unabhaengigkeitsnachweis.

Der [Geometrie-/Statistikanschluss](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_geometry_statistics_2026-11-01.md)
liefert eine exakte FIFO-Centerrekonstruktion und trennt lineare von
nichtlinearen Bewegungsfehlern. 16 neue kleine Kontrollen bestehen.
Der zeitgleiche Vergleich unabhaengiger Gesamtlaeufe erlaubt einen
endlichen Erwartungswert ohne Stationaritaet, aber keine automatische
Langzeitdeutung. Die konservative globale Konfidenzhalbbreite von 35.97
bei zwei disjunkten Replikationspaaren und dem alten Kernel ist groesser
als die globale Kontrast-Betragsschranke 15.37. Keine praktische Nachweisstaerke
daraus ableiten und keine fehlenden Zielbahnen nachtraeglich simulieren.

Der [Diagnose-Vorabcheck](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_diagnostic_preflight_2026-10-29.md)
zeigt, dass lineare Mittelwerte auch bei perfekt abhaengigen Quellen dem
Produktvergleich entsprechen koennen. Der neue Auswerter trennt deshalb
lineare und nichtlineare Fensterbeitraege vom lagangepassten Produktkontrast.
14 kleine Kontrollen bestehen. Eine reine Rechnung am alten Anfangs-
checkpoint begrenzt dort den nichtlinearen Feldrest auf etwa 1.3e-7 des
linearen Signals; keine Schranke fuer die spaetere Bahn oder statistische
Power. Das Ausfuehrungsprotokoll ist noch nicht fertig oder freigegeben.

Der [Paararchiv-Audit](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_pair_archive_audit_2026-10-29.md)
zeigt eine konkrete Datenluecke: Die geprueften P3.1/P3.2/500k-Berichte
archivieren keine dichten Einzelbahnen beider Knoten. Anfangscheckpoint,
Seeds oder Plus-/Minus-Responsezweige ersetzen sie nicht. Ein minimaler
FIFO-Datenvertrag und die exakte endliche Fensterkorrektur sind nun mit
neun kleinen Kontrollen geprueft. Keine neue Simulation, kein Replay und
kein negativer physikalischer Befund aus bloss fehlenden Daten.

Die [Paarantwort bei endlichem Abstand](../reference/memory_pair_finite_separation.md)
ist bis zur Formtensor-Korrektur mit expliziter Restschranke bestimmt.
Zehn synthetische Kontrollen bestehen. Unabhaengige stationaere innere
Verteilungen liefern nach deklarierter Kraftnormierung die bekannte
reziproke Wolkenfaltung. Eine stationaere phasengekoppelte Gegenprobe
behaelt dagegen eine mittlere Unwucht; Einzelstationaritaet reicht nicht.
Die zeitversetzten Kreuzkorrelationen und die Centerbewegung ueber die
Memory-Alterslags liefern zu pruefende Beitraege zum Abschlussfehler. Kein Beleg,
dass native gekoppelte Knoten diese Mittelungsannahmen erfuellen; keine
Masse, Bindung, Quantentheorie oder neue Zielsimulation.

Die [native Potentialbilanz](../reference/memory_pair_energy.md) trennt
exakt Bewegung bei alter Historie von Schreiben, Altern und Ausscheiden.
Ein konstruiertes rauschfreies H=2-Beispiel erhoeht das Lesepotential bei
stillstehendem Punkt allein durch den FIFO-Schritt. Es ist deshalb keine
allgemeine erhaltene oder monoton fallende Gesamtenergie. Acht kleine
synthetische Checks pruefen Bilanz, Codezuordnung und Gegenbeispiele.
Das ist weder ein No-go fuer eine Memory-/Mediumsenergie noch ein
physikalischer Arbeits- oder Massennachweis. Die bereits deklarierten
Center-Aktuatoren sind nicht mit der nativen Kopplung gleichgesetzt.

Der [reziproke Kernel-Oszillator](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_kernel_oscillator_energy_2026-11-24.md)
bilanziert Modulationsarbeit und Oszillatorenergie exakt,
laesst den FIFO-Schreibterm aber als separaten Arbeitsposten
offen. Eine native repulsive Zweiplatz-Loesung hat
konstante gespeicherte Energie bei positivem Schreibdurchsatz.
Negative statische Kruemmung im eingefrorenen Vergleich
kann die Oszillatorfrequenz nicht stabilisieren.
Kein Zufallstest und keine physikalische Schreibquelle.

Der [vom Kernel-Oszillator bezahlte Schreibschritt](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_kernel_paid_write_2026-11-24.md)
fuehrt den offenen Arbeitsposten auf eine Energiegrenze
zurueck. Bei ausreichender Anregung behalten feste oder
zufaellig vorgegebene Phasen dieselbe Gesamtenergie.
Das geschlossene ueberdaempfte Budget kann keine
dauerhafte Positionsbewegung finanzieren, und der
FIFO-Schritt verliert weiterhin den alten Eintrag.

Der [reversible FIFO-Traegerschritt](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_reversible_carrier_2026-11-24.md)
haelt den alten Eintrag, uebertraegt Impuls kanonisch und
bilanziert einen erfolgreichen Write durch einen endlichen
Taktimpuls. Ohne passende Traegerpraeparation schreibt er
keine exakte Kopie. Die bedingte Oszillatorflaechenerhaltung
des vorigen Modells hat bei geometrieabhaengiger Arbeit
keinen globalen Lift mit unveraenderter Phase und Geometrie.
Keine hergeleitete Traegerversorgung oder Quantendynamik.

Der [autonome FIFO-Taktvergleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_carrier_clock_cycle_2026-11-24.md)
fuehrt denselben Traeger mit endlicher Energie ohne Reset
zu einer vorbereiteten Zweiperiode zurueck. Fuer jede
ungerade Laenge ab drei ist sie quer instabil. Eine
skalare zentrale Kernel-Modulation kann den wachsenden
Querimpuls nicht aendern, solange sie den kollinearen
Austausch erhaelt und die Register passiv laesst.
Keine Bindung aus Memory und keine native Zieltrajektorie.

Die [Kraft aus dem FIFO-Zentrum](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_memory_center_cycle_2026-11-24.md)
erhaelt die vorbereitete Rueckkehr und aendert die Querantwort
durch einen Gegenimpuls an die Eintraege. Ein konvexes Zentrum
mit positivem Gewicht des juengsten Orts macht den Kopierfehler
exponentiell instabil; beim verbleibenden Dreiplatzfall waechst
er linear trotz Spektrums auf dem Einheitskreis. Die Speicherorte
stehen im Flug weiter still. Keine native Zieltrajektorie.

Der [bewegliche FIFO-Speicher](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_mobile_memory_cycle_2026-11-24.md)
behaelt die vorbereitete Zweiperiode bei endlicher Masse
der Eintraege. Fuer das Zentrum der zwei juengsten Orte
ist sie bei jedem ganzzahligen Frequenzverhaeltnis instabil.
Eine feste Gegenprobe mit gleichen Massen zeigt ebenfalls
einen wachsenden Kopierfehler. Andere nichtganzzahlige
Faelle und nichtkollineare Zyklen bleiben offen.

Der [Ausschluss rotierender Schreibgeometrien](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_rotating_section_2026-11-24.md)
zeigt bei konstanter Halbperiode, dass die Rueckkehr bei
jedem ganzzahligen Frequenzverhaeltnis nur $\pm1$ auf
dem Einheitskreis traegt. Fuer drei Eintraege und gleiche
Massen gilt das auch mit rationaler Fehlerschranke.
Keine periodische Folge von mehr als zwei Schreibpunkten
in diesen Klassen; andere Flugzeiten bleiben offen.

Der [Rangtest fuer veraenderliche Rotorzeiten](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_timing_cycle_2026-11-24.md)
trennt Kopie und Rueckkehr von der schrittweisen
Energiebilanz. Fuer jedes feste ungerade FIFO-Fenster
und jede feste Periodenzahl gibt es bei hinreichend
kurzen Fluegen nur stationaere absolute Rueckkehr.
Bei allgemeinen Zeiten muss eine nichtkollineare
Folge auf einer Ausnahmemenge liegen. Kein Nachweis,
dass die autonome Dynamik diese Menge verfehlt.

Der [Treue-Test fuer die FIFO-Historie](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_faithful_history_2026-11-24.md)
fordert zusaetzlich, dass alle Speicherorte am Schnitt
wirklich fruehere Kopfpositionen sind. Im beweglichen
Ein-Zentrum-Modell gibt es dann fuer jedes Fenster ab
zwei, beliebige nichtnegative Gewichte und variable
Rotorzeiten nur hoechstens zwei Schreiborte auf einer
absolut periodischen oder dauerhaft beschraenkten Bahn.
Die Kopierbedingung allein schliesst Drift nicht aus.

Das [FIFO-Sechseck mit zwei Kraftprofilen](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_two_center_hexagon_2026-11-24.md)
hat im konservativen Referenzmodell sechs treue
Schreibpunkte ohne Reset. Zwei abgestimmte Normalmoden
kehren je Write ganz zurueck. Der Rotor bleibt intern,
die Anfangslage ist vorbereitet. Eine analytische
Spurschranke belegt Querinstabilitaet; keine stabile
Bindung, keine native Zieltrajektorie.

Die [Rueckstellung der freien Speichermode](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_restored_hexagon_2026-11-24.md)
erhaelt das treue Sechseck, wenn diese Mode je Write ganz
zurueckkehrt. Trotz fehlender interner Drift bleibt ein
reeller wachsender Kopierfehler zwischen Faktor $6/5$ und
$5/4$ je Write. Ein notwendiger Phasenausgleich grenzt
weitere Rueckkopplungen ein; kein Stabilitaetspass.

Das [Sechseck mit Impulsumkehr](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_half_turn_hexagon_2026-11-24.md)
nutzt eine andere Speicherrichtung, die nach einer halben
Periode ihren Impuls umkehrt und ihren Ort behaelt.
Treue Historie und autonomer Takt bleiben erhalten.
Das reziproke Polynom beweist Querinstabilitaet fuer
jede positive Speichermasse. Keine native Zieltrajektorie.

Die [Zweiphasen-Kompensation am Sechseck](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_compensated_hexagon_2026-11-24.md)
erhaelt treue Historie und autonomen Takt, obwohl zwei
angeregte Speichermoden ausserhalb ganzer und halber
Perioden zurueckkehren. Beim konstruierten Massenverhaeltnis
$16/9$ beweisen Intervallvorzeichen weiterhin Querwachstum.
Andere Kompensationen bleiben offen, keine native Zieltrajektorie.

Das [linear stabile FIFO-Sechseck](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/fifo_center_free_hexagon_2026-11-24.md)
nutzt die algebraisch schwerpunktsfreie Richtung.
Bei gleichen Massen und Radius $1/25$ zertifizieren
Intervalle beschraenkte innere Stoerungen in der
Ebene und quer, mit Rotorableitung auf fester Energie
und nach Symmetriereduktion. Treue Historie bleibt.
Keine nichtlineare Bindung oder native Knotenbildung.

Die [Memory-Paarreduktion](../reference/memory_pair_reduction.md) liefert
eine exakte Center-Gleichung mit endlichem FIFO-Rand und nichtlinearem
Rest samt Schranke. 14 kleine synthetische Tests bestehen; kein neuer
Ziellauf. Der lokale kontinuierliche Abschluss hat nur bei deklariertem
Kraftport eine Filtertraegheit. Gemeinsame reziproke Paarenergie bindet
ihr Verhaeltnis an $\tau_AW_A/(\tau_BW_B)$; eine physikalische Auswahl
dieses Arbeitsports fehlt. Im attraktiven isotropen Vierzustandsabschluss
bleibt von einer freien komplexen Normalmode nach einer Periode hoechstens
$e^{-2\pi}$ ihrer Amplitude. Diese begrenzte Anwendung einer bekannten
Spektralschranke ist kein No-go fuer die volle nichtlineare FIFO-Dynamik.

Der [gekoppelte Gauss-Solver](../reference/nucleon_spatial_reference.md)
ist implementiert. 27 neue synthetische Methoden-/Runnertests bestehen;
ein 18-Gauss-Preflight reproduziert den exakten 6D-Oszillator samt
Radius- und Spinobservablen. Die Wellenfunktion wird mitarchiviert.
Dieser synthetische Test ist kein AL1-Nukleonlauf. Die anschliessend
ausdruecklich genehmigten zwei begrenzten Referenzlaeufe sind nun
[abgeschlossen und archiviert](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/nucleon_al1_attempt1_2026-10-28.md):
je etwa 20.4 s, drei feste Basisstufen, zwei Cutoffs, keine Anpassung oder
Wiederholung. Beide endlichen Konsistenz-Passes liefern 930.733 MeV fuer
N und 1242.106 MeV fuer Delta. Das ist kein Kontinuumszertifikat.
Die $v^2$-Proxies 1.752 und 1.179 warnen vor der nichtrelativistischen
Naeherung; das Nukleon-Momentenverhaeltnis -0.660540 liegt um 3.568 Prozent
vom dokumentierten Messvergleich entfernt. Die allgemeine physikalische
Validierung und der Memory-Anschluss bleiben offen. Freigabe verbraucht.

Die [raeumliche Nukleonreferenz](../reference/nucleon_spatial_reference.md)
ist als AL1-Methodenvertrag spezifiziert. Eine analytische Restidentitaet
und 17 synthetische Tests zeigen: Der bisherige feste Spin-/Flavoranteil
ist bei ungleichen Hyperfeinkoeffizienten kein abgeschlossener Ansatz.
Der statische DeepQuark-Codeabgleich identifiziert im gelesenen Baryonpfad
einen gegenueber dem Artikel fehlenden konstanten Term von -64.63 MeV.
Dies ist keine Widerlegung der publizierten Zahlen; die Energiekonvention
muss bei einer Reproduktion abgeglichen werden. Dieser statische
Operatortest ist selbst keine raeumliche Simulation; der oben getrennt
berichtete Ziellauf verwendet den vollstaendigen deklarierten Offset.
Beides liefert keinen emergenten Massennachweis und keine Memory-Aussage.

Der Autor hat den [QCD-/QFT-Referenzzweig](../reference/matter_reference_contract.md)
ausdruecklich getrennt vom Emergenznachweis freigegeben. Die erste
Quark-Zustandskontrolle ist ausgefuehrt: Ladungen, gewaehlter Spin-$1/2$-
Sektor, Farbsingulett und bekannte magnetische Spin-Gewichte stimmen.
Zwoelf Softwaretests bestehen. Das einfache Momentenverhaeltnis $-2/3$
weicht um etwa 2.67 Prozent vom dokumentierten Messvergleich ab, ohne
Nachfit. Keine raeumliche Quarkbindung, keine Gitter-QCD, keine Masse,
kein Elektronenfeld und keine Memory-Emergenz wurden damit simuliert.

Der neue [Wasserstoff-Zielbenchmark](../reference/hydrogen_benchmark.md)
enthaelt gemeinsam Massenverhaeltnis, Ladung, Spin, magnetische Momente,
Bindung und Spektroskopie sowie die Hypothesen Knotengroesse/Traegheit und
FIFO/Spin. Er trennt gesetzte Inputs, unabhaengige Messgroessen und
Vorhersagen. Das ist eine Zieldefinition mit Quellenvergleich, kein neuer
Stabilitaets-, Teilchen- oder Quantenbefund und keine Ausfuehrungsfreigabe.
Die Autorenpraezisierung ordnet ihn Paper III zu: 3D meint die effektive
aeussere Wechselwirkungsbeschreibung, nicht eine Beschraenkung der inneren
Knoten-/Memory-Struktur. Neutron/Betazerfall ist als spaeterer Konsistenztest
ergaenzt, nicht als Deutung einer vorhandenen Instabilitaet.

Der [direkte Paar-Audit](../reference/hydrogen_pair_audit.md) ist
abgeschlossen. Er zeigt fuer die gepruefte Regel: beidseitiges Auslesen
gleicht allgemeine Historien nicht automatisch aus; feste Gauss-Readouts
lokalisierter Quellen haben keinen asymptotischen Coulomb-Schwanz; eine
reine 3D-Projektion kann verborgene Zustandsabhaengigkeit behalten.
16 kleine synthetische Checks pruefen Codezuordnung und Gegenbeispiele.
Das sind begrenzte Strukturaussagen, keine Zielsimulation, keine gemessene
Masse und kein allgemeines No-go fuer kollektive effektive Felder.

Die [Forschungsroadmap](research_roadmap.md) trennt das langfristige Ziel
von den offenen Verbindungen zu effektiver Dynamik, Quantenmechanik und
Gravitation. Der begrenzte [R0-Audit](../reference/foundation_feasibility.md)
ist dokumentiert: raeumliche Kreisphase, nichtkompakter direkter Gauss-Readout
und bedingte klassische Korrelationsgrenzen. Zwoelf synthetische Checks
pruefen die engen Aussagen und Gegenbeispiele gegen Ueberinterpretation.
Das ist kein allgemeines Go oder No-go fuer das Fernziel und keine neue
Produktions- oder FIFO-/P5-Evidenz. Die
[B1-Bestandsanalyse](../reference/operational_contract.md) spezifiziert
Zustand, Quellenvariation, Ein-Schritt-Antwort und bedingte Verteilung des
vorhandenen Frozen-Source-Zweigs. Fuenf neue synthetische Checks pruefen
seine Zuordnung zur Implementierung. Ein physikalischer Zwei-Stationen-
Vertrag mit begruendeter Wahl oder Herleitung des Mehrsystemgesetzes,
Aktuatoren und Detektoren fehlt weiter. Mathematisch definierte Paarkopplungen
existieren; ihre physikalische Auswahl folgt nicht aus dem analytischen Abschluss.

Die [FIFO-Strukturanalyse](../reference/fifo_structure_candidate.md)
identifiziert als begrenzten Arbeitskandidaten eine altersgeordnete
Memory-Schleife mit abgeleitetem Orientierungsrahmen. In gewaehltem 3D
sind die beiden ebenen Drehsinne durch eigentliche Rotation verbunden;
die $\mathbb Z_2$-Wegklassen des nichtentarteten Rahmenbereichs sind keine
zwei Teilchentypen. Im vollen FIFO-Raum laesst sich die Rotationsschleife
ueber erlaubte Rahmenentartungen kontrahieren. Ein separat hergeleiteter
Normalblock macht die gesondert zu pruefende Stabilitaet gegen Auslenkungen aus
der Ebene explizit. 26 kleine synthetische Checks bestehen, einschliesslich
einer kollapsfreien Kontraktion der Rahmenrotation in 4D. Diese synthetischen
Checks sind keine Zielmessung, geschuetzte topologische Ladung oder Wechselwirkungsidentifikation.

Der anschliessende
[Normalstabilitaets-Methodenvertrag](../reference/fifo_normal_stability_contract.md)
reduziert die offene lineare Frage auf den vollstaendigen Formquotienten
nach genau drei normalen Symmetriemoden. Ein Intervallprototyp der bekannten
Schur-Rekursion unterscheidet strikte Stabilitaet, Nicht-Striktheit und
Unentschiedenheit an synthetischen Kontrollen. Zusatzmoden nahe eins bleiben
erhalten; transiente Verstaerkung bleibt von asymptotischem Abklingen
getrennt. Die Rootbox-Anbindung ist jetzt mit frischer Krawczyk-Pruefung
und direkter Weitergabe binaerer Intervallgrenzen implementiert. 23 neue
Kontrollen umfassen konstruierte H=4-Roots mit abklingender und wachsender
Normalmode sowie den Produktionskernel. Der begrenzte H=1200-Ankertest
wurde nach ausdruecklicher Autorenfreigabe samt festen schraegen Stoerungen
einmalig ausgefuehrt. Die
[Auswertung mit Kurven und Rohdaten](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25/analysis.md)
trennt zwei Ergebnisse: Beide frischen Rootzertifikate bestehen, aber die
80-/120-dps-Normaltests bleiben durch Intervallaufweitung unentschieden.
Die zehn float64-Arme ueber 2000 Updates zeigen Abklingen bei 0 Grad
(Endfaktor etwa 0.000462) und starke Formverstaerkung bei 30/45/60/90 Grad
(Endfaktoren etwa 1206/1705/2087/2409). Die ungestoerte Form driftet nur
um maximal abgetastet 2.09e-15. Das ist ein deutlicher begrenzter
Wachstumsbefund, noch kein asymptotischer Instabilitaetsbeweis und kein
allgemeiner 3D-Stabilitaetspass. Es gab keinen Timeout oder weiteren Versuch.
Vor Ausfuehrung bestanden 229 betroffene lokale Regressionstests,
einschliesslich 56 Runner-/Stoerungskontrollen, Lint, strikter
Dokumentationsbau und die vollstaendige GitHub-CI. Diese Softwaretests
enthalten selbst keine Zielauswertung. Die Versuchsgenehmigung ist verbraucht.

Die danach separat angeforderte
[120-Grad-Symmetriekontrolle](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_oblique_120_control_2026-10-25/report.md)
ist ebenfalls abgeschlossen. Beide neuen 120-Grad-Arme stimmen mit den
gespeicherten 60-Grad-Armen bei entgegengesetztem Gesamtvorzeichen an
allen 201 Abtastpunkten ueberein; die groesste absolute Formdistanzdifferenz
betraegt etwa 1.01e-16. Das plausibilisiert Code und Modellsymmetrie, nicht
allgemeine Stabilitaet oder reale Physik. Kein weiterer Normalzertifikatslauf.

Abschnitt 6 des [Methodenvertrags](../reference/fifo_normal_stability_contract.md)
enthaelt nun einen elementaren hinreichenden Vorzeichenbeleg fuer eine
reelle wachsende Normalmode, samt 20 synthetischen Gegenkontrollen.
Die danach separat freigegebene
[Archivauswertung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_archived_normal_slope_2026-10-26/report.md)
belegt jetzt in beiden 80-/120-dps-Datensaetzen strikt
$S\approx-0.3276456990433840337505836<0$ mit ueberlappenden exakten
rationalen Intervallen. Damit existiert am unveraenderten H=1200-Kreis
eine reelle Normalformmode mit Multiplikator groesser als eins. Dieser
Kreis ist kein linear stabiler 3D-Baustein. Der Beleg uebernimmt die
urspruengliche Root-/Koeffizienten-Vertrauensbasis; es gab keine neue
Simulation oder Rootrechnung. Je ein Lauf dauerte 1.531/1.516 Sekunden;
198 lokale Tests, Lint und Dokumentationsbau bestanden vor Ausfuehrung.
Keine Wiederholung, Freigabe verbraucht. Andere FIFO-Strukturen und die
nichtlineare Folgeentwicklung sind dadurch nicht entschieden.

Die anschliessende [starre Strukturpruefung](../reference/fifo_rigid_structure_limits.md)
liefert ohne neue Zielauswertung weitere Grenzen: Ein deterministischer
FIFO-Fixpunkt ist kollabiert; starre relative Gleichgewichte in 3D sind
Punkt, Gerade, Kreis oder Helix. Fuer eine Helix muessen radiale,
tangentiale und axiale Selbstkonsistenz gleichzeitig gelten. Ihr axialer
Grenzwert ist genau $S$; daher gibt es am aktuellen Kreis keine beliebig
nahe Helixfortsetzung. Eine endliche Helix koennte geometrisch haendig sein,
waere aber weder geschuetzter Bahnknoten noch bereits stabiler Baustein.
Die Einschraenkung betrifft nur starre Einzelbahnen in 3D, nicht
kugel-/torusartige Memory-Verteilungen oder hoehere Dimensionen.
Ein expliziter 4D-Zweiebenenansatz zeigt die groessere Klasse bereits
kinematisch; ein eigener Zielroot fehlt.
Die Literaturabgrenzung zu klassischem Delay-Antrieb und Schraubenbewegung
ist mit gelesenen Primaerquellen dokumentiert. 28 neue synthetische
Kontrollen pruefen die Gleichungen und die Grenzen ihrer Reichweite.

Eine getrennte [Paper-I-Forschungsnotiz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/finite_memory_stationarity_2026-10-21.md)
begruendet fuer festes endliches $H$ und positives Gaussrauschen eine
eindeutige relative stationaere Verteilung des beschraenkten nichtlinearen
Drifts. Die Schranke ist nicht uniform fuer verschwindendes Rauschen oder
wachsenden Horizont. Ein exaktes Zweierzyklus-Gegenbeispiel verhindert,
lokale Stabilitaet mit globaler Branch-Selektion gleichzusetzen. Dies sind
analytische Forschungsbefunde, keine neue Radius- oder Transportevidenz.
Eine Ergaenzung derselben Notiz nutzt positive Mittelung, um stationaere
quadratische Momente bis Ordnung $\varepsilon^4$ mit Rest
$O(\varepsilon^6)$ bei festem endlichem $H$ zu begruenden. Alle archivierten
Modellkoeffizienten erfuellen diese zusaetzlichen Voraussetzungen; die
enormen Fehlerkonstanten bestaetigen weder das vorhandene endliche Rauschen
noch praktische Durchmischung, Transport oder den unendlichen Horizont.
Die anschliessende
[Kontraktionsnotiz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/weak_noise_validity_2026-10-21.md)
begruendet die stationaere Momententwicklung unter einer strengeren
globalen Bedingung auch fuer ungekuerztes exponentielles Gedaechtnis.
Alle aktiven archivierten Zellen liegen ausserhalb dieses hinreichenden
Bereichs; das beweist keine Instabilitaet. Ein zusaetzlicher summierbarer
Restterm begruendet nun auch die nichtlineare Transportkorrektur in diesem
engen Bereich, einschliesslich eines expliziten ungekuerzten Koeffizienten.
Numerische Transportvalidierung, Publikationsneuheit, die allgemeine
Gueltigkeit und der separate FIFO-Horizonttransfer bleiben offen.

Update 2026-10-22: Ein externes Zweitmodellreview hat einen konkreten
Transporttest vorgeschlagen. Der
[reproduzierbare Gegencheck](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/external_review_audit_2026-10-22.md)
bestaetigt dessen unendliche Koeffizienten, nicht die Panelreife:
Block-MSD bei Lag 100 und Langzeittransport sind verschieden; der
lineare Bias betraegt 37.17%. Korrekte unabhaengige Gaussreferenz-Skalierung
ergibt etwa 2.32 statt 13.5 Standardabweichungen. Eine anschliessende
[gepaarte Referenzrechnung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paired_transport_feasibility_2026-10-22.md)
kontrolliert den fuehrenden Endlichzeitbias mit einer Zweilaengen-Korrektur
und berechnet die Langblock-Varianz inklusive kubischem Gauss-Chaos.
Die anschliessende
[finite-Stichproben-Rechnung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/finite_block_transport_bound_2026-10-22.md)
begrenzt Sampling plus Blockbias fuer den fuehrenden Koeffizienten beim
diskutierten Budget auf einen konservativen relativen 95%-Radius unter
8.8%. Dies ist eine analytische Referenzrechnung in Gleitkommaarithmetik,
keine Daten-Konfidenz oder Fehlergarantie fuer endliches Rauschen.
Die [Fortsetzung vom 2026-10-23](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/finite_noise_transport_budget_2026-10-23.md)
liefert explizite Schranken fuer zufaelligen Schaetzerrest, Transportrest
und einen vollstaendig vorgefuellten flachen Start. Ein illustratives
10%-Gesamtbudget bei 95% Ueberdeckung ist in exakter Arithmetik fuer einen
sehr kleinen Rauschbereich hinreichend kontrolliert. Am oberen Rand
$\varepsilon\simeq4.46\,10^{-6}$ betraegt der fuehrende Kontrast nur
etwa $9.54\,10^{-10}$ des linearen Beitrags. Die Gleitkommaauswertung
ist kein Intervallzertifikat und bestaetigt weder die fruehere Rauschwahl
$0.007$ noch den bisherigen leeren Speicherstart. Die numerische
Differenzdarstellung wurde anschliessend als
[exakte skalierte Restrekursion](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paired_residual_precision_2026-10-23.md)
geprueft: Kleine deterministische Historien und ein H=600-Ein-Schritt-Test
stimmen mit direkten 80-/110-stelligen Vollkraftrechnungen ueberein.
Das ist keine Langlaufgarantie. Der reine Referenz-Mikrobenchmark misst
etwa 0.261 ms pro Paarupdate; naive serielle Hochrechnung ergibt rund
145 Stunden fuer die diskutierte Paarzahl, ohne RNG/Statistik/I/O.
Die [bedingte Fehlerfortpflanzung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paired_error_propagation_2026-10-23.md)
liefert inzwischen zeituniforme Zustandsschranken fuer vorgegebene lokale
Defekte und Laggrenzen sowie eine separat begrenzte skalare Mittelung.
Die benoetigten lokalen Fehlergrenzen des Simulators und dessen gesamte
Statistik-/Innovationsschnittstelle bleiben unvalidiert. Eine
[Entscheidungsvorlage fuer die fachliche Diskussion](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paper_i_decision_brief_2026-10-23.md)
fasst Resultatkandidat, Literaturabgrenzung und Aufwand zusammen. Sie ist
kein Fachreview und wurde nicht versendet. Praktische Kostenentscheidung,
Neuheitsvergleich und unabhaengiges Fachreview bleiben offen. Keine neue
Zielsimulation oder Panelautorisierung.

Der [Neuheits-Gegencheck vom 2026-10-24](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/gaussian_projection_audit_2026-10-24.md)
zeigt nun eine konkrete Identitaet: Bekannte statistische Linearisierung
reproduziert den gesamten ersten nichtlinearen Transportkoeffizienten.
Ein kubischer Rest mit nichtverschwindender Varianz bleibt dabei erhalten;
dies ist keine exakte lineare Reduktion und kein Nachweis einer gaussverteilten
nichtlinearen stationaeren Dynamik. Der moegliche
Publikationsbeitrag liegt damit in der kontrollierten Gueltigkeit, deren
Abgrenzung gegen rigorose Naeherungstheorie offen bleibt. 32 neue
deterministische Integral-/Matrix-/Projektionschecks bestehen; keine
Zieltrajektorien oder neue Physikevidenz.

Der anschliessende [Satzvergleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/linear_response_scope_audit_2026-10-24.md)
weist eine direkte Totalvariations-Anwendung auf den vollen Historienraum
zurueck, ohne der vorhandenen metrischen Kontraktion zu widersprechen.
Die ergaenzte direkte Poissonrechnung kontrolliert nun intern die
konkreten Observablen, den Korrelations-Resolvent und den Transportrest
uniform im Horizont. Sie behauptet keinen allgemeinen Satzimport und
keine Erweiterung des Gueltigkeitsbereichs. 14 neue synthetische
Matrix-/Quadraturchecks bestaetigen die getrennten Verteilungs- und
Korrelationsbeitraege zum Koeffizienten. Dies staerkt die Einordnung als
Anwendung bekannter Methoden, nicht die Behauptung eines neuen Mechanismus.
Unabhaengige Beweispruefung und Publikationsbewertung bleiben offen.

Der gelieferte [Aging-Volltext](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/aging_full_text_comparison_2026-10-25.md)
ist nun auf Modellebene abgeglichen. Die ungekuerzte lineare Regel ist
nach Parameter- und Startzuordnung exakt das Euler-Schema des Preprints;
sein kontinuierlicher Transportkoeffizient folgt im passend skalierten
Zeitschrittgrenzwert. Zwanzig neue deterministische Checks pruefen diese
Zuordnung, Resolvent und Koeffizienten sowie konkrete Inkonsistenzen der
gelieferten Fassung. Der Preprint behandelt keine nichtlineare
Schwachrauschkorrektur. Das schliesst die Zugriffsluecke, nicht die breitere
Neuheitsfrage oder den fehlenden fundamentalen Anschluss.

| Bereich | Reviewed Befund | Belastbare Lesart |
| --- | --- | --- |
| Paper 0 | technischer Anker | mathematischer Ausgangspunkt |
| Paper I, skalar | kontrollierte co-moving Relaxationswolke; observable-gematchter terminaler RMS-Vergleich | reproduzierbare Baseline, noch nicht PRE-einreichungsreif; Wolkenradius: 0.076% mediane / 0.984% maximale aktive Abweichung, 85 Seed-Traces; Transportvorhersage nicht numerisch validiert, nichtlineare Neuheit offen |
| Native Rotation | sechs lokal eindeutige finite-$H$-Roots; G5 besteht direkte Root-, Spektral- und Nichtlinearitaetsgates bei $H=2400$ | lokale numerische Stabilitaet des vorbereiteten Orbits, keine globale Eindeutigkeit, $H\to\infty$-Stabilitaet oder generische Formation |
| P4-R-S | `p4rs-anchor-scale-transfer-pass` | Zwei-Zellen-Skalentransfer, keine Replikation |
| N0 | `n0-noise-stability-window-bracketed-reviewed-pass` | endliche numerische Robustheitsklammer, keine Planck-Kalibrierung |
| P5-D | `p5d-inconclusive`; drei eigene Produktionsaufrufe technisch verbraucht | keine Interaktionsevidenz; der separate G5-Pass ist ein Single-Loop-Stabilitaetsbefund und keine P5-D-Aussage |
| Source-Audit | `referee-source-ready-with-major-claim-restrictions` | publication source mit offenen Hardening-Auflagen |

## Was der Kreisnachweis genau sagt

Fuer den Anchor mit
`alpha=0.01`, `H=1200`, `eta=0.15`, `A_att=3.5` reduziert das Einsetzen von
$x_n=R e^{in\theta}$ die unveraenderte Grundgleichung exakt auf zwei endliche
Balancesummen. Ein prospektiver Krawczyk-Test schliesst in seinem registrierten
lokalen Kasten genau einen Root ein. Die direkte 2400-dimensionale
mitrotierende Voll-FIFO-Map reproduziert die vorbereitete Historie mit
maximalem Komponentenfehler $2.46\times10^{-15}$; lokale Stoerungen
kontrahieren numerisch. Am spaeteren L3-Kandidaten erreichen zudem zehn
registrierte nichtkreisfoermige Arme den zugehoerigen Orbit.

Fuer diesen vorbereiteten Rotating-wave-FIFO wurde kein KnotScore erhoben.
Das ist derzeit keine fehlende Erfolgszahl: KnotScore v0.5/v0.6 bewertet
kontrollierte Metastabilitaet, Residence und Shape-Stationaritaet, waehrend
Root-, Stabilitaets- und Attraction-Panels eine vorbereitete Kreisloesung
testen. Eine zulaessige gemeinsame Score-/Formationauswertung braeuchte
deshalb ein eigenes prospektives Design mit `eta_zero`-Kontrolle; die
Einordnung steht im
[Experimentkatalog](../reference/experiment_catalog.md).

Das ist der fuer P5 benoetigte kandidatenbezogene Existenz- und
Identitaetsnachweis. Es ist kein globaler Einzigkeitsbeweis: $+\theta$ und
$-\theta$ sind Chiralitaetspartner, globale Rotationen parametrisieren
dieselbe ambiente $SO(2)$-Gruppenbahn, und weitere entfernte Roots sind nicht
ausgeschlossen. P5 darf deshalb einen fest registrierten Kreis als Input
verwenden, aber nicht behaupten, die Parameter erzeugten global nur einen
Kreis.

Der FIFO ist dabei nur eine endliche Alterswarteschlange und schreibt keine
raeumliche Ringtopologie vor. Krawczyk-Balancen, der kollabierende
$\eta=0$-Arm und zehn anziehende nichtkreisfoermige P3-Historien widerlegen
die enge Ringspeicher-Tautologie. Offen bleibt der staerkere Transfer: Die
registrierte Leiter haelt $H\alpha=12$ fest und zeigt nicht, dass Root und
Stabilitaet bei festem $\alpha$ den Grenzfall $H\to\infty$ erreichen. Deshalb
steht vor einer neuen P5-Zielautorisierung ein separates Horizontgate.

Dieses Gate ist inzwischen prospektiv spezifiziert. Es haelt
$\alpha=0.01$, $\eta=0.15$, $M_0$, Kernel und $\varepsilon=0$ fest, trennt
die Vorwaertsleiter bis $H=3600$ von der unteren $H=900,600$-Belastung und
fordert einen Tail-Krawczyk-Einschluss fuer den lokalen Root von
$F_\infty$. Ein negatives Review fand sechs Luecken einschliesslich eines
konstruktiv falschen binary64-Vergleichs; die Amendierung schliesst sie. Das
Suffizienzurteil lautet
`rotating-wave-horizon-transfer-protocol-sufficient-implementation-closed`.
Ergebnisvertrag und rote targetfreie Tests wurden danach getrennt committed;
die kleinste Infrastruktur bestand 40 fokussierte und 985 gesamte Tests. Das
Infrastruktururteil lautet
`rotating-wave-horizon-transfer-contract-infrastructure-pass-runner-incomplete-horizon-run-closed`.
Ein nachfolgendes Negativreview zeigte, dass v1 mehrere registrierte
Abbruchpfade nicht wahrheitsgetreu serialisieren konnte; v2 schloss diese
Nullsemantik. Ein weiteres Negativreview zeigte jedoch, dass positive
Zertifikats-, Spektral- und Trajektorienbeziehungen noch nicht vollstaendig
rekonstruierbar waren. v3 schliesst diese Luecken. Eine erste Linux-CI
falsifizierte dabei native `sin`-/`cos`-Starts als plattformunabhaengig; die
vor jedem Zielzugriff amendierte portable LCG-Konstruktion besteht 59
fokussierte und 1004 gesamte Tests sowie die exakte Linux-CI. Das
Reviewurteil ist
`rotating-wave-horizon-transfer-contract-v3-pass-runner-red-open-target-closed`.
Die anschliessende pure Orchestrierung bestand ihre Stopptests. Ein neuer
Counterexample zeigte jedoch, dass ein einzelnes ausgeschlossenes Halbblatt
als vollstaendige lokale Ausschlussdomain akzeptiert wurde. Validator und
Auditor rekonstruieren deshalb nun unabhaengig Rootbindung, deterministische
dyadische Leafpfade, Praefixfreiheit und vollstaendige Bedeckung. Eine
vollstaendige Ausschlusspartition bei gleichzeitig zertifiziertem Zielroot
wird als Widerspruch verworfen. 70 fokussierte und 1015 gesamte Tests sowie
die exakte Linux-CI sind gruen. Der anschliessende Backend-Bestandsaudit
korrigiert die pauschale Fehlstellenbeschreibung: finite Residuen/Jacobians,
Punkt-Newton, lokale Krawczyk-Boxen sowie FIFO-Map/Jacobian und
Quotientdistanz sind als Bibliothekskerne vorhanden. Der finite-Rootadapter
nutzt den bestehenden Acht-Schritt-Newton-/Krawczyk-Kern. Der anschliessende
Homotopieadapter erweitert denselben Intervallkern auf volle geschlossene
Parameterscheiben und erzwingt 64 Scheiben, strikten Einschluss,
Nachbarueberlappung sowie fail-closed Praefixstopps. Seine CI besteht 1029
Tests; keine registrierte Horizontkante wurde ausgewertet. Der lokale
Ausschlussadapter verwendet denselben Residual-/Krawczyk-Kern und bildet die
feste normalisierte FIFO-Teilung bis Tiefe 20 in den rekonstruierten v3-Record
ab. Er wurde nur an kontrollierten Antworten getestet; keine registrierte
Domain ist ausgeschlossen oder als Rootdomain klassifiziert. Seine
FIFO-kuratierte Implementierungs-CI besteht 1038 Tests. Das anschliessende
Tailzertifikat erweitert das endliche Residuum und beide Jacobi-Spalten um
die registrierten analytischen Normbounds und verwendet danach denselben
outward-rounded Krawczyk-Kern. Null-Tail-Reproduktion, Intervallerweiterung,
Typfehler und Nichtinklusion sind targetfrei getestet. Das damalige
Reviewurteil lautete
`horizon-tail-krawczyk-adapter-target-free-pass-g4-unmeasured`: Zu diesem
Zeitpunkt war kein $H=3600$-Kandidat eingesetzt worden. Offen sind
LCG-Arnoldi, Trajektorienabbildung und Backendkomposition. Die explizite
Nutzerfreigabe vom 2026-09-13 zog einen isolierten G4-Komponentenlauf vor.
Nach gruenem Readiness-Commit und exakter CI startete dieser genau einmal,
brach aber bei der nachgeschalteten Recordvalidierung an einer unzulaessig
exakten Kontrolle der outward-gerundeten aeusseren Box ab. Der Codepfad
rief zuvor mindestens das erste Tailpanel auf; mangels publiziertem Record
ist weder Panelpass noch -fail verwertbar. Ergebnisartefakte und
unabhaengiger Ergebnisaudit entstanden nicht. Der Ausgang ist
`g4-experiment-invalid-outward-box-validation`, nicht G4-Fail.
Die Boxpruefung ist targetfrei auf garantierte Umschliessung plus eng
praezisionsgebundenen Serialisierungsueberschuss korrigiert. Der separat
preregistrierte Retry auf Commit `fb1cc7d` besteht anschliessend beide
strikten 120/160-dps-Tailpanels; ihre Krawczyk-Bilder ueberlappen. Der
Standardbibliothek-Auditor rekonstruiert alle acht Checks und urteilt
`g4-independent-audit-agrees`. Damit ist G4 als isolierte lokale
$F_\infty$-Komponente `pass`. Die G1--G3-Branchverbindung, der
vollstaendige Horizontlauf und P5-D bleiben nicht belegt.

Das anschliessende G4-zu-G5-Meta-Review bestaetigt diese enge Claimgrenze und
findet keinen neuen kritischen G4-Defekt. Die daraus abgeleiteten
LCG-Arnoldi- und Trajektorienadapter bestehen targetfrei: der LCG-Start wird
unveraendert an ARPACK weitergegeben, Ritzvektoren werden v3-konform
gespeichert, Fehler behalten Nullsuffixe, und Instabilitaet verlangt nun das
tatsaechlich gematchte Paar beider Panels. Fortsetzungen bleiben bis zu
vollstaendigen Residual-, Symmetrie-, Panel- und Hashchecks geschlossen.
Der anschliessende Grundgleichungs-Preflight bindet ausserdem $q$, $H$,
$M_0$, $\eta$, Depositionsgewicht, direkte Gewichtssumme, native
Kreiskovarianz, mitrotierenden Fixpunkt, Voll-Jacobian und Symmetrien an
einen kanonisch hashbaren Record. Er bestaetigt targetfrei die beabsichtigte
Architektur: Nur Arnoldi ist linearisiert; die Stoerungsarme iterieren die
nichtlineare Voll-FIFO-Grundgleichung. Nach zwei getrennten
Publikationsincidents schloss Attempt 3 die Recordluecke mit einer dichten
Vollschrittspur. Der einmalige Ziellauf besteht beide Arnoldi-Panels und alle
drei nichtlinearen Stoerungsarme; der unabhaengige Auditor rekonstruiert
Record, Entscheidung und Publikationshashes. Das Ergebnis lautet
`g5-local-direct-stability-pass` fuer exakt $H=2400$. Dies ist kein
Intervallbeweis des vollen Spektrums und keine Aussage ueber
$H\to\infty$, Formation oder Interaktion.

## P5-D Code-Review und Remediation

Das Review trennte eine algebraisch konsistente Center-/Port-Konstruktion von
einer nicht belastbaren Ergebnisstrecke. Es reproduzierte folgende Blocker:

- Der Provenienzguard akzeptiert den inzwischen geschlossenen Ast weiterhin.
- Off-Arme erzeugen konstruktiv nichtendliche Sentinelwerte.
- Endlichkeitspruefung und Auditor sind fuer unbekannte Skalartypen fail-open.
- Die behauptete atomare Ausgabe zweier Dateien ist nicht paarweise atomar.
- Der Renderer setzt Diagnostik auch dann voraus, wenn die Antwort als nicht
  verfuegbar registriert wurde.
- Das Modellvokabular kollidiert zwischen Paper-I-Deposition, Centerfilter,
  Portgroessen und Maschinenrundung; der kanonische Notationsvertrag ist
  deshalb Teil der Remediation.

Die Recovery-Autorisierung ist verbraucht. Inzwischen bildet ein getrackter
maschinenlesbarer Governancezustand diese Schliessung ab; der Runner prueft
ihn vor der alten Provenienzstrecke und vor jeder Arm-Auswertung. Die zweite
targetfreie Teilkorrektur verwendet `null` fuer die nicht anwendbare
Off-Arm-Mobilitaetsmetrik, lehnt unbekannte Typen fail-closed ab und rendert
eine unverfuegbare Antwort ohne Diagnostikzugriff. Das exakte v2-Payloadschema,
die Manifest-zuletzt-Publikation, eine unabhaengige Manifestpruefung sowie die
einmalige CI-/Commit-gebundene Lease sind targetfrei implementiert und
adversarial geprueft. Das separate Readinessreview endete nach 929 lokalen
Tests und gruener CI fuer den exakten Implementierungscommit mit
`p5d-runner-ready-target-still-closed`. Eine danach ausdruecklich und einmalig
autorisierte dritte Ausfuehrung berechnete Panel, Response und Klassifikation,
scheiterte jedoch vor JSON-Encoding am strikten v2-Typvertrag: Die
Channel-off-Energieskala `numpy.finfo(float).tiny` wandelte sechs native
Nullquotienten in `numpy.float64` um. Receipt 3 existiert, Ergebnis, Report,
Manifest und Audit nicht. Damit ist auch dieser Lauf `p5d-inconclusive`, die
Readiness-Abdeckung falsifiziert und die Einmalfreigabe verbraucht. P5 bleibt
geschlossen.

Das danach getrennt geschriebene Produktionspfad-Protokoll wurde in einem
ersten Review wegen sechs Spezifikationsluecken abgelehnt, anschliessend
amendiert und im separaten Suffizienzreview als
`p5d-production-preflight-protocol-sufficient-target-closed` bewertet. Die
Amendierung friert neben drei wissenschaftlichen Quell-Blobs 41
wissenschaftliche Runner-Symbole per AST-Digest ein und oeffnet nur
target-gesperrte Fehltests sowie eine minimale P5-lokale Korrektur an der
vorhandenen Record-Grenze. Python-Standardbibliothek traegt den Datenvertrag;
NumPy-Skalare duerfen die numerische Schicht nicht ungeprueft verlassen. Eine
gemeinsame Projektbibliothek bleibt bis zu einem dokumentierten
Drei-Pipelines-Semantikvergleich gesperrt.

Diese Korrektur ist nun targetfrei abgeschlossen. Der echte Rueckgabepfad
konvertiert nur registrierte NumPy-Skalare werttreu in native Recordtypen und
validiert jeden vollstaendigen Off-/Aktivarm sofort gegen das v2-Schema. Der
reproduzierte Versuch-3-Nullquotient, ein adversariales Typenfeld, ein
synthetisches 64+768-Vollpanel, Publikation und unabhaengiger Auditor sind
gruen; ebenso 945 lokale Tests und CI fuer den exakten Implementierungscommit.
Das neue Review endet mit
`p5d-production-boundary-ready-target-closed-horizon-transfer-required`.
Das ist Infrastruktur-Readiness, keine Interaktionsevidenz und keine
Autorisierung fuer Versuch 4.

## Inferenz

Die Kreisloesungen sind eine geeignete Basis, um center-konjugierte Ports und
gegenseitige Kopplung mathematisch zu untersuchen. Aus den drei bisherigen
Ziellaeufen folgt jedoch nichts ueber reale Wechselwirkung oder Masse.

## Hypothesen

Interaktion, Ladung und Felder sowie Spin, Impuls, Traegheit und Masse bleiben
offen. Insbesondere ist eine zweite Differenz im sichtbaren Pfad noch kein
Nachweis einer positiven, zustandsunabhaengigen Masse. Der reziproke P5-D-Port
besitzt bei angehaltener nativer Centerbewegung exakt ein Relaxationsmodell
erster Ordnung. Ein gekoppelter harmonischer Oszillator ist daher ein
nachgelagerter Falsifikator fuer eine zusaetzliche, gedaechtnisinduzierte
Zustandsdimension und kein bereits eingebautes P5-D-Ergebnis.

## Claim-Grenze

Zulaessig ist: lokal zertifizierte bzw. numerisch kontrollierte Schleifen und
eine algebraisch definierte gegenseitige Center-Kopplung. Nicht zulaessig ist:
eine physikalische Deutung der P5-D-Infrastrukturfehler als positives oder
negatives Interaktionsergebnis.

## Quellen

- Modellreferenz: [Gleichungen](../reference/implemented_equations.md),
  [Rotating Waves](../reference/rotating_wave_foundation.md) und
  [Vokabular](../reference/model_vocabulary.md)
- [P5-D v2-Ergebnisvertrag](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/experiments/current/dynamics/rotation/scalar_memory_loop_p5d_result_schema_v2.json)
- [P5-D Versuch-3-Incident](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_attempt3_numpy_float_schema_failure_2026-09-05.md)
- [P5-D Produktionspfad-Protokoll](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/preregistration/scalar_memory_loop_p5d_production_path_preflight_protocol_2026-09-06.md)
- P5-D Protokollreviews:
  [negatives Erstreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_preflight_protocol_review_2026-09-06.md)
  und
  [Suffizienzreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_preflight_protocol_sufficiency_review_2026-09-06.md), danach das
  [Produktionsgrenzen-Readinessreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_readiness_review_2026-09-07.md)
- Horizontkette:
  [Finite-H Non-Tautology-/Horizont-Audit](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_finite_h_non_tautology_audit_2026-09-07.md),
  [amendiertes Protokoll](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_transfer_protocol_2026-09-08.md),
  [negatives Review](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_protocol_review_2026-09-08.md)
  und
  [Suffizienzreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_protocol_sufficiency_review_2026-09-08.md), danach
  [RED-Review](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_red_contract_review_2026-09-08.md)
  und
  [Infrastrukturreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_contract_infrastructure_review_2026-09-08.md)
  sowie das
  [v3-Vertragsreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_contract_v3_review_2026-09-09.md)
  und das korrigierende
  [Orchestrierungsreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_runner_orchestration_review_2026-09-09.md)
  sowie den
  [Backend-Bestandsaudit](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_backend_reuse_audit_2026-09-09.md)
  und das
  [finite-Rootadapter-Review](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_finite_root_adapter_review_2026-09-09.md)
  sowie das
  [Homotopie-/Intervallreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_homotopy_interval_review_2026-09-09.md)
  und das
  [lokale Ausschlussreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_local_exclusion_review_2026-09-09.md)
- [Claim-Register](paper_claims.md)
