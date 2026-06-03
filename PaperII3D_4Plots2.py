# Robust numerical scaffold for Diagrams 1–4
# ==========================================
# Improvements vs. first draft:
# - Finite memory window N_mem ~ O(alpha^-1)
# - Ensemble averaging (kick vs. no-kick)
# - Differential observable ΔPhi_B(t)
# - Robust onset detection (k-sigma for m consecutive steps)
#
# This scaffold is meant to be PRL-quality and extensible.

import numpy as np
import matplotlib.pyplot as plt
import ctypes, os

# CPU-Affinity: Kerne 0–3
ctypes.windll.kernel32.SetProcessAffinityMask(os.getpid(), 0b1111)

# -----------------------------
# Global parameters
# -----------------------------
eps = 0.3
eta = 0.8
T = 3500
kick_time = 500
kick_strength = 2.0

N_ens = 50  # ensemble size
sigma_cut = 4.0  # onset threshold in sigma units
m_consec = 6  # consecutive steps above threshold

np.random.seed(1)


# -----------------------------
# Kernel
# -----------------------------
def gradK(r, sigma=1.0):
    return -(r / sigma ** 2) * np.exp(-0.5 * (r / sigma) ** 2)


# -----------------------------
# Single-run simulation
# -----------------------------
def run_single(L, alpha, with_kick):
    N_mem = int(5 / alpha)

    xA = np.zeros(T)
    xB = np.zeros(T) + L
    histA = []
    gradB = np.zeros(T)

    for n in range(T - 1):
        # gradients
        gradPhiA = sum(gradK(xA[n] - h) for h in histA)
        gradPhiB = sum(gradK(xB[n] - h) for h in histA)

        # noise
        xA[n + 1] = xA[n] + eps * np.random.randn() - eta * gradPhiA
        xB[n + 1] = xB[n] + eps * np.random.randn() - eta * gradPhiB

        # kick
        if with_kick and n == kick_time:
            xA[n + 1] += kick_strength

        # memory update
        histA = [(1 - alpha) * h + alpha * xA[n + 1] for h in histA]
        histA.append(xA[n + 1])
        if len(histA) > N_mem:
            histA = histA[-N_mem:]

        gradB[n] = gradPhiB

    return gradB


# -----------------------------
# Ensemble-averaged response
# -----------------------------
def ensemble_response(L, alpha):
    G_kick = np.zeros((N_ens, T))
    G_ref = np.zeros((N_ens, T))

    for i in range(N_ens):
        G_kick[i] = run_single(L, alpha, with_kick=True)
        G_ref[i] = run_single(L, alpha, with_kick=False)

    mean_kick = G_kick.mean(axis=0)
    mean_ref = G_ref.mean(axis=0)

    return mean_kick - mean_ref


# -----------------------------
# Onset detection
# -----------------------------
def detect_onset(signal):
    pre = signal[:kick_time]
    sigma = pre.std()

    for n in range(kick_time, T - m_consec):
        if np.all(signal[n:n + m_consec] > sigma_cut * sigma):
            return n - kick_time
    return np.nan


# =================================================
# Diagram 1: Retarded response
# =================================================
alpha0 = 0.05
L0 = 12.0

delta = ensemble_response(L0, alpha0)

plt.figure()
plt.plot(delta)
plt.axvline(kick_time)
plt.xlabel("update index n")
plt.ylabel("Δ response at B")
plt.title("Diagram 1: Retarded response (ensemble-averaged)")
plt.show()

# =================================================
# Diagram 2: Time-of-flight
# =================================================
Ls = np.linspace(6, 26, 6)
onsets = []

for L in Ls:
    delta = ensemble_response(L, alpha0)
    onsets.append(detect_onset(delta))

plt.figure()
plt.plot(Ls, onsets, marker='o')
plt.xlabel("distance L")
plt.ylabel("onset delay Δn")
plt.title("Diagram 2: Time-of-flight")
plt.show()

# =================================================
# Diagram 3: Scaling of c_eff with alpha
# =================================================
alphas = [0.02, 0.04, 0.06, 0.1]
c_eff = []

for a in alphas:
    delta = ensemble_response(L0, a)
    dt = detect_onset(delta)
    c_eff.append(L0 / dt if dt == dt else np.nan)

plt.figure()
plt.plot(alphas, c_eff, marker='o')
plt.xlabel("alpha")
plt.ylabel("effective speed c_eff")
plt.title("Diagram 3: Scaling of c_eff")
plt.show()

# =================================================
# Diagram 4: Operational light cone
# =================================================
pts_t, pts_L = [], []

for L in Ls:
    delta = ensemble_response(L, alpha0)
    dt = detect_onset(delta)
    if dt == dt:
        pts_t.append(dt)
        pts_L.append(L)

plt.figure()
plt.scatter(pts_t, pts_L)
plt.xlabel("Δn (time delay)")
plt.ylabel("distance L")
plt.title("Diagram 4: Operational light cone")
plt.show()
