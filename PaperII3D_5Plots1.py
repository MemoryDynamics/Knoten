import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# =============================
# Parameters
# =============================
eps = 0.3
eta = 0.8
T = 4500
kick_time = 700
kick_strength = 2.0

N_ens = 300          # increase for quality
alpha0 = 0.05
sigma_cut = 2.5      # relaxed threshold
m_consec = 5

np.random.seed(3)

# =============================
# Kernel
# =============================
def gradK(r, sigma=1.0):
    return -(r / sigma**2) * np.exp(-0.5 * (r / sigma)**2)

# =============================
# Single run
# =============================
def run_single(L, alpha, with_kick):
    N_mem = max(20, int(6 / alpha))
    xA = np.zeros(T)
    xB = np.zeros(T) + L
    histA = []
    gradB = np.zeros(T)

    for n in range(T-1):
        gradPhiA = sum(gradK(xA[n] - h) for h in histA)
        gradPhiB = sum(gradK(xB[n] - h) for h in histA)

        xA[n+1] = xA[n] + eps*np.random.randn() - eta*gradPhiA
        xB[n+1] = xB[n] + eps*np.random.randn() - eta*gradPhiB

        if with_kick and n == kick_time:
            xA[n+1] += kick_strength

        histA = [(1-alpha)*h + alpha*xA[n+1] for h in histA]
        histA.append(xA[n+1])
        histA = histA[-N_mem:]

        gradB[n] = gradPhiB

    return gradB

# =============================
# Ensemble response
# =============================
def ensemble_response(L, alpha):
    Gk = np.zeros((N_ens, T))
    Gr = np.zeros((N_ens, T))

    for i in range(N_ens):
        Gk[i] = run_single(L, alpha, True)
        Gr[i] = run_single(L, alpha, False)

    return Gk.mean(axis=0) - Gr.mean(axis=0)

# =============================
# Smoothed onset detection
# =============================
def detect_onset(signal, window=20):
    smooth = np.convolve(signal, np.ones(window)/window, mode="same")
    pre = smooth[:kick_time]
    sigma = pre.std()

    for n in range(kick_time, T-m_consec):
        if np.all(smooth[n:n+m_consec] > sigma_cut*sigma):
            return n - kick_time
    return None

# =============================
# Diagram 1
# =============================
L0 = 12
delta = ensemble_response(L0, alpha0)

plt.figure()
plt.plot(delta)
plt.axvline(kick_time)
plt.xlabel("update index n")
plt.ylabel("Δ response at B")
plt.title("Diagram 1: Retarded response")
plt.savefig("diagram1_retarded_response.pdf")
plt.close()

# =============================
# Diagram 2 + 4
# =============================
Ls = np.linspace(6, 30, 8)
delays = []

for L in Ls:
    delta = ensemble_response(L, alpha0)
    dt = detect_onset(delta)
    delays.append(dt)

# Diagram 2
valid = [(L, d) for L, d in zip(Ls, delays) if d is not None]
if valid:
    Ls_v, dts_v = zip(*valid)
    plt.figure()
    plt.plot(Ls_v, dts_v, marker='o')
    plt.xlabel("distance L")
    plt.ylabel("onset delay Δn")
    plt.title("Diagram 2: Time-of-flight")
    plt.savefig("diagram2_time_of_flight.pdf")
    plt.close()

    # Diagram 4
    plt.figure()
    plt.scatter(dts_v, Ls_v)
    plt.xlabel("Δn")
    plt.ylabel("L")
    plt.title("Diagram 4: Operational light cone")
    plt.savefig("diagram4_light_cone.pdf")
    plt.close()

# =============================
# Diagram 3
# =============================
alphas = [0.02, 0.04, 0.06, 0.1]
c_eff = []

for a in alphas:
    delta = ensemble_response(L0, a)
    dt = detect_onset(delta)
    c_eff.append(L0/dt if dt else np.nan)

plt.figure()
plt.plot(alphas, c_eff, marker='o')
plt.xlabel("alpha")
plt.ylabel("c_eff")
plt.title("Diagram 3: Scaling of c_eff")
plt.savefig("diagram3_ceff_scaling.pdf")
plt.close()

# =============================
# Diagram 5 (starter)
# =============================
np.save("diagram5_seed.npy", np.array(c_eff))

print("All diagrams finished.")
