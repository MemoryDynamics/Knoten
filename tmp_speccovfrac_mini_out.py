import numpy as np
from numpy.random import normal
import time

# small performance measurement

d = 7
N = 2000

epsilon = 0.03
eta = 0.15
alpha = 0.002
sigma_rep = 1.0
sigma_att = 3.0
A_rep = 1.0
B_att = 0.35
memory_horizon = int(6 / alpha)


def grad_double_kernel(x, memory):
    g = np.zeros_like(x)
    for w, y in memory:
        r = x - y
        r2 = np.dot(r, r)
        rep = A_rep * np.exp(-r2/(2*sigma_rep**2)) / sigma_rep**2
        att = B_att * np.exp(-r2/(2*sigma_att**2)) / sigma_att**2
        g += w * (rep - att) * r
    return g

x = np.zeros(d)
memory = []
start = time.perf_counter()
for n in range(N):
    g = grad_double_kernel(x, memory)
    x += epsilon*normal(size=d) - eta*g
    memory = [(w*(1-alpha), y) for w,y in memory]
    memory.append((alpha, x.copy()))
    if len(memory) > memory_horizon:
        memory.pop(0)
end = time.perf_counter()
with open('mini_results.txt', 'w') as f:
    f.write(f'done {N} steps in {end-start} s\n')
    f.write(f'avg {N/(end-start)} steps/s\n')
