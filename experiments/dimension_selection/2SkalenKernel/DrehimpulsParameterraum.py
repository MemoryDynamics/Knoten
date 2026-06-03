import matplotlib.pyplot as plt
import numpy as np

# parameter ranges
kappa_vals = np.linspace(1.02, 10, 120)
beta_vals = np.linspace(0.05, 20, 120)

# spatial dimensions to test
d_values = np.arange(2, 8)

# radial grid
r = np.logspace(-2, 1.2, 6000)

# storage
lmax_map = {}

for d in d_values:

    LMAX = np.zeros((len(beta_vals), len(kappa_vals)))

    for i, beta in enumerate(beta_vals):
        for j, kappa in enumerate(kappa_vals):
            # two-scale kernel potential
            U = np.exp(-(r**2) / 2) - beta * np.exp(-(r**2) / (2 * kappa**2))
            dU = -r * np.exp(-(r**2) / 2) + (beta / kappa**2) * r * np.exp(
                -(r**2) / (2 * kappa**2)
            )

            # centrifugal-weighted function
            F = r**3 * dU
            Fmax = np.max(F)
            if Fmax <= 0:
                lmax = 0
            else:  # solve l(l+d-2) <= Fmax
                disc = (d - 2) ** 2 + 4 * Fmax
                lmax = int((np.sqrt(disc) - (d - 2)) / 2)

            LMAX[i, j] = max(lmax, 0)

    lmax_map[d] = LMAX

# plotting
plt.plot(r, F)

fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()

for idx, d in enumerate(d_values):

    ax = axes[idx]

    im = ax.imshow(
        lmax_map[d],
        origin="lower",
        extent=[kappa_vals[0], kappa_vals[-1], beta_vals[0], beta_vals[-1]],
        aspect="auto",
    )

    ax.set_title(f"d = {d}")
    ax.set_xlabel("kappa")
    ax.set_ylabel("beta")

fig.colorbar(im, ax=axes, label="l_max")

# plt.tight_layout()
plt.show()
