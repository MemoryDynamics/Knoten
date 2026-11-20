"""Permutation-projected correlated Gaussians for the declared L=0 reference.

Analytic Gaussian integrals and SciPy/LAPACK Ritz diagonalization; no training,
parameter optimization, or automatic AL1 execution. Units are caller supplied.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from time import monotonic

import numpy as np
from scipy.linalg import eigh

from experiments.current.reference import nucleon_spatial_preflight as al1


JACOBI = np.array(
    [
        [1 / np.sqrt(2), -1 / np.sqrt(2), 0],
        [1 / np.sqrt(6), 1 / np.sqrt(6), -2 / np.sqrt(6)],
    ]
)
POSITIONS = JACOBI.T
PAIR_VECTORS = np.array([POSITIONS[i] - POSITIONS[j] for i, j in al1.PAIRS])


@dataclass(frozen=True)
class Hamiltonian:
    mass: float
    coulomb: float = 0.0
    linear: float = 0.0
    spin_gaussian: float = 0.0
    spin_range: float = 1.0
    constant: float = 0.0
    oscillator: float = 0.0

    def __post_init__(self):
        if not all(np.isfinite(value) for value in vars(self).values()):
            raise ValueError("Hamiltonian coefficients must be finite")
        if self.mass <= 0 or self.spin_range <= 0:
            raise ValueError("mass and spin range must be positive")


def declared_al1() -> Hamiltonian:
    """The previously frozen operator, including color factor and energy offset."""
    r0 = al1.A_GEV_B_MINUS_1 * al1.MASS_GEV ** (-al1.B)
    return Hamiltonian(
        mass=al1.MASS_GEV,
        coulomb=-al1.KAPPA / 2,
        linear=al1.STRING_GEV2 / 2,
        spin_gaussian=al1.KAPPA_SPIN / (3 * np.sqrt(np.pi) * al1.MASS_GEV**2 * r0**3),
        spin_range=r0,
        constant=3 * al1.MASS_GEV - 1.5 * al1.OFFSET_GEV - al1.C_GEV4 / al1.MASS_GEV**3,
    )


def positive_matrix(matrix: np.ndarray) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=float)
    if matrix.shape != (2, 2) or not np.all(np.isfinite(matrix)):
        raise ValueError("Gaussian exponent must be a finite 2x2 matrix")
    if not np.allclose(matrix, matrix.T, atol=1e-14, rtol=0):
        raise ValueError("Gaussian exponent must be symmetric")
    if np.linalg.eigvalsh(matrix)[0] <= 0:
        raise ValueError("Gaussian exponent must be positive definite")
    return matrix


def gaussian_integrals(a: np.ndarray, b: np.ndarray) -> dict[str, np.ndarray | float]:
    """Normalized exp(-x^T A x), with two 3-vector Jacobi coordinates."""
    a, b = positive_matrix(a), positive_matrix(b)
    c = a + b
    inverse = np.linalg.inv(c)
    overlap = float(
        np.exp(
            0.75 * (np.linalg.slogdet(2 * a)[1] + np.linalg.slogdet(2 * b)[1])
            - 1.5 * np.linalg.slogdet(c)[1]
        )
    )
    pair_u = np.einsum("pi,ij,pj->p", PAIR_VECTORS, inverse, PAIR_VECTORS)
    position_u = np.einsum("pi,ij,pj->p", POSITIONS, inverse, POSITIONS)
    return {
        "overlap": overlap,
        "kinetic_times_mass": float(3 * np.trace(a @ b @ inverse)),
        "internal_r2": float(1.5 * np.trace(inverse)),
        "pair_u": pair_u,
        "position_u": position_u,
        "inverse_distance": 2 / np.sqrt(np.pi * pair_u),
        "distance": 2 * np.sqrt(pair_u / np.pi),
    }


def _doublet() -> np.ndarray:
    states = np.zeros((2, 2, 2, 2))
    states[0, 1, 0, 0] = 1 / np.sqrt(2)
    states[1, 0, 0, 0] = -1 / np.sqrt(2)
    states[0, 0, 1, 1] = np.sqrt(2 / 3)
    states[0, 1, 0, 1] = states[1, 0, 0, 1] = -1 / np.sqrt(6)
    return states.reshape(8, 2)


def internal_basis(sector: str) -> np.ndarray:
    """S_z=I_z=+1/2; four N channels or one Delta(uud) channel."""
    if sector == "nucleon":
        factors = _doublet()
    elif sector == "delta":
        factors = np.zeros((8, 1))
        factors[[1, 2, 4], 0] = 1 / np.sqrt(3)
    else:
        raise ValueError("sector must be nucleon or delta")
    n = factors.shape[1]
    basis = np.empty((64, n * n))
    for labels in product(range(4), repeat=3):
        flavor = np.ravel_multi_index(tuple(label // 2 for label in labels), (2, 2, 2))
        spin = np.ravel_multi_index(tuple(label % 2 for label in labels), (2, 2, 2))
        basis[np.ravel_multi_index(labels, (4, 4, 4))] = np.outer(
            factors[spin], factors[flavor]
        ).ravel()
    return basis


def sector_data(sector: str) -> dict:
    basis = internal_basis(sector)
    n = basis.shape[1]
    symmetries = []
    for permutation in permutations(range(3)):
        d = JACOBI @ np.eye(3)[list(permutation)] @ JACOBI.T
        inverse = tuple(np.argsort(permutation))
        permuted = basis.reshape(4, 4, 4, n).transpose((*inverse, 3)).reshape(64, n)
        symmetries.append((d, basis.T @ permuted))
    labels = np.indices((4, 4, 4)).reshape(3, 64)
    up = labels < 2
    sigma_z = 1 - 2 * (labels % 2)

    def diagonal(values):
        return basis.T @ (values[:, None] * basis)

    return {
        "basis": basis,
        "identity": np.eye(n),
        "symmetries": symmetries,
        "spin_pairs": np.array(
            [(basis.T @ op @ basis).real for op in al1.spin_pair_operators()]
        ),
        "charge_p": np.array(
            [diagonal(np.where(is_up, 2 / 3, -1 / 3)) for is_up in up]
        ),
        "charge_n": np.array(
            [diagonal(np.where(is_up, -1 / 3, 2 / 3)) for is_up in up]
        ),
        "up_spin": diagonal(np.sum(up * sigma_z, axis=0)),
        "down_spin": diagonal(np.sum((~up) * sigma_z, axis=0)),
    }


def primitive_blocks(
    a, b, data, model: Hamiltonian, q_squared: float = 0.0
) -> dict[str, np.ndarray]:
    """Unprojected blocks; charge observables use the NR impulse convention."""
    if not np.isfinite(q_squared) or q_squared < 0:
        raise ValueError("q_squared must be finite and nonnegative")
    g = gaussian_integrals(a, b)
    identity = data["identity"]
    kinetic = g["kinetic_times_mass"] / model.mass
    scalar = kinetic + model.constant + model.oscillator * g["internal_r2"]
    scalar += np.sum(
        model.coulomb * g["inverse_distance"] + model.linear * g["distance"]
    )
    spin_coefficients = model.spin_gaussian * (
        1 + g["pair_u"] / model.spin_range**2
    ) ** (-1.5)
    hamiltonian = scalar * identity + np.einsum(
        "p,pij->ij", spin_coefficients, data["spin_pairs"]
    )
    blocks = {
        "overlap": identity,
        "hamiltonian": hamiltonian,
        "kinetic": kinetic * identity,
        "matter_radius2": g["internal_r2"] / 3 * identity,
        "up_spin": data["up_spin"],
        "down_spin": data["down_spin"],
    }
    for species in ("p", "n"):
        charge = data[f"charge_{species}"]
        blocks[f"charge_{species}_radius2"] = np.einsum(
            "p,pij->ij", 1.5 * g["position_u"], charge
        )
        blocks[f"form_factor_{species}"] = np.einsum(
            "p,pij->ij", np.exp(-q_squared * g["position_u"] / 4), charge
        )
    return {key: g["overlap"] * value for key, value in blocks.items()}


def projected_blocks(a, b, data, model, q_squared=0.0) -> dict[str, np.ndarray]:
    """<P A|O|P B>=<A|O P|B> for the invariant observables below."""
    result = {}
    for d, internal in data["symmetries"]:
        for key, block in primitive_blocks(
            a, d.T @ b @ d, data, model, q_squared
        ).items():
            if key not in result:
                result[key] = np.zeros_like(block)
            result[key] += block @ internal / 6
    return result


def assemble(
    exponents, sector: str, model: Hamiltonian, *, q_squared=0.0, deadline=None
):
    exponents = [positive_matrix(a) for a in exponents]
    if not exponents:
        raise ValueError("at least one Gaussian is required")
    data = sector_data(sector)
    n = data["identity"].shape[0]
    matrices = {}
    for i, a in enumerate(exponents):
        for j, b in enumerate(exponents):
            if deadline is not None and monotonic() >= deadline:
                raise TimeoutError("fixed assembly deadline reached")
            for key, block in projected_blocks(a, b, data, model, q_squared).items():
                if key not in matrices:
                    matrices[key] = np.empty((n * len(exponents),) * 2)
                matrices[key][i * n : (i + 1) * n, j * n : (j + 1) * n] = block
    return matrices


def ritz_ground(hamiltonian, overlap, *, relative_cutoff=1e-10) -> dict:
    """Remove metric null directions explicitly; never regularize by adding a ridge."""
    hamiltonian, overlap = np.asarray(hamiltonian), np.asarray(overlap)
    if (
        hamiltonian.ndim != 2
        or hamiltonian.shape[0] != hamiltonian.shape[1]
        or overlap.shape != hamiltonian.shape
    ):
        raise ValueError("equally sized square matrices required")
    if not 0 < relative_cutoff < 1:
        raise ValueError("relative_cutoff must be between zero and one")
    for matrix in (hamiltonian, overlap):
        if not np.all(np.isfinite(matrix)) or not np.allclose(
            matrix, matrix.conj().T, rtol=0, atol=1e-11 * max(1, np.linalg.norm(matrix))
        ):
            raise ValueError("finite Hermitian matrices required")
    metric_values, metric_vectors = eigh(overlap)
    maximum = metric_values[-1]
    if maximum <= 0 or metric_values[0] < -1e-12 * maximum:
        raise ValueError("overlap must be positive semidefinite and nonzero")
    keep = metric_values > relative_cutoff * maximum
    whitening = metric_vectors[:, keep] / np.sqrt(metric_values[keep])
    reduced = whitening.conj().T @ hamiltonian @ whitening
    values, vectors = eigh((reduced + reduced.conj().T) / 2)
    coefficients = whitening @ vectors[:, 0]
    residual = hamiltonian @ coefficients - values[0] * overlap @ coefficients
    scale = (
        np.linalg.norm(hamiltonian) + abs(values[0]) * np.linalg.norm(overlap)
    ) * np.linalg.norm(coefficients)
    return {
        "energy": float(values[0]),
        "coefficients": coefficients,
        "rank": int(np.sum(keep)),
        "raw_dimension": len(metric_values),
        "metric_eigenvalues": metric_values,
        "retained_condition": float(maximum / metric_values[keep][0]),
        "relative_matrix_residual": float(
            np.linalg.norm(residual) / max(scale, np.finfo(float).tiny)
        ),
        "metric_norm": float(np.vdot(coefficients, overlap @ coefficients).real),
    }


def expectations(matrices, coefficients) -> dict[str, float]:
    norm = np.vdot(coefficients, matrices["overlap"] @ coefficients).real
    if norm <= 0:
        raise ValueError("positive metric norm required")
    return {
        key: float(np.vdot(coefficients, matrix @ coefficients).real / norm)
        for key, matrix in matrices.items()
    }


def proposed_exponents(level: int) -> list[np.ndarray]:
    """Frozen nested grids, not an outcome-selected or optimized basis."""
    ranges = (
        (0.5, 2.0, 8.0),
        (0.5, 2.0, 8.0, 1.0, 4.0),
        (0.5, 2.0, 8.0, 1.0, 4.0, 0.25, 16.0),
    )
    if level not in (0, 1, 2):
        raise ValueError("level must be 0, 1, or 2")
    return [
        np.array([[1 / x**2, correlation / (x * y)], [correlation / (x * y), 1 / y**2]])
        for x, y, correlation in product(ranges[level], ranges[level], (0.0, 0.4))
    ]
