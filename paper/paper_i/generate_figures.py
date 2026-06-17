"""Generate Paper I figures that support the finite-memory model narrative."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np


OUT = Path(__file__).resolve().parent

BLUE = "#2f6f9f"
GREEN = "#5d8a66"
ORANGE = "#c77c2f"
GRAY = "#555555"
LIGHT_BLUE = "#e8f1f7"
LIGHT_GREEN = "#eaf3ec"
LIGHT_ORANGE = "#f8eee2"


def add_box(ax, xy, width, height, text, *, facecolor, edgecolor):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.03,rounding_size=0.025",
        linewidth=1.1,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=9,
    )


def add_arrow(ax, start, end, *, color=GRAY, text=None, text_xy=None):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=11,
        linewidth=1.1,
        color=color,
    )
    ax.add_patch(arrow)
    if text:
        if text_xy is None:
            text_xy = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        ax.text(text_xy[0], text_xy[1], text, ha="center", va="center", fontsize=8)


def markov_embedding() -> None:
    fig, ax = plt.subplots(figsize=(7.1, 3.0))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    add_box(
        ax,
        (0.05, 0.62),
        0.20,
        0.18,
        r"visible state" + "\n" + r"$x_n$",
        facecolor=LIGHT_BLUE,
        edgecolor=BLUE,
    )
    add_box(
        ax,
        (0.05, 0.18),
        0.20,
        0.18,
        r"memory field" + "\n" + r"$\rho_n$",
        facecolor=LIGHT_GREEN,
        edgecolor=GREEN,
    )
    add_box(
        ax,
        (0.39, 0.40),
        0.24,
        0.20,
        r"augmented state" + "\n" + r"$\sigma_n=(x_n,\rho_n)$",
        facecolor="#f4f4f4",
        edgecolor=GRAY,
    )
    add_box(
        ax,
        (0.75, 0.40),
        0.20,
        0.20,
        r"next state" + "\n" + r"$\sigma_{n+1}$",
        facecolor=LIGHT_ORANGE,
        edgecolor=ORANGE,
    )

    add_arrow(ax, (0.25, 0.71), (0.39, 0.54), color=BLUE)
    add_arrow(ax, (0.25, 0.27), (0.39, 0.46), color=GREEN)
    add_arrow(
        ax,
        (0.63, 0.50),
        (0.75, 0.50),
        color=ORANGE,
        text=r"fresh noise $\xi_n$",
        text_xy=(0.69, 0.62),
    )

    ax.text(
        0.50,
        0.78,
        r"$x_n$ alone is generally non-Markovian",
        ha="center",
        va="center",
        fontsize=9,
        color=BLUE,
    )
    ax.text(
        0.50,
        0.18,
        r"$(x_n,\rho_n)$ is Markov by construction",
        ha="center",
        va="center",
        fontsize=9,
        color=GREEN,
    )
    ax.text(
        0.80,
        0.23,
        r"$\rho_{n+1}=(1-\alpha)\rho_n+\alpha G_\sigma(x-x_{n+1})$",
        ha="center",
        va="center",
        fontsize=8,
    )

    fig.tight_layout(pad=0.25)
    fig.savefig(OUT / "fig_markov_embedding.pdf", bbox_inches="tight")
    plt.close(fig)


def memory_weights() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.1, 2.6))
    ages = np.arange(0, 350)
    alphas = [0.01, 0.02, 0.05]
    colors = [BLUE, GREEN, ORANGE]

    for alpha, color in zip(alphas, colors):
        weights = alpha * (1.0 - alpha) ** ages
        mass = 1.0 - (1.0 - alpha) ** (ages + 1)
        ax1.plot(ages, weights, color=color, lw=1.8, label=rf"$\alpha={alpha:g}$")
        ax2.plot(alpha * ages, mass, color=color, lw=1.8)

    ax1.set_xlabel(r"age $m$ (updates)")
    ax1.set_ylabel(r"weight $w_m=\alpha(1-\alpha)^m$")
    ax1.set_yscale("log")
    ax1.grid(True, which="both", lw=0.3, alpha=0.45)
    ax1.legend(frameon=False, fontsize=8)

    ax2.axvline(1.0, color=GRAY, ls="--", lw=1.0)
    ax2.text(1.04, 0.15, r"$m\sim\alpha^{-1}$", fontsize=8, rotation=90, va="bottom")
    ax2.set_xlabel(r"scaled age $\alpha m$")
    ax2.set_ylabel("stored memory mass")
    ax2.set_ylim(0, 1.02)
    ax2.grid(True, lw=0.3, alpha=0.45)

    fig.tight_layout(pad=0.5)
    fig.savefig(OUT / "fig_memory_weights.pdf", bbox_inches="tight")
    plt.close(fig)


def relaxation_diagnostic() -> None:
    rng = np.random.default_rng(7)
    t = np.linspace(0, 10, 42)
    gamma = 0.42
    clean = np.exp(-gamma * t)
    observed = np.clip(clean + rng.normal(0.0, 0.035, size=t.shape), 0.015, None)

    fig, ax = plt.subplots(figsize=(3.45, 2.65))
    ax.scatter(t, observed, s=16, color=BLUE, alpha=0.85, label="trajectory estimate")
    ax.plot(t, clean, color=ORANGE, lw=2.0, label=rf"fit $\exp(-\Gamma_{{\rm rel}}t)$")
    ax.axhline(0, color="#222222", lw=0.7)
    ax.set_xlabel(r"coarse-grained time $t=\alpha n$")
    ax.set_ylabel(r"in-knot autocorrelation $C(t)$")
    ax.set_ylim(0, 1.08)
    ax.grid(True, lw=0.3, alpha=0.45)
    ax.text(
        5.3,
        0.58,
        rf"$\Gamma_{{\rm rel}}\approx {gamma:.2f}$",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#bbbbbb", "lw": 0.6},
    )
    ax.legend(frameon=False, fontsize=8)

    fig.tight_layout(pad=0.4)
    fig.savefig(OUT / "fig_relaxation_diagnostic.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    markov_embedding()
    memory_weights()
    relaxation_diagnostic()


if __name__ == "__main__":
    main()
