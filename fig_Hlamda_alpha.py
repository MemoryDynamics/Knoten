import numpy as np
import matplotlib.pyplot as plt

eta = 1.0
lam = 1.0
eps = 0.2
T = 50.0   # effective observation time

alphas = np.logspace(-4, 0, 200)

Gamma = eta * lam * alphas
D = eps**2 * alphas

Delta_Gamma = np.sqrt(D / T)

fig = plt.figure(figsize=(7, 5))

plt.loglog(alphas, Gamma, 'k-', label=r'$\langle\Gamma\rangle$')
plt.fill_between(
    alphas,
    Gamma - Delta_Gamma,
    Gamma + Delta_Gamma,
    color='gray',
    alpha=0.4,
    label=r'fluctuations'
)

plt.xlabel(r'memory rate $\alpha$')
plt.ylabel(r'relaxation rate $\Gamma$')
plt.title("Emergent drift with microscopic uncertainty")
plt.legend()
plt.grid(True, which="both")
plt.tight_layout()
plt.show()

fig.savefig("fig_alpha_hbar_eff_corrected.pdf", bbox_inches="tight")
