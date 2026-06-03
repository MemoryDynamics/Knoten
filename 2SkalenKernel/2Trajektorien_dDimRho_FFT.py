import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import irfft, rfft

# -------------------------
# parameters
# -------------------------

dims = np.arange(2, 12)

runs = 10
T = 80000

alpha = 0.02

eta = 0.05
Xi = 200

eps = np.sqrt(2 * eta / Xi)

sigma1 = 1.0
sigma2 = 3.0

A = 1.0
B = 0.2

# radial grid
rmax = 20
nr = 400

r = np.linspace(0, rmax, nr)
dr = r[1] - r[0]

# -------------------------
# kernel and FFT precompute
# -------------------------


def kernel(r_):
    g1 = np.exp(-r_ * r_ / (2 * sigma1 * sigma1))
    g2 = np.exp(-r_ * r_ / (2 * sigma2 * sigma2))
    return A * g1 - B * g2


kernel_vals = kernel(r)
kernel_fft = rfft(kernel_vals)


def potential(rho):
    # Faltung via FFT: phi = K * rho
    return irfft(rfft(rho) * kernel_fft, n=nr) * dr


# -------------------------
# gradient
# -------------------------


def grad(phi):
    g = np.zeros_like(phi)
    g[1:-1] = (phi[2:] - phi[:-2]) / (2 * dr)
    # g[0] und g[-1] bleiben 0 (bewusst so gelassen)
    return g


# -------------------------
# deposition (vektorisiert)
# -------------------------


def deposit(rho, ri):
    rho += kernel(abs(r - ri))
    # rho += np.exp(-(r - ri) ** 2 / (2 * sigma1 ** 2))


# -------------------------
# simulation
# -------------------------


def simulate(d, recompute_potential_every=1):
    x1 = np.zeros(d)
    x2 = np.zeros(d)
    x2[0] = 1.0

    x1_prev = x1.copy()
    x2_prev = x2.copy()

    rho = np.zeros(nr)

    angular = []

    phi = potential(rho)
    gphi = grad(phi)

    for t in range(T):

        # ggf. Potential nicht in jedem Schritt neu berechnen
        if t % recompute_potential_every == 0:
            phi = potential(rho)
            gphi = grad(phi)

        rvec = x1 - x2
        dist = np.linalg.norm(rvec)

        idx = min(nr - 1, int(dist / dr))

        if dist > 1e-6:
            force = -gphi[idx] * rvec / dist
        else:
            force = np.zeros_like(rvec)

        noise1 = eps * np.random.normal(size=d)
        noise2 = eps * np.random.normal(size=d)

        x1 += eta * force + noise1
        x2 -= eta * force + noise2

        # memory decay
        rho *= 1 - alpha

        # neue Distanz und Ablagerung
        dist = np.linalg.norm(x1 - x2)
        deposit(rho, dist)

        if t > 10:
            v1 = x1 - x1_prev
            v2 = x2 - x2_prev

            rvec = x1 - x2
            v = v1 - v2

            # L^2 = Sum_{i<j} (r_i v_j - r_j v_i)^2
            L2 = 0.0
            for i in range(d):
                for j in range(i + 1, d):
                    L = rvec[i] * v[j] - rvec[j] * v[i]
                    L2 += L * L

            angular.append(np.sqrt(L2))

        x1_prev = x1.copy()
        x2_prev = x2.copy()

    return np.mean(angular)


# -------------------------
# dimension scan
# -------------------------

stab = np.zeros((runs, len(dims)))

for rseed in range(runs):
    np.random.seed(rseed)

    for i, d in enumerate(dims):
        stab[rseed, i] = simulate(d, recompute_potential_every=1)

    # optional: Zwischenspeichern nach jedem Run
    np.save("stab_partial.npy", stab[: rseed + 1])

mean = stab.mean(axis=0)
std = stab.std(axis=0)

# -------------------------
# plot
# -------------------------

plt.figure(figsize=(7, 5))
plt.errorbar(dims, mean, yerr=std, fmt="o-", capsize=4)
plt.xlabel("dimension")
plt.ylabel("rotation strength")
plt.tight_layout()
plt.show()
