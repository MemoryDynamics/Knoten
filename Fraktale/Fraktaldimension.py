import math

import numpy as np
from numba import njit

# ------------------------------------------------------------
# Kernel force
# ------------------------------------------------------------


@njit
def kernel_force(r, A, B, s1, s2):
    r2 = np.dot(r, r)

    f = np.zeros_like(r)

    if r2 > 1e-12:
        e1 = math.exp(-r2 / (2 * s1 * s1))
        e2 = math.exp(-r2 / (2 * s2 * s2))

        f += A * r / (s1 * s1) * e1
        f -= B * r / (s2 * s2) * e2

    return f


# ------------------------------------------------------------
# Single trajectory
# ------------------------------------------------------------


@njit
def simulate(N, dim, eps, eta, alpha, A, B, s1, s2):
    Nmem = int(5 / alpha) + 1
    x = np.zeros((N, dim))
    mem = np.zeros((Nmem, dim))
    weights = np.zeros(Nmem)
    idx = 0
    for n in range(1, N):
        force = np.zeros(dim)
        for k in range(Nmem):
            w = weights[k]
            if w == 0:
                continue
            r = x[n - 1] - mem[k]
            f = kernel_force(r, A, B, s1, s2)
            force += w * f

        # noise
        noise = np.random.normal(0, 1, dim)
        x[n] = x[n - 1] + eps * noise + eta * alpha * force

        # update memory
        mem[idx] = x[n]
        weights *= 1 - alpha
        weights[idx] = alpha
        idx = (idx + 1) % Nmem

    return x


def fractal_dimension(points):
    bbox = np.max(points) - np.min(points)
    sizes = np.logspace(np.log10(bbox / 200), np.log10(bbox / 5), 12)

    counts = []
    for s in sizes:
        boxes = np.floor(points / s).astype(np.int64)
        unique = np.unique(boxes, axis=0)
        counts.append(len(unique))
    coeff = np.polyfit(np.log(1 / sizes), np.log(counts), 1)
    return coeff[0]


def run_ensemble(runs=10):
    dims = []
    for i in range(runs):
        traj = simulate(
            N=2_000_000, dim=5, eps=0.05, eta=2, alpha=0.01, A=1, B=3, s1=1, s2=0.15
        )

        d = fractal_dimension(traj[10000:])
        dims.append(d)
        print("run", i, "Docc =", d)

    print("mean =", np.mean(dims))
    print("std  =", np.std(dims))


run_ensemble()
