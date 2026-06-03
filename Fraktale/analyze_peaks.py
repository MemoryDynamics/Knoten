import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# --------------------------------------------------
# load data
# --------------------------------------------------

df = pd.read_csv("resultsN.csv")

dims = sorted(df["dim"].unique())

colors = ["blue", "red", "green", "magenta", "black", "cyan", "gray", "lightgray"]

# --------------------------------------------------
# compute mean curves
# --------------------------------------------------

curves = {}

for dim in dims:

    sub = df[df["dim"] == dim]

    grouped = sub.groupby("N")["D"]

    Ns = np.array(sorted(grouped.mean().index), dtype=float)
    means = grouped.mean().values
    stds = grouped.std().values

    curves[dim] = (Ns, means, stds)

# --------------------------------------------------
# plot original
# --------------------------------------------------

plt.figure(figsize=(7, 5))

for i, dim in enumerate(dims):

    Ns, means, stds = curves[dim]

    plt.errorbar(Ns, means, yerr=stds, marker="o", color=colors[i], label=f"d={dim}")

plt.xscale("log")
plt.xlabel("N")
plt.ylabel("Docc")
plt.legend()
plt.title("Fractal dimension scaling")
plt.tight_layout()
plt.show()


# --------------------------------------------------
# extract peaks
# --------------------------------------------------

Dmax = []
Npeak = []

for dim in dims:

    Ns, means, _ = curves[dim]

    idx = np.argmax(means)

    Dmax.append(means[idx])
    Npeak.append(Ns[idx])

    print(f"d={dim}  Dmax={means[idx]:.3f}  Npeak={Ns[idx]:.2e}")

# --------------------------------------------------
# plot Dmax(d)
# --------------------------------------------------

plt.figure()

plt.plot(dims, Dmax, "o-")

plt.xlabel("dimension")
plt.ylabel("D_max")

plt.title("Peak fractal dimension vs embedding dimension")

plt.tight_layout()
plt.show()

# --------------------------------------------------
# plot Npeak(d)
# --------------------------------------------------

plt.figure()

plt.plot(dims, Npeak, "o-")

plt.yscale("log")

plt.xlabel("dimension")
plt.ylabel("N_peak")

plt.title("Structure formation scale")

plt.tight_layout()
plt.show()

# --------------------------------------------------
# curve collapse
# --------------------------------------------------

plt.figure(figsize=(7, 5))

for i, dim in enumerate(dims):

    Ns, means, _ = curves[dim]

    idx = np.argmax(means)

    x = Ns / Ns[idx]

    plt.plot(x, means, "o-", color=colors[i], label=f"d={dim}")

plt.xlabel("N / N_peak")
plt.ylabel("Docc")

plt.title("Curve collapse")

plt.legend()

plt.tight_layout()
plt.show()


df = pd.read_csv("resultsN.csv")

dims = sorted(df["dim"].unique())

curves = {}

for dim in dims:

    sub = df[df["dim"] == dim]
    grouped = sub.groupby("N")["D"]

    Ns = np.array(sorted(grouped.mean().index))
    means = grouped.mean().values

    curves[dim] = (Ns, means)

# extract peaks
Npeak = {}
Dmax = {}

for dim in dims:

    Ns, means = curves[dim]

    i = np.argmax(means)

    Npeak[dim] = Ns[i]
    Dmax[dim] = means[i]

# collapse
plt.figure(figsize=(6, 5))

for dim in dims:

    Ns, means = curves[dim]

    x = Ns / Npeak[dim]
    y = means / Dmax[dim]

    plt.plot(x, y, "o-", label=f"d={dim}")

plt.xscale("log")
plt.xlabel("N / N_peak")
plt.ylabel("D / D_max")
plt.title("Universal scaling collapse")
plt.legend()
plt.show()

X = []
Y = []

for dim in dims:

    Ns, means = curves[dim]

    x = Ns / Npeak[dim]
    y = means / Dmax[dim]

    X.extend(x)
    Y.extend(y)

X = np.array(X)
Y = np.array(Y)


def F(x, gamma):
    return x**gamma / (1 + x**gamma)


popt, _ = curve_fit(F, X, Y, p0=[0.7])

gamma = popt[0]

print(f"gamma={gamma}")
