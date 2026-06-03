from emergenz_knoten import SimulationConfig, simulate_finite_memory_numba
cfg = SimulationConfig(steps=100, dim=7, alpha=0.002, sample_every=20)
res = simulate_finite_memory_numba(cfg, seed=1)
print(res['samples'].shape, res['sample_steps'])
