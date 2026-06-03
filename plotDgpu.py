import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")  # Kein GUI-Backend

alpha_vals = np.logspace(-3, 0, 20)
eta_vals   = np.logspace(-1, 1, 20)

data = np.load("progress_gpu.npz", allow_pickle=True)
D_spec = data["D_spec"]
D_cov = data["D_cov"]
R2_map = data["R2_map"]
print("Fortschritt geladen.")

alpha_vals = np.logspace(-3, 0, 20)
eta_vals   = np.logspace(-1, 1, 20)

# Plot 1: Spectral dimension
plt.figure()
plt.imshow(D_spec, origin="lower",
           extent=[eta_vals[0], eta_vals[-1],
                   alpha_vals[0], alpha_vals[-1]],
           aspect="auto")
#plt.xscale("log")
#plt.yscale("log")
plt.xlabel("eta")
plt.ylabel("alpha")
plt.colorbar(label="d_spec")
plt.tight_layout()
plt.savefig("heatmap_spectral_dimension_gpu_lin.pdf")
plt.close()

# Plot 2: Covariance dimension
plt.figure()
plt.imshow(D_cov, origin="lower",
           extent=[eta_vals[0], eta_vals[-1],
                   alpha_vals[0], alpha_vals[-1]],
           aspect="auto")
#plt.xscale("log")
#plt.yscale("log")
plt.xlabel("eta")
plt.ylabel("alpha")
plt.colorbar(label="d_cov")
plt.tight_layout()
plt.savefig("heatmap_covariance_dimension_gpu_lin.pdf")
plt.close()

# Plot 3: Fit quality
plt.figure()
plt.imshow(R2_map, origin="lower",
           extent=[eta_vals[0], eta_vals[-1],
                   alpha_vals[0], alpha_vals[-1]],
           aspect="auto")
#plt.xscale("log")
#plt.yscale("log")
plt.xlabel("eta")
plt.ylabel("alpha")
plt.colorbar(label="R2 fit quality")
plt.tight_layout()
plt.savefig("heatmap_fit_quality_gpu_lin.pdf")
plt.close()
