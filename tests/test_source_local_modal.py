from __future__ import annotations

import numpy as np

from emergenz_knoten.local_mediator import LocalMediatorGrid, TelegraphMediator
from emergenz_knoten.source_local_modal import telegraph_spatial_mode_reductions


def test_modal_reductions_preserve_stable_complete_telegraph_blocks() -> None:
    reductions = telegraph_spatial_mode_reductions(
        LocalMediatorGrid(0.25, 0.01, 12, 18),
        TelegraphMediator(0.5, 0.1, 0.1),
        readout_position=2.5,
        orders=(8, 16, 32),
    )
    assert tuple(reductions) == (8, 16, 32)
    for order, channel in reductions.items():
        assert channel.order == order
        assert np.max(np.abs(np.linalg.eigvals(channel.transition))) < 1.0


def test_modal_reductions_are_nested_and_source_readout_informed() -> None:
    reductions = telegraph_spatial_mode_reductions(
        LocalMediatorGrid(0.25, 0.01, 12, 18),
        TelegraphMediator(0.5, 0.1, 0.1),
        readout_position=2.5,
        orders=(8, 16),
    )
    assert np.allclose(
        reductions[8].transition,
        reductions[16].transition[:8, :8],
    )
    assert np.allclose(reductions[8].source, reductions[16].source[:8])
    assert np.allclose(reductions[8].readout, reductions[16].readout[:8])
