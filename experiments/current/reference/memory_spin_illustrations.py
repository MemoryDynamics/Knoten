"""Analytic geometry and a separate textbook spinor reference, not a simulation."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "figures/draft/memory_charge_2026-11-19"
INK, MUTED, GRID = "#20282b", "#586469", "#d9dfe1"
HIGH, LOW, DEFECT = "#bc452f", "#2375a6", "#804887"
HULL = "#839b92"


def memory_geometry(phase: int = 0) -> tuple[np.ndarray, np.ndarray]:
    if type(phase) is not int or phase not in range(4):
        raise ValueError("one of the four exact discrete phases required")
    f, g, q = 1 / 2, 2 / 3, 99 / 100
    radius = np.sqrt(-np.log(f) / 2)
    height = np.sqrt(np.log(f / g**2) / 4)
    history = np.array(
        [
            [radius, 0, height],
            [0, -radius, -height],
            [-radius, 0, height],
            [0, radius, -height],
            [radius, 0, height],
        ]
    )
    u = np.log(q)
    root = np.array([u / radius, -u / radius, u / (2 * height)])
    symmetry = np.array([[0, -1, 0], [1, 0, 0], [0, 0, -1]])
    transform = np.linalg.matrix_power(symmetry, phase)
    return history @ transform.T, transform @ root


def spinor(theta):
    theta = np.asarray(theta, dtype=float)
    return np.stack([np.exp(-0.5j * theta), np.exp(0.5j * theta)], axis=-1) / np.sqrt(2)


def spin_observables(theta):
    state = spinor(theta)
    cross = np.conjugate(state[..., 0]) * state[..., 1]
    bloch = np.stack(
        [
            2 * cross.real,
            2 * cross.imag,
            abs(state[..., 0]) ** 2 - abs(state[..., 1]) ** 2,
        ],
        axis=-1,
    )
    overlap = (state[..., 0] + state[..., 1]) / np.sqrt(2)
    return bloch, (1 + bloch[..., 0]) / 2, (1 + overlap.real) / 2


def _style():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 14,
            "text.color": INK,
            "axes.labelcolor": INK,
            "axes.edgecolor": GRID,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.titleweight": "normal",
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.facecolor": "white",
        }
    )


def _save(fig, stem):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        fig.savefig(OUTPUT / f"{stem}.{extension}", dpi=210)
    plt.close(fig)


def draw_memory():
    _style()
    fig = plt.figure(figsize=(8, 9.2))
    fig.text(0.07, 0.955, "Ein serieller Memory-Umlauf", fontsize=23)
    fig.text(
        0.07, 0.920, "Vier Speicherorte einer Bahn, keine vier Teilchen", fontsize=14
    )
    points, root = memory_geometry()
    ax = fig.add_axes([0.025, 0.355, 0.95, 0.545], projection="3d")
    ax.set_proj_type("ortho")
    faces = [
        [points[a], points[b], points[c]]
        for a, b, c in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    ]
    ax.add_collection3d(
        Poly3DCollection(
            faces, facecolors=HULL, edgecolors=HULL, linewidths=0.8, alpha=0.08
        )
    )
    for age in range(4):
        start, end = points[age + 1], points[age]
        direction = end - start
        ax.plot(*np.array([start, end]).T, color=MUTED, lw=1.8)
        midpoint = start + 0.48 * direction
        ax.quiver(
            *midpoint,
            *(0.13 * direction),
            color=MUTED,
            arrow_length_ratio=0.55,
            linewidth=1.5,
        )
    for point in points[:4]:
        color = HIGH if point[2] > 0 else LOW
        ax.scatter(
            *point,
            s=180,
            color=color,
            edgecolors="white",
            linewidths=1.3,
            depthshade=False,
        )
    ax.scatter(
        *points[0],
        s=370,
        facecolors="none",
        edgecolors=INK,
        linewidths=1.7,
        depthshade=False,
    )
    ax.scatter(
        *root,
        s=130,
        marker="D",
        color=DEFECT,
        edgecolors="white",
        linewidths=1,
        depthshade=False,
    )
    ax.set(xlim=(-0.78, 0.78), ylim=(-0.78, 0.78), zlim=(-0.30, 0.30))
    ax.set_box_aspect((1.56, 1.56, 0.60))
    ax.view_init(elev=52, azim=-42)
    # Screen-space labels preserve legibility without moving the plotted sites.
    offsets = [(18, -20), (-12, -23), (-12, 20), (18, 20)]
    for age, (point, offset) in enumerate(zip(points[:4], offsets)):
        label = (
            "jetzt"
            if age == 0
            else f"{age} Schritt" + ("e" if age > 1 else "") + " alt"
        )
        x, y, _ = proj3d.proj_transform(*point, ax.get_proj())
        ax.annotate(
            label,
            (x, y),
            xytext=offset,
            textcoords="offset points",
            ha="left" if offset[0] > 0 else "right",
            va="center",
            fontsize=13,
            arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.8},
        )
    x, y, _ = proj3d.proj_transform(*root, ax.get_proj())
    ax.annotate(
        "+1-Defekt",
        (x, y),
        xytext=(0, 35),
        textcoords="offset points",
        ha="center",
        color=DEFECT,
        fontsize=15,
        zorder=1000,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.94, "pad": 2},
        arrowprops={"arrowstyle": "-", "color": DEFECT, "lw": 1},
    )
    for coordinate in (ax.xaxis, ax.yaxis, ax.zaxis):
        coordinate.set_pane_color((1, 1, 1, 0))
        coordinate._axinfo["grid"]["color"] = "#e3e7e8"
    ax.set_xticks([-0.6, 0, 0.6])
    ax.set_yticks([-0.6, 0, 0.6])
    ax.set_zticks([-0.2, 0, 0.2])
    ax.tick_params(labelsize=10, pad=0)
    ax.set_xlabel(r"$x/\sigma$", labelpad=2)
    ax.set_ylabel(r"$y/\sigma$", labelpad=2)
    ax.set_zlabel(r"$z/\sigma$", labelpad=3)
    handles = [
        Line2D([], [], marker="o", ls="", color=HIGH, label=r"$z=+h$"),
        Line2D([], [], marker="o", ls="", color=LOW, label=r"$z=-h$"),
        Line2D(
            [],
            [],
            marker="o",
            ls="",
            markerfacecolor="none",
            color=INK,
            label="aktueller Ort",
        ),
        Line2D([], [], marker="D", ls="", color=DEFECT, label="Feldnullstelle"),
    ]
    fig.legend(
        handles=handles,
        loc="center",
        bbox_to_anchor=(0.5, 0.355),
        ncol=4,
        frameon=False,
        fontsize=12,
        handletextpad=0.3,
        columnspacing=1,
    )
    fig.text(0.07, 0.304, "Vier diskrete Phasen, von oben gesehen", fontsize=16)
    for phase in range(4):
        axes = fig.add_axes([0.07 + phase * 0.23, 0.115, 0.17, 0.16])
        history, zero = memory_geometry(phase)
        axes.plot(*history[:, :2].T, lw=1, color=MUTED)
        colors = [HIGH if point[2] > 0 else LOW for point in history[:4]]
        axes.scatter(*history[:4, :2].T, s=75, c=colors, zorder=3)
        axes.scatter(
            *history[0, :2], s=180, facecolors="none", edgecolors=INK, lw=1.5, zorder=4
        )
        axes.scatter(*zero[:2], s=45, marker="D", c=DEFECT, zorder=4)
        axes.set(xlim=(-0.78, 0.78), ylim=(-0.78, 0.78), aspect="equal")
        axes.axis("off")
        axes.set_title(f"n = {phase}", fontsize=13, pad=7)
        if phase < 3:
            fig.text(0.267 + phase * 0.23, 0.185, r"$\to$", fontsize=19, color=MUTED)
    fig.text(
        0.07,
        0.072,
        "Die Farben bewahren die H\u00f6he in der 2D-Projektion.",
        fontsize=13,
    )
    fig.text(
        0.07,
        0.037,
        "Sollgeometrie | Stabilit\u00e4t offen | Keine Teilchenidentifikation",
        fontsize=12,
        color=MUTED,
    )
    _save(fig, "memory_structure")


def _phase_arrow(ax, angle, color, *, complex_plane):
    ax.add_patch(Circle((0, 0), 0.85, facecolor="none", edgecolor=GRID, lw=1))
    ax.plot([-1, 1], [0, 0], color=GRID, lw=0.7)
    ax.plot([0, 0], [-1, 1], color=GRID, lw=0.7)
    ax.annotate(
        "",
        xy=(0.85 * np.cos(angle), 0.85 * np.sin(angle)),
        xytext=(0, 0),
        arrowprops={
            "arrowstyle": "-|>",
            "color": color,
            "lw": 2.2,
            "mutation_scale": 14,
        },
    )
    ax.set(xlim=(-1.12, 1.12), ylim=(-1.12, 1.12), aspect="equal")
    ax.axis("off")
    if complex_plane:
        ax.text(1.02, -0.25, "Re", fontsize=9, ha="center", color=MUTED)
        ax.text(-0.18, 0.98, "Im", fontsize=9, ha="right", color=MUTED)
    else:
        ax.text(1.02, -0.25, "x", fontsize=10, ha="center", color=MUTED)
        ax.text(-0.18, 0.98, "y", fontsize=10, ha="right", color=MUTED)


def draw_spin():
    _style()
    fig = plt.figure(figsize=(8, 10.3))
    fig.text(0.07, 0.955, "Spin 1/2 in drei Raumdimensionen", fontsize=21)
    fig.text(
        0.07,
        0.920,
        "Quantenmechanische Referenz, nicht aus Memory hergeleitet",
        fontsize=13,
    )
    angles = np.array([0, 180, 360, 540, 720])
    for column, degrees in enumerate(angles):
        left = 0.235 + column * 0.145
        fig.text(left + 0.055, 0.867, rf"${degrees}^\circ$", ha="center", fontsize=17)
        theta = np.deg2rad(degrees)
        for row, (angle, color) in enumerate(
            [(theta, INK), (-theta / 2, HIGH), (theta / 2, LOW)]
        ):
            ax = fig.add_axes([left, 0.729 - row * 0.15, 0.112, 0.112])
            _phase_arrow(ax, angle, color, complex_plane=row > 0)
    fig.text(0.07, 0.785, "Spinrichtung\nin 3D", va="center", fontsize=14)
    fig.text(0.07, 0.635, "Phase von a", va="center", fontsize=14, color=HIGH)
    fig.text(0.07, 0.485, "Phase von b", va="center", fontsize=14, color=LOW)
    for column, label in [(0, r"$\psi_0$"), (2, r"$-\psi_0$"), (4, r"$\psi_0$")]:
        fig.text(0.290 + column * 0.145, 0.395, label, ha="center", fontsize=18)
    fig.text(
        0.07, 0.350, "a und b: komplexe Amplituden, keine Raumkoordinaten", fontsize=13
    )
    axes = fig.add_axes([0.14, 0.105, 0.79, 0.18])
    theta = np.linspace(0, 4 * np.pi, 361)
    _, spin_probability, interference = spin_observables(theta)
    axes.plot(
        np.rad2deg(theta),
        spin_probability,
        color=MUTED,
        lw=1.7,
        ls="--",
        label="Spinmessung entlang +x",
    )
    axes.plot(
        np.rad2deg(theta),
        interference,
        color=DEFECT,
        lw=2.4,
        label="Interferenz mit Referenzarm",
    )
    axes.set(xlim=(0, 720), ylim=(-0.035, 1.035), xticks=angles, yticks=[0, 0.5, 1])
    axes.spines[["top", "right"]].set_visible(False)
    axes.grid(axis="y", color=GRID, lw=0.7)
    axes.tick_params(labelsize=12)
    axes.set_xlabel(r"Drehwinkel $\theta$ (Grad)", fontsize=13, labelpad=3)
    axes.set_ylabel("Wahrscheinlichkeit", fontsize=12, labelpad=7)
    axes.legend(
        frameon=False,
        fontsize=11,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=1,
    )
    fig.text(
        0.07,
        0.030,
        "360\u00b0: gleiche Spinmessung. Das Minus zeigt sich nur relativ.",
        fontsize=13,
    )
    _save(fig, "spinor_reference")


def main():
    draw_memory()
    draw_spin()
    provenance = {
        "scope": "analytic illustration only; no dynamics or stability evaluation",
        "memory_inputs": {"f": "1/2", "g": "2/3", "q": "99/100", "sigma": 1},
        "geometry_source": "reports/reference/flat_memory_cycle_2026-11-16.md",
        "memory_boundary": "four deposition sites of one history; not four particles; stability open",
        "spin_reference": "psi(theta)=(exp(-i theta/2),exp(+i theta/2))/sqrt(2)",
        "spin_boundary": "assumed quantum reference, not memory-derived; no extra spatial coordinate",
        "spin_source": "https://live.ocw.mit.edu/courses/22-51-quantum-theory-of-radiation-interactions-fall-2012/fb8b6e60579e7a4e1584e44e597c7c05_MIT22_51F12_Ch4.pdf (4.2.4)",
        "interferometer": "balanced coherent arms; U_z(theta) in one arm; zero baseline path phase; spin-insensitive output",
        "figures": ["memory_structure", "spinor_reference"],
    }
    (OUTPUT / "provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "figures": provenance["figures"],
                "target_stability_evaluated": False,
            }
        )
    )


if __name__ == "__main__":
    main()
