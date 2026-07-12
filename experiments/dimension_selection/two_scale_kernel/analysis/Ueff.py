import matplotlib.pyplot as plt
import numpy as np

# -------------------------
# parameters
# -------------------------

sigma1 = 1.0
sigma2 = 3.0

A = 1.0
B = 0.2

l = 3

r = np.linspace(0.1, 0.5, 500)

# -------------------------
# kernel potential
# -------------------------


def phi(r):

    return A * np.exp(-(r**2) / (2 * sigma1**2)) - B * np.exp(-(r**2) / (2 * sigma2**2))


# -------------------------
# dimensions
# -------------------------

d_list = np.arange(2, 10)

U = np.zeros((len(d_list), len(r)))

for i, d in enumerate(d_list):

    centrifugal = l * (l + d - 2) / (2 * r**2)

    U[i] = phi(r) + centrifugal

# -------------------------
# plot
# -------------------------

plt.figure(figsize=(8, 4))

plt.imshow(
    U,
    aspect="auto",
    origin="lower",
    extent=[r.min(), r.max(), d_list.min(), d_list.max()],
    cmap="viridis",
)

plt.xlabel("r")
plt.ylabel("dimension d")

plt.title("Effective potential U_eff(r,d)")

plt.colorbar()

plt.show()
