import csv
import os
import numpy as np
import math
from numba import njit
import multiprocessing as mp
import matplotlib.pyplot as plt
from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit


# ============================================================
# Zwischenspeichern
# ============================================================
def append_csv(row, filename="resultsN.csv"):
    exists = os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["D", "N", "run", "dim"])
#            writer.writerow(["eps", "alpha", "B", "dim", "Deff"])
        writer.writerow(row)

# ============================================================
# Kernel force
# ============================================================
@njit
def kernel_force(r, A, B, s1, s2):
    r2 = np.dot(r, r)
    f = np.zeros_like(r)

    if r2 > 1e-12:
        e1 = math.exp(-r2/(2*s1*s1))
        e2 = math.exp(-r2/(2*s2*s2))
        f += A * r/(s1*s1) * e1
        f -= B * r/(s2*s2) * e2

    return f


# ============================================================
# Simulation (N und Nmem entschärft)
# ============================================================

@njit
def simulate(N, dim, eps, eta, alpha, A, B, s1, s2):
    Nmem = int(5/alpha) + 1
    if Nmem > 300:   # harte Obergrenze
        Nmem = 300

    x = np.zeros((N, dim))
    mem = np.zeros((Nmem, dim))
    weights = np.zeros(Nmem)
    idx = 0

    for n in range(1, N):
        force = np.zeros(dim)

        for k in range(Nmem):
            w = weights[k]
            if w == 0.0:
                continue
            r = x[n-1] - mem[k]
            force += w * kernel_force(r, A, B, s1, s2)

        noise = np.random.normal(0.0, 1.0, dim)
        x[n] = x[n-1] + eps * noise + eta * alpha * force
        mem[idx] = x[n]
        weights *= (1 - alpha)
        weights[idx] = alpha
        idx = (idx + 1) % Nmem

    return x


# ============================================================
# Fractal dimension (leicht robuster)
# ============================================================

def fractal_dimension(points):
    pts = points - np.min(points, axis=0)
    ranges = np.max(pts, axis=0)
    max_range = np.max(ranges)

    sizes = np.logspace(
        np.log10(max_range/200),
        np.log10(max_range/5),
        12
    )

    counts = []
    for s in sizes:
        boxes = np.floor(pts / s).astype(np.int64)
        unique = np.unique(boxes, axis=0)
        counts.append(len(unique))

    counts = np.array(counts)
    coeff = np.polyfit(np.log(1/sizes), np.log(counts), 1)
    return coeff[0]


# ============================================================
# Single simulation run
# ============================================================

def single_run(args):
    eps, alpha, B, dim = args
    traj = simulate(N=300_000,
        dim=dim,eps=eps,eta=2,alpha=alpha,
        A=1,B=B,s1=1,s2=0.15
    )
    points = traj[20_000::10]  # Burn-in + Downsampling
    D = fractal_dimension(points)
    # --- Zwischenspeichern ---
    append_csv([eps, alpha, B, dim, D])

    return (eps, alpha, B, dim, D)


# ============================================================
# Parameter scan
# ============================================================

def parameter_scan():
    eps_vals   = [0.02, 0.05, 0.1, 0.2]
    alpha_vals = [0.005, 0.01, 0.02]
    B_vals     = [2, 3, 4]
    dim_vals   = [2, 3, 4, 5]

    params = []
    runs = 5  # 8 ist machbar, aber 5 reicht oft

    for eps in eps_vals:
        for alpha in alpha_vals:
            for B in B_vals:
                for dim in dim_vals:
                    for _ in range(runs):
                        params.append((eps, alpha, B, dim))

    print("Total simulations:", len(params))

    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(single_run, params)

    arr = np.array(results, dtype=float)
    np.savetxt("scan_results.txt", arr)

    return results


# ============================================================
# Heatmap (eps vs alpha, gemittelt über B, dim)
# ============================================================

def plot_heatmap(results):
    data = defaultdict(list)

    for eps, alpha, B, dim, D in results:
        key = (eps, alpha)
        data[key].append(D)

    eps_vals = sorted(list(set(k[0] for k in data)))
    alpha_vals = sorted(list(set(k[1] for k in data)))

    grid = np.zeros((len(alpha_vals), len(eps_vals)))

    for i, a in enumerate(alpha_vals):
        for j, e in enumerate(eps_vals):
            vals = data[(e, a)]
            grid[i, j] = np.mean(vals)

    plt.figure(figsize=(6, 5))
    plt.imshow(grid, origin="lower", aspect="auto")
    plt.xticks(range(len(eps_vals)), eps_vals)
    plt.yticks(range(len(alpha_vals)), alpha_vals)
    plt.xlabel("eps")
    plt.ylabel("alpha")
    plt.title("Fractal dimension Docc (mean over B, dim)")
    plt.colorbar()
    plt.tight_layout()
    plt.show()


# ============================================================
# Embedding dimension test
# ============================================================

def dimension_test():
    dims = [2, 3, 4, 5, 6]
    eps = 0.05
    alpha = 0.01
    B = 3
    results = []
    for d in dims:
        Ds = []
        for _ in range(3):
            traj = simulate(N=900_000,
                dim=d,eps=eps,eta=2,alpha=alpha,
                A=1,B=B,s1=1,s2=0.15
            )
            points = traj[20_000::10]
            Ds.append(fractal_dimension(points))
        results.append(np.mean(Ds))

    plt.figure()
    plt.plot(dims, results, "o-")
    plt.xlabel("embedding dimension")
    plt.ylabel("Docc")
    plt.title("Dimension selection")
    plt.tight_layout()
    plt.show()


# ============================================================
# Plottet eine 3D-Trajektorie
# ============================================================
def plot_trajectory_3d(traj, step=10, title="3D trajectory"):
    """
        traj : numpy array (N, dim)
        step : Downsampling-Faktor
    """
    if traj.shape[1] < 3:
        raise ValueError("Trajectory must have at least 3 dimensions for 3D plot.")
    pts = traj[::step, :3]  # nur die ersten 3 Dimensionen
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], lw=0.5, color="darkblue")
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")
    ax.set_zlabel("x₃")
    ax.set_title(title)

    plt.tight_layout()
    plt.show()



def scaling_test():
    Ns = [50000,100000,300000,1000000,2500000,6000000,15000000]
    dim = 4
    Ds = []
    for N in Ns:
        traj = simulate(
            N=N, dim=dim,eps=0.05,eta=2,alpha=0.01,A=1,B=3,s1=1,s2=0.15
        )
        pts = traj[20000::10]
        Ds.append(fractal_dimension(pts))
    arr = np.array(Ds, dtype=float)
    np.savetxt("N_results.txt", Ns, arr)
    plt.plot(Ns,Ds,"o-")
    plt.xscale("log")
    plt.xlabel("N")
    plt.ylabel("Docc")
    plt.title("Fractal dimension scaling")
    plt.tight_layout()
    plt.show()

# ============================================================
# Scaling analysis with multiple runs + asymptotic fit
# ============================================================
def scaling_model(N, Dinf, c, beta):
    return Dinf - c * N**(-beta)

def scaling_analysis():
    Ns = [50000,100000,300000,1000000,2500000,6000000,15000000,40000000,60000000]
    dims = [9]   # mehrere Dimensionen gleichzeitig
    runs = 5           # seeds pro Punkt
    results = {}
    for dim in dims:
        mean_vals = []
        std_vals  = []
        max_vals  = []
        print("\nDimension:",dim)
        for N in Ns:
            Ds = []
            for r in range(runs):
                traj = simulate(
                    N=N,dim=dim,eps=0.05,eta=2,alpha=0.01,
                    A=1,B=3,s1=1,s2=0.15)
                pts = traj[20000::10]
                D = fractal_dimension(pts)
                Ds.append(D)
                print("N=",N," run",r," D=",D)
                # --- Zwischenspeichern ---
                append_csv([D,N,r,dim])
            mean_vals.append(np.mean(Ds))
            std_vals.append(np.std(Ds))
            max_vals.append(np.max(Ds))
        results[dim] = (np.array(mean_vals),np.array(std_vals),np.array(max_vals))

    # ========================================================
    # Plot
    # ========================================================

    markers = ["o","^","s","+"]
    colors  = ["blue","red","green","magenta"]
    plt.figure(figsize=(7,5))
    for i,dim in enumerate(dims):
        means, stds = results[dim]
        plt.errorbar(
            Ns,
            means,
            yerr=stds,
            marker=markers[i],
            color=colors[i],
            label=f"d={dim}",
            capsize=4
        )
        # --- scaling fit ---
        try:
            popt,_ = curve_fit(scaling_model,np.array(Ns,dtype=float),means, p0=[3,10,0.5],maxfev=10000)
            Dinf,c,beta = popt
            print("\nFit dimension",dim)
            print("D_inf =",Dinf)
            print("beta  =",beta)
            Nfit = np.logspace(np.log10(min(Ns)),np.log10(max(Ns)*2),200)
            plt.plot(Nfit,scaling_model(Nfit,*popt),color=colors[i],linestyle="--")
        except:
            print("Fit failed for dim",dim)
    plt.xscale("log")
    plt.xlabel("N")
    plt.ylabel("Docc")
    plt.title("Finite-size scaling of fractal dimension")
    plt.legend()
    plt.tight_layout()
    plt.show()

# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
#    traj = simulate(N=300_000,dim=5,eps=0.05,eta=2,alpha=0.01,A=1,B=3,s1=1,s2=0.15)
#    plot_trajectory_3d(traj, step=20, title="Emergence model trajectory")
#    results = parameter_scan()
#    plot_heatmap(results)
#    dimension_test()
#    scaling_test()
    scaling_analysis()
