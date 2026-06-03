import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count
from numba import njit, prange

# ============================================================
# GLOBAL PARAMETERS
# ============================================================

T = 15000
T_sample = 6000
N_ens = 250
eps = 0.35
sigma = 1.0
dt_sample = 200
n_cores = min(6, cpu_count())

alpha_vals = np.logspace(-3, 0, 20)
eta_vals   = np.logspace(-1, 1, 20)

GLOBAL_SEED = 12345

# ============================================================
# Numba-Kernel
# ============================================================

@njit
def gradK_numba(r, sigma):
    norm2 = r[0]*r[0] + r[1]*r[1] + r[2]*r[2]
    return -(r / (sigma*sigma)) * np.exp(-0.5 * norm2 / (sigma*sigma))

@njit
def single_traj_midpoint(alpha, eta, eps, sigma, seed, T, N_mem, T_mid):
    np.random.seed(seed)
    x = np.zeros(3)
    hist = np.zeros((N_mem, 3))
    weights = alpha * (1 - alpha)**np.arange(N_mem)

    x_mid = np.zeros(3)
    r_mid2 = 0.0

    for n in range(T-1):
        mlen = min(n, N_mem)
        gradPhi = np.zeros(3)

        for k in range(mlen):
            idx = (n - k) % N_mem
            diff = x - hist[idx]
            gradPhi += weights[k] * gradK_numba(diff, sigma)

        x += eps * np.random.randn(3) - eta * gradPhi
        hist[n % N_mem] = x

        if n == T_mid:
            x_mid[:] = x
            r_mid2 = x[0]*x[0] + x[1]*x[1] + x[2]*x[2]

    return x_mid, r_mid2

@njit(parallel=True, fastmath=True)
def ensemble_rms(alpha, eta, eps, sigma, base_seed, N_ens, T, N_mem, T_mid):
    s = 0.0
    for k in prange(N_ens):
        _, r2 = single_traj_midpoint(alpha, eta, eps, sigma,
                                     base_seed + k, T, N_mem, T_mid)
        s += r2
    return np.sqrt(s / N_ens)

@njit(parallel=True, fastmath=True)
def ensemble_stats(alpha, eta, eps, sigma, base_seed, N_ens, T, N_mem,
                   times, T_mid, r0):
    n_times = len(times)
    counts = np.zeros(n_times, dtype=np.int64)
    sum_x = np.zeros(3)
    sum_xxT = np.zeros((3,3))

    for k in prange(N_ens):
        np.random.seed(base_seed + k)
        x = np.zeros(3)
        hist = np.zeros((N_mem, 3))
        weights = alpha * (1 - alpha)**np.arange(N_mem)

        t_idx = 0
        for n in range(T-1):
            mlen = min(n, N_mem)
            gradPhi = np.zeros(3)
            for kk in range(mlen):
                idx = (n - kk) % N_mem
                diff = x - hist[idx]
                gradPhi += weights[kk] * gradK_numba(diff, sigma)

            x += eps * np.random.randn(3) - eta * gradPhi
            hist[n % N_mem] = x

            while t_idx < n_times and n == times[t_idx]:
                r2 = x[0]*x[0] + x[1]*x[1] + x[2]*x[2]
                if r2 < r0*r0:
                    counts[t_idx] += 1
                t_idx += 1

            if n == T_mid:
                sum_x += x
                sum_xxT += np.outer(x, x)

    return counts, sum_x, sum_xxT

# ============================================================
# Worker
# ============================================================

def analyze_pair(args):
    i, j, alpha, eta = args
    base_seed = GLOBAL_SEED + i*10000 + j

    N_mem = max(50, int(15/alpha))
    times = np.arange(500, T_sample, dt_sample)
    T_mid = T_sample // 2

    # 1) rms
    rms = ensemble_rms(alpha, eta, eps, sigma, base_seed,
                       N_ens, T, N_mem, T_mid)
    r0 = 0.2 * rms

    # 2) P0(t) + Kovarianz
    counts, sum_x, sum_xxT = ensemble_stats(alpha, eta, eps, sigma,
                                            base_seed + 999999,
                                            N_ens, T, N_mem,
                                            times, T_mid, r0)

    P0 = counts / N_ens

    # spectral dimension
    mask = P0 > 1e-4
    if np.sum(mask) < 5:
        d_spec, R2 = np.nan, 0.0
    else:
        logt = np.log(times[mask])
        logP = np.log(P0[mask])
        slope, residuals, _, _, _ = np.polyfit(logt, logP, 1, full=True)
        slope = slope[0]
        fit = slope * logt + np.mean(logP - slope * logt)
        ss_res = np.sum((logP - fit)**2)
        ss_tot = np.sum((logP - np.mean(logP))**2)
        R2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
        d_spec = -2*slope

    # covariance dimension
    mean_x = sum_x / N_ens
    C = (sum_xxT / N_ens) - np.outer(mean_x, mean_x)
    eigvals = np.linalg.eigvalsh(C)
    if np.sum(eigvals) == 0:
        d_cov = np.nan
    else:
        d_cov = (np.sum(eigvals)**2) / np.sum(eigvals**2)

    return i, j, d_spec, d_cov, R2

# ============================================================
# Checkpointing + Parallelisierung
# ============================================================

def compute_grid():
    shape = (len(alpha_vals), len(eta_vals))

    try:
        data = np.load("progress.npz", allow_pickle=True)
        D_spec = data["D_spec"]
        D_cov  = data["D_cov"]
        R2_map = data["R2_map"]
        print("Fortschritt geladen.")
    except:
        D_spec = np.full(shape, np.nan)
        D_cov  = np.full(shape, np.nan)
        R2_map = np.full(shape, np.nan)

    tasks = [(i, j, a, e)
             for i, a in enumerate(alpha_vals)
             for j, e in enumerate(eta_vals)
             if np.isnan(D_spec[i,j])]

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

    # Plot 1
    plt.figure()
    plt.imshow(D_spec, origin="lower",
               extent=[eta_vals[0],eta_vals[-1],alpha_vals[0],alpha_vals[-1]],
               aspect="auto")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("eta"); plt.ylabel("alpha")
    plt.colorbar(label="d_spec")
    plt.tight_layout()
    plt.savefig("heatmap_spectral_dimension.pdf")
    plt.close()

    # Plot 2
    plt.figure()
    plt.imshow(D_cov, origin="lower",
               extent=[eta_vals[0],eta_vals[-1],alpha_vals[0],alpha_vals[-1]],
               aspect="auto")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("eta"); plt.ylabel("alpha")
    plt.colorbar(label="d_cov")
    plt.tight_layout()
    plt.savefig("heatmap_covariance_dimension.pdf")
    plt.close()

    # Plot 3
    plt.figure()
    plt.imshow(R2_map, origin="lower",
               extent=[eta_vals[0],eta_vals[-1],alpha_vals[0],alpha_vals[-1]],
               aspect="auto")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("eta"); plt.ylabel("alpha")
    plt.colorbar(label="R2 fit quality")
    plt.tight_layout()
    plt.savefig("heatmap_fit_quality.pdf")
    plt.close()
