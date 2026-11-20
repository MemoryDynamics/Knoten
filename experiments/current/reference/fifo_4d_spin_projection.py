"""Real four-component kinematic reference, not a native Memory trajectory."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
import numpy as np

from .memory_spin_illustrations import DEFECT, GRID, HIGH, INK, LOW, MUTED, _style


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "figures/draft/fifo_4d_spin_2026-11-20"
GENERATORS = np.array(
    [
        [[0, 0, 0, 1], [0, 0, -1, 0], [0, 1, 0, 0], [-1, 0, 0, 0]],
        [[0, 0, -1, 0], [0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0]],
        [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]],
    ],
    dtype=int,
)
INITIAL = np.full(4, 0.5)
INTERNAL_STEP = np.pi / 4


def real_rotation(axis, angle):
    axis = np.asarray(axis, dtype=float)
    if axis.shape != (3,) or not np.isfinite(axis).all():
        raise ValueError("a finite three-component axis is required")
    length = np.linalg.norm(axis)
    if length == 0 or not np.isfinite(angle):
        raise ValueError("a nonzero axis and finite angle are required")
    generator = np.einsum("i,ijk->jk", axis / length, GENERATORS)
    return np.cos(angle / 2) * np.eye(4) + np.sin(angle / 2) * generator


def real_orbit(alpha):
    """Prescribed internal angle alpha; the readout angle is derived as 2 alpha."""
    alpha = np.asarray(alpha, dtype=float)
    phase = np.pi / 4
    return np.stack(
        [
            np.cos(phase - alpha),
            np.sin(phase - alpha),
            np.cos(phase + alpha),
            np.sin(phase + alpha),
        ],
        axis=-1,
    ) / np.sqrt(2)


def fifo_reference(step):
    if type(step) is not int:
        raise ValueError("an integer reference step is required")
    return real_orbit(INTERNAL_STEP * (step - np.arange(4)))


def direction_readout(states):
    """Chosen quadratic Bloch map, not the repository's native vector readout."""
    states = np.asarray(states, dtype=float)
    if states.ndim < 1 or states.shape[-1] != 4 or not np.isfinite(states).all():
        raise ValueError("finite four-component states are required")
    a, b, c, d = np.moveaxis(states, -1, 0)
    norm_squared = np.sum(states**2, axis=-1)
    if np.any(norm_squared == 0):
        raise ValueError("the direction is undefined at zero")
    return (
        np.stack(
            [2 * (a * c + b * d), 2 * (a * d - b * c), a * a + b * b - c * c - d * d],
            axis=-1,
        )
        / norm_squared[..., None]
    )


def draw_reference():
    _style()
    fig = plt.figure(figsize=(8, 8.8))
    fig.text(0.06, 0.956, "Ein 4D-Umlauf, zwei 3D-Umdrehungen", fontsize=20)
    fig.text(
        0.06, 0.919, "Vier FIFO-Speicherpl\u00e4tze; Winkel des 3D-Readouts", fontsize=13
    )
    fig.text(
        0.06,
        0.871,
        "4D-Historie: drei Koordinaten + Farbe f\u00fcr die vierte",
        fontsize=13,
    )
    cmap = LinearSegmentedColormap.from_list(
        "fourth_coordinate", [LOW, "#eeeeee", HIGH]
    )
    norm = Normalize(-1 / np.sqrt(2), 1 / np.sqrt(2))
    trace = real_orbit(np.linspace(0, 2 * np.pi, 241))
    circle_angle = np.linspace(0, 2 * np.pi, 241)
    for column, step in enumerate((0, 4, 8)):
        left = 0.025 + column * 0.325
        center = left + 0.15
        fig.text(center, 0.827, rf"${90 * step}^\circ$", ha="center", fontsize=19)
        fig.text(center, 0.798, f"n = {step}", ha="center", fontsize=12, color=MUTED)
        state = fifo_reference(step)
        axes = fig.add_axes([left, 0.545, 0.30, 0.24], projection="3d")
        axes.set_proj_type("ortho")
        axes.plot(*trace[:, :3].T, color=GRID, lw=1)
        axes.plot(*state[:, :3].T, color=MUTED, lw=1.4)
        axes.scatter(
            *state[:, :3].T,
            c=state[:, 3],
            s=[110, 65, 45, 30],
            cmap=cmap,
            norm=norm,
            edgecolors=INK,
            linewidths=0.5,
            depthshade=False,
        )
        axes.scatter(
            *state[0, :3],
            s=220,
            facecolors="none",
            edgecolors=INK,
            lw=1.4,
            depthshade=False,
        )
        for coordinate in (axes.xaxis, axes.yaxis, axes.zaxis):
            coordinate.set_pane_color((1, 1, 1, 0))
            coordinate._axinfo["grid"]["color"] = GRID
        axes.set(xlim=(-0.8, 0.8), ylim=(-0.8, 0.8), zlim=(-0.8, 0.8))
        axes.set_box_aspect((1, 1, 1))
        axes.view_init(elev=23, azim=-54)
        axes.set_xticks([])
        axes.set_yticks([])
        axes.set_zticks([])
        axes.set_xlabel(r"$u_1$", fontsize=11, labelpad=-10)
        axes.set_ylabel(r"$u_2$", fontsize=11, labelpad=-10)
        axes.set_zlabel(r"$u_3$", fontsize=11, labelpad=-10)
        label = r"$-Q_0$" if step == 4 else r"$Q_0$"
        fig.text(center, 0.528, label, ha="center", fontsize=17)

        axes = fig.add_axes([left + 0.045, 0.199, 0.22, 0.19])
        axes.plot(np.cos(circle_angle), np.sin(circle_angle), color=GRID, lw=1)
        readout = direction_readout(state)
        closed = np.vstack([readout, readout[0]])
        axes.plot(*closed[:, :2].T, color=DEFECT, lw=1.3)
        axes.scatter(*readout[:, :2].T, c=DEFECT, s=[100, 55, 38, 26], zorder=3)
        axes.scatter(
            *readout[0, :2], s=210, facecolors="none", edgecolors=INK, lw=1.4, zorder=4
        )
        axes.annotate(
            "",
            xy=readout[0, :2],
            xytext=(0, 0),
            arrowprops={"arrowstyle": "-|>", "color": INK, "lw": 1.8},
        )
        axes.set(xlim=(-1.3, 1.3), ylim=(-1.3, 1.3), aspect="equal")
        axes.axis("off")
        axes.text(1.22, -0.2, "x", fontsize=11)
        axes.text(0.12, 1.16, "y", fontsize=11)
        fig.text(center, 0.177, "gleiches Readout", ha="center", fontsize=12)

    color_axes = fig.add_axes([0.32, 0.481, 0.38, 0.013])
    scalar = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    colorbar = fig.colorbar(
        scalar, cax=color_axes, orientation="horizontal", ticks=[-0.5, 0, 0.5]
    )
    colorbar.ax.tick_params(labelsize=10, length=2)
    fig.text(0.25, 0.480, r"$u_4$", fontsize=12)
    fig.text(0.06, 0.412, "Quadratisches 3D-Richtungsreadout (hier z = 0)", fontsize=14)
    fig.text(
        0.06,
        0.123,
        "360\u00b0: innere Historie negiert. 720\u00b0: vollst\u00e4ndig zur\u00fcck.",
        fontsize=13,
    )
    fig.text(
        0.06,
        0.085,
        "Schwarzer Ring: aktueller Eintrag. Kleinere Punkte: \u00e4ltere Eintr\u00e4ge.",
        fontsize=11,
    )
    fig.text(
        0.06,
        0.046,
        "Umlauf und Readout sind vorgegeben, nicht aus Memory hergeleitet.",
        fontsize=11,
        color=MUTED,
    )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "svg"):
        fig.savefig(OUTPUT / f"fifo_4d_projection.{extension}", dpi=210)
    plt.close(fig)


def main():
    draw_reference()
    provenance = {
        "scope": "analytic real-coordinate construction; no native trajectory or stability evaluation",
        "fifo_slots": 4,
        "four_dimensional_orbit_period_steps": 8,
        "quadratic_readout_period_steps": 4,
        "internal_step_radians": "pi/4",
        "readout_angle": "theta=2*alpha, derived for the chosen quadratic map",
        "head_rule": "prescribed exp((pi/4)*J_z), not native Memory feedback",
        "readout": "normalized quadratic Bloch map, not native Gaussian vector readout",
        "source": "https://arxiv.org/html/1411.4999v2 (sections 2.1-2.2)",
        "native_embedding": "separate analytic identity, no new candidate evaluated",
    }
    (OUTPUT / "provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output": str(OUTPUT), "native_target_evaluated": False}))


if __name__ == "__main__":
    main()
