"""Independent checks of the observables used in Paper I."""
import importlib.util
from pathlib import Path

import numpy as np
import pytest

spec = importlib.util.spec_from_file_location("paper_i_evidence", Path(__file__).with_name("finalize_evidence.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@pytest.mark.parametrize("alpha,horizon,gain", [(0.01,600,0.0), (0.01,600,0.18289241496325967), (0.01,600,0.4322911626404318), (0.08,17,0.3)])
def test_fifo_impulse_matches_independent_frequency_integral(alpha,horizon,gain):
    impulse = module.linear_energies(alpha,horizon,gain)
    frequency = module.spectral_energies(alpha,horizon,gain)
    np.testing.assert_allclose(impulse,frequency,rtol=1e-7)


def test_horizon_one_has_no_cloud_or_relative_radius():
    np.testing.assert_allclose(module.linear_energies(0.1,1,0.4,100),0,atol=1e-13)


def test_random_walk_cloud_variance_from_pairwise_increment_distances():
    alpha,horizon = 0.1,25
    weights = alpha * (1-alpha) ** np.arange(horizon)
    weights /= weights.sum()
    distance = np.abs(np.arange(horizon)[:,None]-np.arange(horizon)[None,:])
    cloud = 0.5 * np.sum(weights[:,None] * weights[None,:] * distance)
    cumulative = np.cumsum(weights)
    relative = np.sum((1-cumulative) ** 2)
    np.testing.assert_allclose(module.linear_energies(alpha,horizon,0.0,1000),[relative,cloud],rtol=1e-10)


def test_infinite_horizon_cloud_and_position_are_distinct():
    alpha,gain=0.1,0.3
    q=1-alpha
    relative=q*q/(1-(q*(1-gain))**2)
    np.testing.assert_allclose(module.linear_energies(alpha,500,gain,4000),[relative,relative/q],rtol=1e-10)


def test_terminal_selection_excludes_sparse_history():
    assert module.terminal_start([1,3,17,*range(1000,1200)]) == 3
    with pytest.raises(ValueError):
        module.terminal_start([1,3,3])
