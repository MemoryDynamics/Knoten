from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np

# -------------------------
# PARAMETERS
# -------------------------
T = 6000
N_ens = 150
eps = 0.3
sigma = 1.0
r0 = 0.5

alpha_vals = np.logspace(-3, -0.3, 10)
eta_vals = np.linspace(0.3, 3.0, 10)


# -------------------------
# Kernel gradient (3D)
# -------------------------
def gradK(r):
    norm = np.linalg.norm(r)
    return -(r / sigma**2) * np.exp(-0.5 * norm**2 / sigma**2)


# -------------------------
# Single trajectory
# -------------------------
def run_single(args):
    alpha, eta = args
    x = np.zeros((T, 3))
    N_mem = max(50, int(10 / alpha))
    hist = np.zeros((N_mem, 3))
    weights = alpha * (1 - alpha) ** np.arange(N_mem)

    for n in range(T - 1):
        mlen = min(n, N_mem - 1)
        if mlen > 0:
            past = hist[:mlen]
            w = weights[:mlen]
            diffs = x[n] - past
            grads = np.array([gradK(d) for d in diffs])
            gradPhi = np.sum(w[:, None] * grads, axis=0)
        else:
            gradPhi = 0.0

        x[n + 1] = x[n] + eps * np.random.randn(3) - eta * gradPhi

        hist[1:] = hist[:-1]
        hist[0] = x[n + 1]

    return x


# -------------------------
# Spectral dimension
# -------------------------
def spectral_dimension(alpha, eta):

    with Pool(4) as pool:
        trajs = pool.map(run_single, [(alpha, eta)] * N_ens)

    trajs = np.array(trajs)

    P0 = []
    times = np.arange(200, T, 200)

    for t in times:
        count = np.sum(np.linalg.norm(trajs[:, t, :], axis=1) < r0)
        P0.append(count / N_ens)

    P0 = np.array(P0)

    mask = P0 > 0
    logt = np.log(times[mask])
    logP = np.log(P0[mask])

    slope = np.polyfit(logt, logP, 1)[0]

    return -2 * slope


# -------------------------
# Heatmap
# -------------------------
if __name__ == "__main__":
    D = np.zeros((len(alpha_vals), len(eta_vals)))

    for i, a in enumerate(alpha_vals):
        for j, e in enumerate(eta_vals):
            print("alpha", a, "eta", e)
            D[i, j] = spectral_dimension(a, e)

    plt.imshow(
        D,
        origin="lower",
        extent=[eta_vals[0], eta_vals[-1], alpha_vals[0], alpha_vals[-1]],
        aspect="auto",
    )

    plt.xlabel("eta")
    plt.ylabel("alpha")
    plt.colorbar(label="d_spec")
    plt.tight_layout()
    plt.savefig("spectral_dimension_heatmap.pdf")
