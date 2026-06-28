from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import SimulationConfig
from emergenz_knoten.anchor import estimate_transfer_operator, simulate_augmented_features
from emergenz_knoten.kernels import exponential_weights


HERE = Path(__file__).resolve().parent


def save_memory_weights() -> None:
    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    horizon = 360
    for alpha in (0.02, 0.05, 0.1):
        weights = exponential_weights(alpha, horizon)
        ax.plot(np.arange(horizon), weights, label=fr"$\alpha={alpha:g}$")
        ax.axvline(1.0 / alpha, color=ax.lines[-1].get_color(), alpha=0.18, lw=1)
    ax.set_xlabel("lag $j$")
    ax.set_ylabel(r"$w_j=\alpha(1-\alpha)^j$")
    ax.set_yscale("log")
    ax.set_ylim(1e-5, 2e-1)
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Normalized exponential memory weights")
    fig.tight_layout()
    fig.savefig(HERE / "fig_memory_weights.pdf")
    plt.close(fig)


def save_transfer_spectrum() -> None:
    cfg = SimulationConfig(
        steps=2500,
        dim=2,
        epsilon=0.03,
        eta=0.15,
        alpha=0.04,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=0.35,
        max_memory=500,
        burn_in=250,
        sample_every=10,
    )
    result = simulate_augmented_features(cfg, seed=7)
    transfer = estimate_transfer_operator(
        result["augmented_features"],
        voxel_size=1.0,
        lag=3,
        lag_time=30.0,
    )
    vals = np.asarray(transfer.eigenvalues)
    vals = vals[np.argsort(-np.abs(vals))]
    vals = vals[: min(20, len(vals))]

    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    theta = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(theta), np.sin(theta), color="0.82", lw=1)
    ax.scatter(vals.real, vals.imag, s=24, color="#1f77b4", edgecolor="white", linewidth=0.4)
    ax.axhline(0.0, color="0.85", lw=0.8)
    ax.axvline(0.0, color="0.85", lw=0.8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xlabel(r"$\operatorname{Re}\lambda$")
    ax.set_ylabel(r"$\operatorname{Im}\lambda$")
    ax.set_title("Example transfer spectrum")
    fig.tight_layout()
    fig.savefig(HERE / "fig_transfer_spectrum.pdf")
    plt.close(fig)


def main() -> None:
    save_memory_weights()
    save_transfer_spectrum()
    print("wrote fig_memory_weights.pdf and fig_transfer_spectrum.pdf")


if __name__ == "__main__":
    main()
