import matplotlib.pyplot as plt
import numpy as np

# Parameter space
alpha = np.linspace(0.01, 1.2, 400)  # memory relaxation
hbar_eff = np.logspace(-3, 0, 400)  # emergent action scale
A, H = np.meshgrid(alpha, hbar_eff)

# Model parameters (dimensionless)
eta = 1.0
lambda_tilde = 1.0

# Finite-memory correction (discrete effect)
f_alpha = A / (1.0 + A)

# Dimensionless control parameter
R = (eta * lambda_tilde / H) * f_alpha

# Plot
fig = plt.figure(figsize=(7, 5))
levels = np.logspace(-1, 2, 40)
cf = plt.contourf(A, H, R, levels=levels, norm="log", cmap="viridis")
plt.colorbar(cf, label=r"$R = (\gamma\lambda/D)\,f(\alpha)$")

# Regime boundaries
plt.contour(A, H, R, levels=[0.3], colors="white", linestyles="--")
plt.contour(A, H, R, levels=[1.0], colors="white", linestyles="-")
plt.contour(A, H, R, levels=[3.0], colors="white", linestyles=":")

# Time-emergence marker
plt.axvline(0.25, color="white", linewidth=1.5, linestyle="dashdot")

# Annotations
plt.text(0.05, 5e-1, "timeless\n(no continuum)", color="white", ha="left", va="center")
plt.text(0.6, 3e-1, "quantum-like\n(fluctuation dominated)", color="white", ha="center")
plt.text(0.6, 5e-3, "classical\n(relaxation dominated)", color="white", ha="center")

plt.xlabel(r"memory relaxation $\alpha$")
plt.ylabel(r"emergent action scale $\hbar_{\mathrm{eff}} \sim \varepsilon^2 \alpha$")
plt.yscale("log")

plt.title(
    "Emergence of Time and Classicality\nin the $(\\alpha, \\hbar_{\\rm eff})$ Plane"
)

plt.tight_layout()
plt.show()

fig.savefig("fig_alpha_hbar_eff_corrected.pdf", bbox_inches="tight")
