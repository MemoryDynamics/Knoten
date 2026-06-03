# Retry improved visualization: ratio of eigenvalues and regime boundaries in (alpha, epsilon)

import numpy as np
import matplotlib.pyplot as plt

# Parameter space
alpha = np.linspace(0, 1.2, 400)
epsilon = np.linspace(0.01, 1.2, 400)
A, E = np.meshgrid(alpha, epsilon)

sigma = 1.0

# Drift magnitude ~ alpha
v = A

# Eigenvalues
lambda_parallel = v**2 + (E**2)*(sigma**2)
lambda_perp = (E**2)*(sigma**2)

# Dimensionless anisotropy measure
R = lambda_parallel / lambda_perp  # = 1 + v^2/(epsilon^2)

fig=plt.figure()
levels = np.linspace(1, 15, 40)
cf = plt.contourf(A, E, R, levels=levels)
plt.colorbar(cf, label=r"$\lambda_\parallel / \lambda_\perp$")

# Regime boundaries
plt.contour(A, E, R, levels=[1.2], colors='white', linestyles='--')
plt.contour(A, E, R, levels=[3.0], colors='white', linestyles='-')
plt.contour(A, E, R, levels=[8.0], colors='white', linestyles=':')

plt.text(0.05, 0.9, "timeless /\n quantum like", color="white")
plt.text(0.45, 0.6, "transitional \nregime", color="white")
plt.text(0.8, 0.25, "classical \n spacetime", color="white")

plt.xlabel(r"memory relaxation $\alpha$")
plt.ylabel(r"stochastic displacement $\varepsilon$")
plt.title("Phase Space ($\\alpha$, $\\varepsilon$): Direction of Time as Eigenvalue Separation")

plt.show()

fig.savefig("fig_alpha.pdf", bbox_inches="tight")