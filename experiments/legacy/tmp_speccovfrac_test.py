import time

import numpy as np
from numpy.random import normal

d = 7
N = 100_000
sample_every = 500

epsilon = 0.03
eta = 0.15
alpha = 0.002
sigma_rep = 1.0
sigma_att = 3.0
A_rep = 1.0
B_att = 0.35
memory_horizon = int(6 / alpha)
window_cov = 4000


def grad_double_kernel(x, memory):
    g = np.zeros_like(x)
    for w, y in memory:
        r = x - y
        r2 = np.dot(r, r)
        rep = A_rep * np.exp(-r2 / (2 * sigma_rep**2)) / sigma_rep**2
        att = B_att * np.exp(-r2 / (2 * sigma_att**2)) / sigma_att**2
        g += w * (rep - att) * r
    return g


def covariance_dimension(points):
    if len(points) < 50:
        return np.nan
    pts = np.array(points)
    C = np.cov(pts.T)
    eig = np.linalg.eigvalsh(C)
    eig = eig[eig > 1e-12]
    p = eig / eig.sum()
    return np.exp(-np.sum(p * np.log(p)))


x = np.zeros(d)
memory = []
samples = []
D_cov = []
Ns = []

start = time.perf_counter()
for n in range(N):
    g = grad_double_kernel(x, memory)
    x += epsilon * normal(size=d) - eta * g
    memory = [(w * (1 - alpha), y) for w, y in memory]
    memory.append((alpha, x.copy()))
    if len(memory) > memory_horizon:
        memory.pop(0)
    if n % sample_every == 0:
        samples.append(x.copy())
        if len(samples) > window_cov:
            samples.pop(0)
        if len(samples) > 200:
            D_cov.append(covariance_dimension(samples))
            Ns.append(n)
    if n % 10000 == 0:
        print("n =", n)
end = time.perf_counter()
print("done", N, "steps in", end - start, "s")
print("computed", len(D_cov), "cov estimates, last", D_cov[-1] if D_cov else None)
