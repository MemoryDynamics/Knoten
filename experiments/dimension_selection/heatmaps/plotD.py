import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")  # Kein GUI-Backend

D = np.load("progress_c.npy", allow_pickle=True)
print("Shape:", D.shape)
print("Min:", D.min(), "Max:", D.max())

alpha_vals = np.logspace(-3, 0, 20)
eta_vals = np.logspace(-1, 1, 20)
plt.figure()
plt.imshow(
    D,
    origin="lower",
    extent=[eta_vals[0], eta_vals[-1], alpha_vals[0], alpha_vals[-1]],
    aspect="auto",
)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("eta")
plt.ylabel("alpha")
plt.colorbar(label="d_spec")
plt.tight_layout()
