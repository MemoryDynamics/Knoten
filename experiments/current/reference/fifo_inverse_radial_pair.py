"""Inverse radial reference for two isolated FIFO cycles, not a native kernel."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np

from emergenz_knoten.kernels import exponential_memory_weights
from emergenz_knoten.vector_memory import vector_gaussian_field


SCALE = 10**8
PERIOD = 10
EDGES = tuple(combinations(range(PERIOD), 2))
BASIS_COLUMNS = tuple(range(38)) + (39, 40)
V_WEIGHTS = exponential_memory_weights(0.001, PERIOD)
S_WEIGHTS = 0.5 ** np.arange(PERIOD)
NUMERATORS = np.array(
    [
        [
            (79123542, 45614746, 32215461, 24980200),
            (-395344108, -228237532, -161278906, -125161100),
            (-78961542, 45482446, 32396361, 25043200),
            (395406208, -228174532, -161312206, -124816400),
            (62100, -91103493, 32235261, 24850600),
            (-39600, 456286065, -161514706, -125007200),
            (-140400, -7200, -97021684, 25200700),
            (-197100, 200700, 483956418, -124935200),
            (-166500, 64800, -5400, -99919000),
            (-5400, 81000, -123300, 499839800),
        ],
        [
            (79049742, 45446446, 32475561, 24833500),
            (553599291, 319338325, 225988829, 174994600),
            (-78992142, 45638146, 32355861, 24876700),
            (158194883, -365271672, -258359090, -200024300),
            (-160200, -91311393, 32111961, 24882100),
            (-237333725, 319386925, -258082790, -199908200),
            (116100, 91800, -97009984, 25195300),
            (-237356225, -136735339, 387179535, -200216900),
            (-118800, -216900, -93600, -100196200),
            (-237264425, -137126839, -96891184, 424847900),
        ],
    ],
    dtype=np.int64,
)


def integer_force_matrix(numerators):
    """Scale the radial design matrix by SCALE * 2**9 for rank certification."""
    matrix = np.zeros((4 * PERIOD, len(EDGES)), dtype=np.int64)
    for e, (i, j) in enumerate(EDGES):
        delta = numerators[i] - numerators[j]
        age = j - i
        matrix[4 * i : 4 * i + 4, e] = (2 ** (9 - age)) * delta
        matrix[4 * j : 4 * j + 4, e] = -(2 ** (age - 1)) * delta
    return matrix


def phase_history(points, phase):
    return points[(phase + np.arange(PERIOD + 1)) % PERIOD]


def _native_vector(history):
    steps = history[:-1] - history[1:]
    directions = steps / np.linalg.norm(steps, axis=1, keepdims=True)
    return vector_gaussian_field(
        history[0], history[:-1], directions, V_WEIGHTS, sigma=1.0
    )


@dataclass(frozen=True)
class RadialProfile:
    distances_squared: np.ndarray
    values: np.ndarray
    half_width: float
    slope: float

    def __call__(self, distances_squared):
        delta = np.asarray(distances_squared)[..., None] - self.distances_squared
        scaled = delta / self.half_width
        inside = np.abs(scaled) < 1
        bump = np.zeros_like(scaled)
        sq = scaled[inside] ** 2
        bump[inside] = np.exp(-sq / (1 - sq))
        return np.sum(bump * (self.values + self.slope * delta), axis=-1)


def inverse_reference(*, slope=0.0):
    """Fit one radial profile to the fixed plus and minus reference cycles."""
    nodes, values = [], []
    for numerators in NUMERATORS:
        points = numerators / SCALE
        matrix = integer_force_matrix(numerators) / (SCALE * 2**9)
        rhs = np.stack(
            [
                points[i - 1] - points[i] - _native_vector(phase_history(points, i))
                for i in range(PERIOD)
            ]
        )
        force_values, _, rank, _ = np.linalg.lstsq(matrix, rhs.ravel(), rcond=None)
        if rank != matrix.shape[0]:
            raise ArithmeticError("unresolved numerical rank in inverse reference")
        delta = np.stack([points[i] - points[j] for i, j in EDGES])
        nodes.extend(np.einsum("ij,ij->i", delta, delta))
        values.extend(force_values)
    nodes = np.asarray(nodes)
    half_width = np.min(np.diff(np.sort(nodes))) / 3
    return RadialProfile(nodes, np.asarray(values), half_width, slope)


def reference_head(history, profile):
    """One head substitution with identical read/write rules in both cycles."""
    delta = history[0] - history[:-1]
    distances_squared = np.einsum("ij,ij->i", delta, delta)
    drift = (S_WEIGHTS * profile(distances_squared)) @ delta
    return history[0] + drift + _native_vector(history)
