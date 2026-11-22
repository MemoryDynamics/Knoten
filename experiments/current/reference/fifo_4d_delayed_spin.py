"""Four-slot delayed feedback with a 720-degree kinematic reference orbit."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LinearSegmentedColormap, Normalize
import numpy as np

from .fifo_4d_spin_projection import GENERATORS, INITIAL, ROOT, real_rotation
from .memory_spin_illustrations import GRID, HIGH, INK, LOW, MUTED, _style


OUTPUT = ROOT / "figures/draft/fifo_4d_spin_2026-11-20/fifo_4d_delayed_spin.gif"
AXIS = np.array([1.0, 2.0, 3.0]) / np.sqrt(14)
STEP = np.pi / 2
BASIS = np.vstack((INITIAL, GENERATORS @ INITIAL)).T


def delayed_step(history):
    """Advance the FIFO by re-inserting the negated oldest entry at the head."""
    history = np.asarray(history, dtype=float)
    if history.shape != (4, 4) or not np.isfinite(history).all():
        raise ValueError("four finite four-component entries are required")
    return np.concatenate((-history[-1:], history[:-1]), axis=0)


def coherent_history(axis=AXIS):
    return np.stack([real_rotation(axis, -age * STEP) @ INITIAL for age in range(4)])


def frame_readout(head):
    """Decode the whole 3D frame, rather than just one direction, from the head."""
    head = np.asarray(head, dtype=float)
    if head.shape != (4,) or not np.isfinite(head).all():
        raise ValueError("a finite four-component head is required")
    length = np.linalg.norm(head)
    if length == 0:
        raise ValueError("the frame is undefined at zero")
    a, x, y, z = BASIS.T @ (head / length)
    v = np.array([x, y, z])
    cross = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    return (a * a - v @ v) * np.eye(3) + 2 * np.outer(v, v) + 2 * a * cross


def draw_animation():
    _style()
    fig = plt.figure(figsize=(7.8, 4.4))
    fig.text(0.06, 0.928, "4D-FIFO: Zwei Drehungen bis zur Wiederkehr", fontsize=17)
    fig.text(0.06, 0.856, "Neuer Kopf = negativer \u00e4ltester Eintrag", fontsize=12)

    def panel(left, title):
        ax = fig.add_axes([left, 0.196, 0.44, 0.53], projection="3d")
        ax.set_proj_type("ortho")
        ax.view_init(elev=22, azim=-58)
        ax.set_box_aspect((1, 1, 1), zoom=1.23)
        ax.set(xlim=(-1.1, 1.1), ylim=(-1.1, 1.1), zlim=(-1.1, 1.1))
        ax.set_axis_off()
        fig.text(left + 0.22, 0.764, title, ha="center", fontsize=12)
        return ax

    inner = panel(0.045, r"FIFO: 3 Koordinaten + Farbe ($u_4$)")
    inner.view_init(elev=48, azim=-155)
    outer = panel(0.515, "Ausgelesener 3D-Rahmen")
    orbit = np.array(
        [
            real_rotation(AXIS, angle) @ INITIAL
            for angle in np.linspace(0, 4 * np.pi, 161)
        ]
    )
    inner.plot(*orbit[:, :3].T, color=GRID, lw=1.8)
    (chain,) = inner.plot([], [], [], color=MUTED, lw=1.4, zorder=3)
    markers = [
        inner.plot([], [], [], "o", ms=size, mec=INK, mew=0.9, zorder=4)[0]
        for size in (12, 8, 7, 6)
    ]
    (ring,) = inner.plot([], [], [], "o", ms=17, mfc="none", mec=INK, zorder=5)
    cmap = LinearSegmentedColormap.from_list("fourth", [LOW, "#eeeeee", HIGH])
    norm = Normalize(-1, 1)
    colorbar = fig.colorbar(
        plt.cm.ScalarMappable(norm=norm, cmap=cmap),
        cax=fig.add_axes([0.155, 0.224, 0.22, 0.018]),
        orientation="horizontal",
        ticks=[-1, 0, 1],
    )
    colorbar.ax.tick_params(labelsize=9, length=2)

    origin = np.zeros(3)
    outer.plot(*np.stack((-AXIS, AXIS)).T, "--", color=MUTED, lw=1)
    outer.plot(*origin, "o", color=INK, ms=4)
    colors = ("#ad3827", "#13715e", "#245d9b")
    arms = [
        outer.plot([], [], [], "-o", color=color, lw=2.4, ms=5)[0] for color in colors
    ]
    for x, label, color in zip(
        (0.67, 0.735, 0.8), ("x", "y", "z"), colors, strict=True
    ):
        fig.text(x, 0.19, label, color=color, ha="center", fontsize=12, weight="bold")

    counter = fig.text(0.06, 0.113, "", fontsize=14)
    caption = fig.text(0.06, 0.053, "", fontsize=11, color=MUTED)
    initial = coherent_history()
    states = [initial]
    for _ in range(8):
        states.append(delayed_step(states[-1]))
    key_captions = {
        0: "Start: Rahmen und FIFO in Ausgangslage",
        40: "Gleicher 3D-Rahmen; alle vier FIFO-Eintr\u00e4ge negiert",
        80: "3D-Rahmen und gesamter 4D-FIFO wieder am Start",
    }

    def update(frame):
        step, fraction = divmod(frame, 10)
        state = states[step]
        if fraction:
            state = state @ real_rotation(AXIS, STEP * fraction / 10).T
        chain.set_data_3d(*state[:, :3].T)
        for marker, point in zip(markers, state, strict=True):
            marker.set_data_3d(*point[:3, None])
            marker.set_markerfacecolor(cmap(norm(point[3])))
        ring.set_data_3d(*state[0, :3, None])
        for arm, tip in zip(arms, frame_readout(state[0]).T, strict=True):
            arm.set_data_3d(*np.stack((origin, tip)).T)
        counter.set_text(
            f"{9 * frame}\u00b0  |  "
            + ("Zwischenbild" if fraction else f"Schritt {step}")
        )
        caption.set_text(
            key_captions.get(
                frame, "Der Kopf von jetzt kehrt in vier Schritten negiert zur\u00fcck."
            )
        )

    frames = [
        frame for frame in range(81) for _ in range(21 if frame in key_captions else 1)
    ]
    animation = FuncAnimation(fig, update, frames=frames)
    try:
        animation.save(OUTPUT, writer=PillowWriter(fps=16), dpi=108)
    finally:
        plt.close(fig)


if __name__ == "__main__":
    draw_animation()
