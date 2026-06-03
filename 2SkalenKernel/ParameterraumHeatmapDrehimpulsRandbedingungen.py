import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

# parameter ranges
kappa_vals = np.linspace(0.9, 1.2, 80)
beta_vals = np.linspace(0, 1.5, 80)

r = np.linspace(0.3, 12, 4000)

l = 23
d = 3
fac = l * (l + d - 2) / 2

Fmax_map = np.zeros((len(beta_vals), len(kappa_vals)))

for i, beta in enumerate(beta_vals):
    for j, kappa in enumerate(kappa_vals):

        U = np.exp(-(r**2) / 2) - beta * np.exp(-(r**2) / (2 * kappa**2))

        F = r**fac * U

        Fmax = np.max(F)

        Fmax_map[i, j] = Fmax

plt.figure(figsize=(7, 5))

plt.imshow(
    Fmax_map,
    origin="lower",
    extent=[kappa_vals[0], kappa_vals[-1], beta_vals[0], beta_vals[-1]],
    aspect="auto",
    norm=LogNorm(),
)

# plt.scatter(x, y, c=Z, norm=LogNorm(vmin=Z.min(), vmax=Z.max()), cmap='F_max')
# plt.colorbar(label="F_max")
# plt.set_yscale('log')  # optional, falls explizit gewünscht

plt.xlabel("kappa")
plt.ylabel("beta")
plt.title("Kernel capacity for high angular momentum")

plt.show()
