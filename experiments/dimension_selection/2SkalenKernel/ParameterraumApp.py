import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# PARAMETERS
# -----------------------------

kappa = 3
beta = 0.2
L = 1.0
# kappa = 0.1      # sigma2/sigma1
# beta  = 1.0      # B/A
# L     = 0.1      # angular  momentum parameter
r0 = 5  # Abstand vom zweiten Teilchen

r = np.linspace(0.5, 10, 2000)

# -----------------------------
# POTENTIAL
# -----------------------------

U = np.exp(-(r**2) / 2) - beta * np.exp(-(r**2) / (2 * kappa**2))

Ueff = U + L**2 / (2 * r**2)

# -----------------------------
# DERIVATIVES
# -----------------------------

dr = r[1] - r[0]

dU = np.gradient(Ueff, dr)
d2U = np.gradient(dU, dr)

# find minima
mins = np.where((dU[:-1] < 0) & (dU[1:] > 0))[0]

# -----------------------------
# PLOT
# -----------------------------

plt.figure(figsize=(7, 5))

plt.plot(r, U, label="U(r)")
plt.plot(r, Ueff, label="U_eff(r)")

for m in mins:
    plt.axvline(r[m], linestyle="--", color="grey")

plt.xlabel("r")
plt.ylabel("potential")
plt.title(f"kappa={kappa}, beta={beta}, L={L}")

plt.legend()
plt.tight_layout()
plt.show()

dims = [2, 3, 4, 5, 6]

plt.figure(figsize=(7, 5))

for d in dims:
    Ueff = U + (d - 1) * L**2 / (2 * r**2)
    plt.plot(r, Ueff, label=f"d={d}")

plt.plot(r, U, "k--", label="U(r)")
plt.legend()
plt.xlabel("r")
plt.ylabel("U_eff")
plt.title(f"kappa={kappa}, beta={beta}, L={L}")
plt.show()
