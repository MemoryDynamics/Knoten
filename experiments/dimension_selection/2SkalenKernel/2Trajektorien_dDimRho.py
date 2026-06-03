import matplotlib.pyplot as plt
import numpy as np

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
# kernel
# -------------------------


def kernel(r):

    g1 = np.exp(-r * r / (2 * sigma1 * sigma1))
    g2 = np.exp(-r * r / (2 * sigma2 * sigma2))

    return A * g1 - B * g2


# -------------------------
# convolution Φ = K * ρ
# -------------------------


def potential(rho):
    phi = np.zeros_like(rho)
    for i in range(nr):
        s = 0
        for j in range(nr):
            rij = abs(r[i] - r[j])
            s += kernel(rij) * rho[j]
        phi[i] = s * dr
    return phi


# -------------------------
# gradient
# -------------------------
def grad(phi):
    g = np.zeros_like(phi)
    g[1:-1] = (phi[2:] - phi[:-2]) / (2 * dr)
    return g


# -------------------------
# deposition
# -------------------------


def deposit(rho, ri):

    for i in range(nr):

        rho[i] += np.exp(-((r[i] - ri) ** 2) / (2 * sigma1**2))


# -------------------------
# simulation
# -------------------------


def simulate(d):

    x1 = np.zeros(d)
    x2 = np.zeros(d)

    x2[0] = 1.0

    x1_prev = x1.copy()
    x2_prev = x2.copy()

    rho = np.zeros(nr)

    angular = []

    for t in range(T):

        phi = potential(rho)
        gphi = grad(phi)

        rvec = x1 - x2
        dist = np.linalg.norm(rvec)

        idx = min(nr - 1, int(dist / dr))

        force = -gphi[idx] * rvec / dist if dist > 1e-6 else 0

        noise1 = eps * np.random.normal(size=d)
        noise2 = eps * np.random.normal(size=d)

        x1 += eta * force + noise1
        x2 -= eta * force + noise2

        rho *= 1 - alpha

        dist = np.linalg.norm(x1 - x2)

        deposit(rho, dist)

        if t > 10:

            v1 = x1 - x1_prev
            v2 = x2 - x2_prev

            rvec = x1 - x2
            v = v1 - v2

            L2 = 0

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

        stab[rseed, i] = simulate(d)


mean = stab.mean(axis=0)
std = stab.std(axis=0)

# -------------------------
# plot
# -------------------------

plt.figure(figsize=(7, 5))

plt.errorbar(dims, mean, yerr=std, fmt="o-", capsize=4)

plt.xlabel("dimension")
plt.ylabel("rotation strength")

plt.show()
