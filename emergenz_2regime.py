import matplotlib
import numpy as np

matplotlib.use("Agg")
from multiprocessing import Pool

import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# =====================================================
# GLOBALS
# =====================================================
T = 5000
kick_time = 800
N_ens = 200
L_values = np.linspace(5, 35, 12)

np.random.seed()


# =====================================================
# KERNEL
# =====================================================
def gradK(r, sigma):
    return -(r / sigma**2) * np.exp(-0.5 * (r / sigma) ** 2)


# =====================================================
# SINGLE RUN (vectorized memory)
# =====================================================
def run_single(args):
    L, alpha, eta, eps, sigma, kick_strength, with_kick = args

    xA = np.zeros(T)
    xB = np.zeros(T) + L

    N_mem = max(50, int(10 / alpha))
    histA = np.zeros(N_mem)
    weights = alpha * (1 - alpha) ** np.arange(N_mem)

    gradB = np.zeros(T)

    for n in range(T - 1):

        # valid memory length
        mlen = min(n, N_mem - 1)

        if mlen > 0:
            past = histA[:mlen]
            w = weights[:mlen]

            gradPhiA = np.sum(w * gradK(xA[n] - past, sigma))
            gradPhiB = np.sum(w * gradK(xB[n] - past, sigma))
        else:
            gradPhiA = 0.0
            gradPhiB = 0.0

        xA[n + 1] = xA[n] + eps * np.random.randn() - eta * gradPhiA
        xB[n + 1] = xB[n] + eps * np.random.randn() - eta * gradPhiB

        if with_kick and n == kick_time:
            xA[n + 1] += kick_strength

        # shift memory
        histA[1:] = histA[:-1]
        histA[0] = xA[n + 1]

        gradB[n] = gradPhiB

    return gradB


# =====================================================
# ENSEMBLE
# =====================================================
def ensemble_response(params):

    L, alpha, eta, eps, sigma, kick_strength = params

    args_kick = [(L, alpha, eta, eps, sigma, kick_strength, True)] * N_ens
    args_ref = [(L, alpha, eta, eps, sigma, kick_strength, False)] * N_ens

    with Pool(processes=4) as pool:
        Gk = pool.map(run_single, args_kick)
        Gr = pool.map(run_single, args_ref)

    Gk = np.array(Gk)
    Gr = np.array(Gr)

    return Gk.mean(axis=0) - Gr.mean(axis=0)


# =====================================================
# FRONT DETECTION
# =====================================================
def detect_front(signal):
    smooth = np.convolve(signal, np.ones(30) / 30, mode="same")
    peaks, props = find_peaks(smooth[kick_time + 50 :], prominence=1e-4)

    if len(peaks) == 0:
        return None

    return peaks[0]


# =====================================================
# RUN REGIME
# =====================================================
def run_regime(name, alpha, eta, eps, sigma, kick_strength):

    delays = []

    for L in L_values:
        delta = ensemble_response((L, alpha, eta, eps, sigma, kick_strength))
        dt = detect_front(delta)
        delays.append(dt if dt is not None else np.nan)

    delays = np.array(delays)

    # ---- Delay vs L ----
    plt.figure()
    plt.plot(L_values, delays, marker="o")
    plt.xlabel("L")
    plt.ylabel("delay")
    plt.title(f"{name}: Delay vs L")
    plt.tight_layout()
    plt.savefig(f"{name}_delay_vs_L.pdf")
    plt.close()

    # ---- Delay vs L^2 ----
    plt.figure()
    plt.plot(L_values**2, delays, marker="o")
    plt.xlabel("L^2")
    plt.ylabel("delay")
    plt.title(f"{name}: Delay vs L^2")
    plt.tight_layout()
    plt.savefig(f"{name}_delay_vs_L2.pdf")
    plt.close()

    # ---- Light cone ----
    plt.figure()
    plt.scatter(delays, L_values)
    plt.xlabel("delay")
    plt.ylabel("L")
    plt.title(f"{name}: Light Cone")
    plt.tight_layout()
    plt.savefig(f"{name}_lightcone.pdf")
    plt.close()


# =====================================================
# DEFINE REGIMES
# =====================================================
regimes = {
    "diffusive": {
        "alpha": 0.05,
        "eta": 0.8,
        "eps": 0.3,
        "sigma": 1.0,
        "kick_strength": 2.0,
    },
    "front": {
        "alpha": 0.01,
        "eta": 3.0,
        "eps": 0.2,
        "sigma": 0.4,
        "kick_strength": 4.0,
    },
}

# =====================================================
# EXECUTION
# =====================================================
if __name__ == "__main__":
    for name, p in regimes.items():
        print(f"Running regime: {name}")
        run_regime(name, **p)

    print("All regimes completed.")
