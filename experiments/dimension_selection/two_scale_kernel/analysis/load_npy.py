import matplotlib.pyplot as plt
import numpy as np

dims = np.arange(2, 12)

stab = np.load("stab_partial.npy")

mean = stab.mean(axis=0)
std = stab.std(axis=0)

# -------------------------
# plot
# -------------------------

plt.figure(figsize=(7, 5))

plt.errorbar(dims, mean, yerr=std, fmt="o-", capsize=4)

plt.xlabel("dimension")
plt.ylabel("relative orbit fluctuation (σ_r / ⟨r⟩)")

plt.tight_layout()
plt.show()
