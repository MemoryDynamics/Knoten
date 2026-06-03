import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


# --------------------------------------------------------
# scaling model
# --------------------------------------------------------
# def scaling_model(N, Dinf, c, beta):
#    return Dinf - c * N**(-beta)
def scaling_model(N, D_inf, N0):
    return D_inf * (1 - np.exp(-N / N0))


def model_full(N, Dinf, N0, Nr):
    return Dinf * (1 - np.exp(-N / N0)) * np.exp(-N / Nr)


# --------------------------------------------------------
# load data
# --------------------------------------------------------
df = pd.read_csv("resultsN.csv")
print(df.head())

# --------------------------------------------------------
# group by dimension
# --------------------------------------------------------
dims = sorted(df["dim"].unique())
plt.figure(figsize=(7, 5))
markers = ["o", "^", "s", "+", "x", "v", "k"]
colors = ["blue", "red", "green", "magenta", "black", "cyan", "yellow"]
for i, dim in enumerate(dims):
    sub = df[df["dim"] == dim]
    grouped = sub.groupby("N")["D"]
    Ns = np.array(sorted(grouped.mean().index), dtype=float)
    means = grouped.mean().values
    stds = grouped.std().values
    maxs = grouped.max().values

    # plot data
    plt.errorbar(
        Ns,
        means,
        yerr=stds,
        marker=markers[i],
        color=colors[i],
        label=f"d={dim}",
        capsize=4,
    )

    # ----------------------------------------------------
    # scaling fit
    # ----------------------------------------------------
    try:
        popt, _ = curve_fit(model_full, Ns, means, p0=[3, 1e5, 1e6], maxfev=10000)
        Dinf, N0, Nr = popt
        print("\nDimension", dim)
        print("D_inf =", Dinf)
        print("N0  =", N0)
        print("Nr  =", Nr)
        Nfit = np.logspace(np.log10(min(Ns)), np.log10(max(Ns) * 2), 200)
        plt.plot(Nfit, model_full(Nfit, *popt), color=colors[i], linestyle="--")
    except Exception as e:
        print("Fit failed for dim", dim)
        print(e)


# --------------------------------------------------------
# plot
# --------------------------------------------------------
plt.xscale("log")
plt.xlabel("N")
plt.ylabel("Docc")
plt.title("Finite-size scaling of fractal dimension")
plt.legend()
plt.tight_layout()
plt.show()
