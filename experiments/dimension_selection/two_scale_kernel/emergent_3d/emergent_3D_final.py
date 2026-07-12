import os

import matplotlib.pyplot as plt
import numpy as np
from numba import njit

# ============================================================
# CONFIG
# ============================================================

D_LIST = np.arange(2, 10)

alpha_list = [0.0015, 0.002, 0.003]
eta_list = [0.1, 0.15, 0.2]

epsilon = 0.03
sigma = 1.0

N_MAX = int(2e8)
sample_every = 2000

plateau_tol = 0.02
plateau_slope = 0.01

checkpoint_file = "checkpoint.npz"
out_dir = "results"
os.makedirs(out_dir, exist_ok=True)

# ============================================================
# RECURSIVE MEMORY (KEY SPEEDUP)
# ============================================================


@njit
def step(x, g_prev, x_prev, alpha, eta, epsilon, sigma):

    # new gradient contribution
    dx = x - x_prev
    r2 = np.dot(dx, dx)

    fac = np.exp(-0.5 * r2 / (sigma * sigma)) / (sigma * sigma)

    g_new = -fac * dx

    # recursive update
    g = (1 - alpha) * g_prev + alpha * g_new

    # stochastic step
    x_new = x + epsilon * np.random.randn(x.shape[0]) - eta * g

    return x_new, g


# ============================================================
# DIMENSION
# ============================================================


@njit
def covariance_dim(points):
    n, d = points.shape
    if n < 20:
        return np.nan

    mean = np.zeros(d)
    for i in range(n):
        mean += points[i]
    mean /= n

    C = np.zeros((d, d))
    for i in range(n):
        diff = points[i] - mean
        for a in range(d):
            for b in range(d):
                C[a, b] += diff[a] * diff[b]
    C /= n

    eig = np.linalg.eigvalsh(C)

    s1 = np.sum(eig)
    s2 = np.sum(eig * eig)

    if s2 == 0:
        return np.nan

    return (s1 * s1) / s2


# ============================================================
# PLATEAU DETECTION
# ============================================================


def check_plateau(Ds, Ns):

    if len(Ds) < 5:
        return False

    d1 = abs(Ds[-1] - Ds[-2])
    d2 = abs(Ds[-2] - Ds[-3])
    d3 = abs(Ds[-3] - Ds[-4])

    slope = abs(Ds[-1] - Ds[-4]) / np.log(Ns[-1] / Ns[-4])

    return (
        d1 < plateau_tol
        and d2 < plateau_tol
        and d3 < plateau_tol
        and slope < plateau_slope
    )


# ============================================================
# SINGLE RUN
# ============================================================


def run_simulation(d, alpha, eta):

    x = np.zeros(d)
    g = np.zeros(d)
    x_prev = np.zeros(d)

    samples = []

    Ns = []
    Ds = []

    for n in range(1, N_MAX):

        x, g = step(x, g, x_prev, alpha, eta, epsilon, sigma)
        x_prev = x.copy()

        if n % sample_every == 0:

            samples.append(x.copy())

            if len(samples) > 2000:
                samples.pop(0)

            D = covariance_dim(np.array(samples))

            Ns.append(n)
            Ds.append(D)

            # adaptive stop
            if check_plateau(Ds, Ns):
                print(f"Plateau reached at N={n} → D≈{D:.3f}")
                break

        if n % 1_000_000 == 0:
            print(f"d={d}, alpha={alpha}, eta={eta}, n={n}")

    return np.array(Ns), np.array(Ds)


# ============================================================
# CHECKPOINT
# ============================================================


def save_checkpoint(data):
    np.savez(checkpoint_file, **data)


def load_checkpoint():
    if not os.path.exists(checkpoint_file):
        return {}
    return dict(np.load(checkpoint_file, allow_pickle=True))


# ============================================================
# MAIN SWEEP
# ============================================================


def main():

    checkpoint = load_checkpoint()

    results = checkpoint.get("results", {})

    for alpha in alpha_list:
        for eta in eta_list:

            key = f"a{alpha}_e{eta}"

            if key not in results:
                results[key] = {}

            for d in D_LIST:

                if str(d) in results[key]:
                    continue

                print(f"\nRUN: d={d}, alpha={alpha}, eta={eta}")

                Ns, Ds = run_simulation(d, alpha, eta)

                results[key][str(d)] = {"N": Ns, "D": Ds}

                save_checkpoint({"results": results})

    save_plots(results)


# ============================================================
# PLOTS
# ============================================================


def save_plots(results):

    # --- D vs N (für einen Satz) ---
    key0 = list(results.keys())[0]

    plt.figure()
    for d in D_LIST:
        data = results[key0].get(str(d))
        if data is None:
            continue
        plt.plot(data["N"], data["D"], label=f"d={d}")

    plt.xscale("log")
    plt.xlabel("N")
    plt.ylabel("D_eff")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "D_vs_N.png"))
    plt.close()

    # --- D_inf vs d ---
    plt.figure()

    for key in results:

        d_vals = []
        D_inf = []

        for d in D_LIST:
            data = results[key].get(str(d))
            if data is None:
                continue
            d_vals.append(d)
            D_inf.append(data["D"][-1])

        plt.plot(d_vals, D_inf, "-o", label=key)

    plt.xlabel("embedding dimension d")
    plt.ylabel("D_eff (plateau)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "D_vs_d.png"))
    plt.close()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
