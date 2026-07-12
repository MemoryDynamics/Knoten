import matplotlib
import numpy as np

matplotlib.use("Agg")
import math

import matplotlib.pyplot as plt
from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_normal_float32

# ============================================================
# GLOBAL PARAMETERS
# ============================================================

T = 1500000  # Deine physikalisch notwendige Zeit
T_sample = 6000
N_ens = 250
eps = 0.35
sigma = 1.0
dt_sample = 200

alpha_vals = np.logspace(-3, 0, 20)
eta_vals = np.logspace(-1, 1, 20)

GLOBAL_SEED = 12345

threads_per_block = 128  # GPU-Thread-Konfiguration

# ============================================================
# CUDA-Kernel: simuliert ein Ensemble von Trajektorien
# ============================================================


@cuda.jit
def simulate_ensemble_kernel(
    alpha,
    eta,
    eps,
    sigma,
    T,
    N_mem,
    T_mid,
    times,
    rng_states,
    hist,
    r_mid2,
    x_mid,
    r2_times,
):
    """
    Pro Thread: eine Trajektorie.
    - hist: (N_ens, N_mem, 3)
    - times: (n_times,)
    - r_mid2: (N_ens,)
    - x_mid: (N_ens, 3)
    - r2_times: (N_ens, n_times)
    """
    k = cuda.grid(1)
    n_ens = r_mid2.shape[0]
    if k >= n_ens:
        return

    # Zustand
    x0 = 0.0
    x1 = 0.0
    x2 = 0.0

    n_times = times.shape[0]
    t_idx = 0

    for n in range(T - 1):
        # effektive Memory-Länge
        mlen = n if n < N_mem else N_mem

        g0 = 0.0
        g1 = 0.0
        g2 = 0.0

        # Kernel-Gradient
        for kk in range(mlen):
            idx = (n - kk) % N_mem
            hx0 = hist[k, idx, 0]
            hx1 = hist[k, idx, 1]
            hx2 = hist[k, idx, 2]

            dx0 = x0 - hx0
            dx1 = x1 - hx1
            dx2 = x2 - hx2

            norm2 = dx0 * dx0 + dx1 * dx1 + dx2 * dx2
            # Gewicht
            w_k = alpha * math.pow(1.0 - alpha, kk)
            fac = -math.exp(-0.5 * norm2 / (sigma * sigma)) / (sigma * sigma)
            g0 += w_k * fac * dx0
            g1 += w_k * fac * dx1
            g2 += w_k * fac * dx2

        # Zufallsschritt (GPU-RNG)
        xi0 = xoroshiro128p_normal_float32(rng_states, k)
        xi1 = xoroshiro128p_normal_float32(rng_states, k)
        xi2 = xoroshiro128p_normal_float32(rng_states, k)

        x0 = x0 + eps * xi0 - eta * g0
        x1 = x1 + eps * xi1 - eta * g1
        x2 = x2 + eps * xi2 - eta * g2

        # History aktualisieren
        hist[k, n % N_mem, 0] = x0
        hist[k, n % N_mem, 1] = x1
        hist[k, n % N_mem, 2] = x2

        # r^2 an Sample-Zeiten speichern
        while t_idx < n_times and n == times[t_idx]:
            r2 = x0 * x0 + x1 * x1 + x2 * x2
            r2_times[k, t_idx] = r2
            t_idx += 1

        # x_mid und r_mid2 speichern
        if n == T_mid:
            x_mid[k, 0] = x0
            x_mid[k, 1] = x1
            x_mid[k, 2] = x2
            r_mid2[k] = x0 * x0 + x1 * x1 + x2 * x2


# ============================================================
# Auswertung: spectral dimension & covariance dimension
# ============================================================


def spectral_dimension_from_P0(times, P0):
    mask = P0 > 1e-4
    if np.sum(mask) < 5:
        return np.nan, 0.0

    logt = np.log(times[mask])
    logP = np.log(P0[mask])

    slope, residuals, _, _, _ = np.polyfit(logt, logP, 1, full=True)
    slope = slope[0]

    fit = slope * logt + np.mean(logP - slope * logt)
    ss_res = np.sum((logP - fit) ** 2)
    ss_tot = np.sum((logP - np.mean(logP)) ** 2)
    R2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return -2 * slope, R2


def covariance_dimension_from_samples(X):
    # X: (N_ens, 3)
    C = np.cov(X.T)

    # numerische Probleme abfangen
    if not np.all(np.isfinite(C)):
        return np.nan

    try:
        eigvals = np.linalg.eigvalsh(C)
    except np.linalg.LinAlgError:
        return np.nan

    if np.sum(eigvals) == 0 or not np.all(np.isfinite(eigvals)):
        return np.nan

    return (np.sum(eigvals) ** 2) / np.sum(eigvals**2)


# ============================================================
# Worker für ein Parameterpaar (CPU-Seite, ruft GPU-Kernel)
# ============================================================


def analyze_pair(i, j, alpha, eta):
    base_seed = GLOBAL_SEED + i * 10000 + j

    # Memory-Länge wie gehabt
    N_mem = max(50, int(15 / alpha))

    # Sample-Zeiten
    times = np.arange(500, T_sample, dt_sample, dtype=np.int32)
    n_times = len(times)
    T_mid = T_sample // 2

    # RNG-States auf GPU
    rng_states = create_xoroshiro128p_states(N_ens, seed=base_seed)

    # Device-Arrays
    hist_d = cuda.device_array((N_ens, N_mem, 3), dtype=np.float32)
    r_mid2_d = cuda.device_array(N_ens, dtype=np.float32)
    x_mid_d = cuda.device_array((N_ens, 3), dtype=np.float32)
    r2_times_d = cuda.device_array((N_ens, n_times), dtype=np.float32)

    # times auf Device
    times_d = cuda.to_device(times)

    # Kernel-Konfiguration
    blocks_per_grid = (N_ens + threads_per_block - 1) // threads_per_block

    # Kernel-Launch
    simulate_ensemble_kernel[blocks_per_grid, threads_per_block](
        float(alpha),
        float(eta),
        float(eps),
        float(sigma),
        int(T),
        int(N_mem),
        int(T_mid),
        times_d,
        rng_states,
        hist_d,
        r_mid2_d,
        x_mid_d,
        r2_times_d,
    )

    # Ergebnisse zurück auf CPU
    r_mid2 = r_mid2_d.copy_to_host().astype(np.float64)
    x_mid = x_mid_d.copy_to_host().astype(np.float64)
    r2_times = r2_times_d.copy_to_host().astype(np.float64)

    # rms und r0
    rms = np.sqrt(np.mean(r_mid2))
    r0 = 0.2 * rms

    # P0(t)
    P0 = np.mean(r2_times < r0 * r0, axis=0)

    # spectral dimension
    d_spec, R2 = spectral_dimension_from_P0(times, P0)

    # covariance dimension
    d_cov = covariance_dimension_from_samples(x_mid)

    return d_spec, d_cov, R2


# ============================================================
# Grid-Berechnung mit Checkpointing
# ============================================================


def compute_grid():
    shape = (len(alpha_vals), len(eta_vals))

    try:
        data = np.load("progress_gpu.npz", allow_pickle=True)
        D_spec = data["D_spec"]
        D_cov = data["D_cov"]
        R2_map = data["R2_map"]
        print("Fortschritt geladen.")
    except:
        D_spec = np.full(shape, np.nan)
        D_cov = np.full(shape, np.nan)
        R2_map = np.full(shape, np.nan)

    tasks = [
        (i, j, a, e)
        for i, a in enumerate(alpha_vals)
        for j, e in enumerate(eta_vals)
        if np.isnan(D_spec[i, j])
    ]

    print(f"{len(tasks)} Parameterpaare zu berechnen (GPU).")

    for i, j, a, e in tasks:
        print(f"Starte: alpha={a:.3g}, eta={e:.3g} (i={i}, j={j})")
        d_s, d_c, R2 = analyze_pair(i, j, a, e)
        D_spec[i, j] = d_s
        D_cov[i, j] = d_c
        R2_map[i, j] = R2

        np.savez("progress_gpu.npz", D_spec=D_spec, D_cov=D_cov, R2_map=R2_map)
        print(
            f"Gespeichert: alpha={a:.3g}, eta={e:.3g}, d_spec={d_s:.3f}, d_cov={d_c:.3f}, R2={R2:.3f}"
        )

    return D_spec, D_cov, R2_map


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    D_spec, D_cov, R2_map = compute_grid()

    # Plot 1: Spectral dimension
    plt.figure()
    plt.imshow(
        D_spec,
        origin="lower",
        extent=[eta_vals[0], eta_vals[-1], alpha_vals[0], alpha_vals[-1]],
        aspect="auto",
    )
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("eta")
    plt.ylabel("alpha")
    plt.colorbar(label="d_spec")
    plt.tight_layout()
    plt.savefig("heatmap_spectral_dimension_gpu.pdf")
    plt.close()

    # Plot 2: Covariance dimension
    plt.figure()
    plt.imshow(
        D_cov,
        origin="lower",
        extent=[eta_vals[0], eta_vals[-1], alpha_vals[0], alpha_vals[-1]],
        aspect="auto",
    )
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("eta")
    plt.ylabel("alpha")
    plt.colorbar(label="d_cov")
    plt.tight_layout()
    plt.savefig("heatmap_covariance_dimension_gpu.pdf")
    plt.close()

    # Plot 3: Fit quality
    plt.figure()
    plt.imshow(
        R2_map,
        origin="lower",
        extent=[eta_vals[0], eta_vals[-1], alpha_vals[0], alpha_vals[-1]],
        aspect="auto",
    )
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("eta")
    plt.ylabel("alpha")
    plt.colorbar(label="R2 fit quality")
    plt.tight_layout()
    plt.savefig("heatmap_fit_quality_gpu.pdf")
    plt.close()
