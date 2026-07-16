from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CATEGORIES = {
    "anchors": [
        "current/anchors/anchor_paper_pipeline.py",
        "current/anchors/anchor_sensitivity_analysis.py",
    ],
    "dimension_selection": [
        "dimension_selection/heatmaps/DimensionsHeatmap.py",
        "dimension_selection/heatmaps/DimensionsHeatmap2Opt.py",
        "dimension_selection/heatmaps/DimensionsHeatmap3Opt.py",
        "dimension_selection/heatmaps/DimensionsHeatmap4OptGPU.py",
        "dimension_selection/heatmaps/DimensionsHeatmapOpt.py",
        "dimension_selection/heatmaps/plotD.py",
        "dimension_selection/heatmaps/plotDgpu.py",
    ],
    "dynamics": [
        "current/dynamics/aatt_transition_report.py",
        "current/dynamics/dimension_claim_audit.py",
        "current/dynamics/dspec_sensitivity_report.py",
        "current/dynamics/dspec_raw_snapshot_report.py",
        "current/dynamics/n_dependence_recheck_report.py",
        "current/dynamics/long_run_metastability.py",
        "current/dynamics/dynamic_center_trace_report.py",
        "current/dynamics/paper_i_evidence_table.py",
        "current/dynamics/ambient_dimension_memory_shape_report.py",
        "current/dynamics/epsilon_dynamic_center_sweep.py",
        "current/dynamics/epsilon_step_balance.py",
        "current/dynamics/epsilon_floor_visual_probe.py",
        "current/dynamics/scalar_n_scaling_report.py",
    ],
    "fractal_analysis": [
        "fractal_analysis/analyze_dimension_claim.py",
        "fractal_analysis/reproduce_dimension_pilot.py",
        "fractal_analysis/plot_d_alpha_n_intensity.py",
        "fractal_analysis/archive_source/scripts/FD2.py",
        "fractal_analysis/archive_source/scripts/Fraktaldimension.py",
        "fractal_analysis/archive_source/scripts/fit_n_plot.py",
        "fractal_analysis/archive_source/scripts/analyze_peaks.py",
    ],
    "kernels": [
        "current/kernels/kernel_shape_probe.py",
        "propagation_speed/ballistic_kernel_probe.py",
    ],
    "knot_stability": [
        "current/knot_stability/Knoten.py",
        "current/knot_stability/Knoten3D.py",
        "current/knot_stability/Knoten3D_prism.py",
        "current/knot_stability/knot_chi_scan.py",
    ],
    "markov": [
        "current/markov/ar_mode_probe.py",
        "current/markov/knot_score_report.py",
        "current/markov/long_run_trace_ar_report.py",
        "current/markov/feature_closure_report.py",
    ],
    "memory": [
        "current/memory/vector_memory_pilot.py",
    ],
    "propagation_speed": [
        "propagation_speed/PaperII3D_4Plots.py",
        "propagation_speed/PaperII3D_4Plots2.py",
        "propagation_speed/PaperII3D_5Plots1.py",
        "propagation_speed/PaperII3D_5Plots2.py",
        "propagation_speed/ballistic_kernel_probe.py",
    ],
    "reference": [
        "current/reference/reference_experiment.py",
        "current/reference/demo_simulation.py",
    ],
    "archive": [
        "archive/lqg/orbit_labor.py",
        "archive/ou_limit/EmergenzGravitation.py",
        "archive/ou_limit/emergenz_2regime.py",
        "archive/ou_limit/Oszillationen.py",
        "archive/ou_limit/OU-Limit.py",
        "archive/legacy/scripts/alpha_plateau_plot.py",
        "archive/legacy/scripts/debug_diagnostics.py",
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
    script_path = ROOT / script
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")
    print(f"Running {script}...")
    return subprocess.run([sys.executable, str(script_path), *extra_args], cwd=str(ROOT)).returncode


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
        help="Script path to run within the selected category.",
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
