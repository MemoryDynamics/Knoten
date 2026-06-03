import matplotlib.pyplot as plt
import numpy as np

# parameters
Gamma = 1.0
D = 0.1
dt = 0.01
steps = 50000
n_traj = 2000

# simulate OU trajectories
x = np.zeros((n_traj, steps))
for t in range(steps - 1):
    x[:, t + 1] = (
        x[:, t] - Gamma * x[:, t] * dt + np.sqrt(2 * D * dt) * np.random.randn(n_traj)
    )

# final distribution
x_final = x[:, -1]

# theoretical ground state
xs = np.linspace(-2, 2, 400)
rho_stat = np.sqrt(Gamma / (2 * np.pi * D)) * np.exp(-Gamma * xs**2 / (2 * D))

# plot
fig = plt.figure(figsize=(6, 4))
plt.hist(x_final, bins=80, density=True, alpha=0.6, label="OU simulation")
plt.plot(xs, rho_stat, "r-", lw=2, label="stationary Gaussian")
plt.xlabel("x")
plt.ylabel("density")
plt.title("OU limit → quantum ground state")
plt.legend()
plt.tight_layout()
plt.show()
fig.savefig("fig_OUlimit.pdf", bbox_inches="tight")
