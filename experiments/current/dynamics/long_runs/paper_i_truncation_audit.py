"""Compare FIFO impulse-response variance with the Paper I AR(1) baseline."""
from pathlib import Path
import json
import math
import statistics


ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'reports/long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.json'
OUTPUT = ROOT / 'reports/long_runs/scalar_hardening/paper_i_truncation_audit_2026-10-09.json'


def impulse_energy(alpha, horizon, gain, steps, cloud=False):
    q = 1.0 - alpha
    tail = q ** horizon
    deposition = alpha / (1.0 - tail)
    history = [0.0] * horizon
    head = 0
    x = center = second_moment = energy = 0.0
    for n in range(steps):
        x_next = x - gain * (x - center) + (1.0 if n == 0 else 0.0)
        oldest = history[head]
        center = q * center + deposition * (x_next - tail * oldest)
        second_moment = q * second_moment + deposition * (x_next ** 2 - tail * oldest ** 2)
        history[head] = x_next
        head = (head + 1) % horizon
        x = x_next
        energy += max(0.0, second_moment - center ** 2) if cloud else (x - center) ** 2
    return energy


def main():
    # Predeclared resolution gate and scientific tolerance, before output.
    tolerance = 0.001  # 0.1% radius difference; finer than reported ~1% errors.
    convergence_tolerance = 1e-10
    assert impulse_energy(0.01, 1, 0.4, 100) < 1e-24
    alpha, horizon = 0.01, 600
    q = 1.0 - alpha
    weights = [alpha * q ** j / (1.0 - q ** horizon) for j in range(horizon)]
    cumulative = 0.0
    random_walk_energy = 0.0
    for weight in weights:
        cumulative += weight
        random_walk_energy += (1.0 - cumulative) ** 2
    assert abs(impulse_energy(alpha, horizon, 0.0, 4000) - random_walk_energy) < 1e-9
    source = json.loads(SOURCE.read_text(encoding='utf-8'))
    records = []
    cache = {}
    for record in source['records']:
        if record['condition'] != 'baseline':
            continue
        assert record['memory_horizon'] == horizon
        gain = record['restoring_per_update_nominal'] * record['stored_memory_mass']
        if gain not in cache:
            short = impulse_energy(alpha, horizon, gain, 20000)
            long = impulse_energy(alpha, horizon, gain, 40000)
            assert abs(long / short - 1.0) < convergence_tolerance
            cache[gain] = long
        radius = math.sqrt(record['dim'] * cache[gain]) * record['epsilon']
        cloud_short = impulse_energy(alpha, horizon, gain, 20000, cloud=True)
        cloud_long = impulse_energy(alpha, horizon, gain, 40000, cloud=True)
        assert abs(cloud_long / cloud_short - 1.0) < convergence_tolerance
        cloud_radius = math.sqrt(record['dim'] * cloud_long) * record['epsilon']
        difference = radius / record['retained_mass_prediction'] - 1.0
        records.append(dict(dim=record['dim'], steps=record['steps'],
                            amplitude_att=record['amplitude_att'], gain=gain,
                            finite_h_radius=radius,
                            finite_h_memory_cloud_rms=cloud_radius,
                            cloud_measured_relative_difference=record['measured_radius_median'] / cloud_radius - 1.0,
                            ar1_radius=record['retained_mass_prediction'],
                            relative_truncation_difference=difference,
                            measured_relative_error=abs(record['measured_radius_median'] / radius - 1.0)))
    result = dict(alpha=alpha, horizon=horizon, tail_weight=q ** horizon,
                  method='Squared causal impulse response of native linear FIFO update; numerical infinite-sum approximation',
                  observable_caveat='Stored measurement is a median memory-cloud radius, not the stationary RMS of x-center. Cloud RMS is a distinct reference; median and RMS must also be distinguished.',
                  radius_tolerance=tolerance, convergence_tolerance=convergence_tolerance,
                  impulse_lengths=[20000, 40000],
                  max_relative_truncation_difference=max(abs(r['relative_truncation_difference']) for r in records),
                  median_measured_relative_error=statistics.median(r['measured_relative_error'] for r in records),
                  max_measured_relative_error=max(r['measured_relative_error'] for r in records),
                  records=records)
    result['tolerance_pass'] = result['max_relative_truncation_difference'] < tolerance
    OUTPUT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, indent=2))


if __name__ == '__main__':
    main()
