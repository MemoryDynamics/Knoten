"""Legacy compatibility layer for the Emergenz Knoten simulation API."""

from .core import (
    SimulationConfig,
    simulate_finite_memory,
    simulate_finite_memory_numba,
)

__all__ = [
    "SimulationConfig",
    "simulate_finite_memory",
    "simulate_finite_memory_numba",
]
