import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count
from numba import njit

# ============================================================
# GLOBAL PARAMETERS
# ============================================================

T = 10000
T_sample = 6000
N_ens = 250
eps = 0.35
sigma = 1.0
dt_sample = 200
n_cores = min(4, cpu_count())

alpha_vals = np.logspace(-3, 0, 20)
eta_vals   = np.logspace(-1, 1, 20)

GLOBAL_SEED = 12345

# ============================================================
# Numba-optimierter Kernelgradient
# ============================================================

@njit
def gradK_numba(r):
    norm2 = r[0]*r[0] + r[1]*r[1] + r[2]*r[2]
    return -(r / (sigma*sigma)) * np.exp(-0.5 * norm2 / (sigma*sigma))

# ============================================================
# Numba-optimierte Trajektorie mit Ringpuffer
# ============================================================

@njit
def run_single_numba(alpha, eta, seed):
    np.random.seed(seed)
    x = np.zeros((T, 3))

    N_mem = max(50, int(15/alpha))
    hist = np.zeros((N_mem, 3))
    weights = alpha * (1 - alpha)**np.arange(N_mem)

    for n in range(T-1):
        mlen = min(n, N_mem)

        gradPhi = np.zeros(3)
        for k in range(mlen):
            idx = (n - k) % N_mem
            diff = x[n] - hist[idx]
            gradPhi += weights[k] * gradK_numba(diff)

        x[n+1] = x[n] + eps * np.random.randn(3) - eta * gradPhi
        hist[n % N_mem] = x[n+1]

    return x

# ============================================================
# Spectral dimension
# ============================================================

def spectral_dimension(trajs):
    times = np.arange(500, T_sample, dt_sample)

    rms = np.sqrt(np.mean(np.sum(trajs[:,T_sample//2,:]**2, axis=1)))
    r0 = 0.2 * rms

    P0 = np.array([
        np.mean(np.linalg.norm(trajs[:,t,:], axis=1) < r0)
        for t in times
    ])

    mask = P0 > 1e-4
    if np.sum(mask) < 5:
        return np.nan, 0.0

    logt = np.log(times[mask])
    logP = np.log(P0[mask])

    slope, residuals, _, _, _ = np.polyfit(logt, logP, 1, full=True)
    slope = slope[0]

    fit = slope * logt + np.mean(logP - slope * logt)
    ss_res = np.sum((logP - fit)**2)
    ss_tot = np.sum((logP - np.mean(logP))**2)
    R2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0

    return -2*slope, R2

# ============================================================
# Covariance dimension
# ============================================================

def covariance_dimension(trajs):
    X = trajs[:,T_sample//2,:]
    C = np.cov(X.T)
    eigvals = np.linalg.eigvalsh(C)

    if np.sum(eigvals) == 0:
        return np.nan

    return (np.sum(eigvals)**2) / np.sum(eigvals**2)

# ============================================================
# Worker für Parameterpaare
# ============================================================

def analyze_pair(args):
    i, j, alpha, eta = args

    base_seed = GLOBAL_SEED + i*10000 + j
    trajs = np.zeros((N_ens, T, 3))

    for k in range(N_ens):
        trajs[k] = run_single_numba(alpha, eta, base_seed + k)

    d_spec, R2 = spectral_dimension(trajs)
    d_cov = covariance_dimension(trajs)

    return i, j, d_spec, d_cov, R2

# ============================================================
# Checkpointing + Parallelisierung
# ============================================================

def compute_grid():
    shape = (len(alpha_vals), len(eta_vals))

    try:
        D_spec, D_cov, R2_map = np.load("progress.npy", allow_pickle=True)
        print("Fortschritt geladen.")
    except:
        D_spec = np.full(shape, np.nan)
        D_cov  = np.full(shape, np.nan)
        R2_map = np.full(shape, np.nan)

    tasks = []
    for i, a in enumerate(alpha_vals):
        for j, e in enumerate(eta_vals):
            if np.isnan(D_spec[i,j]):
                tasks.append((i, j, a, e))

    print(f"{len(tasks)} Parameterpaare zu berechnen.")

    with Pool(n_cores) as pool:
        for i, j, d_s, d_c, R2 in pool.imap_unordered(analyze_pair, tasks):
            D_spec[i,j] = d_s
            D_cov[i,j]  = d_c
            R2_map[i,j] = R2

            np.savez("progress.npz", D_spec=D_spec, D_cov=D_cov, R2_map=R2_map)
            print(f"Gespeichert: alpha={alpha_vals[i]:.3g}, eta={eta_vals[j]:.3g}")

    return D_spec, D_cov, R2_map

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    D_spec, D_cov, R2_map = compute_grid()

    # Plotten wie gehabt
    # ============================================================
    # Plot 1: Spectral dimension
    # ============================================================

    plt.figure()
    plt.imshow(D_spec, origin="lower",
               extent=[eta_vals[0],eta_vals[-1],
                       alpha_vals[0],alpha_vals[-1]],
               aspect="auto")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("eta")
    plt.ylabel("alpha")
    plt.colorbar(label="d_spec")
    plt.tight_layout()
    plt.savefig("heatmap_spectral_dimension.pdf")
    plt.close()

    # ============================================================
    # Plot 2: Covariance dimension
    # ============================================================

    plt.figure()
    plt.imshow(D_cov, origin="lower", extent=[eta_vals[0],eta_vals[-1],
                       alpha_vals[0],alpha_vals[-1]], aspect="auto")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("eta")
    plt.ylabel("alpha")
    plt.colorbar(label="d_cov")
    plt.tight_layout()
    plt.savefig("heatmap_covariance_dimension.pdf")
    plt.close()

    # ============================================================
    # Plot 3: Fit quality
    # ============================================================

    plt.figure()
    plt.imshow(R2_map, origin="lower",
               extent=[eta_vals[0],eta_vals[-1],
                       alpha_vals[0],alpha_vals[-1]],
               aspect="auto")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("eta")
    plt.ylabel("alpha")
    plt.colorbar(label="R2 fit quality")
    plt.tight_layout()
    plt.savefig("heatmap_fit_quality.pdf")
    plt.close()