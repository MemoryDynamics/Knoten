from pathlib import Path

from emergenz_knoten import SimulationConfig, run_simulation


def main() -> None:
    config = SimulationConfig(
        steps=500,
        dim=3,
        alpha=0.05,
        sample_every=10,
        max_memory=100,
        burn_in=50,
    )
    output_path = Path("results/demo_simulation.npz")
    result = run_simulation(config, seed=1, output_path=output_path)
    print(f"Saved {result['samples'].shape} samples to {output_path}")


if __name__ == "__main__":
    main()
