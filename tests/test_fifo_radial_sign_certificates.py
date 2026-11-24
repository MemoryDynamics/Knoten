"""Verify radial sign certificates independently of the LP used to find them."""

from fractions import Fraction
import json
from pathlib import Path

from mpmath import iv
import numpy as np
import pytest

from experiments.current.reference.fifo_inverse_radial_pair import (
    EDGES,
    NUMERATORS,
    PERIOD,
    SCALE,
    integer_force_matrix,
)


CERTIFICATES = json.loads(
    Path(__file__)
    .with_name("fifo_radial_sign_certificates.json")
    .read_text(encoding="utf8")
)


def _dot(left, right):
    return sum(a * b for a, b in zip(left, right, strict=True))


def _complete_duals(matrix, outside, group):
    dependent = group["dependent"]
    free = sorted(set(range(matrix.shape[0])) - set(dependent))
    assert len(outside) == len(dependent)
    choices = group["free_numerators"]
    aug = [
        [Fraction(int(matrix[k, e])) for k in dependent]
        + [-Fraction(_dot([int(matrix[k, e]) for k in free], row)) for row in choices]
        for e in outside
    ]
    for col in range(len(dependent)):
        pivot = next(i for i in range(col, len(aug)) if aug[i][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for i in range(col + 1, len(aug)):
            if aug[i][col]:
                factor = aug[i][col] / aug[col][col]
                aug[i][col:] = [
                    a - factor * b
                    for a, b in zip(aug[i][col:], aug[col][col:], strict=True)
                ]
    for rhs, row in enumerate(choices, len(dependent)):
        result = [Fraction(0)] * matrix.shape[0]
        for k, val in zip(free, row, strict=True):
            result[k] = Fraction(val)
        for i in reversed(range(len(dependent))):
            known = _dot(
                aug[i][i + 1 : len(dependent)], [result[k] for k in dependent[i + 1 :]]
            )
            result[dependent[i]] = (aug[i][rhs] - known) / aug[i][i]
        yield [y / CERTIFICATES["denominator"] for y in result]


def _squared_distance(a, b):
    return sum((int(x) - int(y)) ** 2 for x, y in zip(a, b, strict=True))


def _interval_vector(numerators):
    q = iv.mpf(999) / 1000
    vectors = []
    for head in range(PERIOD):
        field = [iv.mpf(0) for _ in range(4)]
        for age in range(PERIOD):
            j = (head + age) % PERIOD
            new, old = numerators[j], numerators[(j + 1) % PERIOD]
            length = iv.sqrt(_squared_distance(new, old))
            distance = iv.mpf(_squared_distance(numerators[head], new)) / SCALE**2
            coefficient = q**age * iv.exp(-distance / 2) / (1000 * length)
            for k in range(4):
                field[k] += coefficient * (int(new[k]) - int(old[k]))
        vectors.extend(field)
    return vectors


@pytest.fixture(scope="module")
def vector_fields():
    original_dps = iv.dps
    try:
        iv.dps = 50
        yield [_interval_vector(n) for n in NUMERATORS]
    finally:
        iv.dps = original_dps


def _to_interval(value):
    return iv.mpf(value.numerator) / value.denominator


@pytest.mark.parametrize(
    "group", CERTIFICATES["groups"], ids=lambda g: str(g["bounds"])
)
def test_every_gain_requires_both_force_signs_in_each_distance_group(
    group, vector_fields
):
    shape = group["shape"]
    numerators = NUMERATORS[shape]
    matrix = integer_force_matrix(numerators)
    lo, hi = map(Fraction, group["bounds"])
    inside, outside = [], []
    for e, (i, j) in enumerate(EDGES):
        distance = Fraction(_squared_distance(numerators[i], numerators[j]), SCALE**2)
        (inside if lo < distance < hi else outside).append(e)
    assert inside
    target = [
        int(entry) for entry in (np.roll(numerators, 1, axis=0) - numerators).flat
    ]
    for y, (gain_sign, force_sign) in zip(
        _complete_duals(matrix, outside, group),
        CERTIFICATES["gain_and_value_signs"],
        strict=True,
    ):
        # Multiplying by SCALE * 2**9 does not affect the column signs.
        assert all(_dot(y, (int(x) for x in matrix[:, e])) == 0 for e in outside)
        assert all(_dot(y, (int(x) for x in matrix[:, e])) > 0 for e in inside)
        residual_floor = Fraction((17, 46)[shape], 10**7)
        assert force_sign * _dot(y, target) > residual_floor * SCALE * sum(map(abs, y))
        vector_dot = _dot([_to_interval(value) for value in y], vector_fields[shape])
        assert (force_sign * gain_sign * vector_dot).b < 0


def test_distance_groups_are_disjoint_on_each_orbit():
    for shape, count in enumerate([3, 2]):
        bounds = sorted(
            g["bounds"] for g in CERTIFICATES["groups"] if g["shape"] == shape
        )
        assert len(bounds) == count
        assert all(a < b for a, b in bounds)
        assert all(
            b < c for (_, b), (c, _) in zip(bounds[:-1], bounds[1:], strict=True)
        )
