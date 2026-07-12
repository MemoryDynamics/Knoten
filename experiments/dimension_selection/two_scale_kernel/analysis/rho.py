import matplotlib.pyplot as plt
import numpy as np

# -------------------------
# parameters
# -------------------------

T = 150000
dt = 1.0

eps = 0.3
alpha = 0.01
gamma = alpha / dt

nr = 256
rmax = 20
r = np.linspace(0, rmax, nr)
dr = r[1] - r[0]

sigma = 1.0

# -------------------------
# kernel
# -------------------------


def kernel(dist):
    return np.exp(-(dist**2) / (2 * sigma**2))


# -------------------------
# fields
# -------------------------

rho = np.zeros(nr)

x = 0.0

lap_list = []
lhs_list = []

# -------------------------
# laplacian
# -------------------------


def laplacian(f):

    lap = np.zeros_like(f)

    lap[1:-1] = (f[2:] - 2 * f[1:-1] + f[:-2]) / dr**2

    return lap


# -------------------------
# simulation
# -------------------------

for t in range(T):

    rho_old = rho.copy()

    # random walk
    x += eps * np.random.randn()

    # deposit memory
    rho += kernel(np.abs(r - x))

    # forgetting
    rho *= 1 - alpha

    # compute derivatives
    lap = laplacian(rho)

    dt_rho = (rho - rho_old) / dt

    lhs = dt_rho + gamma * rho

    lap_list.append(lap.copy())
    lhs_list.append(lhs.copy())

# flatten arrays
lap_list = np.array(lap_list).flatten()
lhs_list = np.array(lhs_list).flatten()

# -------------------------
# plot
# -------------------------

plt.figure(figsize=(6, 6))
plt.scatter(lap_list, lhs_list, s=1, alpha=0.1)

plt.xlabel("∇²ρ")
plt.ylabel("∂tρ + γρ")

plt.title("Diffusion emergence")

plt.show()
