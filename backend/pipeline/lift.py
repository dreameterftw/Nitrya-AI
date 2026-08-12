from __future__ import annotations

import warnings

import numpy as np


def lift_to_3d(pose_2d: list[np.ndarray | None]) -> list[np.ndarray | None]:
    """
    Lift 2D keypoints into a 3D sequence.

    Phase 1 development uses WHAM manually in Colab for real 3D lifting. Until the
    WHAM batch output is wired back into this package, this local fallback preserves
    the pipeline contract by placing 2D joints on z=0. Do not treat fallback scores
    as passing the Phase 1 exit gate.
    """
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
