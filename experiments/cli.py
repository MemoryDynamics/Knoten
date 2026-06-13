from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]

CATEGORIES = {
    "dimension_selection": [
        "DimensionsHeatmap.py",
        "DimensionsHeatmap2Opt.py",
        "DimensionsHeatmap3Opt.py",
        "DimensionsHeatmap4OptGPU.py",
        "DimensionsHeatmapOpt.py",
        "plotD.py",
        "plotDgpu.py",
    ],
    "propagation_speed": [
        "PaperII3D_4Plots.py",
        "PaperII3D_4Plots2.py",
        "PaperII3D_5Plots1.py",
        "PaperII3D_5Plots2.py",
    ],
    "knot_stability": [
        "Knoten.py",
        "Knoten3D.py",
        "Knoten3D_prism.py",
        "knot_chi_scan.py",
    ],
    "ou_limit": [
        "EmergenzGravitation.py",
        "emergenz_2regime.py",
        "fig_alpha_hbareff.py",
        "fig_Gamma_alpha.py",
        "fig_Hlamda_alpha.py",
        "Oszillationen.py",
        "OU-Limit.py",
    ],
    "fractal_analysis": [
        "analyze_dimension_claim.py",
        "reproduce_dimension_pilot.py",
        "Fraktale/FD2.py",
        "Fraktale/Fraktaldimension.py",
        "Fraktale/fit_n_plot.py",
        "Fraktale/results_plot.py",
        "Fraktale/analyze_peaks.py",
    ],
    "LQG": [
        "orbit_labor.py",
    ],
    "reference": [
        "reference_experiment.py",
    ],
}


def list_categories() -> None:
    print("Available experiment categories:")
    for category in sorted(CATEGORIES):
        print(f"- {category}")


def list_scripts(category: str) -> None:
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category: {category}")
    print(f"Available scripts for {category}:")
    for script in CATEGORIES[category]:
        print(f"- {script}")


def run_script(category: str, script: str, extra_args: list[str]) -> int:
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category: {category}")
    if script not in CATEGORIES[category]:
        raise ValueError(f"Unknown script for {category}: {script}")
    if category == "reference":
        script_path = ROOT / script
    else:
        script_path = ROOT / category / script
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")
    print(f"Running {category}/{script}...")
    return subprocess.run([sys.executable, str(script_path), *extra_args], cwd=str(script_path.parent)).returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run categorized experiment entry points for Emergenz Knoten."
    )
    parser.add_argument(
        "category",
        nargs="?",
        help="Experiment category to run or list.",
        choices=list(CATEGORIES.keys()),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available categories or scripts for a category.",
    )
    parser.add_argument(
        "--script",
        type=str,
        help="Script name to run within the selected category.",
    )
    parser.add_argument(
        "--args",
        nargs=argparse.REMAINDER,
        help="Additional arguments to pass to the selected script.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.category is None:
        if args.list:
            list_categories()
            return
        raise SystemExit("Please select a category or use --list.")

    if args.list:
        list_scripts(args.category)
        return

    if args.script is None:
        raise SystemExit(
            "Please provide --script SCRIPT for the selected category, or use --list to see available scripts."
        )

    extra_args = args.args or []
    code = run_script(args.category, args.script, extra_args)
    if code != 0:
        raise SystemExit(f"Script exited with code {code}")


if __name__ == "__main__":
    main()
