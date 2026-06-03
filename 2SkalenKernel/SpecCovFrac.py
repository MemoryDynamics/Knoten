import numpy as np
from numpy.random import normal
import math

# ============================================================
# PARAMETERS (Paper II optimized)
# ============================================================

d = 7                      # embedding dimension
N = 150_000_000            # steps
sample_every = 2000        # diagnostics sampling

# dynamics
epsilon = 0.03
eta = 0.15
alpha = 0.002

# kernel (double Gaussian)
sigma_rep = 1.0
sigma_att = 3.0

A_rep = 1.0
B_att = 0.35

# memory truncation
memory_horizon = int(6 / alpha)

# diagnostics
window_spec = 2000
window_cov  = 4000


# ============================================================
# FAST DOUBLE KERNEL GRADIENT
# ============================================================

def grad_double_kernel(x, memory):

    g = np.zeros_like(x)

    for w, y in memory:

        r = x - y
        r2 = np.dot(r, r)

        # repulsive
        rep = A_rep * np.exp(-r2/(2*sigma_rep**2)) / sigma_rep**2

        # attractive
        att = B_att * np.exp(-r2/(2*sigma_att**2)) / sigma_att**2

        g += w * (rep - att) * r

    return g


# ============================================================
# FRACTAL DIMENSION (occupancy)
# ============================================================

def fractal_dimension(points):

    if len(points) < 100:
        return np.nan

    pts = np.array(points)
    mins = pts.min(0)
    maxs = pts.max(0)

    scales = np.logspace(-1, 1, 6)

    counts = []

    for s in scales:

        bins = ((pts - mins) / s).astype(int)
        counts.append(len(set(map(tuple,bins))))

    coeff = np.polyfit(np.log(scales), np.log(counts), 1)

    return -coeff[0]


# ============================================================
# COVARIANCE DIMENSION
# ============================================================

def covariance_dimension(points):

    if len(points) < 50:
        return np.nan

    pts = np.array(points)

    C = np.cov(pts.T)

    eig = np.linalg.eigvalsh(C)

    eig = eig[eig > 1e-12]

    p = eig / eig.sum()

    return np.exp(-np.sum(p*np.log(p)))


# ============================================================
# SPECTRAL DIMENSION (diffusion)
# ============================================================

def spectral_dimension(points):

    if len(points) < 100:
        return np.nan

    pts = np.array(points)

    D2 = ((pts[:,None,:]-pts[None,:,:])**2).sum(-1)

    eps = np.median(D2)

    K = np.exp(-D2/eps)

    w = np.linalg.eigvalsh(K)

    w = w[w>1e-8]

    return np.log(len(w)) / np.log(1/w.mean())


# ============================================================
# MAIN SIMULATION
# ============================================================

x = np.zeros(d)

memory = []
weight = 1.0

samples = []

D_occ = []
D_cov = []
D_spec = []
Ns = []

for n in range(N):

    # gradient
    g = grad_double_kernel(x, memory)

    # step
    x += epsilon*normal(size=d) - eta*g

    # update memory weights
    memory = [(w*(1-alpha), y) for w,y in memory]

    # add new point
    memory.append((alpha, x.copy()))

    # truncate memory
    if len(memory) > memory_horizon:
        memory.pop(0)

    # sampling
    if n % sample_every == 0:

        samples.append(x.copy())

        if len(samples) > window_cov:
            samples.pop(0)

        if len(samples) > 200:

            D_occ.append(fractal_dimension(samples))
            D_cov.append(covariance_dimension(samples))
            D_spec.append(spectral_dimension(samples))
            Ns.append(n)

        if n % 1_000_000 == 0:
            print("n =", n)

# ============================================================
# SAVE
# ============================================================

np.savez(
    "3D_emergence_double_kernel.npz",
    N = Ns,
    D_occ = D_occ,
    D_cov = D_cov,
    D_spec = D_spec
)