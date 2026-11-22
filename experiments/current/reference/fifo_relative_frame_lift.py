"""Finite-window path comparison, not a FIFO update or a dynamical connector."""

import numpy as np
from scipy.spatial.transform import Rotation


_CUT_TOL = 1e-12


def _lift_end(frames):
    poses = np.asarray(frames, dtype=float)
    if poses.ndim != 3 or poses.shape[1:] != (3, 3) or poses.shape[0] < 2:
        raise ValueError("at least two ordered 3D frames are required")
    if (
        not np.isfinite(poses).all()
        or not np.allclose(
            poses.transpose(0, 2, 1) @ poses, np.eye(3), atol=1e-10, rtol=0
        )
        or np.any(np.linalg.det(poses) <= 0)
    ):
        raise ValueError("frames must be proper orthogonal matrices")
    quats = Rotation.from_matrix(poses[0].T @ poses).as_quat()
    lift = np.array([0.0, 0.0, 0.0, 1.0])
    for quat in quats[1:]:
        overlap = lift @ quat
        if abs(overlap) <= _CUT_TOL:
            raise ValueError("an internal rotation step is ambiguous at 180 degrees")
        lift = quat if overlap > 0 else -quat
    return lift


def relative_frame_sign(frames_a, frames_b):
    """Lift from each initial pose and close the endpoints along the short arc.

    Samples must be chronological and interpreted with the same body-axis labels.
    The shortest paths are a convention unless actual motion is resolved by the samples.
    """
    overlap = _lift_end(frames_a) @ _lift_end(frames_b)
    if abs(overlap) <= _CUT_TOL:
        raise ValueError("the endpoint join is ambiguous at 180 degrees")
    return 1 if overlap > 0 else -1
