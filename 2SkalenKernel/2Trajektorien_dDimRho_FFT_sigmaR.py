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
# two-scale kernel
# -------------------------


def kernel(r_):

    g1 = np.exp(-r_ * r_ / (2 * sigma1 * sigma1))
    g2 = np.exp(-r_ * r_ / (2 * sigma2 * sigma2))

    return A * g1 - B * g2


kernel_vals = kernel(r)
kernel_fft = rfft(kernel_vals)

# -------------------------
# potential Φ = K * ρ
# -------------------------


def potential(rho):

    return irfft(rfft(rho) * kernel_fft, n=nr) * dr


# -------------------------
# gradient
# -------------------------


def grad(phi):

    g = np.zeros_like(phi)

    g[1:-1] = (phi[2:] - phi[:-2]) / (2 * dr)

    return g


# -------------------------
# deposition using kernel
# -------------------------


def deposit(rho, ri):

    rho += kernel(np.abs(r - ri))


# -------------------------
# simulation
# -------------------------


def simulate(d):

    x1 = np.zeros(d)
    x2 = np.zeros(d)

    x2[0] = 1.0

    rho = np.zeros(nr)

    r_values = []

    phi = potential(rho)
    gphi = grad(phi)

    for t in range(T):

        phi = potential(rho)
        gphi = grad(phi)

        rvec = x1 - x2
        dist = np.linalg.norm(rvec)

        idx = min(nr - 1, int(dist / dr))

        if dist > 1e-8:
            force = -gphi[idx] * rvec / dist
        else:
            force = np.zeros_like(rvec)

        noise1 = eps * np.random.normal(size=d)
        noise2 = eps * np.random.normal(size=d)

        x1 += eta * force + noise1
        x2 -= eta * force + noise2

        # memory decay
        rho *= 1 - alpha

        # deposit memory
        dist = np.linalg.norm(x1 - x2)
        deposit(rho, dist)

        if t > 1000:
            r_values.append(dist)

    r_values = np.array(r_values)

    mean_r = np.mean(r_values)
    std_r = np.std(r_values)

    stability = std_r / mean_r

    return stability


# -------------------------
# dimension scan
# -------------------------

stab = np.zeros((runs, len(dims)))

for rseed in range(runs):

    np.random.seed(rseed)

    for i, d in enumerate(dims):

        stab[rseed, i] = simulate(d)

    np.save("stab_partial.npy", stab[: rseed + 1])


mean = stab.mean(axis=0)
std = stab.std(axis=0)

# -------------------------
# plot
# -------------------------

plt.figure(figsize=(7, 5))

plt.errorbar(dims, mean, yerr=std, fmt="o-", capsize=4)

plt.xlabel("dimension")
plt.ylabel("relative orbit fluctuation (σ_r / ⟨r⟩)")

plt.tight_layout()
plt.show()
