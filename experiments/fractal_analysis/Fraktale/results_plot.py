import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# --------------------------------------------------------
# Modelle
# --------------------------------------------------------


def model(N, Dinf, N0):
    return Dinf * (1 - np.exp(-N / N0))


# optional für hohe d
def model_decay(N, Dinf, N0, decay):
    return Dinf * (1 - np.exp(-N / N0)) * np.exp(-decay * N)


# --------------------------------------------------------
# Daten laden
# --------------------------------------------------------

df = pd.read_csv("resultsN.csv")

dims = sorted(df["dim"].unique())

colors = ["blue", "red", "green", "magenta", "black", "cyan", "gray", "lightgray"]
markers = ["o", "^", "s", "+", "x", "v", "k", "g", "lg"]

plt.figure(figsize=(7, 5))

N0_list = []
Dinf_list = []


for i, dim in enumerate(dims):

    sub = df[df["dim"] == dim]
    grouped = sub.groupby("N")["D"]

    Ns = np.array(sorted(grouped.mean().index), dtype=float)
    means = grouped.mean().values
    stds = grouped.std().values

    plt.errorbar(Ns, means, yerr=stds, marker="o", color=colors[i], label=f"d={dim}")

    # Fit
    try:
        popt, _ = curve_fit(model, Ns, means, p0=[3, 1e6], maxfev=10000)
        Dinf, N0 = popt

        print(f"\nd={dim}")
        print("D_inf =", Dinf)
        print("N0    =", N0)

        Dinf_list.append(Dinf)
        N0_list.append(N0)

        Nfit = np.logspace(np.log10(min(Ns)), np.log10(max(Ns) * 2), 200)

    #        plt.plot(Nfit,model(Nfit,*popt),linestyle="--",color=colors[i])

    except Exception as e:
        print("Fit failed for dim", dim, e)


plt.xscale("log")
plt.xlabel("N")
plt.ylabel("Docc")
plt.legend()
# plt.title("Scaling with exponential saturation and rotational decay")
plt.tight_layout()
plt.show()


# --------------------------------------------------------
# N0 vs dimension
# --------------------------------------------------------

plt.figure()

plt.plot(dims[: len(N0_list)], N0_list, "o-")

plt.yscale("log")

plt.xlabel("dimension")
plt.ylabel("N0 (structure timescale)")
plt.title("Structure formation scale vs dimension")

plt.tight_layout()
plt.show()
