import numpy as np
import matplotlib.pyplot as plt
from numba import njit

# -----------------------------
# PARAMETERS
# -----------------------------

dims = np.arange(2,12)

runs = 10
T = 120000

alpha = 0.02

eta = 0.05
Xi = 200

eps = np.sqrt(2*eta/Xi)

# kernel parameters
sigma1 = 1.0
sigma2 = 3.0

A = 1.0
B = 0.2

grid_size = 128
box = 20.0

dx = box/grid_size
kernel_cut = 5*sigma2

# -----------------------------
# TWO SCALE KERNEL
# -----------------------------

@njit
def kernel(r2):

    g1 = np.exp(-r2/(2*sigma1*sigma1))
    g2 = np.exp(-r2/(2*sigma2*sigma2))

    return A*g1 - B*g2


# -----------------------------
# DEPOSITION
# -----------------------------

@njit
def deposit(grid,x):

    g = grid.shape[0]

    ix = int((x[0]+box/2)/dx)
    iy = int((x[1]+box/2)/dx)

    rmax = int(kernel_cut/dx)

    for i in range(ix-rmax,ix+rmax+1):

        if 0 <= i < g:

            px = -box/2 + i*dx
            dx1 = x[0]-px

            for j in range(iy-rmax,iy+rmax+1):

                if 0 <= j < g:

                    py = -box/2 + j*dx
                    dy1 = x[1]-py

                    r2 = dx1*dx1 + dy1*dy1

                    if r2 < kernel_cut*kernel_cut:

                        grid[i,j] += kernel(r2)


# -----------------------------
# GRADIENT
# -----------------------------

@njit
def gradient(grid,x):

    g = grid.shape[0]

    ix = int((x[0]+box/2)/dx)
    iy = int((x[1]+box/2)/dx)

    ix = max(1,min(g-2,ix))
    iy = max(1,min(g-2,iy))

    gx = (grid[ix+1,iy]-grid[ix-1,iy])/(2*dx)
    gy = (grid[ix,iy+1]-grid[ix,iy-1])/(2*dx)

    return gx,gy


# -----------------------------
# SIMULATION
# -----------------------------

def simulate(d):

    x1 = np.zeros(d)
    x2 = np.zeros(d)

    x2[0] = 1.0

    x1_prev = x1.copy()
    x2_prev = x2.copy()

    grid = np.zeros((grid_size,grid_size))

    angular = []

    for t in range(T):

        # gradient BEFORE deposition
        gx1,gy1 = gradient(grid,x1[:2])
        gx2,gy2 = gradient(grid,x2[:2])

        noise1 = eps*np.random.normal(size=d)
        noise2 = eps*np.random.normal(size=d)

        # move particles
        x1[:2] += -eta*np.array([gx1,gy1]) + noise1[:2]
        x2[:2] += -eta*np.array([gx2,gy2]) + noise2[:2]

        # memory decay
        grid *= (1-alpha)

        # deposition
        deposit(grid,x1[:2])
        deposit(grid,x2[:2])

        # rotation measurement
        if t>10:

            v1 = x1[:2]-x1_prev[:2]
            v2 = x2[:2]-x2_prev[:2]

            r = x1[:2]-x2[:2]
            v = v1-v2

            L = r[0]*v[1]-r[1]*v[0]

            angular.append(np.abs(L))

        x1_prev = x1.copy()
        x2_prev = x2.copy()

    angular = np.array(angular)

    return np.mean(angular)


# -----------------------------
# DIMENSION SCAN
# -----------------------------

stability_runs = np.zeros((runs,len(dims)))

for r in range(runs):

    np.random.seed(r)

    for i,d in enumerate(dims):

        stab = simulate(d)

        stability_runs[r,i] = stab


stab_mean = stability_runs.mean(axis=0)
stab_std = stability_runs.std(axis=0)


# -----------------------------
# PLOT
# -----------------------------

plt.figure(figsize=(8,5))

plt.errorbar(dims,stab_mean,yerr=stab_std,
             fmt='o-',capsize=4)

plt.xlabel("dimension")
plt.ylabel("rotation strength")

plt.savefig("Rotation_vs_Dimension.pdf")

plt.show()