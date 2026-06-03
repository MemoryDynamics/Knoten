# Solid numerical scaffold + Diagrams 1–4
# -------------------------------------------------
# Minimal stochastic trajectory-with-memory model
# Produces:
# (1) Retarded response
# (2) Time-of-flight vs distance
# (3) Scaling of c_eff with memory length (alpha)
# (4) Operational light-cone plot
#
# IMPORTANT:
# - matplotlib only (no seaborn)
# - no explicit color choices
# - single plots per figure

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)

# -----------------------------
# Core parameters
# -----------------------------
eps = 0.3  # noise strength ε
eta = 0.8  # response coefficient η
alpha = 0.05  # memory update parameter α
T = 3000  # total steps
kick_time = 400  # time of impulse
threshold = 1e-3  # detection threshold


# -----------------------------
# Kernel and gradient
# -----------------------------
def K(r, sigma=1.0):
    return np.exp(-0.5 * (r / sigma) ** 2)


def gradK(r, sigma=1.0):
    return -(r / sigma**2) * np.exp(-0.5 * (r / sigma) ** 2)


# -----------------------------
# Simulation
# -----------------------------
def simulate_two_knots(L, alpha, T):
    xA = np.zeros(T)
    xB = np.zeros(T) + L

    histA = []
    response_B = np.zeros(T)

    for n in range(T - 1):
        gradPhiA = sum(gradK(xA[n] - h) for h in histA)
        gradPhiB = sum(gradK(xB[n] - h) for h in histA)

        xiA = eps * np.random.randn()
        xiB = eps * np.random.randn()

        xA[n + 1] = xA[n] + xiA - eta * gradPhiA
        xB[n + 1] = xB[n] + xiB - eta * gradPhiB

        if n == kick_time:
            xA[n + 1] += 2.0

        histA = [(1 - alpha) * h + alpha * xA[n + 1] for h in histA]
        histA.append(xA[n + 1])

        response_B[n] = abs(gradPhiB)

    return response_B


# -----------------------------
# Diagram 1: Retarded response
# -----------------------------
L0 = 10.0
resp = simulate_two_knots(L0, alpha, T)

fig1 = plt.figure()
plt.plot(resp)
plt.axvline(kick_time)
plt.xlabel("update index n")
plt.ylabel("response at B")
plt.title("Diagram 1: Retarded response")
plt.show()

# -----------------------------
# Diagram 2: Time-of-flight vs distance
# -----------------------------
Ls = np.linspace(5, 25, 6)
onsets = []

for L in Ls:
    resp = simulate_two_knots(L, alpha, T)
    idx = np.where(resp > threshold)[0]
    onsets.append(idx[0] - kick_time if len(idx) > 0 else np.nan)

plt.figure()
plt.plot(Ls, onsets, marker="o")
plt.xlabel("distance L")
plt.ylabel("onset delay Δn")
plt.title("Diagram 2: Time-of-flight")
plt.show()

# -----------------------------
# Diagram 3: Scaling of c_eff with alpha
# -----------------------------
alphas = np.array([0.02, 0.05, 0.1, 0.2])
c_eff = []

for a in alphas:
    resp = simulate_two_knots(L0, a, T)
    idx = np.where(resp > threshold)[0]
    c_eff.append(L0 / (idx[0] - kick_time) if len(idx) > 0 else np.nan)

plt.figure()
plt.plot(alphas, c_eff, marker="o")
plt.xlabel("alpha")
plt.ylabel("effective speed c_eff")
plt.title("Diagram 3: Scaling of c_eff with memory")
plt.show()

# -----------------------------
# Diagram 4: Operational light cone
# -----------------------------
points_t = []
points_L = []

for L in Ls:
    resp = simulate_two_knots(L, alpha, T)
    idx = np.where(resp > threshold)[0]
    if len(idx) > 0:
        points_t.append(idx[0] - kick_time)
        points_L.append(L)

plt.figure()
plt.scatter(points_t, points_L)
plt.xlabel("Δn (time delay)")
plt.ylabel("distance L")
plt.title("Diagram 4: Operational light cone")
plt.show()
