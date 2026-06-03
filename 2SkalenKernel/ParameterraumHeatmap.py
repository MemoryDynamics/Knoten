import matplotlib.pyplot as plt
import numpy as np

# --------------------------------
# parameters (already reduced)
# --------------------------------

kappa = 3.0
beta = 0.2

# r grid
r = np.linspace(0.3, 10, 4000)

# base potential
U = np.exp(-(r**2) / 2) - beta * np.exp(-(r**2) / (2 * kappa**2))

dr = r[1] - r[0]

# dimension / angular momentum ranges
dims = np.arange(2, 9)
ls = np.arange(1, 10)

# result matrices
rmin_map = np.zeros((len(ls), len(dims)))
stab_map = np.zeros((len(ls), len(dims)))

for i, l in enumerate(ls):
    for j, d in enumerate(dims):

        # centrifugal barrier
        Ueff = U + l * (l + d - 2) / (2 * r**2)

        # derivatives
        dU = np.gradient(Ueff, dr)
        d2U = np.gradient(dU, dr)

        # minima detection
        mins = np.where((dU[:-1] < 0) & (dU[1:] > 0))[0]

        if len(mins) > 0:
            m = mins[0]
            r0 = r[m]

            if d2U[m] > 0:
                stab_map[i, j] = 1
                rmin_map[i, j] = r0
            else:
                rmin_map[i, j] = np.nan
        else:
            rmin_map[i, j] = np.nan

# --------------------------------
# plotting
# --------------------------------

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

im0 = ax[0].imshow(
    stab_map, origin="lower", aspect="auto", extent=[dims[0], dims[-1], ls[0], ls[-1]]
)

ax[0].set_title("Orbit stability")
ax[0].set_xlabel("dimension d")
ax[0].set_ylabel("angular momentum l")

fig.colorbar(im0, ax=ax[0])


im1 = ax[1].imshow(
    rmin_map, origin="lower", aspect="auto", extent=[dims[0], dims[-1], ls[0], ls[-1]]
)

ax[1].set_title("Orbit radius r₀")
ax[1].set_xlabel("dimension d")
ax[1].set_ylabel("angular momentum l")

fig.colorbar(im1, ax=ax[1])

plt.tight_layout()
plt.show()
