import numpy as np

from emergenz_knoten.reciprocal_modes import reciprocal_scalar_memory_modes


def _full_two_node_matrix(lambda_value: float, g: float, c: float) -> np.ndarray:
    q = 1.0 - lambda_value
    visible = np.array(
        [
            [1.0 - g - c, 0.0, g, c],
            [0.0, 1.0 - g - c, c, g],
        ],
        dtype=float,
    )
    matrix = np.zeros((4, 4), dtype=float)
    matrix[:2] = visible
    matrix[2] = lambda_value * visible[0]
    matrix[2, 2] += q
    matrix[3] = lambda_value * visible[1]
    matrix[3, 3] += q
    return matrix


def test_common_and_relative_formulas_match_the_full_four_state_map() -> None:
    lambda_value = 0.07
    self_gain = 0.02
    cross_gain = 0.08
    result = reciprocal_scalar_memory_modes(
        lambda_value,
        self_gain=self_gain,
        cross_gain=cross_gain,
    )
    expected = np.linalg.eigvals(
        _full_two_node_matrix(lambda_value, self_gain, cross_gain)
    )
    observed = np.asarray(
        [*result.common_multipliers, *result.relative_multipliers],
        dtype=complex,
    )
    expected = expected[np.lexsort((expected.imag, expected.real))]
    observed = observed[np.lexsort((observed.imag, observed.real))]
    assert np.allclose(observed, expected)


def test_compact_baseline_stays_real_across_positive_stable_cross_gains() -> None:
    lambda_value = 0.01
    self_gain = 0.15 * (35.0 / 9.0 - 1.0)
    cross_gains = np.linspace(0.0, 1.0 - self_gain - 1.0e-8, 2001)
    results = [
        reciprocal_scalar_memory_modes(
            lambda_value,
            self_gain=self_gain,
            cross_gain=float(cross_gain),
        )
        for cross_gain in cross_gains
    ]
    assert all(not result.relative_is_complex for result in results)
