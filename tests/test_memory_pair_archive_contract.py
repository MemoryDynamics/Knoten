"""Archive metadata and constructed paths only; no target run or replay."""

import hashlib
import json

import numpy as np
import pytest

from emergenz_knoten.core import update_history
from experiments.current.reference import memory_pair_archive_inventory as audit


def _history_at(initial, positions, step):
    inserted = min(step, len(initial))
    newest = positions[step - inserted + 1 : step + 1][::-1]
    return np.concatenate((newest, initial[: len(initial) - inserted]))


def _gaussian_gradient(displacement):
    return -displacement * np.exp(-np.sum(displacement**2, axis=-1))[..., None] * 2


def test_inventory_visits_all_rows_and_records_bytes_without_replaying(tmp_path):
    path = tmp_path / "summary.json"
    payload = {"rows": [{"diagnostic": [1]}, {"diagnostic": list(range(13))}]}
    path.write_bytes((json.dumps(payload) + "\r\n").encode("utf-8"))
    record = audit.describe(path)
    assert record["longest_lists"][0] == {"path": "$.rows[1].diagnostic", "length": 13}
    assert record["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert record["row_count"] == 2
    path.write_bytes((json.dumps(payload) + "\n").encode("utf-8"))
    normalized = audit.describe(path)
    assert record["sha256"] != normalized["sha256"]
    assert record["sha256_utf8_lf"] == normalized["sha256_utf8_lf"]


def test_inventory_npz_groups_keep_axis_shapes_not_physical_labels(tmp_path):
    path = tmp_path / "branches.npz"
    np.savez(path, branches=np.zeros((7, 2, 3)), steps=np.arange(7))
    record = audit.describe(path)
    assert record["array_count"] == 2
    assert {tuple(group["shape"]) for group in record["array_groups"]} == {
        (7,),
        (7, 2, 3),
    }
    assert "two_nodes" not in record


def test_missing_archive_and_object_array_fail_closed(tmp_path):
    with pytest.raises(FileNotFoundError):
        audit.describe(tmp_path / "missing.npz")
    path = tmp_path / "object.npz"
    np.savez(path, unsafe=np.array([{"x": 1}], dtype=object))
    with pytest.raises(ValueError, match="allow_pickle=False"):
        audit.describe(path)


@pytest.mark.parametrize("horizon", [1, 3, 5])
def test_dense_point_archive_reconstructs_every_fifo_slot(horizon):
    initial = np.arange(horizon * 3, dtype=float).reshape(horizon, 3) / 7
    positions = np.sin(np.arange(33).reshape(11, 3))
    # The initial current point need not equal the newest initial deposit.
    positions[0] = [10, 11, 12]
    history = initial.copy()
    for step in range(len(positions)):
        if step:
            history, filled = update_history(history, positions[step], horizon)
            assert filled == horizon
        np.testing.assert_array_equal(_history_at(initial, positions, step), history)


def test_decimation_loses_a_lag_even_when_sampled_positions_are_identical():
    first = np.zeros((5, 1))
    second = first.copy()
    second[1] = 0.4
    np.testing.assert_array_equal(first[::2], second[::2])
    initial = np.zeros((3, 1))
    history_a = _history_at(initial, first, 2)
    history_b = _history_at(initial, second, 2)
    target = np.array([1.0])
    weights = np.array([0.5, 0.3, 0.2])
    response_a = weights @ _gaussian_gradient(target - history_a)
    response_b = weights @ _gaussian_gradient(target - history_b)
    assert abs(response_a[0] - response_b[0]) > 0.01


def test_relative_paths_do_not_determine_lag_response_under_common_motion():
    base = np.zeros((5, 2, 1))
    base[:, 0, 0] = 1
    moving = base + (0.1 * np.arange(5))[:, None, None]
    np.testing.assert_allclose(base[:, 0] - base[:, 1], moving[:, 0] - moving[:, 1])
    static_lag = base[1:, 0] - base[:-1, 1]
    moving_lag = moving[1:, 0] - moving[:-1, 1]
    assert (
        np.max(abs(_gaussian_gradient(static_lag) - _gaussian_gradient(moving_lag)))
        > 0.05
    )
    translated = base + 4.0
    np.testing.assert_allclose(
        _gaussian_gradient(static_lag),
        _gaussian_gradient(translated[1:, 0] - translated[:-1, 1]),
    )


def test_finite_window_reverse_lag_requires_an_endpoint_term():
    n = np.arange(10)
    first = (0.2 * n + 0.05 * n**2)[:, None]
    second = np.sin(0.4 * n)[:, None]
    start, stop, lag = 3, 8, 2
    direct = _gaussian_gradient(first[start - lag : stop - lag] - second[start:stop])
    negative_lag = _gaussian_gradient(first[:-lag] - second[lag:])
    shifted = negative_lag[start - lag : stop - lag]
    np.testing.assert_array_equal(direct, shifted)
    boundary = (
        np.sum(negative_lag[start - lag : start], axis=0)
        - np.sum(negative_lag[stop - lag : stop], axis=0)
    ) / (stop - start)
    np.testing.assert_allclose(
        np.mean(direct, axis=0),
        np.mean(negative_lag[start:stop], axis=0) + boundary,
        atol=1e-15,
    )
    assert abs(boundary[0]) > 0.01
