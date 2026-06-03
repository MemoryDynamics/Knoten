# Compute effective lambda (Hessian proxy) and visualize trajectory
# Separate plots, no custom styles

import matplotlib.pyplot as plt
import numpy as np

# --- Parameters ---
alpha = 0.0005
eta = 0.2
sigma = 0.5
epsilon = 0.02
N = 100000
window = 20000

tau_p = 1 / alpha

d = 3
max_memory = int(1 / alpha)
x = np.zeros((N, d))
memory_positions = []


def grad_rho(x_current):
    if len(memory_positions) == 0:
        return np.zeros(d)
    centers = np.array(memory_positions)
    diff = x_current - centers
    weights = np.exp(-np.sum(diff**2, axis=1) / (2 * sigma**2))
    grad = np.sum((diff / (sigma**2)) * weights[:, None], axis=0)
    return grad


# --- Simulation ---
for n in range(1, N):
    force = grad_rho(x[n - 1])
    noise = epsilon * np.random.normal(size=d)
    x[n] = x[n - 1] + noise - eta * force

    if np.random.rand() < alpha:
        memory_positions.append(x[n].copy())
        if len(memory_positions) > max_memory:
            memory_positions.pop(0)

# --- Analysis window ---
x_last = x[-window:]

cov = np.cov(x_last.T)
eigvals_cov, _ = np.linalg.eigh(cov)

lambda_est = 1 / eigvals_cov
lambda_max = np.max(lambda_est)

Xi = eta * tau_p * lambda_max

# --- Plot trajectory ---
plt.figure()
ax = plt.axes(projection="3d")
ax.plot3D(x_last[:, 0], x_last[:, 1], x_last[:, 2], linewidth=0.2)
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.set_zlabel("x3")
plt.title("Trajectory (last window)")
plt.show()

# --- Plot lambda spectrum ---
plt.figure()
plt.bar(np.arange(1, 4), lambda_est)
plt.xlabel("Mode index")
plt.ylabel("Estimated lambda")
plt.title("Estimated Hessian Eigenvalues")
plt.show()

print(Xi)
