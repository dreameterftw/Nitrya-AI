from __future__ import annotations

import warnings
import os

import numpy as np


def lift_to_3d(pose_2d: list[np.ndarray | None]) -> list[np.ndarray | None]:
    """
    Lift 2D keypoints into a 3D sequence.

    Phase 5 can route WHAM to Modal by setting USE_REMOTE_GPU=true. The local
    fallback stays available for cheap development iteration.
    """
    if os.getenv("USE_REMOTE_GPU", "").lower() in {"1", "true", "yes"}:
        from .wham_modal import lift_to_3d_with_modal

        return lift_to_3d_with_modal(pose_2d)

    warnings.warn(
        "Using planar z=0 lift fallback. Replace with WHAM output before judging "
        "Phase 1 acceptance.",
        RuntimeWarning,
        stacklevel=2,
    )

    lifted: list[np.ndarray | None] = []
    for frame in pose_2d:
        if frame is None:
            lifted.append(None)
            continue
        xy = np.asarray(frame, dtype=float)
        z = np.zeros((xy.shape[0], 1), dtype=float)
        lifted.append(np.concatenate([xy, z], axis=1))
    return lifted
