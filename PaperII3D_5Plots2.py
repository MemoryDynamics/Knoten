import matplotlib
import numpy as np

matplotlib.use("Agg")
from multiprocessing import Pool

import matplotlib.pyplot as plt

# =====================================================
# PARAMETERS
# =====================================================
eps = 0.3
eta = 0.8
T = 4500
kick_time = 700
kick_strength = 2.0

N_ens = 200
alpha0 = 0.05

np.random.seed(42)


# =====================================================
# KERNEL
# =====================================================
def gradK(r, sigma=1.0):
    return -(r / sigma**2) * np.exp(-0.5 * (r / sigma) ** 2)


# =====================================================
# SINGLE RUN
# =====================================================
def run_single(args):
    L, alpha, with_kick = args
    np.random.seed()

    N_mem = max(20, int(10 / alpha))
    xA = np.zeros(T)
    xB = np.zeros(T) + L
    histA = []
    gradB = np.zeros(T)

    for n in range(T - 1):

        gradPhiA = 0.0
        gradPhiB = 0.0

        # correct discrete memory
        for k, h in enumerate(reversed(histA)):
            weight = alpha * (1 - alpha) ** k
            gradPhiA += weight * gradK(xA[n] - h)
            gradPhiB += weight * gradK(xB[n] - h)

        xA[n + 1] = xA[n] + eps * np.random.randn() - eta * gradPhiA
        xB[n + 1] = xB[n] + eps * np.random.randn() - eta * gradPhiB

        if with_kick and n == kick_time:
            xA[n + 1] += kick_strength

        histA.append(xA[n + 1])
        if len(histA) > N_mem:
            histA = histA[-N_mem:]

        gradB[n] = gradPhiB

    return gradB


# =====================================================
# ENSEMBLE (parallel safe for Windows)
# =====================================================
def ensemble_response(L, alpha):

    args_kick = [(L, alpha, True)] * N_ens
    args_ref = [(L, alpha, False)] * N_ens

    with Pool(processes=4) as pool:
        Gk = pool.map(run_single, args_kick)
        Gr = pool.map(run_single, args_ref)

    Gk = np.array(Gk)
    Gr = np.array(Gr)

    return Gk.mean(axis=0) - Gr.mean(axis=0)


# =====================================================
# SMOOTH + PEAK DETECTION
# =====================================================
def detect_front(signal):
    smooth = np.convolve(signal, np.ones(20) / 20, mode="same")
    threshold = 3 * smooth[:kick_time].std()
    for n in range(kick_time, len(smooth)):
        if smooth[n] > threshold:
            return n - kick_time
    return None


if __name__ == "__main__":
    # =====================================================
    # DIAGRAM 1
    # =====================================================
    L0 = 12
    delta = ensemble_response(L0, alpha0)

    plt.figure()
    plt.plot(delta)
    plt.axvline(kick_time)
    plt.title("Retarded Response")
    plt.xlabel("n")
    plt.ylabel("Δ response")
    plt.tight_layout()
    plt.savefig("diagram1_retarded_response.pdf")
    plt.close()

    # =====================================================
    # DIAGRAM 2 + 4
    # =====================================================
    Ls = np.linspace(6, 30, 8)
    delays = []

    for L in Ls:
        delta = ensemble_response(L, alpha0)
        dt = detect_front(delta)
        delays.append(dt)

    plt.figure()
    plt.plot(Ls, delays, marker="o")
    plt.xlabel("L")
    plt.ylabel("delay")
    plt.tight_layout()
    plt.savefig("diagram2_time_of_flight.pdf")
    plt.close()

    plt.figure()
    plt.scatter(delays, Ls)
    plt.xlabel("delay")
    plt.ylabel("L")
    plt.tight_layout()
    plt.savefig("diagram4_light_cone.pdf")
    plt.close()

    # =====================================================
    # DIAGRAM 3
    # =====================================================
    alphas = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    c_eff = []

    for a in alphas:
        delta = ensemble_response(L0, a)
        dt = detect_front(delta)
        c_eff.append(L0 / dt)

    plt.figure()
    plt.plot(alphas, c_eff, marker="o")
    plt.xlabel("alpha")
    plt.ylabel("c_eff")
    plt.tight_layout()
    plt.savefig("diagram3_ceff_scaling.pdf")
    plt.close()

    # =====================================================
    # DIAGRAM 5 – EFFECTIVE DIMENSION
    # =====================================================
    def effective_dimension(signal):
        window = signal[kick_time + 100 : kick_time + 600]
        cov = np.cov(window)
        eig = np.linalg.eigvalsh([[cov]])
        s1 = np.sum(eig)
        s2 = np.sum(eig**2)
        return (s1**2 / s2) if s2 > 0 else 0

    d_vals = []

    for L in Ls:
        delta = ensemble_response(L, alpha0)
        d_vals.append(effective_dimension(delta))

    plt.figure()
    plt.plot(Ls, d_vals, marker="o")
    plt.xlabel("L")
    plt.ylabel("d_eff")
    plt.tight_layout()
    plt.savefig("diagram5_effective_dimension.pdf")
    plt.close()

    print("All diagrams completed.")
