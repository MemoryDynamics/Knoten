from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ELL_R = 1.0
ELL_A = 3.0
BETA = 0.35


def dkernel_dr(r: float) -> float:
    return (
        -2.0 * r / (ELL_R**2) * np.exp(-(r * r) / (ELL_R**2))
        + 2.0 * BETA * r / (ELL_A**2) * np.exp(-(r * r) / (ELL_A**2))
    )


def grad_kernel(vec: np.ndarray) -> np.ndarray:
    r = float(np.linalg.norm(vec))
    if r < 1e-12:
        return np.zeros_like(vec)
    return dkernel_dr(r) * vec / r


def run(alpha: float, eta: float, *, eps: float = 0.0, steps: int = 8000, dim: int = 2) -> np.ndarray:
    x = np.zeros(dim)
    mem_len = max(5, int(round(1.0 / alpha)))
    history = [x.copy()]
    traj = np.zeros((steps, dim))

    for n in range(steps):
        force = np.zeros(dim)
        weights = np.exp(-np.arange(len(history))[::-1] * alpha)

        for weight, point in zip(weights, history):
            force += weight * grad_kernel(x - point)

        if weights.sum() > 0:
            force /= weights.sum()

        x = x - eta * force + eps * np.random.randn(dim)

        history.append(x.copy())
        if len(history) > mem_len:
            history.pop(0)

        traj[n] = x

    return traj


def curvature(traj: np.ndarray) -> np.ndarray:
    v1 = traj[1:-1] - traj[:-2]
    v2 = traj[2:] - traj[1:-1]
    a = np.linalg.norm(v1, axis=1)
    b = np.linalg.norm(v2, axis=1)
    cross = v1[:, 0] * v2[:, 1] - v1[:, 1] * v2[:, 0]
    kappa = np.zeros_like(a)
    mask = (a > 1e-12) & (b > 1e-12)
    kappa[mask] = np.abs(cross[mask]) / (a[mask] * b[mask])
    return kappa


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a small orbit laboratory sweep.")
    parser.add_argument("--steps", type=int, default=8000)
    parser.add_argument("--output-dir", type=Path, default=Path("../../figures/draft/LQG"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = Path(__file__).resolve().parent / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    cases = [
        (0.1, 0.05),
        (0.05, 0.05),
        (0.025, 0.05),
        (0.1, 0.10),
        (0.05, 0.10),
        (0.025, 0.10),
        (0.1, 0.20),
        (0.05, 0.20),
        (0.025, 0.20),
    ]

    fig, axes = plt.subplots(3, 3, figsize=(10, 10))
    for ax, (alpha, eta) in zip(axes.ravel(), cases):
        traj = run(alpha, eta, eps=0.0, steps=args.steps)
        ax.plot(traj[:, 0], traj[:, 1], lw=0.8)
        ax.set_title(f"alpha={alpha}, eta={eta}, eta/alpha={eta / alpha:.1f}")
        ax.set_aspect("equal")
    plt.tight_layout()
    orbit_path = output_dir / "orbit_sweep.png"
    plt.savefig(orbit_path, dpi=180)
    plt.close(fig)

    fig2, axes2 = plt.subplots(3, 3, figsize=(10, 10))
    for ax, (alpha, eta) in zip(axes2.ravel(), cases):
        traj = run(alpha, eta, eps=0.0, steps=args.steps)
        ax.hist(curvature(traj), bins=50)
        ax.set_title(f"eta/alpha={eta / alpha:.1f}")
    plt.tight_layout()
    curvature_path = output_dir / "curvature_sweep.png"
    plt.savefig(curvature_path, dpi=180)
    plt.close(fig2)

    print(f"Wrote {orbit_path}")
    print(f"Wrote {curvature_path}")


if __name__ == "__main__":
    main()
