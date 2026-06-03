import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------
# Fundamental parameters (dimensionless units)
# -------------------------------------------------
eta = 1.0  # memory drift strength
lam = 1.0  # Hessian eigenvalue
eps = 0.3  # stochastic step scale
T_obs = 50.0  # effective observation time

# Emergent physical parameters
m = 1.0  # effective mass
sigma = 1.0  # knot width

# -------------------------------------------------
# Alpha range
# -------------------------------------------------
alphas = np.logspace(-5, 0, 400)

# -------------------------------------------------
# Mean relaxation rate (drift)
# -------------------------------------------------
Gamma = eta * lam * alphas

# -------------------------------------------------
# Fluctuations of measured relaxation rate
# -------------------------------------------------
D = eps**2 * alphas
Delta_Gamma = np.sqrt(D / T_obs)

# -------------------------------------------------
# Quantum-mechanical reference scale
# -------------------------------------------------
hbar_eff = eps**2 * alphas
Gamma_QM = hbar_eff / (m * sigma**2)

# -------------------------------------------------
# Regime boundaries (Gamma ~ DeltaGamma)
# -------------------------------------------------
ratio = Gamma / Delta_Gamma

alpha_micro = alphas[ratio < 0.5]
alpha_trans = alphas[(ratio >= 0.5) & (ratio <= 2.0)]
alpha_macro = alphas[ratio > 2.0]

# -------------------------------------------------
# Plot
# -------------------------------------------------
fig = plt.figure(figsize=(8, 5))

# Regime shading
plt.axvspan(
    alpha_micro.min(),
    alpha_micro.max(),
    color="#4C72B0",
    alpha=0.15,
    label="quantum-like",
)
plt.axvspan(
    alpha_trans.min(),
    alpha_trans.max(),
    color="#DD8452",
    alpha=0.15,
    label="transition",
)
plt.axvspan(
    alpha_macro.min(), alpha_macro.max(), color="#55A868", alpha=0.15, label="classical"
)

# Mean drift
plt.loglog(
    alphas,
    Gamma,
    "k-",
    linewidth=2,
    label=r"$\langle \Gamma \rangle = \eta\lambda\alpha$",
)

# Fluctuation envelope
plt.fill_between(
    alphas,
    np.maximum(Gamma - Delta_Gamma, 1e-6),
    Gamma + Delta_Gamma,
    color="gray",
    alpha=0.4,
    label=r"$\Gamma \pm \Delta\Gamma$",
)

# Quantum mechanical reference
plt.loglog(
    alphas,
    Gamma_QM,
    "r--",
    linewidth=2,
    label=r"$\Gamma_{\rm QM}=\hbar_{\rm eff}/(m\sigma^2)$",
)

# Labels
plt.xlabel(r"memory relaxation rate $\alpha$")
plt.ylabel(r"relaxation scale $\Gamma$")
plt.title("Emergent classicality from memory-driven dynamics")

plt.legend(frameon=False)
plt.grid(True, which="both", linestyle=":")
plt.tight_layout()
plt.show()

fig.savefig("fig_Gamma_alpha.pdf", bbox_inches="tight")
