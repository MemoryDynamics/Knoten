import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# Matplotlib style (PRD-like)
# ============================================================
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "STIXGeneral"],
        "mathtext.fontset": "stix",
        "font.size": 13,
        "axes.labelsize": 14,
        "axes.titlesize": 15,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "lines.linewidth": 1.6,
    }
)


# ============================================================
# Core dynamics
# ============================================================
def generate_trajectory(
    dim=3, steps=10000, eps=0.1, eta=0.9, alpha=0.2, sigma=0.35, seed=3
):
    rng = np.random.default_rng(seed)
    x = np.zeros(dim)
    traj = [x.copy()]
    memory = []
    weights = []

    def grad_phi(x, memory):
        if len(memory) == 0:
            return np.zeros_like(x)
        diff = x - np.array(memory)
        r2 = np.sum(diff**2, axis=1)
        w_spatial = np.exp(-r2 / (2 * sigma**2))
        w = np.array(weights) * w_spatial
        return np.sum(w[:, None] * diff, axis=0) / (np.sum(w) + 1e-12)

    for n in range(steps):
        xi = rng.normal(size=dim)
        gphi = grad_phi(x, memory)
        x = x + eps * xi - eta * gphi
        traj.append(x.copy())

        # Relaxing memory update
        if len(weights) > 0:
            weights[:] = [(1 - alpha) * wi for wi in weights]

        memory.append(x.copy())
        weights.append(alpha)

    return np.array(traj)


# ============================================================
# Generate trajectories
# ============================================================
traj2d = generate_trajectory(dim=2, steps=8000)
traj3d = generate_trajectory(dim=3, steps=8000)

# ============================================================
# FIGURE 1 — 2D TRAJECTORY (LINE)
# ============================================================
fig1, ax1 = plt.subplots(figsize=(6, 6))
ax1.plot(traj2d[:, 0], traj2d[:, 1], color="black", alpha=0.6, linewidth=0.5)
ax1.set_xlabel(r"$x_1$")
ax1.set_ylabel(r"$x_2$")
ax1.set_title("Memory-driven self-avoiding trajectory")
ax1.set_aspect("equal")
ax1.grid(False)
plt.tight_layout()
plt.show()
fig1.savefig("fig1_knot_trajectory.pdf", bbox_inches="tight")

# ============================================================
# FIGURE 2 — 3D KNOT STRUCTURE (SCATTER)
# ============================================================
fig2 = plt.figure(figsize=(7, 6))
ax2 = fig2.add_subplot(111, projection="3d")

t3 = np.arange(len(traj3d))
sc2 = ax2.scatter(
    traj3d[::3, 0],
    traj3d[::3, 1],
    traj3d[::3, 2],
    c=t3[::3],
    s=2.2,
    cmap="plasma",
    alpha=0.9,
)

ax2.set_xlabel(r"$x_1$")
ax2.set_ylabel(r"$x_2$")
ax2.set_zlabel(r"$x_3$")
ax2.set_title("Emergent knot structure in state space")

cbar2 = plt.colorbar(sc2, ax=ax2, fraction=0.035, pad=0.08)
cbar2.set_label(r"update index $n$")

ax2.grid(False)
ax2.xaxis.pane.fill = False
ax2.yaxis.pane.fill = False
ax2.zaxis.pane.fill = False

plt.tight_layout()
plt.show()
fig2.savefig("fig2_knot_scatter.pdf", bbox_inches="tight")

# ============================================================
# FIGURE 3 — 3D TRAJECTORY (LINE + SCATTER)
# ============================================================
fig3 = plt.figure(figsize=(7, 6))
ax3 = fig3.add_subplot(111, projection="3d")

ax3.plot(
    traj3d[:, 0], traj3d[:, 1], traj3d[:, 2], color="black", linewidth=0.25, alpha=0.55
)

sc3 = ax3.scatter(
    traj3d[::4, 0],
    traj3d[::4, 1],
    traj3d[::4, 2],
    c=t3[::4],
    s=2.0,
    cmap="plasma",
    alpha=0.85,
)

ax3.set_xlabel(r"$x_1$")
ax3.set_ylabel(r"$x_2$")
ax3.set_zlabel(r"$x_3$")
ax3.set_title("Trajectory organization and knot transitions")

cbar3 = plt.colorbar(sc3, ax=ax3, fraction=0.035, pad=0.08)
cbar3.set_label(r"update index $n$")

ax3.grid(False)
ax3.xaxis.pane.fill = False
ax3.yaxis.pane.fill = False
ax3.zaxis.pane.fill = False

plt.tight_layout()
plt.show()
fig3.savefig("fig3_knot_trajectory.pdf", bbox_inches="tight")
