# knot_chi_scan.py

import os
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
from numba import njit

# ============================================================
# CONFIG
# ============================================================

OUT = "chi_scan"
os.makedirs(OUT, exist_ok=True)

N_MAX = 50_000_000
SAMPLE_EVERY = 5000

d = 3

epsilon = 0.03

# baseline
alpha = 0.002

sigma_rep = 50.0
A_rep = 1.0

# sweep over chi = eta/(alpha sigma_att²)

chi_vals = np.logspace(-3, 1, 12)

# keep eta fixed
eta = 0.15

# derive sigma_att
sigma_att_vals = np.sqrt(eta / (alpha * chi_vals))

B_att = 0.35

MEMORY_FACTOR = 20

MAX_SAMPLES = 3000

# ============================================================
# TRUE MEMORY GRADIENT
# ============================================================


@njit
def grad(x, hist, w, sigma_rep, sigma_att, A_rep, B_att):

    d = x.shape[0]

    g = np.zeros(d)

    sr2 = sigma_rep * sigma_rep
    sa2 = sigma_att * sigma_att

    for k in range(hist.shape[0]):

        dx = x - hist[k]

        r2 = np.dot(dx, dx)

        rep = A_rep * np.exp(-0.5 * r2 / sr2) / sr2
        att = B_att * np.exp(-0.5 * r2 / sa2) / sa2

        fac = rep - att

        g += w[k] * fac * dx

    return g


# ============================================================
# DIMENSION
# ============================================================


def covariance_dim(X):

    if len(X) < 20:
        return np.nan

    C = np.cov(X.T)

    eig = np.linalg.eigvalsh(C)

    s1 = np.sum(eig)
    s2 = np.sum(eig**2)

    return s1 * s1 / s2


# ============================================================
# KNOT ANALYSIS
# ============================================================


def knot_analysis(samples, voxel=20, min_visits=20):

    occ = defaultdict(list)

    for t, x in enumerate(samples):

        c = tuple(np.floor(x / voxel).astype(int))

        occ[c].append(t)

    knots = []

    for k, v in occ.items():

        if len(v) < min_visits:
            continue

        v = np.array(v)

        dt = np.diff(v)

        trans = np.sum(dt > 1)

        res = len(v) / (trans + 1)

        knots.append(res)

    if len(knots) == 0:

        return 0, 0

    return len(knots), np.mean(knots)


# ============================================================
# SINGLE RUN
# ============================================================


def run(sigma_att):

    M = max(200, int(MEMORY_FACTOR / alpha))

    weights = np.array([alpha * (1 - alpha) ** k for k in range(M)])

    hist = np.zeros((M, d))

    x = np.zeros(d)

    filled = 0

    samples = []

    D_hist = []

    for n in range(1, N_MAX):

        m = min(filled, M)

        if m > 0:

            g = grad(x, hist[:m], weights[:m], sigma_rep, sigma_att, A_rep, B_att)

        else:

            g = np.zeros(d)

        x += epsilon * np.random.randn(d) - eta * g

        if m < M:

            hist[1 : m + 1] = hist[:m]

            hist[0] = x

            filled += 1

        else:

            hist[1:] = hist[:-1]

            hist[0] = x

        if n % SAMPLE_EVERY == 0:

            samples.append(x.copy())

            if len(samples) > MAX_SAMPLES:

                samples.pop(0)

            D_hist.append(covariance_dim(np.array(samples)))

    nk, res = knot_analysis(samples)

    return (np.array(D_hist), nk, res, samples)


# ============================================================
# MAIN
# ============================================================

results = []

for chi, sigma_att in zip(chi_vals, sigma_att_vals):

    print("chi", chi, "sigma", sigma_att)

    D, nk, res, samples = run(sigma_att)

    results.append([chi, nk, res, np.nanmean(D)])

    np.save(OUT + f"/traj_{chi:.4g}.npy", samples)

results = np.array(results)

# ============================================================
# PLOTS
# ============================================================

plt.figure()

plt.semilogx(results[:, 0], results[:, 1], "-o")

plt.xlabel("chi")
plt.ylabel("knot count")

plt.tight_layout()

plt.savefig(OUT + "/knots_vs_chi.png")

plt.close()

plt.figure()

plt.semilogx(results[:, 0], results[:, 2], "-o")

plt.xlabel("chi")

plt.ylabel("mean residence")

plt.tight_layout()

plt.savefig(OUT + "/residence_vs_chi.png")

plt.close()

plt.figure()

plt.semilogx(results[:, 0], results[:, 3], "-o")

plt.xlabel("chi")

plt.ylabel("mean D_eff")

plt.tight_layout()

plt.savefig(OUT + "/dimension_vs_chi.png")

plt.close()
