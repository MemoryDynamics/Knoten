import os
from multiprocessing import Pool, cpu_count

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")

# -------------------------
# PARAMETERS
# -------------------------
T = 6000
N_ens = 150
eps = 0.3
sigma = 1.0
r0 = 0.5

alpha_vals = np.logspace(-3, -0.3, 10)
eta_vals = np.linspace(0.2, 2.0, 10)

# Anzahl Prozesse (ggf. anpassen)
N_PROCESSES = min(4, cpu_count())

# Fester Seed für Reproduzierbarkeit auf Skript-Ebene
GLOBAL_SEED = 12345


# -------------------------
# Vektorisierter Kernelgradient (3D)
# r: Array (..., 3)
# -------------------------
def gradK_vec(r):
    """
    r: array of shape (M, 3)
    returns: array of shape (M, 3)
    """
    norms = np.linalg.norm(r, axis=1)
    fac = np.exp(-0.5 * norms**2 / sigma**2)[:, None]
    return -(r / sigma**2) * fac


# -------------------------
# Single trajectory mit Ringpuffer
# -------------------------
def run_single(alpha, eta, rng):
    """
    Simuliert eine einzelne Trajektorie für gegebenes (alpha, eta)
    mit einem eigenen RNG (np.random.Generator).
    """
    x = np.zeros((T, 3))

    # Memory-Länge
    N_mem = max(50, int(10 / alpha))
    hist = np.zeros((N_mem, 3))
    weights = alpha * (1 - alpha) ** np.arange(N_mem)

    # Ringpuffer-Index
    # hist[idx] ist jeweils der "neueste" Eintrag
    for n in range(T - 1):
        # Anzahl verfügbarer Vergangenheitsschritte
        mlen = min(n, N_mem)

        if mlen > 0:
            # Wir nehmen die letzten mlen Einträge aus dem Ringpuffer
            # und ordnen sie so, dass hist_recent[0] der jüngste ist.
            idxs = (np.arange(mlen) - 1 - n) % N_mem
            past = hist[idxs]

            diffs = x[n] - past
            grads = gradK_vec(diffs)
            w = weights[:mlen][:, None]
            gradPhi = np.sum(w * grads, axis=0)
        else:
            gradPhi = 0.0

        x[n + 1] = x[n] + eps * rng.normal(size=3) - eta * gradPhi

        # Neuen Punkt in den Ringpuffer schreiben
        hist[n % N_mem] = x[n + 1]

    return x


# -------------------------
# Batch von Trajektorien (für Multiprocessing)
# -------------------------
def run_batch(args):
    """
    args: (alpha, eta, batch_size, base_seed, batch_index)
    Jede Batch bekommt einen eigenen Seed, ist aber deterministisch.
    """
    alpha, eta, batch_size, base_seed, batch_index = args
    seed = base_seed + batch_index
    rng = np.random.default_rng(seed)

    trajs = []
    for _ in range(batch_size):
        # Für jede Trajektorie einen eigenen Substream
        sub_seed = rng.integers(0, 2**32 - 1)
        sub_rng = np.random.default_rng(sub_seed)
        traj = run_single(alpha, eta, sub_rng)
        trajs.append(traj)

    return np.array(trajs)  # shape: (batch_size, T, 3)


# -------------------------
# Spektrale Dimension
# -------------------------
def spectral_dimension(alpha, eta, n_ens=N_ens, n_proc=N_PROCESSES):
    """
    Berechnet die spektrale Dimension für ein Parameterpaar (alpha, eta).
    Nutzt Batching + Multiprocessing über Ensembles.
    """
    # Batching
    batch_size = max(1, n_ens // (2 * n_proc))
    n_batches = (n_ens + batch_size - 1) // batch_size

    base_seed = GLOBAL_SEED + int(1e6 * (hash((float(alpha), float(eta))) % 1e6))

    # Multiprocessing über Batches
    args_list = []
    for b in range(n_batches):
        # Letzte Batch ggf. kleiner
        bs = (
            batch_size
            if (b < n_batches - 1)
            else (n_ens - batch_size * (n_batches - 1))
        )
        args_list.append((alpha, eta, bs, base_seed, b))

    if n_proc > 1:
        with Pool(n_proc) as pool:
            results = pool.map(run_batch, args_list)
        trajs = np.vstack(results)
    else:
        # Fallback: alles im Hauptprozess
        results = [run_batch(a) for a in args_list]
        trajs = np.vstack(results)

    # Sicherstellen, dass wir genau n_ens Trajektorien haben
    trajs = trajs[:n_ens]

    # Rückkehrwahrscheinlichkeit
    P0 = []
    times = np.arange(200, T, 200)

    for t in times:
        dist = np.linalg.norm(trajs[:, t, :], axis=1)
        count = np.sum(dist < r0)
        P0.append(count / n_ens)

    P0 = np.array(P0)

    # Numerische Stabilität: P0 clippen
    P0 = np.clip(P0, 1e-12, 1.0)

    logt = np.log(times)
    logP = np.log(P0)

    # Linearer Fit: log P0 ~ -d_spec/2 * log t + const
    slope = np.polyfit(logt, logP, 1)[0]

    return -2 * slope


# -------------------------
# Heatmap
# -------------------------
def compute_heatmap(alpha_vals, eta_vals):
    shape = (len(alpha_vals), len(eta_vals))

    # Falls Datei existiert → laden
    if os.path.exists("heatmap_progress.npy"):
        D = np.load("heatmap_progress.npy")
        print("Fortschritt geladen.")
    else:
        D = np.full(shape, np.nan)

    for i, a in enumerate(alpha_vals):
        for j, e in enumerate(eta_vals):

            # Überspringen, wenn schon berechnet
            if not np.isnan(D[i, j]):
                print(f"[SKIP] alpha={a:.4g}, eta={e:.4g}")
                continue

            print(f"[RUN ] alpha={a:.4g}, eta={e:.4g}")
            d_spec = spectral_dimension(a, e)
            D[i, j] = d_spec

            # Sofort speichern
            np.save("heatmap_progress.npy", D)

    return D


def plot_heatmap(
    D, alpha_vals, eta_vals, filename="spectral_dimension_heatmap_optimized.pdf"
):
    plt.figure(figsize=(6, 4))

    # Für alpha bietet sich log-Skala an
    extent = [eta_vals[0], eta_vals[-1], alpha_vals[0], alpha_vals[-1]]

    im = plt.imshow(
        D, origin="lower", extent=extent, aspect="auto", interpolation="nearest"
    )

    plt.xlabel("eta")
    plt.ylabel("alpha")
    cbar = plt.colorbar(im)
    cbar.set_label("d_spec")

    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    plt.close()


if __name__ == "__main__":
    D = compute_heatmap(alpha_vals, eta_vals)
    # Speichere die Daten sofort – absolut sicher
    np.save("heatmap_data.npy", D)
    print("Heatmap-Daten gespeichert als heatmap_data.npy")

    # Jetzt erst plotten (headless)
    plot_heatmap(D, alpha_vals, eta_vals)
    print("Fertig. Heatmap gespeichert.")
