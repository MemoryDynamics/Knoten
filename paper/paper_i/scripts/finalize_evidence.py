"""Rebuild Paper I evidence from a committed terminal-trace extract.

Extraction reads historical outputs; rebuilding never launches new simulations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "paper/paper_i"
EVIDENCE = PAPER / "evidence"


def linear_energies(alpha: float, horizon: int, gain: float, steps: int = 20000):
    """Numerical H2 energies for position-relative and cloud observables."""
    if not 0 < alpha < 1 or horizon < 1 or not 0 <= gain < 1:
        raise ValueError("require 0<alpha<1, H>=1 and 0<=g<1")
    q = 1 - alpha
    tail = q ** horizon
    a = alpha / (1 - tail)
    history = np.zeros(horizon)
    x = center = moment = relative_energy = cloud_energy = 0.0
    head = 0
    for n in range(steps):
        x_new = x - gain * (x - center) + (1.0 if n == 0 else 0.0)
        oldest = history[head]
        center = q * center + a * (x_new - tail * oldest)
        moment = q * moment + a * (x_new * x_new - tail * oldest * oldest)
        history[head] = x_new
        head = (head + 1) % horizon
        x = x_new
        variance = moment - center * center
        if variance < -1e-12:
            raise ArithmeticError("negative cloud variance beyond rounding tolerance")
        relative_energy += (x - center) ** 2
        cloud_energy += max(0.0, variance)
    return np.array([relative_energy, cloud_energy])


def spectral_energies(alpha: float, horizon: int, gain: float, points=131072):
    """Independent midpoint spectral integral; uses no FIFO recurrence."""
    omega = (np.arange(points) + 0.5) * math.pi / points
    z = np.exp(-1j * omega)
    q = 1 - alpha
    b = alpha / (1 - q ** horizon) * (1 - (q * z) ** horizon) / (1 - q * z)
    denominator = 1 - z + gain * z * (1 - b)
    power = 1 / np.abs(denominator) ** 2
    return np.array([np.mean(np.abs(1 - b) ** 2 * power),
                     np.mean((1 - np.abs(b) ** 2) * power)])


def terminal_start(steps):
    """Select the maximal regularly sampled terminal block."""
    steps = np.asarray(steps, dtype=np.int64)
    if len(steps) < 2 or np.any(np.diff(steps) <= 0):
        raise ValueError("trace times must be strictly increasing")
    gaps = np.diff(steps)
    start = len(steps) - 2
    while start > 0 and gaps[start - 1] == gaps[-1]:
        start -= 1
    if len(steps) - start < 100:
        raise ValueError("terminal block too short")
    return start


def extract(source_root: Path):
    historical = json.loads((ROOT / "reports/long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.json").read_text())
    arrays, metadata = {}, []
    for slice_index, record in enumerate(historical["records"]):
        source_dir = source_root / Path(record["source"]).name
        condition = record["condition"]
        files = sorted(source_dir.glob(f"case_{condition}_seed*_steps{record['steps']}.json"))
        if len(files) != 5:
            raise ValueError(f"need five cases in {source_dir}: {condition}")
        for path in files:
            payload = path.read_bytes()
            case = json.loads(payload)
            trace = case["diagnostics"]["dynamic_center_trace"]["trace"]
            start = terminal_start(trace["steps"])
            key = f"slice{slice_index:02d}_seed{case['seed']}"
            times = np.asarray(trace["steps"][start:], dtype=np.int64)
            cloud = np.asarray(trace["rms_radii"][start:])
            relative = np.asarray(trace["x_distances"][start:])
            if not (len(times) == len(cloud) == len(relative)) or not np.isfinite(cloud).all() or not np.isfinite(relative).all():
                raise ValueError("invalid trace arrays")
            arrays[key + "_steps"] = times
            arrays[key + "_cloud"] = cloud
            arrays[key + "_relative"] = relative
            config = case["config"]
            assert config["alpha"] == 0.01 and case["memory_horizon"] == 600
            expected_eta = 0.15 if condition == "baseline" else 0.0
            if config["deposition_kernel"] != "delta" or config["eta"] != expected_eta:
                raise ValueError(f"unexpected model convention in {path}")
            if config["sigma_rep"] != 1.0 or config["sigma_att"] != 3.0 or config["amplitude_rep"] != 1.0 or config["memory_mass"] != 1.0:
                raise ValueError(f"unexpected kernel or memory normalization in {path}")
            if config["dim"] != record["dim"] or config["steps"] != record["steps"] or config["epsilon"] != record["epsilon"]:
                raise ValueError(f"slice metadata mismatch in {path}")
            curvature = config["amplitude_att"] / config["sigma_att"] ** 2 - config["amplitude_rep"] / config["sigma_rep"] ** 2
            gain = config["eta"] * case["stored_weight_mass"] * curvature
            metadata.append(dict(key=key, slice=slice_index, seed=case["seed"],
                                 condition=condition, dim=record["dim"], steps=record["steps"],
                                 amplitude_att=record["amplitude_att"],
                                 epsilon=config["epsilon"], alpha=config["alpha"],
                                 horizon=case["memory_horizon"],
                                 gain=gain,
                                 stored_mass=record["stored_memory_mass"],
                                 source=f"{record['source']}/{path.name}", source_sha256=hashlib.sha256(payload).hexdigest(),
                                 source_revision=case["git_revision"], count=len(times),
                                 first_step=int(times[0]), last_step=int(times[-1]), stride=int(times[1]-times[0])))
    EVIDENCE.mkdir(exist_ok=True)
    np.savez_compressed(EVIDENCE / "terminal_traces.npz", **arrays)
    manifest = dict(description="Extracted terminal cloud and position-relative radii; no fitted parameters", cases=metadata,
                    archive_sha256=hashlib.sha256((EVIDENCE / "terminal_traces.npz").read_bytes()).hexdigest())
    (EVIDENCE / "trace_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def rebuild():
    manifest = json.loads((EVIDENCE / "trace_manifest.json").read_text())
    assert hashlib.sha256((EVIDENCE / "terminal_traces.npz").read_bytes()).hexdigest() == manifest["archive_sha256"]
    archive = np.load(EVIDENCE / "terminal_traces.npz", allow_pickle=False)
    summaries, seed_rows, references = [], [], {}
    for case in manifest["cases"]:
        key = case["key"]
        cache_key = (case["alpha"], case["horizon"], case["gain"])
        if cache_key not in references:
            short = linear_energies(*cache_key)
            long = linear_energies(*cache_key, steps=40000)
            spectrum = spectral_energies(*cache_key)
            if np.max(np.abs(long / short - 1)) > 1e-9 or np.max(np.abs(spectrum / short - 1)) > 1e-7:
                raise ArithmeticError("linear references do not converge or agree")
            references[cache_key] = dict(energies=short.tolist(),
                                        doubling_error=float(np.max(np.abs(long / short - 1))),
                                        spectral_error=float(np.max(np.abs(spectrum / short - 1))))
        energies = references[cache_key]["energies"]
        observed = [float(np.sqrt(np.mean(archive[key + "_" + name] ** 2))) for name in ("relative", "cloud")]
        half_ratios = {}
        for name, prediction in zip(("relative", "cloud"), [math.sqrt(case["dim"] * energy) * case["epsilon"] for energy in energies]):
            halves = np.array_split(archive[key + "_" + name], 2)
            half_ratios[name] = [float(np.sqrt(np.mean(h*h)) / prediction) for h in halves]
        predicted = [math.sqrt(case["dim"] * energy) * case["epsilon"] for energy in energies]
        seed_rows.append(dict(**case, observed_relative=observed[0], observed_cloud=observed[1],
                              predicted_relative=predicted[0], predicted_cloud=predicted[1],
                              half_window_ratios=half_ratios,
                              relative_ratio=observed[0] / predicted[0], cloud_ratio=observed[1] / predicted[1]))
    for slice_index in sorted(set(c["slice"] for c in seed_rows)):
        rows = [c for c in seed_rows if c["slice"] == slice_index]
        row = rows[0]
        summary = {k: row[k] for k in ("slice", "condition", "dim", "steps", "amplitude_att", "gain", "predicted_relative", "predicted_cloud", "count", "stride")}
        for name in ("relative", "cloud"):
            values = [r[name + "_ratio"] for r in rows]
            summary[name + "_ratio"] = float(np.median(values))
            summary[name + "_q1"], summary[name + "_q3"] = np.quantile(values, [0.25, 0.75]).tolist()
        summaries.append(summary)
    active = [r for r in summaries if r["condition"] == "baseline"]
    controls = [r for r in summaries if r["condition"] == "eta_zero"]
    errors = {}
    for label, group in (("active", active), ("controls", controls)):
        for name in ("relative", "cloud"):
            differences = [abs(r[name + "_ratio"] - 1) for r in group]
            errors[label + "_" + name + "_median"] = float(np.median(differences))
            errors[label + "_" + name + "_max"] = float(max(differences))
    output = dict(method="Median over five seeds of terminal temporal RMS / fixed linear FIFO RMS", confidence="IQR is seed dispersion, not a confidence interval", reference_checks=[dict(alpha=k[0], horizon=k[1], gain=k[2], **v) for k,v in references.items()], errors=errors, slices=summaries, seeds=seed_rows)
    (EVIDENCE / "matched_radius_results.json").write_text(json.dumps(output, indent=2) + "\n")
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8), sharey=True)
    for ax, name, title in zip(axes, ("cloud", "relative"), ("(a) Memory-cloud RMS", "(b) Position-relative RMS")):
        for group, marker, color, label in ((active, "o", "#177c68", "Feedback"), (controls, "s", "#a94b38", "No feedback")):
            y = np.array([r[name + "_ratio"] for r in group])
            lo = np.array([r[name + "_q1"] for r in group])
            hi = np.array([r[name + "_q3"] for r in group])
            ax.errorbar([r["slice"] for r in group], y, yerr=[y-lo, hi-y], fmt=marker, color=color, markersize=4, capsize=2, linewidth=0.8, label=label)
        ax.axhline(1, color="#555555", linewidth=0.8, linestyle="--")
        ax.set(title=title, xlabel="Slice ID (Table I)")
        ax.grid(axis="y", alpha=0.15)
    axes[0].set_ylabel("Measured / linear FIFO prediction")
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(PAPER / "figures/matched_radius.pdf")
    fig.savefig(PAPER / "figures/matched_radius.png", dpi=180)
    plt.close(fig)
    row_end = chr(92) * 2
    lines = ["\\begin{tabular}{rrrrrr}", "\\hline\\hline", "ID & $d$ & $N/10^6$ & $A_a$ & $R_Q/R_{Q,H}$ & $R_r/R_{r,H}$ " + row_end, "\\hline"]
    for r in summaries:
        amplitude = f"{r['amplitude_att']:.0f}" if r["condition"] == "baseline" else "off"
        lines.append(f"{r['slice']} & {r['dim']} & {r['steps']/1e6:.0f} & {amplitude} & {r['cloud_ratio']:.4f} & {r['relative_ratio']:.4f} " + row_end)
    lines += ["\\hline\\hline", "\\end{tabular}"]
    (EVIDENCE / "radius_table.tex").write_text("\n".join(lines) + "\n")
    macros = {"CloudMedianError": 100*errors["active_cloud_median"], "CloudMaxError": 100*errors["active_cloud_max"],
              "RelativeMedianError": 100*errors["active_relative_median"], "RelativeMaxError": 100*errors["active_relative_max"],
              "ControlCloudMaxError":100*errors["controls_cloud_max"]}
    (EVIDENCE / "result_macros.tex").write_text("\n".join("\\newcommand{\\" + k + "}{" + f"{v:.3f}" + "}" for k,v in macros.items())+"\n")
    control_figures()
    print(json.dumps(errors, indent=2))


def control_figures():
    family = json.loads((ROOT / "reports/kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.json").read_text())
    nonlinear = json.loads((ROOT / "reports/kernels/nonlinearity/fixed_g_RL_d3_N300k_A26_2026-07-19.json").read_text())
    fig, axes = plt.subplots(1,2,figsize=(7.0,2.8))
    for field, marker, color, label in (("single_support","o","#177c68","Attractive only"),("two_scale_support","s","#a94b38","Two scales")):
        rows = family[field]
        x=np.array([r["effective_amplitude"] for r in rows])
        y=np.array([r["dynamic_radius_median"] for r in rows])*1e4
        lo=np.array([r["dynamic_radius_q1"] for r in rows])*1e4
        hi=np.array([r["dynamic_radius_q3"] for r in rows])*1e4
        axes[0].errorbar(x,y,yerr=[y-lo,hi-y],fmt=marker+"-",color=color,markersize=3,linewidth=0.8,capsize=2,label=label)
    axes[0].set(xlabel="Effective amplitude",ylabel="Median cloud radius (units of 1e-4)",title="(a) Matched local curvature")
    axes[0].legend(frameon=False,fontsize=8)
    rows=nonlinear["active_rows"]
    x=np.array(sorted(set(r["target_radius_ratio"] for r in rows)))
    low={r["seed"]:r["normalized_dynamic_radius"] for r in rows if r["target_radius_ratio"]==x[0]}
    ratios=[[r["normalized_dynamic_radius"]/low[r["seed"]] for r in rows if r["target_radius_ratio"]==target] for target in x]
    y=np.array([np.median(v) for v in ratios])
    lo=np.array([np.quantile(v,0.25) for v in ratios])
    hi=np.array([np.quantile(v,0.75) for v in ratios])
    # An endpoint ratio cancels any constant linear cloud/position conversion.
    axes[1].errorbar(x,y,yerr=[y-lo,hi-y],fmt="o-",color="#177c68",markersize=4,capsize=2,linewidth=0.8)
    axes[1].set(xlabel="Nominal position radius / kernel width",ylabel="Paired normalized radius ratio",title="(b) Fixed gain, increasing radius")
    axes[1].set_xscale("log")
    axes[1].set_xticks(x,["0.03","0.1","0.3"])
    for ax in axes:
        ax.grid(axis="y",alpha=0.15)
    fig.tight_layout()
    fig.savefig(PAPER / "figures/kernel_controls.pdf")
    fig.savefig(PAPER / "figures/kernel_controls.png",dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract-from", type=Path, help="Historical long_run_metastability directory")
    args = parser.parse_args()
    if args.extract_from:
        extract(args.extract_from)
    rebuild()
