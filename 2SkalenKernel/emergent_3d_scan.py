# emergent_3d_final_final.py
# ------------------------------------------------------------
# Scientifically faithful implementation:
# - TRUE finite memory history (ring buffer)
# - double kernel (repulsive + attractive)
# - numba CPU accelerated
# - adaptive stop ONLY after minimum N
# - checkpoint / resume
# - parameter sweep
# - dimension scan d=2..9
# - automatic plots
#
# This version intentionally prioritizes correctness over fake speed.
# ------------------------------------------------------------

import os

import matplotlib.pyplot as plt
import numpy as np
from numba import njit

# ============================================================
# CONFIG
# ============================================================

OUTDIR = "results_final"
os.makedirs(OUTDIR, exist_ok=True)

CHECKPOINT = os.path.join(OUTDIR, "checkpoint.npz")

# dimensions to scan
D_LIST = np.arange(2, 10)

# parameter sweep
ALPHAS = [0.0015, 0.0025]
ETAS = [0.12, 0.18]

# noise
EPSILON = 0.03

# double kernel
SIGMA_REP = 1.0
SIGMA_ATT = 3.0
A_REP = 1.0
B_ATT = 0.35

# runtime
N_MAX = int(150_000_000)
SAMPLE_EVERY = 5000

# memory horizon (real weighted history)
# ~20/alpha is robust
MEMORY_FACTOR = 20.0

# adaptive stop
N_MIN_STOP = int(10_000_000)
PLATEAU_TOL = 0.02
PLATEAU_SLOPE = 0.01

# dimension samples
MAX_SAMPLES = 2500


# ============================================================
# TRUE DOUBLE-KERNEL GRADIENT FROM HISTORY
# ============================================================


@njit
def compute_gradient(x, hist, weights, mlen, sigma_rep, sigma_att, A_rep, B_att):

    d = x.shape[0]
    g = np.zeros(d)

    srep2 = sigma_rep * sigma_rep
    satt2 = sigma_att * sigma_att

    for k in range(mlen):

        w = weights[k]

        dx = x - hist[k]
        r2 = 0.0
        for j in range(d):
            r2 += dx[j] * dx[j]

        # repulsive Gaussian
        frep = A_rep * np.exp(-0.5 * r2 / srep2) / srep2

        # attractive Gaussian
        fatt = B_att * np.exp(-0.5 * r2 / satt2) / satt2

        fac = frep - fatt

        for j in range(d):
            g[j] += w * fac * dx[j]

    return g


# ============================================================
# COVARIANCE DIMENSION
# ============================================================


@njit
def covariance_dimension(X):

    n, d = X.shape
    if n < 20:
        return np.nan

    mean = np.zeros(d)
    for i in range(n):
        mean += X[i]
    mean /= n

    C = np.zeros((d, d))

    for i in range(n):
        diff = X[i] - mean
        for a in range(d):
            for b in range(d):
                C[a, b] += diff[a] * diff[b]

    C /= n

    eig = np.linalg.eigvalsh(C)

    s1 = 0.0
    s2 = 0.0

    for i in range(d):
        s1 += eig[i]
        s2 += eig[i] * eig[i]

    if s2 <= 1e-20:
        return np.nan

    return (s1 * s1) / s2


# ============================================================
# SINGLE RUN
# ============================================================


def run_single(d, alpha, eta):

    rng = np.random.default_rng()

    M = max(200, int(MEMORY_FACTOR / alpha))

    # precompute exponential weights
    weights = np.empty(M)
    for k in range(M):
        weights[k] = alpha * ((1.0 - alpha) ** k)

    # state
    x = np.zeros(d)

    # ring/history buffer
    hist = np.zeros((M, d))
    filled = 0

    # samples for dimension
    samples = []
    Ns = []
    Ds = []

    for n in range(1, N_MAX + 1):

        mlen = filled if filled < M else M

        if mlen > 0:
            g = compute_gradient(
                x, hist[:mlen], weights[:mlen], mlen, SIGMA_REP, SIGMA_ATT, A_REP, B_ATT
            )
        else:
            g = np.zeros(d)

        # Euler step
        x = x + EPSILON * rng.standard_normal(d) - eta * g

        # update history: shift right (newest at index 0)
        if mlen < M:
            if mlen > 0:
                hist[1 : mlen + 1] = hist[0:mlen]
            hist[0] = x
            filled += 1
        else:
            hist[1:] = hist[:-1]
            hist[0] = x

        # diagnostics
        if n % SAMPLE_EVERY == 0:

            samples.append(x.copy())
            if len(samples) > MAX_SAMPLES:
                samples.pop(0)

            X = np.array(samples)
            D_eff = covariance_dimension(X)

            Ns.append(n)
            Ds.append(D_eff)

            # adaptive stop only after large N
            if n >= N_MIN_STOP and len(Ds) >= 5:

                d1 = abs(Ds[-1] - Ds[-2])
                d2 = abs(Ds[-2] - Ds[-3])
                d3 = abs(Ds[-3] - Ds[-4])

                slope = abs(Ds[-1] - Ds[-4]) / np.log(Ns[-1] / Ns[-4])

                if (
                    d1 < PLATEAU_TOL
                    and d2 < PLATEAU_TOL
                    and d3 < PLATEAU_TOL
                    and slope < PLATEAU_SLOPE
                ):
                    print(
                        f"Plateau reached d={d} alpha={alpha} eta={eta} N={n} D={D_eff:.3f}"
                    )
                    break

        if n % 1_000_000 == 0:
            print(f"d={d}, alpha={alpha}, eta={eta}, n={n}")

    return np.array(Ns), np.array(Ds)


# ============================================================
# CHECKPOINT
# ============================================================


def load_checkpoint():
    if not os.path.exists(CHECKPOINT):
        return {}
    return dict(np.load(CHECKPOINT, allow_pickle=True))["data"].item()


def save_checkpoint(data):
    np.savez(CHECKPOINT, data=data)


# ============================================================
# PLOTS
# ============================================================


def make_plots(data):

    # ---------------- D_vs_N first parameter set
    keys = list(data.keys())
    if len(keys) == 0:
        return

    key0 = keys[0]

    plt.figure(figsize=(10, 6))

    for d in D_LIST:
        ds = str(d)
        if ds in data[key0]:
            N = data[key0][ds]["N"]
            Dv = data[key0][ds]["D"]
            plt.plot(N, Dv, marker="o", ms=3, label=f"d={d}")

    plt.xscale("log")
    plt.xlabel("N")
    plt.ylabel("D_eff")
    plt.title(f"D(N) for {key0}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, "D_vs_N.png"), dpi=160)
    plt.close()

    # ---------------- plateau vs d
    plt.figure(figsize=(10, 6))

    for key in keys:

        xs = []
        ys = []

        for d in D_LIST:
            ds = str(d)
            if ds in data[key]:
                xs.append(d)
                ys.append(data[key][ds]["D"][-1])

        plt.plot(xs, ys, marker="o", label=key)

    plt.xlabel("embedding dimension d")
    plt.ylabel("plateau D_eff")
    plt.title("Plateau dimension vs embedding dimension")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, "D_vs_d.png"), dpi=160)
    plt.close()


# ============================================================
# MAIN
# ============================================================


def main():

    data = load_checkpoint()

    for alpha in ALPHAS:
        for eta in ETAS:

            key = f"a{alpha}_e{eta}"

            if key not in data:
                data[key] = {}

            for d in D_LIST:

                ds = str(d)

                if ds in data[key]:
                    continue

                print("\n====================================")
                print("RUN", key, "d=", d)
                print("====================================")

                N, Dv = run_single(d, alpha, eta)

                data[key][ds] = {"N": N, "D": Dv}

                save_checkpoint(data)
                make_plots(data)

    make_plots(data)
    print("All runs completed.")


if __name__ == "__main__":
    main()
