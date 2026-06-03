import numpy as np
import matplotlib.pyplot as plt

# ---------- Matplotlib style (PRD-like) ----------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "STIXGeneral"],
    "mathtext.fontset": "stix",
    "font.size": 14,
    "axes.labelsize": 16,
    "axes.titlesize": 16,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "lines.linewidth": 1.8,
})


def generate_trajectory(
    dim=2,
    steps=4000,
    eps=0.15,
    eta=0.8,
    alpha=0.01,
    sigma=0.4,
    seed=1
):
    rng = np.random.default_rng(seed)
    x = np.zeros(dim)
    traj = [x.copy()]
    memory = []

    def grad_phi(x, memory):
        if len(memory) == 0:
            return np.zeros_like(x)
        diff = x - np.array(memory)
        r2 = np.sum(diff**2, axis=1)
        w = np.exp(-r2 / (2 * sigma**2))
        grad = np.sum((w[:, None] * diff), axis=0)
        return grad

    for n in range(steps):
        xi = rng.normal(size=dim)
        gphi = grad_phi(x, memory)
        x = x + eps * xi - eta * gphi
        traj.append(x.copy())

        if rng.random() < alpha:
            memory.append(x.copy())

    return np.array(traj)

traj2d = generate_trajectory(dim=2)

fig, ax = plt.subplots(figsize=(6,6))

t = np.arange(len(traj2d))
ax.scatter(
    traj2d[:,0],
    traj2d[:,1],
    c=t,
    s=1.5,
    cmap="inferno",
    alpha=0.9
)

ax.set_xlabel(r"$x_1$")
ax.set_ylabel(r"$x_2$")
ax.set_title("Memory-driven self-avoiding trajectory")

ax.set_aspect("equal")
plt.tight_layout()
plt.show()

fig.savefig("fig_alpha.pdf", bbox_inches="tight")