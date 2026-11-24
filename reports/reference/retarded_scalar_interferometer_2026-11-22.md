# Ein gemeinsames retardiertes Skalarfeld fuer Kraft und Bahnphase

Stand: 2026-11-22. **Getrennte Referenztheorie**, keine native
Zieltrajektorie und kein neu eingefuehrter Freiheitsgrad im FIFO.
Konkreter Raeumlichkeits- und Zeitvergleich nach dem
[Bahnphasentest](memory_gravity_action_phase_2026-11-22.md)
und dem [thermischen Abtasttest](fifo_thermal_sampling_2026-11-22.md).

**Ergebnis.** Ein und dieselbe lokale skalare Kopplung ergibt hier
eine erst nach Signallaufzeit eintreffende Kraft, eine danach exakt
lineare relative Phase und eine beschraenkte Vakuum-Dephasierung.
Die individuelle Einschaltverzoegerung kuerzt sich in der spaeten
Phasendifferenz exakt heraus. Die Referenz bietet damit einen
positiven Vergleich fuer die gemeinsame Kopplung, nicht fuer ihre
Herleitung aus Memory. Sie setzt 3D, Wellengleichung, Quantisierung
und klassische kontrollierte Quellen voraus.

## 1. Das festgelegte Feld

In Einheiten $c=\hbar=1$ benutze ein freies reelles masseloses
Skalarfeld auf flacher Raumzeit mit Hamiltonian

$$
H[J]=\frac12\int_{\mathbb R^3}
  (\Pi^2+|\nabla\phi|^2)\,d^3x-\int J\phi\,d^3x.
$$

Die Quellen sind vorgegebene, normierte Kugelprofile $f_a$
(homogene Kugel mit Radius a). Eine gemeinsame Quelle mit
Kopplung $q_S$ im Ursprung wird bei $t=0$ eingeschaltet.
Die beiden alternativen Probestrukturen mit gleicher Kopplung
$q_P$ liegen fuer $0\le t\le T$ bei $\mathbf r_A,\mathbf r_B$.
Beide haben $r_i=|\mathbf r_i|>2a$, damit sie die Quellkugel
nicht schneiden; die beiden alternativen Probeprofile muessen
untereinander nicht disjunkt sein. Das ist ein kontrolliertes
Quellenprotokoll, keine freie mechanische Flugbahn und kein
Modell der Strahlteiler.

Der retardierte Green-Kern fuer $\partial_t^2-\Delta$
ist $G_R(t,\mathbf r)=\delta(t-|\mathbf r|)/(4\pi|\mathbf r|)$
bei $|\mathbf r|>0$. Er folgt etwa aus der radialen
Fourier-Inversion von $\Theta(t)\sin(kt)/k$.
Dieselben Feldgleichungen und derselbe Term $-\int J\phi$
bestimmen Quelle und Probe. Die statische skalare Vorzeichenregel
wurde bereits im
[Interaktionsinventar](interaction_structure_inventory_2026-11-02.md)
vom elektrischen Gauss-Zwang unterschieden. Neu in diesem
Vergleich sind die Einschaltphase und ihr Kontrast aus demselben
raeumlich aufgeloesten Feld.

## 2. Kraft und exakte Einschaltphase

Schreibe $\langle\cdot\rangle_i$ fuer den normierten Mittelwert
ueber einen Quell- und einen Probepunkt in den beiden Kugeln
des Arms i, und $\ell$ fuer den Abstand dieser Punkte.
Das durch die gemeinsame Quelle am Probekopf gelesene
Potential und die akkumulierte Phase des Arms sind

$$
U_i(t)=-\frac{q_S q_P}{4\pi}
     \left\langle\frac{\Theta(t-\ell)}{\ell}\right\rangle_i,
\qquad
\phi_i(T)=-\int_0^T U_i(t)\,dt
=\frac{q_S q_P}{4\pi}
  \left\langle\frac{(T-\ell)_+}{\ell}\right\rangle_i .
$$

Bis $t=r_i-2a$ bleibt die Quellenantwort null. Ab $t=r_i+2a$
ist sie exakt statisch. In diesem Bereich gilt
$\langle1/\ell\rangle_i=1/r_i$: die Verteilung der beiden
relativen Punktverschiebungen ist radial und liegt innerhalb
der Kugel mit Radius $2a$, ausserhalb der Beobachtermitte.
Der aeussere Kugelpotentialwert folgt direkt durch Winkelmittelung.
Daraus ergibt sich die raeumliche Kraft
$-q_Sq_P\mathbf r_i/(4\pi r_i^3)$ im voll erreichten
Bereich und fuer $T>\max(r_A,r_B)+2a$

$$
\phi_i(T)=\frac{q_Sq_P}{4\pi}(T/r_i-1),\qquad
\Delta\phi(T)=\frac{q_Sq_P T}{4\pi}
   \left(\frac1{r_A}-\frac1{r_B}\right).
$$

Der konstante Laufzeitbeitrag ist auf beiden Armen derselbe.
Das folgt hier aus der Form des 3D-Wellenkerns, dem synchronen
Einschalten und gleichen integrierten Probekopplungen. Es
rechtfertigt keinen instantanen Einfluss vor dem Signal.
Auch ist es kein allgemeiner Satz fuer beliebige Quellenpulse.
Eine Newton-Kalibrierung $q_i=\sqrt{4\pi G}\,m_i$ wuerde
vorhandene mechanische Massen voraussetzen. Mit dieser
gesetzten Kalibrierung folgt im schwachen Hoehenvergleich aus
demselben Potential der gravitative Phasenanstieg; weder die
Massenregel noch G folgen aus dem Modell.

## 3. Kontrast aus dem quantisierten selben Feld

Quantisiere nur das freie Feld und beginne im Vakuum.
Die Quellen bleiben kontrollierte klassische Profile pro
Arm. Lineare Anregung erzeugt kohaerente Modenzustaende.
Nach [Feynman und Vernon (1963), insbesondere Abschnitt IV](https://doi.org/10.1016/0003-4916(63)90068-X)
enthaelt der Einflussfaktor den Term
$+i(J_A-J_B)G_R(J_A+J_B)/2$. Die Selbstbeitraege der
beiden Proben sind gleich; auch die Kreuzterme zwischen den
Proben sind in diesem symmetrischen Protokoll gleich.
Damit bleibt im Phasenanteil genau der retardierte Effekt
der gemeinsamen Quelle aus Abschnitt 2. Der Betrag ist der
Ueberlapp der Vakuumverschiebungen, wie auch in der Methode
von [Li (2025) fuer ein Skalarfeld](https://doi.org/10.1103/PhysRevD.111.044022)
ueber die Differenz der Anregungen. Die gemeinsame Quelle
kuerzt sich in dieser Differenz exakt heraus.

Seien $d=|\mathbf r_A-\mathbf r_B|$ und
$\tilde f_a(k)=3[\sin(ka)-ka\cos(ka)]/(ka)^3$.
Die Differenz der Modenamplituden ist

$$
\delta\alpha_{\mathbf k}
=\frac{i q_P\tilde f_a(k)}{(2\pi)^{3/2}\sqrt{2k}}
\bigl(e^{-i\mathbf k\cdot\mathbf r_A}
      -e^{-i\mathbf k\cdot\mathbf r_B}\bigr)
\int_0^T e^{ikt}\,dt .
$$

Der negative Logarithmus der idealen Sichtbarkeit ist
$\Gamma_T=\tfrac12\int|\delta\alpha_{\mathbf k}|^2d^3k$.
Das Winkelmittel liefert

$$
\Gamma_T=\frac{q_P^2}{2\pi^2}\int_0^\infty
  |\tilde f_a(k)|^2 [1-\operatorname{sinc}(kd)]
  \frac{1-\cos(kT)}{k}\,dk,
\qquad \operatorname{sinc}(s)=\frac{\sin s}{s}.
$$

Fuer festes $d>0$ verhaelt sich der T-unabhaengige Integrand
am Ursprung wie $O(k)$: Die Zweige haben gleiche Gesamtladung
und unterscheiden sich erst in der Ortsverteilung. Im UV
faellt er dank endlichem a wie $O(k^{-5})$. Das
Riemann-Lebesgue-Lemma gibt einen endlichen Grenzwert
$\Gamma_\infty$ (Integral ohne den Kosinusterm) und fuer
alle T gilt $0\le\Gamma_T\le2\Gamma_\infty$. Die Phase
kann also unbeschraenkt mit der Haltezeit wachsen, waehrend
der Kontrast nicht sekulaer abfaellt. Der Grenzwert betrifft
die *relative* Sichtbarkeit, nicht einen als Fock-Vakuum
behaupteten statischen Zustand der einzelnen geladenen Quelle
bei unendlicher Haltezeit.

## 4. Woran ein Memory-Kandidat zu messen ist

Der Referenzkanal koppelt eine Kraft proportional $q_Sq_P$,
eine Phasensteigung mit demselben Produkt und eine
quellunabhaengige Vakuum-Dephasierung proportional $q_P^2$.
Die Kombination diskriminiert staerker als eine statische
$1/r$-Kurve. Insbesondere hat der bisherige
[kritische Dichtekanal](collective_fifo_screening_2026-11-21.md)
eine quartische Aufbauzeit statt der hier eingesetzten
Signallaufzeit. Nicht die gleiche statische Potenz, sondern
der Kraft-/Phasen-/Kontrastvertrag ist zu reproduzieren.
Es fehlen dynamisch entstehende Quellen, ein aus Memory
hergeleitetes Medium, universelle Massenkopplung und jede
Einstein-Tensorstruktur. Es wurde auch kein gebundener
Quantenzustand aus diesem Interferometer hergeleitet.

[Quadratur und Sichtbarkeitsreferenz](../../experiments/current/reference/retarded_scalar_interferometer.py)
und [feste Kontrollen](../../tests/test_retarded_scalar_interferometer.py).
Keine native Trajektorie, keine Parametersuche.
